#!/usr/bin/env python3
"""Independent consistency check of cyl.labels with a room-level billiard tracer.

For random rational points s and directions (p, q), trace the billiard path of
direction (p, q) from s in the room with exact Fractions (specular reflection
at walls; stop when a vertex is hit). At the midpoint of every segment piece
inside a cell, read the family (+ when the velocity is parallel to (p, q),
- when parallel to (p, -q)) and the strip index, and look up the label. All
labels met along one trajectory must agree (they are the DP cylinder of the
leaf). Trajectories that hit a vertex are singular leaves: the labels of the
pieces met must then still agree on each side... we only check regular ones.

Also checks: in a one-cylinder direction the single cylinder is full; the
`faces` rule (diamond centre test) against brute-force sampling.

usage: python3 check_labels.py
"""
import random
import sys
from fractions import Fraction as Fr
from math import gcd, floor

sys.path.insert(0, ".")
from cyl import labels, point_type  # noqa: E402
from cover import faces  # noqa: E402

random.seed(13)


def trace(cells, s, v, maxseg=2000):
    """Yield (cell, midpoint, velocity) for each piece; return 'closed',
    'vertex'."""
    x, y = s
    vx, vy = v
    start = (x, y, vx, vy)
    pieces = []
    for _ in range(maxseg):
        # next grid crossing
        tx = ((floor(x) + 1 - x) / vx if vx > 0 else (x - (floor(x) if x != floor(x) else x - 1)) / -vx) if vx != 0 else None
        ty = ((floor(y) + 1 - y) / vy if vy > 0 else (y - (floor(y) if y != floor(y) else y - 1)) / -vy) if vy != 0 else None
        cand = [t for t in (tx, ty) if t is not None]
        t = min(cand)
        mx, my = x + vx * t / 2, y + vy * t / 2
        cell = (floor(mx), floor(my))
        assert cell in cells, (cell, s, v)
        pieces.append((cell, (mx, my), (vx, vy)))
        if len(pieces) > 1 and (vx, vy) == (start[2], start[3]):
            # does the piece pass through s?  s = (x,y) + lam (vx,vy), 0 < lam <= t
            lam = (s[0] - x) / vx if vx != 0 else (s[1] - y) / vy
            if 0 < lam <= t and x + vx * lam == s[0] and y + vy * lam == s[1]:
                return pieces, "closed"
        x, y = x + vx * t, y + vy * t
        # at (x, y) on a grid line; decide what lies ahead
        onx = x == floor(x)
        ony = y == floor(y)
        if onx and ony:
            ty_ = point_type(cells, int(x), int(y))
            if ty_ in ("convex", "reflex"):
                return pieces, "vertex"
            # flat or interior: next cell along diagonal
            nxt = (floor(x) if vx > 0 else floor(x) - 1, floor(y) if vy > 0 else floor(y) - 1)
            if nxt not in cells:
                # flat wall: reflect the component normal to the wall
                c1 = (floor(x) if vx > 0 else floor(x) - 1, floor(y) if vy < 0 else floor(y) - 1)
                # wall is horizontal if the cell across in x (same y side) is inside
                horiz = (floor(x) if vx > 0 else floor(x) - 1, floor(y) - 1 if vy > 0 else floor(y)) in cells
                if horiz:
                    vy = -vy
                else:
                    vx = -vx
        elif onx:
            nxt = (floor(x) if vx > 0 else floor(x) - 1, floor(y))
            if nxt not in cells:
                vx = -vx
        else:
            nxt = (floor(x), floor(y) if vy > 0 else floor(y) - 1)
            if nxt not in cells:
                vy = -vy
    raise RuntimeError("no closure")


def piece_label(L, cell, m, v, p, q):
    vx, vy = v
    if vx * q == vy * p:   # parallel to (p, q): plus family, value q x - p y
        val = q * m[0] - p * m[1]
        k = floor(val)
        assert val != k
        return L.plus[cell][k]
    val = q * m[0] + p * m[1]
    k = floor(val)
    assert val != k
    return L.minus[cell][k]


def main():
    from cover import full_cylinders
    rooms = {
        "A6a": [(0, 0), (0, 1), (0, 2), (0, 3), (1, 1), (1, 2)],
        "A7": [(0, 0), (1, 0), (0, 1), (0, 2), (1, 2), (0, 3), (1, 3)],
        "cross": [(x, y) for x in range(4) for y in range(1, 3)] + [(1, 0), (2, 0), (1, 3), (2, 3)],
        "L3": [(0, 0), (1, 0), (0, 1)],
    }
    sys.path.insert(0, "../d3-review")
    from surface import q22_cells
    rooms["q22"] = sorted(q22_cells())
    ntraj = 0
    for nm, cells in rooms.items():
        cells = frozenset(cells)
        for p in range(0, 6):
            for q in range(0, 6):
                if gcd(p, q) != 1:
                    continue
                L = labels(cells, p, q)
                fl = full_cylinders(L, cells)
                if L.ncyl == 1:
                    assert fl == [True], (nm, p, q)
                for _ in range(40):
                    c = random.choice(sorted(cells))
                    s = (c[0] + Fr(random.randint(1, 96), 97), c[1] + Fr(random.randint(1, 96), 97))
                    if (q * s[0] - p * s[1]).denominator == 1 or (q * s[0] + p * s[1]).denominator == 1:
                        continue
                    pieces, how = trace(cells, s, (Fr(p), Fr(q)))
                    if how != "closed":
                        continue
                    labs = {piece_label(L, cell, m, v, p, q) for cell, m, v in pieces}
                    assert len(labs) == 1, (nm, p, q, s, labs)
                    ntraj += 1
        print(nm, "ok")
    # faces rule vs sampling
    for p in range(1, 5):
        for q in range(1, 5):
            if gcd(p, q) != 1:
                continue
            for a in range(-2, 3):
                for b in range(-2, 3):
                    fs = set(faces(a, b, p, q))
                    N = 4 * p * q * 7
                    seen = set()
                    for i in range(1, N):
                        for j in range(1, N):
                            x, y = a + Fr(i, N), b + Fr(j, N)
                            u, w = q * x - p * y, q * x + p * y
                            if u == floor(u) or w == floor(w):
                                continue
                            seen.add((floor(u), floor(w)))
                    assert seen <= fs, (p, q, a, b)
                    assert fs <= seen or True
                    if fs != seen:
                        # sampling may miss thin faces; refine
                        assert False, (p, q, a, b, fs - seen)
    print("faces rule ok; trajectories checked:", ntraj)


if __name__ == "__main__":
    main()
