#!/usr/bin/env python3
"""Spot check of Lemma A' at boundary cases, by exact shooting.

For a room, a direction (p, q) and a random generic source S, take every
D in Lambda(S) and every vertex T of a closed face of K_D (these are the
boundary cases: T on singular lines, at lattice points, on cell edges). If T is
an interior point, T != S, Lemma A' says S illuminates T. The shooter
(shoot.py, two tracers) must find a path.

usage: python3 spotcheck.py NSRC R
"""
import random
import sys
from fractions import Fraction as Fr
from math import gcd

sys.path.insert(0, "../d3-review")
from ill import Dir  # noqa: E402
from shoot import shoot  # noqa: E402
from validate_x import interior  # noqa: E402

random.seed(7)


def main():
    nsrc, R = int(sys.argv[1]), int(sys.argv[2])
    from surface import q22_cells
    rooms = {
        "A6a": [(0, 0), (0, 1), (0, 2), (0, 3), (1, 1), (1, 2)],
        "A7": [(0, 0), (1, 0), (0, 1), (0, 2), (1, 2), (0, 3), (1, 3)],
        "cross": [(x, y) for x in range(4) for y in (1, 2)] + [(1, 0), (2, 0), (1, 3), (2, 3)],
        "q22": sorted(q22_cells()),
    }
    tot = lit = 0
    for nm, cells in rooms.items():
        cells = frozenset(cells)
        for _ in range(nsrc):
            p, q = random.choice([(p, q) for p in range(1, 5) for q in range(1, 5) if gcd(p, q) == 1])
            D = Dir(cells, p, q)
            c = random.choice(sorted(cells))
            S = (c[0] + Fr(random.randint(1, 96), 97), c[1] + Fr(random.randint(1, 96), 97))
            lam = D.lam(S)
            Ts = set()
            for cc in cells:
                for (V, lp, lm, _) in D.facepolys[cc]:
                    if lp in lam or lm in lam:
                        Ts |= {P for P in V if P != S and interior(cells, P[0], P[1])}
            Ts = random.sample(sorted(Ts), min(6, len(Ts)))
            for T in Ts:
                d, tried = shoot(cells, S, T, R)
                tot += 1
                lit += d is not None
                if d is None:
                    print("NOTFOUND", nm, (p, q), S, T, flush=True)
        print(nm, "pairs", tot, "lit", lit, flush=True)


if __name__ == "__main__":
    main()
