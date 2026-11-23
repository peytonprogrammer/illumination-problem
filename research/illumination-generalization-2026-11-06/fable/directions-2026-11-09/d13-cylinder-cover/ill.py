#!/usr/bin/env python3
"""Accumulated cylinder certificate (Theorem C in theory.md), exact.

For a room point s and a direction theta, Lambda_theta(s) = DP cylinders that
contain a lift of s in their open interior; K_D = projection to the room of
the closure of D. Lemma A' gives: s illuminates every interior point of
  Ill(s) = union over theta in Theta, D in Lambda_theta(s) of K_D.
s is DONE when Ill(s) contains the whole room.

The room is cut into relatively open cells (faces, open edges, vertices) by
the singular lines of all directions processed so far, but only cells that are
not yet done are kept and refined. Each live cell carries Q, a list of closed
convex polygons whose union contains the closure of P \\ Ill(s) for every s in
the cell (Ill is constant on a cell). A cell is done when Q has no 2D piece.

Cells are closed convex vertex tuples; the cell itself is the relative
interior. Arithmetic is Fraction.
"""
from fractions import Fraction as Fr
from math import floor

from cyl import labels, point_type
from cover import faces
from xset import normalize, clip, clip_all, cell_hps, band, prune, bbox, intersect


def floorfr(x):
    return x.numerator // x.denominator


class Dir:
    def __init__(self, cells, p, q):
        self.p, self.q = p, q
        self.cells = cells
        self.L = labels(cells, p, q)
        self.fl = {c: list(faces(c[0], c[1], p, q)) for c in cells}
        # closed face polygons per room cell, with labels
        self.facepolys = {}
        for c in cells:
            a, b = c
            sq = square(a, b)
            lst = []
            for (i, j) in self.fl[c]:
                V = clip_all(sq, band(q, -p, i, i + 1) + band(q, p, j, j + 1))
                if len(V) >= 3:
                    lst.append((V, self.L.plus[c][i], self.L.minus[c][j], bbox(V)))
            self.facepolys[c] = lst

    def _cells_with(self, P):
        x, y = P
        xs = [floorfr(x)] if x.denominator != 1 else [int(x) - 1, int(x)]
        ys = [floorfr(y)] if y.denominator != 1 else [int(y) - 1, int(y)]
        return [(a, b) for a in xs for b in ys if (a, b) in self.cells]

    def lam(self, P):
        """Lambda(P) as a set of cylinder ids; P an interior point."""
        p, q, L = self.p, self.q, self.L
        u = q * P[0] - p * P[1]
        v = q * P[0] + p * P[1]
        cs = self._cells_with(P)
        out = set()
        if u.denominator != 1:
            k = floorfr(u)
            out.add(L.plus[cs[0]][k])
        else:
            k = int(u)
            labs = [L.plusline[c][k] for c in cs if k in L.plusline[c]]
            assert labs, (P, "plus line not found")
            if labs[0] is not None:
                out.add(labs[0])
        if v.denominator != 1:
            k = floorfr(v)
            out.add(L.minus[cs[0]][k])
        else:
            k = int(v)
            labs = [L.minusline[c][k] for c in cs if k in L.minusline[c]]
            assert labs, (P, "minus line not found")
            if labs[0] is not None:
                out.add(labs[0])
        return out

    def singular_lines(self, c):
        """Singular lines meeting the open cell c: list of (alpha, beta, k)
        meaning alpha x + beta y = k."""
        p, q, L = self.p, self.q, self.L
        out = [(q, -p, k) for k, lab in L.plusline[c].items() if lab is None]
        out += [(q, p, k) for k, lab in L.minusline[c].items() if lab is None]
        return out


def square(a, b):
    return normalize([(Fr(a), Fr(b)), (Fr(a + 1), Fr(b)), (Fr(a + 1), Fr(b + 1)), (Fr(a), Fr(b + 1))])


def rep_point(V):
    n = len(V)
    return (sum(P[0] for P in V) / n, sum(P[1] for P in V) / n)


def split(V, lines):
    """Split the relatively open cell relint(V) by lines; returns list of
    closed vertex tuples whose relative interiors partition relint(V)."""
    cellsl = [V]
    for (al, be, k) in lines:
        nxt = []
        for W in cellsl:
            vals = [al * P[0] + be * P[1] - k for P in W]
            if len(W) == 1 or min(vals) >= 0 or max(vals) <= 0:
                # line does not cross the relative interior (it may contain
                # W or touch its boundary)
                nxt.append(W)
                continue
            lo = clip(W, al, be, k)
            hi = clip(W, -al, -be, -k)
            mid = clip_all(W, [(al, be, k), (-al, -be, -k)])
            nxt += [lo, hi, mid]
        cellsl = nxt
    return cellsl


def subtract(Q, D, lamset):
    """Q minus union of K_D for D in lamset: keep closed faces with both labels
    outside lamset."""
    out = []
    for (c, V) in Q:
        bv = bbox(V)
        for (F, lp, lm, bf) in D.facepolys[c]:
            if lp in lamset or lm in lamset:
                continue
            if bf[2] <= bv[0] or bv[2] <= bf[0] or bf[3] <= bv[1] or bv[3] <= bf[1]:
                continue
            I = intersect(V, F)
            if len(I) >= 3:
                out.append((c, I))
    return out


def prune_q(Q):
    by = {}
    for c, V in Q:
        by.setdefault(c, []).append(V)
    out = []
    for c, lst in by.items():
        for V in prune(lst):
            out.append((c, V))
    return out


def initial_cells(cells):
    out = []
    for (a, b) in sorted(cells):
        out.append(((a, b), square(a, b)))
        if (a + 1, b) in cells:
            out.append(((a, b), normalize([(Fr(a + 1), Fr(b)), (Fr(a + 1), Fr(b + 1))])))
        if (a, b + 1) in cells:
            out.append(((a, b), normalize([(Fr(a), Fr(b + 1)), (Fr(a + 1), Fr(b + 1))])))
        if point_type(cells, a + 1, b + 1) == "interior":
            out.append(((a, b), ((Fr(a + 1), Fr(b + 1)),)))
    return out


def run(cells, dirs, verbose=False, maxcells=300000):
    """Returns the list of live (room cell, cell, Q) after all directions, and
    stats."""
    cells = frozenset(cells)
    Q0 = [(c, square(*c)) for c in sorted(cells)]
    live = [(c, V, Q0) for c, V in initial_cells(cells)]
    hist = []
    for (p, q) in dirs:
        D = Dir(cells, p, q)
        nl = []
        for (c, V, Q) in live:
            for W in split(V, D.singular_lines(c)):
                lam = D.lam(rep_point(W))
                Qn = prune_q(subtract(Q, D, lam)) if lam else Q
                if Qn:
                    nl.append((c, W, Qn))
        live = nl
        dims = [0, 0, 0]
        for (_, W, _) in live:
            dims[min(len(W), 3) - 1] += 1
        hist.append(((p, q), D.L.ncyl, len(live), dims))
        if verbose:
            print(f"  dir {p},{q}: ncyl {D.L.ncyl} live {len(live)} dims {dims}", flush=True)
        if len(live) > maxcells:
            raise RuntimeError("too many live cells")
        if not live or dims[1] == dims[2] == 0:
            pass
    return live, hist
