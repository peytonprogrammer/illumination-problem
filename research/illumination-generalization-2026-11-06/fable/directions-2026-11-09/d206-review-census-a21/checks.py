"""Read-only re-aggregation of d205 outputs (a21 and parity-gap), written fresh."""
from collections import Counter
from hashlib import sha256
from pathlib import Path
import json
here = Path(__file__).resolve().parent
D = here.parent / 'd205-census-a21'
D9 = here.parent / 'd9-census-w22'
A001168 = [1, 2, 6, 19, 63, 216, 760, 2725, 9910, 36446, 135268, 505861, 1903890, 7204874, 27394666,
           104592937, 400795844, 1540820542, 5940738676, 22964779660, 88983512783]
out = {}

def parse(f):
    lines = f.read_text().splitlines()
    assert lines[-1] == '# DONE'
    rooms, elig, exp, shot, fixed = Counter(), Counter(), Counter(), {}, Counter()
    for l in lines:
        v = l.split()
        if v[:2] == ['#', 'fixed']: fixed[int(v[3])] += int(v[4])
        if v[:2] == ['#', 'count']: rooms[int(v[3]), int(v[5])] += int(v[7]); elig[int(v[3]), int(v[5])] += int(v[9])
        if v[0] == 'EXPECT': exp[int(v[1]), int(v[2])] += int(v[3])
        if v[0] == 'SHOT': shot[int(v[1]), int(v[2])] = tuple(map(int, v[3:]))
    return rooms, elig, exp, shot, fixed

# ---- area 21 ----
man = json.loads((D / 'a21/manifest.json').read_text())
R, E, X, S, FX = Counter(), Counter(), Counter(), Counter(), Counter()
same = diff = surv = 0
for i in range(man['shards']):
    f = D / f'a21/{i}.counts'
    rec = json.loads((D / f'a21/{i}.done.json').read_text())
    assert rec['counts_sha256'] == sha256(f.read_bytes()).hexdigest()
    assert (D / f'a21/{i}.sv').read_text() == '' and (D / f'a21/{i}.err').read_text() == ''
    rooms, elig, exp, shot, fixed = parse(f)
    for k, (e, s, d, u) in shot.items():
        assert elig[k] == e and exp[k] == s + d and u == 0, (i, k)
    assert {k for k, v in elig.items() if v} == set(shot) and set(exp) == {k for k in shot if shot[k][1] + shot[k][2]}
    R.update(rooms); FX.update(fixed)
    for k, (e, s, d, u) in shot.items(): same += s; diff += d; surv += u
assert all(k[0] == 21 for k in R)
# Only shard 0 records prefix nodes (<11); nodes >= 11 are dealt disjointly by their size-11 ancestor.
fixed_ok = all(FX[n] == A001168[n-1] for n in range(1, 22))
tot = json.loads((D / 'a21/totals.json').read_text())
out['a21'] = dict(shards=man['shards'], rooms=sum(R.values()), same=same, different=diff, pairs=same+diff, survivors=surv,
                  fixed21=FX[21], fixed_matches_A001168=fixed_ok,
                  totals_json_agrees=(tot['rooms'], tot['same_pairs'], tot['different_pairs'], tot['survivors']) == (sum(R.values()), same, diff, surv),
                  rooms_by_W={w: R[21, w] for w in range(4, 21, 2)})
# ---- parity gap 17-20 ----
hist = Counter()
for f in (D9 / 'runs/a20').glob('job-*.counts'):
    for l in f.read_text().splitlines():
        v = l.split()
        if v[:2] == ['#', 'count'] and int(v[5]) <= 20: hist[int(v[3]), int(v[5])] += int(v[7])
d9same = Counter()
for key, row in json.loads((D9 / 'census_totals.json').read_text())['per_W_area'].items():
    w, a = map(int, key.split(','))
    if w <= 20:
        assert row['pairs'] == row['lit_by_shooting']
        d9same[a, w] += row['pairs']
pg = {}
for a in range(17, 21):
    man = json.loads((D / f'parity-gap/a{a}/manifest.json').read_text())
    R2, D2, SM = Counter(), Counter(), 0
    for i in range(man['shards']):
        f = D / f'parity-gap/a{a}/{i}.counts'
        rec = json.loads((D / f'parity-gap/a{a}/{i}.done.json').read_text())
        assert rec['counts_sha256'] == sha256(f.read_bytes()).hexdigest()
        assert (D / f'parity-gap/a{a}/{i}.sv').read_text() == ''
        rooms, elig, exp, shot, fixed = parse(f)
        for k, (e, s, d, u) in shot.items():
            assert s == 0 and u == 0 and exp[k] == d and elig[k] == e
        R2.update(rooms)
        for k, (e, s, d, u) in shot.items(): D2[k[1]] += d
    rooms_match = all(R2[a, w] == hist[a, w] for w in range(4, 21, 2))
    pg[a] = dict(shards=man['shards'], rooms=sum(R2.values()), different=sum(D2.values()), rooms_match_d9=rooms_match)
    if a == 20:
        all20 = Counter()
        for f in (D / 'validation').glob('[0-9]*.counts'):
            for l in f.read_text().splitlines():
                v = l.split()
                if v[0] == 'EXPECT': all20[int(v[2])] += int(v[3])
        pg[a]['same_plus_diff_equals_allpairs_by_W'] = all(d9same[20, w] + D2[w] == all20[w] for w in range(4, 21, 2))
        pg[a]['all_pairs_area20'] = sum(all20.values()); pg[a]['d9_same_area20'] = sum(v for k, v in d9same.items() if k[0] == 20)
out['parity_gap'] = pg
out['different_17_20'] = sum(v['different'] for v in pg.values())
# canonical-key check on sampled witness rooms, with an independent implementation of d205's key order
def key(cells):
    xs = [x for x, y in cells]; ys = [y for x, y in cells]
    w, h = max(xs) - min(xs) + 1, max(ys) - min(ys) + 1
    rows = [0] * h
    for x, y in cells: rows[y - min(ys)] |= 1 << (x - min(xs))
    return (w, h, tuple(rows))
T8 = [lambda x, y: (x, y), lambda x, y: (-x, y), lambda x, y: (x, -y), lambda x, y: (-x, -y),
      lambda x, y: (y, x), lambda x, y: (-y, x), lambda x, y: (y, -x), lambda x, y: (-y, -x)]
noncanon = rooms_seen = 0
seen = set()
for f in sorted((here / 'rerun').glob('*.wit')):
    for l in f.read_text().splitlines():
        v = list(map(int, l.split())); cells = list(zip(v[8::2], v[9::2]))
        k0 = key(cells)
        if k0 in seen: continue
        seen.add(k0); rooms_seen += 1
        if min(key([t(x, y) for x, y in cells]) for t in T8) != k0: noncanon += 1
out['sample_rooms_canonical'] = dict(distinct_rooms=rooms_seen, not_minimal=noncanon)
print(json.dumps(out, indent=1))
