"""d173 review checks for band-chain-characters.md (snapshot 2026-11-22 1332).

Named explicit rooms only, exact Fraction arithmetic for every traced shot, no room
or direction searches, no network. trace() is copied verbatim from d170 (via d172).
Run: python3 -B checks.py > checks.log
"""
import math
import random
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


# ---------------------------------------------------------------- verbatim from d170
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


def lcm(a, b):
    return a * b // gcd(a, b)


def rep(v, per):
    """Representative of v modulo per in (-per/2, per/2]."""
    r = v % per
    return r - per if r > per / 2 else r


def dist1(x):
    """Distance from a rational x to the integers."""
    r = x % 1
    return min(r, 1 - r)


def minP(mid):
    """Least P>0 with P*d in 2u*Z for every middle run (d, u); P=None if there are none."""
    P = F(1)
    first = True
    for d, u in mid:
        q = F(2 * u) / F(d)          # P must be a multiple of q
        if first:
            P, first = q, False
        else:                        # lcm of two rationals n1/d1, n2/d2 = lcm(n)/gcd(d)
            P = F(lcm(P.numerator, q.numerator), gcd(P.denominator, q.denominator))
    return None if first else P


# ---------------------------------------------------------------- the note's construction
class Chain:
    """A monotone chain. axis: 'y' means longitudinal y (transverse x), 'x' the reverse.
    ldir: sign of longitudinal motion from source to target. Transverse chart t = phys - t0.
    src=(lo,hi), tgt=(lo,hi) transverse intervals of the endpoint runs; mid=[(d_j,u_j)];
    g1: longitudinal coordinate of the first gate; c0: constant base line; delta: clearance."""

    def __init__(self, name, poly, axis, ldir, t0, src, tgt, mid, g1, c0, delta, P=None, floor=None):
        self.name, self.poly, self.axis, self.ldir, self.t0 = name, poly, axis, ldir, F(t0)
        self.src, self.tgt = tuple(map(F, src)), tuple(map(F, tgt))
        self.mid = [(F(d), F(u)) for d, u in mid]
        self.g1, self.c0, self.delta = F(g1), F(c0), F(delta)
        self.P = F(P) if P is not None else minP(self.mid)
        self.floor = floor        # longitudinal coordinate of a full far wall of the target run, or None
        for d, u in self.mid:
            assert (self.P * d / (2 * u)).denominator == 1

    def lt(self, p):              # (longitudinal, transverse) of a physical point
        return (p[1], p[0] - self.t0) if self.axis == 'y' else (p[0], p[1] - self.t0)

    def setup(self, S, T, use_floor=False):
        ls, ts = self.lt(S)
        lT, tT = self.lt(T)
        a = (self.g1 - ls) * self.ldir
        dsum = sum(d for d, _ in self.mid)
        glast = self.g1 + self.ldir * dsum
        b = (lT - glast) * self.ldir
        assert a > 0 and b >= 0
        if use_floor:
            h = (self.floor - glast) * self.ldir
            assert 0 < b < h
            b = 2 * h - b
        w, V = self.src[1] - self.src[0], self.tgt[1] - self.tgt[0]
        D = a + dsum + b
        gates = [a]
        for d, _ in self.mid:
            gates.append(gates[-1] + d)
        return dict(a=a, b=b, w=w, V=V, D=D, gates=gates, ts=ts, tT=tT, dsum=dsum)

    def alpha(self, s):
        return (-self.P * s['a'] / (2 * s['w']), self.P * s['b'] / (2 * s['V']))

    def solutions(self, S, T, use_floor=False, kmax=None):
        """Exact finite test (rational alpha): all (k mod N, signs) with k*alpha in the open
        rectangle about theta. Returns (N, list of (k, e1, e2, err1, err2))."""
        s = self.setup(S, T, use_floor)
        al = self.alpha(s)
        N = lcm(al[0].denominator, al[1].denominator)
        lo_s, lo_t = self.src[0], self.tgt[0]
        X0s = [(1, s['ts']), (-1, 2 * lo_s - s['ts'])]
        Z0s = [(1, s['tT']), (-1, 2 * lo_t - s['tT'])]
        P, a, b, w, V, dl, c0 = self.P, s['a'], s['b'], s['w'], s['V'], self.delta, self.c0
        out = []
        for k in range(N if kmax is None else min(N, kmax)):
            for e1, X0 in X0s:
                r1 = rep(X0 - c0 + k * P * a, 2 * w)
                if not abs(r1) < dl:
                    continue
                for e2, Z0 in Z0s:
                    r2 = rep(Z0 - c0 - k * P * b, 2 * V)
                    if abs(r2) < dl:
                        out.append((k, e1, e2, r1, r2))
        return N, out, s

    def theta_test(self, S, T, use_floor=False):
        """Same test phrased on the torus: k*alpha - theta in the open rectangle (eps1, eps2)."""
        s = self.setup(S, T, use_floor)
        al = self.alpha(s)
        N = lcm(al[0].denominator, al[1].denominator)
        e1s, e2s = self.delta / (2 * s['w']), self.delta / (2 * s['V'])
        ths1 = [(s['ts'] - self.c0) / (2 * s['w']), (2 * self.src[0] - s['ts'] - self.c0) / (2 * s['w'])]
        ths2 = [(s['tT'] - self.c0) / (2 * s['V']), (2 * self.tgt[0] - s['tT'] - self.c0) / (2 * s['V'])]
        for k in range(N):
            if any(dist1(k * al[0] - t) < e1s for t in ths1) and any(dist1(k * al[1] - t) < e2s for t in ths2):
                return True
        return False

    def shoot(self, S, T, sol, s, use_floor=False, shift=0):
        k, e1, e2, r1, r2 = sol
        k = k + shift
        P, a, D = self.P, s['a'], s['D']
        sigma = k * P + (r2 - r1) / D
        ell = [r1 + (r2 - r1) * t / D for t in s['gates']]
        gates_ok = all(abs(g) < self.delta for g in ell)
        tv = e1 * sigma * D             # transverse displacement (physical sign) per full travel
        lv = self.ldir * D
        vec = (tv, lv) if self.axis == 'y' else (lv, tv)
        st, pos, con = trace(self.poly, S, (S[0] + vec[0], S[1] + vec[1]))
        lit = st == 'end' and pos == (F(T[0]), F(T[1]))
        note = ''
        if use_floor and st == 'corner':
            # stop-earlier argument of deep-terminal-band: same launch, direct travel length
            sd = self.setup(S, T, False)
            f = sd['D'] / D
            st2, pos2, _ = trace(self.poly, S, (S[0] + vec[0] * f, S[1] + vec[1] * f))
            lit = st2 == 'end' and pos2 == (F(T[0]), F(T[1]))
            note = 'floor-corner->stop-early'
        return dict(lit=lit, gates_ok=gates_ok, st=st, n=len(con), k=k, note=note,
                    maxell=max(abs(g) for g in ell))


