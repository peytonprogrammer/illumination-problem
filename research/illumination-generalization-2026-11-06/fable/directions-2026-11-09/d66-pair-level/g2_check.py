"""d66: half-integer marks (gap G2 at Lambda = (1/2)Z^2), exact integer billiards.

The room P is scaled by 2 (each cell becomes 2 x 2 cells); billiards in 2P are billiards in P.
Pairs: interior lattice points S < T of 2P, not both in 2Z^2 (so at least one mark of P is a
non-lattice half-integer point), either parity. g1_check.shoot with parity 0 (same class in 2P)
and 1 (different class). A pair with no witness at max(p, q) <= H, then H2, is UNRESOLVED.
Rooms: the named rooms and the R* rooms of pair_level.json with area >= 21 and a same-class pair.
Usage: python3 -B g2_check.py H H2
"""
import json
import sys
import time
from math import gcd
import g1_check as G  # noqa: E402  (path setup, CPU limit 300 s)
from g1_check import shoot, lattice_points, status, D, HERE, NZ, named_rooms  # noqa: E402


def lit_pairs(cells, H, ipts, want):
    lim = 8 * len(lattice_points(cells)) + 8
    lit = set()
    for S in ipts:
        tg = {T for T in ipts if (min(S, T), max(S, T)) in want} - {S}
        if not tg:
            continue
        for p in range(H + 1):
            for q in range(H + 1):
                if gcd(p, q) != 1 or not tg:
                    continue
                for sx in (1, -1):
                    for sy in ((1, -1) if q else (1,)):
                        if not p and sy < 0:
                            continue
                        for par in (0, 1):
                            for T, c in shoot(cells, S, p, q, sx, sy, tg, lim, parity=par):
                                tg.discard(T)
                                lit.add((min(S, T), max(S, T)))
    return lit


def run(cells, H, H2):
    c2 = {(2 * i + u, 2 * j + v) for i, j in cells for u in (0, 1) for v in (0, 1)}
    ipts = [p for p in lattice_points(c2) if status(c2, p) == 'interior']
    want = {(S, T) for S in ipts for T in ipts if S < T and not (S[0] % 2 == S[1] % 2 == T[0] % 2 == T[1] % 2 == 0)}
    lit = lit_pairs(c2, H, ipts, want)
    rest = want - lit
    if rest:
        lit |= lit_pairs(c2, H2, sorted({s for pr in rest for s in pr}), rest)
    return len(want), sorted(want - lit)


if __name__ == '__main__':
    H, H2 = int(sys.argv[1]), int(sys.argv[2])
    t0 = time.process_time()
    cov = [r for r in json.load(open(D / 'd64-finite-case' / 'data' / 'covers.json'))['rooms'] if r['normalized']]
    cov.sort(key=lambda r: (r['n'], r['cells']))
    cm = dict(named_rooms())
    cm.update(Z12=NZ.Z12, S10=NZ.S10)
    for k in (1843, 1490, 453):
        cm['room%d' % k] = cov[k]['cells']
    for r in json.load(open(HERE / 'pair_level.json'))['rooms']:
        if r['name'].startswith('cov') and r['n'] >= 21 and r['counts'].get('pairs'):
            cm[r['name']] = cov[int(r['name'][3:])]['cells']
    tot = [0, 0, 0]
    for name, cells in cm.items():
        npairs, un = run(set(map(tuple, cells)), H, H2)
        tot[0] += 1
        tot[1] += npairs
        tot[2] += len(un)
        if un or not name.startswith('cov'):
            print(name, 'half-integer pairs', npairs, 'unresolved', len(un), un[:4], flush=True)
    print('rooms %d half-integer pairs %d unresolved %d CPU %.1f' % (tot[0], tot[1], tot[2], time.process_time() - t0))
