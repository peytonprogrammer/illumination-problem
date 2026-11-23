"""Rerun every variant that still has an unlit pair at a larger direction bound.

The rooms are regenerated from (k, name) with run53.candidates.  No pair is
designated, so shootall stops as soon as every pair is lit (lastsum = the
direction bound that was needed).  Witnesses for the marks come from the first run.
usage: python3 -B rerun53.py BOUND OUT.jsonl IN.jsonl ...
"""
import json
import subprocess
import sys
import tempfile
from multiprocessing import Pool

import rooms53 as Q
import run53
import slit45 as S


def job(c):
    k, fam, name, tiles = c
    o = S.build(sorted(tiles))
    elig = [p for p in o['pts'] if o['ptype'][p] == 'I']
    with tempfile.TemporaryDirectory() as td:
        S.write_origami(o, td + '/o.txt', elig)
        r = subprocess.run([str(Q.HERE / 'shootall'), str(BOUND), td + '/o.txt'], capture_output=True, text=True, check=True).stdout.splitlines()
    kv = dict(x.split('=') for x in r[0].split())
    unl = [(elig[int(l.split()[1])], elig[int(l.split()[2])]) for l in r[1:]]
    return dict(k=k, family=fam, name=name, bound=BOUND, pairs=int(kv['pairs']), unlit=int(kv['unlit']),
                lastsum=int(kv['lastsum']), unlit_pairs=unl)


def init(b):
    global BOUND
    BOUND = b


if __name__ == '__main__':
    bound, out = int(sys.argv[1]), sys.argv[2]
    want = {}
    for f in sys.argv[3:]:
        for l in open(f):
            r = json.loads(l)
            if r['status'] in ('ok', 'pinched') and r['unlit'] > 0:
                want.setdefault(r['k'], set()).add(r['name'])
    cands = []
    for k, names in sorted(want.items()):
        for c in run53.candidates(k, k, k, k if k <= 3 else 0):
            if c[2] in names:
                names.discard(c[2])
                cands.append(c)
                if not names:
                    break
        assert not names, (k, names)
    print('rerun', len(cands), flush=True)
    with Pool(3, initializer=init, initargs=(bound,)) as pool, open(out, 'w') as fh:
        for r in pool.imap(job, cands, chunksize=1):
            fh.write(json.dumps(r) + '\n')
            fh.flush()
            print(r['k'], r['family'], r['name'], 'unlit', r['unlit'], 'lastsum', r['lastsum'], flush=True)
