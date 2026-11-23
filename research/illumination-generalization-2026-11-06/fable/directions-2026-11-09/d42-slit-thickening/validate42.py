"""Replay check of shootall's LIT claims on sampled pairs, plus a negative test.

For a sample of 'ok' rooms from the given result files and NPAIR random eligible
pairs per room, rerun shootall with that pair designated, then replay the
first and the shortest witness with the independent plane tracer (slit45.trace).
Negative test: the same witness with the target moved to a different
eligible point, and with the direction rotated by 90 degrees, must fail.
usage: python3 -B validate42.py SEED NROOM NPAIR BOUND file.jsonl ...
"""
import json
import random
import subprocess
import sys
import tempfile

import rooms42 as Q
import slit45 as S

seed, nroom, npair, bound = map(int, sys.argv[1:5])
rng = random.Random(seed)
rows = [json.loads(l) for f in sys.argv[5:] for l in open(f)]
rows = [r for r in rows if r['status'] == 'ok']
rng.shuffle(rows)
tot = ok = neg_rej = neg_tot = 0
with tempfile.TemporaryDirectory() as td:
    for r in rows[:nroom]:
        k = r['k']
        room = Q.make_room(k) if r['kind'] == 'slit' else Q.make_room(k, [tuple(p) for p in r['obs']])
        c = room['c']
        o = S.build(room['tiles'], room['slit'])
        elig = [p for p in o['pts'] if o['ptype'][p] == 'I' and p[0] % c == 0 and p[1] % c == 0]
        poly = r['poly'] = [tuple(p) for p in r['poly']]
        segs = [(poly[i], poly[(i + 1) % len(poly)]) for i in range(len(poly))]
        corners = set(poly)
        if room['slit']:
            segs.append((room['slit'][0][0], room['slit'][-1][1]))
            corners |= {room['slit'][0][0], room['slit'][-1][1]}
        unlit = {tuple(map(tuple, u)) for u in r['unlit_pairs']}
        for _ in range(npair):
            a, b = rng.sample(elig, 2)
            ac, bc = (a[0] // c, a[1] // c), (b[0] // c, b[1] // c)
            if (ac, bc) in unlit or (bc, ac) in unlit:
                continue
            S.write_origami(o, td + '/o.txt', elig, a, b)
            line = subprocess.run(['./shootall', str(bound), td + '/o.txt'], capture_output=True, text=True, check=True).stdout.split('\n')[0]
            kv = dict(x.split('=') for x in line.split())
            for key in ('first', 'best'):
                tot += 1
                if kv[key] == 'none':
                    print('NO WITNESS', r['k'], r['kind'], r['obs'], a, b)
                    continue
                dx, dy, m = map(int, kv[key].split(','))
                good = S.trace(segs, corners, a, (dx, dy), m, b)[0]
                ok += good
                if not good:
                    print('REPLAY FAIL', r['k'], r['kind'], r['obs'], a, b, kv[key])
                other = rng.choice([p for p in elig if p not in (a, b)]) if len(elig) > 2 else a
                neg_tot += 2
                neg_rej += not S.trace(segs, corners, a, (dx, dy), m, other)[0]
                neg_rej += not S.trace(segs, corners, a, (-dy, dx), m, b)[0]
print('witnesses replayed %d / %d; negative tests rejected %d / %d' % (ok, tot, neg_rej, neg_tot))
