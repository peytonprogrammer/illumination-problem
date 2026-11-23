"""d162 referee checks for parallel-mouth-combs (snapshot 2026-11-22 05:25).

Exact Fraction arithmetic. polygon(), trace() and the hall-with-full-side-arms constructor are
copied from d161-review-adjarm/checks.py. The tracer stops at every vertex, convex or reflex.
Rooms: DB55 and two more explicit half-turn dumbbells; five explicit stacked halls that satisfy
8Ah <= cu; two that violate it; one two-sided member; the named rooms R22-base and DB55.
No room search. Every traced shot is the one the note constructs, except in section 4 where
failing pairs of the violating rooms get the d161 shot or a short list of the note's own
travel candidates E + 2mA.
Run: python3 -B checks.py > checks.log
"""
import json
import time
from fractions import Fraction as F
from itertools import combinations
from math import floor, gcd
from functools import reduce
from pathlib import Path

T0 = time.process_time()
HERE = Path(__file__).resolve().parent
ARCH = HERE.parent
H2 = F(1, 2)


def log(*a):
    print(*a, flush=True)


def cells_rect(a, b, c, d):
    return {(x, y) for x in range(a, b) for y in range(c, d)}


def polygon(cells):  # copied from d161
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


def trace(P, A, B, maxrefl=10**6):  # copied from d161
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


def interior(cells, p):
    xs = [int(p[0]) - 1, int(p[0])] if F(p[0]).denominator == 1 else [floor(p[0])]
    ys = [int(p[1]) - 1, int(p[1])] if F(p[1]).denominator == 1 else [floor(p[1])]
    return all((i, j) in cells for i in xs for j in ys)


def half_points(cells):
    xs = [c[0] for c in cells]; ys = [c[1] for c in cells]
    return [(F(i, 2), F(j, 2)) for i in range(2 * min(xs), 2 * max(xs) + 3)
            for j in range(2 * min(ys), 2 * max(ys) + 3) if interior(cells, (F(i, 2), F(j, 2)))]


def reflex(P):
    n = len(P)
    cr = lambda a, b, c: (b[0]-a[0])*(c[1]-b[1]) - (b[1]-a[1])*(c[0]-b[0])
    return sum(1 for i in range(n) if cr(P[i-1], P[i], P[(i+1) % n]) < 0)


def edge_gcds(P):
    n = len(P)
    hx = [abs(P[(i+1) % n][0]-P[i][0]) for i in range(n) if P[i][1] == P[(i+1) % n][1]]
    vy = [abs(P[(i+1) % n][1]-P[i][1]) for i in range(n) if P[i][0] == P[(i+1) % n][0]]
    return reduce(gcd, hx), reduce(gcd, vy)


def runs(cells, axis, k):
    idx = sorted(c[0] if axis == 'h' else c[1] for c in cells if (c[1] if axis == 'h' else c[0]) == k)
    out = []
    for i in idx:
        if out and out[-1][1] == i: out[-1][1] = i + 1
        else: out.append([i, i + 1])
    return out


def fr(p):
    return f"({p[0]}, {p[1]})"


DB = cells_rect(0, 5, 0, 5) | cells_rect(5, 8, 2, 3) | cells_rect(8, 13, 0, 5)

# ================================================================== 1. half-turn dumbbell
log("# 1. Half-turn dumbbell")


def dumbbell_shot(x0, x1, yc, w, S):
    """Note's shot from left-chamber mark S. Returns (B, k, e, T)."""
    b = F(x1 - x0) / 2
    a, p = F(x0) - S[0], S[1] - F(yc)
    v = -b * p / (a * w)
    k = floor(v + H2)
    e = (b * p + a * k * w) / (a + b)
    ctr = (F(x0) + b, F(yc) + k * w)
    B = (2 * ctr[0] - S[0], 2 * ctr[1] - S[1])
    T = (2 * (F(x0) + b) - S[0], 2 * F(yc) - S[1])
    return B, k, e, T, a, b, abs(v - k) == H2


def path_points(S, con, end):
    return [S] + [c[0] for c in con] + [end]


def crossing(pts, x):
    for P_, Q_ in zip(pts, pts[1:]):
        if (P_[0] - x) * (Q_[0] - x) < 0 or Q_[0] == x and P_[0] != x:
            t = (x - P_[0]) / (Q_[0] - P_[0])
            return P_[1] + t * (Q_[1] - P_[1])
    return None


