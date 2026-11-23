"""d182 review checks for l1-growth-modes.md (snapshot 1933).

Named room DBas only (d110 geom.ROOMS), plus the note's own W=10 ledger realization (static check).
Exact Fraction arithmetic. Insertions are made only on DBas at hand-chosen cuts. Every traced velocity
is the one the note's slope formula prescribes from a named base shot. No room/ray/direction/word search.
trace() is copied verbatim from d181-review-collar/checks.py (itself verbatim from d175).
Run: python3 -B checks.py > checks.log
"""
import time
from fractions import Fraction as F
from math import floor, gcd

T0 = time.process_time()
FAIL = []


def log(*a):
    print(*a, flush=True)


def check(ok, msg):
    log(('  PASS ' if ok else '  FAIL ') + msg)
    if not ok:
        FAIL.append(msg)


# ------------------------------------------------------------------ copied verbatim from d181/d175
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


def dbas(L=4, d2=4):  # DBas = (5,0,4,4,-1,6,1,1); L = corridor length, d2 = right chamber depth
    return dumbbell(5, 0, 4, d2, -1, 6, 1, 1, L)


def strictly_simple(P):
    """Axis-parallel polygon: nonadjacent edges disjoint, adjacent edges meet only at the shared vertex."""
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


def lcm(*a):
    r = 1
    for x in a:
        r = r * x // gcd(r, x)
    return r


def nearest(q):
    return floor(q + F(1, 2))


def predict(s0, X, M, P, t):
    k = nearest(F(t) * s0 / P)
    s = (X * s0 + M * k * P) / (X + M * t)
    e = t * s - k * P
    return k, s, e


def run_case(label, room_of_t, S_of_t, T_of_t, sgn, s0, X, M, P, ts, mu, transpose=False, inserted=None):
    """sgn = (hx, vy) initial signs. If transpose, s0 is |dx|/|dy| and X is total vertical travel.
    mu = least transverse gate margin of the base shot. The running error is (s-s0)(x - bX/M), so
    |error| <= X|s-s0| <= XMP/(2(X+Mt)); the itinerary is guaranteed once XMP/(2(X+Mt)) < mu.
    Below that threshold outcomes are logged as INFO, not asserted."""
    thr = (F(X * M * P, 2) / mu - X) / M
    log(f"\n## {label}: s0={s0}, travel={X}, M={M}, P={P}, margin mu={mu}; guaranteed for t > {thr} ~ {float(thr):.1f}")
    s0, X = F(s0), F(X)
    res = {}
    base_contacts = None
    for t in ts:
        P_ = room_of_t(t)
        assert strictly_simple(P_), "room not strictly simple"
        S, T = S_of_t(t), T_of_t(t)
        k, s, e = predict(s0, X, M, P, t)
        tot = X + M * t
        if not transpose:
            B = (S[0] + sgn[0] * tot, S[1] + sgn[1] * s * tot)
        else:
            B = (S[0] + sgn[0] * s * tot, S[1] + sgn[1] * tot)
        ev, end, con = trace(P_, S, B)
        ok = ev == 'end' and end == (F(T[0]), F(T[1]))
        ident = X * (s - s0) + M * e == 0
        b1 = abs(s - s0) <= F(M * P, 2) / tot
        b2 = abs(e) <= X * P / (2 * tot)
        outside = [(c, kk) for c, kk in con if not (inserted and inserted(t, c))]
        if t == 0:
            base_contacts = [kk for _, kk in outside]
        same = base_contacts is not None and [kk for _, kk in outside] == base_contacts
        res[t] = ok
        if 0 < t <= thr:
            log(f"  INFO t={t} (below threshold): k={k}, s={s}; {ev} at {fr(end)}; reaches target {ok}; "
                f"base itinerary kept {same}; identity {ident}, bounds {b1 and b2}")
            continue
        check(ok and ident and b1 and b2 and (t == 0 or same),
              f"t={t}: k={k}, s={s}, e={e}; {ev} at {fr(end)} (target {fr(T)}); "
              f"identity {ident}, |s-s0| bound {b1}, |e| bound {b2}; {len(con)} contacts, "
              f"{len(outside)} outside strips, base pattern kept {same}")
    return res


