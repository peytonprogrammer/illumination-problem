"""Run the census decider orbitc on every same-class interior pair of each room (area <= 40).
usage: orb.py roomsfile CAP"""
import sys, subprocess, time
OC = "../d9-census-w22/orbitc"
for line in open(sys.argv[1]):
    v = list(map(int, line.split())); A = v[0]; cells = set(zip(v[1::2], v[2::2]))
    if A > 40: print("skip A", A); continue
    pts = [(x, y) for (x, y) in {(a + i, b + j) for a, b in cells for i in (0, 1) for j in (0, 1)}
           if all((x - i, y - j) in cells for i in (0, 1) for j in (0, 1))]
    dark = lit = 0; st = 0; t = time.time(); status = "ok"
    for cl in range(4):
        src = sorted(p for p in pts if (p[0] & 1) + 2 * (p[1] & 1) == cl)[:64]
        if len(src) < 2: continue
        prob = "%d %s | %d %s\n" % (A, " ".join("%d %d" % c for c in sorted(cells)), len(src), " ".join("%d %d" % p for p in src))
        r = subprocess.run([OC, sys.argv[2]], input=prob, capture_output=True, text=True)
        if r.returncode: status = "FAIL " + r.stderr.strip(); continue
        out = r.stdout.splitlines(); st = max(st, int(out[0].split()[1]))
        for l in out[1:]:
            if l.endswith("DARK"): dark += 1; print("  DARK", l.strip())
            else: lit += 1
    print("A %d lit %d dark %d maxstates %d %.2fs %s" % (A, lit, dark, st, time.time() - t, status), flush=True)
