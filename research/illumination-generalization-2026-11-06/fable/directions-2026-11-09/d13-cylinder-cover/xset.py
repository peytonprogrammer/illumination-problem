#!/usr/bin/env python3
"""Exact candidate set X' (Theorem B' in theory.md) for one room.

For a direction theta = (p, q), p, q >= 1, and a room point s, Lambda(s) is
the set of DP cylinders that contain a lift of s in their open interior.
Lambda(s) is COVERING when the closures of its cylinders project onto the
room. Bad_theta = { s : Lambda(s) not covering }. Theorem B': every endpoint
of a dark pair lies in X' = intersection of Bad_theta over the directions used.

Bad_theta, intersected with a closed cell, is the union of
  - closed faces (i, j) whose label pair {plus[i], minus[j]} is not covering;
  - closed sub-segments of SINGULAR lines inside one strip of the other
    family whose label is not covering by itself;
  - crossing points of two singular lines (Lambda empty);
  - interior lattice points of the cell with non-covering Lambda.
(Regular lines carry the label of both neighbouring strips, so they add
nothing beyond the closures of the faces.) See theory.md, Lemma 3.

Pieces are closed convex sets with rational vertices: points, segments,
polygons. All arithmetic is Fraction.
"""
from fractions import Fraction as Fr
from math import gcd

from cyl import labels, point_type
from cover import faces

# ---------------------------------------------------------------- geometry


def _cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def normalize(V):
    """Canonical closed convex set from a vertex list: () empty, (P,) point,
    (A, B) segment (A < B), or a CCW polygon starting at its min vertex."""
    if not V:
        return ()
    U = sorted(set(V))
    if len(U) == 1:
        return (U[0],)
    a, b = U[0], U[-1]
    if all(_cross(a, b, c) == 0 for c in U):
        return (a, b)   # collinear: lexicographic extremes are the ends
    # convex hull (monotone chain) to drop collinear / duplicate points
    lower, upper = [], []
    for P in U:
        while len(lower) >= 2 and _cross(lower[-2], lower[-1], P) <= 0:
            lower.pop()
        lower.append(P)
    for P in reversed(U):
        while len(upper) >= 2 and _cross(upper[-2], upper[-1], P) <= 0:
            upper.pop()
        upper.append(P)
    return tuple(lower[:-1] + upper[:-1])


def clip(V, a, b, c):
    """Intersect closed convex set (vertex tuple) with a x + b y <= c."""
    n = len(V)
    if n == 0:
        return ()
    if n == 1:
        P = V[0]
        return V if a * P[0] + b * P[1] <= c else ()
    out = []
    for i in range(n):
        P, Q = V[i], V[(i + 1) % n]
        fp = a * P[0] + b * P[1] - c
        fq = a * Q[0] + b * Q[1] - c
        if fp <= 0:
            out.append(P)
        if (fp < 0 < fq) or (fq < 0 < fp):
            t = fp / (fp - fq)
            out.append((P[0] + t * (Q[0] - P[0]), P[1] + t * (Q[1] - P[1])))
    return normalize(out)


def clip_all(V, hps):
    for a, b, c in hps:
        V = clip(V, a, b, c)
        if not V:
            return ()
    return V


def contains(B, P):
    """Point P in closed convex set B."""
    n = len(B)
    if n == 1:
        return B[0] == P
    if n == 2:
        A, C = B
        if _cross(A, C, P) != 0:
            return False
        return min(A[0], C[0]) <= P[0] <= max(A[0], C[0]) and min(A[1], C[1]) <= P[1] <= max(A[1], C[1])
    return all(_cross(B[i], B[(i + 1) % n], P) >= 0 for i in range(n))


def subset(A, B):
    return all(contains(B, P) for P in A)


def bbox(V):
    xs = [P[0] for P in V]
    ys = [P[1] for P in V]
    return min(xs), min(ys), max(xs), max(ys)


def cell_hps(a, b):
    return [(-1, 0, -a), (1, 0, a + 1), (0, -1, -b), (0, 1, b + 1)]


def band(alpha, beta, lo, hi):
    """lo <= alpha x + beta y <= hi"""
    return [(-alpha, -beta, -lo), (alpha, beta, hi)]


