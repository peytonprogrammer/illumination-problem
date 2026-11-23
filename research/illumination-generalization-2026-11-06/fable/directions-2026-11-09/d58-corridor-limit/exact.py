"""Exact (Fraction) tools for d58: rooms from order types with real gaps, an
independent billiard tracer, and the window families H (Lemma H), E (dead-end
bounce), in the canonical frame of Lemma H (corridor point T above the door
line y = d, viewer S below, channel [a, b] x [s2, d])."""
import sys
from fractions import Fraction as Fr
from math import gcd, floor, ceil
sys.path.insert(0, '../d57-witness-mining-r3/tools')
from rooms import Room
import newlemmas as nl
from newlemmas import Geo, SYMS


# ------------------------------------------------------------------ rooms
class RRoom:
    """Order type (cell set on an nx x ny grid) with real gaps gx, gy."""
    def __init__(self, nx, ny, cells, gx, gy):
        self.nx, self.ny, self.cells = nx, ny, set(cells)
        self.xs = [Fr(0)]
        for g in gx: self.xs.append(self.xs[-1] + Fr(g))
        self.ys = [Fr(0)]
        for g in gy: self.ys.append(self.ys[-1] + Fr(g))
        self.walls = self._walls()
        self.verts = set()
        for o, c, u0, u1 in self.walls:
            for u in (u0, u1):
                self.verts.add((c, u) if o == 'v' else (u, c))

    def ins(self, i, j):
        return (i, j) in self.cells

    def _walls(self):
        W = []
        for i in range(self.nx + 1):
            j = 0
            while j < self.ny:
                if self.ins(i - 1, j) != self.ins(i, j):
                    j0 = j
                    while j < self.ny and self.ins(i - 1, j) != self.ins(i, j) \
                            and self.ins(i - 1, j) == self.ins(i - 1, j0): j += 1
                    W.append(('v', self.xs[i], self.ys[j0], self.ys[j]))
                else: j += 1
        for j in range(self.ny + 1):
            i = 0
            while i < self.nx:
                if self.ins(i, j - 1) != self.ins(i, j):
                    i0 = i
                    while i < self.nx and self.ins(i, j - 1) != self.ins(i, j) \
                            and self.ins(i, j - 1) == self.ins(i0, j - 1): i += 1
                    W.append(('h', self.ys[j], self.xs[i0], self.xs[i]))
                else: i += 1
        return W

    def coord(self, t, axis, f):
        """Real coordinate of position-type index t; f in (0,1) = offset fraction if t odd."""
        cs = self.xs if axis == 0 else self.ys
        if t % 2 == 0: return cs[t // 2]
        i = t // 2
        return cs[i] + Fr(f) * (cs[i + 1] - cs[i])


def trace(room, S, vec, T, maxhits=10 ** 6):
    """Follow the billiard path from S whose unfolding is S + t*vec, 0 <= t <= 1.
    Returns (ok, reflections, reason). ok iff no vertex is touched and the path
    ends exactly at T."""
    x, y = Fr(S[0]), Fr(S[1])
    dx, dy = Fr(vec[0]), Fr(vec[1])
    if dx == 0 or dy == 0: return False, 0, 'axis-parallel'
    rem = Fr(1)
    nref = 0
    while True:
        best = None
        for o, c, u0, u1 in room.walls:
            if o == 'v':
                t = (c - x) / dx
                if t <= 0 or t > rem: continue
                yy = y + t * dy
                if u0 <= yy <= u1:
                    hit = (t, 'v', c, yy)
                    if best is None or t < best[0]: best = hit
            else:
                t = (c - y) / dy
                if t <= 0 or t > rem: continue
                xx = x + t * dx
                if u0 <= xx <= u1:
                    hit = (t, 'h', xx, c)
                    if best is None or t < best[0]: best = hit
        if best is None:
            x, y = x + rem * dx, y + rem * dy
            return ((x, y) == (Fr(T[0]), Fr(T[1])), nref, 'end' if (x, y) == (Fr(T[0]), Fr(T[1])) else f'miss {x},{y}')
        t, o, px, py = best
        if o == 'v': hx, hy = px, py
        else: hx, hy = px, py
        if (hx, hy) in room.verts: return False, nref, f'vertex {hx},{hy}'
        if t == rem: return False, nref, 'ends on wall'
        x, y = x + t * dx, y + t * dy
        rem -= t
        if o == 'v': dx = -dx
        else: dy = -dy
        nref += 1
        if nref > maxhits: return False, nref, 'too many'


# ------------------------------------------------------------ canonical frame
def canonical(nx, ny, mask, sym):
    """Order type transformed by sym (as in newlemmas.Geo.tr), as (nx', ny', cells)."""
    R = Room(nx, ny, mask, [2] * nx, [2] * ny)
    g = Geo(R.cells, R.W, R.H)
    o = g.tr(sym)
    cells = {(x // 2, y // 2) for (x, y) in o.cells}
    return o.W // 2, o.H // 2, cells, g


# ------------------------------------------------------------------ families
def frgcd(A, B):
    """Positive generator of the group A Z + B Z for rationals A, B (not both 0)."""
    den = A.denominator * B.denominator // gcd(A.denominator, B.denominator)
    a, b = int(A * den), int(B * den)
    return Fr(gcd(a, b), den)


def ext_gcd(a, b):
    if b == 0: return (abs(a), 1 if a >= 0 else -1, 0)
    g, x, y = ext_gcd(b, a % b)
    return g, y, x - (a // b) * y


def window_candidates(geo, hh, eps1, eps2, limit=8):
    """Family with corridor-point image depth hh above the door line:
    candidates (s', X) with s' = a + eps1 (s1 - a) + 2Lk, X = p + eps2 tau + 2wm and
    p < xi < q, xi = (hh s' + D X)/(D + hh). Returns up to `limit` window values,
    each with a list of (k, m) along the kernel (resonant) or a single (k, m)."""
    a, b, p, q, d, S, T = geo
    L, w, tau, D = b - a, q - p, T[0] - p, d - S[1]
    A, B = 2 * L * hh, 2 * w * D
    g = frgcd(A, B)
    c = hh * (a + eps1 * (S[0] - a)) + D * (p + eps2 * tau)
    lo, hi = p * (D + hh), q * (D + hh)
    # values v = c + g N in (lo, hi)
    N0 = floor((lo - c) / g) + 1
    out = []
    den = A.denominator * B.denominator
    Ai, Bi, gi = int(A * den), int(B * den), int(g * den)
    _, x0, y0 = ext_gcd(Ai, Bi)          # Ai x0 + Bi y0 = gi
    kx, ky = Bi // gi, -(Ai // gi)       # kernel direction
    N = N0
    while c + g * N < hi and len(out) < limit:
        v = c + g * N
        k0, m0 = x0 * N, y0 * N
        # reduce k0 toward 0 along the kernel
        if kx: t = -round(Fr(k0, kx)); k0, m0 = k0 + t * kx, m0 + t * ky
        out.append((v, k0, m0, kx, ky))
        N += 1
    return out, (L, w, tau, D, A, B, g)


def H_path(geo, eps1, eps2, k, m, hh):
    """Unfolded vector from S for candidate (k, m) with image depth hh."""
    a, b, p, q, d, S, T = geo
    L, w, tau, D = b - a, q - p, T[0] - p, d - S[1]
    sp = a + eps1 * (S[0] - a) + 2 * L * k
    X = p + eps2 * tau + 2 * w * m
    return (eps1 * (X - sp), D + hh), sp, X
