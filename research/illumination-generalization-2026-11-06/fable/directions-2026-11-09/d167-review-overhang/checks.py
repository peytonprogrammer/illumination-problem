"""d167 review checks for overhang-escape.md and nonspanning-entry.md (snapshots 2026-11-22 0758).

Named explicit rooms only. Exact Fraction arithmetic throughout. polygon(), trace() and
cells_rect() are copied verbatim from d164-attack-combs/attack.py (itself from d162/d161).
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


# ------------------------------------------------------------------ copied from d164
def cells_rect(a, b, c, d):
    return {(x, y) for x in range(a, b) for y in range(c, d)}


def polygon(cells):
    E = {}
    for x, y in cells:
        if (x, y - 1) not in cells: E[(x, y)] = (x + 1, y)
        if (x + 1, y) not in cells: E[(x + 1, y)] = (x + 1, y + 1)
        if (x, y + 1) not in cells: E[(x + 1, y + 1)] = (x, y + 1)
        if (x - 1, y) not in cells: E[(x, y + 1)] = (x, y)
    s = min(E)
    pts, p = [s], E[s]
    while p != s:
        pts.append(p); p = E[p]
    n = len(pts)
    V = []
    for i in range(n):
        a, b, c = pts[i - 1], pts[i], pts[(i + 1) % n]
        if (b[0] - a[0], b[1] - a[1]) != (c[0] - b[0], c[1] - b[1]):
            V.append(b)
    assert len(E) == n, "not strictly simple"
    return V


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


# ------------------------------------------------------------------ helpers
def fr(p):
    return f"({p[0]},{p[1]})"


def fold(X, l, w):
    """Fold developed abscissa X into [l, l+w]. Returns (pos, sign) or None if on a wall line."""
    m = (X - l) % (2 * w)
    if m == 0 or m == w:
        return None
    return (l + m, 1) if m < w else (l + 2 * w - m, -1)


def turn_word(V):
    n = len(V)
    area2 = sum(V[i][0] * V[(i + 1) % n][1] - V[(i + 1) % n][0] * V[i][1] for i in range(n))
    if area2 < 0:
        V = V[::-1]
    out = ''
    for i in range(n):
        a, b, c = V[i - 1], V[i], V[(i + 1) % n]
        cr = (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])
        out += 'L' if cr > 0 else 'R'
    return out


def same_class(u, w):
    if len(u) != len(w):
        return False
    rots = lambda s: {s[i:] + s[:i] for i in range(len(s))}
    return w in rots(u) or w in rots(u[::-1])


# ================================================================== note 1: overhang-escape
log('# Note 1: overhang-escape.md')

# Room B as in d164: hall [0,6]x[0,32], parent [1,3]x[32,33], child [2,5]x[33,34]
class Hang:
    def __init__(self, name, A, H, p0, v, h, j0, j1, ctop, child):
        self.name, self.A, self.H, self.p0, self.v, self.h = name, A, H, p0, v, h
        self.j0, self.j1, self.ctop = j0, j1, ctop
        self.cells = cells_rect(0, A, 0, H) | cells_rect(p0, p0 + v, H, H + h) | cells_rect(*child)
        self.P = polygon(self.cells)
        self.w = j1 - j0
        self.child = child

    def L(self, d, B):
        return min((d + self.h + B) * self.w / (2 * d), (d + self.h + B) * self.v / (d + self.h))

    def marks(self):
        cx0, cx1, cy0, cy1 = self.child
        return [(F(i, 2), F(j, 2)) for i in range(2 * cx0 + 1, 2 * cx1) for j in range(2 * cy0 + 1, 2 * cy1)]


RB = Hang('B (d164)', 6, 32, 1, 2, 1, 2, 3, 34, (2, 5, 33, 34))
RP = Hang('R2: hall [0,5]x[0,30], parent [2,3]x[30,32], child [1,4]x[32,33]', 5, 30, 2, 1, 2, 2, 3, 33, (1, 4, 32, 33))
RC = Hang('R3: hall [0,7]x[0,42], parent [1,4]x[42,43], child [3,6]x[43,45]', 7, 42, 1, 3, 1, 3, 4, 45, (3, 6, 43, 45))

log('## 1. Necessity in B')
log(f'   B polygon vertices: {RB.P}')
check((3, 33) in RB.P and (2, 33) in RB.P, 'upper lips (2,33) and (3,33) are polygon vertices (rays stop there)')
M = (F(4), F(67, 2))
# straight line from M through (e,33): lower crossing at y=32
for e in [F(2), F(5, 2), F(29, 10), F(3)]:
    x32 = e + (e - M[0]) * (F(33) - 32) / (M[1] - 33)
    check(x32 == 3 * e - 8, f'line through (e,33) e={e} meets y=32 at 3e-8={3*e-8}')
check(all(3 * F(e) - 8 < 1 for e in [F(2) + F(k, 1000) for k in range(1, 1000)]), '3e-8 < 1 on a 1/1000 grid of (2,3); affine in e with value 1 only at e=3')
# exhaustive first-event check over primitive directions
nd, first = 0, {}
for p in range(-100, 101):
    for q in range(-100, 101):
        if (p, q) == (0, 0) or gcd(abs(p), abs(q)) != 1:
            continue
        nd += 1
        st, pos, con = trace(RB.P, M, (M[0] + 200 * p, M[1] + 200 * q), maxrefl=1)
        y = con[0][0][1] if con else pos[1]
        if y < 32:
            k = 'reached hall straight'
        elif st == 'corner':
            k = 'corner ' + fr(pos)
        else:
            k = ('parent ' if y < 33 else 'child ') + con[0][1]
        first[k] = first.get(k, 0) + 1
log(f'   directions |p|,|q|<=100 from (4,67/2): {nd}; first events {first}')
check('reached hall straight' not in first, 'no direction reaches the hall (y<32) before its first contact')
# open set x > 3 + 2 delta; sharpness on the other side
ok_open, sharp = True, True
for d in [F(1, 10), F(1, 4), F(1, 2), F(3, 4), F(9, 10)]:
    for x in [3 + 2 * d + F(1, 10**4), (3 + 2 * d + 5) / 2, 5 - F(1, 10**4)]:
        if x >= 5:
            continue
        sup = 3 + (3 - x) / d          # value of e + (e-x)/d at e=3
        ok_open &= sup < 1
    x = 3 + 2 * d - F(1, 100)
    e = 3 - F(1, 10**6)
    sharp &= 1 < e + (e - x) / d < 3
check(ok_open, 'for 3+2d < x < 5 the lower-crossing sup 3+(3-x)/d < 1 (strict failure)')
check(sharp, 'for x = 3+2d-1/100 a straight escape exists (bound is sharp)')
check(M[0] == 3 + 2 * F(1, 2), 'the displayed mark (4,67/2) has x = 3+2d exactly: boundary of the open set, failure rests on the lip')

log('## 1b. Constructed witness (4,67/2) -> (1/2,1/2), direction (-149,-66)')
e = F(379, 132)
check((e - 4, F(-1, 2)) == (F(-149, 132), F(-66, 132)), 'direction through (379/132,33) is (-149,-66)')
check(3 * e - 8 == F(27, 44) and 2 - F(27, 44) == F(61, 44), 'lower crossing 27/44 folds to 61/44')
check(262 - 66 * e == F(145, 2) and F(145, 2) % 12 == F(1, 2), 'developed hall abscissa 145/2 folds mod 12 to 1/2')
end = (M[0] - 149 * F(33, 66), M[1] - 66 * F(33, 66))
st, pos, con = trace(RB.P, M, end)
kinds = {}
for (cx, cy), k in con:
    lab = 'parent side' if cy > 32 else ('hall side' if k == 'v' else 'horizontal')
    kinds[lab] = kinds.get(lab, 0) + 1
log(f'   trace: {st} at {fr(pos)}; contacts {kinds}')
check(st == 'end' and pos == (F(1, 2), F(1, 2)) and kinds.get('parent side') == 1 and 'horizontal' not in kinds,
      'witness reaches (1/2,1/2) exactly: 1 parent-side bounce, no horizontal bounce')


log('## 2. Sufficient condition L(B) > 2A: construction from the proof, traced exactly')


def construct(R, M, t, B, piece='largest'):
    """Return list of candidate (e, endpoint) for target (t, H-B) per the proof's construction."""
    x = M[0]
    d = M[1] - (R.H + R.h)
    k1 = 1 + R.h / d
    Xl, Xr = R.j0 + R.h * (R.j0 - x) / d, R.j1 + R.h * (R.j1 - x) / d
    bnds = [Xl] + [R.p0 + k * R.v for k in range(floor((Xl - R.p0) / R.v) + 1, floor((Xr - R.p0) / R.v) + 1)
                   if Xl < R.p0 + k * R.v < Xr] + [Xr]
    pieces = [(bnds[i], bnds[i + 1]) for i in range(len(bnds) - 1)]
    if piece == 'largest':
        pieces = [max(pieces, key=lambda pc: pc[1] - pc[0])]
    out = []
    for a, b in pieces:
        k = floor(((a + b) / 2 - R.p0) / R.v)
        sg = 1 if k % 2 == 0 else -1
        # X(e) = k1 e - h x/d ; folded F = p0 + (X-p0-kv) (sg=+1) or p0+v-(X-p0-kv) (sg=-1)
        # Y(e) = F + sg*B*(e-x)/d  -> affine alpha e + beta
        def Y(e):
            X = k1 * e - R.h * x / d
            Fv = R.p0 + (X - R.p0 - k * R.v) if sg > 0 else R.p0 + R.v - (X - R.p0 - k * R.v)
            return Fv + sg * B * (e - x) / d
        ea, eb = (a + R.h * x / d) / k1, (b + R.h * x / d) / k1
        ya, yb = Y(ea), Y(eb)
        lo, hi = min(ya, yb), max(ya, yb)
        alpha = (yb - ya) / (eb - ea)
        for base in (t, -t):
            n0 = floor((lo - base) / (2 * R.A))
            for n in range(n0, n0 + int((hi - lo) / (2 * R.A)) + 3):
                y = base + 2 * R.A * n
                if lo < y < hi:
                    ee = ea + (y - ya) / alpha
                    out.append((ee, (x + (ee - x) * (d + R.h + B) / d, M[1] - (d + R.h + B))))
    return out


