"""d185 review checks for l1-db55-odd-lengths.md (snapshot 2012).

Named rooms only: the DB55 two-box layout, d110 dumbbell(5,0,H1,5,0,H2,2,1,L), at the named lengths
L = 1, 3, 7, 9, 11, 21 (claim), and the controls L = 5 (5 | L) and L = 2, 4 (even), with heights
(H1,H2) = (5,5), (5,9), (7,15), (31,4) plus the note's replay heights. Exact Fraction arithmetic.
trace() and dumbbell() are copied verbatim from d183-review-db55top/checks.py (which copied them from
d181/d175 and d110). flow(), one_return() and chord() are d183's, generalized from span 13 to span C.
Every traced velocity is one the note prescribes: cylinder directions (t,1) with t = 5, 10; the chord
produced by unrolling a cylinder; the grid shots (50k, +-1) with k from the displayed congruences; and
the reviewed d112 A' slope, extended into the far box. Marks and phases are named adversarial points
near corners, seam levels and mouth lips. No room, ray, direction or word search.
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


# ------------------------------------------------------------------ copied verbatim from d183 (d181/d175)
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


def dumbbell(d1, b1, h1, d2, b2, h2, p, w, L):  # copied from d110 geom.py via d181/d183
    assert b1 < p and p + w < b1 + h1 and b2 < p and p + w < b2 + h2
    x2 = d1 + L
    V = [(0, b1), (d1, b1), (d1, p), (x2, p), (x2, b2), (x2 + d2, b2), (x2 + d2, b2 + h2),
         (x2, b2 + h2), (x2, p + w), (d1, p + w), (d1, b1 + h1), (0, b1 + h1)]
    return dict(d1=d1, b1=b1, h1=h1, d2=d2, b2=b2, h2=h2, p=p, w=w, L=L, V=V)


# ------------------------------------------------------------------ the room family of the note
def fr(p):
    return '(' + ','.join(str(c) for c in p) + ')'


SEC = F(2)  # the note's upward section y = 2, including the floor reflection over the corridor
CLAIM_L = [1, 3, 7, 9, 11, 21]
HEIGHTS = [(5, 5), (5, 9), (7, 15), (31, 4)]
CACHE = {}


class Room:
    def __init__(s, L, H1, H2):
        s.L, s.H1, s.H2, s.C = L, H1, H2, L + 10
        s.P = dumbbell(5, 0, H1, 5, 0, H2, 2, 1, L)['V']
        s.Vset = {(F(a), F(b)) for a, b in s.P}
        s.levels = sorted({F(0), F(2), F(3), F(H1), F(H2)})

    def H_at(s, x):
        return s.H1 if x < 5 else s.H2

    def fold(s, u):
        r = F(u) % (2 * s.C)
        assert r not in (0, s.C), r
        return (r, 1) if r < s.C else (2 * s.C - r, -1)

    def u_of(s, x, sx):
        return F(x) % (2 * s.C) if sx > 0 else F(-x) % (2 * s.C)

    def in_corr(s, x):
        return 5 < x < s.C - 5

    def interior(s, p):
        x, y = F(p[0]), F(p[1])
        return (0 < x < 5 and 0 < y < s.H1) or (s.C - 5 < x < s.C and 0 < y < s.H2) or (0 < x < s.C and 2 < y < 3)


def room(L, H1, H2):
    key = (L, H1, H2)
    if key not in CACHE:
        CACHE[key] = Room(L, H1, H2)
    return CACHE[key]


def flow(R, X, Y, vx, vy, stop):
    """d183 flow(), generalized: step level to level among 0,2,3,H1,H2 with the verbatim trace()."""
    X, Y, total = F(X), F(Y), F(0)
    for _ in range(10**5):
        nxt = min(l for l in R.levels if l > Y) if vy > 0 else max(l for l in R.levels if l < Y)
        dy = abs(nxt - Y)
        ev, end, con = trace(R.P, (X, Y), (X + vx * dy, Y + vy * dy))
        if ev == 'corner' or end in R.Vset:
            return 'corner', end, total + dy
        if any(k == 'h' for _, k in con):
            return 'early-h', end, total
        if sum(1 for _, k in con if k == 'v') % 2:
            vx = -vx
        total += dy
        X, Y = end
        if ev == 'wall-end':
            if X in (0, R.C) or (X in (5, R.C - 5) and not 2 < Y < 3):
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


def one_return(R, t, u):
    x, sx = R.fold(u)
    return flow(R, x, SEC, sx * t, 1, at_section)


def predicted_V(R, t, u):
    up = R.fold(u + t)[0]
    lo = R.fold(u + 2 * t)[0]
    return 2 + (0 if R.in_corr(up) else 2 * (R.H_at(up) - 3)) + (0 if R.in_corr(lo) else 4)


eps = F(1, 1000)

# ================================================================== 0. room definition
log("# 0. Room: d110 dumbbell(5,0,H1,5,0,H2,2,1,L) against the note's description")
for L in CLAIM_L + [2, 5]:
    for H1, H2 in HEIGHTS:
        R = room(L, H1, H2)
        C = R.C
        note = [(0, 0), (5, 0), (5, 2), (C - 5, 2), (C - 5, 0), (C, 0), (C, H2), (C - 5, H2), (C - 5, 3), (5, 3),
                (5, H1), (0, H1)]
        area = F(sum(R.P[i][0] * R.P[(i + 1) % 12][1] - R.P[(i + 1) % 12][0] * R.P[i][1] for i in range(12)), 2)
        hor = sorted({abs(R.P[i][0] - R.P[(i + 1) % 12][0]) for i in range(12)} - {0})
        ok = R.P == note and area == 5 * H1 + 5 * H2 + L
        if not ok or (H1, H2) == (5, 9):
            check(ok, f"L={L} (H1,H2)=({H1},{H2}): 12 vertices match the note, area {area} = 5H1+5H2+L, "
                      f"horizontal lengths {hor}, horizontal gcd {gcd(5, L)}")
log("   L=5 has horizontal gcd 5, so it is not horizontally normalized; it is a control only.")

# ================================================================== 1. cycle structure formula
log("\n# 1. Cycle count of u -> u+2t on Z/2C (= gcd(2t,2C)) for t = 5, 10 and the shot moduli")
log("   L : C : #cycles t=5 : #cycles t=10 : gcd(50,2C) : gcd(100,2C)")
for L in range(1, 41):
    C = L + 10
    row = (gcd(10, 2 * C), gcd(20, 2 * C), gcd(50, 2 * C), gcd(100, 2 * C))
    log(f"   {L:2d} : {C:2d} : {row[0]:2d} : {row[1]:2d} : {row[2]:2d} : {row[3]:2d}" +
        ("   <- odd, coprime to 5" if L % 2 and L % 5 else ""))
ok = all((gcd(10, 2 * (L + 10)) == 2) == (L % 5 != 0) for L in range(1, 1001)) and \
     all((gcd(20, 2 * (L + 10)) == 2 and gcd(100, 2 * (L + 10)) == 2) == (L % 2 == 1 and L % 5 != 0)
         for L in range(1, 1001))
check(ok, "for L = 1..1000: t=5 gives two cycles iff 5 does not divide L; t=10 and the same-bank modulus "
          "gcd(100,2C) give 2 iff L is odd and coprime to 5")

# ================================================================== 2. traced return map
log("\n# 2. Upward section y=2: one traced return equals u -> u+2t mod 2C, phases eps=1/1000 either side of")
log("   every integer u in [0,2C) (this includes every phase whose seam, floor, roof or section abscissa is a corner)")
for L in CLAIM_L + [2, 5]:
    for H1, H2 in HEIGHTS:
        R = room(L, H1, H2)
        C = R.C
        for t in (5, 10):
            phases = [(j + s * eps) % (2 * C) for j in range(2 * C) for s in (1, -1)]
            bad = []
            for u in phases:
                ev, st, tot = one_return(R, t, u)
                if ev != 'stop' or R.u_of(st[0], st[2]) != (u + 2 * t) % (2 * C) or tot != predicted_V(R, t, u):
                    bad.append((str(u), ev, tot))
            check(not bad, f"L={L} (H1,H2)=({H1},{H2}) t={t}: {len(phases)} phases return to u+2t with the "
                           f"predicted vertical travel" + (f"; bad {bad[:4]}" if bad else ""))

log("\n   Traced cycle structure: permutation of the 2C unit intervals induced by the traced return of j+1/2")
for L, H1, H2 in [(1, 5, 9), (3, 31, 4), (7, 7, 15), (21, 5, 5), (2, 5, 9), (4, 7, 15), (5, 5, 9)]:
    R = room(L, H1, H2)
    C = R.C
    for t in (5, 10):
        perm = {}
        for j in range(2 * C):
            ev, st, tot = one_return(R, t, j + F(1, 2))
            perm[j] = int(R.u_of(st[0], st[2])) if ev == 'stop' else None
        seen, cyc = set(), []
        for j in range(2 * C):
            if j not in seen:
                n, i = 0, j
                while i not in seen and i is not None:
                    seen.add(i)
                    i = perm[i]
                    n += 1
                cyc.append(n)
        expect = gcd(2 * t, 2 * C)
        check(None not in perm.values() and len(cyc) == expect,
              f"L={L} (H1,H2)=({H1},{H2}) t={t}: traced permutation has {len(cyc)} cycles of lengths "
              f"{sorted(set(cyc))} (gcd(2t,2C) = {expect})" +
              ("  [claim range]" if L % 2 and L % 5 else "  [control]"))

log("\n   Full cycle closes exactly: C returns from u = 5 - 1/1000, (L,H1,H2) = (21,31,4), t = 10")
R = room(21, 31, 4)
u0 = 5 - eps
u, per, ok = u0, F(0), True
for i in range(R.C):
    ev, st, tot = one_return(R, 10, u)
    ok &= ev == 'stop'
    per += tot
    u = R.u_of(st[0], st[2])
check(ok and u == u0, f"{R.C} returns close at u={u}; period vertical travel {per}")

# ================================================================== 3. invariant
log("\n# 3. Invariant: first upward section phase u = sx*x - t*sy*y + 2t (mod 2) for all four lifts")


def NAMED(R):
    C, H1, H2 = R.C, R.H1, R.H2
    return [(5 - F(1, 7), 3 + F(1, 9)), (F(1, 3), H1 - F(1, 5)), (C - 5 + F(1, 11), 2 - F(1, 13)),
            (5 + F(1, 3), 3 - F(1, 17)), (C - F(2, 7), F(1, 19)), (5, F(5, 2) + F(1, 101)),
            (C - 5, 2 + F(1, 97)), (C - F(1, 3), H2 - F(1, 23))]


for L, H1, H2 in [(1, 5, 9), (3, 31, 4), (7, 7, 15), (11, 5, 5), (21, 5, 9), (2, 7, 15)]:
    R = room(L, H1, H2)
    for t in (5, 10):
        bad, nrun = [], 0
        for p in NAMED(R):
            cls = {}
            for sx in (1, -1):
                for sy in (1, -1):
                    ev, st, tot = flow(R, p[0], p[1], sx * t, sy, at_section)
                    nrun += 1
                    inv = (sx * p[0] - t * sy * p[1] + 2 * t) % 2
                    if ev != 'stop' or R.u_of(st[0], st[2]) % 2 != inv:
                        bad.append((fr(p), sx, sy, ev))
                    cls[(sx, sy)] = inv < 1
            if cls[(1, 1)] == cls[(-1, -1)] or cls[(1, -1)] == cls[(-1, 1)]:
                bad.append((fr(p), 'negation does not swap'))
        check(not bad, f"L={L} (H1,H2)=({H1},{H2}) t={t}: {nrun} lifts reach the section in the predicted class; "
                       f"negating both signs swaps cylinders" + (f"; bad {bad}" if bad else ""))

log("\n   Half-integer survivor at t=5 (x and 5y strict half-integers): its lifts sit on rims of both parities")
for L, H1, H2, p in [(7, 7, 15, (F(5, 2), F(7, 10))), (1, 5, 9, (F(19, 2), F(71, 10))), (2, 5, 9, (F(7, 2), F(1, 10)))]:
    R = room(L, H1, H2)
    us = []
    for sx in (1, -1):
        for sy in (1, -1):
            ev, st, tot = flow(R, p[0], p[1], sx * 5, sy, at_section)
            if ev == 'stop':
                us.append(R.u_of(st[0], st[2]))
    par = {int(u) % 2 for u in us if u.denominator == 1}
    check(all(u.denominator == 1 for u in us) and par == {0, 1},
          f"L={L} (H1,H2)=({H1},{H2}) mark {fr(p)}: reached section phases {[str(u) for u in us]}, rim parities {sorted(par)}")


# ================================================================== 4. cylinder chords
def chord(R, t, S, T, rim=False):
    """d183 chord(), generalized to span C: unroll the cylinder and trace the straight chord S -> T."""
    C = R.C
    lifts = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    def reach(p, sx, sy):
        ev, st, tot = flow(R, p[0], p[1], sx * t, sy, at_section)
        return (R.u_of(st[0], st[2]), tot) if ev == 'stop' else None

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
            for m in range(C):
                um = (uS + 2 * t * m) % (2 * C)
                d = (uT - um) % (2 * C)
                if d > C:
                    d -= 2 * C
                if (not rim and abs(d) < 1 and int(um) == int(uT) and um % 1 and uT % 1) or (rim and abs(d) == 1):
                    break
            else:
                continue
            SV, u, okr = F(0), (uS + F(d, 2) if rim else uS), True
            for _ in range(m):
                ev, st, tot = one_return(R, t, u)
                okr &= ev == 'stop'
                SV += tot
                u = R.u_of(st[0], st[2])
            dY = aS + SV - aT
            dX = t * dY + d
            ev, end, con = trace(R.P, S, (S[0] + sxS * dX, S[1] + syS * dY))
            return okr and ev == 'end' and end == (F(T[0]), F(T[1])), (sxS, syS, m, d, dX, dY, len(con), ev)
    return False, None


log("\n# 4. Cylinder chords built from the unrolled cylinder, traced exactly")
CH = [
    (7, 7, 15, 5, (5 - F(1, 1000), 3 + F(1, 1000)), (17 - F(1, 997), 15 - F(1, 991)), False,
     "t=5 off-rim: next to reflex (5,3) -> next to the right cap corner (C,H2)"),
    (1, 31, 4, 5, (F(1, 997), F(1, 991)), (5 + F(1, 3), 2 + F(1, 7)), False,
     "t=5 off-rim: next to floor corner (0,0) -> corridor, L=1"),
    (21, 5, 9, 5, (31 - 5 + F(1, 1000), 2 - F(1, 1000)), (F(49, 10), 2 + F(1, 1000)), False,
     "t=5 off-rim: next to reflex (C-5,2) -> inside the far left mouth"),
    (7, 7, 15, 5, (F(5, 2), F(7, 10)), (2, 1), True,
     "t=5 opposite rims: half-integer survivor -> grid mark (2,1)"),
    (3, 5, 9, 5, (F(1, 2), F(37, 10)), (12, 9 - F(1, 5)), True,
     "t=5 opposite rims: half-integer survivor -> grid mark (12,44/5), unequal heights"),
    (9, 31, 4, 10, (1, F(1, 5)), (16, 4 - F(1, 5)), True,
     "t=10 opposite rims on the residual grid: x parities 1, 0 near floor and cap corners"),
    (11, 7, 15, 10, (4, 3), (17, 2), True,
     "t=10 opposite rims: seam marks beside both reflex corner levels, x parities 0, 1"),
]
for L, H1, H2, t, S, T, rim, lab in CH:
    R = room(L, H1, H2)
    assert R.interior(S) and R.interior(T)
    ok, info = chord(R, t, S, T, rim)
    check(ok, f"L={L} (H1,H2)=({H1},{H2}) {lab}: {fr(S)} -> {fr(T)}; signs, m, delta, (dX,dY), contacts = {info}")


# ================================================================== 5. residual-grid shots
def bank_seam(y):
    return F(3) if y >= 3 else F(2)


def solve(coef, rhs, C):
    ks = [k for k in range(1, C + 1) if (coef * k - rhs) % (2 * C) == 0]
    return ks[0] if ks else None


def shot(R, PA, PB, force=None):
    """The note's construction for an opposite-box pair of residual bank marks. The left mark starts rightward."""
    C = R.C
    S, T = (F(PA[0]), F(PA[1])), (F(PB[0]), F(PB[1]))
    if S[0] > T[0]:
        S, T = T, S
    a, b = S[0], T[0]
    assert a.denominator == 1 and b.denominator == 1 and 1 <= a <= 4 and C - 4 <= b <= C - 1 and (b - a) % 2 == 0
    assert (5 * S[1]).denominator == 1 and (5 * T[1]).denominator == 1 and not 2 < S[1] < 3 and not 2 < T[1] < 3
    vs = -1 if S[1] >= 3 else 1
    legS, legT = abs(S[1] - bank_seam(S[1])), abs(T[1] - bank_seam(T[1]))
    if (S[1] >= 3) != (T[1] >= 3):
        k = force or solve(50, b - a, C)
        case, Vt = "opposite banks", legS + 1 + legT
        if k is None:
            return False, dict(S=S, T=T, case=case + ": no k", k=None, speed=None, n=0, ev='unsolvable')
    else:
        choice = None
        for e in ((force[1],) if force else (1, -1)):
            k = force[0] if force else solve(100, e * b - a, C)
            if k is None:
                continue
            z = (a + 50 * k) % (2 * C)
            good = z % C not in (0, 5, C - 5)
            if good or force:
                choice = (k, e, z, good)
                break
        if choice is None:
            return False, dict(S=S, T=T, case="same bank: no sign works", k=None, speed=None, n=0, ev='unsolvable')
        k, e, z, good = choice
        zf = R.fold(z)[0] if z % C else z
        exc = 0 if R.in_corr(zf) else (4 if S[1] >= 3 else 2 * (R.H_at(zf) - 3))
        case = f"same bank, eps={e:+d}, z={z} ({'corridor' if exc == 0 else 'box excursion'})"
        Vt = legS + 2 + exc + legT
    t = 50 * k
    ev, end, con = trace(R.P, S, (S[0] + t * Vt, S[1] + vs * Vt))
    return ev == 'end' and end == T, dict(S=S, T=T, case=case, k=k, speed=(t, vs), n=len(con), ev=ev, end=end)