def prune(pieces):
    """Drop duplicates and pieces contained in another piece."""
    uniq = list(dict.fromkeys(pieces))
    uniq.sort(key=lambda V: -len(V) if len(V) > 2 else -len(V))
    keep = []
    boxes = []
    for V in sorted(uniq, key=lambda V: (-(len(V) >= 3), -len(V))):
        bx = bbox(V)
        dominated = False
        for W, bw in zip(keep, boxes):
            if bw[0] <= bx[0] and bw[1] <= bx[1] and bx[2] <= bw[2] and bx[3] <= bw[3] and subset(V, W):
                dominated = True
                break
        if not dominated:
            keep.append(V)
            boxes.append(bx)
    return keep


# ---------------------------------------------------------------- bad sets


class DirData:
    """Labels, covering table, and bad pieces of one direction."""

    def __init__(self, cells, p, q):
        self.p, self.q = p, q
        L = labels(cells, p, q)
        self.L = L
        self.cells = cells
        nc = L.ncyl
        # covering table for label sets of size <= 2
        fl = {}
        for c in cells:
            fl[c] = list(faces(c[0], c[1], p, q))
        self.facelist = fl

        def covers(S):
            return all(L.plus[c][i] in S or L.minus[c][j] in S for c in cells for (i, j) in fl[c])
        self.cov = {}
        for d1 in range(nc):
            for d2 in range(d1, nc):
                self.cov[frozenset((d1, d2))] = covers({d1, d2})
        self.cov[frozenset()] = False

    def covering(self, S):
        S = frozenset(x for x in S if x is not None)
        return self.cov[S]

    def lattice_lambda(self, x0, y0):
        L, p, q = self.L, self.p, self.q
        k = q * x0 - p * y0
        m = q * x0 + p * y0
        c = (x0, y0) if (x0, y0) in self.cells else (x0 - 1, y0 - 1)
        lp = L.plusline[c][k]
        c = (x0 - 1, y0) if (x0 - 1, y0) in self.cells else (x0, y0 - 1)
        lm = L.minusline[c][m]
        return {lp, lm}

    def bad_pieces(self, c):
        """Closed convex pieces whose union is Bad_theta intersected with the closed cell c."""
        L, p, q = self.L, self.p, self.q
        a, b = c
        ch = cell_hps(a, b)
        sq = normalize([(Fr(a), Fr(b)), (Fr(a + 1), Fr(b)), (Fr(a + 1), Fr(b + 1)), (Fr(a), Fr(b + 1))])
        out = []
        for (i, j) in self.facelist[c]:
            if not self.covering({L.plus[c][i], L.minus[c][j]}):
                out.append(band(q, -p, i, i + 1) + band(q, p, j, j + 1) + ch)
        m0 = q * a + p * b
        k0 = q * a - p * b
        for k, lab in L.plusline[c].items():
            if lab is not None:
                continue
            for j in range(m0, m0 + p + q):
                if not self.covering({L.minus[c][j]}):
                    out.append(band(q, -p, k, k) + band(q, p, j, j + 1) + ch)
        for k, lab in L.minusline[c].items():
            if lab is not None:
                continue
            for i in range(k0 - p, k0 + q):
                if not self.covering({L.plus[c][i]}):
                    out.append(band(q, p, k, k) + band(q, -p, i, i + 1) + ch)
        pts = []
        for k, lab in L.plusline[c].items():
            if lab is not None:
                continue
            for m, lab2 in L.minusline[c].items():
                if lab2 is not None:
                    continue
                P = (Fr(k + m, 2 * q), Fr(m - k, 2 * p))
                if a <= P[0] <= a + 1 and b <= P[1] <= b + 1:
                    pts.append(P)
        for (x0, y0) in ((a, b), (a + 1, b), (a, b + 1), (a + 1, b + 1)):
            if point_type(self.cells, x0, y0) == "interior":
                if not self.covering(self.lattice_lambda(x0, y0)):
                    pts.append((Fr(x0), Fr(y0)))
        res = []
        for hps in out:
            V = clip_all(sq, hps)
            if V:
                res.append(V)
        res += [(P,) for P in pts]
        return res


def directions(B):
    ds = [(p, q) for p in range(1, B + 1) for q in range(1, B + 1) if gcd(p, q) == 1]
    ds.sort(key=lambda d: (d[0] + d[1], d))
    return ds


