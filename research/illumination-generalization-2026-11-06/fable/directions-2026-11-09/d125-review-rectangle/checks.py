"""D125 checks: exact replays for large-rectangle-access.md and rectangle-windings.md.

Run: python3 -B checks.py > checks.log

All arithmetic is exact (fractions.Fraction). No room, ray, direction or
reflection-word search is run. Every traced direction is the matching root
that the note's construction prescribes for the named room.

Part A  opposite doors (large-rectangle-access.md), explicit H0, d = 4 doors.
Part B  perpendicular doors (rectangle-windings.md), torus winding lemma and
        the explicit rational clearance bound, d = 4 doors on all four sides.
Part C  shared-corner regime: a K = 1 winding past the far corner, checked at
        three scales, with the note's normalized c-test evaluated alongside.
"""
from fractions import Fraction as Fr
from math import ceil, floor, gcd

OK = True


def check(cond, msg):
    global OK
    print(("PASS " if cond else "FAIL ") + msg)
    if not cond:
        OK = False


# ---------------------------------------------------------------- tracer
def build_room(W, H, stubs):
    """Rectangle [0,W]x[0,H] with rectangular stubs.

    stubs: list of (side, lo, hi, depth); side in 'B','R','T','L'.
    Returns the counterclockwise vertex list of the union polygon.
    """
    by = {s: sorted([(lo, hi, dep) for (sd, lo, hi, dep) in stubs if sd == s])
          for s in 'BRTL'}
    V = [(Fr(0), Fr(0))]
    for lo, hi, dep in by['B']:
        V += [(lo, Fr(0)), (lo, -dep), (hi, -dep), (hi, Fr(0))]
    V.append((W, Fr(0)))
    for lo, hi, dep in by['R']:
        V += [(W, lo), (W + dep, lo), (W + dep, hi), (W, hi)]
    V.append((W, H))
    for lo, hi, dep in reversed(by['T']):
        V += [(hi, H), (hi, H + dep), (lo, H + dep), (lo, H)]
    V.append((Fr(0), H))
    for lo, hi, dep in reversed(by['L']):
        V += [(Fr(0), hi), (-dep, hi), (-dep, lo), (Fr(0), lo)]
    return V


def trace(V, S, T, direction, max_events=10000):
    """Exact billiard trace from S in the given direction until T is hit.

    Returns (status, events). status is 'hit', 'vertex' or 'max'.
    Hitting any polygon vertex counts as failure (conservative).
    """
    n = len(V)
    edges = [(V[i], V[(i + 1) % n]) for i in range(n)]
    vset = set(V)
    p = S
    dx, dy = direction
    events = []
    for _ in range(max_events):
        best = None
        for (a, b) in edges:
            if a[0] == b[0]:  # vertical edge
                if dx == 0:
                    continue
                t = (a[0] - p[0]) / dx
                if t <= 0:
                    continue
                y = p[1] + t * dy
                if min(a[1], b[1]) <= y <= max(a[1], b[1]):
                    if best is None or t < best[0]:
                        best = (t, 'V', (a[0], y))
            else:  # horizontal edge
                if dy == 0:
                    continue
                t = (a[1] - p[1]) / dy
                if t <= 0:
                    continue
                x = p[0] + t * dx
                if min(a[0], b[0]) <= x <= max(a[0], b[0]):
                    if best is None or t < best[0]:
                        best = (t, 'H', (x, a[1]))
        t, kind, q = best
        # does the target lie on the open segment p -> q (or at q)?
        rx, ry = T[0] - p[0], T[1] - p[1]
        if rx * dy == ry * dx:
            tt = rx / dx if dx != 0 else ry / dy
            if 0 < tt <= t:
                return 'hit', events
        if q in vset:
            events.append(('vertex', q))
            return 'vertex', events
        events.append((kind, q))
        if kind == 'V':
            dx = -dx
        else:
            dy = -dy
        p = q
    return 'max', events


def is_prime(m):
    if m < 2:
        return False
    i = 2
    while i * i <= m:
        if m % i == 0:
            return False
        i += 1
    return True


def frac_mod(x, m):
    return x - m * floor(x / m)


