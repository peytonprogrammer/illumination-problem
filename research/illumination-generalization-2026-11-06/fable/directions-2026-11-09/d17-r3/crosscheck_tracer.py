"""Cross-check the tracer in rooms.py against ../d15-small-r/raycast.py.
Rooms: the first 300 rooms of each r in runs/g_rooms.txt (no new rooms).
Per room: 40 random (interior lattice point, direction) cases, seed 20261110."""
import sys, random, time
from math import gcd
sys.path.insert(0, "../d15-small-r")
from raycast import follow
from rooms import Room, step
rng = random.Random(20261110)
t0 = time.time(); n = agree = bad = vert = 0; seen = {}
for l in open("runs/g_rooms.txt"):
    a, b = l.split("|"); r, nx, ny, mask, *gx = map(int, a.split())
    seen[r] = seen.get(r, 0) + 1
    if seen[r] > 300: continue
    R = Room(nx, ny, mask, gx, list(map(int, b.split()))); pts = R.interior_points()
    for _ in range(40 if pts else 0):
        S = rng.choice(pts); dx, dy = rng.randint(-30, 30), rng.randint(-30, 30)
        if dx == 0 and dy == 0: continue
        m = gcd(abs(dx), abs(dy)); x, y, sx, sy = S[0], S[1], (1 if dx >= 0 else -1), (1 if dy >= 0 else -1)
        mine = (x, y)
        for _i in range(m):
            st = step(R, x, y, abs(dx) // m, abs(dy) // m, sx, sy)
            if st is None: mine = None; break
            x, y, sx, sy, _h = st; mine = (x, y)
        end, ok = follow(R.cells, S, (dx, dy))
        theirs = (int(end[0]), int(end[1])) if ok else None
        n += 1; vert += mine is None
        if mine == theirs: agree += 1
        else:
            bad += 1
            if bad <= 3: print("MISMATCH", l.strip(), S, (dx, dy), mine, end, ok)
print("cases", n, "agree", agree, "mismatch", bad, "vertex hits (mine)", vert, "seconds", round(time.time() - t0, 1))
