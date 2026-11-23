"""Cylinder decomposition of the room double in both axial directions, computed from the
cells (no hard-coded table). Least pointwise rim-fixing shear lambda = lcm over cylinders of
C/gcd(C,h), C = 2*width. Then checks that the twist shift lambda*j mod C is 0 at every
integral distance j from the lower rim, i.e. every lattice lift (front and back) is fixed."""
import sys
from math import gcd, lcm
from room import cells, marks, is_corner, is_reflex, boundary_cycle


def cylinders(C, transpose=False):
    if transpose:
        C = {(y, x) for (x, y) in C}
    rows = {}
    for (x, y) in C:
        rows.setdefault(y, set()).add(x)
    pieces = {}
    for y, xs in rows.items():
        xs = sorted(xs); L = xs[0]
        for i, x in enumerate(xs):
            if i + 1 == len(xs) or xs[i + 1] != x + 1:
                pieces[(y, L)] = x + 1
                if i + 1 < len(xs):
                    L = xs[i + 1]
    cyl = []
    used = set()
    for (y, L) in sorted(pieces):
        if (y, L) in used:
            continue
        R = pieces[(y, L)]; top = y + 1; used.add((y, L))
        while pieces.get((top, L)) == R and not any(is_corner(C, X, top) for X in range(L, R + 1)):
            used.add((top, L)); top += 1
        cyl.append((L, R, y, top))  # run [L,R], heights [y,top]
    return cyl


def analyse(l):
    C = cells(l)
    S, T, c = marks(l)
    poly = boundary_cycle(C)
    r = sum(is_reflex(C, *v) for v in poly)
    out = {"l": l, "n": len(C), "walls": len(poly), "reflex": r}
    for name, tr in (("H", False), ("V", True)):
        cyl = cylinders(C, tr)
        lam = lcm(*(2 * (R - L) // gcd(2 * (R - L), top - y) for (L, R, y, top) in cyl))
        moved = [(L, R, y, top, j) for (L, R, y, top) in cyl for j in range(top - y + 1)
                 if (lam * j) % (2 * (R - L))]
        out[name] = {"cyl(C,h,run,levels)": [(2 * (R - L), top - y, (L, R), (y, top)) for (L, R, y, top) in cyl],
                     "lambda": lam, "levels_moved": moved}
    out["S"], out["T"], out["c"] = S, T, c
    return out


if __name__ == "__main__":
    for l in map(int, sys.argv[1:]):
        o = analyse(l)
        print(f"l={l} n={o['n']} walls={o['walls']} reflex={o['reflex']} S={tuple(map(str,o['S']))} T={tuple(map(str,o['T']))}")
        for k in "HV":
            print(f"  {k}: lambda={o[k]['lambda']} lattice-levels moved={o[k]['levels_moved']}")
            print(f"     cylinders {o[k]['cyl(C,h,run,levels)']}")
