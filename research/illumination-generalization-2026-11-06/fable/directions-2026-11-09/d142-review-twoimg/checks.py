"""d142 checks for two-image-midpoints.md (snapshot 2026-11-22 01:00).

Exact Fraction arithmetic on named rooms only: R22 (manuscript vertex list), its
five-square staircase P, and d141's rooms H, B, O, M (definitions imported from
d141's checks.py). No room search and no direction search.

Model. X is the square-tiled unfolding (4 sheets for orthogonal rooms, 8 for
mixed). An X-square is (physical unit cell, sheet); a half cell cut by a
diagonal wall is paired with its mirror sheet. h, v are the right and up
neighbour permutations, computed by exact billiard tracing of a generic sample
point. A translation quotient Y of X over the base torus is a block system of
<h, v>. A half-turn of Y is a block permutation s with s h s^-1 = h^-1 and
s v s^-1 = v^-1 (integer centre; this is every -I map once Y has a zero, and
every admissible one when Y is a torus). Admissible for f: X -> Y means: an
involution, no fixed square centre or edge midpoint, and every X-vertex over a
fixed Y-vertex is a corner lift.

Run: python3 -B checks.py > checks.log
"""
import importlib.util
import os
import cmath
from fractions import Fraction as Fr
from itertools import permutations

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location(
    "d141checks", os.path.join(HERE, "..", "d141-review-freeht", "checks.py"))
d141 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(d141)
D141_ROOMS = {r[0][0]: r[1] for r in d141.ROOMS}

I2 = ((1, 0), (0, 1))
NEG = ((-1, 0), (0, -1))
ROT = ((0, -1), (1, 0))


def mm(A, B):
    return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)) for i in range(2))


def mv(A, v):
    return (A[0][0] * v[0] + A[0][1] * v[1], A[1][0] * v[0] + A[1][1] * v[1])


def tr(A):
    return ((A[0][0], A[1][0]), (A[0][1], A[1][1]))


def refl_lin(d):
    if d[1] == 0:
        return ((1, 0), (0, -1))
    if d[0] == 0:
        return ((-1, 0), (0, 1))
    return ((0, 1), (1, 0)) if d[0] * d[1] > 0 else ((0, -1), (-1, 0))


def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def floor(x):
    return x.numerator // x.denominator


