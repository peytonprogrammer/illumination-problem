"""d55 relaxed orthogonal lattice rooms: model, enumeration, unfolding for orbitr.

A room is (cells, slits): cells is a set of unit cells (i, j) = [i, i+1] x [j, j+1];
slits is a set of interior unit edges (both side cells present) that are walls.
An edge is a sorted pair of lattice points.

Valid room: the interior (open cells, open non-wall edges between two cells,
lattice points whose four cells are present with no wall on the four edges at
the point) is connected and simply connected.  For this open surface built from
open cells, chi = F - E + V, and connected + chi == 1 <=> simply connected.

Sectors.  At a lattice point the present cells are joined across an edge ray at
the point when both cells are present and the edge is not a wall.  Each sector
(component) is one point of the room's abstract closure:
    'int'  4 cells, cyclically joined       interior point, regular
    1      path of 1 cell                    convex corner (cone pi/2, stops paths)
    2      path of 2 cells                   flat wall point (regular, reflects)
    3      path of 3 cells                   reflex corner (stops)
    4      path of 4 cells                   slit tip, angle 2 pi (stops; 4 pi in the double)
A pinch is a point with two 1-sectors (two diagonal cells).  A slit foot on a flat
wall is two 1-sectors; a slit foot at a reflex corner is a 1-sector and a 2-sector.
"""
from itertools import combinations

SYMS = [lambda x, y: (x, y), lambda x, y: (-x, y), lambda x, y: (x, -y), lambda x, y: (-x, -y),
        lambda x, y: (y, x), lambda x, y: (-y, x), lambda x, y: (y, -x), lambda x, y: (-y, -x)]


def ek(p, q):
    return (p, q) if p < q else (q, p)


def around(p):
    x, y = p
    # NE, NW, SW, SE and the rays between consecutive cells: N, W, S, E
    cells = [(x, y), (x - 1, y), (x - 1, y - 1), (x, y - 1)]
    rays = [ek((x, y), (x, y + 1)), ek((x - 1, y), (x, y)), ek((x, y - 1), (x, y)), ek((x, y), (x + 1, y))]
    return cells, rays          # ray k lies between cells[k] and cells[(k + 1) % 4]


def sectors(cells, slits, p):
    """List of (type, [cells]) at lattice point p."""
    cs, rays = around(p)
    pres = [c in cells for c in cs]
    opn = [pres[k] and pres[(k + 1) % 4] and rays[k] not in slits for k in range(4)]
    if all(opn):
        return [('int', cs)]
    out = []
    seen = [False] * 4
    for k in range(4):
        if not pres[k] or seen[k]:
            continue
        # walk back to the start of the path containing k
        s = k
        while opn[(s - 1) % 4] and pres[(s - 1) % 4] and (s - 1) % 4 != k:
            s = (s - 1) % 4
        run = [s]
        seen[s] = True
        cur = s
        while opn[cur]:
            cur = (cur + 1) % 4
            if seen[cur]:
                break
            run.append(cur)
            seen[cur] = True
        out.append((len(run), [cs[j] for j in run]))
    return out


def lattice_points(cells):
    pts = set()
    for (i, j) in cells:
        pts |= {(i, j), (i + 1, j), (i, j + 1), (i + 1, j + 1)}
    return pts


def sector_table(cells, slits):
    """{point: [(type, cells)]} for every lattice point of the room."""
    return {p: sectors(cells, slits, p) for p in lattice_points(cells)}


def interior_points(cells, slits, tab=None):
    tab = tab or sector_table(cells, slits)
    return sorted(p for p, s in tab.items() if s[0][0] == 'int')


def open_edges(cells, slits):
    out = []
    for (i, j) in cells:
        for nb, e in (((i + 1, j), ek((i + 1, j), (i + 1, j + 1))), ((i, j + 1), ek((i, j + 1), (i + 1, j + 1)))):
            if nb in cells and e not in slits:
                out.append(((i, j), nb))
    return out


def is_valid(cells, slits, tab=None):
    tab = tab or sector_table(cells, slits)
    oe = open_edges(cells, slits)
    V = sum(1 for s in tab.values() if s[0][0] == 'int')
    if len(cells) - len(oe) + V != 1:
        return False
    adj = {c: [] for c in cells}
    for a, b in oe:
        adj[a].append(b)
        adj[b].append(a)
    start = next(iter(cells))
    seen = {start}
    st = [start]
    while st:
        u = st.pop()
        for w in adj[u]:
            if w not in seen:
                seen.add(w)
                st.append(w)
    return len(seen) == len(cells)


