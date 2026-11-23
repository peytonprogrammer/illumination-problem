"""d67: independent checks of d64 (imports no d64, d52, d10, d62 or d63 module; reads d64 data only).

Part 1  For every room in d64 data/covers.json: own strictly-simple test, own reflex count, own
        normalization (gcd of maximal edge lengths), own B_x (finest W-invariant partition of the
        cells that merges every 2-cycle of g_x = V_p H_q), scope = some class with 1 < blocks < n.
        Counts in-scope rooms (per area) and same-class interior pairs (all four classes).
Part 2  Exact integer billiards (own code): for every same-class interior pair of every in-scope
        room, search primitive directions (p, q), max(p, q) <= H, all signs, for a path S -> T that
        avoids corners (absorbed at convex and reflex vertices). A witness proves the pair lit.
Part 3  The 37 point-level per-target-dark pairs listed in d64 logs/pointlevel.log: billiard witness.
Usage: python3 -B indep.py HMAX
"""
import json
import re
import sys
import time
from collections import Counter, defaultdict
from itertools import combinations
from math import gcd
from pathlib import Path

D64 = Path(__file__).resolve().parent.parent / 'd64-finite-case'


# ---------- room geometry ----------
def vertex_cells(x, y):
    return ((x - 1, y - 1), (x, y - 1), (x - 1, y), (x, y))


def lattice_pts(cs):
    pts = set()
    for (i, j) in cs:
        pts |= {(i, j), (i + 1, j), (i, j + 1), (i + 1, j + 1)}
    return pts


def vstatus(cs, p):
    k = sum(c in cs for c in vertex_cells(*p))
    if k == 4:
        return 'int'
    if k == 3:
        return 'rfx'
    if k == 1:
        return 'cvx'
    if k == 2:
        a, b, c, d = (c in cs for c in vertex_cells(*p))
        return 'pinch' if (a and d) or (b and c) else 'smooth'
    return 'out'


def connected(cs):
    cs = set(cs)
    st = [next(iter(cs))]
    seen = {st[0]}
    while st:
        i, j = st.pop()
        for nb in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if nb in cs and nb not in seen:
                seen.add(nb)
                st.append(nb)
    return len(seen) == len(cs)


def no_holes(cs):
    xs = [c[0] for c in cs]
    ys = [c[1] for c in cs]
    x0, x1, y0, y1 = min(xs) - 1, max(xs) + 1, min(ys) - 1, max(ys) + 1
    st = [(x0, y0)]
    seen = {(x0, y0)}
    while st:
        i, j = st.pop()
        for nb in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if x0 <= nb[0] <= x1 and y0 <= nb[1] <= y1 and nb not in cs and nb not in seen:
                seen.add(nb)
                st.append(nb)
    return len(seen) + len(cs) == (x1 - x0 + 1) * (y1 - y0 + 1)


def strictly_simple(cs):
    return connected(cs) and no_holes(cs) and all(vstatus(cs, p) != 'pinch' for p in lattice_pts(cs))


def edge_lengths(cs):
    """Walk the boundary: maximal edge lengths, horizontal and vertical. Vertices = cvx/rfx points."""
    corners = [p for p in lattice_pts(cs) if vstatus(cs, p) in ('cvx', 'rfx')]
    # each corner has exactly one horizontal and one vertical boundary edge leaving it
    H, V = [], []
    cset = set(corners)
    for (x, y) in corners:
        # horizontal edge to the right: boundary segment [x, x+1] at height y exists iff exactly one
        # of the cells (x, y-1), (x, y) is present
        for dx in (1,):
            if ((x, y - 1) in cs) != ((x, y) in cs):
                L = 1
                while (x + L, y) not in cset:
                    L += 1
                H.append(L)
        if ((x - 1, y) in cs) != ((x, y) in cs):
            L = 1
            while (x, y + L) not in cset:
                L += 1
            V.append(L)
    return H, V


def normalized(cs):
    H, V = edge_lengths(cs)
    gh = gv = 0
    for L in H:
        gh = gcd(gh, L)
    for L in V:
        gv = gcd(gv, L)
    return gh == 1 and gv == 1


