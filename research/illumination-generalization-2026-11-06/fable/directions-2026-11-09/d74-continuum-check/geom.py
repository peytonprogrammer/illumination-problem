"""d74: room combinatorics, DP-cylinder labels, exact convex clipping, exact billiard tracer.

Written from the theory (d13 theory.md, Lemma A') only. No code of Astra's checker is used.
All arithmetic is exact (int / Fraction).
"""
from fractions import Fraction as F
from math import gcd


# ---------------------------------------------------------------- rooms
def read_rooms(path):
    """Lines 'area walls x0 y0 x1 y1 ... [|]' -> list of frozenset cells."""
    out = []
    for line in open(path):
        tok = line.replace('|', ' ').split()
        if not tok:
            continue
        a = int(tok[0])
        xs = list(map(int, tok[2:]))
        assert len(xs) == 2 * a, line
        out.append(frozenset(zip(xs[0::2], xs[1::2])))
    return out


def around(cs, x, y):
    return [(x - 1, y - 1) in cs, (x, y - 1) in cs, (x - 1, y) in cs, (x, y) in cs]


def pt_kind(cs, x, y):
    k = sum(around(cs, x, y))
    if k == 4:
        return 'int'
    if k == 3:
        return 'rfx'
    if k == 1:
        return 'cvx'
    if k == 2:
        a, b, c, d = around(cs, x, y)
        return 'pinch' if (a and d) or (b and c) else 'flat'
    return 'out'


def walls(cs):
    pts = {(i + dx, j + dy) for (i, j) in cs for dx in (0, 1) for dy in (0, 1)}
    return sum(pt_kind(cs, *p) in ('cvx', 'rfx') for p in pts)


def is_corner(cs, x, y):
    return pt_kind(cs, x, y) in ('cvx', 'rfx', 'pinch')


def interior_point(cs, x, y):
    """Exact test: (x, y) rational lies in int P."""
    fx, fy = x.__floor__(), y.__floor__()
    xi, yi = x == fx, y == fy
    if not xi and not yi:
        return (fx, fy) in cs
    if xi and not yi:
        return (fx - 1, fy) in cs and (fx, fy) in cs
    if yi and not xi:
        return (fx, fy - 1) in cs and (fx, fy) in cs
    return pt_kind(cs, fx, fy) == 'int'


