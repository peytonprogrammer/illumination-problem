"""d171 review checks for ferrers-residual-inequalities.md (snapshot 2026-11-22 0855).

Named explicit rooms only, exact Fraction arithmetic, no searches over rooms.
trace() is copied verbatim from d170-review-ferrers2/checks.py (from d168 / d167).
Run: python3 -B checks.py > checks.log
"""
import random
import time
from fractions import Fraction as F
from math import gcd, floor, ceil

T0 = time.process_time()
FAIL = []


def log(*a):
    print(*a, flush=True)


def check(ok, msg):
    log(('  PASS ' if ok else '  FAIL ') + msg)
    if not ok:
        FAIL.append(msg)


# ------------------------------------------------------------------ copied verbatim from d170
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


def den(q):
    return F(q).denominator


def lcm(a, b):
    return a * b // gcd(a, b)


def fr(p):
    return '(' + ','.join(str(c) for c in p) + ')'


class Room:
    """Widths w<u<v<W top to bottom, heights c,d,e,h top to bottom (as d168/d170)."""

    def __init__(self, name, w, u, v, W, c, d, e, h):
        self.name = name
        self.w, self.u, self.v, self.W = map(F, (w, u, v, W))
        self.c, self.d, self.e, self.h = map(F, (c, d, e, h))
        self.y3 = self.h + self.e + self.d
        self.H = self.y3 + self.c
        y1, y2, y3, H = self.h, self.h + self.e, self.y3, self.H
        self.P = [(0, 0), (W, 0), (W, y1), (v, y1), (v, y2), (u, y2), (u, y3), (w, y3), (w, H), (0, H)]

    def transposed(self):
        w, u, v, W, c, d, e, h = self.w, self.u, self.v, self.W, self.c, self.d, self.e, self.h
        return Room(self.name + "'", h, e + h, d + e + h, c + d + e + h, W - v, v - u, u - w, w)

    # ---- the four earlier tests and the chord test
    def chord(self):
        return self.d * (self.v - self.u) <= self.e * (self.u - self.w)

    def A(self):  # d170 (1)
        w, u, v, d, e, h = self.w, self.u, self.v, self.d, self.e, self.h
        return w * (e + h) <= u * d and (u + w) * h * (e + h) <= v * e * (d + e + h)

    def B(self):  # d168 denominator test with optimal P0
        P0 = lcm(den(self.d / (2 * self.u)), den(self.e / (2 * self.v)))
        return den(P0 * self.h / self.W) > floor(self.W / self.w) ** 2

    def tests(self):
        T = self.transposed()
        return dict(C=self.chord(), A=self.A(), At=T.A(), B=self.B(), Bt=T.B())


rnd = random.Random(171)

# ================================================================== item 1: d17 Lemma C+ (perp) on type 4991
log('# Item 1: d17 Lemma C+ perp form, staircase frame')
log('  Hub G=[0,v]x[0,y3]; door 1 = top cell door [0,w]x{y3}, flat end (0,y3), mirror side x=0;')
log('  door 2 = {v}x[0,h], flat end (v,0), mirror side floor. Window: |a|<w at y=y3, |b|<h at x=v.')


def cplus_candidates(R, S, T, K=40):
    """All window candidates (signs, k1, k2) with |k|<=K. Unfolded S'=(e1*x+2wk1, ys), T'=(z, e2*yt+2hk2)."""
    w, v, h, y3 = R.w, R.v, R.h, R.y3
    x, ys = S
    z, yt = T
    out = []
    for e1 in (1, -1):
        for e2 in (1, -1):
            for k1 in range(-K, K + 1):
                sx = e1 * x + 2 * w * k1
                for k2 in range(-K, K + 1):
                    ty = e2 * yt + 2 * h * k2
                    if ty >= y3:
                        continue
                    a = sx + (z - sx) * (ys - y3) / (ys - ty)
                    if not (-w < a < w):
                        continue
                    b = ys + (ty - ys) * (v - sx) / (z - sx)
                    if -h < b < h:
                        out.append((e1, e2, k1, k2, (e1 * (z - sx), ty - ys)))
    return out


