"""d83 step 4: targeted per-candidate check for rooms whose saved witnesses all have
source-class midpoints.

For each off-class regular coincidence (point M, 2-cycle {a, b}) a path S -> T with
midpoint M is a half-segment S -> M of developing vector u followed by its straight
continuation M -> T of the same vector u, so the whole path has vector 2u. A developed
lift of M differs from M by integer-line reflections, so u = M' - S with
u = M - S (mod 2). The check runs over those u with max(|u_x|, |u_y|) <= BOUND only;
it can confirm a candidate but cannot refute one. A confirmation requires:
  - tracer.py: S + u ends at M with no corner hit, arriving in a cell of {a, b};
    S + 2u ends at T with no corner hit;
  - d3 surface.py: the same signed vectors u and 2u end at M and T.
Run: python3 -B step4.py
"""
import time
from fractions import Fraction as Fr
from math import gcd

import stress as ST  # noqa: E402

from room import status  # noqa: E402
from tracer import advance  # noqa: E402
import surface as SF  # noqa: E402

BOUND = 32
ROOMS = ['R22-L1-005', 'R22-L1-006', 'R22-L1-022', 'R22-L1-027']


def arrival_cell(M, v):
    return (M[0] - 1 if v[0] > 0 else M[0], M[1] - 1 if v[1] > 0 else M[1])


def check(cells, S, T, M, cyc, idx, surf, u):
    end, ok, _, v = advance(cells, Fr(S[0]), Fr(S[1]), Fr(u[0]), Fr(u[1]))
    if not ok or end != (M[0], M[1]):
        return False
    if status(cells, M) == 'interior':
        if v[0] == 0 or v[1] == 0:
            return False   # axis direction: no diagonal 2-cycle is crossed straight
        if idx[arrival_cell(M, v)] not in cyc:
            return False
    end2, ok2, _, _ = advance(cells, Fr(S[0]), Fr(S[1]), Fr(2 * u[0]), Fr(2 * u[1]))
    if not ok2 or end2 != (T[0], T[1]):
        return False
    if u[0] != 0 and u[1] != 0:
        s = (Fr(S[0]), Fr(S[1]))
        rp, a, _ = surf.segment(s, u)
        rp2, b, _ = surf.segment(s, (2 * u[0], 2 * u[1]))
        assert a and b and rp == (M[0], M[1]) and rp2 == (T[0], T[1]), 'tracers disagree'
        return True
    return 'axis (tracer.py only)'


def main():
    import json
    t0 = time.process_time()
    rooms = {x['id']: x for x in map(json.loads, open(ST.D8 / 'results.jsonl'))}
    print('\nSTEP 4, bound max|u| <= %d' % BOUND)
    for rid in ROOMS:
        x = rooms[rid]
        cells = set(map(tuple, x['cells']))
        S, T = map(tuple, x['marks'])
        n, r, d, reg, idx = ST.coincidences(cells, S, T)
        surf = SF.Surface(cells)
        print(rid)
        reached = 0
        off = [(c, p, k, cy) for c, p, k, cy in reg if c != (0, 0)]
        for c, M, kind, cy in off:
            sx, sy = (M[0] - S[0]) % 2, (M[1] - S[1]) % 2
            us = [(i, j) for i in range(-BOUND, BOUND + 1) for j in range(-BOUND, BOUND + 1)
                  if (i - sx) % 2 == 0 and (j - sy) % 2 == 0 and (i, j) != (0, 0)]
            us.sort(key=lambda u: (u[0] ** 2 + u[1] ** 2, u))
            hit = None
            for u in us:
                try:
                    res = check(cells, S, T, M, cy, idx, surf, u)
                except RuntimeError:
                    continue
                if res:
                    hit = (u, res)
                    break
            reached += hit is not None
            print('   %-3s M=%s %-8s cycle=%s: %s' % (
                ST.NAMES[c], M, kind, cy,
                'reached, u=%s, path vector 2u=%s, gcd(u)=%d, second tracer=%s'
                % (hit[0], (2 * hit[0][0], 2 * hit[0][1]), gcd(*hit[0]), hit[1]) if hit
                else 'not reached within bound'))
        print('   off-class candidates reached: %d of %d' % (reached, len(off)))
    print('STEP 4 CPU seconds: %.1f' % (time.process_time() - t0))


main()
