#!/usr/bin/env python3
"""Decide the pairs of interior candidate points left by orbitfilter.py.

For every unordered pair {S, T} of distinct interior candidates:
  1. cylinder certificate (directions 1 <= p, q <= B), either point as the
     source, either class;
  2. otherwise the exact two-tracer shooter of shoot.py with radii R1 < R2 ...

A pair that survives both steps is printed as UNDECIDED (a dark candidate; the
shooter cannot prove darkness).

The shooter skips directions that run along a lattice line (dplib.shoot2).

usage: python3 gridcheck.py rooms.txt ROOM_INDEX B candidates.txt R1,R2,... [PART NPARTS]
With PART and NPARTS, only every NPARTS-th uncertified pair is shot.
"""
import sys
from fractions import Fraction as Fr
from itertools import combinations

from dplib import Cert, read_rooms, shoot2
from shoot import MSurf


def main():
    cells = read_rooms(sys.argv[1])[int(sys.argv[2]) - 1]
    B = int(sys.argv[3])
    radii = [int(z) for z in sys.argv[5].split(",")]
    pts = []
    for line in open(sys.argv[4]):
        tok = line.split()
        if line.startswith("#") or len(tok) < 3 or tok[2] != "interior":
            continue
        pts.append((Fr(tok[0]), Fr(tok[1])))
    C = Cert(cells, B)
    # labels of every candidate in every direction, as a source and as a target
    src = {P: [C.source_labels(d, P) for d in C.dirs] for P in pts}
    tgt = {P: [C.target_labels(d, P) for d in C.dirs] for P in pts}

    def certified(S, T):
        for (lp, lm), (tp, tm) in zip(src[S], tgt[T]):
            if lp is not None and (lp in tp or lp in tm):
                return True
            if lm is not None and (lm in tm or lm in tp):
                return True
        return False

    npairs = ncert = 0
    rest = []
    for S, T in combinations(pts, 2):
        npairs += 1
        if certified(S, T) or certified(T, S):
            ncert += 1
        else:
            rest.append((S, T))
    print(f"# room {sys.argv[2]} interior candidates {len(pts)} pairs {npairs} certified {ncert} to shoot {len(rest)}", flush=True)
    if len(sys.argv) > 7:
        rest = rest[int(sys.argv[6])::int(sys.argv[7])]
    shot = {R: 0 for R in radii}
    und = []
    M = MSurf(cells)
    for S, T in rest:
        for R in radii:
            v, _ = shoot2(cells, S, T, R, M)
            if v is not None:
                shot[R] += 1
                print(f"LIT {S[0]},{S[1]};{T[0]},{T[1]} dir {v[0]},{v[1]} R {R}", flush=True)
                break
        else:
            und.append((S, T))
            print(f"UNDECIDED {S[0]},{S[1]};{T[0]},{T[1]} up to R {radii[-1]}", flush=True)
    print(f"# room {sys.argv[2]} lit by shooting per radius {shot} undecided {len(und)}")


if __name__ == "__main__":
    main()
