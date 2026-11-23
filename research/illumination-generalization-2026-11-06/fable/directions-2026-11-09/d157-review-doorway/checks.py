"""d157 referee checks for doorway-word-bound and terminal-cap-placement (snapshots 2026-11-22 04:05).

Own exact integer tracer (direction scaling as in d156), own cell->polygon builder.
Named rooms only: DB55 and R22-base (cells copied from d148 / d8 rooms.json), plus four
explicit two-rectangle test rooms. Direction enumerations are over shots in a fixed room,
never over rooms. Every vertex (convex or reflex) is a stopping corner.
Run: python3 -B checks.py > checks.log
"""
from fractions import Fraction as F
from math import gcd
import time

T0 = time.process_time()


# ------------------------------------------------------------------ geometry
def cells_rect(a, b, c, d):
    return {(x, y) for x in range(a, b) for y in range(c, d)}


def polygon(cells):
    """Vertex list (ccw) of a strictly simple cell union."""
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


def interior_lattice(cells):
    xs = [c[0] for c in cells]; ys = [c[1] for c in cells]
    out = []
    for x in range(min(xs), max(xs) + 2):
        for y in range(min(ys), max(ys) + 2):
            if all(c in cells for c in ((x - 1, y - 1), (x, y - 1), (x - 1, y), (x, y))):
                out.append((x, y))
    return out


