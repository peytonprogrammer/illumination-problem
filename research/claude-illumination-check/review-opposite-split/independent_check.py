"""Independent check of the prescribed 26.7/26.8/26.11/26.12 segments.

No room, ray, direction, word, cylinder, or orbit search. Each case lists
the tiles that its hypotheses FORCE present (U) or absent (Z). A path must
use only U tiles, bounce only on U|Z edges, and avoid every lattice point.
Moving mirrors are detected from the pocket triangle, not hard-coded.
Q is computed by dual-number differentiation and by Section 3 formula (2).
"""
from fractions import Fraction as F
from math import gcd, atan2, pi
import json, sys

# ---------- canonical tiling ----------
def lab(p):
    x, y = p
    if x % 2 == 0 and y % 2 == 0: return 'A'
    if x % 2 and y % 2: return 'B'
    return 'C'

def tri(*v):
    t = frozenset(tuple(map(int, q)) for q in v)
    assert len(t) == 3 and sorted(lab(q) for q in t) == ['A', 'B', 'C'], v
    return t

def cell_tris(i, j):
    sq = [(i, j), (i + 1, j), (i + 1, j + 1), (i, j + 1)]
    a = [q for q in sq if lab(q) == 'A'][0]
    b = [q for q in sq if lab(q) == 'B'][0]
    return [tri(a, b, c) for c in sq if lab(c) == 'C']

def fan(a):
    """All 8 canonical triangles at A point a."""
    x, y = a
    out = set()
    for i in (x - 1, x):
        for j in (y - 1, y):
            out.update(t for t in cell_tris(i, j) if a in t)
    assert len(out) == 8
    return out

def cross(a, b): return a[0] * b[1] - a[1] * b[0]
def sub(a, b): return (a[0] - b[0], a[1] - b[1])
def add(a, b): return (a[0] + b[0], a[1] + b[1])
def mul(k, a): return (k * a[0], k * a[1])
def dot(a, b): return a[0] * b[0] + a[1] * b[1]

def contains(t, p):
    v = sorted(t)
    s = [cross(sub(v[(k + 1) % 3], v[k]), sub(p, v[k])) for k in range(3)]
    return all(c >= 0 for c in s) or all(c <= 0 for c in s)