# ---------------------------------------------------------------- cylinders for one direction
class Direction:
    """DP-cylinder structure of room cs in M-direction (p, q), p, q >= 1 coprime.

    Room segment = (cell, fam, K2) with fam 0 = plus (t = q x - p y), fam 1 = minus (s = q x + p y),
    K2 = 2 * (value of t or s on the segment).  Odd K2: midline of an open band (a band is the open
    strip (K2-1)/2 < t < (K2+1)/2 inside the open cell).  Even K2: an integer line crossing the open
    cell.  Unoriented billiard flow links segment ends; a segment end at a corner is singular.
    """

    def __init__(self, cs, p, q):
        self.cs, self.p, self.q = cs, p, q
        self.par = {}
        self.sing = set()      # roots (in line union-find) of singular integer-line orbits
        # integer lines
        lpar = {}

        def lfind(a):
            r = a
            while lpar[r] != r:
                r = lpar[r]
            while lpar[a] != r:
                lpar[a], a = r, lpar[a]
            return r
        lines, bands = [], []
        for c in cs:
            for fam in (0, 1):
                lo, hi = self.rng(c, fam)
                for K in range(lo, hi):           # bands K .. K+1
                    bands.append((c, fam, 2 * K + 1))
                for K in range(lo + 1, hi):       # integer lines strictly inside
                    lines.append((c, fam, 2 * K))
        for s in lines:
            lpar[s] = s
        bad = []
        for s in lines:
            for nxt in self.ends(s):
                if nxt is None:
                    bad.append(s)
                else:
                    a, b = lfind(s), lfind(nxt)
                    if a != b:
                        lpar[a] = b
        singroots = {lfind(s) for s in bad}
        self.singular = {s for s in lines if lfind(s) in singroots}
        # bands
        bpar = {b: b for b in bands}

        def bfind(a):
            r = a
            while bpar[r] != r:
                r = bpar[r]
            while bpar[a] != r:
                bpar[a], a = r, bpar[a]
            return r

        def bunion(a, b):
            a, b = bfind(a), bfind(b)
            if a != b:
                bpar[a] = b
        for s in bands:
            for nxt in self.ends(s):
                assert nxt is not None and nxt in bpar, (s, nxt)
                bunion(s, nxt)
        for (c, fam, K2) in lines:
            if (c, fam, K2) not in self.singular:
                bunion((c, fam, K2 - 1), (c, fam, K2 + 1))
        self.label = {b: bfind(b) for b in bands}
        self.ncyl = len(set(self.label.values()))

    def rng(self, c, fam):
        """Open range (lo, hi) of t (fam 0) or s (fam 1) over cell c; lo, hi integers."""
        a, b = c
        p, q = self.p, self.q
        if fam == 0:
            return q * a - p * (b + 1), q * (a + 1) - p * b
        return q * a + p * b, q * (a + 1) + p * (b + 1)

    def chord(self, c, fam, k):
        """End points (lower x first) of the line {t or s = k} inside closed cell c."""
        a, b = c
        p, q = self.p, self.q
        if fam == 0:   # y = (q x - k) / p increasing
            x0 = max(F(a), F(k + p * b, q))
            x1 = min(F(a + 1), F(k + p * (b + 1), q))
            return (x0, (q * x0 - k) / p), (x1, (q * x1 - k) / p)
        x0 = max(F(a), F(k - p * (b + 1), q))
        x1 = min(F(a + 1), F(k - p * b, q))
        return (x0, (k - q * x0) / p), (x1, (k - q * x1) / p)

    def reflect(self, fam, k, axis, w):
        """Reflection of family/value across the wall line x = w (axis 'v') or y = w (axis 'h')."""
        p, q = self.p, self.q
        if axis == 'v':
            return 1 - fam, 2 * q * w - k
        return (1, k + 2 * p * w) if fam == 0 else (0, k - 2 * p * w)

    def ends(self, seg):
        """The two continuations of seg (None = hits a corner)."""
        c, fam, K2 = seg
        k = F(K2, 2)
        A, B = self.chord(c, fam, k)
        p, q = self.p, self.q
        vy = q if fam == 0 else -q
        res = []
        for E, sx, sy in ((B, 1, 1 if vy > 0 else -1), (A, -1, -1 if vy > 0 else 1)):
            res.append(self.step(c, fam, k, E, sx, sy))
        return res

    def step(self, c, fam, k, E, sx, sy):
        cs = self.cs
        a, b = c
        x, y = E
        xi, yi = x.denominator == 1, y.denominator == 1
        H, V, D = (a + sx, b), (a, b + sy), (a + sx, b + sy)
        if xi and yi:
            h, v, d = H in cs, V in cs, D in cs
            if h and v and d:
                nc, nf, nk = D, fam, k
            elif h and not v and not d:
                nf, nk = self.reflect(fam, k, 'h', int(y))
                nc = H
            elif v and not h and not d:
                nf, nk = self.reflect(fam, k, 'v', int(x))
                nc = V
            else:
                return None
        elif xi:
            if H in cs:
                nc, nf, nk = H, fam, k
            else:
                nf, nk = self.reflect(fam, k, 'v', int(x))
                nc = c
        else:
            assert yi
            if V in cs:
                nc, nf, nk = V, fam, k
            else:
                nf, nk = self.reflect(fam, k, 'h', int(y))
                nc = c
        K2 = 2 * nk
        assert K2.denominator == 1
        return (nc, nf, int(K2))

    def tval(self, fam, x, y):
        return self.q * x - self.p * y if fam == 0 else self.q * x + self.p * y

    def labels_at(self, x, y):
        """Lambda(S) for an interior point S = (x, y): set of DP-cylinder labels."""
        out = set()
        fx, fy = x.__floor__(), y.__floor__()
        cands = [(fx - i, fy - j) for i in (0, 1) for j in (0, 1)]
        for fam in (0, 1):
            k = self.tval(fam, x, y)
            for c in cands:
                if c not in self.cs:
                    continue
                if not (c[0] <= x <= c[0] + 1 and c[1] <= y <= c[1] + 1):
                    continue
                lo, hi = self.rng(c, fam)
                if not (lo < k < hi):
                    continue
                if k.denominator != 1:
                    out.add(self.label[(c, fam, 2 * (k.__floor__()) + 1)])
                elif (c, fam, 2 * int(k)) not in self.singular:
                    out.add(self.label[(c, fam, 2 * int(k) + 1)])
                break
            else:
                raise AssertionError('no cell for label', x, y, fam)
        return out

    def singular_lines(self, c):
        """Singular integer lines crossing open cell c: list of (a, b, cst) meaning a x + b y = cst."""
        out = []
        p, q = self.p, self.q
        for fam in (0, 1):
            lo, hi = self.rng(c, fam)
            for K in range(lo + 1, hi):
                if (c, fam, 2 * K) in self.singular:
                    out.append((q, -p, K) if fam == 0 else (q, p, K))
        return out

    def kept_runs(self, c, lam):
        """Maximal runs [i1, i2] (closed t-range) of plus bands of c with label not in lam; same for minus."""
        runs = []
        for fam in (0, 1):
            lo, hi = self.rng(c, fam)
            r, cur = [], None
            for K in range(lo, hi):
                ok = self.label[(c, fam, 2 * K + 1)] not in lam
                if ok and cur is None:
                    cur = K
                if not ok and cur is not None:
                    r.append((cur, K))
                    cur = None
            if cur is not None:
                r.append((cur, hi))
            runs.append(r)
        return runs


