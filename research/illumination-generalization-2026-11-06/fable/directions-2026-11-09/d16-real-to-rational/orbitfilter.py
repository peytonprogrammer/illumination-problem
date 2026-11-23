#!/usr/bin/env python3
"""Twist-escape filter (Lemma T' of reduction.md) on dpcover's live cells.

stdin: the DP_LIVE dump of dpcover for one room. argv: rooms file, room index.

Steps, all exact:
 1. Cross radius r: every live cell lies in {|x - nx| <= r} or {|y - ny| <= r}
    for a lattice point (nx, ny), except live cells that are single points of
    the grid Gamma = (1/Lv)Z x (1/Lh)Z. The script requires r < 1/3.
 2. D from Lemma T': if r < 1/4, D = lcm(Lh lcm(3, Lv), Lv lcm(3, Lh));
    otherwise D = lcm(Lh lcm(60, 2 Lv), Lv lcm(60, 2 Lh)). A point of a dark
    DP pair has both coordinates in (1/D)Z.
 3. LiveGrid: the points of (1/D)Z^2 in the closed live cells. LvGrid: their
    images in (Z/D)^2, closed under the sign changes of both coordinates.
 4. NE: the largest subset of LvGrid invariant under (x, y) -> (x + Lh y, y)
    and (x, y) -> (x, y + Lv x). A point of a dark DP pair projects into NE.
 5. Output: the points of LiveGrid over NE ("x y kind", kind = interior, wall).

With a third argument FILE, the script also writes a sample of dead grid points
for validate.py: up to 300 points of (1/D)Z^2 next to LiveGrid but outside it,
and up to 300 random points of the room outside LiveGrid.
"""
import random
import sys
from fractions import Fraction as Fr
from math import ceil, floor, lcm

from dplib import in_room, is_interior, is_vertex, read_rooms, twist_periods


def contains(V, i, j, N):
    """Is (i/N, j/N) in the closed convex hull of V (points (X, Y, d))?"""
    def cr(A, B):
        ax, ay = B[0] * A[2] - A[0] * B[2], B[1] * A[2] - A[1] * B[2]
        px, py = i * A[2] - A[0] * N, j * A[2] - A[1] * N
        c = ax * py - ay * px
        return (c > 0) - (c < 0)
    if len(V) == 1:
        return i * V[0][2] == V[0][0] * N and j * V[0][2] == V[0][1] * N
    if len(V) == 2:
        if cr(V[0], V[1]) != 0:
            return False
        A, B = V
        ax, ay = B[0] * A[2] - A[0] * B[2], B[1] * A[2] - A[1] * B[2]
        px, py = i * A[2] - A[0] * N, j * A[2] - A[1] * N
        if ax * px + ay * py < 0:
            return False
        return (px * px + py * py) * B[2] * B[2] <= (ax * ax + ay * ay) * N * N
    s = [cr(V[t], V[(t + 1) % len(V)]) for t in range(len(V))]
    return all(z >= 0 for z in s) or all(z <= 0 for z in s)


def main():
    cells = read_rooms(sys.argv[1])[int(sys.argv[2]) - 1]
    LH, LV = twist_periods(cells)
    polys = []
    cross = Fr(0)
    box = Fr(0)
    nexc = 0
    for line in sys.stdin:
        if not line.startswith("L "):
            continue
        V = []
        for z in line.split()[3:]:
            a, b = z.split(",")
            xn, xd = a.split("/")
            yn, yd = b.split("/")
            V.append((int(xn), int(yn), int(xd)))
        k = min(len(V), 3)
        cx = sum(Fr(v[0], v[2]) for v in V[:k]) / k
        cy = sum(Fr(v[1], v[2]) for v in V[:k]) / k
        nx, ny = floor(cx + Fr(1, 2)), floor(cy + Fr(1, 2))
        mx = max(Fr(abs(v[0] - nx * v[2]), v[2]) for v in V)
        my = max(Fr(abs(v[1] - ny * v[2]), v[2]) for v in V)
        box = max(box, mx, my)
        if len(V) == 1 and (LV * V[0][0]) % V[0][2] == 0 and (LH * V[0][1]) % V[0][2] == 0 and min(mx, my) >= Fr(1, 4):
            nexc += 1          # exceptional live point on the grid Gamma
        else:
            cross = max(cross, min(mx, my))
        polys.append(V)
    assert cross < Fr(1, 3), f"cross radius {cross} is not below 1/3"
    if cross < Fr(1, 4):
        D = lcm(LH * lcm(3, LV), LV * lcm(3, LH))
    else:
        D = lcm(LH * lcm(60, 2 * LV), LV * lcm(60, 2 * LH))
    live = set()
    for V in polys:
        x0 = min(Fr(v[0], v[2]) for v in V)
        x1 = max(Fr(v[0], v[2]) for v in V)
        y0 = min(Fr(v[1], v[2]) for v in V)
        y1 = max(Fr(v[1], v[2]) for v in V)
        for i in range(ceil(x0 * D), floor(x1 * D) + 1):
            for j in range(ceil(y0 * D), floor(y1 * D) + 1):
                if (i, j) not in live and contains(V, i, j, D):
                    live.add((i, j))
    lv = set()
    for (i, j) in live:
        for si in (1, -1):
            for sj in (1, -1):
                lv.add(((si * i) % D, (sj * j) % D))
    # greatest invariant subset
    ne = set(lv)
    work = list(ne)
    while work:
        z = work.pop()
        if z not in ne:
            continue
        i, j = z
        nb = (((i + LH * j) % D, j), ((i - LH * j) % D, j), (i, (j + LV * i) % D), (i, (j - LV * i) % D))
        if any(w not in ne for w in nb):
            ne.discard(z)
            work.extend(w for w in nb if w in ne)
    out = sorted((i, j) for (i, j) in live if (i % D, j % D) in ne)
    kinds = {}
    for (i, j) in out:
        P = (Fr(i, D), Fr(j, D))
        kinds[(i, j)] = "interior" if is_interior(cells, P) else "wall"
    nint = sum(1 for k in kinds.values() if k == "interior")
    print(f"# room {sys.argv[2]} Lh {LH} Lv {LV} live cells {len(polys)} box radius {box} cross radius {cross} "
          f"exceptional grid points {nexc} D {D} live grid points {len(live)} torus {len(lv)} "
          f"invariant {len(ne)} candidates {len(out)} interior {nint}")
    for (i, j) in out:
        print(Fr(i, D), Fr(j, D), kinds[(i, j)])
    if len(sys.argv) > 3:
        rng = random.Random(1)

        def ok(i, j):
            P = (Fr(i, D), Fr(j, D))
            return (i, j) not in live and in_room(cells, P) and not is_vertex(cells, P)
        near = set()
        for (i, j) in rng.sample(sorted(live), min(len(live), 3000)):
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                if ok(i + di, j + dj):
                    near.add((i + di, j + dj))
        near = rng.sample(sorted(near), min(len(near), 300))
        xs = [c[0] for c in cells]
        ys = [c[1] for c in cells]
        far = set()
        while len(far) < 300:
            i, j = rng.randrange(min(xs) * D, (max(xs) + 1) * D + 1), rng.randrange(min(ys) * D, (max(ys) + 1) * D + 1)
            if ok(i, j):
                far.add((i, j))
        with open(sys.argv[3], "w") as f:
            for (i, j) in near + sorted(far):
                f.write(f"{Fr(i, D)} {Fr(j, D)}\n")


if __name__ == "__main__":
    main()
