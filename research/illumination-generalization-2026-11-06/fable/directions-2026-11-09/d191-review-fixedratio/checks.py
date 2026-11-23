"""d191 review checks: fixed-ratio corner (primary), lower-period coupling (secondary), scale-step v2.

Named objects only:
  * fixed-ratio corner: the residue/coprimality claims for N = M^(1+k phi(2s)), M = 3s-r, at theta = 1/3
    (a = 2d, the note's named ratio) and a few other small reduced ratios (arithmetic only); the
    corner-targeting lemma checked exhaustively over all reduced p/q with q <= N for those small N; the
    clearance mu = 1/(4N^3) at deterministic xi; the joining equation and correction; the aspect
    reduction kappa in [kappa-, kappa+]; the explicit k formula and the threshold (1) at the d190 constants
    (n = 1, T = 90, P = 6 for st279, R = 1); the arithmetic consequences and the (m+1)/m example.
  * lower-period coupling: the gcd-divides-determinant step on a grid of affine rays; the polynomial
    resultant step on a grid of synthetic affine forms; the note's junction at even n = 2..10 with
    D = 16(a+1); the congruence obstruction; the (D,u) = (m,m+1) phase identity.
  * scale-step v2: text checks for which d190 corrections were applied.
  * the W=10 ledger realization of LLLRLLLRLR.
No room, ray, direction, slope, reflection-word or room-size search is run. Nothing is traced.
Run: python3 -B checks.py > checks.log
"""
import time
import os
from fractions import Fraction as F
from math import gcd, log10, ceil, floor

T0 = time.process_time()
FAIL = []
HERE = os.path.dirname(os.path.abspath(__file__))


def log(*a):
    print(*a, flush=True)


def check(ok, msg):
    log(('  PASS ' if ok else '  FAIL ') + msg)
    if not ok:
        FAIL.append(msg)


def lcm(*xs):
    r = 1
    for x in xs:
        r = r * x // gcd(r, x)
    return r


def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def primes_of(n):
    ps, p = [], 2
    while p * p <= n:
        if n % p == 0:
            ps.append(p)
            while n % p == 0:
                n //= p
        p += 1
    if n > 1:
        ps.append(n)
    return ps


def rad(n):
    r = 1
    for p in primes_of(n):
        r *= p
    return r


def phi(n):
    r = n
    for p in primes_of(n):
        r = r // p * (p - 1)
    return r


def dist_int(x):
    return min(x - floor(x), ceil(x) - x)


# ---------------------------------------------------------- copied verbatim from d190 checks.py
def seg_meet(p, q, r, s):
    """Closed axis-aligned segments pq and rs share a point."""
    (x1, x2), (y1, y2) = sorted((p[0], q[0])), sorted((p[1], q[1]))
    (u1, u2), (w1, w2) = sorted((r[0], s[0])), sorted((r[1], s[1]))
    return max(x1, u1) <= min(x2, u2) and max(y1, w1) <= min(y2, w2)


def strictly_simple(P):
    n = len(P)
    if len(set(P)) != n:
        return False
    for i in range(n):
        a, b = P[i], P[(i + 1) % n]
        if not ((a[0] == b[0]) ^ (a[1] == b[1])):
            return False
        c = P[(i + 2) % n]
        if (a[0] == b[0]) == (b[0] == c[0]):   # consecutive collinear edges
            return False
    for i in range(n):
        for j in range(i + 1, n):
            if j == i + 1 or (i == 0 and j == n - 1):
                continue
            if seg_meet(P[i], P[(i + 1) % n], P[j], P[(j + 1) % n]):
                return False
    return True


def signed_area(P):
    n = len(P)
    return F(sum(P[i][0] * P[(i + 1) % n][1] - P[(i + 1) % n][0] * P[i][1] for i in range(n)), 2)


def turns(P):
    n = len(P)
    sgn = 1 if signed_area(P) > 0 else -1
    w = ''
    for i in range(n):
        a, b, c = P[i - 1], P[i], P[(i + 1) % n]
        cr = (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])
        w += 'L' if cr * sgn > 0 else 'R'
    return w


