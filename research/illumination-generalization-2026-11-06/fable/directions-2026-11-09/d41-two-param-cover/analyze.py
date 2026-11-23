#!/usr/bin/env python3
"""analyze.py RUN.txt... -- per pair: certificate level, and the structure of the uncovered set at the last
listed level before cover: share with odd part of gcd(g_i, Q) > 1 against the uniform baseline, slit-shadow
test (g_i + dup_i = 0 modulo the odd part of L_i * lcm(1..P)), and anti-diagonal concentration."""
import sys, re
from math import gcd, lcm
from collections import Counter
def odd(n):
    while n % 2 == 0: n //= 2
    return n
for fn in sys.argv[1:]:
    hdr = open(fn).readline(); m = re.search(r'dup (\d+),(\d+).*L1=(\d+) L2=(\d+)', hdr)
    d1, d2, L1, L2 = map(int, m.groups())
    U, C = {}, {}
    for ln in open(fn):
        t = ln.split()
        if t[0] == 'UL': U.setdefault(int(t[2]), {}).setdefault(int(t[1]), []).append((int(t[3]), int(t[4])))
        if t[0] == 'C': C[int(t[1])] = ln.strip()
    for i in sorted(C):
        lv = U.get(i, {})
        if not lv: print(f"{fn} pair {i}: {C[i]}; nothing listed"); continue
        p = max(lv); S = lv[p]; lc = lcm(*range(1, p + 1)); Q1, Q2 = 2 * L1 * lc, 2 * L2 * lc
        # slit shadow: g + dup = 0 modulo an odd modulus 2 L p' / gcd(q, 2L) for some p' <= p: i.e. g + dup shares
        # the full odd part of L with... report share with odd(gcd(g+dup, Q)) >= odd(L) * 3 or > 1
        def share(f): return sum(1 for s in S if f(s)) / len(S)
        o1 = share(lambda s: odd(gcd(s[0] + d1, Q1)) > 1); o2 = share(lambda s: odd(gcd(s[1] + d2, Q2)) > 1)
        both = share(lambda s: odd(gcd(s[0] + d1, Q1)) > 1 and odd(gcd(s[1] + d2, Q2)) > 1)
        base1 = sum(1 for a in range(1, Q1, 2) if odd(gcd(a + d1, Q1)) > 1) / (Q1 // 2)
        base2 = sum(1 for a in range(1, Q2, 2) if odd(gcd(a + d2, Q2)) > 1) / (Q2 // 2)
        big = share(lambda s: odd(gcd(s[0] + d1, Q1)) * odd(gcd(s[1] + d2, Q2)) >= 15)
        diag = Counter((a + b) % gcd(Q1, Q2) for a, b in S); anti = Counter((a - b) % gcd(Q1, Q2) for a, b in S)
        d1s = Counter(a for a, b in S); d2s = Counter(b for a, b in S)
        print(f"{fn} pair {i}: {C[i][:40]} | last listed p={p} |U|={len(S)} Q=({Q1},{Q2}) | distinct g1 {len(d1s)} g2 {len(d2s)}"
              f" | odd-gcd>1: g1 {o1:.2f} (base {base1:.2f}) g2 {o2:.2f} (base {base2:.2f}) both {both:.2f} (base {base1*base2:.2f})"
              f" | prod>=15 {big:.2f} | lines g1+g2: {len(diag)} g1-g2: {len(anti)}")
