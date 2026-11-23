"""d138 referee checks for rigidity-area.2026-11-21-2330.md.

Exact integer / Fraction arithmetic. Named rooms only; no search over rooms,
rays, directions or reflection words.  Run: python3 -B checks.py > checks.log
"""
import re
import resource
import time
from fractions import Fraction as F
from math import gcd
from pathlib import Path

resource.setrlimit(resource.RLIMIT_CPU, (300, 300))
T0 = time.process_time()
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def out(*a):
    print(*a, flush=True)


# ---------------------------------------------------------------- geometry
def area2(P):
    return sum(P[i][0] * P[(i + 1) % len(P)][1] - P[(i + 1) % len(P)][0] * P[i][1]
               for i in range(len(P)))


def edges(P):
    return [(P[(i + 1) % len(P)][0] - P[i][0], P[(i + 1) % len(P)][1] - P[i][1])
            for i in range(len(P))]


def seg_inter(a, b, c, d):
    """True if closed segments ab, cd intersect."""
    def orient(p, q, r):
        v = (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
        return (v > 0) - (v < 0)

    def onseg(p, q, r):
        return min(p[0], q[0]) <= r[0] <= max(p[0], q[0]) and min(p[1], q[1]) <= r[1] <= max(p[1], q[1])
    o1, o2, o3, o4 = orient(a, b, c), orient(a, b, d), orient(c, d, a), orient(c, d, b)
    if o1 != o2 and o3 != o4:
        return True
    return ((o1 == 0 and onseg(a, b, c)) or (o2 == 0 and onseg(a, b, d)) or
            (o3 == 0 and onseg(c, d, a)) or (o4 == 0 and onseg(c, d, b)))


def strictly_simple(P):
    n = len(P)
    if len(set(P)) != n:
        return False
    for i in range(n):
        for j in range(i + 1, n):
            if j == i + 1 or (i == 0 and j == n - 1):
                continue
            if seg_inter(P[i], P[(i + 1) % n], P[j], P[(j + 1) % n]):
                return False
    # no collinear consecutive edges (each vertex a genuine corner)
    E = edges(P)
    return all(E[i][0] * E[i - 1][1] - E[i][1] * E[i - 1][0] != 0 for i in range(n))


def inside(P, x, y):
    """Strict interior test by ray casting; (x,y) assumed generic."""
    c = False
    n = len(P)
    for i in range(n):
        (x1, y1), (x2, y2) = P[i], P[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            xi = x1 + F(y - y1) * (x2 - x1) / (y2 - y1)
            if xi > x:
                c = not c
    return c


def mat_mul(A, B):
    return ((A[0][0] * B[0][0] + A[0][1] * B[1][0], A[0][0] * B[0][1] + A[0][1] * B[1][1]),
            (A[1][0] * B[0][0] + A[1][1] * B[1][0], A[1][0] * B[0][1] + A[1][1] * B[1][1]))


def mv(A, v):
    return (A[0][0] * v[0] + A[0][1] * v[1], A[1][0] * v[0] + A[1][1] * v[1])


I2 = ((1, 0), (0, 1))
D4 = [((1, 0), (0, 1)), ((-1, 0), (0, -1)), ((1, 0), (0, -1)), ((-1, 0), (0, 1)),
      ((0, 1), (1, 0)), ((0, -1), (-1, 0)), ((0, -1), (1, 0)), ((0, 1), (-1, 0))]


def refl(e):
    dx, dy = e
    if dy == 0:
        return ((1, 0), (0, -1))
    if dx == 0:
        return ((-1, 0), (0, 1))
    if dx == dy:
        return ((0, 1), (1, 0))
    if dx == -dy:
        return ((0, -1), (-1, 0))
    raise ValueError(e)


# ------------------------------------------------------- 2D integer lattices
def hnf(gens):
    """Upper-triangular basis ((a,b),(0,c)) of the Z-span of integer 2-vectors."""
    # column-style: reduce first coordinates by gcd
    rows = [tuple(g) for g in gens if g != (0, 0)]
    a_row = None
    rest = []
    for r in rows:
        if a_row is None:
            if r[0] != 0:
                a_row = r
            else:
                rest.append(r)
            continue
        x, y = a_row, r
        while y[0] != 0:
            q = x[0] // y[0]
            x, y = y, (x[0] - q * y[0], x[1] - q * y[1])
        a_row = x
        rest.append(y)
    c = 0
    for r in rest:
        assert r[0] == 0
        c = gcd(c, r[1])
    if a_row is None:
        return None
    a, b = a_row
    if a < 0:
        a, b = -a, -b
    if c:
        b %= c
    return ((a, b), (0, c))


def covol(B):
    return abs(B[0][0] * B[1][1])


def in_lat(B, z):
    (a, b), (_, c) = B
    if z[0] % a:
        return False
    k = z[0] // a
    r = z[1] - k * b
    return r % c == 0 if c else r == 0


# ------------------------------------------------------------ unfolding
def unfold(P):
    """Glue copy g to copy g*rho_e along wall e.  Return placements t_g, holonomies."""
    P = [tuple(v) for v in P]
    E = edges(P)
    t = {I2: (0, 0)}
    queue = [I2]
    hol = []
    while queue:
        g = queue.pop()
        for i, e in enumerate(E):
            r = refl(e)
            p = P[i]
            rp = mv(r, p)
            shift = mv(g, (p[0] - rp[0], p[1] - rp[1]))
            g2 = mat_mul(g, r)
            t2 = (shift[0] + t[g][0], shift[1] + t[g][1])
            if g2 not in t:
                t[g2] = t2
                queue.append(g2)
            elif t[g2] != t2:
                hol.append((t2[0] - t[g2][0], t2[1] - t[g2][1]))
    return t, hol


def place(g, tg, P):
    return [(mv(g, v)[0] + tg[0], mv(g, v)[1] + tg[1]) for v in P]


def room_report(name, P, y=(F(13, 97), F(29, 101))):
    P = [tuple(v) for v in P]
    A = F(area2(P), 2)
    assert A > 0, 'orient CCW'
    ss = strictly_simple(P)
    t, hol = unfold(P)
    ncop = len(t)
    base = P[0]
    gens = []
    for g, tg in t.items():
        for v in place(g, tg, P):
            gens.append((v[0] - base[0], v[1] - base[1]))
    gens += hol
    Lg = hnf(gens)                                   # corner-period lattice from gluing
    grp = [g for g in D4 if g in t] if ncop == 4 else D4
    Le = hnf([mv(g, e) for g in grp for e in edges(P)])   # images of edges under room group
    Ld4 = hnf([mv(g, e) for g in D4 for e in edges(P)])   # images under all of D4
    content = 0
    for v in P:
        content = gcd(content, gcd(v[0] - base[0], v[1] - base[1]))
    gx = gy = 0
    for e in edges(P):
        gx, gy = gcd(gx, e[0]), gcd(gy, e[1])
    c = covol(Lg)
    ent = gcd(gcd(Lg[0][0], Lg[0][1]), Lg[1][1])
    inv = all(in_lat(Lg, mv(g, b)) for g in grp for b in (Lg[0], Lg[1]))
    d4inv = all(in_lat(Lg, mv(g, b)) for g in D4 for b in (Lg[0], Lg[1]))
    # holonomies and corner images lie in Lambda; corners map to one point mod Lambda
    # direct degree: preimages of a generic point of R^2/Lambda
    deg = 0
    for g, tg in t.items():
        Q = place(g, tg, P)
        xs = [q[0] for q in Q]
        ys = [q[1] for q in Q]
        for zx in range(min(xs) - 1, max(xs) + 1):
            for zy in range(min(ys) - 1, max(ys) + 1):
                if in_lat(Lg, (zx, zy)) and inside(Q, zx + y[0], zy + y[1]):
                    deg += 1
    # second generic point to confirm constancy
    y2 = (F(71, 89), F(5, 83))
    deg2 = 0
    for g, tg in t.items():
        Q = place(g, tg, P)
        xs = [q[0] for q in Q]
        ys = [q[1] for q in Q]
        for zx in range(min(xs) - 1, max(xs) + 1):
            for zy in range(min(ys) - 1, max(ys) + 1):
                if in_lat(Lg, (zx, zy)) and inside(Q, zx + y2[0], zy + y2[1]):
                    deg2 += 1
    out('==', name)
    out('   vertices', P)
    out('   W', len(P), 'area', A, 'strictly simple', ss, 'copies in connected unfolding', ncop)
    out('   scalar content', content, ' axis contents (gx,gy)', (gx, gy))
    out('   Lambda from gluing (HNF)', Lg, 'covolume c =', c, ' gcd of entries', ent)
    out('   Lambda == span of room-group edge images:', Lg == Le,
        '| == span of all-D4 edge images:', Lg == Ld4, ' (D4-span HNF', Ld4, ')')
    out('   holonomies found', len(hol), 'all in Lambda', all(in_lat(Lg, h) for h in hol))
    out('   Lambda invariant under room group', inv, '| under all of D4', d4inv,
        '| 2Z^2 in Lambda', in_lat(Lg, (2, 0)) and in_lat(Lg, (0, 2)))
    out('   direct degree at two generic points', deg, deg2)
    out('   copies*area/c =', ncop * A / c, '  c*d/copies =', F(c * deg, ncop),
        '  c*d/8 =', F(c * deg, 8), '  identity area == c*d/%d:' % ncop, A == F(c * deg, ncop))
    return dict(A=A, c=c, d=deg, ncop=ncop, L=Lg)


# =================================================================== 1. census scope
out('# 1. Census scope (READMEs read as text; no census rerun)')
r9 = (ROOT / 'd9-census-w22' / 'README.md').read_text()
r11 = (ROOT / 'd11-census-45' / 'README.md').read_text()
for pat in [r'area at most 20 and at most 22 walls', r'Not covered:\*\* rooms with area 21']:
    out('  d9 README contains %-45r' % pat, bool(re.search(pat, r9)))
for pat in [r'every strictly simple room with `N ≤ 32` tiles, `W ≤ 24` and an A/B pair',
            r'every strictly simple room with `N ≤ 24` and a C pair',
            r'C pairs inside the A/B-census rooms \(`N ≤ 32`, `W ≤ 24`\)',
            r'Diagonal walls never\s+pass through C points',
            r'`x \+ y ∈ 2Z` and `x − y ∈ 2Z`']:
    out('  d11 README contains %-60r' % pat[:60], bool(re.search(pat, r11)))
# tile area: canonical45 tiles are half unit squares
tri = [(0, 0), (1, 0), (1, 1)]
out('  canonical45 tile area', F(area2(tri), 2), '=> area 20 <-> N = 40 tiles')
out('  gaps at area <= 20: A/B N=33..40; C N=25..32 outside rooms with an A/B pair; C N=33..40')
# a named integer-vertex mixed room no G-image of which is canonical45
Pmix = [(0, 0), (3, 0), (4, 1), (4, 2), (2, 4), (0, 4)]
out('  named room M (square side 4, chamfers on x-y=3 and x+y=6):', Pmix,
    'strictly simple', strictly_simple(Pmix), 'area', F(area2(Pmix), 2))
# canonical45 needs every diagonal wall on x+y even (slope -1 walls) and x-y even (slope 1);
# G = D4 and translations (a,b), a+b even.  Translations shift x+y and x-y by a+b, a-b (same
# parity) -- so parities of the two intercepts change together.  D4 maps {x+y, x-y} to
# {+-(x+y), +-(x-y)}, preserving the pair of parities as a set.
ints = set()
E = edges(Pmix)
for i, e in enumerate(E):
    p = Pmix[i]
    if e[0] == e[1]:
        ints.add(('x-y', (p[0] - p[1]) % 2))
    elif e[0] == -e[1]:
        ints.add(('x+y', (p[0] + p[1]) % 2))
out('  diagonal intercept parities of M', sorted(ints),
    '-> mixed parities, so no G-image (nor its (1,0) translate) lies in canonical45')
for s in [(1, 0), (0, 1), (1, 1)]:
    Q = [(x + s[0], y + s[1]) for x, y in Pmix]
    par = sorted({('x-y' if E[i][0] == E[i][1] else 'x+y',
                   ((Q[i][0] - Q[i][1]) if E[i][0] == E[i][1] else (Q[i][0] + Q[i][1])) % 2)
                  for i in range(len(E)) if abs(E[i][0]) == abs(E[i][1])})
    out('    translate by', s, 'parities', par)
out('  scaling M by 2 to fit canonical45 gives area', 4 * F(area2(Pmix), 2), '> 20')

# =================================================================== 2. progression
out()
out('# 2. Primitive progression e + 2 J t v (arithmetic and geometry; darkness not tested)')
# Named linear family: chamfered square, side s, chamfer leg l, marks S, T; 0 < l < s.
# Anchored vertex vector (walls) and marks are linear in (s, l, mark params).


def cham(s, l):
    return [(0, 0), (s, 0), (s, s - l), (s - l, s), (0, s)]


def flat(P):
    return [c for v in P for c in v]


def content(vec):
    g = 0
    for x in vec:
        g = gcd(g, x)
    return g


e_room, e_marks = cham(18, 7), [(2, 2), (10, 4)]
v_room, v_marks = cham(6, 2), [(1, 1), (3, 1)]
Ew, Vw = flat(e_room), flat(v_room)
minors = [abs(Ew[i] * Vw[j] - Ew[j] * Vw[i]) for i in range(len(Ew)) for j in range(i + 1, len(Ew))]
J = min(m for m in minors if m)
out('  seed walls content', content(Ew), ' v walls content', content(Vw), ' J =', J)
bad_noJ = []
ok = True
for t in range(1, 1501):
    W = [a + 2 * J * t * b for a, b in zip(Ew, Vw)]
    if content(W) != 1:
        ok = False
    W0 = [a + 2 * t * b for a, b in zip(Ew, Vw)]
    if content(W0) != 1 and len(bad_noJ) < 6:
        bad_noJ.append((t, content(W0)))
out('  content 1 for t = 1..1500 with factor J:', ok)
out('  without J (e + 2 t v): first failures (t, content)', bad_noJ)
geo = True
for t in (1, 2, 5, 50, 500):
    k = 2 * J * t
    s, l = 18 + k * 6, 7 + k * 2
    R = cham(s, l)
    M = [(a[0] + k * b[0], a[1] + k * b[1]) for a, b in zip(e_marks, v_marks)]
    par = all((M[i][0] - e_marks[i][0]) % 2 == 0 and (M[i][1] - e_marks[i][1]) % 2 == 0 for i in range(2))
    # strict interior for lattice marks: check inequalities 0<x<s, 0<y<s, x+y<2s-l
    strict = all(0 < m[0] < s and 0 < m[1] < s and m[0] + m[1] < 2 * s - l for m in M)
    resc = [(F(x, k), F(y, k)) for x, y in R]
    dist = max(max(abs(a[0] - b[0]), abs(a[1] - b[1])) for a, b in zip(resc, v_room))
    out('   t=%-4d k=2Jt=%-5d side %-6d leg %-5d area %-12s content %d marks interior %s parity kept %s'
        ' rescaled-vs-v max deviation %s' % (t, k, s, l, F(area2(R), 2), content(flat(R)), strict, par,
                                             float(dist)))
    geo &= strictly_simple(R) and strict and par
out('  all members strictly simple with interior marks and kept parities:', geo)
out('  limit v =', v_room, 'strictly simple', strictly_simple(v_room),
    ' min gap / diameter', F(min(2, 6 - 2), 6))
# orthogonal caveat: scalar content 1 does not give axis contents 1 along a progression
Lx = [(0, 0), (6, 0), (6, 1), (3, 1), (3, 2), (0, 2)]
out('  orthogonal caveat: L-room', Lx, 'scalar content', content(flat(Lx)),
    'but x-content', content([v[0] for v in Lx]), '(axis normalization differs)')

# =================================================================== 3. area = c d / copies
out()
out('# 3. Corner-period lattice and covering degree on named rooms')
results = {}
results['L'] = room_report('L-tromino (orthogonal)', [(0, 0), (2, 0), (2, 1), (1, 1), (1, 2), (0, 2)])
results['L3'] = room_report('L with x-content 3 (orthogonal, scalar content 1)', Lx)
cross = [(1, 0), (3, 0), (3, 1), (4, 1), (4, 3), (3, 3), (3, 4), (1, 4), (1, 3), (0, 3), (0, 1), (1, 1)]
results['cross'] = room_report('12-wall cross (orthogonal)', cross)
for U, L in ((4, 1), (4, 2), (5, 1)):
    db = [(0, 0), (U, 0), (U, 2), (U + L, 2), (U + L, 0), (2 * U + L + 1, 0), (2 * U + L + 1, 5),
          (U + L, 5), (U + L, 3), (U, 3), (U, 5), (0, 5)]
    results['db%d%d' % (U, L)] = room_report('r=4 dumbbell U=%d, U+1, L=%d, height 5, door 2<y<3' % (U, L), db)
for q in (3, 6):
    P = cham(6 * q, 2 * q + 1)
    r = room_report('d135 chamfered square, side 6q, leg 2q+1, q=%d (mixed)' % q, P)
    out('   note formula d = 288q^2 - 4(2q+1)^2 =', 288 * q * q - 4 * (2 * q + 1) ** 2,
        ' area 36q^2-(2q+1)^2/2 =', 36 * q * q - F((2 * q + 1) ** 2, 2),
        ' match', r['d'] == 288 * q * q - 4 * (2 * q + 1) ** 2 and r['c'] == 1)
results['A'] = room_report('d135 room A, square with one chamfer (mixed)', [(0, 0), (2, 0), (2, 1), (1, 2), (0, 2)])
hexr = [(0, 0), (2, 0), (3, 1), (2, 2), (0, 2), (-1, 1)]
results['hex'] = room_report('hexagon, all edges a = b mod 2 (mixed, c=2 control)', hexr)
# sqrt2-similarity: (x,y) -> ((x+y)/2, (y-x)/2) maps the c=2 lattice onto Z^2
img = [((x + y) // 2, (y - x) // 2) for x, y in hexr]
assert all((x + y) % 2 == 0 for x, y in hexr)
results['hex_img'] = room_report('image of hexagon under 45-degree rotation by 1/sqrt2', img)
# gcd(6q, 4q-1) for small q
out('  gcd(6q,4q-1) for q=1..9:', [(q, gcd(6 * q, 4 * q - 1)) for q in range(1, 10)])

out()
out('CPU seconds', round(time.process_time() - T0, 3))
