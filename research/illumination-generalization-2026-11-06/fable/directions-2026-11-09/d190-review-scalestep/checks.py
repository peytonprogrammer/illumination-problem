"""d190 review checks for the scale-step snapshot (snapshot.md, sha256 835be639...).

Named objects only:
  * the note's constants and inequality chain (gate elimination, coset lemma, gcd/lcm step, (1),
    far-wall shift, final ratio bound), checked as exact identities/inequalities on a fixed
    deterministic grid of small integer and rational parameters (arithmetic only, no rooms);
  * st279's upper run widths (3, 3, 5) for the stated P = 6 and P = 30;
  * the note's two-rectangle junction: lower [0,D]x[0,a+1], upper [-2,1]x[a+1,a+b+2], marks (1,1) and
    (-1,a+1+b), at even b = 2, 4, 6, 8, 10 with D = a = (b+1)^2+1 and D = a = b+2;
  * the note's W=10 ledger realization of LLLRLLLRLR.
The only traced paths are the straight upper branch of the junction at closed-form speeds 3/(2b) and
1/b. No room, ray, direction, slope, word or room-size search is run.
trace() is copied verbatim from d189 (d184/d182/d181/d175).
Run: python3 -B checks.py > checks.log
"""
import time
from fractions import Fraction as F
from math import gcd, isqrt
from itertools import product
from decimal import Decimal, getcontext

T0 = time.process_time()
FAIL = []


def log(*a):
    print(*a, flush=True)


def check(ok, msg):
    log(('  PASS ' if ok else '  FAIL ') + msg)
    if not ok:
        FAIL.append(msg)


# ------------------------------------------------------------------ copied verbatim from d189
def trace(P, A, B, maxrefl=10**6):
    n = len(P)
    hw = [(P[i], P[(i + 1) % n]) for i in range(n) if P[i][1] == P[(i + 1) % n][1]]
    vw = [(P[i], P[(i + 1) % n]) for i in range(n) if P[i][0] == P[(i + 1) % n][0]]
    V = {(F(a), F(b)) for a, b in P}
    X, Y = F(A[0]), F(A[1])
    vx, vy = F(B[0]) - X, F(B[1]) - Y
    tau, contacts = F(1), []
    for _ in range(maxrefl):
        best = None
        if vx:
            for a, b in vw:
                t = (a[0] - X) / vx
                if t > 0 and (best is None or t < best[0]) and min(a[1], b[1]) <= Y + vy * t <= max(a[1], b[1]):
                    best = (t, 'v')
        if vy:
            for a, b in hw:
                t = (a[1] - Y) / vy
                if t > 0 and (best is None or t < best[0]) and min(a[0], b[0]) <= X + vx * t <= max(a[0], b[0]):
                    best = (t, 'h')
        if best is None or best[0] > tau:
            return 'end', (X + vx * tau, Y + vy * tau), contacts
        t, kind = best
        X, Y = X + vx * t, Y + vy * t
        if best[0] == tau:
            return 'wall-end', (X, Y), contacts
        tau -= t
        if (X, Y) in V:
            return 'corner', (X, Y), contacts
        contacts.append(((X, Y), kind))
        if kind == 'v': vx = -vx
        else: vy = -vy
    return 'limit', (X, Y), contacts


def lcm(*xs):
    r = 1
    for x in xs:
        r = r * x // gcd(r, x)
    return r