def cplus_room(R, pairs, expect_valid):
    nc = nv = nbad = 0
    signs_missing = 0
    mx = 0
    firstbad = None
    for S, T in pairs:
        cands = cplus_candidates(R, S, T)
        signs_missing += len({(c[0], c[1]) for c in cands}) < 4
        for e1, e2, k1, k2, (dx, dy) in cands:
            nc += 1
            st, pos, con = trace(R.P, S, (S[0] + dx, S[1] + dy))
            mx = max(mx, len(con))
            if st == 'end' and pos == T:
                nv += 1
            else:
                nbad += 1
                if firstbad is None:
                    firstbad = (S, T, (e1, e2, k1, k2), st, pos)
    return nc, nv, nbad, signs_missing, mx, firstbad


def open_pairs(R, n_rand, dens=(3, 7, 11, 13)):
    Ss = [(F(2 * i + 1, 2), F(2 * j + 1, 2)) for i in range(int(R.w)) for j in range(int(R.y3), int(R.H))]
    Ts = [(F(2 * i + 1, 2), F(2 * j + 1, 2)) for i in range(int(R.v), int(R.W)) for j in range(int(R.h))]
    pairs = [(s, t) for s in Ss for t in Ts]
    for _ in range(n_rand):
        q = rnd.choice(dens)
        s = (F(rnd.randint(1, int(R.w) * q - 1), q), R.y3 + F(rnd.randint(1, int(R.c) * q - 1), q))
        q = rnd.choice(dens)
        t = (R.v + F(rnd.randint(1, int(R.W - R.v) * q - 1), q), F(rnd.randint(1, int(R.h) * q - 1), q))
        pairs.append((s, t))
    return pairs


O1 = Room('O1', 2, 3, 4, 5, 1, 1, 1, 5)
O2 = Room('O2', 2, 3, 4, 6, 2, 1, 1, 2)
S1 = Room('S1', 2, 3, 4, 6, 3, 1, 3, 2)          # strict: d(v-u)=1 < e(u-w)=3
N1 = Room('N1', 1, 2, 3, 4, 1, 1, 1, 1)          # ledger realization, equality
for R in (O1, O2, S1, N1):
    lhs, rhs = R.d * (R.v - R.u), R.e * (R.u - R.w)
    pairs = open_pairs(R, 12)
    nc, nv, nbad, sm, mx, fb = cplus_room(R, pairs, True)
    log(f'  {R.name} {fr((R.w, R.u, R.v, R.W))}; {fr((R.c, R.d, R.e, R.h))}: d(v-u)={lhs}, e(u-w)={rhs}, '
        f'{len(pairs)} pairs, {nc} window candidates, max {mx} reflections')
    check(lhs <= rhs, f'{R.name}: chord hypothesis holds')
    check(sm == 0, f'{R.name}: every pair has a window candidate for all 4 sign pairs (|k|<=40)')
    check(nbad == 0, f'{R.name}: every window candidate traces exactly to T, no corner ({nv}/{nc})')
    if fb:
        log('     first bad', fb)

# controls below the chord: the lemma must not be read as unconditional
D17 = Room('D17', 3, 4, 9, 12, 3, 4, 2, 3)
RES = Room('RES', 10, 11, 13, 100, 87, 2, 1, 10)
nc, nv, nbad, sm, mx, fb = cplus_room(D17, [((F(1), F(10)), (F(10), F(1)))], False)
check(nc > 0 and nv == 0, f'control D17 below chord, r3.md pair (1,10)-(10,1): {nc} window candidates, '
      f'{nv} valid (r3.md: none valid); first failure {fb[3] if fb else None}')
nc, nv, nbad, sm, mx, fb = cplus_room(RES, [((F(5), F(55)), (F(55), F(5))), ((F(1, 2), F(27, 2)), (F(199, 2), F(1, 2)))], False)
log(f'  info RES below chord, 2 pairs: {nbad} of {nc} window candidates invalid (hypothesis is sufficient, not necessary)')

