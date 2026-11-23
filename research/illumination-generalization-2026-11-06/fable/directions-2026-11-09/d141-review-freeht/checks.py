"""d141 checks for free-half-turns.md (snapshot 2026-11-22 00:45).

Exact integer/Fraction arithmetic on named rooms only. No room search, no ray
search. Coordinates are scaled by 4 so that tile vertices, edge midpoints and
the quarter-square tiling are integral.

For each room the unfolding X is built combinatorially: tiles (T, g) with T a
quarter-square triangle of the room and g a sheet in the wall group G (or D4).
Across an interior edge the sheet is kept; across a wall w the sheet becomes
g*s_w. An affine automorphism with derivative A is a tile permutation
(T,g) -> (f(T), g*) with physical affine part f, linear part g*^-1 A g, that
commutes with every edge gluing. All of them are found exactly: seed one base
tile at each of the |X| possible images and propagate (a permutation
conjugacy). This finds every automorphism that preserves the tiling, which is
every automorphism once X has a cone point (cone points are lattice points and
the derivative is in D4).

Run: python3 -B checks.py > checks.log
"""
from fractions import Fraction as Fr
from itertools import combinations
from collections import deque

S4 = 4  # coordinate scale

# ------------------------------------------------------------------ linear algebra
I2 = ((1, 0), (0, 1))
NEG = ((-1, 0), (0, -1))
D4 = [((1, 0), (0, 1)), ((0, -1), (1, 0)), ((-1, 0), (0, -1)), ((0, 1), (-1, 0)),
      ((1, 0), (0, -1)), ((-1, 0), (0, 1)), ((0, 1), (1, 0)), ((0, -1), (-1, 0))]
NAME = {D4[0]: "I", D4[1]: "R", D4[2]: "-I", D4[3]: "R^3", D4[4]: "diag(1,-1)",
        D4[5]: "diag(-1,1)", D4[6]: "swap", D4[7]: "-swap"}


def mm(A, B):
    return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)) for i in range(2))


def mv(A, v):
    return (A[0][0] * v[0] + A[0][1] * v[1], A[1][0] * v[0] + A[1][1] * v[1])


def inv(A):  # orthogonal
    return ((A[0][0], A[1][0]), (A[0][1], A[1][1]))


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def gen_group(gens):
    G = {I2}
    frontier = [I2]
    while frontier:
        new = []
        for g in frontier:
            for s in gens:
                h = mm(g, s)
                if h not in G:
                    G.add(h)
                    new.append(h)
        frontier = new
    return G


def refl_of_dir(d):
    """Linear reflection fixing direction d (axial or diagonal)."""
    if d[1] == 0:
        return ((1, 0), (0, -1))
    if d[0] == 0:
        return ((-1, 0), (0, 1))
    if d[0] * d[1] > 0:
        return ((0, 1), (1, 0))
    return ((0, -1), (-1, 0))


# affine maps (M, c): x -> Mx + c
def ap(f, x):
    return add(mv(f[0], x), f[1])


def comp(f, g):  # f o g
    return (mm(f[0], g[0]), add(mv(f[0], g[1]), f[1]))


def aff_refl(a, b):
    s = refl_of_dir(sub(b, a))
    return (s, sub(a, mv(s, a)))


# ------------------------------------------------------------------ polygons
def area2(P):
    return sum(cross(P[i], P[(i + 1) % len(P)]) for i in range(len(P)))


def edges(P):
    return [(P[i], P[(i + 1) % len(P)]) for i in range(len(P))]


def on_seg(p, a, b):
    return cross(sub(b, a), sub(p, a)) == 0 and min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) \
        and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])


def seg_inter(p1, p2, q1, q2):
    def o(a, b, c):
        v = cross(sub(b, a), sub(c, a))
        return (v > 0) - (v < 0)
    o1, o2, o3, o4 = o(p1, p2, q1), o(p1, p2, q2), o(q1, q2, p1), o(q1, q2, p2)
    if o1 != o2 and o3 != o4:
        return True
    return (o1 == 0 and on_seg(q1, p1, p2)) or (o2 == 0 and on_seg(q2, p1, p2)) or \
        (o3 == 0 and on_seg(p1, q1, q2)) or (o4 == 0 and on_seg(p2, q1, q2))


