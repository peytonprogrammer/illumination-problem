"""Machine checks for theorem.md. Exact arithmetic (rooms.py). Writes verify-results.json.

V1  Classification table and proved bounds for every allowed triangle with n <= NMAX.
V2  Dead triangles (largest angle >= 2 pi/3): no tile can be attached to the star.
V3  Right triangles, n >= 8: the overlaps that kill every connection out of a full star.
V4  Shared B tip (obtuse): the forced two-star configuration is valid only for (n, b) = (8, 2).
V5  Explicit rooms: wall counts against the proved lower bounds.
"""
import json
import sys
import time

from rooms import Geo, Invalid, analyze, obstruction_classes, tau_fixed_classes, tiles_overlap
from build import arc_family, complete_right, skeletons, two_star

NMAX = 40
out = {}


def kind(n, b):
    """Type and proved lower bound (None = no room with two interior A points)."""
    c = n - 1 - b
    assert b < c
    if 3 * c >= 2 * n:
        return 'dead', None
    if 2 * c == n:
        if n == 4:
            return 'right', 22
        if n == 6:
            return 'right', 26
        return 'right-dead', None
    if (n, b) == (8, 2):
        return 'obtuse-45', 32
    if 3 * b == n:
        return 'obtuse-60', 4 * n
    assert n % b != 0
    return 'obtuse-generic', 4 * n + 2