log("\n# 5. Residual-grid shots: speed (50k, +-1), k from the note's congruences, exact trace")
log("   For each named room: all 8 (a,d) with a+d odd, at 6 named height pairs (seams beside the reflex")
log("   corners, 1/5 off both seams, 1/5 under the caps, 1/5 over the floors, mixed).")


def YS(R):
    return [(F(3), F(3), "both on seam y=3"), (F(2), F(2), "both on seam y=2"),
            (F(16, 5), F(9, 5), "1/5 above y=3 / 1/5 below y=2"),
            (R.H1 - F(1, 5), R.H2 - F(1, 5), "both 1/5 under the caps"),
            (F(1, 5), F(1, 5), "both 1/5 over the floors"), (R.H1 - F(1, 5), F(2), "cap / seam y=2")]


TOT = [0, 0]
MAXN = 0
for L in CLAIM_L:
    for H1, H2 in HEIGHTS:
        R = room(L, H1, H2)
        C = R.C
        nok = n = 0
        bad = []
        cases = {}
        for a in range(1, 5):
            for d in range(1, 5):
                if (a + d) % 2 == 0:
                    continue
                for yA, yB, lab in YS(R):
                    ok, info = shot(R, (a, yA), (C - d, yB))
                    n += 1
                    nok += ok
                    MAXN = max(MAXN, info['n'])
                    key = info['case'].split(',')[0] + (', ' + info['case'].split(',')[1].strip() if 'eps' in info['case'] else '')
                    cases[key] = cases.get(key, 0) + 1
                    if not ok:
                        bad.append((fr(info['S']), fr(info['T']), info['case'], info['k'], info['ev']))
        TOT[0] += nok
        TOT[1] += n
        check(nok == n, f"L={L} (H1,H2)=({H1},{H2}): {nok}/{n} reach the target; cases {cases}" +
              (f"; bad {bad[:3]}" if bad else ""))