def best_order(sols, N):
    """Order solutions by |k| using the representative of k in (-N/2, N/2]."""
    out = []
    for k, e1, e2, r1, r2 in sols:
        kk = k - N if k > N // 2 else k
        out.append((abs(kk), (kk, e1, e2, r1, r2)))
    out.sort(key=lambda z: z[0])
    return [z[1] for z in out]


def run_pairs(C, pairs, itins, label, max_tries=4):
    """For each pair: exact test per itinerary; replay the constructed shot when it passes."""
    npass = nlit = nbad = nfail = ngate = 0
    nfloor_corner = 0
    maxrefl = 0
    failed = []
    for S, T in pairs:
        passed = False
        for use_floor in itins:
            N, sols, s = C.solutions(S, T, use_floor)
            if not sols:
                continue
            passed = True
            ok = False
            for sol in best_order(sols, N)[:max_tries]:
                r = C.shoot(S, T, sol, s, use_floor)
                ngate += not r['gates_ok']
                maxrefl = max(maxrefl, r['n'])
                if r['note']:
                    nfloor_corner += 1
                if r['lit'] and r['gates_ok']:
                    ok = True
                    break
            nlit += ok
            nbad += not ok
            if not ok:
                log(f'     BAD replay {S}-{T} floor={use_floor}: {r}')
            break
        npass += passed
        if not passed:
            nfail += 1
            failed.append((S, T))
    log(f'   {label}: {len(pairs)} pairs; test passes {npass} (replayed lit {nlit}, replay failures {nbad}); '
        f'test fails {nfail}; gate-bound violations {ngate}; floor-corner stop-early uses {nfloor_corner}; '
        f'max reflections {maxrefl}')
    return dict(npass=npass, nlit=nlit, nbad=nbad, nfail=nfail, failed=failed, ngate=ngate)


