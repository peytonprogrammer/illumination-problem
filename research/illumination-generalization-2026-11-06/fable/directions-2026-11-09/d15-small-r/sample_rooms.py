"""Test (b): fixed-seed sample of rooms with 10 or 12 walls in a 16 x 16 box.
Writes runs/b_sample.txt (one room per line) and runs/b_in{0,1,2}.txt for
verify.c.  Usage: sample_rooms.py [rooms_per_r]"""
import sys, random
from export_cert import lines_for
SEED, BOX = 20261109, 16
N = int(sys.argv[1]) if len(sys.argv) > 1 else 50000
rng = random.Random(SEED)
def gaps(n):
    c = [0] + sorted(rng.sample(range(1, BOX + 1), n))
    return [c[i + 1] - c[i] for i in range(n)]
by_type = {}
with open("runs/b_sample.txt", "w") as rec:
    rec.write(f"# seed {SEED} box {BOX} rooms_per_r {N}; columns: r nx ny mask gx.. | gy..\n")
    for r in (3, 4):
        types = [tuple(map(int, l.split())) for l in open(f"types_r{r}.txt")]
        for _ in range(N):
            nx, ny, W, mask = rng.choice(types)
            gx, gy = gaps(nx), gaps(ny)
            by_type.setdefault((nx, ny, mask), []).append((gx, gy))
            rec.write(f"{r} {nx} {ny} {mask} {' '.join(map(str, gx))} | {' '.join(map(str, gy))}\n")
outs = [open(f"runs/b_in{w}.txt", "w") for w in range(3)]
for idx, ((nx, ny, mask), rooms) in enumerate(sorted(by_type.items())):
    f = outs[idx % 3]
    f.write("\n".join(lines_for(nx, ny, mask)) + "\n")
    for gx, gy in rooms:
        f.write("ROOM " + " ".join(map(str, gx + gy)) + "\n")
for f in outs:
    f.write("END\n"); f.close()
print("types", len(by_type), "rooms", sum(len(v) for v in by_type.values()))
