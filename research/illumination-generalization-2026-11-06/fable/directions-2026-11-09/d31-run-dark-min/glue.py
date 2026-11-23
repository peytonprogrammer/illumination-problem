"""d31: dark rooms with a run, built from reflected copies of a parity base.

1. Bases: every strictly simple polyomino with area <= AMAX (up to the 8
   symmetries) and every parity class A such that each non-A lattice point
   is a corner and R has >= 2 A points ("parity property").
2. Glued rooms: sets of copies g(R), g in the group of reflections in integer
   lattice lines (x -> +-x + even, y -> +-y + even), connected by edge
   adjacency, cells disjoint, fold map P -> R single-valued on lattice points.
   Every set reachable by reflecting one copy across the line of one of its
   boundary edges is generated, up to D = 6 copies. This includes every
   gluing tree across walls joining two convex corners.
3. Kept: strictly simple rooms with a run (two adjacent identical non-empty
   cell rows or columns) and interior A points S, T with fold(S) != fold(T)
   and neither on the run line. Dark by the fold-back lemma.

usage: python3 glue.py AMAX D
"""
import sys, json
from itertools import product

AMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 8
DMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 6
NB = ((1, 0), (-1, 0), (0, 1), (0, -1))


def around(cells, p):
    x, y = p
    return [(x, y) in cells, (x - 1, y) in cells, (x - 1, y - 1) in cells, (x, y - 1) in cells]


def points(cells):
    return {(x + a, y + b) for (x, y) in cells for a in (0, 1) for b in (0, 1)}


def ptype(cells, p):
    q = around(cells, p); n = sum(q)
    if n == 1: return 'convex'
    if n == 3: return 'reflex'
    if n == 4: return 'int'
    if n == 2 and (q[0] and q[2] or q[1] and q[3]): return 'PINCH'
    return 'flat'


def room_ok(cells):
    """Connected, no pinch, no hole. Returns (types, W, r) or None."""
    seen, st = set(), [next(iter(cells))]
    while st:
        c = st.pop()
        if c in seen: continue
        seen.add(c)
        st.extend((c[0] + d[0], c[1] + d[1]) for d in NB if (c[0] + d[0], c[1] + d[1]) in cells)
    if seen != cells: return None
    t = {p: ptype(cells, p) for p in points(cells)}
    if 'PINCH' in t.values(): return None
    cv = sum(v == 'convex' for v in t.values()); rf = sum(v == 'reflex' for v in t.values())
    if cv - rf != 4: return None
    return t, cv + rf, rf


def norm(cells):
    mx = min(x for x, _ in cells); my = min(y for _, y in cells)
    return tuple(sorted((x - mx, y - my) for x, y in cells))


def canon(cells):
    best = None
    for sw, fx, fy in product((0, 1), (1, -1), (1, -1)):
        c = [((y, x) if sw else (x, y)) for x, y in cells]
        c = norm([(fx * x, fy * y) for x, y in c])
        if best is None or c < best: best = c
    return best


def polyominoes(amax):
    level = {((0, 0),)}
    out = [((0, 0),)]
    for _ in range(amax - 1):
        nxt = set()
        for p in level:
            s = set(p)
            for (x, y) in p:
                for d in NB:
                    c = (x + d[0], y + d[1])
                    if c not in s: nxt.add(canon(s | {c}))
        level = nxt; out.extend(sorted(level))
    return out


def cls(p): return (p[0] & 1, p[1] & 1)


def bases(amax):
    res = []
    for poly in polyominoes(amax):
        cells = set(poly)
        ok = room_ok(cells)
        if not ok: continue
        t, W, r = ok
        for A in product((0, 1), (0, 1)):
            if all(v in ('convex', 'reflex') for p, v in t.items() if cls(p) != A):
                apts = sorted(p for p in t if cls(p) == A)
                if len(apts) >= 2:
                    res.append({'cells': poly, 'A': A, 'W': W, 'r': r, 'Apts': apts})
    return res


# transforms g = (sx, sy, tx, ty): point (x,y) -> (sx x + tx, sy y + ty), tx, ty even
def gp(g, p): return (g[0] * p[0] + g[2], g[1] * p[1] + g[3])
def gc(g, c):
    x, y = gp(g, c)
    return (x if g[0] > 0 else x - 1, y if g[1] > 0 else y - 1)
def ginv(g): return (g[0], g[1], -g[0] * g[2], -g[1] * g[3])
def gmul(a, b):  # a o b
    return (a[0] * b[0], a[1] * b[1], a[0] * b[2] + a[2], a[1] * b[3] + a[3])