# ================================================================== 1. static checks for the classification
log("# 1. Classification: gap count and the W=10 ledger realization")
W = 20
m = W // 2
check(2 * (m - 1) == 18 and 2 * (m - 1) + 4 == 22,
      f"W=20: {m} vertical and {m} horizontal walls -> at most {m} lines and {m-1} gaps per axis; total 18, 22 with marks")
V10 = [(2, 0), (4, 0), (4, 1), (3, 1), (3, 4), (0, 4), (0, 3), (1, 3), (1, 2), (2, 2)]


def turnword(P):
    n, w = len(P), ''
    for i in range(n):
        a, b, c = P[i - 1], P[i], P[(i + 1) % n]
        cr = (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])
        w += 'L' if cr > 0 else 'R'
    return w


def canon(w):
    n = len(w)
    rots = [w[i:] + w[:i] for i in range(n)]
    rev = w[::-1].translate(str.maketrans('LR', 'LR'))
    rots += [rev[i:] + rev[:i] for i in range(n)]
    return min(rots)


tw = turnword(V10)
check(strictly_simple(V10) and tw.count('L') - tw.count('R') == 4 and canon(tw) == canon('LLLRLLLRLR'),
      f"W=10 realization is strictly simple with turn word {tw} ~ LLLRLLLRLR")
# monotone reparametrization (x,y) -> (f(x), g(y)) on DBas: one example per axis keeps strict simplicity
f = {0: 0, 5: 7, 9: 8, 13: 20}
g = {-1: -1, 0: 3, 1: 4, 2: 9, 4: 10, 5: 30}
Pm = [(f[x], g[y]) for x, y in dbas()]
check(strictly_simple(dbas()) and strictly_simple(Pm), "DBas and one monotone gap change of DBas are strictly simple")

# ================================================================== 2/3. transfer theorem traces
log("\n# 2-3. Transfer theorem: exact traces on DBas with insertions")
S0, T0p = (1, 3), (11, 3)
ev, end, con = trace(dbas(), S0, (1 + 14, 3 - 4))
check(ev == 'end' and end == (11, 3) and [c for c, _ in con] == [(8, 1), (13, F(17, 7))],
      f"base DBas shot (1,3)->(11,3) velocity (7,-2): {ev} at {fr(end)}, contacts {[fr(c) for c, _ in con]}")

# 2a. named control in detail at t=100
t = 100
k, s, e = predict(F(2, 7), 14, 1, 2, t)
check((k, s) == (14, F(16, 57)), f"t=100: k={k}, s={s} (note: k=14, s=16/57)")
entry = 3 - 4 * s
check(entry == F(107, 57), f"entry height at x=5: {entry} (note: 107/57)")
# fold the corridor leg: corridor [5,109]x[1,2]; downward from height entry
ph = (entry - 1) - 104 * s          # unfolded height relative to floor, measured downward
phase = ph % 2
check((-ph) % 2 == F(18, 57), f"unfolded corridor height change rel. floor = {ph}; signed (upward-positive) phase mod 2 = {(-ph) % 2} (note: 18/57)")
# physical exit height and vertical sign from folding a downward ray at unfolded height ph (period 2)
r = ph % 2
exit_h, up = (1 + r, False) if r <= 1 else (1 + 2 - r, True)
# an unfolded ray moving downward: within each period, the image moves up on the "reflected" half
# (direct derivation: fold z -> z if z in [0,1], 2-z if z in [1,2]; the derivative sign flips on [1,2])
check(exit_h == F(75, 57) and up, f"corridor exit at x=109: height {exit_h}, upward={up} (note: 75/57 upward)")
check(exit_h + 4 * s == F(139, 57) and exit_h + 6 * s == 3, f"cap height {exit_h + 4*s}, target height {exit_h + 6*s}")
P100 = dbas(4 + t)
ev, end, con = trace(P100, S0, (1 + 114, 3 - 114 * s))
check(ev == 'end' and end == (111, 3), f"t=100 trace: {ev} at {fr(end)}, {len(con)} contacts, "
      f"last contact {[fr(c) for c, _ in con[-1:]]}")