# DB55 named pair
P = polygon(DB)
S = (F(4), F(1))
B, k, e, T, a, b, tie = dumbbell_shot(5, 8, F(5, 2), 1, S)
ev, end, con = trace(P, S, B)
pts = path_points(S, con, end)
d = (B[0] - S[0], B[1] - S[1]); g = gcd(d[0].numerator * d[1].denominator, d[1].numerator * d[0].denominator)
log(f"   DB55 (4,1)->(9,4): a={a}, b={b}, p={S[1]-F(5,2)}, -bp/(aw)={-b*(S[1]-F(5,2))/a}, k={k}, e={e}, "
    f"bound aw/(2(a+b))={a/(2*(a+b))}")
log(f"   developed centre (13/2,{F(5,2)+k}); unfolded end {fr(B)}; direction ratio {d[1]/d[0]} (5,7 -> {F(7,5)})")
log(f"   traced: {ev}, end {fr(end)}, target {fr(T)}, contacts {[fr(c[0]) for c in con]}")
log(f"   mouth ordinates: x=5 -> {crossing(pts, 5)}, x=8 -> {crossing(pts, 8)}; physical point at x=13/2 -> {crossing(pts, F(13, 2))}")
log(f"   (1,1) half-turn partner: {fr((13 - 1, 5 - 1))} (so (1,1)-(9,1) is not a half-turn pair)")
# saved right-cap path, slope -37/8, x-travel 16
ev, end, con = trace(P, (1, 1), (17, 1 - 74))
pts = path_points((F(1), F(1)), con, end)
log(f"   saved cap path from (1,1), slope -37/8, x-travel 16: {ev}, end {fr(end)}")
log(f"      first x=5 crossing {crossing(pts, 5)}, first x=8 crossing {crossing(pts, 8)}, "
    f"vertical-wall contacts {[fr(c[0]) for c in con if c[1] == 'v']}")

DUMB = [
    ("DB55 (w=1, b=3/2)", DB, 5, 8, F(5, 2), 1),
    ("H2: [0,4]x[0,6] + corridor [4,10]x[1,3] + half-turn (w=2, b=3)",
     cells_rect(0, 4, 0, 6) | cells_rect(4, 10, 1, 3) | cells_rect(10, 14, -2, 4), 4, 10, 2, 2),
    ("H3: [0,3]x[0,7] + corridor [3,4]x[5,7] flush + half-turn (w=2, b=1/2)",
     cells_rect(0, 3, 0, 7) | cells_rect(3, 4, 5, 7) | cells_rect(4, 7, 5, 12), 3, 4, 6, 2),
]
for name, cells, x0, x1, yc, w in DUMB:
    P = polygon(cells)
    marks = [q for q in half_points(cells) if q[0] < x0]
    bad = ties = 0; maxr = 0; maxe = F(0); lit_contacts_ok = True
    for S in marks:
        B, k, e, T, a, b, tie = dumbbell_shot(x0, x1, yc, w, S)
        ties += tie
        assert abs(e) <= a * w / (2 * (a + b)) < F(w, 2)
        maxe = max(maxe, abs(e) / F(w, 2))
        ev, end, con = trace(P, S, B)
        ok = ev == 'end' and end == T and interior(cells, T)
        ok = ok and all(kd == 'h' and x0 < q[0] < x1 and q[1] in (yc - F(w, 2), yc + F(w, 2)) for q, kd in con)
        if ok:
            pts = path_points(S, con, end)
            ok = crossing(pts, x0) == yc + e and crossing(pts, x1) == yc - e and crossing(pts, F(x0 + x1, 2)) == yc
        maxr = max(maxr, len(con))
        if not ok:
            bad += 1
            if bad <= 3: log(f"      FAIL {fr(S)} k={k} e={e} {ev} {fr(end)}")
    log(f"   {name}: {len(P)} walls; {len(marks)} half-lattice chamber marks; failures {bad}; "
        f"tie cases (bp/(aw) half-integral) {ties}; max |e|/(w/2) {maxe}; max corridor reflections {maxr}")

# ================================================================== 2. stacked halls
log("\n# 2. Stacked halls: hall [0,A]x[0,c], rectangles (l,r,bottom,top)")


