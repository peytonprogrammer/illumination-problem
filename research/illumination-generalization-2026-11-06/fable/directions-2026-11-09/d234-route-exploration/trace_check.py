"""Independent exact cell-based billiard trace of one direction in the chart.

Room = union of the five tier rectangles (unit lattice cells). Fails on any
corner contact (lattice boundary point that isn't a straight wall point).
Usage: trace_check.py residual m V dir | trace_check.py d233 N V dir
"""
import sys
from fractions import Fraction as F
from math import floor


def room(N, lv):
    tiers = [(0, 5 * N // 2), (0, N), (N - 1, 2 * N + 1), (2 * N, 3 * N), (2 * N, 4 * N)]
    rects = [(x0, x1, lv[i], lv[i + 1]) for i, (x0, x1) in enumerate(tiers)]
    return lambda i, j: any(a <= i < b and c <= j < d for a, b, c, d in rects)


def trace(N, lv, S, T, vx, vy, maxsteps=10 ** 6):
    inside = room(N, lv)
    px, py = F(S[0]), F(S[1])
    hv = hh = 0
    for _ in range(maxsteps):
        # next grid-line crossing
        tx = (F(floor(px) + 1) - px) / vx if vx > 0 else (px - (F(-floor(-px)) - 1)) / -vx
        ty = (F(floor(py) + 1) - py) / vy if vy > 0 else (py - (F(-floor(-py)) - 1)) / -vy
        t = min(tx, ty)
        nx, ny = px + vx * t, py + vy * t
        # target on this segment?
        dx, dy = T[0] - px, T[1] - py
        if dx * vy == dy * vx and 0 < dx / vx <= t:
            return "HIT", hv, hh
        mx, my = (px + nx) / 2, (py + ny) / 2
        if not inside(floor(mx), floor(my)):
            return f"LEFT ROOM at {(px, py)}", hv, hh
        px, py = nx, ny
        onx, ony = px.denominator == 1, py.denominator == 1
        i, j = int(floor(px)), int(floor(py))
        if onx and ony:
            cells = [inside(i - 1, j - 1), inside(i, j - 1), inside(i - 1, j), inside(i, j)]
            k = sum(cells)
            if k == 4:
                continue
            straight_h = cells in ([True, True, False, False], [False, False, True, True])
            straight_v = cells in ([True, False, True, False], [False, True, False, True])
            if straight_h:
                vy = -vy; hh += 1
            elif straight_v:
                vx = -vx; hv += 1
            else:
                return f"CORNER at {(px, py)}", hv, hh
            continue
        if onx:  # crossing vertical line x=i
            ahead = inside(i if vx > 0 else i - 1, floor(py))
            if not ahead:
                vx = -vx; hv += 1
        else:
            ahead = inside(floor(px), j if vy > 0 else j - 1)
            if not ahead:
                vy = -vy; hh += 1
    return "MAXSTEPS", hv, hh


if __name__ == "__main__":
    mode, k, V, d0 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    if mode == "d233":
        N = k; B = 2 * N + 2; lv = (-1, 0, 1, 1 + B, 2 + B, 3 + B); y4 = 2 + B
    else:
        N = 64 * k * k; lv = (-(k + 2), 0, 1, 1 + k, 2 + k, 3 + 2 * k); y4 = 2 + k
    X = 3 * N // 2 + 1
    print(mode, k, V, d0, trace(N, lv, (N - 1, 0), (5 * N // 2, y4), F(X), F(V * d0)))
