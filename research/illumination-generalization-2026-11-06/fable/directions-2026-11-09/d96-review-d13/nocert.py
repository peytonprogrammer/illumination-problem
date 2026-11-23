#!/usr/bin/env python3
"""List the uncertified pairs of test.py's sampling (same seed), to compare
with cover.c's full-run live points. usage: python3 -B nocert.py SEED NPAIRS B ROOM"""
import random, subprocess, sys
from math import gcd
import test as T_
seed, npairs, B, room = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
rng = random.Random(seed)
kinds = ["G", "G", "E", "L", "L", "L", "V"]
for name, (area, W, cl) in T_.ROOMS.items():
    cells = set(cl)
    pairs = []
    while len(pairs) < npairs:
        S = T_.sample(rng, cells, B, rng.choice(kinds))
        T = T_.sample(rng, cells, B, rng.choice(kinds + ["L", "L"]))
        if S != T and not (S[0].denominator == S[1].denominator == T[0].denominator == T[1].denominator == 1):
            pairs.append((S, T))
    if name != room:
        continue
    inp = "%d %d %s\n" % (area, W, " ".join("%d %d" % c for c in cl))
    for S, T in pairs:
        d1 = S[0].denominator * S[1].denominator // gcd(S[0].denominator, S[1].denominator)
        d2 = T[0].denominator * T[1].denominator // gcd(T[0].denominator, T[1].denominator)
        inp += "%d %d %d %d %d %d\n" % (S[0] * d1, S[1] * d1, d1, T[0] * d2, T[1] * d2, d2)
    out = subprocess.run([T_.HERE + "/harness", str(B)], input=inp, capture_output=True, text=True).stdout.split("\n")
    for (S, T), r in zip(pairs, out):
        if r.startswith("NOCERT"):
            print("NOCERT S=(%s,%s) T=(%s,%s)" % (S[0], S[1], T[0], T[1]))
