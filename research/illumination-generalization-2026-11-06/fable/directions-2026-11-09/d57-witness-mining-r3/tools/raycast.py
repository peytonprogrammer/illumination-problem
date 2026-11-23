"""Wall-by-wall billiard ray caster with exact fractions. It works on the list
of maximal wall segments of the room, not on cells, and it is independent of
verify.c and of the d8 tracer.

follow(cells, S, V): follow the path from interior point S with velocity V for
unit time. Returns (end point, ok); ok is False if the path meets a vertex."""
from fractions import Fraction as Fr


def wall_segments(cells):
    cells = set(cells)
    hor, ver = {}, {}                      # y -> sorted unit x's ; x -> unit y's
    for (i, j) in cells:
        if (i, j - 1) not in cells: hor.setdefault(j, []).append(i)
        if (i, j + 1) not in cells: hor.setdefault(j + 1, []).append(i)
        if (i - 1, j) not in cells: ver.setdefault(i, []).append(j)
        if (i + 1, j) not in cells: ver.setdefault(i + 1, []).append(j)
    verts = set()
    for (i, j) in cells:
        for p in ((i, j), (i + 1, j), (i, j + 1), (i + 1, j + 1)):
            n = sum((p[0] + a, p[1] + b) in cells for a in (-1, 0) for b in (-1, 0))
            if n in (1, 3): verts.add(p)
    H = [(y, x, x + 1) for y, xs in hor.items() for x in xs]
    V = [(x, y, y + 1) for x, ys in ver.items() for y in ys]
    return H, V, verts


def follow(cells, S, V):
    H, Vw, verts = wall_segments(cells)
    x, y = Fr(S[0]), Fr(S[1]); vx, vy = Fr(V[0]), Fr(V[1]); left = Fr(1)
    while left > 0:
        best = left; hit = None
        for (wy, x0, x1) in H:
            if vy != 0:
                t = (wy - y) / vy
                if 0 < t <= best and x0 <= x + t * vx <= x1 and (t < best or hit is None): best, hit = t, 'h'
        for (wx, y0, y1) in Vw:
            if vx != 0:
                t = (wx - x) / vx
                if 0 < t <= best and y0 <= y + t * vy <= y1 and (t < best or hit is None): best, hit = t, 'v'
        for (px, py) in verts:               # a vertex on the path up to the first wall hit
            dx, dy = px - x, py - y
            if dx * vy == dy * vx:
                t = dx / vx if vx != 0 else (dy / vy if vy != 0 else None)
                if t is not None and 0 < t <= best: return (None, False)
        x += best * vx; y += best * vy; left -= best
        if hit == 'h': vy = -vy
        elif hit == 'v': vx = -vx
    return ((x, y), True)
