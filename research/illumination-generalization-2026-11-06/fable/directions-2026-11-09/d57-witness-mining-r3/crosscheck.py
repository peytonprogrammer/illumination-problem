"""Soundness cross-check of the exact point certifier against the independent
replay: random open pairs, random dyadic parameter points, raw shooter
candidates (before re-tracing, so many have a wrong hit order) plus random
wall sequences. Counts certifier-True & replay-False (must be 0)."""
import json, random, time
from fractions import Fraction as Fr
import wm, bb, replay
rng = random.Random(11)
rows = {r['mask']: r for r in json.load(open('tools/cert_r3.json'))}
pairs = [(int(m), eval(s), eval(t)) for m, s, t, k in (l.rstrip('\n').split('\t') for l in open('kinds_r3.tsv'))]
n = tt = tf = ft = same_order = 0; t0 = time.process_time()
for mask, S, T in rng.sample(pairs, 40):
    r = rows[mask]; ot = wm.OT.from_mask(r['nx'], r['ny'], mask); par = wm.Param(ot, S, T)
    C = bb.Cover(par, D=4, dp=8, seed=rng.random())
    v = C.sample_region(); pb = [(x, x) for x in v]
    vals = {k: x / bb.SC for k, x in enumerate(v)}; ex = {k: Fr(x, bb.SC) for k, x in enumerate(v)}
    ev = lambda f: sum(c * ex[k] for k, c in f)
    xs = [ev(f) for f in par.xf]; ys = [ev(f) for f in par.yf]
    Sx = (ev(par.Sf[0]), ev(par.Sf[1])); Tx = (ev(par.Tf[0]), ev(par.Tf[1]))
    fw = wm.float_walls(ot, *wm.realize(par, vals)[:2])
    cands = list(wm.shoot(fw, wm.realize(par, vals)[2], wm.realize(par, vals)[3], 1500, 10))[:60]
    cands += [tuple(rng.randrange(len(ot.walls)) for _ in range(rng.randrange(0, 6))) for _ in range(40)]
    for it in cands:
        B = wm.build(par, it)
        dx, dy = ev(B['dx']), ev(B['dy'])
        if dx == 0 or dy == 0: continue
        conds, _ = wm.conditions(par, it, 1 if dx > 0 else -1, 1 if dy > 0 else -1)
        c = wm.certify(conds, pb)
        rp = replay.lit_by(ot.cells, xs, ys, Sx, Tx, (ev(B['Tstar'][0]), ev(B['Tstar'][1])))[0]
        n += 1; tt += c and rp; tf += c and not rp; ft += (not c) and rp
        if rp and not c:      # replay checks only the end point; compare hit order
            tr = wm.float_trace(fw, (float(Sx[0]), float(Sx[1])), (float(dx), float(dy)), 80)
            same_order += tr == tuple(it)
print(json.dumps(dict(checked=n, cert_and_replay=tt, cert_not_replay=tf, replay_not_cert=ft, of_which_same_hit_order=same_order,
                      cpu=round(time.process_time() - t0, 1))))