def dirs(B):
    out = [(p, q) for p in range(1, B + 1) for q in range(1, B + 1) if gcd(p, q) == 1]
    out.sort(key=lambda d: (max(d), d[0] + d[1], d))
    return out


# ---------------------------------------------------------------- convex polygons (vertex lists)
def clip(poly, a, b, c, sense):
    """poly ∩ {sense * (a x + b y - c) <= 0}.  poly is a closed convex vertex list (ccw or degenerate)."""
    n = len(poly)
    if n == 0:
        return []
    vals = [sense * (a * x + b * y - c) for (x, y) in poly]
    if all(v <= 0 for v in vals):
        return poly
    if all(v > 0 for v in vals):
        return []
    out = []
    for i in range(n):
        P, vp = poly[i], vals[i]
        Qp, vq = poly[(i + 1) % n], vals[(i + 1) % n]
        if vp <= 0:
            out.append(P)
        if (vp < 0 < vq) or (vq < 0 < vp):
            t = vp / (vp - vq)
            out.append((P[0] + t * (Qp[0] - P[0]), P[1] + t * (Qp[1] - P[1])))
    ded = []
    for v in out:
        if not ded or ded[-1] != v:
            ded.append(v)
    while len(ded) > 1 and ded[0] == ded[-1]:
        ded.pop()
    return ded


def area2(poly):
    s = 0
    n = len(poly)
    for i in range(n):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % n]
        s += x0 * y1 - x1 * y0
    return s


def square(c):
    a, b = c
    return [(F(a), F(b)), (F(a + 1), F(b)), (F(a + 1), F(b + 1)), (F(a), F(b + 1))]


def bbox(poly):
    xs = [v[0] for v in poly]
    ys = [v[1] for v in poly]
    return min(xs), max(xs), min(ys), max(ys)


def convex_intersect(P, Q):
    """Do closed convex sets P, Q (vertex lists, any dimension 0..2) intersect?  Exact, via SAT
    for polygons; lower-dimensional sets are handled by clipping."""
    R = P
    n = len(Q)
    if n >= 3:
        for i in range(n):
            (x0, y0), (x1, y1) = Q[i], Q[(i + 1) % n]
            a, b = y1 - y0, x0 - x1          # outward normal for ccw Q
            R = clip(R, a, b, a * x0 + b * y0, 1)
            if not R:
                return False
        return True
    if n == 1:
        return point_in(Q[0], P)
    # Q segment: intersect P with the segment line and the segment slab
    (x0, y0), (x1, y1) = Q
    a, b = y1 - y0, x0 - x1
    R = clip(R, a, b, a * x0 + b * y0, 1)
    R = clip(R, a, b, a * x0 + b * y0, -1)
    if not R:
        return False
    dx, dy = x1 - x0, y1 - y0
    R = clip(R, dx, dy, dx * x1 + dy * y1, 1)
    R = clip(R, dx, dy, dx * x0 + dy * y0, -1)
    return bool(R)


