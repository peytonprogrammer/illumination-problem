"""d183 review checks for l1-dbas55-top-phase.md (snapshot 1952).

Named room only: the DB55 top-line stretch, d110 dumbbell(5,0,H,5,0,H,2,1,L=3), at named heights
H = 4, 5, 7, 15, 31, 101. Exact Fraction arithmetic. trace() is copied verbatim from
d181-review-collar/checks.py (itself verbatim from d175). Every traced velocity is one the note
prescribes: the cylinder direction (t,1) for t = 10, 20, 100; the cylinder chord that the note's
unrolling argument produces; the exceptional-grid shots (100k, +-1) with k from the displayed
congruences; and the reviewed chamber-to-strip slope. Marks and section phases are named adversarial
points near corners, critical levels and mouth lips. No room, ray, direction or word search.
Run: python3 -B checks.py > checks.log
"""
import time
from fractions import Fraction as F
from math import gcd

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


def dumbbell(d1, b1, h1, d2, b2, h2, p, w, L):  # copied from d110 geom.py via d181
    assert b1 < p and p + w < b1 + h1 and b2 < p and p + w < b2 + h2
    x2 = d1 + L
    V = [(0, b1), (d1, b1), (d1, p), (x2, p), (x2, b2), (x2 + d2, b2), (x2 + d2, b2 + h2),
         (x2, b2 + h2), (x2, p + w), (d1, p + w), (d1, b1 + h1), (0, b1 + h1)]
    return dict(d1=d1, b1=b1, h1=h1, d2=d2, b2=b2, h2=h2, p=p, w=w, L=L, V=V)


def fr(p):
    return '(' + ','.join(str(c) for c in p) + ')'


HS = [4, 5, 7, 15, 31, 101]
SEC = F(5, 2)
CORNER_X = {0, 5, 8, 13}


def room(H):
    return dumbbell(5, 0, H, 5, 0, H, 2, 1, 3)['V']


def interior(p, H):
    x, y = F(p[0]), F(p[1])
    box = (0 < x < 5 or 8 < x < 13) and 0 < y < H
    band = 0 < x < 13 and 2 < y < 3
    return box or band


def fold(u):
    r = F(u) % 26
    assert r not in (0, 13), r
    return (r, 1) if r < 13 else (26 - r, -1)


def u_of(x, sx):
    return F(x) % 26 if sx > 0 else F(-x) % 26


# ------------------------------------------------------------------ level-stepping driver around trace()
def flow(P, H, X, Y, vx, vy, stop):
    """Follow the billiard flow from (X,Y) with velocity (vx,vy), stepping level to level among the
    critical heights 0,2,5/2,3,H with the verbatim trace(). Returns ('stop', state, travel) when
    stop(state) holds after a step, or ('corner'|..., point, travel)."""
    levels = sorted({F(0), F(2), SEC, F(3), F(H)})
    Vset = {(F(a), F(b)) for a, b in P}
    X, Y, total = F(X), F(Y), F(0)
    for _ in range(10**5):
        nxt = min(l for l in levels if l > Y) if vy > 0 else max(l for l in levels if l < Y)
        dy = abs(nxt - Y)
        ev, end, con = trace(P, (X, Y), (X + vx * dy, Y + vy * dy))
        if ev == 'corner' or end in Vset:
            return 'corner', end, total + dy
        if any(k == 'h' for _, k in con):
            return 'early-h', end, total
        if sum(1 for _, k in con if k == 'v') % 2:
            vx = -vx
        total += dy
        X, Y = end
        if ev == 'wall-end':  # ended on a wall exactly at a level: apply that wall's reflection
            if X in (0, 13) or (X in (5, 8) and not 2 < Y < 3):
                vx = -vx
            else:
                vy = -vy
        elif ev != 'end':
            return ev, end, total
        st = (X, Y, vx, vy)
        if stop(st):
            return 'stop', st, total
    return 'limit', (X, Y), total


def at_section(st):
    return st[1] == SEC and st[3] > 0


def one_return(P, H, t, u):
    x, sx = fold(u)
    return flow(P, H, x, SEC, sx * t, 1, at_section)