class Stack:
    def __init__(self, name, A, c, rects):
        self.name, self.A, self.c, self.rects = name, A, c, rects
        cl = cells_rect(0, A, 0, c)
        for l, r, b, t in rects:
            cl |= cells_rect(l, r, b, t)
        self.cells, self.P = cl, polygon(cl)
        self.ratio = max(F(8 * A * (t - c), (c * (r - l))) for l, r, b, t in rects) if rects else 0

    def rect_of(self, p):
        """Containing rectangle of an elevated mark, preferring the upper one at a seam."""
        for R in self.rects:
            l, r, b, t = R
            if l < p[0] < r and b <= p[1] < t:
                return R
        raise AssertionError(p)

    def root_of(self, x):
        for l, r, b, t in self.rects:
            if b == self.c and l < x < r:
                return (l, r)


def signs(room, p, target):
    """Allowed physical inward directions (+1 right, -1 left) for a mark."""
    if p[1] <= room.c:
        return (1, -1)
    l, r, b, t = room.rect_of(p)
    dr, dl = r - p[0], p[0] - l
    return (1, -1) if dr == dl else ((1,) if dr > dl else (-1,))


def stack_shots(room, S, T):
    """List of (B, label) shots of the note for S, T. label: 'direct', 'chosen', 'other'."""
    c, A = room.c, room.A
    ys, yt = S[1], T[1]
    if (ys < c and yt <= c) or (yt < c and ys <= c):
        return [(T, 'direct')]
    if ys == c and yt == c and room.root_of(S[0]) == room.root_of(T[0]):
        return [(T, 'direct')]
    out = []
    D = ys + yt; f = ys / D
    for ss in signs(room, S, False):
        for dt in signs(room, T, True):
            st = -dt
            Xs, Xt = ss * S[0], st * T[0]
            E = (Xt - Xs) % (2 * A)
            if E == 0: E = 2 * A
            cands = [E, E + 2 * A]
            corner = [((Xs + f * Ee) % A) == 0 for Ee in cands]
            assert not all(corner), (S, T)
            pick = 0 if not corner[0] else 1
            for i, Ee in enumerate(cands):
                if corner[i]: continue
                out.append(((S[0] + ss * Ee, ys - D), 'chosen' if i == pick else 'other', Ee / D))
    return out


def check_stack(room, S, T, shot, stats):
    B, lab = shot[0], shot[1]
    ev, end, con = trace(room.P, S, B)
    ok = ev == 'end' and end == T
    A, c = room.A, room.c
    if lab == 'direct':
        ok = ok and not con
    else:
        ok = ok and all((kd == 'h' and q[1] == 0 and 0 < q[0] < A) or (kd == 'v' and q[0] in (0, A) and 0 < q[1] < c)
                        for q, kd in con)
        # clearance ratio: horizontal displacement of each elevated leg over u/2
        slope = shot[2]
        for p in (S, T):
            if p[1] > c:
                l, r, b, t = room.rect_of(p)
                stats['clear'] = max(stats.get('clear', 0), slope * (p[1] - c) / (F(r - l) / 2))
    stats.setdefault(lab, [0, 0]); stats[lab][0] += 1
    if not ok:
        stats[lab][1] += 1
        stats.setdefault('fails', []).append((S, T, lab, ev, end))
    return ok


def stack_summary(room):
    P = room.P
    xs = sorted({x for x, _ in room.cells}); ys = sorted({y for _, y in room.cells})
    vmulti = [k for k in xs if len(runs(room.cells, 'v', k)) > 1]
    hmulti = [k for k in ys if len(runs(room.cells, 'h', k)) > 1]
    gx, gy = edge_gcds(P)
    return (f"{len(P)} walls, r={reflex(P)}, area {len(room.cells)}, edge gcds ({gx},{gy}), "
            f"max 8Ah/(cu) = {room.ratio}, columns with >1 component {len(vmulti)}, rows with >1 component {len(hmulti)}")


