"""d52 step 3/4: which class-quotient triples co-occur in one room at r <= 8?

Collects every in-scope disc cover P (r <= 8, corners in >= 3 classes) over every admissible K,
dedupes P up to lattice isometry, and tabulates for each mark class a with >= 2 interior points:
the triple (delta_y, d_y, z_y) for y != a, and, per pair (S, T), how many of the three B_y
separate it. A positive would be a pair separated by all three.
Usage: python3 -B triples.py RMAX K_admissible.json
"""
import json
import sys
from collections import Counter
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from fold import *  # noqa
import enum_P  # noqa
from analyze_K import deltas  # noqa
from sanity import full_canon  # noqa

rmax = int(sys.argv[1])
adm = json.load(open(sys.argv[2]))
rooms = {}
for k in adm:
    K = [list(r) for r in k['canon']]
    for dl in deltas(k, rmax):
        coll = set()
        enum_P.covers(K, k['z'], dl, rmax, collect=coll)
        for P in coll:
            P = [list(r) for r in P]
            rooms.setdefault(full_canon(P), P)
print('distinct disc covers with r <= %d (up to lattice isometry): %d' % (rmax, len(rooms)))
sepcount = Counter()
triples = Counter()
triples_all_sep = Counter()
scope = true = 0
best = []
for P in rooms.values():
    prof = profile(P)
    if len([c for c, ts in prof.items() if 'cvx' in ts or 'rfx' in ts]) < 3:
        continue
    scope += 1
    tr = is_room(P)
    true += tr
    n = len(P[0])
    blks = {y: B(P, y) for y in CLASSES}
    dat = {}
    for y in CLASSES:
        K = quotient(P, blks[y])
        s = summary(profile(K))
        dat[y] = (n // len(K[0]), len(K[0]), s['z'])
    for a in CLASSES:
        pts = interior_points(P, a)
        if len(pts) < 2:
            continue
        ys = [y for y in CLASSES if y != a]
        key = tuple(sorted(dat[y] for y in ys))
        triples[key] += 1
        tabs = [separation_table(P, blks[y], a) for y in ys]
        mx = 0
        for i in range(len(pts)):
            for j in range(i + 1, len(pts)):
                c = sum(1 for tab in tabs if not (tab[i] & tab[j]))
                sepcount[(c, tr)] += 1
                mx = max(mx, c)
        if mx == 3:
            triples_all_sep[key] += 1
        if mx == 2:
            best.append((n, prof and summary(prof)['z'], tr, key))
print('in scope (>= 3 corner classes): %d, of which true strictly simple rooms: %d' % (scope, true))
print('mark pairs by number of classes y != a whose B_y separates the pair (count, true room):')
for k in sorted(sepcount):
    print('   separated in %d of 3 classes, true room=%s: %d pairs' % (k[0], k[1], sepcount[k]))
print('distinct (delta, d, z) triples for y != a, over (room, a) with >= 2 interior a-points: %d' % len(triples))
print('triples with all three separating some pair:', dict(triples_all_sep))
print('most common triples:')
for k, v in triples.most_common(12):
    print('   ', k, v)
print('true rooms with a pair separated in 2 of 3 classes: %d' % len([b for b in best if b[2]]))
for b in sorted(set(b for b in best if b[2]))[:10]:
    print('    n=%d r=%d triple=%s' % (b[0], b[1], b[3]))
