#!/usr/bin/env python3
"""stretch.py -- explicit stretched rooms and cross-checks against orbitc (complete decider, area <= 40).
usage: stretch.py ROOMFILE AXIS CB G   -> prints orbitc problem line for row CB stretched to height G,
       with all skeleton interior lattice points as sources (moved with the band)."""
import sys
def load(fn):
    v = list(map(int, open(fn).read().split())); return [(v[1+2*i], v[2+2*i]) for i in range(v[0])]
def stretch(cells, ax, cb, g):
    if ax: cells = [(y, x) for x, y in cells]
    out = []
    for x, y in cells:
        if y < cb: out.append((x, y))
        elif y > cb: out.append((x, y + g - 1))
        else: out += [(x, y + j) for j in range(g)]
    S = set(cells)
    pts = [(X, Y) for X in range(40) for Y in range(40) if all((X-a, Y-b) in S for a in (0, 1) for b in (0, 1))]
    pts = [(X, Y if Y <= cb else Y + g - 1) for X, Y in pts]
    return out, pts
if __name__ == "__main__":
    cells = load(sys.argv[1]); ax, cb, g = map(int, sys.argv[2:5])
    out, pts = stretch(cells, ax, cb, g)
    print(len(out), " ".join(f"{x} {y}" for x, y in out), "|", len(pts), " ".join(f"{x} {y}" for x, y in pts))
