"""Independent enumeration of order types of strictly simple orthogonal
polygons with r = 0, 1, 2 reflex corners.

Method (differs from d15-small-r/enum_types.c and check_types.py, which
enumerate cell subsets): enumerate closed vertex walks with alternating
horizontal and vertical edges on the integer grid {0..r+1}^2, keep the simple
ones, compress coordinates to ranks, and canonicalize under the 8 symmetries.

Also classifies each type by its cyclic turn sequence, counts position types
and position-type pairs, and compares with the author's types_r*.txt and
cert_r*.json.

Usage: python3 -B enum_check.py
"""
import json
import os
import sys
from itertools import product

HERE = os.path.dirname(os.path.abspath(__file__))
AUTH = os.path.join(HERE, "..", "d15-small-r")


def seg_points(a, b):
    """Lattice points of the closed axis-parallel segment ab."""
    (x0, y0), (x1, y1) = a, b
    if x0 == x1:
        return {(x0, y) for y in range(min(y0, y1), max(y0, y1) + 1)}
    return {(x, y0) for x in range(min(x0, x1), max(x0, x1) + 1)}


def simple(vs):
    """Strictly simple: lattice points of edges are disjoint except shared
    end points of consecutive edges. (All coordinates are integers, so two
    edges that meet do so at a lattice point.)"""
    n = len(vs)
    edges = [seg_points(vs[i], vs[(i + 1) % n]) for i in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            common = edges[i] & edges[j]
            if j == i + 1:
                if common != {vs[j]}:
                    return False
            elif i == 0 and j == n - 1:
                if common != {vs[0]}:
                    return False
            elif common:
                return False
    return True


def walks(W, N):
    """All closed alternating walks with W vertices on {0..N}^2, first edge horizontal."""
    out = []

    def rec(vs):
        k = len(vs)
        if k == W:
            # closing edge is vertical (W even, first edge horizontal)
            if vs[-1][0] == vs[0][0] and vs[-1][1] != vs[0][1]:
                out.append(tuple(vs))
            return
        x, y = vs[-1]
        if k % 2 == 1:      # next edge horizontal
            for nx_ in range(N + 1):
                if nx_ != x:
                    rec(vs + [(nx_, y)])
        else:
            for ny_ in range(N + 1):
                if ny_ != y:
                    rec(vs + [(x, ny_)])

    for x0, y0 in product(range(N + 1), repeat=2):
        for x1 in range(N + 1):
            if x1 != x0:
                rec([(x0, y0), (x1, y0)])
    return out


def inside_cells(vs, nx, ny):
    """Cells (i, j) of the rank grid whose center is inside the polygon (even-odd rule)."""
    n = len(vs)
    cells = set()
    for i in range(nx):
        for j in range(ny):
            cx, cy = i + 0.5, j + 0.5
            cnt = 0
            for k in range(n):
                (x0, y0), (x1, y1) = vs[k], vs[(k + 1) % n]
                if x0 == x1 and x0 > cx and min(y0, y1) < cy < max(y0, y1):
                    cnt += 1
            if cnt % 2:
                cells.add((i, j))
    return frozenset(cells)


def canon(nx, ny, cells):
    best = None
    for tr in (0, 1):
        for fx in (0, 1):
            for fy in (0, 1):
                out = []
                for (i, j) in cells:
                    a = nx - 1 - i if fx else i
                    b = ny - 1 - j if fy else j
                    out.append((b, a) if tr else (a, b))
                dims = (ny, nx) if tr else (nx, ny)
                key = (dims, tuple(sorted(out)))
                if best is None or key < best:
                    best = key
    return best


def turn_class(vs):
    """Cyclic gaps between reflex corners (sorted) for a simple polygon."""
    n = len(vs)
    area2 = sum(vs[i][0] * vs[(i + 1) % n][1] - vs[(i + 1) % n][0] * vs[i][1] for i in range(n))
    turns = []
    for i in range(n):
        a, b, c = vs[i - 1], vs[i], vs[(i + 1) % n]
        cr = (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])
        turns.append('L' if (cr > 0) == (area2 > 0) else 'R')
    idx = [i for i, t in enumerate(turns) if t == 'R']
    gaps = tuple(sorted((idx[(k + 1) % len(idx)] - idx[k]) % n or n for k in range(len(idx)))) if idx else ()
    return gaps


def show(nx, ny, cells):
    return "/".join("".join("#" if (i, j) in cells else "." for i in range(nx)) for j in reversed(range(ny)))


def interior_types(nx, ny, cells):
    out = []
    for X in range(2 * nx + 1):
        for Y in range(2 * ny + 1):
            xs = [X // 2] if X % 2 else [X // 2 - 1, X // 2]
            ys = [Y // 2] if Y % 2 else [Y // 2 - 1, Y // 2]
            if all((i, j) in cells for i in xs for j in ys):
                out.append((X, Y))
    return out


def main():
    grand_pairs = 0
    for r in (0, 1, 2):
        W = 2 * r + 4
        types = {}
        for vs in walks(W, r + 1):
            if not simple(vs):
                continue
            xs = sorted({v[0] for v in vs})
            ys = sorted({v[1] for v in vs})
            rk = [(xs.index(x), ys.index(y)) for x, y in vs]
            nx, ny = len(xs) - 1, len(ys) - 1
            cells = inside_cells(rk, nx, ny)
            key = canon(nx, ny, cells)
            types.setdefault(key, set()).add(turn_class(vs))
        # author's list
        auth = set()
        for line in open(os.path.join(AUTH, f"types_r{r}.txt")):
            nx, ny, Wa, mask = map(int, line.split())
            cells = frozenset((i, j) for j in range(ny) for i in range(nx) if (mask >> (i + nx * j)) & 1)
            auth.add(canon(nx, ny, cells))
        mine = set(types)
        print(f"r={r}: my order types {len(mine)}, author's {len(auth)}, "
              f"only mine {len(mine - auth)}, only author's {len(auth - mine)}")
        cert = {tuple(sorted((c['nx'], c['ny']))) + (c['shape'],): c
                for c in json.load(open(os.path.join(AUTH, f"cert_r{r}.json")))}
        tot = 0
        for key in sorted(mine):
            (nx, ny), cl = key
            cells = set(cl)
            pts = interior_types(nx, ny, cells)
            npt = len(pts)
            ngrid = sum(1 for (X, Y) in pts if X % 2 == 0 and Y % 2 == 0)
            pairs = npt * (npt + 1) // 2 - ngrid
            tot += pairs
            print(f"   {nx}x{ny} {show(nx, ny, cells):14s} reflex gaps {sorted(types[key])} "
                  f"position types {npt} (of which interior grid points {ngrid}) pairs {pairs}")
        apairs = sum(sum(c['counts'].values()) + len(c['uncovered'])
                     for c in json.load(open(os.path.join(AUTH, f"cert_r{r}.json"))))
        print(f"   position-type pairs: mine {tot}, author's {apairs}")
        grand_pairs += tot
    print("total pairs r<=2:", grand_pairs)


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    main()
