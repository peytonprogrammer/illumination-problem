"""d100: compare the independent tile-pair residual (cert2) with the census residual.

Usage: python3 -B compare.py RES_R0 RES_R1 CENSUS_REGIONS [NSAMPLE]

1. Open tile pairs: cert2's set vs eighteen-audit.txt's lists.
2. Box containment (load-bearing): every vertex of every cert2 product lies in the closed cells
   of an audited tile pair and within 1/17 of that pair's designated grid point at each end.
   Designated points come from cert2's own output and are then compared with the census.
3. Literal containment (evidence): random points of cert2 products, looked up in the closures
   of the census products.
"""
import random
import sys
from ast import literal_eval
from fractions import Fraction as F
from pathlib import Path

from compare_lib import load, load_census, in_census

HERE = Path(__file__).resolve().parent
CTX = HERE.parents[3]
audit = [l for l in (CTX / 'qclass-closure/offgrid/results/eighteen-audit.txt').read_text().splitlines()
         if l.startswith('cells ')]
ROOMS, AUDIT = [], []
for l in audit:
    coords, pairs = l[6:].split(' open tile pairs ')
    xy = list(map(int, coords.split()))
    ROOMS.append(list(zip(xy[::2], xy[1::2])))
    AUDIT.append(set(literal_eval(pairs)))
for r, line in enumerate((HERE / 'rooms.txt').read_text().splitlines()):
    xy = list(map(int, line.split()))[2:]
    assert sorted(zip(xy[::2], xy[1::2])) == ROOMS[r] == sorted(ROOMS[r])  # cert2 indexes sorted cells

for r, fn in enumerate(sys.argv[1:3]):
    print(f'room {r}:', [l.strip() for l in open(fn) if l.startswith('DONE')][0])
mine, centers = load(sys.argv[1:3], ROOMS)
bad = centers.pop(None)
myopen = [{(a, b) for rr, a, b, *_ in mine if rr == r} for r in range(2)]
for r in range(2):
    print(f'room {r}: d100 open tile pairs {len(myopen[r])}, census {len(AUDIT[r])}, '
          f'd100 not in census {sorted(myopen[r] - AUDIT[r])}, census not in d100 {sorted(AUDIT[r] - myopen[r])}')
print('tile-pair ends without a unique grid point within 1/17:', len(bad), bad[:5])
maxdev = F(0)
for r, a, b, src, P, W in mine:
    tgt = b if src == a else a
    for cell, poly in ((src, P), (tgt, W)):
        g = centers.get((r, a, b, cell))
        if g:
            maxdev = max(maxdev, max(max(abs(x - g[0]), abs(y - g[1])) for x, y in poly))
print(f'd100 products {len(mine)}; maximum displacement from designated point {maxdev}')

theirs, tcenters, nt = load_census(sys.argv[3])
print(f'census products {nt}; tile pairs {len({k[:3] for k in tcenters})}')
same = set(tcenters) == set(centers) and all(tcenters[k] == g for k, g in centers.items())
print('designated grid points equal to census:', same)
ok = same and not bad and maxdev <= F(1, 17) and all(myopen[r] <= AUDIT[r] for r in range(2))
print('BOX CONTAINMENT:', 'PASS' if ok else 'FAIL')

rng = random.Random(100)


def sample(poly):
    w = [rng.randint(1, 1000) for _ in poly]
    t = sum(w)
    return (sum(F(c, t) * x for c, (x, _) in zip(w, poly)), sum(F(c, t) * y for c, (_, y) in zip(w, poly)))


NS = int(sys.argv[4]) if len(sys.argv) > 4 else 300
miss = 0
for _ in range(NS):
    r, a, b, src, P, W = mine[rng.randrange(len(mine))]
    tgt = b if src == a else a
    S, T = sample(P), sample(W)
    if not in_census(theirs, r, src, tgt, S, T):
        miss += 1
        if miss <= 5:
            print('NOT IN CENSUS PRODUCT', r, src, tgt, S, T)
print(f'literal containment sample: {NS} random d100 residual pairs, {NS - miss} inside a census product closure, {miss} outside')
assert ok
