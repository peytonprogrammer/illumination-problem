"""D132 checks for parametric-orbits.2026-11-21-2200.md.

Exact integer billiard replay on the two named directional families
(cov279 slice q=4u, st279 at m=32,48), plus arithmetic checks of the
Schwarz-Christoffel exponents, the Presburger shift witnesses and the
Hadamard/Cramer step of the conditional bound.  No room-family search:
only the rooms named in the note are built.  Directions (p,1) are scanned
on those fixed rooms.  Run: python3 -B checks.py
"""
from fractions import Fraction
from itertools import combinations
from math import gcd, isqrt, ceil, sqrt
import random
import time

T0 = time.process_time()
MAX_ROWS = 200000  # cap on unit-vertical-travel steps per launch


def cells_from_bands(bands):
    cells = set()
    for (x0, x1, y0, y1) in bands:
        for i in range(x0, x1):
            for j in range(y0, y1):
                cells.add((i, j))
    return cells


def runs_of(cells):
    run = {}
    rows = {}
    for (i, j) in cells:
        rows.setdefault(j, []).append(i)
    for j, xs in rows.items():
        xs.sort()
        start = xs[0]
        prev = xs[0]
        for i in xs[1:] + [None]:
            if i is None or i != prev + 1:
                for k in range(start, prev + 1):
                    run[(k, j)] = (start, prev + 1)
                if i is not None:
                    start = i
            if i is not None:
                prev = i
    return run


def corner_census(cells):
    pts = set()
    for (i, j) in cells:
        for dx in (0, 1):
            for dy in (0, 1):
                pts.add((i + dx, j + dy))
    reflex = convex = pinch = 0
    for (x, y) in pts:
        quad = [(x - 1, y - 1) in cells, (x, y - 1) in cells,
                (x - 1, y) in cells, (x, y) in cells]
        n = sum(quad)
        if n == 3:
            reflex += 1
        elif n == 1:
            convex += 1
        elif n == 2 and quad[0] == quad[3]:
            pinch += 1
    return reflex, convex, pinch


def shoot(cells, run, S, T, p, sx, sy):
    """Ray from lattice point S with direction (sx*p, sy*1), p>0 integer.
    Returns (verdict, time, info).  verdict in lit/periodic/reflex/convex/pinch/cap.
    Rows are traversed exactly: inside an open row strip x moves by p with
    reflections in the row run; lattice points occur only at integer y."""
    x, y = S
    seen = set()
    t = 0
    ymax = y
    while t < MAX_ROWS:
        key = (x, y, sx, sy)
        if key in seen:
            return "periodic", t, ymax
        seen.add(key)
        j = y if sy > 0 else y - 1
        i = x if sx > 0 else x - 1
        a, b = run[(i, j)]
        L = b - a
        th = (x - a) if sx > 0 else (2 * L - (x - a))
        th = (th + p) % (2 * L)
        if 0 < th < L:
            x, sx = a + th, 1
        elif L < th < 2 * L:
            x, sx = a + 2 * L - th, -1
        elif th == L:
            x, sx = b, 1
        else:
            x, sx = a, -1
        y += sy
        t += 1
        ymax = max(ymax, y)
        if (x, y) == T:
            return "lit", t, ymax
        A = (x - 1 if sx > 0 else x, y - 1 if sy > 0 else y)
        Hc = (x if sx > 0 else x - 1, A[1])
        Vc = (A[0], y if sy > 0 else y - 1)
        Dc = (Hc[0], Vc[1])
        h, v, d = Hc in cells, Vc in cells, Dc in cells
        if h and v and d:
            continue
        if h and not v and not d:
            sy = -sy
            continue
        if v and not h and not d:
            sx = -sx
            continue
        n = 1 + h + v + d
        return ("reflex" if n == 3 else "convex" if n == 1 else "pinch"), t, ymax
    return "cap", t, ymax


def verdict(cells, run, S, T, p):
    res = []
    for sx in (1, -1):
        for sy in (1, -1):
            res.append((sx, sy) + shoot(cells, run, S, T, p, sx, sy))
    lit = [r for r in res if r[2] == "lit"]
    return bool(lit), res


log = []


def out(s=""):
    print(s)


