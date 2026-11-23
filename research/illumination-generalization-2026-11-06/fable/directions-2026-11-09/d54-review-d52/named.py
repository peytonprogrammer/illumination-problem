"""d52: named rooms (22-wall room, P6, 12-wall cross) through the d52 W-set code. No search."""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fold import *  # noqa

R22 = [(-1, -1), (-1, 1), (0, 1), (0, 2), (1, 2), (1, 3), (3, 3), (3, 2), (4, 2), (4, 1), (5, 1),
       (5, 0), (3, 0), (3, 1), (1, 1), (1, -1), (2, -1), (2, -3), (1, -3), (1, -2), (0, -2), (0, -1)]
Q5 = {(0, 0), (1, 0), (1, 1), (2, 1), (2, 2)}
P6 = Q5 | {(i, -j - 1) for i, j in Q5} | {(5 - i, -j - 1) for i, j in Q5} | {(i, 5 - j) for i, j in Q5}
CROSS = {(i, j) for i in range(4) for j in range(1, 3)} | {(i, j) for i in range(1, 3) for j in range(4)}
ROOMS = {'22-wall': cells_from_polygon(R22), 'P6': P6, 'cross': CROSS}


def report(name, cells):
    G, order = from_cells(cells)
    prof = profile(G)
    s = summary(prof)
    n = len(G[0])
    print('==', name, 'n', n, 'r', s['z'], 'convex', s['cvx'], 'genus0', s['genus0'],
          'strictly simple', strictly_simple(cells))
    out = {}
    for x in CLASSES:
        blk = B(G, x)
        assert blk == congruence_G(G, two_cycle_pairs(G, x)) or \
            len(set(blk)) == len(set(congruence_G(G, two_cycle_pairs(G, x))))
        K = quotient(G, blk)
        kp = profile(K)
        ks = summary(kp)
        d = len(K[0])
        print('  class', x, 'd', d, 'delta', n // d, 'z', ks['z'], 'p', ks['p'], 'cone', ks['cone'],
              'types', {c: sorted(t) for c, t in kp.items()})
        out[x] = dict(d=d, delta=n // d, z=ks['z'], canon=canon(K))
    pos, nb = positives(G)
    print('  positives (a, S, T):', [(a, s, t) for a, s, t in pos])
    return G, out, pos


if __name__ == '__main__':
    res = {}
    for name, cells in ROOMS.items():
        G, out, pos = report(name, cells)
        res[name] = {str(x): dict(d=v['d'], delta=v['delta'], z=v['z'], canon=v['canon'])
                     for x, v in out.items()}
    json.dump(res, open(Path(__file__).resolve().parent / 'named_quotients.json', 'w'))