# ---------------------------------------------------------------- rooms
def staircase(ws, hs):
    """Left-aligned staircase; widths and heights listed top to bottom (Ferrers convention)."""
    n = len(ws)
    ys = [F(0)]
    for hh in reversed(hs):
        ys.append(ys[-1] + hh)        # ys[i] = top of the i-th row from the bottom
    rw = list(reversed(ws))           # widths bottom to top
    P = [(F(0), F(0)), (F(rw[0]), F(0))]
    for i in range(n - 1):
        P += [(F(rw[i]), ys[i + 1]), (F(rw[i + 1]), ys[i + 1])]
    P += [(F(rw[-1]), ys[-1]), (F(0), ys[-1])]
    return P, ys


def ferrers_chain(name, ws, hs, delta=None):
    P, ys = staircase(ws, hs)
    n = len(ws)
    # longitudinal y downward; source run = top row, target = bottom row
    mid = [(hs[j], ws[j]) for j in range(1, n - 1)]
    g1 = ys[n - 1]                    # top of the second row from the top = first gate
    return Chain(name, P, 'y', -1, 0, (0, ws[0]), (0, ws[-1]), mid, g1, 0,
                 ws[0] if delta is None else delta, floor=F(0)), ys


def half_lattice_open(x0, x1, y0, y1):
    pts = []
    x = F(x0) + F(1, 2)
    while x < x1:
        y = F(y0) + F(1, 2)
        while y < y1:
            pts.append((x, y))
            y += F(1, 2)
        x += F(1, 2)
    return pts


def rnd_open(rnd, x0, x1, y0, y1, dens=(31, 97)):
    def q():
        n = rnd.choice(dens)
        return F(rnd.randint(1, n - 1), n)
    return (F(x0) + (F(x1) - F(x0)) * q(), F(y0) + (F(y1) - F(y0)) * q())


rnd = random.Random(173)

# ================================================================== item 1: construction
log('# Item 1: the construction, replayed exactly')
log(' 1a. Many-band named room S8 (W=18): left-aligned staircase, widths top-down (1,2,4,6,8,10,12,16),')
log('     heights (2,1,2,3,4,5,6,3); six middle bands with d_j = u_j/2, so P = 4; delta = 1 (common left side).')
S8, ys8 = ferrers_chain('S8', [1, 2, 4, 6, 8, 10, 12, 16], [2, 1, 2, 3, 4, 5, 6, 3])
check(len(S8.poly) == 18 and S8.P == 4, f'S8 has {len(S8.poly)} walls, P = {S8.P}, 7 gates')
H8 = ys8[-1]
pairs = []
for _ in range(10):
    pairs.append((rnd_open(rnd, 0, 1, H8 - 2, H8, dens=(5, 7, 11, 13)), rnd_open(rnd, 12, 16, 0, 3, dens=(5, 7, 11, 13))))
pairs += [((F(1, 2), H8 - 1), (F(29, 2), F(3, 2))), ((F(1, 2), H8 - F(1, 2)), (F(13), F(1)))]
r = run_pairs(S8, pairs, [False, True], 'S8 direct then floor')
check(r['nbad'] == 0 and r['ngate'] == 0, 'S8: every passing pair replays to T; every gate offset |l(t_j)| < delta')

log(' 1b. Interpolation bound: |l(t)| <= max(|err1|,|err2|) at every t in [0,D], any number of gates (symbolic).')
okI = True
for _ in range(2000):
    e1, e2 = F(rnd.randint(-999, 999), 1000), F(rnd.randint(-999, 999), 1000)
    D = F(rnd.randint(1, 500), rnd.randint(1, 7))
    ts = sorted(F(rnd.randint(0, 10**4), 10**4) * D for _ in range(rnd.randint(1, 40)))
    okI &= all(abs(e1 + (e2 - e1) * t / D) <= max(abs(e1), abs(e2)) for t in ts)
check(okI, '2000 random gate lists (up to 40 gates): linear interpolation stays inside the endpoint errors')