cap = [c for c, kk in con if kk == 'v']
check(cap == [(113, F(139, 57))], f"only vertical contact is the cap at {[fr(c) for c in cap]}")
check(all(5 < c[0] < 109 and c[1] in (1, 2) for c, kk in con if kk == 'h'),
      f"all {sum(kk == 'h' for _, kk in con)} horizontal contacts lie on the corridor's long walls")
# old slope control: fixed s0 works iff t multiple of 7 (in this itinerary)
for tt in (98, 100):
    ev, end, con = trace(dbas(4 + tt), S0, (1 + 14 + tt, 3 - F(2, 7) * (14 + tt)))
    log(f"   fixed slope 2/7 at t={tt}: {ev} at {fr(end)}; reaches target: {end == (11 + tt, 3)}")

corr = lambda t, c: 5 < c[0] < 5 + t + 1 and c[1] in (1, 2)   # inserted strip [6, 6+t] (cut at x=6)
# 2b. named shot, insertion amounts (note's 100 and the brief's 37, 250, 1001; 0..12 shows the threshold)
r1 = run_case("A: named DBas shot, cut x=6 in the corridor", lambda t: dbas(4 + t), lambda t: S0,
              lambda t: (11 + t, 3), (1, -1), F(2, 7), 14, 1, 2, [0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 37, 100, 250, F(2003, 3), 999, 1001], F(1, 7),
              inserted=lambda t, c: 6 <= c[0] <= 6 + t and c[1] in (1, 2))

# threshold for the named shot, then every t in 0..60 traced exactly
# Per-gate version for this shot: delta=|s-s0| <= 1/(14+t) and e=-14*delta, so the error at (x,b) is
# delta*(x-14b). Left door (x=4,b=0): 4*delta < 1/7. Right door (x=8,b=1): 6*delta < 2/7. Cap (x=12,b=1):
# 2*delta, margin 18/7. Floor and ceiling hits lie on the corridor's long walls, between the two doors.
# So t > 14 suffices for this shot (the single-margin bound above gives t > 84; the note's box bound
# X+Mt > P max(M,X)/(2 eta), with eta < 2/63 from |8 ds + e| < 2/7 and |4 ds| < 1/7, gives t > 427).
bad = []
for t in range(0, 61):
    k, s, e = predict(F(2, 7), 14, 1, 2, t)
    ev, end, con = trace(dbas(4 + t), S0, (1 + 14 + t, 3 - s * (14 + t)))
    if not (ev == 'end' and end == (11 + t, 3)):
        bad.append((t, ev))
log(f"   named shot, t = 0..60: failures {bad}")
check(all(t <= 14 for t, _ in bad), "every failure is at or below the per-gate threshold t > 14 for this shot")

# 2c. two crossings of one cut, both horizontal senses, a ceiling and a floor bounce in the corridor
SC, TC = (1, F(3, 2)), (3, F(4, 3))
ev, end, con = trace(dbas(), SC, (1 + 22, F(3, 2) + F(22, 12)))
check(ev == 'end' and end == TC and [c for c, _ in con] == [(7, 2), (13, F(3, 2)), (7, 1)],
      f"base two-crossing shot {fr(SC)} slope 1/12 up, X=22: {ev} at {fr(end)}, contacts {[fr(c) for c, _ in con]}")
run_case("C: two crossings of the corridor cut x=6 (rightward, then leftward after the cap)",
         lambda t: dbas(4 + t), lambda t: SC, lambda t: TC, (1, 1), F(1, 12), 22, 2, 2,
         [0, 37, 100, 250, 999, 1001], F(1, 6), inserted=lambda t, c: 6 <= c[0] <= 6 + t and c[1] in (1, 2))

