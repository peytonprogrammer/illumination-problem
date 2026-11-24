"""D215 referee checks: ratio compactness (note-snapshot.md).

Reuses the d212 exact integer-scaled tracer and the d213 staircase helper
stair_room, imported unchanged. Named room only:
  STAIR : offset staircase x[0,3],[1,4],[3,6],[4,7], heights 2,1+x,1+y,2
          (and a y-scaled copy for rational gains); T=(5, roof-1).
  Claim 5: S=(2,1).  Claim 6: S=(1,1).
No room enumeration and no direction, word or room-size search: every traced
ray is the note's prescribed direction (k, D) or (6, D).
Run: nice -n 10 python3 -B checks.py
"""
import importlib.util
import os
import random
import time
from fractions import Fraction as F
from math import gcd, isqrt, floor

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, "..", rel, "checks.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


K = load("d212checks", "d212-review-descent-skeleton")
M13 = load("d213checks", "d213-review-marked-selection")
rects, trace, reached = K.rects, K.trace, K.reached
stair_room = M13.stair_room

T0 = time.process_time()
FAILS = []
f2 = lambda t: isqrt(2 * t * t)
f15 = lambda x: isqrt(x ** 3)


def say(*a):
    print(*a, flush=True)


def check(cond, msg):
    say(("PASS " if cond else "FAIL ") + msg)
    if not cond:
        FAILS.append(msg)


