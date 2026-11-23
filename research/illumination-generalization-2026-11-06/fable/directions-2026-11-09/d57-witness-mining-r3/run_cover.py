"""Cover the truncated region of one open pair and replay it.
Usage: run_cover.py mask S0 S1 T0 T1 D dp maxboxes cpu [replay]
Prints one JSON line."""
import sys, json, time, resource
import wm, bb, replay
rows = {r['mask']: r for r in json.load(open('tools/cert_r3.json'))}
a = sys.argv[1:]
mask, S, T = int(a[0]), (int(a[1]), int(a[2])), (int(a[3]), int(a[4]))
D, dp, mb, cpu = int(a[5]), int(a[6]), int(a[7]), float(a[8])
rp = len(a) > 9 and a[9] == 'replay'
r = rows[mask]
par = wm.Param(wm.OT.from_mask(r['nx'], r['ny'], mask), S, T)
t0 = time.process_time()
C = bb.Cover(par, D=D, dp=dp).run(maxboxes=mb, cpu=cpu)
from collections import Counter
its = Counter(it for b, it in C.cert)
out = dict(mask=mask, S=S, T=T, D=D, dp=dp, dims=sum(l < h for l, h in C.box0), **C.stats,
           closed_trunc=not C.unc, unc=len(C.unc), n_itins=len(its),
           max_ref=max((len(i) for i in its), default=None),
           top=[(list(i), c) for i, c in its.most_common(5)])
if C.unc:
    f, miss = C.fraction(100); out['frac'] = f
if rp:
    out['replay_points'], out['replay_fail'] = replay.replay_cover(C)
out['cpu_total'] = round(time.process_time() - t0, 2)
print(json.dumps(out), flush=True)
