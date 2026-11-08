"""Stage A of the bounded mirror-room enumeration (Daniel approved 2026-11-02: "ok do 1 then 2").

Section 33 coordinates: pocket B=(1,1), A=(2,0), C=(1,0); portal x=1, 0<y<1. Start from the literal
pocket alone (pocket-detection.md Section 1): the leaf triangle, the triangle across its portal, and
the straight walls past B and past C. Trace one ray of the mirror band (Section 10.1: every ray of the
family shares one itinerary), from (1,1/3) with velocity (-1,-1). At every undecided cell the ray
enters, branch on "in the room" or "out" (a wall). A diagonal wall ends the branch: the room isn't a
diagonal mirror. After each decision, local raw-fan propagation runs at every touched lattice point.
A branch closes when the ray re-enters the portal: it is a mirror band exactly when it returns to the
start point with velocity (1,-1). A branch whose ray enters a square outside the box is counted as
escaped, never dropped silently. Parameters are fixed below: box half-width R and crossing cap.
"""
import json
import math
import sys
from fractions import Fraction as F

R = int(sys.argv[1])          # box: squares i in [1-R, R], j in [-R, R-1]
CAP = 2000                    # crossing cap per branch (safety; hits are reported)
Y0 = F(1, 3)


def key(x, y):
    i, j = math.floor(x), math.floor(y)
    d = (x - y) - (i - j) if (i - j) % 2 == 0 else (x + y) - (i + j + 1)
    assert d != 0
    return (i, j, d > 0)


def verts(k):
    i, j, s = k
    if (i - j) % 2 == 0:
        return ((i, j), (i + 1, j), (i + 1, j + 1)) if s else ((i, j), (i + 1, j + 1), (i, j + 1))
    return ((i + 1, j), (i + 1, j + 1), (i, j + 1)) if s else ((i, j), (i + 1, j), (i, j + 1))


def ptype(p):
    return "A" if p[0] % 2 == 0 and p[1] % 2 == 0 else "B" if p[0] % 2 and p[1] % 2 else "C"


_AT = {}


def tris_at(p):
    """Canonical triangles with vertex p, counterclockwise by centroid angle."""
    if p not in _AT:
        out = []
        for i in (p[0] - 1, p[0]):
            for j in (p[1] - 1, p[1]):
                for s in (False, True):
                    k = (i, j, s)
                    if p in verts(k):
                        c = [sum(v[t] for v in verts(k)) / 3 - p[t] for t in (0, 1)]
                        out.append((math.atan2(c[1], c[0]) % (2 * math.pi), k))
        _AT[p] = [k for _, k in sorted(out)]
    return _AT[p]


def masks(n, sizes):
    out = [0]
    for m in sizes:
        if m == n:
            out.append((1 << n) - 1)
            continue
        for st in range(n):
            out.append(sum(1 << ((st + t) % n) for t in range(m)))
    return out


ALLOWED = {"A": masks(8, range(1, 9)), "B": masks(8, [1, 2, 3, 5, 6, 7]), "C": masks(4, [1, 3])}


def propagate(asg, points):
    """Raw local fans: one contiguous sector; B not 180/360; C only 90/270. Returns False on conflict."""
    work = list(points)
    while work:
        p = work.pop()
        ks = tris_at(p)
        ok = [m for m in ALLOWED[ptype(p)]
              if all(asg.get(k) is None or asg[k] == (m >> b & 1) for b, k in enumerate(ks))]
        if not ok:
            return False
        for b, k in enumerate(ks):
            if asg.get(k) is None:
                vals = {m >> b & 1 for m in ok}
                if len(vals) == 1:
                    asg[k] = vals.pop()
                    work.extend(verts(k))
    return True


def next_crossing(z, v):
    best = None
    vals = [(z[0], v[0], 1), (z[1], v[1], 1), (z[0] - z[1], v[0] - v[1], 2), (z[0] + z[1], v[0] + v[1], 2)]
    for fam, (f, df, step) in enumerate(vals):
        if df == 0:
            continue
        target = (math.floor(f / step) + 1) * step if df > 0 else (math.ceil(f / step) - 1) * step
        t = F(target - f) / df
        if best is None or t < best[0]:
            best = (t, fam, False)
        elif t == best[0]:
            best = (t, fam, True)
    assert not best[2]
    return best[0], best[1]