# ---------------------------------------------------------------- cov279
out("== Check 1: cov279 slice q=4u, S=(4,1), T=(12,1), p=8v ==")
out("Room bands from thin-room.md: (0,2q)x(0,2), (2q-3,4q)x(2,3), (2q,5q)x(3,4), (4q,6q)x(4,6)")
all_ok = True
for u in (4, 7, 10, 13):
    q = 4 * u
    bands = [(0, 2 * q, 0, 2), (2 * q - 3, 4 * q, 2, 3), (2 * q, 5 * q, 3, 4), (4 * q, 6 * q, 4, 6)]
    cells = cells_from_bands(bands)
    run = runs_of(cells)
    rfx, cvx, pin = corner_census(cells)
    assert len(cells) == 13 * q + 3
    out(f"q={q} (u={u}): area {len(cells)} = 13q+3, reflex {rfx}, convex {cvx}, pinch {pin}")
    mism = []
    stops = 0
    left = 0
    rows = []
    for v in range(1, 2 * u + 4):
        p = 8 * v
        lit, res = verdict(cells, run, (4, 1), (12, 1), p)
        pred = gcd(u, v) == 1
        if lit != pred:
            mism.append(v)
        for r in res:
            if r[2] in ("reflex", "convex", "pinch", "cap"):
                stops += 1
            if r[4] > 2:
                left += 1
        tmin = min((r[3] for r in res if r[2] == "lit"), default=None)
        rows.append(f"v={v}:{'L' if lit else 'D'}" + (f"@t{tmin}" if lit else ""))
    all_ok &= not mism
    out("  " + " ".join(rows))
    out(f"  mismatches vs gcd(u,v)=1: {mism or 'none'}; launches stopped at a corner/cap: {stops}; "
        f"launches leaving the bottom rectangle: {left}")
out(f"Check 1 result: {'PASS' if all_ok else 'FAIL'} (lit iff gcd(u,v)=1 on every tested (u,v))")

# specific claims at q=16
q = 16
bands = [(0, 32, 0, 2), (29, 64, 2, 3), (32, 80, 3, 4), (64, 96, 4, 6)]
cells = cells_from_bands(bands)
run = runs_of(cells)
_, res = verdict(cells, run, (4, 1), (12, 1), 24)
out("q=16, v=3 launches (sx, sy, verdict, time, ymax): " + str(res))
dev = 4 + 24 * 2
out(f"  developed abscissa 4+24*2={dev}; fold mod 64 -> {64 - dev if dev % 64 > 32 else dev % 64}")
_, res = verdict(cells, run, (4, 1), (12, 1), 32)
out("q=16, v=4 launches: " + str(res))
# abscissae at height-one returns for v=4
xs = sorted({min((4 + s * 32 * t) % 64, 64 - (4 + s * 32 * t) % 64) for t in range(0, 40, 2) for s in (1, -1)})
out(f"  v=4 folded abscissae at height-one returns: {xs}")
out()

# ---------------------------------------------------------------- st279
out("== Check 2: st279 end-stretch m, S=(2,1), T=(6,1), p multiple of 4 ==")
out("Bands from stabilizer-orbits.md: (0,m)x[0,m], (m,m+1)x[m-1,m+2], (m+1,m+2)x[m,m+3], (m+2,2m+2)x[m+2,2m+2]")
st_ok = True
for m in (32, 48):
    bands = [(0, m, 0, m), (m - 1, m + 2, m, m + 1), (m, m + 3, m + 1, m + 2), (m + 2, 2 * m + 2, m + 2, 2 * m + 2)]
    cells = cells_from_bands(bands)
    run = runs_of(cells)
    rfx, cvx, pin = corner_census(cells)
    assert len(cells) == 2 * m * m + 6
    mism = []
    litps = []
    for p in range(4, 4 * m + 1, 4):
        lit, res = verdict(cells, run, (2, 1), (6, 1), p)
        pred = (p % m) in (4, m - 4)
        if lit != pred:
            mism.append(p)
        if lit:
            litps.append(p)
    st_ok &= not mism
    out(f"m={m}: area {len(cells)}, reflex {rfx}, convex {cvx}; lit p in [4,{4*m}]: {litps}; "
        f"mismatches vs p=+-4 mod m: {mism or 'none'}")