def incident(p):
    x, y = p
    fx, fy = int(x // 1), int(y // 1)
    out = set()
    for i in (fx - 1, fx):
        for j in (fy - 1, fy):
            out.update(t for t in cell_tris(i, j) if contains(t, p))
    assert out
    return out

def is_lattice(p): return p[0].denominator == 1 and p[1].denominator == 1

# ---------- path checks ----------
def check_segment(a, b, U, log):
    d = sub(b, a)
    ts = {F(0), F(1)}
    for f in (lambda q: q[0], lambda q: q[1], lambda q: q[0] - q[1], lambda q: q[0] + q[1]):
        fa, fb = f(a), f(b)
        if fa == fb: continue
        lo, hi = min(fa, fb), max(fa, fb)
        for n in range(int(lo // 1) - 1, int(hi // 1) + 2):
            t = (n - fa) / (fb - fa)
            if 0 < t < 1: ts.add(t)
    ts = sorted(ts)
    samples = ts[1:-1] + [(x + y) / 2 for x, y in zip(ts, ts[1:])]
    for t in samples:
        p = add(a, mul(t, d))
        assert not is_lattice(p), ('lattice point inside open segment', a, b, p)
        need = incident(p)
        assert need <= U, ('segment needs unforced tile', a, b, p, [sorted(x) for x in need - U])
    log.append(('segment ok', a, b))

def edge_at(p, tangent):
    """The canonical edge on the line through p with this tangent, p interior."""
    if tangent == (1, 0):
        assert p[1].denominator == 1 and p[0].denominator > 1
        x0 = int(p[0] // 1); return ((x0, int(p[1])), (x0 + 1, int(p[1])))
    if tangent == (0, 1):
        assert p[0].denominator == 1 and p[1].denominator > 1
        y0 = int(p[1] // 1); return ((int(p[0]), y0), (int(p[0]), y0 + 1))
    if tangent == (1, 1):
        c = p[0] - p[1]; assert c.denominator == 1 and int(c) % 2 == 0
        x0 = int(p[0] // 1); assert p[0] != x0
        return ((x0, x0 - int(c)), (x0 + 1, x0 + 1 - int(c)))
    if tangent == (1, -1):
        c = p[0] + p[1]; assert c.denominator == 1 and int(c) % 2 == 0
        x0 = int(p[0] // 1); assert p[0] != x0
        return ((x0, int(c) - x0), (x0 + 1, int(c) - x0 - 1))
    raise AssertionError

def reflect_vec(v, tangent):
    n2 = dot(tangent, tangent)
    return sub(mul(F(2) * dot(v, tangent) / n2, tangent), v)

def check_bounce(prev, p, nxt, U, Z, pocket, log):
    din, dout = sub(p, prev), sub(nxt, p)
    hits = []
    for tg in ((1, 0), (0, 1), (1, 1), (1, -1)):
        r = reflect_vec(din, tg)
        if cross(r, dout) == 0 and dot(r, dout) > 0 and cross(tg, din) != 0:
            hits.append(tg)
    assert len(hits) == 1, ('not a unique specular reflection', prev, p, nxt)
    tg = hits[0]
    e = edge_at(p, tg)
    sides = [t for t in incident(p) if set(e) <= t]
    assert len(sides) == 2
    s_in = cross(tg, sub(prev, p))
    near = [t for t in sides if cross(tg, sub(sorted(t - set(e))[0], p)) * s_in > 0]
    far = [t for t in sides if t not in near]
    assert len(near) == 1 and len(far) == 1
    assert near[0] in U, ('incoming side not forced present', p)
    assert far[0] in Z, ('far side of mirror not forced absent', p, sorted(far[0]))
    moving = set(e) <= pocket
    log.append(('bounce ok', p, 'edge', e, 'MOVING' if moving else 'fixed'))
    return tg, e, moving

# ---------- dual numbers for d/dt ----------
class D:
    def __init__(s, v, d=F(0)): s.v, s.d = F(v), F(d)
    def __add__(s, o): o = o if isinstance(o, D) else D(o); return D(s.v + o.v, s.d + o.d)
    __radd__ = __add__
    def __sub__(s, o): o = o if isinstance(o, D) else D(o); return D(s.v - o.v, s.d - o.d)
    def __rsub__(s, o): return D(o) - s
    def __mul__(s, o): o = o if isinstance(o, D) else D(o); return D(s.v * o.v, s.v * o.d + s.d * o.v)
    __rmul__ = __mul__

def dreflect(pt, normal, c):
    """Reflect dual point pt in the line normal.x = c (c dual)."""
    n2 = F(dot(normal, normal))
    k = (pt[0] * normal[0] + pt[1] * normal[1] - c) * (F(2) / n2)
    return (pt[0] - k * normal[0], pt[1] - k * normal[1])

def line_of(e):
    (x1, y1), (x2, y2) = e
    normal = (y2 - y1, x1 - x2)
    return normal, normal[0] * x1 + normal[1] * y1

def linpart(normal):
    a, b = normal; n2 = F(a * a + b * b)
    return ((1 - 2 * a * a / n2, -2 * a * b / n2), (-2 * a * b / n2, 1 - 2 * b * b / n2))

def matmul(M, N): return tuple(tuple(sum(M[i][k] * N[k][j] for k in range(2)) for j in range(2)) for i in range(2))
def matvec(M, v): return (M[0][0] * v[0] + M[0][1] * v[1], M[1][0] * v[0] + M[1][1] * v[1])
I2 = ((F(1), F(0)), (F(0), F(1)))

# ---------- corner link / pi sector ----------
def wedge(t, p):
    q = [v for v in t if v != p]
    a = [atan2(v[1] - p[1], v[0] - p[0]) for v in q]
    lo, hi = sorted(a)
    if hi - lo > pi: lo, hi = hi, lo + 2 * pi
    return lo, hi

def occupied(p, U, Z):
    ts = incident(p)
    assert all(t in U or t in Z for t in ts), ('corner link not fully forced', p)
    return [wedge(t, p) for t in ts if t in U], sum(1 for t in ts if t in U)

def covered(theta0, theta1, wedges):
    """Is the closed arc [theta0, theta1] (ccw, theta1>theta0) inside the union?"""
    N = 720
    for k in range(N + 1):
        th = theta0 + (theta1 - theta0) * k / N
        ok = False
        for lo, hi in wedges:
            for s in (-4 * pi, -2 * pi, 0, 2 * pi, 4 * pi):
                if lo - 1e-12 <= th + s <= hi + 1e-12: ok = True
        if not ok: return False
    return True

def ang(v): return atan2(float(v[1]), float(v[0]))

def check_sector(corner, prev, nxt, flank, U, Z, log):
    wedges, nU = occupied(corner, U, Z)
    angle_deg = 0
    for t in incident(corner):
        if t in U:
            angle_deg += 90 if lab(corner) == 'C' else 45
    ts = ang(sub(prev, corner))          # source germ
    to = ang(sub(nxt, corner))           # physical outgoing germ
    if flank is None:
        assert abs(((to - ts) % (2 * pi)) - pi) < 1e-12, 'straight continuation not collinear'
        ok = covered(ts, ts + pi, wedges) or covered(to, to + pi, wedges)
        assert ok, 'straight pi arc leaves the physical link'
        log.append(('pi sector STRAIGHT inside one physical copy', corner, 'link deg', angle_deg))
        return angle_deg
    # flank: a wall ray from corner along direction flank
    phi = ang(flank)
    # the ray must be a wall: exactly one of the two tiles along it is present
    q = add(corner, flank)
    along = [t for t in incident(corner) if corner in t and tuple(q) in t]
    assert len(along) == 2 and sum(t in U for t in along) == 1 and sum(t in Z for t in along) == 1, ('flank is not a wall ray', corner, flank)
    nrm = lambda a: a % (2 * pi)
    ts, to, phi = nrm(ts), nrm(to), nrm(phi)
    tdev = nrm(2 * phi - to)              # developed outgoing germ across the flank
    gap = nrm(tdev - ts)
    assert abs(gap - pi) < 1e-9, 'developed germs are not opposite'
    found = []
    for sgn in (1, -1):                   # the two length-pi arcs starting at ts
        dist = nrm(sgn * (phi - ts))      # distance from ts to the flank along sgn
        if 1e-12 < dist < pi - 1e-12:     # flank crossed exactly once, strictly inside
            php = ts + sgn * dist
            orig = tuple(sorted((ts, php)))
            end = ts + sgn * pi
            refl_phys = tuple(sorted((php, 2 * php - end)))   # reflected part, mapped back
            assert abs(nrm(2 * php - end) - to) < 1e-9
            if covered(*orig, wedges) and covered(*refl_phys, wedges):
                found.append(sgn)
    assert len(found) == 1, ('no unique embedded pi sector through the flank', corner, found)
    log.append(('pi sector via fixed flank', corner, 'flank dir', flank, 'link deg', angle_deg))
    return angle_deg

# ---------- case runner ----------
def run_case(c):
    log = []
    U, Z, pocket, u = c['U'], c['Z'], c['pocket'], c['u']
    assert not (U & Z)
    first, second = c['first'], c['second']
    S, T, corner = first[0], second[-1], first[-1]
    assert S == (0, 0) and T == (4, 0) and second[0] == corner
    assert incident(S) <= U and incident(T) <= U, 'marks not interior'
    assert is_lattice(corner) and lab(corner) in 'BC'
    for path in (first, second):
        for a, b in zip(path, path[1:]): check_segment(a, b, U, log)
    mirrors = []  # (normal, offset, moving, position: before/after corner)
    for path, where in ((first, 'pre'), (second, 'post')):
        for a, p, b in zip(path, path[1:], path[2:]):
            tg, e, mv = check_bounce(a, p, b, U, Z, pocket, log)
            n, off = line_of(e)
            mirrors.append((n, off, mv, where))
    flank = c.get('flank')
    angle = check_sector(corner, first[-2], second[1], flank, U, Z, log)
    assert angle == c['corner_angle'], (angle, c['corner_angle'])
    # corner flank reflection inserted after the corner (any split is equivalent; checked below)
    seq = [m for m in mirrors if m[3] == 'pre']
    if flank is not None:
        fn = (-flank[1], flank[0]); seq_corner = (fn, dot(fn, corner), False, 'corner')
    else:
        seq_corner = None
    post = [m for m in mirrors if m[3] == 'post']
    full = seq + ([seq_corner] if seq_corner else []) + post
    corner_moves = corner in pocket
    # physical velocity unfolding: half-vectors and durations
    def unfold(path, mlist):
        R = I2; total = (F(0), F(0))
        for k, (a, b) in enumerate(zip(path, path[1:])):
            total = add(total, matvec(R, sub(b, a)))
            if k < len(mlist): R = matmul(R, linpart(mlist[k][0]))
        return total, R
    w1, Rp = unfold(first, seq)
    Rc = matmul(Rp, linpart(seq_corner[0])) if seq_corner else Rp
    w2r, _ = unfold(second, post)
    w2 = matvec(Rc, w2r)
    assert w1 == w2 == c['w'], (w1, w2, c['w'])
    assert gcd(int(w1[0]), int(w1[1])) == 1
    # dual-number development of ACTUAL T and of the corner
    def dev(pt, mlist):
        P = (D(pt[0]), D(pt[1]))
        for n, off, mv, _ in reversed(mlist):
            cdual = D(off, dot(n, u) if mv else 0)
            P = dreflect(P, n, cdual)
        return P
    Tp = dev(T, full)
    Cpt = (D(corner[0], u[0] if corner_moves else 0), D(corner[1], u[1] if corner_moves else 0))
    Cp = Cpt
    for n, off, mv, _ in reversed(seq):
        Cp = dreflect(Cp, n, D(off, dot(n, u) if mv else 0))
    Tv, Cv = (Tp[0].v, Tp[1].v), (Cp[0].v, Cp[1].v)
    assert sub(Cv, S) == sub(Tv, Cv) == c['w'], ('developed halves differ', Cv, Tv)
    Q = (Tp[0].d - 2 * Cp[0].d, Tp[1].d - 2 * Cp[1].d)
    # Section 3 formula (2): sum_{j>=p} L_j a_j - sum_{j<p} L_j a_j - 2 L_p v_c
    Q2 = (F(0), F(0)); L = I2; p_index = len(seq)
    for j, (n, off, mv, _) in enumerate(full):
        a_j = mul(F(2) * dot(n, u) / dot(n, n), n) if mv else (F(0), F(0))
        if j == p_index:
            vc = u if corner_moves else (F(0), F(0))
            Q2 = sub(Q2, mul(2, matvec(L, vc)))
        sign = 1 if j >= p_index else -1
        Q2 = add(Q2, mul(sign, matvec(L, a_j)))
        L = matmul(L, linpart(n))
    if p_index == len(full):
        vc = u if corner_moves else (F(0), F(0)); Q2 = sub(Q2, mul(2, matvec(L, vc)))
    assert Q == Q2, ('dual-number and formula (2) disagree', Q, Q2)
    # alternative split: corner flank counted BEFORE the corner
    if seq_corner:
        Lp2 = matmul(Rp, linpart(seq_corner[0]))
        vc = u if corner_moves else (F(0), F(0))
        assert matvec(Lp2, vc) == matvec(Rp, vc), 'split position changes corner term'
    moving = [m for m in full if m[2]]
    n_diag_moving = sum(1 for m in moving if m[0][0] != 0 and m[0][1] != 0)
    assert (Q[0] - n_diag_moving) % 2 == 0 and (Q[1] - n_diag_moving) % 2 == 0, 'parity criterion (3) violated'
    det = w1[0] * Q[1] - w1[1] * Q[0]
    assert Q != (0, 0) and det != 0
    assert Q == c['Q_claim'] and det == c['det_claim'], (Q, det)
    return dict(name=c['name'], w=[str(x) for x in w1], developed_corner=[str(x) for x in Cv],
                developed_actual_T=[str(x) for x in Tv], moving_ordinary_mirrors=len(moving),
                corner_moves=corner_moves, Q=[str(x) for x in Q], det=str(det),
                corner_angle_deg=angle, steps=len(log))

def P(x, y): return (F(x), F(y))

# ---------- forced tile sets ----------
S0, T0, M0 = (0, 0), (4, 0), (2, 0)
FULL = fan(S0) | fan(T0)
M_UP = {t for t in fan(M0) if all(q[1] >= 0 for q in t)}
assert len(M_UP) == 4
BASE_U = FULL | M_UP
BASE_Z = fan(M0) - M_UP

def only(a, keep):
    keep = set(keep); assert keep <= fan(a); return keep, fan(a) - keep

# opposite pocket at (4,-2): A=(4,-2), C=(4,-1), B=(5,-1)
POCK_OPP = tri((4, -2), (4, -1), (5, -1))
popp_U, popp_Z = only((4, -2), [POCK_OPP])
L_low_U, L_low_Z = only((6, 0), [tri((6, 0), (5, 0), (5, -1)), tri((6, 0), (6, -1), (5, -1))])
NON_CENTER_Z = fan((6, -2)) | fan((2, -2)) | fan((6, 2))  # not centers in the 26.7 list
OPP_U = BASE_U | popp_U | L_low_U
OPP_Z = BASE_Z | popp_Z | L_low_Z | NON_CENTER_Z

N_right_tri = tri((2, 2), (2, 1), (3, 1)); N_left_tri = tri((2, 2), (2, 1), (1, 1))
N_right_sq2 = tri((2, 2), (3, 2), (3, 1)); N_left_sq2 = tri((2, 2), (1, 2), (1, 1))
# N is a leaf with one portal and m<=2 (q=0 square or q=1 triangle).
N_right_Z = fan((2, 2)) - {N_right_tri, N_right_sq2}
N_left_Z = fan((2, 2)) - {N_left_tri, N_left_sq2}

Tup_left_tri = tri((4, 2), (4, 1), (3, 1)); Tup_left_sq2 = tri((4, 2), (3, 2), (3, 1))
Tup_right_tri = tri((4, 2), (4, 1), (5, 1)); Tup_right_sq2 = tri((4, 2), (5, 2), (5, 1))

pocket_opp = {(4, -2), (4, -1), (5, -1)}
cases = []
# 26.8: N right (left central flank fixed); N size and T-up unknown
cases.append(dict(name='26.8 opposite, N right, fixed flank at B',
    U=OPP_U | {N_right_tri}, Z=OPP_Z | N_right_Z, pocket=pocket_opp, u=P(1, 0),
    first=[P(0, 0), P(F(5, 3), 1), P(5, -1)],
    second=[P(5, -1), P(6, F(-2, 5)), P(F(16, 3), 0), P(F(11, 3), -1), P(3, F(-3, 5)), P(4, 0)],
    flank=(1, 0), corner_angle=225, w=P(5, 3), Q_claim=P(-2, 0), det_claim=6))
# 26.11: N left, T-up left m=1
U11 = OPP_U | {Tup_left_tri}
Z11 = OPP_Z | N_left_Z | (fan((4, 2)) - {Tup_left_tri})
first11 = [P(0, 0), P(F(7, 3), 1), P(6, F(-4, 7)), P(5, -1)]
cases.append(dict(name='26.11 opposite, N left, T-up left m=1, straight pi',
    U=U11, Z=Z11, pocket=pocket_opp, u=P(1, 0), first=first11,
    second=[P(5, -1), P(4, F(-10, 7)), P(F(22, 5), F(-8, 5)), P(F(16, 5), F(6, 5)), P(5, F(3, 7)), P(4, 0)],
    flank=None, corner_angle=225, w=P(7, 3), Q_claim=P(1, 1), det_claim=4))
# 26.12: N left, T-up left m=2 square
U12 = OPP_U | {Tup_left_tri, Tup_left_sq2}
Z12 = OPP_Z | N_left_Z | (fan((4, 2)) - {Tup_left_tri, Tup_left_sq2})
cases.append(dict(name='26.12 opposite, N left, T-up left m=2 square, straight pi',
    U=U12, Z=Z12, pocket=pocket_opp, u=P(1, 0), first=first11,
    second=[P(5, -1), P(4, F(-10, 7)), P(F(22, 5), F(-8, 5)), P(3, F(5, 3)), P(F(22, 7), 2), P(4, 0)],
    flank=None, corner_angle=225, w=P(7, 3), Q_claim=P(1, 1), det_claim=4))

# 26.7 corridor-side pocket at (4,2), slide u=(1,0)
L_up_rect_U, L_up_rect_Z = only((6, 0), [tri((6, 0), (5, 0), (5, 1)), tri((6, 0), (6, 1), (5, 1))])
L_up_tri_U, L_up_tri_Z = only((6, 0), [tri((6, 0), (5, 0), (5, 1))])
L_low_any_Z = fan((6, 0)) - {tri((6, 0), (5, 0), (5, -1)), tri((6, 0), (6, -1), (5, -1))}
# upper rectangle: B=(5,1), pocket = T-up right triangle
pu, pz = only((4, 2), [Tup_right_tri])
cases.append(dict(name='26.7 corridor, L upper rectangle, B=(5,1), midpoint C',
    U=BASE_U | L_up_rect_U | pu, Z=BASE_Z | L_up_rect_Z | pz | fan((6, 2)),
    pocket={(4, 2), (4, 1), (5, 1)}, u=P(1, 0),
    first=[P(0, 0), P(4, 1)], second=[P(4, 1), P(6, F(1, 2)), P(4, 0)],
    flank=(-1, 0), corner_angle=270, w=P(4, 1), Q_claim=P(-2, 0), det_claim=2))
# upper triangle: B=(3,1), pocket = T-up left triangle
pu, pz = only((4, 2), [Tup_left_tri])
cases.append(dict(name='26.7 corridor, L upper triangle, B=(3,1), midpoint C',
    U=BASE_U | L_up_tri_U | pu, Z=BASE_Z | L_up_tri_Z | pz | fan((6, 2)),
    pocket={(4, 2), (4, 1), (3, 1)}, u=P(1, 0),
    first=[P(0, 0), P(4, 1)],
    second=[P(4, 1), P(F(16, 3), F(2, 3)), P(F(11, 2), 0), P(F(28, 5), F(2, 5)), P(4, 0)],
    flank=(1, 0), corner_angle=270, w=P(4, 1), Q_claim=P(-2, 0), det_claim=2))
# lower portal: B=(3,1) forced, N left forced; L size unknown
cases.append(dict(name='26.7 corridor, L lower portal, midpoint B=(3,1)',
    U=BASE_U | {tri((6, 0), (5, 0), (5, -1))} | pu, Z=BASE_Z | L_low_any_Z | pz | N_left_Z | fan((6, 2)),
    pocket={(4, 2), (4, 1), (3, 1)}, u=P(1, 0),
    first=[P(0, 0), P(3, 1)], second=[P(3, 1), P(5, F(1, 3)), P(4, 0)],
    flank=(-1, 0), corner_angle=225, w=P(3, 1), Q_claim=P(-2, 0), det_claim=2))

results = []
for c in cases:
    results.append(run_case(c))

# ---------- local incidence facts used by the case split ----------
def angle_at(p, tiles):
    return sum(90 if lab(p) == 'C' else 45 for t in incident(p) if t in tiles)
leaf_opts = lambda a, port_tri, sq_tri: {'m1': {port_tri}, 'm2': {port_tri, sq_tri}}
local = {}
# B=(5,-1): T full + pocket + each L option
Lopts = {'upper m1': {tri((6, 0), (5, 0), (5, 1))},
         'upper m2': {tri((6, 0), (5, 0), (5, 1)), tri((6, 0), (6, 1), (5, 1))},
         'lower m1': {tri((6, 0), (5, 0), (5, -1))},
         'lower m2': {tri((6, 0), (5, 0), (5, -1)), tri((6, 0), (6, -1), (5, -1))}}
local['B=(5,-1) angle by L option'] = {k: angle_at((5, -1), FULL | M_UP | {POCK_OPP} | v) for k, v in Lopts.items()}
# Alternative orientation B=(3,-1): pocket left triangle, M upper only
local['B=(3,-1) angle, left-pointing opposite pocket'] = angle_at((3, -1), FULL | M_UP | {tri((4, -2), (4, -1), (3, -1))})
Nopts = {'left m1': {N_left_tri}, 'left m2': {N_left_tri, N_left_sq2},
         'right m1': {N_right_tri}, 'right m2': {N_right_tri, N_right_sq2}}
Topts = {'left m1': {Tup_left_tri}, 'left m2': {Tup_left_tri, Tup_left_sq2},
         'right m1': {Tup_right_tri}, 'right m2': {Tup_right_tri, Tup_right_sq2}}
local['(3,1) angle, N x T-up options'] = {f'N {a} / Tup {b}': angle_at((3, 1), FULL | M_UP | Nv | Tv)
                                          for a, Nv in Nopts.items() for b, Tv in Topts.items()}
assert local['B=(5,-1) angle by L option'] == {'upper m1': 135, 'upper m2': 135, 'lower m1': 180, 'lower m2': 225}
assert local['B=(3,-1) angle, left-pointing opposite pocket'] == 135
for k, v in local['(3,1) angle, N x T-up options'].items():
    if k.startswith('N left') and 'Tup right' in k: assert v == 180   # smooth: forbidden by rawness
print(json.dumps(dict(cases=results, local_incidence=local), indent=2))

# ---------- negative controls: each must be REJECTED ----------
import copy
def expect_fail(label, case):
    try:
        run_case(case)
    except AssertionError as e:
        import traceback
        line = traceback.extract_tb(e.__traceback__)[-1].line
        return dict(control=label, rejected=True, reason=(str(e) or line)[:110])
    raise SystemExit('NEGATIVE CONTROL WRONGLY PASSED: ' + label)
neg = []
c = copy.copy(cases[0]); c['Z'] = OPP_Z | N_left_Z | {N_right_tri}; c['U'] = OPP_U | {N_left_tri}
neg.append(expect_fail('26.8 path with N LEFT (first bounce lands in a portal)', c))
c = copy.copy(cases[1]); c['U'] = U12; c['Z'] = Z12
neg.append(expect_fail('26.11 path in the m=2 square case (D+ is not a wall)', c))
c = copy.copy(cases[1]); c['pocket'] = set()
neg.append(expect_fail('26.11 with pocket motion ignored (claimed Q must fail)', c))
c = copy.copy(cases[1]); c['second'] = c['second'][:-1] + [P(4, 1)]
neg.append(expect_fail('26.11 with endpoint replaced by C=(4,1), not actual T', c))
c = copy.copy(cases[3]); c['flank'] = (1, 0)
neg.append(expect_fail('26.7 upper rectangle using the pocket side as flank', c))
# Withdrawn 26.8 end-leaf attempt: first reflection at (5/2,1) with N right forced.
endU = BASE_U | {N_right_tri}
endZ = BASE_Z | N_right_Z
c = dict(name='withdrawn end leaf', U=endU, Z=endZ, pocket={(6, 0), (5, 0), (5, 1)}, u=P(0, 1),
         first=[P(0, 0), P(F(5, 2), 1), P(5, 0)], second=[P(5, 0), P(3, F(-4, 5)), P(F(7, 2), -1), P(5, F(-2, 5)), P(4, 0)],
         flank=(0, -1), corner_angle=270, w=P(5, 2), Q_claim=P(0, 2), det_claim=10)
neg.append(expect_fail('withdrawn 26.8 end-leaf path under forced N right', c))

# ---------- moving-term ablation for 26.11 (hand formula (2) terms) ----------
L2 = ((F(-1), F(0)), (F(0), F(-1)))           # H1*V6 linear part
L3 = matmul(L2, linpart((1, 0)))               # after the moving vertical
aV, aD = (F(2), F(0)), (F(1), F(-1))
corner_term = mul(-2, matvec(L2, (F(1), F(0))))
terms = dict(vertical=matvec(L2, aV), diagonal=matvec(L3, aD), corner=corner_term)
ablation = {
    'all terms': add(add(terms['vertical'], terms['diagonal']), corner_term),
    'drop moving vertical': add(terms['diagonal'], corner_term),
    'drop moving diagonal': add(terms['vertical'], corner_term),
    'corner only (fixed-mirror shortcut)': corner_term}
assert ablation['all terms'] == (1, 1) and ablation['drop moving diagonal'] == (0, 0)

# ---------- prescribed fixtures: independent wall/raw/simple count ----------
def leaf(a, *tris): return {tri(*t) for t in tris}
def fixture(tup_sq):
    R = set(fan((0, 0)) | fan((4, 0)) | M_UP)
    R |= leaf((2, 2), ((2, 2), (2, 1), (1, 1)))                                   # N left triangle
    R |= {tri((6, 0), (5, 0), (5, -1)), tri((6, 0), (6, -1), (5, -1))}             # right lower square
    R |= {POCK_OPP, Tup_left_tri} | ({Tup_left_sq2} if tup_sq else set())
    R |= {tri((-2, 0), (-1, 0), (-1, -1)), tri((0, 2), (0, 1), (-1, 1)), tri((0, -2), (0, -1), (1, -1))}
    return R
def audit(R):
    from collections import Counter, defaultdict
    ec = Counter()
    for t in R:
        v = sorted(t)
        for i in range(3):
            for j in range(i + 1, 3): ec[(v[i], v[j])] += 1
    bnd = [e for e, k in ec.items() if k == 1]
    deg = defaultdict(int)
    for a, b in bnd: deg[a] += 1; deg[b] += 1
    assert all(d == 2 for d in deg.values()), 'boundary pinch'
    adj = defaultdict(list)
    for a, b in bnd: adj[a].append(b); adj[b].append(a)
    start = bnd[0][0]; seen = {start}; cur = start; prev = None
    while True:
        nx = [q for q in adj[cur] if q != prev]
        nxt = nx[0] if prev is not None else adj[cur][0]
        if nxt == start: break
        assert nxt not in seen; seen.add(nxt); prev, cur = cur, nxt
    assert len(seen) == len(deg), 'boundary is not one cycle'
    angle = defaultdict(int)
    for t in R:
        for p in t:
            angle[p] += 90 if lab(p) == 'C' else 45
    verts = {p for t in R for p in t}
    interior = sorted(p for p in verts if p not in deg)
    corners = [p for p in deg if angle[p] != 180]
    smooth_nonA = [p for p in deg if angle[p] == 180 and lab(p) != 'A']
    interior_nonA = [p for p in interior if lab(p) != 'A']
    return dict(tiles=len(R), walls=len(corners), interior=interior, smooth_nonA=smooth_nonA,
                interior_nonA=interior_nonA, B=angle[(5, -1)], C=angle[(4, -1)], A=angle[(4, -2)],
                at_3_1=angle[(3, 1)])
fx = {'26.11 W25 fixture': audit(fixture(False)), '26.12 W26 fixture': audit(fixture(True))}
assert fx['26.11 W25 fixture']['walls'] == 25 and fx['26.12 W26 fixture']['walls'] == 26
for v in fx.values():
    assert v['interior'] == [(0, 0), (4, 0)] and not v['smooth_nonA'] and not v['interior_nonA']
    assert (v['A'], v['B'], v['C']) == (45, 225, 270)
print(json.dumps(dict(negative_controls=neg,
                      ablation_26_11={k: [str(x) for x in v] for k, v in ablation.items()},
                      fixtures=fx), indent=2, default=str))
