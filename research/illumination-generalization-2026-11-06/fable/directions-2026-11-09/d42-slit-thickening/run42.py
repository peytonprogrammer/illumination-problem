"""Enumerate thickenings of Monteil's slit room and decide all pairs by shooting.

usage: [KMIN=k] [KINDS=thick,...] python3 -B run42.py KMAX BOUND OUT.jsonl [WORKERS]
"""
import json
import os
import sys
import tempfile
from multiprocessing import Pool

import rooms42 as Q
import slit45 as S

ENDS = ('flat', 'up', 'down', 'roof')


def in_closed(pt, poly):
    """Point in closed convex ccw polygon."""
    m = len(poly)
    for i in range(m):
        a, b = poly[i], poly[(i + 1) % m]
        if (b[0] - a[0]) * (pt[1] - a[1]) - (b[1] - a[1]) * (pt[0] - a[0]) < 0:
            return False
    return True


def candidates(kmax):
    seen = set()
    for k in range(1, kmax + 1):
        yield dict(k=k, kind='slit', w=0, xl=3 * k, top=2 * k, end='slit')
        for top, kind in ((2 * k, 'thick'), (2 * k - 1, 'other-top-1'), (2 * k + 1, 'other-top+1')):
            if top <= k:
                continue
            for w in range(1, 4 * k):
                for xl in range(3 * k - w, 3 * k + 1):
                    xr = xl + w
                    if xl <= k or xr >= 5 * k:
                        continue
                    for end in ENDS:
                        obs = Q.obstacle(k, xl, xr, top, end)
                        if obs is None or tuple(obs) in seen:
                            continue
                        seen.add(tuple(obs))
                        # a thickening contains the slit (up to its tip height); marks stay outside
                        if not all(in_closed((3 * k, y), obs) for y in range(k, min(top, 2 * k) + 1)):
                            continue
                        if any(in_closed((k * x, k * y), obs) for x, y in Q.MARKS0):
                            continue
                        place = 'left' if xr == 3 * k else 'right' if xl == 3 * k else 'centred' if xl + xr == 6 * k else 'offset'
                        yield dict(k=k, kind=kind, w=w, xl=xl, top=top, end=end, place=place)


def job(cand):
    k = cand['k']
    if cand['kind'] == 'slit':
        room = Q.make_room(k)
    else:
        obs = Q.obstacle(k, cand['xl'], cand['xl'] + cand['w'], cand['top'], cand['end'])
        if obs is None:
            return None
        room = Q.make_room(k, obs)
        if room is None:
            return dict(cand, status='obstacle-outside')
        # marks must be strictly outside the obstacle (interior points of the room)
    tiles = room['tiles']
    if not Q.connected(tiles):
        return dict(cand, status='disconnected')
    b = Q.R.boundary(tiles)
    if not b['simple']:
        return dict(cand, status='not-simple')
    c = room['c']
    o = S.build(tiles, room['slit'])
    for m in room['marks']:
        if o['ptype'].get((c * m[0], c * m[1])) != 'I':
            return dict(cand, status='mark-not-interior')
    W = len(Q.clean(b['cycle'][:-1])) + (2 if room['slit'] else 0)
    if W > 22:
        return dict(cand, status='W>22', W=W)
    with tempfile.TemporaryDirectory() as td:
        a = Q.analyse(room, BOUND, td)
    a.pop('orbit_line')
    a.pop('segs')
    a['obs'] = room['obs']
    a['tilekey'] = hash(tuple(tiles))
    return dict(cand, status='ok', **a)


def init(b):
    global BOUND
    BOUND = b


if __name__ == '__main__':
    kmax, bound, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    workers = int(sys.argv[4]) if len(sys.argv) > 4 else 3
    kmin = int(os.environ.get('KMIN', '1'))
    kinds = os.environ.get('KINDS')
    cands = [c for c in candidates(kmax) if c['k'] >= kmin and (not kinds or c['kind'] in kinds.split(',') or c['kind'] == 'slit')]
    print('candidates', len(cands), flush=True)
    with Pool(workers, initializer=init, initargs=(bound,)) as pool, open(out, 'w') as fh:
        for r in pool.imap(job, cands, chunksize=1):
            if r is None:
                continue
            fh.write(json.dumps(r) + '\n')
            fh.flush()
            if r['status'] == 'ok':
                print(r['k'], r['kind'], r['w'], r['xl'], r['top'], r['end'], 'W', r['W'], 'pts', r['n_points'], 'unlit', r['unlit'],
                      'best', r['best'] and (r['best']['dir'], r['best']['m'], r['best']['refl'], r['best']['replay']), flush=True)
