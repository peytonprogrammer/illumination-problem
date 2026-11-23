"""d97: independent check of the d68 counting identity and the corner-only area bound.

For each named room and each parity class y in {0,1}^2, classify every class-y lattice point
by its cell incidence k = number of unit cells of the room among the 4 around it:
  k=1 convex corner, k=3 reflex corner, k=4 interior, k=2 split into smooth (edge-adjacent
  cells) and pinch (diagonal cells). Then check n = cvx + 2 smooth + 2 pinch + 3 rfx + 4 int.
Also check v - r = 4 (strictly simple), W = 2r + 4, and the corner-only bound n <= 4r + 4.
Rooms: R22 (d8 rooms.json first), crosses P_b b=7,9 (BB/cross-placement.md), U2 (d84
indep.py), 10 census rooms (first room at each of 10 areas in qclass-closure/witnesses.txt.gz),
plus one deliberately pinched control shape (not a room) to show what pinches do.
"""
import gzip, json, sys
from itertools import product
from pathlib import Path

D = Path(__file__).resolve().parent.parent
Q = D.parents[2] / "qclass-closure"


def rect(x0, x1, y0, y1):
    return {(x, y) for x in range(x0, x1) for y in range(y0, y1)}


def U2(k=0):  # copied from d84 indep.py
    base = rect(0, 9, 0, 2) | rect(0, 2, 2, 9) | rect(7, 9, 2, 7) | rect(5, 7, 5, 7)
    return {(x + (4 * k if x >= 4 else 0), y) for x, y in base} | rect(4, 4 + 4 * k, 0, 2)


def cross(b):  # P_b = [-b,b]x[-2,2] u [-2,2]x[-b,b]
    return rect(-b, b, -2, 2) | rect(-2, 2, -b, b)


def facts(cells):
    pts = {(x + a, y + b) for x, y in cells for a, b in product((0, 1), repeat=2)}
    out = {}
    for y in product((0, 1), repeat=2):
        c = dict(cvx=0, smooth=0, pinch=0, rfx=0, int=0)
        for p in pts:
            if (p[0] - y[0]) % 2 or (p[1] - y[1]) % 2:
                continue
            q = [((p[0] + a, p[1] + b) in cells) for a, b in ((-1, -1), (0, -1), (-1, 0), (0, 0))]
            k = sum(q)
            if k == 2:
                c["pinch" if q[0] == q[3] else "smooth"] += 1  # q[0]==q[3] -> diagonal pair
            else:
                c[{1: "cvx", 3: "rfx", 4: "int"}[k]] += 1
        # cell-side count: each cell's class-y corner, counted directly
        direct = sum(1 for x, z in cells for a, b in product((0, 1), repeat=2)
                     if (x + a - y[0]) % 2 == 0 and (z + b - y[1]) % 2 == 0)
        c["rhs"] = c["cvx"] + 2 * (c["smooth"] + c["pinch"]) + 3 * c["rfx"] + 4 * c["int"]
        c["direct"] = direct
        out[y] = c
    v = sum(o["cvx"] for o in out.values())
    r = sum(o["rfx"] for o in out.values())
    pinch = sum(o["pinch"] for o in out.values())
    return out, v, r, pinch


def census_rooms():
    want = [10, 13, 16, 19, 21, 24, 27, 30, 33, 36]
    got = {}
    with gzip.open(Q / "witnesses.txt.gz", "rt") as f:
        for line in f:
            if line[0] != "R":
                continue
            t = line.split()
            area = int(t[2])
            if area in want and area not in got:
                nums = list(map(int, t[5:]))
                cells = set(zip(nums[0::2], nums[1::2]))
                assert len(cells) == area
                got[area] = (f"census R{t[1]} (area {area}, W {t[3]}, align {t[4]})", cells)
                if len(got) == len(want):
                    break
    return [got[a] for a in want if a in got]


def main():
    rooms = json.load(open(D / "d8-perturbation-test" / "rooms.json"))
    r0 = rooms[0]
    named = [(f"R22 ({r0['id']})", {tuple(c) for c in r0["cells"]}),
             ("cross P_7", cross(7)), ("cross P_9", cross(9)), ("U2 (k=0)", U2(0))]
    named += census_rooms()
    named.append(("CONTROL pinched shape (two 2x2 squares touching at a point)",
                  rect(0, 2, 0, 2) | rect(2, 4, 2, 4)))
    fails = 0
    for name, cells in named:
        out, v, r, pinch = facts(cells)
        n = len(cells)
        print(f"== {name}: n={n} v={v} r={r} v-r={v - r} W={v + r} pinch_points={pinch}")
        for y, c in sorted(out.items()):
            ok = c["rhs"] == n == c["direct"]
            fails += not ok
            co = c["smooth"] == c["int"] == 0
            line = (f"  y={y}: cvx={c['cvx']} smooth={c['smooth']} pinch={c['pinch']} "
                    f"rfx={c['rfx']} int={c['int']} -> rhs={c['rhs']} {'OK' if ok else 'FAIL'}")
            if co:
                line += (f" | corner-only: 3rfx+cvx+2pinch={3 * c['rfx'] + c['cvx'] + 2 * c['pinch']}"
                         f" <= 4r+4={4 * r + 4}: {n <= 4 * r + 4}")
            print(line)
    print(f"identity failures: {fails}")


main()