class Room:
    def __init__(self, name, verts):
        P = list(verts)
        if sum(cross(P[i], P[(i + 1) % len(P)]) for i in range(len(P))) < 0:
            P = P[::-1]
        self.name, self.P, self.W = name, P, len(P)
        self.vset = set(P)
        self.E = [(P[i], P[(i + 1) % len(P)]) for i in range(len(P))]
        self.walls = []
        for a, b in self.E:
            s = refl_lin((b[0] - a[0], b[1] - a[1]))
            t = (a[0] - mv(s, a)[0], a[1] - mv(s, a)[1])
            self.walls.append((a, b, s, t))
        G, fr = {I2}, [I2]
        while fr:
            nw = []
            for g in fr:
                for w in self.walls:
                    k = mm(g, w[2])
                    if k not in G:
                        G.add(k)
                        nw.append(k)
            fr = nw
        self.G = sorted(G)
        self.mixed = len(G) == 8
        self.rho = ROT if self.mixed else NEG
        self.angles = d141.angle_units(P)
        # cells
        xs, ys = [p[0] for p in P], [p[1] for p in P]
        self.diag = {}
        for a, b, s, t in self.walls:
            if a[0] != b[0] and a[1] != b[1]:
                n = abs(b[0] - a[0])
                sx, sy = (b[0] - a[0]) // n, (b[1] - a[1]) // n
                for k in range(n):
                    p, q = (a[0] + k * sx, a[1] + k * sy), (a[0] + (k + 1) * sx, a[1] + (k + 1) * sy)
                    self.diag[(min(p[0], q[0]), min(p[1], q[1]))] = (s, t)
        self.cells = []
        for i in range(min(xs), max(xs)):
            for j in range(min(ys), max(ys)):
                probes = [(Fr(2 * i + 1, 2), j + Fr(1, 10)), (i + Fr(9, 10), Fr(2 * j + 1, 2)),
                          (Fr(2 * i + 1, 2), j + Fr(9, 10)), (i + Fr(1, 10), Fr(2 * j + 1, 2))]
                if any(self.inside(q) for q in probes):
                    self.cells.append((i, j))
        self.build()

    def inside(self, p):
        return d141.inside(self.P, p)

    def key(self, q, g):
        Q = (floor(q[0]), floor(q[1]))
        assert self.inside(q) is True and Q in self.cells, (self.name, q)
        if Q in self.diag:
            g = min(g, mm(g, self.diag[Q][0]))
        return (Q, g)

    def LL(self, K):
        (i, j), g = K
        cs = [mv(g, c) for c in ((i, j), (i + 1, j), (i, j + 1), (i + 1, j + 1))]
        return (min(c[0] for c in cs), min(c[1] for c in cs))

    def refl(self, Q, q):
        s, t = self.diag[Q]
        u = mv(s, q)
        return (u[0] + t[0], u[1] + t[1])

    def phys(self, K, o, closed=False):
        """Point (p, g) at chart offset o of square K."""
        Q, g0 = K
        L = self.LL(K)
        q = mv(tr(g0), (L[0] + o[0], L[1] + o[1]))
        st = self.inside(q)
        if Q not in self.diag or st is True or (closed and st is None):
            return q, g0
        return self.refl(Q, q), mm(g0, self.diag[Q][0])

    def offset(self, K, p, g):
        Q, g0 = K
        q = p if g == g0 else self.refl(Q, p)
        c, L = mv(g0, q), self.LL(K)
        return (c[0] - L[0], c[1] - L[1])

    def move(self, K, e):
        o0 = (Fr(37, 100), Fr(21, 100))
        p, g = self.phys(K, o0)
        d, rem, last = mv(tr(g), e), Fr(1), None
        while True:
            best = None
            for idx, (a, b, s, t) in enumerate(self.walls):
                if idx == last:
                    continue
                den = cross(d, (b[0] - a[0], b[1] - a[1]))
                if den == 0:
                    continue
                ap = (a[0] - p[0], a[1] - p[1])
                tt = Fr(cross(ap, (b[0] - a[0], b[1] - a[1])), den)
                uu = Fr(cross(ap, d), den)
                if tt > 0 and 0 <= uu <= 1 and (best is None or tt < best[0]):
                    best = (tt, idx, uu)
            if best is None or best[0] >= rem:
                p = (p[0] + rem * d[0], p[1] + rem * d[1])
                break
            tt, idx, uu = best
            assert 0 < uu < 1, "ray hit a vertex"
            p = (p[0] + tt * d[0], p[1] + tt * d[1])
            s = self.walls[idx][2]
            d, g, rem, last = mv(s, d), mm(g, s), rem - tt, idx
        K2 = self.key(p, g)
        assert self.offset(K2, p, g) == o0
        return K2

    def build(self):
        keys = set()
        for Q in self.cells:
            for g in self.G:
                if Q in self.diag:
                    g = min(g, mm(g, self.diag[Q][0]))
                keys.add((Q, g))
        self.keys = sorted(keys)
        self.n = len(self.keys)
        self.idx = {K: i for i, K in enumerate(self.keys)}
        self.h = [self.idx[self.move(K, (1, 0))] for K in self.keys]
        self.v = [self.idx[self.move(K, (0, 1))] for K in self.keys]
        assert sorted(self.h) == list(range(self.n)) and sorted(self.v) == list(range(self.n))
        # copy rotation R on squares
        o0 = (Fr(37, 100), Fr(21, 100))
        self.R = []
        for K in self.keys:
            p, g = self.phys(K, o0)
            self.R.append(self.idx[self.key(p, mm(self.rho, g))])
        # vertex classes and corner lifts
        self.vcls = corner_classes(self.n, self.h, self.v)
        offs = {"LL": (0, 0), "LR": (1, 0), "UL": (0, 1), "UR": (1, 1)}
        self.vphys = {}
        for (i, c), r in self.vcls.items():
            q, _ = self.phys(self.keys[i], offs[c], closed=True)
            assert self.vphys.setdefault(r, q) == q
        self.F = {r for r, q in self.vphys.items() if q in self.vset}

    def genus(self):
        return genus_of(self.n, self.vcls)

    def locate(self, p, g):
        """(square, offset in [0,1)^2) of the lift (p, g); p may lie on a wall."""
        eps = (Fr(1, 1000), Fr(1, 1013))
        cands = [g] + [mm(g, w[2]) for w in self.walls if d141.on_seg(p, w[0], w[1])]
        for g1 in cands:
            q = mv(tr(g1), eps)
            q = (p[0] + q[0], p[1] + q[1])
            if self.inside(q) is True:
                K = self.key(q, g1)
                o = self.offset(K, p, g1)
                assert 0 <= o[0] < 1 and 0 <= o[1] < 1
                return (self.idx[K], o)
        raise AssertionError("cannot locate")

    def lifts(self, p):
        return sorted({self.locate(p, g) for g in self.G})