log(f"   total {TOT[0]}/{TOT[1]}; largest smooth-contact count {MAXN}")

log("\n   The note's four exact replays, with the d183 tracer")
REPLAY = [(1, 7, (1, F(21, 5)), (9, F(31, 5)), 1, 94), (3, 5, (1, 1), (9, 1), 9, 610),
          (7, 7, (3, F(21, 5)), (15, F(32, 5)), 11, 571), (9, 15, (2, 1), (16, F(61, 5)), 17, 1778)]
for L, H, S, T, k, nref in REPLAY:
    R = room(L, H, H)
    ok, info = shot(R, S, T)
    check(ok and info['k'] == k and info['n'] == nref,
          f"(L,H)=({L},{H}) {fr(S)}->{fr(T)}: {info['case']}, k={info['k']} (note {k}), speed {info['speed']}, "
          f"{info['n']} contacts (note {nref}), {info['ev']}")

log("\n   Controls on the intermediate-corner test")
for L, H1, H2, S, T in [(1, 5, 9, (1, F(16, 5)), (9, F(41, 5))), (3, 7, 15, (4, F(1, 5)), (12, F(1, 5))),
                        (7, 31, 4, (2, F(16, 5)), (16, F(16, 5)))]:
    R = room(L, H1, H2)
    C = R.C
    a, b = S[0], T[0]
    for e in (1, -1):
        k = solve(100, e * b - a, C)
        z = (a + 50 * k) % (2 * C)
        good = z % C not in (0, 5, C - 5)
        ok, info = shot(R, S, T, force=(k, e))
        test = (a + e * b) % C
        log(f"   L={L} {fr(S)}->{fr(T)} eps={e:+d}: k={k}, z={z}, a+eps*b mod C = {test}, "
            f"test {'passes' if good else 'fails'}; trace {info['ev']}" +
            (f" at {fr(info['end'])}" if info['ev'] == 'corner' else ""))
        check(good == ok and good == (test not in (0, 10 % C, (-10) % C)),
              f"L={L} eps={e:+d}: note's residue test predicts the trace ({'lit' if ok else 'corner'})")

