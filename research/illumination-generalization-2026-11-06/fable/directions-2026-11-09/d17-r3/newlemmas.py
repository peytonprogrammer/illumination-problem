"""Lemma H and Lemma C+ on lattice rooms (unit cells), with constructive checks.

Geo = unit-cell set plus box size. All hypotheses are read off unit cells, so
a room with all gaps 2 gives the position-type (metric-free) part: the type
(X, Y) is the lattice point (X, Y)."""
from math import gcd
from fractions import Fraction as Fr
from rooms import step


class Geo:
    def __init__(self, cells, W, H):
        self.cells, self.W, self.H = cells, W, H
        self.memo, self.fl = {}, None

    def npt(self, x, y):
        c = self.cells
        return ((x - 1, y - 1) in c) + ((x, y - 1) in c) + ((x - 1, y) in c) + ((x, y) in c)

    def tr(self, g):
        t, fx, fy = g
        out = set()
        for (x, y) in self.cells:
            a = self.W - 1 - x if fx else x
            b = self.H - 1 - y if fy else y
            out.add((b, a) if t else (a, b))
        return Geo(out, self.H, self.W) if t else Geo(out, self.W, self.H)

    def tp(self, g, P):
        t, fx, fy = g
        x, y = P
        if fx: x = self.W - x
        if fy: y = self.H - y
        return (y, x) if t else (x, y)


CHECK_K = True      # False: enumerate C+ configurations without the metric condition on K
SYMS = [(t, fx, fy) for t in (0, 1) for fx in (0, 1) for fy in (0, 1)]


def row_run(c, x, y):
    """Maximal run [a, b) of cells in unit row y that contains cell (x, y)."""
    a, b = x, x + 1
    while (a - 1, y) in c: a -= 1
    while (b, y) in c: b += 1
    return a, b


def col_run(c, x, y):
    a, b = y, y + 1
    while (x, a - 1) in c: a -= 1
    while (x, b) in c: b += 1
    return a, b


def _corridor_up(geo, T):
    """T in a vertical corridor; returns (p, q, mouth level d). Rows d..t2-1
    have the run [p, q); row d-1 doesn't."""
    c = geo.cells
    t1, t2 = T
    p, q = row_run(c, t1, t2 - 1)
    d = t2 - 1
    while (p, d - 1) in c and row_run(c, p, d - 1) == (p, q): d -= 1
    return p, q, d


def _channel_up(geo, S):
    """Rows s2..top-1 above S have one run [a, b). Returns (a, b, top)."""
    c = geo.cells
    s1, s2 = S
    a, b = row_run(c, s1, s2)
    top = s2 + 1
    while (a, top) in c and row_run(c, a, top) == (a, b): top += 1
    return a, b, top


def _corridor_right(geo, S):
    """S in a horizontal corridor; returns (ylo, yhi, largest door line gd)."""
    c = geo.cells
    s1, s2 = S
    lo, hi = col_run(c, s1, s2)
    gd = s1 + 1
    while (gd, lo) in c and col_run(c, gd, lo) == (lo, hi): gd += 1
    return lo, hi, gd


