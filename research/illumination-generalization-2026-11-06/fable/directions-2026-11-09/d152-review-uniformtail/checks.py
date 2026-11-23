"""d152 referee checks for uniform-tail.md and stretch-stability.md (0310 snapshots).

Named rooms only; no room, direction or witness search. Exact integer arithmetic.
Lattice decisions use d8's complete SL(2,Z)-orbit decider (unchanged, imported).
Run: python3 -B checks.py > checks.log
"""
import json
import math
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ARCH = HERE.parent
sys.path.insert(0, str(ARCH / "d8-perturbation-test"))
import room as RM          # noqa: E402
from decider import decide, regular_points   # noqa: E402

T0 = time.process_time()


def rect(a, b, c, d):
    return {(i, j) for i in range(a, b) for j in range(c, d)}


def geometry(cells):
    s = RM.summary(cells)
    vs = RM.vertex_cycle(cells)
    hl = [abs(vs[k][0] - vs[(k + 1) % len(vs)][0]) for k in range(len(vs))]
    vl = [abs(vs[k][1] - vs[(k + 1) % len(vs)][1]) for k in range(len(vs))]
    hg = math.gcd(*[x for x in hl if x])
    vg = math.gcd(*[y for y in vl if y])
    return dict(W=s["W"], r=s["r"], area=s["area"], simple=RM.is_strictly_simple(cells),
                hgcd=hg, vgcd=vg)


def full_lattice(name, cells, cap=3_000_000, interior_only=False):
    regs = regular_points(cells)
    if interior_only or len(regs) > 60:   # orbit.c accepts at most 60 sources
        regs = [p for p in regs if RM.status(cells, p) == "interior"]
        name += " [interior lattice sources only]"
    assert len(regs) <= 60
    t = time.process_time()
    res = decide(cells, regs, cap=cap)
    dark = sorted({tuple(sorted((p, q))) for p in regs for q in regs
                   if p != q and (p, q) not in res["lit"]})
    print(f"  {name}: status {res['status']}, states {res['states']}, regular pts {len(regs)}, "
          f"unlit unordered pairs {len(dark)}, cpu {time.process_time() - t:.1f}s")
    if dark and len(dark) <= 12:
        print("    unlit:", dark)
    return res, dark


rooms = {r["id"]: r for r in json.load(open(ARCH / "d8-perturbation-test" / "rooms.json"))}
R22 = {tuple(c) for c in rooms["R22-base"]["cells"]}

# ---------------------------------------------------------------- 1. dilation
print("== 1. Dilation by m on R22 (exact similarity; lattice-mark caveat)")
R22x2 = {(2 * i + a, 2 * j + b) for (i, j) in R22 for a in (0, 1) for b in (0, 1)}
print("  R22 geometry", geometry(R22), " 2*R22 geometry", geometry(R22x2))
res1, dark1 = full_lattice("R22", R22)
res2, dark2 = full_lattice("2*R22", R22x2)
img = sorted(tuple(sorted(((2 * p[0], 2 * p[1]), (2 * q[0], 2 * q[1])))) for p, q in dark1)
if res2["status"] == "DONE":
    print("  images of R22 dark pairs dark in 2*R22:", set(img) <= set(dark2))
    new = [pq for pq in dark2 if pq not in img]
    half = [pq for pq in new if any(c % 2 for pt in pq for c in pt)]
    print(f"  dark pairs of 2*R22 not images of R22 lattice pairs: {len(new)}, "
          f"of which with a half-integer preimage: {len(half)}")
    # every lattice pair of R22 maps to a lattice pair of 2*R22 with the same verdict
    regs1 = [p for p in regular_points(R22) if RM.status(R22, p) == "interior"]
    agree = all(((p, q) in res1["lit"]) == (((2 * p[0], 2 * p[1]), (2 * q[0], 2 * q[1])) in res2["lit"])
                for p in regs1 for q in regs1 if p != q)
    print("  verdict of every R22 lattice pair equals verdict of its image:", agree)

# ------------------------------------------------- 2. R22 arm-length variants
print("\n== 2. R22 arm (prong) slices: same wall pattern, unit corridor lengthened")
J = R22 - {(1, -3)}
print("  junction J = R22-L1-027 (R22 minus (1,-3))", geometry(J),
      " equals named room:", J == {tuple(c) for c in rooms["R22-L1-027"]["cells"]})
for nm, add in (("R22-L1-007 bottom prong 1->2", (1, -4)), ("R22-L1-025 right prong 1->2", (5, 0))):
    c = R22 | {add}
    assert c == {tuple(x) for x in rooms[nm.split()[0]]["cells"]}
    print(f"  {nm}:", geometry(c))
    full_lattice(nm, c)
# Top arm: width 2 over 1<x<3, both mouth endpoints (1,2),(3,2) reflex (not flush with J's sides).
Jt = R22 - {(1, 2), (2, 2)}
print("  junction Jt = R22 minus top arm", geometry(Jt),
      " mouth endpoints:", RM.status(R22, (1, 2)), RM.status(R22, (3, 2)))