# ================================================================== 6. residue arithmetic
log("\n# 6. Residue arithmetic of the bank cases, all odd C = L+10 coprime to 5 with L <= 989")
badC = []
needneg = {}
for L in range(1, 990, 2):
    if L % 5 == 0:
        continue
    C = L + 10
    for a in range(1, 5):
        for d in range(1, 5):
            if (a + d) % 2 == 0:
                continue
            b = C - d
            opp = solve(50, b - a, C) is not None
            okpos = (a + b) % C not in (0, 10 % C, (-10) % C)
            okneg = (a - b) % C not in (0, 10 % C, (-10) % C)
            same = solve(100, b - a, C) is not None and solve(100, -b - a, C) is not None
            if not (opp and same and (okpos or okneg)):
                badC.append((L, a, d))
            if not okpos:
                needneg.setdefault(L, []).append((a, d))
check(not badC, "opposite banks solvable; both same-bank congruences solvable; one sign passes the corner test "
                "for every (a,d) and every such C" + (f"; bad {badC[:5]}" if badC else ""))
check(sorted(needneg) == [1, 3] and needneg[1] == [(a, d) for a in range(1, 5) for d in range(1, 5)
                                                     if (a + d) % 2 and abs(a - d) == 1]
      and needneg[3] == [(1, 4), (4, 1)],
      f"eps=+1 fails only at L=1 (|a-d|=1) and L=3 (|a-d|=3): {needneg}")

