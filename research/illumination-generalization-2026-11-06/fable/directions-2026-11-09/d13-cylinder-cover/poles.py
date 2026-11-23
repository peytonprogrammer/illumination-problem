#!/usr/bin/env python3
"""Pole-pair test: for each pair of convex corners (poles of DP), list the
directions in which one DP cylinder touches both poles.

A convex corner c is the vertex of exactly one cell; the DP cylinder D_theta(c)
adjacent to the pole is the label of any point of that cell close enough to c
(Lemma P in theory.md). We read it from the face of the cell that has c as a
vertex: for p, q >= 1 the plus strip and minus strip at the corner.

usage: python3 poles.py B < rooms   (lines "C3 area W x0 y0 ...")
prints one line per room: area W obstructed_pairs total_pairs cells
"""
import sys
from math import gcd

from cyl import labels, point_type


def convex_corners(cells):
    out = []
    for (a, b) in cells:
        for dx in (0, 1):
            for dy in (0, 1):
                P = (a + dx, b + dy)
                if point_type(cells, *P) == "convex":
                    out.append((P, (a, b)))
    return sorted(out)


def pole_label(L, P, cell, p, q):
    """Cylinder adjacent to the pole P (a corner of cell)."""
    a, b = cell
    x, y = P
    # strip of each family next to the corner, inside the cell
    # plus value q x - p y at the corner; moving into the cell by (dx, dy)
    dx = 1 if x == a else -1
    dy = 1 if y == b else -1
    u = q * x - p * y
    v = q * x + p * y
    # direction into the cell changes u by q*dx - p*dy (nonzero sign unless 0)
    du = q * dx - p * dy
    dv = q * dx + p * dy
    # choose the family whose value moves off the line strictly
    if dv != 0:
        k = v if dv > 0 else v - 1
        return L.minus[cell][k]
    k = u if du > 0 else u - 1
    return L.plus[cell][k]


def directions(B):
    ds = [(p, q) for p in range(1, B + 1) for q in range(1, B + 1) if gcd(p, q) == 1]
    ds.sort(key=lambda d: (d[0] + d[1], d))
    return ds


def obstructed_pairs(cells, B):
    cells = frozenset(cells)
    cc = convex_corners(cells)
    n = len(cc)
    shared = [[False] * n for _ in range(n)]
    for (p, q) in directions(B):
        L = labels(cells, p, q)
        lab = [pole_label(L, P, c, p, q) for P, c in cc]
        for i in range(n):
            for j in range(i + 1, n):
                if lab[i] == lab[j]:
                    shared[i][j] = True
    return [(cc[i][0], cc[j][0]) for i in range(n) for j in range(i + 1, n) if not shared[i][j]], n * (n - 1) // 2


if __name__ == "__main__":
    B = int(sys.argv[1])
    for line in sys.stdin:
        t = line.split()
        if not t or t[0] != "C3":
            continue
        A, W = int(t[1]), int(t[2])
        v = list(map(int, t[3:]))
        cells = [(v[2 * i], v[2 * i + 1]) for i in range(A)]
        obs, tot = obstructed_pairs(cells, B)
        print(A, W, len(obs), tot, " ".join(f"{a},{b}" for a, b in cells), "|", " ".join(f"{P}-{Q}".replace(" ", "") for P, Q in obs), flush=True)
