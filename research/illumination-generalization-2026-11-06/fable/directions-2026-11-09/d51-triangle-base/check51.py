"""d51: read-only certificate data for the named rooms over the (2,4,4) base O_h.

Sheets are canonical45 tiles. kappa_E crosses the tile edge of type E
(AB = hypotenuse, AC, BC legs) and fixes the tile at a wall or slit edge.
g_A = k_AC k_AB, g_B = k_BC k_AB, g_C = k_AC k_BC (d11 convention).
Points of Q = DR over class X are the cycles of g_X; e = cycle length.

For each named room and its marked pair this prints, for the canonical
factors B_x (Par) and R_y (Rig), the degrees d, delta, the fibre profiles,
the rigid points, separation of the four lift pairs, and the two
inequalities of memo section 3.

No search: five fixed polygons. Run: python3 -B check51.py
"""
import sys
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'd11-census-45'))
import rooms45 as R  # noqa: E402

ORD = {'A': 4, 'B': 4, 'C': 2}


def cls(p):
    x, y = p
    if x % 2 == 0 and y % 2 == 0:
        return 'A'
    if x % 2 and y % 2:
        return 'B'
    return 'C'


def build(tiles, slit=()):
    tiles = [tuple(t) for t in tiles]
    n = len(tiles)
    V = [R.tile_verts(*t) for t in tiles]
    slit = {frozenset(e) for e in slit}
    own = {}
    for a in range(n):
        for k in range(3):
            own.setdefault(frozenset((V[a][k], V[a][(k + 1) % 3])), []).append(a)
    kap = {}
    for E in ('AB', 'AC', 'BC'):
        perm = list(range(n))
        for a in range(n):
            for k in range(3):
                e = (V[a][k], V[a][(k + 1) % 3])
                if ''.join(sorted(cls(e[0]) + cls(e[1]))) != E:
                    continue
                o = own[frozenset(e)]
                if len(o) == 2 and frozenset(e) not in slit:
                    perm[a] = o[0] if o[1] == a else o[1]
        kap[E] = perm
    comp = lambda f, g: [f[g[i]] for i in range(n)]  # f after g
    g = {'A': comp(kap['AC'], kap['AB']), 'B': comp(kap['BC'], kap['AB']), 'C': comp(kap['AC'], kap['BC'])}
    vert = {X: [next(p for p in V[a] if cls(p) == X) for a in range(n)] for X in 'ABC'}
    return dict(n=n, V=V, kap=kap, g=g, vert=vert)


def cycles(perm, elems=None):
    elems = range(len(perm)) if elems is None else elems
    seen, out = set(), []
    for s in elems:
        if s in seen:
            continue
        c = [s]
        seen.add(s)
        t = perm[s]
        while t != s:
            c.append(t)
            seen.add(t)
            t = perm[t]
        out.append(c)
    return out


