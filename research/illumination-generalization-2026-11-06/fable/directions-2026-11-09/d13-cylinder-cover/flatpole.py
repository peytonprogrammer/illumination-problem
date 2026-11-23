#!/usr/bin/env python3
"""Corner / flat-point obstruction test (Proposition O' in theory.md).

For a convex corner c and a flat boundary lattice point f, and every direction
(p, q) with 1 <= p, q <= B, compare D_theta(c) (pole label, as in poles.py)
with the set A_theta(f) of DP cylinders adjacent to f: the labels of the open
plus and minus strips that touch f inside its two cells. If D_theta(c) is
never in A_theta(f), no certificate from these directions covers a
neighbourhood of (c, f).

usage: python3 flatpole.py B x0 y0 x1 y1 ...     (cells of one room)
"""
import sys
from math import gcd

from cyl import labels, point_type
from poles import convex_corners, directions, pole_label


def flat_points(cells):
    out = set()
    for (a, b) in cells:
        for dx in (0, 1):
            for dy in (0, 1):
                if point_type(cells, a + dx, b + dy) == "flat":
                    out.add((a + dx, b + dy))
    return sorted(out)


def adjacent_labels(L, f, cells, p, q):
    """Labels of open strips whose closure contains f, inside the cells at f."""
    x, y = f
    labs = set()
    for c in [(x - 1, y - 1), (x, y - 1), (x - 1, y), (x, y)]:
        if c not in cells:
            continue
        u, v = q * x - p * y, q * x + p * y
        for k in (u - 1, u):
            if k in L.plus[c]:
                labs.add(L.plus[c][k])
        for k in (v - 1, v):
            if k in L.minus[c]:
                labs.add(L.minus[c][k])
    return labs


def main():
    B = int(sys.argv[1])
    v = list(map(int, sys.argv[2:]))
    cells = frozenset((v[2 * i], v[2 * i + 1]) for i in range(len(v) // 2))
    cc = convex_corners(cells)
    fl = flat_points(cells)
    shared = {(P, f): False for P, _ in cc for f in fl}
    for (p, q) in directions(B):
        L = labels(cells, p, q)
        for P, c in cc:
            d = pole_label(L, P, c, p, q)
            for f in fl:
                if d in adjacent_labels(L, f, cells, p, q):
                    shared[(P, f)] = True
    obs = sorted(k for k, s in shared.items() if not s)
    print(f"B {B}: corner-flat pairs never sharing a cylinder: {len(obs)} of {len(shared)}")
    for P, f in obs:
        print("  ", P, f)


if __name__ == "__main__":
    main()
