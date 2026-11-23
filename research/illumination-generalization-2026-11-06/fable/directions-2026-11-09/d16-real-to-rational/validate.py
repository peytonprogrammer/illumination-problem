#!/usr/bin/env python3
"""Independent checks of dpcover's localization claim and of the certificate.

Check 1 (completeness of dead cells). dpcover reports LRAD = r: every live
source cell lies in the closed L-infinity box of radius r around a lattice
point. So a source S outside all boxes must have, for every target T and each
class, a direction with 1 <= p, q <= B whose cylinder through S+ contains the
target in its closure. The script recomputes that with cyl.labels for sampled
sources (generic, small denominators, wall points) and targets (small
denominators, points next to corners, wall points).

Check 2 (soundness). For sampled interior pairs and classes with a
certificate, the class-restricted exact shooter must find a billiard path.

Check 3. On wall points the plus and minus labels agree (S+ = S- in DP).

Check 4 (twists). For sampled interior pairs with a billiard path of unfolded
vector v0 ending on sheet e, and each of h, h^-1, v, v^-1: the image pair on M
must be joined by the path with vector (derivative of the twist) * v0, ending
on the image sheet. This tests dplib.twist, which twistcheck.py relies on.

With a sources file (lines "x y", from orbitfilter.py), check 1 uses these
sources instead: points that dpcover reports as dead.

usage: python3 validate.py rooms.txt ROOM_INDEX B R_NUM R_DEN [seed [box|cross [SOURCES]]]
"""
import random
import sys
from fractions import Fraction as Fr
from math import floor

from dplib import (Cert, in_room, is_interior, is_vertex, m_end, read_rooms, room_end, shoot_class, twist,
                   twist_periods)
from shoot import MSurf, images


CROSS = False


def near_lattice(P, r):
    """Box mode: P is in the box of radius r around a lattice point. Cross mode
    (for rooms that are only cross-localized): P is within r of a lattice line,
    or P is the centre of a cell."""
    dx, dy = abs(P[0] - round(P[0])), abs(P[1] - round(P[1]))
    if CROSS:
        return min(dx, dy) <= r or (dx == Fr(1, 2) and dy == Fr(1, 2))
    return dx <= r and dy <= r