def lit_by(R, M, t, B, piece, floor_ok=False):
    tgt = (t, R.H - B) if B < R.H else (t, B - R.H)   # B >= H: reflected row B' = 2H - B
    for ee, end in construct(R, M, t, B, piece):
        st, pos, con = trace(R.P, M, end)
        if st == 'end' and pos == tgt:
            hz = sum(1 for c in con if c[1] == 'h')
            if hz == 0 or floor_ok:
                return True, hz
    return False, None


def run_room(R, near=2):
    log(f'### {R.name}; A={R.A}, H={R.H}, v={R.v}, h={R.h}, w={R.w}')
    log(f'   polygon {R.P}')
    tot = {'claimed rows': 0, 'claimed pairs': 0, 'claimed lit': 0, 'below rows': 0, 'below pairs': 0,
           'below lit (largest piece)': 0, 'below lit (all pieces)': 0}
    nearest = None
    for M in R.marks():
        d = M[1] - (R.H + R.h)
        for yy in range(1, 2 * R.H):
            B = R.H - F(yy, 2)
            Lb = R.L(d, B)
            ts = [F(i, 2) for i in range(1, 2 * R.A)]
            if Lb > 2 * R.A:
                tot['claimed rows'] += 1
                r = Lb / (2 * R.A)
                if nearest is None or r < nearest[0]:
                    nearest = (r, M, B)
                for t in ts:
                    tot['claimed pairs'] += 1
                    ok, _ = lit_by(R, M, t, B, 'largest')
                    tot['claimed lit'] += ok
                    if not ok:
                        log(f'   COUNTEREXAMPLE mark {fr(M)} target {fr((t, R.H - B))} L={Lb}')
            elif Lb > 2 * R.A - near:
                tot['below rows'] += 1
                for t in ts:
                    tot['below pairs'] += 1
                    tot['below lit (largest piece)'] += lit_by(R, M, t, B, 'largest')[0]
                    tot['below lit (all pieces)'] += lit_by(R, M, t, B, 'all')[0]
    log(f'   {tot}')
    if nearest:
        log(f'   nearest-to-equality claimed row: L/2A = {nearest[0]} ({float(nearest[0]):.4f}) mark {fr(nearest[1])} depth {nearest[2]}')
    check(tot['claimed lit'] == tot['claimed pairs'], f'{R.name}: every half-lattice target on every row with L>2A lit by the largest-piece shot')
    return tot


