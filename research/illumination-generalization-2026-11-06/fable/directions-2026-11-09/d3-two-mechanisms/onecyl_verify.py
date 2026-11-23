#!/usr/bin/env python3
"""Independent certificate that a direction is one-cylinder on the double DP.

Method (does not use the strip formula of cylcount.py). Take a prime N > p+q.
Nodes are the regular closed leaves through interior (1/N)-grid points, in all
line classes. Join the leaves through two axis-adjacent interior grid points
X, X+e (same sheet) when no line q*x - p*y in Z lies strictly between them.
The short segment from X to X+e then crosses no singular leaf, so every join
is inside one cylinder: #components >= #cyl(M). Because the half-turn pairs
the cylinders of M, #cyl(M) >= 2. So #components == 2 certifies exactly two
cylinders on M, that is, one cylinder on DP.

Usage: onecyl_verify.py ROOM p q [p q ...]
"""
import sys
from leafcheck import build, forward, neg


def components(room, p, q):
    N = next(n for n in (5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47)
             if n > abs(p) + abs(q))
    cells, pts = build(room, N)
    ptset = set(pts)
    dirs = ((p, q), (-p, q), (p, -q), (-p, -q))
    leaf = {}       # state -> leaf id, or -1 if singular
    nleaf = 0
    for pt in pts:
        for d in dirs:
            if (pt, d) in leaf:
                continue
            F, closed = forward(cells, N, pt, d)
            chain = [(pt, d)] + F
            if closed:
                for s in chain:
                    leaf[s] = nleaf
                nleaf += 1
            else:
                Bk, _ = forward(cells, N, pt, neg(d))
                for s in chain:
                    leaf[s] = -1
                for s in Bk:
                    leaf[(s[0], neg(s[1]))] = -1
    parent = list(range(nleaf))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for (X, d), lid in leaf.items():
        if lid < 0:
            continue
        L = d[1] * X[0] - d[0] * X[1]
        for e in ((1, 0), (0, 1)):
            Y = (X[0] + e[0], X[1] + e[1])
            if Y not in ptset:
                continue
            lid2 = leaf[(Y, d)]
            if lid2 < 0:
                continue
            L2 = d[1] * Y[0] - d[0] * Y[1]
            lo, hi = min(L, L2), max(L, L2)
            # an integer line strictly between  <=>  a multiple of N in (lo,hi)
            if (hi - 1) // N * N > lo:
                continue
            a, b = find(lid), find(lid2)
            if a != b:
                parent[a] = b
    return len({find(i) for i in range(nleaf)}), nleaf, N


if __name__ == "__main__":
    room = sys.argv[1]
    v = list(map(int, sys.argv[2:]))
    for p, q in zip(v[0::2], v[1::2]):
        c, n, N = components(room, p, q)
        print(f"room={room} direction=({p},{q}) grid N={N} regular leaves={n} "
              f"components={c} -> {'ONE cylinder on DP (certified)' if c == 2 else 'not certified'}")