# algebra: chord condition = "V2 on or above chord V1V3", and is transpose invariant
okc = okt = True
for _ in range(3000):
    w = F(rnd.randint(1, 50), rnd.randint(1, 9)); u = w + F(rnd.randint(1, 50), rnd.randint(1, 9))
    v = u + F(rnd.randint(1, 50), rnd.randint(1, 9)); W = v + 1
    c, d, e, h = (F(rnd.randint(1, 50), rnd.randint(1, 9)) for _ in range(4))
    R = Room('r', w, u, v, W, c, d, e, h)
    ychord = (h + e + d) + (h - (h + e + d)) * (u - w) / (v - w)
    okc &= (R.chord() == (h + e >= ychord))
    okt &= (R.chord() == R.transposed().chord())
check(okc, 'chord test d(v-u)<=e(u-w) equals "(u,h+e) on or above chord (w,h+e+d)-(v,h)" (3000 random rational rooms)')
check(okt, 'chord test is invariant under the diagonal transpose (3000 random rational rooms)')

# ================================================================== item 2: RES certificate
log('\n# Item 2: RES certificate, grid (0,10,11,13,100)')
okw = True
for t in range(-30, 31):
    for k in range(-30, 31):
        i, M = 19 * t + 26 * k, 209 * t + 286 * k
        j = F(11 * i - t, 26)
        okw &= (2 * M == 22 * i and j.denominator == 1 and 3 * M - 22 * i - 26 * j == t)
check(okw, 'i=19t+26k, M=209t+286k, j=(11i-t)/26 integral and 2M=22i, 3M-22i-26j=t (|t|,|k|<=30)')
# completeness: every integer solution of 2M=22i, 3M-22i-26j=t has this form
okc = all(((11 * i - t) % 26 != 0) or ((i - 19 * t) % 26 == 0) for t in range(-60, 61) for i in range(-300, 301))
check(okc, 'every integer solution (i,j) has i = 19t (mod 26), so the family is complete')

# 142 exceptional depths
exc = set()
for q in range(1, 11):
    for p in range(1, 143 * q):
        r = F(p, q)
        if 0 < r < F(143, 10) and den(F(143, 5) - r) <= 10:
            exc.add(r)
bs = sorted(F(200) * r / 286 for r in exc)
check(len(bs) == 142 and all(0 < b < 10 for b in bs), f'exceptional depths: {len(bs)} (note: 142)')


def AH(B, a0):
    L = 3 + B
    eta = F(10) * L / (L + a0)
    return L, eta, (11 * L - eta * (1 + B)) / 2, 13 * L - eta * B


def intervals(B, a0, lo=F(13), hi=F(100)):
    """Open z-intervals inside a window around (lo,hi) certified by the note's sufficient inequalities."""
    L, eta, A, H = AH(B, a0)
    q = den(F(286) * B / 200)
    sp = F(200, q)
    out = []
    tm = floor((H + 3 * A) / L)
    for t in range(-tm, tm + 1):
        zl, zr = max(-A, (-H - L * t) / 3), min(A, (H - L * t) / 3)
        if zl >= zr:
            continue
        c0 = (209 * B + 1) * t
        n0 = ceil((lo - 400 - c0 - zr) / sp)
        n1 = floor((hi + 400 - c0 - zl) / sp)
        for n in range(n0, n1 + 1):
            out.append((c0 + n * sp + zl, c0 + n * sp + zr))
    return out


def merge(iv):
    iv = sorted(iv)
    m = []
    for l, r in iv:
        if m and l < m[-1][1]:          # strictly overlapping only
            m[-1] = (m[-1][0], max(m[-1][1], r))
        else:
            m.append((l, r))
    return m


def covers(iv, lo=F(13), hi=F(100)):
    return any(l <= lo and r >= hi for l, r in merge(iv))


uncov = [b for b in bs if not covers(intervals(b, 0) + intervals(20 - b, 0))]
check(uncov == [F(100, 11)], f'a0=0: direct+floor intervals cover (13,100) at all exceptional depths except {uncov}')
b0 = F(100, 11)
m = [I for I in merge(intervals(b0, 0) + intervals(20 - b0, 0)) if I[1] > 13 and I[0] < 100]
log('  at b=100/11, merged intervals meeting (13,100):', [fr(I) for I in m])
check(m == [(F(-395, 22), F(395, 22)), (F(485, 22), F(1275, 22)), (F(1365, 22), F(3035, 22))],
      'these are exactly the note\'s three intervals')