for R in (RB, RP, RC):
    run_room(R)

log('### equality row in B: mark (4,67/2), depth 21/2 (L = 12 = 2A, not claimed)')
M = (F(4), F(67, 2)); B = F(21, 2)
check(RB.L(F(1, 2), B) == 12, 'L(21/2) = 2A exactly at d=1/2')
miss = [t for t in [F(i, 2) for i in range(1, 12)] if not lit_by(RB, M, t, B, 'largest')[0]]
log(f'   targets on y={RB.H - B} missed by the largest-piece family: {[str(t) for t in miss]}')

log('### floor extension in B (bonus): rows with L(B) <= 2A, mark row d=1/2, via the reflected row B\'=2H-B')
nrow = npair = nlit = 0
hzs = set()
for M in RB.marks():
    d = F(1, 2)
    for yy in range(1, 64):
        B = 32 - F(yy, 2)
        if RB.L(d, B) > 12:
            continue
        Bp = 64 - B
        assert RB.L(d, Bp) > 24
        nrow += 1
        for t in [F(i, 2) for i in range(1, 12)]:
            npair += 1
            ok, hz = lit_by(RB, M, t, Bp, 'largest', floor_ok=True)
            nlit += ok
            hzs.add(hz)
log(f'   rows {nrow}, pairs {npair}, lit via reflected row {nlit}; floor bounces used {sorted(hzs)}')
check(nlit == npair and hzs == {1}, 'floor construction (one floor bounce) lights every half-lattice target on rows where direct descent is not claimed')
# application numerics for general delta in (0,1)
check(all(RB.L(F(99, 100), F(t)) > (2 + F(t)) / 2 for t in (1, 10, 22)) and (2 + 22) / 2 == 12 and (2 + 46) / 2 == 24 and 64 - 46 == 18,
      'B application: L(t) > (2+t)/2, direct for B>=22, floor (L(B\')>24 needs B\'>=46) for B<=18')


