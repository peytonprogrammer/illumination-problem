#!/usr/bin/env python3
"""Exact shooter for pairs of rational interior points, with two tracers.

For a pair (s, t) of a room, every billiard path from s to t unfolds to a
straight segment from s to an image t' = (e1 tx + 2m, e2 ty + 2n). The shooter
tries images t' in order of distance, up to radius R. For each it follows the
direction v = t' - s for time 0 < time <= 1 with two independent exact tracers:

  room_hits  -- the billiard in the room: specular reflection at walls,
                legal reflection at flat boundary lattice points, failure at a
                convex or reflex corner;
  m_hits     -- the straight line on the four-copy translation surface M
                (squares with right/up gluings, as in cyl.Surface), failure at
                any lift of a convex or reflex corner.

Each tracer reports whether t is met before failure. A pair is LIT when both
tracers agree on some direction; the script aborts if they ever disagree.

usage: python3 shoot.py R < pairs       lines "cells | x/d,y/d;x/d,y/d ..."
  where cells are "x0 y0 x1 y1 ...". Prints one line per pair.
"""
import sys
from fractions import Fraction as Fr
from math import floor

from cyl import Surface, point_type


def piece_contains(P, d, T, tmax):
    """Is T = P + lam d for some 0 < lam <= tmax?"""
    if d[0] != 0:
        lam = (T[0] - P[0]) / d[0]
    else:
        lam = (T[1] - P[1]) / d[1]
    return 0 < lam <= tmax and P[0] + lam * d[0] == T[0] and P[1] + lam * d[1] == T[1]


def room_hits(cells, s, t, v):
    x, y = s
    vx, vy = v
    tleft = Fr(1)
    while tleft > 0:
        tx = ((floor(x) + 1 - x) / vx if vx > 0 else (x - (floor(x) if x != floor(x) else x - 1)) / -vx) if vx != 0 else None
        ty = ((floor(y) + 1 - y) / vy if vy > 0 else (y - (floor(y) if y != floor(y) else y - 1)) / -vy) if vy != 0 else None
        dt = min(z for z in (tx, ty) if z is not None)
        step = min(dt, tleft)
        if piece_contains((x, y), (vx, vy), t, step):
            return True
        if dt > tleft:
            return False
        tleft -= dt
        x, y = x + vx * dt, y + vy * dt
        onx, ony = x == floor(x), y == floor(y)
        if onx and ony:
            kind = point_type(cells, int(x), int(y))
            if kind in ("convex", "reflex"):
                return False
            nxt = (floor(x) if vx > 0 else floor(x) - 1, floor(y) if vy > 0 else floor(y) - 1)
            if nxt not in cells:
                horiz = (floor(x) if vx > 0 else floor(x) - 1, floor(y) - 1 if vy > 0 else floor(y)) in cells
                if horiz:
                    vy = -vy
                else:
                    vx = -vx
        elif onx:
            if (floor(x) if vx > 0 else floor(x) - 1, floor(y)) not in cells:
                vx = -vx
        else:
            if (floor(x), floor(y) if vy > 0 else floor(y) - 1) not in cells:
                vy = -vy
    return False


SHEETS = [(1, 1), (-1, 1), (1, -1), (-1, -1)]


class MSurf:
    def __init__(self, cells):
        self.cells = cells
        S = Surface(cells)
        self.sq, self.r, self.u, self.ri, self.ui = S.sq, S.r, S.u, S.ri, S.ui

    def room_point(self, i, xi, eta):
        (a, b), (e1, e2) = self.sq[i]
        return (a + xi if e1 == 1 else a + 1 - xi, b + eta if e2 == 1 else b + 1 - eta)

    def local(self, i, P):
        (a, b), (e1, e2) = self.sq[i]
        return (P[0] - a if e1 == 1 else a + 1 - P[0], P[1] - b if e2 == 1 else b + 1 - P[1])


def m_hits(M, s, t, v):
    cell = (floor(s[0]), floor(s[1]))
    i = M.sq.index((cell, (1, 1)))
    xi, eta = M.local(i, s)
    vx, vy = v
    tleft = Fr(1)
    while tleft > 0:
        tx = ((1 - xi) / vx if vx > 0 else xi / -vx) if vx != 0 else None
        ty = ((1 - eta) / vy if vy > 0 else eta / -vy) if vy != 0 else None
        dt = min(z for z in (tx, ty) if z is not None)
        step = min(dt, tleft)
        tl = M.local(i, t)
        if 0 <= tl[0] <= 1 and 0 <= tl[1] <= 1 and piece_contains((xi, eta), (vx, vy), tl, step):
            return True
        if dt > tleft:
            return False
        tleft -= dt
        xi, eta = xi + vx * dt, eta + vy * dt
        hx, hy = tx == dt, ty == dt
        if hx and hy:
            P = M.room_point(i, xi, eta)
            if point_type(M.cells, int(P[0]), int(P[1])) in ("convex", "reflex"):
                return False
            j1 = M.r[i] if vx > 0 else M.ri[i]
            j1 = M.u[j1] if vy > 0 else M.ui[j1]
            j2 = M.u[i] if vy > 0 else M.ui[i]
            j2 = M.r[j2] if vx > 0 else M.ri[j2]
            assert j1 == j2, "regular corner with inconsistent gluing"
            i = j1
            xi, eta = (Fr(0) if vx > 0 else Fr(1)), (Fr(0) if vy > 0 else Fr(1))
        elif hx:
            i = M.r[i] if vx > 0 else M.ri[i]
            xi = Fr(0) if vx > 0 else Fr(1)
        else:
            i = M.u[i] if vy > 0 else M.ui[i]
            eta = Fr(0) if vy > 0 else Fr(1)
    return False


def images(s, t, R):
    out = []
    for e1 in (1, -1):
        for e2 in (1, -1):
            for m in range(-R, R + 1):
                for n in range(-R, R + 1):
                    T = (e1 * t[0] + 2 * m, e2 * t[1] + 2 * n)
                    d = (T[0] - s[0], T[1] - s[1])
                    n2 = d[0] ** 2 + d[1] ** 2
                    if 0 < n2 <= R * R:
                        out.append((n2, d))
    out.sort()
    return [d for _, d in out]


def shoot(cells, s, t, R):
    M = MSurf(cells)
    tried = 0
    for v in images(s, t, R):
        tried += 1
        a = room_hits(cells, s, t, v)
        b = m_hits(M, s, t, v)
        if a != b:
            raise RuntimeError(f"tracers disagree: {sorted(cells)} {s} {t} {v} room={a} M={b}")
        if a:
            return v, tried
    return None, tried


def parse_pt(z):
    x, y = z.split(",")
    return (Fr(x), Fr(y))


if __name__ == "__main__":
    R = int(sys.argv[1])
    for line in sys.stdin:
        if "|" not in line:
            continue
        cs, ps = line.split("|", 1)
        v = list(map(int, cs.split()))
        cells = frozenset((v[2 * k], v[2 * k + 1]) for k in range(len(v) // 2))
        for pr in ps.split():
            s, t = map(parse_pt, pr.split(";"))
            d, tried = shoot(cells, s, t, R)
            status = "LIT" if d else "NOTFOUND"
            print(status, " ".join(map(str, v)), "|", f"{s[0]},{s[1]};{t[0]},{t[1]}", "|", f"dir {d[0]},{d[1]}" if d else "", "tried", tried, flush=True)