check(F(395, 22) - 13 == F(109, 22), 'reflection step: a >= 395/22 - 13 = 109/22')
m2 = [I for I in merge(intervals(b0, F(109, 22)) + intervals(20 - b0, F(109, 22))) if I[1] > 13 and I[0] < 100]
log('  at b=100/11, a0=109/22:', [fr(I) for I in m2])
iv2 = intervals(b0, F(109, 22)) + intervals(20 - b0, F(109, 22))
check(len(m2) == 1 and m2[0][0] < 13 and m2[0][1] > 100, 'a0=109/22: one merged interval strictly contains (13,100)')
check(m2[0][0] <= F(-71341, 550) and m2[0][1] >= F(126891, 550), "it contains the note's (-71341/550,126891/550)")
ends = ({l for l, r in iv2}, {r for l, r in iv2})
log(f"  note's endpoints are endpoints of single intervals: left {F(-71341, 550) in ends[0]}, right {F(126891, 550) in ends[1]}")
log('  (component endpoints depend on how far the enumeration window extends; only containment matters)')
# non-exceptional b: one route with q>=11 has spacing 200/q <= 200/11 < 23+B = interval length at t=0
L, eta, A, H = AH(F(0), 0)
check(2 * A == 23 and F(200, 11) < 23, 'rotation step: t=0 interval length 23+B exceeds spacing 200/11')
Pset = {(F(a), F(b)) for a, b in RES.P}
check({(b, a) for a, b in Pset} == Pset, 'RES is invariant under (x,y)->(y,x)')


def res_shot(S, T, a0=0, maxM=None):
    """Note's construction. Returns list of candidate dicts sorted by |M| (only small |M| kept)."""
    x, ys = S
    z, yt = T
    a, b = ys - 13, 10 - yt
    cands = []
    for B in (b, 20 - b):
        L, eta, A, H = AH(B, a0)
        q = den(F(286) * B / 200)
        tm = floor((H + 3 * A) / L)
        for t in range(-tm, tm + 1):
            zl, zr = max(-A, (-H - L * t) / 3), min(A, (H - L * t) / 3)
            if zl >= zr:
                continue
            for k in range(-q - 2, q + 3):
                M = 209 * t + 286 * k
                base = z - t - M * B
                # Z = base + 200 m in (zl, zr)
                for mm in range(ceil((zl - base) / 200) - 1, floor((zr - base) / 200) + 2):
                    Z = base + 200 * mm
                    if zl < Z < zr:
                        cands.append((abs(M), B, t, k, M, Z, L))
    cands.sort(key=lambda c: c[0])
    return cands


def res_trace(S, T, a0=0, cap=60000):
    x, ys = S
    a = ys - 13
    cands = res_shot(S, T, a0)
    if not cands:
        return 'nocand', None
    _, B, t, k, M, Z, L = cands[0]
    Dtot = a + L
    res = []
    for sgn in (1, -1):
        rhs = sgn * x + a * M + a * Z / L
        E = rhs / (1 + a / L)
        per = F(20) / (1 + a / L)
        E = E - per * round(E / per)
        if abs(E) > 10 * L / (L + a) or abs(E) >= 10:
            res.append(('E-range', None)); continue
        g1 = (1 + B) * E / L + 2 * Z / L
        g2 = t + B * E / L + 3 * Z / L
        if not (abs(g1) < 11 and abs(g2) < 13):
            res.append(('gate', (g1, g2))); continue
        s = M + (Z - E) / L                 # developed slope per unit descent
        st, pos, con = trace(RES.P, S, (S[0] + sgn * s * Dtot, S[1] - Dtot), maxrefl=cap)
        res.append((st, pos, len(con), M, B))
        if st == 'end' and pos == T:
            return 'ok', (sgn, M, B, t, k, len(con))
    return 'fail', res


def res_batch(pairs, label, a0=0):
    nok, mx, bad, rts = 0, 0, [], set()
    for S, T in pairs:
        st, info = res_trace(S, T, a0)
        if st == 'ok':
            nok += 1; mx = max(mx, info[5]); rts.add('floor' if info[2] > 10 else 'direct')
        else:
            bad.append((S, T, st, info))
    check(nok == len(pairs), f'{label}: {nok}/{len(pairs)} pairs reach T exactly via the certificate '
          f'(routes {sorted(rts)}, max {mx} reflections)')
    for S, T, st, info in bad[:3]:
        log('     bad', fr(S), fr(T), st, info)


