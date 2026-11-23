"""Monteil's pinched room (Transparent blocking, slide 4), its scalings and pinch resolutions.

Coordinates: lattice units, y up.  Read from the PDF stroke path (8 PDF units per
lattice unit, offset (0.977, 0.965)); see monteil_p4.trace.  The boundary walk is
clockwise and visits the pinch Q = (4, 4) twice.
"""
import subprocess
from pathlib import Path

import rooms45 as R
import slit45 as S

HERE = Path(__file__).resolve().parent

P0 = [(1, 4), (1, 5), (2, 6), (2, 5), (3, 5), (4, 4), (3, 4), (3, 3), (4, 3), (4, 4), (5, 3), (5, 2),
      (6, 2), (5, 1), (4, 1), (4, 0), (3, 1), (3, 2), (2, 2), (2, 3), (1, 3), (0, 4)]
Q0 = (4, 4)
MARKS0 = ((2, 4), (4, 2))       # red S, green T


def clean(poly):
    """Drop repeated and collinear vertices of a closed walk."""
    out = []
    for p in poly:
        if not out or out[-1] != p:
            out.append(p)
    if out[0] == out[-1]:
        out.pop()
    changed = True
    while changed:
        changed = False
        m = len(out)
        for i in range(m):
            a, b, c = out[i - 1], out[i], out[(i + 1) % m]
            if (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0]) == 0:
                out.pop(i)
                changed = True
                break
    return out


def tiles_of(poly):
    return set(R.tiles_from_polygon(poly))


def scaled(k):
    return [(k * x, k * y) for x, y in P0]


def base_tiles(k):
    """Tiles of the scaled pinched room.  point_in_polygon on tile centroids handles the pinch."""
    return tiles_of(scaled(k))


def mirror_tile(t):
    """Reflection (x, y) -> (y, x): swaps the two wedges and S <-> T."""
    return R.tri_to_ijh([(y, x) for x, y in R.tile_verts(*t)])


def wedge_tiles(k):
    """R1: triangle (3k,4k) (4k,4k) (3k,5k) above the hole; R2 its mirror right of the hole."""
    r1 = tiles_of([(3 * k, 4 * k), (4 * k, 4 * k), (3 * k, 5 * k)])
    r2 = {mirror_tile(t) for t in r1}
    tip1 = [t for t in r1 if (4 * k, 4 * k) in R.tile_verts(*t)]
    assert len(tip1) == 1
    return r1, r2, tip1[0], mirror_tile(tip1[0])


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


def check(tiles, marks):
    """Strict simplicity, W, marks interior.  Returns (status, W, poly)."""
    if not tiles or not connected(tiles):
        return 'disconnected', None, None
    b = R.boundary(tiles)
    if not b['simple']:
        return 'not-simple', b['W_cycle'], None
    poly = clean(b['cycle'][:-1])
    if any(m not in b['interior'] for m in marks):
        return 'mark-not-interior', len(poly), poly
    return 'ok', len(poly), poly


def shoot(o, elig, Sm, Tm, bound, fn):
    S.write_origami(o, fn, elig, Sm, Tm)
    r = subprocess.run([str(HERE / 'shootall'), str(bound), str(fn)], capture_output=True, text=True, check=True).stdout.splitlines()
    kv = dict(x.split('=') for x in r[0].split())
    unl = [(elig[int(l.split()[1])], elig[int(l.split()[2])]) for l in r[1:]]
    return kv, unl


def seg_dist2_num(P, D, Qp):
    """Squared distance from point Qp to the segment P + t D, t in [0, 1] (Fractions)."""
    w = (Qp[0] - P[0], Qp[1] - P[1])
    dd = D[0] * D[0] + D[1] * D[1]
    t = (w[0] * D[0] + w[1] * D[1]) / dd
    t = min(max(t, 0), 1)
    e = (w[0] - t * D[0], w[1] - t * D[1])
    return e[0] * e[0] + e[1] * e[1]


def analyse(tiles, marks, bound, workdir, Qp, orig_segs=None):
    """All-pairs shooting on the room; witnesses for the marks replayed in the plane."""
    tiles = sorted(tiles)
    st, W, poly = check(tiles, marks)
    out = dict(status=st, W=W, N=len(tiles))
    if st != 'ok':
        return out
    o = S.build(tiles)
    elig = [p for p in o['pts'] if o['ptype'][p] == 'I']
    out['n_points'] = len(elig)
    kv, unl = shoot(o, elig, marks[0], marks[1], bound, Path(workdir) / 'origami.txt')
    out.update(pairs=int(kv['pairs']), lit=int(kv['lit']), unlit=int(kv['unlit']), bound=bound, lastsum=int(kv['lastsum']))
    out['unlit_pairs'] = unl
    segs = [(poly[i], poly[(i + 1) % len(poly)]) for i in range(len(poly))]
    corners = set(poly)
    newwall = [not on_walls(s, orig_segs) for s in segs] if orig_segs else [False] * len(segs)
    out['poly'] = poly
    for key in ('first', 'best'):
        if kv[key] == 'none':
            out[key] = None
            continue
        dx, dy, m = map(int, kv[key].split(','))
        ok, nrefl, hits = S.trace(segs, corners, marks[0], (dx, dy), m, marks[1], record=True)
        faces = ''.join('N' if newwall[i] else 'o' for _, i in hits)
        dq = min_dist2_to(marks[0], marks[1], hits, Qp)
        out[key] = dict(dir=(dx, dy), m=m, len2=m * m * (dx * dx + dy * dy), replay=ok, refl=nrefl, faces=faces,
                        dQ2=str(dq))
        if key == 'best':
            out[key]['hits'] = [(str(P[0]), str(P[1])) for P, _ in hits]
    out['nsq'] = o['nsq']
    return out


def min_dist2_to(Sm, Tm, hits, Qp):
    """Minimum squared distance from the polyline S, reflection points, T to Qp."""
    from fractions import Fraction as Fr
    pts = [(Fr(Sm[0]), Fr(Sm[1]))] + [P for P, _ in hits] + [(Fr(Tm[0]), Fr(Tm[1]))]
    return min(seg_dist2_num(a, (b[0] - a[0], b[1] - a[1]), Qp) for a, b in zip(pts, pts[1:]))


def on_walls(s, orig_segs):
    """True if segment s lies inside one of the original wall segments."""
    (a, b) = s
    for (c, d) in orig_segs:
        e = (d[0] - c[0], d[1] - c[1])
        if all((p[0] - c[0]) * e[1] - (p[1] - c[1]) * e[0] == 0 for p in (a, b)):
            hi = e[0] * e[0] + e[1] * e[1]
            if all(0 <= (p[0] - c[0]) * e[0] + (p[1] - c[1]) * e[1] <= hi for p in (a, b)):
                return True
    return False


def orig_segs(k):
    P = scaled(k)
    return [(P[i], P[(i + 1) % len(P)]) for i in range(len(P))]
