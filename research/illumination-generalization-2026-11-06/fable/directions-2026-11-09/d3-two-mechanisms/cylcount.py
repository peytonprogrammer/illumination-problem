#!/usr/bin/env python3
"""Count cylinders of the unfolding M (marked at every corner lift) in a
rational direction (p,q), p,q != 0, for a unit-cell room.

Method. Every corner lift lies on a line q*x - p*y in Z (unfolded coordinates).
A strip is the region between two consecutive such lines; it has no marked
point, so it lies in one cylinder. Two strips sharing an integer-line leaf lie
in one cylinder exactly when that leaf is regular (closed, no corner). Hence

    #cyl(M) = #strips - #regular integer-line leaves.

Take a prime N not dividing p*q. Every leaf on a line of class +-1/N and every
integer-line leaf passes through interior (1/N)-grid points, so leafcheck's
tracer finds them all. Each strip has exactly two leaves of class +-1/N.
The half-turn tau never fixes a cylinder (its fixed points are corner lifts),
so #cyl(DP) = #cyl(M)/2.

Usage: cylcount.py ROOM B      (lists directions with max(p,q) <= B)
"""
import sys
from math import gcd
from leafcheck import build, forward, neg


def cyl_count(room, p, q, cache={}):
    N = next(n for n in (3, 5, 7, 11, 13, 17, 19, 23) if (p * q) % n)
    key = (room, N)
    if key not in cache:
        cache[key] = build(room, N)
    cells, pts = cache[key]
    seen = set()
    strips2 = 0   # closed leaves of class +-1
    regular0 = 0  # regular closed leaves of class 0
    sing_pts = set()  # interior lattice points lying on singular leaves
    for pt in pts:
        for d in ((p, q), (-p, q), (p, -q), (-p, -q)):
            c = (d[1] * pt[0] - d[0] * pt[1]) % N
            if c not in (0, 1, N - 1) or (pt, d) in seen:
                continue
            F, closed = forward(cells, N, pt, d)
            chain = [(pt, d)] + F
            if c != 0:
                assert closed
                strips2 += 1
                seen.update(chain)
            elif closed:
                regular0 += 1
                seen.update(chain)
            else:
                Bk, _ = forward(cells, N, pt, neg(d))
                full = chain + [(s[0], neg(s[1])) for s in Bk]
                seen.update(full)
                for s in full:
                    if s[0][0] % N == 0 and s[0][1] % N == 0:
                        sing_pts.add((s[0][0] // N, s[0][1] // N))
    assert strips2 % 2 == 0
    cylM = strips2 // 2 - regular0
    assert cylM % 2 == 0
    return cylM // 2, sorted(sing_pts)


if __name__ == "__main__":
    room, B = sys.argv[1], int(sys.argv[2])
    hist = {}
    for p in range(1, B + 1):
        for q in range(1, B + 1):
            if gcd(p, q) != 1:
                continue
            for sq in (1, -1):
                n, sing = cyl_count(room, p, sq * q)
                hist[n] = hist.get(n, 0) + 1
                if n == 1:
                    print(f"one-cylinder on DP: ({p},{sq*q})  interior lattice points on singular leaves: {sing}")
    print(f"room={room} B={B} histogram of #cyl(DP): {sorted(hist.items())}")
