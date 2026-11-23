#!/usr/bin/env python3
"""Independent exact check for the d16 review (task 3).

Room: the 22-vertex dark room. Checks, with exact rationals, that
(1,3),(3,5) has no vertex-free billiard path among unfolded images
(e1*tx+2m, e2*ty+2n), |m|,|n| <= R, and that slid pairs of the Theorem 1
shape (S moves by delta along an axis, T by rho*delta) are lit.
Written from scratch; it shares no code with d16-real-to-rational.
"""
import sys
from fractions import Fraction as Fr
from math import floor, ceil

VERTS = [(0,2),(0,4),(1,4),(1,5),(2,5),(2,6),(4,6),(4,5),(5,5),(5,4),(6,4),
         (6,3),(4,3),(4,4),(2,4),(2,2),(3,2),(3,0),(2,0),(2,1),(1,1),(1,2)]

def inside(px, py):
    c = False
    n = len(VERTS)
    for k in range(n):
        (x0, y0), (x1, y1) = VERTS[k], VERTS[(k + 1) % n]
        if (y0 > py) != (y1 > py) and px < x0 + (py - y0) * (x1 - x0) / (y1 - y0):
            c = not c
    return c

CELLS = {(i, j) for i in range(6) for j in range(6) if inside(i + 0.5, j + 0.5)}

def around(i, j):
    return [c for c in ((i-1, j-1), (i, j-1), (i-1, j), (i, j)) if c in CELLS]

def ahead(x, v):
    """time to the next integer strictly ahead of x at speed v != 0"""
    return (floor(x) + 1 - x) / v if v > 0 else (x - (ceil(x) - 1)) / -v

def trace(S, T, v):
    """True iff the billiard path from S with velocity v meets T in time (0,1]
    before touching a vertex."""
    x, y = S
    vx, vy = v
    left = Fr(1)
    while left > 0:
        dt = min(ahead(p, w) for p, w in ((x, vx), (y, vy)) if w != 0)
        step = min(dt, left)
        lam = (T[0] - x) / vx if vx != 0 else (T[1] - y) / vy
        if 0 < lam <= step and x + lam * vx == T[0] and y + lam * vy == T[1]:
            return True
        if dt > left:
            return False
        left -= dt
        x, y = x + vx * dt, y + vy * dt
        ix, iy = x.denominator == 1, y.denominator == 1
        if ix and iy:
            a = around(int(x), int(y))
            if len(a) in (1, 3):
                return False                      # vertex
            if len(a) == 2:                       # flat wall point
                if a[0][0] == a[1][0]:            # room on one side in x: vertical wall
                    vx = -vx
                else:
                    vy = -vy
            assert len(a) in (2, 4)
        elif ix:
            nxt = (int(x) if vx > 0 else int(x) - 1, floor(y))
            if nxt not in CELLS:
                vx = -vx
        else:
            nxt = (floor(x), int(y) if vy > 0 else int(y) - 1)
            if nxt not in CELLS:
                vy = -vy
    return False

def interior(P):
    """every unit cell whose closure contains P is in the room"""
    xs = (int(P[0]) - 1, int(P[0])) if P[0].denominator == 1 else (floor(P[0]),)
    ys = (int(P[1]) - 1, int(P[1])) if P[1].denominator == 1 else (floor(P[1]),)
    return all((i, j) in CELLS for i in xs for j in ys)

def lit(S, T, R):
    """smallest max(|m|,|n|) of a lighting image, or None"""
    for r in range(R + 1):
        for m in range(-r, r + 1):
            for n in range(-r, r + 1):
                if max(abs(m), abs(n)) != r:
                    continue
                for e1 in (1, -1):
                    for e2 in (1, -1):
                        v = (e1 * T[0] + 2 * m - S[0], e2 * T[1] + 2 * n - S[1])
                        if v != (0, 0) and trace(S, T, v):
                            return r
    return None

if __name__ == "__main__":
    R = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    area2 = sum(VERTS[k][0] * VERTS[(k + 1) % 22][1] - VERTS[(k + 1) % 22][0] * VERTS[k][1] for k in range(22))
    assert abs(area2) == 2 * len(CELLS)
    print("cells", len(CELLS))
    S0, T0 = (Fr(1), Fr(3)), (Fr(3), Fr(5))
    print("base pair (1,3),(3,5): lit radius =", lit(S0, T0, R), "(None = dark up to R=%d)" % R)
    # control: a pair in one rectangle must be lit
    print("control (1/2,5/2),(3/2,7/2):", lit((Fr(1,2), Fr(5,2)), (Fr(3,2), Fr(7,2)), R))
    worst, dark, skipped = 0, [], 0
    for axis in (0, 1):
        for rho in (Fr(1), Fr(-1), Fr(2), Fr(-2), Fr(1, 2), Fr(-1, 2), Fr(3), Fr(-1, 3)):
            for d in (2, 3, 5, 7, 11, 50):
                for sg in (1, -1):
                    delta = Fr(sg, d)
                    S, T = list(S0), list(T0)
                    S[axis] += delta
                    T[axis] += rho * delta
                    if not (interior(S) and interior(T)):
                        skipped += 1
                        continue
                    r = lit(tuple(S), tuple(T), R)
                    if r is None:
                        dark.append((axis, rho, delta))
                    else:
                        worst = max(worst, r)
    print("slid pairs tested: %d (skipped %d with a point outside the room), not lit up to R: %d, largest lighting radius: %d"
          % (192 - skipped, skipped, len(dark), worst))
    for row in dark:
        print("  unlit:", row)