log(' 1c. Torus phrasing equals the coordinate phrasing (theta, alpha, eps as in the note) on 60 S8/Ferrers pairs.')
U1, _ = ferrers_chain('U1', [2, 3, 5, 6], [7, 1, 1, 3])
agree = True
for C, top, tx0, th in [(S8, H8, 12, 3), (U1, 12, 5, 3)]:
    for _ in range(30):
        Sx = rnd_open(rnd, 0, C.src[1], C.g1, top, dens=(7, 11))
        Tt = rnd_open(rnd, tx0, C.tgt[1], 0, th, dens=(7, 11))
        for fl in (False, True):
            agree &= bool(C.solutions(Sx, Tt, fl)[1]) == C.theta_test(Sx, Tt, fl)
check(agree, 'exact test via k*alpha in theta + (-eps1,eps1)x(-eps2,eps2) agrees with |err_i| < delta')

# ================================================================== item 2: relations
log('\n# Item 2: failure requires a short relation; rank-one scalar test')
c25 = 25 / (6 * math.pi ** 2)
log(f'   sum bound 25*sum(j^-2)/pi^4 = 25/(6 pi^2) = {c25:.4f}')
check(c25 < 1 and all((2 * j + 3) ** 2 <= 25 * j * j for j in range(1, 1000)), '(2j+3)^2 <= 25 j^2 for j>=1 and 25/(6pi^2) < 1')


def finite_test(al, th, eps):
    N = lcm(al[0].denominator, al[1].denominator)
    return any(all(dist1(k * al[i] - th[i]) < eps[i] for i in (0, 1)) for k in range(N))


def short_rel(al, eps, bound=2):
    """Least t = max_i eps_i |m_i| over nonzero m with m.alpha integral, searched in the box t < bound."""
    best = None
    M1, M2 = int(bound / eps[0]) + 1, int(bound / eps[1]) + 1
    for m1 in range(0, M1 + 1):
        for m2 in range(-M2, M2 + 1):
            if (m1, m2) <= (0, 0) and not (m1 == 0 and m2 > 0):
                continue
            t = max(eps[0] * abs(m1), eps[1] * abs(m2))
            if t < bound and ((m1 * al[0] + m2 * al[1]).denominator == 1):
                best = t if best is None or t < best else best
    return best


nf = nok = 0
tmax = F(0)
for _ in range(1500):
    al = (F(rnd.randint(0, 59), rnd.randint(1, 60)), F(rnd.randint(0, 59), rnd.randint(1, 60)))
    eps = (F(rnd.randint(1, 50), 200), F(rnd.randint(1, 50), 200))
    th = (F(rnd.randint(0, 999), 1000), F(rnd.randint(0, 999), 1000))
    if not finite_test(al, th, eps):
        nf += 1
        t = short_rel(al, eps)
        nok += t is not None
        if t is not None:
            tmax = max(tmax, t)
check(nf > 0 and nok == nf, f'1500 random rational instances: {nf} failures, each has a nonzero m in L with '
      f'max eps_i|m_i| < 2 (largest least-t seen {float(tmax):.3f})')
log('   Sharpness: alpha=(1/q,0) with eps1 < 1/(2q) misses theta1=1/(2q); the least relation (q,0) has t = q*eps1 < 1/2.')
q = 7
check(not finite_test((F(1, q), F(0)), (F(1, 2 * q), F(0)), (F(1, 2 * q) - F(1, 1000), F(1, 3))),
      'q=7 example fails with t just under 1/2, so the constant 2 in the note is at most 4x from sharp')

log('   Rank-one scalar test against a float orbit (k <= 40000), irrational coordinates:')
s2 = math.sqrt(2)
cases = [('L=Z(3,0)', (1 / 3, s2 - 1), (3, 0)), ('L=Z(2,2)', (s2 - 1, 0.5 - (s2 - 1)), (2, 2))]
ok_r1 = True
nchk = 0
for nm, al, m in cases:
    for _ in range(200):
        th = (rnd.random(), rnd.random())
        eps = (rnd.uniform(0.005, 0.2), rnd.uniform(0.005, 0.2))
        lhs = abs(((m[0] * th[0] + m[1] * th[1]) + 0.5) % 1 - 0.5)
        rhs = abs(m[0]) * eps[0] + abs(m[1]) * eps[1]
        if abs(lhs - rhs) < 2e-3:
            continue
        hit = False
        for k in range(1, 40001):
            if all(abs(((k * al[i] - th[i]) + 0.5) % 1 - 0.5) < eps[i] for i in (0, 1)):
                hit = True
                break
        ok_r1 &= hit == (lhs < rhs)
        nchk += 1