def closure(n, gens, pairs):
    par = list(range(n))

    def f(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x

    def u(a, b):
        a, b = f(a), f(b)
        if a != b:
            par[a] = b
            return True
        return False
    for a, b in pairs:
        u(a, b)
    changed = True
    while changed:
        changed = False
        for s in range(n):
            r = f(s)
            for p in gens:
                if u(p[s], p[r]):
                    changed = True
    return [f(s) for s in range(n)]


def factor(room, blk):
    n = room['n']
    roots = sorted(set(blk))
    idx = {r: i for i, r in enumerate(roots)}
    b = [idx[x] for x in blk]
    d = len(roots)
    ind = {}
    for X in 'ABC':
        p = [None] * d
        for s in range(n):
            t = b[room['g'][X][s]]
            assert p[b[s]] in (None, t), 'not a block system'
            p[b[s]] = t
        ind[X] = p
    return b, d, ind


def qpoints(room):
    """Q points over each class: list of (cycle, lattice point)."""
    out = {}
    for X in 'ABC':
        out[X] = [(c, room['vert'][X][c[0]]) for c in cycles(room['g'][X])]
    return out


def walk(room, b, ind, cs, x, start_pt, live, reg):
    """Light-trail over-approximation in M along the base edge cs-x (memo Lemma 2.3)."""
    gs, gx = ind[cs], ind[x]
    cyc_s = {}
    for c in cycles(gs):
        for β in c:
            cyc_s[β] = tuple(sorted(c))
    cyc_x = {}
    for c in cycles(gx):
        for β in c:
            cyc_x[β] = tuple(sorted(c))
    half = lambda perm, β, X: perm[perm[β]] if ORD[X] == 4 else perm[β]
    K = {start_pt}
    states = set()
    stack = [(β, 'to_x') for β in start_pt]
    while stack:
        β, dr = stack.pop()
        if (β, dr) in states:
            continue
        states.add((β, dr))
        if dr == 'to_x':
            p = cyc_x[β]
            if reg[x](p):
                stack.append((half(gx, β, x), 'to_s'))
            elif live[x](p):
                stack.append((β, 'to_s'))
        else:
            p = cyc_s[β]
            K.add(p)
            if reg[cs](p):
                stack.append((half(gs, β, cs), 'to_x'))
            elif live[cs](p):
                stack.append((β, 'to_x'))
    return K


def analyse(name, poly, marks, slit=()):
    tiles = R.tiles_from_polygon(poly)
    room = build(tiles, slit)
    n = room['n']
    qp = qpoints(room)
    # corner data
    corners = {X: [(len(c), pt) for c, pt in qp[X] if len(c) != ORD[X]] for X in 'ABC'}
    t = {X: sum(1 for c, _ in qp[X] if len(c) == ORD[X]) for X in 'ABC'}
    K = {X: sum(e for e, _ in corners[X]) for X in 'ABC'}
    W = sum(len(v) for v in corners.values())
    print('=' * 72)
    print(name, 'tiles N =', n, ' non-regular Q points (corners) =', W)
    for X in 'ABC':
        prof = Counter(e for e, _ in corners[X])
        print('  class %s: regular Q points t=%d, corner profile %s, sum k = %d, fibre check 4t+K = %d'
              % (X, t[X], dict(sorted(prof.items())), K[X], ORD[X] * t[X] + K[X]))
    S, T = marks
    X0 = cls(S)
    assert cls(T) == X0
    lifts = {}
    for P in (S, T):
        ls = [c for c, pt in qp[X0] if pt == P]
        assert len(ls) == 2 and all(len(c) == ORD[X0] for c in ls), (P, ls)
        lifts[P] = ls
    print('  marks', S, T, 'class', X0)
    gens = [room['g'][X] for X in 'ABC']
    others = [X for X in 'ABC' if X != X0]
    fac = {}
    for X in 'ABC':
        pairs = []
        for c, _ in qp[X]:
            if len(c) == ORD[X]:
                for s in c:
                    pairs.append((s, room['g'][X][room['g'][X][s]] if ORD[X] == 4 else room['g'][X][s]))
        fac['B_' + X] = closure(n, gens, pairs)
        pairs = [(c[0], s) for c, _ in qp[X] for s in c]
        fac['R_' + X] = closure(n, gens, pairs)
    for fname, blk in fac.items():
        b, d, ind = factor(room, blk)
        delta = n // d
        assert delta * d == n
        kinv = all(len({b[room['kap'][E][s]] for s in range(n) if b[s] == i}) == 1
                   for E in room['kap'] for i in range(d))
        # M points and their Q preimages
        mpts = {}
        for X in 'ABC':
            mp = {}
            for c in cycles(ind[X]):
                mp[tuple(sorted(c))] = []
            for c, pt in qp[X]:
                key = next(k for k in mp if b[c[0]] in k)
                mp[key].append((len(c), pt))
            mpts[X] = mp
        prof = {X: dict(sorted(Counter(len(k) for k in mpts[X]).items())) for X in 'ABC'}
        rigid = []
        for X in 'ABC':
            for k, pre in mpts[X].items():
                e = len(k)
                if (ORD[X] == 4 and e in (3, 5, 6, 7, 8)) or (ORD[X] == 2 and e >= 3):
                    rigid.append((X, e, sorted(pre)))
        live = {X: (lambda X: lambda p: any(e == ORD[X] for e, _ in mpts[X][p]))(X) for X in 'ABC'}
        reg = {X: (lambda X: lambda p: len(p) == ORD[X])(X) for X in 'ABC'}
        img = {P: [next(k for k in mpts[X0] if b[c[0]] in k) for c in lifts[P]] for P in (S, T)}
        print('  %s: d=%d delta=%d kappa-invariant=%s profiles A%s B%s C%s rigid=%d'
              % (fname, d, delta, kinv, prof['A'], prof['B'], prof['C'], len(rigid)))
        for X, e, pre in rigid[:6]:
            print('      rigid point over %s, e_M=%d, preimages (e_Q, point): %s' % (X, e, pre))
        if len(rigid) > 6:
            print('      ...', len(rigid) - 6, 'more')
        kind, X = fname.split('_')
        if d == 1:
            continue
        if kind == 'B' and X != X0:
            sep = all(a != c for a in img[S] for c in img[T])
            print('      Par(%s): no regular point over %s; all 4 lift pairs separated: %s' % (X, X, sep))
            Xr = X
        elif kind == 'R' and X != X0:
            Xr = X
            for x in others:
                if x == X or X == X0:
                    continue
                # Rig(x) with identity at y = X needs y outside {X0, x}
                ok = True
                for a in img[S]:
                    Kset = walk(room, b, ind, X0, x, a, live, reg)
                    if any(c in Kset for c in img[T]):
                        ok = False
                print('      Rig(%s), identity at %s: all lift pairs separated: %s' % (x, X, ok))
        else:
            continue
        # inequality (3.1): N <= ORD*(... ) ; X_r = class whose regular points ramify
        o = ORD[Xr]
        lhs_t = t[Xr]
        ram_bound = (2 * delta - 2) if (kind == 'B' or o == 2) else (2 * delta - 2) // 3
        print('      (3.1) regular Q points over %s: t=%d <= RH budget %d : %s ; N=%d <= %d*%d + %d = %d : %s'
              % (Xr, lhs_t, ram_bound, lhs_t <= ram_bound, n, o, ram_bound, K[Xr], o * ram_bound + K[Xr],
                 n <= o * ram_bound + K[Xr]))
    return room


def main():
    t0 = time.process_time()
    k = R.worksheet_constants()
    analyse('room22_tri (22-wall orthogonal room, canonical45 tiles)', k['ROOM22'], [(0, 0), (2, 2)])
    analyse('castro24', k['CASTRO24'], list(k['PUBLISHED_ST']))
    analyse('tokarsky26', k['TOKARSKY26'], list(k['PUBLISHED_ST']))
    slit_outer = [(0, 2), (1, 2), (1, 1), (2, 0), (2, 1), (4, 1), (4, 0), (5, 1), (5, 2), (6, 2), (5, 3), (4, 3),
                  (4, 4), (3, 3), (2, 4), (2, 3), (1, 3)]
    analyse('monteil slit room (not strictly simple)', slit_outer, [(2, 2), (4, 2)], slit=[((3, 1), (3, 2))])
    analyse('wolecki22 pinched (not strictly simple)', R.WOLECKI22, [(0, 0), (2, 2)])
    print('CPU seconds: %.2f' % (time.process_time() - t0))


if __name__ == '__main__':
    main()
