"""D136 checks for reciprocal-resonance.2026-11-21-2230.md.

Exact rational linear algebra only (fractions.Fraction).  No room-family search:
only the named rooms are built (cov279 slice and stretch, st279 end-square
stretch, the U/U+1 dumbbell of length-periodicity.md).  Abstract coefficient
tuples are enumerated in part A only; they are not rooms.
Run: python3 -B checks.py > checks.log
"""
from fractions import Fraction as F
from itertools import product, combinations
from math import gcd, isqrt, log10, sqrt, ceil, exp, log
import random
import time

T0 = time.process_time()
random.seed(136)


def out(*a):
    print(*a, flush=True)


# ------------------------------------------------------------ linear algebra
def rref(rows, ncols):
    M = [[F(v) for v in r] for r in rows]
    piv, r = [], 0
    for c in range(ncols):
        k = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if k is None:
            continue
        M[r], M[k] = M[k], M[r]
        pv = M[r][c]
        M[r] = [v / pv for v in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        piv.append(c)
        r += 1
        if r == len(M):
            break
    return M[:r], piv


def rank(rows, ncols):
    return len(rref(rows, ncols)[0]) if rows else 0


def nullspace(rows, ncols):
    if not rows:
        return [[F(int(i == j)) for i in range(ncols)] for j in range(ncols)]
    R, piv = rref(rows, ncols)
    free = [c for c in range(ncols) if c not in piv]
    basis = []
    for f in free:
        v = [F(0)] * ncols
        v[f] = F(1)
        for i, p in enumerate(piv):
            v[p] = -R[i][f]
        basis.append(v)
    return basis


def span_basis(vecs, n):
    return rref(vecs, n)[0] if vecs else []


def contains(big, small, n):
    return rank(big + small, n) == rank(big, n)


def mat_vec(C, v):
    return [sum(c * x for c, x in zip(row, v)) for row in C]


def bil(x, C, y):
    return sum(x[i] * C[i][j] * y[j] for i in range(len(x)) for j in range(len(y)))


def det_int(A):
    """Bareiss, integer matrix."""
    A = [list(map(int, r)) for r in A]
    n = len(A)
    if n == 0:
        return 1
    sign, prev = 1, 1
    for k in range(n - 1):
        if A[k][k] == 0:
            sw = next((i for i in range(k + 1, n) if A[i][k] != 0), None)
            if sw is None:
                return 0
            A[k], A[sw] = A[sw], A[k]
            sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                A[i][j] = (A[i][j] * A[k][k] - A[i][k] * A[k][j]) // prev
        prev = A[k][k]
    return sign * A[n - 1][n - 1]


def rank_test(Cs, a, b):
    """The note's test: K = common kernel of flattened C_i, X = column span,
    Y = row span, Fx/Fy = fully free directions (left/right kernels)."""
    rows = [[C[i][j] for i in range(a) for j in range(b)] for C in Cs]
    t = rank(rows, a * b)
    K = nullspace(rows, a * b)
    cols, rws = [], []
    for v in K:
        M = [[v[i * b + j] for j in range(b)] for i in range(a)]
        cols += [[M[i][j] for i in range(a)] for j in range(b)]
        rws += [M[i][:] for i in range(a)]
    X = span_basis(cols, a)
    Y = span_basis(rws, b)
    Fx = nullspace([[C[i][j] for i in range(a)] for C in Cs for j in range(b)], a) if Cs else nullspace([], a)
    Fy = nullspace([C[i][:] for C in Cs for i in range(a)], b) if Cs else nullspace([], b)
    return t, K, X, Y, Fx, Fy


# ============================================================ A. pencil bound
out("== A. Pencil height bound 4J^2 (exhaustive over abstract coefficient tuples) ==")


def rat_roots(c2, c1, c0):
    """rational roots of c2 X^2 + c1 X + c0 (not identically zero)."""
    if c2 == 0:
        if c1 == 0:
            return []
        return [F(-c0, c1)]
    D = c1 * c1 - 4 * c2 * c0
    if D < 0:
        return []
    s = isqrt(D)
    if s * s != D:
        return []
    return list({F(-c1 + s, 2 * c2), F(-c1 - s, 2 * c2)})


def pencil_max(J):
    worst, worst_mid, cnt, solved = 0, 0, 0, 0
    rng = range(-J, J + 1)
    for e in product(rng, repeat=8):
        a11, a12, a21, a22, b11, b12, b21, b22 = e
        # e1: (a11 X + a21) Y + (a12 X + a22) = 0 ; e2 likewise with b
        A, B = (a11, a21), (a12, a22)
        C, D = (b11, b21), (b12, b22)
        # R_X = A D - B C as polynomial in X: coefficients
        rx2 = A[0] * D[0] - B[0] * C[0]
        rx1 = A[0] * D[1] + A[1] * D[0] - B[0] * C[1] - B[1] * C[0]
        rx0 = A[1] * D[1] - B[1] * C[1]
        # R_Y: regroup e1 as (a11 Y + a12) X + (a21 Y + a22)
        P, Q = (a11, a12), (a21, a22)
        Rr, S = (b11, b12), (b21, b22)
        ry2 = P[0] * S[0] - Q[0] * Rr[0]
        ry1 = P[0] * S[1] + P[1] * S[0] - Q[0] * Rr[1] - Q[1] * Rr[0]
        ry0 = P[1] * S[1] - Q[1] * Rr[1]
        if (rx2, rx1, rx0) == (0, 0, 0) or (ry2, ry1, ry0) == (0, 0, 0):
            continue
        cnt += 1
        for X in rat_roots(rx2, rx1, rx0):
            for Y in rat_roots(ry2, ry1, ry0):
                if (a11 * X + a21) * Y + a12 * X + a22 == 0 and (b11 * X + b21) * Y + b12 * X + b22 == 0:
                    solved += 1
                    h = max(abs(X.numerator), X.denominator, abs(Y.numerator), Y.denominator)
                    worst = max(worst, h)
                    if rx0 == 0 or ry0 == 0:
                        worst_mid = max(worst_mid, h)
    return worst, worst_mid, cnt, solved


for J in (1, 2):
    w, wm, cnt, solved = pencil_max(J)
    out(f"J={J}: {cnt} systems with both determinants nonzero, {solved} affine rational solutions; "
        f"max height {w} (bound 4J^2={4*J*J}, 2J^2={2*J*J}); max height when a constant term vanishes {wm}")
# the J = 4ME^2 example: coefficient of x_i y_j in n1 d1 u2 + n2 d2 u1 is at most 2ME^2
worstJ = 0
for _ in range(2000):
    E, M = random.randint(1, 4), random.randint(1, 4)
    u1, u2, d1, d2 = ([random.randint(-E, E) for _ in range(2)] for _ in range(4))
    n1, n2 = random.randint(-M, M), random.randint(-M, M)
    C = [[n1 * d1[j] * u2[i] + n2 * d2[j] * u1[i] for j in range(2)] for i in range(2)]
    worstJ = max(worstJ, max(abs(c) for r in C for c in r) / (M * E * E))
out(f"J/(M E^2) over 2000 random two-term identities: max {worstJ:.2f} (note uses 4; 2 suffices)")

# reciprocal redundancy: d1 u2 - d2 u1 and u1 d2 - u2 d1 are the same polynomial
out("\nReciprocal example: x=(u1,u2), y=(d1,d2).  Identity d1/u1=d2/u2 -> C=[[0,-1],[1,0]] (x rows).")
C1 = [[F(0), F(-1)], [F(1), F(0)]]          # x^T C y = -u1 d2 + u2 d1
C1t = [[F(0), F(1)], [F(-1), F(0)]]         # u1/d1 = u2/d2 cleared: u1 d2 - u2 d1
out(f"  transposed test is -1 times the same form: {all(C1t[i][j] == -C1[i][j] for i in range(2) for j in range(2))}")
for N in (1, 10, 1000):
    x, y = [F(N), F(N + 1)], [F(N), F(N + 1)]
    out(f"  N={N}: widths/depths (N,N+1) satisfy it: {bil(x, C1, y) == 0}; height {N+1}")
t, K, X, Y, Fx, Fy = rank_test([C1], 2, 2)
out(f"  rank test: t={t}, dim K={len(K)}, dim X={len(X)}, dim Y={len(Y)} (true factors are lines)")
out()

# ============================================================ B. Cramer / Hadamard
out("== B. Cramer spanning vectors of K and defining rows: entry bounds ==")


def cramer_kernel(R):
    """Integer kernel vectors by the note's pivot-minor rule."""
    n = len(R[0])
    Rr, piv = rref(R, n)
    t = len(piv)
    # independent rows of R
    ind, cur = [], []
    for r in R:
        if rank(cur + [r], n) > len(cur):
            cur.append(r)
            ind.append(r)
    B = [[ind[i][p] for p in piv] for i in range(t)]
    dB = det_int(B)
    vecs = []
    for f in [c for c in range(n) if c not in piv]:
        v = [0] * n
        v[f] = dB
        for k, p in enumerate(piv):
            Bk = [row[:] for row in B]
            for i in range(t):
                Bk[i][k] = ind[i][f]
            v[p] = -det_int(Bk)
        vecs.append(v)
    return vecs, t


worst_ratio = 0
for trial in range(150):
    n = random.randint(4, 12)
    t0 = random.randint(1, n - 1)
    M = random.randint(1, 3)
    R = [[random.randint(-2 * M, 2 * M) for _ in range(n)] for _ in range(t0)]
    vecs, t = cramer_kernel(R)
    if t == 0:
        continue
    assert all(sum(r[i] * v[i] for i in range(n)) == 0 for r in R for v in vecs)
    assert rank(vecs, n) == n - t
    Delta = ceil(max(1, 2 * M * sqrt(max(1, t))) ** t)
    mx = max(abs(c) for v in vecs for c in v)
    assert mx <= Delta
    worst_ratio = max(worst_ratio, mx / Delta)
    # defining rows of span(vecs) (dimension j): kernel of the j x n matrix
    j = len(vecs)
    if j < n:
        rows2, _ = cramer_kernel(vecs)
        H = ceil((sqrt(j) * mx) ** j)
        assert max(abs(c) for r in rows2 for c in r) <= H
        assert all(sum(r[i] * v[i] for i in range(n)) == 0 for r in rows2 for v in vecs)
out(f"150 random integer systems: kernel vectors integral, span K, entries <= Delta; "
    f"max entry/Delta = {worst_ratio:.2e}; defining rows <= ceil((sqrt(j) Delta)^j): all PASS")
out()

# ============================================================ C. what the test decides
out("== C. Exactness of the dimension test ==")
# C1: equivalence (dim X = dim Vx and dim Y = dim Vy)  <=>  K = Vx (x) Vy
agree = 0
for trial in range(60):
    a, b = random.randint(2, 4), random.randint(2, 4)
    jx, jy = random.randint(1, a), random.randint(1, b)
    Bx = [[F(random.randint(-2, 2)) for _ in range(a)] for _ in range(jx)]
    By = [[F(random.randint(-2, 2)) for _ in range(b)] for _ in range(jy)]
    if rank(Bx, a) < jx or rank(By, b) < jy:
        continue
    prodvecs = [[bx[i] * by[j] for i in range(a) for j in range(b)] for bx in Bx for by in By]
    ann = nullspace(prodvecs, a * b)  # annihilator of Vx(x)Vy
    k = random.randint(0, len(ann))
    coefs = [[F(random.randint(-2, 2)) for _ in ann] for _ in range(k)]
    rowsC = [[sum(cf * v[c] for cf, v in zip(cr, ann)) for c in range(a * b)] for cr in coefs]
    Cs = [[[r[i * b + j] for j in range(b)] for i in range(a)] for r in rowsC]
    t, K, X, Y, Fx, Fy = rank_test(Cs, a, b)
    dims_ok = len(X) == jx and len(Y) == jy
    K_eq = len(K) == jx * jy
    assert contains(X, Bx, a) and contains(Y, By, b)
    assert dims_ok == K_eq
    agree += 1
out(f"C1. {agree} random instances: (dim X=dim Vx and dim Y=dim Vy) <=> K = Vx(x)Vy, i.e. "
    f"t = ab - jx*jy.  PASS")
# C2: identities determine the factors uniquely, yet the dimension test fails
E = lambda i, j: [[F(int((r, c) == (i, j))) for c in range(2)] for r in range(2)]
C_a = E(1, 1)                                   # x2 y2 = 0
C_b = [[F(0), F(1)], [F(-1), F(0)]]             # x1 y2 - x2 y1 = 0
t, K, X, Y, Fx, Fy = rank_test([C_a, C_b], 2, 2)
# all rank-one matrices in K: K = span(E11, E12+E21): [[a,b],[b,0]] rank one iff b = 0
out(f"C2. identities x2y2=0, x1y2-x2y1=0: t={t}, dim K={len(K)}, dim X={len(X)}, dim Y={len(Y)}; "
    f"K basis {[[str(c) for c in v] for v in K]}")
uniq = []
for x1, x2, y1, y2 in product(range(-3, 4), repeat=4):
    if (x1, x2) != (0, 0) and (y1, y2) != (0, 0) and x2 * y2 == 0 and x1 * y2 - x2 * y1 == 0:
        uniq.append(((x1, x2), (y1, y2)))
lines = {(tuple(F(c, max(map(abs, x))) * (1 if next(v for v in x if v) > 0 else -1) for c in x),
          tuple(F(c, max(map(abs, y))) * (1 if next(v for v in y if v) > 0 else -1) for c in y)) for x, y in uniq}
out(f"    product solutions (lines) with entries in [-3,3]: {sorted((tuple(map(str,a)),tuple(map(str,b))) for a,b in lines)}")
out("    => the factors are pinned to (e1, e1) with height 1, but X = Y = Q^2: test is sufficient, not necessary.")
out()


# ============================================================ D. named rooms
class Aff:
    """affine form in parameters: dict name->coef, '' is constant."""

    def __init__(self, d):
        self.d = {k: F(v) for k, v in d.items()}

    def ev(self, P):
        return self.d.get('', F(0)) + sum(c * P[k] for k, c in self.d.items() if k)

    def __sub__(self, o):
        r = dict(self.d)
        for k, v in o.d.items():
            r[k] = r.get(k, F(0)) - v
        return Aff(r)


def A(**kw):
    c = kw.pop('c', 0)
    d = dict(kw)
    d[''] = c
    return Aff(d)


class Named:
    def __init__(self, name, xlev, ylev, rects, S, T, sample, params, seamT=None):
        """xlev/ylev: dict label->Aff.  rects: list of (xlo,xhi,ylo,yhi) labels
        (union = room).  S, T: (xlabel, ylabel).  sample: parameter dict used for
        the order type.  params: list of parameter dicts spanning the family."""
        self.name = name
        self.P0 = sample
        self.xl = sorted(xlev, key=lambda k: xlev[k].ev(sample))
        self.yl = sorted(ylev, key=lambda k: ylev[k].ev(sample))
        vx = [xlev[k].ev(sample) for k in self.xl]
        vy = [ylev[k].ev(sample) for k in self.yl]
        assert all(p < q for p, q in zip(vx, vx[1:])) and all(p < q for p, q in zip(vy, vy[1:]))
        self.xlev, self.ylev = xlev, ylev
        self.ix = {k: i for i, k in enumerate(self.xl)}
        self.iy = {k: i for i, k in enumerate(self.yl)}
        self.a, self.b = len(self.xl) - 1, len(self.yl) - 1
        # cells
        self.cells = set()
        for (x0, x1, y0, y1) in rects:
            for i in range(self.ix[x0], self.ix[x1]):
                for j in range(self.iy[y0], self.iy[y1]):
                    self.cells.add((i, j))
        self.S = (self.ix[S[0]], self.iy[S[1]])
        self.T = (self.ix[T[0]], self.iy[T[1]])
        # family spans (gap vectors at the given parameter points)
        gx = lambda P: [xlev[self.xl[k + 1]].ev(P) - xlev[self.xl[k]].ev(P) for k in range(self.a)]
        gy = lambda P: [ylev[self.yl[k + 1]].ev(P) - ylev[self.yl[k]].ev(P) for k in range(self.b)]
        for P in params:
            assert all(g > 0 for g in gx(P)) and all(g > 0 for g in gy(P)), (name, P)
        self.Vx = span_basis([gx(P) for P in params], self.a)
        self.Vy = span_basis([gy(P) for P in params], self.b)
        self.gx, self.gy = gx, gy
        self.params = params

    # decomposition into maximal rectangles of one orientation
    def rects(self, horiz):
        cells = self.cells
        if horiz:
            lines_ = {}
            for (i, j) in cells:
                lines_.setdefault(j, []).append(i)
            runs = []
            for j in sorted(lines_):
                xs = sorted(lines_[j])
                s = xs[0]
                for p, q in zip(xs, xs[1:] + [None]):
                    if q != p + 1:
                        runs.append((s, p + 1, j))
                        s = q
            # merge identical runs in consecutive rows
            R = []
            for (s, e, j) in runs:
                for r in R:
                    if r[0] == s and r[1] == e and r[3] == j:
                        r[3] = j + 1
                        break
                else:
                    R.append([s, e, j, j + 1])
            return [tuple(r) for r in R]       # (x0,x1,y0,y1) in index units
        else:
            T = Named.__new__(Named)
            T.cells = {(j, i) for (i, j) in cells}
            return [(y0, y1, x0, x1) for (x0, x1, y0, y1) in Named.rects(T, True)]

    def route(self, horiz):
        R = self.rects(horiz)
        # adjacency across sides transverse to travel
        def adj(r, s):
            if horiz:   # share a horizontal seam
                if r[3] == s[2] or s[3] == r[2]:
                    return max(r[0], s[0]) < min(r[1], s[1])
            else:
                if r[1] == s[0] or s[1] == r[0]:
                    return max(r[2], s[2]) < min(r[3], s[3])
            return False
        G = {i: [j for j in range(len(R)) if j != i and adj(R[i], R[j])] for i in range(len(R))}

        def containing(p):
            return [i for i, r in enumerate(R) if r[0] <= p[0] <= r[1] and r[2] <= p[1] <= r[3]]

        def path(a_, b_):
            prev, Q = {a_: None}, [a_]
            for u in Q:
                for v in G[u]:
                    if v not in prev:
                        prev[v] = u
                        Q.append(v)
            p, u = [], b_
            while u is not None:
                p.append(u)
                u = prev[u]
            return p[::-1]
        cS, cT = containing(self.S), containing(self.T)
        common = set(cS) & set(cT)
        if common:
            return R, None, 'direct (marks in one closed rectangle)'
        best = None
        for s in cS:
            for t in cT:
                p = path(s, t)
                if best is None or len(p) < len(best):
                    best = p
        return R, best, None

    def forms(self, horiz):
        """For each used rectangle: (width form, travel form) as gap vectors.
        Horizontal: width in x-gaps, travel in y-gaps.  Vertical: width in
        y-gaps, travel in x-gaps."""
        R, p, why = self.route(horiz)
        if p is None:
            return [], why
        na, nb = (self.a, self.b) if horiz else (self.b, self.a)
        out_ = []
        # coordinate of marks along travel axis / transverse
        tr = (lambda pt: pt[1]) if horiz else (lambda pt: pt[0])
        for k, ri in enumerate(p):
            r = R[ri]
            w0, w1, t0, t1 = (r[0], r[1], r[2], r[3]) if horiz else (r[2], r[3], r[0], r[1])
            width = [F(int(w0 <= g < w1)) for g in range(na)]
            sides = []
            for nb_ in ([p[k - 1]] if k > 0 else []) + ([p[k + 1]] if k < len(p) - 1 else []):
                s = R[nb_]
                st0 = s[2] if horiz else s[0]
                sides.append('lo' if st0 < t0 else 'hi')
            if k == 0 or k == len(p) - 1:
                m = tr(self.S if k == 0 else self.T)
                side = sides[0]
                lo, hi = (m, t1) if side == 'hi' else (t0, m)
                kind = 'partial'
            else:
                lo, hi = t0, t1
                kind = 'full' if sides[0] != sides[1] else 'doubled'
            travel = [F(int(lo <= g < hi)) for g in range(nb)]
            assert any(travel), (self.name, horiz, k)
            out_.append((width, travel, kind, ri))
        return out_, None


def restrict(form, B):
    return [sum(f * v for f, v in zip(form, b)) for b in B]


def two_term_identities(fam, horiz):
    """All two-term resonances n_i alpha_i + n_j alpha_j = 0 holding
    identically on the family span Vx x Vy; returned as x-by-y matrices."""
    fs, why = fam.forms(horiz)
    ids = []
    a, b = fam.a, fam.b
    for (i, fi), (j, fj) in combinations(enumerate(fs), 2):
        ui, di = fi[0], fi[1]
        uj, dj = fj[0], fj[1]
        # horizontal: alpha = d(y)/(2u(x)); identity n_i d_i u_j + n_j d_j u_i (x(x)y)
        if horiz:
            P = [[uj[r] * di[c] for c in range(b)] for r in range(a)]
            Q = [[ui[r] * dj[c] for c in range(b)] for r in range(a)]
        else:  # alpha = d(x)/(2u(y))
            P = [[di[r] * uj[c] for c in range(b)] for r in range(a)]
            Q = [[dj[r] * ui[c] for c in range(b)] for r in range(a)]
        vP = [bil(bx, P, by) for bx in fam.Vx for by in fam.Vy]
        vQ = [bil(bx, Q, by) for bx in fam.Vx for by in fam.Vy]
        ns = nullspace([[p, q] for p, q in zip(vP, vQ)], 2)
        if len(ns) == 1:
            ni, nj = ns[0]
            L = 1
            for v in (ni, nj):
                L = L * v.denominator // gcd(L, v.denominator)
            ni, nj = int(ni * L), int(nj * L)
            g = gcd(ni, nj)
            ni, nj = ni // g, nj // g
            C = [[ni * P[r][c] + nj * Q[r][c] for c in range(b)] for r in range(a)]
            ids.append(((i, j), (ni, nj), C))
    return fs, why, ids


def relation_dim(fam, horiz, nsamp=40):
    """dim of {n : sum n_i alpha_i == 0 on the family flat}, by exact evaluation
    at random rational points of Vx x Vy, then re-verified at fresh points."""
    fs, _ = fam.forms(horiz)
    if not fs:
        return 0, []
    def pt():
        while True:
            cx = [F(random.randint(1, 60)) for _ in fam.Vx]
            cy = [F(random.randint(1, 60)) for _ in fam.Vy]
            x = [sum(c * bx[i] for c, bx in zip(cx, fam.Vx)) for i in range(fam.a)]
            y = [sum(c * by[i] for c, by in zip(cy, fam.Vy)) for i in range(fam.b)]
            vals = []
            ok = True
            for (u, d, _, _) in fs:
                uu = sum(c * v for c, v in zip(u, x if horiz else y))
                dd = sum(c * v for c, v in zip(d, y if horiz else x))
                if uu == 0:
                    ok = False
                vals.append(dd / (2 * uu) if uu else 0)
            if ok:
                return vals
    rows = [pt() for _ in range(nsamp)]
    ns = nullspace(rows, len(fs))
    for v in ns:
        for _ in range(30):
            assert sum(c * a_ for c, a_ in zip(v, pt())) == 0
    return len(ns), ns


def report(fam, known):
    out(f"-- {fam.name}")
    out(f"   gaps a={fam.a} (x), b={fam.b} (y); family span dims jx={len(fam.Vx)}, jy={len(fam.Vy)}; "
        f"area at sample {sum((fam.gx(fam.P0)[i]) * (fam.gy(fam.P0)[j]) for i, j in fam.cells)}")
    allC = []
    for horiz in (True, False):
        lab = 'horizontal' if horiz else 'vertical'
        fs, why, ids = two_term_identities(fam, horiz)
        if why:
            out(f"   {lab} route: {why}")
            continue
        kinds = [k for (_, _, k, _) in fs]
        rd, ns = relation_dim(fam, horiz)
        out(f"   {lab} route: {len(fs)} rectangles {kinds}; resonance-relation space on the flat: dim {rd}"
            + (f" basis {[[str(c) for c in v] for v in ns]}" if ns else ''))
        for (ij, n, C) in ids:
            assert all(bil(bx, C, by) == 0 for bx in fam.Vx for by in fam.Vy)
            out(f"     two-term identity on rectangles {ij} with n={n}; max|C|={max(abs(c) for r in C for c in r)}")
        allC += [C for (_, _, C) in ids]
    t, K, X, Y, Fx, Fy = rank_test(allC, fam.a, fam.b)
    need = fam.a * fam.b - len(fam.Vx) * len(fam.Vy)
    assert contains(X, fam.Vx, fam.a) and contains(Y, fam.Vy, fam.b)
    out(f"   rank test: t={t} independent identities (equality needs t = ab - jx*jy = {need}); "
        f"dim X={len(X)} vs jx={len(fam.Vx)}, dim Y={len(Y)} vs jy={len(fam.Vy)}; "
        f"fully free directions: {len(Fx)} in x, {len(Fy)} in y")
    out(f"   test verdict: {'factors recovered' if (len(X), len(Y)) == (len(fam.Vx), len(fam.Vy)) else 'NOT recovered'}; "
        f"known: {known}")
    return t, need


out("== D. Rank test on the named rooms (route identities on each family span) ==")
fams = []
# cov279 thin-room bands: (0,2q)x(0,2) (2q-3,4q)x(2,3) (2q,5q)x(3,4) (4q,6q)x(4,6)
covx = dict(X0=A(c=0), Xa=A(q=2, c=-3), Xb=A(q=2), Xc=A(q=4), Xd=A(q=5), Xe=A(q=6))
covy = dict(Y0=A(c=0), Y2=A(c=2), Y3=A(c=3), Y4=A(c=4), Y6=A(c=6))
covR = [('X0', 'Xb', 'Y0', 'Y2'), ('Xa', 'Xc', 'Y2', 'Y3'), ('Xb', 'Xd', 'Y3', 'Y4'), ('Xc', 'Xe', 'Y4', 'Y6')]
# 1. directional slice q = 4u, S=(4,1), T=(12,1)
fams.append((Named('cov279 slice q=4u, S=(4,1), T=(12,1) [parametric-orbits directional pair]',
                   dict(covx, S=A(c=4), T=A(c=12)), dict(covy, M=A(c=1)), covR, ('S', 'M'), ('T', 'M'),
                   {'q': F(16)}, [{'q': F(4 * u)} for u in (4, 7, 10)]),
             'all-direction pair directly visible; directional orbit (p,1)=(8v,1) lit iff gcd(u,v)=1'))
# 2. stretch q = 12j+4, S=(q/2,1), T=(3q,3) (d130 pair; T on the seam y=3, first band toward S is band 1)
fams.append((Named('cov279 stretch q=12j+4, S=(q/2,1), T=(3q,3) [d130 pair]',
                   dict(covx, S=A(q=F(1, 2)), T=A(q=3)), dict(covy, M=A(c=1)), covR, ('S', 'M'), ('T', 'Y3'),
                   {'q': F(16)}, [{'q': F(12 * j + 4)} for j in (1, 2, 3)]),
             'lit for every q=12j+4 (d127 all same-parity pairs, 3 does not divide q; d130 witnesses)'))
# 3. stretch, cross pair S=(q/2,1), T=(5q,5)
fams.append((Named('cov279 stretch q=12j+4, S=(q/2,1), T=(9q/2,5) [cross pair, same parity]',
                   dict(covx, S=A(q=F(1, 2)), T=A(q=F(9, 2))), dict(covy, M=A(c=1), N=A(c=5)), covR, ('S', 'M'), ('T', 'N'),
                   {'q': F(16)}, [{'q': F(12 * j + 4)} for j in (1, 2, 3)]),
             'lit for every q=12j+4 (d127: all same-parity pairs when 3 does not divide q)'))
# 4. st279 end-square stretch: (0,m)^2, (m-1,m+2)x(m,m+1), (m,m+3)x(m+1,m+2), (m+2,2m+2)^2
stx = dict(X0=A(c=0), Xa=A(m=1, c=-1), Xb=A(m=1), Xc=A(m=1, c=2), Xd=A(m=1, c=3), Xe=A(m=2, c=2))
sty = dict(Y0=A(c=0), Ya=A(m=1), Yb=A(m=1, c=1), Yc=A(m=1, c=2), Ye=A(m=2, c=2))
stR = [('X0', 'Xb', 'Y0', 'Ya'), ('Xa', 'Xc', 'Ya', 'Yb'), ('Xb', 'Xd', 'Yb', 'Yc'), ('Xc', 'Xe', 'Yc', 'Ye')]
fams.append((Named('st279 slice m, S=(2,1), T=(6,1) [parametric-orbits directional pair]',
                   dict(stx, S=A(c=2), T=A(c=6)), dict(sty, M=A(c=1)), stR, ('S', 'M'), ('T', 'M'),
                   {'m': F(32)}, [{'m': F(16 * k)} for k in (2, 3, 4)]),
             'all-direction pair directly visible; directional orbit lit iff p = +-4 mod m'))
fams.append((Named('st279 end-square stretch m, S=(m/2,m/2), T=(3m/2+2,3m/2+2) [square centres]',
                   dict(stx, S=A(m=F(1, 2)), T=A(m=F(3, 2), c=2)), dict(sty, M=A(m=F(1, 2)), N=A(m=F(3, 2), c=2)),
                   stR, ('S', 'M'), ('T', 'N'), {'m': F(32)}, [{'m': F(16 * k)} for k in (2, 3, 4)]),
             'all-direction status of this pair not reviewed; d130 proves the named fat pairs lit (Omega(sqrt m) reflections)'))
# 5. dumbbell of length-periodicity.md: chambers U and U+1 wide, height 5, centred unit door (2,3), corridor L
dbx = dict(X0=A(c=0), Xu=A(U=1), Xv=A(U=1, L=1), Xw=A(U=2, L=1, c=1), S=A(c=2), T=A(U=1, L=1, c=2))
dby = dict(Y0=A(c=0), Y1=A(c=1), Y2=A(c=2), Y3=A(c=3), Y5=A(c=5))
dbR = [('X0', 'Xu', 'Y0', 'Y5'), ('Xu', 'Xv', 'Y2', 'Y3'), ('Xv', 'Xw', 'Y0', 'Y5')]
fams.append((Named('dumbbell U, U+1, height 5, S=(2,1), T=(U+L+2,3) [length-periodicity marks]',
                   dbx, dby, dbR, ('S', 'Y1'), ('T', 'Y3'), {'U': F(4), 'L': F(7)},
                   [{'U': F(u), 'L': F(l)} for u, l in ((4, 1), (4, 9), (7, 3), (9, 20))]),
             'opposite-chamber pairs lit for all L >= K (period-one tail; resonant-gluing K=21 for the reviewed dumbbells)'))
for fam, known in fams:
    report(fam, known)
out()

# st279 extra: show the one forced identity alpha1 = alpha2 (two identical 3x1 strips)
# ============================================================ E. directional replay
out("== E. Directional controls (exact replay, capped) ==")
MAXROWS = 200000


def shoot(cells, run, S, T, p, sx, sy):
    x, y = S
    seen = set()
    t = 0
    while t < MAXROWS:
        key = (x, y, sx, sy)
        if key in seen:
            return 'periodic'
        seen.add(key)
        j = y if sy > 0 else y - 1
        i = x if sx > 0 else x - 1
        a, b = run[(i, j)]
        L = b - a
        th = (x - a) if sx > 0 else (2 * L - (x - a))
        th = (th + p) % (2 * L)
        if 0 < th < L:
            x, sx = a + th, 1
        elif L < th < 2 * L:
            x, sx = a + 2 * L - th, -1
        elif th == L:
            x, sx = b, 1
        else:
            x, sx = a, -1
        y += sy
        t += 1
        if (x, y) == T:
            return 'lit'
        Ac = (x - 1 if sx > 0 else x, y - 1 if sy > 0 else y)
        Hc = (x if sx > 0 else x - 1, Ac[1])
        Vc = (Ac[0], y if sy > 0 else y - 1)
        Dc = (Hc[0], Vc[1])
        h, v, d = Hc in cells, Vc in cells, Dc in cells
        if h and v and d:
            continue
        if h and not v and not d:
            sy = -sy
            continue
        if v and not h and not d:
            sx = -sx
            continue
        return 'stop'
    return 'cap'


def build(bands):
    cells = set()
    for (x0, x1, y0, y1) in bands:
        cells |= {(i, j) for i in range(x0, x1) for j in range(y0, y1)}
    run = {}
    rows = {}
    for (i, j) in cells:
        rows.setdefault(j, []).append(i)
    for j, xs in rows.items():
        xs.sort()
        s = xs[0]
        for p, q in zip(xs, xs[1:] + [None]):
            if q != p + 1:
                for k in range(s, p + 1):
                    run[(k, j)] = (s, p + 1)
                s = q
    return cells, run


def lit_dir(cells, run, S, T, p):
    return any(shoot(cells, run, S, T, p, sx, sy) == 'lit' for sx in (1, -1) for sy in (1, -1))


dark_pts, mism = [], 0
for u in (4, 7):
    q = 4 * u
    cells, run = build([(0, 2 * q, 0, 2), (2 * q - 3, 4 * q, 2, 3), (2 * q, 5 * q, 3, 4), (4 * q, 6 * q, 4, 6)])
    for v in range(1, 2 * u + 4):
        L_ = lit_dir(cells, run, (4, 1), (12, 1), 8 * v)
        mism += L_ != (gcd(u, v) == 1)
        if not L_:
            dark_pts.append([F(u), F(v)])
out(f"cov279 u=4,7: mismatches vs gcd(u,v)=1: {mism}; directional-dark (u,v) points {[(int(a),int(b)) for a,b in dark_pts]}; "
    f"their rational span has dim {rank(dark_pts, 2)}")
m = 32
cells, run = build([(0, m, 0, m), (m - 1, m + 2, m, m + 1), (m, m + 3, m + 1, m + 2), (m + 2, 2 * m + 2, m + 2, 2 * m + 2)])
mism, litp = 0, []
for p in range(4, 4 * m + 1, 4):
    L_ = lit_dir(cells, run, (2, 1), (6, 1), p)
    mism += L_ != ((p % m) in (4, m - 4))
    if L_:
        litp.append(p)
out(f"st279 m=32: lit p = {litp}; mismatches vs p=+-4 mod m: {mism}")
out("Both marks pairs share the bottom band, so the flat-resonance route is empty (direct chord).")
out()

# ============================================================ F. constants
out("== F. Scale of the conditional constants ==")


def Mmin(eps, k):
    """least M with exp(-4 M eps^2) < (2M+1)^(-k)."""
    lo = 1
    while not (-4 * lo * eps * eps < -k * log(2 * lo + 1)):
        lo *= 2
    hi, lo = lo, max(1, lo // 2)
    while lo < hi:
        mid = (lo + hi) // 2
        if -4 * mid * eps * eps < -k * log(2 * mid + 1):
            hi = mid
        else:
            lo = mid + 1
    return hi


for eps, k in ((1 / 8, 2), (1 / 8, 9), (1 / 64, 4), (1 / 1024, 4), (1 / 4096, 4)):
    out(f"  eps={eps:.3g}, k={k}: least M = {Mmin(eps, k)}")
# cov279 cross pair: door overlap width 3 between band 0 and 1, U = 3q, nu = 4 traversals
for q in (16, 40, 100, 1000):
    eps = min(1 / 8, (3 / 2) / (8 * 4 * 3 * q))
    out(f"  cov279 cross route at q={q}: eps <= {eps:.3g} -> M >= {Mmin(eps, 4)}")
eps = min(1 / 8, (1 / 2) / (8 * 4 * 3))
out(f"  cov279 cross route at the flat point with door offset c=q (gaps stay positive): eps <= {eps:.3g} -> M >= {Mmin(eps, 4)} for every q")
for M in (1, 10):
    a = b = 11
    t = a * b - 1
    lD = t * log10(2 * M * sqrt(t))
    lH = 11 * (0.5 * log10(11) + lD)
    lcensus = log10(144) + 242 * (log10(2) + lH)
    d = 22
    lD2 = d * (0.5 * log10(d) + lH)
    larea = log10(4 * d ** 4) + 2 * lD2
    out(f"  M={M}, a=b=11, t=ab-1=120: log10 Delta={lD:.1f}, log10 H={lH:.1f}, "
        f"log10(d133 witness pairs per cell)={lcensus:.3g}, log10(d132 area bound)={larea:.3g}")
# identity count available from tree routes at W <= 20 (k <= r+1 = 9 rectangles per orientation)
k = 9
avail = 2 * k * (k - 1) // 2
out(f"  two-term identities from both tree routes, k<=9 each: at most {avail}; "
    f"equality needs ab - jx*jy <= {avail}, i.e. jx*jy >= {121-avail} at a=b=11")
out(f"\nCPU seconds: {time.process_time() - T0:.1f}")
