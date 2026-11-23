"""d67: fixed-polyomino count of d64's in-scope rooms (scope by indep.py's own B_x), per area,
for comparison with polyo.c. Usage: python3 -B compare.py polyo_n16.log"""
import json
import re
import sys
from collections import Counter
from indep import wset, nblocks, D64

D4 = [lambda x, y: (x, y), lambda x, y: (-x, y), lambda x, y: (x, -y), lambda x, y: (-x, -y),
      lambda x, y: (y, x), lambda x, y: (-y, x), lambda x, y: (y, -x), lambda x, y: (-y, -x)]


def orbit_size(cells):
    imgs = set()
    for f in D4:
        pts = [f(i, j) for i, j in cells]
        mx = min(p[0] for p in pts)
        my = min(p[1] for p in pts)
        imgs.add(frozenset((a - mx, b - my) for a, b in pts))
    return len(imgs)


fixed = Counter()
for r in json.load(open(D64 / 'data' / 'covers.json'))['rooms']:
    if not r['normalized']:
        continue
    cells = [tuple(c) for c in r['cells']]
    n = len(cells)
    G = wset(cells)
    if any(1 < nblocks(G, p, q) < n for p in (0, 1) for q in (0, 1)):
        fixed[n] += orbit_size(cells)
brute = {}
for line in open(sys.argv[1]):
    m = re.match(r'n (\d+) fixed \d+ rooms_fixed \d+ inscope_fixed (\d+)', line)
    if m:
        brute[int(m.group(1))] = int(m.group(2))
bad = 0
for n in sorted(brute):
    ok = brute[n] == fixed.get(n, 0)
    bad += not ok
    print('n %2d brute fixed in-scope %6d   d64 covers.json in-scope (fixed images) %6d  %s' % (
        n, brute[n], fixed.get(n, 0), 'ok' if ok else 'MISMATCH'))
print('mismatches', bad)
