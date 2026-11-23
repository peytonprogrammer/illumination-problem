"""D116 checks for generic-line.md steps 1-2. Synthetic and one named room only."""
from fractions import Fraction as F
from decimal import Decimal, getcontext
import random
getcontext().prec = 60

# Check 1: slab rectangles of the four-reflex cross with x half-width 7+t.
# Horizontal bar [-(7+t),7+t]x[-2,2], vertical bar [-2,2]x[-7,7].
def slabs(t):
    xs = sorted({-(7+t), -2, 2, 7+t})
    out = []
    for a, b in zip(xs, xs[1:]):
        mid = (a+b)/2
        h = 14 if abs(mid) < 2 else 4      # height of the vertical run in this slab
        out.append((b-a, 2*h))             # (width d_j(t), circumference c_j)
    return out
print("check1 cross slabs (width, circumference):")
for t in [F(0), F(1,3), F(-1,5)]:
    print("  t=%s" % t, slabs(t))
c0 = [c for _, c in slabs(F(0))]
assert all([c for _, c in slabs(F(k, 7))] == c0 for k in range(-3, 4))
print("  circumferences constant in t:", c0)

# Check 2: twist arithmetic. Random rational a_j, b_j, c_j; t0 = sqrt(2) or pi digits.
def frac(x): return x - int(x) if x >= 0 else x - int(x) + 1
random.seed(116)
t0 = Decimal(2).sqrt()
worst = Decimal(0)
for trial in range(200):
    m = random.randint(2, 6)
    a = [F(random.randint(1, 40), random.randint(1, 9)) for _ in range(m)]
    b = [F(random.randint(-20, 20), random.randint(1, 9)) for _ in range(m)]
    c = [F(random.randint(2, 30), random.randint(1, 5)) for _ in range(m)]
    K = 1
    from math import lcm
    for j in range(m):
        K = lcm(K, (a[j]/c[j]).denominator, (b[j]/c[j]).denominator)
    eta = Decimal(random.randint(-500, 500)) / 10000
    target = frac(eta / K)
    # find n <= 2e5 with frac(n t0) closest to target
    best, bn = Decimal(2), None
    x = Decimal(0)
    for n in range(1, 200001):
        x += t0
        f = x - int(x)
        e = abs(f - target); e = min(e, 1 - e)
        if e < best: best, bn = e, n
    s = K * bn
    for j in range(m):
        dj = Decimal(a[j].numerator)/a[j].denominator + Decimal(b[j].numerator)/b[j].denominator * t0
        cj = Decimal(c[j].numerator)/c[j].denominator
        tw = (s * dj) % cj
        want = (eta * Decimal(b[j].numerator)/b[j].denominator) % cj
        err = abs(tw - want); err = min(err, cj - err)
        worst = max(worst, err / (K*abs(Decimal(b[j].numerator)/b[j].denominator)+1))
    if trial < 3:
        print("check2 trial", trial, "K=%d n=%d |frac(n t0)-eta/K|=%.2e" % (K, bn, best))
print("check2: 200 trials, max normalized twist error = %.2e (bound ~ |frac err|)" % worst)

# Check 3 (control): rational t0 gives a finite twist orbit, so the arc is not reached.
t0r = F(3, 7); a, b, c = F(2), F(1), F(5)
vals = sorted({(n*(a+b*t0r)) % c for n in range(1, 500)})
print("check3 control: rational t0=3/7 twist values mod c:", len(vals), "distinct")