# 2d. two cuts with different interval heights: corridor x=6 (height 1) and right chamber x=12 (height 6)
for a1, a2 in ((1, 1), (1, 3)):
    M = a1 + 2 * a2
    run_case(f"D: cuts x=6 (weight {a1}, height 1) and x=12 (weight {a2}, height 6, crossed twice); P=lcm(2,12)",
             lambda t, a1=a1, a2=a2: dbas(4 + a1 * t, 4 + a2 * t), lambda t: S0, lambda t, a1=a1: (11 + a1 * t, 3),
             (1, -1), F(2, 7), 14, M, 12, [0, 37, 100, 250, 1001, 5000], F(1, 7),
             inserted=lambda t, c, a1=a1, a2=a2: (6 <= c[0] <= 6 + a1 * t and c[1] in (1, 2)) or
             (12 + a1 * t <= c[0] <= 12 + a1 * t + a2 * t and c[1] in (-1, 5)))


# 2e. transposed: one horizontal cut y=5/2 meeting two intervals of different widths, (0,5) and (9,13)
def dbas_tall(t):
    return [(0, 0), (5, 0), (5, 1), (9, 1), (9, -1), (13, -1), (13, 5 + t), (9, 5 + t), (9, 2), (5, 2),
            (5, 4 + t), (0, 4 + t)]


ins_e = lambda t, c: F(5, 2) <= c[1] <= F(5, 2) + t and c[0] in (0, 5, 9, 13)
run_case("E: transposed, cut y=5/2 crossing widths 5 and 4 (down, then up); P=lcm(10,8)=40",
         dbas_tall, lambda t: (1, 3 + t), lambda t: (11, 3 + t), (1, -1), F(7, 2), 4, 2, 40,
         [0, 37, 100, 250, 1001, 5000], F(1, 2), transpose=True, inserted=ins_e)
log("\n   control: E with P a multiple of only one crossed width (P=10 or P=8)")
for Pw in (10, 8):
    out = []
    for t in (37, 100, 250, 1001, 5000):
        k, s, e = predict(F(7, 2), 4, 2, Pw, t)
        tot = 4 + 2 * t
        ev, end, con = trace(dbas_tall(t), (1, 3 + t), (1 + s * tot, 3 + t - tot))
        out.append((t, ev == 'end' and end == (11, 3 + t)))
    ks = [predict(F(7, 2), 4, 2, Pw, t)[0] for t, _ in out]
    log(f"   P={Pw}: reaches target {out}; k*P mod 8 (right-chamber doubled width) = {[k * Pw % 8 for k in ks]}, "
        f"mod 10 (left) = {[k * Pw % 10 for k in ks]}")
    check(not all(o for _, o in out), f"P={Pw} (not a multiple of both doubled widths) misses at some t")

log("   P=10 successes have k*P = 0 or 4 mod 8. A shift of 4 is half the doubled width 8: it mirrors the")
log("   right chamber about x=11, which is the target's abscissa. So these are coincidences of a centred target.")

# ================================================================== 4. logic of the consequence (no computation)
log("\n# 4. Consequence: contrapositive bookkeeping on the named shot")
# If (1,3)-(11+t,3) is lit at base t0, the theorem applied at base t0 lights it for t0+t, t large.
# Check one instance: base t0=37 (its own shot from 2b), then insert further amounts on the same ray.
k, s37, e = predict(F(2, 7), 14, 1, 2, 37)
X37, M37 = 14 + 37, 1
for t in (100, 1001):
    k2, s2, e2 = predict(s37, X37, M37, 2, t)
    ev, end, con = trace(dbas(4 + 37 + t), S0, (1 + X37 + t, 3 - s2 * (X37 + t)))
    check(ev == 'end' and end == (11 + 37 + t, 3),
          f"re-based at t0=37 (s0={s37}, X={X37}): insert {t} more -> s={s2}, {ev} at {fr(end)}")

log(f"\nCPU {time.process_time() - T0:.2f}s; failures: {len(FAIL)}")
for f_ in FAIL:
    log("  FAILED: " + f_)