def egcd(a, b):
    if b == 0:
        return (a, 1, 0)
    g, x, y = egcd(b, a % b)
    return (g, y, x - (a // b) * y)


def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


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


# ====================================================================== §0 constants
log('§0 constants of the theorem')
for n in (1, 2, 3):
    m = 4 * n
    T = 1 + fib(3 * m - 1)
    log(f'  INFO lattice area n={n}: m={m}, T=1+F_{3*m-1}={T}, eta=1/(4T^2)=1/{4*T*T}')
check(fib(0) == 0 and fib(1) == 1 and fib(11) == 89, 'F_0=0, F_1=1, F_11=89 (n=1 gives T=90)')
# Stability: alpha=(3-sqrt5)/2; no p/q with q<=T within 1/(4T^2) (checked with 60-digit decimals at T=90)
getcontext().prec = 60
alpha = (Decimal(3) - Decimal(5).sqrt()) / 2
T = 90
rad = Decimal(1) / (4 * T * T)
bad = [(p, q) for q in range(1, T + 1) for p in range(0, q + 1) if abs(alpha - Decimal(p) / q) <= rad]
check(not bad, f'alpha +- 1/(4T^2) contains no p/q with q <= T = {T} (closed interval width 1/(2T^2))')
check(all(p * p - 3 * p * q + q * q != 0 for q in range(1, T + 1) for p in range(q + 1)),
      'p^2-3pq+q^2 != 0 for 0<=p<=q<=90 (the d124 quadratic estimate numerator)')
# st279 upper run widths
wid_visited, wid_all = [3], [3, 3, 5]
check(lcm(*[2 * w for w in wid_visited]) == 6 and lcm(*[2 * w for w in wid_all]) == 30,
      'st279: visited-run period lcm(6)=6; all upper runs lcm(6,6,10)=30')
check(2 * lcm(*range(1, 9)) == 1680 and all(1680 % (2 * w) == 0 for w in range(1, 9)),
      'P=2 lcm(1..W) is divisible by 2w for every run width w<=W (W=8 shown, P=1680)')

# ====================================================================== §1 gate elimination
log('§1 gate elimination: u(A+tB)v in t(ue-c)+g_A Z, explicit v_phys, index (2Dt l - AuP k)/g_A')
grid = list(product((1, 2, 3), (1, 2, 5), (3, 7), (1, 2), (11, 30), (1, 4), (-3, 2), (6, 30)))
ok_id = ok_seam = ok_onto = 0
for (u, t, A, B, D, c, e, P) in grid:
    gA = gcd(2 * D * t, A * u * P)
    for l, k in product((-2, 0, 1, 3), (-1, 0, 2)):
        vphys = F(u * e - c + 2 * D * l + u * B * k * P, A + t * B)
        v = F(t, u) * vphys - k * P
        # lower positive sheet: c + A vphys == u(e - B v) + 2 D l, and v_phys = u(v+kP)/t
        if c + A * vphys == u * (e - B * v) + 2 * D * l and vphys == F(u, t) * (v + k * P):
            ok_seam += 1
        lhs = u * (A + t * B) * v - t * (u * e - c)
        if lhs == 2 * D * t * l - A * u * P * k and (lhs / gA).denominator == 1:
            ok_id += 1
    g, x, y = egcd(2 * D * t, -A * u * P)
    # g may be negative-signed: normalise; index of (x, y) is +-1
    if abs(2 * D * t * x - A * u * P * y) == gA:
        ok_onto += 1
NT = len(grid) * 12
check(ok_seam == NT, f'seam congruence and v_phys=u(v+kP)/t hold on all {NT} grid lifts')
check(ok_id == NT, f'u(A+tB)v - t(ue-c) = 2Dt l - AuP k, an integer multiple of g_A, on all {NT} lifts')
check(ok_onto == len(grid), f'index map (l,k) -> (2Dt l - AuP k)/g_A attains +-1 (onto Z) on all {len(grid)} tuples')

# ====================================================================== §2 floor corners: coset lemma
log('§2 floor-route corner lemma')
ok_step = 0
for (a, d, t, B) in product((1, 2, 5, 9), (1, 2, 3, 7), (1, 2, 4), (1, 3)):
    D = 13
    A = a + 2 * d
    st = F(2 * D * d, A + t * B)
    ok_step += (0 < st < D)
check(ok_step == 4 * 4 * 3 * 2, 'incrementing l moves the floor coordinate by 2Dd/(A+tB), strictly in (0,D), on 96 grid points')
# exhaustive verification of "two consecutive indices => a corner-free lift" on named small tuples:
# enumerate lifts in a box, group by index, and check no two consecutive indices are all-corner.
ok_pair = tot_pair = 0
for (u, t, a, d, B, D, c, e, P) in [(1, 1, 3, 1, 1, 6, 2, 1, 6), (2, 3, 4, 2, 2, 10, 3, -1, 6),
                                     (1, 2, 6, 3, 1, 9, 4, 0, 4), (3, 1, 2, 1, 1, 12, 5, 2, 6),
                                     (1, 1, 4, 2, 1, 4, 1, 1, 2), (1, 1, 2, 1, 1, 3, 1, 0, 2)]:
    A = a + 2 * d
    gA = gcd(2 * D * t, A * u * P)
    fib_ = {}
    for l in range(-40, 41):
        for k in range(-40, 41):
            idx = (2 * D * t * l - A * u * P * k) // gA
            vphys = F(u * e - c + 2 * D * l + u * B * k * P, A + t * B)
            corner = ((c + d * vphys) / D).denominator == 1
            fib_.setdefault(idx, []).append(corner)
    for i in range(-5, 5):
        if i in fib_ and i + 1 in fib_:
            tot_pair += 1
            ok_pair += not (all(fib_[i]) and all(fib_[i + 1]))
check(ok_pair == tot_pair and tot_pair > 0,
      f'{tot_pair} consecutive index pairs on 6 small tuples: never both fibres all-corner (lifts in |l|,|k|<=40)')

# ====================================================================== §3 gcd/lcm step and (1)
log('§3 gcd/lcm step: gcd(g_a,g_L) | uP gcd(a,2d); lcm | 2Dt; hence (1)')
ok_g = n_g = 0
for (u, t, a, d, D, P) in product((1, 2, 3), (1, 2, 5), (3, 4, 9, 12), (1, 2, 3, 6), (7, 12, 30), (6, 30)):
    L = a + 2 * d
    ga, gL = gcd(2 * D * t, a * u * P), gcd(2 * D * t, L * u * P)
    G, Lc = gcd(ga, gL), lcm(ga, gL)
    gam = gcd(a, 2 * d)
    n_g += 1
    ok_g += ((u * P * gam) % G == 0 and (2 * D * t) % Lc == 0 and ga * gL <= u * P * gam * 2 * D * t)
check(ok_g == n_g, f'on {n_g} grid tuples: gcd | uP*gamma, lcm | 2Dt, g_a g_L <= 2uP gamma D t')
check(all(gcd(a, a + 2 * d) == gcd(a, 2 * d) for a in range(1, 40) for d in range(1, 20)),
      'gcd(a, a+2d) = gcd(a, 2d) for 1<=a<40, 1<=d<20')
# (1) from window failures: u(a+tB)eta <= g_a, u(L+tB)eta <= 2 g_L  =>  D >= u(a+tB)(L+tB)eta^2/(4 gamma P t)
log('  INFO (1): u^2(a+tB)(L+tB)eta^2 <= 2 g_a g_L <= 4 u P gamma D t, i.e. D >= u(a+tB)(L+tB)eta^2/(4 gamma P t)')

# ====================================================================== §4 far-wall shift and final bound
log('§4 far-wall: Q, C, delta, e\' < 0, s uR < L, height step, final ratio bound')
ok4 = n4 = 0
for (R, B, t, L, P, eta, u, z_over_u) in product((1, F(5, 2), 7), (1, 3), (1, 4, 50), (3, 10, 200), (6, 30),
                                                (F(1, 4), F(1, 100)), (1, 3), (0, F(1, 2), 1)):
    zu = z_over_u * R                       # 0 <= z/u <= R
    Q = max(F(1), 1 + F(R) / B, F(2 * R * t, L))
    # worst case: inf|v'| just above Q, sup|v'| = inf + eta, with inf <= Q + P
    for inf_ in (Q + F(1, 1000), Q + P):
        sup_ = inf_ + eta
        C = 2 + 2 * R + P + eta
        e_p = zu + B * (-inf_)              # intercept at the least negative speed (largest e')
        s_max = F(t) / (u * inf_)
        width = F(t) / (u * inf_) - F(t) / (u * sup_)
        n4 += 1
        ok4 += (sup_ <= C * (1 + F(t, L)) and e_p < 0 and s_max * u * R < L
                and width >= t * eta / (u * C * C * (1 + F(t, L)) ** 2))
check(ok4 == n4, f'on {n4} grid cases: sup|v\'| <= C(1+t/L), e\' < 0, s uR < L, delta >= t eta/[u C^2 (1+t/L)^2]')
ok5 = n5 = 0
for (D, c, a, d, ue) in product((10, 37), (1, 5, 9), (2, 6), (1, 4), (F(-1, 3), -5, -40)):
    if not 0 < c < D: continue
    h = a + d
    step = F(2 * h * (D - c)) / (2 * D - c - ue)
    n5 += 1
    ok5 += (0 < step < h and 2 * D - c - ue > D)
check(ok5 == n5, f'far-wall height step 2h(D-c)/(2D-c-ue\') in (0,h), and 2D-c-ue\' > D, on {n5} cases')
check(all(2 * (a + d) > a + 2 * d for a in range(1, 30) for d in range(1, 30)),
      'return roof spacing: 2h > L, so 2h/s > uR follows from s uR < L')
ok6 = n6 = 0
for (a, d, t, B) in product((1, 2, 5, 40), (1, 3, 20), (1, 7, 1000), (1, 2, 9)):
    L = a + 2 * d
    n6 += 1
    ok6 += (F((a + t * B) * (L + t * B)) / (1 + F(t, L)) ** 2 >= a * L)
check(ok6 == n6, f'(a+tB)(L+tB)/(1+t/L)^2 >= aL for B>=1, a<=L on {n6} cases')
# final: (a+tB)(L+tB) eta^3 <= 16 h gamma P C^2 (1+t/L)^2  =>  a/gamma <= 16 P C^2 / eta^3 (since L >= h)
ok7 = n7 = 0
for (u, t, a, d, B, P, eta, C) in product((1, 5), (1, 3, 40), (3, 8, 50), (1, 2, 5), (1, 4), (6,), (F(1, 4),), (F(41, 4),)):
    L, h, gam = a + 2 * d, a + d, gcd(a, 2 * d)
    # D allowed by (1) at its minimum and by the far-wall failure at its maximum
    Dmin = F(u * (a + t * B) * (L + t * B)) * eta ** 2 / (4 * gam * P * t)
    Dmax = 4 * h * u * C * C * (1 + F(t, L)) ** 2 / (t * eta)
    K = 16 * P * C * C / eta ** 3
    n7 += 1
    ok7 += ((Dmin <= Dmax) <= (F(a, gam) <= K))   # joint failure implies a/gamma <= K
check(ok7 == n7, f'joint failure (Dmin <= Dmax) implies a/gamma <= K on {n7} cases')
log('  INFO symbolic: Dmin<=Dmax <=> (a+tB)(L+tB)eta^3 <= 16 h gamma P C^2 (1+t/L)^2; u and t cancel exactly')

# ====================================================================== §5 growing depth
log('§5 growing-depth consequences')
check(all(gcd(a, 2 * d) <= 2 * d for a in range(1, 60) for d in range(1, 30)), 'gamma = gcd(a,2d) <= 2d')
for (p, q) in ((2, 2), (1, 1), (2, 1), (3, 4), (5, 6)):      # a = p n, 2d = q n
    vals = {F(p * n, gcd(p * n, q * n)) for n in range(2, 60, 2)}
    check(len(vals) == 1, f'a:2d = {p}:{q} family: a/gcd(a,2d) is constant {vals.pop()} (bounded, so open)')

# ====================================================================== §6 two-rectangle junction
log('§6 the note\'s two-rectangle junction')
for b in (2, 4, 6, 8, 10):
    for tag, a in (('(b+1)^2+1', (b + 1) ** 2 + 1), ('b+2', b + 2)):
        D = a
        Pj = [(0, 0), (D, 0), (D, a + 1), (1, a + 1), (1, a + b + 2), (-2, a + b + 2), (-2, a + 1), (0, a + 1)]
        S, Tm = (1, 1), (-1, a + 1 + b)
        w = turns(Pj)
        gh, gv = wall_gcds(Pj)
        ok = (strictly_simple(Pj) and len(Pj) == 8 and w.count('R') == 2 and (gh, gv) == (1, 1)
              and gcd(a + 1, b + 1) == 1 and inside(Pj, *S) and inside(Pj, *Tm) and S != Tm
              and (S[0] + S[1]) % 2 == (Tm[0] + Tm[1]) % 2)
        check(ok, f'b={b}, D=a={tag}={a}: strictly simple, W=8, 2 reflex, wall gcds (1,1), gcd(a+1,b+1)=1, '
                  f'marks interior, same parity')
        # straight upper branch: speed v (horizontal per unit vertical, downward from target)
        # seam abscissa -1 + b v must lie in the open overlap (0,1): v in (1/b, 2/b), length exactly 1/b = w/b
        v = F(3, 2 * b)
        end = (Tm[0] + (b + 1) * v, Tm[1] - (b + 1))
        r1 = trace(Pj, Tm, end)
        v0 = F(1, b)
        r0 = trace(Pj, Tm, (Tm[0] + b * v0 + v0, Tm[1] - b - 1))
        check(r1[0] == 'end' and not r1[2] and r0[0] == 'corner' and r0[1] == (0, a + 1),
              f'b={b}: speed 3/(2b) crosses the width-1 seam at x=1/2 with no contact; speed 1/b hits the reflex '
              f'corner (0,{a + 1}); straight-branch window has length 1/b')
check(all(F(b, (b + 1) ** 2 + 1) < F(1, b + 1) for b in (10, 100, 1000)), 'b/a -> 0 on D=a=(b+1)^2+1 (b = o(a))')
# Contrast inside the note's own theorem: physical speeds are u(v+kP)/t, so the physical window is (u/t)*eta.
eta_ = F(1, 32400)
check(all(F(u, u) * eta_ == eta_ for u in (1, 10, 10**6)),
      'exact stretch u=t: physical window (u/t)eta = eta for every t, even with t=o(a); the impossibility needs w/b -> 0')

# ====================================================================== §7 arm phase
log('§7 appendage phase: excursion of height H in an arm of width w adds 2Hv mod 2w')


def fold(x, w):
    r = x % (2 * w)
    return (r, 1) if r <= w else (2 * w - r, -1)


ok8 = n8 = 0
for (w, H, v, x0) in product((1, 2, 3), (1, 2, 5), (F(1, 3), F(1, 2), F(3, 4), 1, F(5, 2)), (F(1, 7), F(1, 2))):
    if x0 >= w: continue
    pos, sgn = fold(x0 + 2 * H * v, w)
    same = (pos == x0 and sgn == 1)
    n8 += 1
    ok8 += (same == ((2 * H * v) % (2 * w) == 0))
check(ok8 == n8, f'return to entry coordinate with original horizontal sign iff 2Hv = 0 mod 2w, on {n8} cases')
# earlier roof contacts formula
ok9 = n9 = 0
for (D, c, h, d, s, j) in product((20,), (3, 11), (5, 9), (1, 2), (F(1, 3), F(2, 1)), (0, 1, 2)):
    l = F((2 * j + 1) * h + d) / s
    if not 0 < l < 2 * D - c: continue
    x = D - abs(D - (c + l))
    xu = c + l
    x_fold = xu if xu <= D else 2 * D - xu
    n9 += 1
    ok9 += (x == x_fold and -d + s * l == (2 * j + 1) * h)
check(ok9 == n9, f'l_j = ((2j+1)h+d)/s reaches unfolded roof height (2j+1)h from -d; x_j = D-|D-(c+l_j)| folds once ({n9} cases)')

# ====================================================================== §8 ledger realization
log('§8 W=10 ledger realization')
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