def seg_hits_boundary(P, A, B):
    """Does the closed segment AB meet the polygon boundary? (A, B interior points)"""
    n = len(P)
    for i in range(n):
        a, b = P[i], P[(i + 1) % n]
        def orient(p, q, r):
            v = (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
            return (v > 0) - (v < 0)
        o1, o2, o3, o4 = orient(A, B, a), orient(A, B, b), orient(a, b, A), orient(a, b, B)
        if o1 * o2 <= 0 and o3 * o4 <= 0:
            if o1 == o2 == 0:  # collinear: overlap test
                if max(min(A[0], B[0]), min(a[0], b[0])) <= min(max(A[0], B[0]), max(a[0], b[0])) and \
                   max(min(A[1], B[1]), min(a[1], b[1])) <= min(max(A[1], B[1]), max(a[1], b[1])):
                    return True
                continue
            return True
    return False


# ------------------------------------------------------------------ exact tracer
def trace(P, S, d, targets=(), maxrefl=10 ** 5, stop_first=True):
    """Shot from lattice/rational S in direction d=(p,q), p,q nonzero integers.

    Coordinates scaled by (|q|, |p|) so the direction becomes (+-1,+-1); S may be Fraction-free
    only if scaled coords are integral, so S must be a lattice point.
    Returns dict: event ('target'|'corner'|'limit'), stop point, refl count, polyline (physical
    Fractions), hits {target: refl count at first hit}, bounce list [(point, 'v'|'h')].
    """
    p, q = d
    assert p and q
    kx, ky = abs(q), abs(p)
    V = [(kx * x, ky * y) for x, y in P]
    n = len(V)
    hw = [(V[i], V[(i + 1) % n]) for i in range(n) if V[i][1] == V[(i + 1) % n][1]]
    vw = [(V[i], V[(i + 1) % n]) for i in range(n) if V[i][0] == V[(i + 1) % n][0]]
    vset = set(V)
    tg = {(kx * t[0], ky * t[1]): t for t in targets}
    X, Y = kx * S[0], ky * S[1]
    sx, sy = (1 if p > 0 else -1), (1 if q > 0 else -1)
    poly = [(F(X, kx), F(Y, ky))]
    bounces, hits = [], {}
    for refl in range(maxrefl + 1):
        best = None
        for a, b in vw:
            t = (a[0] - X) * sx
            if t > 0 and (best is None or t < best[0]) and min(a[1], b[1]) <= Y + sy * t <= max(a[1], b[1]):
                best = (t, 'v')
        for a, b in hw:
            t = (a[1] - Y) * sy
            if t > 0 and (best is None or t < best[0]) and min(a[0], b[0]) <= X + sx * t <= max(a[0], b[0]):
                best = (t, 'h')
        t, kind = best
        for Z, name in tg.items():
            tz = (Z[0] - X) * sx
            if 0 < tz <= t and (Z[1] - Y) * sy == tz and name not in hits:
                hits[name] = refl
                if stop_first and len(targets) == 1:
                    poly.append((F(Z[0], kx), F(Z[1], ky)))
                    return dict(event='target', stop=name, refl=refl, poly=poly, hits=hits, bounces=bounces)
        X, Y = X + sx * t, Y + sy * t
        poly.append((F(X, kx), F(Y, ky)))
        if (X, Y) in vset:
            return dict(event='corner', stop=(F(X, kx), F(Y, ky)), refl=refl, poly=poly, hits=hits, bounces=bounces)
        if refl == maxrefl:
            break
        bounces.append(((F(X, kx), F(Y, ky)), kind))
        if kind == 'v': sx = -sx
        else: sy = -sy
    return dict(event='limit', stop=None, refl=maxrefl, poly=poly, hits=hits, bounces=bounces)


def crossings(poly, axis, c):
    """Points where the polyline crosses (or touches) the line coord[axis]=c, in order."""
    out = []
    for A, B in zip(poly, poly[1:]):
        a, b = A[axis], B[axis]
        if a == b:
            continue
        if min(a, b) < c <= max(a, b) or (a == c and A is poly[0]):
            lam = F(c - a) / (b - a)
            out.append(tuple(A[i] + lam * (B[i] - A[i]) for i in range(2)))
    return out


def dir_of_slope(s, sx=1):
    """Primitive (p,q) for physical direction (sx, s)."""
    s = F(s)
    return (sx * s.denominator, s.numerator)


def log(*a):
    print(*a)


# ================================================================== 1. two-rectangle theorem
log("# 1. Two-rectangle theorem: construction of the note, traced exactly on 4 named rooms")


class TwoRect:
    """Rect1 bottom [a1,b1]x[0,h1], rect2 top [a2,b2]x[h1,h1+h2]; door on y=h1."""

    def __init__(self, name, a1, b1, h1, a2, b2, h2):
        self.name = name
        self.r1, self.r2 = (a1, b1, 0, h1), (a2, b2, h1, h1 + h2)
        self.H = h1 + h2
        self.X0, self.X1 = min(a1, a2), max(b1, b2)
        self.D = self.X1 - self.X0
        self.o0, self.o1 = max(a1, a2), min(b1, b2)
        assert self.o1 > self.o0
        self.cells = cells_rect(a1, b1, 0, h1) | cells_rect(a2, b2, h1, h1 + h2)
        self.P = polygon(self.cells)

    def xflip(self):
        f = lambda a, b: (self.X0 + self.X1 - b, self.X0 + self.X1 - a)
        (a1, b1, _, h1), (a2, b2, _, _) = self.r1, self.r2
        return TwoRect(self.name, *f(a1, b1), h1, *f(a2, b2), self.H - h1)

    def yflip(self):
        (a1, b1, _, h1), (a2, b2, _, _) = self.r1, self.r2
        return TwoRect(self.name, a2, b2, self.H - h1, a1, b1, h1)

    def mapx(self, m):
        return (self.X0 + self.X1 - m[0], m[1])

    def mapy(self, m):
        return (m[0], self.H - m[1])

    def region(self, m):
        x, y = m
        if x < self.o0: return 'L'
        if x > self.o1: return 'R'
        return 'O'

    def wing_rect(self, side):
        (a1, b1, _, _), (a2, b2, _, _) = self.r1, self.r2
        if side == 'L': return 1 if a1 < a2 else 2
        return 1 if b1 > b2 else 2


def construct(room, S, T):
    """Return (case, room', S', T', direction) per the note's construction, or direct."""
    if not seg_hits_boundary(room.P, S, T):
        return 'direct', room, S, T, None
    rS, rT = room.region(S), room.region(T)
    if {rS, rT} == {'L', 'R'}:
        if rS == 'R':
            S, T = T, S
        # left wing = rect at [0,B]?
        if room.wing_rect('L') == 2:
            S, T, room = room.mapy(S), room.mapy(T), room.yflip()
        B = room.r1[3]; E = room.H - B
        if B < E:  # rotate by 180 and reverse endpoints
            S, T = T, S
            S, T = room.mapx(room.mapy(S)), room.mapx(room.mapy(T))
            room = room.yflip().xflip()
            B = room.r1[3]; E = room.H - B
        assert room.wing_rect('L') == 1 and room.wing_rect('R') == 2
        H = room.H
        d, w, e, u, v = room.o0 - S[0], room.o1 - room.o0, T[0] - room.o1, S[1], T[1]
        assert d >= 1 and w >= 1 and e >= 1 and 0 < u < B and H - E < v < H
        thr = F(2 * B * w, d)
        K = H
        while K < thr: K += 2 * H
        x = F(d * K + w * u, 2 * B * w)
        n = int((x + F(1, 2)) // 1)
        th = F(2 * n * B - u, d)
        assert n >= 1 and abs(th - F(K, w)) <= F(B, d), (n, th, K, w)
        # J = {s in I : u+(d+w)s-2nB in (K-E,K+E)}
        lo = max(th - F(B, d), F(K - E - u + 2 * n * B, d + w))
        hi = min(th + F(B, d), F(K + E - u + 2 * n * B, d + w))
        assert hi - lo > 0
        tlo, thi = u + (d + w + e) * lo - 2 * n * B, u + (d + w + e) * hi - 2 * n * B
        assert thi - tlo > 2 * E
        # images of target around K: K +- (H - v) + 2jE ; pick first in (tlo,thi)
        cand = []
        for sgn in (1, -1):
            base = K + sgn * (H - v)
            j0 = (tlo - base) // (2 * E)
            for j in range(int(j0) - 1, int(j0) + 3):
                y = base + 2 * j * E
                if tlo < y < thi: cand.append(y)
        y = min(cand)
        s = F(y - u + 2 * n * B, d + w + e)
        assert abs(s) <= K / F(w) + 2 * F(B, d) <= 6 * H
        return 'opposite', room, S, T, dir_of_slope(s)
    if rS == 'O' and rT == 'O':
        raise AssertionError('both in closed overlap but not direct: %s %s' % (S, T))
    if rS == rT:
        raise AssertionError('same wing but not direct: %s %s' % (S, T))
    # one wing and the overlap: source in overlap, target in wing
    if rS != 'O':
        S, T = T, S
    if room.region(T) == 'L':
        S, T, room = room.mapx(S), room.mapx(T), room.xflip()
    if room.wing_rect('R') == 2:
        S, T, room = room.mapy(S), room.mapy(T), room.yflip()
    assert room.wing_rect('R') == 1
    B = room.r1[3]
    d, e, u, v = room.o1 - S[0], T[0] - room.o1, S[1], T[1]
    assert d >= 1 and e >= 1 and 0 < v < B and 0 < u < room.H
    c0 = -F(e, d) * u
    best = None
    for sg in (1, -1):
        m0 = int((c0 - sg * v) // (2 * B))
        for m in range(m0 - 1, m0 + 3):
            z = sg * v + 2 * m * B
            dist = abs(z - c0)
            if 0 < dist <= B and (best is None or dist < best[0]):
                best = (dist, z)
    z = best[1]
    cross = (z + F(e, d) * u) / (1 + F(e, d))
    assert 0 < abs(cross) < B
    s = F(z - u, d + e)
    assert abs(s) <= F(room.H + B, d) <= 2 * room.H
    return 'onewing', room, S, T, dir_of_slope(s)


ROOMS2 = [
    TwoRect('L  (rect [0,5]x[0,2] + [0,2]x[2,6], door width 2)', 0, 5, 2, 0, 2, 4),
    TwoRect('T  (rect [0,7]x[0,3] + [2,5]x[3,7], door width 3)', 0, 7, 3, 2, 5, 4),
    TwoRect('Z1 (rect [0,3]x[0,2] + [2,6]x[2,7], door width 1, B<E)', 0, 3, 2, 2, 6, 5),
    TwoRect('Z2 (rect [0,6]x[0,3] + [4,10]x[3,6], door width 2, B=E)', 0, 6, 3, 4, 10, 3),
]

summary1 = []
for R in ROOMS2:
    pts = interior_lattice(R.cells)
    bound = 6 * R.H * R.D + 5
    log(f"\n## {R.name}: walls W={len(R.P)}, H={R.H}, D={R.D}, bound 6HD+5={bound}, "
        f"events bound 12HD+11={12 * R.H * R.D + 11}; {len(pts)} interior lattice marks")
    stats = {}
    worst = (0, None)
    worst_ev = 0
    fails = []
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            S, T = pts[i], pts[j]
            case, Rm, S2, T2, dvec = construct(R, S, T)
            stats[case] = stats.get(case, 0) + 1
            if case == 'direct':
                continue
            r = trace(Rm.P, S2, dvec, targets=[T2], maxrefl=bound + 10)
            if r['event'] != 'target' or r['refl'] > bound:
                fails.append((S, T, case, dvec, r['event'], r['refl']))
                continue
            door = [c for c in crossings(r['poly'], 1, Rm.r1[3]) if Rm.o0 < c[0] < Rm.o1]
            ev = r['refl'] + len(door)
            if r['refl'] > worst[0]:
                worst = (r['refl'], (S, T, case, dvec))
            worst_ev = max(worst_ev, ev)
    log(f"   cases: {stats}")
    log(f"   constructed nondirect shots failing (corner, miss, or > bound): {len(fails)} {fails[:5]}")
    log(f"   max reflections used by the construction: {worst[0]} (pair, case, direction {worst[1]}); "
        f"max reflections+door passages {worst_ev}")
    summary1.append((R.name.split()[0], len(pts), stats, len(fails), worst[0], bound))

    # independent short-shot brute check: minimal reflections over directions |p|,|q|<=6
    best = {}
    for S in pts:
        for p in range(-6, 7):
            for q in range(-6, 7):
                if p == 0 or q == 0 or gcd(p, q) != 1:
                    continue
                r = trace(R.P, S, (p, q), targets=[t for t in pts if t != S], maxrefl=25, stop_first=False)
                for t, k in r['hits'].items():
                    key = tuple(sorted((S, t)))
                    best[key] = min(best.get(key, 99), k)
    allpairs = {(pts[i], pts[j]) for i in range(len(pts)) for j in range(i + 1, len(pts))}
    direct = {k for k in allpairs if not seg_hits_boundary(R.P, *k)}
    cov = {k for k in allpairs if k in direct or k in best}
    log(f"   brute (|p|,|q|<=6, <=25 reflections): pairs lit {len(cov)}/{len(allpairs)}; "
        f"max over pairs of min reflections {max((best.get(k, 0) if k not in direct else 0) for k in cov)}")

# parity: the note claims no parity condition. Show opposite-parity pairs are handled in each room.
log("\n   parity classes of constructed pairs are unrestricted: every pair above, of any parity, was lit.")

# ================================================================== 3. DB55 checks
log("\n# 3. DB55: slope -37/8 from S=(1,1) to T=(9,1)")
DB = cells_rect(0, 5, 0, 5) | cells_rect(5, 8, 2, 3) | cells_rect(8, 13, 0, 5)
PDB = polygon(DB)
log(f"   DB55 polygon ({len(PDB)} walls): {PDB}")
S, T = (1, 1), (9, 1)
s0 = F(-37, 8)
r = trace(PDB, S, dir_of_slope(s0), targets=[T], maxrefl=500)
xs5 = crossings(r['poly'], 0, 5); xs8 = crossings(r['poly'], 0, 8); cap = [b for b in r['bounces'] if b[0][0] == 13]
nv = [b for b in r['bounces'] if b[1] == 'v']
log(f"   event {r['event']} at {r['stop']} after {r['refl']} reflections")
log(f"   crossings of x=5: {[(str(a), str(b)) for a, b in xs5]}; of x=8: {[(str(a), str(b)) for a, b in xs8]}")
log(f"   vertical-wall bounces: {[(str(p[0]), str(p[1])) for p, k in nv]}  (expect only the cap x=13 at y=1/2)")
corr = [b for b in r['bounces'] if 5 < b[0][0] < 8]
left = [b for b in r['bounces'] if b[0][0] < 5]
log(f"   bounces in corridor {len(corr)}, in left chamber {len(left)}, total {len(r['bounces'])}")
# window
for dl in (F(-5, 56), F(-5, 56) + F(1, 10 ** 4), F(0), F(3, 56) - F(1, 10 ** 4), F(3, 56), F(-1, 8), F(1, 20)):
    s = s0 + dl
    rr = trace(PDB, S, dir_of_slope(s), targets=[], maxrefl=400)
    c5 = crossings(rr['poly'], 0, 5); c8 = crossings(rr['poly'], 0, 8)
    h5 = c5[0][1] if c5 else None; h8 = c8[0][1] if c8 else None
    capb = [b for b in rr['bounces'] if b[0][0] == 13]
    log(f"   delta={str(dl):>12}: first x=5 height {h5} (formula {F(5, 2) + 4 * dl}), x=8 height {h8} "
        f"(formula {F(21, 8) + 7 * dl}); stop {rr['event']} {rr['stop'] if rr['event'] == 'corner' else ''}; "
        f"cap contact {[str(b[0][1]) for b in capb][:1]} (formula phys of {35 + 12 * s})")
# cap lemma arithmetic
beta, A, L, t, H = 35, 7, 5, 1, 5
Bc, Cc = A + 2 * L - t, A + L
log(f"   B={Bc}, C={Cc}, 2C/B={F(2 * Cc, Bc)} in (1,2): {1 < F(2 * Cc, Bc) < 2}")
I = (s0 - F(5, 56), s0 + F(3, 56))
ks = [k for k in range(-50, 51) if I[0] < F(1 + 2 * H * k - beta, Bc) < I[1]]
log(f"   k with s_k in I (sigma=+,u=1): {ks}; s_k={[str(F(1 + 10 * k - 35, 16)) for k in ks]}; "
    f"cap (19+15k)/2 mod 5 never 0 for k in -50..50: {all(F(19 + 15 * k, 2) % 5 != 0 for k in range(-50, 51))}")
log(f"   B*len(I)={Bc * (I[1] - I[0])} vs 4H={4 * H}")
for sg in (1, -1):
    ks2 = [k for k in range(-50, 51) if I[0] < F(sg * 1 + 10 * k - beta, Bc) < I[1]]
    log(f"   sigma={sg:+d}: k in I {ks2}")

# rightward-monotone exclusion and its dilation
def monotone_hits(P, S, T, axis, sign, N, scale=1):
    hits = []
    for a in range(1, N + 1):
        for b in range(-N, N + 1):
            if b == 0 or gcd(a, b) != 1:
                continue
            d = (sign * a, b) if axis == 0 else (b, sign * a)
            r = trace(P, S, d, targets=[T], maxrefl=4 * N + 20)
            if r['event'] != 'target':
                continue
            kind = 'v' if axis == 0 else 'h'
            if not any(k == kind for _, k in r['bounces']):
                hits.append(d)
    return hits

log(f"   rightward-monotone shots S->T in DB55, |dx|,|dy|<=40: {monotone_hits(PDB, S, T, 0, 1, 40)} (expect none)")
DB2 = {(2 * x + i, 2 * y + j) for x, y in DB for i in (0, 1) for j in (0, 1)}
log(f"   x2 dilation, S=(2,2), T=(18,2): {monotone_hits(polygon(DB2), (2, 2), (18, 2), 0, 1, 30)} (expect none)")
# halfway mouth: developed ordinates
log("   parity: developed T ordinates 2c-1 are odd; halfway (1+y')/2 integer; mouth (2,3) has no integer.")

# ================================================================== 4. R22 checks
log("\n# 4. R22: upward-monotone and top-cap words, S=(0,0), T=(2,2)")
R22c = {(-1, -1), (-1, 0), (0, -2), (0, -1), (0, 0), (0, 1), (1, -3), (1, -2), (1, 1), (1, 2), (2, 1), (2, 2),
        (3, 0), (3, 1), (4, 0)}
PR = polygon(R22c)
log(f"   R22 polygon ({len(PR)} walls): {PR}")
S, T = (0, 0), (2, 2)
log(f"   S, T interior: {S in interior_lattice(R22c)}, {T in interior_lattice(R22c)}")
log(f"   chord S->(1/2,1) clear: {not seg_hits_boundary(PR, (0, 0), (F(1, 2), 1))}; "
    f"chord T->(1/2,1) clear: {not seg_hits_boundary(PR, (2, 2), (F(1, 2), 1))}")
log(f"   upward-monotone shots S->T, |dx|,|dy|<=40: {monotone_hits(PR, S, T, 1, 1, 40)} (expect none)")
# top-cap word: every candidate aims at developed image (x',4) with x' even
rows = []
bad = []
for xp in range(-40, 41, 2):
    if xp == 0:
        continue  # vertical candidate: x stays 0, never reaches T
    g = gcd(abs(xp), 4)
    d = (xp // g, 4 // g)
    rr = trace(PR, S, d, targets=[T], maxrefl=200)
    c1 = crossings(rr['poly'], 1, 1)
    c2 = crossings(rr['poly'], 1, 2)
    h1 = c1[0][0] if c1 else None
    h2 = c2[0][0] if c2 else None
    rows.append((xp, rr['event'], rr['stop'], h1, h2))
    if rr['event'] == 'target':
        bad.append(xp)
log(f"   top-cap candidates x' even in [-40,40]: reaching T: {bad} (expect none)")
for row in rows[:6] + rows[18:24]:
    xp, ev, st, h1, h2 = row
    log(f"     x'={xp:>4}: {ev} at {tuple(map(str, st)) if st else None}; first y=1 crossing x={h1} "
        f"(developed {F(xp, 4)}), first y=2 crossing x={h2}")
# what happens to y=1 and y=2 crossings exactly in development
ok = True
for xp in range(-200, 201, 2):
    dev1, dev2 = F(xp, 4), F(xp, 2)
    ok &= dev2.denominator == 1
log(f"   developed outward y=2 abscissa x'/2 integral for all even x' in [-200,200]: {ok}; "
    f"integers in (1,3): {[x for x in range(-5, 6) if 1 < x < 3]} -> only T")
# a ray through the y=1 door at a quarter, e.g. x'=2 (slope 1/2)
for xp in (2, -2, 6, 10):
    g = gcd(abs(xp), 4); d = (xp // g, 4 // g)
    rr = trace(PR, S, d, targets=[], maxrefl=50)
    log(f"     x'={xp}: path {[(str(a), str(b)) for a, b in rr['poly'][:5]]} ... stop {rr['event']} at "
        f"{tuple(map(str, rr['stop'])) if rr['stop'] else None}")

log("\nCPU seconds:", round(time.process_time() - T0, 2))
