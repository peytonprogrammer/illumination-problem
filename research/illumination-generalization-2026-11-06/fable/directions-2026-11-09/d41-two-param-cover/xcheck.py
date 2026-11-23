#!/usr/bin/env python3
"""xcheck.py ROOM AXIS B1 B2 G2 GMAX PMAX -- independent check of band2: replicate row B2 G2 times explicitly,
run d28's band.c on row B1 (g1 = 1, 3, .., GMAX), and compare least p with band2's PT mode for the original pair(s)."""
import sys, subprocess, re
room, ax, b1, b2, g2, gmax, pmax = sys.argv[1], *map(int, sys.argv[2:])
v = list(map(int, open(room).read().split())); cells = [(v[1+2*i], v[2+2*i]) for i in range(v[0])]
if ax: cells = [(y, x) for x, y in cells]
out = []
for x, y in cells:
    if y < b2: out.append((x, y))
    elif y > b2: out.append((x, y + g2 - 1))
    else: out += [(x, y + j) for j in range(g2)]
txt = f"{len(out)} " + " ".join(f"{x} {y}" for x, y in out)
band = "../d28-band-stabilization/band"
r = subprocess.run([band, "0", str(b1 if b1 < b2 else b1 + g2 - 1), str(pmax), str(gmax)], input=txt, capture_output=True, text=True).stdout
pairs = {i: tuple(map(int, m)) for i, *m in [ (int(a), b, c, d, e) for a, b, c, d, e in re.findall(r"# pair (\d+) \((\d+),(\d+)\)-\((\d+),(\d+)\)", r)]}
ref = {(int(g), int(i)): int(p) for _, g, i, p, *_ in (l.split() for l in r.splitlines() if l.startswith("G "))}
hdr = subprocess.run(["./band2", str(ax), str(b1), str(b2), "1"], stdin=open(room), capture_output=True, text=True).stdout
mine = {int(a): (int(b), int(c), int(d), int(e)) for a, b, c, d, e in re.findall(r"# pair (\d+) \((\d+),(\d+)\)-\((\d+),(\d+)\)", hdr)}
bad = n = 0
for j, (x0, y0, x1, y1) in mine.items():
    sh = lambda y: y + g2 - 1 if y > b2 else y
    i = [k for k, c in pairs.items() if c == (x0, sh(y0), x1, sh(y1))][0]
    for g1 in range(1, gmax + 1, 2):
        o = subprocess.run(["./band2", str(ax), str(b1), str(b2), str(pmax)], stdin=open(room), capture_output=True, text=True,
                           env={"PT": f"{g1},{g2}"}).stdout
        p = [int(l.split()[4]) for l in o.splitlines() if l.startswith("PT") and int(l.split()[3]) == j][0]
        n += 1; bad += p != ref[(g1, i)]
print(f"{room} ax{ax} rows {b1},{b2} g2={g2}: {n} (g1,pair) compared, {bad} mismatches")
