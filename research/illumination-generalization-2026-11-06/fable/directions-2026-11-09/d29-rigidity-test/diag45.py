#!/usr/bin/env python3
"""Run check for the 12 clean 24-wall 45-degree dark rooms of d11 (S=(0,2), T=(0,6))."""
import re, sys
from runs_poly import runs
txt = open(sys.argv[1]).read()
rows = [l for l in txt.splitlines() if l.startswith("| `2_0-") and "parity-W24" in l]
for l in rows:
    name = re.search(r"parity-W24-\d+", l).group(0)
    poly = [tuple(map(int, m)) for m in re.findall(r"\((-?\d+),(-?\d+)\)", l.split("|")[3])]
    if not poly: continue
    r = runs(poly, (0, 2), (0, 6))
    ys = [p[1] for p in poly]; xs = [p[0] for p in poly]
    print(name, "W", len(poly), "box", max(xs)-min(xs), "x", max(ys)-min(ys),
          "run rows", r["rows"][0], "run cols", r["cols"][0],
          "vertex-free rows", r["rows"][1], "vertex-free cols", r["cols"][1])