log("\n   Even-L reduction and the note's L=2 example")
R = room(2, 5, 5)
us = {}
for p in [(2, 1), (8, 1)]:
    for sx in (1, -1):
        for sy in (1, -1):
            ev, st, tot = flow(R, p[0], p[1], sx * 5, sy, at_section)
            us[(p, sx, sy)] = (str(R.u_of(st[0], st[2])) if ev == 'stop' else ev)
vals = [F(v) for v in us.values() if v != 'corner']
pars = {int(v) % 2 for v in vals} if all(v.denominator == 1 for v in vals) else {'nonintegral'}
log(f"   L=2, t=5 section phases of (2,1) and (8,1): {us}")
check(pars == {1} and (2 - 5) % 2 == (8 - 5) % 2, "both marks sit only on odd rims at t=5 (x-5y odd at both)")
check(all((100 * k - r) % 24 for k in range(1, 13) for r in (8 - 2, -8 - 2)),
      "L=2: 100k = +-8 - 2 (mod 24) has no solution, as the note says")
check(gcd(20, 24) == 4, "L=2: t=10 gives gcd(20,24) = 4 cycles (traced in section 2)")
log("   Even L in the normalized range below 21: " + str([L for L in range(1, 21) if L % 2 == 0 and L % 5]))

log("\n   L=5 control: the t=5 return has 10 cycles; the shot congruences fail for some residual pairs")
fails5 = [(a, d) for a in range(1, 5) for d in range(1, 5) if (a + d) % 2 and solve(50, 15 - d - a, 15) is None]
check(gcd(10, 30) == 10 and len(fails5) > 0, f"C=15: gcd(10,30)=10; 50k = b-a (mod 30) unsolvable for {fails5}")