check(ok_r1, f'rank-one test dist(m.theta,Z) < |m1|eps1+|m2|eps2 matches the orbit on {nchk} instances '
      '(including the non-primitive generator (2,2))')

# ================================================================== item 3: named rooms
log('\n# Item 3: the test on named rooms')
log(' 3a. Ferrers residuals (d171): left-wall beam, delta = w, P minimal; direct itinerary, then floor return b -> 2h-b.')
FERRERS = {'U1': ([2, 3, 5, 6], [7, 1, 1, 3]), 'U2': ([1, 2, 3, 4], [13, 2, 1, 4]),
           'U2b': ([1, 2, 3, 5], [1, 2, 1, 4]), 'T1': ([3, 4, 12, 13], [1, 1, 1, 1])}
FCH = {}
for nm, (ws, hs) in FERRERS.items():
    C, ys = ferrers_chain(nm, ws, hs)
    FCH[nm] = C
    w, u, v, W = ws
    c, d, e, h = hs
    H = ys[-1]
    y3 = h + e + d
    src = half_lattice_open(0, w, y3, H)
    tgt = half_lattice_open(v, W, 0, h)
    pairs = [(S, T) for S in src for T in tgt]
    if len(pairs) > 80:
        pairs = rnd.sample(pairs, 80)
    pairs += [(rnd_open(rnd, 0, w, y3, H), rnd_open(rnd, v, W, 0, h)) for _ in range(8)]
    log(f'   {nm}: widths {ws} heights {hs}, P = {C.P}, Ph/W = {C.P * h / W}')
    rd = run_pairs(C, pairs, [False], f'{nm} direct only')
    rf = run_pairs(C, pairs, [False, True], f'{nm} direct or floor')
    check(rd['nbad'] == 0 and rf['nbad'] == 0 and rf['ngate'] == 0, f'{nm}: every passing pair replays exactly to T')
    if rf['failed']:
        S, T = rf['failed'][0]
        b = h - T[1]
        log(f'     first failing pair {S}-{T}: b = {b}, Pb/(2W) = {C.P * b / (2 * W)}, '
            f'P(2h-b)/(2W) = {C.P * (2 * h - b) / (2 * W)}')

log(' 3b. Source phase is free when delta = w and the source run shares the beam side (any x in (0,w), any phase).')
okfree = True
for _ in range(3000):
    x = F(rnd.randint(1, 999), 1000)
    phi = F(rnd.randint(0, 9999), 10000)
    okfree &= dist1(phi - x / 2) < F(1, 2) or dist1(phi + x / 2) < F(1, 2)
check(okfree, 'for theta1 = +-x/(2w), 0<x<w, and eps1 = 1/2 one sign always works: the test is one-dimensional')
log('   So on these rooms the test is: some k with dist(+-z - kPb, 2V Z) < w, i.e. with q = den(Pb/(2V)),')
log('   dist(z, (2V/q) Z) < w. That is the d168/d170 terminal-strip test at the single depth b.')

log(' 3c. Explicit failing lines for the left-wall beam (both itineraries), exact:')
U1c = FCH['U1']
fail_b = [F(2 * j, 5) for j in range(1, 8)]
okl = True
for b in fail_b:
    for z in (F(11, 2), F(51, 10), F(599, 100)):
        S, T = (F(1), F(17, 2)), (z, 3 - b)
        okl &= not U1c.solutions(S, T, False)[1] and not U1c.solutions(S, T, True)[1]
check(okl, 'U1: for b in (2/5)Z (7 lines) every z and both itineraries fail (5b/2 and 15-5b/2 integral)')
U2c = FCH['U2']
okl2 = True
for b in (F(4, 3), F(8, 3)):
    S, T = (F(1, 2), F(15)), (F(7, 2), 4 - b)
    okl2 &= not U2c.solutions(S, T, False)[1] and not U2c.solutions(S, T, True)[1]
