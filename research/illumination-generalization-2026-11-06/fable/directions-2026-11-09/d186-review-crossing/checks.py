"""d186 review checks for l1-crossing-gap-transfer.md and l1-cross-cap-budget.md (snapshot 2032).

Named rooms only: the st279 (m=5) slice R(a,D) of the crossing note, and the d184 DBas family room2(t1,t2).
Named parameter values only. Every traced velocity is computed from a formula in the notes
(gate congruence, far-wall endpoint equation, corridor gluing condition) or is a velocity printed in a note.
Congruences are solved by modular inverses, not by trying directions. No room, ray, direction or word search.
The st279 residual (a<=93, D<=376) is NOT enumerated.
trace() is copied verbatim from d184/d182. shoot() is the d109 polygon-edge tracer, adapted to a vertex list.
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


def fr(p):
    return '(' + ','.join(str(c) for c in p) + ')'


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


def room2(t1, t2):
    return dumbbell(5 + t1, 0, 4, 4, -1, 6, 1, 1, 4 + t2)


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


def inv(x, m):
    return pow(x, -1, m) if m > 1 else 0


def first_in(r, g, lo, hi):
    """least element of r + gZ strictly inside (lo,hi), or None (closed form, no search)."""
    k = floor(F(lo - r, g)) + 1
    x = r + g * k
    return x if x < hi else None


def gate(A, D, c, e, a_for_window):
    """Note's gate: (A+1)z in c + A e + 2 gcd(D, 3A) Z, z in (0,1) (b=w=1, W=3). Returns (z, v) with
    z == c + A v (mod 2D), z == e - v (mod 6), or None."""
    g2 = 2 * gcd(D, 3 * A)
    N0 = first_in(c + A * e, g2, 0, A + 1)
    if N0 is None:
        return None
    z = F(N0, A + 1)
    N = (A + 1) * z - c - A * e          # integer, divisible by g2 = gcd(6A, 2D)
    assert N.denominator == 1 and N % g2 == 0
    m = 2 * D // g2
    l = (int(N) // g2) * inv((6 * A // g2) % m, m) % m if m > 1 else 0
    v = e - z + 6 * l
    assert ((z - c - A * v) / (2 * D)).denominator == 1 and ((z - e + v) / 6).denominator == 1
    return z, v


def route_kind(ev, a, D):
    floor_hits = [q for k, q in ev if k == 'h' and q[1] == 4 - a]
    far = [q for k, q in ev if k == 'v' and q[0] == 5 - D]
    hs = [q for k, q in ev if k == 'h']
    return floor_hits, far, hs


# ================================================================== 0. named rooms
log("# 0. Named rooms")
P45 = st(4, 5)
check(area(P45) == 2 * 25 + 6 and strictly_simple(P45) and wall_gcds(P45) == (1, 1),
      f"st(4,5) is st279 m=5: area {area(P45)} = 2m^2+6 = 56, strictly simple, wall gcds {wall_gcds(P45)}")
for a, D in [(7, 21), (7, 22), (7, 35), (11, 33), (13, 78), (13, 90), (101, 303)]:
    P = st(a, D)
    check(strictly_simple(P) and wall_gcds(P) == (1, 1) and (S_st(a)[1] - T_st[1]) % 2 == 0 and S_st(a)[0] % 2 == T_st[0] % 2,
          f"st({a},{D}): strictly simple, wall gcds (1,1), S={fr(S_st(a))} T={fr(T_st)} same parity, area {area(P)}")

# ================================================================== 1a. exact one-seam transfer (direct ascent)
log("\n# 1a. Direct-ascent gate (a+1)z in c + a e + gcd(2D,6a)Z, z in (0,1); c in {1,-1}, e in {-1,-3}")


def direct(a, D):
    out = []
    for c in (1, -1):
        for e in (-1, -3):
            r = gate(a, D, c, e, a)
            if r: out.append((c, e) + r)
    return out


def trace_direct(a, D, c, z, v):
    dz = v if c == 1 else -v          # c=-1 is the reflected source image
    ev = shoot(st(a, D), S_st(a), (-dz, 1), T_st)
    fl, far, hs = route_kind(ev, a, D)
    nref = len(ev) - 1
    return ev[-1][0] == 'reach' and not hs, nref


for a, D in [(4, 5), (7, 22), (11, 34), (13, 90)]:
    sols = direct(a, D)
    c, e, z, v = sols[0]
    ok, nref = trace_direct(a, D, c, z, v)
    check(len(sols) == 4 and ok, f"(a,D)=({a},{D}): spacing {gcd(2*D, 6*a)} < a+1={a+1}; all 4 (c,e) gates open; "
          f"(c,e)=({c},{e}) z={z} v={v}: exact trace reaches T with only lateral reflections ({nref})")
for a in (7, 11, 13, 101):
    for D in (3 * a, 6 * a):
        g = gcd(2 * D, 6 * a)
        res = sorted({(c + a * e) % g for c in (1, -1) for e in (-1, -3)})
        check(g == 6 * a and res == sorted({5 * a + 1, 5 * a - 1, 3 * a + 1, 3 * a - 1}) and all(r > a + 1 for r in res)
              and direct(a, D) == [], f"prime a={a}, D={D}: spacing 6a={g}, residues {res} all > a+1; direct gate closed")
# Presburger argument with named periods: failure at D=3a*k, success at D+P when a does not divide P
for a, k, P in [(7, 1, 2), (13, 2, 12), (101, 1, 60)]:
    D = 3 * a * k
    check(direct(a, D) == [] and len(direct(a, D + P)) > 0,
          f"row a={a}: fail at D={D}, succeed at D+P={D+P} (P={P}, a does not divide P)")

# ================================================================== 1c. DBas exceptional line t1 = 10
log("\n# 1c. DBas line t1=10: s = (least even > (L+28)/14)/(L+28), L = 4 + t2; launch (1,-s) from (1,3)")


def dbas_line(t2):
    L = 4 + t2
    lo = F(L + 28, 14)
    m = floor(lo) + 1
    if m % 2: m += 1
    s = F(m, L + 28)
    assert F(1, 14) < s < F(1, 7)
    P = room2(10, t2)
    T = (21 + t2, 3)
    ev = shoot(P, (1, 3), (1, -s), T)
    x2 = 15 + L
    corr = [q for k, q in ev if k == 'h' and 15 < q[0] < x2 and q[1] in (1, 2)]
    box = [(k, q) for k, q in ev[:-1] if q[0] >= x2]
    want = [('v', x2 + 4), ('v', x2), ('v', x2 + 4)]
    pattern = [(k, q[0]) for k, q in box] == want and box[1][1][1] > 2
    # independent check with the d184 unfolded trace (velocity scaled to total horizontal travel 14+L+14)
    X = 14 + L + 14
    tr = trace(P, (1, 3), (1 + X, 3 - s * X))
    return s, len(ev) - 1, pattern and len(corr) + 3 == len(ev) - 1, tr[0] == 'end' and tr[1] == T, strictly_simple(P)


claimed = {0: (F(1, 8), 4), 56: (F(1, 11), 8), 500: (F(10, 133), 40), 1001: (F(74, 1033), 74)}
for t2 in (0, 56, 500, 1001, F(1, 2), 3, 57, 10007):
    s, nref, pat, tr_ok, simp = dbas_line(t2)
    extra = ''
    if t2 in claimed:
        extra = f"; note claims s={claimed[t2][0]}, {claimed[t2][1]} reflections"
        ok = (s, nref) == claimed[t2]
    else:
        ok = True
    check(ok and pat and tr_ok and simp, f"t2={t2}: s={s}, reach T with {nref} smooth reflections, "
          f"itinerary corridor + cap/portal(y>2)/cap {pat}, d184 trace agrees {tr_ok}{extra}")
# interval length claim
for L in (F(1, 1000), 4, 60):
    check(F(L + 28, 7) - F(L + 28, 14) > 2, f"L={L}: ((L+28)/14,(L+28)/7) has length {F(L+28,14)} > 2")

# ================================================================== 2. cross-cap budget
log("\n# 2. Cap budget: st279 specialization c=d=b=w=1, i=0, W=3, h=a+1")
# gate congruence specialization: g_A = gcd(bD, AW) = gcd(D,3A); 2 g_A = gcd(2D, 6A) at A=a
for a, D in [(7, 21), (101, 303)]:
    check(2 * gcd(D, 3 * a) == gcd(2 * D, 6 * a), f"({a},{D}): 2gcd(bD,aW)={2*gcd(D,3*a)} equals crossing-note spacing gcd(2D,6a)")
# shift invariance 2DW/g_A and corner residue periodicity (general symbols at named values)
for (A, b, D, W, d, c) in [(9, 1, 21, 3, 1, 1), (12, 2, 35, 5, 2, 3)]:
    gA = gcd(b * D, A * W)
    dv = F(2 * D * W, gA)
    check((A * dv / (2 * D)).denominator == 1 and (b * dv / (2 * W)).denominator == 1,
          f"A={A},b={b},D={D},W={W}: v -> v+2DW/g_A={dv} preserves both legs")
    zj = lambda j: c + F(A, d) * (j * D - c)
    check(((zj(5 + 2 * d) - zj(5)) / (2 * D)).denominator == 1, f"d={d}: corner gate z depends only on j mod 2d")
# floor-corner impossibility for st279
for a, D, j in [(7, 21, 3), (101, 303, 7)]:
    v = j * D - 1
    z = 1 + (a + 2) * v
    check(z.__class__ is int, f"({a},{D}): floor corner j={j} gives v={v}, z={z} integral, so not in (0,1)")
# far-wall increment strictly between 0 and h
for (D, c, e, h) in [(35, 1, -1, 8), (21, 1, -1, 8), (40, 3, -7, 6)]:
    inc = F(2 * h * (D - c), 2 * D - c - e)
    check(0 < inc < h, f"D={D},c={c},e={e},h={h}: corner increment 2h(D-c)/(2D-c-e)={inc} in (0,h)")
# bounds
lhs = lambda a: F((a + 1) * (a + 3), 24)
check(lhs(93) <= 4 * 94 and lhs(94) > 4 * 95, f"(a+1)(a+3)/24 <= 4(a+1) iff a <= 93: a=93 gives {lhs(93)} <= 376; a=94 gives {lhs(94)} > 380")
check(4 * (93 + 1) == 376, "D <= 4(a+1) <= 376")
b, d, w, W, i, e = 1, 1, 1, 3, 0, -1
delta = F(b, i - e) - F(b, i + w - e)
check(delta == F(1, 2) and (i + w) * F(b, i - e) == 1,
      f"e=-1: delta={delta}; hypothesis (i+w)b/(i-e)<1 holds with equality only ({(i+w)*F(b,i-e)}) -- see review Low 1")
gen = max(d, F(4 * d * W * (2 * d + 1), w), F(64 * b * d * W, w * w) / delta)
check(gen == 384, f"general theorem at st279 data gives a <= {gen}, D <= 8(a+1); specialization sharpens to 93 and 4(a+1)")

log("\n# 2b. Replay rows (velocities from the note, recomputed from the gate / far-wall equations)")
rows = [(7, 21, (F(-23, 5), -1), 'floor', 5), (7, 35, (-1, F(4, 7)), 'far wall', 5),
        (101, 303, (F(-2753, 52), -1), 'floor', 37)]
for a, D, vel, kind, nref_claim in rows:
    if kind == 'floor':
        A = a + 2
        z, v = gate(A, D, 1, -1, a)
        recomputed = (-v, -1)
    else:
        h = a + 1
        # endpoint: d + s(2D-c-e) - b = (2j+1)h, s in (1/2,1); least odd multiple of h above D
        q = floor(F(D, h)) + 1
        if q % 2 == 0: q += 1
        s = F(q * h, 2 * D)
        recomputed = (-1, s)
    ev = shoot(st(a, D), S_st(a), vel, T_st)
    fl, far, hs = route_kind(ev, a, D)
    vs = [q for k, q in ev if k == 'v']
    shape = (len(fl) == 1 and ev[0] == ('h', fl[0])) if kind == 'floor' else (len(far) == 1 and vs == far)
    check(tuple(F(x) for x in recomputed) == tuple(F(x) for x in vel) and ev[-1][0] == 'reach' and shape
          and len(ev) - 1 == nref_claim,
          f"a={a}, D={D}: velocity {fr(vel)} recomputed {fr(recomputed)}; route {kind}; reaches T with {len(ev)-1} reflections (note {nref_claim})")
# direct route closed at two of the rows (3a | D) -- the floor row is needed there
check(direct(7, 21) == [] and direct(101, 303) == [], "direct gate closed at (7,21) and (101,303)")

log(f"\nCPU {time.process_time() - T0:.2f} s; failures: {len(FAIL)}")
for f_ in FAIL:
    log("  FAILED: " + f_)
