"""Exact checks for d195 snapshot.md (sha256 prefix 800033b9).

Uses only parameters named in the note: e, s, B, j, l (ell), A, v, Z, P, k,
the strip (lo, hi), eta, H, b, rho, K. No room, ray, direction, word, or size
search. Exact rationals throughout.
"""
import random
import time
from fractions import Fraction as F
from math import ceil, floor

random.seed(195)
t0 = time.process_time()
results = []


def check(name, ok, detail=""):
    results.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {detail}")


def rq(lo, hi, den=37):
    return F(random.randint(lo * den, hi * den), den)


def mod(x, m):
    return x - m * floor(x / m)


# 1. Endpoint equation and the three phases y-Av, y, y+Av.
n1 = bad = 0
for _ in range(20000):
    Z = rq(1, 6)
    C = 2 * Z
    j = F(random.randint(1, 5))
    ell = rq(0, 1) * j
    B, A, v = rq(1, 5), F(random.randint(1, 4)), rq(-1, 1, 101)
    e, s = rq(0, 12), rq(0, 12)
    rhs = mod(e - s - (B + 2 * j - ell + 2 * A) * v, C)
    y0 = (e + s - (B + ell) * v) / 2
    for rep in (0, 1):  # two solutions z modulo C
        z = rhs / 2 + rep * Z
        p1 = s + (j - ell) * v + z      # first gate contact
        p2 = p1 + A * v                  # far wall
        p3 = p2 + A * v                  # return to gate
        n1 += 1
        before = p3 + j * v + z          # phase at the target-side edge
        ok = mod(before - (e - B * v), C) == 0
        ok &= mod(p1 - (y0 - A * v), Z) == 0 and mod(p2 - y0, Z) == 0 and mod(p3 - (y0 + A * v), Z) == 0
        # the two representatives differ by exactly Z (two midpoint candidates mod 2Z)
        if not ok:
            bad += 1
check("endpoint equation and phases y-Av, y, y+Av (both z reps)", bad == 0, f"{n1} cases")

# 2. Open-strip test: endpoints strictly inside <=> whole two-leg path strictly inside.
n2 = bad = 0
for _ in range(20000):
    lo, hi = rq(0, 3), rq(3, 7)
    y, A, v = rq(-1, 8), F(random.randint(1, 4)), rq(-1, 1, 53)
    pts = [y - A * v + F(i, 40) * 2 * A * v for i in range(41)]  # piecewise-linear, same slope
    inside_all = all(lo < p < hi for p in pts)
    test = lo + abs(A * v) < y < hi - abs(A * v)
    n2 += 1
    if inside_all != test:
        bad += 1
check("strip test l+|Av|<y<r-|Av| iff path stays strictly in strip", bad == 0, f"{n2} cases")


# 3. Period shift with solid strip walls: folding preserves exit height and sign
#    when kP*A is a multiple of 2(hi-lo); generic shifts do not.
def fold(h0, dv, A, lo, hi):
    """Enter at height h0 with vertical speed dv per unit horizontal, travel A.
    Return (exit height, sign of vertical velocity) after reflections at lo, hi."""
    L = hi - lo
    u = mod(h0 - lo + dv * A, 2 * L)
    sgn = 1 if dv > 0 else -1
    if u <= L:
        return lo + u, sgn
    return lo + 2 * L - u, -sgn


n3 = bad = 0
for _ in range(5000):
    lo = F(random.randint(0, 3))
    hi = lo + random.randint(1, 4)
    A = F(random.randint(1, 5))
    L = hi - lo
    h0 = rq(int(lo), int(hi))
    if not lo < h0 < hi:
        continue
    v = rq(0, 1, 97)  # positive vertical speed; P > 0
    if v == 0:
        continue
    k = random.randint(1, 6)
    # P a multiple of 2L so that kP*A is a multiple of 2L
    P = 2 * L * random.randint(1, 3)
    e0 = fold(h0, v, A, lo, hi)
    e1 = fold(h0, v + k * P, A, lo, hi)
    n3 += 1
    if e0 != e1:
        bad += 1
check("period shift kPA = 0 mod 2L preserves signed exit", bad == 0, f"{n3} cases")
# a shift with kPA not a multiple of 2L changes the exit for some example
ex = fold(F(1, 2), F(1, 10), F(1), F(0), F(1)) != fold(F(1, 2), F(1, 10) + 1, F(1), F(0), F(1))
check("shift with kPA not = 0 mod 2L can change the exit", ex)

