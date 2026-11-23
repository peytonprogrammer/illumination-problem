#!/usr/bin/env python3
"""d96 referee test: cover.c certificates against brute-force exact tracing.

For each named room, sample random real-mark pairs (S, T) of distinct interior
points with exact rational coordinates: generic points, points on interior cell
edges, points on lines q x -/+ p y = k (p, q <= B, the candidate singular and
boundary lines), and interior lattice points. Ask cover.c (through harness.c,
which reuses cover.c's own functions) whether Ill_Theta(S) contains T. For every
certified pair, search a legal billiard path exhaustively over unfolded images
t' = (e1 Tx + 2m, e2 Ty + 2n) by increasing length, with the d87 tracer
(billiard.py); confirm each found path with trace2, a second tracer written here.

usage: python3 -B test.py SEED NPAIRS B RMAX
"""
import random
import subprocess
import sys
from fractions import Fraction as F
from math import gcd, isqrt

HERE = sys.path[0]
D = HERE + "/.."
sys.path.insert(0, D + "/d87-review-cross-corners")
import billiard  # noqa: E402


def trace2(cells, S, v):
    """Second tracer (written here). Follow S + t v, t in (0, 1], in the room.
    Return the endpoint, or None if a corner (1 or 3 cells) is touched.
    Between events the open segment lies in one closed cell; at a wall the
    normal velocity component flips."""
    x, y = S
    vx, vy = v
    t = F(0)
    def cnt(X, Y):
        return sum((X - i, Y - j) in cells for i in (0, 1) for j in (0, 1))
    while True:
        cand = []
        if vx:
            X = (x.numerator // x.denominator) + (1 if vx > 0 else 0) if x.denominator > 1 else x + (1 if vx > 0 else -1)
            cand.append((X - x) / vx)
        if vy:
            Y = (y.numerator // y.denominator) + (1 if vy > 0 else 0) if y.denominator > 1 else y + (1 if vy > 0 else -1)
            cand.append((Y - y) / vy)
        dt = min(cand)
        if t + dt >= 1:
            x, y = x + vx * (1 - t), y + vy * (1 - t)
            return (x, y)
        t += dt
        x, y = x + vx * dt, y + vy * dt
        if x.denominator == 1 and y.denominator == 1:
            k = cnt(x, y)
            if k in (1, 3):
                return None
            if k == 4:
                continue
            # flat point: the cell ahead is missing; reflect across the wall
            if vx == 0 or vy == 0:
                vx, vy = -vx, -vy
                continue
            ax = x if vx > 0 else x - 1
            ay = y if vy > 0 else y - 1
            assert (ax, ay) not in cells
            if (ax, ay - (1 if vy > 0 else -1)) in cells:
                vy = -vy  # the cell ahead in x, same row as before, is present: horizontal wall
            else:
                vx = -vx
            continue
        if x.denominator == 1:
            col = x if vx > 0 else x - 1
            row = y.numerator // y.denominator
            if (col, row) not in cells:
                vx = -vx
        else:
            row = y if vy > 0 else y - 1
            col = x.numerator // x.denominator
            if (col, row) not in cells:
                vy = -vy

ROOMS = {}
for line in open(HERE + "/rooms.txt"):
    tok = line.split()
    nums = list(map(int, tok[1:]))
    ROOMS[tok[0]] = (nums[0], nums[1], [(nums[2 + 2 * i], nums[3 + 2 * i]) for i in range(nums[0])])


def interior(cells, x, y):
    xs = [x.numerator // x.denominator] if x.denominator > 1 else [int(x) - 1, int(x)]
    ys = [y.numerator // y.denominator] if y.denominator > 1 else [int(y) - 1, int(y)]
    return all((a, b) in cells for a in xs for b in ys)


def rnd_frac(rng):
    den = rng.randint(101, 997)
    return F(rng.randint(1, den - 1), den)


def sample(rng, cells, B, kind):
    cl = sorted(cells)
    while True:
        a, b = rng.choice(cl)
        if kind == "G":
            x, y = a + rnd_frac(rng), b + rnd_frac(rng)
        elif kind == "E":
            if rng.random() < 0.5:
                x, y = F(a + 1), b + rnd_frac(rng)
            else:
                x, y = a + rnd_frac(rng), F(b + 1)
        elif kind == "V":
            x, y = F(a + 1), F(b + 1)
        else:  # "L": on q x - s p y = k
            p, q = rng.randint(1, B), rng.randint(1, B)
            if gcd(p, q) != 1:
                continue
            sg = rng.choice((1, -1))
            y = b + rnd_frac(rng) if rng.random() < 0.8 else F(b + rng.randint(0, 1))
            lo, hi = q * a - sg * p * y, q * (a + 1) - sg * p * y
            klo, khi = int(lo) + 1 if lo.denominator == 1 else -(-lo.numerator // lo.denominator), hi.numerator // hi.denominator
            ks = [k for k in range(int(klo), int(khi) + 1) if lo < k < hi]
            if not ks:
                continue
            k = rng.choice(ks)
            x = (k + sg * p * y) / q
        if interior(cells, x, y):
            return (x, y)


def images(T, R):
    tx, ty = T
    out = []
    for e1 in (1, -1):
        for e2 in (1, -1):
            for m in range(-R, R + 1):
                for n in range(-R, R + 1):
                    out.append((e1 * tx + 2 * m, e2 * ty + 2 * n))
    return out


def find_path(cells, S, T, R):
    cand = images(T, R)
    cand.sort(key=lambda t: (t[0] - S[0]) ** 2 + (t[1] - S[1]) ** 2)
    for t in cand:
        v = (t[0] - S[0], t[1] - S[1])
        if v == (0, 0) or v[0] ** 2 + v[1] ** 2 > R * R:
            continue
        try:
            r = billiard.run(cells, S, v, F(1))
        except RuntimeError:
            continue
        if r["ok"] and r["end"] == (T[0], T[1]):
            assert trace2(cells, S, v) == (T[0], T[1]), ("tracers disagree", S, T, v)
            return v
    return None


def main():
    seed, npairs, B, R = map(int, sys.argv[1:5])
    rng = random.Random(seed)
    kinds = ["G", "G", "E", "L", "L", "L", "V"]
    tot = {}
    for name, (area, W, cl) in ROOMS.items():
        cells = set(cl)
        pairs = []
        while len(pairs) < npairs:
            S = sample(rng, cells, B, rng.choice(kinds))
            T = sample(rng, cells, B, rng.choice(kinds + ["L", "L"]))
            if S != T and not (S[0].denominator == S[1].denominator == T[0].denominator == T[1].denominator == 1):
                pairs.append((S, T))
        inp = "%d %d %s\n" % (area, W, " ".join("%d %d" % c for c in cl))
        for S, T in pairs:
            d1 = S[0].denominator * S[1].denominator // gcd(S[0].denominator, S[1].denominator)
            d2 = T[0].denominator * T[1].denominator // gcd(T[0].denominator, T[1].denominator)
            inp += "%d %d %d %d %d %d\n" % (S[0] * d1, S[1] * d1, d1, T[0] * d2, T[1] * d2, d2)
        out = subprocess.run([HERE + "/harness", str(B)], input=inp, capture_output=True, text=True, check=True).stdout.split("\n")
        ncert = nfound = 0
        fails = []
        for (S, T), res in zip(pairs, out):
            if not res.startswith("CERT"):
                continue
            ncert += 1
            v = find_path(cells, S, T, R)
            if v is None:
                fails.append((S, T, res))
            else:
                nfound += 1
        print("%s B=%d pairs %d certified %d path_found %d not_found %d" % (name, B, len(pairs), ncert, nfound, len(fails)), flush=True)
        for S, T, res in fails:
            print("  NOTFOUND S=(%s,%s) T=(%s,%s) %s" % (S[0], S[1], T[0], T[1], res), flush=True)
        tot[name] = (len(pairs), ncert, nfound, len(fails))
    print("TOTAL", tot)


if __name__ == "__main__":
    main()