# ---------- W-set and B_x ----------
def wset(cells):
    idx = {c: k for k, c in enumerate(cells)}
    G = [[0] * len(cells) for _ in range(4)]   # V0, V1, H0, H1 (even/odd lines)
    for k, (i, j) in enumerate(cells):
        for par in (0, 1):
            nb = (i - 1, j) if i % 2 == par else (i + 1, j)
            G[par][k] = idx.get(nb, k)
            nb = (i, j - 1) if j % 2 == par else (i, j + 1)
            G[2 + par][k] = idx.get(nb, k)
    return G


def congruence(G, pairs, gens):
    n = len(G[0])
    par = list(range(n))

    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a
    todo = list(pairs)
    while todo:
        a, b = todo.pop()
        ra, rb = find(a), find(b)
        if ra == rb:
            continue
        par[ra] = rb
        for g in gens:
            todo.append((g[a], g[b]))
    return len({find(a) for a in range(n)})


def nblocks(G, p, q, rot_only=False):
    n = len(G[0])
    gx = [G[p][G[2 + q][u]] for u in range(n)]
    pairs = [(u, gx[u]) for u in range(n) if gx[u] != u and gx[gx[u]] == u]
    if rot_only:
        gens = [[G[a][G[2 + b][u]] for u in range(n)] for a in (0, 1) for b in (0, 1)]
    else:
        gens = G
    return congruence(G, pairs, gens)


# ---------- exact billiards ----------
def shoot(cs, S, p, q, sx, sy, targets, cap=200000):
    """Integer billiard from lattice point S in direction (sx p, sy q). Returns set of targets hit
    (stops at the first absorbing corner or when the state repeats)."""
    hit = set()
    X, Y = S
    if q == 0 or p == 0:          # axis-parallel: every event is a lattice point
        dx, dy = (sx, 0) if q == 0 else (0, sy)
        start = (X, Y, dx, dy)
        seen = {start}
        for _ in range(cap):
            X += dx
            Y += dy
            if (X, Y) in targets:
                hit.add((X, Y))
            k = sum(c in cs for c in vertex_cells(X, Y))
            if k == 4:
                pass
            elif k == 2:
                dx, dy = -dx, -dy
            else:
                return hit
            st = (X, Y, dx, dy)
            if st in seen:
                return hit
            seen.add(st)
        raise RuntimeError('cap')
    Xs, Ys = S[0] * q, S[1] * p    # x scaled by q, y scaled by p: unit speed in both
    seen = {(S[0], S[1], sx, sy)}
    for _ in range(cap):
        rx, ry = Xs % q, Ys % p
        ddx = (q - rx) if sx > 0 else (rx if rx else q)
        ddy = (p - ry) if sy > 0 else (ry if ry else p)
        st = min(ddx, ddy)
        Xs += sx * st
        Ys += sy * st
        if ddx == ddy:
            x, y = Xs // q, Ys // p
            if (x, y) in targets:
                hit.add((x, y))
            fi = x - 1 if sx > 0 else x
            fj = y - 1 if sy > 0 else y
            ai = x if sx > 0 else x - 1
            aj = y if sy > 0 else y - 1
            hA, vA, dg = (ai, fj) in cs, (fi, aj) in cs, (ai, aj) in cs
            k = 1 + hA + vA + dg
            if k == 4:
                pass
            elif k == 2 and hA:
                sy = -sy
            elif k == 2 and vA:
                sx = -sx
            else:
                return hit
            state = (x, y, sx, sy)
            if state in seen:
                return hit
            seen.add(state)
        elif ddx < ddy:
            x = Xs // q
            j = Ys // p
            across = (x if sx > 0 else x - 1, j)
            if across not in cs:
                sx = -sx
        else:
            y = Ys // p
            i = Xs // q
            across = (i, y if sy > 0 else y - 1)
            if across not in cs:
                sy = -sy
    raise RuntimeError('cap')


def dirs_upto(H):
    out = []
    for m in range(1, H + 1):
        for p in range(0, m + 1):
            for q in range(0, m + 1):
                if max(p, q) == m and gcd(p, q) == 1:
                    out.append((p, q))
    return out