# ================================================================== note 2: nonspanning-entry
log('\n# Note 2: nonspanning-entry.md')
VR = [(0, 2), (0, 0), (1, 0), (1, 1), (5, 1), (5, 5), (4, 5), (4, 4), (2, 4), (2, 3), (3, 3), (3, 2)]
cellsR = cells_rect(0, 1, 0, 1) | cells_rect(0, 5, 1, 2) | cells_rect(3, 5, 2, 3) | cells_rect(2, 5, 3, 4) | cells_rect(4, 5, 4, 5)
PR = polygon(cellsR)
check(set(PR) == set(VR), 'ledger vertices = boundary of runs (0,1),(0,5),(3,5),(2,5),(4,5)')
check(same_class(turn_word(VR), 'LLLRLLLRLLRR'), f'turn word {turn_word(VR)} is LLLRLLLRLLRR up to rotation/reversal')
RUNS = [(0, 1), (0, 5), (3, 5), (2, 5), (4, 5)]   # level j: y in [j, j+1]
MOUTH = {1: (0, 1), 2: (3, 5), 3: (3, 5), 4: (4, 5)}


def through2(e, s):
    """From crossing (e,1) moving right with s per unit rise: [(pos, velocity sign)] at y=2,3,4, or None."""
    pos, vel, out = e, s, []
    for lev in (1, 2, 3):
        l, r = RUNS[lev]
        w = r - l
        X = pos - l + vel
        m = X % (2 * w)
        if m == 0 or m == w:
            return None
        pos = l + m if m < w else l + 2 * w - m
        if floor(X / w) % 2:
            vel = -vel
        a, b = MOUTH[lev + 1]
        if not (a < pos < b):
            return None
        out.append((pos, 1 if vel > 0 else -1))
    return out


