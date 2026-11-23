"""d170 review checks for ferrers-two-windings.md (snapshot 2026-11-22 0835).

Named explicit rooms only, exact Fraction arithmetic, no searches.
trace() is copied verbatim from d168-review-ferrers/checks.py (from d167 / d164).
Run: python3 -B checks.py > checks.log
"""
import random
import time
from fractions import Fraction as F
from math import gcd, floor

T0 = time.process_time()
FAIL = []


def log(*a):
    print(*a, flush=True)


def check(ok, msg):
    log(('  PASS ' if ok else '  FAIL ') + msg)
    if not ok:
        FAIL.append(msg)


# ------------------------------------------------------------------ copied verbatim from d168
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


def nearest(q):
    return floor(q + F(1, 2))


class Room:
    """Left-attached runs, widths w<u<v<W top to bottom, heights c,d,e,h top to bottom (as d168)."""

    def __init__(self, name, w, u, v, W, c, d, e, h):
        self.name = name
        self.w, self.u, self.v, self.W = map(F, (w, u, v, W))
        self.c, self.d, self.e, self.h = map(F, (c, d, e, h))
        y1, y2, y3, H = self.h, self.h + self.e, self.h + self.e + self.d, self.h + self.e + self.d + self.c
        self.y2, self.y3, self.H = y2, y3, H
        self.P = [(0, 0), (W, 0), (W, y1), (v, y1), (v, y2), (u, y2), (u, y3), (w, y3), (w, H), (0, H)]

    def transposed(self):
        w, u, v, W, c, d, e, h = self.w, self.u, self.v, self.W, self.c, self.d, self.e, self.h
        return Room(self.name + "'", h, e + h, d + e + h, c + d + e + h, W - v, v - u, u - w, w)

    def cond1(self):
        w, u, v, d, e, h = self.w, self.u, self.v, self.d, self.e, self.h
        return w * (e + h) <= u * d, (u + w) * h * (e + h) <= v * e * (d + e + h)

    def d170(self):
        return all(self.cond1())

    def d168(self):
        P0 = lcm(den(self.d / (2 * self.u)), den(self.e / (2 * self.v)))
        return den(P0 * self.h / self.W) > floor(self.W / self.w) ** 2

    def shot(self, S, T):
        """The note's construction. Returns data dict incl. physical direction (dx, dy)."""
        w, u, v, d, e = self.w, self.u, self.v, self.d, self.e
        x, ys = S
        z, yt = T
        a, b = ys - self.y3, self.h - yt
        L = d + e + b
        D = a + L
        j = nearest(e * z / (2 * v * b))
        i0 = d * (z + 2 * v * j) / (2 * u * (e + b))
        i = nearest(i0)
        M = (z + 2 * u * i + 2 * v * j) / L
        R1 = d * M - 2 * u * i
        R2 = (d + e) * M - 2 * u * i - 2 * v * j
        X = (x + M * a + w) % (2 * w) - w
        Mp = M - X / D
        g1, g2, g3 = X * L / D, R1 + X * (e + b) / D, R2 + X * b / D
        return dict(a=a, b=b, L=L, D=D, i=i, j=j, i0=i0, M=M, R1=R1, R2=R2, X=X, Mp=Mp,
                    g=(g1, g2, g3), dir=(Mp * D, -D))


def fr(p):
    return '(' + ','.join(str(c) for c in p) + ')'


def replay(R, S, T, joints=False):
    s = R.shot(S, T)
    w, u, v, d, e, b, L = R.w, R.u, R.v, R.d, R.e, s['b'], s['L']
    bounds = (abs(s['R1']) <= u * (e + b) / L and abs(s['R2']) <= v * b / (e + b) + u * b / L
              and abs(s['R2'] - (e * T[0] - 2 * v * b * s['j']) / (e + b) - (-2 * u * b / L) * (s['i'] - s['i0'])) == 0)
    gates = abs(s['g'][0]) < w and abs(s['g'][1]) < u and abs(s['g'][2]) < v
    dx, dy = s['dir']
    st, pos, con = trace(R.P, S, (S[0] + dx, S[1] + dy))
    ok = st == 'end' and pos == T
    jok = True
    if joints:  # physical crossing abscissae equal |gate| at each joint
        for t, gv in zip((s['a'], s['a'] + d, s['a'] + d + e), s['g']):
            st2, p2, _ = trace(R.P, S, (S[0] + dx * t / s['D'], S[1] + dy * t / s['D']))
            jok &= st2 in ('end', 'wall-end') and p2[0] == abs(gv)  # wall-end: gate 0, smooth contact with x=0
    return ok and bounds and gates and jok, s, st, pos, len(con)


