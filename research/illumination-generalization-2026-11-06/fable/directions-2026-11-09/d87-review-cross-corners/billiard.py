"""Independent exact billiard tracer for unit-cell rooms (D87 referee).

A room is a set of unit cells (x, y) = [x, x+1] x [y, y+1]. Velocities are
integer vectors; one unit of time moves the developed point by the velocity.
Written from scratch; it does not import D8 or D85 code.
"""
from fractions import Fraction as F
from math import floor, ceil


def incid(cells, p):
    x, y = p
    return sum((x - i, y - j) in cells for i in (0, 1) for j in (0, 1))


def is_interior_pt(cells, p):
    """Point (Fractions) strictly inside the closed room's interior, or a smooth wall point."""
    x, y = p
    xs = [floor(x)] if x.denominator > 1 else [int(x) - 1, int(x)]
    ys = [floor(y)] if y.denominator > 1 else [int(y) - 1, int(y)]
    return any((a, b) in cells for a in xs for b in ys)


def run(cells, start, vel, tmax, stop_at=None):
    """Follow the billiard from `start` with velocity `vel` for time tmax.

    Returns dict(end, vel, ok, hits, events). ok=False means a corner (incidence 1 or 3)
    was touched at time t <= tmax; then `end` is that corner and `t` its time.
    hits lists (t, lattice point, incidence) for every lattice point met at t > 0.
    contacts lists (t, point, 'V'|'H') for every wall reflection.
    """
    x, y = F(start[0]), F(start[1])
    vx, vy = vel
    t = F(0)
    hits, contacts = [], []
    while True:
        tx = ty = None
        if vx:
            nx = floor(x) + 1 if vx > 0 else ceil(x) - 1
            tx = (nx - x) / vx
        if vy:
            ny = floor(y) + 1 if vy > 0 else ceil(y) - 1
            ty = (ny - y) / vy
        dt = min(d for d in (tx, ty) if d is not None)
        if t + dt > tmax:
            x, y = x + vx * (tmax - t), y + vy * (tmax - t)
            return dict(end=(x, y), vel=(vx, vy), ok=True, hits=hits, contacts=contacts, t=tmax)
        t += dt
        x, y = x + vx * dt, y + vy * dt
        onv = x.denominator == 1
        onh = y.denominator == 1
        if onv and onh:
            p = (int(x), int(y))
            k = incid(cells, p)
            hits.append((t, p, k))
            if k in (1, 3) or (stop_at is not None and p == stop_at):
                return dict(end=p, vel=(vx, vy), ok=False, hits=hits, contacts=contacts, t=t, k=k)
            if k == 4:
                continue
            assert k == 2
            X, Y = p
            # Cells ahead in the direction of travel.
            cx = X if vx > 0 else X - 1
            cy = Y if vy > 0 else Y - 1
            if vx == 0 or vy == 0:
                raise RuntimeError('axial motion through a wall lattice point')
            ahead = (cx, cy) in cells
            if ahead:
                raise RuntimeError('k=2 but ahead cell present: grazing')
            # Which reflection: horizontal wall if the two cells are stacked side by side.
            if ((X - 1, Y) in cells and (X, Y) in cells) or ((X - 1, Y - 1) in cells and (X, Y - 1) in cells):
                vy = -vy
                contacts.append((t, p, 'H'))
            else:
                vx = -vx
                contacts.append((t, p, 'V'))
            continue
        if onv and tx is not None and dt == tx:
            col = int(x) if vx > 0 else int(x) - 1
            if (col, floor(y)) not in cells:
                vx = -vx
                contacts.append((t, (x, y), 'V'))
        elif onh and ty is not None and dt == ty:
            row = int(y) if vy > 0 else int(y) - 1
            if (floor(x), row) not in cells:
                vy = -vy
                contacts.append((t, (x, y), 'H'))
        else:
            raise RuntimeError('no crossing')