bands = [(0, 32, 0, 32), (31, 34, 32, 33), (32, 35, 33, 34), (34, 66, 34, 66)]
cells = cells_from_bands(bands)
run = runs_of(cells)
_, res = verdict(cells, run, (2, 1), (6, 1), 36)
out("m=32, p=36 launches: " + str(res))
_, res = verdict(cells, run, (2, 1), (6, 1), 40)
out("m=32, p=40 launches: " + str(res))
out(f"Check 2 result: {'PASS' if st_ok else 'FAIL'}")
out()

# ---------------------------------------------------------------- arithmetic
out("== Check 3: Schwarz-Christoffel and orientation-cover arithmetic ==")
for r in (6, 8):
    n = 2 * r + 4
    s = Fraction(r, 2) - Fraction(r + 4, 2)
    # q = c^2 prod (z-a)^eps dz^2 ; at infinity exponent sum r-(r+4) = -4 -> regular nonzero
    g = (n - 2) // 2  # hyperelliptic v^2 = degree-n polynomial, n even
    # omega order at branch point, local s^2 = z-a: v~s, dz~2s ds
    convex_order = 1 + 1 - 2
    reflex_order = 1 + 1
    zeros = r * reflex_order
    out(f"r={r}: prevertices {n}, f' exponent sum {s} (needs -2), genus {g} (needs r+1={r+1}), "
        f"ord omega convex {convex_order}, reflex {reflex_order}, total zeros {zeros} = 2g-2 {2*g-2}")
out()

out("== Check 4: Presburger shift witnesses ==")
bad = []
for P in range(1, 200):
    u = 3 * P + 1
    if not (u % 3 == 1 and u >= 4 and gcd(u, P) == 1):
        bad.append(P)
    # v = k*u has gcd u>1 (dark); v+P has gcd(u, P) = 1 (lit)
    M = 2 * P + 5
    # st279 variable w=p/4 lit iff w = +-1 mod M; shift by P moves 1 to 1+P, not +-1 mod M
    if (1 + P) % M in (1, M - 1):
        bad.append(("st", P))
out(f"cov279: u=3P+1 gives gcd(u,P)=1 and u=1 mod 3 for P=1..199; st279: 1+P not +-1 mod M>2P+4. "
    f"failures: {bad or 'none'}")
out()

out("== Check 5: Cramer/Hadamard denominator bound on small random rational subspaces ==")


def solve_exact(rows, rhs, d):
    M = [[Fraction(v) for v in row] + [Fraction(b)] for row, b in zip(rows, rhs)]
    piv = []
    r = 0
    for c in range(d):
        k = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if k is None:
            continue
        M[r], M[k] = M[k], M[r]
        inv = M[r][c]
        M[r] = [v / inv for v in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        piv.append(c)
        r += 1
    for i in range(r, len(M)):
        if M[i][d] != 0:
            return None
    if r < d:
        return None
    x = [Fraction(0)] * d
    for i, c in enumerate(piv):
        x[c] = M[i][d]
    return x


random.seed(132)
worst = 0
tests = 0
viol = 0
for trial in range(300):
    d = random.choice([3, 4, 5])
    H = random.choice([1, 2, 3])
    k = random.randint(1, d - 2)
    A = [[random.randint(-H, H) for _ in range(d)] for _ in range(k)]
    Delta = ceil((sqrt(d) * H) ** d)
    for nz in range(d + 1):
        for Z in combinations(range(d), nz):
            rows = A + [[1 if c == z else 0 for c in range(d)] for z in Z] + [[1] * d]
            rhs = [0] * (k + nz) + [1]
            x = solve_exact(rows, rhs, d)
            if x is None or any(v < 0 for v in x):
                continue
            den = 1
            for v in x:
                den = den * v.denominator // gcd(den, v.denominator)
            tests += 1
            worst = max(worst, den / Delta)
            if den > Delta:
                viol += 1
out(f"{tests} vertices checked; max denominator/Delta = {worst:.4f}; violations {viol}")
W = 20
d22 = 2 * ((W // 2 + 2) - 1)
out(f"W=20: distinct coords per axis <= {W//2}+2, gaps d = {d22}")
out()
out(f"CPU seconds: {time.process_time() - T0:.1f}")
