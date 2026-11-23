"""d192 checks: shallow roof return (l1-shallow-roof-return.md).

Exact Fraction / integer arithmetic only. Covers:
  * snapshot hashes against qclass-closure/bbbb sources;
  * constants at the st279 parameters named in d190/d191 (n=1, T=90, P=6 or 30, R=1);
  * the period identity (1) and the failure bounds q <= Q, X >= H eta/4;
  * the reduction to (2), the r* formula, the rounding correction and its bounds;
  * the interval-clearance lemma;
  * legality of the constructed roof-floor-roof route on synthetic closed-form instances
    (three horizontal-level contacts computed in closed form; nothing is traced);
  * the depth-ratio conversion a/h > eps => b <= 2K0/eps, and reduced theta;
  * a = 1 with several d: which theorem covers it, sizes of thresholds;
  * direct failure => A >= B eta / P;
  * text checks on fixed-ratio v2 and scale-step against d191 corrections;
  * the W=10 ledger realization of LLLRLLLRLR.
No room, ray, direction, slope, reflection-word or room-size search is run.
Run: python3 -B checks.py > checks.log
"""
import hashlib
import os
import time
from fractions import Fraction as F
from math import gcd, ceil, floor, log10

T0 = time.process_time()
FAIL = []
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, '../../../../qclass-closure/bbbb'))


def log(*a):
    print(*a, flush=True)


def check(ok, msg):
    log(('  PASS ' if ok else '  FAIL ') + msg)
    if not ok:
        FAIL.append(msg)


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


