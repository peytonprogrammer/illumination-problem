#!/usr/bin/env python3
"""Reviewer's independent checks for Theorem Q22.

1. Room sanity: rebuild the 22-wall room from the manuscript's copy formulas,
   compare the vertex cycle with the manuscript's 22 listed vertices, list
   interior lattice points, and list the integer points of the staircase P.
2. Cylinder counts on M for (4,7), (7,4) and their mirror directions, plus
   control rooms with known answers.
3. X computed by brute force over (1/(2*lcm)) Z^2 mod Z^2.
4. Leaves through the four lifts of (0,0) and (2,2): regular or singular.

Usage: python3 check_q22.py
"""
from fractions import Fraction as Fr
from math import gcd
from itertools import product
from surface import Surface, q22_cells, boundary_cycle, point_type

MANUSCRIPT_VERTS = [(-1, -1), (0, -1), (0, -2), (1, -2), (1, -3), (2, -3),
                    (2, -1), (1, -1), (1, 1), (3, 1), (3, 0), (5, 0),
                    (5, 1), (4, 1), (4, 2), (3, 2), (3, 3), (1, 3),
                    (1, 2), (0, 2), (0, 1), (-1, 1)]


def cyl_dir(S, p, q):
    """Cylinders of M in direction (p,q) (any signs, pq != 0)."""
    if q < 0:
        # reflect room in y: direction (p,-q) on room R <-> (p,q) on mirror room
        S = Surface({(a, -b - 1) for a, b in S.cells})
        q = -q
    if p < 0:
        S = Surface({(-a - 1, b) for a, b in S.cells})
        p = -p
    return S.cylinders(p, q)


def main():
    cells = q22_cells()
    verts, vset = boundary_cycle(cells)
    print("walls (vertices):", len(verts))
    # compare as cyclic sequences up to rotation/reversal
    def canon(c):
        n = len(c)
        cands = []
        for seq in (c, c[::-1]):
            for k in range(n):
                cands.append(tuple(seq[k:] + seq[:k]))
        return min(cands)
    print("vertex cycle equals manuscript list:", canon(verts) == canon(MANUSCRIPT_VERTS))
    conv = sum(point_type(cells, *v) == "convex" for v in verts)
    print("convex/reflex:", conv, len(verts) - conv, " area:", len(cells))
    lat = {(x, y) for a, b in cells for x in (a, a + 1) for y in (b, b + 1)}
    interior = sorted(p for p in lat if point_type(cells, *p) == "interior")
    flat = sorted(p for p in lat if point_type(cells, *p).startswith("flat"))
    print("interior lattice points:", interior)
    print("flat (removable) boundary lattice points:", flat)
    classes = {(x % 2, y % 2) for x, y in verts}
    print("corner classes C:", sorted(classes))
    Pst = {(-1, -1), (0, -1), (0, -2), (1, -2), (1, -3)}
    latP = sorted({(x, y) for a, b in Pst for x in (a, a + 1) for y in (b, b + 1)})
    print("staircase P integer points and types:",
          [(p, point_type(Pst, *p)) for p in latP])

    S = Surface(cells)
    print("\nsquares in M:", len(S.sq))
    for p, q in [(4, 7), (7, 4), (4, -7), (7, -4), (-4, 7), (-7, -4)]:
        c, ns = cyl_dir(S, p, q)
        print(f"direction ({p},{q}): strips={ns} cylinders on M={c} -> on DP={Fr(c, 2)}")

    print("\ncontrols:")
    rooms = {
        "square": {(0, 0)},
        "L3": {(0, 0), (1, 0), (0, 1)},
        "cross": {(i, j) for i in range(4) for j in range(4) if 1 <= j <= 2 or 1 <= i <= 2},
        "stair5": Pst,
    }
    for name, rc in rooms.items():
        R = Surface(rc)
        hist = {}
        ones = []
        for p in range(1, 9):
            for q in range(1, 9):
                if gcd(p, q) != 1:
                    continue
                c, _ = R.cylinders(p, q)
                hist[c // 2 if c % 2 == 0 else ("odd", c)] = hist.get(c // 2 if c % 2 == 0 else ("odd", c), 0) + 1
                if c == 2:
                    ones.append((p, q))
        print(f"  {name}: hist #cyl(DP) for 1<=p,q<=8: {sorted(hist.items(), key=str)}; one-cyl: {ones[:12]}")

    # full scan of q22 for comparison with the audit table (both signs of q)
    hist = {}
    ones = []
    for p in range(1, 15):
        for q in range(1, 15):
            if gcd(p, q) != 1:
                continue
            for sq in (1, -1):
                c, _ = cyl_dir(S, p, sq * q)
                assert c % 2 == 0
                hist[c // 2] = hist.get(c // 2, 0) + 1
                if c == 2:
                    ones.append((p, sq * q))
    print("\nq22 #cyl(DP) histogram, max(p,q)<=14, both signs:", sorted(hist.items()))
    print("q22 one-cylinder directions:", ones)

    # X by brute force
    dirs = [(4, 7), (7, 4)]
    den = 2 * 7 * 4
    X = []
    for i, j in product(range(den), repeat=2):
        s1, s2 = Fr(i, den), Fr(j, den)
        if all((q * s1 - p * s2).denominator == 1 and (q * s1 + p * s2).denominator == 1 for p, q in dirs):
            X.append((s1, s2))
    print("\nX mod Z^2 (brute force over (1/56)Z^2, which contains X by the 2q s1, 2p s2 bound):",
          [(str(a), str(b)) for a, b in X])

    # leaves through the lifts of the marks
    print("\nleaves through lifts of the marks (lift = lower-left corner of a square):")
    for mark in [(0, 0), (2, 2)]:
        for p, q in [(4, 7), (7, 4)]:
            res = []
            for e in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
                c = (mark[0] - (1 - e[0]) // 2, mark[1] - (1 - e[1]) // 2)
                i = S.idx[(c, e)]
                assert S.corner_room_point(i, 0, 0) == mark
                res.append("regular" if S.leaf_regular(p, q, i, Fr(0)) else "singular")
            print(f"  mark {mark}, direction ({p},{q}): {res}")


if __name__ == "__main__":
    main()