MEMBERS = [
    Stack("M1: A=6,c=48; [0,3]x[48,49] > child [1,3]x[49,50]; sibling [4,6]x[48,50]", 6, 48,
          [(0, 3, 48, 49), (1, 3, 49, 50), (4, 6, 48, 50)]),
    Stack("M2: A=8,c=64; siblings [1,3]h2, [4,5]h1, [6,8]h2", 8, 64,
          [(1, 3, 64, 66), (4, 5, 64, 65), (6, 8, 64, 66)]),
    Stack("M3: A=8,c=64; [0,4]x[64,65] > child [1,3]x[65,66]; sibling [5,7]x[64,66]", 8, 64,
          [(0, 4, 64, 65), (1, 3, 65, 66), (5, 7, 64, 66)]),
    Stack("M4: A=5,c=80; 3 levels [0,4]x[80,81] > [1,4]x[81,82] > [1,3]x[82,83]", 5, 80,
          [(0, 4, 80, 81), (1, 4, 81, 82), (1, 3, 82, 83)]),
    Stack("M5: A=9,c=72; four unit teeth [1,2],[3,4],[5,6],[7,8], h=1", 9, 72,
          [(1, 2, 72, 73), (3, 4, 72, 73), (5, 6, 72, 73), (7, 8, 72, 73)]),
]


def run_member(room, verbose=True):
    pts = half_points(room.cells)
    up = [p for p in pts if p[1] >= room.c]
    hall = [p for p in pts if p[1] < room.c]
    st = {}
    npairs = 0
    for S in up:
        for T in hall:
            npairs += 1
            for sh in stack_shots(room, S, T):
                check_stack(room, S, T, sh, st)
    for S, T in combinations(up, 2):
        npairs += 1
        for sh in stack_shots(room, S, T):
            check_stack(room, S, T, sh, st)
    return pts, up, hall, npairs, st


for room in MEMBERS:
    assert room.ratio <= 1
    pts, up, hall, npairs, st = run_member(room)
    log(f"   {room.name}\n      {stack_summary(room)}")
    log(f"      {len(pts)} half-lattice points ({len(up)} at y>=c); {npairs} pairs with a mark at y>=c; "
        f"shots [traced, failed]: direct {st.get('direct')}, chosen {st.get('chosen')}, other candidate {st.get('other')}; "
        f"max leg displacement/(u/2) {st.get('clear')}")
    for f_ in st.get('fails', [])[:4]:
        log(f"      FAIL {f_}")
    log(f"      hall-hall pairs: {len(hall)*(len(hall)-1)//2}, direct chords in the open convex hall (not traced)")

# f = 1/2 corner exclusion, arithmetic
log("   corner rule: for y_s=y_t the E-candidate floor abscissa (X_s+X_t)/2 is never in A*Z (checked inside stack_shots by assert)")

# ================================================================== 3. violating members
log("\n# 3. Members violating 8Ah <= cu")


class Room:  # d161 hall with full-side arms
    NORMAL = {'R': (1, 0), 'T': (0, 1), 'L': (-1, 0), 'B': (0, -1)}

    def __init__(self, name, x0, x1, y0, y1, arms):
        self.name, self.h, self.arms = name, (x0, x1, y0, y1), {k: d for k, d in arms.items() if d}
        c = cells_rect(x0, x1, y0, y1)
        for s, d in self.arms.items():
            c |= {'R': cells_rect(x1, x1 + d, y0, y1), 'L': cells_rect(x0 - d, x0, y0, y1),
                  'T': cells_rect(x0, x1, y1, y1 + d), 'B': cells_rect(x0, x1, y0 - d, y0)}[s]
        self.cells, self.P = c, polygon(c)

    def region(self, p):
        x0, x1, y0, y1 = self.h
        if x0 <= p[0] <= x1 and y0 <= p[1] <= y1: return 'H'
        return 'R' if p[0] > x1 else 'L' if p[0] < x0 else 'T' if p[1] > y1 else 'B'

    def corner(self, a, b):
        x0, x1, y0, y1 = self.h
        return (x1 if 'R' in (a, b) else x0, y1 if 'T' in (a, b) else y0)


OPP = {('R', 'L'), ('L', 'R'), ('T', 'B'), ('B', 'T')}


