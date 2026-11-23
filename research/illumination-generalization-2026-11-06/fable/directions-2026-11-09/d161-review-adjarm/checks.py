"""d161 referee checks for adjacent-arm-illumination (snapshot 2026-11-22 05:12).

Exact rational arithmetic throughout. polygon() is copied from d159-review-timepair/checks.py
(itself from d158). The tracer is a general-direction Fraction tracer: every vertex, convex or
reflex, stops the ray. Rooms: four explicit hall-with-full-side-arm members (the 6-wall L(3,3,3),
a T, the odd cross P_7, an unequal-depth plus), the 16 arm subsets of one hall, and the named
rooms R22-base (d8 rooms.json) and DB55 (d157 cells). No searches over rooms or directions:
every traced shot is the one the note constructs.
Run: python3 -B checks.py > checks.log
"""
import json
import random
import time
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

T0 = time.process_time()
HERE = Path(__file__).resolve().parent
ARCH = HERE.parent


def log(*a):
    print(*a, flush=True)


def cells_rect(a, b, c, d):
    return {(x, y) for x in range(a, b) for y in range(c, d)}


def polygon(cells):  # copied from d159 / d158
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


# ------------------------------------------------------------------ exact tracer
def trace(P, A, B, maxrefl=10**6):
    """Ray from A whose unfolded straight image ends at B. Returns (event, end, contacts).
    event 'end' means the full unfolded length was travelled without a corner."""
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


