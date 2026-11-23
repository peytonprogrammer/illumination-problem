"""Replay check of shootall's LIT claims on sampled pairs, plus negative tests (port of d42's validate42).

For NROOM random strictly simple variants and NPAIR random eligible pairs per room, rerun
shootall with that pair designated and replay the first and the shortest witness with the
independent plane tracer (slit45.trace).  Negative tests: the same witness with the target
moved to another eligible point, and with the direction rotated by 90 degrees, must fail.
EXTRA=k:name:bound designates the marks of one more room at a larger bound.
usage: python3 -B validate53.py SEED NROOM NPAIR BOUND file.jsonl ...
"""
import json
import os
import random
import subprocess
import sys
import tempfile

import rooms53 as Q
import run53
import slit45 as S

seed, nroom, npair, bound = map(int, sys.argv[1:5])
rng = random.Random(seed)
rows = [json.loads(l) for f in sys.argv[5:] for l in open(f)]
rows = [r for r in rows if r['status'] == 'ok']
rng.shuffle(rows)
pick = {}
for r in rows[:nroom]:
    pick.setdefault(r['k'], set()).add(r['name'])
extra = os.environ.get('EXTRA')
if extra:
    ek, ename, eb = extra.split(':')
    pick.setdefault(int(ek), set()).add(ename)
rooms = []
for k, names in sorted(pick.items()):
    names = set(names)
    for c in run53.candidates(k, k, k, k if k <= 3 else 0):
        if c[2] in names:
            names.discard(c[2])
            rooms.append(c)
            if not names:
                break


def witness(o, elig, a, b, bd, fn):
    S.write_origami(o, fn, elig, a, b)
    line = subprocess.run(['./shootall', str(bd), fn], capture_output=True, text=True, check=True).stdout.split('\n')[0]
    return dict(x.split('=') for x in line.split())


tot = ok = neg_rej = neg_tot = 0
with tempfile.TemporaryDirectory() as td:
    for k, fam, name, tiles in rooms:
        st, W, poly = Q.check(tiles, ((2 * k, 4 * k), (4 * k, 2 * k)))
        o = S.build(sorted(tiles))
        elig = [p for p in o['pts'] if o['ptype'][p] == 'I']
        segs = [(poly[i], poly[(i + 1) % len(poly)]) for i in range(len(poly))]
        corners = set(poly)
        if extra and (k, name) == (int(ek), ename):
            kv = witness(o, elig, (2 * k, 4 * k), (4 * k, 2 * k), int(eb), td + '/o.txt')
            res = []
            for key in ('first', 'best'):
                dx, dy, m = map(int, kv[key].split(','))
                good, nrefl, hits = S.trace(segs, corners, (2 * k, 4 * k), (dx, dy), m, (4 * k, 2 * k), record=True)
                res.append((key, (dx, dy), m, nrefl, good))
            print('EXTRA marks', k, name, 'W', W, 'bound', eb, res)
        for _ in range(npair):
            a, b = rng.sample(elig, 2)
            kv = witness(o, elig, a, b, bound, td + '/o.txt')
            for key in ('first', 'best'):
                tot += 1
                if kv[key] == 'none':
                    print('NO WITNESS', k, name, a, b, key)
                    continue
                dx, dy, m = map(int, kv[key].split(','))
                good = S.trace(segs, corners, a, (dx, dy), m, b)[0]
                ok += good
                if not good:
                    print('REPLAY FAIL', k, name, a, b, key, dx, dy, m)
                c = rng.choice([p for p in elig if p not in (a, b)])
                for d2, t2 in (((dx, dy), c), ((-dy, dx), b)):
                    neg_tot += 1
                    acc = S.trace(segs, corners, a, d2, m, t2)[0]
                    neg_rej += not acc
                    if acc:
                        print('NEG ACCEPTED', k, name, a, d2, m, t2)
print('rooms', len(rooms), 'witnesses replayed', ok, 'of', tot, '; negative tests rejected', neg_rej, 'of', neg_tot)
