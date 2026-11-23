"""d139 checks for diagonal-periods.md (snapshot 2026-11-22 00:10).

Exact Fraction/integer arithmetic on named rooms only. No room, ray-direction
or reflection-word search. Run: python3 -B checks.py > checks.log
"""
from fractions import Fraction as Fr
from math import gcd, floor
from itertools import combinations

# ---------------------------------------------------------------- rooms
ROOMS = {
    # mixed-parity rooms
    "M": [(0, 0), (3, 0), (4, 1), (4, 2), (2, 4), (0, 4)],
    "R2 (two 225-degree corners)": [(1, 0), (4, 0), (4, 2), (2, 2), (1, 3), (1, 4), (0, 4), (0, 1)],
    "R3 (270-degree notch)": [(0, 0), (2, 0), (2, 1), (3, 1), (4, 2), (4, 4), (1, 4), (0, 3)],
    # canonical45 controls
    "C1 canonical c=1": [(0, 0), (3, 0), (3, 1), (2, 2), (0, 2)],
    "C2 canonical c=2 pentagon": [(0, 0), (2, 0), (2, 2), (1, 3), (0, 2)],
}
MIXED = ["M", "R2 (two 225-degree corners)", "R3 (270-degree notch)"]

D4 = [((1, 0), (0, 1)), ((0, -1), (1, 0)), ((-1, 0), (0, -1)), ((0, 1), (-1, 0)),
      ((1, 0), (0, -1)), ((-1, 0), (0, 1)), ((0, 1), (1, 0)), ((0, -1), (-1, 0))]


def F(p):
    return (p[0] - p[1], p[0] + p[1])


def mat_mul(A, B):
    return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)) for i in range(2))


def mat_vec(A, v):
    return (A[0][0] * v[0] + A[0][1] * v[1], A[1][0] * v[0] + A[1][1] * v[1])


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def area(P):
    return Fr(sum(cross(P[i], P[(i + 1) % len(P)]) for i in range(len(P))), 2)


def ccw(P):
    return P if area(P) > 0 else P[::-1]


def edges(P):
    return [(P[i], P[(i + 1) % len(P)]) for i in range(len(P))]


