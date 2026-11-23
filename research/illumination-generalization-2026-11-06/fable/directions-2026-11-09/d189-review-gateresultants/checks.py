"""d189 review checks for the gate-resultants snapshot (snapshot.md, sha256 5a2e76a1...).

Named rooms only: the st279 (m=5) crossing slice st(a,D) that the note names, at
  * the d188 ray a = 7+2n, D = 3a (n = 0, 1, 5, 20, 31, 44, 47, 100, the d188 named list), and
  * the note's family D = a(a+2), odd a, at a = 9 (least odd a meeting the note's own sufficient
    condition D*delta > 4h, solved in closed form) and a = 101 (d186's named a).
Every traced velocity comes from a closed-form gate or root formula in the note (modular inverse,
least root above an endpoint). No room, ray, direction, slope, word or room-size search is run.
trace(), shoot(), strictly_simple(), st(), area(), wall_gcds() are copied verbatim from d188/d186.
Run: python3 -B checks.py > checks.log
"""
import time
from fractions import Fraction as F
from math import floor, ceil, gcd

T0 = time.process_time()
FAIL = []


def log(*a):
    print(*a, flush=True)


def check(ok, msg):
    log(('  PASS ' if ok else '  FAIL ') + msg)
    if not ok:
        FAIL.append(msg)


# ------------------------------------------------------------------ copied verbatim from d184 (d182/d181/d175)
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


# ------------------------------------------------------------------ d109 path.py shoot(), adapted: polygon vertex list
def shoot(P, s, d, t, maxev=100000):
    """Events (kind, point) from s in direction d until t is reached; raises on corner hit."""
    n = len(P)
    E = [((F(P[i][0]), F(P[i][1])), (F(P[(i + 1) % n][0]), F(P[(i + 1) % n][1]))) for i in range(n)]
    V = {a for a, _ in E}
    p, d, t, ev = (F(s[0]), F(s[1])), (F(d[0]), F(d[1])), (F(t[0]), F(t[1])), []
    for _ in range(maxev):
        best = None
        for (a, b) in E:
            if a[0] == b[0]:
                if d[0] == 0: continue
                tt = (a[0] - p[0]) / d[0]
                if tt <= 0: continue
                y = p[1] + tt * d[1]
                if min(a[1], b[1]) <= y <= max(a[1], b[1]) and (best is None or tt < best[0]):
                    best = (tt, 'x', (a[0], y))
            else:
                if d[1] == 0: continue
                tt = (a[1] - p[1]) / d[1]
                if tt <= 0: continue
                x = p[0] + tt * d[0]
                if min(a[0], b[0]) <= x <= max(a[0], b[0]) and (best is None or tt < best[0]):
                    best = (tt, 'y', (x, a[1]))
        tt, kind, q = best
        ttT = (t[0] - p[0]) / d[0] if d[0] != 0 else (t[1] - p[1]) / d[1]
        if 0 < ttT < tt and p[0] + ttT * d[0] == t[0] and p[1] + ttT * d[1] == t[1]:
            ev.append(('reach', t)); return ev
        if q in V:
            raise RuntimeError(f"corner hit at {q}")
        ev.append(('v' if kind == 'x' else 'h', q))
        d = (-d[0], d[1]) if kind == 'x' else (d[0], -d[1])
        p = q
    raise RuntimeError("no arrival")


# ------------------------------------------------------------------ d184 geometry (copied)
def strictly_simple(P):
    n = len(P)
    E = [(P[i], P[(i + 1) % n]) for i in range(n)]

    def inter(e, f):
        (a, b), (c, d) = e, f
        if a[0] == b[0] and c[0] == d[0]:
            return a[0] == c[0] and max(min(a[1], b[1]), min(c[1], d[1])) <= min(max(a[1], b[1]), max(c[1], d[1]))
        if a[1] == b[1] and c[1] == d[1]:
            return a[1] == c[1] and max(min(a[0], b[0]), min(c[0], d[0])) <= min(max(a[0], b[0]), max(c[0], d[0]))
        if a[1] == b[1]:
            (a, b), (c, d) = (c, d), (a, b)
        return min(c[0], d[0]) <= a[0] <= max(c[0], d[0]) and min(a[1], b[1]) <= c[1] <= max(a[1], b[1])
    for i in range(n):
        for j in range(i + 2, n):
            if i == 0 and j == n - 1:
                continue
            if inter(E[i], E[j]):
                return False
    return all((P[i - 1][0] == P[i][0]) != (P[i][0] == P[(i + 1) % n][0]) for i in range(n))


