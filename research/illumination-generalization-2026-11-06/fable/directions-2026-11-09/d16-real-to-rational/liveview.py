#!/usr/bin/env python3
"""Summarize dpcover's live cells (DP_LIVE=1 dump on stdin).

For each live cell: the lattice point nearest to its first vertex average, and
the L-infinity radius of the cell around that point. Prints a histogram of
radii per dimension and the cells with radius above a threshold.

usage: DP_LIVE=1 ./dpcover B 1 MAXLIVE < room 2>&1 >/dev/null | python3 liveview.py THRESH_NUM THRESH_DEN
"""
import sys
from collections import Counter
from fractions import Fraction as Fr

th = Fr(int(sys.argv[1]), int(sys.argv[2]))
hist = Counter()
far = []
hosts_far = Counter()
n = 0
for line in sys.stdin:
    if not line.startswith("L "):
        continue
    tok = line.split()
    dim = int(tok[1])
    pts = []
    for z in tok[3:]:
        a, b = z.split(",")
        pts.append((Fr(a), Fr(b)))
    cx = sum(p[0] for p in pts[:3]) / min(len(pts), 3)
    cy = sum(p[1] for p in pts[:3]) / min(len(pts), 3)
    hx, hy = round(cx), round(cy)
    r = max(max(abs(p[0] - hx), abs(p[1] - hy)) for p in pts)
    n += 1
    hist[(dim, min(int(r * 20), 19))] += 1
    if r > th:
        hosts_far[(hx, hy, dim)] += 1
        if len(far) < 60:
            far.append((float(r), dim, int(tok[2]), [(float(p[0]), float(p[1])) for p in pts]))
print("live cells", n)
for dim in (0, 1, 2):
    print("dim", dim, "radius histogram (bins of 1/20):", [hist[(dim, k)] for k in range(20)])
print("cells with radius >", th, ":", sum(hosts_far.values()), "by (host, dim):", sorted(hosts_far.items()))
for f in far:
    print("  FAR r=%.4f dim=%d nQ=%d" % f[:3], " ".join("(%.4f,%.4f)" % p for p in f[3]))
