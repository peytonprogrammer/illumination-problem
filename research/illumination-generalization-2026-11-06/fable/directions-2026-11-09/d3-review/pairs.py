#!/usr/bin/env python3
"""Explicit legal billiard paths between interior (1/N)-grid points of the
22-wall room, found and checked by two exact tracers written by the reviewer.

Search: for S, T, try unfolded targets t' = (g1*T1 + 2*m1, g2*T2 + 2*m2),
g in {+-1}^2, |m_i| <= R, by increasing length, skipping axis-parallel ones.
Tracer 1 (surface.Surface.segment) develops the segment on the square-tiled
unfolding M. Tracer 2 (room_trace below) reflects in room coordinates. A pair
counts as LIT only when both tracers agree that the path avoids every polygon
vertex and ends at T.

Usage: python3 pairs.py N R
"""
import math
import sys
from fractions import Fraction as Fr
from itertools import product
from surface import Surface, q22_cells, point_type


def room_trace(cells, s, d):
    """Billiard from s with velocity d for unit time, in room coordinates.
    Returns (end point, list of reflection points) or (None, reason)."""
    pos = list(s)
    v = list(d)
    t = Fr(0)
    refl = []
    while True:
        # next crossing of an integer line in x and in y (strictly later)
        cand = []
        for k in (0, 1):
            if v[k] == 0:
                continue
            x = pos[k]
            nxt = math.floor(x) + 1 if v[k] > 0 else math.ceil(x) - 1
            cand.append(((nxt - x) / v[k], k))
        dt = min(c[0] for c in cand)
        if t + dt >= 1:
            end = (pos[0] + (1 - t) * v[0], pos[1] + (1 - t) * v[1])
            return end, refl
        t += dt
        pos = [pos[0] + dt * v[0], pos[1] + dt * v[1]]
        axes = [k for c, k in cand if c == dt]
        if len(axes) == 2:  # lattice point
            ty = point_type(cells, int(pos[0]), int(pos[1]))
            if ty in ("convex", "reflex"):
                return None, f"vertex {tuple(map(int, pos))}"
            if ty == "flat-v":
                v[0] = -v[0]; refl.append(tuple(pos))
            elif ty == "flat-h":
                v[1] = -v[1]; refl.append(tuple(pos))
            elif ty != "interior":
                raise AssertionError("left the room")
        else:
            k = axes[0]
            g = int(pos[k])
            o = pos[1 - k]
            fl = o.numerator // o.denominator
            if k == 0:
                beyond = (g, fl) if v[0] > 0 else (g - 1, fl)
            else:
                beyond = (fl, g) if v[1] > 0 else (fl, g - 1)
            if beyond not in cells:
                v[k] = -v[k]
                refl.append(tuple(pos))


def interior_points(cells, N):
    xs = [a for a, b in cells]; ys = [b for a, b in cells]
    out = []
    for X in range(min(xs) * N, (max(xs) + 1) * N + 1):
        for Y in range(min(ys) * N, (max(ys) + 1) * N + 1):
            x, y = Fr(X, N), Fr(Y, N)
            # interior iff a small disk is in the room: all cells touching the point
            cx = [x.numerator // x.denominator] if x.denominator != 1 else [int(x) - 1, int(x)]
            cy = [y.numerator // y.denominator] if y.denominator != 1 else [int(y) - 1, int(y)]
            if all((a, b) in cells for a in cx for b in cy):
                out.append((x, y))
    return out


def find_path(S, cells, s, T, R):
    cands = []
    for g1, g2 in product((1, -1), repeat=2):
        for m1 in range(-R, R + 1):
            for m2 in range(-R, R + 1):
                tp = (g1 * T[0] + 2 * m1, g2 * T[1] + 2 * m2)
                d = (tp[0] - s[0], tp[1] - s[1])
                if d[0] == 0 or d[1] == 0:
                    continue
                cands.append((d[0] ** 2 + d[1] ** 2, d))
    cands.sort()
    tried = 0
    for _, d in cands:
        tried += 1
        end, ok, ev = S.segment(s, d)
        if not ok or end != T:
            continue
        end2, refl = room_trace(cells, s, d)
        assert end2 == T, ("tracers disagree", s, T, d, end2, refl)
        return d, refl, tried
    return None, None, tried


def main(N, R):
    cells = q22_cells()
    S = Surface(cells)
    pts = interior_points(cells, N)
    print(f"N={N}: {len(pts)} interior grid points; pairs (incl. S=T): {len(pts)*(len(pts)+1)//2}")
    unlit = []
    maxlen = 0
    lines = []
    for i in range(len(pts)):
        for j in range(i, len(pts)):
            s, T = pts[i], pts[j]
            d, refl, tried = find_path(S, cells, s, T, R)
            if d is None:
                unlit.append((s, T, tried))
                continue
            maxlen = max(maxlen, max(abs(d[0]), abs(d[1])))
            lines.append(f"{tuple(map(str, s))} -> {tuple(map(str, T))}: direction {tuple(map(str, d))}, "
                         f"{len(refl)} reflections")
    print(f"lit pairs: {len(lines)}; largest |coordinate| of displacement used: {maxlen}")
    for s, T, tried in unlit:
        print(f"NO PATH FOUND: {tuple(map(str, s))} -> {tuple(map(str, T))} ({tried} candidates, R={R})")
    return lines


if __name__ == "__main__":
    N, R = int(sys.argv[1]), int(sys.argv[2])
    lines = main(N, R)
    if len(sys.argv) > 3:
        with open(sys.argv[3], "w") as f:
            f.write("\n".join(lines) + "\n")
