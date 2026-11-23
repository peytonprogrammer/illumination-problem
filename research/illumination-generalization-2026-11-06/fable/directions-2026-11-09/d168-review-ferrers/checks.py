"""d168 review checks for ferrers-terminal-strip.md (snapshot 2026-11-22 0813).

Named explicit rooms only. Exact Fraction arithmetic. trace() is copied verbatim from
d167-review-overhang/checks.py (itself from d164-attack-combs/attack.py).
Run: python3 -B checks.py > checks.log
"""
import json
import random
import time
from fractions import Fraction as F
from math import gcd, floor

T0 = time.process_time()
FAIL = []
HERE = __file__.rsplit('/', 1)[0]


def log(*a):
    print(*a, flush=True)


def check(ok, msg):
    log(('  PASS ' if ok else '  FAIL ') + msg)
    if not ok:
        FAIL.append(msg)


# ------------------------------------------------------------------ copied from d167 / d164
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


def turn_word(V):
    n = len(V)
    out = ''
    for i in range(n):
        a, b, c = V[i - 1], V[i], V[(i + 1) % n]
        cr = (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])
        out += 'L' if cr > 0 else 'R'
    return out


def same_class(u, w):
    rots = lambda s: {s[i:] + s[:i] for i in range(len(s))}
    return len(u) == len(w) and (w in rots(u) or w in rots(u[::-1]))


# ------------------------------------------------------------------ the room and the note's construction
def den(q):
    return F(q).denominator


def lcm(a, b):
    return a * b // gcd(a, b)


class Room:
    """Note orientation: left-attached runs, widths w<u<v<W top to bottom, heights c,d,e,h."""

    def __init__(self, name, w, u, v, W, c, d, e, h):
        self.name = name
        self.w, self.u, self.v, self.W = map(F, (w, u, v, W))
        self.c, self.d, self.e, self.h = map(F, (c, d, e, h))
        y1, y2, y3, H = self.h, self.h + self.e, self.h + self.e + self.d, self.h + self.e + self.d + self.c
        self.y3, self.H = y3, H
        self.P = [(0, 0), (W, 0), (W, y1), (v, y1), (v, y2), (u, y2), (u, y3), (w, y3), (w, H), (0, H)]
        self.P0 = lcm(den(self.d / (2 * self.u)), den(self.e / (2 * self.v)))
        self.Q = floor(self.W / self.w)

    def transposed(self):
        w, u, v, W, c, d, e, h = self.w, self.u, self.v, self.W, self.c, self.d, self.e, self.h
        return Room(self.name + ' (transposed)', h, e + h, d + e + h, c + d + e + h, W - v, v - u, u - w, w)

    def den_test(self):
        q = den(self.P0 * self.h / self.W)
        return q, self.Q ** 2, q > self.Q ** 2

    def rotation_dens(self, b):
        return den(self.P0 * b / (2 * self.W)), den(self.P0 * (2 * self.h - b) / (2 * self.W))

    def construct(self, S, T, kmax):
        """The note's shot: M = k*P0, |Z|<w, Z+MB = +-z mod 2W, X = +-x+Ma rep in [-w,w].
        Returns (k, route, physical direction) for the smallest |k| found, else None."""
        x, ys = S
        z, yt = T
        w, W, h = self.w, self.W, self.h
        a, b = ys - self.y3, h - yt
        for kk in range(0, kmax + 1):
            for k in ([kk, -kk] if kk else [0]):
                M = k * self.P0
                for route, B in (('direct', b), ('floor', 2 * h - b)):
                    D = a + self.d + self.e + B
                    for sz in (1, -1):
                        Z = (sz * z - M * B + W) % (2 * W) - W      # rep in [-W, W)
                        if not (-w < Z < w):
                            continue
                        for sx in (1, -1):
                            X = (sx * x + M * a + w) % (2 * w) - w
                            if route == 'floor':
                                tf = a + self.d + self.e + h
                                Lf = X + (Z - X) * tf / D + M * h
                                if Lf % W == 0:
                                    continue
                            travel = Z - X + M * D
                            return k, route, (sx * travel, -D)
        return None


def lit_by_construction(R, S, T, kmax):
    c = R.construct(S, T, kmax)
    if c is None:
        return None, None
    k, route, (dx, dy) = c
    st, pos, con = trace(R.P, S, (S[0] + dx, S[1] + dy))
    return (st == 'end' and pos == T), (k, route, (dx, dy), st, len(con))