def corner_classes(n, h, v):
    par = {}

    def f(x):
        while par.setdefault(x, x) != x:
            par[x] = par[par[x]]
            x = par[x]
        return x

    def u(a, b):
        par[f(a)] = f(b)
    for i in range(n):
        u((i, "LR"), (h[i], "LL"))
        u((i, "UR"), (h[i], "UL"))
        u((i, "UL"), (v[i], "LL"))
        u((i, "UR"), (v[i], "LR"))
    return {(i, c): f((i, c)) for i in range(n) for c in ("LL", "LR", "UL", "UR")}


def genus_of(n, vcls):
    V = len(set(vcls.values()))
    return 1 - (V - n) // 2  # chi = V - E + F = V - n


def is_conn(n, h, v):
    seen, st = {0}, [0]
    while st:
        x = st.pop()
        for y in (h[x], v[x]):
            if y not in seen:
                seen.add(y)
                st.append(y)
    return len(seen) == n


# ------------------------------------------------------------------ quotients
class Quot:
    """Y = X / block system. blk[i] = block of X-square i."""

    def __init__(self, X, blk):
        self.X = X
        ids = sorted(set(blk))
        ren = {b: k for k, b in enumerate(ids)}
        self.blk = [ren[b] for b in blk]
        self.n = len(ids)
        self.deg = X.n // self.n
        self.h = [None] * self.n
        self.v = [None] * self.n
        for i in range(X.n):
            for arr, perm in ((self.h, X.h), (self.v, X.v)):
                b2 = self.blk[perm[i]]
                assert arr[self.blk[i]] in (None, b2), "not a block system"
                arr[self.blk[i]] = b2
        self.hi = inv_perm(self.h)
        self.vi = inv_perm(self.v)
        self.vcls = corner_classes(self.n, self.h, self.v)
        self.g = genus_of(self.n, self.vcls)
        # X-vertex classes over each Y-vertex class
        self.over = {}
        for (i, c), r in X.vcls.items():
            self.over.setdefault(self.vcls[(self.blk[i], c)], set()).add(r)

    def pt(self, xp):
        return (self.blk[xp[0]], xp[1])

    def halfturns(self):
        out = []
        for k in range(self.n):
            s = [None] * self.n
            s[0], st, ok = k, [0], True
            while st and ok:
                a = st.pop()
                for b, im in ((self.h[a], self.hi[s[a]]), (self.v[a], self.vi[s[a]])):
                    if s[b] is None:
                        s[b] = im
                        st.append(b)
                    elif s[b] != im:
                        ok = False
            if ok and None not in s and sorted(s) == list(range(self.n)):
                out.append(s)
        return out

    def admissible(self, s):
        """(involution, fixed centres/edge midpoints, fixed vertices, all-forbidden-over-fixed)."""
        invol = all(s[s[i]] == i for i in range(self.n))
        bad = sum(1 for i in range(self.n) if s[i] == i) + \
            sum(1 for i in range(self.n) if s[i] == self.h[i]) + \
            sum(1 for i in range(self.n) if s[i] == self.v[i])
        imc = {"LL": "UR", "LR": "UL", "UL": "LR", "UR": "LL"}
        fixv = {self.vcls[(i, c)] for i in range(self.n) for c in imc
                if self.vcls[(s[i], imc[c])] == self.vcls[(i, c)]}
        forb = all(self.over[r] <= self.X.F for r in fixv)
        return invol, bad, len(fixv), invol and bad == 0 and forb

    def act(self, s, p):
        b, o = p
        b, o = s[b], (1 - o[0], 1 - o[1])
        if o[0] == 1:
            b, o = self.h[b], (Fr(0), o[1])
        if o[1] == 1:
            b, o = self.v[b], (o[0], Fr(0))
        return (b, o)