log('## 3. Crossing sequence and perturbation rectangle')
e0, s0 = F(1, 2), F(16, 5)
seq = through2(e0, s0)
log(f'   crossings at y=2,3,4 (pos, sign): {[(str(p), g) for p, g in seq]}')
check([p for p, _ in seq] == [F(37, 10), F(31, 10), F(41, 10)] and seq[-1][1] == 1, 'sequence 37/10, 31/10, 41/10, final sign +')
forms = lambda e, s: (e + s, 10 - e - 2 * s, e + 3 * s - 6)
check(forms(e0, s0) == tuple(p for p, _ in seq), 'closed forms e+s, 10-e-2s, e+3s-6 match')
margins = [min(p - MOUTH[k][0], MOUTH[k][1] - p) for k, (p, _) in zip((2, 3, 4), seq)]
log(f'   baseline margins {[str(m) for m in margins]}')
ok = True
for de in (F(-1, 100), F(1, 100)):
    for ds in (F(-1, 100), F(1, 100)):
        r = through2(e0 + de, s0 + ds)
        ok &= r is not None and [p for p, _ in r] == list(forms(e0 + de, s0 + ds)) and [g for _, g in r] == [g for _, g in seq]
check(min(margins) == F(1, 10) and ok, 'min margin 1/10; closed rectangle corners keep the same sheets and signs (affine, so whole rectangle)')
# sheet margins for the folds themselves (developed coordinates stay in their sheets)
dev = [(e0 + s0, 0, 5), (e0 + 2 * s0, 3, 2), (10 - e0 - 3 * s0, 2, 3)]
log(f'   developed coords per band {[(str(X), l, w) for X, l, w in dev]}: distances to sheet lines '
    f'{[str(min((X - l) % w, w - (X - l) % w)) for X, l, w in dev]}')
ok = True
grid = [F(i, 400) for i in range(-3, 4)]
for k in range(0, 6):
    for de in grid:
        for ds in grid:
            ok &= through2(e0 + de, s0 + ds + 60 * k) == through2(e0 + de, s0 + ds)
check(ok, 's -> s+60k (k=0..5) leaves every signed mouth crossing unchanged on a 7x7 grid of the rectangle')
check(all(60 % (2 * (r - l)) == 0 for l, r in RUNS[1:4]) and [2 * (r - l) for l, r in RUNS[1:4]] == [10, 4, 6], 'doubled widths 10, 4, 6 divide 60')

log('## 3b. Exact replay S=(3/10,3/4) -> T=(43/10,9/2), direction (-16,5)')
S, T = (F(3, 10), F(3, 4)), (F(43, 10), F(9, 2))
D = T[1] - S[1]
st, pos, con = trace(PR, S, (S[0] - F(16, 5) * D, T[1]))
log(f'   {st} at {fr(pos)}, contacts {[fr(c[0]) for c in con]}')
check(st == 'end' and pos == T and [c[0] for c in con] == [(0, F(27, 32)), (5, F(77, 32)), (2, F(107, 32)), (5, F(137, 32))],
      'tracer returns T exactly with reflections (0,27/32),(5,77/32),(2,107/32),(5,137/32)')


def endpoints(e, s, a, b):
    """Physical source abscissa (row 1-a) and target abscissa (row 4+b); None if illegal."""
    src = fold(e - a * s, 0, 1)
    seq = through2(e, s)
    if src is None or seq is None:
        return None
    p4, g4 = seq[-1]
    tg = fold(p4 + g4 * s * b, 4, 1)
    if tg is None:
        return None
    return src, tg, seq


def solve_pair(a, b, x, z, kmax=None):
    """The note's construction: nearest translate under s->s+60k, then exact correction. Returns (k, de, ds) or None."""
    x0b = e0 - a * s0
    z0b = F(41, 10) + b * s0
    best = None
    # translates are periodic; scan one full period of k (q*q') or kmax
    qa, qb = (30 * a).denominator, (30 * b).denominator
    K = kmax if kmax is not None else qa * qb // gcd(qa, qb)
    for k in range(K):
        x0 = (x0b - 60 * k * a) % 2
        z0 = (z0b + 60 * k * b - 4) % 2 + 4
        dx = x - x0; dx = (dx + 1) % 2 - 1
        dz = z - z0; dz = (dz + 1) % 2 - 1
        m = max(abs(dx), abs(dz))
        if best is None or m < best[0]:
            best = (m, k, dx, dz)
    m, k, dx, dz = best
    ds = (dz - dx) / (3 + a + b)
    de = dx + a * ds
    if abs(ds) < F(1, 100) and abs(de) < F(1, 100):
        return k, de, ds, m
    return None