def main():
    rooms = read_rooms(sys.argv[1])
    idx, B = int(sys.argv[2]), int(sys.argv[3])
    r = Fr(int(sys.argv[4]), int(sys.argv[5]))
    rng = random.Random(int(sys.argv[6]) if len(sys.argv) > 6 else 1)
    cells = rooms[idx - 1]
    global CROSS
    CROSS = len(sys.argv) > 7 and sys.argv[7] == "cross"
    C = Cert(cells, B)
    xs = [c[0] for c in cells]
    ys = [c[1] for c in cells]
    x0, x1, y0, y1 = min(xs), max(xs) + 1, min(ys), max(ys) + 1

    def grid(d):
        return [(Fr(i, d), Fr(j, d)) for i in range(x0 * d, x1 * d + 1) for j in range(y0 * d, y1 * d + 1)
                if in_room(cells, (Fr(i, d), Fr(j, d))) and not is_vertex(cells, (Fr(i, d), Fr(j, d)))]

    # sources outside the boxes
    sources = []
    for d in (2, 3, 4, 5, 7):
        sources += [P for P in grid(d) if not near_lattice(P, r)]
    big = 1009
    while len(sources) < 400 + len(grid(2)):
        P = (Fr(rng.randrange(x0 * big, x1 * big), big), Fr(rng.randrange(y0 * big, y1 * big), big))
        if in_room(cells, P) and not near_lattice(P, r):
            sources.append(P)
    # just outside the boxes, on the lattice lines and on the diagonals
    eps = r + Fr(1, 997)
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            for dx, dy in ((eps, 0), (-eps, 0), (0, eps), (0, -eps), (eps, eps), (eps, -eps), (-eps, eps), (-eps, -eps),
                           (eps, Fr(1, 91)), (Fr(1, 91), eps)):
                P = (x + dx, y + dy)
                if in_room(cells, P) and not near_lattice(P, r):
                    sources.append(P)
    sources = sorted(set(sources))
    if len(sys.argv) > 8:
        sources = sorted({(Fr(t[0]), Fr(t[1])) for t in (l.split() for l in open(sys.argv[8])) if len(t) == 2})
    # targets: small grid, wall points, points next to every lattice point
    targets = grid(3) + grid(4)
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            for dx in (-3, -1, 0, 1, 3):
                for dy in (-2, -1, 0, 1, 2):
                    P = (x + Fr(dx, 1013), y + Fr(dy, 1013))
                    if in_room(cells, P) and not is_vertex(cells, P):
                        targets.append(P)
    targets = sorted(set(targets))
    nwall = sum(1 for P in sources if not is_interior(cells, P))
    print(f"room {idx}: B {B} radius {r} sources {len(sources)} (wall {nwall}) targets {len(targets)}", flush=True)

    # check 3
    bad3 = 0
    for S in sources:
        if is_interior(cells, S):
            continue
        for d in C.dirs:
            lp, lm = C.source_labels(d, S)
            if lp != lm:
                bad3 += 1
    print(f"check 3 (plus label = minus label on wall sources): mismatches {bad3}", flush=True)

    # check 1
    fail = 0
    worst = (0, None)
    npairs = 0
    for S in sources:
        for T in targets:
            if T == S:
                continue
            for cls in (0, 1):
                npairs += 1
                d = C.one_sided(S, T, cls)
                if d is None:
                    fail += 1
                    if fail <= 10:
                        print("  UNCERTIFIED", S, T, "par" if cls == 0 else "cross")
                elif max(d) > worst[0]:
                    worst = (max(d), (S, T, cls, d))
    print(f"check 1: triples {npairs} uncertified {fail} largest max(p,q) used {worst[0]}", flush=True)

    Msurf = MSurf(cells)
    # check 2
    inter = [P for P in sources if is_interior(cells, P)]
    tint = [P for P in targets if is_interior(cells, P)]
    bad2 = tested = 0
    for _ in range(300):
        S, T, cls = rng.choice(inter), rng.choice(tint), rng.randrange(2)
        if S == T:
            continue
        d = C.one_sided(S, T, cls)
        if d is None:
            continue
        tested += 1
        v = shoot_class(cells, S, T, 4 * max(d) + 8, cls, Msurf)
        if v is None:
            bad2 += 1
            print("  CERTIFIED BUT NO PATH", S, T, cls, d)
    print(f"check 2: certified triples shot {tested}, without a path {bad2}", flush=True)

    # check 4
    LH, LV = twist_periods(cells)
    tested = bad4 = 0
    gens = [(True, LH, 1), (True, LH, -1), (False, LV, 1), (False, LV, -1)]
    while tested < 400:
        S = (Fr(rng.randrange(x0 * 60, x1 * 60), 60), Fr(rng.randrange(y0 * 60, y1 * 60), 60))
        T = (Fr(rng.randrange(x0 * 84, x1 * 84), 84), Fr(rng.randrange(y0 * 84, y1 * 84), 84))
        if S == T or not is_interior(cells, S) or not is_interior(cells, T):
            continue
        for v0 in images(S, T, 3):
            if v0[0] == 0 or v0[1] == 0:
                continue
            a = room_end(cells, S, v0)
            if a is None or a[0] != T:
                continue
            e = a[1]
            for hor, lam, sg in gens:
                s2 = twist(cells, (S[0], S[1], 1, 1), hor, lam, sg)
                t2 = twist(cells, (T[0], T[1], e[0], e[1]), hor, lam, sg)
                S2, T2 = (s2[0], s2[1]), (t2[0], t2[1])
                if not is_interior(cells, S2) or not is_interior(cells, T2):
                    continue
                w = (v0[0] + sg * lam * v0[1], v0[1]) if hor else (v0[0], v0[1] + sg * lam * v0[0])
                w = (s2[2] * w[0], s2[3] * w[1])          # room vector at the image source
                if w[0] == 0 or w[1] == 0:
                    continue
                tested += 1
                r1, r2 = room_end(cells, S2, w), m_end(Msurf, S2, w)
                want = (s2[2] * t2[2], s2[3] * t2[3])
                if r1 is None or r2 is None or r1[0] != T2 or r1[1] != want or r2 != want:
                    bad4 += 1
                    if bad4 <= 5:
                        print("  TWIST MISMATCH", S, T, v0, hor, sg, s2, t2, w, r1, r2)
            break
    print(f"check 4: twisted paths tested {tested}, mismatches {bad4}", flush=True)


if __name__ == "__main__":
    main()
