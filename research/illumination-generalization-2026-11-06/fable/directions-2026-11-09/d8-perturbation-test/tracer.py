"""Room-level billiard tracer with exact Fractions (no unfolding).

trace(cells, S, D) follows the billiard path that starts at room point S with
initial velocity D = (DX, DY) (integers) for unit time, reflecting in the walls.
It returns (endpoint, ok, lattice_points_visited). ok is False when the path
touches a polygon vertex (convex or reflex corner) at any time in (0, 1].
"""
from fractions import Fraction as Fr
from math import floor, ceil

from room import status


def normalize_start(cells, S, D):
    """At a flat wall point S, reflect an outward velocity component (the same
    path in the unfolding). Raise if D runs along the wall. Then check that the
    first cell entered is a room cell."""
    X, Y = S
    DX, DY = D
    if status(cells, S) == "smooth":
        below = (X - 1, Y - 1) in cells and (X, Y - 1) in cells
        above = (X - 1, Y) in cells and (X, Y) in cells
        left = (X - 1, Y - 1) in cells and (X - 1, Y) in cells
        if below or above:
            if DY == 0:
                raise RuntimeError("start runs along a horizontal wall")
            if (DY > 0) != above:
                DY = -DY
        else:
            if DX == 0:
                raise RuntimeError("start runs along a vertical wall")
            if (DX < 0) != left:
                DX = -DX
    cx = X if DX > 0 else X - 1
    cy = Y if DY > 0 else Y - 1
    if DX != 0 and DY != 0:
        assert (cx, cy) in cells, "start leaves the room"
    return DX, DY


def trace(cells, S, D):
    cells = set(cells)
    D = normalize_start(cells, S, D)
    end, ok, visited, _ = advance(cells, Fr(S[0]), Fr(S[1]), Fr(D[0]), Fr(D[1]))
    return end, ok, visited


def advance(cells, x, y, vx, vy):
    """Follow the billiard flow for unit time. Returns (end, ok, visited, v_end)."""
    assert (vx, vy) != (0, 0)
    t = Fr(0)
    visited = []
    while True:
        tx = ty = None
        if vx != 0:
            nx = floor(x) + 1 if vx > 0 else ceil(x) - 1
            tx = (nx - x) / vx
        if vy != 0:
            ny = floor(y) + 1 if vy > 0 else ceil(y) - 1
            ty = (ny - y) / vy
        dt = min(d for d in (tx, ty) if d is not None)
        if t + dt > 1:   # a lattice point at t = 1 is processed first (reflection)
            x, y = x + vx * (1 - t), y + vy * (1 - t)
            end = (x, y)
            if x.denominator == 1 and y.denominator == 1:
                st = status(cells, (int(x), int(y)))
                if st not in ("interior", "smooth"):
                    return end, False, visited, (vx, vy)
            return end, True, visited, (vx, vy)
        t += dt
        x, y = x + vx * dt, y + vy * dt
        if x.denominator == 1 and y.denominator == 1:
            p = (int(x), int(y))
            st = status(cells, p)
            visited.append(p)
            if st != "interior" and st != "smooth":
                return p, False, visited, (vx, vy)
            if st == "smooth":
                X, Y = p
                below = (X - 1, Y - 1) in cells and (X, Y - 1) in cells
                above = (X - 1, Y) in cells and (X, Y) in cells
                left = (X - 1, Y - 1) in cells and (X - 1, Y) in cells
                if below or above:          # horizontal wall through p
                    if vy == 0:
                        raise RuntimeError("path runs along a horizontal wall")
                    if (vy > 0 and below) or (vy < 0 and above):
                        vy = -vy
                    else:
                        raise RuntimeError("arrived from outside")
                else:                       # vertical wall through p
                    if vx == 0:
                        raise RuntimeError("path runs along a vertical wall")
                    if (vx > 0 and left) or (vx < 0 and not left):
                        vx = -vx
                    else:
                        raise RuntimeError("arrived from outside")
            continue
        # crossing a grid line at a non-lattice point
        if x.denominator == 1 and (tx is not None and dt == tx):
            # vertical line x = integer, y not integer
            row = floor(y)
            col = int(x) if vx > 0 else int(x) - 1
            if (col, row) not in cells:
                vx = -vx
        elif y.denominator == 1 and (ty is not None and dt == ty):
            col = floor(x)
            row = int(y) if vy > 0 else int(y) - 1
            if (col, row) not in cells:
                vy = -vy
        else:
            raise RuntimeError("no crossing")


def certify(cells, S, T, D):
    """Try the four sign choices of D from S. Return the signed vector that
    gives a legal path ending at T, or None."""
    for sx in (1, -1):
        for sy in (1, -1):
            if (sx == -1 and D[0] == 0) or (sy == -1 and D[1] == 0):
                continue
            try:
                Ds = normalize_start(cells, S, (sx * D[0], sy * D[1]))
                end, ok, _ = trace(cells, S, Ds)
            except (RuntimeError, AssertionError):
                continue
            if ok and end == (Fr(T[0]), Fr(T[1])):
                return Ds
    return None


def ray_reach(cells, S, d, sources):
    """Sources met by the billiard ray from S with primitive velocity d, before
    it meets a vertex or returns to S with velocity d. One lattice step per
    unit time."""
    cells = set(cells)
    x, y = Fr(S[0]), Fr(S[1])
    vx, vy = Fr(d[0]), Fr(d[1])
    start = (x, y, vx, vy)
    met = set()
    src = set(sources)
    for _ in range(100000):
        end, ok, _, (vx, vy) = advance(cells, x, y, vx, vy)
        if not ok:
            return met
        x, y = end
        p = (int(x), int(y))
        if (x, y, vx, vy) == start:
            return met
        if p in src:
            met.add(p)
    raise RuntimeError("ray did not close")