# ================================================================== 7. d112 A' extended into the far box
def strip_shot(R, S, T):
    """d112 A' slope (as in d183), with the strip extended through the corridor into the far box."""
    C = R.C
    S, T = (F(S[0]), F(S[1])), (F(T[0]), F(T[1]))
    left = S[0] < 5
    x = 5 - S[0] if left else S[0] - (C - 5)
    z = T[0] - 5 if left else (C - 5) - T[0]
    above = S[1] > 3
    h = S[1] - 3 if above else 2 - S[1]
    tt = 3 - T[1] if above else T[1] - 2
    lo = h * z / tt
    A = x
    while not A > lo:
        A += 10
    assert A < lo + 10 * (1 + h / tt)
    vel = ((1 if left else -1) * (A + z), (-1 if above else 1) * (h + tt))
    ev, end, con = trace(R.P, S, (S[0] + vel[0], S[1] + vel[1]))
    return ev == 'end' and end == T, (A, z, vel, len(con), ev)


log("\n# 7. Box bank mark to a band mark in the far box: d112 A' slope with the strip extended, exact trace")
for L, H1, H2 in [(1, 5, 9), (3, 31, 4), (7, 7, 15), (21, 5, 5), (2, 5, 9), (5, 7, 15)]:
    R = room(L, H1, H2)
    C = R.C
    cases = [((4, F(1, 10)), (C - F(1, 1000), 2 + F(1, 1000)), "left floor side to far outer wall, lower lip level"),
             ((1, H1 - F(1, 10)), (C - 5 + F(1, 1000), 3 - F(1, 1000)), "left cap to just past the far mouth, upper lip"),
             ((C - 1, 3 + F(1, 1000)), (F(1, 1000), 2 + F(1, 1000)), "just above the right reflex to the far outer wall"),
             ((C - 4, F(1, 997)), (F(5, 2), 3 - F(1, 991)), "right floor to the middle of the far box band"),
             ((C - F(1, 3), H2 - F(1, 7)), (F(1, 2), F(5, 2)), "right cap corner to far box band"),
             ((2, 3 + F(1, 5)), (C - 2, F(5, 2)), "residual-grid bank mark to residual-grid band mark")]
    nok, rows = 0, []
    for S, T, lab in cases:
        assert R.interior(S) and R.interior(T)
        ok, info = strip_shot(R, S, T)
        nok += ok
        if not ok or L in (1, 21):
            check(ok, f"L={L} (H1,H2)=({H1},{H2}) {lab}: {fr(S)} -> {fr(T)}, (A, z, velocity, contacts) = {info}")
    check(nok == len(cases), f"L={L} (H1,H2)=({H1},{H2}): {nok}/{len(cases)} extended-strip shots reach the target")

log(f"\nCPU {time.process_time() - T0:.1f} s; failures: {len(FAIL)}")
for f_ in FAIL:
    log("  FAILED:", f_)
