"""Enumerate strictly simple resolutions of the pinch in Monteil's slide-4 room and shoot all pairs.

Scale k: room k*P0, pinch Q = (4k, 4k), hole [3k,4k]^2, marks (2k,4k), (4k,2k).
The two room wedges at Q are R1 = triangle (3k,4k) (4k,4k) (3k,5k) above the hole
and its mirror R2 (in y = x) to the right of the hole.  A resolution is strictly
simple only if the hole joins the exterior at Q, i.e. wall material separates the
wedge tips.  Families (one-sided shapes are applied to R1; R2 versions are mirror
images with S and T swapped, so they give the same verdicts and are not rerun):

  V(w)   vertical cut x = 4k-w across R1, 1 <= w <= k  (removes triangle Q, Q-(w,0), Q+(-w,w))
  D(a)   45-degree chamfer across R1 along x - y = -2a, 1 <= 2a <= k
  T(s)   hole top raised to y = 4k+s inside R1, 1 <= s <= k (shifts the hole's top wall)
  A|B    shape A on R1 and shape B on R2 (both tips cut; unordered up to the mirror)
  shift(s1,s2)  hole translated by (s1, s2), -1 <= s1, s2 <= k-1
  door(w)       wedges joined through the exterior at Q (hole enclosed): expected not simple
  plug1 / plug2 every tile subset of R1 (and R2) containing the tip tile, for small k
  win1          k = 1: every subset of the 8 tiles in [3,5]^2 toggled (added or removed)

usage: python3 -B run53.py KMAX BOUND OUT.jsonl [WORKERS]   env KMIN, KEX1 (plug1 up to), KEX2 (plug2 up to)
"""
import itertools
import json
import os
import sys
import tempfile
from multiprocessing import Pool

import rooms53 as Q


def shape(k, kind, n):
    """Tile set removed from R1 for shape kind ('V', 'D', 'T') with parameter n."""
    q = 4 * k
    if kind == 'V':
        poly = [(q, q), (q - n, q + n), (q - n, q)]
    elif kind == 'D':
        poly = [(q, q), (q - n, q + n), (q - 2 * n, q)]
    elif kind == 'T':
        poly = [(3 * k, q), (q, q), (q - n, q + n), (3 * k, q + n)]
    return Q.tiles_of(Q.clean(poly))


def shapes(k):
    out = [('V%d' % w, shape(k, 'V', w)) for w in range(1, k + 1)]
    out += [('D%d' % a, shape(k, 'D', a)) for a in range(1, k // 2 + 1)]
    out += [('T%d' % s, shape(k, 'T', s)) for s in range(1, k + 1)]
    return out


def mirror(ts):
    return {Q.mirror_tile(t) for t in ts}


def candidates(kmin, kmax, kex1, kex2):
    for k in range(kmin, kmax + 1):
        base = Q.base_tiles(k)
        r1, r2, tip1, tip2 = Q.wedge_tiles(k)
        hole = Q.tiles_of([(3 * k, 3 * k), (4 * k, 3 * k), (4 * k, 4 * k), (3 * k, 4 * k)])
        yield k, 'pinched', 'pinched', base
        sh = shapes(k)
        for name, X in sh:
            yield k, 'one-sided', name + '|-', base - X
        for (n1, X1), (n2, X2) in itertools.combinations_with_replacement(sh, 2):
            yield k, 'two-sided', n1 + '|' + n2, base - X1 - mirror(X2)
        for s1 in range(-1, k):
            for s2 in range(-1, k):
                if (s1, s2) == (0, 0) or s1 > s2:
                    continue          # s1 > s2 is the mirror image of (s2, s1)
                sq = Q.tiles_of([(3 * k + s1, 3 * k + s2), (4 * k + s1, 3 * k + s2), (4 * k + s1, 4 * k + s2), (3 * k + s1, 4 * k + s2)])
                yield k, 'shift', 'shift(%d,%d)' % (s1, s2), (base | hole) - sq
        if k <= 3:
            for w in range(1, k + 1):
                box = Q.tiles_of([(4 * k - w, 4 * k - w), (4 * k + w, 4 * k - w), (4 * k + w, 4 * k + w), (4 * k - w, 4 * k + w)])
                yield k, 'door', 'door(%d)' % w, base | (box - hole)
        if k <= kex1 or k <= kex2:
            rest = sorted(r1 - {tip1})
            ones = []
            for m in range(len(rest) + 1):
                for sub in itertools.combinations(rest, m):
                    X = {tip1, *sub}
                    st, W, _ = Q.check(base - X, ((2 * k, 4 * k), (4 * k, 2 * k)))
                    if st == 'ok':
                        ones.append(X)
            if k <= kex1:
                for i, X in enumerate(ones):
                    yield k, 'plug1', 'plug1-%d' % i, base - X
            if k <= kex2:
                for i, j in itertools.combinations_with_replacement(range(len(ones)), 2):
                    yield k, 'plug2', 'plug2-%d-%d' % (i, j), base - ones[i] - mirror(ones[j])
        if k == 1:
            win = sorted(Q.tiles_of([(3, 3), (5, 3), (5, 5), (3, 5)]))
            for m in range(1, len(win) + 1):
                for sub in itertools.combinations(win, m):
                    yield k, 'win1', 'win1-' + ''.join('%d%d%d' % t for t in sub), base ^ set(sub)


def job(c):
    k, fam, name, tiles = c
    marks = ((2 * k, 4 * k), (4 * k, 2 * k))
    with tempfile.TemporaryDirectory() as td:
        if fam == 'pinched':
            import slit45 as S
            o = S.build(sorted(tiles))
            elig = [p for p in o['pts'] if o['ptype'][p] == 'I']
            kv, unl = Q.shoot(o, elig, marks[0], marks[1], BOUND, td + '/o.txt')
            a = dict(status='pinched', W=22, N=len(tiles), n_points=len(elig), pairs=int(kv['pairs']), lit=int(kv['lit']),
                     unlit=int(kv['unlit']), bound=BOUND, lastsum=int(kv['lastsum']), unlit_pairs=unl, first=None, best=None)
        else:
            a = Q.analyse(tiles, marks, BOUND, td, (4 * k, 4 * k), Q.orig_segs(k))
    return dict(k=k, family=fam, name=name, **a)


def init(b):
    global BOUND
    BOUND = b


if __name__ == '__main__':
    kmax, bound, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    workers = int(sys.argv[4]) if len(sys.argv) > 4 else 3
    kmin = int(os.environ.get('KMIN', '1'))
    kex1 = int(os.environ.get('KEX1', '0'))
    kex2 = int(os.environ.get('KEX2', '0'))
    seen = {}
    cands = []
    for c in candidates(kmin, kmax, kex1, kex2):
        key = (c[0], frozenset(c[3]))
        if key in seen:
            continue        # same room under an earlier (more descriptive) name
        seen[key] = c[2]
        cands.append(c)
    print('candidates', len(cands), flush=True)
    with Pool(workers, initializer=init, initargs=(bound,)) as pool, open(out, 'w') as fh:
        for r in pool.imap(job, cands, chunksize=1):
            fh.write(json.dumps(r) + '\n')
            fh.flush()
            if r['status'] in ('ok', 'pinched'):
                b = r['best']
                print(r['k'], r['family'], r['name'], 'W', r['W'], 'pts', r['n_points'], 'unlit', r['unlit'],
                      'best', b and (b['dir'], b['m'], b['refl'], b['faces'], b['replay']), flush=True)