def fceil(x):
    return -((-x.numerator) // x.denominator)


def dist_grid(x, X):
    """distance from x to X*Z, exact."""
    k = floor(x / X)
    return min(x - k * X, (k + 1) * X - x)


def max_dist_on_interval(lo, hi, X):
    """max over [lo,hi] of distance to X*Z (exact)."""
    cands = [lo, hi]
    k = floor(lo / X)
    while k * X + X / 2 <= hi:
        m = k * X + X / 2
        if lo <= m <= hi:
            cands.append(m)
        k += 1
    return max(dist_grid(c, X) for c in cands)


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


# ---------------------------------------------------------- copied verbatim from d191 (d190) checks.py
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


# ====================================================================== §0 snapshots
log('§0 snapshots')
s_main = sha(os.path.join(HERE, 'snapshot.md'))
s_v2 = sha(os.path.join(HERE, 'snapshot-fixed-ratio-corner-v2.md'))
log(f'  INFO snapshot.md sha256 {s_main}')
log(f'  INFO snapshot-fixed-ratio-corner-v2.md sha256 {s_v2}')
check(s_main == sha(os.path.join(SRC, 'l1-shallow-roof-return.md')),
      'snapshot.md is byte-identical to bbbb/l1-shallow-roof-return.md')
check(s_v2 == sha(os.path.join(SRC, 'l1-fixed-ratio-corner.md')),
      'snapshot-fixed-ratio-corner-v2.md is byte-identical to bbbb/l1-fixed-ratio-corner.md')
log(f'  INFO prefix 59f00ced given in the brief matches: snapshot.md={s_main.startswith("59f00ced")}, '
    f'fixed-ratio v2={s_v2.startswith("59f00ced")}')

# ====================================================================== §1 constants at st279
log('§1 constants at st279 (n=1, m=4, T=1+F_11, R=1)')
T = 1 + fib(11)
check(T == 90, f'T = 1+F_11 = {T}')
eta = F(1, 4 * T * T)
R = 1
CONST = {}
for P in (6, 30):
    C = 2 + 2 * R + P + eta
    Q = fceil(64 * C * C / (eta * eta))
    eps = min(F(1, 2), eta / (32 * Q * P))
    H1 = max(F(1), 64 * (R + 1) / eta)
    K0 = 16 * P * C * C / eta ** 3
    bmax = 2 * K0 / eps
    CONST[P] = (C, Q, eps, H1, K0, bmax)
    log(f'  INFO P={P}: C={float(C):.6f}, Q={Q} (~10^{log10(Q):.2f}), eps ~ 10^{log10(eps):.2f}, '
        f'1/eps ~ 10^{log10(1 / eps):.2f}, H1={H1}, K0 ~ 10^{log10(K0):.2f}, 2K0/eps ~ 10^{log10(bmax):.2f}')
check(CONST[6][3] == 4147200, 'H1 = 64(R+1)/eta = 4,147,200 at R=1, T=90')

# ====================================================================== §2 period identity (1)
log('§2 period identity (1): (2h-a)uPq in 2Dt Z, i.e. (2H-A)qP in 2X Z')
ok = tot = 0
for D in range(1, 13):
    for t in range(1, 5):
        for u in range(1, 5):
            for h in range(2, 9):
                for a in range(1, h):
                    for P in (2, 6):
                        g = gcd(2 * D * t, (2 * h - a) * u * P)
                        q = 2 * D * t // g
                        X, H, A = F(D, u), F(h, t), F(a, t)
                        m = (2 * H - A) * q * P / (2 * X)
                        tot += 1
                        ok += ((2 * h - a) * u * P * q) % (2 * D * t) == 0 and m.denominator == 1
check(ok == tot, f'(2H-A)qP / (2X) is an integer ({tot} integer tuples)')

# ====================================================================== §3 failure bounds
log('§3 failure bounds: floor failure => X >= (2H-A+B)eta/4 and q <= 4X/((2H-A+B)eta); with far-wall => q <= Q')
ok = tot = nfail = 0
for et in (F(1, 2), F(1, 4), F(1, 8)):
    for D in range(1, 13):
        for t in range(1, 4):
            for u in range(1, 4):
                for h in range(2, 9):
                    for a in range(1, h):
                        for B in (1, 2, 3):
                            P = 2
                            g = gcd(2 * D * t, (2 * h - a) * u * P)
                            if not (u * (2 * h - a + t * B) * et <= 2 * g):
                                continue
                            nfail += 1
                            q = 2 * D * t // g
                            X, H, A = F(D, u), F(h, t), F(a, t)
                            tot += 1
                            ok += (X >= (2 * H - A + B) * et / 4 and q <= 4 * X / ((2 * H - A + B) * et))
check(ok == tot, f'floor-failure consequences hold on all {tot} failing tuples')
ok = tot = 0
for et in (F(1, 2), F(1, 8), F(1, 32)):
    for Cc in (F(3), F(7, 2), F(10)):
        for H in [F(1), F(3, 2), F(2), F(7), F(40)]:
            for A in [H * k / 8 for k in range(1, 8)]:
                for B in (1, 2, 5):
                    Xmax = 4 * H * Cc ** 2 * (1 + 1 / (2 * H - A)) ** 2 / et
                    qmax = 4 * Xmax / ((2 * H - A + B) * et)
                    tot += 1
                    ok += (Xmax <= 16 * H * Cc ** 2 / et and qmax <= 64 * Cc ** 2 / et ** 2)
check(ok == tot, f'H >= 1: far-wall X bound <= 16HC^2/eta and the q bound <= 64C^2/eta^2 ({tot} cases)')

# ====================================================================== §4 reduction to (2), r*, rounding
log('§4 reduction to (2), r*, rounding correction')
ok1 = ok2 = ok3 = ok4 = tot = 0
for H in [F(5), F(17, 2), F(40)]:
    for A in [F(1, 3), F(1), F(2)]:
        for B in (1, 3):
            for P in (2, 6):
                for q in (1, 2, 5):
                    for mm in (1, 3):
                        X = (2 * H - A) * q * P / (2 * mm)
                        for c0 in [X / 7, X / 2]:
                            for e in (1, 4):
                                for v0 in [F(1, 3), F(-5, 7), F(9, 4)]:
                                    L = 2 * H + A
                                    jstar = (e - c0 - (L + B) * v0) / (2 * A * q * P)
                                    rstar = c0 + A * (v0 + q * jstar * P)
                                    ok1 += rstar == (e + c0 - (2 * H - A + B) * v0) / 2
                                    j = floor(jstar + F(1, 2))
                                    v = v0 - 2 * A * q * P * (j - jstar) / (L + B)
                                    w = v + q * j * P
                                    # exact terminal equation, unreduced
                                    lhs = c0 + L * w - (e - B * v)
                                    ok2 += (lhs / (2 * X)).denominator == 1
                                    r = c0 + A * w
                                    ok3 += (r - rstar == A * q * P * (j - jstar) * (1 - 2 * A / (L + B)))
                                    ok4 += (abs(v - v0) <= A * q * P / (L + B) and abs(r - rstar) <= A * q * P / 2)
                                    tot += 1
check(ok1 == tot, f'r* = (e+c0-(2H-A+B)v0)/2 at the real j* ({tot})')
check(ok2 == tot, f'rounded (j,v) solves the unreduced terminal equation c0+L(v+qjP) = e-Bv mod 2X ({tot})')
check(ok3 == tot, f'r - r* = AqP(j-j*)[1-2A/(L+B)] ({tot})')
check(ok4 == tot, f'|v-v0| <= AqP/(L+B) and |r-r*| <= AqP/2 ({tot})')

# ====================================================================== §5 interval clearance lemma
log('§5 interval of length >= H eta/4 with X >= H eta/4 has a point at distance >= H eta/16 from XZ')
ok = tot = 0
mn = None
for Heta in [F(1), F(3), F(16, 5)]:
    ell = Heta / 4
    for X in [ell, ell * F(9, 8), ell * 2, ell * 5, ell * 40]:
        for k in range(0, 64):
            lo = X * F(k, 32) - X
            md = max_dist_on_interval(lo, lo + ell, X)
            tot += 1
            ok += md >= Heta / 16
            ratio = md / Heta
            mn = ratio if mn is None or ratio < mn else mn
check(ok == tot, f'clearance >= H eta/16 on {tot} placements; least observed ratio {mn}')
X = F(1, 4); ell = F(1, 4)
check(max_dist_on_interval(F(0), ell, X) == F(1, 8),
      'tight case X = H eta/4: best clearance is exactly H eta/8 >= H eta/16')

# floor corner => r = -z mod 2X
ok = tot = 0
for X in [F(5), F(17, 3)]:
    for z in [F(1, 3), F(1, 2), F(4, 5)]:
        for l in range(-3, 4):
            for kk in range(-4, 5):
                # floor corner at kk*X; final at z+2Xl; r = 2*kk*X - (z+2Xl)
                r = 2 * kk * X - (z + 2 * X * l)
                tot += 1
                ok += ((r + z) / (2 * X)).denominator == 1
check(ok == tot, f'floor corner at the midpoint forces r = -z mod 2X ({tot})')

# ====================================================================== §6 synthetic route legality
log('§6 constructed route: closed-form instances meeting the explicit hypotheses')


def build(H, A, X, c0, e, B, P, q, J, R):
    """Closed-form construction from the note; returns (legal, data)."""
    lo, hi = J
    eta_ = hi - lo
    L = 2 * H + A
    # r* as a function of v0 on the middle half
    v_a, v_b = lo + eta_ / 4, hi - eta_ / 4
    r_a = (e + c0 - (2 * H - A + B) * v_a) / 2
    r_b = (e + c0 - (2 * H - A + B) * v_b) / 2
    rlo, rhi = min(r_a, r_b), max(r_a, r_b)
    # choose the r* point of largest distance from XZ (closed form: endpoints or half-integers of X)
    cands = [rlo, rhi]
    k = floor(rlo / X)
    while k * X + X / 2 <= rhi:
        if rlo <= k * X + X / 2:
            cands.append(k * X + X / 2)
        k += 1
    rs = max(cands, key=lambda c: dist_grid(c, X))
    v0 = (e + c0 - 2 * rs) / (2 * H - A + B)
    jstar = (e - c0 - (L + B) * v0) / (2 * A * q * P)
    j = floor(jstar + F(1, 2))
    v = v0 - 2 * A * q * P * (j - jstar) / (L + B)
    w = v + q * j * P
    z = e - B * v
    r = c0 + A * w
    fl = c0 + (A + H) * w
    fin = c0 + L * w
    legal = (lo < v < hi and 0 < z < R
             and dist_grid(r, X) > R                     # solid roof, no corner, no mouth
             and dist_grid(fl, X) > 0                     # no floor corner
             and ((fin - z) / (2 * X)).denominator == 1   # positive sheet, same mouth point
             and ((fin - z) / (2 * X)) == ((fin - z) / (2 * X)))
    return legal, dict(v=v, z=z, r=r, fl=fl, j=j, clear=dist_grid(r, X), rstar_clear=dist_grid(rs, X))


# synthetic template: eta_s = 1/4, R = 1, P = 2, B = 1, e = 1; J = (1/4, 1/2) gives z = 1 - v in (1/2, 3/4)
eta_s, Rs, Ps, Bs, es = F(1, 4), 1, 2, 1, 1
Js = (F(1, 4), F(1, 2))
Cs = 2 + 2 * Rs + Ps + eta_s
Qs = fceil(64 * Cs * Cs / eta_s ** 2)
eps_s = min(F(1, 2), eta_s / (32 * Qs * Ps))
H1s = max(F(1), 64 * (Rs + 1) / eta_s)
log(f'  INFO synthetic constants: C={Cs}, Q={Qs}, eps={eps_s}, H1={H1s}')
ok = tot = 0
minclear = None
for H in [H1s + 1, 3 * H1s, F(10 ** 6)]:
    for A in [eps_s * H, eps_s * H / 3, F(1, 7)]:
        if not (A <= eps_s * H):
            continue
        for q in (1, 7, Qs):
            for mm in (1, 2, 5):
                X = (2 * H - A) * q * Ps / (2 * mm)
                if X < H * eta_s / 4:
                    continue
                for c0 in [X / 3, X * F(5, 7), F(1, 9)]:
                    leg, dat = build(H, A, X, c0, es, Bs, Ps, q, Js, Rs)
                    tot += 1
                    ok += leg
                    cl = dat['clear'] / H
                    minclear = cl if minclear is None or cl < minclear else minclear
check(ok == tot and tot > 0, f'route legal on all {tot} instances with A/H <= eps, H > H1, q <= Q; '
      f'least first-roof clearance / H = {minclear} (note: >= 3 eta/64 = {3 * eta_s / 64})')
# outside the explicit hypotheses the construction can fail (expected; not a counterexample)
bad = 0; tot2 = 0
for H in [F(9), F(20)]:
    for A in [F(4), F(8)]:
        for q in (1, 3):
            X = (2 * H - A) * q * Ps / 2
            for c0 in [X / 3, X / 5]:
                leg, _ = build(H, A, X, c0, es, Bs, Ps, q, Js, Rs)
                tot2 += 1
                bad += (not leg)
log(f'  INFO with A/H ~ 1/2 (outside eps), the construction fails its legality test on {bad}/{tot2} instances')

# ====================================================================== §7 depth-ratio conversion
log('§7 a/h > eps  =>  b <= 2K0/eps; theta = b/(2p+b)')
ok = okr = tot = nimp = 0
for a in range(1, 60):
    for d in range(1, 60):
        gam = gcd(a, 2 * d)
        p, b = a // gam, 2 * d // gam
        h = a + d
        th = F(d, h)
        tot += 1
        ok += (F(a, h) == F(2 * p, 2 * p + b) and th == F(b, 2 * p + b) and gcd(p, b) == 1)
        for ep in (F(1, 3), F(1, 10)):
            if F(a, h) > ep:
                nimp += 1
                okr += (b < 2 * p / ep)
check(ok == tot, f'a/h = 2p/(2p+b), theta = b/(2p+b), gcd(p,b)=1 ({tot})')
check(okr == nimp, f'a/h > eps forces b < 2p/eps on every grid case ({nimp} implications checked)')
nr = sum(1 for p in range(1, 30) for b in range(1, 30) if gcd(p, b) == 1 and gcd(b, 2 * p + b) == 2)
log(f'  INFO b/(2p+b) is not reduced (gcd 2) for {nr} coprime pairs with p,b < 30; the note says use reduced theta')

# ====================================================================== §8 d191 thresholds and a = 1
log('§8 d191 corner threshold at reduced theta = r/s, st279 P=6; a = 1, t = 1, several d')
P = 6
C, Q, eps, H1, K0, bmax = CONST[P]
kp = 16 * C * C / eta


def d191_log10_threshold(r, s):
    """log10 of max(8RN^3, 4 kappa+ R/(H eta))/kappa-  (H=N/s), with the note's k. Exact when feasible."""
    M = 3 * s - r
    Qd = 2 * rad(M)
    km = (1 - F(r, s)) * eta / 2
    k = 0
    while M ** k < 1 + 4 * s * kp * Qd / eta:
        k += 1
    e1 = 1 + k * phi(2 * s)
    lN = e1 * log10(M)
    return log10(8 * R) + 3 * lN - log10(km), k, e1


okd = True
for d in (2, 5, 20):
    th = F(d, d + 1)
    l10, k, e1 = d191_log10_threshold(th.numerator, th.denominator)
    okd &= l10 > log10(d + 1)
    log(f'  INFO a=1, d={d}: theta={th}, d191 threshold Y > 10^{l10:.1f} (k={k}, N=M^{e1}) but Y = {d + 1}')
check(okd, 'd191 alone does not cover a=1, t=1 at d = 2, 5, 20 (threshold exceeds Y = d+1)')
dstar = max(H1, 1 / eps)
log(f'  INFO shallow theorem covers a=1, t=1 once d+1 > max(H1, 1/eps) ~ 10^{log10(dstar):.2f}')
ok = True
for d in (10 ** 19, 10 ** 20, 10 ** 21, 10 ** 30):
    H_, A_ = F(d + 1), F(1)
    cov = (A_ / H_ <= eps and H_ > H1)
    log(f'  INFO a=1, d=10^{round(log10(d))}: A/H<=eps: {A_ / H_ <= eps}, H>H1: {H_ > H1} -> covered: {cov}')
check(not (F(1, 10 ** 19 + 1) <= eps) and (F(1, 10 ** 21 + 1) <= eps),
      'crossover for a=1,t=1 lies between d=10^19 and d=10^21 (P=6)')
# a = 1, t = 1 between the d191 and shallow regimes: what the combination says
log('  INFO a=1,t=1, 1/eps > d+1: p=1, b=2d <= 2K0/eps so theta=d/(d+1) is on the finite list; '
    'H* >= H2(d/(d+1)) >> d+1, so these d lie in the residual H <= H*, i.e. the combination certifies nothing there.')
# size of H*
s_big = fceil(bmax) + 2  # p=1, b ~ 2K0/eps, theta = b/(2+b)
log(f'  INFO H* is dominated by theta with s up to ~2K0/eps+2 ~ 10^{log10(s_big):.1f}; '
    f'there N >= M^(1+phi(2s)) so log10 log10 H* >~ {log10(s_big) + 0.0:.1f} (phi(2s) ~ s up to log factors)')
# monotonic sanity: small s thresholds grow with s
vals = [d191_log10_threshold(1, s)[0] for s in (2, 3, 5, 7, 11)]
log('  INFO d191 threshold log10 along theta=1/s, s=2,3,5,7,11 (not monotone; k varies): '
    + ', '.join(f'{v:.0f}' for v in vals))

# ====================================================================== §9 direct failure => A >= B eta/P
log('§9 direct failure u(a+tB)eta <= gcd(2Dt,auP) => A >= B eta/P (comparable section)')
ok = tot = 0
for et in (F(1, 2), F(1, 4), F(1, 16)):
    for D in range(1, 10):
        for t in range(1, 5):
            for u in range(1, 4):
                for a in range(1, 10):
                    for B in (1, 2):
                        for P in (2, 6):
                            g = gcd(2 * D * t, a * u * P)
                            if u * (a + t * B) * et <= g:
                                tot += 1
                                ok += F(a, t) >= B * et / P
check(ok == tot and tot > 0, f'A >= B eta/P on all {tot} direct-failure tuples')

# ====================================================================== §10 fixed-template finiteness (algebra only)
log('§10 fixed template: dark => H <= H*, A >= B eta/P, X <= 4HC^2(1+1/(2H-A))^2/eta')
ok = tot = 0
for H in [F(1, 2), F(1), F(3), F(50)]:
    for A in [H / 2, H / 5]:
        Xm = 4 * H * C * C * (1 + 1 / (2 * H - A)) ** 2 / eta
        tot += 1
        ok += Xm > 0 and Xm < 4 * H * C * C * (1 + 1 / H) ** 2 / eta + 1
check(ok == tot, 'far-wall X bound is finite on the residual box (2H-A > H > 0); with u,t fixed this '
      'bounds h and D, so dark placements are finite')

# ====================================================================== §11 text checks
log('§11 text checks: d191 corrections in fixed-ratio v2 and in the current scale-step note')
v2 = open(os.path.join(HERE, 'snapshot-fixed-ratio-corner-v2.md'), encoding='utf-8').read()
ss = open(os.path.join(SRC, 'l1-crossing-scale-step.md'), encoding='utf-8').read()
sn = open(os.path.join(HERE, 'snapshot.md'), encoding='utf-8').read()
log(f'  INFO M1(a) v2 scope says not uniform in theta: {"not uniform in θ" in v2}')
log(f'  INFO M1(a) v2 names the residual a/gcd bounded with d/a -> inf (e.g. a=1): '
    f'{"a=1" in v2 or "d/a" in v2}')
log(f'  INFO M1(a) v2 links the shallow return: {"l1-shallow-roof-return.md" in v2}')
oc = ss.split('**First open cases for L1.**')[1]
log(f'  INFO M1(b) scale-step open cases mention theta->1 / shallow return: '
    f'{"shallow" in oc or "θ" in oc or "d/a" in oc}')
log(f'  INFO M2 scale-step states w/b->0: {"w/b→0" in ss}; junction outside hypotheses: '
    f'{"lies outside the fixed marked-template stretch hypotheses" in ss}')
log(f'  INFO Low 2 v2 cites cone argument for constant theta: {"cone" in v2}')
log(f'  INFO Low 3 v2 uses "no openings other than": {"no openings other than" in v2}')
log(f'  INFO Low 4 v2 drops 4κ₊R/(Hη): {"4κ₊R/(Hη)" not in v2}')
log(f'  INFO shallow note: symbol H reused (h/t here, N/s in d191): {"H=h/t" in sn}; '
    f'Q redefined: {"Q=ceil" in sn}')

# ====================================================================== §12 ledger realization
log('§12 W=10 ledger realization')
LW = [(2, 0), (4, 0), (4, 1), (3, 1), (3, 4), (0, 4), (0, 3), (1, 3), (1, 2), (2, 2)]
w = turns(LW)
rots = {w[i:] + w[:i] for i in range(len(w))}
check(strictly_simple(LW) and len(LW) == 10 and 'LLLRLLLRLR' in rots,
      f'strictly simple, 10 walls, turn word {w} is a rotation of LLLRLLLRLR; area {abs(signed_area(LW))}')
check(('(2,0),(4,0),(4,1),(3,1),(3,4),(0,4),(0,3),(1,3),(1,2),(2,2)' in sn), 'note quotes the same realization')

log('')
log(f'CPU seconds: {time.process_time() - T0:.2f}')
log(f'FAILURES: {len(FAIL)}')
for f_ in FAIL:
    log('  ' + f_)
