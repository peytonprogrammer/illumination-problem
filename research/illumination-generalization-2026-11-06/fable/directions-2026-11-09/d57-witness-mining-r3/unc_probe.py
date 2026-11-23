"""Where do the uncovered boxes of a collinear pair sit? Runs the cover
(D=2, dp=4, 45 s), then for each uncovered box centre records: relative box
size, the shortest exactly valid itinerary at the centre, and the distance of
the one-bounce reflection point (s1+t1)/2 to the nearest grid line x_i,
divided by the smallest gap. Usage: unc_probe.py mask S0 S1 T0 T1"""
import sys, json, math
from collections import Counter
import wm, bb
rows = {r['mask']: r for r in json.load(open('tools/cert_r3.json'))}
a = list(map(int, sys.argv[1:6]))
mask, S, T = a[0], (a[1], a[2]), (a[3], a[4])
r = rows[mask]
par = wm.Param(wm.OT.from_mask(r['nx'], r['ny'], mask), S, T)
C = bb.Cover(par, D=2, dp=4).run(maxboxes=10**7, cpu=45)
SC = bb.SC
print(json.dumps(dict(stats=C.stats, unc=len(C.unc), cert=len(C.cert))))
logvol0 = sum(math.log2(h - l) for l, h in C.box0 if h > l)
sizes, mids, short = Counter(), [], Counter()
ax = 0 if S[1] == T[1] else 1                      # collinear along x if same Y
for box in C.unc[:400]:
    c = {k: (l + h) // 2 for k, (l, h) in enumerate(box)}
    sizes[round(sum(math.log2(h - l) for l, h in box if h > l) - logvol0)] += 1
    ev = lambda f: sum(cf * c[k] for k, cf in f)
    g = [ev(f) for f in (par.xf if ax == 0 else par.yf)]
    m = (ev(par.Sf[ax]) + ev(par.Tf[ax])) / 2
    gap = min(g[i + 1] - g[i] for i in range(len(g) - 1))
    mids.append(min(abs(m - x) for x in g) / gap)
    v = {k: x / SC for k, x in c.items()}
    best = None
    for it, sx, sy in wm.mine(par, v, 3000, 16):
        conds, _ = wm.conditions(par, it, sx, sy)
        if wm.certify(conds, [(x, x) for x in c.values()]): best = it; break
    short[len(best) if best is not None else None] += 1
mids.sort()
print(json.dumps(dict(n_probed=min(400, len(C.unc)), log2_rel_volume=sorted(sizes.items()),
      shortest_len_at_centre=sorted(short.items(), key=str),
      midpoint_to_gridline_over_mingap_quantiles=[round(mids[int(q * (len(mids) - 1))], 4) for q in (0, .1, .25, .5, .75, .9, 1)])))
