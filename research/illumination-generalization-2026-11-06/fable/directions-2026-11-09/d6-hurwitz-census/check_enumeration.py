"""Independent brute-force check of enumerate_tuples.py for small n.

Loops over ALL (g_a, g_b, g_c) in A^3 (A = cycle lengths <= 3), sets g_d = (g_a g_b g_c)^-1,
keeps transitive genus-0 tuples with g_d in A, and dedupes by canon_plain.  Also checks the
orbit-counting identity  #labelled tuples = sum over classes of n!/|Aut|.

Run: python3 -B check_enumeration.py 6   (n = 6 takes a few minutes)
"""
import sys
from math import factorial

from hurwitz import mul, inv, is_transitive, canon_plain, decode
from enumerate_tuples import allowed_perms, enumerate_n, enumerate_n_by_class, ind


def automorphisms(t, n):
    """Number of permutations commuting with every generator (transitive t)."""
    count = 0
    for y in range(n):
        phi = {0: y}
        q = [0]
        ok = True
        for x in q:
            for g in t:
                a, b = g[x], g[phi[x]]
                if a in phi:
                    if phi[a] != b:
                        ok = False
                        break
                else:
                    phi[a] = b
                    q.append(a)
            if not ok:
                break
        if ok and len(set(phi.values())) == n:
            count += 1
    return count


def main():
    n = int(sys.argv[1])
    A = allowed_perms(n)
    Aset = set(A)
    indA = {p: ind(p) for p in A}
    target = 2 * n - 2
    labelled = 0
    classes = set()
    for a in A:
        for b in A:
            ab = mul(a, b)
            s = indA[a] + indA[b]
            if s > target:
                continue
            for c in A:
                if s + indA[c] > target:
                    continue
                d = inv(mul(ab, c))
                if d not in Aset or s + indA[c] + indA[d] != target:
                    continue
                t = (a, b, c, d)
                if is_transitive(t, n):
                    labelled += 1
                    classes.add(canon_plain(t))
    tuples, stats = enumerate_n(n, log=lambda *x: None)
    mine = {canon_plain(t) for t in tuples}
    by_class = {canon_plain(t) for t in enumerate_n_by_class(n)}
    mass = sum(factorial(n) // automorphisms(decode(k, n, False)[0], n) for k in mine)
    print('n', n, 'brute-force classes', len(classes), 'enumerate_tuples classes', len(mine),
          'equal', classes == mine, '| per-class enumerator equal', by_class == mine, '| labelled brute', labelled, 'mass formula', mass, 'equal', labelled == mass)
    assert classes == mine == by_class and labelled == mass


if __name__ == '__main__':
    main()