def light_from(cs, S, targets, H):
    """Return {T: (p, q, sx, sy)} witnesses for targets reachable with max(p, q) <= H."""
    left = set(targets)
    wit = {}
    for p, q in dirs_upto(H):
        sxs = (1, -1) if p else (1,)
        sys_ = (1, -1) if q else (1,)
        for sx in sxs:
            for sy in sys_:
                for T in shoot(cs, S, p, q, sx, sy, left):
                    wit[T] = (p, q, sx, sy)
                left -= set(wit)
                if not left:
                    return wit
    return wit


if __name__ == '__main__':
    HMAX = int(sys.argv[1])
    t0 = time.process_time()
    data = json.load(open(D64 / 'data' / 'covers.json'))
    allrooms = data['rooms']
    norm = [r for r in allrooms if r['normalized']]
    norm.sort(key=lambda r: (r['n'], r['cells']))
    c = Counter()
    scope_by_n = Counter()
    norm_by_n = Counter()
    pairs_total = 0
    unlit = []
    maxH = 0
    hist = Counter()
    inscope_idx = []
    for r in allrooms:
        cs = set(tuple(x) for x in r['cells'])
        c['flag_mismatch'] += normalized(cs) != r['normalized']
    for idx, r in enumerate(norm):
        cells = [tuple(x) for x in r['cells']]
        cs = set(cells)
        n = len(cells)
        if not strictly_simple(cs):
            c['NOT_STRICTLY_SIMPLE'] += 1
        rfx = sum(vstatus(cs, p) == 'rfx' for p in lattice_pts(cs))
        if rfx > 8:
            c['R_GT_8'] += 1
        norm_by_n[n] += 1
        G = wset(cells)
        nb = {(p, q): nblocks(G, p, q) for p in (0, 1) for q in (0, 1)}
        nbr = {(p, q): nblocks(G, p, q, True) for p in (0, 1) for q in (0, 1)}
        c['W_vs_rot_mismatch'] += nb != nbr
        if not any(1 < v < n for v in nb.values()):
            continue
        c['in_scope'] += 1
        scope_by_n[n] += 1
        inscope_idx.append(idx)
        ints = [p for p in lattice_pts(cs) if vstatus(cs, p) == 'int']
        bycls = defaultdict(list)
        for p in ints:
            bycls[(p[0] % 2, p[1] % 2)].append(p)
        for cl, L in bycls.items():
            pr = list(combinations(sorted(L), 2))
            pairs_total += len(pr)
            for S in sorted(L):
                Ts = {T for T in L if T != S}
                if not Ts:
                    continue
                w = light_from(cs, S, Ts, HMAX)
                for T in Ts:
                    if T in w:
                        hist[max(w[T][0], w[T][1])] += 1
                    elif S < T:
                        unlit.append((idx, S, T))
    print('rooms in covers.json', len(allrooms), 'normalized', len(norm), dict(c))
    print('normalized by n', sorted(norm_by_n.items()))
    print('in-scope by n', sorted(scope_by_n.items()))
    print('same-class interior pairs in in-scope rooms', pairs_total)
    print('ordered (S,T) witnesses by max(p,q):', sorted(hist.items()))
    print('unordered pairs with no witness at H <= %d:' % HMAX, len(unlit), unlit[:20])
    # Part 3: the 37 point-level pairs
    pl = open(D64 / 'logs' / 'pointlevel.log').read()
    pat = re.compile(r'room (\d+) a=\((\d), (\d)\) x=(\w) S,T=\(\((\d+), (\d+)\), \((\d+), (\d+)\)\)')
    got = 0
    for m in pat.finditer(pl):
        idx = int(m.group(1))
        S = (int(m.group(5)), int(m.group(6)))
        T = (int(m.group(7)), int(m.group(8)))
        cs = set(tuple(x) for x in norm[idx]['cells'])
        assert vstatus(cs, S) == 'int' and vstatus(cs, T) == 'int' and (S[0] - T[0]) % 2 == 0 and (S[1] - T[1]) % 2 == 0
        w = light_from(cs, S, {T}, HMAX)
        xcls = {'b': None}
        ok = T in w
        got += ok
        print('PL room %d S=%s T=%s per-target-dark x=%s : %s' % (
            idx, S, T, m.group(4), ('lit dir %s' % (w[T],)) if ok else 'NO WITNESS'))
    print('point-level pairs with billiard witness:', got)
    print('CPU %.1f' % (time.process_time() - t0))