b = F(4, 9)
S, T = (F(1, 2), F(15)), (F(15, 4), 4 - b)
okl2 &= not U2c.solutions(S, T, False)[1] and not U2c.solutions(S, T, True)[1]
check(okl2, 'U2: b in {4/3, 8/3} (all z) and b = 4/9 with z = 15/4 fail both itineraries')


def shotA(R_ws, R_hs, S, T):
    """deep-terminal-band (A) floor-return shot, replayed exactly."""
    w, u, v, W = map(F, R_ws)
    c, d, e, h = map(F, R_hs)
    P, ys = staircase(R_ws, R_hs)
    y3 = h + e + d
    x, a = S[0], S[1] - y3
    z, b = T[0], h - T[1]
    B = 2 * h - b
    L = d + e + B
    E = rep(x + a * z / L, 2 * w) / (1 + a / L)
    s = (z - E) / L
    Dt = a + L
    st, pos, con = trace(P, S, (S[0] + s * Dt, S[1] - Dt))
    return st == 'end' and pos == T


okA = all(shotA([2, 3, 5, 6], [7, 1, 1, 3], (F(1), F(17, 2)), (z, 3 - b)) for b in fail_b for z in (F(11, 2), F(599, 100)))
okA &= all(shotA([1, 2, 3, 4], [13, 2, 1, 4], (F(1, 2), F(15)), (z, 4 - b))
           for b, z in ((F(4, 3), F(7, 2)), (F(8, 3), F(7, 2)), (F(4, 9), F(15, 4))))
check(okA, 'the same U1/U2 pairs are lit by the (A) floor-return shot, whose gate offsets exceed w')

log(' 3d. Pyramid leftovers (d172 V1-761, V2-8051, V3-5111) and the 761 V=384 obstruction room.')


def rows_of(nx, ny, mask):
    rows = []
    for j in range(ny):
        cols = [i for i in range(nx) if (mask >> (i + nx * j)) & 1]
        rows.append((cols[0], cols[-1] + 1))
    return rows


def polygon(rows, X, Y):
    pts = []
    for k, (l, r) in enumerate(rows):
        pts += [(X[r], Y[k]), (X[r], Y[k + 1])]
    for k in reversed(range(len(rows))):
        l, r = rows[k]
        pts += [(X[l], Y[k + 1]), (X[l], Y[k])]
    out = []
    for p in pts:
        if not out or out[-1] != p:
            out.append(p)
    if out[0] == out[-1]:
        out.pop()
    changed = True
    while changed:
        changed = False
        for i in range(len(out)):
            a, b, c = out[i - 1], out[i], out[(i + 1) % len(out)]
            if (a[0] == b[0] == c[0]) or (a[1] == b[1] == c[1]) or a == b:
                out.pop(i)
                changed = True
                break
    return out


def cum(g):
    return [F(sum(g[:k])) for k in range(len(g) + 1)]


PYR = {761: (3, 4), 8051: (4, 4), 5111: (4, 4)}
OPEN = {761: [((1, 7), (5, 3))], 8051: [((1, 1), (7, 5)), ((2, 1), (7, 5)), ((3, 1), (7, 5))],
        5111: [((1, 7), (7, 3))]}
LEFT = [('V1-761', 761, (3, 1, 6), (1, 5, 1, 2)), ('V2-8051', 8051, (2, 2, 1, 6), (2, 1, 4, 2)),
        ('V3-5111', 5111, (3, 1, 1, 5), (1, 4, 1, 2))]