def shoot(c, S, v, T):
    """Trace from S with (not necessarily primitive) developed displacement v; reach T exactly."""
    g = gcd(abs(v[0]), abs(v[1]))
    return reached(trace(c, S, (v[0] // g, v[1] // g), g), T)


def stair_q(p, r, q):
    """Staircase with rational gains p/q, r/q, y-axis scaled by q (diagonal scaling)."""
    h = [2 * q, q + p, q + r, 2 * q]
    ys = [0, h[0], h[0] + h[1], h[0] + h[1] + h[2], sum(h)]
    xs = [(0, 3), (1, 4), (3, 6), (4, 7)]
    return rects(*[(xs[i][0], xs[i][1], ys[i], ys[i + 1]) for i in range(4)])


# ------------------------------------------------------------------ claim 5
def ks35(alpha, kmax=None):
    """All k = 3,5 mod 6 with 1 < k*alpha < 2."""
    lo = floor(1 / alpha) + 1
    return [k for k in range(lo, int(2 / alpha) + 1) if k % 6 in (3, 5) and 1 < k * alpha < 2]


def claim5_room(x, y, q=1, allk=False):
    """Return (#k tried, #legal). x,y are numerators over q."""
    c = stair_q(x, y, q) if q > 1 else stair_room(x, y)
    Dq = 4 * q + x + y                       # scaled axial travel
    S, T = (2, q), (5, q + 4 * q + x + y)    # roof - q
    lower = min(x, y)
    alpha = F(lower + 2 * q, Dq)
    ks = ks35(alpha)
    if not allk: ks = ks[:1]
    ok = 0
    for k in ks:
        if x <= y:
            ok += shoot(c, S, (k, Dq), T)
        else:                                 # 180-degree rotation: start at T, go down-left
            ok += shoot(c, T, (-k, -Dq), S)
    return len(ks), ok


def claim5():
    say("\n=== Claim 5: reflected construction, lower mark x=2")
    # existence of k: union of (1/k, 2/k) over k=3,5 mod 6 covers (0, 2/3)
    seq = [k for k in range(3, 10 ** 5) if k % 6 in (3, 5)]
    check(all(b < 2 * a for a, b in zip(seq, seq[1:])), "k_{i+1} < 2 k_i for k=3,5 mod 6 up to 1e5 (5<6, 9<10, ...)")
    check(all(ks35(F(a, 1000)) for a in range(1, 667)), "a valid k exists for alpha = j/1000, j=1..666")
    # grid 0..60 each, smallest k
    bad = []; n = 0
    for x in range(61):
        for y in range(61):
            nk, ok = claim5_room(x, y)
            n += 1
            if not (nk >= 1 and ok == nk): bad.append((x, y))
    check(not bad, f"integer grid 0<=x,y<=60 ({n} rooms, both orders via start at T when x>y): smallest k legal and reaches (bad {bad[:10]})")
    # every admissible k on a smaller grid
    bad = []; tot = 0
    for x in range(0, 31, 3):
        for y in range(0, 31):
            nk, ok = claim5_room(x, y, allk=True)
            tot += nk
            if ok != nk: bad.append((x, y))
    check(not bad, f"every admissible k (not only the smallest), x in 0..30 step 3, y 0..30: {tot} traces, all legal")
    # x^1.5 and sqrt2 samples
    bad = []; kk = []
    for x in range(0, 201):
        y = f15(x)
        nk, ok = claim5_room(x, y)
        if not (nk and ok == nk): bad.append(x)
        alpha = F(x + 2, 4 + x + y); kk.append((x, ks35(alpha)[0]))
    check(not bad, f"y=floor(x^1.5), x=0..200: smallest k legal (bad {bad})")
    say(f"    sample k on x^1.5 curve: {[p for p in kk if p[0] in (4, 16, 49, 100, 144, 196)]}  (order sqrt x)")
    bad = [t for t in range(0, 201) if claim5_room(t, f2(t)) != (1, 1)]
    bad += [t for t in range(0, 201) if claim5_room(f2(t), t) != (1, 1)]
    check(not bad, f"sqrt2 family t=0..200, both orders: smallest k legal (bad {bad})")
    # rational (real) gains through y-scaling
    bad = []; n = 0
    for q in (2, 3, 7):
        for x in range(0, 40, 3):
            for y in range(0, 40, 5):
                nk, ok = claim5_room(x, y, q)
                n += 1
                if not (nk and ok == nk): bad.append((x, y, q))
    check(not bad, f"rational gains x/q, y/q with q in 2,3,7 ({n} rooms): construction legal (bad {bad[:5]})")


# ------------------------------------------------------------------ claim 6
def region(a, b, c):
    return b + c - 2 * a > 0 and c - b > 0 and 2 * a + 2 * b - c > 0


def claim6():
    say("\n=== Claim 6: nondirect pair, lower mark x=1")
    x, y = 15, 21; D = 4 + x + y
    xs = [1 + F(6 * t, D) for t in (1, 2 + x, D - 1)]
    phys = [v if v <= 6 else 12 - v for v in xs]
    check(phys == [F(23, 20), F(71, 20), F(103, 20)] and 1 + F(4 * 17, 40) == F(27, 10),
          f"(15,21): crossings {phys}; direct middle abscissa {1 + F(68, 40)} outside (3,4)")
    c = stair_room(15, 21)
    S, T = (1, 1), (5, 5 + x + y)
    check(len(c) == 126 and shoot(c, S, (6, D), T) and not shoot(c, S, (4, D), T),
          "(15,21): area 126; ray (6,40) legal and reaches T; direct chord (4,40) not legal")
    # region vs trace on integer grid (a=1,b=x,c=y)
    miss = []; extra = []; inside = 0; direct_in = 0
    mirror = lambda a, b, c: b + c - 2 * a > 0 and b - c > 0 and 2 * a + 2 * c - b > 0
    for x in range(61):
        for y in range(61):
            c = stair_room(x, y); D = 4 + x + y; T = (5, 5 + x + y)
            r = region(1, x, y)
            inside += r
            leg = shoot(c, (1, 1), (6, D), T)
            if r and not leg: miss.append((x, y))
            if leg and not r: extra.append((x, y))
            if r: direct_in += shoot(c, (1, 1), (4, D), T)
    check(not miss, f"grid 0..60: region => ray (6,D) legal and reaches T ({inside} inside; failures {miss[:10]})")
    check(all(mirror(1, x, y) for x, y in extra) and len(extra) == sum(mirror(1, x, y) for x in range(61) for y in range(61)),
          f"observation (not claimed by the note): (6,D) also lights the {len(extra)} grid rooms of the mirror region "
          "b>c, 2a+2c-b>0, b+c>2a (middle crossing in (4,5), extra reflection at x=4)")
    check(direct_in == 0, "grid 0..60: direct chord is never legal inside the region (direct abscissa < 3)")
    # sqrt2 family with the new mark
    fam = [t for t in range(0, 201) if region(1, t, f2(t))]
    bad = [t for t in fam if not shoot(stair_room(t, f2(t)), (1, 1), (6, 4 + t + f2(t)), (5, 5 + t + f2(t)))]
    check(not bad and fam == list(range(3, 201)),
          f"sqrt2 family: region holds exactly for t=3..200 (t=0,1,2 have c<=b), ray (6,D) legal for all")
    # radius
    def rad(a, b, c): return min((b + c - 2 * a) / 4, (c - b) / 2, (2 * a + 2 * b - c) / 5)
    z = (F(1, 37), F(15, 37), F(21, 37))
    check(rad(*z) == F(11, 185), f"radius at (1,15,21)/37 = {rad(*z)}")
    # sup-norm ball: random rational points with |dv| < r keep all signs; and r is sharp in the ambient cube
    rnd = random.Random(215); ok = True
    for _ in range(20000):
        r = rad(*z)
        d = [F(rnd.randint(-10 ** 6 + 1, 10 ** 6 - 1), 10 ** 6) * r for _ in range(3)]
        ok &= region(*(zi + di for zi, di in zip(z, d)))
    edge = [z[0] - F(11, 185), z[1] - F(11, 185), z[2] + F(11, 185)]
    check(ok and (2 * edge[0] + 2 * edge[1] - edge[2]) == 0,
          "20000 random points of the open ambient sup ball keep all three signs; radius is attained at a corner (ambient-sharp)")
    # sqrt2 face center, exact in Q(sqrt2): numbers (p, q) = p + q sqrt2
    def sgn(p, q):   # sign of p + q sqrt2, exact
        if p >= 0 and q >= 0: return (p > 0 or q > 0)
        if p <= 0 and q <= 0: return -1 if (p < 0 or q < 0) else 0
        return 1 if (p * p - 2 * q * q) * (1 if p > 0 else -1) > 0 else -1
    # tests times (1+sqrt2): L1 = 1+sqrt2, L2 = sqrt2-1, L3 = 2-sqrt2; radius*(1+sqrt2): (1+s)/4, (s-1)/2, (2-s)/5
    r1, r2, r3 = (F(1, 4), F(1, 4)), (F(-1, 2), F(1, 2)), (F(2, 5), F(-1, 5))
    less = lambda u, v: sgn(v[0] - u[0], v[1] - u[1]) == 1
    check(less(r3, r2) and less(r3, r1) and sgn(*r3) == 1,
          "sqrt2 face (0,1,sqrt2)/(1+sqrt2): min is (2-sqrt2)/(5(1+sqrt2)) exactly (sign tests in Q(sqrt2))")
    say(f"    numeric: {(2 - 2 ** .5) / (5 * (1 + 2 ** .5)):.6f} vs {(2 ** .5 - 1) / (2 * (1 + 2 ** .5)):.6f}, {0.25:.6f}")
    # x^1.5 construction: k = 0,4 mod 6 in (2/alpha, 3/alpha)
    bad = []; used = 0; first = None
    for x in range(1, 201):
        y = f15(x); D = 4 + x + y
        alpha = F(x + 2, D)
        if not alpha < F(1, 4): continue
        first = first or x
        ks = [k for k in range(floor(2 / alpha) + 1, int(3 / alpha) + 1) if k % 6 in (0, 4) and 2 < k * alpha < 3]
        used += 1
        if not ks or not shoot(stair_room(x, y), (1, 1), (ks[0], D), (5, 5 + x + y)): bad.append(x)
    check(not bad, f"y=floor(x^1.5): alpha<1/4 from x={first}; for all {used} such x<=200 a k=0,4 mod 6 exists and the ray is legal")
    bad = []; n = 0
    for x in range(1, 61):
        for y in range(3 * x + 5, 3 * x + 60):
            D = 4 + x + y; alpha = F(x + 2, D)
            ks = [k for k in range(floor(2 / alpha) + 1, int(3 / alpha) + 1) if k % 6 in (0, 4) and 2 < k * alpha < 3]
            n += 1
            if not ks or not all(shoot(stair_room(x, y), (1, 1), (k, D), (5, 5 + x + y)) for k in ks): bad.append((x, y))
    check(not bad, f"grid x=1..60, y=3x+5..3x+59 ({n} rooms, alpha<1/4): every k=0,4 mod 6 in (2/alpha,3/alpha) legal")


# ------------------------------------------------------------------ claim 4
def claim4():
    say("\n=== Claim 4: effective radius rho = min(1, min p(z)/(2 max(1,B(p))))")
    rnd = random.Random(4)
    ok_grad = ok_half = True
    for trial in range(300):
        n = rnd.randint(1, 4)
        mons = {}
        for _ in range(rnd.randint(1, 6)):
            m = tuple(rnd.randint(0, 3) for _ in range(n))
            mons[m] = F(rnd.randint(-9, 9), rnd.randint(1, 4))
        B = sum(abs(cf) * sum(m) for m, cf in mons.items())
        ev = lambda v: sum(cf * eval_m(m, v) for m, cf in mons.items())
        for _ in range(5):
            v = [F(rnd.randint(-1000, 1000), 1000) for _ in range(n)]   # whole cube [-1,1]^n
            g = sum(abs(sum(cf * m[i] * eval_m(tuple(mj - (j == i) for j, mj in enumerate(m)), v)
                            for m, cf in mons.items() if m[i] > 0)) for i in range(n))
            ok_grad &= g <= B
        z = [F(rnd.randint(0, 1000), 1000) for _ in range(n)]
        pz = ev(z)
        if pz <= 0: continue
        rho = min(F(1), pz / (2 * max(F(1), B)))
        for _ in range(10):
            v = [min(F(1), max(F(0), zi + F(rnd.randint(-999, 999), 1000) * rho)) for zi in z]
            ok_half &= ev(v) >= pz / 2
    check(ok_grad, "sum_i |d_i p| <= B(p) at 1500 random points of [-1,1]^n (300 random polynomials)")
    check(ok_half, "p(v) >= p(z)/2 for sampled v in the sup ball of radius rho intersected with [0,1]^n")
    # sharpness example: p = v at z=0 face is excluded; p = 1 - 2v: B=2
    check(min(F(1), F(1) / (2 * 2)) == F(1, 4), "p=1-2v at z=0: rho=1/4, p >= 1/2 there (tight half slack)")
    # consistency with claim 6: linear tests give half the claim-6 radius
    z = (F(1, 37), F(15, 37), F(21, 37))
    tests = [((-2, 1, 1)), ((0, -1, 1)), ((2, 2, -1))]
    rho = min(F(1), min(sum(ci * zi for ci, zi in zip(t, z)) / (2 * max(1, sum(map(abs, t)))) for t in tests))
    check(rho == F(11, 370), f"claim-4 formula on the claim-6 tests at (1,15,21)/37 gives {rho} = (11/185)/2")


def eval_m(m, v):
    out = F(1)
    for e, x in zip(m, v):
        out *= x ** e
    return out


if __name__ == '__main__':
    claim5()
    claim6()
    claim4()
    say(f"\nTOTAL FAIL {len(FAILS)}; cpu {time.process_time()-T0:.1f}s")
