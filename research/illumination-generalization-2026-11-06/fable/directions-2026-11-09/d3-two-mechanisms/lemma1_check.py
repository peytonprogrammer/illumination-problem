#!/usr/bin/env python3
"""Brute-force check of Lemma 1 (torus-level blocking) of audit.md.

For s in (1/N)Z^2 cap [0,1)^2 and u in (1/N)Z^2 cap [0,2)^2 (u stands for one
reflected image class gamma*t + 2Z^2), enumerate candidates t' = u + 2m,
|m_i| <= M, t' != s, and the lattice points in the open segment (s,t').
Compare 'every candidate meets a C-class lattice point' with the prediction:
  (a) u != -s and not (s lattice and u == s) mod 2Z^2: a candidate avoiding
      Z^2 exists (never blocked, for every C);
  (b) u == -s mod 2Z^2, s not lattice: blocked iff C is all four classes;
  (c) s lattice, u == s mod 2Z^2: blocked iff C contains the three classes
      other than the class of s.
The enumeration bound M can only under-report clean candidates, so the test
also asserts that the predicted clean candidate is found within M.
"""
from fractions import Fraction as Fr
from itertools import combinations
from math import gcd, floor, ceil


def lattice_classes_on_open_segment(s, t):
    """Set of classes mod 2 of lattice points strictly inside segment s->t."""
    d = (t[0] - s[0], t[1] - s[1])
    out = set()
    # lattice points z = s + lam*d, 0<lam<1
    if d[0] != 0:
        lo, hi = sorted((s[0], t[0]))
        for x in range(floor(lo), ceil(hi) + 1):
            lam = (x - s[0]) / d[0]
            if 0 < lam < 1:
                y = s[1] + lam * d[1]
                if y.denominator == 1:
                    out.add((x % 2, int(y) % 2))
    else:
        if s[0].denominator == 1:
            lo, hi = sorted((s[1], t[1]))
            for y in range(floor(lo), ceil(hi) + 1):
                if lo < y < hi:
                    out.add((int(s[0]) % 2, y % 2))
    return out


def main(Nmax=6, M=3):
    ALL = [(0, 0), (1, 0), (0, 1), (1, 1)]
    Cs = [frozenset(ALL)] + [frozenset(c) for c in combinations(ALL, 3)]
    checked = 0
    for N in range(1, Nmax + 1):
        for a in range(N):
            for b in range(N):
                s = (Fr(a, N), Fr(b, N))
                s_lat = s[0].denominator == 1 and s[1].denominator == 1
                for c in range(2 * N):
                    for e in range(2 * N):
                        u = (Fr(c, N), Fr(e, N))
                        anti = ((u[0] + s[0]) / 2).denominator == 1 and ((u[1] + s[1]) / 2).denominator == 1
                        same = ((u[0] - s[0]) / 2).denominator == 1 and ((u[1] - s[1]) / 2).denominator == 1
                        cands = []
                        for m1 in range(-M, M + 1):
                            for m2 in range(-M, M + 1):
                                t = (u[0] + 2 * m1, u[1] + 2 * m2)
                                if t != s:
                                    cands.append(lattice_classes_on_open_segment(s, t))
                        for C in Cs:
                            blocked = all(cl & C for cl in cands)
                            if s_lat and same:
                                pred = set(ALL) - {(int(s[0]) % 2, int(s[1]) % 2)} <= C
                            elif anti:
                                pred = C == frozenset(ALL)
                            else:
                                pred = False
                                assert any(not cl for cl in cands), (s, u)
                            assert blocked == pred, (N, s, u, sorted(C), blocked, pred)
                            checked += 1
    print(f"Lemma 1 brute force: {checked} (s, image class, C) cases agree, N<={Nmax}, |m|<={M}")


if __name__ == "__main__":
    main()
