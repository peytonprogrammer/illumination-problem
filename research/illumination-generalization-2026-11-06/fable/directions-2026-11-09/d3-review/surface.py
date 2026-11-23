#!/usr/bin/env python3
"""Reviewer's independent model of the unfolding M of an orthogonal lattice room.

Written without reading or importing the author's tracer. M is built as a
square-tiled surface: one unit square per (room cell, sheet eps in {+-1}^2),
with right/up neighbour permutations. All arithmetic is integer or Fraction.

Conventions.
- A room is a set of unit cells, named by lower-left corner (a, b).
- Square (c, eps). In sheet eps the developing chart is z = eps * x, so moving
  in developing +x means moving in room direction eps1 * x.
- The lower-left developing corner of square ((a, b), eps) is the room point
  (a + (1 - eps1)/2, b + (1 - eps2)/2).
- A lattice point of M is MARKED when its room point is a polygon vertex
  (convex or reflex). Flat boundary lattice points and interior lattice points
  are unmarked (regular, cone angle 2 pi).
"""
from fractions import Fraction as Fr

SHEETS = [(1, 1), (-1, 1), (1, -1), (-1, -1)]


def q22_cells():
    """22-wall room exactly as in manuscript.tex: P0 = P, P1 = (x,-y), P2 = (4-x,-y)."""
    P = [(-1, -1), (0, -1), (0, -2), (1, -2), (1, -3)]
    out = set(P)
    out |= {(a, -b - 1) for a, b in P}          # (x,y) -> (x,-y)
    out |= {(3 - a, -b - 1) for a, b in P}      # (x,y) -> (4-x,-y)
    assert len(out) == 15
    return out


def point_type(cells, x, y):
    """Classify the room lattice point (x, y)."""
    ll, lr, ul, ur = ((x - 1, y - 1) in cells, (x, y - 1) in cells,
                      (x - 1, y) in cells, (x, y) in cells)
    n = ll + lr + ul + ur
    if n == 4:
        return "interior"
    if n == 0:
        return "outside"
    if n == 2 and ((ll and lr) or (ul and ur)):
        return "flat-h"   # on a horizontal wall
    if n == 2 and ((ll and ul) or (lr and ur)):
        return "flat-v"   # on a vertical wall
    if n == 1:
        return "convex"
    if n == 3:
        return "reflex"
    raise ValueError("pinch point: room not simple")


def boundary_cycle(cells):
    """Return the polygon vertices (turning points) in boundary order."""
    pts = {(x, y) for a, b in cells for x in (a, a + 1) for y in (b, b + 1)}
    verts = {p for p in pts if point_type(cells, *p) in ("convex", "reflex")}
    # unit boundary edges
    edges = set()
    for a, b in cells:
        if (a - 1, b) not in cells: edges.add(frozenset({(a, b), (a, b + 1)}))
        if (a + 1, b) not in cells: edges.add(frozenset({(a + 1, b), (a + 1, b + 1)}))
        if (a, b - 1) not in cells: edges.add(frozenset({(a, b), (a + 1, b)}))
        if (a, b + 1) not in cells: edges.add(frozenset({(a, b + 1), (a + 1, b + 1)}))
    adj = {}
    for e in edges:
        u, v = tuple(e)
        adj.setdefault(u, []).append(v)
        adj.setdefault(v, []).append(u)
    assert all(len(v) == 2 for v in adj.values()), "boundary not a simple cycle"
    start = min(verts)
    cyc, prev, cur = [start], None, start
    while True:
        nxt = [v for v in adj[cur] if v != prev][0] if prev else adj[cur][0]
        prev, cur = cur, nxt
        if cur == start:
            break
        cyc.append(cur)
    assert len(cyc) == len(adj), "boundary has more than one component"
    return [p for p in cyc if p in verts], verts


