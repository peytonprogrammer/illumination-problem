"""Population F for claim T1: scaled base rooms with 10 walls.
Usage: gen_fine.py  -> writes runs/f_in{0,1,2}.txt and runs/f_rooms.txt"""
import sys, itertools
sys.path.insert(0, "../d15-small-r")
from export_cert import lines_for
def comps(n, B):
    """all tuples of n positive integers with sum <= B"""
    out = []
    def rec(pre, left):
        if len(pre) == n: out.append(tuple(pre)); return
        for v in range(1, left - (n - 1 - len(pre)) + 1): rec(pre + [v], left - v)
    rec([], B); return out
types = [tuple(map(int, l.split())) for l in open("../d15-small-r/types_r3.txt")]
outs = [open(f"runs/f_in{w}.txt", "w") for w in range(3)]
rec = open("runs/f_rooms.txt", "w"); n = 0
for idx, (nx, ny, W, mask) in enumerate(types):
    f = outs[idx % 3]
    f.write("\n".join(lines_for(nx, ny, mask)) + "\n")
    for q, B in ((2, 6), (3, 5), (4, 4)):
        for gx in comps(nx, B):
            for gy in comps(ny, B):
                g = [q * v for v in gx + gy]
                f.write("ROOM " + " ".join(map(str, g)) + "\n"); n += 1
                rec.write(f"{nx} {ny} {mask} {q} {' '.join(map(str, g))}\n")
for f in outs: f.write("END\n"); f.close()
print("rooms", n)
