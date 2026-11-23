#!/usr/bin/env python3
"""d96 stress test at R22's known dark pair (1,3)-(3,5) (file coordinates).

1. The dark pair itself, both orders, must be NOCERT for every B in 4..16.
2. Pairs with S at or near (1,3) and T at or near (3,5) (offsets <= 1/20,
   including S or T exactly at the lattice point, and offsets along the
   diagonals): certified pairs must have a legal path (search radius RMAX).

usage: python3 -B near.py SEED NPAIRS B RMAX
"""
import random
import subprocess
import sys
from fractions import Fraction as F

import test as T_

seed, npairs, B, R = map(int, sys.argv[1:5])
area, W, cl = T_.ROOMS["R22"]
cells = set(cl)
head = "%d %d %s\n" % (area, W, " ".join("%d %d" % c for c in cl))


def ask(pairs, b):
    inp = head
    for S, T in pairs:
        d1 = S[0].denominator * S[1].denominator
        d2 = T[0].denominator * T[1].denominator
        inp += "%d %d %d %d %d %d\n" % (S[0] * d1, S[1] * d1, d1, T[0] * d2, T[1] * d2, d2)
    return subprocess.run([T_.HERE + "/harness", str(b)], input=inp, capture_output=True,
                          text=True, check=True).stdout.split("\n")


A, Bp = (F(1), F(3)), (F(3), F(5))
for b in range(4, 17, 2):
    r = ask([(A, Bp), (Bp, A)], b)
    print("dark pair B=%d: %s | %s" % (b, r[0], r[1]), flush=True)

rng = random.Random(seed)


def near(P):
    mode = rng.random()
    if mode < 0.15:
        return P
    den = rng.randint(21, 400)
    dx, dy = F(rng.randint(-den // 20, den // 20), den), F(rng.randint(-den // 20, den // 20), den)
    if mode < 0.45:
        dy = dx * rng.choice((1, -1))   # on a diagonal through P
    while True:
        Q = (P[0] + dx, P[1] + dy)
        if T_.interior(cells, *Q):
            return Q
        dx, dy = dx / 2, dy / 2


pairs = []
while len(pairs) < npairs:
    S, T = near(A), near(Bp)
    if rng.random() < 0.5:
        S, T = T, S
    if (S, T) not in ((A, Bp), (Bp, A)):
        pairs.append((S, T))
res = ask(pairs, B)
nc = nf = 0
for (S, T), r in zip(pairs, res):
    if r.startswith("CERT"):
        nc += 1
        v = T_.find_path(cells, S, T, R)
        if v is None:
            print("  NOTFOUND S=(%s,%s) T=(%s,%s) %s" % (S[0], S[1], T[0], T[1], r), flush=True)
        else:
            nf += 1
print("near-dark B=%d pairs %d certified %d path_found %d not_found %d" % (B, len(pairs), nc, nf, nc - nf))