class Surface:
    def __init__(self, cells):
        self.cells = set(cells)
        self.sq = [(c, e) for c in sorted(self.cells) for e in SHEETS]
        self.idx = {s: i for i, s in enumerate(self.sq)}
        n = len(self.sq)
        self.r = [0] * n
        self.u = [0] * n
        for i, ((a, b), (e1, e2)) in enumerate(self.sq):
            nb = (a + e1, b)
            self.r[i] = self.idx[(nb, (e1, e2))] if nb in self.cells else self.idx[((a, b), (-e1, e2))]
            nb = (a, b + e2)
            self.u[i] = self.idx[(nb, (e1, e2))] if nb in self.cells else self.idx[((a, b), (e1, -e2))]
        self.ri = [0] * n
        self.ui = [0] * n
        for i in range(n):
            self.ri[self.r[i]] = i
            self.ui[self.u[i]] = i
        assert sorted(self.r) == list(range(n)) and sorted(self.u) == list(range(n))

    def corner_room_point(self, i, ox, oy):
        """Room point of the developing corner (ox, oy) in {0,1}^2 of square i."""
        (a, b), (e1, e2) = self.sq[i]
        return (a + (ox if e1 == 1 else 1 - ox), b + (oy if e2 == 1 else 1 - oy))

    def marked_ll(self, i):
        return point_type(self.cells, *self.corner_room_point(i, 0, 0)) in ("convex", "reflex")

    def room_point(self, i, off):
        (a, b), (e1, e2) = self.sq[i]
        return (a + (off[0] if e1 == 1 else 1 - off[0]), b + (off[1] if e2 == 1 else 1 - off[1]))

    # ---- leaves in direction (p, q), p, q >= 1 -------------------------------
    def step(self, p, q, i, t):
        """From bottom edge of square i at offset t in [0,1), follow direction
        (p,q) to the next bottom-edge crossing. Returns (j, t2, through_corner)."""
        w = t + Fr(p, q)
        k = w.numerator // w.denominator
        j = i
        for _ in range(k):
            j = self.r[j]
        j = self.u[j]
        t2 = w - k
        return j, t2, (t2 == 0)

    def leaf_regular(self, p, q, i, t):
        """Trace the leaf through (square i, bottom offset t). True when it
        closes without meeting a marked point."""
        if t == 0 and self.marked_ll(i):
            return False
        j, s = i, t
        for _ in range(4 * len(self.sq) * (p + q) + 10):
            j, s, corner = self.step(p, q, j, s)
            if corner and self.marked_ll(j):
                return False
            if (j, s) == (i, t):
                return True
        raise RuntimeError("leaf did not close")

    def cylinders(self, p, q):
        """Count cylinders of M (marked set = polygon-vertex lifts) in direction
        (p,q), p,q >= 1 coprime, by strips between integer leaves."""
        n = len(self.sq)
        # strip permutation on slots (square, j), j = 0..q-1
        def nxt(i, j):
            k = (j + p) // q
            for _ in range(k):
                i = self.r[i]
            return self.u[i], (j + p) % q
        strip = {}
        nstrips = 0
        for i in range(n):
            for j in range(q):
                if (i, j) in strip:
                    continue
                cur = (i, j)
                while cur not in strip:
                    strip[cur] = nstrips
                    cur = nxt(*cur)
                assert cur == (i, j)
                nstrips += 1
        parent = list(range(nstrips))

        def find(a):
            while parent[a] != a:
                parent[a] = parent[parent[a]]
                a = parent[a]
            return a
        regular_int_leaves = set()
        for i in range(n):
            # non-lattice integer-leaf crossings on the bottom edge
            for j in range(1, q):
                if self.leaf_regular(p, q, i, Fr(j, q)):
                    parent[find(strip[(i, j - 1)])] = find(strip[(i, j)])
            # crossing at the lower-left lattice corner
            if self.leaf_regular(p, q, i, Fr(0)):
                parent[find(strip[(i, 0)])] = find(strip[(self.ri[i], q - 1)])
        comps = len({find(a) for a in range(nstrips)})
        return comps, nstrips

    # ---- straight segments in M (any direction) ------------------------------
    def segment(self, s, d):
        """Develop the segment z(l) = s + l*d, 0 < l <= 1, from the lift of room
        point s in sheet (1,1). Returns (endpoint room point, ok, events) where ok
        is False when the open segment or endpoint meets a marked point.
        Axis-parallel d is not supported (callers skip it)."""
        dx, dy = d
        assert dx != 0 and dy != 0
        sx = 1 if dx > 0 else -1
        sy = 1 if dy > 0 else -1
        # developing square containing s + small*d (sheet (1,1): dev = room)
        X = s[0].numerator // s[0].denominator
        Y = s[1].numerator // s[1].denominator
        if s[0].denominator == 1 and dx < 0: X -= 1
        if s[1].denominator == 1 and dy < 0: Y -= 1
        if (X, Y) not in self.cells:
            return None, False, ["start square outside room"]
        i = self.idx[((X, Y), (1, 1))]
        lam = Fr(0)
        events = []
        while True:
            # next vertical / horizontal grid crossing
            xn = X + 1 if dx > 0 else X
            yn = Y + 1 if dy > 0 else Y
            lx = (xn - s[0]) / dx
            ly = (yn - s[1]) / dy
            ln = min(lx, ly)
            if ln >= 1:
                end = (s[0] + dx, s[1] + dy)
                off = (end[0] - X, end[1] - Y)
                rp = self.room_point(i, off)
                if off[0] in (0, 1) and off[1] in (0, 1):
                    ox, oy = int(off[0]), int(off[1])
                    if point_type(self.cells, *self.corner_room_point(i, ox, oy)) in ("convex", "reflex"):
                        return rp, False, events + ["ends at marked point"]
                return rp, True, events
            if lx == ly:
                ox = 1 if dx > 0 else 0
                oy = 1 if dy > 0 else 0
                rp = self.corner_room_point(i, ox, oy)
                ty = point_type(self.cells, *rp)
                if ty in ("convex", "reflex"):
                    return None, False, events + [f"hits corner {rp}"]
                events.append(("lattice", rp, ty))
                i = (self.r if dx > 0 else self.ri)[i]
                i = (self.u if dy > 0 else self.ui)[i]
                X += sx
                Y += sy
            elif lx < ly:
                i = (self.r if dx > 0 else self.ri)[i]
                X += sx
            else:
                i = (self.u if dy > 0 else self.ui)[i]
                Y += sy
            lam = ln
