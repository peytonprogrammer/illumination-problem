"""Search for half-rational dark families S=(x,y0), T=((k-a*x)/b, v0) allowed by Theorem X
(family.md): a*y0+b*v0 and a*y0-b*v0 integers. Exact integer ray tracer, conservative
(a ray through any lattice point counts as blocked). Usage: search.py MODE [R]"""
import sys, itertools
from math import gcd, floor

def trace(cells, sx, sy, dx, dy, Q):
    """Billiard path from (sx,sy) with unfolded displacement (dx,dy), units 1/Q.
    Returns the end room point, or None if the path meets a lattice point."""
    if dy == 0 and sy % Q == 0: return None
    ux = sx // Q
    uy = sy // Q if sy % Q else (sy // Q if dy > 0 else sy // Q - 1)
    i, j, e1, e2 = ux, uy, 1, 1
    gx, gy = (1 if dx > 0 else -1), (1 if dy > 0 else -1)
    bx, by = abs(dx), abs(dy)
    while True:
        ax = abs((ux + (dx > 0)) * Q - sx) if dx else None
        ay = abs((uy + (dy > 0)) * Q - sy) if dy else None
        okx = dx != 0 and ax < bx
        oky = dy != 0 and ay < by
        if okx and oky:
            c = ax * by - ay * bx
            if c == 0: return None
            okx, oky = c < 0, c > 0
        if okx:
            ux += gx
            if (i + e1 * gx, j) in cells: i += e1 * gx
            else: e1 = -e1
        elif oky:
            uy += gy
            if (i, j + e2 * gy) in cells: j += e2 * gy
            else: e2 = -e2
        else: break
    fx, fy = sx + dx - ux * Q, sy + dy - uy * Q
    return (i * Q + (fx if e1 == 1 else Q - fx), j * Q + (fy if e2 == 1 else Q - fy))

def interior(cells, px, py, Q):
    if px % Q == 0: return False
    i = px // Q
    if py % Q: return (i, py // Q) in cells
    return (i, py // Q) in cells and (i, py // Q - 1) in cells

def lit(cells, S, T, Q, R):
    rays = []
    for m in range(-R, R + 1):
        for n in range(-R, R + 1):
            for e1 in (1, -1):
                for e2 in (1, -1):
                    d = (e1 * T[0] + 2 * m * Q - S[0], e2 * T[1] + 2 * n * Q - S[1])
                    rays.append((d[0] * d[0] + d[1] * d[1], d))
    rays.sort()
    for _, d in rays:
        if d != (0, 0) and trace(cells, S[0], S[1], d[0], d[1], Q) == T: return d
    return None

def candidates(cells, a, b):
    """Yield (S,T,Q,label): one sample per slide interval of each family allowed by Theorem X."""
    Q = 2 * 101 * abs(a) * abs(b)
    xs = [c[0] for c in cells]; ys = [c[1] for c in cells]
    x0, x1, y0_, y1_ = min(xs), max(xs) + 1, min(ys), max(ys) + 1
    hy = Q // (2 * abs(a)); hv = Q // (2 * abs(b))
    for Y in range(y0_ * Q + hy, y1_ * Q, hy):
        for V in range(y0_ * Q + hv, y1_ * Q, hv):
            if (a * Y + b * V) % Q or (a * Y - b * V) % Q: continue
            for i in range(x0, x1):
                for r in range(abs(a)):
                    X = i * Q + (r * 101 + 37) * 2 * abs(b)      # x = i + (r+37/101)/|a|
                    if not interior(cells, X, Y, Q): continue
                    for k in range(-abs(a) * (abs(x1) + abs(x0) + 1) - abs(b) * (abs(x1) + abs(x0) + 1),
                                   abs(a) * (abs(x1) + abs(x0) + 1) + abs(b) * (abs(x1) + abs(x0) + 1) + 1):
                        num = k * Q - a * X
                        if num % b: continue
                        U = num // b
                        if (U, V) == (X, Y) or not interior(cells, U, V, Q): continue
                        yield (X, Y), (U, V), Q, (a, b, k)

def simple(cells):
    xs = [c[0] for c in cells]; ys = [c[1] for c in cells]
    for (i, j) in cells:                       # no diagonal pinch
        for di, dj in ((1, 1), (1, -1)):
            if (i + di, j + dj) in cells and (i + di, j) not in cells and (i, j + dj) not in cells: return False
    box = {(i, j) for i in range(min(xs) - 1, max(xs) + 2) for j in range(min(ys) - 1, max(ys) + 2)} - cells
    seen, st = set(), [next(iter(box))]
    while st:
        p = st.pop()
        if p in seen: continue
        seen.add(p)
        for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            q = (p[0] + d[0], p[1] + d[1])
            if q in box and q not in seen: st.append(q)
    return len(seen) == len(box)

def polyominoes(nmax):
    norm = lambda s: frozenset((i - min(x for x, _ in s), j - min(y for _, y in s)) for i, j in s)
    level = {frozenset({(0, 0)})}; out = {1: level}
    for n in range(2, nmax + 1):
        nxt = set()
        for s in level:
            for (i, j) in s:
                for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    c = (i + d[0], j + d[1])
                    if c not in s: nxt.add(norm(s | {c}))
        level = nxt; out[n] = level
    return out

def plus_tree(centers):
    cells = set()
    for (i, j) in centers:
        cells |= {(2 * i, 2 * j), (2 * i + 1, 2 * j), (2 * i - 1, 2 * j), (2 * i, 2 * j + 1), (2 * i, 2 * j - 1)}
    return cells

def run(rooms, slopes, R, R2):
    tot = surv = 0
    for name, cells in rooms:
        cells = set(cells)
        for a, b in slopes:
            for S, T, Q, lab in candidates(cells, a, b):
                tot += 1
                if lit(cells, S, T, Q, R) is None and lit(cells, S, T, Q, R2) is None:
                    surv += 1
                    print("SURVIVOR", name, sorted(cells), lab, "S", S, "T", T, "Q", Q, flush=True)
    print("rooms", len(rooms), "slopes", slopes, "candidates", tot, "survivors", surv, "R", R, R2, flush=True)

if __name__ == "__main__":
    mode = sys.argv[1]
    unit = [(1, 1), (1, -1)]
    other = [(a, s * b) for a in (1, 2, 3) for b in (1, 2, 3) for s in (1, -1) if gcd(a, b) == 1 and (a, b) != (1, 1)]
    if mode == "poly":
        nmax = int(sys.argv[2]); P = polyominoes(nmax)
        rooms = [("poly%d" % n, s) for n in range(2, nmax + 1) for s in P[n] if simple(set(s))]
        run(rooms, unit, 3, 8)
    elif mode == "polyother":
        nmax = int(sys.argv[2]); P = polyominoes(nmax)
        rooms = [("poly%d" % n, s) for n in range(2, nmax + 1) for s in P[n] if simple(set(s))]
        run(rooms, other, 3, 8)
    elif mode == "plus":
        nmax = int(sys.argv[2]); P = polyominoes(nmax)
        rooms = []
        for n in range(1, nmax + 1):
            for s in P[n]:
                if not any({(i, j), (i + 1, j), (i, j + 1), (i + 1, j + 1)} <= s for (i, j) in s) and simple(set(s)):
                    rooms.append(("plus%d" % n, plus_tree(s)))
        run(rooms, unit if len(sys.argv) < 4 else other, 3, 8)