def prim(v):
    g = gcd(abs(v[0]), abs(v[1]))
    return (v[0] // g, v[1] // g)


def wall(a, b):
    """(type, intercept) of the line through edge a-b."""
    d = prim(sub(b, a))
    if d[1] == 0:
        return ("y", a[1])
    if d[0] == 0:
        return ("x", a[0])
    if d[0] * d[1] < 0:
        return ("x+y", a[0] + a[1])
    return ("x-y", a[0] - a[1])


def refl(e):
    """Linear reflection fixing direction e."""
    if e[1] == 0:
        return ((1, 0), (0, -1))
    if e[0] == 0:
        return ((-1, 0), (0, 1))
    if e[0] * e[1] > 0:
        return ((0, 1), (1, 0))
    return ((0, -1), (-1, 0))


def seg_inter(p1, p2, q1, q2):
    """True if closed segments intersect."""
    def o(a, b, c):
        v = cross(sub(b, a), sub(c, a))
        return (v > 0) - (v < 0)

    def on(a, b, c):
        return min(a[0], b[0]) <= c[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= c[1] <= max(a[1], b[1])
    o1, o2, o3, o4 = o(p1, p2, q1), o(p1, p2, q2), o(q1, q2, p1), o(q1, q2, p2)
    if o1 != o2 and o3 != o4:
        return True
    return (o1 == 0 and on(p1, p2, q1)) or (o2 == 0 and on(p1, p2, q2)) or \
           (o3 == 0 and on(q1, q2, p1)) or (o4 == 0 and on(q1, q2, p2))


def strictly_simple(P):
    E = edges(P)
    n = len(E)
    for i, j in combinations(range(n), 2):
        if j == i + 1 or (i == 0 and j == n - 1):
            a, b = E[i] if j == i + 1 else E[j]
            c = E[j][1] if j == i + 1 else E[i][1]
            if cross(sub(b, a), sub(c, b)) == 0:
                return False  # collinear consecutive: not a corner
            continue
        if seg_inter(*E[i], *E[j]):
            return False
    return True


def angle_units(P):
    """Interior angle of each vertex in units of pi/4 (P ccw)."""
    out = []
    n = len(P)
    for i in range(n):
        a, b, c = P[i - 1], P[i], P[(i + 1) % n]
        u, v = prim(sub(b, a)), prim(sub(c, b))
        # turning angle in units of pi/4
        dirs = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        t = (dirs.index(v) - dirs.index(u)) % 8
        if t > 4:
            t -= 8
        out.append(4 - t)
    return out


def inside(P, p):
    """Strict interior test (winding / crossing), p Fraction pair; None on boundary."""
    for a, b in edges(P):
        if cross(sub(b, a), sub(p, a)) == 0 and min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) \
                and min(a[1], b[1]) <= p[1] <= max(a[1], b[1]):
            return None
    c = False
    for a, b in edges(P):
        if (a[1] > p[1]) != (b[1] > p[1]):
            x = a[0] + Fr(p[1] - a[1]) * (b[0] - a[0]) / (b[1] - a[1])
            if x > p[0]:
                c = not c
    return c


def interior_lattice(P):
    xs = [v[0] for v in P]
    ys = [v[1] for v in P]
    return [(x, y) for x in range(min(xs), max(xs) + 1) for y in range(min(ys), max(ys) + 1)
            if inside(P, (x, y)) is True]


# ---------------------------------------------------------------- lattices
def egcd(a, b):
    if b == 0:
        return (abs(a), 1 if a >= 0 else -1, 0)
    g, s, t = egcd(b, a % b)
    return (g, t, s - (a // b) * t)


def hnf(vecs):
    piv = [0, 0]
    rest = []
    for r in vecs:
        r = [int(r[0]), int(r[1])]
        if r == [0, 0]:
            continue
        x, a = r[0], piv[0]
        if x == 0:
            rest.append(r)
            continue
        if a == 0:
            piv = r
            continue
        g, s, t = egcd(a, x)
        newp = [s * piv[0] + t * r[0], s * piv[1] + t * r[1]]
        other = [(x // g) * piv[0] - (a // g) * r[0], (x // g) * piv[1] - (a // g) * r[1]]
        assert other[0] == 0 and newp[0] == g
        piv = newp
        rest.append(other)
    d = 0
    for r in rest:
        d = gcd(d, r[1])
    if piv[0] < 0:
        piv = [-piv[0], -piv[1]]
    if d:
        piv[1] %= d
    return ((piv[0], piv[1]), (0, d))


def covol(L):
    return L[0][0] * L[1][1]


def reduce_mod(L, p):
    (a, b), (_, d) = L
    k = floor(Fr(p[0]) / a)
    p = (p[0] - k * a, p[1] - k * b)
    m = floor(Fr(p[1]) / d)
    return (p[0], p[1] - m * d)


CHECKER = hnf([(1, 1), (0, 2)])
TWO = hnf([(2, 0), (0, 2)])

# ---------------------------------------------------------------- tracer
def trace(P, S, d, T, bounces=14):
    """Exact billiard from S in integer direction d. Returns breakpoints, stop reason."""
    pts = [S]
    p = (Fr(S[0]), Fr(S[1]))
    cur_edge = None
    for _ in range(bounces):
        best = None
        for idx, (a, b) in enumerate(edges(P)):
            if idx == cur_edge:
                continue
            e = sub(b, a)
            den = cross(d, e)
            if den == 0:
                continue
            w = sub(a, p)
            s = Fr(cross(w, e), den)
            u = Fr(cross(w, d), den)
            if s > 0 and 0 <= u <= 1 and (best is None or s < best[0]):
                best = (s, u, idx)
        s, u, idx = best
        q = (p[0] + s * d[0], p[1] + s * d[1])
        # passes through target?
        w = sub(T, p)
        if cross(d, w) == 0 and 0 < (w[0] * d[0] + w[1] * d[1]) and \
                (w[0] * d[0] + w[1] * d[1]) < s * (d[0] ** 2 + d[1] ** 2):
            pts.append(T)
            return pts, "hit-target"
        pts.append(q)
        if u == 0 or u == 1:
            return pts, "corner"
        a, b = edges(P)[idx]
        d = mat_vec(refl(sub(b, a)), d)
        p, cur_edge = q, idx
    return pts, "bounce-limit"


# ---------------------------------------------------------------- unfolding
def tri_verts(t):
    i, j, k = t
    c = (Fr(2 * i + 1, 2), Fr(2 * j + 1, 2))
    sq = [(i, j), (i + 1, j), (i + 1, j + 1), (i, j + 1)]
    return (c, sq[k], sq[(k + 1) % 4])


def tri_nbrs(t):
    """[(edge endpoints, neighbour triangle)] for the 3 edges."""
    i, j, k = t
    c, p, q = tri_verts(t)
    out_n = [(i, j - 1, 2), (i + 1, j, 3), (i, j + 1, 0), (i - 1, j, 1)][k]
    return [((p, q), out_n), ((c, q), (i, j, (k + 1) % 4)), ((c, p), (i, j, (k - 1) % 4))]


def unfold(P):
    xs = [v[0] for v in P]
    ys = [v[1] for v in P]
    tris = set()
    for i in range(min(xs), max(xs)):
        for j in range(min(ys), max(ys)):
            for k in range(4):
                t = (i, j, k)
                v = tri_verts(t)
                cen = (sum(x[0] for x in v) / 3, sum(x[1] for x in v) / 3)
                if inside(P, cen):
                    tris.add(t)
    I = ((1, 0), (0, 1))
    root = (min(tris), I)
    A = {root: (I, (Fr(0), Fr(0)))}
    queue = [root]
    hol = []
    adj = {}

    def neighbours(f):
        t, g = f
        res = []
        for (a, b), tn in tri_nbrs(t):
            if tn in tris:
                res.append(((a, b), (tn, g), None))
            else:
                rho = refl(sub(b, a))
                res.append(((a, b), (t, mat_mul(g, rho)), (a, rho)))
        return res
    while queue:
        f = queue.pop()
        gf, bf = A[f]
        for (a, b), fn, w in neighbours(f):
            adj.setdefault(f, []).append(((a, b), fn))
            if w is None:
                exp = (gf, bf)
            else:
                q, rho = w
                qq = sub(q, mat_vec(rho, q))
                exp = (mat_mul(gf, rho), add(mat_vec(gf, qq), bf))
            if fn not in A:
                A[fn] = exp
                queue.append(fn)
            else:
                assert A[fn][0] == exp[0]
                hol.append(sub(exp[1], A[fn][1]))
    return tris, A, hol, adj


def develop(A, f, x):
    g, b = A[f]
    return add(mat_vec(g, x), b)


def period_data(P):
    tris, A, hol, adj = unfold(P)
    faces = list(A)
    assert len(faces) == 8 * len(tris), "unfolding not connected with 8 copies"
    Labs = hnf(hol)
    corner_pos = []
    for v in P:
        for f in faces:
            if v in tri_verts(f[0]):
                corner_pos.append(develop(A, f, v))
    base = corner_pos[0]
    Lrel = hnf(hol + [sub(c, base) for c in corner_pos])
    return tris, A, adj, Labs, Lrel, corner_pos


def degree(A, L, p):
    (a, b), (_, d) = L
    cnt = 0
    for f in A:
        V = [develop(A, f, x) for x in tri_verts(f[0])]
        xmin = min(v[0] for v in V)
        xmax = max(v[0] for v in V)
        ymin = min(v[1] for v in V)
        ymax = max(v[1] for v in V)
        r = reduce_mod(L, p)
        for i in range(floor((xmin - r[0]) / a) - 1, floor((xmax - r[0]) / a) + 2):
            x0, y0 = r[0] + i * a, r[1] + i * b
            for j in range(floor((ymin - y0) / d) - 1, floor((ymax - y0) / d) + 2):
                q = (x0, y0 + j * d)
                s = [cross(sub(V[(k + 1) % 3], V[k]), sub(q, V[k])) for k in range(3)]
                if all(z > 0 for z in s) or all(z < 0 for z in s):
                    cnt += 1
    return cnt


def translation_group(P):
    """Translation subgroup of the affine reflection group, anchored at an axial-diagonal vertex."""
    n = len(P)
    O = None
    for i in range(n):
        t1 = wall(P[i - 1], P[i])[0]
        t2 = wall(P[i], P[(i + 1) % n])[0]
        if {t1, t2} & {"x", "y"} and {t1, t2} & {"x+y", "x-y"}:
            O = P[i]
            lin = [refl(sub(P[i], P[i - 1])), refl(sub(P[(i + 1) % n], P[i]))]
            break
    # closure of linear parts at O
    grp = {((1, 0), (0, 1))}
    while True:
        new = {mat_mul(g, r) for g in grp for r in lin} | grp
        if new == grp:
            break
        grp = new
    taus = []
    for a, b in edges(P):
        rho = refl(sub(b, a))
        q = sub(a, O)
        taus.append(sub(q, mat_vec(rho, q)))
    gens = [mat_vec(g, t) for g in grp for t in taus]
    return O, len(grp), taus, hnf(gens)


def lifts_and_cones(P, A, adj, v):
    faces = [f for f in A if v in tri_verts(f[0])]
    parent = {f: f for f in faces}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for f in faces:
        for (a, b), fn in adj[f]:
            if v in (a, b) and fn in parent:
                parent[find(f)] = find(fn)
    comps = {}
    for f in faces:
        comps.setdefault(find(f), []).append(f)
    # each face contributes angle pi/4 at a lattice vertex
    return sorted(len(c) for c in comps.values())


# ---------------------------------------------------------------- report
def hdr(s):
    print()
    print("=" * 72)
    print(s)
    print("=" * 72)


def intercepts(P):
    return [wall(a, b) for a, b in edges(P) if wall(a, b)[0] in ("x+y", "x-y")]


def scalar_content(P):
    g = 0
    for v in P:
        w = sub(v, P[0])
        g = gcd(g, gcd(abs(w[0]), abs(w[1])))
    return g


def main():
    hdr("1. Rooms, the map F, corner types, marks, paths")
    for name in ROOMS:
        ROOMS[name] = ccw(ROOMS[name])
    for name in MIXED + ["C1 canonical c=1", "C2 canonical c=2 pentagon"]:
        P = ROOMS[name]
        FP = [F(v) for v in P]
        diag = intercepts(P)
        par = sorted({k % 2 for _, k in diag})
        print(f"\n[{name}] vertices {P}")
        print(f"  strictly simple: {strictly_simple(P)}  W={len(P)}  area={area(P)}  "
              f"scalar content={scalar_content(P)}")
        print(f"  diagonal walls {diag}  intercept parities {par}  mixed={par == [0, 1]}")
        ang = angle_units(P)
        print(f"  angles (pi/4 units) {ang}")
        if name not in MIXED:
            continue
        FPc = ccw(FP)
        Fdiag = intercepts(FPc)
        print(f"  F image {FP}")
        print(f"  F image strictly simple: {strictly_simple(FPc)}  W={len(FPc)}  area={area(FPc)}  "
              f"ratio={area(FPc) / area(P)}")
        print(f"  F image diagonal intercepts {Fdiag}  all even: {all(k % 2 == 0 for _, k in Fdiag)}")
        print(f"  F image angles {angle_units(FP if area(FP) > 0 else FP)}  same as original: "
              f"{angle_units(FP) == ang}")
        tiles = 0
        xs = [v[0] for v in FP]
        ys = [v[1] for v in FP]
        for i in range(min(xs), max(xs)):
            for j in range(min(ys), max(ys)):
                for cen in ([(Fr(3 * i + 2, 3), Fr(3 * j + 1, 3)), (Fr(3 * i + 1, 3), Fr(3 * j + 2, 3))]
                            if (i + j) % 2 == 0 else
                            [(Fr(3 * i + 1, 3), Fr(3 * j + 1, 3)), (Fr(3 * i + 2, 3), Fr(3 * j + 2, 3))]):
                    if inside(FPc, cen):
                        tiles += 1
        print(f"  canonical45 tiles in F image: N={tiles}; 4*area(P)={4 * area(P)}")
        # marks
        L0 = interior_lattice(P)
        L1 = interior_lattice(FPc)
        cls = lambda X: "A" if X[0] % 2 == 0 and X[1] % 2 == 0 else ("B" if X[0] % 2 and X[1] % 2 else "C")
        ok_cls = all(cls(F(s)) == ("A" if (s[0] + s[1]) % 2 == 0 else "B") for s in L0)
        AB1 = sorted(X for X in L1 if cls(X) != "C")
        print(f"  interior lattice points: {len(L0)}; images A/B with class = checkerboard parity: {ok_cls}")
        print(f"  F maps interior lattice points onto interior A/B points of F image: "
              f"{sorted(F(s) for s in L0) == AB1}  (C points in image: {len(L1) - len(AB1)}, "
              f"preimages are square centres)")
        # legal paths: fixed list of directions from the first two interior points
        dirs = [(1, 0), (0, 1), (1, 1), (1, -1), (2, 1), (1, 2), (3, 1), (1, -2), (3, -2)]
        agree = 0
        tot = 0
        reasons = {}
        S = L0[0]
        T = L0[-1]
        for d in dirs:
            p1, r1 = trace(P, S, d, T)
            p2, r2 = trace(FPc, F(S), F(d), F(T))
            tot += 1
            same = r1 == r2 and [F(x) for x in p1] == p2
            agree += same
            reasons[r1] = reasons.get(r1, 0) + 1
        print(f"  traced {tot} rays from {S} (target {T}): F(trace) == trace of F image in {agree}/{tot}; "
              f"stop reasons {reasons}")

    hdr("2. Minimality: obstruction and integrality of the candidate similarities")
    for name in MIXED:
        P = ROOMS[name]
        diag = intercepts(P)
        # translations mod 2 and D4: parity set of diagonal intercepts
        imgs = set()
        for g in D4:
            for c in [(0, 0), (1, 0), (0, 1), (1, 1)]:
                Q = [add(mat_vec(g, v), c) for v in P]
                imgs.add(tuple(sorted({k % 2 for _, k in intercepts(ccw(Q))})))
        anch = [sub(v, P[0]) for v in P]
        g_id = scalar_content(P)
        g_F = 0
        for w in anch:
            fw = F(w)
            g_F = gcd(g_F, gcd(abs(fw[0]), abs(fw[1])))
        colours = sorted({(v[0] + v[1]) % 2 for v in P})
        odd_t_keeps = all(tuple(sorted({(t * k) % 2 for _, k in diag})) == (0, 1) for t in (1, 3, 5))
        half_F_integral = all(fw % 2 == 0 for w in anch for fw in F(w))
        print(f"[{name}] parity sets over D4 x (Z/2)^2 translations: {sorted(imgs)}")
        print(f"  vertex colours (x+y mod 2): {colours}; gcd anchored entries: {g_id}; "
              f"gcd of F(anchored) entries: {g_F}")
        print(f"  odd t keeps mixed parity: {odd_t_keeps}; (1/2)F integral: {half_F_integral}; "
              f"=> least canonical area {2 * area(P)} = 2*area via F (t=1); t*Id needs t>=2, area {4 * area(P)}")
    P3 = [(3 * x, 3 * y) for x, y in ROOMS["M"]]
    print(f"[3M control, content 3] area {area(P3)}; (1/3)F(3M)=F(M) has canonical area "
          f"{2 * area(ROOMS['M'])} < 2*area(3M)={2 * area(P3)}: primitivity hypothesis needed")

    hdr("3. Periods: unfolding cycles vs translation subgroup; degrees; sites")
    gp = (Fr(1, 7), Fr(3, 11))
    gp2 = (Fr(5, 13), Fr(2, 17))
    for name in MIXED + ["C1 canonical c=1", "C2 canonical c=2 pentagon"] + ["F(M)"]:
        P = ROOMS[name] if name != "F(M)" else ccw([F(v) for v in ROOMS["M"]])
        tris, A, adj, Labs, Lrel, cpos = period_data(P)
        O, ordlin, taus, T = translation_group(P)
        Ar = area(P)
        dabs = degree(A, Labs, gp)
        drel = degree(A, Lrel, gp)
        print(f"\n[{name}] area {Ar}, faces {len(A)} (= 8 x {len(tris)} quarter-squares)")
        print(f"  Lambda_abs (cycles) HNF {Labs}, covol {covol(Labs)}; translation subgroup of G "
              f"(O={O}, |linear group|={ordlin}) HNF {T}; equal: {Labs == T}")
        print(f"  Lambda_rel HNF {Lrel}, covol {covol(Lrel)}; index {covol(Labs) // covol(Lrel)}; "
              f"Lambda_abs == checkerboard: {Labs == CHECKER}; == 2Z^2: {Labs == TWO}")
        print(f"  2*Lambda_rel inside Lambda_abs (half-turn lemma): "
              f"{all(reduce_mod(Labs, (2 * v[0], 2 * v[1])) == (0, 0) for v in Lrel)}")
        print(f"  d_abs counted {dabs} (2nd point {degree(A, Labs, gp2)}), 8*area/covol = {8 * Ar / covol(Labs)}, "
              f"4*area = {4 * Ar}, 2*area = {2 * Ar}")
        print(f"  d_rel counted {drel}, 8*area/covol = {8 * Ar / covol(Lrel)}")
        sites_c = sorted({tuple(int(z) for z in reduce_mod(Labs, c)) for c in cpos})
        print(f"  corner lifts project to sites {sites_c}")
        if name == "F(M)" or name.startswith("C"):
            continue
        marks = interior_lattice(P)
        bad = 0
        nl = None
        for s in marks:
            sites = set()
            copies = set()
            for f in A:
                if s in tri_verts(f[0]):
                    sites.add(reduce_mod(Labs, develop(A, f, s)))
                    copies.add(f[1])
            nl = len(copies)
            exp = reduce_mod(Labs, s)
            if sites != {exp}:
                bad += 1
        print(f"  interior lattice marks: {len(marks)}; each has {nl} lifts; marks whose lifts all project "
              f"to the single site S mod Lambda_abs: {len(marks) - bad}/{len(marks)}")
        same = [(s, t) for s, t in combinations(marks, 2) if (s[0] + s[1]) % 2 == (t[0] + t[1]) % 2]
        print(f"  same-checkerboard pairs: {len(same)}; all 16 lifts on one site: {bad == 0}")
        # quarter turn fixes both sites
        R = ((0, -1), (1, 0))
        print(f"  quarter turn fixes both sites: "
              f"{all(reduce_mod(Labs, mat_vec(R, s)) == s for s in sites_c)}")
        # cone angles
        rows = []
        ang = angle_units(P)
        ok = True
        for v, a in zip(P, ang):
            comps = lifts_and_cones(P, A, adj, v)
            g4 = gcd(4, a)
            ok &= len(comps) == g4 and all(c == 8 * a // g4 for c in comps) and sum(comps) == 8 * a
            rows.append((v, a, len(comps), [f"{Fr(c, 4)}pi" for c in comps], Fr(sum(comps), 8)))
        for r in rows:
            print(f"    corner {r[0]} angle {r[1]}pi/4: {r[2]} lifts, cone angles {r[3]}, "
                  f"outgoing germs per direction {r[4]}")
        print(f"  lifts = gcd(4,a) and cone = 2pi a/gcd(4,a), total germs = a: {ok}")

    hdr("4. Direction classes mod 2 on the checkerboard torus (M)")
    for m, n in [(1, 0), (0, 1), (2, 1), (1, 2), (3, 2), (1, 1), (1, -1), (3, 1), (1, 3), (5, 3)]:
        # D basis (1,1),(1,-1): m,n = p+q, p-q
        if (m + n) % 2:
            p, q = m + n, m - n
        else:
            p, q = (m + n) // 2, (m - n) // 2
        g = gcd(abs(p), abs(q))
        p, q = p // g, q // g
        # primitive (m,n): s*(m,n) is integral only for integer s, so the closed leaf from
        # site 0 meets the odd site iff the unit step (m,n) is off D
        hits = reduce_mod(CHECKER, (m, n)) == reduce_mod(CHECKER, (1, 0))
        print(f"  physical ({m},{n}) -> D-basis ({p},{q}); both odd: {p % 2 == 1 and q % 2 == 1}; "
              f"leaf from 0 meets odd site: {hits}")


if __name__ == "__main__":
    main()
