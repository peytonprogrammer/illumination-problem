"""Monteil's slit room, its scalings and thickenings; driver helpers."""
import subprocess
import tempfile
from pathlib import Path

import rooms45 as R
import slit45 as S

HERE = Path(__file__).resolve().parent

# Monteil, Transparent blocking, page 5, read from the PDF vector data (8 PDF units per lattice
# unit; y flipped so that y points up).  Counter-clockwise.
P0 = [(3, 1), (4, 1), (4, 0), (5, 1), (5, 2), (6, 2), (5, 3), (4, 3), (4, 4), (3, 3), (2, 4), (2, 3),
      (1, 3), (0, 2), (1, 2), (1, 1), (2, 0), (2, 1)]
SLIT0 = ((3, 1), (3, 2))          # foot on the bottom wall, tip inside
MARKS0 = ((2, 2), (4, 2))         # red, green


def clean(poly):
    """Drop repeated and collinear vertices."""
    out = []
    for p in poly:
        if out and out[-1] == p:
            continue
        out.append(p)
    if out[0] == out[-1]:
        out.pop()
    changed = True
    while changed:
        changed = False
        m = len(out)
        for k in range(m):
            a, b, c = out[k - 1], out[k], out[(k + 1) % m]
            if (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0]) == 0:
                out.pop(k)
                changed = True
                break
    return out


def area2(poly):
    return sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1] for i in range(len(poly)))


def diag_ok(poly):
    """All diagonal edges on lines x+y, x-y even (canonical45 tiling)."""
    m = len(poly)
    for k in range(m):
        a, b = poly[k], poly[(k + 1) % m]
        if a[0] != b[0] and a[1] != b[1] and (a[0] + a[1]) % 2:
            return False
    return True


def unit_edges(a, b):
    dx = (b[0] > a[0]) - (b[0] < a[0])
    dy = (b[1] > a[1]) - (b[1] < a[1])
    out = []
    p = a
    while p != b:
        q = (p[0] + dx, p[1] + dy)
        out.append((p, q))
        p = q
    return out


def obstacle(k, xl, xr, top, end):
    """Thick wall standing on y = k: box [xl,xr] x [k,top], end 'flat', 'up' (/), 'down' (\\), 'roof'.
    Returns a ccw polygon or None."""
    w = xr - xl
    h = top - k
    if end == 'flat':
        poly = [(xl, k), (xr, k), (xr, top), (xl, top)]
    elif end == 'up':      # top face rises to the right: from (xl, top - w) to (xr, top)
        if w <= h:
            poly = [(xl, k), (xr, k), (xr, top), (xl, top - w)]
        else:
            poly = [(xr - h, k), (xr, k), (xr, top)]
    elif end == 'down':    # top face falls to the right: from (xl, top) to (xr, top - w)
        if w <= h:
            poly = [(xl, k), (xr, k), (xr, top - w), (xl, top)]
        else:
            poly = [(xl, k), (xl + h, k), (xl, top)]
    elif end == 'roof':
        if w % 2:
            return None
        xm = (xl + xr) // 2
        hw = w // 2
        if hw <= h:
            poly = [(xl, k), (xr, k), (xr, top - hw), (xm, top), (xl, top - hw)]
        else:
            poly = [(xm - h, k), (xm + h, k), (xm, top)]
    else:
        raise ValueError(end)
    return clean(poly)


def tiles_in(poly, c):
    return R.tiles_from_polygon([(c * x, c * y) for x, y in poly])


def make_room(k, obs=None, slit=True):
    """Scaled room; with obs (ccw polygon) subtracted; slit kept only if slit=True and obs is None.
    Returns dict with tiles (canonical45, scale c), c, slit edges (scaled), marks (scaled, room units)."""
    poly = [(k * x, k * y) for x, y in P0]
    c = 1 if (diag_ok(poly) and (obs is None or diag_ok(obs))) else 2
    tiles = set(tiles_in(poly, c))
    if obs is not None:
        ot = set(tiles_in(obs, c))
        if not ot <= tiles:
            return None
        tiles -= ot
    sl = []
    if obs is None and slit:
        a, b = SLIT0
        sl = unit_edges((c * k * a[0], c * k * a[1]), (c * k * b[0], c * k * b[1]))
    marks = tuple((k * x, k * y) for x, y in MARKS0)
    return dict(k=k, c=c, tiles=sorted(tiles), slit=sl, marks=marks, poly=poly, obs=obs)


