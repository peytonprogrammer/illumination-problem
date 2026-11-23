#!/usr/bin/env python3
"""Cylinders of DP in a rational direction, labelled on the room.

Room: a set of unit cells (a, b) (a strictly simple polyomino).
M: the four-copy unfolding, one unit square per (cell, sheet). Sheet
eps = (e1, e2) uses the developing chart z = (e1 x, e2 y), as in
d3-review/surface.py. Marked points (Sigma) are the lifts of polygon vertices.

Direction (p, q) with p >= 0, q >= 1, gcd 1. Directions with other signs give
the same room picture (the deck group K of M maps them to these), and (1, 0)
is handled by transposing the room (see `labels`).

Room-level families for a direction (p, q):
  plus  family: lines q x - p y = k (k integer), open strips k < q x - p y < k+1
  minus family: lines q x + p y = k,               open strips k < q x + p y < k+1
A room point s has one DP lift per family: the plus lift (sheets (1,1),
(-1,-1), exchanged by tau) and the minus lift (sheets (1,-1), (-1,1)).

`labels(cells, p, q)` returns a Labels object with
  plus[(a,b)][k]  = DP cylinder id of the open plus strip k in cell (a,b)
  minus[(a,b)][k] = same for the minus family
  plusline[(a,b)][k]  = DP cylinder id of the plus line q x - p y = k inside
                        the open cell (None when the leaf is singular)
  minusline[(a,b)][k] = same for minus lines
  ncyl = number of DP cylinders
  area[c] = area of DP cylinder c (in unit squares of DP; total = room area * 2)
Only lines that cross the open cell are listed: for the plus family in cell
(a, b), k ranges over q a - p b - p < k < q a - p b + q; strips over
q a - p b - p <= k < q a - p b + q.
"""
from math import gcd

SHEETS = [(1, 1), (-1, 1), (1, -1), (-1, -1)]


def point_type(cells, x, y):
    ll, lr, ul, ur = ((x - 1, y - 1) in cells, (x, y - 1) in cells,
                      (x - 1, y) in cells, (x, y) in cells)
    n = ll + lr + ul + ur
    if n == 4:
        return "interior"
    if n == 0:
        return "outside"
    if n == 1:
        return "convex"
    if n == 3:
        return "reflex"
    if (ll and lr) or (ul and ur) or (ll and ul) or (lr and ur):
        return "flat"
    raise ValueError("pinch point")


class Surface:
    def __init__(self, cells):
        self.cells = frozenset(cells)
        self.sq = [(c, e) for c in sorted(self.cells) for e in SHEETS]
        self.idx = {s: i for i, s in enumerate(self.sq)}
        n = len(self.sq)
        self.r, self.u = [0] * n, [0] * n
        for i, ((a, b), (e1, e2)) in enumerate(self.sq):
            nb = (a + e1, b)
            self.r[i] = self.idx[(nb, (e1, e2))] if nb in self.cells else self.idx[((a, b), (-e1, e2))]
            nb = (a, b + e2)
            self.u[i] = self.idx[(nb, (e1, e2))] if nb in self.cells else self.idx[((a, b), (e1, -e2))]
        self.ri, self.ui = [0] * n, [0] * n
        for i in range(n):
            self.ri[self.r[i]] = i
            self.ui[self.u[i]] = i
        # marked lower-left developing corner
        self.mll = []
        for i, ((a, b), (e1, e2)) in enumerate(self.sq):
            x = a + (0 if e1 == 1 else 1)
            y = b + (0 if e2 == 1 else 1)
            self.mll.append(point_type(self.cells, x, y) in ("convex", "reflex"))


class Labels:
    pass


def _uf_find(par, a):
    while par[a] != a:
        par[a] = par[par[a]]
        a = par[a]
    return a


def m_cylinders(S, p, q):
    """Strip slots (i, j), j = 0..q-1, of M in direction (p, q), q >= 1.
    Returns (comp, ptreg, nslots): comp[(i*q+j)] = M-cylinder root of the strip
    slot; ptreg[i*q+j] = True when the leaf through bottom offset j/q of square
    i is regular (closes without meeting Sigma)."""
    n = len(S.sq)
    ns = n * q
    cyc = [-1] * ns
    nc = 0
    for t in range(ns):
        if cyc[t] >= 0:
            continue
        cur = t
        while cyc[cur] < 0:
            cyc[cur] = nc
            i, j = divmod(cur, q)
            k = (j + p) // q
            for _ in range(k):
                i = S.r[i]
            cur = S.u[i] * q + (j + p) % q
        assert cur == t
        nc += 1
    regl = [True] * nc
    for i in range(n):
        if S.mll[i]:
            regl[cyc[i * q]] = False
    par = list(range(nc))
    for i in range(n):
        for j in range(1, q):
            if regl[cyc[i * q + j]]:
                a, b = _uf_find(par, cyc[i * q + j - 1]), _uf_find(par, cyc[i * q + j])
                par[a] = b
        if regl[cyc[i * q]]:
            a, b = _uf_find(par, cyc[i * q]), _uf_find(par, cyc[S.ri[i] * q + q - 1])
            par[a] = b
    comp = [_uf_find(par, cyc[t]) for t in range(ns)]
    ptreg = [regl[cyc[t]] for t in range(ns)]
    return comp, ptreg, nc


def _slot(S, i, m, q):
    """Square i, local strip/line index m (may be negative) -> slot index."""
    while m < 0:
        i = S.ri[i]
        m += q
    return i * q + m