def point_in(pt, P):
    if len(P) == 1:
        return P[0] == pt
    if len(P) == 2:
        (x0, y0), (x1, y1) = P
        cr = (x1 - x0) * (pt[1] - y0) - (y1 - y0) * (pt[0] - x0)
        if cr != 0:
            return False
        d = (pt[0] - x0) * (x1 - x0) + (pt[1] - y0) * (y1 - y0)
        return 0 <= d <= (x1 - x0) ** 2 + (y1 - y0) ** 2
    n = len(P)
    for i in range(n):
        (x0, y0), (x1, y1) = P[i], P[(i + 1) % n]
        if (x1 - x0) * (pt[1] - y0) - (y1 - y0) * (pt[0] - x0) < 0:
            return False
    return True


# ---------------------------------------------------------------- exact billiard tracer (rational)
def trace(cs, S, v):
    """Follow the billiard from S with velocity v for time 1.  Returns the end point, or None if the
    path touches a corner (convex or reflex vertex) at time in (0, 1]."""
    x, y = F(S[0]), F(S[1])
    vx, vy = F(v[0]), F(v[1])
    t = F(0)
    while True:
        # next grid crossing
        cand = []
        if vx != 0:
            nx = (x.__floor__() + 1) if vx > 0 else (x.__ceil__() - 1)
            cand.append((nx - x) / vx)
        if vy != 0:
            ny = (y.__floor__() + 1) if vy > 0 else (y.__ceil__() - 1)
            cand.append((ny - y) / vy)
        dt = min(cand)
        if t + dt >= 1:
            return (x + (1 - t) * vx, y + (1 - t) * vy)
        x, y, t = x + dt * vx, y + dt * vy, t + dt
        xi, yi = x.denominator == 1, y.denominator == 1
        sx = 1 if vx > 0 else -1
        sy = 1 if vy > 0 else -1
        cx = int(x) - (1 if vx > 0 else 0) if xi else x.__floor__()   # current cell before the crossing
        cy = int(y) - (1 if vy > 0 else 0) if yi else y.__floor__()
        if xi and vx == 0:
            cx = int(x)
        if yi and vy == 0:
            cy = int(y)
        if xi and yi and vx != 0 and vy != 0:
            k = pt_kind(cs, int(x), int(y))
            if k == 'int':
                continue
            if k != 'flat':
                return None
            H, V = (cx + sx, cy) in cs, (cx, cy + sy) in cs
            if H:
                vy = -vy
            elif V:
                vx = -vx
            else:
                raise AssertionError
        elif xi and yi:
            # axis-parallel motion through a lattice point
            k = pt_kind(cs, int(x), int(y))
            if k == 'int':
                continue
            if k != 'flat':
                return None
            ahead = (cx + sx, cy) if vx != 0 else None
            # flat point on an axis-parallel path: passes along a wall or hits it head-on
            raise NotImplementedError('axis-parallel through boundary point')
        elif xi and vx != 0:
            if (cx + sx, cy) not in cs:
                vx = -vx
        elif yi and vy != 0:
            if (cx, cy + sy) not in cs:
                vy = -vy


def images(T, R):
    """Unfolded images (e1 tx + 2m, e2 ty + 2n) of T within L-inf radius R of the origin grid."""
    tx, ty = F(T[0]), F(T[1])
    for m in range(-R, R + 1):
        for n in range(-R, R + 1):
            for e1 in (1, -1):
                for e2 in (1, -1):
                    yield (e1 * tx + 2 * m, e2 * ty + 2 * n)


def lit_pair(cs, S, T, R):
    """Search an explicit billiard path S -> T among unfolded images within radius R. Returns velocity."""
    S = (F(S[0]), F(S[1]))
    T = (F(T[0]), F(T[1]))
    ims = sorted(set(images(T, R)), key=lambda im: (im[0] - S[0]) ** 2 + (im[1] - S[1]) ** 2)
    for im in ims:
        v = (im[0] - S[0], im[1] - S[1])
        if v == (0, 0) or v[0] == 0 or v[1] == 0:
            continue
        end = trace(cs, S, v)
        if end == T:
            return v
    return None