c = R22 | {(1, 3), (2, 3)}
assert c == {tuple(x) for x in rooms["R22-L1-012"]["cells"]}
print("  R22-L1-012 top arm 1->2:", geometry(c))
full_lattice("R22-L1-012 top arm 1->2", c)
# The d114/d124 capped-arm whole-room tail needs ell >= 36 w [1+2F_(3m)]^2, m = 4 area(J).
m = 4 * len(J)
F = [0, 1]
while len(F) < 3 * m + 2:
    F.append(F[-1] + F[-2])
ell0 = 36 * (1 + 2 * F[3 * m]) ** 2
print(f"  capped-arm explicit threshold for R22 bottom prong: m = {m}, "
      f"ell0 = 36(1+2F_{3*m})^2 has {len(str(ell0))} digits")
print("  top arm: m = 4 area(Jt) =", 4 * len(Jt), "; (2,2) lies on the open top-arm mouth:",
      RM.status(Jt, (2, 2)), "in Jt")
print("  R22 dark pair (0,0)-(2,2) lies in J:",
      all(RM.status(J, p) == "interior" for p in ((0, 0), (2, 2))))

# -------------------------------------------------- 3. three-chamber room
print("\n== 3. Three 3x3 chambers, unit corridors X=Y=3k+1 over 1<y<2")


def three(X, Y):
    return (rect(0, 3, 0, 3) | rect(3, 3 + X, 1, 2) | rect(3 + X, 6 + X, 0, 3)
            | rect(6 + X, 6 + X + Y, 1, 2) | rect(6 + X + Y, 9 + X + Y, 0, 3))


for k in range(0, 9):
    X = Y = 3 * k + 1
    g = geometry(three(X, Y))
    ok = (g["W"] == 20 and g["r"] == 8 and g["simple"] and g["area"] == 27 + X + Y
          and g["hgcd"] == 1 and g["vgcd"] == 1)
    print(f"  k={k} X=Y={X}: {g} checks={ok} BBBB-by-area(>64): {g['area'] > 64}")
# counter-check: X=Y=3 is not horizontally normalized
print("  control X=Y=3:", geometry(three(3, 3)))


def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


print("  thresholds at X=Y (cut X; sealed sub-room area 18+Y, extent 6+Y):")
for k in (0, 1, 6, 10, 100):
    X = Y = 3 * k + 1
    mm = 4 * (18 + Y)
    real = 36 * (1 + 2 * fib(3 * mm)) ** 2
    lat = 4 * (1 + fib(3 * mm - 1)) ** 2
    print(f"    k={k}: X={X}; D124 all-real bound has {len(str(real))} digits (X >= bound: {X >= real}); "
          f"lattice bound digits {len(str(lat))} (X >= : {X >= lat}); X > 4(6+Y): {X > 4 * (6 + Y)}")
print("  (for X=Y, X > 4(6+X) is impossible; F_n >= n for n>=5 makes both D124 bounds exceed X)")
# orbit.c caps a room at 63 cells, so the BBBB members (k >= 6, >= 65 cells) are out of reach.
for k in (0, 1, 5):
    X = Y = 3 * k + 1
    full_lattice(f"three-chamber X=Y={X}", three(X, Y), cap=1_500_000, interior_only=True)

# ---------------------------------------------------- 4. named controls
print("\n== 4. Named controls")
for H in (5, 7):
    c = rect(0, 5, 0, H) | rect(5, 8, 2, 3) | rect(8, 13, 0, H)
    d = 5
    print(f"  DB55 H={H}: {geometry(c)}; chamber depths 5,5 -> d112 'L>4d' gives L>={4 * d + 1}")
for b in (7, 9):
    c = rect(-b, b, -2, 2) | rect(-2, 2, -b, b)
    arm = 4 * (b - 2)
    print(f"  cross b={b}: {geometry(c)}; arm length {b - 2}, arm area {arm}, "
          f"junction without one arm {len(c) - arm}")
sc = ARCH.parent.parent.parent / "qclass-closure" / "bbbb" / "stretch-control.py"
snap = ARCH / "d95-review-queue" / "snapshots" / "stretch-control.2026-11-22-0310.py"
print("  bbbb/stretch-control.py identical to snapshot:", sc.read_text() == snap.read_text())
t = time.time()
out = subprocess.run([sys.executable, "-B", str(sc)], capture_output=True, text=True)
print("  replay rc", out.returncode, f"wall {time.time() - t:.1f}s")
print("  " + out.stdout.strip().replace("\n", "\n  "))
if out.stderr.strip():
    print("  stderr:", out.stderr.strip()[-500:])

import resource
ru = resource.getrusage(resource.RUSAGE_CHILDREN)
print(f"\nTotal CPU: this process {time.process_time() - T0:.1f}s, children {ru.ru_utime + ru.ru_stime:.1f}s")
