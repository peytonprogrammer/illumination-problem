#!/usr/bin/env python3
"""Decide pairs with the twists (invariance of DP illumination under <h, v>).

stdin: lines "UNDECIDED x,y;x,y ..." from gridcheck.py. For each pair (S, T)
and each class, the script walks the <h, v>-orbit of the pair of lifts on M
(breadth first, at most MAXORB elements). The room pair is lit as soon as one
image pair is lit in its class: by a cylinder certificate (either point as the
source), or by the class-restricted two-tracer shooter with radius R when both
image points are interior.

The action of h and v on M is dplib.twist.

usage: python3 twistcheck.py rooms.txt ROOM_INDEX B R MAXORB < undecided
"""
import sys
from collections import deque
from fractions import Fraction as Fr

from dplib import Cert, canon, is_interior, is_vertex, read_rooms, shoot_class, twist, twist_periods
from shoot import MSurf


def main():
    cells = read_rooms(sys.argv[1])[int(sys.argv[2]) - 1]
    B, R, MAXORB = int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    LH, LV = twist_periods(cells)
    C = Cert(cells, B)
    M = MSurf(cells)
    gens = [("h", True, LH, 1), ("H", True, LH, -1), ("v", False, LV, 1), ("V", False, LV, -1)]
    nlit = nund = 0
    for line in sys.stdin:
        if not line.startswith("UNDECIDED"):
            continue
        a, b = line.split()[1].split(";")
        S = tuple(Fr(z) for z in a.split(","))
        T = tuple(Fr(z) for z in b.split(","))
        verdict = None
        sizes = []
        for cls in (0, 1):
            start = ((S[0], S[1], 1, 1), (T[0], T[1], 1, 1 if cls == 0 else -1))
            seen = {start: ""}
            dq = deque([start])
            while dq and verdict is None:
                ps, pt = dq.popleft()
                word = seen[(ps, pt)]
                S2, T2 = (ps[0], ps[1]), (pt[0], pt[1])
                c2 = 0 if ps[2] * ps[3] * pt[2] * pt[3] == 1 else 1
                assert not is_vertex(cells, S2) and not is_vertex(cells, T2)
                if S2 != T2:
                    d = C.one_sided(S2, T2, c2) or C.one_sided(T2, S2, c2)
                    if d:
                        verdict = f"class {cls} word '{word}' image {S2[0]},{S2[1]};{T2[0]},{T2[1]} class {c2} cylinder {d[0]},{d[1]}"
                    elif is_interior(cells, S2) and is_interior(cells, T2):
                        v = shoot_class(cells, S2, T2, R, c2, M)
                        if v:
                            verdict = f"class {cls} word '{word}' image {S2[0]},{S2[1]};{T2[0]},{T2[1]} class {c2} path {v[0]},{v[1]}"
                if verdict is None and len(seen) < MAXORB:
                    for name, hor, lam, sg in gens:
                        nxt = (canon(cells, twist(cells, ps, hor, lam, sg)), canon(cells, twist(cells, pt, hor, lam, sg)))
                        if nxt not in seen:
                            seen[nxt] = word + name
                            dq.append(nxt)
            sizes.append(len(seen))
            if verdict:
                break
        if verdict:
            nlit += 1
            print(f"LIT {a};{b} {verdict}", flush=True)
        else:
            nund += 1
            print(f"UNDECIDED {a};{b} orbit elements visited {sizes}", flush=True)
    print(f"# lit {nlit} undecided {nund}")


if __name__ == "__main__":
    main()
