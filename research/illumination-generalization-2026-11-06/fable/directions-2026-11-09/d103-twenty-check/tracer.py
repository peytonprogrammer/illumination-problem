"""D103 exact billiard tracer for a lattice room given by unit cells (own code).

trace(C, s, v): follow the straight unfolded segment s -> s+v through the room.
A crossing through a grid vertex is allowed only at a regular interior vertex
(4 cells) or a smooth wall vertex (2 collinear cells). Returns the physical end
point, or None if the path meets a corner or starts outside.
find_path(C, s, t, R): search the reflected images (+-tx + 2M, +-ty + 2N) of t,
|M|,|N| <= R, nearest first, and return a displacement that ends at t.
"""
from fractions import Fraction as F
from math import lcm
from itertools import product


def occ(C, X, Y):
    return [(X - i, Y - j) in C for i in (1, 0) for j in (1, 0)]


def is_corner(C, X, Y):
    o = occ(C, X, Y)  # cells (X-1,Y-1),(X-1,Y),(X,Y-1),(X,Y)
    k = sum(o)
    if k in (1, 3):
        return True
    if k == 2:
        return o[0] == o[3]  # diagonal pair
    return False


def trace(C, s, v):
    D = lcm(*(z.denominator for z in (*s, *v)))
    Sx, Sy, Vx, Vy = (int(z * D) for z in (*s, *v))
    if Vx == 0 or Vy == 0:
        return None
    hx, hy = (1 if Vx > 0 else -1), (1 if Vy > 0 else -1)
    ux = Sx // D if Sx % D else Sx // D - (hx < 0)
    uy = Sy // D if Sy % D else Sy // D - (hy < 0)
    a, b = ux, uy
    if (a, b) not in C:
        return None
    fx = fy = 1
    # times of the next vertical / horizontal unfolded line, as numerators over |Vx|*|Vy|
    AX, AY = abs(Vx), abs(Vy)
    nx = ux + (hx > 0)  # next vertical line index
    ny = uy + (hy > 0)
    while True:
        tx = abs(nx * D - Sx) * AY  # time * AX*AY
        ty = abs(ny * D - Sy) * AX
        T1 = AX * AY
        if tx >= T1 and ty >= T1:
            break
        if tx == ty:
            px, py = fx * hx, fy * hy
            X, Y = a + (px > 0), b + (py > 0)
            if is_corner(C, X, Y):
                return None
        if tx <= ty:
            px = fx * hx
            if (a + px, b) in C:
                a += px
            else:
                fx = -fx
            ux += hx; nx += hx
        if ty <= tx:
            py = fy * hy
            if (a, b + py) in C:
                b += py
            else:
                fy = -fy
            uy += hy; ny += hy
    ox = F(Sx + Vx - ux * D, D)
    oy = F(Sy + Vy - uy * D, D)
    x = a + (ox if fx == 1 else 1 - ox)
    y = b + (oy if fy == 1 else 1 - oy)
    return (x, y)


def interior(C, p):
    x, y = p
    xs = [x.numerator // x.denominator] if x.denominator > 1 else [int(x) - 1, int(x)]
    ys = [y.numerator // y.denominator] if y.denominator > 1 else [int(y) - 1, int(y)]
    return all((i, j) in C for i in xs for j in ys)


def find_path(C, s, t, R):
    cands = []
    for M, N, sx, sy in product(range(-R, R + 1), range(-R, R + 1), (1, -1), (1, -1)):
        img = (sx * t[0] + 2 * M, sy * t[1] + 2 * N)
        v = (img[0] - s[0], img[1] - s[1])
        if v[0] and v[1]:
            cands.append((v[0] ** 2 + v[1] ** 2, v))
    cands.sort()
    seen = set()
    for _, v in cands:
        if v in seen:
            continue
        seen.add(v)
        if trace(C, s, v) == tuple(t):
            return v
    return None
