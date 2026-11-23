"""Cross-checks of shoot.c output against code written by other agents.

For a sample of rooms in a shoot output file (R/K/P lines):
  1. strict simplicity and W by the boundary walk in check_enum_small.py;
     r recounted; k recounted per class;
  2. B_min block count and N_min separation for every pair, recomputed with
     d2-factor-audit/room_model.py (pillow permutations lam, rho, the and its
     union-find closure under the group generators), origin at the pair class;
  3. every non-axis lit certificate replayed with d3-review/surface.py
     Surface.segment (Fraction arithmetic, the reviewer's own unfolding);
     axis certificates are replayed with a small grid-line walker here.
usage: python3 crosscheck.py shoot_output [every_nth]
"""
import sys
from fractions import Fraction as Fr

HERE = sys.path[0]
sys.path.insert(1, HERE + "/../d2-factor-audit")
sys.path.insert(2, HERE + "/../d3-review")
import room_model as rm                      # noqa: E402
import surface as d3                         # noqa: E402
from check_enum_small import boundary_walls  # noqa: E402


def opn(path):
    """Open a text file, or its gzip-compressed copy path + '.gz'."""
    import gzip
    import os
    if not os.path.exists(path) and os.path.exists(path + ".gz"):
        return gzip.open(path + ".gz", "rt")
    return open(path)


def around(cells, p):
    x, y = p
    return sum(c in cells for c in ((x - 1, y - 1), (x, y - 1), (x - 1, y), (x, y)))


def nmin_ref(cells, origin):
    """Return (#blocks, blk-of-cell) using room_model's closure."""
    cl, idx, lam, rho, the = rm.pillow_model(cells, origin)
    cp = rm.class_perms(lam, rho, the)
    seeds = [c for k in ("C1", "B", "C2") for c in rm.cycles(cp[k]) if len(c) == 2]
    part = rm.closure_partition(len(cl), (lam, rho, the), seeds)
    blk = {}
    for b, block in enumerate(part):
        for a in block:
            blk[cl[a]] = b
    return len(part), blk


def sep_ref(cells, blk, S, T):
    def cs(p):
        x, y = p
        return [(x - 1, y - 1), (x, y - 1), (x - 1, y), (x, y)]
    return not ({blk[c] for c in cs(S)} & {blk[c] for c in cs(T)})


def axis_walk(cells, S, d, m):
    (x, y), (ex, ey) = S, d
    for _ in range(m):
        nx, ny = x + ex, y + ey
        k = around(cells, (nx, ny))
        if k in (0, 1, 3):
            return None
        if k == 2:
            ex, ey = -ex, -ey
        x, y = nx, ny
    return (x, y)


def main():
    path = sys.argv[1]
    every = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    nroom = nchecked = npairs = ncert = 0
    bad = []
    room = None
    cur_cls = None
    for line in opn(path):
        f = line.split()
        if not f or f[0] == "#":
            continue
        if f[0] == "R":
            nroom += 1
            take = (nroom % every == 0)
            if not take:
                room = None
                continue
            area, W, r = int(f[2]), int(f[3]), int(f[4])
            v = list(map(int, f[5:]))
            cells = {(v[i], v[i + 1]) for i in range(0, len(v), 2)}
            room = (cells, area, W, r)
            nchecked += 1
            w2 = boundary_walls(cells)
            pts = {(x + a, y + b) for x, y in cells for a in (0, 1) for b in (0, 1)}
            r2 = sum(around(cells, p) == 3 for p in pts)
            if w2 != W or r2 != r or len(cells) != area or W != 2 * r + 4:
                bad.append(("geometry", f[1], W, w2, r, r2))
            ref_cache = {}
        elif f[0] == "K" and room is not None:
            cells = room[0]
            ox, oy, k, nb = map(int, f[1:5])
            pts = {(x + a, y + b) for x, y in cells for a in (0, 1) for b in (0, 1)}
            k2 = sum(1 for p in pts if ((p[0] - ox) % 2, (p[1] - oy) % 2) != (0, 0)
                     and around(cells, p) in (2, 4))
            nb2, blk = nmin_ref(cells, (ox, oy))
            ref_cache = blk
            cur_cls = (ox, oy)
            if k2 != k or nb2 != nb:
                bad.append(("class", f, k2, nb2))
        elif f[0] == "P" and room is not None:
            cells = room[0]
            S, T = (int(f[1]), int(f[2])), (int(f[3]), int(f[4]))
            npairs += 1
            sep = int(f[6])
            if sep_ref(cells, ref_cache, S, T) != bool(sep):
                bad.append(("sep", S, T, sep))
            if f[5] == "L":
                dx, dy, m = int(f[7]), int(f[8]), int(f[9])
                ncert += 1
                if dx == 0 or dy == 0:
                    end = axis_walk(cells, S, (dx, dy), m)
                    ok = end == T
                else:
                    srf = d3.Surface(cells)
                    end, ok, _ = srf.segment((Fr(S[0]), Fr(S[1])), (m * dx, m * dy))
                    ok = ok and end == (Fr(T[0]), Fr(T[1]))
                if not ok:
                    bad.append(("path", S, T, dx, dy, m, end))
    print(f"rooms in file {nroom}, checked {nchecked}, pairs {npairs}, certificates replayed {ncert}")
    print(f"mismatches: {len(bad)}")
    for b in bad[:20]:
        print("  ", b)


if __name__ == "__main__":
    main()
