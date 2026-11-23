"""d66: exact integer billiards (d62 billiard.shoot, no permutations) on the R* rows of pair_level.

For each listed (room, S, T): for each direction class x in {b, c, d}, the set of copy bits on
arrival at T over all primitive (p, q) with max(p, q) <= H and all four sign choices. An empty
set means no billiard witness of class x up to H (consistent with an orbit x-dark verdict).
Usage: python3 -B billiard_check.py H
"""
import json
import resource
import sys
from math import gcd
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = HERE.parent
sys.path.insert(0, str(D / 'd62-review-d61'))
sys.path.insert(0, str(D / 'd10-mechanisms'))
from billiard import shoot  # noqa: E402
from roomtools import lattice_points  # noqa: E402

resource.setrlimit(resource.RLIMIT_CPU, (120, 120))
XN = {(1, 0): 'b', (1, 1): 'c', (0, 1): 'd'}
CASES = [('cov4181', (2, 3), (4, 3)), ('cov4269', (3, 2), (3, 4)), ('cov80', (1, 2), (3, 2)),
         ('cov82', None, None), ('cov137', None, None)]

if __name__ == '__main__':
    H = int(sys.argv[1])
    rooms = [r for r in json.load(open(D / 'd64-finite-case' / 'data' / 'covers.json'))['rooms']
             if r['normalized']]
    rooms.sort(key=lambda r: (r['n'], r['cells']))
    rows = json.load(open(HERE / 'pair_level.json'))['dark_rows']
    dirs = [(p, q) for p in range(H + 1) for q in range(H + 1) if gcd(p, q) == 1]
    for name, S, T in CASES:
        if S is None:
            r0 = next(r for r in rows if r['room'] == name)
            S, T = tuple(r0['S']), tuple(r0['T'])
        cells = set(tuple(c) for c in rooms[int(name[3:])]['cells'])
        lim = 8 * len(lattice_points(cells)) + 8
        out = {}
        for x in 'bcd':
            C = set()
            for p, q in dirs:
                if XN[(p % 2, q % 2)] != x:
                    continue
                for sx in (1, -1):
                    for sy in (1, -1):
                        for Tt, c in shoot(cells, S, p, q, sx, sy, {T}, lim):
                            C.add(c)
            out[x] = sorted(C)
        orbit_dark = sorted({r['x'] for r in rows if r['room'] == name and tuple(r['S']) == S
                             and tuple(r['T']) == T})
        print(name, S, T, 'billiard copy bits per class:', out, 'orbit x-dark rows at:', orbit_dark, flush=True)