def strictly_simple(P):
    E = edges(P)
    n = len(E)
    for i in range(n):
        a, b = E[i]
        c = E[(i + 1) % n][1]
        if cross(sub(b, a), sub(c, b)) == 0:
            return False
    for i, j in combinations(range(n), 2):
        if j == i + 1 or (i == 0 and j == n - 1):
            continue
        if seg_inter(*E[i], *E[j]):
            return False
    return True


def inside(P, p):
    """True strict interior, False exterior, None boundary. p may be Fractions."""
    for a, b in edges(P):
        if on_seg(p, a, b):
            return None
    c = False
    for a, b in edges(P):
        if (a[1] > p[1]) != (b[1] > p[1]):
            x = a[0] + Fr(p[1] - a[1]) * (b[0] - a[0]) / (b[1] - a[1])
            if x > p[0]:
                c = not c
    return c


DIRS = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]


def prim(v):
    from math import gcd
    g = gcd(abs(v[0]), abs(v[1]))
    return (v[0] // g, v[1] // g)


def angle_units(P):
    out = []
    n = len(P)
    for i in range(n):
        a, b, c = P[i - 1], P[i], P[(i + 1) % n]
        t = (DIRS.index(prim(sub(c, b))) - DIRS.index(prim(sub(b, a)))) % 8
        if t > 4:
            t -= 8
        out.append(4 - t)
    return out


# ------------------------------------------------------------------ unfolding
class Room:
    def __init__(self, name, verts, full_d4=False):
        self.name = name
        P = verts if area2(verts) > 0 else verts[::-1]
        self.P0 = P
        self.P = [(S4 * x, S4 * y) for x, y in P]
        assert strictly_simple(self.P), name
        self.angles = angle_units(P)
        xs = [v[0] for v in P]
        ys = [v[1] for v in P]
        tiles = []
        for i in range(min(xs), max(xs)):
            for j in range(min(ys), max(ys)):
                a, b, c, d = (4 * i, 4 * j), (4 * i + 4, 4 * j), (4 * i + 4, 4 * j + 4), (4 * i, 4 * j + 4)
                m = (4 * i + 2, 4 * j + 2)
                for u, v in ((a, b), (b, c), (c, d), (d, a)):
                    T = frozenset((u, v, m))
                    cen = (Fr(u[0] + v[0] + m[0], 3), Fr(u[1] + v[1] + m[1], 3))
                    if inside(self.P, cen):
                        tiles.append(T)
        self.tiles = tiles
        self.tileset = set(tiles)
        self.wall_lin = {}
        gens = set()
        for a, b in edges(self.P):
            gens.add(refl_of_dir(prim(sub(b, a))))
        self.Gwall = gen_group(gens)
        self.G = set(D4) if full_d4 else self.Gwall
        self.sheets = sorted(self.G)
        # tile adjacency
        self.nb = {}
        for T in tiles:
            for e in combinations(sorted(T), 2):
                e = frozenset(e)
                a, b = sorted(e)
                third = next(iter(T - e))
                r = aff_refl(a, b)
                T2 = frozenset((a, b, ap(r, third)))
                if T2 in self.tileset:
                    self.nb[(T, e)] = ("int", T2, None)
                else:
                    self.nb[(T, e)] = ("wall", T, r)
        self.X = [(T, g) for T in tiles for g in self.sheets]
        self.corners = set(self.P)

    # neighbour of X tile across physical edge e (same physical edge on both sides)
    def xnbr(self, x, e):
        T, g = x
        kind, T2, r = self.nb[(T, e)]
        if kind == "int":
            return (T2, g)
        return (T, mm(g, r[0]))

    def stab(self, p):
        gens = [refl_of_dir(prim(sub(b, a))) for a, b in edges(self.P) if on_seg(p, a, b)]
        return gen_group(gens)

    def xpoint(self, p, g):
        return (p, frozenset(mm(g, h) for h in self.stab(p)))

    def components(self):
        seen = {}
        k = 0
        for x in self.X:
            if x in seen:
                continue
            dq = deque([x])
            seen[x] = k
            while dq:
                y = dq.popleft()
                for e in combinations(sorted(y[0]), 2):
                    z = self.xnbr(y, frozenset(e))
                    if z not in seen:
                        seen[z] = k
                        dq.append(z)
            k += 1
        return k, seen

    def genus(self):
        V = set()
        E = set()
        for T in self.tiles:
            for v in T:
                for g in self.sheets:
                    V.add(self.xpoint(v, g))
            for e in combinations(sorted(T), 2):
                e = frozenset(e)
                a, b = sorted(e)
                mid = (Fr(a[0] + b[0], 2), Fr(a[1] + b[1], 2))
                st = self.stab(mid)
                for g in self.sheets:
                    E.add((e, frozenset(mm(g, h) for h in st)))
        F = len(self.X)
        ncomp, _ = self.components()
        chi = len(V) - len(E) + F
        return ncomp, chi

    def candidate_points(self):
        pts = set()
        for T in self.tiles:
            for v in T:
                pts.add(v)
            for a, b in combinations(sorted(T), 2):
                pts.add(((a[0] + b[0]) // 2, (a[1] + b[1]) // 2))
        return pts

    def containing_tile(self, p):
        for T in self.tiles:
            a, b, c = sorted(T)
            s1, s2, s3 = cross(sub(b, a), sub(p, a)), cross(sub(c, b), sub(p, b)), cross(sub(a, c), sub(p, c))
            if (s1 >= 0 and s2 >= 0 and s3 >= 0) or (s1 <= 0 and s2 <= 0 and s3 <= 0):
                return T
        raise ValueError(p)


def tile_affine(T0, T1, M):
    """Affine f with linear part M and f(T0) = T1, or None."""
    s0 = (sum(v[0] for v in T0), sum(v[1] for v in T0))
    s1 = (sum(v[0] for v in T1), sum(v[1] for v in T1))
    d = sub(s1, mv(M, s0))
    if d[0] % 3 or d[1] % 3:
        return None
    f = (M, (d[0] // 3, d[1] // 3))
    if frozenset(ap(f, v) for v in T0) != T1:
        return None
    return f


def propagate(room, A, x0, y0):
    """Try to extend x0 -> y0 to an automorphism with derivative A on x0's component."""
    T0, g0 = x0
    T1, g1 = y0
    M = mm(mm(inv(g1), A), g0)
    f = tile_affine(T0, T1, M)
    if f is None:
        return None
    phi = {x0: (y0, f)}
    dq = deque([x0])
    while dq:
        x = dq.popleft()
        y, f = phi[x]
        for e in combinations(sorted(x[0]), 2):
            e = frozenset(e)
            fe = frozenset(ap(f, v) for v in e)
            x2 = room.xnbr(x, e)
            y2 = room.xnbr(y, fe)
            M2 = mm(mm(inv(y2[1]), A), x2[1])
            f2 = tile_affine(x2[0], y2[0], M2)
            if f2 is None or frozenset(ap(f2, v) for v in e) != fe:
                return None
            if x2 in phi:
                if phi[x2] != (y2, f2):
                    return None
            else:
                phi[x2] = (y2, f2)
                dq.append(x2)
    return phi


def automorphisms(room, A):
    _, comp_of = room.components()
    x0 = room.X[0]
    found = []
    for y0 in room.X:
        phi = propagate(room, A, x0, y0)
        if phi is None:
            continue
        if len(phi) != len(room.X):
            continue  # only defined on a component (handled separately)
        if len({v[0] for v in phi.values()}) != len(room.X):
            continue
        found.append(phi)
    return found


def physical_part(phi):
    fs = {v[1] for v in phi.values()}
    return fs.pop() if len(fs) == 1 else None


def apply_point(room, phi, p, g):
    T = room.containing_tile(p)
    y, f = phi[(T, g)]
    q = ap(f, p)
    return room.xpoint(q, y[1])


def fixed_points(room, phi):
    out = []
    for p in room.candidate_points():
        cosets = {room.xpoint(p, g) for g in room.sheets}
        for xp in cosets:
            g = next(iter(xp[1]))
            if apply_point(room, phi, p, g) == xp:
                out.append(xp)
    return out


def is_involution(phi):
    return all(phi[phi[x][0]][0] == x for x in phi)


def physical_symmetries(room):
    E = {frozenset(e) for e in edges(room.P)}
    out = []
    for L in D4:
        img0 = mv(L, room.P[0])
        for v in room.P:
            c = sub(v, img0)
            if {frozenset(add(mv(L, w), c) for w in e) for e in E} == E:
                out.append((L, c))
    return out


def describe_sym(L, c):
    s = NAME[L]
    if L == I2:
        return "identity"
    if L == NEG:
        return "central symmetry about (%s,%s)" % (Fr(c[0], 2 * S4), Fr(c[1], 2 * S4))
    if L in (D4[1], D4[3]):
        return "quarter turn"
    # reflection: fixed line {x: Lx + c = x}
    if L == D4[4]:
        return "reflection y=%s" % Fr(c[1], 2 * S4)
    if L == D4[5]:
        return "reflection x=%s" % Fr(c[0], 2 * S4)
    if L == D4[6]:
        return "reflection y=x%+s" % Fr(c[1], S4) if c[1] else "reflection y=x"
    return "reflection x+y=%s" % Fr(c[0], S4)


def lift(room, sigma, A):
    """The lift (p,g) -> (sigma p, A g L^-1) as a tile map, or None if not a map into X."""
    L, c = sigma
    phi = {}
    for (T, g) in room.X:
        g2 = mm(mm(A, g), inv(L))
        T2 = frozenset(ap(sigma, v) for v in T)
        if g2 not in room.G or T2 not in room.tileset:
            return None
        phi[(T, g)] = ((T2, g2), sigma)
    return phi


def respects_gluing(room, phi):
    for x, (y, f) in phi.items():
        for e in combinations(sorted(x[0]), 2):
            e = frozenset(e)
            fe = frozenset(ap(f, v) for v in e)
            x2 = room.xnbr(x, e)
            if phi[x2][0] != room.xnbr(y, fe):
                return False
    return True


def fmt_pt(xp):
    p, cos = xp
    return "(%s,%s)[%d sheets]" % (Fr(p[0], S4), Fr(p[1], S4), len(cos))


def header(s):
    print("=" * 76)
    print(s)
    print("=" * 76)


# ------------------------------------------------------------------ rooms
ROOMS = [
    ("H  d138 hexagon", [(0, 0), (2, 0), (3, 1), (2, 2), (0, 2), (-1, 1)], False),
    ("D  square with two opposite chamfers", [(1, 0), (3, 0), (3, 2), (2, 3), (0, 3), (0, 1)], False),
    ("A  square with one chamfer (d135 room A)", [(0, 0), (2, 0), (2, 1), (1, 2), (0, 2)], False),
    ("B  V-notch (d135 room B)", [(0, 0), (4, 0), (4, 4), (2, 2), (0, 4)], False),
    ("O  octagon, all four corners chamfered", [(1, 0), (2, 0), (3, 1), (3, 2), (2, 3), (1, 3), (0, 2), (0, 1)], False),
    ("M  asymmetric hexagon (d139 room M)", [(0, 0), (3, 0), (4, 1), (4, 2), (2, 4), (0, 4)], False),
    ("L  orthogonal L, natural 4-copy unfolding", [(0, 0), (2, 0), (2, 1), (1, 1), (1, 2), (0, 2)], False),
    ("X  orthogonal 12-wall cross, natural 4-copy unfolding",
     [(1, 0), (2, 0), (2, 1), (3, 1), (3, 2), (2, 2), (2, 3), (1, 3), (1, 2), (0, 2), (0, 1), (1, 1)], False),
]


def axis_meets(room, L, c):
    """Boundary fixed points of a physical reflection, classified."""
    sig = (L, c)
    pts = []
    P = room.P
    # a fixed boundary point is a fixed vertex or the midpoint of an edge mapped to itself reversed
    for v in P:
        if ap(sig, v) == v:
            pts.append(("vertex", v))
    for a, b in edges(P):
        if {ap(sig, a), ap(sig, b)} == {a, b} and ap(sig, a) == b:
            m = ((a[0] + b[0]) // 2, (a[1] + b[1]) // 2)
            pts.append(("edge midpoint", m))
    return pts



# ------------------------------------------------------------------ section 5 helpers
def compose(a, b):
    """a o b as tile maps."""
    return {x: (a[b[x][0]][0], comp(a[b[x][0]][1], b[x][1])) for x in b}


def inverse(a):
    return {a[x][0]: (x, (inv(a[x][1][0]), mv(inv(a[x][1][0]), (-a[x][1][1][0], -a[x][1][1][1])))) for x in a}


def key(phi, room):
    return tuple(phi[x][0] for x in room.X)


def element_order(room, phi):
    ident = tuple(room.X)
    k, cur = 1, phi
    while key(cur, room) != ident:
        cur = compose(phi, cur)
        k += 1
    return k


def subgroups(room, elems):
    """All subgroups generated by at most 2 elements (enough for the groups met here, order <= 8)."""
    keys = {key(e, room): e for e in elems}
    ident = tuple(room.X)

    def gen(gs):
        H = {ident}
        frontier = [ident]
        while frontier:
            new = []
            for hk in frontier:
                h = keys[hk]
                for g in gs:
                    kk = key(compose(g, h), room)
                    if kk not in H:
                        H.add(kk)
                        new.append(kk)
            frontier = new
        return frozenset(H)
    subs = {gen([e1, e2]) for e1 in elems for e2 in elems}
    return [[keys[k] for k in H] for H in subs]


def quotient_mechanisms(room):
    """(Gamma, psi): Gamma a subgroup of Trans(X), psi a -I map normalising Gamma with psi^2 in Gamma,
    every element of the coset Gamma psi having only forbidden fixed points. Then [psi] is a half-turn of
    X/Gamma whose fixed points are all forbidden, and the midpoint argument on X/Gamma blocks every
    path in X from x to any point of Gamma psi(x)."""
    tr = automorphisms(room, I2)
    mi = automorphisms(room, NEG)
    only_forb = {key(p, room): all(q[0] in room.corners for q in fixed_points(room, p)) for p in mi}
    out = []
    for Gam in subgroups(room, tr):
        gk = {key(g, room) for g in Gam}
        for psi in mi:
            if key(compose(psi, psi), room) not in gk:
                continue
            pinv = inverse(psi)
            if not all(key(compose(psi, compose(g, pinv)), room) in gk for g in Gam):
                continue
            coset = [compose(g, psi) for g in Gam]
            if all(only_forb[key(c, room)] for c in coset):
                out.append((Gam, psi, coset))
    return tr, mi, out


def main():
    header("1. Rooms, unfoldings, and all affine automorphisms with derivative -I and I")
    summary = []
    for name, verts, full in ROOMS:
        room = Room(name, verts, full)
        ncomp, chi = room.genus()
        g = (2 * ncomp - chi) // 2
        print("\n[%s] vertices %s" % (name, verts))
        print("  strictly simple: True  angles (pi/4): %s  wall group order %d  sheets %d  tiles %d  X tiles %d"
              % (room.angles, len(room.Gwall), len(room.G), len(room.tiles), len(room.X)))
        print("  X components %d, chi %d, genus of each component %s" % (ncomp, chi, (2 - chi // ncomp) // 2))
        syms = physical_symmetries(room)
        print("  physical symmetries (%d): %s" % (len(syms), [describe_sym(*s) for s in syms]))
        for s in syms:
            L, c = s
            if L in (D4[4], D4[5], D4[6], D4[7]):
                print("    %s meets boundary at: %s" % (describe_sym(*s),
                      [(k, (Fr(p[0], S4), Fr(p[1], S4))) for k, p in axis_meets(room, L, c)]))
        res = {}
        for Aname, A in (("-I", NEG), ("I", I2)):
            auts = automorphisms(room, A)
            phys = [physical_part(phi) for phi in auts]
            hidden = sum(1 for f in phys if f is None)
            expected = sum(1 for s in syms if lift(room, s, A) is not None)
            print("  derivative %s: %d automorphisms found; physical lifts %d; hidden (not a lift of one isometry) %d;"
                  " predicted lifts (p,g)->(sigma p, A g L^-1) that land in X: %d"
                  % (Aname, len(auts), len(auts) - hidden, hidden, expected))
            res[Aname] = auts
            if Aname == "-I":
                for phi, f in zip(auts, phys):
                    fx = fixed_points(room, phi)
                    forb = [p for p in fx if p[0] in room.corners]
                    nonf = [p for p in fx if p[0] not in room.corners]
                    tag = describe_sym(*f) if f else "HIDDEN"
                    is_tau = f is not None and f[0] == I2
                    kind = "tau" if is_tau else ("FREE" if not fx else ("all fixed points forbidden" if not nonf else "has non-forbidden fixed points"))
                    print("    -I lift of %-34s involution=%s  fixed: %d forbidden, %d non-forbidden -> %s"
                          % (tag, is_involution(phi), len(forb), len(nonf), kind))
                    if nonf and len(nonf) <= 6:
                        print("        non-forbidden fixed points: %s" % [fmt_pt(p) for p in nonf])
                    if is_tau:
                        allc = {room.xpoint(v, gg) for v in room.corners for gg in room.sheets}
                        print("        tau fixes all %d corner lifts: %s; fixed set == corner lifts: %s"
                              % (len(allc), allc <= set(fx), set(fx) == allc))
                    summary.append((name, tag, kind))
        # RH check for Y = X / tau
        tau = [phi for phi in res["-I"] if physical_part(phi) and physical_part(phi)[0] == I2]
        if ncomp == 1 and tau:
            nfix = len(fixed_points(room, tau[0]))
            gx = (2 - chi) // 2
            gy2 = (2 * gx - 2 - nfix) // 2 + 2  # 2gx-2 = 2(2gy-2)+nfix
            gy = gy2 // 2
            print("  genus(X)=%d, #Fix(tau)=%d, genus(Y=X/tau)=%d  (odd: %s)" % (gx, nfix, gy, gy % 2 == 1))
        # corner lift counts vs formula
        if len(room.Gwall) == 8:
            ok = True
            for v, a in zip(room.P, room.angles):
                n_lifts = len({room.xpoint(v, gg) for gg in room.sheets})
                from math import gcd
                ok &= n_lifts == gcd(4, a)
            print("  corner lifts = gcd(4,a) at every corner: %s" % ok)

    header("2. Orthogonal rooms on the full 8-copy (two-component) unfolding")
    for name, verts, _ in ROOMS[6:]:
        room = Room(name, verts, True)
        ncomp, comp_of = room.components()
        print("\n[%s] with D4 sheets: components %d" % (name, ncomp))
        for s in physical_symmetries(room):
            if s[0] in (D4[6], D4[7]):
                phi = lift(room, s, NEG)
                ok = respects_gluing(room, phi)
                swaps = all(comp_of[x] != comp_of[phi[x][0]] for x in phi)
                fx = fixed_points(room, phi)
                print("  -I lift of %s: automorphism %s, swaps components %s, fixed points %d"
                      % (describe_sym(*s), ok, swaps, len(fx)))
                print("    (so S-lift and T-lift lie in different components; no path joins them)")
            if s[0] in (D4[4], D4[5]):
                phi = lift(room, s, NEG)
                print("  -I lift of %s lands in natural 4-copy unfolding: %s"
                      % (describe_sym(*s), lift(Room(name, verts, False), s, NEG) is not None))

    header("3. Claim (b): from one source lift, targets reached by -I involutions with only forbidden fixed points")
    room = Room(*ROOMS[0])
    S = (4, 2)   # (1, 1/2) scaled by 4
    T = (4, 6)   # (1, 3/2)
    auts = automorphisms(room, NEG)
    good = []
    for phi in auts:
        fx = fixed_points(room, phi)
        if all(p[0] in room.corners for p in fx) and is_involution(phi):
            good.append(phi)
    print("  H: -I involutions with all fixed points forbidden: %d (%s)"
          % (len(good), [describe_sym(*physical_part(phi)) for phi in good]))
    for g in room.sheets:
        src = room.xpoint(S, g)
        tgts = set()
        for phi in good:
            im = apply_point(room, phi, S, g)
            if im[0] == T:
                tgts.add(im)
        print("  source sheet %-10s -> blocked T-lifts %d: %s" % (NAME[g], len(tgts), [NAME[next(iter(t[1]))] for t in tgts]))
    # every -I automorphism, not only the free ones: which T-lifts it sends (S,I) to
    allimg = {}
    for phi in auts:
        im = apply_point(room, phi, S, I2)
        allimg[describe_sym(*physical_part(phi))] = (Fr(im[0][0], 4), Fr(im[0][1], 4), NAME[next(iter(im[1]))])
    print("  images of (S, I) under all -I automorphisms: %s" % allimg)

    header("4. Claim (c): the hexagon chord")
    P = room.P
    print("  S=(1,1/2) inside: %s; T=(1,3/2) inside: %s" % (inside(P, S), inside(P, T)))
    crosses = [e for e in edges(P) if seg_inter(S, T, *e)]
    print("  edges meeting the closed chord S-T: %s" % crosses)
    print("  corners on chord: %s" % [v for v in P if on_seg(v, S, T)])
    sig = [s for s in physical_symmetries(room) if s[0] == D4[4]][0]
    print("  reflection used: %s; sigma(S)==T: %s" % (describe_sym(*sig), ap(sig, S) == T))
    eta = [phi for phi in good if physical_part(phi)[0] == D4[4]][0]
    for g in room.sheets:
        im = apply_point(room, eta, S, g)
        chord_end = room.xpoint(T, g)
        assert im[0] == T
        if g == I2:
            print("  eta(S, I) = (T, %s); chord ends at (T, I); equal: %s"
                  % (NAME[next(iter(im[1]))], im == chord_end))
    print("  all 8 sheets: eta(S,g) != (T,g): %s" % all(apply_point(room, eta, S, g) != room.xpoint(T, g) for g in room.sheets))
    mid = (4, 4)
    print("  chord midpoint (1,1) on sheet I mapped to sheet %s (not fixed: %s)"
          % (NAME[next(iter(apply_point(room, eta, mid, I2)[1]))], apply_point(room, eta, mid, I2) != room.xpoint(mid, I2)))
    # better-placed marks: square centres mirrored by y=1
    S2, T2 = (2, 2), (2, 6)
    print("  square centres (1/2,1/2),(1/2,3/2): inside %s %s; chord meets edges %s"
          % (inside(P, S2), inside(P, T2), [e for e in edges(P) if seg_inter(S2, T2, *e)]))
    print("  doubled room 2H content: gcd of doubled coordinates = 2; doubled marks (2,1),(2,3) parity of x+y: %d %d"
          % ((2 + 1) % 2, (2 + 3) % 2))

    header("5. Intermediate translation covers X/Gamma: half-turns whose fixed points are all forbidden")
    for name, verts, full in ROOMS[:6]:
        room = Room(name, verts, full)
        Sx = (Fr(53, 10), Fr(27, 10))  # (1.325, 0.675) scaled by 4
        if not inside(room.P, Sx):
            Sx = (Sx[0] + 4, Sx[1] + 4)
        assert inside(room.P, Sx), name
        tr, mi, mechs = quotient_mechanisms(room)
        print("\n[%s] |Trans(X)| = %d, element orders %s; |-I maps| = %d"
              % (name, len(tr), sorted(element_order(room, t) for t in tr), len(mi)))
        print("  -I maps with all fixed points forbidden: %s"
              % [(describe_sym(*physical_part(p)) if physical_part(p) else "HIDDEN", "order %d" % element_order(room, p),
                  "%d fixed" % len(fixed_points(room, p)))
                 for p in mi if all(q[0] in room.corners for q in fixed_points(room, p))])
        tau = [p for p in mi if physical_part(p) and physical_part(p)[0] == I2][0]
        print("  tau commutes with every element of Trans(X): %s"
              % all(key(compose(tau, t), room) == key(compose(t, tau), room) for t in tr))
        print("  mechanisms (Gamma, psi): %d, |Gamma| in %s" % (len(mechs), sorted({len(m[0]) for m in mechs})))
        blocked = {}
        for Gam, psi, coset in mechs:
            for c in coset:
                im = apply_point(room, c, Sx, I2)
                if im[0] != Sx:
                    blocked.setdefault(im[0], set()).add((im, len(Gam), physical_part(c) is not None))
        imgs = {ap(s_, Sx) for s_ in physical_symmetries(room)}
        print("  source (S, I) with S = (%s, %s)" % (Fr(Sx[0], 4), Fr(Sx[1], 4)))
        for p, s_ in sorted(blocked.items()):
            lifts = {b[0] for b in s_}
            print("    target (%s, %s): %d blocked lift(s) of 8; |Gamma| in %s; blocking map physical: %s;"
                  " target = physical image of S: %s"
                  % (Fr(p[0], 4), Fr(p[1], 4), len(lifts), sorted({b[1] for b in s_}),
                     sorted({b[2] for b in s_}), p in imgs))
        if room.name.startswith("B"):
            hid = [t for t in tr if physical_part(t) is None]
            t = hid[0]
            fs = {}
            for (T, g), (y, f) in t.items():
                fs.setdefault(T, set()).add(f)
            print("  a hidden translation: physical parts per tile take %d distinct values; S goes to %s"
                  % (len({f for v in fs.values() for f in v}),
                     sorted({(Fr(apply_point(room, t, Sx, g)[0][0], 4), Fr(apply_point(room, t, Sx, g)[0][1], 4))
                             for g in room.sheets})))


if __name__ == "__main__":
    main()
