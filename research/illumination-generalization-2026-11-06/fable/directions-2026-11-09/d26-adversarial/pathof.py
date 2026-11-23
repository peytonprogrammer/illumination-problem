"""Shortest corner-free path for one pair, by the independent plane tracer of xcheck.py.
usage: pathof.py roomfile sx sy tx ty Lmax   -> prints (p,q), signs, steps m, length"""
import sys, math
from math import gcd
src = open("xcheck.py").read().split("bad = tot = 0")[0]
exec(src)
v = list(map(int, open(sys.argv[1]).readline().replace("ROOM", "").split())); cells = set(zip(v[1::2], v[2::2]))
S = (int(sys.argv[2]), int(sys.argv[3])); T = (int(sys.argv[4]), int(sys.argv[5])); L2 = int(sys.argv[6]) ** 2
best = []
R = int(math.isqrt(L2)) // 2 + 1
for p in range(R + 1):
    for q in range(R + 1):
        if gcd(p, q) != 1 or 4 * (p * p + q * q) > L2: continue
        for gx0 in (1, -1):
            for gy0 in (1, -1):
                if (q == 0 and gy0 < 0) or (p == 0 and gx0 < 0): continue
                X, Y, gx, gy, m = S[0], S[1], gx0, gy0, 0
                while True:
                    m += 1
                    if m * m * (p * p + q * q) > L2: break
                    if q == 0: X += gx
                    elif p == 0: Y += gy
                    else: X, Y, gx, gy = step(cells, X, Y, gx, gy, p, q)
                    k = kcells(cells, X, Y); n = sum(k)
                    if n in (1, 3): break
                    if n == 2:
                        if k[0] == k[2]: gx = -gx
                        else: gy = -gy
                    elif (X, Y) == T and m % 2 == 0: best.append((m * math.hypot(p, q), p * gx0, q * gy0, m)); break
                    if (X, Y) == S and (gx, gy) == (gx0, gy0): break
best.sort()
print("paths found:", len(best), "shortest five (length, dx, dy, steps):", [(round(a, 2), b, c, d) for a, b, c, d in best[:5]])