def predicted_V(H, t, u):
    up = fold(u + F(t, 2))[0]
    lo = fold(u + F(3 * t, 2))[0]
    return 2 + (0 if 5 < up < 8 else 2 * (H - 3)) + (0 if 5 < lo < 8 else 4)


# ================================================================== 1. room definition
log("# 1. Room: d110 dumbbell(5,0,H,5,0,H,2,1,3) against the note's union and the d181 family")
for H in HS:
    V = room(H)
    note = [(0, 0), (5, 0), (5, 2), (8, 2), (8, 0), (13, 0), (13, H), (8, H), (8, 3), (5, 3), (5, H), (0, H)]
    area = F(sum(V[i][0] * V[(i + 1) % 12][1] - V[(i + 1) % 12][0] * V[i][1] for i in range(12)), 2)
    vert = {abs(V[i][1] - V[(i + 1) % 12][1]) for i in range(12)} - {0}
    hor = {abs(V[i][0] - V[(i + 1) % 12][0]) for i in range(12)} - {0}
    g = lambda s: __import__('functools').reduce(gcd, s)
    check(V == note and area == 10 * H + 3 and g(vert) == 1 and g(hor) == 1,
          f"H={H}: vertices = note's union, area {area} = 10H+3, vertical lengths {sorted(vert)}, "
          f"horizontal {sorted(hor)}, gcds 1; H parity {'odd (in d181 family)' if H % 2 else 'even (beyond d181 family)'}")
check(dumbbell(5, 0, 5, 5, 0, 5, 2, 1, 3)['V'] == room(5), "H=5 equals d181 ROOMS['DB55'] at L=3")