def search_lit(R, S, T, pmax, maxrefl):
    """Bounded direction search: is T on some segment of a vertex-free path from S?"""
    Vs = {(F(a), F(b)) for a, b in R.P}
    n = len(R.P)
    hw = [(R.P[i], R.P[(i + 1) % n]) for i in range(n) if R.P[i][1] == R.P[(i + 1) % n][1]]
    vw = [(R.P[i], R.P[(i + 1) % n]) for i in range(n) if R.P[i][0] == R.P[(i + 1) % n][0]]
    for p in range(-pmax, pmax + 1):
        for q in range(-pmax, pmax + 1):
            if (p, q) == (0, 0) or gcd(abs(p), abs(q)) != 1:
                continue
            X, Y, vx, vy = F(S[0]), F(S[1]), F(p), F(q)
            acc = F(0)
            for r in range(maxrefl):
                best = None
                if vx:
                    for A, B in vw:
                        t = (A[0] - X) / vx
                        if t > 0 and (best is None or t < best[0]) and min(A[1], B[1]) <= Y + vy * t <= max(A[1], B[1]):
                            best = (t, 'v')
                if vy:
                    for A, B in hw:
                        t = (A[1] - Y) / vy
                        if t > 0 and (best is None or t < best[0]) and min(A[0], B[0]) <= X + vx * t <= max(A[0], B[0]):
                            best = (t, 'h')
                t, kind = best
                # T on the open segment (X,Y)->(X+vx t, Y+vy t)?
                if vx:
                    s = (T[0] - X) / vx
                else:
                    s = (T[1] - Y) / vy
                if 0 < s < t and X + vx * s == T[0] and Y + vy * s == T[1]:
                    return (p, q), r, acc + s
                acc += t
                X, Y = X + vx * t, Y + vy * t
                if (X, Y) in Vs:
                    break
                if kind == 'v': vx = -vx
                else: vy = -vy
    return None


def fr(p):
    return f"({p[0]},{p[1]})"


# ================================================================== item 1: the lattice issue
log('# Item 1: condition (1) on lattice rooms')
ROOMS = {
    'R1': Room('R1 widths 2,3,4,5 heights 1,1,1,1', 2, 3, 4, 5, 1, 1, 1, 1),
    'R2': Room('R2 widths 2,3,4,5 heights 2,6,8,2', 2, 3, 4, 5, 2, 6, 8, 2),
    'R3': Room('R3 widths 3,4,5,7 heights 1,2,1,3', 3, 4, 5, 7, 1, 2, 1, 3),
    'R4': Room('R4 widths 3,5,6,8 heights 1,2,4,1', 3, 5, 6, 8, 1, 2, 4, 1),
    'N1': Room('N1 ledger realization widths 1,2,3,4 heights 1,1,1,1', 1, 2, 3, 4, 1, 1, 1, 1),
    'N2': Room('N2 d17 chain widths 3,4,9,12 heights 3,4,2,3', 3, 4, 9, 12, 3, 4, 2, 3),
}
for key, R in ROOMS.items():
    al, be, ga = R.d / (2 * R.u), R.e / (2 * R.v), R.h / R.W
    # span_Q{al, be} = Q since al != 0 is rational; ga = (ga/al)*al with ga/al rational
    check(isinstance(ga / al, F) and (ga / al) * al == ga,
          f'{key}: h/W={ga} = ({ga/al})*d/(2u) lies in span_Q (condition (1) fails)')
    Rt = R.transposed()
    alt, gat = Rt.d / (2 * Rt.u), Rt.h / Rt.W
    check((gat / alt) * alt == gat, f'{key}: transposed h\'/W\'={gat} in span (transposed condition fails)')
    check(same_class(turn_word(R.P), 'LLLLLRLRLR') and same_class(turn_word(Rt.P), 'LLLLLRLRLR'),
          f'{key}: room and transpose have word LLLLLRLRLR (turns {turn_word(R.P)})')

log('## Denominator test, both orientations (P = minimal P0)')
for key, R in ROOMS.items():
    q, Q2, ok = R.den_test()
    qt, Q2t, okt = R.transposed().den_test()
    log(f'   {key}: P0={R.P0} Q={R.Q} den(P0 h/W)={q} vs Q^2={Q2} -> {"COVERED" if ok else "not covered"};'
        f' transposed P0={R.transposed().P0} den={qt} vs {Q2t} -> {"COVERED" if okt else "not covered"}')