# ------------------------------------------------------------------ hall-with-arms rooms
class Room:
    """Hall [x0,x1]x[y0,y1]; arms: dict side->depth, side in R,T,L,B; each arm spans the full side."""
    NORMAL = {'R': (1, 0), 'T': (0, 1), 'L': (-1, 0), 'B': (0, -1)}

    def __init__(self, name, x0, x1, y0, y1, arms):
        self.name, self.h, self.arms = name, (x0, x1, y0, y1), {k: d for k, d in arms.items() if d}
        c = cells_rect(x0, x1, y0, y1)
        for s, d in self.arms.items():
            c |= {'R': cells_rect(x1, x1 + d, y0, y1), 'L': cells_rect(x0 - d, x0, y0, y1),
                  'T': cells_rect(x0, x1, y1, y1 + d), 'B': cells_rect(x0, x1, y0 - d, y0)}[s]
        self.cells, self.P = c, polygon(c)

    def interior(self, p):
        xs = [int(p[0]) - 1, int(p[0])] if F(p[0]).denominator == 1 else [int(F(p[0]) // 1)]
        ys = [int(p[1]) - 1, int(p[1])] if F(p[1]).denominator == 1 else [int(F(p[1]) // 1)]
        return all((i, j) in self.cells for i in xs for j in ys)

    def region(self, p):
        x0, x1, y0, y1 = self.h
        if x0 <= p[0] <= x1 and y0 <= p[1] <= y1: return 'H'
        return 'R' if p[0] > x1 else 'L' if p[0] < x0 else 'T' if p[1] > y1 else 'B'

    def corner(self, a, b):
        x0, x1, y0, y1 = self.h
        cx = x1 if 'R' in (a, b) else x0
        cy = y1 if 'T' in (a, b) else y0
        return (cx, cy)


OPP = {('R', 'L'), ('L', 'R'), ('T', 'B'), ('B', 'T')}


def first_above(a, r, period):
    """Least element of {r + period*j} strictly greater than a."""
    j = (a - r) // period + 1
    return r + period * j


def construct(room, S, T):
    """The note's shot. Returns (start, unfolded_end, target, info)."""
    rs, rt = room.region(S), room.region(T)
    if rs == 'H' or rt == 'H' or rs == rt or (rs, rt) in OPP:
        return S, T, T, dict(case='bar')
    x0, x1, y0, y1 = room.h
    c = room.corner(rs, rt)
    na, nb = Room.NORMAL[rs], Room.NORMAL[rt]
    # canonical map p -> (na.(p-c), nb.(p-c)); S-arm becomes the right arm, T-arm the upper arm
    fwd = lambda p: (na[0] * (p[0] - c[0]) + na[1] * (p[1] - c[1]), nb[0] * (p[0] - c[0]) + nb[1] * (p[1] - c[1]))
    back = lambda q: (c[0] + na[0] * q[0] + nb[0] * q[1], c[1] + na[1] * q[0] + nb[1] * q[1])
    ext = lambda n: (x1 - x0) if n[0] else (y1 - y0)
    W, H = ext(na), ext(nb)           # hall extent along S-arm axis, along T-arm axis
    s, t = fwd(S), fwd(T)
    X, U, V, Y = F(s[0]), -F(s[1]), -F(t[0]), F(t[1])
    assert X > 0 and 0 < U < H and Y > 0 and 0 < V < W, (S, T, X, U, V, Y)
    info = dict(X=X, U=U, V=V, Y=Y, H=H, W=W, arm=rs)
    if X * Y < U * V:
        return S, T, T, dict(info, case='direct')
    if X >= V:
        a, b = X * Y / V, X * Y / V + H * (1 + X / V)
        Z = min(first_above(a, U, 2 * H), first_above(a, -U, 2 * H))
        assert a < Z < b
        return T, back((X, -Z)), S, dict(info, case='right', Z=Z, arm=rs, win=(a, b))
    assert Y > U
    a, b = X * Y / U, X * Y / U + W * (1 + Y / U)
    Z = min(first_above(a, V, 2 * W), first_above(a, -V, 2 * W))
    assert a < Z < b
    return S, back((-Z, Y)), T, dict(info, case='upper', Z=Z, arm=rt, win=(a, b))


def contacts_ok(room, contacts, arm):
    """Every contact lies strictly beyond the mouth of the arm and on one of its two parallel sides."""
    x0, x1, y0, y1 = room.h
    for (x, y), kind in contacts:
        if arm in 'RL':
            if kind != 'h' or y not in (y0, y1) or not (x > x1 if arm == 'R' else x < x0): return False
        else:
            if kind != 'v' or x not in (x0, x1) or not (y > y1 if arm == 'T' else y < y0): return False
    return True


def run_pair(room, S, T, stats):
    A, B, tgt, info = construct(room, S, T)
    ev, end, con = trace(room.P, A, B)
    ok = ev == 'end' and end == (F(tgt[0]), F(tgt[1]))
    case = info['case']
    stats.setdefault(case, [0, 0]); stats[case][0] += 1
    if ok and case in ('right', 'upper'):
        ok = contacts_ok(room, con, info['arm'])
    if ok and case in ('bar', 'direct'):
        ok = not con
    if not ok:
        stats[case][1] += 1
        stats.setdefault('fails', []).append((S, T, info, ev, end))
    if case in ('right', 'upper', 'direct'):
        X, U, V, Y = info['X'], info['U'], info['V'], info['Y']
        if X * Y == U * V: stats['XY=UV'] = stats.get('XY=UV', 0) + 1
        if X == V and case == 'right': stats['X=V'] = stats.get('X=V', 0) + 1
        stats['maxrefl'] = max(stats.get('maxrefl', 0), len(con))
    return ok


def fr(p):
    return f"({p[0]}, {p[1]})"


# ================================================================== 1. definition
log("# 1. Class definition: one hall [0,3]x[0,2], all 16 arm subsets (depths R=2,T=3,L=1,B=4)")
DEP = {'R': 2, 'T': 3, 'L': 1, 'B': 4}
for k in range(5):
    for sub in combinations('RTLB', k):
        rm = Room('sub', 0, 3, 0, 2, {s: DEP[s] for s in sub})
        refl = sum(1 for i in range(len(rm.P))
                   if (lambda a, b, c: (b[0]-a[0])*(c[1]-b[1]) - (b[1]-a[1])*(c[0]-b[0]))(rm.P[i-1], rm.P[i], rm.P[(i+1) % len(rm.P)]) < 0)
        log(f"   arms {''.join(sub) or '-':4s}: walls {len(rm.P):2d}, reflex {refl}")
log("   (polygon() asserts strict simplicity for every subset)")

# ================================================================== 2. arithmetic checks of the proof
log("\n# 2. Window/gap arithmetic")
log("   gap set {2jH+-U}: gaps 2U, 2H-2U; window length H(1+X/V) >= 2H iff X >= V")
H, U = F(2), F(1)
for Y in (F(1), F(5)):
    X = V = F(1)
    a, b = X * Y / V, X * Y / V + H * (1 + X / V)
    z1 = first_above(a, U, 2 * H)
    log(f"   X=V=1,U=1,H=2,Y={Y}: window ({a},{b}); single progression U+4j gives {z1} "
        f"(strictly inside: {a < z1 < b}); both progressions give {min(z1, first_above(a, -U, 2*H))}")
log("   right-arm-only ablation (no reversal) on L(3,3,3) roles X=z,U=1,V=x,Y=y is in section 3")

# ================================================================== 3. named shots
log("\n# 3a. Six-wall L(3,3,3): S=(-3,3), T=(3,-1)")


def Lcells(x, y, z):
    return {(i, j) for i in range(-x - 2, z + 1) for j in range(-2, y + 1) if not (i >= 0 and j >= 0)}


L333 = Room('L(3,3,3)', -5, 0, -2, 0, {'T': 4, 'R': 4})
assert L333.cells == Lcells(3, 3, 3)
log(f"   L(3,3,3) equals hall [-5,0]x[-2,0] + top arm depth 4 + right arm depth 4: True; walls {len(L333.P)}")
S, T = (-3, 3), (3, -1)
x = y = z = 3; A_ = x + 2
Z = min(first_above(F(y * z), x, 2 * A_), first_above(F(y * z), -x, 2 * A_))
log(f"   note formula: least of 2j*5+-3 above yz=9 is Z={Z}; window ({y*z},{y*z + A_*(1+y)})")
ev, end, con = trace(L333.P, T, (-Z, y))
path = [T] + [c[0] for c in con] + [end]
log(f"   traced from T toward (-{Z},{y}): {ev}, path {' -> '.join(fr(p) for p in path[::-1])}")
log(f"   matches note (-3,3)->(0,9/4)->(-5,1)->(3,-1): {path[::-1] == [(-3,3),(0,F(9,4)),(-5,1),(3,-1)]}")
yc = F(0); xc = (y * z - Z) / F(1 + y)
log(f"   mouth crossing at y=0: x={xc} (in (-5,0): {-5 < xc < 0})")
A3, B3, tg, inf = construct(L333, S, T)
log(f"   generic constructor on this pair: case {inf['case']}, Z={inf.get('Z')}, unfolded end {fr(B3)}")
ev, end, con = trace(L333.P, S, T)
log(f"   direct shot S->T: {ev} at {fr(end)} after {len(con)} contacts")
n = len(L333.P)
for i in range(n):
    a, b = L333.P[i], L333.P[(i + 1) % n]
    img = (2 * a[0] - T[0], T[1]) if a[0] == b[0] else (T[0], 2 * a[1] - T[1])
    ev, end, con = trace(L333.P, S, img)
    reach = ev == 'end' and end == T
    log(f"   one-reflection image across wall {a}-{b}: {ev}, contacts {len(con)}, legal 1-reflection shot: {reach}")

log("\n# 3b. Odd cross P_7: S=(6,0), T=(0,6)")
P7 = Room('P_7', -2, 2, -2, 2, {'R': 5, 'T': 5, 'L': 5, 'B': 5})
A7, B7, tg7, inf = construct(P7, (6, 0), (0, 6))
log(f"   constructor: case {inf['case']}, X,U,V,Y,W,H = {inf['X']},{inf['U']},{inf['V']},{inf['Y']},{inf['W']},{inf['H']}, "
    f"window {inf['win'][0]},{inf['win'][1]}, Z={inf['Z']}, image {fr(B7)}")
ev, end, con = trace(P7.P, A7, B7)
log(f"   traced from T: {ev}, contacts {[fr(c[0]) for c in con]}, end {fr(end)}")
v = (F(B7[0]) - 0, F(B7[1]) - 6)
for lab, (k, c0) in (("x=2", (0, 2)), ("y=2", (1, 2))):
    t = (c0 - (0, 6)[k]) / v[k]
    log(f"   unfolded line crosses {lab} at {fr(((0 + v[0]*t), (6 + v[1]*t)))}")

# ================================================================== 4. exhaustive half-lattice tests
log("\n# 4. Exhaustive tests: all unordered pairs of distinct lattice and half-lattice interior points")
MEMBERS = [
    L333,
    Room('T: hall [0,3]x[0,2], L=4,R=1,T=5', 0, 3, 0, 2, {'L': 4, 'R': 1, 'T': 5}),
    P7,
    Room('plus: hall [0,3]x[0,4], R=1,T=6,L=3,B=2', 0, 3, 0, 4, {'R': 1, 'T': 6, 'L': 3, 'B': 2}),
]
ABL = 0
for rm in MEMBERS:
    xs = [p[0] for p in rm.P]; ys = [p[1] for p in rm.P]
    pts = [(F(i, 2), F(j, 2)) for i in range(2 * min(xs), 2 * max(xs) + 1)
           for j in range(2 * min(ys), 2 * max(ys) + 1) if rm.interior((F(i, 2), F(j, 2)))]
    st, bad = {}, 0
    abl_miss = 0
    for S, T in combinations(pts, 2):
        if not run_pair(rm, S, T, st): bad += 1
        # ablation: always use the S-arm window (no reversal), adjacent non-direct pairs only
        _, _, _, inf = construct(rm, S, T)
        if inf['case'] == 'upper':
            X, U_, V_, Y_, H_ = inf['X'], inf['U'], inf['V'], inf['Y'], inf['H']
            a, b = X * Y_ / V_, X * Y_ / V_ + H_ * (1 + X / V_)
            zz = min(first_above(a, U_, 2 * H_), first_above(a, -U_, 2 * H_))
            if not zz < b: abl_miss += 1
    cases = {k: v for k, v in st.items() if k in ('bar', 'direct', 'right', 'upper')}
    log(f"   {rm.name} ({len(rm.P)} walls): {len(pts)} points, {len(pts)*(len(pts)-1)//2} pairs; "
        f"cases [traced, failed] {cases}; XY=UV pairs {st.get('XY=UV', 0)}, X=V right-arm pairs {st.get('X=V', 0)}, "
        f"max reflections {st.get('maxrefl', 0)}; failures {bad}")
    log(f"      reversal-needed pairs where the S-arm window alone holds no image: {abl_miss}")
    for f_ in st.get('fails', [])[:5]:
        log(f"      FAIL {f_}")

# ================================================================== 5. random rational points
log("\n# 5. Random rational points (seed 161), 1500 pairs per member, denominators up to 997")
rnd = random.Random(161)
for rm in MEMBERS:
    xs = [p[0] for p in rm.P]; ys = [p[1] for p in rm.P]
    def rp():
        while True:
            d = rnd.randint(2, 997)
            p = (F(rnd.randint(min(xs) * d, max(xs) * d), d), F(rnd.randint(min(ys) * d, max(ys) * d), d))
            if rm.interior(p):
                return p
    st, bad = {}, 0
    for _ in range(1500):
        S, T = rp(), rp()
        if S == T: continue
        if not run_pair(rm, S, T, st): bad += 1
    cases = {k: v for k, v in st.items() if k in ('bar', 'direct', 'right', 'upper')}
    log(f"   {rm.name}: cases {cases}, max reflections {st.get('maxrefl', 0)}, failures {bad}")
    for f_ in st.get('fails', [])[:5]:
        log(f"      FAIL {f_}")
# mouth-line points (on the hall-arm seam) paired with points in adjacent arms
st, bad = {}, 0
rm = MEMBERS[3]
for _ in range(1500):
    d = rnd.randint(2, 997)
    S = (F(3), F(rnd.randint(1, 4 * d - 1), d))          # on the right mouth x=3
    T = (F(rnd.randint(1, 3 * d - 1), d), F(4) + F(rnd.randint(1, 6 * d - 1), d))   # in top arm
    if not run_pair(rm, S, T, st): bad += 1
log(f"   seam points on x=3 to top-arm points in {rm.name}: bar-case [traced, failed] {st.get('bar')}, failures {bad}")

# ================================================================== 6. R22 and DB55
log("\n# 6. Sections of R22-base and DB55")
ROOMS = {r["id"]: {tuple(c) for c in r["cells"]} for r in json.load(open(ARCH / "d8-perturbation-test" / "rooms.json"))}
R22 = ROOMS["R22-base"]
DB = cells_rect(0, 5, 0, 5) | cells_rect(5, 8, 2, 3) | cells_rect(8, 13, 0, 5)


def runs(cells, axis, k):
    """Open intervals of the line (y=k+1/2 if axis=='h' else x=k+1/2) inside the room."""
    idx = sorted(c[0] if axis == 'h' else c[1] for c in cells if (c[1] if axis == 'h' else c[0]) == k)
    out = []
    for i in idx:
        if out and out[-1][1] == i: out[-1][1] = i + 1
        else: out.append([i, i + 1])
    return out


for name, cells in (("R22-base", R22), ("DB55", DB)):
    P = polygon(cells)
    ys = sorted({c[1] for c in cells}); xs = sorted({c[0] for c in cells})
    hb = {k: runs(cells, 'h', k) for k in ys}; vb = {k: runs(cells, 'v', k) for k in xs}
    log(f"   {name}: {len(P)} walls; rows (y=k+1/2) with >1 component: "
        f"{ {k + F(1, 2): v for k, v in hb.items() if len(v) > 1} }")
    log(f"      columns (x=k+1/2) with >1 component: { {k + F(1, 2): v for k, v in vb.items() if len(v) > 1} }")
log(f"   DB55 line y=1 (integer, between rows 0 and 1): components {runs(DB, 'h', 0)} and {runs(DB, 'h', 1)} (rows agree)")
log(f"   R22 cells (0,1) [centre (1/2,3/2)] in room: {(0, 1) in R22}; (1,0) [centre (3/2,1/2)] in room: {(1, 0) in R22}")
log(f"   R22 marks {[r['marks'] for r in json.load(open(ARCH / 'd8-perturbation-test' / 'rooms.json')) if r['id'] == 'R22-base'][0]}")

# orthoconvex rooms outside the class: one-interval sections are necessary, not sufficient
for name, cells in (("S-tetromino", {(0, 0), (1, 0), (1, 1), (2, 1)}),
                    ("3-step staircase", {(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (0, 2)})):
    P = polygon(cells)
    multi = [k for k in {c[1] for c in cells} if len(runs(cells, 'h', k)) > 1] + \
            [k for k in {c[0] for c in cells} if len(runs(cells, 'v', k)) > 1]
    log(f"   {name}: {len(P)} walls, rows/columns with >1 component: {multi or 'none'} (orthoconvex, not hall+arms)")
log(f"\nCPU {time.process_time() - T0:.1f}s")
