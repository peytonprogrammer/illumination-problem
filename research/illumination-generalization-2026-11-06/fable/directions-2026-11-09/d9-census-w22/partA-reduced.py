#!/usr/bin/env python3
"""Map every reduced (non-normalized) room to its normalized form.

A room whose corner x-differences have gcd gx and y-differences gcd gy is
diag(gx, gy) applied to a normalized room R of area A / (gx * gy).  This
script builds all such images from the normalized rooms of area <= AMAX / 2,
removes duplicates up to the 8 lattice symmetries, and counts them per
(W, area) and per certificate class of R.

Usage: partA-reduced.py ALLROOMS C3ROOMS AMAX
  ALLROOMS: "area W x y ..." lines with every room of area <= AMAX / 2
  C3ROOMS:  rooms file of partA-cert (lines "C3 area W x y ...")
"""
import sys, os
from math import gcd
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from check_enum_small import canon


def corners(cells):
    cnt = Counter()
    for x, y in cells:
        for dx in (0, 1):
            for dy in (0, 1):
                cnt[(x + dx, y + dy)] += 1
    return [p for p, k in cnt.items() if k in (1, 3)]


def parse(t):
    a = int(t[0]); xs = list(map(int, t[2:2 + 2 * a]))
    return a, int(t[1]), [(xs[2 * i], xs[2 * i + 1]) for i in range(a)]


allf, c3f, amax = sys.argv[1], sys.argv[2], int(sys.argv[3])
c3 = set()
for l in open(c3f):
    t = l.split()
    if t[0] == "C3":
        a, W, cells = parse(t[1:])
        c3.add(canon(cells))
seen = {}
for l in open(allf):
    t = l.split()
    a, W, cells = parse(t)
    if 2 * a > amax:
        continue
    cor = corners(cells)
    x0, y0 = cor[0]
    gx = gy = 0
    for x, y in cor:
        gx = gcd(gx, x - x0); gy = gcd(gy, y - y0)
    if gx > 1 or gy > 1:
        continue
    cls = "iii" if canon(cells) in c3 else "i/ii"
    for sx in range(1, amax + 1):
        for sy in range(1, amax + 1):
            if (sx, sy) == (1, 1) or a * sx * sy > amax:
                continue
            img = [(x * sx + i, y * sy + j) for x, y in cells for i in range(sx) for j in range(sy)]
            seen[canon(img)] = (W, a * sx * sy, cls)
tab = Counter(seen.values())
for k in sorted(tab):
    print("W %d area %d normal-form class %s rooms %d" % (k[0], k[1], k[2], tab[k]))
print("total reduced rooms", len(seen), "with normal form in class iii", sum(v for k, v in tab.items() if k[2] == "iii"))
