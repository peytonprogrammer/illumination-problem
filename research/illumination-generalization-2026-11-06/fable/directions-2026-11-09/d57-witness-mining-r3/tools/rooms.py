"""Lattice rooms, position types, and an exact billiard tracer for d17.

A room is (nx, ny, mask, gx, gy): order type plus integer gap lengths.
Points are lattice points; rational points are handled by scaling the room.
The tracer is independent of d15 verify.c: it walks unit steps of a primitive
direction with exact integer arithmetic (lattice point to lattice point) and
uses the cell set only."""
from math import gcd


class Room:
    def __init__(self, nx, ny, mask, gx, gy):
        self.nx, self.ny, self.mask = nx, ny, mask
        self.gx, self.gy = list(gx), list(gy)
        self.xs = [0]
        for g in gx: self.xs.append(self.xs[-1] + g)
        self.ys = [0]
        for g in gy: self.ys.append(self.ys[-1] + g)
        self.W, self.H = self.xs[-1], self.ys[-1]
        self.cells = set()
        for j in range(ny):
            for i in range(nx):
                if (mask >> (i + nx * j)) & 1:
                    for x in range(self.xs[i], self.xs[i + 1]):
                        for y in range(self.ys[j], self.ys[j + 1]):
                            self.cells.add((x, y))

    def npt(self, x, y):
        c = self.cells
        return ((x - 1, y - 1) in c) + ((x, y - 1) in c) + ((x - 1, y) in c) + ((x, y) in c)

    def interior_points(self):
        return [(x, y) for x in range(1, self.W) for y in range(1, self.H) if self.npt(x, y) == 4]

    def ptype(self, P):
        x, y = P
        def t(v, cs):
            for i in range(len(cs) - 1):
                if cs[i] == v: return 2 * i
                if cs[i] < v < cs[i + 1]: return 2 * i + 1
            return 2 * (len(cs) - 1)
        return (t(x, self.xs), t(y, self.ys))

    def shape(self):
        return "/".join("".join("#" if (self.mask >> (i + self.nx * j)) & 1 else "." for i in range(self.nx))
                        for j in reversed(range(self.ny)))


def step(room, x, y, dx, dy, sx, sy):
    """One unit of the primitive direction (dx, dy) >= 0 with signs (sx, sy),
    from lattice point (x, y). Returns (x, y, sx, sy, hits) or None if a vertex
    is met. hits = list of ('v'|'h', coordinate) wall hits in order."""
    c = room.cells
    hits = []
    if dx == 0 or dy == 0:
        nx_, ny_ = x + (sx if dx else 0), y + (sy if dy else 0)
        k = room.npt(nx_, ny_)
        if k == 4: return nx_, ny_, sx, sy, hits
        if k != 2: return None
        horiz = ((nx_ - 1, ny_ - 1) in c and (nx_, ny_ - 1) in c) or ((nx_ - 1, ny_) in c and (nx_, ny_) in c)
        if dx:
            if horiz: return None
            return nx_, ny_, -sx, sy, [('v', nx_)]
        if not horiz: return None
        return nx_, ny_, sx, -sy, [('h', ny_)]
    cx = x if sx > 0 else x - 1
    cy = y if sy > 0 else y - 1
    i = j = 1
    while True:
        l, r = i * dy, j * dx
        if l < r:
            if (cx + sx, cy) in c: cx += sx
            else:
                hits.append(('v', cx + 1 if sx > 0 else cx)); sx = -sx
            i += 1
        elif l > r:
            if (cx, cy + sy) in c: cy += sy
            else:
                hits.append(('h', cy + 1 if sy > 0 else cy)); sy = -sy
            j += 1
        else:
            px = cx + 1 if sx > 0 else cx
            py = cy + 1 if sy > 0 else cy
            k = room.npt(px, py)
            if k == 4:
                cx += sx; cy += sy
            elif k == 2:
                horiz = ((px - 1, py - 1) in c and (px, py - 1) in c) or ((px - 1, py) in c and (px, py) in c)
                vert = ((px - 1, py - 1) in c and (px - 1, py) in c) or ((px, py - 1) in c and (px, py) in c)
                if horiz:
                    hits.append(('h', py)); sy = -sy; cx += sx
                elif vert:
                    hits.append(('v', px)); sx = -sx; cy += sy
                else: return None
            else: return None
            assert i == dx and j == dy
            return px, py, sx, sy, hits


def shoot(room, S, T, bound, want_all=False):
    """Primitive directions with |u| + |v| <= bound, by increasing |u| + |v|.
    Returns (u, v, steps, hits) of the first lit direction, or None."""
    res = []
    lim = 4 * (room.W + 1) * (room.H + 1) + 8
    for s in range(1, bound + 1):
        for u in range(0, s + 1):
            v = s - u
            if gcd(u, v) != 1: continue
            for sx0 in ((1, -1) if u else (1,)):
                for sy0 in ((1, -1) if v else (1,)):
                    x, y, sx, sy = S[0], S[1], sx0, sy0
                    allh = []
                    for n in range(1, lim + 1):
                        r = step(room, x, y, u, v, sx, sy)
                        if r is None: break
                        x, y, sx, sy, h = r
                        allh += h
                        if (x, y) == tuple(T):
                            out = (u * sx0, v * sy0, n, allh)
                            if not want_all: return out
                            res.append(out); break
                        if (x, y) == tuple(S) and (sx, sy) == (sx0, sy0): break
    return res if want_all else None
