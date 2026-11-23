"""Fixed-polygon check for Proposition R1 (no room search).

The L-tromino stretched by 3 along x has 9 cells. Its vertices occupy all four parity
classes, and the gcd of its horizontal edge lengths is 3. The script lists every factor
of its double and marks the pillowcase factors. A proper pillowcase factor shows that
"corners occupy three parity classes" cannot replace "gcd 1 per axis" in R1.

Run: python3 -B room_r1.py
"""
from lib import all_block_systems
from check_u import Fac, is_pillowcase
from room_r4 import room_tuple

for name, cells in (('L-tromino (normalized, control)', [(0, 0), (1, 0), (0, 1)]),
                    ('L-tromino stretched by 3 along x', [(i, 0) for i in range(6)] + [(i, 1) for i in range(3)])):
    cl, idx, t, k = room_tuple(set(cells))
    n = len(cl)
    pts = {(i + dx, j + dy) for (i, j) in cells for dx in (0, 1) for dy in (0, 1)}
    star = lambda p: sum(1 for c in ((p[0] - 1, p[1] - 1), (p[0], p[1] - 1), (p[0] - 1, p[1]), p) if c in cells)
    corner_classes = sorted({(p[0] % 2, p[1] % 2) for p in pts if star(p) in (1, 3)})
    print(f'== {name}: {n} cells; parity classes of the corners: {corner_classes}')
    for w in all_block_systems(t):
        F = Fac(t, w)
        print(f'   factor of degree {F.m}: types', [sorted(F.len[y], reverse=True) for y in range(4)],
              '| pillowcase:', is_pillowcase(F))