def connected(tiles):
    ts = set(tiles)
    own = {}
    for t in ts:
        v = R.tile_verts(*t)
        for i in range(3):
            own.setdefault(frozenset((v[i], v[(i + 1) % 3])), []).append(t)
    adj = {t: [] for t in ts}
    for o in own.values():
        if len(o) == 2:
            adj[o[0]].append(o[1])
            adj[o[1]].append(o[0])
    st = [next(iter(ts))]
    seen = {st[0]}
    while st:
        x = st.pop()
        for y in adj[x]:
            if y not in seen:
                seen.add(y)
                st.append(y)
    return len(seen) == len(ts)


def analyse(room, bound, workdir):
    """Strict simplicity, W, origami, all-pairs shooting, witness replay."""
    c = room['c']
    tiles = room['tiles']
    out = dict(k=room['k'], c=c, N=len(tiles))
    b = R.boundary(tiles)
    out['simple'] = b['simple'] and connected(tiles)
    cyc = b['cycle'][:-1]
    poly = clean([(x, y) for x, y in cyc])
    if room['slit']:
        # the slit foot is a flat point of the outer cycle: corners = polygon corners + foot + tip
        foot, tip = room['slit'][0][0], room['slit'][-1][1]
        out['W_outer'] = len(poly)
        out['W'] = len(poly) + 2          # foot and tip become corners
    else:
        out['W'] = len(poly)
    out['W_cycle'] = b['W_cycle']
    o = S.build(tiles, room['slit'])
    marks = [(c * x, c * y) for x, y in room['marks']]
    for m in marks:
        assert o['ptype'].get(m) == 'I', ('mark not interior', m)
    elig = [p for p in o['pts'] if o['ptype'][p] == 'I' and p[0] % c == 0 and p[1] % c == 0]
    out['n_points'] = len(elig)
    fn = Path(workdir) / 'origami.txt'
    S.write_origami(o, fn, elig, marks[0], marks[1])
    r = subprocess.run([str(HERE / 'shootall'), str(bound), str(fn)], capture_output=True, text=True, check=True).stdout.splitlines()
    kv = dict(x.split('=') for x in r[0].split())
    out.update(pairs=int(kv['pairs']), lit=int(kv['lit']), unlit=int(kv['unlit']), bound=bound, lastsum=int(kv['lastsum']))
    out['unlit_pairs'] = [(elig[int(l.split()[1])], elig[int(l.split()[2])]) for l in r[1:]]
    # witness replay in the plane (independent tracer); segments from the boundary cycle + slit
    segs = [(poly[i], poly[(i + 1) % len(poly)]) for i in range(len(poly))]
    corners = set(poly)
    if room['slit']:
        segs.append((room['slit'][0][0], room['slit'][-1][1]))
        corners |= {room['slit'][0][0], room['slit'][-1][1]}
    out['poly'] = poly
    for key in ('first', 'best'):
        if kv[key] == 'none':
            out[key] = None
            continue
        dx, dy, m = map(int, kv[key].split(','))
        ok, nrefl, hits = S.trace(segs, corners, marks[0], (dx, dy), m, marks[1], record=True)
        L2 = m * m * (dx * dx + dy * dy)
        out[key] = dict(dir=(dx, dy), m=m, len2_room=L2 / (c * c), replay=ok, refl=nrefl,
                        walls=sorted({tuple(map(tuple, segs[i])) for _, i in hits}), hits=[(str(P[0] / c), str(P[1] / c), i) for P, i in hits])
    out['orbit_line'] = S.orbit_line(o, marks[0], marks[1]) if o['nsq'] <= 255 else None
    out['nsq'] = o['nsq']
    out['segs'] = segs
    return out
