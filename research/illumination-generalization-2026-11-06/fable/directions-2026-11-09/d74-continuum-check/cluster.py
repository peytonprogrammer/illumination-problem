"""d74: group the live residue of a cert run (D74ALL=1 output) by nearest lattice point, and list
which groups are mutual partners.  Usage: python3 -B cluster.py LOG"""
import sys
from fractions import Fraction as F
from collections import Counter, defaultdict
grp = {}
cnt = Counter()
part = {}
for line in open(sys.argv[1]):
    if not line.startswith('PIECE'):
        continue
    head, tail = line.split('|')
    h = head.split()
    pid, dim = int(h[1]), int(h[3])
    pts = [tuple(F(u) for u in t.split(',')) for t in h[4:]]
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    g = (round((min(xs) + max(xs)) / 2), round((min(ys) + max(ys)) / 2))
    grp[pid] = g
    cnt[g] += 1
    part[pid] = [int(u) for u in tail.split()[1:-1]]
print('groups', dict(cnt))
pairs = Counter()
for a, ps in part.items():
    for b in ps:
        if b in grp:
            pairs[tuple(sorted((grp[a], grp[b])))] += 1
print('mutual group pairs (from first <=12 partners per piece):')
for k, v in sorted(pairs.items()):
    print('  ', k, v)