# 4. Strip excursion at v+kP: even when the base path stays in the strip, the
#    shifted path reflects off lo/hi; with solid walls and kPA = 0 mod 2L the
#    return height equals base return y+Av (signed).
n4 = bad = 0
for _ in range(5000):
    lo, L = F(random.randint(0, 3)), random.randint(1, 4)
    hi = lo + L
    A, v = F(random.randint(1, 4)), rq(0, 1, 211)
    if v == 0:
        continue
    y = rq(int(lo), int(hi), 59)
    if not lo + A * v < y < hi - A * v:
        continue
    P, k = 2 * L, random.randint(1, 5)
    h1, s1 = fold(y - A * v, v + k * P, A, lo, hi)   # out to far wall
    h2, s2 = fold(h1, s1 * (v + k * P), A, lo, hi)   # back (same vertical velocity)
    n4 += 1
    if not (h1 == y and h2 == y + A * v and s2 == 1):
        bad += 1
check("shifted excursion returns at y+Av with same vertical sense", bad == 0, f"{n4} cases")

# 5. q0 bound: if the mismatch sweep (B+l)eta >= C/q0 a grid residue is hit,
#    so direct failure forces q0 < C/((B+l)eta) <= C/(B eta) <= 2(H*+bmax)/(Bmin eta).
n5 = bad = 0
for _ in range(3000):
    H, b = rq(1, 4, 7), F(random.randint(1, 4))
    C = 2 * (H + b)
    ell, P = rq(0, 2, 11), F(random.randint(1, 6))
    B, eta, s, e = rq(1, 3, 5), rq(0, 1, 13), rq(0, 9), rq(0, 9)
    if ell == 0 or eta == 0:
        continue
    q0 = (ell * P / C).denominator
    v0 = rq(0, 2, 17)
    # mismatch m(v) = e - Bv - s - l v on [v0, v0+eta]; grid {k l P mod C}
    grid = sorted(mod(kk * ell * P, C) for kk in range(q0))
    m_hi = mod(e - B * v0 - s - ell * v0, C)
    sweep = (B + ell) * eta
    hit = any(mod(m_hi - g, C) <= sweep for g in grid)
    n5 += 1
    if sweep >= C / q0 and not hit:
        bad += 1
    if not hit and not (q0 < C / (sweep) <= C / (B * eta)):
        bad += 1
    Hs, bmax, Bmin = H + rq(0, 2), b + random.randint(0, 2), B - rq(0, 1, 5) / 2
    if Bmin > 0 and not (C / (B * eta) <= 2 * (Hs + bmax) / (Bmin * eta)):
        bad += 1
check("q0 <= 2(H+b)/(B eta) <= 2(H*+bmax)/(Bmin eta) on direct failure", bad == 0, f"{n5} cases")

# 6. K tail: K = 1+ceil(8/(pi^2 rho^3)) gives 4/(pi^2 K rho^3) < 1/2.
PI_LO = F(31415926535897932384626433832795, 10 ** 31)
PI_HI = PI_LO + F(1, 10 ** 31)
n6 = bad = 0
for den in range(9, 200):
    for r in (F(1, den), F(3, 4 * den)):
        lo_val, hi_val = 8 / (PI_HI ** 2 * r ** 3), 8 / (PI_LO ** 2 * r ** 3)
        K = 1 + ceil(lo_val)
        n6 += 1
        # K is determined exactly when both pi bounds give the same ceiling
        if ceil(lo_val) != ceil(hi_val) or not 4 / (PI_LO ** 2 * K * r ** 3) < F(1, 2):
            bad += 1
check("K tail below 1/2 for rho < 1/8", bad == 0, f"{n6} rho values")

# 7. Small-v remark: a contact approaching a strip end at rate c (y - lo = c v)
#    passes the strip test at small v iff c > A. So "v near zero" alone does not settle it.
ok = True
for c in (F(1, 2), F(1), F(2)):
    for A in (F(1), F(3, 2)):
        passes = all((F(0) + abs(A * v) < c * v) for v in (F(1, 10 ** p) for p in range(1, 8)))
        ok &= passes == (c > A)
check("endpoint-approach clearance at small v holds iff rate > A", ok)

cpu = time.process_time() - t0
print(f"\n{sum(results)}/{len(results)} checks passed, {len(results) - sum(results)} failures, {cpu:.1f} CPU-s")