def boundary_edges(cells, slits):
    out = set(slits)
    for (i, j) in cells:
        for nb, e in (((i + 1, j), ek((i + 1, j), (i + 1, j + 1))), ((i - 1, j), ek((i, j), (i, j + 1))),
                      ((i, j + 1), ek((i, j + 1), (i + 1, j + 1))), ((i, j - 1), ek((i, j), (i + 1, j)))):
            if nb not in cells:
                out.add(e)
    return out


def wall_counts(cells, slits, nslits, tab=None):
    """W_walk: turning visits of the boundary walk (sides; slit = 2 sides, pinch = 2 corners).
    W_slit1 = W_walk - nslits (slit as 1 side, its foot still splits the wall it stands on).
    W_seg: maximal straight runs of wall edges as point sets (slit merged with collinear walls,
    walls through a pinch or a T-foot not split)."""
    tab = tab or sector_table(cells, slits)
    walk = sum(1 for s in tab.values() for (t, _) in s if t in (1, 3, 4))
    be = boundary_edges(cells, slits)
    seg = 0
    for (p, q) in be:
        if p[1] == q[1]:                       # horizontal edge p -> q = p + (1, 0)
            prev = ek((p[0] - 1, p[1]), p)
        else:
            prev = ek((p[0], p[1] - 1), p)
        if prev not in be:
            seg += 1
    return walk, walk - nslits, seg


def reflex_count(tab):
    return sum(1 for s in tab.values() for (t, _) in s if t == 3)


def n_pinches(cells, slits, tab=None):
    tab = tab or sector_table(cells, slits)
    return sum(1 for p, s in tab.items() if len(s) == 2 and s[0][0] == 1 and s[1][0] == 1
               and not any(e in slits for e in around(p)[1]))


# ---------------------------------------------------------------- canonical form

def transform(cells, slits, f):
    tc = [f(i, j) for (i, j) in cells]
    # cell (i, j) maps to the cell whose min corner is min over images of its corners
    newcells = []
    for (i, j) in cells:
        cs = [f(i + u, j + v) for u in (0, 1) for v in (0, 1)]
        newcells.append((min(c[0] for c in cs), min(c[1] for c in cs)))
    newslits = [ek(f(*p), f(*q)) for (p, q) in slits]
    mx = min(c[0] for c in newcells)
    my = min(c[1] for c in newcells)
    nc = tuple(sorted((x - mx, y - my) for (x, y) in newcells))
    ns = tuple(sorted(ek((p[0] - mx, p[1] - my), (q[0] - mx, q[1] - my)) for (p, q) in newslits))
    return nc, ns


def canon(cells, slits=()):
    return min(transform(cells, slits, f) for f in SYMS)


# ---------------------------------------------------------------- enumeration

def free_polyominoes(amax):
    """Yield (area, canonical cell tuple) for every free polyomino (edge-connected) of area <= amax."""
    level = {canon({(0, 0)})[0]}
    for a in range(1, amax + 1):
        for c in sorted(level):
            yield a, c
        if a == amax:
            break
        nxt = set()
        for c in level:
            cs = set(c)
            for (i, j) in c:
                for nb in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                    if nb not in cs:
                        nxt.add(canon(cs | {nb})[0])
        level = nxt


def candidate_slits(cells, tab, lmax):
    """Straight slits: foot at a non-interior lattice point, then 1..lmax unit edges whose far
    end points are interior points of the slit-free room.  Returned as (foot, tip, edges)."""
    out = []
    for p, s in tab.items():
        if s[0][0] == 'int':
            continue
        for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            edges = []
            cur = p
            for L in range(1, lmax + 1):
                nxt = (cur[0] + d[0], cur[1] + d[1])
                if nxt not in tab or tab[nxt][0][0] != 'int':
                    break
                e = ek(cur, nxt)
                # the edge must have cells on both sides (true: nxt is interior)
                edges.append(e)
                out.append((p, nxt, tuple(edges)))
                cur = nxt
    return out


def slit_configs(cells, tab, smax, lmax, min_interior=0):
    """Disjoint sets of at most smax candidate slits.  A slit of length L removes exactly L interior
    points (its tip and inner points), so configurations leaving fewer than min_interior are skipped."""
    v0 = sum(1 for s in tab.values() if s[0][0] == 'int')
    cand = [c for c in candidate_slits(cells, tab, lmax) if v0 - len(c[2]) >= min_interior]
    pts = []
    for (foot, tip, edges) in cand:
        ps = {foot}
        for e in edges:
            ps |= set(e)
        pts.append(ps)
    yield ()
    for k in range(1, smax + 1):
        for combo in combinations(range(len(cand)), k):
            if v0 - sum(len(cand[i][2]) for i in combo) < min_interior:
                continue
            if any(pts[a] & pts[b] for a, b in combinations(combo, 2)):
                continue
            yield tuple(cand[i] for i in combo)


