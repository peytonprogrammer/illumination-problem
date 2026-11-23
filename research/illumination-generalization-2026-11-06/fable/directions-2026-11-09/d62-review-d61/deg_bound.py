"""d62: check the d61 section 6 bound deg N_x <= (r + 4) + 3 r_x <= 4r + 4 on the named rooms.

B_x computed here by union-find closure (own code). Checks: N_x has no regular point over x,
P - Z = 4 on N_x, Z(N_x) <= r, and the bound.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'd61-fold-converse'))
sys.path.insert(0, str(HERE.parent / 'd10-mechanisms'))
from roomtools import room_tuple, lattice_points, status  # noqa: E402
from fold_converse import rooms  # noqa: E402
from check_fc import cycles  # noqa: E402


def closure(gens, n, pairs):
    par = list(range(n))

    def f(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x
    q = list(pairs)
    while q:
        s, t = q.pop()
        a, b = f(s), f(t)
        if a == b:
            continue
        par[a] = b
        for g in gens:
            q.append((g[s], g[t]))
    blocks = {}
    for s in range(n):
        blocks.setdefault(f(s), []).append(s)
    return list(blocks.values())


for name, cells in rooms():
    pts = lattice_points(cells)
    origin = min(p for p in pts if status(cells, p) == 'convex')
    room, t = room_tuple(cells, origin)
    n = len(t[0])
    r = sum(status(cells, p) == 'reflex' for p in pts)
    cls = {(0, 0): 0, (1, 0): 1, (1, 1): 2, (0, 1): 3}
    for j in (1, 2, 3):
        rx = sum(status(cells, p) == 'reflex' and cls[((p[0] - origin[0]) % 2, (p[1] - origin[1]) % 2)] == j
                 for p in pts)
        pairs = [tuple(c) for c in cycles(t[j]) if len(c) == 2]
        P = closure(t, n, pairs)
        where = {s: k for k, b in enumerate(P) for s in b}
        ind = [tuple(where[g[b[0]]] for b in P) for g in t]
        lens = [[len(c) for c in cycles(g)] for g in ind]
        poles = sum(L.count(1) for L in lens)
        zeros = sum(L.count(3) for L in lens)
        assert all(l <= 3 for L in lens for l in L)
        assert 2 not in lens[j], 'regular point over x'
        assert poles - zeros == 4, (poles, zeros)
        assert zeros <= r
        deg = len(P)
        assert deg == lens[j].count(1) + 3 * lens[j].count(3)
        ok = deg <= r + 4 + 3 * rx <= 4 * r + 4
        print('%-8s n=%2d r=%d x=%s deg N_x=%2d  P=%d Z=%d  P_x=%d Z_x=%d r_x=%d  bound r+4+3r_x=%d  4r+4=%d  %s'
              % (name, n, r, 'abcd'[j], deg, poles, zeros, lens[j].count(1), lens[j].count(3), rx,
                 r + 4 + 3 * rx, 4 * r + 4, 'ok' if ok else 'VIOLATED'))
