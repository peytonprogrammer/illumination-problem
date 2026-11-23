"""Check DUMP lines of verify.c (stdin) with the d8 tracer and with raycast.py."""
import sys
sys.path.insert(0, "../d8-perturbation-test")
import tracer, raycast
n = bad = 0
for line in sys.stdin:
    if not line.startswith("DUMP"): continue
    f = line.split()
    px, py, vx, vy, qx, qy = map(int, f[1:7])
    cells = {tuple(map(int, c.split(","))) for c in f[8][6:].split(";") if c}
    end, ok, _ = tracer.trace(cells, (px, py), (vx, vy))
    e2, ok2 = raycast.follow(cells, (px, py), (vx, vy))
    good = ok and ok2 and tuple(end) == (qx, qy) and e2 == (qx, qy)
    n += 1
    if not good:
        bad += 1; print("MISMATCH", line.strip()[:200], end, ok, e2, ok2)
print("paths checked", n, "mismatches", bad)