def egcd(a, b):
    if b == 0: return a, 1, 0
    g, x, y = egcd(b, a % b)
    return g, y, x - (a // b) * y


def trace(geo, S, T, dx, dy):
    """Follow direction (dx, dy) from S for gcd(|dx|, |dy|) primitive steps."""
    n = gcd(abs(dx), abs(dy))
    u, v = abs(dx) // n, abs(dy) // n
    x, y, sx, sy = S[0], S[1], (1 if dx >= 0 else -1), (1 if dy >= 0 else -1)
    for _ in range(n):
        r = step(geo, x, y, u, v, sx, sy)
        if r is None: return False
        x, y, sx, sy, _h = r
    return (x, y) == tuple(T)


# ------------------------------------------------------------------ Lemma H
def H_configs(geo, S, T):
    """Canonical frame: T above S. Yields (a, b, p, q, d)."""
    if S[1] >= T[1]: return
    p, q, dlow = corridor_up(geo, T)
    a, b, top = channel_up(geo, S)
    if a > p or b < q: return
    # only the mouth of the maximal corridor: a door above it puts S and T in one strip
    if S[1] < dlow <= top: yield a, b, p, q, dlow


def H_solve(cfg, S, T):
    """For each sign pair: (eps1, eps2, dx, dy) of a candidate with p < xi < q, or None."""
    a, b, p, q, d = cfg
    L, w, tau, D, h = b - a, q - p, T[0] - p, d - S[1], T[1] - d
    A, B = 2 * L * h, 2 * w * D
    g, x0, y0 = egcd(A, B)
    lo, hi = p * (D + h), q * (D + h)
    out = []
    for e1 in (1, -1):
        for e2 in (1, -1):
            c = h * (a + e1 * (S[0] - a)) + D * (p + e2 * tau)
            r = (c - lo) % g
            v = lo + (r if r else g)
            if v >= hi:
                out.append(None); continue
            per = 4 * L * w * (D + h) // g
            best = None
            while v < hi:                      # shortest candidate over all xi in the door
                N = (v - c) // g
                sp = a + e1 * (S[0] - a) + 2 * L * x0 * N
                X = p + e2 * tau + 2 * w * y0 * N
                dx = (X - sp + per // 2) % per - per // 2
                if best is None or abs(dx) < abs(best[0]): best = (dx, v)
                v += g
            dx, v = best
            assert (v - D * dx) % (D + h) == 0     # s' = (v - D dx)/(D + h) is a lattice image
            out.append((e1, e2, e1 * dx, D + h)); continue
            out.append((e1, e2, e1 * (X - sp), D + h))
    return out


def H_resonant(cfg, S, T):
    a, b, p, q, d = cfg
    L, w, D, h = b - a, q - p, d - S[1], T[1] - d
    return D > h and (L * h) % (w * D) == 0


# ----------------------------------------------------------------- Lemma C+
def Cperp_configs(geo, S, T):
    """Canonical frame: S in a horizontal corridor left of the hub with its flat
    end on the floor; T in a vertical corridor above the hub with its flat end
    on the right side. Yields (gd, ylo, yhi, g1, h1, p2, inP) with inP = G in P."""
    c = geo.cells
    if not (S[0] < T[0] and S[1] < T[1]): return
    ylo, yhi, gdmax = corridor_right(geo, S)
    p2, g1, h1low = corridor_up(geo, T)
    for gd in range(S[0] + 1, min(gdmax, p2) + 1):
        if not all((x, ylo) in c and (x, ylo - 1) not in c for x in range(gd, g1)): continue
        for h1 in range(max(h1low, yhi), T[1]):
            if not all((g1 - 1, y) in c and (g1, y) not in c for y in range(ylo, h1)): continue
            dx, dy = p2 - gd, h1 - yhi
            ok = inP = True
            for x in range(gd, g1):
                for y in range(ylo, h1):
                    if (x, y) in c: continue
                    inP = False
                    if (dx == 0 and dy == 0) or dx * (y - yhi) - dy * (x + 1 - gd) < 0: ok = False
            if ok or not CHECK_K: yield gd, ylo, yhi, g1, h1, p2, inP


def Cperp_solve(geo, cfg, S, T, K=200):
    gd, ylo, yhi, g1, h1, p2, _ = cfg
    L, H, w1, w2 = g1 - gd, h1 - ylo, yhi - ylo, g1 - p2
    al, s, t, be = gd - S[0], S[1] - ylo, T[0] - gd, T[1] - h1
    out = []
    for e1 in (1, -1):
        for e2 in (1, -1):
            th0 = L + e2 * (t - L)
            found = None
            for k1 in range(1, -K - 1, -1):
                sg = e1 * s + 2 * w1 * k1
                M = H + be - sg
                if sg >= w1 or M <= be: continue
                f = 1 - Fr(be, M)
                tlo = (L - w2 + Fr(al * be, M)) / f
                thi = (L + w2 + Fr(al * be, M)) / f
                k2 = (tlo - th0) // (2 * w2) + 1
                while th0 + 2 * w2 * k2 < thi:
                    th = th0 + 2 * w2 * k2
                    a = sg + Fr(M * al, th + al)
                    if -w1 < a < w1 and trace(geo, S, T, th + al, e1 * M):
                        found = (e1, e2, th + al, e1 * M); break
                    k2 += 1
                if found: break
            out.append(found)
    return out


def Cpar_configs(geo, S, T):
    """Canonical frame: S in a horizontal corridor left of the hub, T in one
    right of it, both flat ends on a common floor. Yields (gd, g1, ylo, w1, w2, inP)."""
    c = geo.cells
    if S[0] >= T[0]: return
    ylo, yhi, gdmax = corridor_right(geo, S)
    if geo.fl is None: geo.fl = Geo({(geo.W - 1 - x, y) for (x, y) in c}, geo.W, geo.H)
    fl = geo.fl
    ylo2, yhi2, g1m = corridor_right(fl, (geo.W - T[0], T[1]))
    if ylo2 != ylo: return
    g1min = geo.W - g1m
    w1, w2 = yhi - ylo, yhi2 - ylo
    for gd in range(S[0] + 1, gdmax + 1):
        for g1 in range(max(g1min, gd + 1), T[0]):
            if not all((x, ylo) in c and (x, ylo - 1) not in c for x in range(gd, g1)): continue
            L = g1 - gd
            ok = inP = True
            for x in range(gd, g1):
                top = max(w1 * L + (w2 - w1) * (x - gd), w1 * L + (w2 - w1) * (x + 1 - gd))
                for y in range(ylo, max(yhi, yhi2)):
                    if (x, y) in c: continue
                    inP = False
                    if (y - ylo) * L < top: ok = False
            if ok or not CHECK_K: yield gd, g1, ylo, w1, w2, inP


def Cpar_solve(geo, cfg, S, T):
    gd, g1, ylo, w1, w2, _ = cfg
    L, al, be, s, t = g1 - gd, gd - S[0], T[0] - g1, S[1] - ylo, T[1] - ylo
    tot = al + L + be
    K1 = (w1 + al * (w1 + w2) // L) // (2 * w1) + 2
    out = []
    for e1 in (1, -1):
        for e2 in (1, -1):
            found = None
            for k1 in sorted(range(-K1, K1 + 1), key=abs):
                sg = e1 * s + 2 * w1 * k1
                bound = Fr((w1 + w2) * tot, L)
                k2 = (sg - bound - e2 * t) // (2 * w2)
                while e2 * t + 2 * w2 * k2 <= sg + bound:
                    th = e2 * t + 2 * w2 * k2
                    a = sg + Fr((th - sg) * al, tot)
                    b = th - Fr((th - sg) * be, tot)
                    if abs(a) < w1 and abs(b) < w2 and trace(geo, S, T, tot, e1 * (th - sg)):
                        found = (e1, e2, tot, e1 * (th - sg)); break
                    k2 += 1
                if found: break
            out.append(found)
    return out


def _memo(fn):
    def f(geo, P):
        k = (fn.__name__, P)
        if k not in geo.memo: geo.memo[k] = fn(geo, P)
        return geo.memo[k]
    return f


corridor_up, channel_up, corridor_right = _memo(_corridor_up), _memo(_channel_up), _memo(_corridor_right)
