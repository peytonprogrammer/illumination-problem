#!/usr/bin/env python3
"""allpairs.py ROOMFILE AXIS CB G -> orbitc problem with ALL interior lattice points of the stretched room as sources."""
import sys
from stretch import load, stretch
cells = load(sys.argv[1]); ax, cb, g = map(int, sys.argv[2:5])
out, _ = stretch(cells, ax, cb, g); S = set(out)
pts = [(X, Y) for X in range(60) for Y in range(60) if all((X-a, Y-b) in S for a in (0, 1) for b in (0, 1))]
print(len(out), " ".join(f"{x} {y}" for x, y in out), "|", len(pts), " ".join(f"{x} {y}" for x, y in pts))
