"""D87: independent replay of the nine R22 corner-support rows and the eps repair."""
from fractions import Fraction as F
from itertools import combinations
from math import gcd
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from billiard import run, incid

HERE = Path(__file__).resolve().parent
D8 = HERE.parent / 'd8-perturbation-test'

# R22 typed in from the d8 rooms.json picture, then compared with the archive.
ROWS = {2: [1, 2], 1: [0, 1, 2, 3], 0: [-1, 0, 3, 4], -1: [-1, 0], -2: [0, 1], -3: [1]}
R22 = {(x, y) for y, xs in ROWS.items() for x in xs}
arch = next(r for r in json.loads((D8 / 'rooms.json').read_text()) if r['id'] == 'R22-base')
assert R22 == {tuple(c) for c in arch['cells']}
S, T = (0, 0), (2, 2)

pts = {(x + i, y + j) for x, y in R22 for i in (0, 1) for j in (0, 1)}
reflex = sorted(p for p in pts if incid(R22, p) == 3)
convex = sorted(p for p in pts if incid(R22, p) == 1)
print('R22 reflex', reflex, 'count', len(reflex), 'convex count', len(convex), 'walls', len(reflex) + len(convex))
assert incid(R22, S) == 4 and incid(R22, T) == 4

rows = [
    ((0, -1), 'L2-0320', (-8, 11), (8, -11), 1, 3),
    ((0, 1), 'L1-004', (-2, 1), (-2, -1), 1, 1),
    ((1, -2), 'L1-027', (7, -4), (-7, -4), 1, 1),
    ((1, -1), 'L2-0210', (9, -5), (-9, 5), 1, 1),
    ((1, 1), 'L1-008', (1, 1), (-1, -1), 1, 1),
    ((1, 2), 'L1-000', (3, 2), (3, 2), 1, 1),
    ((3, 1), 'L2-0210', (9, 5), (9, 5), 1, 1),
    ((3, 2), 'L2-0398', (9, 2), (9, 2), 1, 1),
    ((4, 1), 'L1-021', (4, 7), (4, -7), 1, 1),
]
assert sorted(r[0] for r in rows) == reflex

records = {}
for line in (D8 / 'results.jsonl').read_text().splitlines():
    r = json.loads(line)
    records[r['id']] = r

sites = []
for C, src, vs, vt, i, j in rows:
    a = run(R22, S, vs, i + 1)          # run past the claimed step count; must stop at C
    b = run(R22, T, vt, j + 1)
    assert not a['ok'] and a['end'] == C and a['t'] == i and a['k'] == 3, (C, a)
    assert not b['ok'] and b['end'] == C and b['t'] == j and b['k'] == 3, (C, b)
    assert a['vel'] == tuple(-v for v in b['vel']), (a['vel'], b['vel'])
    # Straight continuation through C: cell behind (incoming) and cell ahead must both be room cells.
    vx, vy = a['vel']
    ahead = (C[0] if vx > 0 else C[0] - 1, C[1] if vy > 0 else C[1] - 1)
    behind = (C[0] - 1 if vx > 0 else C[0], C[1] - 1 if vy > 0 else C[1])
    assert ahead in R22 and behind in R22
    inner = [p for _, p, _ in a['hits']] + [p for _, p, _ in b['hits']]
    assert all(k in (2, 4) for _, p, k in a['hits'][:-1] + b['hits'][:-1])
    assert S not in inner and T not in inner
    site = set(inner)
    sites.append(site)
    # Provenance: the archived witness has the same slope up to signs.
    rec = records['R22-' + src]
    w = next(p['witness'] for p in rec['pairs'] if p['marks'])
    g = gcd(*w)
    prov = tuple(abs(c) // g for c in w) == tuple(map(abs, vs)) == tuple(map(abs, vt))
    cls = (vs[0] % 2, vs[1] % 2)
    print(f'{C} S-leg t={a["t"]} T-leg t={b["t"]} arrival {a["vel"]} / {b["vel"]} '
          f'sites {sorted(site)} incid {[k for _,_,k in a["hits"]+b["hits"]]} class {cls} '
          f'Cclass {(C[0]%2, C[1]%2)} provenance {prov} '
          f'midpoint-is-C {i == j}')
    assert prov and cls == (C[0] % 2, C[1] % 2)

assert all(x.isdisjoint(y) for x, y in combinations(sites, 2))
print('intermediate site sets pairwise disjoint; sizes', [len(s) for s in sites])


def repaired_route(C, vs, steps, N):
    """Scale R22 by N, fill the one missing cell at N*C, trace from N*S for N*steps."""
    big = {(N * x + u, N * y + v) for x, y in R22 for u in range(N) for v in range(N)}
    X, Y = N * C[0], N * C[1]
    quad = [(X + u, Y + v) for u in (-1, 0) for v in (-1, 0)]
    missing = [q for q in quad if q not in big]
    assert len(missing) == 1
    big.add(missing[0])
    assert incid(big, (X, Y)) == 4
    r = run(big, (0, 0), vs, steps * N)
    return r['ok'] and r['end'] == (F(N * T[0]), F(N * T[1])), r


print('\neps repair (eps = 1/N), whole route from S:')
for N in (11, 12, 13, 24):
    res = []
    for C, src, vs, vt, i, j in rows:
        ok, r = repaired_route(C, vs, i + j, N)
        res.append(ok)
        if not ok:
            print(f'  N={N} {C} fails: stop at {r["end"]} t={r.get("t")}')
    print(f'  N={N}: {sum(res)}/9 legal')


# Minimum wall-contact gap next to C, in original units, for each route.
print('\nnearest non-corner wall contact to C along C\'s two walls:')
for C, src, vs, vt, i, j in rows:
    a = run(R22, S, vs, i)
    b = run(R22, T, vt, j)
    best = None
    for c in a['contacts'] + b['contacts']:
        _, (px, py), kind = c
        px, py = F(px), F(py)
        if kind == 'V' and px == C[0]:
            d = abs(py - C[1])
        elif kind == 'H' and py == C[1]:
            d = abs(px - C[0])
        else:
            continue
        best = d if best is None else min(best, d)
    lim = F(1, max(map(abs, vs)))
    print(f'  {C} v={vs} nearest {best} (1/max|component| = {lim})')