def candidate_set(cells, dirs, verbose=False, maxpieces=200000):
    """Return (pieces by cell, list of directions used, DirData list)."""
    cells = frozenset(cells)
    X = {c: [normalize([(Fr(c[0]), Fr(c[1])), (Fr(c[0] + 1), Fr(c[1])),
                        (Fr(c[0] + 1), Fr(c[1] + 1)), (Fr(c[0]), Fr(c[1] + 1))])] for c in cells}
    used = []
    for (p, q) in dirs:
        dd = DirData(cells, p, q)
        changed = False
        total = 0
        for c in cells:
            if not X[c]:
                continue
            bp = dd.bad_pieces(c)
            bb = [bbox(V) for V in bp]
            new = []
            for V in X[c]:
                bv = bbox(V)
                for W, bw in zip(bp, bb):
                    if bw[2] < bv[0] or bv[2] < bw[0] or bw[3] < bv[1] or bv[3] < bw[1]:
                        continue
                    I = intersect(V, W)
                    if I:
                        new.append(I)
            new = prune(new)
            if new != X[c]:
                changed = True
            X[c] = new
            total += len(new)
        if changed:
            used.append((p, q))
        if verbose:
            dims = summary(X)
            print(f"  dir {p},{q}: ncyl {dd.L.ncyl} pieces {total} dims {dims}", flush=True)
        if total > maxpieces:
            raise RuntimeError("too many pieces")
        if max_dim(X) == 0:
            break
    return X, used


def intersect(V, W):
    """Intersection of two closed convex sets given by vertex tuples."""
    if len(W) == 1:
        return W if contains(V, W[0]) else ()
    if len(V) == 1:
        return V if contains(W, V[0]) else ()
    # clip V by the half-planes (or line) of W
    if len(W) == 2:
        A, B = W
        a, b = B[1] - A[1], A[0] - B[0]
        c = a * A[0] + b * A[1]
        hps = [(a, b, c), (-a, -b, -c)]
        # and the extent along the segment
        dx, dy = B[0] - A[0], B[1] - A[1]
        hps += [(-dx, -dy, -(dx * A[0] + dy * A[1])), (dx, dy, dx * B[0] + dy * B[1])]
        return clip_all(V, hps)
    hps = []
    n = len(W)
    for i in range(n):
        A, B = W[i], W[(i + 1) % n]
        # inside is left of A->B (CCW): cross(A,B,P) >= 0
        # cross = (B-A) x (P-A) = (Bx-Ax)(Py-Ay) - (By-Ay)(Px-Ax) >= 0
        # -> (By-Ay) Px - (Bx-Ax) Py <= (By-Ay) Ax - (Bx-Ax) Ay
        a, b = B[1] - A[1], -(B[0] - A[0])
        hps.append((a, b, a * A[0] + b * A[1]))
    return clip_all(V, hps)


def summary(X):
    d = [0, 0, 0]
    for c, ps in X.items():
        for V in ps:
            d[min(len(V), 3) - 1] += 1
    return d


def max_dim(X):
    m = -1
    for ps in X.values():
        for V in ps:
            m = max(m, min(len(V), 3) - 1)
    return m


def interior_pieces(cells, X):
    """Drop pieces that lie in the boundary of the room. Returns a flat,
    deduplicated list of pieces that meet the interior."""
    out = []
    for c, ps in X.items():
        for V in ps:
            if len(V) == 1:
                P = V[0]
                if is_interior(cells, P):
                    out.append(V)
            elif len(V) == 2:
                M = ((V[0][0] + V[1][0]) / 2, (V[0][1] + V[1][1]) / 2)
                if is_interior(cells, M):
                    out.append(V)
                # a segment on a wall has its midpoint on the wall
            else:
                out.append(V)
    return prune(out)


def is_interior(cells, P):
    x, y = P
    if x.denominator == 1 and y.denominator == 1:
        return point_type(cells, int(x), int(y)) == "interior"
    if x.denominator == 1:
        X0 = int(x)
        Y0 = y.numerator // y.denominator
        return (X0 - 1, Y0) in cells and (X0, Y0) in cells
    if y.denominator == 1:
        Y0 = int(y)
        X0 = x.numerator // x.denominator
        return (X0, Y0 - 1) in cells and (X0, Y0) in cells
    return (x.numerator // x.denominator, y.numerator // y.denominator) in cells