hl = [((F(2 * i + 1, 2), F(2 * j + 1, 2)), (F(2 * p + 1, 2), F(2 * q + 1, 2)))
      for i in (0, 4, 9) for j in (13, 40, 99) for p in (13, 56, 99) for q in (0, 9)]
res_batch(hl, 'RES half-lattice (54 pairs, corners of the cells and the middle)')
rp = []
for _ in range(20):
    b = rnd.choice(bs) if rnd.random() < 0.5 else F(rnd.randint(1, 10 * 7 - 1), 7)
    rp.append(((F(rnd.randint(1, 10 * 13 - 1), 13), 13 + F(rnd.randint(1, 87 * 11 - 1), 11)),
               (13 + F(rnd.randint(1, 87 * 9 - 1), 9), 10 - b)))
res_batch(rp, 'RES random rational (20 pairs, half at exceptional depths)')
crit = [((F(10, 11), 13 + F(109, 22) + F(1, 100)), (F(395, 22) + F(1, 50), 10 - b0)),
        ((F(10, 11), F(99)), (F(20), 10 - b0)),
        ((F(1, 3), F(50)), (F(60), 10 - b0)),
        ((F(9), F(20)), (F(99), 10 - b0))]
res_batch(crit, 'RES depth b=100/11, a>=109/22, z in the a0=0 gaps', a0=F(109, 22))
# the a0=0 gap is genuine for the fixed-a0 inequality, not a dark pair: control
st, info = res_trace((F(10, 11), F(14)), (F(20), 10 - b0), a0=0)
log(f'  control: a=1 < 109/22, z=20 in the a0=0 gap -> certificate status {st} (expected nocand)')
check(st == 'nocand', 'control: the certificate gives no candidate in the a0=0 gap at b=100/11, as the note says')

# ================================================================== item 3: union coverage on named rooms
log('\n# Item 3: coverage C | A | At | B | Bt on named rooms')
rooms = [O1, O2, S1, N1, D17, RES,
         Room('T1', 3, 4, 12, 13, 1, 1, 1, 1),
         Room('U1', 2, 3, 5, 6, 7, 1, 1, 3),
         Room('U1b', 2, 3, 5, 9, 1, 1, 1, 3),
         Room('U2', 1, 2, 3, 4, 13, 2, 1, 4),
         Room('U2b', 1, 2, 3, 5, 1, 2, 1, 4)]
for R in rooms:
    t = R.tests()
    log(f'  {R.name:4s} {fr((R.w, R.u, R.v, R.W))}; {fr((R.c, R.d, R.e, R.h))}: ' +
        ' '.join(f'{k}={int(v)}' for k, v in t.items()))
U = {R.name: R.tests() for R in rooms}
check(U['O1']['C'] and U['O2']['C'] and not any(v for k, v in U['O1'].items() if k != 'C')
      and not any(v for k, v in U['O2'].items() if k != 'C'), 'O1, O2 covered by the chord test only (equality)')
check(not any(U['RES'].values()), 'RES fails all five tests (needs the note\'s certificate)')
check(U['T1']['At'] and not (U['T1']['C'] or U['T1']['A'] or U['T1']['B'] or U['T1']['Bt']),
      'T1 is covered only by At (so coverage differs with and without d170 transpose)')
for nm in ('U1', 'U1b', 'U2', 'U2b'):
    check(not any(U[nm].values()), f'{nm} fails all five tests: uncovered lattice room')

# family claim: (2,3,5,W; c,1,1,3), W>=6, c>=7 fails all five tests (sample of the family)
okf = all(not any(Room('f', 2, 3, 5, W, c, 1, 1, 3).tests().values()) for W in range(6, 40) for c in range(7, 40))
check(okf, 'family (2,3,5,W; c,1,1,3), 6<=W<40, 7<=c<40: all five tests fail')

log(f'\n{len(FAIL)} FAIL; CPU {time.process_time() - T0:.1f} s')