# ---- V1 ---------------------------------------------------------------------
rows = []
for n in range(4, NMAX + 1, 2):
    for b in range(1, n // 2):
        k, bound = kind(n, b)
        rows.append(dict(n=n, b=b, c=n - 1 - b, type=k, bound=bound,
                         E=sorted(obstruction_classes(n, b)), tau_fixed=sorted(tau_fixed_classes(n, b))))
live = [r for r in rows if r['bound'] is not None]
ok1 = all(r['tau_fixed'] for r in rows)                       # some class always obstructs
ok1 &= all(set(r['E']) <= set(r['tau_fixed']) for r in rows)
# among triangles that admit two interior A points, cleanliness constrains only right triangles and (8, 2)
ok1 &= all((r['E'] != []) == (2 * r['c'] == r['n'] or (r['n'], r['b']) == (8, 2))
           for r in rows if r['type'] != 'dead')
min6 = min(r['bound'] for r in live if r['n'] >= 6)
min6_other = min(r['bound'] for r in live if r['n'] >= 6 and (r['n'], r['b']) != (6, 2))
out['V1'] = dict(PASS=bool(ok1 and min6 == 26 and min6_other == 32), triangles=len(rows), live=len(live),
                 min_bound_n_ge_6=min6, min_bound_n_ge_6_excluding_306090=min6_other,
                 live_table=[(r['n'], r['b'], r['c'], r['type'], r['bound']) for r in live if r['n'] <= 24])

# ---- V2 ---------------------------------------------------------------------
ok2, cnt2 = True, 0
for n in range(6, 22, 2):
    for b in range(1, n // 2):
        if kind(n, b)[0] != 'dead':
            continue
        g = Geo(n, b)
        star = g.star(g.base)
        analyze(g, star)
        for t in star:
            cnt2 += 1
            try:
                analyze(g, star + [g.reflect_tile(t, 0)])
                ok2 = False
            except Invalid:
                pass
out['V2'] = dict(PASS=ok2, attachments_tested=cnt2)

# ---- V3 ---------------------------------------------------------------------
ok3, rows3 = True, []
for n in range(6, NMAX + 1, 2):
    b = n // 2 - 1
    g = Geo(n, b)
    base = g.base                              # (S, B, C_i)
    tau_i = g.reflect_tile(base, 0)            # third tile at C_i, near B
    ups = g.reflect_tile(tau_i, 2)             # across spoke M_i - B
    w_near = g.reflect_tile(ups, 0)            # across B - C'
    ups2 = g.reflect_tile(ups, 1)              # across spoke M_i - C'
    w_far = g.reflect_tile(ups2, 0)
    base2 = g.reflect_tile(base, 2)            # the other star tile at B: (S, B, C_{i+1})
    N = g.reflect_tile(base2, 0)
    F = g.reflect_tile(g.reflect_tile(base2, 1), 0)
    ov = {a + '-' + c: tiles_overlap(g, x, y) for a, x in (('N', N), ('F', F)) for c, y in (('wnear', w_near), ('wfar', w_far))}
    five_tiles_impossible = 5 * b >= 2 * n
    if n == 6:
        good = not any(ov.values())            # the hexagon tiling: no conflict
    elif n == 8:
        good = all(ov.values()) and not five_tiles_impossible
    else:
        good = five_tiles_impossible and ov['F-wfar']
    ok3 &= good
    rows3.append(dict(n=n, overlaps=ov, five_tiles_at_B_impossible=five_tiles_impossible, as_claimed=good))
out['V3'] = dict(PASS=ok3, rows=rows3)

# ---- V4 ---------------------------------------------------------------------
ok4, rows4 = True, []
for n in range(8, NMAX + 1, 2):
    for b in range(1, n // 2):
        if not kind(n, b)[0].startswith('obtuse') or 3 * b >= n:
            continue
        g = Geo(n, b)
        try:
            r = analyze(g, two_star(g))
            res = 'valid, %d walls' % r['walls']
            good = (n, b) == (8, 2) and r['walls'] == 32 and r['clean'] and len(r['interior_A']) == 2
        except Invalid as e:
            res = 'invalid: %s' % e
            good = (n, b) != (8, 2)
        ok4 &= good
        rows4.append((n, b, res))
out['V4'] = dict(PASS=ok4, rows=rows4)

# ---- V5 ---------------------------------------------------------------------
rows5, ok5 = [], True
t0 = time.time()
for n, b in [(6, 2), (8, 2), (10, 3), (12, 4), (14, 4), (14, 5), (16, 5), (16, 6), (18, 6), (20, 8)]:
    g = Geo(n, b)
    k, bound = kind(n, b)
    fam = arc_family(g)
    w = fam[0]['walls'] if fam else None
    row = dict(n=n, b=b, c=g.c, type=k, proved_lower_bound=bound, arc_family_walls=w,
               arc_tiles=(fam[1] + 1) if fam else None,
               corner_types=fam[0]['corner_types'] if fam else None,
               flat=fam[0]['flat'] if fam else None, interior=fam[0]['interior'] if fam else None,
               sharp=(w == bound))
    ok5 &= w is not None and w >= bound
    rows5.append(row)
# 45-45-90: arc family with one third tile per C tip, all completions checked
g = Geo(4, 1)
best4 = None
for j, first, K in skeletons(g):
    r = complete_right(g, K, max_full=10 ** 6)
    if r and (best4 is None or r['walls'] < best4['walls']):
        best4 = r
rows5.append(dict(n=4, b=1, c=2, type='right', proved_lower_bound=22,
                  arc_family_walls=best4['walls'] if best4 else None,
                  corner_types=best4['corner_types'] if best4 else None))
ok5 &= best4 is not None and best4['walls'] >= 22
# 45-45-90, shared corner (x = 1): the 18-tile skeleton has no clean completion with one third tile per C tip
shared4 = complete_right(g, two_star(g), max_full=10 ** 6)
rows5.append(dict(n=4, b=1, type='right, shared-corner skeleton', arc_family_walls=shared4['walls'] if shared4 else None))
ok5 &= shared4 is None
# right triangles n >= 8: the arc family must be empty
for n in (8, 10, 12):
    g = Geo(n, n // 2 - 1)
    fam = arc_family(g)
    rows5.append(dict(n=n, b=n // 2 - 1, type='right-dead', arc_family_walls=fam[0]['walls'] if fam else None))
    ok5 &= fam is None
out['V5'] = dict(PASS=ok5, seconds=round(time.time() - t0, 1), rows=rows5)

out['ALL_PASS'] = all(v['PASS'] for v in out.values() if isinstance(v, dict))
json.dump(out, open('verify-results.json', 'w'), indent=1)
for k, v in out.items():
    print(k, v['PASS'] if isinstance(v, dict) else v)
for r in out['V5']['rows']:
    print('  ', r)
