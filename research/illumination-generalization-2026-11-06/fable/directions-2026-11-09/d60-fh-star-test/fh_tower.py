"""d60 tower step: FH* one level up the block lattice, on cross12 only (the only named room
with more than one proper block system).  For block systems Pi_low < Pi_high with Pi_high
minimal above Pi_low, N' = DP / Pi_low plays the role of DP and N = DP / Pi_high the role of
the minimal factor.  N' is handed to fh_star.run_pair_factor as its own pillowcase cover
(Hurwitz moves commute with taking the quotient), with marks on the N'-images of S and T.

Run: python3 -B fh_tower.py [--wall]
"""
import sys
from itertools import combinations
from fh_star import (run_pair_factor, points_of, D, load, room_tuple, lattice_points, status, d4,
                     cycles, O9)


def refines(fine, coarse):
    return all(any(set(b) <= set(c) for c in coarse) for b in fine)


def quotient(t, part):
    tq = tuple(d4.induced(g, part) for g in t)
    where = {s: k for k, b in enumerate(part) for s in b}
    return tq, where


def images(tq_y, where, lifts):
    """N'-points (cycles of the induced corner permutation) under the given DP points."""
    out = []
    cyc = {x: tuple(c) for c in cycles(tq_y) for x in c}
    for L in lifts:
        c = cyc[where[L[0]]]
        if list(c) not in out:
            out.append(list(c))
    return out


def main(wall):
    cells = load(D / 'd41-two-param-cover' / 'rooms' / 'cross12.txt')
    kinds = ('interior', 'smooth') if wall else ('interior',)
    pts = [p for p in lattice_points(cells) if status(cells, p) in kinds]
    for S, T in combinations(pts, 2):
        room, t = room_tuple(cells, S)
        n = len(t[0])
        _, LS = points_of(room, t, S, S)
        y_T, LT = points_of(room, t, T, S)
        reach, _, _ = O9.decide(cells, [S, T], wanted={frozenset((S, T))})
        truth = 'lit' if T in reach[S] else 'dark'
        systems = [P for P in d4.all_block_systems(list(t), n) if 1 < len(P) < n]
        for lo in systems:
            for hi in systems:
                if lo == hi or not refines(lo, hi):
                    continue
                if any(M not in (lo, hi) and refines(lo, M) and refines(M, hi) for M in systems):
                    continue                                   # hi not minimal above lo
                tq, where = quotient(t, lo)
                hi_q = sorted(sorted({where[s] for s in b}) for b in hi)
                IS, IT = images(tq[0], where, LS), images(tq[y_T], where, LT)
                if y_T == 0 and {tuple(c) for c in IS} & {tuple(c) for c in IT}:
                    print('cross12 S=%s T=%s  %d->%d blocks: images already equal in N\' (step vacuous)'
                          ' truth=%s' % (S, T, len(lo), len(hi), truth))
                    continue
                st = run_pair_factor(tq, IS, IT, y_T, hi_q)
                hyp = st['equal_images'] or st['Nlit']
                verdict = ('n/a (not lit in N)' if not hyp else
                           'lifts' if st['Qadm'] else 'NO LIFT')
                strong = (st['witness_no_lift'] == 0) if st['Nlit'] else None
                print('cross12 S=%s T=%s %s  N\'=%d -> N=%d blocks  truth(DP)=%s  lit in N\'=%s  eq_N=%s'
                      ' Nlit=%s  WEAK=%s STRONG=%s -> %s (%d states)'
                      % (S, T, 'abcd'[y_T], len(lo), len(hi), truth, st['Qlit'], st['equal_images'],
                         st['Nlit'], st['Qadm'], strong, verdict, st['states']))


if __name__ == '__main__':
    main('--wall' in sys.argv)
