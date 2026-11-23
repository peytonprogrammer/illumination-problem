"""d193 checks: overlap phase, projective crossing, comparable width bound.

Exact Fraction / integer arithmetic only, on parameters named in the three notes.
Covers:
  * snapshot hashes against qclass-closure/bbbb sources;
  * note 1: sheet embedding constants (0 or 2*beta), the window constants and their
    inequalities, the component count N, the mismatch/correction step on synthetic
    (delta1, delta2) offsets (no k search), the Fourier tail constant, identity (2),
    the consequence (3), the D/u formula, the p=q=1 cancellation, the lcm example;
  * note 2: the gcd facts, the divisor (2) on all small tuples satisfying (1), the
    bounded-mouth bounds, the two-generator bound w/u > 1/(BKP), the symbolic family,
    a template-aligned family with gcd(D,u)=L, the rational-period example;
  * note 3: the reduction L | Pq(jB - iA beta), the explicit bounds and area formula,
    vacuity of Delta = 0 when r = 1 and 0 < w < D, the complementary and intersection
    widths, the source-inside grid estimate, the thin-column condition;
  * the W=10 ledger realization of LLLRLLLRLR.
No room, ray, direction, slope, reflection-word or room-size search is run.
Run: python3 -B checks.py > checks.log
"""
import hashlib
import os
import time
from fractions import Fraction as F
from math import gcd, ceil, floor, log10
from itertools import product

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


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def fceil(x):
    x = F(x)
    return -((-x.numerator) // x.denominator)


def fmod(x, M):
    return x - floor(x / M) * M


def dist_int(x):
    x = F(x)
    return min(x - floor(x), floor(x) + 1 - x)


def rgcd(a, b):
    """rational gcd of positive rationals a, b."""
    a, b = F(a), F(b)
    den = a.denominator * b.denominator // gcd(a.denominator, b.denominator)
    return F(gcd(int(a * den), int(b * den)), den)


def rlcm(a, b):
    a, b = F(a), F(b)
    return a * b / rgcd(a, b)


def lcm(a, b):
    return a * b // gcd(a, b)


# ---------------------------------------------------------- copied verbatim from d192 (d191, d190) checks.py
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


def fold(phase, H):
    """circle of circumference 2H -> (height, vertical sign)."""
    s = fmod(phase, 2 * H)
    return (s, 1) if s < H else (2 * H - s, -1)


# ====================================================================== §0 snapshots
log('§0 snapshots')
NOTES = {'snapshot-l1-overlap-phase.md': ('l1-overlap-phase.md', '0ff49116'),
         'snapshot-l1-projective-crossing.md': ('l1-projective-crossing.md', '19909ad5'),
         'snapshot-l1-comparable-width-bound.md': ('l1-comparable-width-bound.md', '92402b95')}
TXT = {}
for snap, (src, pre) in NOTES.items():
    s = sha(os.path.join(HERE, snap))
    log(f'  INFO {snap} sha256 {s}')
    check(s == sha(os.path.join(SRC, src)) and s.startswith(pre),
          f'{snap} is byte-identical to bbbb/{src} and matches brief prefix {pre}')
    TXT[src] = open(os.path.join(HERE, snap), encoding='utf-8').read()
n1, n2, n3 = TXT['l1-overlap-phase.md'], TXT['l1-projective-crossing.md'], TXT['l1-comparable-width-bound.md']

# ====================================================================== §1 note 1: sheet embedding
log('§1 overlap-phase: lower phase -> tall phase embedding adds 0 or 2*beta')
ok, cnt = True, 0
for al in (F(1, 3), F(1), F(5, 2), F(7)):
    for be in (F(1), F(2), F(3)):
        for k in range(1, 40):
            ph = 2 * al * F(k, 40)
            if fmod(ph, al) == 0:
                continue
            y, sg = fold(ph, al)
            const = 0 if ph < al else 2 * be
            y2, sg2 = fold(ph + const, al + be)
            ok &= (y, sg) == (y2, sg2)
            cnt += 1
check(ok, f'folded height and vertical sign agree on {cnt} lower phases (upward sheet +0, downward sheet +2beta)')

# ====================================================================== §2 note 1: window constants
log('§2 overlap-phase: uniform window constants and the mismatch correction')
ok_ineq, ok_comp, ok_corr, ncase, ncomp, ncorr = True, True, True, 0, 0, 0
for (amin, amax, be, L, m, V, eta, Bmin) in product(
        (F(1, 4), F(1)), (F(2), F(9)), (F(1), F(3)), (F(1, 2), F(5)), (F(1, 10), F(1, 4)),
        (F(1), F(3)), (F(1, 50), F(1, 4)), (F(1, 2), F(2))):
    xmin = m * amin / (2 * (V + 1))
    N = 3 + fceil(L * eta / amin)
    l = eta / (8 * N)
    m0 = min(m * amin / 2, 4 * l * xmin)
    r = min(l, m0 / (4 * (L + 1)))
    rho = min(F(1, 8), m0 / (8 * amax), Bmin * r / (8 * (2 * amax + be)))
    ncase += 1
    ok_ineq &= all(v > 0 for v in (xmin, l, m0, r, rho))
    ok_ineq &= L * r + 2 * amax * rho <= m0 / 2          # left sheet fixed on the r-interval
    ok_ineq &= 2 * (2 * amax + be) * rho / Bmin <= r / 4  # correction stays inside the r-interval
    ok_ineq &= xmin * V < m * amin / 2                    # small-x case
    # component count: J=(s0, s0+eta), phase theta*al + x*sigma, fold points al*Z
    for al in (amin, amax):
        for x in (xmin, (xmin + L) / 2, L):
            for th in (m, F(1, 2)):
                s0 = F(-1, 3)
                lo, hi = th * al + x * s0, th * al + x * (s0 + eta)
                cuts = [F(k) * al for k in range(floor(lo / al), floor(hi / al) + 2) if lo < k * al < hi]
                ncomp += 1
                ok_comp &= len(cuts) + 1 <= N
                pts = [s0] + [(c - th * al) / x for c in cuts] + [s0 + eta]
                longest = max(b - a for a, b in zip(pts, pts[1:]))
                ok_comp &= longest >= 8 * l
                # midpoint clearance from fold boundary
                i = max(range(len(pts) - 1), key=lambda i: pts[i + 1] - pts[i])
                mid = (pts[i] + pts[i + 1]) / 2
                ph = th * al + x * mid
                d = min(fmod(ph, al), al - fmod(ph, al))
                if x >= xmin:
                    ok_comp &= d >= 4 * l * xmin
    # mismatch correction on synthetic offsets |delta1|,|delta2| <= rho (no k search)
    for d1, d2 in product((-rho, 0, rho), (-rho, rho / 3, rho)):
        for x, eps, B in ((xmin, F(1, 100), Bmin), (L, F(1), Bmin + 1)):
            al = amax
            mis0 = 2 * al * d1 + 2 * (al + be) * d2
            ok_corr &= abs(mis0) <= 2 * (2 * amax + be) * rho
            dsig = -mis0 / (x + eps + B)
            ok_corr &= abs(dsig) <= r / 4
            ok_corr &= abs(x * dsig) + 2 * al * abs(d1) <= m0 / 2
            ncorr += 1
check(ok_ineq, f'all constants positive and the three margin inequalities hold on {ncase} parameter tuples')
check(ok_comp, f'component count <= N, longest component >= 8l, midpoint clearance >= 4 l x_min on {ncomp} cases')
check(ok_corr, f'mismatch <= 2(2a_max+b)rho, |correction| <= r/4, sheet drift <= m0/2 on {ncorr} synthetic offsets')

log('  Fourier truncation: K = 1+ceil(16/(pi^2 rho^3)), tail <= 4/(pi^2 rho^3 K)')
PI2_LO, PI2_HI = F(98696, 10000), F(98697, 10000)   # 9.8696 < pi^2 < 9.8697
ok = True
# X stands for the true value pi^2 rho^3; K = 1+ceil(16/X) gives X*K >= X+16 > 16, so tail < 1/4.
for rho in (F(1, 8), F(1, 100), F(1, 10 ** 6), F(3, 10 ** 9)):
    for pi2 in (PI2_LO, (PI2_LO + PI2_HI) / 2, PI2_HI):
        X = pi2 * rho ** 3
        K = 1 + fceil(16 / X)
        ok &= 4 / (X * K) < F(1, 4)
check(ok, 'omitted product mass 2*(1/rho)*2/(pi^2 rho^2 K) < 1/4 at four rho values and three stand-ins for pi^2 (d184 with k=2)')

# ====================================================================== §3 note 1: separation algebra
log('§3 overlap-phase: identity (2), consequence (3), D/u formula')
ok2, ok3, okD, n_2, n_3 = True, True, True, 0, 0
for (al, be, P, x, eps) in product((F(1, 2), F(3, 2), F(7, 5)), (F(1), F(2)), (2, 6),
                                   (F(1, 3), F(5, 4)), (F(1, 7), F(1, 1000))):
    z0 = P * (x + eps) / (2 * al)
    for p, q in product(range(-3, 4), range(-3, 4)):
        lhs = p * P * x / (2 * al) + q * P * eps / (2 * (al + be))
        rhs = p * z0 + (P * eps / 2) * (F(q) / (al + be) - F(p) / al)
        ok2 &= lhs == rhs
        n_2 += 1
check(ok2, f'(1) equals p z0 + (P eps/2)[q/(a+b) - p/a] on {n_2} cases')
# (3): if the correction vanishes then alpha = beta p/(q-p)
for be in (1, 2, 3):
    for p, q in product(range(-5, 6), range(-5, 6)):
        if q == 0 or p == 0 or q == p:
            continue
        al = F(be * p, q - p)
        if al <= 0:
            continue
        ok3 &= F(q) / (al + be) - F(p) / al == 0
        ok3 &= al.numerator <= be * abs(p) and al.denominator <= abs(q - p)
        n_3 += 1
        # D/u formula with c/D = i/j
        for i, j in ((1, 2), (1, 3), (2, 5)):
            for nn in range(1, 6):
                z0 = F(nn, p)
                if z0 <= 0:
                    continue
                Du = 2 * al * z0 / (2 * (1 - F(i, j)))   # P = 2
                okD &= Du == F(2 * be * nn * j, 2 * (q - p) * (j - i))
check(ok3, f'correction zero <=> alpha = beta p/(q-p); numerator <= beta|p|, denominator <= |q-p| on {n_3} (p,q,beta)')
check(okD, 'D/u = 2 beta n j/[P(q-p)(j-i)] with P=2 on all generated cases')
# p=q=1 cancellation
ok = True
for al in (F(1, 2), F(4, 3), F(11, 7)):
    for be, P, eps, nn in product((1, 2), (2, 6), (F(1, 9), F(1, 1000)), (0, 1, 3)):
        z0 = nn + (P * eps / 2) * (1 / al - F(1) / (al + be))
        ok &= (z0 + (P * eps / 2) * (F(1) / (al + be) - 1 / al)) == nn
check(ok, 'p=q=1: z0 = n + (P eps/2)(1/a - 1/(a+b)) satisfies (2) exactly for every alpha')
# lcm example
ok = True
for M in range(2, 60):
    ok &= rlcm(2 * M, 2 * (M + 1)) == 2 * M * (M + 1)
    ok &= rlcm(F(2), F(2 * (M + 1), M)) == 2 * (M + 1)
check(ok, 'heights M, M+1 with unit travel: period 2M(M+1); in units of M it is 2(M+1), M=2..59')

# ====================================================================== §4 note 2: divisor
log('§4 projective crossing: gcd facts and L | Pqw on all small tuples satisfying (1)')
ok = True
for m, n in product(range(1, 60), range(1, 60)):
    if gcd(m, n) != 1:
        continue
    for be in (1, 2, 3, 4, 6, 12):
        T = m + be * n
        g = gcd(m, be)
        ok &= gcd(T, n) == 1 and gcd(T, m) == g and gcd(T // g, m // g) == 1
check(ok, 'gcd(T,n)=1, gcd(T,m)=gcd(m,beta), gcd(T/g, m/g)=1 for coprime m,n<60 and six beta')
ok, nsat, okB = True, 0, True
for m, n in product(range(1, 9), range(1, 9)):
    if gcd(m, n) != 1:
        continue
    H = F(m, n)
    for be, P in product((1, 2, 3), (1, 2, 6)):
        T = m + be * n
        L = T // gcd(m, be)
        for u, w in product((1, 2, 3, 5, 6, 10), (1, 2, 3, 4, 7)):
            for s in range(1, 13):            # s = D - w - c
                for p, q in product(range(-3, 4), range(-3, 4)):
                    if q == 0:
                        continue
                    v = F(P * p * s) / (2 * u * H) + F(P * q * w) / (2 * u * (H + be))
                    if v.denominator != 1:
                        continue
                    nsat += 1
                    ok &= (P * q * w) % L == 0
                    Kq = abs(q)
                    okB &= n <= Kq * P * w and m <= be * Kq * P * w
check(ok, f'(1) integral => L | Pqw on all {nsat} satisfying tuples')
check(okB, 'and n <= |q| P w, m <= beta |q| P w on the same tuples (bounded-mouth theorem with K >= |q|)')

log('  two-generator presentation: gcd(D,u)=1 => u <= Bn and w/u > 1/(BKP)')
ok, cnt = True, 0
for m, n in product(range(1, 30), range(1, 30)):
    if gcd(m, n) != 1:
        continue
    for A, B in ((1, 1), (2, 1), (1, 2), (3, 2), (2, 5)):
        g = gcd(A * m, B * n)
        D, u = A * m // g, B * n // g
        if gcd(D, u) != 1:
            ok = False
        for be, P, q in product((1, 2), (2, 6), (1, -2, 3)):
            T = m + be * n
            L = T // gcd(m, be)
            K = abs(q)
            for w in range(1, D + 1):
                if (P * q * w) % L == 0:
                    ok &= u <= B * n and F(w, u) > F(1, B * K * P)
                    cnt += 1
check(ok, f'on {cnt} (m,n,A,B,beta,P,q,w) with L | Pqw')

log('  symbolic family: t=m, h=m+1, N=2m+3, u=mN, D=(m+1)N, beta=1, P=2, w=2m+1, D-w-c=(m+1)(N-1)/2')
ok_all, odd_needed = True, False
for mm in range(2, 80):
    N = 2 * mm + 3
    t, h, u, D, w, P, be = mm, mm + 1, mm * N, (mm + 1) * N, 2 * mm + 1, 2, 1
    s = F((mm + 1) * (N - 1), 2)
    c = D - w - s
    H = F(h, t)
    lhs = F(P * 2) * s / (2 * u * H) + F(P * 1 * w) / (2 * u * (H + be))
    T = h + be * t
    L = T // gcd(h, be)
    good = (s.denominator == 1 and 0 < c < D - w and gcd(gcd(D, u), w) == 1 and gcd(h, t) == 1
            and F(D, u) / H == 1 and lhs == 1 and L == w
            and F(P * 2) * s / (2 * u * H) == F(N - 1, N) and F(P * w) / (2 * u * (H + be)) == F(1, N)
            and gcd(D, u) == N)
    if mm >= 5 and mm % 2 == 1:
        ok_all &= good
    elif not good:
        odd_needed = True
check(ok_all, 'odd m in 5..79: integral, 0<c<D-w, gcd(D,u,w)=1, gcd(h,t)=1, kappa=1, (1)=(N-1)/N+1/N=1, L=w, gcd(D,u)=N')
log(f'  INFO the same identities fail for some even m or m<5: {odd_needed} (odd m >= 5 is not needed)')

log('  template-aligned w=u with gcd(D,u)=L (independent offset needed for normalization), kappa=1')
ok = True
for mm in range(2, 80):
    t, h, be, P = mm, mm + 1, 1, 2
    L = 2 * mm + 1
    u, D, w, c = mm * L, (mm + 1) * L, mm * L, mm
    H = F(h, t)
    p, q = 1, 2
    lhs = F(P * p * (D - w - c)) / (2 * u * H) + F(P * q * w) / (2 * u * (H + be))
    ok &= lhs == 1 and gcd(D, u) == L and F(D, u) / H == 1 and 0 < c < D - w and w == 1 * u
check(ok, 'm=2..79: (p,q)=(1,2) satisfies (1) with c=m; L divides u; so an offset that restores gcd(D,u,o)=1 '
          'defeats note 3 even for a template-aligned mouth')

log('  rational-period example: lcm(2, (2s+1)/s) = 2(2s+1); L = 2s+1 at H=(s+1)/s, beta=1')
ok = True
for s_ in range(1, 200):
    Pp = rlcm(F(2), F(2 * s_ + 1, s_))
    L = (s_ + 1 + s_) // gcd(s_ + 1, 1)
    ok &= Pp == 2 * (2 * s_ + 1) and Pp.denominator == 1 and Pp.numerator % L == 0
check(ok, 's=1..199')
ok = True
for m, n in product(range(1, 15), range(1, 15)):
    if gcd(m, n) != 1:
        continue
    for be, Pn, Pd in product((1, 2), (1, 3, 10), (1, 2, 7)):
        if gcd(Pn, Pd) != 1:
            continue
        P = F(Pn, Pd)
        T = m + be * n
        L = T // gcd(m, be)
        H = F(m, n)
        for u, w, s, p, q in product((1, 3, 4), (1, 2, 5), range(1, 7), range(-2, 3), (1, -1, 2)):
            v = P * p * s / (2 * u * H) + P * q * w / (2 * u * (H + be))
            if v.denominator == 1:
                ok &= (Pn * q * w) % L == 0
check(ok, 'rational P = Pn/Pd: (1) integral => L | Pn q w on the grid')

# ====================================================================== §5 note 3
log('§5 comparable width bound: L | Pq(jB - iA beta) and the explicit bounds')
ok, okb, cnt, cntb = True, True, 0, 0
for m, n in product(range(1, 25), range(1, 25)):
    if gcd(m, n) != 1:
        continue
    for A, B in ((1, 1), (2, 1), (1, 2), (3, 2), (5, 3)):
        g = gcd(A * m, B * n)
        D, u = A * m // g, B * n // g
        for be in (1, 2, 3):
            T = m + be * n
            L = T // gcd(m, be)
            for r, i, j in product((1, 2), range(-2, 3), range(-3, 4)):
                if (i * D + j * u) % r or i * D + j * u <= 0:
                    continue
                w = (i * D + j * u) // r
                if w >= D:
                    continue
                Dl = j * B - i * A * be
                for P, q in product((1, 2, 6), (1, -1, 2, 3)):
                    if (P * q * w) % L:
                        continue
                    cnt += 1
                    ok &= (P * q * Dl) % L == 0
                    if Dl != 0:
                        K = abs(q)
                        S = K * P * abs(Dl)
                        V = 7
                        okb &= m <= be * S and n <= S and D <= A * be * S and u <= B * S
                        okb &= D * m + V * u * n <= (A * be * be + V * B) * S * S
                        cntb += 1
check(ok, f'L | Pqw => L | Pq(jB - iA beta) on {cnt} normalized tuples (D=Am/g, u=Bn/g, rw=iD+ju)')
check(okb, f'h<=beta S, t<=S, D<=A beta S, u<=B S, Dh+Vut<=(A beta^2+VB)S^2 on {cntb} tuples with Delta != 0')

log('  Delta = 0 with r = 1 forces w >= D (so it cannot occur for a lower-wing source)')
ok, cnt = True, 0
for A, B, be in product(range(1, 8), range(1, 8), range(1, 5)):
    if gcd(A, B) != 1:
        continue
    G = gcd(B, A * be)
    for kk in range(-3, 4):
        i, j = kk * B // G, kk * A * be // G
        for D, u in ((5, 3), (7, 2), (13, 11), (1, 9)):
            w = i * D + j * u
            cnt += 1
            ok &= (j * B - i * A * be == 0) and (w <= 0 or w > D)
check(ok, f'every integral (i,j) parallel to (B, A beta) gives w <= 0 or w > D ({cnt} cases)')
ok = True
for A, B, be, k in product(range(1, 6), range(1, 6), range(1, 4), range(0, 6)):
    ok &= (-k * B - A * be) != 0 and (-k) * B - 1 * A * be == -k * B - A * be
check(ok, 'w = D - ku: Delta = -kB - A beta != 0 for k >= 0')
ok = True
for D, u, l_, r1 in product(range(1, 30), range(1, 8), range(-2, 4), range(-1, 6)):
    wid = min(D, r1 * u) - max(0, l_ * u)
    if wid <= 0:
        continue
    forms = []
    if min(D, r1 * u) == r1 * u and max(0, l_ * u) == l_ * u:
        forms.append(('ju', r1 - l_))
    if min(D, r1 * u) == D:
        forms.append(('D-ku', max(l_, 0)))
    if max(0, l_ * u) == 0 and min(D, r1 * u) == r1 * u:
        forms.append(('ju', r1))
    good = any((f == 'ju' and k_ > 0 and wid == k_ * u) or (f == 'D-ku' and k_ >= 0 and wid == D - k_ * u)
               for f, k_ in forms)
    ok &= good
check(ok, 'every positive min(D, r1 u) - max(0, l u) is ju (j>0) or D - ku (k>=0)')
log('  INFO k = 0 gives w = D: no source with 0 < c < D - w exists; only the source-inside paragraph applies')

log('  source inside the column: rational gcd(2(H+beta), lP) <= lP, and an open interval longer than it meets every coset')
ok, cnt = True, 0
for H, be, l_, P in product((F(1, 2), F(5, 3), F(7, 4)), (1, 2), (F(1, 5), F(2, 3), F(3)), (2, 6)):
    gg = rgcd(2 * (H + be), l_ * P)
    ok &= gg <= l_ * P and (2 * (H + be) / gg).denominator == 1 and (l_ * P / gg).denominator == 1
    for target in (F(0), F(1, 3), gg / 2):
        for lo in (F(-7, 3), F(0), F(5, 11)):
            hi = lo + gg * F(1001, 1000)
            kk = floor((lo - target) / gg) + 1
            pt = target + kk * gg
            ok &= lo < pt < hi or (lo < pt + gg < hi)
            cnt += 1
check(ok, f'{cnt} cases')
ok = True
for B, eta, P, eps in product((F(1), F(3)), (F(1, 32400), F(1, 10)), (6, 30), (F(1, 10 ** 7), F(1, 10 ** 3))):
    if eps < B * eta / P:
        for l_ in (eps, eps / 2, eps / 7):
            ok &= (l_ + B) * eta > l_ * P
check(ok, 'eps < B eta / P and l <= eps imply (l+B) eta > l P')
log(f'  INFO template-aligned column eps = j >= 1 vs B eta/P at st279 (B=1, eta=1/32400, P=6): '
    f'{float(F(1, 32400) / 6):.2e}; the thin-column alternative covers only l < B eta/(P - eta) there')

# ====================================================================== §6 size of the constants
log('§6 size of K and S (INFO)')
# With d192's comparable region alpha_max = H*, rho <= m0/(8 H*) so K >= 16 (8 H*)^3/(pi^2 m0^3).
for Hs in (F(10) ** 6, F(10) ** 20):
    m0 = F(1, 10 ** 40)
    rho = m0 / (8 * Hs)
    K = 1 + fceil(16 / (PI2_LO * rho ** 3))
    log(f'  INFO alpha_max=10^{round(log10(Hs))}, m0=1e-40: K ~ 10^{len(str(K)) - 1}; area ~ S^2 >= K^2 ~ 10^{2 * (len(str(K)) - 1)}')
log('  INFO d192: H* is roughly a double exponential in 10^37 at st279, so K and the area bound are at least a fixed power of H*')

# ====================================================================== §7 text checks
log('§7 text checks')
check('k≥0' in n3 and 'w=D−ku' in n3, 'note 3 states w = D - ku with k >= 0 (k = 0 is w = D)')
check('first-hit' in n1 and 'axes interchanged' in n1, 'note 1 cites d124 first hit with axes interchanged as the upper input')
check('not for all W≤20 charts' in n3, 'note 3 scope sentence present')
check('does not refute illumination' in n2, 'note 2 labels the symbolic family as not refuting illumination')
log(f'  INFO note 2 restricts the family to odd m: {"Take odd m≥5" in n2}')
log(f'  INFO note 3 mentions the two-rectangle (eight-wall) theorem: {"two-rectangle" in n3 or "eight-wall" in n3}')

# ====================================================================== §8 ledger
log('§8 W=10 ledger realization')
LW = [(2, 0), (4, 0), (4, 1), (3, 1), (3, 4), (0, 4), (0, 3), (1, 3), (1, 2), (2, 2)]
w_ = turns(LW)
rots = {w_[i:] + w_[:i] for i in range(len(w_))}
check(strictly_simple(LW) and len(LW) == 10 and 'LLLRLLLRLR' in rots,
      f'strictly simple, 10 walls, turn word {w_} is a rotation of LLLRLLLRLR; area {abs(signed_area(LW))}')
quote = '(2,0),(4,0),(4,1),(3,1),(3,4),(0,4),(0,3),(1,3),(1,2),(2,2)'
check(all(quote in t_ for t_ in (n1, n2, n3)), 'all three notes quote the same realization')

log('')
log(f'CPU seconds: {time.process_time() - T0:.2f}')
log(f'FAILURES: {len(FAIL)}')
for f_ in FAIL:
    log('  ' + f_)