# ------------------------------------------------------------------ st279 (m=5) crossing slice of the note
def st(a, D):
    """Bands: y in (4-a,5) x [5-D,5]; (5,6) x [4,7]; (6,7) x [5,8]; (7,12) x [7,12]."""
    return [(5 - D, 4 - a), (5, 4 - a), (5, 5), (7, 5), (7, 6), (8, 6), (8, 7), (12, 7), (12, 12), (7, 12),
            (7, 7), (5, 7), (5, 6), (4, 6), (4, 5), (5 - D, 5)]


S_st = lambda a: (4, 5 - a)
T_st = (6, 6)


def area(P):
    n = len(P)
    return abs(sum(F(P[i][0]) * P[(i + 1) % n][1] - F(P[(i + 1) % n][0]) * P[i][1] for i in range(n))) / 2


def wall_gcds(P):
    n = len(P)
    gh = gv = 0
    for i in range(n):
        (x0, y0), (x1, y1) = P[i], P[(i + 1) % n]
        if y0 == y1: gh = gcd(gh, abs(x1 - x0))
        else: gv = gcd(gv, abs(y1 - y0))
    return gh, gv



def first_in(r, g, lo, hi):
    """least element of r + gZ strictly inside (lo,hi), or None (closed form)."""
    k = floor(F(lo - r, g)) + 1
    x = r + g * k
    return x if x < hi else None


# Note coordinates for st279: z = 5 - x, roof y = 5, mouth z in (0,1) so R = 1, c = 1, d = 1, h = a+1.
# Upper approach to T = (6,6): z_T = -1, B = 1, e = -1, J = {v0 : z = e - B v0 in (0,1)} = (-2,-1), eta = 1.
c, d, B, e, R = 1, 1, 1, -1, 1
Jlo, Jhi = F(-2), F(-1)
eta = Jhi - Jlo
P6 = 6            # 2 * width of the only visited upper run (5,6)x[4,7]
P30 = 30          # lcm of 2*widths of all upper runs: widths 3, 3, 5


log('§0 setup')
P = st(7, 21)
check(strictly_simple(P) and wall_gcds(P) == (1, 1), 'st(7,21) strictly simple, wall gcds (1,1)')
log('  INFO upper runs above the roof y=5 in z=5-x: (5,6)x z[-2,1] width 3; (6,7)x z[-3,0] width 3; (7,12) width 5')
log('  INFO P per the note\'s literal definition (all upper runs) = lcm(6,6,10) = %d; the note uses P = 6' % P30)

# ---------------------------------------------------------------- §1 periodic upper approach
log('§1 periodic upper approach in st279: same seam z, v = v0 + kP, reach T with no horizontal contact')
for v0 in (F(-3, 2), F(-5, 4), F(-7, 4)):
    z0 = e - B * v0
    for k in (-10, -3, -2, -1, 0, 1, 2, 3, 10):
        v = v0 + P6 * k
        start = (5 - z0, F(5))
        ev = shoot(st(7, 21), start, (-v, 1), T_st)
        hs = [q for kk, q in ev if kk == 'h']
        nlat = len([1 for kk, q in ev if kk == 'v'])
        check(ev[-1][0] == 'reach' and not hs,
              f'v0={v0}, k={k:>3}: v={v}, z={z0}, reaches T, {nlat} lateral reflections, intercept e+BkP={e + B * P6 * k}')