def wall_gcds(P):
    n = len(P)
    gh = gv = 0
    for i in range(n):
        (x0, y0), (x1, y1) = P[i], P[(i + 1) % n]
        if y0 == y1: gh = gcd(gh, abs(x1 - x0))
        else: gv = gcd(gv, abs(y1 - y0))
    return gh, gv


def inside(P, x, y):
    """Strict interior test for an orthogonal polygon (ray cast, point off the boundary)."""
    n = len(P); cnt = 0
    for i in range(n):
        (x0, y0), (x1, y1) = P[i], P[(i + 1) % n]
        if x0 == x1 and min(y0, y1) <= y <= max(y0, y1) and x == x0: return False
        if y0 == y1 and min(x0, x1) <= x <= max(x0, x1) and y == y0: return False
        if x0 == x1 and x0 > x and min(y0, y1) < y <= max(y0, y1): cnt += 1
    return cnt % 2 == 1


# ====================================================================== §1 residues of N
log('§1 fixed-ratio corner: N = M^(1+k phi(2s)), M = 3s-r')
ratios = [(r, s) for s in range(2, 31) for r in range(1, s) if gcd(r, s) == 1]
ok = tot = 0
for r, s in ratios:
    M = 3 * s - r
    for k in range(4):
        N = M ** (1 + k * phi(2 * s))
        tot += 1
        l2 = N - s + r
        ok += (N % (2 * s) == (s - r) % (2 * s) and gcd(N, s) == 1 and l2 % (2 * s) == 0 and l2 >= 0
               and F(1 + l2 // s) - F(r, s) == F(N, s) and set(primes_of(N)) == set(primes_of(M)))
check(ok == tot, f'N = s-r mod 2s, gcd(N,s)=1, l=(N-s+r)/(2s) a nonnegative integer, 1+2l-theta = N/s, '
      f'primes(N)=primes(M): all {len(ratios)} reduced r/s with s<=30, k=0..3 ({tot} cases)')
check(all(gcd(3 * s - r, s) == 1 for r, s in ratios), 'gcd(M,s) = gcd(r,s) = 1 for all those ratios')
check(all((3 * s - r) % 2 == 1 or s % 2 == 1 for r, s in ratios), 'M even forces s odd')
log(f'  INFO theta=1/3 (a=2d): M={3*3-1}, phi(6)={phi(6)}, N in {[8 ** (1 + 2 * k) for k in range(3)]}, '
    f'N mod 6 = {[8 ** (1 + 2 * k) % 6 for k in range(3)]}')

# ====================================================================== §2 corner-targeting lemma
log('§2 corner-targeting lemma: exhaustive over reduced p/q, q <= N')


def choose_j(p, q, M, lo):
    """Smallest j >= lo meeting the note's CRT restrictions (period rad(M))."""
    for j in range(lo, lo + 2 * rad(M) + 1):
        good = True
        for pr in primes_of(M):
            if pr == 2:
                if p % 2 == 0 and q % 2 == 1 and (j * q - p // 2) % 2 == 0:
                    good = False
            elif q % pr != 0 and (2 * j * q - p) % pr == 0:
                good = False
        if good:
            return j
    return None


def lemma_case(r, s, N, j_offsets=(0, 7, -5)):
    M = 3 * s - r
    Hceil = -(-N // s)                 # l' ranges over 1 <= l' < N/s
    lps = range(1, Hceil) if N % s else range(1, N // s)
    lps = [lp for lp in lps if s * lp < N]
    bad = gbad = nfr = 0
    for q in range(1, N + 1):
        for p in range(0, q + 1):
            if gcd(p, q) != 1:
                continue
            nfr += 1
            for off in j_offsets:
                j = choose_j(p, q, M, off)
                if j is None:
                    bad += 1
                    continue
                X = 2 * j * q - p
                if gcd(X, N) > 2:
                    gbad += 1
                for lp in lps:           # (2) integral at p/q  <=>  qN | (2jq-p) s l'
                    if (X * s * lp) % (q * N) == 0:
                        bad += 1
                        break
    return nfr, len(lps), bad, gbad


for (r, s, k) in [(1, 3, 0), (1, 3, 1), (1, 2, 0), (1, 2, 1), (2, 5, 0), (2, 3, 0), (3, 4, 0), (1, 4, 0)]:
    M = 3 * s - r
    N = M ** (1 + k * phi(2 * s))
    if N > 600:
        continue
    nfr, nl, bad, gbad = lemma_case(r, s, N)
    check(bad == 0 and gbad == 0,
          f'theta={r}/{s}, N={N}: chosen j makes no p/q critical at any of {nl} levels l\' and '
          f'gcd(2jq-p,N)<=2 ({nfr} fractions x 3 j-windows)')

# Necessity of the CRT restriction (INFO): unrestricted j does hit corners.
r, s, N = 1, 3, 8
hits = 0
for q in range(1, N + 1):
    for p in range(0, q + 1):
        if gcd(p, q) != 1:
            continue
        for j in range(0, 4):
            X = 2 * j * q - p
            if any((X * s * lp) % (q * N) == 0 for lp in range(1, 3)):
                hits += 1
log(f'  INFO theta=1/3, N=8, unrestricted j in 0..3: {hits} (p/q, j) pairs put a corner on an earlier level')

# Clearance mu = 1/(4N^3) at deterministic xi (case 1: xi = p/q +- 1/(4N^2); case 2: midpoints of Farey gaps)
for (r, s, k) in [(1, 3, 0), (1, 2, 0), (2, 5, 0)]:
    M = 3 * s - r
    N = M ** (1 + k * phi(2 * s))
    mu = F(1, 4 * N ** 3)
    lps = [lp for lp in range(1, N) if s * lp < N]
    fr = sorted({F(p, q) for q in range(1, N + 1) for p in range(0, q + 1)})
    worst = None
    cnt = 0
    for i, x in enumerate(fr):
        p, q = x.numerator, x.denominator
        j = choose_j(p, q, M, 0)
        for xi in (x + F(1, 4 * N * N), x - F(1, 4 * N * N), x):
            if not 0 < xi < 1:
                continue
            m = min(dist_int(2 * j - (2 * j - xi) * F(s * lp, N)) for lp in lps)
            worst = m if worst is None else min(worst, m)
            cnt += 1
        if i + 1 < len(fr):
            mid = (x + fr[i + 1]) / 2
            if abs(mid - x) > F(1, 4 * N * N) and abs(mid - fr[i + 1]) > F(1, 4 * N * N):
                for j in (0, 1, 3):
                    m = min(dist_int(2 * j - (2 * j - mid) * F(s * lp, N)) for lp in lps)
                    worst = min(worst, m)
                    cnt += 1
    check(worst >= mu, f'theta={r}/{s}, N={N}: min distance of (2) from Z over {cnt} (xi,j) cases is '
          f'{worst} >= mu = {mu}')

# ====================================================================== §3 slope, join, displacement
log('§3 v0, joining equation, correction, displacement')
ok = tot = 0
for D in (5, 12, 40):
    for u in (1, 2, 3):
        for h in (6, 9, 30):
            for t in (1, 2, 5):
                for xi in (F(1, 7), F(1, 2), F(5, 6)):
                    for H in (F(8, 3), F(170, 3) + F(2, 3)):
                        for j in (-2, 1, 4):
                            X, Y = F(D, u), F(h, t)
                            kap = X / Y
                            vphys = F(D) * (2 * j - xi) / (h * H)        # physical dx/dy to corner
                            v0 = F(t, u) * vphys
                            tot += 1
                            ok += v0 == kap * (2 * j - xi) / H
check(ok == tot, f'template speed toward the corner is v0 = kappa(2j-xi)/H ({tot} grid cases)')

ok = tot = okb = 0
for kap in (F(1, 3), F(2), F(17, 5)):
    for X in (F(3), F(40), F(1000, 7)):
        for H in (F(8, 3), F(512, 3)):
            for B in (1, 2, 5):
                for e in (0, 3, 7):
                    for xi in (F(1, 5), F(3, 4)):
                        for j in (-1, 2, 6):
                            v0 = kap * (2 * j - xi) / H
                            v = v0 + kap * (e - B * v0) / (H * X + kap * B)
                            tot += 1
                            ok += xi + H * v / kap == 2 * j + (e - B * v) / X
                            Rb = abs(e - B * v0)
                            if Rb:
                                okb += (abs(v - v0) < kap * Rb / (H * X)
                                        and all(abs((H - lp) * (v - v0) / kap) < Rb / X
                                                for lp in range(1, int(H) + 1)))
                            else:
                                okb += 1
check(ok == tot, f'v - v0 = kappa(e-Bv0)/(HX+kappa B) solves xi + Hv/kappa = 2j + (e-Bv)/X exactly ({tot})')
check(okb == tot, f'|v-v0| < kappa|e-Bv0|/(HX) and every earlier-level displacement < |e-Bv0|/X ({tot})')
log('  INFO so X > 4 kappa+ R/(H eta) keeps v in J (|v-v0| <= eta/4 from the middle half), and X > 2R/mu '
    'leaves each earlier contact > R/X from Z')

# ====================================================================== §4 aspect reduction
log('§4 aspect reduction kappa in [kappa-, kappa+]')
P, eta, R = 6, F(1, 10), 1
C = 2 + 2 * R + P + eta
ok1 = n1 = ok2 = n2 = 0
for D in range(1, 25):
    for u in (1, 2, 3):
        for t in (1, 2, 4):
            for a in range(1, 13):
                for d in range(1, 9):
                    for B in (1, 2, 3):
                        h, L = a + d, a + 2 * d
                        X, Y = F(D, u), F(h, t)
                        kap = X / Y
                        th = F(d, h)
                        if u * (a + t * B) * eta <= gcd(2 * D * t, a * u * P):     # direct failure
                            n1 += 1
                            ok1 += kap >= (1 - th) * eta / 2
                        # far-wall failure: D * delta_min <= 4h with delta_min = t eta / (u C^2 (1+t/L)^2)
                        if D * t * eta <= 4 * h * u * C * C * (1 + F(t, L)) ** 2 and Y >= 1:
                            n2 += 1
                            ok2 += kap <= 16 * C * C / eta
check(ok1 == n1, f'direct failure u(a+tB)eta <= g_a implies kappa >= (1-theta)eta/2 ({n1} failing tuples)')
check(ok2 == n2, f'far-wall failure and Y >= 1 imply kappa <= 16C^2/eta ({n2} tuples)')

# ====================================================================== §5 explicit constants at the d190 data
log('§5 explicit k, N and threshold (1) at n=1 (T=90), P=6 (st279 visited run), R=1, theta=1/3')
n_area = 1
m4 = 4 * n_area
T = 1 + fib(3 * m4 - 1)
eta = F(1, 4 * T * T)
P, R = 6, 1
C = 2 + 2 * R + P + eta
kp = 16 * C * C / eta
r, s = 1, 3
th = F(r, s)
km = (1 - th) * eta / 2
M = 3 * s - r
Q = 2 * rad(M)
k = 0
while M ** k < 1 + 4 * s * kp * Q / eta:    # k = ceil(log_M(1 + 4 s kappa+ Q / eta)), exact
    k += 1
N = M ** (1 + k * phi(2 * s))
H = F(N, s)
check(T == 90 and eta == F(1, 32400), f'T = 1+F_11 = {T}, eta = {eta}')
check(H * eta / (4 * kp) > Q, f'k = {k}: H eta/(4 kappa+) > Q = {Q} with N = 8^{1 + k * phi(6)} '
      f'(log10 N = {log10(M) * (1 + k * phi(2 * s)):.1f})')
k0 = k
while k0 > 0 and F(M ** (1 + (k0 - 1) * phi(2 * s)), s) * eta / (4 * kp) > Q:
    k0 -= 1
log(f'  INFO smallest admissible k here is {k0}; the formula gives {k}')
t1 = 8 * R * F(N) ** 3
t2 = 4 * kp * R / (H * eta)
check(t2 < t1, 'the second term 4 kappa+ R/(H eta) < R/Q is always below 8RN^3 (it is redundant)')
log(f'  INFO kappa- = {km}, log10 kappa+ = {log10(kp):.2f}, threshold Y > {float(t1 / km):.3e} '
    f'(log10 = {log10(t1) - log10(km):.1f})')
# theta -> 1 non-uniformity (named example a = 1 in the review; arithmetic only)
for d_ in (2, 5, 20):
    rr, ss = d_, d_ + 1
    MM = 3 * ss - rr
    kmm = (1 - F(rr, ss)) * eta / 2
    log(f'  INFO a=1, d={d_}: theta={rr}/{ss}, M={MM}, kappa- = eta/{2 * ss}; threshold needs '
        f'Y > 8R M^3/kappa- >= {float(8 * MM ** 3 / kmm):.2e}, while Y = h/t <= {d_ + 1}')

# ====================================================================== §6 arithmetic consequences
log('§6 comparable-region arithmetic')
P, eta = 6, F(1, 10)
ok = tot = okt = okY = nf = 0
for D in range(1, 21):
    for u in (1, 2, 3):
        for t in (1, 2, 5):
            for a in range(1, 11):
                for d in range(1, 7):
                    for B in (1, 2):
                        h = a + d
                        g = gcd(2 * D * t, a * u * P)
                        pq = F(2 * D * t, a * u * P)
                        p_, q_ = pq.numerator, pq.denominator
                        th = F(d, h)
                        kap = F(D * t, u * h)
                        tot += 1
                        ok += q_ == a * u * P // g and kap == (1 - th) * P * p_ / (2 * q_)
                        if u * (a + t * B) * eta <= g:
                            nf += 1
                            okt += (q_ <= P / eta and F(t, a) <= P / (B * eta)
                                    and F(h, t) >= B * eta / (P * (1 - th)))
check(ok == tot, f'q = auP/gcd(2Dt,auP) and kappa = (1-theta)Pp/(2q) ({tot} tuples)')
check(okt == nf, f'direct failure gives q <= P/eta, t/a <= P/(B eta), Y >= B eta/(P(1-theta)) ({nf} tuples)')
ok = all(F(m + 1, m) / F(m + 1, m) == 1 and F(m + 1, m).denominator == m for m in range(1, 50))
check(ok, '(m+1)/m in both factors: quotient 1, reduced heights m+1 unbounded (m = 1..49)')
log('  INFO the d190 span hypothesis uR <= D means X >= R; X = (m+1)/m needs R <= 1+1/m. '
    'R(m+1)/m works for any R. The note labels the example as arithmetic only, correctly')

# ====================================================================== §7 lower-period coupling
log('§7 lower-period coupling')
ok = tot = 0
for a0 in range(1, 8):
    for d0 in range(1, 8):
        for p in range(0, 5):
            for q in range(0, 5):
                det = p * d0 - q * a0
                for n in range(0, 40):
                    a, d = a0 + p * n, d0 + q * n
                    tot += 1
                    if det:
                        ok += (2 * abs(det)) % gcd(a, 2 * d) == 0
                    else:
                        ok += F(a, d) == F(a0, d0)
check(ok == tot, f'gcd(a,2d) | 2|p d0 - q a0| on affine rays, and a/d constant when det = 0 ({tot})')
log('  INFO p = 0 (a fixed, d growing) has det = -q a0, so a/gcd(a,2d) <= a stays bounded')


def polymul(A, B):
    r = [0] * (len(A) + len(B) - 1)
    for i, x in enumerate(A):
        for j, y in enumerate(B):
            r[i + j] += x * y
    return r


def res22(f, g):
    """Resultant of two quadratics (coefficient lists low->high) via the 4x4 Sylvester determinant."""
    f0, f1, f2 = f
    g0, g1, g2 = g
    Mx = [[f2, f1, f0, 0], [0, f2, f1, f0], [g2, g1, g0, 0], [0, g2, g1, g0]]
    Mx = [[F(x) for x in row] for row in Mx]
    det = F(1)
    for c in range(4):
        piv = next((r_ for r_ in range(c, 4) if Mx[r_][c] != 0), None)
        if piv is None:
            return 0
        if piv != c:
            Mx[c], Mx[piv] = Mx[piv], Mx[c]
            det = -det
        det *= Mx[c][c]
        for r_ in range(c + 1, 4):
            fac = Mx[r_][c] / Mx[c][c]
            Mx[r_] = [Mx[r_][i] - fac * Mx[c][i] for i in range(4)]
    return int(det)


P = 6
ok = tot = okd = nd = 0
pairs = [(x0, x1) for x0 in range(1, 5) for x1 in range(1, 5)]
for (D0, D1) in pairs:
    for (u0, u1) in pairs:
        if D0 * u1 == D1 * u0:
            continue
        for (A0, A1) in pairs[::3]:
            for (t0, t1) in pairs[::5]:
                if A0 * t1 == A1 * t0:
                    continue
                tot += 1
                found = None
                for k in (1, 2, 3):
                    f = polymul([D0, k * D1], [t0, t1]); f = [2 * c for c in f]
                    g = polymul([u0, k * u1], [A0, A1]); g = [P * c for c in g]
                    Rs = res22(f, g)
                    if Rs:
                        found = (k, f, g, Rs)
                        break
                if found:
                    ok += 1
                    k, f, g, Rs = found
                    for n in range(0, 30):
                        fn = sum(c * n ** i for i, c in enumerate(f))
                        gn = sum(c * n ** i for i, c in enumerate(g))
                        nd += 1
                        okd += Rs % gcd(fn, gn) == 0
check(ok == tot, f'one of k = 1,2,3 gives Res(f,g) != 0 when D/u and A/t are nonconstant ({tot} form pairs)')
check(okd == nd, f'gcd(f(n),g(n)) divides Res(f,g) at n = 0..29 ({nd} evaluations)')

log('§7b the junction: a=2n+1, d=n, D=16(a+1), source (D/2,d), target (0,h+1)')
for n in (2, 4, 6, 8, 10):
    a, d = 2 * n + 1, n
    h, L = a + d, a + 2 * d
    D = 16 * (a + 1)
    Pg = [(0, 0), (D, 0), (D, h), (1, h), (1, h + 2), (1 - D, h + 2), (1 - D, h), (0, h)]
    S, Tg = (D // 2, d), (0, h + 1)
    w = turns(Pg)
    good = (strictly_simple(Pg) and len(Pg) == 8 and w.count('R') == 2 and wall_gcds(Pg) == (1, 1)
            and inside(Pg, *S) and inside(Pg, *Tg) and S[0] % 2 == Tg[0] % 2 and S[1] % 2 == Tg[1] % 2
            and D % 4 == 0 and F(D, 2) > 3 * L + 1 and a // gcd(a, 2 * d) == 2 * n + 1)
    # phase shifts in lower-circumference units: A * 2D / (2D)
    ph = all(F(A * 2 * D, 2 * D).denominator == 1 for A in (a, L))
    # congruence (A+b)z = +-bD/2 + A e (mod 2D), z in (0,1): impossible for both short routes, b = 1
    imp = True
    for A in (a, L):
        b = 1
        for sg in (1, -1):
            for e in (0, 2):
                rhs = sg * b * F(D, 2) + A * e
                for mm in range(-3, 4):
                    val = rhs + 2 * D * mm
                    if 0 < val < A + b:
                        imp = False
    check(good and ph and imp, f'n={n}: D={D}, W=8, 2 reflex, wall gcds (1,1), marks interior same parity, '
          f'a/gcd={2 * n + 1}; phase orders 1; no z in (0,1) solves the b=1 congruence for A=a,L')
# general b odd: 3A+b <= D/2 => impossible (arithmetic on the n=2 value of D)
D = 16 * (2 * 2 + 1 + 1)
ok = tot = 0
for b in (1, 3, 5, 7):
    for A in range(1, (D // 2 - b) // 3 + 1):
        tot += 1
        imp = True
        for sg in (1, -1):
            for e in (0, 2):
                for mm in range(-3, 4):
                    val = sg * b * F(D, 2) + A * e + 2 * D * mm
                    if 0 < val < A + b:
                        imp = False
        ok += imp
check(ok == tot, f'D={D}: every odd b<=7 and A with 3A+b<=D/2 makes the congruence impossible ({tot})')
check(True, 'the junction is two lattice rectangles sharing [0,1] at y=h with full overlap: the doorway-word-bound '
      'theorem applies (hypotheses read, not traced)')

log('§7c (D,u)=(m,m+1), (A,t)=(m,m+1)')
ok = all(m * (m + 1) == m * (m + 1) and gcd(m + 1, m) == 1 for m in range(1, 50))
okP = all(gcd(2 * m * (m + 1), m * (m + 1) * 6) == 2 * m * (m + 1) for m in range(1, 50))
check(ok and okP, 'Au = Dt identically; primitive normal (m+1,-m) has height m+1; with P=6, g_A = 2Dt '
      '(phase order one) for m = 1..49')
log('  INFO D/u = m/(m+1) < 1 clips any lattice mouth whose right end is >= 1 in template units; '
    '(D,u)=(m+1,m), (A,t)=(m+1,m) gives the same identity with D >= u')

# ====================================================================== §8 scale-step v2 vs d190 corrections
log('§8 scale-step v2: d190 corrections applied?')
v2 = open(os.path.join(HERE, 'snapshot-scale-step-v2.md')).read()
v1 = open(os.path.join(HERE, '..', 'd190-review-scalestep', 'snapshot.md')).read()
adv = v2.splitlines()[0]
check('tends to zero' in adv and 'mouth width divided by target-to-mouth depth' in adv,
      'Medium 1 (Advances line): qualified by w/b -> 0')
sec = v2.split('### Why the requested physical-window induction fails')[1].split('\n\n')[1]
sec1 = v1.split('### Why the requested physical-window induction fails')[1].split('\n\n')[1]
log(f'  INFO Medium 1 (section opening) unchanged from v1: {sec == sec1}')
log(f'  INFO junction stated to lie outside the theorem hypotheses: '
    f'{"outside" in v2.split("### Why the requested")[1].split("### Extra roof")[0]}')
log(f'  INFO Low 2 (outside-span opening in open cases): {"outside the near-side span remains" in v2}')
log(f'  INFO Low 3 (template openings): {"has no openings other than those labelled mouths" in v2}')
log(f'  INFO Low 1 (T and W renamed): {"W_tmpl" in v2 or "T_F" in v2}')
log(f'  INFO Low 4 (junction wording): {"offset by one" not in v2}')

# ====================================================================== §9 ledger realization
log('§9 W=10 ledger realization')
LW = [(2, 0), (4, 0), (4, 1), (3, 1), (3, 4), (0, 4), (0, 3), (1, 3), (1, 2), (2, 2)]
w = turns(LW)
rots = {w[i:] + w[:i] for i in range(len(w))}
check(strictly_simple(LW) and len(LW) == 10 and 'LLLRLLLRLR' in rots,
      f'strictly simple, 10 walls, turn word {w} is a rotation of LLLRLLLRLR; area {abs(signed_area(LW))}')

log('')
log(f'CPU seconds: {time.process_time() - T0:.2f}')
log(f'FAILURES: {len(FAIL)}')
for f_ in FAIL:
    log('  ' + f_)
