"""D124: exact checks for qclass-closure/bbbb/effective-chamber.md.

Own code. Exact arithmetic only: Fraction, and a small Q(sqrt5) field for the
irrational slope alpha = 1/phi^2 = (3 - sqrt5)/2. Named rooms only (DBas,
DB55, DBw2 from d110 geom.ROOMS). No search over rooms, rays, directions or
reflection words: every slope used is alpha itself or the root the note's
construction prescribes.
"""
import sys
import time
from fractions import Fraction as Fr
from math import isqrt

T0 = time.process_time()


def log(*a):
    print(*a)
    sys.stdout.flush()


# ---------------------------------------------------------------- Q(sqrt5)
class Q5:
    __slots__ = ('a', 'b')  # a + b*sqrt5

    def __init__(self, a, b=0):
        self.a, self.b = Fr(a), Fr(b)

    @staticmethod
    def c(x):
        return x if isinstance(x, Q5) else Q5(x)

    def __add__(s, o):
        o = Q5.c(o); return Q5(s.a + o.a, s.b + o.b)
    __radd__ = __add__

    def __neg__(s):
        return Q5(-s.a, -s.b)

    def __sub__(s, o):
        return s + (-Q5.c(o))

    def __rsub__(s, o):
        return Q5.c(o) - s

    def __mul__(s, o):
        o = Q5.c(o); return Q5(s.a * o.a + 5 * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__

    def __truediv__(s, o):
        o = Q5.c(o)
        n = o.a * o.a - 5 * o.b * o.b
        return s * Q5(o.a / n, -o.b / n)

    def __rtruediv__(s, o):
        return Q5.c(o) / s

    def sign(s):
        a, b = s.a, s.b
        if b == 0:
            return (a > 0) - (a < 0)
        if a == 0:
            return (b > 0) - (b < 0)
        if (a > 0) == (b > 0):
            return 1 if a > 0 else -1
        # opposite signs: compare a^2 with 5 b^2
        if a * a > 5 * b * b:
            return 1 if a > 0 else -1
        return 1 if b > 0 else -1

    def __abs__(s):
        return -s if s.sign() < 0 else s

    def __float__(s):
        r5 = Fr(isqrt(5 * 10 ** 800), 10 ** 400)
        return float(s.a + s.b * r5)

    def __eq__(s, o):
        o = Q5.c(o); return s.a == o.a and s.b == o.b

    def __hash__(s):
        return hash((s.a, s.b))

    def __lt__(s, o): return (s - o).sign() < 0
    def __le__(s, o): return (s - o).sign() <= 0
    def __gt__(s, o): return (s - o).sign() > 0
    def __ge__(s, o): return (s - o).sign() >= 0

    def floor(s):
        D = s.a.denominator * s.b.denominator
        A = s.a.numerator * (D // s.a.denominator)
        B = s.b.numerator * (D // s.b.denominator)
        if B == 0:
            f = 0
        elif B > 0:
            f = isqrt(5 * B * B)
        else:
            f = -isqrt(5 * B * B) - 1
        return (A + f) // D

    def __repr__(s):
        return f"({s.a} + {s.b}*sqrt5)"


ALPHA = Q5(Fr(3, 2), Fr(-1, 2))  # 1/phi^2


def floor_k_alpha(k):
    # floor(k(3-sqrt5)/2) exactly
    return (3 * k - isqrt(5 * k * k) - 1) // 2 if k > 0 else 0


# ---------------------------------------------------------------- Fibonacci
FIB = [0, 1]
while len(FIB) < 400:
    FIB.append(FIB[-1] + FIB[-2])


def W(k):
    a, b = '0', '01'
    if k == 0:
        return a
    for _ in range(k - 1):
        a, b = b, b + a
    return b


# ---------------------------------------------------------------- rooms
ROOMS = {  # (d1, b1, h1, d2, b2, h2, p, w): d110 geom.ROOMS
    'DBas': (5, 0, 4, 4, -1, 6, 1, 1),
    'DB55': (5, 0, 5, 5, 0, 5, 2, 1),
    'DBw2': (5, 0, 5, 5, 0, 6, 1, 2),
}


def chambers(name, L):
    d1, b1, h1, d2, b2, h2, p, w = ROOMS[name]
    x2 = d1 + L
    A = dict(x0=0, x1=d1, y0=b1, y1=b1 + h1, px=d1, side=+1)
    B = dict(x0=x2, x1=x2 + d2, y0=b2, y1=b2 + h2, px=x2, side=-1)
    return A, B, p, w


# ---------------------------------------------------------------- tracer
def rect_trace(ch, p, w, S, dx, dy, target=None, maxev=10 ** 5):
    """Trace in a sealed rectangular chamber from S with velocity (dx, dy)
    (dx = +-1). Stops at the first open-portal hit (returns exit) or, if a
    target is given, at the target. Any vertex or portal-endpoint hit is
    illegal. Works over Fraction or Q5. Returns dict with word (list of wall
    labels), travel a, exit (y, vertical sign) or 'target'."""
    x0, x1, y0, y1, px = ch['x0'], ch['x1'], ch['y0'], ch['y1'], ch['px']
    forbidden = {(x0, y0), (x1, y0), (x0, y1), (x1, y1), (px, p), (px, p + w)}
    P = (S[0], S[1])
    word, a = [], Fr(0)
    for _ in range(maxev):
        cands = []
        xe = x1 if dx > 0 else x0
        tx = (xe - P[0]) / dx
        ye = y1 if (dy > 0) else y0
        ty = (ye - P[1]) / dy
        if target is not None:
            u = (target[0] - P[0], target[1] - P[1])
            tt = u[0] / dx
            if tt > 0 and u[1] == tt * dy and tt <= min(tx, ty):
                a = a + abs(u[0])
                return dict(word=word, a=a, end='target')
        if tx < ty:
            t, kind = tx, 'v'
        elif ty < tx:
            t, kind = ty, 'h'
        else:
            return dict(word=word, a=a, end='corner-tie')
        Q = (P[0] + t * dx, P[1] + t * dy)
        a = a + abs(Q[0] - P[0])
        if any(Q[0] == fx and Q[1] == fy for (fx, fy) in forbidden):
            return dict(word=word, a=a, end=('vertex', Q))
        if kind == 'v':
            if Q[0] == px and p < Q[1] < p + w:
                if target is not None:
                    return dict(word=word, a=a, end='portal-before-target')
                return dict(word=word, a=a, end='exit', y=Q[1], sy=1 if dy > 0 else -1)
            word.append(('v', Q[0]))
            dx = -dx
        else:
            word.append(('h', Q[1]))
            dy = -dy
        P = Q
    return dict(word=word, a=a, end='maxev')


# ---------------------------------------------------------------- cover
def cover(ch, p, w):
    """Four-copy square-tiled cover of a sealed rectangular chamber.
    Squares (i, j, sx, sy) with (i, j) the physical lower-left cell corner.
    Returns ids, R, U (lists), Rhit (bool per square)."""
    cells = [(i, j) for i in range(ch['x0'], ch['x1']) for j in range(ch['y0'], ch['y1'])]
    cs = set(cells)
    sq = [(i, j, sx, sy) for (i, j) in cells for sx in (1, -1) for sy in (1, -1)]
    idx = {s: n for n, s in enumerate(sq)}
    R, U, Rhit = [], [], []
    for (i, j, sx, sy) in sq:
        nb = (i + sx, j)
        if nb in cs:
            R.append(idx[(i + sx, j, sx, sy)]); Rhit.append(False)
        else:
            R.append(idx[(i, j, -sx, sy)])
            xe = i + 1 if sx > 0 else i
            Rhit.append(xe == ch['px'] and p <= j < p + w)
        nb = (i, j + sy)
        U.append(idx[nb + (sx, sy)] if nb in cs else idx[(i, j, sx, -sy)])
    return sq, idx, R, U, Rhit


def read_word(word, x, R, U, Rhit):
    """Read letters from square x; return (step of first hit or None, final square)."""
    for k, c in enumerate(word):
        if c == '1':
            x = U[x]
        if Rhit[x]:
            return k, R[x]
        x = R[x]
    return None, x


def block_data(R, U, Rhit, kmax):
    n = len(R)
    # g as tuple: g[x] = image. compose(g, h) = g after h.
    comp = lambda g, h: tuple(g[h[x]] for x in range(n))
    inv = lambda g: tuple(sorted(range(n), key=lambda x: g[x]))
    g0 = tuple(R)
    RU = tuple(R[U[x]] for x in range(n))
    g1 = comp(RU, g0)
    P0 = frozenset(x for x in range(n) if Rhit[x])
    P1 = frozenset(x for x in range(n) if Rhit[x] or Rhit[U[R[x]]])
    gs, Ps = [g0, g1], [P0, P1]
    for k in range(kmax - 1):
        gk, gk1 = gs[-2], gs[-1]
        gi = inv(gk1)
        Ps.append(Ps[-1] | frozenset(gi[x] for x in Ps[-2]))
        gs.append(comp(gk, gk1))
    return gs, Ps


# ================================================================ section A
log('== A. Thresholds for the named chamber pairs ==')
TH = {}
for name, (d1, b1, h1, d2, b2, h2, p, w) in ROOMS.items():
    areaA, areaB = d1 * h1, d2 * h2
    m = 4 * max(areaA, areaB)
    T = 1 + FIB[3 * m - 1]
    Llat = 4 * w * T * T
    H = 2 * FIB[3 * m] + 1
    Lreal = 36 * w * H * H
    TH[name] = dict(m=m, T=T, Llat=Llat, H=H, Lreal=Lreal, w=w)
    log(f"{name}: areas {areaA},{areaB}; m={m}; w={w}")
    log(f"  T = 1+F_{3*m-1} = {T}  ({len(str(T))} digits)")
    log(f"  lattice threshold 4wT^2 = {Llat}  ({len(str(Llat))} digits)")
    log(f"  H = 2F_{3*m}+1 has {len(str(H))} digits; real threshold 36wH^2 has {len(str(Lreal))} digits")

# ================================================================ section B
log('\n== B. Fibonacci word phase, substitution, Diophantine bounds ==')
NW = 100000
tail = ''.join(str(floor_k_alpha(k + 1) - floor_k_alpha(k)) for k in range(1, NW + 1))
first = floor_k_alpha(1) - floor_k_alpha(0)
log('first letter (k=0):', first)
fw = W(24)
log('|W_24| =', len(fw), '= F_26 =', FIB[26])
log('tail agrees with fixed point W_inf on', NW, 'letters:', tail == fw[:NW])
log('|W_k| = F_(k+2) for k<=24:', all(len(W(k)) == FIB[k + 2] for k in range(25)))
# positions of ones = floor(m phi^2) = floor(m phi) + m ; floor(m phi) = m + floor(m/phi)
ones = [i + 1 for i, c in enumerate(tail) if c == '1']


def floor_m_phi2(m):  # phi^2 = (3+sqrt5)/2
    return (3 * m + isqrt(5 * m * m)) // 2


log('m-th one at floor(m phi^2), all ones in prefix:', all(ones[j] == floor_m_phi2(j + 1) for j in range(len(ones))))
# Diophantine: |alpha - p/q| > 1/(3q^2) for nearest p, 1<=q<=20000
ok = True
lowest = None
for q in range(1, 20001):
    pf = floor_k_alpha(q)
    for pp in (pf, pf + 1):
        diff = abs(ALPHA - Fr(pp, q))
        ok &= diff > Fr(1, 3 * q * q)
        r = float(diff * (q * q))
        lowest = r if lowest is None else min(lowest, r)
log('|alpha-p/q| > 1/(3q^2) for all q<=20000 and both neighbours p:', ok)
log('min over these of q^2|alpha-p/q| (float) =', round(lowest, 6))
# every length-2F_(k+3) factor contains W_k, k=1..10
res = []
for k in range(1, 11):
    Nk = 2 * FIB[k + 3]
    wk = W(k)
    good = all(wk in tail[i:i + Nk] for i in range(0, 20000))
    res.append((k, Nk, good))
log('length-2F_(k+3) windows (20000 starts) contain W_k:', res)

# ================================================================ section C
log('\n== C. Cover automaton for the five named sealed chambers ==')
COVERS = {}
for name in ROOMS:
    A, B, p, w = chambers(name, 0)
    for tag, ch in (('A', A), ('B', B)):
        sq, idx, R, U, Rhit = cover(ch, p, w)
        M = len(sq)
        kmax = 3 * (M - 1) + 2
        gs, Ps = block_data(R, U, Rhit, kmax)
        # brute check of recurrence for k <= 10
        brute = all(Ps[k] == frozenset(x for x in range(M) if read_word(W(k), x, R, U, Rhit)[0] is not None)
                    for k in range(11))
        perm_ok = all(tuple(read_word(W(k), x, R, U, [False] * M)[1] for x in range(M)) == gs[k] for k in range(9))
        nested = all(Ps[k] <= Ps[k + 1] for k in range(len(Ps) - 1))
        kfull = next(k for k in range(len(Ps)) if len(Ps[k]) == M)
        growth = all(len(Ps[i + 3]) > len(Ps[i]) for i in range(len(Ps) - 3) if len(Ps[i]) < M)
        # transitivity of <R,U>
        seen, st = {0}, [0]
        while st:
            x = st.pop()
            for y in (R[x], U[x]):
                if y not in seen:
                    seen.add(y); st.append(y)
        COVERS[(name, tag)] = (sq, idx, R, U, Rhit)
        log(f"{name}{tag}: M={M}, |P_0|={len(Ps[0])}, transitive={len(seen)==M}, recurrence=brute {brute}, "
            f"perm {perm_ok}, nested {nested}, 3-step growth {growth}; first full k={kfull} "
            f"(proof bound 3(M-1)={3*(M-1)}); worst first-hit travel <= 1+F_{kfull+2}={1+FIB[kfull+2]}")

# ================================================================ section D
log('\n== D. Lattice replay at L = 4wT^2 exactly, all cross lattice pairs ==')


def leg_alpha_and_cover(name, tag, ch, p, w, S, sx, sy):
    """First hit at slope alpha (Q5 tracer) and via the cover automaton."""
    r = rect_trace(ch, p, w, (Q5(S[0]), Q5(S[1])), sx, sy * ALPHA)
    sq, idx, R, U, Rhit = COVERS[(name, tag)]
    # chamber-relative cell coordinates: covers were built at L=0
    off = ch['x0'] - (0 if tag == 'A' else ROOMS[name][0])
    X, Y = S[0] - off, S[1]
    x = idx[(X + (sx - 1) // 2, Y + (sy - 1) // 2, sx, sy)]
    word = '0' + tail[:5000]
    k, _ = read_word(word, x, R, U, Rhit)
    return r, k


def phase_exit(r, p):
    """Signed phase at the door, height above the door floor, in tracing direction."""
    return r['sy'] * (r['y'] - p)


def replay(name, L, pairs, launchA=(1, 1), launchB=(-1, 1), detail=()):
    A, B, p, w = chambers(name, L)
    T = TH[name]['T']
    half = Fr(1, 4 * T * T)
    nok, agree, maxa = 0, 0, 0
    for (S, Tg) in pairs:
        rA, kA = leg_alpha_and_cover(name, 'A', A, p, w, S, *launchA)
        rB, kB = leg_alpha_and_cover(name, 'B', B, p, w, Tg, *launchB)
        assert rA['end'] == 'exit' and rB['end'] == 'exit', (S, Tg, rA['end'], rB['end'])
        a, b = rA['a'], rB['a']
        agree += (a == kA + 1 and b == kB + 1)
        maxa = max(maxa, a, b)
        # phi_A forward sign; phi_B with forward sign = minus backward sign
        phA = phase_exit(rA, p)
        phB = -phase_exit(rB, p)
        Fal = L * ALPHA + phA - phB  # Q5
        kappa = Fal.b * (-2)  # coefficient of alpha: alpha = 3/2 - sqrt5/2
        c = Fal - kappa * ALPHA
        assert c.b == 0 and kappa == L + a + b, (kappa, L + a + b)
        Mm = (Fal / (2 * w) + Fr(1, 2)).floor()
        s = (2 * w * Mm - c.a) / kappa
        inI = (ALPHA - half) < Q5(s) < (ALPHA + half)
        # rational trace at s
        qA = rect_trace(A, p, w, (Fr(S[0]), Fr(S[1])), launchA[0], launchA[1] * s)
        qB = rect_trace(B, p, w, (Fr(Tg[0]), Fr(Tg[1])), launchB[0], launchB[1] * s)
        same = (qA['end'] == 'exit' and qB['end'] == 'exit' and qA['word'] == rA['word']
                and qB['word'] == rB['word'] and qA['a'] == a and qB['a'] == b)
        FA = phase_exit(qA, p)
        Fs = L * s + FA - (-phase_exit(qB, p))
        # corridor fold
        ph = FA + L * s
        rr = ph - 2 * w * ((ph + w) // (2 * w))  # in [-w, w)
        legal_mouth = rr != 0 and rr != -w
        hgt, sg = (rr, 1) if rr > 0 else (-rr, -1)
        # forward trace in B from the mouth to the target
        fB = rect_trace(B, p, w, (Fr(B['px']), p + hgt), 1, sg * s, target=(Fr(Tg[0]), Fr(Tg[1])))
        good = inI and same and Fs == 2 * w * Mm and legal_mouth and fB['end'] == 'target'
        nok += good
        if (S, Tg) in detail or not good:
            ncorr = (ph / w).__floor__()
            log(f"  {name} L={len(str(L))}-digit  S={S} T=(x2+{Tg[0]-B['x0']},{Tg[1]}): alpha-legs a={a.a}, b={b.a} "
                f"(cover steps {kA+1},{kB+1}); A exit y={rA['y']} sign {rA['sy']}, B back exit y={rB['y']} sign {rB['sy']}")
            log(f"     F(alpha) = c + kappa*alpha with c={c.a}, kappa=L+{a+b}; M={Mm} ({len(str(Mm))} digits)")
            log(f"     s* = {s.numerator}/{s.denominator}" if len(str(s.denominator)) < 30 else
                f"     s*: numerator {len(str(s.numerator))} digits, denominator {len(str(s.denominator))} digits")
            log(f"     s* in alpha+-1/(4T^2): {inI}; 4T^2|s*-alpha| = {float(abs(Q5(s)-ALPHA) * (4*T*T)):.4f}")
            log(f"     legs at s* keep alpha words: {same}; A exit y~{float(qA['y']):.12f}, B back exit y~{float(qB['y']):.12f}")
            log(f"     F(s*) = 2wM exactly: {Fs == 2*w*Mm}; arrival height at B mouth ~{float(hgt):.12f} sign {sg}; "
                f"~{len(str(ncorr))}-digit number of corridor wall contacts")
            log(f"     forward trace in B from mouth reaches T: {fB['end']}; contacts before T: {len(fB['word'])} in B, {len(qA['word'])} in A")
    return nok, len(pairs), agree, maxa.a


def interior_lattice(ch):
    return [(x, y) for x in range(ch['x0'] + 1, ch['x1']) for y in range(ch['y0'] + 1, ch['y1'])]


NAMED = {}
for name in ROOMS:
    L = TH[name]['Llat']
    A, B, p, w = chambers(name, L)
    x2 = B['x0']
    named = {'DBas': [((1, 3), (x2 + 2, 3)), ((4, 1), (x2 + 3, 4))],
             'DB55': [((1, 1), (x2 + 3, 1)), ((2, 4), (x2 + 1, 2))],
             'DBw2': [((1, 1), (x2 + 4, 5)), ((3, 2), (x2 + 2, 2))]}[name]
    pairs = [(S, Tg) for S in interior_lattice(A) for Tg in interior_lattice(B)]
    nok, n, agree, maxa = replay(name, L, pairs, detail=named)
    log(f"{name}: constructed path legal for {nok}/{n} cross lattice pairs; "
        f"tracer and cover first-hit travel agree {agree}/{n}; max leg travel {maxa} (proof bound T has {len(str(TH[name]['T']))} digits)")

# other launch sheets for the marked DBas pair ("any signed launch works")
log('\n  DBas marked pair (1,3)-(x2+2,3), all four source sheets x two backward sheets:')
L = TH['DBas']['Llat']
A, B, p, w = chambers('DBas', L)
x2 = B['x0']
tot = 0
for la in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
    for lb in ((-1, 1), (-1, -1)):
        nok, n, agree, maxa = replay('DBas', L, [((1, 3), (x2 + 2, 3))], launchA=la, launchB=lb)
        tot += nok
log(f"  legal for {tot}/8 launch-sheet combinations")
log('section D CPU s:', round(time.process_time() - T0, 1))

# ================================================================ section E
log('\n== E. Real-mark replay at L = 36wH^2 (stand-in for the excluded-slope step) ==')


def replay_real(name, pairs):
    L = TH[name]['Lreal']
    H = TH[name]['H']
    A, B, p, w = chambers(name, L)
    half = Fr(1, 12 * H * H)
    out = 0
    for (S, Tg) in pairs:
        rA = rect_trace(A, p, w, (Q5(S[0]), Q5(S[1])), 1, ALPHA)
        rB = rect_trace(B, p, w, (Q5(Tg[0]), Q5(Tg[1])), -1, ALPHA)
        a, b = rA['a'], rB['a']
        phA, phB = phase_exit(rA, p), -phase_exit(rB, p)
        Fal = L * ALPHA + phA - phB
        kappa = Fal.b * (-2)
        c = Fal - kappa * ALPHA
        assert kappa == L + a + b and c.b == 0
        Mm = (Fal / (2 * w) + Fr(1, 2)).floor()
        s = (2 * w * Mm - c.a) / kappa
        inI = (ALPHA - half) < Q5(s) < (ALPHA + half)
        qA = rect_trace(A, p, w, (Fr(S[0]), Fr(S[1])), 1, s)
        qB = rect_trace(B, p, w, (Fr(Tg[0]), Fr(Tg[1])), -1, s)
        same = qA['word'] == rA['word'] and qB['word'] == rB['word'] and qA['end'] == qB['end'] == 'exit'
        ph = phase_exit(qA, p) + L * s
        rr = ph - 2 * w * ((ph + w) // (2 * w))
        hgt, sg = (rr, 1) if rr > 0 else (-rr, -1)
        fB = rect_trace(B, p, w, (Fr(B['px']), p + hgt), 1, sg * s, target=(Fr(Tg[0]), Fr(Tg[1])))
        good = inI and same and rr not in (0, -w) and fB['end'] == 'target'
        out += good
        log(f"  {name} S={S} T=(x2+{Tg[0]-B['x0']},{Tg[1]}): a={a.a}, b={b.a}; s* in I: {inI}; words kept: {same}; reaches T: {fB['end']}")
    return out


for name in ROOMS:
    A, B, p, w = chambers(name, TH[name]['Lreal'])
    x2 = B['x0']
    pairs = [((Fr(7, 3), Fr(13, 5)), (x2 + Fr(5, 7), Fr(31, 9))),
             ((Fr(1, 2), Fr(1, 2)), (x2 + Fr(7, 2), Fr(9, 2))),
             ((Fr(22, 7), Fr(10, 3)), (x2 + Fr(3, 11), Fr(1, 13) + B['y0']))]
    k = replay_real(name, pairs)
    log(f"  {name}: {k}/3 real pairs legal")

# ================================================================ section F
log('\n== F. Section 3 and 4 arithmetic ==')
# parity class count inside a u-by-v rectangle
okp = True
for u in range(2, 31):
    for v in range(2, 31):
        best = 0
        for cx in (0, 1):
            for cy in (0, 1):
                cnt = sum(1 for x in range(1, u) for y in range(1, v) if x % 2 == cx and y % 2 == cy)
                best = max(best, cnt)
        okp &= best == (u // 2) * (v // 2)
log('max parity-class count of interior points of u-by-v = floor(u/2)floor(v/2), u,v<=30:', okp)
# midpoint count identity: folded midpoint abscissae of (sx +- tx)/2 + k u, k in -6..6
import random
random.seed(1)


def fold(X, u):
    X = X % (2 * u)
    return X if X <= u else 2 * u - X


okm = True
for _ in range(200):
    u, v = random.randint(2, 9), random.randint(2, 9)
    s = (Fr(random.randint(-50, 50), 7), Fr(random.randint(-50, 50), 11))
    t = (Fr(random.randint(-50, 50), 13), Fr(random.randint(-50, 50), 3))
    xs = {fold((s[0] + e * t[0]) / 2 + k * u, u) for e in (1, -1) for k in range(-6, 7)}
    ys = {fold((s[1] + e * t[1]) / 2 + k * v, v) for e in (1, -1) for k in range(-6, 7)}
    okm &= len(xs) <= 4 and len(ys) <= 4
log('folded midpoint abscissae and ordinates <= 4 each (200 random rational endpoint pairs):', okm)
# cross rectangle bound: any axis rectangle in P_b has a side <= 4 (logic check on grid)
okc = True
for b in (7, 9, 11):
    inside = lambda x, y: (abs(x) <= b and abs(y) <= 2) or (abs(x) <= 2 and abs(y) <= b)
    # a rectangle [x0,x1]x[y0,y1] in the cross with both sides > 4 would need a corner outside
    for x0 in range(-b, b):
        for x1 in range(x0 + 5, b + 1):
            for y0 in range(-b, b):
                for y1 in range(y0 + 5, b + 1):
                    if all(inside(x, y) for x in (x0, x1) for y in (y0, y1)):
                        okc = False
log('no lattice rectangle with both sides >= 5 has all corners in P_b, b=7,9,11:', okc)
# valency budget
n = 120
log('2(n-8)-16-floor(n/2) at n=120:', 2 * (n - 8) - 16 - n // 2, '; >= 3n/2-32 for n in 120..10^4:',
    all(2 * (k - 8) - 16 - k // 2 >= Fr(3, 2) * k - 32 for k in range(120, 10001)))
rate = 3933192 / 72.5
log(f'd102 rate {rate:.1f} witnesses/s; CPU-h per witness {1/rate/3600:.4e}; '
    f'1e11 rooms -> {1e11/rate/3600:.0f} h; 1e12 -> {1e12/rate/3600:.0f} h')
log('total CPU s:', round(time.process_time() - T0, 1))