def first_above(a, r, period):
    return r + period * ((a - r) // period + 1)


def construct161(room, S, T):  # copied from d161
    rs, rt = room.region(S), room.region(T)
    if rs == 'H' or rt == 'H' or rs == rt or (rs, rt) in OPP:
        return S, T, T
    x0, x1, y0, y1 = room.h
    c = room.corner(rs, rt)
    na, nb = Room.NORMAL[rs], Room.NORMAL[rt]
    fwd = lambda p: (na[0] * (p[0] - c[0]) + na[1] * (p[1] - c[1]), nb[0] * (p[0] - c[0]) + nb[1] * (p[1] - c[1]))
    back = lambda q: (c[0] + na[0] * q[0] + nb[0] * q[1], c[1] + na[1] * q[0] + nb[1] * q[1])
    ext = lambda n: (x1 - x0) if n[0] else (y1 - y0)
    W, H = ext(na), ext(nb)
    s, t = fwd(S), fwd(T)
    X, U, V, Y = F(s[0]), -F(s[1]), -F(t[0]), F(t[1])
    if X * Y < U * V:
        return S, T, T
    if X >= V:
        a, b = X * Y / V, X * Y / V + H * (1 + X / V)
        Z = min(first_above(a, U, 2 * H), first_above(a, -U, 2 * H))
        return T, back((X, -Z)), S
    a, b = X * Y / U, X * Y / U + W * (1 + Y / U)
    Z = min(first_above(a, V, 2 * W), first_above(a, -V, 2 * W))
    return S, back((-Z, Y)), T


def extended(room, S, T, M=12):
    """The note's travel family with E + 2mA, m < M, every sign pair."""
    D = S[1] + T[1]
    for ss in (1, -1):
        for st in (1, -1):
            E = (st * T[0] - ss * S[0]) % (2 * room.A) or 2 * room.A
            for m in range(M):
                ev, end, con = trace(room.P, S, (S[0] + ss * (E + 2 * m * room.A), S[1] - D))
                if ev == 'end' and end == T:
                    return True
    return False


V1 = Stack("V1: A=6,c=12; tall tooth [2,3]x[12,16] (T shape)", 6, 12, [(2, 3, 12, 16)])
V2 = Stack("V2: M1 shape with c=24", 6, 24, [(0, 3, 24, 25), (1, 3, 25, 26), (4, 6, 24, 26)])
T161 = Room('T', 2, 3, 0, 12, {'L': 2, 'R': 3, 'T': 4})
assert T161.cells == V1.cells
for room in (V1, V2):
    pts, up, hall, npairs, st = run_member(room)
    fails = st.get('fails', [])
    fpairs = sorted({(f_[0], f_[1]) for f_ in fails if f_[2] == 'chosen'})
    # a pair fails the note's construction if every chosen shot for it fails
    allfail = []
    for S, T in fpairs:
        shots = [sh for sh in stack_shots(room, S, T) if sh[1] == 'chosen']
        if all(not (lambda r: r[0] == 'end' and r[1] == T)(trace(room.P, S, sh[0])) for sh in shots):
            allfail.append((S, T))
    log(f"   {room.name}\n      {stack_summary(room)}")
    log(f"      {npairs} pairs with a mark at y>=c; chosen shots [traced, failed] {st.get('chosen')}; "
        f"other candidate {st.get('other')}; max leg displacement/(u/2) {st.get('clear')}")
    log(f"      pairs where every sign choice of the chosen shot fails: {len(allfail)}; examples {[(fr(a), fr(b)) for a, b in allfail[:3]]}")
    if room is V1:
        res = 0
        for S, T in allfail:
            A_, B_, tg = construct161(T161, S, T)
            ev, end, con = trace(T161.P, A_, B_)
            res += ev == 'end' and end == (F(tg[0]), F(tg[1]))
        log(f"      d161 adjacent-arm shot (room = hall [2,3]x[0,12] + arms L2,R3,T4) lights {res}/{len(allfail)} of them")
    else:
        res = sum(extended(room, S, T) for S, T in allfail)
        log(f"      note's family E+2mA (m<12, all signs) lights {res}/{len(allfail)} of them")

# ================================================================== 3b. two-sided member
log("\n# 3b. Two-sided member (read; light test): A=24, c=192, top root [6,8]x[192,193], bottom root [16,18]x[-1,0]")


def two_sided():
    A, c = 24, 192
    cells = cells_rect(0, A, 0, c) | cells_rect(6, 8, c, c + 1) | cells_rect(16, 18, -1, 0)
    P = polygon(cells)
    mouths = {'top': (6, 8), 'bot': (16, 18)}
    pts = [p for p in half_points(cells)]
    stack = [p for p in pts if p[1] >= c or p[1] <= 0]
    hallL = [p for p in pts if 0 < p[1] < c and p[0].denominator == 1 and p[1].denominator == 1]
    bank = lambda p: 'top' if p[1] >= c else 'bot' if p[1] <= 0 else None
    bad = n = 0
    for S in stack:
        for T in hallL + [q for q in stack if q != S]:
            bs, bt = bank(S), bank(T)
            n += 1
            # map so that S's bank is the top bank
            g = (lambda p: p) if bs == 'top' else (lambda p: (p[0], c - p[1]))
            s_, t_ = g(S), g(T)
            ok = False
            # sign set: farther end of the stack rectangle for stack marks
            def sg(p, q):
                bq = bank(q)
                if bq is None:
                    return (1, -1)
                l, r = mouths[bq]
                dr, dl = r - q[0], q[0] - l
                return (1, -1) if dr == dl else ((1,) if dr > dl else (-1,))
            direct_case = (bt is not None and bt != bs) or (bt is None and t_[1] <= c - F(c, 4))
            for ss in sg(s_, S):
                for dt in sg(t_, T):
                    E = (-dt * t_[0] - ss * s_[0]) % (2 * A) or 2 * A
                    if direct_case:
                        B = (s_[0] + ss * E, t_[1])
                        cands = [B]
                    else:
                        D = s_[1] + t_[1]; f = s_[1] / D
                        lo, hi = mouths['bot' if bs == 'top' else 'top']  # x is unchanged by g
                        cands = []
                        for Ee in (E, E + 2 * A):
                            z = (ss * s_[0] + f * Ee) % (2 * A)
                            z = z if z <= A else 2 * A - z
                            if z % A != 0 and not (lo <= z <= hi):
                                cands.append((s_[0] + ss * Ee, s_[1] - D))
                        assert cands, (S, T)
                        cands = cands[:1]
                    Bp = g(cands[0])
                    ev, end, con = trace(P, S, Bp)
                    ok = ev == 'end' and end == T
                    if not ok:
                        bad += 1
                        if bad <= 3: log(f"      FAIL {fr(S)} {fr(T)} {ev} {fr(end)}")
    log(f"   {len(P)} walls; {len(stack)} stack/seam marks x ({len(hallL)} lattice hall marks + stack marks): {n} pairs, failures {bad}")


two_sided()

# ================================================================== 4. R22 and DB55
log("\n# 4. Sections of R22-base and DB55")
ROOMS = {r["id"]: {tuple(c) for c in r["cells"]} for r in json.load(open(ARCH / "d8-perturbation-test" / "rooms.json"))}
R22 = ROOMS["R22-base"]
for name, cells in (("R22-base", R22), ("DB55", DB)):
    P = polygon(cells)
    ys = sorted({c[1] for c in cells}); xs = sorted({c[0] for c in cells})
    log(f"   {name}: {len(P)} walls, r={reflex(P)}, area {len(cells)}, edge gcds {edge_gcds(P)}")
    log(f"      rows y=k+1/2 with >1 component: { {str(k + H2): runs(cells, 'h', k) for k in ys if len(runs(cells, 'h', k)) > 1} }")
    log(f"      columns x=k+1/2 with >1 component: { {str(k + H2): runs(cells, 'v', k) for k in xs if len(runs(cells, 'v', k)) > 1} }")
    bx = (min(xs), max(xs) + 1); by = (min(ys), max(ys) + 1)
    n = len(P)
    spans = [(P[i], P[(i+1) % n]) for i in range(n) if P[i][1] == P[(i+1) % n][1] and
             sorted((P[i][0], P[(i+1) % n][0])) == list(bx)]
    vspans = [(P[i], P[(i+1) % n]) for i in range(n) if P[i][0] == P[(i+1) % n][0] and
              sorted((P[i][1], P[(i+1) % n][1])) == list(by)]
    log(f"      bounding box {bx}x{by}; walls spanning full width {spans}; full height {vspans}")
# DB55 as a two-sided stacked hall
hall = cells_rect(0, 13, 2, 3)
top = cells_rect(0, 5, 3, 5) | cells_rect(8, 13, 3, 5)
bot = cells_rect(0, 5, 0, 2) | cells_rect(8, 13, 0, 2)
log(f"   DB55 = hall [0,13]x[2,3] + top roots [0,5],[8,13] (h=2) + bottom roots [0,5],[8,13] (h=2): {hall | top | bot == DB}")
log(f"      two-sided metric: 16Ah = {16*13*2} vs cu = {1*5}; mouth window [A/4,A/3] = [{F(13,4)},{F(13,3)}] vs mouths [0,5],[8,13]")
log(f"      one-sided metric with hall [0,13]x[2,3] needs a solid floor: bottom line y=2 is open on (0,5) and (8,13)")

log(f"\nCPU {time.process_time() - T0:.1f}s")