def marks(R, rnd, n_rand, srcs=None, tgts=None, dens=(7, 11, 13, 97, 101, 1009)):
    w, v, W, h, y3, H = R.w, R.v, R.W, R.h, R.y3, R.H
    Ss = srcs or [(F(2 * i + 1, 2), F(2 * j + 1, 2)) for i in range(int(w)) for j in range(int(y3), int(H))]
    Ts = tgts or [(F(2 * i + 1, 2), F(2 * j + 1, 2)) for i in range(int(v), int(W)) for j in range(int(h))]
    pairs = [(s_, t_) for s_ in Ss for t_ in Ts]
    for _ in range(n_rand):
        q = rnd.choice(dens)
        s_ = (F(rnd.randint(1, int(w) * q - 1), q), y3 + F(rnd.randint(1, int(H - y3) * q - 1), q))
        q = rnd.choice(dens)
        t_ = (v + F(rnd.randint(1, int(W - v) * q - 1), q), F(rnd.randint(1, int(h) * q - 1), q))
        pairs.append((s_, t_))
    return pairs


def run_room(R, pairs, label):
    nok, mx, bad = 0, 0, []
    for S, T in pairs:
        ok, s, st, pos, n = replay(R, S, T, joints=True)
        nok += ok
        mx = max(mx, n)
        if not ok:
            bad.append((S, T, st, pos))
    check(nok == len(pairs), f'{label}: construction + exact trace reaches T, gates and bounds hold, joint '
          f'abscissae = |gate|, for {nok}/{len(pairs)} pairs (max {mx} reflections)')
    for S, T, st, pos in bad[:3]:
        log(f'     bad {fr(S)}-{fr(T)}: {st} at {fr(pos)}')


rnd = random.Random(170)

# ================================================================== item 1: algebra
log('# Item 1: proof identities on 3000 random rational instances')
ok_id = ok_b = ok_mono = True
for _ in range(3000):
    w, u, v = sorted(rnd.sample(range(1, 60), 3))
    d, e, hh = (F(rnd.randint(1, 40), rnd.randint(1, 7)) for _ in range(3))
    b = hh * F(rnd.randint(1, 99), 100)
    z = F(rnd.randint(1, 999), 7)
    j = rnd.randint(-50, 50)
    L = d + e + b
    i0 = d * (z + 2 * v * j) / (2 * u * (e + b))
    for i in (i0, i0 + F(rnd.randint(-9, 9), 7)):
        M = (z + 2 * u * i + 2 * v * j) / L
        R1, R2 = d * M - 2 * u * i, (d + e) * M - 2 * u * i - 2 * v * j
        ok_id &= L * M - 2 * u * i - 2 * v * j == z
        ok_id &= R1 == -2 * u * (e + b) / L * (i - i0)
        ok_id &= R2 == (e * z - 2 * v * b * j) / (e + b) - 2 * u * b / L * (i - i0)
    a = F(rnd.randint(1, 99), 3)
    D = a + L
    ok_b &= (u + w) * (e + b) / L <= u if w * (e + b) <= u * d else (u + w) * (e + b) / L > u
    lhs = v * b / (e + b) + (u + w) * b / L
    ok_b &= (lhs <= v) == ((u + w) * b * (e + b) <= v * e * L)
    b2 = b + F(1, 1000)
    ok_mono &= b * (e + b) / (d + e + b) < b2 * (e + b2) / (d + e + b2)