# ============================================================ Part A
print("=" * 70)
print("Part A. Opposite doors: large-rectangle-access.md")
print("=" * 70)
d, w, rho0 = 4, Fr(2), Fr(1)
I_lo, I_hi = Fr(1, 4), Fr(3, 4)
delta = I_hi - I_lo
Bc = max(64, ceil(Fr(32) / (rho0 * delta)))
k0 = 4 * d + 8
P = 2 ** k0 * Bc
Q = 32 * P
H0 = 8 * w * P * Q ** d
print(f"d={d} w={w} rho0={rho0} I=[{I_lo},{I_hi}] delta={delta}")
print(f"B={Bc} k0={k0} P=2^{P.bit_length()-1} Q=2^{Q.bit_length()-1} "
      f"H0=2^{int(H0).bit_length()-1} (exact {H0 == 2**174})")

primes = []
for i in range(k0):
    m = 2 ** i * Bc + 1
    while not is_prime(m):
        m += 1
    assert m < 2 ** (i + 1) * Bc
    primes.append(m)
prod = 1
for q_ in primes:
    prod *= q_
check(all(q_ % 2 == 1 and q_ <= P for q_ in primes), "Bertrand primes odd and <= P")
check(prod > Q ** d, f"product of the {k0} primes exceeds Q^d")
check(prod > Bc ** k0 * 2 ** (k0 * (k0 - 1) // 2) > 0 and
      Q ** d == Bc ** d * 2 ** ((k0 + 5) * d), "product bound and Q^d identity as stated")

# Named room.  H = W = 7 * 2^172 >= H0 = 2^174.
H = 7 * 2 ** 172
W = H
rho = Fr(W, H)
check(H >= H0 and rho >= rho0, "H >= H0 and W/H >= rho0")
# Doors (lattice endpoints, width 2): left L1 (entry), L2; right R1 (exit), R2.
doors = {
    'L1': ('L', Fr(2 * H, 7)), 'L2': ('L', Fr(4 * H, 7)),
    'R1': ('R', Fr(5 * H, 7)), 'R2': ('R', Fr(6 * H, 7)),
}
for nm, (sd, lo) in doors.items():
    print(f"  door {nm}: side {sd}, y in [{lo * 7 / H}H/7, {lo * 7 / H}H/7 + 2], "
          f"center/H = {lo * 7 / H}/7 + 1/H")
stubs = [(sd, lo, lo + 2, Fr(2)) for (sd, lo) in doors.values()]
V = build_room(Fr(W), Fr(H), stubs)
print(f"  room polygon has {len(V)} vertices; marks are lattice points")
S = (Fr(-1), Fr(2 * H, 7) + 1)          # in L1's stub, depth 1
T = (Fr(W + 1), Fr(5 * H, 7) + 1)       # in R1's stub, depth 1

# Simultaneous approximation.  The proof needs only D <= Q^d and
# |c_i - C_i/D| <= 1/(QD); the pigeonhole merely guarantees one exists.
centers = {nm: (lo + 1) / H for nm, (sd, lo) in doors.items()}
D = 7
C = {nm: round(c * D) for nm, c in centers.items()}
check(1 <= D <= Q ** d, "1 <= D <= Q^d")
check(all(abs(centers[nm] - Fr(C[nm], D)) <= Fr(1, Q * D) for nm in centers),
      "|c_i - C_i/D| <= 1/(QD) for all four centers")
p = next(q_ for q_ in primes if D % q_ != 0)
print(f"  D={D}, C={C}, p={p}")

# Signs: entry upward at L1, forward exit upward at R1.
a_c, b_c = centers['L1'], centers['R1']
A_, B1 = C['L1'], C['R1']
q = p


def a_of(s):  # normalized entry height: S at depth 1, slope s upward
    return (S[1] + s) / H


def b_of(s):  # normalized exit height: forward arrives up-right, T at depth 1
    return (T[1] - s) / H


check(all(abs(a_of(s) - a_c) <= w / (2 * H) and abs(b_of(s) - b_c) <= w / (2 * H)
          for s in (I_lo, I_hi)), "access heights within w/(2H) of centers on I")

# choose k: nominal slope in the middle half of I, B1-A+2kD != 0 mod p.
mid_lo, mid_hi = I_lo + delta / 4, I_hi - delta / 4
k_lo = ceil((q * rho * mid_lo - (b_c - a_c)) / 2)
k_hi = floor((q * rho * mid_hi - (b_c - a_c)) / 2)
check(k_hi - k_lo + 1 >= 2, f"middle half holds >= 2 consecutive k ({k_lo}..{k_hi})")
k = next(kk for kk in (k_lo, k_lo + 1) if (B1 - A_ + 2 * kk * D) % p != 0)
print(f"  k={k}, residue (B1-A+2kD) mod p = {(B1 - A_ + 2 * k * D) % p}")


def f_mis(s):
    return q * rho * s + a_of(s) - b_of(s) - 2 * k


check(f_mis(I_lo) < 0 < f_mis(I_hi), "IVT: mismatch changes sign on I")
check(min(-f_mis(I_lo), f_mis(I_hi)) >= q * rho * delta / 4 - w / H,
      "endpoint mismatch >= q rho delta/4 - w/H")
# a, b are affine in s, so the IVT root is explicit:
s = (2 * k + Fr(T[1] - S[1], H)) / (q * rho + Fr(2, H))
check(f_mis(s) == 0 and I_lo < s < I_hi, f"matching root s = {float(s):.12f} in I")

# predicted crossings and the modular clearance
grid_d = Fr(1, p * D)
bound = Fr(1, p * D) - w / H - Fr(2, Q * D)
check(w / H + Fr(2, Q * D) < Fr(1, 2 * p * D), "w/H + 2/(QD) < 1/(2pD)")
minclear = None
for j in range(1, q):
    Yj = (1 - Fr(j, q)) * Fr(A_, D) + Fr(j, q) * Fr(B1, D) + Fr(2 * j * k, q)
    yj = (1 - Fr(j, q)) * a_of(s) + Fr(j, q) * b_of(s) + Fr(2 * j * k, q)
    distY = min(abs(Yj * D - round(Yj * D)), Fr(1)) / D
    assert distY >= grid_d, (j, distY)
    # physical height and side of the j-th crossing
    ym = frac_mod(yj, 2)
    yphys = ym if ym <= 1 else 2 - ym
    side = 'R' if j % 2 == 1 else 'L'
    # clearance to corners and door edges on that side (normalized)
    cl = min(yphys, 1 - yphys)
    for nm, (sd, lo) in doors.items():
        if sd == side:
            lo_n, hi_n = lo / H, (lo + 2) / H
            if lo_n <= yphys <= hi_n:
                cl = Fr(-1)
            else:
                cl = min(cl, abs(yphys - lo_n), abs(yphys - hi_n))
    minclear = cl if minclear is None else min(minclear, cl)
check(True, f"dist(Y_j,(1/D)Z) >= 1/(pD) for all 0<j<{q}")
check(minclear > 0 and minclear >= bound,
      f"every intermediate crossing misses doors and corners; min clearance "
      f"{float(minclear):.6f} >= proof bound {float(bound):.6f}")

status, ev = trace(V, S, T, (Fr(1), s))
nV = sum(1 for e in ev if e[0] == 'V')
nH = sum(1 for e in ev if e[0] == 'H')
check(status == 'hit', f"exact physical trace from S reaches T ({nV} vertical, "
      f"{nH} horizontal reflections)")
check(nV == q - 1, "vertical reflections = p - 1 as the proof prescribes")
# compare traced vertical hit heights with predicted y_j
vh = [e[1][1] for e in ev if e[0] == 'V']
pred = []
for j in range(1, q):
    yj = (1 - Fr(j, q)) * a_of(s) + Fr(j, q) * b_of(s) + Fr(2 * j * k, q)
    ym = frac_mod(yj, 2)
    pred.append((ym if ym <= 1 else 2 - ym) * H)
check(vh == pred, "traced vertical-contact heights equal the predicted y_j exactly")

# Tracer control: move L2 so that its door contains the 2nd crossing.
y2 = pred[1]
lo2 = floor(y2) - 0  # lattice door [floor(y2), floor(y2)+2] contains y2
doors_c = dict(doors)
doors_c['L2'] = ('L', Fr(lo2))
Vc = build_room(Fr(W), Fr(H), [(sd, lo, lo + 2, Fr(2)) for (sd, lo) in doors_c.values()])
st_c, ev_c = trace(Vc, S, T, (Fr(1), s), max_events=400)
first_out = next((i for i, e in enumerate(ev_c) if e[1][0] < 0), None)
check(st_c != 'hit' and first_out is not None,
      f"control: door moved onto crossing 2 -> path enters the L2 stub at event "
      f"{first_out} and never reaches T (status {st_c})")

# ============================================================ Part B
print()
print("=" * 70)
print("Part B. Perpendicular doors: rectangle-windings.md")
print("=" * 70)
# Normalized layout (W = H, rho = 1): left entry a = 1/6, top exit b = 1/6,
# extra doors: bottom at x = 2/3, right at y = 1/2.  Common denominator 6.
den = 6
a_n, b_n = Fr(1, 6), Fr(1, 6)
xbot, yright = Fr(2, 3), Fr(1, 2)
wB = Fr(2)
IB_lo, IB_hi = Fr(3, 4), Fr(5, 4)
rhoB = Fr(1)
A2 = (Fr(0), a_n)          # entry upward -> +a
B2 = (b_n, Fr(1))          # exit rightward -> +b, last coord same side as a
# Forbidden set on R^2 / 2Z^2: corners + reflected door centers.
Fset = [(Fr(0), Fr(0)), (Fr(1), Fr(0)), (Fr(0), Fr(1)), (Fr(1), Fr(1)),
        (Fr(0), a_n), (Fr(0), 2 - a_n),
        (b_n, Fr(1)), (2 - b_n, Fr(1)),
        (xbot, Fr(0)), (2 - xbot, Fr(0)),
        (Fr(1), yright), (Fr(1), 2 - yright)]
# Halve to the unit torus.
Ah = (A2[0] / 2, A2[1] / 2)
dh = ((B2[0] - A2[0]) / 2, (B2[1] - A2[1]) / 2)
Fh = [(x / 2, y / 2) for (x, y) in Fset]
v = (1, 1)                 # slope 1, inside the middle half [7/8, 9/8]
u = (1, 0)                 # u(v) = 1


def det(p1, p2):
    return p1[0] * p2[1] - p1[1] * p2[0]


dv = det(v, dh)
check(dv != 0, f"det(v,d) = {dv} != 0")
Nb = len(Fh) * (1 + ceil(abs(dv)))
print(f"  |F| = {len(Fh)}, N = {Nb}")
print(f"  layout: left a={a_n}, top b={b_n}, bottom x={xbot}, right y={yright}; v={v}")
# direct chord clear (folds into the open rectangle)
check(all(not (0 < x < 1 and 0 < y < 1) for (x, y) in Fset),
      "no frozen center lies in the open rectangle, so the direct chord is clear")

congr = []  # (t, c): collision iff K t = c (mod 1)
for f in Fh:
    g = frac_mod(det(v, (f[0] - Ah[0], f[1] - Ah[1])), 1)
    # t * dv = g + n, 0 < t < 1
    for nn in range(int(min(0, floor(dv - g))) - 1, int(max(0, ceil(dv - g))) + 2):
        t = (g + nn) / dv
        if 0 < t < 1:
            c = u[0] * (f[0] - Ah[0] - t * dh[0]) + u[1] * (f[1] - Ah[1] - t * dh[1])
            congr.append((t, frac_mod(c, 1)))
check(len(congr) <= Nb, f"{len(congr)} collision congruences <= N")
check(all(c != 0 for (t, c) in congr), "K = 0 violates none (original chord clear)")
for (t, c) in congr:
    print(f"    congruence K*{t} = {c} (mod 1)")
h = 1
changed = True
while changed:
    changed = False
    for (t, c) in congr:
        bden = t.denominator
        qq = bden // gcd(bden, h)
        if 1 < qq <= 2 * Nb + 1:
            h *= qq
            changed = True
check(h <= (2 * Nb + 1) ** Nb, f"h = {h} <= (2N+1)^N")


def slope_ok(K):
    Dx = B2[0] - A2[0] + 2 * K * v[0]
    Dy = B2[1] - A2[1] + 2 * K * v[1]
    tau = Dy / Dx
    return Dx >= 1 and Dy >= 1 and IB_lo + (IB_hi - IB_lo) / 4 <= tau <= IB_hi - (IB_hi - IB_lo) / 4


K0 = 1
while not slope_ok(K0):
    K0 += 1
# monotone: slope tends to 1 from above as K grows
check(all(slope_ok(K0 + i) for i in range(50)), f"K0 = {K0}; slope in middle half beyond K0")
m0 = -(-K0 // h)
survivors = [m * h for m in range(m0, m0 + Nb + 1)
             if all(frac_mod(m * h * t - c, 1) != 0 for (t, c) in congr)]
check(len(survivors) >= 1, f"some K among the N+1 multiples survives "
      f"({len(survivors)} of {Nb + 1})")
K = survivors[0]


def hits_F_direct(KK):
    """Does the open developed segment A2 -> B2 + 2KK v pass through F mod 2Z^2?"""
    ex, ey = B2[0] - A2[0] + 2 * KK * v[0], B2[1] - A2[1] + 2 * KK * v[1]
    for (fx, fy) in Fset:
        # A2 + t(ex,ey) = (fx + 2i, fy + 2j), 0<t<1: scan the finitely many t with
        # x-coordinate congruent to fx mod 2.
        for i in range(floor((A2[0] - fx) / 2) - 1, ceil((A2[0] + ex - fx) / 2) + 2):
            t = (fx + 2 * i - A2[0]) / ex
            if 0 < t < 1 and frac_mod(A2[1] + t * ey - fy, 2) == 0:
                return True
    return False


pred_bad = [KK for KK in range(0, K0 + Nb + 1)
            if any(frac_mod(KK * t - c, 1) == 0 for (t, c) in congr)]
dir_bad = [KK for KK in range(0, K0 + Nb + 1) if hits_F_direct(KK)]
check(pred_bad == dir_bad, f"congruence prediction matches direct incidence for "
      f"K = 0..{K0 + Nb} (blocked: {dir_bad})")
check(K <= K0 + (Nb + 1) * h, f"K = {K} within K0 + (N+1)h")
Dx = B2[0] - A2[0] + 2 * K * v[0]
Dy = B2[1] - A2[1] + 2 * K * v[1]
tau = Dy / Dx
print(f"  developed displacement D = ({Dx}, {Dy}), tau = {tau}")


def fold(z):
    zm = frac_mod(z, 2)
    return zm if zm <= 1 else 2 - zm


crossings = []  # (wall, along-wall coord)
for nn in range(1, ceil(Dx)):
    y = A2[1] + tau * nn
    crossings.append(('R' if nn % 2 else 'L', fold(y)))
for mm in range(1, int(Dy + A2[1])):
    if Fr(mm) <= A2[1]:
        continue
    x = A2[0] + (mm - A2[1]) / tau
    crossings.append(('T' if mm % 2 else 'B', fold(x)))
forb = {'L': [a_n], 'R': [yright], 'T': [b_n], 'B': [xbot]}
c_min = Fr(1)
for wall, z in crossings:
    for f in [Fr(0), Fr(1)] + forb[wall]:
        c_min = min(c_min, abs(z - f))
check(c_min > 0, f"{len(crossings)} intermediate crossings clear of frozen centers "
      f"and corners; c = {c_min}")
c_lb = Fr(1, den ** 2 * max(1, Dx, Dy))
check(c_min >= c_lb, f"explicit rational bound c >= 1/(d^2 max(1,Dx,Dy)) = {c_lb}")
eta = min(a_n, 1 - a_n, b_n, 1 - b_n)
lo_r, hi_r = rhoB * IB_lo, rhoB * IB_hi
mu = min(tau - lo_r, hi_r - tau)
tmax = hi_r
mx = max(tau, 1 / tau)


def estar(cv):
    return min(eta / 2, Dx / 2, Dy / 2, mu * Dx / (2 * (1 + tmax)), cv / (2 + 2 * mx))


e_true, e_lb = estar(c_min), estar(c_lb)
HB_true = wB / (2 * e_true)
HB_lb = wB / (2 * e_lb)
print(f"  e* (actual c) = {e_true}, threshold H > {float(HB_true):.3f}")
print(f"  e* (rational lower bound) = {e_lb}, threshold H > {float(HB_lb):.3f}")
HB = den * (floor(HB_lb / den) + 1)
check(Fr(HB) > HB_lb and HB % den == 0, f"chosen H = W = {HB}")
WB = HB
eB = wB / (2 * min(WB, HB))
check(eB < e_lb, "e = w/(2 min(W,H)) below the explicit margin")
# Named room: designated doors left [H/6-1,H/6+1], top [H/6-1,H/6+1]; extra
# bottom [2H/3-1, 2H/3+1], right [H/2-1, H/2+1].  Stub depth 1.
stB = [('L', Fr(HB, 6) - 1, Fr(HB, 6) + 1, Fr(1)),
       ('T', Fr(HB, 6) - 1, Fr(HB, 6) + 1, Fr(1)),
       ('B', Fr(2 * HB, 3) - 1, Fr(2 * HB, 3) + 1, Fr(1)),
       ('R', Fr(HB, 2) - 1, Fr(HB, 2) + 1, Fr(1))]
VB = build_room(Fr(WB), Fr(HB), stB)
SB = (Fr(-1, 2), Fr(HB, 6))          # entry height H/6 + s/2
TB = (Fr(HB, 6), Fr(HB) + Fr(1, 2))  # exit abscissa H/6 - 1/(2s)


def mismatchB(s_):
    ax = (SB[1] + s_ / 2) / HB
    bx = (TB[0] - 1 / (2 * s_)) / WB
    Dx_ = bx + 2 * K * v[0]
    Dy_ = 1 - ax + 2 * K * v[1]
    return rhoB * s_ * Dx_ - Dy_


check(mismatchB(IB_lo) < 0 < mismatchB(IB_hi), "endpoint mismatch has opposite signs on I")
# rho s Dx(s) = Dy(s) is affine in s after multiplying out:
num = (1 + 2 * K) - SB[1] / HB + Fr(1, 2 * WB)
den_s = rhoB * (TB[0] / WB + 2 * K) + Fr(1, 2 * HB)
sB = num / den_s
check(mismatchB(sB) == 0 and IB_lo < sB < IB_hi, f"matching root s = {sB}")
stat, evB = trace(VB, SB, TB, (Fr(1), sB))
check(stat == 'hit', f"exact physical trace reaches T ({len(evB)} reflections)")
check(len(evB) == len(crossings), "reflection count equals predicted crossing count")

# ============================================================ Part C
print()
print("=" * 70)
print("Part C. Shared corner: doors at fixed physical offsets 2 from (0,H)")
print("=" * 70)
for Hc in (1000, 10 ** 9, 2 ** 200):
    Wc = Fr(3 * Hc, 2)
    Hc = Fr(Hc)
    stC = [('L', Hc - 3, Hc - 1, Fr(1)), ('T', Fr(1), Fr(3), Fr(1))]
    VC = build_room(Wc, Hc, stC)
    SC = (Fr(-1, 2), Hc - 2)        # downward entry: A(s) = 2 + s/2 below corner
    TC = (Fr(2), Hc + Fr(1, 2))     # leftward exit: B(s) = 2 + 1/(2s)
    # K = 1, v = (1,1), entry sheet -a, exit sheet -b: physical displacement
    # (2W - B(s), 2H - A(s)) at slope s.
    sC = (2 * Hc - Fr(3, 2)) / (2 * Wc - Fr(3, 2))
    As, Bs = 2 + sC / 2, 2 + 1 / (2 * sC)
    check(sC * (2 * Wc - Bs) == 2 * Hc - As and Fr(1, 2) < sC < 2,
          f"H={Hc if Hc < 10**10 else '2^200'}: root s={float(sC):.9f} in access range (1/2,2)")
    stat, evC = trace(VC, SC, TC, (Fr(1), -sC))
    hits = [(e[0], e[1]) for e in evC]
    miss_bottom = Wc - hits[0][1][0] if stat == 'hit' else None
    check(stat == 'hit', f"  trace reaches T; contacts: "
          f"bottom at {float(miss_bottom):.6f} left of corner (W,0), "
          f"right wall at height {float(hits[1][1][1]):.6f}")
    check(miss_bottom == 5 * (1 + sC) / (4 * sC), "  bottom miss = 5(1+s)/(4s) exactly")
    # normalized c-test of the note for this path (one far-corner crossing)
    tauC = (2 * Hc - As) / Hc / ((2 * Wc - Bs) / Wc)
    c_norm = miss_bottom / Wc
    eC = Fr(2) / (2 * min(Wc, Hc))
    lhs = c_norm / (2 + 2 * max(tauC, 1 / tauC))
    print(f"  note's c-test: c/(2+2max) = {float(lhs * Hc):.4f}/H vs e = "
          f"{float(eC * Hc):.4f}/H -> {'passes' if eC < lhs else 'fails'}")

print()
print("ALL PASS" if OK else "SOME CHECKS FAILED")
