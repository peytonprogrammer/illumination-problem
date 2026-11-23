#!/usr/bin/env python3
"""Exact leaf tracer for lattice orthogonal rooms (unions of unit cells).

For a room and a denominator N, list all interior points of (1/N)Z^2. For every
primitive direction (p,q) with max(p,q) <= B and all four sign choices, trace
every billiard leaf exactly in integer arithmetic. Two distinct interior points
on one leaf piece (one closed leaf, or the part of a leaf between two corner
hits) are joined by a legal path. The script reports the pairs that no traced
direction joins. Unjoined pairs are CANDIDATES only: a finite direction bound
never proves darkness.

Usage: leafcheck.py ROOM N B
"""
import sys
from fractions import Fraction
from functools import cmp_to_key
from math import gcd

ROOMS = {
    # 22-wall room of restricted-theorem-note/attainment-check.txt, 15 cells,
    # marks (0,0) and (2,2). Cells are named by their lower-left corner.
    "q22": [(-1, -1), (0, -1), (0, -2), (1, -2), (1, -3),
            (-1, 0), (0, 0), (0, 1), (1, 1), (1, 2),
            (4, 0), (3, 0), (3, 1), (2, 1), (2, 2)],
    # five-square staircase (fold base of q22)
    "stair5": [(-1, -1), (0, -1), (0, -2), (1, -2), (1, -3)],
    "L3": [(0, 0), (1, 0), (0, 1)],
    # 12-wall cross: bars [0,4]x[1,3] and [1,3]x[0,4]
    "cross": [(i, j) for i in range(4) for j in range(4)
              if (1 <= j <= 2) or (1 <= i <= 2)],
    # plus (X) pentomino: all 12 lattice points are corners
    "plus": [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],
    "square": [(0, 0)],
    "rect21": [(0, 0), (1, 0)],
}

_CMP = cmp_to_key(lambda a, b: a[0] * b[1] - b[0] * a[1])


def interior(cells, N, X, Y):
    a, rx = divmod(X, N)
    b, ry = divmod(Y, N)
    if rx and ry:
        return (a, b) in cells
    if rx == 0 and ry:
        return (a, b) in cells and (a - 1, b) in cells
    if ry == 0 and rx:
        return (a, b) in cells and (a, b - 1) in cells
    return all(c in cells for c in ((a, b), (a - 1, b), (a, b - 1), (a - 1, b - 1)))


def build(room, N):
    cells = set(ROOMS[room])
    xs = [c[0] for c in cells]
    ys = [c[1] for c in cells]
    pts = [(X, Y)
           for X in range(min(xs) * N, (max(xs) + 1) * N + 1)
           for Y in range(min(ys) * N, (max(ys) + 1) * N + 1)
           if interior(cells, N, X, Y)]
    return cells, pts