check(ok_id, 'LM-2ui-2vj = z; R1 = -2u(e+b)(i-i0)/L; R2 = (ez-2vbj)/(e+b) - 2ub(i-i0)/L')
check(ok_b, 'gate tests: (u+w)(e+b)/L<=u iff w(e+b)<=ud; vb/(e+b)+(u+w)b/L<=v iff (u+w)b(e+b)<=veL')
check(ok_mono, 'b(e+b)/(d+e+b) strictly increasing in b')
ok_c = True
for _ in range(2000):
    X = F(rnd.randint(-100, 100), 100) * 5
    a, d, e, b = (F(rnd.randint(1, 60), rnd.randint(1, 9)) for _ in range(4))
    D, M, x0 = a + d + e + b, F(rnd.randint(-999, 999), 13), F(rnd.randint(-99, 99), 7)
    s = lambda t: (X - M * a) + t * (M - X / D)
    ok_c &= s(a) == X * (d + e + b) / D and s(a + d) - d * M == X * (e + b) / D
    ok_c &= s(a + d + e) - (d + e) * M == X * b / D and s(D) - (d + e + b) * M == 0
check(ok_c, 'source correction: X(1-t/D) gives XL/D, X(e+b)/D, Xb/D at joints, 0 at target')

# ================================================================== item 2: exact replays
log('# Item 2: named rooms')
G = Room('G grid (0,2,10,23,230)', 2, 10, 23, 230, 207, 13, 8, 2)
N1 = Room('N1 ledger (1,2,3,4; 1,1,1,1)', 1, 2, 3, 4, 1, 1, 1, 1)
N2 = Room('N2 d17 (3,4,9,12; 3,4,2,3)', 3, 4, 9, 12, 3, 4, 2, 3)
A1 = Room('A1 (1,3,5,7; 1,2,1,1)', 1, 3, 5, 7, 1, 2, 1, 1)
A2 = Room('A2 (2,5,9,12; 2,3,2,2)', 2, 5, 9, 12, 2, 3, 2, 2)
T1 = Room('T1 (3,4,12,13; 1,1,1,1)', 3, 4, 12, 13, 1, 1, 1, 1)
RES = Room('RES grid (0,10,11,13,100)', 10, 11, 13, 100, 87, 2, 1, 10)
R1 = Room('R1 (2,3,4,5; 1,1,1,1)', 2, 3, 4, 5, 1, 1, 1, 1)
for R in (G, N1, N2, A1, A2, T1, RES, R1):
    Rt = R.transposed()
    log(f'   {R.name}: (1) direct {R.cond1()} transposed {Rt.cond1()}; d168 direct {R.d168()} transposed {Rt.d168()}')
check(G.d170() and G.cond1() == (True, True) and 2 * 10 == 20 and 12 * 2 * 10 == 240 and 23 * 8 * 23 == 4232,
      'G satisfies (1): 20<=130, 240<=4232')
check(N1.d170() and N1.w * (N1.e + N1.h) == N1.u * N1.d, 'N1 satisfies (1) with EQUALITY in the first test (2=2)')
check(N2.d170(), 'N2 satisfies (1): 15<=16, 105<=162')
check(A1.d170() and A2.d170(), 'A1, A2 satisfy (1)')
check(not T1.d170() and T1.transposed().d170(), 'T1 fails (1) directly, passes transposed (second test with equality 36=36)')
check(not RES.d170() and not RES.transposed().d170() and not RES.d168() and not RES.transposed().d168(),
      'RES fails d170 and d168 in both orientations')

log('## G: the note pair (1,115)-(115,1)')
ok, s, st, pos, n = replay(G, (F(1), F(115)), (F(115), F(1)), joints=True)
check(ok and s['j'] == 20 and s['i'] == 75 and s['M'] == F(2535, 22) and s['X'] == F(21, 11) and s['Mp'] == F(2189, 19),
      f"G note pair: j={s['j']} i={s['i']} M={s['M']} X={s['X']} slope={s['Mp']}, trace {st} at {fr(pos)}")
check(n == 5490, f'G note pair: {n} side reflections (note says 5,490)')
log(f"   gates {[str(g) for g in s['g']]} vs widths 2,10,23")

