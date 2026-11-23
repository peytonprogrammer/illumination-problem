"""Run run_cover logic over a shard of the open pairs.
Usage: batch.py kinds(e.g. 1 or 23) D dp maxboxes cpu replay(0/1) shard nshards out.jsonl"""
import sys, json, time, resource
import wm, bb, replay
from collections import Counter
kinds, D, dp, mb, cpu, rp, sh, ns, outp = sys.argv[1:]
D, dp, mb, cpu, rp, sh, ns = int(D), int(dp), int(mb), float(cpu), int(rp), int(sh), int(ns)
rows = {r['mask']: r for r in json.load(open('tools/cert_r3.json'))}
pairs = []
for line in open('kinds_r3.tsv'):
    m, s, t, k = line.rstrip('\n').split('\t')
    if k in kinds: pairs.append((int(m), eval(s), eval(t), k))
out = open(outp, 'a')
for n, (mask, S, T, k) in enumerate(pairs):
    if n % ns != sh: continue
    r = rows[mask]
    par = wm.Param(wm.OT.from_mask(r['nx'], r['ny'], mask), S, T)
    t0 = time.process_time()
    C = bb.Cover(par, D=D, dp=dp).run(maxboxes=mb, cpu=cpu)
    its = Counter(it for b, it in C.cert)
    o = dict(mask=mask, shape=r['shape'], S=S, T=T, kind=k, D=D, dp=dp,
             dims=sum(l < h for l, h in C.box0), **C.stats, closed_trunc=not C.unc,
             unc=len(C.unc), n_itins=len(its), max_ref=max((len(i) for i in its), default=None),
             pool=len(C.pool), pool_max_ref=max((len(i) for i in C.pool), default=None),
             top=[(list(i), c) for i, c in its.most_common(3)])
    if C.unc: o['frac'] = C.fraction(100)[0]
    if rp and not C.unc: o['replay_points'], o['replay_fail'] = replay.replay_cover(C, nvert=4, nint=1)
    o['cpu_total'] = round(time.process_time() - t0, 2)
    out.write(json.dumps(o) + '\n'); out.flush()