def glue(base, dmax):
    R = set(base['cells']); Rpts = points(R)
    redges = []  # boundary unit edges of R as reflection lines: ('x', a) or ('y', b)
    for (x, y) in R:
        if (x + 1, y) not in R: redges.append(('x', x + 1))
        if (x - 1, y) not in R: redges.append(('x', x))
        if (x, y + 1) not in R: redges.append(('y', y + 1))
        if (x, y - 1) not in R: redges.append(('y', y))
    lines = sorted(set(redges))
    refl = {('x', a): (-1, 1, 2 * a, 0) for k, a in lines if k == 'x'}
    refl.update({('y', b): (1, -1, 0, 2 * b) for k, b in lines if k == 'y'})

    def key(gs):  # canonical up to the group action
        return min(tuple(sorted(gmul(ginv(h), g) for g in gs)) for h in gs)

    ident = (1, 1, 0, 0)
    level = {(ident,): None}
    found = []; mins = {}
    for d in range(2, dmax + 1):
        nxt = {}
        for gs in level:
            cells = {}; fold = {}
            for g in gs:
                for c in R: cells[gc(g, c)] = g
                for p in Rpts: fold[gp(g, p)] = p
            for g in gs:
                for ln in lines:
                    # reflection line of this edge in the copy g(R): rho' = g rho g^-1
                    rho = gmul(gmul(g, refl[ln]), ginv(g))
                    g2 = gmul(rho, g)
                    if g2 in gs: continue
                    if any(gc(g2, c) in cells for c in R): continue
                    if any(fold.get(gp(g2, p), p) != p for p in Rpts): continue
                    k = key(gs + (g2,))
                    if k not in nxt: nxt[k] = None
        level = nxt
        for gs in level:
            cells = set(); fold = {}
            for g in gs:
                cells |= {gc(g, c) for c in R}
                for p in Rpts: fold[gp(g, p)] = p
            ok = room_ok(cells)
            if not ok: continue
            t, W, r = ok
            st = mins.setdefault(d, [99, 99, 99, 99])
            st[0] = min(st[0], W)
            runs = find_runs(cells)
            if dark_pairs(t, fold, base['A'], [('y', 10**6)]): st[1] = min(st[1], W)
            if not runs: continue
            st[2] = min(st[2], W)
            pairs = dark_pairs(t, fold, base['A'], runs)
            if pairs:
                st[3] = min(st[3], W)
                found.append({'d': d, 'W': W, 'r': r, 'area': len(cells), 'gs': gs,
                              'cells': sorted(cells), 'runs': runs, 'pairs': pairs})
        print(f"  d={d}: {len(level)} copy sets, {sum(f['d'] == d for f in found)} dark rooms with a run;",
              "min W [simple, separated pair, run, run+separated pair]:", mins.get(d), flush=True)
    return found


def find_runs(cells):
    out = []
    for ax in (0, 1):
        rows = {}
        for c in cells: rows.setdefault(c[1 - ax], set()).add(c[ax])
        for y in rows:
            if y + 1 in rows and rows[y] == rows[y + 1]:
                out.append(('y' if ax == 0 else 'x', y + 1))  # line coordinate
    return out


def dark_pairs(t, fold, A, runs):
    S = sorted(p for p, v in t.items() if v == 'int' and cls(p) == A)
    res = []
    for i in range(len(S)):
        for j in range(i + 1, len(S)):
            a, b = S[i], S[j]
            if fold[a] == fold[b]: continue
            best = None
            for k, c in runs:
                ax = 1 if k == 'y' else 0
                ca, cb = a[ax], b[ax]
                if ca == c or cb == c: continue
                pos = 'strong' if abs(ca - c) >= 2 and abs(cb - c) >= 2 else 'weak'
                if best is None or pos == 'strong': best = (pos, k, c)
            if best: res.append((a, b, best))
    return res


if __name__ == '__main__':
    B = bases(AMAX)
    print(f"bases with the parity property, area <= {AMAX}: {len(B)}")
    for b in B: print("  ", b['cells'], "A", b['A'], "W", b['W'], "A points", b['Apts'])
    allf = []
    for b in B:
        print("base", b['cells'], "A", b['A'], flush=True)
        for f in glue(b, DMAX):
            f['base'] = b['cells']; f['A'] = b['A']; allf.append(f)
    seen = {}
    for f in allf:
        k = canon(f['cells'])
        if k not in seen or f['W'] < seen[k]['W']: seen[k] = f
    rooms = sorted(seen.values(), key=lambda f: (f['W'], f['area']))
    print(f"distinct dark rooms with a run: {len(rooms)}")
    for pos in ('weak', 'strong'):
        rs = [f for f in rooms if any(p[2][0] == pos or pos == 'weak' for p in f['pairs'])]
        if rs: print(f"min W ({pos} position): {rs[0]['W']}")
    byW = {}
    for f in rooms:
        st = any(p[2][0] == 'strong' for p in f['pairs'])
        byW.setdefault(f['W'], [0, 0])[st] += 1
    print("W: [weak only, strong]", dict(sorted(byW.items())))
    json.dump(rooms, open('found.json', 'w'), default=list)