def coord(G, k, f):
    return G[k // 2] if k % 2 == 0 else G[k // 2] + (G[k // 2 + 1] - G[k // 2]) * f


for name, mask, gx, gy in LEFT:
    nx, ny = PYR[mask]
    rows = rows_of(nx, ny, mask)
    X, Y = cum(gx), cum(gy)
    poly = polygon(rows, X, Y)
    for S0, T0_ in OPEN[mask]:
        if mask == 8051:
            sr, mr, tr, ldir = 0, 1, 2, 1
        else:
            sr, mr, tr, ldir = 3, 2, 1, -1
        x0 = X[rows[sr][0]]
        assert X[rows[mr][0]] == x0 and X[rows[tr][0]] == x0
        w, u, V = (X[rows[r][1]] - x0 for r in (sr, mr, tr))
        d = gy[mr]
        g1 = Y[sr] if ldir == -1 else Y[sr + 1]
        delta = min(min(w, u), min(u, V))
        C = Chain(name, poly, 'y', ldir, x0, (0, w), (0, V), [(d, u)], g1, 0, delta)
        prs = []
        for _ in range(13):
            f = lambda: F(rnd.randint(1, 96), 97)
            prs.append(((coord(X, S0[0], f()), coord(Y, S0[1], f())), (coord(X, T0_[0], f()), coord(Y, T0_[1], f()))))
        prs[0] = ((coord(X, S0[0], F(1, 2)), coord(Y, S0[1], F(1, 2))), (coord(X, T0_[0], F(1, 2)), coord(Y, T0_[1], F(1, 2))))
        log(f'   {name} pair {S0}-{T0_}: (w,u,V)=({w},{u},{V}) d={d} delta={delta} P={C.P}')
        rr = run_pairs(C, prs, [False], f'{name} {S0}-{T0_} direct')
        check(rr['nbad'] == 0, f'{name} {S0}-{T0_}: every passing pair replays to T')

R761 = [(0, 0), (2, 0), (2, 1), (384, 1), (384, 65), (4, 65), (4, 67), (2, 67), (2, 69), (0, 69)]
R761 = [(F(a), F(b)) for a, b in R761]
S7, T7 = (F(1, 100), F(68)), (F(192), F(33))
fwd = Chain('761fwd', R761, 'y', -1, 0, (0, 2), (0, 384), [(2, 4)], 67, 0, 2)
N, sols, s = fwd.solutions(S7, T7)
log(f'   761 V=384 forward: P={fwd.P}, alpha={fwd.alpha(s)}, N={N}, solutions {len(sols)}')
check(fwd.P == 4 and fwd.alpha(s) == (-1, F(1, 6)) and not sols, 'forward chart: alpha = (-1, 1/6) and the test fails (note)')
# The floor y=1 of the V-run is not a full wall (tooth (0,2)x(0,1)); the cap reflection b=96 is checked as a rotation only.
check(F(4 * 96, 768) == F(1, 2) and math.gcd(192, 384) == 192 and 192 % 384 != 0,
      'cap rotation 4*96/768 = 1/2: multiples of 384 stay 192 from z = 192, so the cap itinerary also fails')
# perpendicular chart: longitudinal -x from T, transverse y-1; runs (0,64) [x in (4,384)], (0,66) [x in (2,4)], (-1,68) [x in (0,2)]
perp = Chain('761perp', R761, 'x', -1, 1, (0, 64), (-1, 68), [(2, 66)], 4, 32, 32)
N, sols, s = perp.solutions(T7, S7)
log(f'   761 V=384 perpendicular (T to S): beam y = 33, delta = 32, P={perp.P}, alpha={perp.alpha(s)}, N={N}, '
    f'solutions {len(sols)}')
okp = False
for sol in best_order(sols, N)[:6]:
    rp = perp.shoot(T7, S7, sol, s)
    if rp['lit'] and rp['gates_ok']:
        okp = True
        log(f'     replay k={rp["k"]}: lit, {rp["n"]} reflections, max gate offset {float(rp["maxell"]):.3f} < 32')
        break
check(okp, '761 V=384: the perpendicular chart passes the test and its constructed shot traces T -> S exactly')

log(' 3e. R22 (d8 rooms.json R22-base): dark pair (0,0)-(2,2).')
CELLS = [(-1, -1), (-1, 0), (0, -2), (0, -1), (0, 0), (0, 1), (1, -3), (1, -2), (1, 1), (1, 2), (2, 1), (2, 2),
         (3, 0), (3, 1), (4, 0)]
cs = set(CELLS)
log('   Vertical sweep from (0,0): source run x in (-1,1) for y in (-1,1); one gate y=1, opening (0,1) with vertices')
log('   at both ends; target run x in (0,4), y in (1,2), T on its far line (b=1). No middle band, so P is free.')
check((-1, 1) not in cs and (1, 0) not in cs and (1, 1) in cs and (0, 1) in cs and (4, 1) not in cs and (-1, 1) not in cs,
      'R22 chain geometry: (0,1) and (1,1) are vertices, run sides are solid')
w, V, a, b = F(2), F(4), F(1), F(1)
# best clearance: base x = 1/2, delta = 1/2. Generic P: L = {m : m1 a/(2w) = m2 b/(2V)} = Z(1,2)
m = (1, 2)
check(F(m[0]) * a / (2 * w) == F(m[1]) * b / (2 * V), 'with P generic, L has rank one, generated by m = (1,2)')
eps = (F(1, 2) / (2 * w), F(1, 2) / (2 * V))
rhs = abs(m[0]) * eps[0] + abs(m[1]) * eps[1]
vals = set()
for X0 in (F(0), F(-2)):               # lifts of x=0 in (-1,1): 0 and 2*(-1)-0
    for Z0 in (F(2), F(-2)):           # lifts of z=2 in (0,4): 2 and -2
        th = ((X0 - F(1, 2)) / (2 * w), (Z0 - F(1, 2)) / (2 * V))
        vals.add(dist1(m[0] * th[0] + m[1] * th[1]))
check(vals == {F(1, 4)} and rhs == F(1, 4), f'R22: dist(m.theta, Z) = 1/4 = |m1|eps1+|m2|eps2 for every lift: '
      'the strict rank-one test fails exactly at equality')
crosses = {(X + 4 * i + Z + 8 * j) / 2 for X in (0, 2) for Z in (2, -2) for i in range(-3, 4) for j in range(-3, 4)}
check(all(F(c).denominator == 1 for c in crosses), 'every single-pass developed line S->T crosses y=1 at an integer x '
      '(a vertex or outside the opening), so the one-gate family has no shot')


def cell_polygon(cells):
    """Boundary of a union of unit cells, as a counter-clockwise vertex list without collinear points."""
    E = set()
    for (x, y) in cells:
        for e in (((x, y), (x + 1, y)), ((x + 1, y), (x + 1, y + 1)), ((x + 1, y + 1), (x, y + 1)), ((x, y + 1), (x, y))):
            if (e[1], e[0]) in E:
                E.remove((e[1], e[0]))
            else:
                E.add(e)
    nxt = dict(E)
    assert len(nxt) == len(E)
    p0 = min(nxt)
    pts, p = [p0], nxt[p0]
    while p != p0:
        pts.append(p)
        p = nxt[p]
    out = [pts[i] for i in range(len(pts))
           if not ((pts[i - 1][0] == pts[i][0] == pts[(i + 1) % len(pts)][0]) or
                   (pts[i - 1][1] == pts[i][1] == pts[(i + 1) % len(pts)][1]))]
    return out


R22P = cell_polygon(CELLS)
R22P = [(F(a), F(b)) for a, b in R22P]
area = sum(R22P[i][0] * R22P[(i + 1) % len(R22P)][1] - R22P[(i + 1) % len(R22P)][0] * R22P[i][1]
           for i in range(len(R22P))) / 2
check(len(R22P) == 22 and area == 15, f'R22 polygon: {len(R22P)} vertices, area {area} = 15 cells')
st, pos, _ = trace(R22P, (F(0), F(0)), (F(2), F(2)))
check(st == 'corner' and pos == (1, 1), f'direct segment (0,0)->(2,2) stops at the vertex {pos}')
# a nearby pair, T' = (2, 19/10): b = 9/10, rank one m = (9,20), RHS = 9/8+20/16 > 1/2, so the test passes for generic P.
Tn = (F(2), F(19, 10))
r22c = Chain('R22-one-gate', R22P, 'y', 1, 0, (-1, 1), (0, 4), [], 1, F(1, 2), F(1, 2), P=F(1, 7))
N, sols, s = r22c.solutions((F(0), F(0)), Tn)
okn = False
for sol in best_order(sols, N)[:6]:
    rp = r22c.shoot((F(0), F(0)), Tn, sol, s)
    if rp['lit'] and rp['gates_ok']:
        okn = True
        break
check(okn, f'control: zero-middle-band chain with P = 1/7 lights (0,0)-(2,19/10) (N={N}, {len(sols)} solutions, '
      f'replay k={rp["k"]}, {rp["n"]} reflections)')

log(f'\nCPU {time.process_time() - T0:.1f}s; FAIL {len(FAIL)}')
