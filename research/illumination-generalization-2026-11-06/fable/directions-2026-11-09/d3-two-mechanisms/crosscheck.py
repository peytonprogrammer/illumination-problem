#!/usr/bin/env python3
"""Independent ray-casting tracer (Fractions, boundary edges) to cross-check
leafcheck.forward. Compares the ordered interior (1/N)-points visited.

Usage: crosscheck.py ROOM N B SAMPLES
"""
import random
import sys
from fractions import Fraction as Fr
from math import gcd
from leafcheck import ROOMS, build, forward


def boundary(cells):
    V, H = set(), set()  # V: (x, y) unit edge {x} x [y,y+1]; H: [x,x+1] x {y}
    for (i, j) in cells:
        if (i - 1, j) not in cells: V.add((i, j))
        if (i + 1, j) not in cells: V.add((i + 1, j))
        if (i, j - 1) not in cells: H.add((i, j))
        if (i, j + 1) not in cells: H.add((i, j + 1))
    return V, H


def corner_type(cells, a, b):
    inn = [c in cells for c in ((a - 1, b - 1), (a, b - 1), (a - 1, b), (a, b))]
    n = sum(inn)
    if n == 4: return "int"
    if n == 2 and ((inn[0] and inn[1]) or (inn[2] and inn[3])): return "hwall"
    if n == 2 and ((inn[0] and inn[2]) or (inn[1] and inn[3])): return "vwall"
    return "corner"


def trace(cells, N, start, d, maxpts):
    V, H = boundary(cells)
    pos = (Fr(start[0], N), Fr(start[1], N))
    v = (Fr(d[0], N), Fr(d[1], N))  # one unit of time = one (1/N)-lattice step
    pts = []
    clock = Fr(0)  # time since start; lattice visits at integer clock
    while len(pts) < maxpts:
        # first boundary hit
        best = None
        if v[0]:
            for (x, y) in V:
                t = (x - pos[0]) / v[0]
                if t > 0:
                    yy = pos[1] + t * v[1]
                    if y <= yy <= y + 1 and (best is None or t < best[0]):
                        best = (t, "v")
        if v[1]:
            for (x, y) in H:
                t = (y - pos[1]) / v[1]
                if t > 0:
                    xx = pos[0] + t * v[0]
                    if x <= xx <= x + 1 and (best is None or t < best[0]):
                        best = (t, "h")
        t = best[0]
        # interior lattice visits strictly before the hit
        k = int(clock) + 1 if clock == int(clock) else -(-clock.numerator // clock.denominator)
        while k < clock + t and len(pts) < maxpts:
            p = (pos[0] + (k - clock) * v[0], pos[1] + (k - clock) * v[1])
            pts.append((int(p[0] * N), int(p[1] * N)))
            k += 1
        hit = (pos[0] + t * v[0], pos[1] + t * v[1])
        clock += t
        pos = hit
        if hit[0].denominator == 1 and hit[1].denominator == 1:
            ty = corner_type(cells, int(hit[0]), int(hit[1]))
            if ty == "corner":
                return pts, "corner"
            if ty == "hwall": v = (v[0], -v[1])
            elif ty == "vwall": v = (-v[0], v[1])
            else: raise AssertionError("boundary hit at interior point")
        elif hit[0].denominator == 1 and best[1] == "v":
            v = (-v[0], v[1])
        else:
            v = (v[0], -v[1])
    return pts, "cut"


def main(room, N, B, samples):
    cells, pts = build(room, N)
    rnd = random.Random(20261109)
    bad = 0
    for _ in range(samples):
        s = rnd.choice(pts)
        while True:
            p, q = rnd.randint(-B, B), rnd.randint(-B, B)
            if (p, q) != (0, 0) and gcd(p, q) == 1:
                break
        # the independent tracer needs generic motion: skip sliding starts
        F, closed = forward(cells, N, s, (p, q))
        ref = [x[0] for x in F]
        if closed:
            ref = ref + [s] + ref  # one more lap for comparison
        # open leaf: allow one extra point so the tracer must reach the corner
        got, why = trace(cells, N, s, (p, q), len(ref) + (0 if closed else 1))
        if got != ref[:len(got)] or (not closed and (why != "corner" or len(got) != len(ref))):
            bad += 1
            print("MISMATCH", s, (p, q), closed, why, len(ref), len(got))
    print(f"room={room} N={N} samples={samples} mismatches={bad}")


if __name__ == "__main__":
    main(sys.argv[1], *map(int, sys.argv[2:5]))
