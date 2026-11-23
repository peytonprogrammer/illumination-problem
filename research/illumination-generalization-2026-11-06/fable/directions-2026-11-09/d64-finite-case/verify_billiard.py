"""d64: exact-billiard cross-check of rl_test rows on selected rooms (no permutations).

For each room index, recompute every row with rl_test.test_room, group rows by (a, S, T, x), and
compare the number of x-lit lift pairs with d62 billiard.shoot over all primitive directions
(p, q), max(p, q) <= H, of class x. A lift pair with different N_x images is x-dark by R3, so
the orbit count is the number of lit rows. Billiard count: 2|C| (both interior), |C| (one
interior), [C nonempty] (both smooth), C = set of copy bits on arrival.
Usage: python3 -B verify_billiard.py H idx [idx ...]
"""
import sys
from collections import defaultdict
from math import gcd
from pathlib import Path
import json
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'd62-review-d61'))
import rl_test  # noqa: E402
from billiard import shoot  # noqa: E402
from roomtools import lattice_points, status  # noqa: E402

XN = {(1, 0): 'b', (1, 1): 'c', (0, 1): 'd'}

if __name__ == '__main__':
    H = int(sys.argv[1])
    rooms = [r for r in json.load(open(HERE / 'data' / 'covers.json'))['rooms'] if r['normalized']]
    rooms.sort(key=lambda r: (r['n'], r['cells']))
    tot_bad = tot_groups = 0
    for idx in map(int, sys.argv[2:]):
        cells = set(tuple(c) for c in rooms[idx]['cells'])
        rows, _ = rl_test.test_room(idx, sorted(cells), None)
        groups = defaultdict(lambda: [0, 0])
        for r in rows:
            S, T = tuple(r['pA']), tuple(r['pB'])
            if S == T:
                continue
            key = (min(S, T), max(S, T), r['x'])
            groups[key][0] += r['lit']
            groups[key][1] += 1
        dirs = [(p, q) for p in range(H + 1) for q in range(H + 1) if gcd(p, q) == 1]
        lim = 8 * len(lattice_points(cells)) + 8
        bad = 0
        for (S, T, x), (nlit, nrows) in groups.items():
            C = set()
            for p, q in dirs:
                if XN[(p % 2, q % 2)] != x:
                    continue
                for sx in (1, -1):
                    for sy in (1, -1):
                        for Tt, c in shoot(cells, S, p, q, sx, sy, {T}, lim):
                            C.add(c)
            iS, iT = status(cells, S) == 'interior', status(cells, T) == 'interior'
            mine = 2 * len(C) if (iS and iT) else (len(C) if (iS or iT) else int(bool(C)))
            if mine != nlit:
                bad += 1
                print('room %d %s %s x=%s orbit lit %d of %d rows, billiard %d' % (idx, S, T, x, nlit, nrows, mine))
        tot_bad += bad
        tot_groups += len(groups)
        print('room %d n=%d groups %d dark groups %d mismatches %d' % (
            idx, len(cells), len(groups), sum(1 for v in groups.values() if v[0] == 0), bad), flush=True)
    print('H=%d total groups %d mismatches %d' % (H, tot_groups, tot_bad))