REFLECT = {0: lambda v: (-v[0], v[1]), 1: lambda v: (v[0], -v[1])}


def in_box(k):
    return 1 - R <= k[0] <= R and -R <= k[1] <= R - 1


def initial():
    asg = {}
    pocket = key(F(4, 3), F(1, 3))
    for k in tris_at((2, 0)):
        asg[k] = int(k == pocket)
    near = lambda x, y: key(F(x), F(y))
    asg[near("0.9", "0.5")] = 1                     # across the portal
    asg[near("0.9", "1.5")] = 1                     # left of the wall past B
    asg[near("1.1", "1.5")] = 0                     # right of the wall past B
    asg[near("0.9", "-0.5")] = 1                    # left of the wall past C
    assert verts(pocket) == ((1, 0), (2, 0), (1, 1))
    pts = {p for k in asg for p in verts(k)}
    assert propagate(asg, pts)
    return asg


stats = {"closed": 0, "not_mirror_return": 0, "diagonal_wall": 0, "escaped": 0, "conflict": 0, "cap": 0}
bands = []


def explore(z, v, asg, walls, steps):
    start = ((1, Y0), (-1, -1))
    while True:
        steps += 1
        if steps > CAP:
            stats["cap"] += 1
            return
        t1, fam = next_crossing(z, v)
        p = (z[0] + t1 * v[0], z[1] + t1 * v[1])
        if fam == 0 and p[0] == 1 and 0 < p[1] < 1 and v[0] > 0:
            if p == start[0] and v == (1, -1):
                stats["closed"] += 1
                bands.append({"crossings": steps, "walls": walls, "asg": dict(asg)})
            else:
                stats["not_mirror_return"] += 1
            return
        t2, _ = next_crossing(p, v)
        k = key(p[0] + t2 / 2 * v[0], p[1] + t2 / 2 * v[1])
        if not in_box(k):
            stats["escaped"] += 1
            return
        val = asg.get(k)
        if val is None:
            choices = [1] if fam in (2, 3) else [1, 0]
            for c in choices:
                a2 = dict(asg)
                a2[k] = c
                if propagate(a2, verts(k)):
                    explore(z, v, a2, list(walls), steps - 1)
                else:
                    stats["conflict"] += 1
            if fam in (2, 3):
                stats["diagonal_wall"] += 1   # the "out" choice at a diagonal ends the branch
            return
        if val == 1:
            z = p
            continue
        if fam in (2, 3):
            stats["diagonal_wall"] += 1
            return
        walls.append((fam, str(p[0]), str(p[1])))
        v = REFLECT[fam](v)
        z = p


def shape33(asg):
    """Section 33's local shape: full fan at (0,0), square [0,1]x[1,2], leaf at (0,-2)."""
    fan = [asg.get(k) for k in tris_at((0, 0))]
    sq = [asg.get(key(F(1, 3), F(4, 3))), asg.get(key(F(2, 3), F(5, 3)))]
    leaf = key(F(1, 3), F(-4, 3))
    lf = [asg.get(k) for k in tris_at((0, -2))]
    lf_ok = None if None in lf else all(x == int(k == leaf) for x, k in zip(lf, tris_at((0, -2))))
    return {"fan00_full": None if None in fan else all(fan), "square_0_1x1_2": None if None in sq else all(sq),
            "leaf_0_m2": lf_ok}


def main():
    asg = initial()
    sys.setrecursionlimit(100000)
    explore((F(1), Y0), (-1, -1), asg, [], 0)
    out = []
    for b in bands:
        tris_in = sorted(k for k, x in b["asg"].items() if x == 1)
        out.append({"crossings": b["crossings"], "wall_hits": b["walls"], "n_in": len(tris_in),
                    "tris_in": [list(verts(k)) for k in tris_in],
                    "tris_out": [list(verts(k)) for k, x in sorted(b["asg"].items()) if x == 0],
                    "shape33": shape33(b["asg"])})
    json.dump({"R": R, "cap": CAP, "y0": str(Y0), "stats": stats, "bands": out}, open(f"mirror_bands_R{R}.json", "w"))
    print(f"R={R} stats={stats}")
    for i, b in enumerate(out):
        print(f"  band {i}: crossings={b['crossings']} wall_hits={len(b['wall_hits'])} decided_in={b['n_in']} shape33={b['shape33']}")


if __name__ == "__main__":
    main()
