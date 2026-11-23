"""Independent enumeration of abstract parity targets N -> pillowcase, d <= 6.

Different parametrisation from the audit's enum_targets.py: corner
permutations (gA, gC2, gB, gC1) with gA gC2 gB gC1 = 1, genus from
Riemann-Hurwitz (not Gauss-Bonnet), canonical form by BFS relabelling.
Reports how many tuples the genus condition removes, so the reader can see
that "the formulas hold on the output" is forced by the filter.
"""
import itertools
import sys
from collections import Counter
from fractions import Fraction


def cyc_lengths(p):
    seen, out = set(), []
    for i in range(len(p)):
        if i not in seen:
            L, j = 0, i
            while j not in seen:
                seen.add(j)
                j = p[j]
                L += 1
            out.append(L)
    return sorted(out)


def comp(p, q):          # apply q first
    return tuple(p[x] for x in q)


def inverse(p):
    q = [0] * len(p)
    for i, x in enumerate(p):
        q[x] = i
    return tuple(q)


def canon(gens, d):
    best = None
    for s in range(d):
        new = {s: 0}
        order = [s]
        k = 0
        while k < len(order):
            a = order[k]
            k += 1
            for g in gens:
                b = g[a]
                if b not in new:
                    new[b] = len(order)
                    order.append(b)
        if len(order) < d:
            return None      # not transitive
        key = tuple(tuple(new[g[a]] for a in order) for g in gens)
        if best is None or key < best:
            best = key
    return best


for d in range(1, (int(sys.argv[1]) if len(sys.argv) > 1 else 6) + 1):
    perms = list(itertools.permutations(range(d)))
    t13 = [p for p in perms if set(cyc_lengths(p)) <= {1, 3}]
    t123 = [p for p in perms if set(cyc_lengths(p)) <= {1, 2, 3}]
    reps = {}
    for p in t123:
        reps.setdefault(tuple(cyc_lengths(p)), p)
    found = {}
    genus_removed = set()
    for gA in reps.values():
        for gC2 in t13:
            for gB in t13:
                gC1 = inverse(comp(gA, comp(gC2, gB)))
                if not set(cyc_lengths(gC1)) <= {1, 3}:
                    continue
                key = canon((gA, gC2, gB), d)
                if key is None:
                    continue
                branch = sum(d - len(cyc_lengths(g)) for g in (gA, gC2, gB, gC1))
                if branch != 2 * d - 2:
                    genus_removed.add(key)
                    continue
                found[key] = (gA, gC1, gB, gC2)
    inv_count = Counter()
    bad = 0
    for gA, gC1, gB, gC2 in found.values():
        cA = Counter(cyc_lengths(gA))
        pA, RA, zA = cA[1], cA[2], cA[3]
        zs = {X: Counter(cyc_lengths(g))[3] for X, g in (("C1", gC1), ("B", gB), ("C2", gC2))}
        Zp = sum(zs.values())
        zN = Zp + zA
        if Fraction(Zp) != pA + Fraction(3, 2) * RA + 2 * zA - 1 or zN != d - 1 - Fraction(RA, 2):
            bad += 1
        X = [k for k, v in zs.items() if v == 0]
        inv_count[(zN, pA, RA, zA)] += 1
    print(f"d={d}: {len(found)} parity targets of genus 0; {len(genus_removed)} transitive "
          f"parity tuples of higher genus removed; formula failures on the kept ones: {bad}")
    for k in sorted(inv_count):
        print(f"    (z_N, p_A, R_A, z_A) = {k}: {inv_count[k]}")
