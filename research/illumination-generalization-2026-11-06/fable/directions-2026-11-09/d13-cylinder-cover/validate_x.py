#!/usr/bin/env python3
"""Validation on class (i)/(ii) rooms: the live points of Theorem C must lie in
Part A's candidate set X.

Enumerates all strictly simple polyomino rooms with area <= AMAX (one per
symmetry class). For each room, computes in Python (cyl.labels) the one-
cylinder directions with 1 <= p, q <= B and
  X = intersection over those directions of
      {interior points on a singular line of both families},
which is the candidate set of Lemma A / Theorem B for these directions. Rooms
with no one-cylinder direction (class (iii)) are skipped. Then runs
`./cover2 B 1 ...` with COVER_PTS=1 and checks live points subset of X.

usage: python3 validate_x.py AMAX B
"""
import subprocess
import sys
from fractions import Fraction as Fr
from math import gcd

from cyl import labels, point_type


def rooms(amax):
    seen = set()
    out = []
    frontier = [frozenset([(0, 0)])]
    for n in range(1, amax + 1):
        nxt = set()
        for P in frontier:
            if n == amax:
                break
            for (a, b) in P:
                for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    c = (a + d[0], b + d[1])
                    if c not in P:
                        nxt.add(norm(P | {c}))
        for P in frontier:
            key = canon(P)
            if key not in seen:
                seen.add(key)
                if strictly_simple(P):
                    out.append(sorted(P))
        frontier = list(nxt)
    return out


def norm(P):
    mx = min(a for a, _ in P)
    my = min(b for _, b in P)
    return frozenset((a - mx, b - my) for a, b in P)


def canon(P):
    keys = []
    for sx in (1, -1):
        for sy in (1, -1):
            for sw in (False, True):
                Q = [((b, a) if sw else (a, b)) for a, b in P]
                Q = norm(frozenset((sx * a, sy * b) for a, b in Q))
                keys.append(tuple(sorted(Q)))
    return min(keys)


def strictly_simple(P):
    xs = [a for a, _ in P] + [a + 1 for a, _ in P]
    ys = [b for _, b in P] + [b + 1 for _, b in P]
    V = E = 0
    for x in range(min(xs), max(xs) + 1):
        for y in range(min(ys), max(ys) + 1):
            m = [(x - 1, y - 1) in P, (x, y - 1) in P, (x - 1, y) in P, (x, y) in P]
            if m == [True, False, False, True] or m == [False, True, True, False]:
                return False
            if any(m):
                V += 1
    edges = set()
    for (a, b) in P:
        edges |= {((a, b), (a + 1, b)), ((a, b), (a, b + 1)), ((a + 1, b), (a + 1, b + 1)), ((a, b + 1), (a + 1, b + 1))}
    E = len(edges)
    return V - E + len(P) == 1


def walls(P):
    return len({(a + dx, b + dy) for (a, b) in P for dx in (0, 1) for dy in (0, 1)
                if point_type(P, a + dx, b + dy) in ("convex", "reflex")})


def xset(P, B):
    X = None
    nd = 0
    for p in range(1, B + 1):
        for q in range(1, B + 1):
            if gcd(p, q) != 1:
                continue
            L = labels(P, p, q)
            if L.ncyl != 1:
                continue
            nd += 1
            # singular segments: (cell, k); a point lies on a singular leaf of a
            # family when some cell whose closure holds it has a singular line
            # of that family through it (lines are indexed per open cell)
            pl = {(c, k) for c in P for k, lab in L.plusline[c].items() if lab is None}
            mi = {(c, k) for c in P for k, lab in L.minusline[c].items() if lab is None}
            S = set()
            for (c1, k) in pl:
                for (c2, k2) in mi:
                    if abs(c1[0] - c2[0]) > 1 or abs(c1[1] - c2[1]) > 1:
                        continue
                    x, y = Fr(k + k2, 2 * q), Fr(k2 - k, 2 * p)
                    if all(c[0] <= x <= c[0] + 1 and c[1] <= y <= c[1] + 1 for c in (c1, c2)) and interior(P, x, y):
                        S.add((x, y))
            X = S if X is None else X & S
    return X, nd


def interior(P, x, y):
    if x.denominator == 1 and y.denominator == 1:
        return point_type(P, int(x), int(y)) == "interior"
    if x.denominator == 1:
        return (int(x) - 1, y.numerator // y.denominator) in P and (int(x), y.numerator // y.denominator) in P
    if y.denominator == 1:
        return (x.numerator // x.denominator, int(y) - 1) in P and (x.numerator // x.denominator, int(y)) in P
    return True


def main():
    amax, B = int(sys.argv[1]), int(sys.argv[2])
    rs = rooms(amax)
    data = []
    for P in rs:
        X, nd = xset(frozenset(P), B)
        if nd == 0:
            continue
        data.append((P, X))
    inp = "".join(f"{len(P)} {walls(frozenset(P))} " + " ".join(f"{a} {b}" for a, b in P) + "\n" for P, _ in data)
    res = subprocess.run(["./cover2", str(B), "1", "400000"], input=inp, capture_output=True, text=True,
                         env={"COVER_PTS": "1", "COVER_ALLDIRS": "1"})
    live = {}
    for ln in res.stderr.split("\n"):
        if ln.startswith("PT "):
            _, rid, pt = ln.split()
            x, y = pt.split(",")
            live.setdefault(int(rid), set()).add((Fr(x), Fr(y)))
    status = {}
    for ln in res.stdout.split("\n"):
        if ln.startswith("ROOM"):
            t = ln.split()
            status[int(t[1])] = t[4]
    nX = nL = bad = 0
    eq = 0
    for k, (P, X) in enumerate(data, start=1):
        L = live.get(k, set())
        nX += len(X)
        nL += len(L)
        if status[k] != "DONE" or not L <= X:
            bad += 1
            print("MISMATCH", P, status[k], sorted(L - X))
        eq += L == X
    print(f"rooms(class i/ii, area<={amax}) {len(data)}  sum|X| {nX}  sum|X'| {nL}  X'==X {eq}  X' not within X {bad}")


if __name__ == "__main__":
    main()
