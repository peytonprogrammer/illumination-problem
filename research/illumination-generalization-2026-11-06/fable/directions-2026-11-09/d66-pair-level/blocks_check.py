"""d66: block systems and deck involutions of DP -> B for the R* rooms with a per-target failure.
Usage: python3 -B blocks_check.py
"""
import json
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
D = HERE.parent
sys.path.insert(0, str(D / 'd64-finite-case'))
sys.path.insert(0, str(D / 'd65-nx-equals-b'))
import rl_test  # noqa: E402,F401
from realize import d4, room_tuple, lattice_points, cycles  # noqa: E402
from rl_room import centraliser  # noqa: E402

cov = [r for r in json.load(open(D / 'd64-finite-case' / 'data' / 'covers.json'))['rooms'] if r['normalized']]
cov.sort(key=lambda r: (r['n'], r['cells']))
for k in (4181, 4269, 80, 82, 137):
    cells = set(map(tuple, cov[k]['cells']))
    o = lattice_points(cells)[0]
    room, t = room_tuple(cells, o)
    n = len(t[0])
    systems = [P for P in d4.all_block_systems(list(t), n) if 1 < len(P) < n]
    cen = [c for c in centraliser(t) if c != tuple(range(n))]
    print('cov%d n %d proper block systems %s deck group order %d cycle types %s' % (
        k, n, sorted(len(P) for P in systems), len(cen) + 1,
        [sorted((len(c) for c in cycles(g)), reverse=True) for g in t]))
