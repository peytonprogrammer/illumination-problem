#!/usr/bin/env python3
"""Cross-check partA-cert's cylinder counter against d3-review/surface.py.

surface.Surface.cylinders(p, q) traces every integer leaf with exact
fractions and unions strips; partA-cert uses one slot permutation.  The two
share no code.  Usage: partA-crosscheck_cyl.py ROOMFILE CYLB EVERY
ROOMFILE holds "area W x y ..." lines; every EVERY-th normalized room is
checked for all coprime 1 <= p, q <= CYLB.
"""
import subprocess, sys, os
from math import gcd
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "d3-review"))
from surface import Surface

roomfile, B, every = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
rooms = [l.split() for l in open(roomfile) if l.strip() and not l.startswith("#")]
rooms = rooms[::every]
tmp = os.path.join(HERE, "runs", "partA", "test")
src = os.path.join(tmp, "xc.rooms_in")
with open(src, "w") as f:
    for r in rooms:
        f.write(" ".join(r) + "\n")
subprocess.run([os.path.join(HERE, "partA-cert"), "1", str(-B), "0", src,
                os.path.join(tmp, "xc.out"), os.path.join(tmp, "xc.sv"), os.path.join(tmp, "xc.list")], check=True)
c_res = {}
cur = None
for l in open(os.path.join(tmp, "xc.list")):
    t = l.split()
    if t[0] == "ROOM":
        cur = int(t[1]); c_res[cur] = {}
    elif t[0] == "DIR":
        c_res[cur][(int(t[1]), int(t[2]))] = int(t[3])
checked = mism = 0
for rid, r in enumerate(rooms, 1):
    if rid not in c_res:
        continue  # reduced (non-normalized) room
    a = int(r[0]); xs = list(map(int, r[2:]))
    cells = [(xs[2 * i], xs[2 * i + 1]) for i in range(a)]
    S = Surface(cells)
    for (p, q), cc in c_res[rid].items():
        comps, _ = S.cylinders(p, q)
        checked += 1
        if comps != cc:
            mism += 1
            print("MISMATCH", rid, p, q, cc, comps, cells)
print(f"rooms {len(c_res)} directions {checked} mismatches {mism}")
