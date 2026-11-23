"""d184 review checks for l1-gap-hyperplanes.md (snapshot 1952).

Named room DBas only (d110 geom.ROOMS), with insertions at hand-chosen cross-sections of DBas.
Exact Fraction arithmetic. trace() is copied verbatim from d182-review-growthmodes/checks.py.
Every traced velocity is either (a) the note's own formula slope, or (b) an endpoint slope of the
named seed word (the note's finite "exact fixed-word test"), traced at one named point to validate
the gate list derived by hand. No room, ray, direction or word search is run.
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


# ------------------------------------------------------------------ copied verbatim from d182/d181/d175
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


def fr(p):
    return '(' + ','.join(str(c) for c in p) + ')'


# ------------------------------------------------------------------ d110 geom (copied)
def dumbbell(d1, b1, h1, d2, b2, h2, p, w, L):
    assert b1 < p and p + w < b1 + h1 and b2 < p and p + w < b2 + h2
    x2 = d1 + L
    return [(0, b1), (d1, b1), (d1, p), (x2, p), (x2, b2), (x2 + d2, b2), (x2 + d2, b2 + h2),
            (x2, b2 + h2), (x2, p + w), (d1, p + w), (d1, b1 + h1), (0, b1 + h1)]


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


def nearest(q):
    return floor(q + F(1, 2))


# Two-parameter DBas family: t1 into the left box x-gap (cut c1 = 3 + 1/4, height 4, P1 = 8),
# t2 into the corridor x-gap (cut c2 = 6 + 1/4, height 1, P2 = 2). Seed (1,3) -> (11,3), velocity (7,-2).
def room2(t1, t2):
    return dumbbell(5 + t1, 0, 4, 4, -1, 6, 1, 1, 4 + t2)


S = (1, 3)
tgt2 = lambda t1, t2: (11 + t1 + t2, 3)
C1, C2 = F(13, 4), F(25, 4)
s0, X, Y, p, q = F(2, 7), 14, 4, 2, 7


def outside_pattern(con, t1, t2):
    """contacts outside the two inserted strips [c1, c1+t1] and [c2+t1, c2+t1+t2]"""
    out = []
    for (x, y), k in con:
        if C1 <= x <= C1 + t1 and y in (0, 4):
            continue
        if C2 + t1 <= x <= C2 + t1 + t2 and y in (1, 2):
            continue
        xr = x - t1 - t2 if x > C2 + t1 else (x - t1 if x > C1 else x)
        out.append((k, y if k == 'h' else xr))
    return out


BASE_PATTERN = [('h', 1), ('v', 13)]

# ================================================================== 0. base seed
log("# 0. Base seed on DBas (L=4): (1,3) -> (11,3), velocity (7,-2), X=14, Y=4, s0=2/7")
ev, end, con = trace(room2(0, 0), S, (1 + 14, 3 - 4))
check(ev == 'end' and end == (11, 3) and [c for c, _ in con] == [(8, 1), (13, F(17, 7))] and outside_pattern(con, 0, 0) == BASE_PATTERN, f"base: {ev} at {fr(end)}, contacts {[(fr(c), k) for c, k in con]}")

# ================================================================== 1. lattice threshold
log("\n# 1. Lattice threshold t > XPq - X/M (margin 1/(2q)) and t > XP/(2mu) - X/M")
for c in (C1, C2, F(49, 4)):
    yc = 3 - s0 * (c - 1) if c < 13 else None
    if c == F(49, 4):   # right-box cut 12+1/4, crossed twice (out at height 1+(c-8)*s0, back at 17/7+(13-c)*s0)
        ys = [1 + (c - 8) * s0, F(17, 7) + (13 - c) * s0]
    else:
        ys = [yc]
    odd = all((y * 2 * q).denominator == 1 and int(y * 2 * q) % 2 == 1 for y in ys)
    check(odd, f"cut x={c} (= integer + 1/(2p), p=2): crossing heights {ys} are odd multiples of 1/(2q)=1/14")
# all vertex abscissas are integers, so the seed's heights there are multiples of 1/q
check(all((s0 * (x - 1)).denominator in (1, 7) for x in range(0, 14)), "seed heights at integer abscissas are multiples of 1/7")
# measured margin of the seed's gates (mouth (5,2): 1/7; right mouth 9: 2/7; cut c2: 1/2; cap: large)
mu = min(F(1, 7), F(2, 7), F(1, 2))
check(mu >= F(1, 2 * q), f"measured mu = {mu} >= 1/(2q) = {F(1, 2*q)}")


def thr(X, M, P, mu):
    return F(X * P, 2) / mu - F(X, M)


check(thr(14, 1, 2, F(1, 7)) == 84 and thr(14, 1, 2, F(1, 14)) == 182, "named control: t > 84 (mu=1/7), t > 182 (q only)")


def predict(s0, X, M, P, t):
    k = nearest(F(t) * s0 / P)
    s = (X * s0 + M * k * P) / (X + M * t)
    return k, s


for t in (183, 185, 200, 500):
    k, s = predict(s0, 14, 1, 2, t)
    ev, end, con = trace(room2(0, t), S, (1 + 14 + t, 3 - s * (14 + t)))
    ok = ev == 'end' and end == tgt2(0, t) and outside_pattern(con, 0, t) == BASE_PATTERN
    check(ok, f"corridor ray t={t} (> 182): s={s}; {ev} at {fr(end)}; base pattern kept {outside_pattern(con,0,t)==BASE_PATTERN}")
# two cuts on one ray (d182 case D1): corridor weight 1, right box weight 1 crossed twice: X=14, M=3, P=12
T1 = thr(14, 3, 12, F(1, 14))
log(f"   d182 D1 ray (corridor + right box, M=3, P=12): lattice threshold t > {T1} ~ {float(T1):.1f}")
for t in (1172, 1500):
    k, s = predict(s0, 14, 3, 12, t)
    P_ = dumbbell(5, 0, 4, 4 + t, -1, 6, 1, 1, 4 + t)
    ev, end, con = trace(P_, S, (1 + 14 + 3 * t, 3 - s * (14 + 3 * t)))
    check(ev == 'end' and end == (11 + t, 3), f"D1 ray t={t}: s={s}; {ev} at {fr(end)}; {len(con)} contacts")

# ================================================================== 2. exact two-gap test
log("\n# 2. Exact fixed-word test for (t1, t2) = (left box, corridor), cuts c1=13/4, c2=25/4")
log("   Drop D(x) = 3 - y in the positive development. Seed word gates (retained x):")
log("   cut c1: D in (-1,3) both banks; mouth x=5: 4s+e1 in (1,2); cut c2: 21s/4+e1 in (1,2) and +e2 in (1,2);")
log("   right mouth x=9: 8s+e1+e2 in (2,3); cap x=13 in (0,6); endpoint 14s+e1+e2 = 4.")
log("   With e1 = t1 s - 8k1, e2 = t2 s - 2k2 the endpoint gives s = (4+8k1+2k2)/N, N = 14+t1+t2.")
log("   Eliminating e2: chart test  <=> exists even m, s=m/N in (8/35,1/3), t1 s mod 8 in (1-4s, 2-21s/4).")
log("   Word test (cut-c2 sheet dropped) <=> s in (1/6,1/3), t1 s mod 8 in (1-4s, 2-4s).")

CH = dict(lo=F(8, 35), hi=F(1, 3), u=F(21, 4))   # chart: upper window 2 - (21/4) s
WD = dict(lo=F(1, 6), hi=F(1, 3), u=F(4))       # word


def feasible(t1, t2, T=CH):
    N = 14 + t1 + t2
    out = []
    for m in range(ceil(T['lo'] * N), floor(T['hi'] * N) + 1):
        if m % 2:
            continue
        s = F(m, N)
        if not (T['lo'] < s < T['hi']):
            continue
        lo_w, hi_w = 1 - 4 * s, 2 - T['u'] * s
        v = t1 * s
        k1 = ceil((v - hi_w) / 8)
        e1 = v - 8 * k1
        if lo_w < e1 < hi_w:
            out.append((m, k1, (m - 4 - 8 * k1) // 2))
    return out


def gates_hold(t1, t2, m, k1):
    """the hand-derived chart gates, evaluated directly"""
    N = 14 + t1 + t2
    s = F(m, N)
    k2 = F(m - 4 - 8 * k1, 2)
    e1, e2 = t1 * s - 8 * k1, t2 * s - 2 * k2
    g = [-1 < s * (C1 - 1) < 3, -1 < s * (C1 - 1) + e1 < 3, 1 < 4 * s + e1 < 2,
         1 < (C2 - 1) * s + e1 < 2, 1 < (C2 - 1) * s + e1 + e2 < 2, 2 < 8 * s + e1 + e2 < 3,
         0 < 12 * s + e1 + e2 < 6, 14 * s + e1 + e2 == 4]
    return all(g)


def bank_signature(con, end, t1, t2):
    """(bank, horizontal sign, vertical sign) at every crossing of the four cut banks, in order"""
    banks = [('c1', C1), ("c1'", C1 + t1), ('c2', C2 + t1), ("c2'", C2 + t1 + t2)]
    pts = [(F(S[0]), F(S[1]))] + [c for c, _ in con] + [end]
    sig = []
    for a, b in zip(pts, pts[1:]):
        dx, dy = b[0] - a[0], b[1] - a[1]
        hits = [(abs(c - a[0]), nm) for nm, c in banks if min(a[0], b[0]) < c < max(a[0], b[0])]
        for _, nm in sorted(hits):
            sig.append((nm, 1 if dx > 0 else -1, 1 if dy > 0 else -1))
    return sig


BASE_SIG = [('c1', 1, -1), ("c1'", 1, -1), ('c2', 1, -1), ("c2'", 1, -1)]


def trace2(t1, t2, m):
    N = 14 + t1 + t2
    ev, end, con = trace(room2(t1, t2), S, (1 + N, 3 - m))
    reach = ev == 'end' and end == tgt2(t1, t2)
    same = reach and outside_pattern(con, t1, t2) == BASE_PATTERN and bank_signature(con, end, t1, t2) == BASE_SIG
    return reach, same, ev, end, len(con)


# 2a. validate the hand-derived gates: at one named point trace every endpoint slope of the seed word
for (t1, t2) in ((37, 61), (45, 40), (120, 133)):
    N = 14 + t1 + t2
    ms = [m for m in range(ceil(F(1, 6) * N), floor(F(1, 3) * N) + 1) if m % 2 == 0 and F(1, 6) < F(m, N) < F(1, 3)]
    chart = {m for m, _, _ in feasible(t1, t2, CH)}
    word = {m for m, _, _ in feasible(t1, t2, WD)}
    agree = True
    rows = []
    for m in ms:
        reach, same, ev, end, nc = trace2(t1, t2, m)
        rows.append((m, reach, same))
        if same != (m in chart):
            agree = False
            log(f"   mismatch m={m}: reach {reach}, seed chart itinerary {same}, chart-test {m in chart}")
    log(f"   ({t1},{t2}): N={N}; {len(ms)} endpoint slopes of the word in (1/6,1/3); chart-feasible m {sorted(chart)}; "
        f"word-feasible m {sorted(word)}; traced: reach target {[m for m, r, _ in rows if r]}, "
        f"with the seed's contacts and cut-bank sheets {[m for m, _, sm in rows if sm]}")
    check(agree, f"({t1},{t2}): traced 'seed chart itinerary' (outside contacts + sheets at all 4 banks) "
          f"agrees with the chart test on all {len(ms)} slopes")
    check(all(gates_hold(t1, t2, m, k1) for m, k1, _ in feasible(t1, t2, CH)), f"({t1},{t2}): direct gate evaluation agrees")

# 2b. line criterion. Line beta*t1 - alpha*t2 = a in direction (alpha, beta), g = alpha+beta.
# Exactly t1 s = 2 alpha j/g - kappa s (m = 2j), kappa = (14 alpha - a)/g, residues in Delta Z, Delta = gcd(2alpha,8g)/g.
def phi(alpha, beta, a, T=CH):
    g = alpha + beta
    kap = F(14 * alpha - a, g)
    Dl = F(gcd(2 * alpha, 8 * g), g)
    lo, hi = T['lo'], T['hi']
    L = lambda s: 1 + (kap - 4) * s
    U = lambda s: 2 + (kap - T['u']) * s
    rmin, rmax = min(L(lo), L(hi)), max(U(lo), U(hi))
    for r in range(ceil(rmin / Dl), floor(rmax / Dl) + 1):
        rho = r * Dl
        a_, b_ = lo, hi                      # solve L(s) < rho < U(s) on (lo, hi)
        for c0, c1, sgn in ((1, kap - 4, 1), (2, kap - T['u'], -1)):
            # sgn=1: c0 + c1 s < rho ; sgn=-1: c0 + c1 s > rho
            if c1 == 0:
                if (sgn == 1 and not c0 < rho) or (sgn == -1 and not c0 > rho):
                    a_, b_ = 1, 0
                continue
            x = (rho - c0) / c1
            if (c1 > 0) == (sgn == 1):
                b_ = min(b_, x)
            else:
                a_ = max(a_, x)
        if a_ < b_:
            return True, rho, (a_, b_)
    return False, None, None


def exceptional_lines(T, wmin, name):
    log(f"\n   Exceptional lines of this seed ({name}). Directions with Delta < {wmin} never fail (window >= {wmin}).")
    dirs = []
    for g in range(1, 14):
        for alpha in range(0, g + 1):
            beta = g - alpha
            if gcd(alpha, beta) != 1:
                continue
            Dl = F(gcd(2 * alpha, 8 * g), g)
            if Dl >= wmin:
                dirs.append((alpha, beta, Dl))
    exc, tot = {}, 0
    for alpha, beta, Dl in dirs:
        g = alpha + beta
        # union length >= |kappa - 4|(hi-lo) must be <= Delta <= 8 for failure; scan that range of a exactly
        kmax = 4 + F(8) / (T['hi'] - T['lo']) + 1
        alo, ahi = floor(14 * alpha - g * kmax), ceil(14 * alpha + g * kmax)
        bad = [a for a in range(alo, ahi + 1) if not phi(alpha, beta, a, T)[0]]
        if alpha == 0:
            bad = [a for a in bad if a >= 0]          # line t1 = a
        if beta == 0:
            bad = [a for a in bad if a <= 0]          # line t2 = -a
        exc[(alpha, beta)] = bad
        tot += len(bad)
        log(f"   direction ({alpha},{beta}), Delta={Dl}: failing a in [{alo},{ahi}]: {bad}")
    log(f"   total {tot} exceptional lines. (line: beta*t1 - alpha*t2 = a; (0,1): t1=a; (1,0): t2=-a; (1,1): t2=t1-a)")
    return exc


EXC = exceptional_lines(CH, F(5, 7), "chart test, cuts at 13/4 and 25/4")
EXCW = exceptional_lines(WD, F(1), "word test, cut sheets dropped")


def on_exc(t1, t2):
    return [(al, be, be * t1 - al * t2) for (al, be), bad in EXC.items() if be * t1 - al * t2 in bad]


# 2c. named points
NOTE_P = 8


def note_slope(t1, t2, u=s0):
    K1, K2 = NOTE_P * nearest(t1 * u / NOTE_P), NOTE_P * nearest(t2 * u / NOTE_P)
    return F(Y + K1 + K2, X + t1 + t2), K1, K2


named = [('(1,1) a=5: t2=t1-5', 500, 495), ('(1,1) a=5', 1000, 995), ('(1,1) a=4', 1000, 996),
         ('t1=10', 10, 500), ('t1=10', 10, 1001),
         ('d182 offset c=1', 500, 501), ('d182 offset c=1', 1000, 1001), ('d182 offset c=7', 1000, 1007),
         ('offset c=-1', 2000, 1999), ('generic', 777, 1234), ('generic', 1500, 400), ('generic', 1234, 2345)]
for alpha, beta in ((2, 1), (4, 1)):
    if EXC.get((alpha, beta)):
        a = EXC[(alpha, beta)][len(EXC[(alpha, beta)]) // 2]
        # integer point beta*t1 - alpha*t2 = a with t2 ~ 400
        for t2 in range(400, 400 + beta + alpha + 1):
            if (a + alpha * t2) % beta == 0:
                named.append((f'({alpha},{beta}) a={a}', (a + alpha * t2) // beta, t2))
                break
log("")
for label, t1, t2 in named:
    exc = on_exc(t1, t2)
    fe = feasible(t1, t2, CH)
    fw = feasible(t1, t2, WD)
    pred_fail = bool(exc)
    sn, K1, K2 = note_slope(t1, t2)
    rn, sn_same, ev, end, nc = trace2(t1, t2, sn * (14 + t1 + t2))
    msg = f"{label} ({t1},{t2}): on exceptional lines {exc}; chart-feasible slopes {len(fe)}, word-feasible {len(fw)}; "
    if fe:
        m, k1, k2 = min(fe, key=lambda r: abs(F(r[0], 14 + t1 + t2) - s0))
        reach, same, ev2, end2, nc2 = trace2(t1, t2, m)
        c8 = [r for r in fe if r[0] % 8 == 4]
        msg += (f"trace of s={F(m, 14+t1+t2)} (k1={k1},k2={k2}): reach {reach}, seed itinerary {same}, {nc2} contacts; "
                f"common-P=8 slopes (m = 4 mod 8) {len(c8)}; ")
        ok = (not pred_fail) and reach and same
    else:
        ok = pred_fail
    msg += f"note slope at u=s0 (K={K1},{K2}) s={sn}: {ev} at {fr(end)}, seed pattern {sn_same}"
    check(ok, msg)

# 2d. on a chart-exceptional line the word test can still succeed: trace one word slope
t1, t2 = 1000, 995
fw = feasible(t1, t2, WD)
m = min(fw, key=lambda r: abs(F(r[0], 14 + t1 + t2) - s0))[0]
ev, end, con = trace(room2(t1, t2), S, (1 + 14 + t1 + t2, 3 - m))
check(ev == 'end' and end == tgt2(t1, t2) and bank_signature(con, end, t1, t2) != BASE_SIG,
      f"({t1},{t2}) word slope s={F(m, 14+t1+t2)}: {ev} at {fr(end)}; outside contacts {outside_pattern(con, t1, t2)}, "
      f"cut-bank sheets {bank_signature(con, end, t1, t2)} (seed chart: {BASE_SIG})")

# ================================================================== 3. perpendicular, disjoint strips
log("\n# 3. Perpendicular insertions with disjoint strips: corridor x-cut (tx), y=5/2 cut through both boxes (ty)")


def room_perp(tx, ty):
    return dumbbell(5, 0, 4 + ty, 4, -1, 6 + ty, 1, 1, 4 + tx)


def perp_slope(tx, ty, u=s0, P=40):
    K = P * nearest(tx * u / P)
    B = P * nearest(F(ty) / u / P)
    s = F(Y + K + 2 * ty, X + tx + 2 * B)       # x-cut crossed once, y-cut crossed twice
    return s, K, B


for tx, ty in ((1401, 80), (2801, 160), (4201, 241), (2000, 123), (700, 35), (999, 400)):
    s, K, B = perp_slope(tx, ty)
    D = X + tx + 2 * B
    P_ = room_perp(tx, ty)
    assert strictly_simple(P_)
    ev, end, con = trace(P_, (1, 3 + ty), (1 + D, 3 + ty - s * D))
    e = tx * s - K
    f = F(ty) / s - B
    vc = [c for c, k in con if k == 'v']
    msg = (f"(tx,ty)=({tx},{ty}): K={K}, B={B}, s={s}; x-error {e} ({float(e):.4f}), y horizontal error {f} "
           f"({float(f):.4f}); {ev} at {fr(end)}; {len(con)} reflections, {len(vc)} vertical")
    if (tx, ty) == (1401, 80):
        check(s == F(564, 1975) and K == 400 and B == 280 and ev == 'end' and end == (1412, 83) and len(con) == 528,
              "note control " + msg)
    elif max(abs(e), abs(f)) < F(1, 2):
        check(ev == 'end' and end == (11 + tx, 3 + ty), "phases near P*Z at u=s0: " + msg)
    else:
        log("  INFO u=s0 is not a valid trial slope here (a phase error exceeds 1/2): " + msg)
# identity behind the formula: Y + sum_x K + sum_y t = s (X + sum_x t + sum_y B) <=> Y - sX = sum_x e - sum_y s f
s, K, B = perp_slope(1401, 80)
check(Y - s * X == (1401 * s - K) - 2 * s * (F(80) / s - B), "endpoint identity Y - sX = sum_x e - sum_y s*f holds exactly")

# ================================================================== 4. L2 seed source: a W=20 chart with no area<=20 member
log("\n# 4. L2 scope: a W=20 staircase chart has 45 occupied unit cells, so no member has area <= 20")
st = [(0, 0), (9, 0)] + [pt for i in range(9, 1, -1) for pt in ((i, 10 - i), (i - 1, 10 - i))] + [(1, 9), (0, 9)]
area2 = sum(st[i][0] * st[(i + 1) % len(st)][1] - st[(i + 1) % len(st)][0] * st[i][1] for i in range(len(st)))
check(len(st) == 20 and strictly_simple(st) and area2 == 90,
      f"staircase with {len(st)} walls, strictly simple {strictly_simple(st)}, unit-gap area {F(area2, 2)} > 20")

def area(P):
    return abs(F(sum(P[i][0] * P[(i + 1) % len(P)][1] - P[(i + 1) % len(P)][0] * P[i][1] for i in range(len(P))), 2))


check(all(area(room2(a, b)) == 48 + 4 * a + b for a, b in ((0, 0), (10, 500), (1000, 995))),
      "the two-gap DBas family has area 48 + 4 t1 + t2 >= 48, so the area<=20 census holds none of its members")

log(f"\nCPU {time.process_time() - T0:.2f}s; failures: {len(FAIL)}")
for f_ in FAIL:
    log("  FAILED: " + f_)