log('## 3c. CRT replay a=1/101, b=1/103, x=3/4, z=17/4')
a, b, x, z = F(1, 101), F(1, 103), F(3, 4), F(17, 4)
r = solve_pair(a, b, x, z)
k, de, ds, m = r
log(f'   nearest translate: k={k}, max error {m}, de={de}, ds={ds}')
# the note rounds each coordinate to its nearest grid point and uses CRT; reproduce that k
x0b, z0b = e0 - a * s0, F(41, 10) + b * s0
def crt_k():
    # x: grid x0b - 60k a mod 2 has spacing 2/101; want residue r1 = round((x0b - x)/(2a*30)) ... solve directly
    jx = round(((x0b - x) % 2) / F(2, 101)) % 101       # 60 k a = 60k/101 == x0b - x (mod 2) -> 30k == jx (mod 101)
    jz = round(((z - z0b) % 2) / F(2, 103)) % 103       # 60 k b == z - z0b (mod 2) -> 30k == jz (mod 103)
    for kk in range(101 * 103):
        if (30 * kk - jx) % 101 == 0 and (30 * kk - jz) % 103 == 0:
            return kk
kc = crt_k()
dsn, den = F(-211, 314130), F(559, 125652)
log(f'   CRT with per-coordinate rounding: k={kc}')
check(kc == 2740, 'CRT k = 2740')
sN = s0 + 60 * 2740 + dsn
check(sN == F(10328795401, 62826), f'slope 16/5+60*2740+ds = {sN}')
eN = e0 + den
ep = endpoints(eN, sN, a, b)
log(f'   endpoints {ep[0]}, {ep[1]}; mouths {[str(p) for p, _ in ep[2]]}')
check(ep[0] == (F(3, 4), 1) and ep[1][0] == F(17, 4), 'folding gives exactly 3/4 and 17/4')
check([p for p, _ in ep[2]] == [F(155129, 41884), F(389131, 125652), F(515479, 125652)] and ep[2][-1][1] == 1 and eN == F(63385, 125652),
      'mouth abscissas 63385/125652, 155129/41884, 389131/125652, 515479/125652 and final sign +')
check(abs(den) < F(1, 100) and abs(dsn) < F(1, 100), 'corrections inside the rectangle')
t1 = time.process_time()
S2 = (x, 1 - a)
Dt = (4 + b) - (1 - a)
sgn0 = ep[0][1]  # physical upward velocity at source is sign*s
st, pos, con = trace(PR, S2, (S2[0] + sgn0 * sN * Dt, 4 + b))
log(f'   full Fraction trace: {st} at {fr(pos)}; {len(con)} reflections; {time.process_time() - t1:.1f}s')
check(st == 'end' and pos == (z, 4 + b), 'exact tracer reaches (17/4, 4+1/103) from (3/4, 100/101)')

log('## 4. Full-row theorem: which rows, which pairs')
# case 2 rows a=1/101, b=1/103: pairs on a grid incl. near-wall abscissas, by the construction + fold verifier
xs = [F(1, 1000), F(1, 8), F(1, 2), F(3, 4), F(999, 1000)]
zs = [4 + t for t in xs]
good = 0
for xx in xs:
    for zz in zs:
        r = solve_pair(a, b, xx, zz)
        if r:
            k, de, ds, _ = r
            ep = endpoints(e0 + de, s0 + 60 * k + ds, a, b)
            good += ep is not None and ep[0][0] == xx and ep[1][0] == zz
check(good == 25, f'case 2 (a=1/101,b=1/103): construction hits all 25 test pairs exactly ({good})')
# half-lattice rows of the realization: a = b = 1/2; interior half-lattice marks there
hl_src = [(F(i, 2), F(1, 2)) for i in range(1, 2)]
hl_tgt = [(F(i, 2), F(9, 2)) for i in range(9, 10)]
log(f'   half-lattice rows y=1/2 (bottom tip) and y=9/2 (top tip); interior half-lattice marks {[fr(p) for p in hl_src]} {[fr(p) for p in hl_tgt]}')
a = b = F(1, 2)
log(f'   30a = {30*a}, 30b = {30*b}: integers, so conditions 1 and 2 both fail; 60k*a = 30k = 0 mod 2 (no rotation)')
r = solve_pair(a, b, F(1, 2), F(9, 2), kmax=1)
log(f'   theorem family for (1/2,1/2)-(9/2,9/2): {"certified" if r else "not in the certified patch image"}')
check(r is None, 'the half-lattice pair is outside the certified patch (nearest error 2/5 vs radius ~1/100)')
# what the patch does certify on those rows: image box of the rectangle at a=b=1/2
x0, z0 = e0 - s0 / 2, F(41, 10) + s0 / 2
log(f'   certified set at a=b=1/2: (x,z) near fold({x0})={fold(x0,0,1)}, fold({z0})={fold(z0,4,1)}; '
    f'image of |de|,|ds|<1/100 under (de - ds/2, de + 7ds/2): parallelogram of half-widths 3/200, 9/200')