def forward(cells, N, start, d):
    """Trace the billiard leaf from interior point `start` in direction d.

    Coordinates are scaled by N. The unfolded line is U(t) = start + t*d and
    the room position is (sx*Ux + ox, sy*Uy + oy). Returns (states, closed):
    the later states (point, room direction) at interior (1/N)-points, in
    order, and whether the leaf closed up (True) or hit a corner (False).
    """
    P, Q = d
    sx = sy = 1
    ox = oy = 0
    out = []
    j = 0
    limit = 64 * N * (len(cells) + 1)
    while True:
        Ux, Uy = start[0] + j * P, start[1] + j * Q
        ev = []  # wall-line crossings strictly inside the step (j, j+1)
        if P:
            lo, hi = (Ux, Ux + P) if P > 0 else (Ux + P, Ux)
            k = lo // N + 1
            while k * N < hi:
                ev.append((abs(k * N - Ux), abs(P), 0, k * N))
                k += 1
        if Q:
            lo, hi = (Uy, Uy + Q) if Q > 0 else (Uy + Q, Uy)
            k = lo // N + 1
            while k * N < hi:
                ev.append((abs(k * N - Uy), abs(Q), 1, k * N))
                k += 1
        if len(ev) > 1:
            ev.sort(key=_CMP)
        for tn, td, axis, g in ev:  # time tn/td after step j
            if axis == 0:
                rx = sx * g + ox
                a = rx // N
                b = (sy * (Uy * td + Q * tn) + oy * td) // (td * N)
                beyond = (a, b) if sx * P > 0 else (a - 1, b)
                if beyond not in cells:
                    ox = rx + sx * g
                    sx = -sx
            else:
                ry = sy * g + oy
                b = ry // N
                a = (sx * (Ux * td + P * tn) + ox * td) // (td * N)
                beyond = (a, b) if sy * Q > 0 else (a, b - 1)
                if beyond not in cells:
                    oy = ry + sy * g
                    sy = -sy
        j += 1
        Ux, Uy = start[0] + j * P, start[1] + j * Q
        rx, ry = sx * Ux + ox, sy * Uy + oy
        a, mx = divmod(rx, N)
        b, my = divmod(ry, N)
        if mx == 0 and my == 0:  # lattice point of the room
            inn = [c in cells for c in
                   ((a - 1, b - 1), (a, b - 1), (a - 1, b), (a, b))]
            n = sum(inn)
            if n != 4:
                if n == 2 and ((inn[0] and inn[1]) or (inn[2] and inn[3])):
                    assert Q != 0
                    oy = ry + sy * Uy
                    sy = -sy
                    continue
                if n == 2 and ((inn[0] and inn[2]) or (inn[1] and inn[3])):
                    assert P != 0
                    ox = rx + sx * Ux
                    sx = -sx
                    continue
                return out, False  # corner
        elif mx == 0 and P:
            beyond = (a, b) if sx * P > 0 else (a - 1, b)
            if beyond not in cells:
                ox = rx + sx * Ux
                sx = -sx
                continue
        elif my == 0 and Q:
            beyond = (a, b) if sy * Q > 0 else (a, b - 1)
            if beyond not in cells:
                oy = ry + sy * Uy
                sy = -sy
                continue
        st = ((rx, ry), (sx * P, sy * Q))
        if st == (start, d):
            return out, True
        out.append(st)
        if j > limit:
            raise RuntimeError("no recurrence within limit")


def directions(B):
    return [(p, q) for p in range(B + 1) for q in range(B + 1)
            if (p, q) != (0, 0) and gcd(p, q) == 1]


def neg(d):
    return (-d[0], -d[1])


def run(room, N, B, verbose=True):
    cells, pts = build(room, N)
    idx = {p: i for i, p in enumerate(pts)}
    n = len(pts)
    lit = [bytearray(n) for _ in range(n)]
    for (p, q) in directions(B):
        seen = set()
        for pt in pts:
            for d in {(p, q), (-p, q), (p, -q), (-p, -q)}:
                if (pt, d) in seen:
                    continue
                F, closed = forward(cells, N, pt, d)
                chain = [(pt, d)] + F
                if not closed:
                    Bk, c2 = forward(cells, N, pt, neg(d))
                    assert not c2
                    chain += Bk
                for s in chain:
                    seen.add(s)
                    seen.add((s[0], neg(s[1])))
                ids = sorted({idx[s[0]] for s in chain})
                for i in ids:
                    row = lit[i]
                    for k in ids:
                        row[k] = 1
    unlit = [(pts[i], pts[k]) for i in range(n) for k in range(i + 1, n)
             if not lit[i][k]]
    if verbose:
        print(f"room={room} N={N} B={B} points={n} pairs={n*(n-1)//2} "
              f"unjoined={len(unlit)}")
        for a, b in unlit[:300]:
            print("  ", frac(a, N), frac(b, N))
    return pts, unlit


def frac(p, N):
    return "(" + ",".join(str(Fraction(c, N)) for c in p) + ")"


if __name__ == "__main__":
    run(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
