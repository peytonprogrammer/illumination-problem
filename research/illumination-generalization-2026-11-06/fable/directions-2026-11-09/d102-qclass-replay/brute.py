"""d102 completeness spot check: direct fixed-polyomino enumeration (Redelmeier) through area NMAX.

Keeps strictly simple polyominoes (connected, no holes, no pinch) with <= 20 walls, >= 2 interior
lattice points, and some parity class whose points in the closed room are all corners (1 or 3
cells). Reduces modulo the 8 square symmetries and compares per-area counts with the room list in
qclass-closure/witnesses.txt.gz. Shares no code with enumerate.cpp, independent.c or polyo.c.
Usage: python3 -B brute.py NMAX
"""
import gzip
import sys
from collections import Counter
from pathlib import Path

NMAX = int(sys.argv[1])
Q = Path(__file__).resolve().parents[4] / 'qclass-closure'


def canon(cells):
    best = None
    for sw in (0, 1):
        for fx in (1, -1):
            for fy in (1, -1):
                pts = [((y if sw else x) * fx, (x if sw else y) * fy) for x, y in cells]
                mx = min(p[0] for p in pts)
                my = min(p[1] for p in pts)
                t = tuple(sorted((a - mx, b - my) for a, b in pts))
                if best is None or t < best:
                    best = t
    return best


def qualifies(cells):
    cs = set(cells)
    deg = Counter()
    for x, y in cells:
        deg[(x, y)] += 1
        deg[(x + 1, y)] += 1
        deg[(x, y + 1)] += 1
        deg[(x + 1, y + 1)] += 1
    walls = interior = 0
    regular = set()   # parity classes containing a non-corner point of the closed room
    for (x, y), d in deg.items():
        if d == 2 and (((x - 1, y - 1) in cs) == ((x, y) in cs)):
            return False   # diagonal pair: pinch
        if d in (1, 3):
            walls += 1
        else:
            regular.add((x & 1, y & 1))
            interior += d == 4
    if walls > 20 or interior < 2 or len(regular) == 4:
        return False
    # holes: Euler characteristic V - E + F = 1 for a simply connected pinch-free cell complex
    V = len(deg)
    E = len({(x, y, 0) for x, y in cells} | {(x, y + 1, 0) for x, y in cells}
            | {(x, y, 1) for x, y in cells} | {(x + 1, y, 1) for x, y in cells})
    return V - E + len(cells) == 1


found = Counter()
seen = set()


def redelmeier(poly, untried, excluded):
    n = len(poly)
    if qualifies(poly):
        c = canon(poly)
        if c not in seen:
            seen.add(c)
            found[n] += 1
    if n == NMAX:
        return
    untried = list(untried)
    while untried:
        c = untried.pop()
        poly.append(c)
        new = []
        x, y = c
        for nb in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if (nb[1] > 0 or (nb[1] == 0 and nb[0] >= 0)) and nb not in excluded:
                new.append(nb)
        excl2 = excluded | set(new)
        redelmeier(poly, untried + new, excl2)
        poly.pop()
        excluded = excluded | {c}


redelmeier([], [(0, 0)], {(0, 0)})
census = Counter()
with gzip.open(Q / 'witnesses.txt.gz', 'rt') as f:
    for line in f:
        if line.startswith('R '):
            n = int(line.split()[2])
            if n <= NMAX:
                census[n] += 1
print('area brute census')
for n in range(1, NMAX + 1):
    print(n, found[n], census[n], 'ok' if found[n] == census[n] else 'MISMATCH')