def lit_pair_search(P, S, T, H=40, maxrefl=80):
    """Bounded direct search for a legal path S->T in this named room (no room search)."""
    for p in range(-H, H + 1):
        for q in range(-H, H + 1):
            if (p, q) == (0, 0) or gcd(abs(p), abs(q)) != 1:
                continue
            X, Y = S
            vx, vy = F(p), F(q)
            tau = F(0)
            for _ in range(maxrefl):
                st, pos, con = trace(P, (X, Y), (X + 100 * vx, Y + 100 * vy), maxrefl=1)
                nxt = con[0][0] if con else pos
                # does T lie on segment (X,Y)->nxt ?
                ux, uy = nxt[0] - X, nxt[1] - Y
                if ux * (T[1] - Y) == uy * (T[0] - X) and min(X, nxt[0]) <= T[0] <= max(X, nxt[0]) and min(Y, nxt[1]) <= T[1] <= max(Y, nxt[1]) and (T[0] - X) * ux + (T[1] - Y) * uy > 0:
                    tau += ((T[0] - X) / vx) if vx else ((T[1] - Y) / vy)
                    st2, pos2, con2 = trace(P, S, (S[0] + tau * p, S[1] + tau * q))
                    return (p, q), _, st2, pos2 == T, len(con2)
                tau += ((nxt[0] - X) / vx) if vx else ((nxt[1] - Y) / vy)
                if st == 'corner' or not con:
                    break
                (X, Y), kind = con[0]
                if kind == 'v': vx = -vx
                else: vy = -vy
    return None


t1 = time.process_time()
res = lit_pair_search(PR, (F(1, 2), F(1, 2)), (F(9, 2), F(9, 2)), H=12, maxrefl=60)
log(f'   bounded search (|p|,|q|<=12, <=60 reflections) for (1/2,1/2)-(9/2,9/2): (direction, reflections before T, retrace status, retrace hits T, retrace contacts) = {res}; {time.process_time() - t1:.1f}s')
check(res is not None and res[2] == 'end' and res[3], 'the half-lattice pair is lit by another path (independent full retrace)')
# rows with q<101 (e.g. a=1/97): condition 2 not met; does the construction still fail somewhere?
a, b = F(1, 97), F(1, 103)
fails = [(xx, zz) for xx in [F(i, 40) for i in range(1, 40)] for zz in [4 + F(j, 40) for j in range(1, 40, 6)] if solve_pair(a, b, xx, zz) is None]
log(f'   a=1/97 (q=97<101), b=1/103: construction fails on {len(fails)} of {39*7} grid pairs (condition 2 threshold matters: {bool(fails)})')

log('## 5. Generalization determinant')
for (a, b) in [(F(1, 101), F(1, 103)), (F(1, 2), F(1, 2))]:
    de_, ds_ = F(1, 10**6), F(1, 10**6)
    base = endpoints(e0, s0, a, b)
    pe = endpoints(e0 + de_, s0, a, b); ps = endpoints(e0, s0 + ds_, a, b)
    sx, sz = base[0][1], base[1][1]
    J = [[(pe[0][0] - base[0][0]) / de_ * sx, (ps[0][0] - base[0][0]) / ds_ * sx],
         [(pe[1][0] - base[1][0]) / de_ * sz, (ps[1][0] - base[1][0]) / ds_ * sz]]
    det = J[0][0] * J[1][1] - J[0][1] * J[1][0]
    check(J == [[1, -a], [1, 3 + b]] and det == 3 + a + b, f'a={a},b={b}: sign-corrected Jacobian {J}, det {det} = D+a+b')

log(f'\n## done: {len(FAIL)} failures {FAIL}; CPU {time.process_time() - T0:.1f}s')
