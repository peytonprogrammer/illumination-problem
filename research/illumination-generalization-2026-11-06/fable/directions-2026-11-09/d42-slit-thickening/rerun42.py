"""Rerun every 'ok' room with unlit pairs at a larger direction bound.
usage: python3 -B rerun42.py BOUND OUT.jsonl IN.jsonl ...
"""
import json
import sys
import tempfile
import time

import rooms42 as Q

bound, out = int(sys.argv[1]), sys.argv[2]
with open(out, 'w') as fh:
    for f in sys.argv[3:]:
        for l in open(f):
            r = json.loads(l)
            if r['status'] != 'ok' or r['unlit'] == 0:
                continue
            t0 = time.time()
            room = Q.make_room(r['k']) if r['kind'] == 'slit' else Q.make_room(r['k'], [tuple(p) for p in r['obs']])
            with tempfile.TemporaryDirectory() as td:
                a = Q.analyse(room, bound, td)
            a.pop('orbit_line')
            a.pop('segs')
            keep = {x: r[x] for x in ('k', 'kind', 'w', 'xl', 'top', 'end', 'place') if x in r}
            res = dict(keep, status='ok', **a, obs=room['obs'], prev_bound=r['bound'], prev_unlit=r['unlit'], secs=round(time.time() - t0, 1))
            fh.write(json.dumps(res) + '\n')
            fh.flush()
            print(r['k'], r['kind'], r['w'], r['xl'], r['top'], r['end'], 'W', a['W'], 'unlit', r['unlit'], '->', a['unlit'], a['unlit_pairs'][:4], res['secs'], 's', flush=True)