check(all(ROOMS[k].den_test()[2] for k in ('R1', 'R2', 'R3', 'R4')), 'R1-R4 pass the direct denominator test')
check(not any(ROOMS[k].den_test()[2] or ROOMS[k].transposed().den_test()[2] for k in ('N1', 'N2')),
      'N1, N2 fail the test in both orientations')

log('## Necessary condition floor(W/w)^2 < W (den(P0 h/W) <= W)')
for w in range(1, 6):
    Ws = [W for W in range(w + 3, w * w + w + 2) if (W // w) ** 2 < W]
    log(f'   w={w}: admissible W = {Ws}')
check(all((W // 1) ** 2 >= W for W in range(4, 200)), 'w=1: no W passes (Q=W, Q^2>=W)')
check(all(not ((W // w) ** 2 < W) for w in range(1, 40) for W in range(w * w + w, w * w + 3 * w)),
      'no W >= w^2+w passes, for w < 40 (closed form: need Q <= w, hence W <= w^2+w-1)')

log('## Explicit infinite family F: widths (2,3,4,5), any c,d,e >= 1, 5 not dividing h')
okF = True
for d in range(1, 13):
    for e in range(1, 17):
        R = Room('F', 2, 3, 4, 5, 1, d, e, 1)
        okF &= R.P0 % 5 != 0 and 24 % R.P0 == 0
check(okF, 'P0 divides 24 (dens of d/6, e/8), so P0 is prime to 5 and den(P0 h/5)=5>4 iff 5 does not divide h')
check(not Room('F', 2, 3, 4, 5, 1, 1, 1, 5).den_test()[2], 'h=5 member (2,3,4,5;1,1,1,5) is not covered')

# ================================================================== item 2: what d15 leaves
log('# Item 2: d15 cert_r3 entry for the staircase')
C = json.load(open(HERE + '/../d15-small-r/cert_r3.json'))
ent = [c for c in C if c['shape'] == '#.../##../###./####'][0]
log(f"   mask {ent['mask']} counts {ent['counts']} uncovered {ent['uncovered']}")
rows = [[(ent['mask'] >> (y * ent['nx'] + x)) & 1 for x in range(ent['nx'])] for y in range(ent['ny'])]
log(f'   rows y=0..3 from mask (bit y*nx+x): {rows}')
check(rows == [[1, 1, 1, 1], [1, 1, 1, 0], [1, 1, 0, 0], [1, 0, 0, 0]], 'mask = bottom full row, top row only x-cell 0')
check(ent['uncovered'] == [[[1, 7], [7, 1]]], 'only open-cell pair (1,7)-(7,1): top cell vs bottom-right cell [v,W]x[0,h]')

# ================================================================== item 3: algebra of the proof
log('# Item 3: identities in the proof')
ok1 = ok2 = True
rnd = random.Random(168)
for _ in range(2000):
    a, b, h, d, e, w = (F(rnd.randint(1, 50), rnd.randint(1, 20)) for _ in range(6))
    if b >= h:
        b, h = h / 2, h
    D = a + d + e + 2 * h - b
    tf = a + d + e + h
    ok1 &= (1 - tf / D) == (h - b) / D and (h - b) / D < F(1, 2)
    Z, X = F(rnd.randint(-99, 99), 100) * w, F(rnd.randint(-100, 100), 100) * w
    for t in (a, a + d, a + d + e):
        L = X + (Z - X) * t / D
        ok2 &= abs(L) <= w - (t / D) * (w - abs(Z))
check(ok1, 'floor shift coefficient 1 - t_f/D = (h-b)/D < 1/2 (2000 random rational cases)')
check(ok2, 'joint bound |L(t)| <= w - (t/D)(w-|Z|) (2000 random cases)')
okd = True
for q1 in range(1, 9):
    for q2 in range(1, 9):
        for p1 in range(q1):
            for p2 in range(q2):
                okd &= den(F(p1, q1) + F(p2, q2)) <= max(q1, q2) ** 2
check(okd, 'sum of two rationals with dens <= Q has den <= Q^2 (Q <= 8 exhaustive)')

# ================================================================== named control from the note
log('# Note control: d17 chain N2, S=(1,10), T=(10,1), direction (163,-9)')
N2 = ROOMS['N2']
check(N2.P0 == 18 and N2.den_test() == (2, 16, False), 'N2: P0=18, den(P0 h/W)=2 <= 16, test fails')
check(N2.rotation_dens(F(2)) == (2, 1), 'N2 at b=2: both rotation dens <= Q=4')
st, pos, con = trace(N2.P, (1, 10), (1 + 163, 10 - 9))
nh = sum(1 for _, k in con if k == 'h')
check(st == 'end' and pos == (10, 1) and nh == 0 and len(con) == 31,
      f'trace (163,-9) from (1,10): {st} at {fr(pos)}, {len(con)} reflections, {nh} horizontal')

# ================================================================== item 4: exact replays
log('# Item 4: exact replays of the note construction in covered rooms')


def terminal_marks(R, n_rand, rnd):
    w, v, W, h, y3, H = R.w, R.v, R.W, R.h, R.y3, R.H
    Ss = [(F(2 * i + 1, 2), F(2 * j + 1, 2)) for i in range(int(w)) for j in range(int(y3), int(H))]
    Ts = [(F(2 * i + 1, 2), F(2 * j + 1, 2)) for i in range(int(v), int(W)) for j in range(int(h))]
    pairs = [(s, t) for s in Ss for t in Ts]
    for _ in range(n_rand):
        dd = rnd.choice([7, 11, 13, 97, 101, 1009])
        s = (F(rnd.randint(1, int(w) * dd - 1), dd), y3 + F(rnd.randint(1, int(H - y3) * dd - 1), dd))
        dd2 = rnd.choice([3, 4, 6, 9, 101, 1013])
        t = (v + F(rnd.randint(1, int(W - v) * dd2 - 1), dd2), F(rnd.randint(1, int(h) * dd2 - 1), dd2))
        pairs.append((s, t))
    return pairs


for key in ('R1', 'R2', 'R3', 'R4'):
    R = ROOMS[key]
    pairs = terminal_marks(R, 8, rnd)
    nlit, worst, routes = 0, 0, {}
    for S, T in pairs:
        b = R.h - T[1]
        q1, q2 = R.rotation_dens(b)
        pred = q1 > R.Q or q2 > R.Q
        ok, info = lit_by_construction(R, S, T, kmax=2 * int(R.W) * max(q1, q2) + 2)
        if ok:
            nlit += 1
            routes[info[1]] = routes.get(info[1], 0) + 1
            worst = max(worst, info[4])
        else:
            log(f'   {key} FAIL pair {fr(S)}-{fr(T)} pred={pred} info={info}')
        check(pred, f'{key} {fr(S)}-{fr(T)}: rotation dens ({q1},{q2}) has one > Q={R.Q}') if not pred else None
    check(nlit == len(pairs), f'{R.name}: construction + exact trace hits T for {nlit}/{len(pairs)} pairs '
          f'(routes {routes}, max reflections {worst})')

log('# Item 4b: uncovered rooms N1, N2 (named pairs only)')
for key in ('N1', 'N2'):
    R = ROOMS[key]
    pairs = terminal_marks(R, 3, rnd)
    if key == 'N2':
        pairs = [((F(1), F(10)), (F(10), F(1)))] + pairs[:4] + pairs[-3:]
    for S, T in pairs:
        b = R.h - T[1]
        ok, info = lit_by_construction(R, S, T, kmax=4 * int(R.W) * 4 + 2)
        if ok:
            log(f'   {key} {fr(S)}-{fr(T)}: note construction works, k={info[0]} {info[1]} dir={info[2]}, {info[4]} refl')
            continue
        res = search_lit(R, S, T, pmax=12, maxrefl=60)
        if res:
            (p, q), r, s = res
            st, pos, con = trace(R.P, S, (S[0] + s * p, S[1] + s * q))
            check(st == 'end' and pos == T, f'{key} {fr(S)}-{fr(T)}: construction fails (rotation dens '
                  f'{R.rotation_dens(b)}, Q={R.Q}); dir ({p},{q}) lights it, {len(con)} refl, independent retrace')
        else:
            log(f'   {key} {fr(S)}-{fr(T)}: construction fails; no witness with |p|,|q|<=12, <=60 refl (UNRESOLVED)')

log(f'\n## done: {len(FAIL)} failures {FAIL}; CPU {time.process_time() - T0:.1f}s')
