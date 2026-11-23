"""d69: cross-check decomp.trace (no forbidden flips) against d66 g1_check.shoot on fixed
direction lists (max(p, q) <= 5), same-class interior pairs, a few rooms.  Not a witness search:
both tracers see the same finite list, and only agreement is reported.
Usage: python3 -B crosscheck.py
"""
import sys
from math import gcd
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'd66-pair-level'))
import g1_check as G  # noqa: E402
import decomp  # noqa: E402

rooms = decomp.handbuilt()
named = decomp.cells_of(None)
agree = dis = hits = 0
for name in ('DB55', 'U2', 'c4181s', 'dumb12', 'cross12', 'R22'):
    cells = rooms.get(name) or named[name]
    lim = 8 * len(decomp.lattice_points(cells)) + 8
    for S, T in decomp.same_class_pairs(cells):
        for p in range(6):
            for q in range(6):
                if gcd(p, q) != 1:
                    continue
                for sx in (1, -1):
                    for sy in (1, -1):
                        a = bool(G.shoot(cells, S, p, q, sx, sy, {T}, lim, parity=0))
                        b = decomp.trace(cells, S, T, p, q, sx, sy, lim, set())
                        agree += a == b
                        dis += a != b
                        hits += a
print('agree', agree, 'disagree', dis, 'hits', hits)