# ================================================================== 2. cylinder return map
log("\n# 2. Upward section y=5/2: one return equals u -> u+2t mod 26, at adversarial phases")
log("   Phases: eps=1/1000 either side of each integer u whose upper seam abscissa u+t/2 or lower seam")
log("   abscissa u+3t/2 folds to a corner abscissa 5 or 8, plus eps off the outer walls u=0,13.")
eps = F(1, 1000)
for t in (10, 20, 100):
    base = set()
    for c in (5, 8, 18, 21):
        base.add((c - t // 2) % 26)
        base.add((c - 3 * t // 2) % 26)
    base |= {0, 13}
    phases = sorted({(b + s * eps) % 26 for b in base for s in (1, -1)})
    for H in HS:
        bad = []
        for u in phases:
            ev, st, tot = one_return(room(H), H, t, u)
            if ev != 'stop' or u_of(st[0], st[2]) != (u + 2 * t) % 26 or tot != predicted_V(H, t, u):
                bad.append((str(u), ev, tot))
        check(not bad, f"t={t}, H={H}: {len(phases)} phases return to u+2t with predicted vertical travel" +
              (f"; bad {bad}" if bad else ""))
    check(gcd(2 * t, 26) == 2 and (t // 10) % 13 != 0, f"t={t}: gcd(2t,26)=2, 13 does not divide k={t // 10}")

log("\n   Full 13-return cycle at H=101, t=100, from u=5-1/1000 (next to the mouth tip)")
H, t = 101, 100
u0 = 5 - eps
u, per, ok = u0, F(0), True
for i in range(13):
    ev, st, tot = one_return(room(H), H, t, u)
    ok &= ev == 'stop'
    per += tot
    u = u_of(st[0], st[2])
check(ok and u == u0, f"13 returns close up exactly at u={u}; period vertical travel {per}")

# ================================================================== 3. transverse invariant
log("\n# 3. Invariant: first upward section phase u = sx - t*ty + 5t/2 mod 2 for all four lifts")
NAMED = lambda H: [(5 - F(1, 7), 3 + F(1, 9)), (F(1, 3), H - F(1, 5)), (8 + F(1, 11), 2 - F(1, 13)),
                   (6 + F(1, 3), 3 - F(1, 17)), (12 + F(5, 7), F(1, 19)), (5, F(5, 2) + F(1, 101))]
for H in (4, 7, 31):
    for t in (10, 20, 100):
        bad, nrun = [], 0
        for p in NAMED(H):
            classes = {}
            for sx in (1, -1):
                for sy in (1, -1):
                    ev, st, tot = flow(room(H), H, p[0], p[1], sx * t, sy, at_section)
                    nrun += 1
                    inv = (sx * p[0] - t * sy * p[1] + F(5 * t, 2)) % 2
                    if ev != 'stop' or u_of(st[0], st[2]) % 2 != inv:
                        bad.append((fr(p), sx, sy, ev))
                    classes[(sx, sy)] = inv < 1
            if classes[(1, 1)] == classes[(-1, -1)] or classes[(1, -1)] == classes[(-1, 1)]:
                bad.append((fr(p), 'negation does not swap cylinders'))
        check(not bad, f"H={H}, t={t}: {nrun} lifts reach the section at the predicted class; "
              f"negating both signs swaps cylinders" + (f"; bad {bad}" if bad else ""))


# ================================================================== 4. cylinder chords
def chord(H, t, S, T, rim=False):
    """Build the note's cylinder chord from S to T in direction class t and trace it.
    Interior case: S and T have lifts in the same open cylinder. Rim case: opposite rims."""
    P = room(H)
    lifts = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    def reach(p, sx, sy):  # signed travel a: the section point is the lift plus a*(t,1)
        ev, st, tot = flow(P, H, p[0], p[1], sx * t, sy, at_section)
        if ev == 'stop':
            return u_of(st[0], st[2]), tot
        # rim marks on a short saddle connection: follow the leaf backward to a downward section crossing
        ev, st, tot = flow(P, H, p[0], p[1], -sx * t, -sy, lambda q: q[1] == SEC and q[3] < 0)
        return (u_of(st[0], -st[2]), -tot) if ev == 'stop' else None

    for (sxS, syS) in lifts:
        rS = reach(S, sxS, syS)
        if not rS:
            continue
        uS, aS = rS
        for (sxT, syT) in lifts:
            rT = reach(T, sxT, syT)
            if not rT:
                continue
            uT, aT = rT
            if not rim and (uS % 2 < 1) != (uT % 2 < 1):
                continue
            if rim and (uS.denominator != 1 or uT.denominator != 1 or (uS - uT) % 2 == 0):
                continue
            for m in range(13):
                um = (uS + 2 * t * m) % 26
                d = (uT - um) % 26
                if d > 13:
                    d -= 26
                if (not rim and abs(d) < 1 and int(um) == int(uT) and um % 1 and uT % 1) or (rim and abs(d) == 1):
                    break
            else:
                continue
            # vertical travel of the cylinder over m returns, measured on an interior leaf of the interval
            SV, u, okr = F(0), (uS + F(d, 2) if rim else uS), True
            for _ in range(m):
                ev, st, tot = one_return(P, H, t, u)
                okr &= ev == 'stop'
                SV += tot
                u = u_of(st[0], st[2])
            dY = aS + SV - aT
            dX = t * dY + d
            ev, end, con = trace(P, S, (S[0] + sxS * dX, S[1] + syS * dY))
            return okr and ev == 'end' and end == (F(T[0]), F(T[1])), (sxS, syS, m, d, dX, dY, len(con), ev)
    return False, None


log("\n# 4. Cylinder chords built from the unrolled cylinder, traced exactly")
CH = [  # (H, t, S, T, rim, label)
    (15, 10, (5 - F(1, 1000), 3 + F(1, 1000)), (13 - F(1, 997), 15 - F(1, 991)), False,
     "next to reflex (5,3) -> next to cap corner (13,H)"),
    (101, 10, (F(1, 997), F(1, 991)), (6 + F(1, 3), 2 + F(1, 7)), False, "next to floor corner (0,0) -> corridor"),
    (7, 10, (8 + F(1, 1000), 2 - F(1, 1000)), (4 + F(9, 10), 2 + F(1, 1000)), False,
     "next to reflex (8,2) -> just inside the left mouth"),
    (5, 20, (F(1, 2), F(1, 20)), (12 + F(1, 2), 5 - F(1, 20)), False,
     "t=10-rim marks (x+-10y integral) that are off-rim at t=20"),
    (31, 20, (F(1, 2), 31 - F(1, 20)), (8 + F(1, 2), 2 + F(1, 20)), False,
     "t=10-rim marks near cap corner and near reflex (8,2)"),
    (4, 100, (4, 3), (9, 2), True, "t=100 opposite rims: x parities 0,1 at the reflex seams"),
    (15, 100, (1, F(1, 10)), (12, 15 - F(1, 10)), True, "t=100 opposite rims near floor and cap corners"),
]
for H, t, S, T, rim, lab in CH:
    ok, info = chord(H, t, S, T, rim)
    check(ok, f"H={H}, t={t}, {lab}: {fr(S)} -> {fr(T)}; lift signs, m, delta, (dX,dY), contacts = {info}")


# ================================================================== 5. exceptional-grid shots
def band(y):
    return 2 < y < 3


def seam(y):
    return F(3) if y >= 3 else F(2)


def shot(H, P1, P2, kforce=None):
    """The note's construction for an opposite-box pair of grid marks. Returns trace verdict and data."""
    P1, P2 = (F(P1[0]), F(P1[1])), (F(P2[0]), F(P2[1]))
    if band(P1[1]) and not band(P2[1]):
        P1, P2 = P2, P1
    if band(P2[1]) and not band(P1[1]):
        S, T = P1, P2  # bank mark is the source
    else:
        S, T = (P1, P2) if P1[0] < 5 else (P2, P1)
    mir = S[0] > 8
    Sm, Tm = ((13 - S[0], S[1]), (13 - T[0], T[1])) if mir else (S, T)
    a, b, yS, yT = Sm[0], Tm[0], Sm[1], Tm[1]
    assert a.denominator == 1 and b.denominator == 1 and 1 <= a <= 4 and 9 <= b <= 12 and (b - a) % 2 == 0
    vs = -1 if yS >= 3 else 1
    legS = abs(yS - seam(yS))
    if band(yT):
        j = abs(yT - seam(yS)) * 10
        case = f"one in band, j={j}"
        ks = [k for k in range(1, 14) if (a + 10 * j * k) % 26 in (b, 26 - b)]
        k = kforce or ks[0]
        assert (a + 10 * j * k) % 26 in (b, 26 - b)
        Vt = legS + j / 10
    elif (yS >= 3) != (yT >= 3):
        case = "opposite banks"
        k = kforce or [k for k in range(1, 14) if (a + 100 * k) % 26 in (b, 26 - b)][0]
        assert (a + 100 * k) % 26 in (b, 26 - b)
        Vt = legS + 1 + abs(yT - seam(yT))
    else:
        case = "same bank"
        good = []
        for k in ([kforce] if kforce else range(1, 14)):
            if (a + 200 * k) % 26 in (b, 26 - b):
                z = (a + 100 * k) % 26
                eps_ = 1 if (a + 200 * k) % 26 == b else -1
                good.append((k, z, eps_, z % 13 not in (0, 5, 8)))
        k, z, epsn, zok = [g for g in good if g[3]][0]
        zf = fold(z)[0] if z % 13 else z
        exc = 0 if 5 < zf < 8 else (4 if yS >= 3 else 2 * (H - 3))
        case += f", eps={epsn}, z={z}, intermediate {'corridor' if exc == 0 else 'box excursion'}"
        Vt = legS + 2 + exc + abs(yT - seam(yT))
    tt = 100 * k
    vel = ((-1 if mir else 1) * tt * Vt, vs * Vt)
    ev, end, con = trace(room(H), S, (S[0] + vel[0], S[1] + vel[1]))
    ok = ev == 'end' and end == T
    return ok, dict(S=S, T=T, case=case, k=k, speed=((-1 if mir else 1) * tt, vs), n=len(con), ev=ev,
                    mirrored=mir)


log("\n# 5. Exceptional-grid shots: speed (100k, +-1), k from the note's congruences, exact trace")


def GRID(H):
    h = F(H) - F(1, 10)
    return [
        ((4, 3), (10, 2), "both on seams, left mark beside reflex (5,3), zero legs"),
        ((1, h), (11, F(1, 10)), "near cap and floor corners"),
        ((4, F(31, 10)), (10, F(19, 10)), "one tenth off both mouth-lip levels"),
        ((3, 2), (11, h), "seam y=2 to just under the cap"),
        ((1, h), (11, h), "same top bank, (1,11): eps=-1 fails"),
        ((2, 3), (12, 3), "same top bank on the seam, (2,12): eps=-1 fails"),
        ((1, 2), (11, F(1, 10)), "same bottom bank, (1,11)"),
        ((2, F(1, 10)), (12, F(1, 10)), "same bottom bank near floor corners, (2,12)"),
        ((4, F(31, 10)), (12, h), "same top bank, b-a=8"),
        ((4, 2), (10, 2), "same bottom seam, b-a=6"),
        ((4, 3), (10, F(29, 10)), "bank on seam, band mark j=1 under the upper lip"),
        ((1, F(1, 10)), (11, F(21, 10)), "bottom bank to band, j=1 over the lower lip"),
        ((4, h), (10, F(21, 10)), "cap to band, j=9"),
        ((3, F(25, 10)), (9, h), "band mark on the left, bank mark on the right (mirrored)"),
        ((10, F(1, 10)), (2, F(29, 10)), "bank mark on the right, band j=9 (mirrored)"),
    ]


for H in HS:
    nok, rows = 0, []
    for P1, P2, lab in GRID(H):
        ok, d = shot(H, P1, P2)
        nok += ok
        rows.append((ok, P1, P2, lab, d))
    for ok, P1, P2, lab, d in rows:
        if not ok or H in (4, 101):
            check(ok, f"H={H} {lab}: {fr(d['S'])} -> {fr(d['T'])}, {d['case']}, k={d['k']}, speed {d['speed']}, "
                  f"{d['n']} smooth contacts, {d['ev']}")
    check(nok == len(rows), f"H={H}: {nok}/{len(rows)} grid shots reach the target")

log("\n   Control: same bank with eps=-1 at (a,b)=(1,11), H=7: the intermediate seam phase is a corner")
for H in (7, 101):
    a, b = 1, 11
    k = [k for k in range(1, 14) if (a + 200 * k) % 26 == 26 - b][0]
    z = (a + 100 * k) % 26
    S, T = (F(1), F(H) - F(1, 10)), (F(11), F(H) - F(1, 10))
    V_ = (S[1] - 3) + 2 + 4 + (T[1] - 3)
    ev, end, con = trace(room(H), S, (S[0] + 100 * k * V_, S[1] - V_))
    check(ev == 'corner' and z % 13 in (0, 5, 8), f"H={H}: eps=-1 gives k={k}, z={z} (z mod 13 = {z % 13}); "
          f"trace stops at {ev} {fr(end)} as the note predicts")

# ================================================================== 6. the note's table
log("\n# 6. The note's five exact checks, replayed with the d181 tracer")
TABLE = [(5, (1, 1), (9, 1), (1100, 1), 1490), (7, (1, F(51, 10)), (11, F(43, 10)), (200, -1), 167),
         (15, (2, F(121, 10)), (12, F(133, 10)), (200, -1), 807), (7, (2, F(11, 10)), (10, F(61, 10)), (1100, 1), 964),
         (7, (3, F(41, 10)), (9, F(26, 10)), (600, -1), 150)]
for H, S, T, v, nref in TABLE:
    ok, d = shot(H, S, T, kforce=v[0] // 100)
    check(ok and d['speed'] == v and d['n'] == nref,
          f"H={H} {fr(S)}->{fr(T)}: construction gives speed {d['speed']} (note {v}), {d['n']} contacts (note {nref}), {d['ev']}")

# ================================================================== 7. arithmetic of the case split
log("\n# 7. Residue arithmetic behind the three opposite-box cases (all a in 1..4, b in 9..12, same parity)")
pairs = [(a, b) for a in range(1, 5) for b in range(9, 13) if (b - a) % 2 == 0]
opp = all(any((a + 100 * k) % 26 in (b, 26 - b) for k in range(1, 14)) for a, b in pairs)
check(opp, f"opposite banks: a+100k = +-b mod 26 solvable for all {len(pairs)} pairs")
same_fail = []
for a, b in pairs:
    okany = False
    for e in (1, -1):
        if (a + e * b) % 13 not in (0, 3, 10):
            okany = True
    neg_bad = (a - b) % 13 in (0, 3, 10)
    if neg_bad:
        same_fail.append((a, b, (a + b) % 13))
    if not okany:
        FAIL.append(f"same bank {a},{b}")
check(all((a + b) % 13 not in (0, 3, 10) for a, b, _ in same_fail) and sorted((a, b) for a, b, _ in same_fail) == [(1, 11), (2, 12)],
      f"same bank: eps=-1 fails only at {[(a, b) for a, b, _ in same_fail]}; eps=+1 sums mod 13 {[s for *_, s in same_fail]} are good")
check(all(gcd(10 * j, 26) == 2 for j in range(1, 10)) and
      all(any((a + 10 * j * k) % 26 in (b, 26 - b) for k in range(1, 14)) for a, b in pairs for j in range(1, 10)),
      "one-in-band: gcd(10j,26)=2 and a+10jk = +-b solvable for j=1..9 and all pairs")
check(all((2 * z) % 13 in (0, 3, 10) for z in (0, 5, 8)) and sorted({(2 * z) % 13 for z in (0, 5, 8)}) == [0, 3, 10],
      "bad intermediate residues z = 0,+-5 mod 13 double to 0,+-3 = {0,3,10}")
# survivor algebra: at t=10,20 all lifts on rims iff x+-10y, x+-20y integral => x, 10y integral
for x, y in [(F(1, 2), F(1, 20)), (F(3), F(7, 10)), (F(5), F(23, 10))]:
    r10 = all(((sx * x + sy * 10 * y) % 1) == 0 for sx in (1, -1) for sy in (1, -1))
    r20 = all(((sx * x + sy * 20 * y) % 1) == 0 for sx in (1, -1) for sy in (1, -1))
    log(f"   mark {fr((x, y))}: all-rim at t=10: {r10}, at t=20: {r20}, survivor: {r10 and r20}")
check(F(100) * F(7, 10) % 2 == 0 and F(5 * 100, 2) % 2 == 0, "t=100: 100y and 5t/2 even on the tenths grid")

# ================================================================== 8. chamber-to-strip lemma (d112 A')
log("\n# 8. Box mark to corridor or mouth mark: reviewed d112 A' slope, exact trace")


def strip_shot(H, S, T):
    S, T = (F(S[0]), F(S[1])), (F(T[0]), F(T[1]))
    left = S[0] < 5
    x = 5 - S[0] if left else S[0] - 8
    z = T[0] - 5 if left else 8 - T[0]
    above = S[1] > 3
    h = S[1] - 3 if above else 2 - S[1]
    tt = 3 - T[1] if above else T[1] - 2
    lo = h * z / tt
    A = x
    while not A > lo:
        A += 10
    assert A < lo + 10 * (1 + h / tt)
    vel = ((1 if left else -1) * (A + z), (-1 if above else 1) * (h + tt))
    ev, end, con = trace(room(H), S, (S[0] + vel[0], S[1] + vel[1]))
    return ev == 'end' and end == T, (A, vel, len(con), ev)


for H in (4, 31, 101):
    h = F(H) - F(1, 10)
    for S, T, lab in [((4, F(1, 10)), (8, F(21, 10)), "floor corner side to far mouth lip"),
                      ((1, h), (8, F(29, 10)), "cap to far mouth under the upper lip"),
                      ((12, 3 + F(1, 1000)), (5, 2 + F(1, 1000)), "just above the right reflex to far left mouth lip"),
                      ((9, F(1, 997)), (6 + F(1, 2), 3 - F(1, 991)), "right floor to corridor near roof")]:
        ok, info = strip_shot(H, S, T)
        check(ok, f"H={H} {lab}: {fr(S)} -> {fr(T)}, A, velocity, contacts = {info}")

# sanity: all marks used are interior
allmarks = [m for H in HS for P1, P2, _ in GRID(H) for m in ((H, P1), (H, P2))]
check(all(interior(p, H) for H, p in allmarks), f"all {len(allmarks)} grid marks are interior points")

log(f"\nCPU {time.process_time() - T0:.1f} s; failures: {len(FAIL)}")
for f_ in FAIL:
    log("  FAILED:", f_)
