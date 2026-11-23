"""Independent plane tracer (reflection law in the room plane, no unfolding tables).
Cross-checks adv's shortest corner-free segment length for every same-class pair.
usage: xcheck.py roomsfile   (lines: "A x0 y0 ...")"""
import sys, subprocess, math
from math import gcd

def kcells(cells, X, Y):
    return [(X - 1, Y - 1) in cells, (X, Y - 1) in cells, (X - 1, Y) in cells, (X, Y) in cells]

def step(cells, X, Y, gx, gy, p, q):
    """One primitive lattice step from lattice point (X,Y), room direction (gx*p, gy*q).
    Returns (X,Y,gx,gy) at the next lattice point, before the reflection there."""
    i, j = X - (gx < 0), Y - (gy < 0)
    assert (i, j) in cells
    a = b = 1
    while a < p or b < q:
        if a * q < b * p:
            a += 1
            if (i + gx, j) in cells: i += gx
            else: gx = -gx
        else:
            b += 1
            if (i, j + gy) in cells: j += gy
            else: gy = -gy
    return i + (gx > 0), j + (gy > 0), gx, gy

def minlens(cells, S, L2):
    """dict T -> min squared length of a corner-free path from S, length^2 <= L2."""
    out = {}
    R = int(math.isqrt(L2)) // 2 + 1
    for p in range(0, R + 1):
        for q in range(0, R + 1):
            if gcd(p, q) != 1 or 4 * (p * p + q * q) > L2: continue
            for gx0 in (1, -1):
                for gy0 in (1, -1):
                    if (q == 0 and gy0 < 0) or (p == 0 and gx0 < 0): continue
                    X, Y, gx, gy = S[0], S[1], gx0, gy0
                    m = 0
                    while True:
                        m += 1
                        if m * m * (p * p + q * q) > L2: break
                        if q == 0: X += gx
                        elif p == 0: Y += gy
                        else: X, Y, gx, gy = step(cells, X, Y, gx, gy, p, q)
                        k = kcells(cells, X, Y); n = sum(k)
                        if n in (1, 3): break
                        if n == 2:
                            if k[0] == k[2]: gx = -gx     # both left or both right cells: vertical wall
                            else: gy = -gy
                        elif m % 2 == 0 and (X, Y) != S:
                            v = m * m * (p * p + q * q)
                            if v < out.get((X, Y), 1 << 60): out[(X, Y)] = v
                        if (X, Y) == S and (gx, gy) == (gx0, gy0): break
    return out

bad = tot = 0
for line in open(sys.argv[1]):
    v = list(map(int, line.split())); A = v[0]
    cells = set(zip(v[1::2], v[2::2])); assert len(cells) == A
    res = subprocess.run(["./adv", "check", "2", "8", "v"], input=line, capture_output=True, text=True).stdout
    want = {}; sym = 0
    for l in res.splitlines():
        if l.startswith("P "):
            f = l.split(); want[(int(f[1]), int(f[2]), int(f[3]), int(f[4]))] = int(f[5]); sym += f[6] != f[7]
        if l.startswith("UNLIT"): want[tuple(map(int, l.split()[1:]))] = None
    srcs = {}
    for (a, b, c, d), w in want.items(): srcs.setdefault((a, b), []).append(((c, d), w))
    nb = 0
    for S, lst in srcs.items():
        L2 = max([w for _, w in lst if w is not None] or [120 * 120])
        got = minlens(cells, S, L2)
        for T, w in lst:
            tot += 1
            if got.get(T) != w: nb += 1; print("MISMATCH", S, T, w, got.get(T))
    bad += nb
    print("room A", A, "pairs", len(want), "mismatches", nb, "count-asymmetries", sym, flush=True)
print("TOTAL pairs", tot, "mismatches", bad)
