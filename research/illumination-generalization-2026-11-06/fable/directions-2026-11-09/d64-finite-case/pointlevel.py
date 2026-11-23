"""d64: point-level form of RL on rooms with a distinct-interior counterexample row.
A point pair (S != T interior, class a) is point-x-dark when every row (lift pair with equal N_x
image) of (S, T, x) is dark; lift pairs with different images are x-dark by R3. Reports point-x-dark
pairs whose dark rows lack a certificate. Usage: python3 -B pointlevel.py"""
import glob
import json
import time
from collections import defaultdict
import rl_test

t0 = time.process_time()
dark = []
for f in glob.glob('data/rl_*.json'):
    dark += [r for r in json.load(open(f))['special_rows'] if not r['lit']]
ids = sorted({r['room'] for r in dark if r['pA'] != r['pB'] and r['sA'] == r['sB'] == 'interior'})
rooms = [r for r in json.load(open('data/covers.json'))['rooms'] if r['normalized']]
rooms.sort(key=lambda r: (r['n'], r['cells']))
tot = defaultdict(int)
for idx in ids:
    rows, _ = rl_test.test_room(idx, [tuple(c) for c in rooms[idx]['cells']], None)
    g = defaultdict(list)
    for r in rows:
        if r['pA'] != r['pB'] and r['sA'] == r['sB'] == 'interior':
            g[(str(r['a']), r['x'], tuple(sorted((tuple(r['pA']), tuple(r['pB'])))))].append(r)
    for k, rs in g.items():
        tot['groups'] += 1
        if all(not r['lit'] for r in rs):
            tot['point_x_dark'] += 1
            if any(r['counterexample'] for r in rs):
                tot['point_x_dark_uncertified'] += 1
                print('point-level counterexample: room %d a=%s x=%s S,T=%s rows=%d' % (idx, k[0], k[1], k[2], len(rs)))
        elif any(not r['lit'] for r in rs):
            tot['mixed'] += 1
print('rooms', len(ids), dict(tot), 'CPU %.1f' % (time.process_time() - t0))
