"""Cross-checks of the light decider on the whole census at small n.

1. Orbit invariance.  For EVERY tuple whose g_a has >= 2 two-cycles, rerun the marked
   pure-braid orbit and the factor analysis from that tuple in its own labelling.  All
   tuples of one pure-braid orbit must give the same multiset of per-pair verdicts
   (lit, original-conjecture prediction, G1 prediction) and the same orbit sizes.
2. s2^2 redundancy.  Adding s2^2 and its inverse to the pure generators changes no
   orbit size and no lit set.
3. Independent arc scheme.  Run the FULL braid group B_4 (s0, s1, s2 and inverses, corner
   labels carried, 'a' at any position) and use the tail arc between the position of 'a'
   and EVERY other position.  The lit set must equal the pure-braid lit set.

Run: python3 -B check_orbit_invariance.py 7
"""
import sys
from collections import Counter, deque

from hurwitz import (marked_orbit, plain_orbit, initial_pt, move, canon_plain, arc_components,
                     PURE_GENS_WITH_S2, _relabel, _encode)
from enumerate_tuples import ClassEnumerator, genus0_classes
from census import analyse_orbit


def b4_lit(t):
    labels = ('a', 'b', 'c', 'd')
    pt, plen = initial_pt(t[0])
    n = len(t[0])

    def canon(t_, L, pt_):
        ia = L.index('a')
        roots = [i for i in range(n) if pt_[i] == 0]
        best = None
        for r in roots:
            lab, order = _relabel(t_, r)
            e = (L, _encode(t_, lab, order, pt_))
            if best is None or e < best:
                best = e
        return best

    seen = {canon(t, labels, pt)}
    q = deque([(t, labels, pt)])
    lit = set()
    while q:
        t_, L, pt_ = q.popleft()
        ia = L.index('a')
        for j in range(4):
            if j == ia:
                continue
            for comp in arc_components(t_[ia], pt_, plen, t_[j]):
                cl = sorted(comp)
                for x in range(len(cl)):
                    for y in range(x + 1, len(cl)):
                        lit.add(frozenset((cl[x], cl[y])))
        for i in range(3):
            for s in (1, -1):
                t2, L2, pt2 = move(t_, L, pt_, i, s)
                c = canon(t2, L2, pt2)
                if c not in seen:
                    seen.add(c)
                    q.append((t2, L2, pt2))
    return lit, len(seen)


def main():
    n = int(sys.argv[1])
    E = ClassEnumerator(n)
    stats = Counter()
    for cts in genus0_classes(n):
        found = E.enumerate_class(cts)
        sig_of_orbit = {}
        for key, t in found.items():
            pt0, plen = initial_pt(t[0])
            if sum(1 for L in plen if L == 2) < 2:
                continue
            res = marked_orbit(t)
            a = analyse_orbit(t, n, res['lit'], plen, pt0)
            sig = (res['states'], tuple(sorted((p['lit'], p['predicted_dark'], p['g1_predicted_dark'])
                                               for p in a['pairs'])))
            orb = frozenset(plain_orbit(t))
            stats['tuples_checked'] += 1
            if orb in sig_of_orbit:
                assert sig_of_orbit[orb] == sig, (cts, t)
                stats['agree_with_orbit_mate'] += 1
            else:
                sig_of_orbit[orb] = sig
                stats['orbits'] += 1
                r2 = marked_orbit(t, gens=PURE_GENS_WITH_S2)
                assert r2['states'] == res['states'] and r2['lit'] == res['lit']
                stats['s2sq_redundant'] += 1
                lit_b4, size_b4 = b4_lit(t)
                assert lit_b4 == res['lit'], (cts, t, lit_b4, res['lit'])
                stats['b4_scheme_agrees'] += 1
                stats['b4_states_total'] += size_b4
    print('n', n, dict(stats))


if __name__ == '__main__':
    main()
