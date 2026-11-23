#!/usr/bin/env python3
"""For a room, list one-cylinder directions (p,q) of DP with 1<=p,q<=B
(strip formula), certify a chosen few with the independent union-find check,
and compute the exceptional set
    X = { s in R^2 : q*s1 + p*s2 in Z and q*s1 - p*s2 in Z for all certified (p,q) }.
By Lemma A, every interior point outside X illuminates every other interior
point. X is a lattice containing Z^2; the script prints X mod Z^2.

Usage: exceptional.py ROOM B
"""
import sys
from fractions import Fraction as Fr
from math import gcd
from cylcount import cyl_count
from onecyl_verify import components


def main(room, B):
    ones = [(p, q) for p in range(1, B + 1) for q in range(1, B + 1)
            if gcd(p, q) == 1 and cyl_count(room, p, q)[0] == 1]
    print(f"room={room}: {len(ones)} one-cylinder directions with 1<=p,q<={B}: {ones}")
    if not ones:
        return
    def X_of(dirs):
        P = 1
        Q = 1
        for p, q in dirs:
            P = P * p // gcd(P, p)
            Q = Q * q // gcd(Q, q)
        out = []
        for i in range(2 * Q):
            for j in range(2 * P):
                s1, s2 = Fr(i, 2 * Q), Fr(j, 2 * P)
                if all((q * s1 + p * s2).denominator == 1 and
                       (q * s1 - p * s2).denominator == 1 for p, q in dirs):
                    out.append((s1, s2))
        return out
    # greedy: smallest certified subset that minimizes X
    chosen = []
    best = None
    for d in sorted(ones, key=lambda d: max(d)):
        trial = chosen + [d]
        x = X_of(trial)
        if best is None or len(x) < len(best):
            c, n, N = components(room, *d)
            if c != 2:
                print(f"  direction {d}: union-find check gives {c} components, NOT certified; skipped")
                continue
            chosen, best = trial, x
            print(f"  certified {d} (grid {N}); |X mod Z^2| = {len(x)}")
        if len(best) == 1:
            break
    print(f"  certified directions used: {chosen}")
    print(f"  X mod Z^2 = {[(str(a), str(b)) for a, b in best]}")


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]))
