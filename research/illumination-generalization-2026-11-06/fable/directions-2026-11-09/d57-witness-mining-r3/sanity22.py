"""Sanity: the machinery must not certify the dark pair of the 22-wall room
(d38-review/check_named.py: vertices R22, S = (0, 0), T = (2, 2)).

Both points have even position types (they lie on grid lines), so the type
region is the 11-dim gap space (gx0 = 1); the dark pair sits at all gaps = 1.
(a) Mine at the exact point: no itinerary may pass the exact check.
(b) Mine at 20 nearby perturbed rooms; every itinerary found there must fail
    the exact check at the dark point and fail to certify on every box
    gap in [1 - 2^-k, 1 + 2^-k], k = 1..20, which contains the dark point.
(c) Run the box cover on gaps in [1 - 2^-6, 1 + 2^-6] with a cap; no
    certified box may contain the dark point."""
import json, random, time
from fractions import Fraction as Fr
import wm, bb, replay

R22 = [(-1, -1), (-1, 1), (0, 1), (0, 2), (1, 2), (1, 3), (3, 3), (3, 2), (4, 2), (4, 1), (5, 1),
       (5, 0), (3, 0), (3, 1), (1, 1), (1, -1), (2, -1), (2, -3), (1, -3), (1, -2), (0, -2), (0, -1)]
SC = bb.SC


def inside(px, py, poly):
    c = False
    for k in range(len(poly)):
        (x1, y1), (x2, y2) = poly[k], poly[(k + 1) % len(poly)]
        if (y1 > py) != (y2 > py) and px < x1 + (py - y1) * (x2 - x1) / (y2 - y1): c = not c
    return c


X = sorted({p[0] for p in R22}); Y = sorted({p[1] for p in R22})
cells = [(i, j) for i in range(len(X) - 1) for j in range(len(Y) - 1)
         if inside(X[i] + .5, Y[j] + .5, R22)]
ot = wm.OT(len(X) - 1, len(Y) - 1, cells)
S = (2 * X.index(0), 2 * Y.index(0)); T = (2 * X.index(2), 2 * Y.index(2))
par = wm.Param(ot, S, T)
print('walls', len(ot.walls), 'cells', len(cells), 'S type', S, 'T type', T, 'vars', len(par.names))
assert len(ot.walls) == 22
dark = [SC] * len(par.names)
pb = [(x, x) for x in dark]
t0 = time.process_time()
out = {}

# (a)
vals = {k: 1.0 for k in range(len(par.names))}
c = wm.mine(par, vals, nang=8000, maxref=20)
ok_exact = []
for it, sx, sy in c:
    conds, _ = wm.conditions(par, it, sx, sy)
    if wm.certify(conds, pb): ok_exact.append(it)
out['a_mined_candidates'] = len(c); out['a_exact_valid'] = len(ok_exact)

# (b)
rng = random.Random(3)
pool = {}
for _ in range(20):
    v = {k: (1.0 if par.names[k] == 'gx0' else 1 + rng.uniform(-.02, .02)) for k in range(len(par.names))}
    vi = [int(v[k] * SC) for k in range(len(par.names))]
    for it, sx, sy in wm.mine(par, v, nang=4000, maxref=14):
        conds, B = wm.conditions(par, it, sx, sy)
        if wm.certify(conds, [(x, x) for x in vi]): pool[it] = conds
fails_point = sum(not wm.certify(cd, pb) for cd in pool.values())
cert_boxes = 0
for it, cd in pool.items():
    for k in range(1, 21):
        r = SC >> k
        box = [(SC, SC) if par.names[j] == 'gx0' else (SC - r, SC + r) for j in range(len(par.names))]
        cert_boxes += wm.certify(cd, box)
out['b_itins_valid_nearby'] = len(pool); out['b_fail_at_dark_point'] = fails_point
out['b_boxes_certified_containing_dark_point'] = cert_boxes

# replay at the dark point for every nearby itinerary (independent tracer)
xs, ys = X[:], Y[:]
xs = [Fr(x - X[0]) for x in X]; ys = [Fr(y - Y[0]) for y in Y]
Sxy = (Fr(0 - X[0]), Fr(0 - Y[0])); Txy = (Fr(2 - X[0]), Fr(2 - Y[0]))
ex = {k: Fr(1) for k in range(len(par.names))}
ev = lambda f: sum(cf * ex[k] for k, cf in f)
lit = 0
for it in pool:
    B = wm.build(par, it)
    lit += replay.lit_by(ot.cells, xs, ys, Sxy, Txy, (ev(B['Tstar'][0]), ev(B['Tstar'][1])))[0]
out['b_replay_lit_at_dark_point'] = lit

# (c)
C = bb.Cover(par, D=2, dp=4, nang=3000, maxref=14)
r = SC >> 6
C.box0 = [(SC, SC) if nm == 'gx0' else (SC - r, SC + r) for nm in par.names]
C.run(maxboxes=6000, cpu=60)
contains = sum(all(l <= x <= h for x, (l, h) in zip(dark, b)) for b, _ in C.cert)
out['c_stats'] = C.stats; out['c_certified'] = len(C.cert); out['c_uncovered'] = len(C.unc)
out['c_cert_boxes_containing_dark_point'] = contains
out['c_unc_boxes_containing_dark_point'] = sum(all(l <= x <= h for x, (l, h) in zip(dark, b)) for b in C.unc)
out['cpu'] = round(time.process_time() - t0, 2)
print(json.dumps(out))