def inv_perm(p):
    q = [0] * len(p)
    for i, x in enumerate(p):
        q[x] = i
    return q


def coverage(Y, A, B, adm):
    """Pairs (x, y) in A x B with e f(x) = f(y) for some admissible e; also coincident pairs."""
    fA = [Y.pt(x) for x in A]
    fB = [Y.pt(y) for y in B]
    cov = set()
    for s in adm:
        for i, a in enumerate(fA):
            im = Y.act(s, a)
            for j, b in enumerate(fB):
                if im == b:
                    cov.add((i, j))
    coinc = sum(1 for a in fA for b in fB if a == b)
    per_src = [sum(1 for j in range(len(B)) if (i, j) in cov) for i in range(len(A))]
    return len(cov), coinc, per_src, len(set(fA)), len(set(fB))


def closure(X, a, b):
    par = list(range(X.n))

    def f(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x
    st = [(a, b)]
    while st:
        x, y = st.pop()
        rx, ry = f(x), f(y)
        if rx == ry:
            continue
        par[rx] = ry
        st.append((X.h[x], X.h[y]))
        st.append((X.v[x], X.v[y]))
    return [f(i) for i in range(X.n)]


def block_systems(X, sizes):
    seen, out = set(), []
    for k in range(1, X.n):
        blk = closure(X, 0, k)
        cnt = {}
        for b in blk:
            cnt[b] = cnt.get(b, 0) + 1
        sz = set(cnt.values())
        if len(sz) == 1 and sz.pop() in sizes:
            canon = tuple(sorted(tuple(sorted(i for i in range(X.n) if blk[i] == b)) for b in cnt))
            if canon not in seen:
                seen.add(canon)
                out.append(blk)
    return out


def translations(X):
    out = []
    for k in range(X.n):
        t = [None] * X.n
        t[0], st, ok = k, [0], True
        while st and ok:
            a = st.pop()
            for b, im in ((X.h[a], X.h[t[a]]), (X.v[a], X.v[t[a]])):
                if t[b] is None:
                    t[b] = im
                    st.append(b)
                elif t[b] != im:
                    ok = False
        if ok and sorted(t) == list(range(X.n)):
            out.append(tuple(t))
    return out


def subgroups(elems):
    E = set(elems)
    ident = tuple(range(len(elems[0])))

    def comp(a, b):
        return tuple(a[b[i]] for i in range(len(a)))

    def gen(gs):
        H, fr = {ident}, [ident]
        while fr:
            nw = []
            for x in fr:
                for g in gs:
                    y = comp(g, x)
                    if y not in H:
                        H.add(y)
                        nw.append(y)
            fr = nw
        return frozenset(H)
    return sorted({gen([a, b]) for a in E for b in E}, key=len)


def orbit_blocks(n, Gam):
    blk = list(range(n))
    for i in range(n):
        blk[i] = min(t[i] for t in Gam)
    return blk


def refine(X, Y):
    """Block system of u: X -> Z, Z the normalisation of x -> (f(R^j x))_j (meet of R-conjugates)."""
    l = 4 if X.mixed else 2
    labels = []
    for i in range(X.n):
        lab, j = [], i
        for _ in range(l):
            lab.append(Y.blk[j])
            j = X.R[j]
        labels.append(tuple(lab))
    ren = {}
    return Quot(X, [ren.setdefault(x, len(ren)) for x in labels])


def R_lift(X, xp):
    """Copy rotation of a lift, via its physical point."""
    p, g = X.phys(X.keys[xp[0]], xp[1], closed=True)
    return X.locate(p, mm(X.rho, g))


def analyse(X, Y, A, B, label, refine_check=True):
    hts = Y.halfturns()
    info = [Y.admissible(s) for s in hts]
    adm = [s for s, inf in zip(hts, info) if inf[3]]
    free_adm = sum(1 for inf in info if inf[3] and inf[2] == 0)
    ncov, coinc, per_src, nA, nB = coverage(Y, A, B, adm)
    print("  %-34s deg %2d genus %2d | half-turns %2d, invol %2d, admissible %d (free %d) |"
          " |f(A)|=%d |f(B)|=%d coincident %2d | pairs covered %2d/%d, max per source %d"
          % (label, Y.deg, Y.g, len(hts), sum(1 for i in info if i[0]), len(adm), free_adm,
             nA, nB, coinc, ncov, len(A) * len(B), max(per_src)))
    res = dict(cov=ncov, total=len(A) * len(B), coinc=coinc, adm=len(adm))
    if refine_check:
        Z = refine(X, Y)
        hz = Z.halfturns()
        az = [s for s in hz if Z.admissible(s)[3]]
        fz = [s for s in az if Z.admissible(s)[2] == 0]
        nz, cz, pz, nAz, nBz = coverage(Z, A, B, az)
        # refinement implication: pair covered on Y for all R^j-rotations => covered on Z by a free map
        l = 4 if X.mixed else 2
        Aidx = {a: i for i, a in enumerate(A)}
        Bidx = {b: j for j, b in enumerate(B)}
        covY = set()
        fA, fB = [Y.pt(x) for x in A], [Y.pt(y) for y in B]
        for s in adm:
            for i, a in enumerate(fA):
                for j, b in enumerate(fB):
                    if Y.act(s, a) == b:
                        covY.add((i, j))
        need, ok = 0, 0
        for i, x in enumerate(A):
            for j, y in enumerate(B):
                xs, ys, good = x, y, True
                for _ in range(l):
                    if (Aidx[xs], Bidx[ys]) not in covY:
                        good = False
                        break
                    xs, ys = R_lift(X, xs), R_lift(X, ys)
                if good:
                    need += 1
                    fzA, fzB = Z.pt(x), Z.pt(y)
                    if any(Z.act(s, fzA) == fzB for s in fz):
                        ok += 1
        print("  %-34s   refinement Z: deg u %d, genus %d, |u(A)|=%d |u(B)|=%d, admissible %d (free %d),"
              " covered %d/%d; R-orbit-covered pairs on Y %d, of which covered on Z by a free map %d"
              % ("", Z.deg, Z.g, nAz, nBz, len(az), len(fz), nz, len(A) * len(B), need, ok))
        res.update(zcov=nz, need=need, ok=ok)
    return res


def header(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def wall_bound(W):
    return (3 * W - 8) // 2  # max genus(X) - 1 for a mixed room with W corners


# ------------------------------------------------------------------ Moebius counts
def proj_eq(a, b):
    return abs(a[0] * b[1] - a[1] * b[0]) < 1e-9 * (abs(a[0]) + abs(a[1])) * (abs(b[0]) + abs(b[1]))


def mob_from(p, q):
    """Matrix sending projective points p1,p2,p3 to q1,q2,q3."""
    def std(pts):
        p1, p2, p3 = pts
        det = p2[0] * p1[1] - p1[0] * p2[1]
        al = (p3[0] * p1[1] - p1[0] * p3[1]) / det
        be = (p2[0] * p3[1] - p3[0] * p2[1]) / det
        return ((al * p2[0], be * p1[0]), (al * p2[1], be * p1[1]))

    def minv(M):
        (a, b), (c, d) = M
        D = a * d - b * c
        return ((d / D, -b / D), (-c / D, a / D))

    def mul(M, N):
        return tuple(tuple(sum(M[i][k] * N[k][j] for k in range(2)) for j in range(2)) for i in range(2))
    return mul(std(q), minv(std(p)))


def apply_m(M, z):
    return (M[0][0] * z[0] + M[0][1] * z[1], M[1][0] * z[0] + M[1][1] * z[1])


def eligible_count(pts):
    """Moebius involutions preserving the set pts and fixing exactly two of its points."""
    found = []
    n = len(pts)
    for img in permutations(range(n), 3):
        M = mob_from(pts[:3], [pts[k] for k in img])
        perm = []
        for z in pts:
            w = apply_m(M, z)
            m = [k for k in range(n) if proj_eq(w, pts[k])]
            if len(m) != 1:
                break
            perm.append(m[0])
        else:
            if sorted(perm) == list(range(n)) and perm != list(range(n)):
                if all(perm[perm[k]] == k for k in range(n)) and sum(perm[k] == k for k in range(n)) == 2:
                    found.append(tuple(perm))
    return len(set(found)), sorted(set(found))


def main():
    header("0. Inequalities: where the wall count enters")
    print("  genus(X)-1 <= (3W-8)/2 for mixed rooms. Needed lower bounds from the note's cases:")
    print("   elliptic H, singleton set: deg u >= 8, genus(Z) >= 5  -> genus(X)-1 >= 32")
    print("   genus(H) >= 3: genus(Z) >= 11 -> deg u <= floor(bound/10); deg 2 unramified: genus(Z)-1 <= bound/2")
    for W in range(18, 26):
        b = wall_bound(W)
        gz = [g for g in range(11, b // 2 + 2) if g % 2 == 1 and 2 * (g - 1) <= b]
        b2 = {g: g - 9 for g in gz}
        maxdeg = b // 10
        gz3 = [g for g in range(11, 40) if g % 2 == 1 and 3 * (g - 1) <= b]
        print("  W=%2d: max genus(X)-1 = %2d | singleton elliptic open: %-5s | max deg u (genus H>=3) = %d |"
              " deg-2 genus(Z) options %s, b2 = %s | deg-3 genus(Z) options %s"
              % (W, b, b >= 32, maxdeg, gz, [b2[g] for g in gz], gz3))

    header("1. Moebius involutions fixing exactly 2 of the b2 order-two branch values")
    w3 = cmath.exp(2j * cmath.pi / 3)
    inf = (1, 0)

    def P(z):
        return (z, 1)
    sets = {
        "b2=4 generic {0,inf,1,2+i/3}": [P(0), inf, P(1), P(2 + 1j / 3)],
        "b2=4 harmonic {0,inf,1,-1}": [P(0), inf, P(1), P(-1)],
        "b2=4 equianharmonic {inf,1,w,w^2}": [inf, P(1), P(w3), P(w3 * w3)],
        "b2=6 octahedron {0,inf,+-1,+-i}": [P(0), inf, P(1), P(-1), P(1j), P(-1j)],
        "b2=6 hexagon (6th roots of 1)": [P(cmath.exp(1j * cmath.pi * k / 3)) for k in range(6)],
        "b2=6 V4 orbits {0,inf,+-2,+-1/2}": [P(0), inf, P(2), P(-2), P(0.5), P(-0.5)],
        "b2=6 D2 {0,inf,+-1,+-3i}": [P(0), inf, P(1), P(-1), P(3j), P(-3j)],
        "b2=2 {0,inf}": [P(0), inf],
    }
    for name, pts in sets.items():
        if len(pts) < 3:
            print("  %-36s at most 1 (an involution is fixed by its two fixed points)" % name)
            continue
        c, f = eligible_count(pts)
        print("  %-36s eligible involutions: %d %s" % (name, c, f))

    header("2. Unfoldings of the named rooms")
    rooms = {}
    defs = [("R22", [(-1, -1), (0, -1), (0, -2), (1, -2), (1, -3), (2, -3), (2, -1), (1, -1), (1, 1), (3, 1),
                     (3, 0), (5, 0), (5, 1), (4, 1), (4, 2), (3, 2), (3, 3), (1, 3), (1, 2), (0, 2), (0, 1), (-1, 1)]),
            ("P-staircase", [(-1, -1), (-1, 0), (1, 0), (1, -1), (2, -1), (2, -3), (1, -3), (1, -2), (0, -2), (0, -1)]),
            ("H", D141_ROOMS["H"]), ("B", D141_ROOMS["B"]), ("O", D141_ROOMS["O"]), ("M", D141_ROOMS["M"])]
    for name, verts in defs:
        X = Room(name, verts)
        rooms[name] = X
        g = X.genus()
        from math import gcd
        if X.mixed:
            pred = 1 + (4 * (X.W - 2) - sum(gcd(4, a) for a in X.angles)) // 2
        else:
            pred = 1 + sum(1 for a in X.angles if a == 6)
        T = translations(X)
        print("  %-12s W=%2d mixed=%-5s sheets %d squares %3d connected %s genus %2d (corner formula %2d)"
              " corner lifts %2d |Trans(X)| %d"
              % (name, X.W, X.mixed, len(X.G), X.n, is_conn(X.n, X.h, X.v), g, pred, len(X.F), len(T)))
        assert g == pred
        X.trans = T

    header("3. Replays: every translation quotient by a subgroup of Trans(X), every block system of size 2 and 3")
    S0 = (Fr(53, 40), Fr(27, 40))
    cases = {
        "R22": [((0, 0), (2, 2), "dark pair S,T")],
        "H": [((1, Fr(1, 2)), (1, Fr(3, 2)), "S,T mirrored by y=1"),
              (S0, (S0[0], 2 - S0[1]), "d141 S and its y=1 mirror")],
        "B": [(S0, (Fr(27, 40), Fr(53, 40)), "d141 S, hidden target 1"),
              (S0, (Fr(133, 40), Fr(107, 40)), "d141 S, hidden target 2"),
              (S0, (4 - S0[0], S0[1]), "d141 S and x=2 mirror")],
        "O": [(S0, (Fr(27, 40), Fr(67, 40)), "d141 S, quarter-turn target 1"),
              (S0, (Fr(93, 40), Fr(53, 40)), "d141 S, quarter-turn target 2"),
              (S0, (S0[0], 3 - S0[1]), "d141 S and y=3/2 mirror")],
        "M": [(S0, (Fr(5, 2), Fr(7, 4)), "d141 S and an arbitrary point")],
    }
    summary = []
    for name, lst in cases.items():
        X = rooms[name]
        quots = []
        for Gam in subgroups(X.trans):
            lab = "X/Gamma, |Gamma|=%d" % len(Gam)
            quots.append((lab, orbit_blocks(X.n, Gam)))
        galois = {tuple(sorted(set(tuple(sorted(i for i in range(X.n) if b[i] == c)) for c in b))) for _, b in quots}
        for blk in block_systems(X, {2, 3}):
            canon = tuple(sorted(set(tuple(sorted(i for i in range(X.n) if blk[i] == c)) for c in blk)))
            if canon in galois:
                continue
            sz = X.n // len(set(blk))
            quots.append(("block system, size %d (non-Galois)" % sz, blk))
        nb2 = sum(1 for b in block_systems(X, {2}))
        nb3 = sum(1 for b in block_systems(X, {3}))
        print("\n[%s] translation subgroups %d; block systems of size 2: %d, size 3: %d"
              % (name, len(subgroups(X.trans)), nb2, nb3))
        for Sp, Tp, desc in lst:
            assert X.inside(Sp) is True and X.inside(Tp) is True
            A, B = X.lifts(Sp), X.lifts(Tp)
            print(" pair %s: S=(%s,%s) T=(%s,%s), |A|=%d |B|=%d"
                  % (desc, Sp[0], Sp[1], Tp[0], Tp[1], len(A), len(B)))
            for lab, blk in quots:
                r = analyse(X, Quot(X, blk), A, B, lab)
                summary.append((name, desc, lab, r))
    header("4. Summary of section 3")
    allcov = [s for s in summary if s[3]["cov"] == s[3]["total"]]
    print("  quotient/pair cases: %d; cases where one quotient covers all pairs: %d" % (len(summary), len(allcov)))
    print("  max covered fraction: %s" % (max((s[3]["cov"], s[3]["total"], s[0], s[1], s[2]) for s in summary),))
    disj = [s for s in summary if s[3]["coinc"] == 0]
    print("  refinement step when f(A), f(B) are disjoint (covered on Y for all R-rotations =>"
          " covered on Z by a free map): %s over %d cases, %d nonvacuous"
          % (all(s[3]["need"] == s[3]["ok"] for s in disj), len(disj), sum(1 for s in disj if s[3]["need"])))
    bad = [(s[0], s[1], s[2], s[3]["need"], s[3]["ok"]) for s in summary if s[3]["need"] != s[3]["ok"]]
    print("  cases where it fails (all have coincident images, so the all-pairs hypothesis already fails): %s"
          % bad)
    print("  nonzero coverage cases: %s"
          % [(s[0], s[1], s[2], "%d/%d" % (s[3]["cov"], s[3]["total"]), "coinc %d" % s[3]["coinc"])
             for s in summary if s[3]["cov"]])
    print("  cases with coincident images f(A) meets f(B): %s"
          % sorted({(s[0], s[1], s[2]) for s in summary if s[3]["coinc"]}))

    header("5. R22: the staircase fold as a degree-3 translation map M -> M_P")
    X, Pm = rooms["R22"], rooms["P-staircase"]
    folds = [(I2, (0, 0)), (((1, 0), (0, -1)), (0, 0)), (NEG, (4, 0))]
    o0 = (Fr(37, 100), Fr(21, 100))
    fmap = []
    for K in X.keys:
        p, g = X.phys(K, o0)
        hits = []
        for L, t in folds:
            q = mv(L, p)
            q = (q[0] + t[0], q[1] + t[1])
            if Pm.inside(q) is True:
                hits.append((q, mm(g, L)))
        assert len(hits) == 1
        q, gq = hits[0]
        KP = Pm.key(q, gq)
        assert Pm.offset(KP, q, gq) == o0
        fmap.append(Pm.idx[KP])
    ok = all(fmap[X.h[i]] == Pm.h[fmap[i]] and fmap[X.v[i]] == Pm.v[fmap[i]] for i in range(X.n))
    print("  fold is a translation map of square-tiled surfaces: %s; degree %d" % (ok, X.n // Pm.n))
    cls = {}
    for (i, c), r in X.vcls.items():
        cls.setdefault(Pm.vcls[(fmap[i], c)], set()).add(r)
    viol = [(Pm.vphys[rp], sorted({X.vphys[r] for r in rs if r not in X.F}))
            for rp, rs in cls.items() if rp in Pm.F and not rs <= X.F]
    print("  forbidden vertices of M_P whose fibre contains non-forbidden points of M: %d" % len(viol))
    for v in sorted(viol):
        print("    P corner %s  <- regular points of Q at %s" % v)
    A, B = X.lifts((0, 0)), X.lifts((2, 2))
    fa = sorted({(fmap[a[0]], a[1]) for a in A})
    fb = sorted({(fmap[b[0]], b[1]) for b in B})
    print("  images of the 4 S-lifts: %d points; of the 4 T-lifts: %d points; chart offsets %s %s"
          % (len(fa), len(fb), sorted({x[1] for x in fa}), sorted({x[1] for x in fb})))
    print("  -> the fold violates the full-fibre rule, so the theorem's hypothesis cannot be met through it;"
          " R22 is orthogonal, so section 3 of the note excludes every common quotient at every W.")


if __name__ == "__main__":
    main()
