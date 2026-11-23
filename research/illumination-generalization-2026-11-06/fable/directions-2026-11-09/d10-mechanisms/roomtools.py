"""Exact tools for ONE given orthogonal lattice room (no room search).

A room is a set of unit cells (i, j) = [i, i+1] x [j, j+1].  The class origin is an
interior or boundary lattice point `origin`; class a = origin + 2Z^2, b = a + (1, 0),
c = a + (1, 1), d = a + (0, 1).  The pillowcase tuple is (g_a, g_b, g_c, g_d) in the
conventions of d6-hurwitz-census/hurwitz.py (validated there on the 22-wall room).
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'd6-hurwitz-census'))
import d4_monodromy as d4                      # noqa: E402
from hurwitz import (mul, inv, ident, cycles, cycle_type, cycle_index, marked_orbit,  # noqa: E402
                     initial_pt)

NAMES = 'abcd'
OFFS = {(0, 0): 0, (1, 0): 1, (1, 1): 2, (0, 1): 3}


def cells_from_vertices(verts):
    return set(d4.squares_from_polygon(list(verts)))


def cells_from_rows(rows, x0=0, y_top=0):
    """rows: strings top to bottom, '#' = cell; first row has j = y_top."""
    out = set()
    for r, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch == '#':
                out.add((x0 + i, y_top - r))
    return out


def shifted(cells, origin):
    ox, oy = origin
    return sorted((i - ox, j - oy) for (i, j) in cells)


def room_tuple(cells, origin=(0, 0)):
    """Return (room, t) with t = (g_a, g_b, g_c, g_d); sheets are room.sheets."""
    room = d4.Room('room', 'square', shifted(cells, origin), [])
    g = room.gen
    t = (g[(0, 0)], inv(g[(1, 0)]), g[(1, 1)], inv(g[(0, 1)]))
    assert mul(mul(mul(t[0], t[1]), t[2]), t[3]) == ident(room.degree)
    return room, t


def status(cells, p):
    x, y = p
    k = sum(1 for c in ((x - 1, y - 1), (x, y - 1), (x - 1, y), (x, y)) if c in cells)
    return {0: 'outside', 1: 'convex', 2: 'smooth', 3: 'reflex', 4: 'interior'}[k]


def lattice_points(cells):
    pts = set()
    for (i, j) in cells:
        pts |= {(i, j), (i + 1, j), (i, j + 1), (i + 1, j + 1)}
    return sorted(pts)


def is_strictly_simple(cells):
    """Connected, simply connected, and no pinch vertex (two cells meeting only diagonally)."""
    cells = set(cells)
    start = next(iter(cells))
    seen = {start}
    st = [start]
    while st:
        i, j = st.pop()
        for nb in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if nb in cells and nb not in seen:
                seen.add(nb)
                st.append(nb)
    if len(seen) != len(cells):
        return False
    xs = [c[0] for c in cells]
    ys = [c[1] for c in cells]
    box = {(i, j) for i in range(min(xs) - 1, max(xs) + 2) for j in range(min(ys) - 1, max(ys) + 2)} - cells
    start = (min(xs) - 1, min(ys) - 1)
    seen = {start}
    st = [start]
    while st:
        i, j = st.pop()
        for nb in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if nb in box and nb not in seen:
                seen.add(nb)
                st.append(nb)
    if len(seen) != len(box):
        return False                      # a hole
    for (x, y) in lattice_points(cells):
        q = [(x - 1, y - 1) in cells, (x, y - 1) in cells, (x - 1, y) in cells, (x, y) in cells]
        if sum(q) == 2 and ((q[0] and q[3]) or (q[1] and q[2])):
            return False                  # pinch
    return True


def ledger(cells, origin=(0, 0)):
    out = {'area': len(cells), 'reflex': [], 'convex': [], 'transparent': {x: [] for x in 'bcd'},
           'regular_a': []}
    for p in lattice_points(cells):
        s = status(cells, p)
        cl = NAMES[OFFS[((p[0] - origin[0]) % 2, (p[1] - origin[1]) % 2)]]
        if s == 'reflex':
            out['reflex'].append(p)
        elif s == 'convex':
            out['convex'].append(p)
        elif cl == 'a':
            out['regular_a'].append((p, s))
        else:
            out['transparent'][cl].append((p, s))
    out['r'] = len(out['reflex'])
    out['W'] = 2 * out['r'] + 4
    assert len(out['convex']) == out['r'] + 4
    out['k'] = sum((2 if s == 'interior' else 1) for x in 'bcd' for (_, s) in out['transparent'][x])
    return out


def closure_partition(n, gens, seed_pairs):
    par = list(range(n))

    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a

    queue = []

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            par[ra] = rb
            queue.append((a, b))

    for a, b in seed_pairs:
        union(a, b)
    allg = list(gens) + [inv(g) for g in gens]
    while queue:
        a, b = queue.pop()
        for g in allg:
            union(g[a], g[b])
    blocks = {}
    for a in range(n):
        blocks.setdefault(find(a), []).append(a)
    return sorted(blocks.values())


def induced(g, part):
    where = {s: b for b, blk in enumerate(part) for s in blk}
    return tuple(where[g[blk[0]]] for blk in part)


def class_congruence(t, classes):
    """Finest G-invariant partition whose quotient has no 2-cycle over the given corners
    (indices 1, 2, 3 = b, c, d)."""
    n = len(t[0])
    seeds = [tuple(c) for x in classes for c in cycles(t[x]) if len(c) == 2]
    return closure_partition(n, t, seeds)


def a_image(t, part, sheet):
    """Point of N = Q / part over corner a under the Q-point containing `sheet`."""
    where = {s: b for b, blk in enumerate(part) for s in blk}
    ga = induced(t[0], part)
    cid, lens = cycle_index(ga)
    return cid[where[sheet]], lens[cid[where[sheet]]]


def lifts(room, t, p, origin=(0, 0)):
    """Regular points of DP over the class-a lattice point p: list of sheet lists."""
    q = (p[0] - origin[0], p[1] - origin[1])
    c, pts = room.points_at(q)
    assert c == (0, 0)
    return [sorted(cy) for cy in pts]


def decide_pairs(t, sheet_sets_S, sheet_sets_T, max_states=None):
    """Exact verdict for each (lift of S, lift of T): returns (list of (i, j, lit), states)."""
    pt, plen = initial_pt(t[0])
    res = marked_orbit(t, max_states=max_states)
    assert res['complete']
    out = []
    for i, ss in enumerate(sheet_sets_S):
        for j, tt in enumerate(sheet_sets_T):
            P, Q = pt[ss[0]], pt[tt[0]]
            assert plen[P] == 2 and plen[Q] == 2
            out.append((i, j, frozenset((P, Q)) in res['lit']))
    return out, res['states'], res
