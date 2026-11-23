"""Classify lit certificates by the class of the developed path's midpoint.

The parity argument (pi-rotation about the midpoint M of the developed segment
from S to T) needs M to be a point whose pi-rotation the factor N_min kills:
an A or B point for C pairs.  This script reads shoot45 per-pair lines
(CERTMAX large) and tallies, per class X and per N_min separation flag, the
class of M: A, B, C, or "half" (M is the centre of a unit square, m*(dx,dy)
odd in both coordinates).

usage: python3 -B cmid45.py shoot.out
"""
import sys
from collections import Counter


def mid_class(sx, sy, X, Y):
    if X % 2 and Y % 2:
        return 'half'
    if X % 2 or Y % 2:
        return 'edge'   # cannot happen for same-class pairs
    mx, my = sx + X // 2, sy + Y // 2
    return 'A' if mx % 2 == 0 and my % 2 == 0 else 'B' if mx % 2 and my % 2 else 'C'


def main():
    c = Counter()
    for line in open(sys.argv[1]):
        p = line.split()
        if not p or p[0] != 'P' or p[6] != 'L':
            continue
        sx, sy = int(p[2]), int(p[3])
        dx, dy, m = int(p[7]), int(p[8]), int(p[9])
        sep = int(p[p.index('sep') + 1])
        c[(p[1], sep, mid_class(sx, sy, m * dx, m * dy))] += 1
    print('class sep midpoint_class lit_pairs')
    for k, v in sorted(c.items()):
        print(*k, v)


if __name__ == '__main__':
    main()