t0 = time.process_time()
Gs = [(F(1, 2), F(47, 2)), (F(3, 2), F(49, 2)), (F(1, 2), F(121, 2)), (F(3, 2), F(231, 2))]
Gt = [(F(47, 2), F(1, 2)), (F(231, 2), F(3, 2)), (F(459, 2), F(1, 2)), (F(459, 2), F(3, 2))]
pairs = [(a_, b_) for a_ in Gs for b_ in Gt]
for _ in range(6):
    q = rnd.choice((3, 7, 11))
    pairs.append(((F(rnd.randint(1, 2 * q - 1), q), 23 + F(rnd.randint(1, 30 * q), q)),
                  (23 + F(rnd.randint(1, 207 * q - 1), q), F(rnd.randint(q // 2 + 1, 2 * q - 1), q))))
run_room(G, pairs, 'G 16 half-lattice + 6 random rational pairs')
log(f'   G CPU {time.process_time() - t0:.1f}s')

for R in (N1, N2, A1, A2):
    run_room(R, marks(R, rnd, 10), f'{R.name}: all half-lattice open-pair marks + 10 random')

log('## T1 via the transpose')
T1t = T1.transposed()
pairs = marks(T1t, rnd, 10)
run_room(T1t, pairs, f'{T1t.name} (transposed frame)')
okb = True
for S, T in pairs:  # map back: path from T^swap to S^swap in T1
    s = T1t.shot(S, T)
    dx, dy = s['dir']
    Sb, Tb = (S[1], S[0]), (T[1], T[0])  # Sb in T1's bottom-right cell, Tb in T1's top cell
    st, pos, _ = trace(T1.P, Sb, (Sb[0] + dy, Sb[1] + dx))
    okb &= st == 'end' and pos == Tb
check(okb, f'T1 original frame: all {len(pairs)} mapped shots go from the bottom-right mark to the top mark')

log('## Control: construction where (1) fails')
for R, S, T in ((RES, (F(5), F(55)), (F(55), F(5))), (R1, (F(1, 2), F(7, 2)), (F(9, 2), F(1, 2)))):
    ok, s, st, pos, n = replay(R, S, T)
    log(f"   {R.name} {fr(S)}-{fr(T)}: gates {[str(g) for g in s['g']]} widths {R.w},{R.u},{R.v}; trace {st} at {fr(pos)}")
cnt = sum(replay(RES, S, T)[0] for S, T in marks(RES, rnd, 0, tgts=[(F(55), F(5)), (F(201, 2), F(19, 2))],
                                                        srcs=[(F(i, 2), F(j, 2)) for i in (1, 9, 19) for j in (27, 55, 199)]))
log(f'   RES: nearest-rounding shot succeeds for {cnt}/18 named pairs')

# ================================================================== item 3: coverage
log('# Item 3: coverage of named rooms by d168 u d170 (both orientations)')
NAMED = [G, N1, N2, A1, A2, T1, RES, R1,
         Room('R2', 2, 3, 4, 5, 2, 6, 8, 2), Room('R3', 3, 4, 5, 7, 1, 2, 1, 3), Room('R4', 3, 5, 6, 8, 1, 2, 4, 1),
         Room('O1 (2,3,4,5; 1,1,1,5)', 2, 3, 4, 5, 1, 1, 1, 5), Room('O2 grid (0,2,3,4,6)', 2, 3, 4, 6, 2, 1, 1, 2)]
for R in NAMED:
    Rt = R.transposed()
    flags = dict(d168=R.d168(), d168T=Rt.d168(), d170=R.d170(), d170T=Rt.d170())
    log(f'   {R.name}: {flags} -> {"COVERED" if any(flags.values()) else "OUTSIDE"}')
ok_cf = True
for _ in range(3000):  # closed form of the transposed test
    w, u, v, W = sorted(rnd.sample(range(1, 40), 4))
    c, d, e, h = (rnd.randint(1, 30) for _ in range(4))
    R = Room('', w, u, v, W, c, d, e, h)
    cf = (h * u <= (e + h) * (v - u), (e + 2 * h) * w * u <= (d + e + h) * (u - w) * v)
    ok_cf &= R.transposed().cond1() == cf
check(ok_cf, "transposed (1) == [hu <= (e+h)(v-u), (e+2h)wu <= v(u-w)(d+e+h)] (3000 random rooms)")
for nm in ('O1 (2,3,4,5; 1,1,1,5)', 'O2 grid (0,2,3,4,6)'):
    R = [r for r in NAMED if r.name == nm][0]
    check(not (R.d168() or R.transposed().d168() or R.d170() or R.transposed().d170()), f'{nm} is OUTSIDE d168 u d170')

log(f'\n## done: {len(FAIL)} failures {FAIL}; CPU {time.process_time() - T0:.1f}s')
