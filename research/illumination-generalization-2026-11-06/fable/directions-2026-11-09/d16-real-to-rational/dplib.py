#!/usr/bin/env python3
"""DP-level helpers shared by validate.py and gridcheck.py.

A room point S has two DP lifts: S+ (sheets (1,1), (-1,-1)) and S- (sheets
(1,-1), (-1,1)). For a direction (p, q) the plus label of S is the DP cylinder
through S+ and the minus label is the DP cylinder through S- (cyl.labels).

Class "par" is the DP pair (S+, T+); class "cross" is (S+, T-).
"""
from fractions import Fraction as Fr
from math import floor, gcd, lcm

from cyl import labels, point_type
from shoot import MSurf, images, m_hits, room_hits


def read_rooms(path):
    rooms = []
    for line in open(path):
        tok = line.split()
        if not tok or tok[0].startswith("#"):
            continue
        if tok[0][0].isalpha():
            tok = tok[1:]
        v = list(map(int, tok[2:]))
        rooms.append(frozenset((v[2 * k], v[2 * k + 1]) for k in range(len(v) // 2)))
    return rooms


def closed_cells(cells, P):
    """Cells whose closed unit square contains P."""
    x, y = P
    xs = [floor(x) - 1, floor(x)] if x == floor(x) else [floor(x)]
    ys = [floor(y) - 1, floor(y)] if y == floor(y) else [floor(y)]
    return [(a, b) for a in xs for b in ys if (a, b) in cells]


def in_room(cells, P):
    return bool(closed_cells(cells, P))


def is_interior(cells, P):
    x, y = P
    nx = 2 if x == floor(x) else 1
    ny = 2 if y == floor(y) else 1
    return len(closed_cells(cells, P)) == nx * ny


def is_vertex(cells, P):
    x, y = P
    return x == floor(x) and y == floor(y) and point_type(cells, int(x), int(y)) in ("convex", "reflex")


def twist_periods(cells):
    """(Lambda_h, Lambda_v): lcm of 2 * (run length) over rows and columns."""
    rows, cols = set(), set()
    for (a, b) in cells:
        l = a
        while (l - 1, b) in cells:
            l -= 1
        r = a
        while (r + 1, b) in cells:
            r += 1
        rows.add(2 * (r - l + 1))
        l = b
        while (a, l - 1) in cells:
            l -= 1
        r = b
        while (a, r + 1) in cells:
            r += 1
        cols.add(2 * (r - l + 1))
    return lcm(*rows), lcm(*cols)


def directions(B):
    d = [(p, q) for p in range(1, B + 1) for q in range(1, B + 1) if gcd(p, q) == 1]
    d.sort(key=lambda t: (t[0] + t[1], t[0], t[1]))
    return d


class Cert:
    """Cylinder certificates for one room, directions 1 <= p, q <= B."""

    def __init__(self, cells, B):
        self.cells = cells
        self.dirs = directions(B)
        self.L = {}

    def lab(self, d):
        if d not in self.L:
            self.L[d] = labels(self.cells, d[0], d[1])
        return self.L[d]

    def source_labels(self, d, P):
        """(plus label, minus label) of the leaves through P+ and P-; None when singular."""
        L = self.lab(d)
        p, q = d
        cs = closed_cells(self.cells, P)
        out = []
        for fam, val in ((0, q * P[0] - p * P[1]), (1, q * P[0] + p * P[1])):
            strip, line = (L.plus, L.plusline) if fam == 0 else (L.minus, L.minusline)
            found = set()
            if val != floor(val):
                for c in cs:
                    if floor(val) in strip[c]:
                        found.add(strip[c][floor(val)])
            else:
                for c in cs:
                    if int(val) in line[c]:
                        found.add(line[c][int(val)])
            assert len(found) == 1, (d, P, fam, found)
            out.append(found.pop())
        return tuple(out)

    def target_labels(self, d, P):
        """Sets of plus and minus labels over the closed faces that contain P."""
        L = self.lab(d)
        p, q = d
        cs = closed_cells(self.cells, P)
        out = []
        for fam, val in ((0, q * P[0] - p * P[1]), (1, q * P[0] + p * P[1])):
            strip = L.plus if fam == 0 else L.minus
            ks = [floor(val)] if val != floor(val) else [int(val) - 1, int(val)]
            out.append({strip[c][k] for c in cs for k in ks if k in strip[c]})
        return tuple(out)

    def one_sided(self, S, T, cls):
        """First direction whose cylinder through S+ has T+ (par) or T- (cross) in its closure."""
        for d in self.dirs:
            lp, lm = self.source_labels(d, S)
            tp, tm = self.target_labels(d, T)
            if cls == 0:
                ok = (lp is not None and lp in tp) or (lm is not None and lm in tm)
            else:
                ok = (lp is not None and lp in tm) or (lm is not None and lm in tp)
            if ok:
                return d
        return None


def room_end(cells, s, v):
    """Billiard path from the interior point s with unfolded vector v, time 1.
    Returns (end point, sheet), or None when the path meets a corner before
    time 1. The sheet records the parity of the reflections in vertical and in
    horizontal walls."""
    x, y = s
    vx, vy = v
    sx, sy = (vx > 0) - (vx < 0), (vy > 0) - (vy < 0)
    tleft = Fr(1)
    while True:
        tx = ((floor(x) + 1 - x) / vx if vx > 0 else (x - (floor(x) if x != floor(x) else x - 1)) / -vx) if vx != 0 else None
        ty = ((floor(y) + 1 - y) / vy if vy > 0 else (y - (floor(y) if y != floor(y) else y - 1)) / -vy) if vy != 0 else None
        dt = min(z for z in (tx, ty) if z is not None)
        if dt >= tleft:
            return (x + vx * tleft, y + vy * tleft), (1 if vx * sx >= 0 else -1, 1 if vy * sy >= 0 else -1)
        tleft -= dt
        x, y = x + vx * dt, y + vy * dt
        onx, ony = x == floor(x), y == floor(y)
        if onx and ony:
            if point_type(cells, int(x), int(y)) in ("convex", "reflex"):
                return None
            nxt = (floor(x) if vx > 0 else floor(x) - 1, floor(y) if vy > 0 else floor(y) - 1)
            if nxt not in cells:
                if (floor(x) if vx > 0 else floor(x) - 1, floor(y) - 1 if vy > 0 else floor(y)) in cells:
                    vy = -vy
                else:
                    vx = -vx
        elif onx:
            if (floor(x) if vx > 0 else floor(x) - 1, floor(y)) not in cells:
                vx = -vx
        else:
            if (floor(x), floor(y) if vy > 0 else floor(y) - 1) not in cells:
                vy = -vy


def m_end(M, s, v):
    """Straight path on M from the lift of s on sheet (1, 1) with vector v, time 1.
    Returns the sheet of the square that holds the end point, or None when the
    path meets a corner lift before time 1."""
    i = M.sq.index(((floor(s[0]), floor(s[1])), (1, 1)))
    xi, eta = M.local(i, s)
    vx, vy = v
    tleft = Fr(1)
    while True:
        tx = ((1 - xi) / vx if vx > 0 else xi / -vx) if vx != 0 else None
        ty = ((1 - eta) / vy if vy > 0 else eta / -vy) if vy != 0 else None
        dt = min(z for z in (tx, ty) if z is not None)
        if dt >= tleft:
            return M.sq[i][1]
        tleft -= dt
        xi, eta = xi + vx * dt, eta + vy * dt
        hx, hy = tx == dt, ty == dt
        if hx and hy:
            P = M.room_point(i, xi, eta)
            if point_type(M.cells, int(P[0]), int(P[1])) in ("convex", "reflex"):
                return None
            i = M.r[i] if vx > 0 else M.ri[i]
            i = M.u[i] if vy > 0 else M.ui[i]
            xi, eta = (Fr(0) if vx > 0 else Fr(1)), (Fr(0) if vy > 0 else Fr(1))
        elif hx:
            i = M.r[i] if vx > 0 else M.ri[i]
            xi = Fr(0) if vx > 0 else Fr(1)
        else:
            i = M.u[i] if vy > 0 else M.ui[i]
            eta = Fr(0) if vy > 0 else Fr(1)


def shoot_class(cells, s, t, R, cls, M=None):
    """Exact shooter for one class (0: par, 1: cross); s and t interior points.

    For each unfolded vector v from shoot.images: the billiard path of time 1
    (room tracer) and the straight path on M (M tracer) must both avoid the
    corners, or both meet one. A direction counts when the path ends at t on
    a sheet of the requested class. The two tracers must report the same
    sheet. Directions along a lattice line are skipped.
    Returns a direction or None."""
    M = M or MSurf(cells)
    for v in images(s, t, R):
        if (v[0] == 0 and s[0] == floor(s[0])) or (v[1] == 0 and s[1] == floor(s[1])):
            continue
        a = room_end(cells, s, v)
        b = m_end(M, s, v)
        if (a is None) != (b is None):
            raise RuntimeError(f"tracers disagree: {sorted(cells)} {s} {t} {v}")
        if a is None or a[0] != t:
            continue
        if a[1] != b:
            raise RuntimeError(f"sheet mismatch: {sorted(cells)} {s} {t} {v} {a} {b}")
        if (b[0] * b[1] == 1) == (cls == 0):
            return v
    return None


def run_of(cells, x, y, horizontal):
    """Maximal run [A, B] of the room through (x, y) along its row or its column.
    The transverse coordinate must not be an integer."""
    if horizontal:
        b = floor(y)
        a = floor(x) if (floor(x), b) in cells else floor(x) - 1
        lo = hi = a
        while (lo - 1, b) in cells:
            lo -= 1
        while (hi + 1, b) in cells:
            hi += 1
        return lo, hi + 1
    a = floor(x)
    b = floor(y) if (a, floor(y)) in cells else floor(y) - 1
    lo = hi = b
    while (a, lo - 1) in cells:
        lo -= 1
    while (a, hi + 1) in cells:
        hi += 1
    return lo, hi + 1


def twist(cells, pt, horizontal, lam, sign):
    """h^sign (horizontal) or v^sign on the point pt = (x, y, e1, e2) of M.

    In the chart (e1 x, e2 y) of its sheet, h moves the point along its row by
    lam * (height above the lower lattice line); in the room this is a
    one-dimensional billiard in the row. Points on horizontal lattice lines
    are fixed. v is the same with the two coordinates exchanged."""
    x, y, e1, e2 = pt
    if horizontal:
        if y == floor(y):
            return pt
        eta = y - floor(y) if e2 == 1 else 1 - (y - floor(y))
        A, Bq = run_of(cells, x, y, True)
        n = Bq - A
        u = (x - A) if e1 == 1 else 2 * n - (x - A)
        u = (u + sign * lam * eta) % (2 * n)
        return (A + u, y, 1, e2) if u <= n else (A + 2 * n - u, y, -1, e2)
    if x == floor(x):
        return pt
    xi = x - floor(x) if e1 == 1 else 1 - (x - floor(x))
    A, Bq = run_of(cells, x, y, False)
    n = Bq - A
    u = (y - A) if e2 == 1 else 2 * n - (y - A)
    u = (u + sign * lam * xi) % (2 * n)
    return (x, A + u, e1, 1) if u <= n else (x, A + 2 * n - u, e1, -1)


def canon(cells, pt):
    """One representative for a non-lattice wall point of M (two sheets are glued there)."""
    x, y, e1, e2 = pt
    if x == floor(x) and y != floor(y) and not ((floor(x) - 1, floor(y)) in cells and (floor(x), floor(y)) in cells):
        e1 = 1
    if y == floor(y) and x != floor(x) and not ((floor(x), floor(y) - 1) in cells and (floor(x), floor(y)) in cells):
        e2 = 1
    return (x, y, e1, e2)


def shoot2(cells, s, t, R, M=None):
    """Room-level exact shooter with both tracers of shoot.py.

    Directions that run along a lattice line (vertical from a point with
    integer x, horizontal from a point with integer y) are skipped: m_hits
    does not detect corners on such a path. Skipping can only lose witnesses.
    Returns (direction or None, number of directions tried)."""
    M = M or MSurf(cells)
    tried = 0
    for v in images(s, t, R):
        if (v[0] == 0 and s[0] == floor(s[0])) or (v[1] == 0 and s[1] == floor(s[1])):
            continue
        tried += 1
        a = room_hits(cells, s, t, v)
        b = m_hits(M, s, t, v)
        if a != b:
            raise RuntimeError(f"tracers disagree: {sorted(cells)} {s} {t} {v} room={a} M={b}")
        if a:
            return v, tried
    return None, tried