def labels(cells, p, q):
    cells = frozenset(cells)
    if q == 0:
        # horizontal direction: transpose the room, use (0, 1), map back.
        assert p == 1
        T = labels({(b, a) for a, b in cells}, 0, 1)
        L = Labels()
        L.p, L.q, L.ncyl, L.area = 1, 0, T.ncyl, T.area
        # original plus line k: q x - p y = -y = k  <->  transposed x' = y = -k,
        # transposed (p,q)=(0,1) plus family: x' = k'. So orig plus k = trans plus -k
        # for lines, and orig plus strip k (-y in (k,k+1), y in (-k-1,-k)) =
        # trans plus strip -k-1. Orig minus family: y = k  <-> trans minus x' = k.
        L.plus, L.minus, L.plusline, L.minusline = {}, {}, {}, {}
        for (a, b) in cells:
            tc = (b, a)
            L.plus[(a, b)] = {-k - 1: v for k, v in T.plus[tc].items()}
            L.plusline[(a, b)] = {-k: v for k, v in T.plusline[tc].items()}
            L.minus[(a, b)] = dict(T.minus[tc])
            L.minusline[(a, b)] = dict(T.minusline[tc])
        return L
    assert q >= 1 and p >= 0 and gcd(p, q) == 1
    S = Surface(cells)
    comp, ptreg, nstrips = m_cylinders(S, p, q)
    # DP cylinders: merge tau-images (same room strip, sheets eps and -eps)
    roots = sorted(set(comp))
    rid = {r: t for t, r in enumerate(roots)}
    par = list(range(len(roots)))

    def merge(x, y):
        a, b = _uf_find(par, rid[comp[x]]), _uf_find(par, rid[comp[y]])
        par[a] = b

    def sidx(cell, sheet):
        return S.idx[(cell, sheet)]

    L = Labels()
    L.p, L.q = p, q
    plus_slots, minus_slots, plusline_slots, minusline_slots = {}, {}, {}, {}
    for (a, b) in cells:
        k0 = q * a - p * b
        ps, ms, pl, ml = {}, {}, {}, {}
        for k in range(k0 - p, k0 + q):
            s1 = _slot(S, sidx((a, b), (1, 1)), k - k0, q)
            s4 = _slot(S, sidx((a, b), (-1, -1)), q * (a + 1) - p * (b + 1) - k - 1, q)
            merge(s1, s4)
            ps[k] = s1
        m0 = q * a + p * b
        for k in range(m0, m0 + p + q):
            s3 = _slot(S, sidx((a, b), (1, -1)), k - q * a - p * (b + 1), q)
            s2 = _slot(S, sidx((a, b), (-1, 1)), q * (a + 1) + p * b - k - 1, q)
            merge(s3, s2)
            ms[k] = s3
        # lines strictly inside the cell (as point slots: leaf through the
        # bottom offset of the given local index)
        for k in range(k0 - p + 1, k0 + q):
            pl[k] = _slot(S, sidx((a, b), (1, 1)), k - k0, q)
        for k in range(m0 + 1, m0 + p + q):
            ml[k] = _slot(S, sidx((a, b), (1, -1)), k - q * a - p * (b + 1), q)
        plus_slots[(a, b)], minus_slots[(a, b)] = ps, ms
        plusline_slots[(a, b)], minusline_slots[(a, b)] = pl, ml
    dproots = sorted({_uf_find(par, t) for t in range(len(roots))})
    did = {r: t for t, r in enumerate(dproots)}
    L.ncyl = len(dproots)
    L.nmcyl = len(roots)
    L.nstrips = nstrips

    def lab(slot):
        return did[_uf_find(par, rid[comp[slot]])]

    def linelab(slot):
        # a line point slot: regular leaf -> label of the strip just above it
        return lab(slot) if ptreg[slot] else None

    L.plus = {c: {k: lab(s) for k, s in d.items()} for c, d in plus_slots.items()}
    L.minus = {c: {k: lab(s) for k, s in d.items()} for c, d in minus_slots.items()}
    L.plusline = {c: {k: linelab(s) for k, s in d.items()} for c, d in plusline_slots.items()}
    L.minusline = {c: {k: linelab(s) for k, s in d.items()} for c, d in minusline_slots.items()}
    # areas: each M strip slot carries area 1/q of ... use room faces instead:
    # area of DP cylinder = sum over cells of (area of plus strips + minus strips)
    from fractions import Fraction as Fr
    area = [Fr(0)] * L.ncyl
    for (a, b) in cells:
        k0 = q * a - p * b
        for k, c in L.plus[(a, b)].items():
            area[c] += strip_area(k - k0, p, q)
        m0 = q * a + p * b
        for k, c in L.minus[(a, b)].items():
            area[c] += strip_area(k - m0 - p, p, q)
    L.area = area
    return L


def strip_area(m, p, q):
    """Area of {(x,y) in [0,1]^2 : m < q x - p y < m+1}, exact."""
    from fractions import Fraction as Fr

    def F(t):  # area of {q x - p y < t} in the unit square
        # integrate over x: y > (q x - t)/p  (p>0), length 1 - clamp((qx-t)/p)
        if p == 0:
            # q x < t
            return Fr(min(max(Fr(t, q), 0), 1))
        # piecewise linear integrand; integrate exactly by breakpoints
        pts = sorted({Fr(0), Fr(1)} | {x for x in (Fr(t, q), Fr(t + p, q)) if 0 < x < 1})
        tot = Fr(0)
        for x0, x1 in zip(pts, pts[1:]):
            xm = (x0 + x1) / 2

            def g(x):
                y = (q * x - t) / Fr(p)
                return 1 - min(max(y, 0), 1)
            # g linear on [x0, x1]
            tot += (g(x0) + g(x1)) / 2 * (x1 - x0)
        return tot
    return F(m + 1) - F(m)