# ---------------------------------------------------------------- unfolding for orbitr

SHEETS = ((1, 1), (-1, 1), (1, -1), (-1, -1))


def sector_type_of(tab, p, cell):
    for t, cs in tab[p]:
        if cell in cs:
            return t
    raise KeyError((p, cell))


def unfolding(cells, slits, sources, tab=None):
    """4-fold unfolding as in d9 orbit.py, with slit edges as walls and decoration by sector."""
    tab = tab or sector_table(cells, slits)
    cl = sorted(cells)
    sq = [(c, s) for c in cl for s in range(4)]
    ix = {t: k for k, t in enumerate(sq)}
    sid = {p: k for k, p in enumerate(sources)}
    h, v, dec = [], [], []
    for (c, s) in sq:
        (i, j), (sx, sy) = c, SHEETS[s]
        nb = (i + sx, j)
        e = ek((i + 1, j), (i + 1, j + 1)) if sx > 0 else ek((i, j), (i, j + 1))
        h.append(ix[(nb, s)] if nb in cells and e not in slits else ix[(c, SHEETS.index((-sx, sy)))])
        nb = (i, j + sy)
        e = ek((i, j + 1), (i + 1, j + 1)) if sy > 0 else ek((i, j), (i + 1, j))
        v.append(ix[(nb, s)] if nb in cells and e not in slits else ix[(c, SHEETS.index((sx, -sy)))])
        lab = (i + (1 if sx < 0 else 0), j + (1 if sy < 0 else 0))
        t = sector_type_of(tab, lab, c)
        if t == 'int':
            dec.append(sid.get(lab, -2))
        elif t == 2:
            assert lab not in sid
            dec.append(-2)
        else:
            assert lab not in sid
            dec.append(-1)
    return h, v, dec


def problem_line(cells, slits, sources, tab=None):
    h, v, dec = unfolding(cells, slits, sources, tab)
    return '%d %d %s %s %s' % (len(h), len(sources), ' '.join(map(str, h)), ' '.join(map(str, v)),
                               ' '.join(map(str, dec)))


def parse_result(line):
    f = line.split()
    status, nst, nun = f[0], int(f[1]), int(f[2])
    rest = list(map(int, f[3:]))
    pairs = [(rest[2 * k], rest[2 * k + 1]) for k in range(nun)]
    return status, nst, pairs


def room_str(cells, slits):
    return 'C=' + ';'.join('%d,%d' % c for c in sorted(cells)) + ' S=' + ';'.join(
        '%d,%d-%d,%d' % (p[0], p[1], q[0], q[1]) for (p, q) in sorted(slits))


def parse_room(s):
    c, sl = s.split(' S=')
    cells = {tuple(map(int, x.split(','))) for x in c[2:].split(';')}
    slits = set()
    if sl.strip():
        for x in sl.strip().split(';'):
            a, b = x.split('-')
            slits.add(ek(tuple(map(int, a.split(','))), tuple(map(int, b.split(',')))))
    return cells, slits


def picture(cells, slits, marks=()):
    xs = [c[0] for c in cells]
    ys = [c[1] for c in cells]
    rows = []
    for y in range(max(ys) + 1, min(ys) - 1, -1):
        r = ''
        for x in range(min(xs), max(xs) + 2):
            p = (x, y)
            r += '*' if p in marks else ('+' if p in lattice_points(cells) else ' ')
            e = ek(p, (x + 1, y))
            onb = (x, y) in cells or (x, y - 1) in cells
            if e in slits:
                r += '='
            elif ((x, y) in cells) != ((x, y - 1) in cells):
                r += '-'
            else:
                r += ' '
        rows.append(r)
        if y > min(ys):
            r = ''
            for x in range(min(xs), max(xs) + 2):
                e = ek((x, y - 1), (x, y))
                if e in slits:
                    r += 'H'
                elif ((x - 1, y - 1) in cells) != ((x, y - 1) in cells):
                    r += '|'
                else:
                    r += ' '
                r += '#' if (x, y - 1) in cells else ' '
            rows.append(r)
    return '\n'.join(rows)