# lateral-reflection count is |kP|/W = 2|k| (even), as the parity argument says
ev = shoot(st(7, 21), (5 - F(1, 2), F(5)), (-(F(-3, 2) + 6 * 7), 1), T_st)
check(len([1 for kk, q in ev if kk == 'v']) == 14, 'k=7: 14 = 2k lateral reflections (even parity, kP/W = 2k)')

# ---------------------------------------------------------------- §2 short routes in v-form on the d188 ray
log('§2 v-form gate (A+B)v0 in e-c+g_A Z, g_A = gcd(2D, A P), on the d188 ray a=7+2n, D=3a')


def vgate(A, D, Pp):
    g = gcd(2 * D, A * Pp)
    N = first_in(e - c, g, (A + B) * Jlo, (A + B) * Jhi)
    if N is None:
        return None
    v0 = F(N, A + B)
    rhs = e - B * v0 - c - A * v0           # = A*Pp*k mod 2D, integer multiple of g
    assert rhs.denominator == 1 and int(rhs) % g == 0
    m = 2 * D // g
    k = (int(rhs) // g) * pow((A * Pp // g) % m, -1, m) % m if m > 1 else 0
    v = v0 + Pp * k
    assert ((c + A * v - (e - B * v0)) / (2 * D)).denominator == 1
    return v0, k, v, g


rows = []
for n in (0, 1, 5, 20, 31, 44, 47, 100):
    a = 7 + 2 * n; D = 3 * a
    Pm = st(a, D)
    check(strictly_simple(Pm) and wall_gcds(Pm) == (1, 1), f'n={n}: st({a},{D}) strictly simple, gcds (1,1)')
    dr = vgate(a, D, P6)
    check(dr is None and gcd(2 * D, a * P6) == 6 * a, f'n={n}: direct g_a = gcd(2D,6a) = 6a = {6 * a}; no direct v-gate solution')
    fl = vgate(a + 2 * d, D, P6)
    v0, k, v, g = fl
    check(g == 6, f'n={n}: floor g = gcd(6a, 6(a+2)) = {g}')
    check(((c + d * v) / D).denominator != 1, f'n={n}: floor phase c+dv = {c + d * v} not in DZ (no floor corner)')
    ev = shoot(Pm, S_st(a), (-v, -1), T_st)
    hs = [q for kk, q in ev if kk == 'h']
    ok = ev[-1][0] == 'reach' and len(hs) == 1 and hs[0][1] == 4 - a
    check(ok, f'n={n}: floor shot v0={v0}, k={k}, seam v={v}: reaches T, only horizontal contact is the floor; {len(ev) - 1} reflections')
    rows.append((n, a, D, v, len(ev) - 1))
# cross-check with d188 table velocities (d188 lists launch velocities; seam speed here is in z, launch dx = -v)
log('  INFO (n, a, D, seam v, reflections): ' + '; '.join(f'({n},{a},{D},{v},{r})' for n, a, D, v, r in rows))

# ---------------------------------------------------------------- §3 bounded modulus along the affine ray
log('§3 bounded modulus on D = 21 + 6n, a = 7 + 2n (p=6, q=2, D0=21, a0=7)')
p, q, D0, a0 = 6, 2, 21, 7
Delta = {j: q * D0 - p * (a0 + j) for j in (0, 2 * d)}
check(Delta[0] == 0 and Delta[2] == -12 and Delta[0] - Delta[2] == 2 * d * p, f'Delta_0 = {Delta[0]}, Delta_2 = {Delta[2]}, difference 2dp = {2 * d * p}')
for n in (0, 1, 5, 20, 31, 44, 47, 100):
    a = a0 + q * n; D = D0 + p * n
    check(q * D - p * (a + 2) == Delta[2], f'n={n}: qD - p(a+2) = {q * D - p * (a + 2)} constant')
    g2 = gcd(2 * D, (a + 2) * P6)
    check((2 * P6 * abs(Delta[2])) % g2 == 0, f'n={n}: g_(a+2) = {g2} divides 2P|Delta_2| = {2 * P6 * abs(Delta[2])}')
R0 = 2 * P6 * abs(Delta[2])
for n in (R0, 2 * R0, 7 * R0):
    a = a0 + q * n; D = D0 + p * n
    check(gcd(2 * D, (a + 2) * P6) == gcd(2 * D0, (a0 + 2) * P6), f'n={n} (R0={R0} | n): g_(a+2) = base value {gcd(2 * D0, (a0 + 2) * P6)}')
log('  INFO direct route: Delta_0 = 0, so g_a = 6a is unbounded on this ray, as the "at least one Delta_j" clause allows')
# with the literal P = 30
for n in (0, 1, 5, 20):
    a = 7 + 2 * n; D = 3 * a
    log(f'  INFO P=30, n={n}: floor g = gcd(6a,30(a+2)) = {gcd(2 * D, 30 * (a + 2))} (= 6*gcd(a,5) for odd a)')
    check(gcd(2 * D, 30 * (a + 2)) == 6 * gcd(a, 5), f'P=30, n={n}: floor modulus 6*gcd(a,5), still bounded')

# ---------------------------------------------------------------- §4 D = a(a+2): raw moduli >= 2a
log('§4 family D = a(a+2), odd a: gcd(2D,6a) and gcd(2D,6(a+2)) >= 2a')
for a in (7, 9, 11, 13, 15, 101, 1001):
    D = a * (a + 2)
    g0, g2 = gcd(2 * D, 6 * a), gcd(2 * D, 6 * (a + 2))
    check(g0 == 2 * a * gcd(a + 2, 3) and g2 == 2 * (a + 2) * gcd(a, 3) and min(g0, g2) >= 2 * a,
          f'a={a}: g_a = {g0} = 2a*gcd(a+2,3), g_(a+2) = {g2} = 2(a+2)*gcd(a,3)')
    g0b, g2b = gcd(2 * D, 30 * a), gcd(2 * D, 30 * (a + 2))
    check(min(g0b, g2b) >= 2 * a, f'a={a}, P=30: moduli {g0b}, {g2b} still >= 2a')

# ---------------------------------------------------------------- §5 far-wall return on D = a(a+2)
log('§5 far-wall return: d + s(2D-c-e\') - B = (2j+1)h, s in (1/2,1) (k=0: v in (-2,-1) already negative, e\'=-1)')
slo, shi = F(1, 2), F(1)
delta = shi - slo
check(delta == abs(1 / Jlo - 1 / Jhi) and R * shi <= 1, f'delta = |1/v_l - 1/v_r| = {delta}; R s < 1 on the open interval')
# least odd a with D*delta > 4h, D = a(a+2), h = a+1: a(a+2)/2 > 4(a+1) <=> a^2 - 6a - 8 > 0 <=> a > 3+sqrt(17) = 7.12
a_min = 9
check(F(a_min * (a_min + 2)) * delta > 4 * (a_min + 1) and not (F(7 * 9) * delta > 4 * 8),
      'closed form: a=9 is the least odd a with D*delta > 4h on D=a(a+2) (a=7 gives 31.5 <= 32)')
for a in (9, 101):
    D = a * (a + 2); h = a + 1; ep = e
    Pm = st(a, D)
    check(strictly_simple(Pm) and wall_gcds(Pm) == (1, 1), f'a={a}: st({a},{D}) strictly simple, gcds (1,1)')
    L = 2 * D - c - ep
    # roots s_j = ((2j+1)h + B - d)/L; least j with s_j > 1/2
    j0 = floor(F(slo * L - B + d - h, 2 * h)) + 1
    roots = [F((2 * j + 1) * h + B - d, L) for j in (j0, j0 + 1)]
    check(all(slo < s < shi for s in roots), f'a={a}: two consecutive roots {roots[0]}, {roots[1]} in (1/2,1)')
    step = F(2 * h * (D - c), L)
    check(0 < step < h, f'a={a}: far-wall height step 2h(D-c)/(2D-c-e\') = {step} in (0,h={h})')
    corners = [((d + s * (D - c)) / h).denominator == 1 for s in roots]
    check(not all(corners), f'a={a}: corner flags {corners}; not both corners')
    for s, cf in zip(roots, corners):
        if cf:
            log(f'  INFO a={a}: s={s} hits a far-wall corner, skipped as the note allows')
            continue
        ev = shoot(Pm, S_st(a), (-1, s), T_st)
        vs = [q for kk, q in ev if kk == 'v']
        hs = [q for kk, q in ev if kk == 'h']
        lower_lat = [q for q in vs if q[1] < 5]
        roof_x = [q[0] for q in hs if q[1] == 5]
        ok = (ev[-1][0] == 'reach' and len(lower_lat) == 1 and lower_lat[0][0] == 5 - D
              and all(5 - x > R for x in roof_x))
        check(ok, f'a={a}: far-wall s={s}: reaches T, one lower lateral reflection at x=5-D, '
                  f'{len(hs)} roof/floor contacts, all roof contacts at z > R; {len(ev) - 1} reflections')
        zseam = ep + B / s
        check(0 < zseam < 1, f'a={a}: seam z = e\' + B/s = {zseam} in the mouth')
    # INFO: short-route gates at this a (not claimed by the note)
    dr = vgate(a, D, P6); fl = vgate(a + 2, D, P6)
    log(f'  INFO a={a}: direct v-gate {"none" if dr is None else dr[2]}, floor v-gate {"none" if fl is None else fl[2]}')

# ---------------------------------------------------------------- §6 constants
log('§6 explicit residual constants')
Pp = P6
bound_a = max(F(d), F(2 * d * Pp * (2 * d + 1)) / eta, F(32 * d * Pp) / (delta * eta ** 2))
log(f'  INFO st279 instance (d=1,B=1,P=6,eta=1,delta=1/2): a <= {bound_a}, D <= 4(a+d)/delta = 8(a+1)')
check(bound_a == 384, 'st279 instance of the note\'s box: a <= max{1, 36, 384} = 384')
# (1) at st279 equals cap-budget (1): (a+1)(a+3) eta^2 <= 4dPD = 24D
check(4 * d * Pp == 24, '(1) at st279: (a+1)(a+3) <= 24 D, identical to d186-reviewed cap-budget (1)')
# specialization b = B = 1, P = 2W, eta = w/b vs cap budget constants
for (dd, W, w) in ((1, 3, 1),):
    b = 1; PP = 2 * W; et = F(w, b)
    check(F(2 * dd * PP * (2 * dd + 1)) / et == F(4 * dd * W * (2 * dd + 1), w), 'b=1: 2dP(2d+1)/eta = cap 4dW(2d+1)/w')
    check(F(32 * dd * PP) / et ** 2 == F(64 * b * dd * W, w * w), 'b=1: 32dP/(delta eta^2) = cap 64bdW/(w^2 delta)')
# gcd/lcm step: g_a g_(a+2d) <= 4dPD on named points
for (a, D) in ((7, 21), (9, 27), (9, 99), (101, 303), (101, 10403)):
    ga, gb = gcd(2 * D, a * Pp), gcd(2 * D, (a + 2 * d) * Pp)
    G, Lc = gcd(ga, gb), ga * gb // gcd(ga, gb)
    check((2 * d * Pp) % G == 0 and (2 * D) % Lc == 0 and ga * gb <= 4 * d * Pp * D,
          f'(a,D)=({a},{D}): gcd(g_a,g_(a+2d))={G} | 2dP, lcm={Lc} | 2D, product {ga * gb} <= 4dPD = {4 * d * Pp * D}')
# floor-count threshold uses a < A + B
log('  INFO the a-bound uses a^2 eta^2 < (a+B)(a+2d+B) eta^2 <= 16dP(a+d)/delta <= 32dPa/delta for a >= d')

log('')
log(f'CPU seconds: {time.process_time() - T0:.2f}')
log(f'FAILURES: {len(FAIL)}')
for f_ in FAIL:
    log('  ' + f_)
