"""d174 review checks for deep-terminal-band.md (snapshot 2026-11-22 1332).

Named explicit rooms only, exact Fraction arithmetic, no searches over rooms.
trace() and Room are copied from d171-review-ferrers-res/checks.py (trace verbatim).
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


rnd = random.Random(174)


# ================================================================== new tests from the note
def prime_power_parts(q):
    out, p = [], 2
    while p * p <= q:
        if q % p == 0:
            pk = 1
            while q % p == 0:
                q //= p; pk *= p
            out.append(pk)
        p += 1
    if q > 1:
        out.append(q)
    return out


def P0(R):
    return lcm(den(R.d / (2 * R.u)), den(R.e / (2 * R.v)))


def An(R):      # note (A): d(W-u) <= (u-w)(e+h) and (d+e)(W-v) <= h(v-w)
    return R.d * (R.W - R.u) <= (R.u - R.w) * (R.e + R.h) and (R.d + R.e) * (R.W - R.v) <= R.h * (R.v - R.w)


def Bp(R):      # note prime-power case: some prime power dividing den(P0 h/W) is >= W/w
    q = den(P0(R) * R.h / R.W)
    return any(pk >= R.W / R.w for pk in prime_power_parts(q))


def Blcm(R):    # common strengthening: q is not lcm(q1,q2) with q1,q2 < W/w
    q = den(P0(R) * R.h / R.W)
    ds = [k for k in range(1, q + 1) if q % k == 0 and k < R.W / R.w]
    return not any(lcm(a, b) == q for a in ds for b in ds)


def alltests(R):
    T = R.transposed()
    return dict(C=R.chord(), A170=R.A(), A170t=T.A(), B=R.B(), Bt=T.B(),
                An=An(R), Ant=An(T), Bp=Bp(R), Bpt=Bp(T))


def opair_marks(R, n_rand, dens=(3, 7, 11, 13)):
    """Half-lattice points strictly inside the open top cell and the open cell (v,W)x(0,h), plus random rational."""
    Ss = [(F(i, 2), F(j, 2)) for i in range(1, int(2 * R.w)) for j in range(int(2 * R.y3) + 1, int(2 * R.H))]
    Ts = [(F(i, 2), F(j, 2)) for i in range(int(2 * R.v) + 1, int(2 * R.W)) for j in range(1, int(2 * R.h))]
    pairs = [(s, t) for s in Ss for t in Ts]
    rp = []
    for _ in range(n_rand):
        q = rnd.choice(dens)
        s = (F(rnd.randint(1, int(R.w) * q - 1), q), R.y3 + F(rnd.randint(1, int(R.c) * q - 1), q))
        q = rnd.choice(dens)
        t = (R.v + F(rnd.randint(1, int(R.W - R.v) * q - 1), q), F(rnd.randint(1, int(R.h) * q - 1), q))
        rp.append((s, t))
    return pairs, rp


def nearest(x, per):
    r = x - per * floor(x / per)
    return r - per if r > per / 2 else r


# ---------------------------------------------------------------- (A) construction
def shotA(R, S, T):
    w, u, v, W, d, e, h, y3 = R.w, R.u, R.v, R.W, R.d, R.e, R.h, R.y3
    x, ys = S
    z, yt = T
    a, b = ys - y3, h - yt
    B = 2 * h - b
    L = d + e + B
    E = nearest(x + a * z / L, 2 * w) / (1 + a / L)
    s = (z - E) / L
    g = (E, ((e + B) * E + d * z) / L, (B * E + (d + e) * z) / L)
    Xf = g[2] + h * (z - g[2]) / B
    Dt = a + L
    return dict(a=a, b=b, B=B, L=L, E=E, s=s, g=g, Xf=Xf, Dt=Dt,
                src_ok=((E - a * s - x) / (2 * w)).denominator == 1)


def runA(R, S, T):
    p = shotA(R, S, T)
    st, pos, con = trace(R.P, S, (S[0] + p['s'] * p['Dt'], S[1] - p['Dt']))
    hcon = [c for c in con if c[1] == 'h']
    gates_ok = abs(p['g'][0]) < R.w and abs(p['g'][1]) < R.u and abs(p['g'][2]) < R.v
    floor_ok = 0 < p['Xf'] < R.W and hcon == [((p['Xf'], F(0)), 'h')]
    ok = st == 'end' and pos == T and gates_ok and floor_ok and p['src_ok']
    return ok, p, st, pos, len(con)


log('# Item 1: floor-return theorem (A)')
# algebra on random rational symbols (no tracing): gate formulas, gate bounds, floor crossing
okf = okb = okx = oks = True
nA = 0
for _ in range(4000):
    w = F(rnd.randint(1, 40), rnd.randint(1, 7)); u = w + F(rnd.randint(1, 40), rnd.randint(1, 7))
    v = u + F(rnd.randint(1, 40), rnd.randint(1, 7)); W = v + F(rnd.randint(1, 40), rnd.randint(1, 7))
    c, d, e, h = (F(rnd.randint(1, 40), rnd.randint(1, 7)) for _ in range(4))
    R = Room('r', w, u, v, W, c, d, e, h)
    x = w * F(rnd.randint(1, 999), 1000); z = v + (W - v) * F(rnd.randint(1, 999), 1000)
    a = c * F(rnd.randint(1, 999), 1000); b = h * F(rnd.randint(1, 999), 1000)
    p = shotA(R, (x, R.y3 + a), (z, h - b))
    E, s, L, B = p['E'], p['s'], p['L'], p['B']
    lin = lambda t: E + s * t
    okf &= (lin(d) == p['g'][1] and lin(d + e) == p['g'][2] and lin(L) == z and p['src_ok']
            and lin(d + e + h) == p['Xf'] and abs(E) < w)
    if An(R):
        nA += 1
        okb &= abs(p['g'][1]) < u and abs(p['g'][2]) < v
        okx &= 0 < p['Xf'] < W
    # equivalences: gate-2 bound <= u  <=>  d(W-u) <= (u-w)(e+B); gate-3 bound <= v <=> (d+e)(W-v) <= B(v-w)
    oks &= ((((e + B) * w + d * W) / L <= u) == (d * (W - u) <= (u - w) * (e + B)))
    oks &= (((B * w + (d + e) * W) / L <= v) == ((d + e) * (W - v) <= B * (v - w)))
check(okf, 'gate formulas E, ((e+B)E+dz)/L, (BE+(d+e)z)/L, source congruence, |E|<w, floor value (4000 random rooms)')
check(oks, 'gate-bound equivalences with B in place of h (4000 random rooms)')
check(okb and okx, f'under (A): |g2|<u, |g3|<v and 0<floor crossing<W ({nA} random rooms satisfying (A))')

U1 = Room('U1', 2, 3, 5, 6, 7, 1, 1, 3)
U2 = Room('U2', 1, 2, 3, 4, 13, 2, 1, 4)
U2b = Room('U2b', 1, 2, 3, 5, 1, 2, 1, 4)
T1 = Room('T1', 3, 4, 12, 13, 1, 1, 1, 1)
E1 = Room('E1', 2, 3, 5, 7, 2, 1, 1, 3)      # equality in the first inequality of (A)
E2 = Room('E2', 1, 2, 3, 5, 1, 1, 1, 2)      # equality in both inequalities of (A)
for R in (U1, U2, E1, E2):
    l1, r1 = R.d * (R.W - R.u), (R.u - R.w) * (R.e + R.h)
    l2, r2 = (R.d + R.e) * (R.W - R.v), R.h * (R.v - R.w)
    log(f'  {R.name} {fr((R.w, R.u, R.v, R.W))}; {fr((R.c, R.d, R.e, R.h))}: (A) {l1}<={r1}, {l2}<={r2}')
check((U1.d * (U1.W - U1.u), (U1.u - U1.w) * (U1.e + U1.h)) == (3, 4) and An(U1), 'U1 satisfies (A): 3<=4, 2<=9 (as note)')
check(An(U2), 'U2 satisfies (A): 4<=5, 3<=8 (as note)')
check(not An(U2b) and not An(T1), '(A) fails on U2b (6>5) and T1 (9>2)')
# note's table shots
for R, S, T, sl, nref in ((U1, (F(1), F(17, 2)), (F(11, 2), F(3, 2)), F(17, 20), 3),
                          (U2, (F(1, 2), F(27, 2)), (F(7, 2), F(2)), F(14, 31), 5)):
    ok, p, st, pos, nc = runA(R, S, T)
    check(ok and p['s'] == sl and nc == nref, f'{R.name} note shot {fr(S)}->{fr(T)}: slope {p["s"]} (note {sl}), '
          f'{nc} reflections (note {nref}), floor at x={p["Xf"]}')
for R in (U1, U2, E1, E2):
    hl, rp = opair_marks(R, 40)
    for lab, pairs in (('half-lattice', hl), ('random rational', rp)):
        res = [runA(R, S, T) for S, T in pairs]
        bad = [(S, T, r[2], r[3]) for (S, T), r in zip(pairs, res) if not r[0]]
        mx = max(r[4] for r in res)
        check(not bad, f'{R.name} {lab}: {len(pairs) - len(bad)}/{len(pairs)} (A) shots end at T, gates strict, '
              f'one floor contact at the predicted x in (0,W), max {mx} reflections')
        for bb in bad[:2]:
            log('     bad', bb)

# control: (A) failing -> the construction can break (not required by the theorem)
hl, rp = opair_marks(T1, 0)
nbad = sum(not runA(T1, S, T)[0] for S, T in hl)
log(f'  control T1 (A fails): {nbad}/{len(hl)} half-lattice (A) shots fail some gate/trace condition')


# ---------------------------------------------------------------- prime-power case
def shotBp(R, S, T, force=None, prefer_floor=False):
    """Theorem-faithful: choose B whose rotation P0*B/(2W) has den >= W/w, the least k>=0 with |Z|<=w,
    then a sign with |X|<w. Returns dict or None."""
    w, W, d, e, h, y3 = R.w, R.W, R.d, R.e, R.h, R.y3
    x, ys = S
    z, yt = T
    a, b = ys - y3, h - yt
    P = P0(R)
    opts = []
    for B in (b, 2 * h - b):
        qB = den(P * B / (2 * W))
        if qB >= W / w:
            opts.append((B, qB))
    if prefer_floor:
        opts = opts[::-1]
    if force:
        opts = [(force[0], None)]
    for B, qB in opts:
        ks = [force[1]] if force else range(qB)
        for k in ks:
            M = k * P
            Z = nearest(z - M * B, 2 * W)
            if Z == W and w >= W:
                pass
            if abs(Z) > w:
                if abs(Z - 2 * W) <= w: Z -= 2 * W
                elif abs(Z + 2 * W) <= w: Z += 2 * W
                else: continue
            for sg in (1, -1):
                X = nearest(sg * x + M * a, 2 * w)
                if abs(X) >= w:
                    continue
                D = a + d + e + B
                return dict(B=B, qB=qB, k=k, M=M, Z=Z, X=X, sg=sg, D=D, a=a, b=b, slope=M + (Z - X) / D)
        if not force:
            return dict(fail='no k with |Z|<=w', B=B, qB=qB)
    return None


def runBp(R, S, T, force=None, prefer_floor=False):
    p = shotBp(R, S, T, force, prefer_floor)
    if p is None or 'fail' in p:
        return False, p, 'nocand', None, 0, False
    w, d, e, h = R.w, R.d, R.e, R.h
    dx = p['sg'] * p['slope']
    st, pos, con = trace(R.P, S, (S[0] + dx * p['D'], S[1] - p['D']))
    early = False
    if st == 'corner' and p['B'] != p['b']:
        # note: stop at vertical travel a+d+e+b (mirror point of the reflected target through the floor corner)
        D2 = p['a'] + d + e + p['b']
        st, pos, con = trace(R.P, S, (S[0] + dx * D2, S[1] - D2))
        early = True
    a, D, X, Z = p['a'], p['D'], p['X'], p['Z']
    gates = [X + tau * (Z - X) / D for tau in (a, a + d, a + d + e)]
    ok = st == 'end' and pos == T and all(abs(g) < w for g in gates)
    return ok, p, st, pos, len(con), early


log('\n# Item 2: prime-power equality case of the terminal strip test')
# algebra: if p^k | lcm(q1,q2) then p^k | q1 or q2; den(r1+r2) | lcm(q1,q2)
okl = all((lcm(q1, q2) % pk != 0) or (q1 % pk == 0) or (q2 % pk == 0)
          for q1 in range(1, 80) for q2 in range(1, 80) for pk in (2, 3, 4, 5, 7, 8, 9, 11, 13, 16, 25, 27, 49))
check(okl, 'a prime power dividing lcm(q1,q2) divides q1 or q2 (q1,q2<80)')
oks = all(lcm(F(p1, q1).denominator, F(p2, q2).denominator) % (F(p1, q1) + F(p2, q2)).denominator == 0
          for q1 in range(1, 30) for q2 in range(1, 30) for p1 in range(q1) for p2 in range(0, q2, 3))
check(oks, 'den(r1+r2) divides lcm(den r1, den r2) (q<30)')
# spacing: multiples of p/q mod 1 have spacing 1/q, so closed cover with |Z|<=w iff 2W/q <= 2w
okc = True
for W, w, q in ((5, 1, 5), (13, 3, 13), (10, 2, 5), (12, 3, 4)):
    pts = sorted({F(2 * W * j, q) for j in range(q)})
    gap = max([pts[i + 1] - pts[i] for i in range(len(pts) - 1)] + [2 * W - pts[-1] + pts[0]])
    okc &= (gap <= 2 * w) == (q >= F(W, w))
check(okc, 'spacing 2W/q <= 2w iff q >= W/w (named (W,w,q) incl. equality 5/1 and 10/2)')
# strict gates with |Z| = w
okg = True
for _ in range(2000):
    w = F(rnd.randint(1, 30), rnd.randint(1, 5)); X = w * F(rnd.randint(-999, 999), 1000)
    Z = w * rnd.choice((1, -1)); D = F(rnd.randint(2, 300), rnd.randint(1, 5)); tau = D * F(rnd.randint(1, 999), 1000)
    okg &= abs(X + tau * (Z - X) / D) < w
check(okg, 'gate values X+tau(Z-X)/D are strictly inside (-w,w) for |X|<w, |Z|=w, 0<tau<D (2000 random)')
# the two signs cannot both give a representative at +-w
okr = all(not ((nearest(F(i, 7) + F(j, 3), 2) in (1, -1)) and (nearest(-F(i, 7) + F(j, 3), 2) in (1, -1)))
          for i in range(1, 7) for j in range(-30, 31))
check(okr, 'w=1, 0<x<1: x+Ma and -x+Ma are never both at the boundary +-w (x=i/7, Ma=j/3)')

for R in (U2b, T1):
    q = den(P0(R) * R.h / R.W)
    log(f'  {R.name}: P0={P0(R)}, P0 h/W={P0(R) * R.h / R.W}, q={q}, prime powers {prime_power_parts(q)}, '
        f'W/w={R.W / R.w}, floor(W/w)^2={floor(R.W / R.w) ** 2}: Bp={Bp(R)} B(d168)={R.B()}')
check(Bp(U2b) and not U2b.B() and P0(U2b) == 6 and P0(U2b) * U2b.h / U2b.W == F(24, 5), 'U2b: P=6, Ph/W=24/5, 5=W/w; prime-power case holds, d168 B fails')
check(Bp(T1) and not T1.B(), 'T1: q=13 >= 13/3, so the prime-power case covers T1 (note attributes T1 only to d170 transpose)')

# note's U2b shot
S, T = (F(1, 2), F(15, 2)), (F(4), F(7, 3))
ok, p, st, pos, nc, early = runBp(U2b, S, T, force=(F(19, 3), 3))
check(ok and p['M'] == 18 and p['Z'] == 0 and p['sg'] * p['slope'] == F(1065, 59) and nc == 57,
      f'U2b note shot: b=5/3, B=19/3, M={p["M"]}, Z={p["Z"]}, dx/descent={p["sg"] * p["slope"]}, {nc} reflections (note 1065/59, 57)')
for R in (U2b, T1):
    hl, rp = opair_marks(R, 40)
    for lab, pairs in (('half-lattice', hl), ('random rational', rp)):
        for pf in (False, True):
            res = [runBp(R, S, T, prefer_floor=pf) for S, T in pairs]
            bad = [(S, T, r[2], r[3], r[1]) for (S, T), r in zip(pairs, res) if not r[0]]
            mx = max(r[4] for r in res)
            nfl = sum(1 for r in res if r[1] and r[1].get('B') != r[1].get('b'))
            ne = sum(1 for r in res if r[5])
            check(not bad, f'{R.name} {lab}{" (floor route preferred)" if pf else ""}: {len(pairs) - len(bad)}/{len(pairs)} '
                  f'prime-power shots end at T ({nfl} floor routes, {ne} early stops at a floor-corner aim, max {mx} reflections)')
            for bb in bad[:2]:
                log('     bad', bb)

# floor-corner aim, constructed explicitly in U2b. M=30 makes Mh = 0 mod W; b=1/5 makes MB = -6 mod 10.
# Solve the floor value X + Mh + lam(Z-X) = jW for Z, with lam=(a+d+e+h)/D, then z = Z + MB mod 2W.
R = U2b
S = (F(1, 2), F(15, 2)); a = F(1, 2); b = F(1, 5); B = 2 * R.h - b; M = 30; D = a + R.d + R.e + B
lam = (a + R.d + R.e + R.h) / D
cases = []
for sg in (1, -1):
    X = nearest(sg * S[0] + M * a, 2 * R.w)
    if abs(X) >= R.w:
        continue
    for j in range(int(M * R.h / R.W) - 3, int(M * R.h / R.W) + 4):
        Z = X + (j * R.W - X - M * R.h) / lam
        z = (Z + M * B) % (2 * R.W)
        if abs(Z) <= R.w and R.v < z < R.W:
            cases.append((sg, X, Z, z, j))
log(f'  U2b floor-corner aims, M=30, b=1/5: {[(c[0], str(c[1]), str(c[2]), str(c[3]), c[4]) for c in cases]}')
okcorner = bool(cases)
for sg, X, Z, z, j in cases:
    T = (z, R.h - b)
    slope = M + (Z - X) / D
    gates = [X + tau * (Z - X) / D for tau in (a, a + R.d, a + R.d + R.e)]
    st, pos, con = trace(R.P, S, (S[0] + sg * slope * D, S[1] - D))
    D2 = a + R.d + R.e + b
    st2, pos2, con2 = trace(R.P, S, (S[0] + sg * slope * D2, S[1] - D2))
    log(f'    sign {sg}, X={X}, Z={Z}, z={z}: gates {[str(g) for g in gates]}; full trace {st} at {fr(pos)}; '
        f'truncated trace {st2} at {fr(pos2)}, {len(con2)} reflections')
    okcorner &= (st == 'corner' and pos[1] == 0 and st2 == 'end' and pos2 == T and all(abs(g) < R.w for g in gates))
check(okcorner, 'U2b: when the line aims at a floor corner, the truncated path (travel a+d+e+b) already ends at T')

# incomparability of B (d168) and Bp
Wx, wx, qx = 60, 8, 60
check(qx > floor(F(Wx, wx)) ** 2 and not any(pk >= F(Wx, wx) for pk in prime_power_parts(qx)),
      'B and Bp are incomparable: W=60, w=8, q=60 passes B (60>49) but every prime power (4,3,5) is < 7.5')
check(Bp(U2b) and not U2b.B(), 'and U2b passes Bp but not B')
okL = True
for W in range(2, 60):
    for w in range(1, W):
        for q in [k for k in range(1, W + 1) if W % k == 0]:
            Bq = q > floor(F(W, w)) ** 2
            Bpq = any(pk >= F(W, w) for pk in prime_power_parts(q))
            ds = [k for k in range(1, q + 1) if q % k == 0 and k < F(W, w)]
            Lq = not any(lcm(x, y) == q for x in ds for y in ds)
            okL &= ((Bq or Bpq) <= Lq)
check(okL, 'the lcm test (q is not lcm(q1,q2) with q1,q2 < W/w) implies-from both B and Bp (W<60)')


# ================================================================== item 4: coverage
log('\n# Item 4: coverage of LLLLLRLRLR by C, A170, A170t, B, Bt, An, Ant, Bp, Bpt')
# closed forms of the transposed new tests, and threshold forms in W and c
okt = okw = okc = okf = True
for _ in range(4000):
    w = F(rnd.randint(1, 40), rnd.randint(1, 7)); u = w + F(rnd.randint(1, 40), rnd.randint(1, 7))
    v = u + F(rnd.randint(1, 40), rnd.randint(1, 7)); W = v + F(rnd.randint(1, 40), rnd.randint(1, 7))
    c, d, e, h = (F(rnd.randint(1, 40), rnd.randint(1, 7)) for _ in range(4))
    R = Room('r', w, u, v, W, c, d, e, h)
    T = R.transposed()
    okt &= An(T) == ((v - u) * (c + d) <= e * u and (v - w) * c <= w * (d + e))
    Wstar = max(u + (u - w) * (e + h) / d, v + h * (v - w) / (d + e))      # An holds iff W <= min(...)
    Wmin = min(u + (u - w) * (e + h) / d, v + h * (v - w) / (d + e))
    okw &= An(R) == (W <= Wmin)
    cmin = min(e * u / (v - u) - d, w * (d + e) / (v - w))
    okc &= An(T) == (c <= cmin)
    okf &= (R.chord(), R.A(), T.A()) == (Room('r', w, u, v, W + 17, c + 5, d, e, h).chord(),
                                         Room('r', w, u, v, W + 17, c + 5, d, e, h).A(),
                                         Room('r', w, u, v, W + 17, c + 5, d, e, h).transposed().A())
check(okt, 'An transposed = (v-u)(c+d) <= eu and (v-w)c <= w(d+e) (4000 random rooms)')
check(okw, 'An holds iff W <= min{u+(u-w)(e+h)/d, v+h(v-w)/(d+e)} (4000 random rooms)')
check(okc, 'An transposed holds iff c <= min{eu/(v-u)-d, w(d+e)/(v-w)} (4000 random rooms)')
check(okf, 'C, A170, A170t do not depend on W or c (4000 random rooms)')

O1 = Room('O1', 2, 3, 4, 5, 1, 1, 1, 5)
O2 = Room('O2', 2, 3, 4, 6, 2, 1, 1, 2)
S1 = Room('S1', 2, 3, 4, 6, 3, 1, 3, 2)
N1 = Room('N1', 1, 2, 3, 4, 1, 1, 1, 1)
D17 = Room('D17', 3, 4, 9, 12, 3, 4, 2, 3)
RES = Room('RES', 10, 11, 13, 100, 87, 2, 1, 10)
U1b = Room('U1b', 2, 3, 5, 9, 1, 1, 1, 3)
G1 = Room('G2860', 10, 11, 13, 2860, 2847, 2, 1, 10)
V1 = Room('V1', 2, 3, 5, 9, 3, 1, 1, 3)
V2 = Room('V2', 1, 2, 3, 6, 3, 2, 1, 4)
keys = ['C', 'A170', 'A170t', 'B', 'Bt', 'An', 'Ant', 'Bp', 'Bpt']
log('  room   widths; heights          ' + ' '.join(f'{k:>5s}' for k in keys))
TT = {}
for R in (O1, O2, S1, N1, D17, RES, T1, U1, U1b, U2, U2b, G1, V1, V2):
    t = alltests(R); TT[R.name] = t
    log(f'  {R.name:6s} {fr((R.w, R.u, R.v, R.W)) + "; " + fr((R.c, R.d, R.e, R.h)):24s} ' +
        ' '.join(f'{int(t[k]):>5d}' for k in keys))
check(TT['U1']['An'] and TT['U2']['An'] and TT['U2b']['Bp'] and TT['T1']['Bp'],
      'U1, U2 covered by (A); U2b, T1 covered by the prime-power case (no transpose needed)')
check(not any(TT['RES'].values()), 'RES still fails every test (covered only by the d171 certificate)')
for nm in ('G2860', 'V1', 'V2'):
    check(not any(TT[nm].values()), f'{nm} fails all nine tests (both orientations, with and without transposes)')
# V1 derivation: q = 1 in both orientations
for R in (V1, V2, G1):
    Tr = R.transposed()
    log(f'  {R.name}: P0={P0(R)}, q=den(P0 h/W)={den(P0(R) * R.h / R.W)}; transposed P0={P0(Tr)}, '
        f'q={den(P0(Tr) * Tr.h / Tr.W)}; An first ineq {R.d * (R.W - R.u)}>{(R.u - R.w) * (R.e + R.h)}, '
        f'Ant first ineq {(R.v - R.u) * (R.c + R.d)}>{R.e * R.u}')
okfam = all(not any(alltests(Room('f', 2, 3, 5, 90 * m, 40 * n - 5, 1, 1, 3)).values())
            for m in range(1, 6) for n in range(1, 6))
check(okfam, 'family (2,3,5,90m; 40n-5,1,1,3) fails all nine tests, m,n = 1..5 (q=m, transposed q=n)')
okfam2 = all(not any(alltests(Room('g', 10, 11, 13, 2860 * k, 2860 * k - 13, 2, 1, 10)).values()) for k in range(1, 6))
check(okfam2, "note's grid (0,10,11,13,2860k), k=1..5, fails all nine tests")
# a sample V1 pair at b=3/2: both rotations have denominator 2 < W/w, so the strip test is silent there.
S, T = (F(1), F(13, 2)), (F(7), F(3, 2))
rb = [P0(V1) * B / (2 * V1.W) for B in (F(3, 2), 2 * V1.h - F(3, 2))]
ok, p, st, pos, nc = runA(V1, S, T)
log(f'  control V1 pair {fr(S)}-{fr(T)}: rotations {[str(r) for r in rb]} (dens < 9/2); the (A) shot still has gates '
    f'{[str(g) for g in p["g"]]} inside (2,3,5) and traces {st} at {fr(pos)}: tests are sufficient only')

# ================================================================== side check: the note's smallest-open-word polygon
Pw = [(2, 0), (4, 0), (4, 1), (3, 1), (3, 4), (0, 4), (0, 3), (1, 3), (1, 2), (2, 2)]
n = len(Pw)
area2 = sum(Pw[i][0] * Pw[(i + 1) % n][1] - Pw[(i + 1) % n][0] * Pw[i][1] for i in range(n))
word = ''
for i in range(n):
    p0, p1, p2 = Pw[i - 1], Pw[i], Pw[(i + 1) % n]
    cr = (p1[0] - p0[0]) * (p2[1] - p1[1]) - (p1[1] - p0[1]) * (p2[0] - p1[0])
    word += 'L' if cr * area2 > 0 else 'R'
rots = {word[i:] + word[:i] for i in range(n)}
check('LLLRLLLRLR' in rots, f'note polygon has turn word {word} (cyclic class contains LLLRLLLRLR), area {area2 // 2}')

log(f'\n{len(FAIL)} FAIL; CPU {time.process_time() - T0:.1f} s')
