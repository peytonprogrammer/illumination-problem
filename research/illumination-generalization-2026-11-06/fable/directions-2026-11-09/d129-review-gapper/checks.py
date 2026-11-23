"""Referee checks for thin-gap-periods.2026-11-21-2100.md (exact rational arithmetic only)."""
from fractions import Fraction as F
from math import gcd
from functools import reduce
import time, sys
sys.stdout.reconfigure(line_buffering=True)

T0 = time.time()

def lcm(*xs):
    return reduce(lambda a, b: a * b // gcd(a, b), xs, 1)

# ---------------------------------------------------------------- geometry
def dumbbell(U, L=2):
    """Left chamber (0,U)x(0,5), corridor (U,U+L)x(2,3), right chamber (U+L,2U+L+1)x(0,5). CCW."""
    R = U + L
    return [(0, 0), (U, 0), (U, 2), (R, 2), (R, 0), (R + U + 1, 0), (R + U + 1, 5),
            (R, 5), (R, 3), (U, 3), (U, 5), (0, 5)]

def lroom(X, Y, w=3):
    """Named L room: horizontal arm (0,X)x(0,w), vertical arm (0,w)x(0,Y). CCW."""
    return [(0, 0), (X, 0), (X, w), (w, w), (w, Y), (0, Y)]

def edges(V):
    return [(V[i], V[(i + 1) % len(V)]) for i in range(len(V))]

def area2(V):
    return sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in edges(V))

def reflexes(V):
    out = []
    n = len(V)
    for i in range(n):
        a, b, c = V[i - 1], V[i], V[(i + 1) % n]
        cr = (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])
        if cr < 0:
            out.append(b)
    return out

def wall_gcds(V):
    h = [abs(b[0] - a[0]) for a, b in edges(V) if a[1] == b[1]]
    v = [abs(b[1] - a[1]) for a, b in edges(V) if a[0] == b[0]]
    return reduce(gcd, h), reduce(gcd, v), sorted(h), sorted(v)

def strictly_inside(V, P):
    x, y = P
    for (x0, y0), (x1, y1) in edges(V):  # not on boundary
        if min(x0, x1) <= x <= max(x0, x1) and min(y0, y1) <= y <= max(y0, y1):
            return False
    c = 0
    for (x0, y0), (x1, y1) in edges(V):
        if x0 == x1 and x < x0 and min(y0, y1) < y <= max(y0, y1):
            c += 1
    return c % 2 == 1

def square_fits(V, x, y, s):
    """Closed axis square [x,x+s]x[y,y+s] in closed room: test sample points on a fine grid of cells (lattice rooms)."""
    for i in range(s):
        for j in range(s):
            if not strictly_inside(V, (F(2 * (x + i) + 1, 2), F(2 * (y + j) + 1, 2))):
                return False
    return True

# ---------------------------------------------------------------- exact tracer
def trace(V, S, d, T, max_steps=20000):
    """Exact billiard. Stops at any vertex (reflex -> 'reflex', convex -> 'convex') or when T is on the path."""
    E = edges(V)
    vx = set(V)
    rx = set(reflexes(V))
    px, py = F(S[0]), F(S[1])
    dx, dy = F(d[0]), F(d[1])
    Tx, Ty = F(T[0]), F(T[1])
    log = []
    for step in range(max_steps):
        best = None
        hit = []
        for (x0, y0), (x1, y1) in E:
            if x0 == x1 and dx != 0:
                t = (x0 - px) / dx
                if t > 0:
                    y = py + t * dy
                    if min(y0, y1) <= y <= max(y0, y1):
                        if best is None or t < best:
                            best, hit = t, [('v', x0, y)]
                        elif t == best:
                            hit.append(('v', x0, y))
            elif y0 == y1 and dy != 0:
                t = (y0 - py) / dy
                if t > 0:
                    x = px + t * dx
                    if min(x0, x1) <= x <= max(x0, x1):
                        if best is None or t < best:
                            best, hit = t, [('h', x, y0)]
                        elif t == best:
                            hit.append(('h', x, y0))
        # target on open segment (pos, pos+best*d] ?
        if dx != 0:
            s = (Tx - px) / dx
        else:
            s = (Ty - py) / dy
        if 0 < s <= best and px + s * dx == Tx and py + s * dy == Ty:
            return 'T', (Tx, Ty), step, log
        qx, qy = px + best * dx, py + best * dy
        log.append((qx, qy, hit[0][0]))
        if (qx, qy) in vx:
            return ('reflex' if (qx, qy) in rx else 'convex'), (qx, qy), step, log
        for k, _, _ in hit:
            if k == 'v':
                dx = -dx
            else:
                dy = -dy
        px, py = qx, qy
    return 'maxsteps', (px, py), max_steps, log

def primitive_dirs(B, bmax):
    out = []
    for p in range(1, B + 1):
        for b in range(-bmax, bmax + 1):
            if gcd(p, abs(b)) == 1:
                out += [(p, b), (-p, b)]
    return out

ok_all = True
def check(cond, msg):
    global ok_all
    ok_all &= bool(cond)
    print(('PASS ' if cond else 'FAIL ') + msg)

# ================================================================ 1. geometry
print('== 1. dumbbell geometry ==')
for B in range(1, 7):
    M = lcm(*range(1, B + 1)); a = 10 * M; U = 2 * a
    V = dumbbell(U)
    S, T = (U - a, 2), (U + 2 + a, 2)
    gh, gv, hs, vs = wall_gcds(V)
    rx = reflexes(V)
    A = area2(V) // 2
    tau_ok = square_fits(V, 0, 0, 5) and max(y for _, y in V) - min(y for _, y in V) == 5
    check(len(V) == 12 and A == 10 * U + 7 and len(rx) == 4 and gh == 1 and gv == 1 and tau_ok
          and strictly_inside(V, S) and strictly_inside(V, T) and (S[0] + S[1]) % 2 == (T[0] + T[1]) % 2,
          f'B={B} a={a} U={U}: walls={len(V)} area={A} reflex={rx} gcd_h={gh} gcd_v={gv} tau=5 S,T interior same parity')

print('-- symbolic: transverse displacement at first contact with x=U, B<=12 --')
for B in range(1, 13):
    M = lcm(*range(1, B + 1)); a = 10 * M
    good = all((a * b) % p == 0 and ((a * b) // p) % 10 == 0 and ((3 * a * b) // p) % 10 == 0
               for p in range(1, B + 1) for b in range(-50, 51))
    check(good, f'B={B}: a*b/p and 3a*b/p are multiples of 10 for all 1<=p<=B, |b|<=50')

print('-- minimality of the factor 10*lcm for this sufficient condition (10p | a for all p<=B) --')
for B in range(1, 9):
    need = lcm(*[10 * p for p in range(1, B + 1)])
    check(need == 10 * lcm(*range(1, B + 1)), f'B={B}: lcm(10,20,...,10B) = 10*lcm(1..B) = {need}')

# ================================================================ 2. witness
print('== 2. one-reflection witness (a+1,1) ==')
for B in range(1, 7):
    M = lcm(*range(1, B + 1)); a = 10 * M; U = 2 * a
    V = dumbbell(U); S, T = (U - a, 2), (U + 2 + a, 2)
    m = F(1, a + 1)
    yU = 2 + a * m; ceil_x = S[0] + (3 - 2) / m; yR = 3 - (U + 2 - ceil_x) * m; yT = yR - a * m
    sym = (yU == 3 - m and ceil_x == U + 1 and yR == 3 - m and yT == 2 and 2 < yU < 3)
    res, pt, steps, log = trace(V, S, (a + 1, 1), T)
    refl = [e for e in log]
    check(sym and res == 'T' and len(refl) == 1 and refl[0] == (U + 1, 3, 'h') and gcd(a + 1, 1) == 1,
          f'B={B}: mouth heights {yU},{yR}; ceiling hit at ({ceil_x},3); tracer -> {res} after {len(refl)} reflection(s)')

# ================================================================ 3. exhaustive tracer
print('== 3. exact tracer, all primitive |p|<=B, |b|<=30, both horizontal signs, plus axial ==')
for B in (2, 3, 4):
    M = lcm(*range(1, B + 1)); a = 10 * M; U = 2 * a
    V = dumbbell(U); S, T = (U - a, 2), (U + 2 + a, 2)
    dirs = primitive_dirs(B, 30) + [(1, 0), (-1, 0), (0, 1), (0, -1)]
    bad = []; total = 0
    for d in dirs:
        if d[0] == 0:
            # vertical: stays on x=a; tracer would bounce forever, so check analytically
            ok = 0 < S[0] < U
            if not ok: bad.append(d)
            continue
        res, pt, steps, log = trace(V, S, d, T)
        total += steps
        xs_before = [q[0] for q in log[:-1]]
        if not (res == 'reflex' and pt == (U, 2) and all(x < U for x in xs_before)):
            bad.append((d, res, pt))
    check(not bad, f'B={B} a={a}: {len(dirs)} directions, {total} reflections; all stop at ({U},2) on first contact with x=U, none reaches T. bad={bad[:3]}')

print('-- extra: a = 5*lcm(1..B) (half the stated a) also intercepts, at (U,2) or (U,3) --')
for B in (2, 3, 4):
    M = lcm(*range(1, B + 1)); a = 5 * M; U = 2 * a
    V = dumbbell(U); S, T = (U - a, 2), (U + 2 + a, 2)
    stops = set(); bad = []
    for d in primitive_dirs(B, 30) + [(1, 0), (-1, 0)]:
        res, pt, steps, log = trace(V, S, d, T)
        if res != 'reflex' or pt not in ((U, 2), (U, 3)):
            bad.append((d, res, pt))
        stops.add(pt)
    res, pt, _, _ = trace(V, S, (a + 1, 1), T)
    check(not bad and res == 'T', f'B={B} a={a}: stops at {sorted(stops)}; witness (a+1,1) -> {res}; bad={bad[:3]}')

print('-- control: a non-multiple a (a = 10*lcm + 1) lets some |p|<=B direction cross the doorway --')
for B in (2, 3):
    a = 10 * lcm(*range(1, B + 1)) + 1; U = 2 * a
    V = dumbbell(U); S, T = (U - a, 2), (U + 2 + a, 2)
    crossed = 0
    for d in primitive_dirs(B, 30):
        res, pt, steps, log = trace(V, S, d, T, max_steps=3000)
        if any(q[0] > U for q in log) or res == 'T':
            crossed += 1
    check(crossed > 0, f'B={B} a={a}: {crossed} directions get past x=U (tracer is not trivially absorbing)')

# ================================================================ 4. compression lemma
print('== 4. periodic compression ==')
tau0 = 5; Lc = lcm(*range(1, tau0 + 1))
# 4a dumbbell B=1, witness (11,1); lengthen long x gap (S.x, U) by Delta
a, U = 10, 20
for Delta, expect in ((2 * 11 * Lc, True), (11 * Lc, True), (11, False), (1, False)):
    V = dumbbell(U + Delta); S, T = (a, 2), (U + Delta + 2 + a, 2)
    res, pt, _, _ = trace(V, S, (11, 1), T)
    tag = 'period multiple' if Delta % (2 * 11 * Lc) == 0 else ('Delta*b/p in 2h Z' if (Delta * 1) % (11 * 10) == 0 else 'not a period')
    check((res == 'T') == expect, f'dumbbell U=20 gap +{Delta} ({tag}): direction (11,1) -> {res}')

# 4b named L room, tau=3, long x and y gaps simultaneously
X = Y = 40; w = 3; tau0 = 3; Lc = lcm(1, 2, 3)
V = lroom(X, Y, w); S, T = (20, 1), (1, 20)
gh, gv, _, _ = wall_gcds(V)
print(f'L room {V}: tau={w}, reflexes={reflexes(V)}, S={S}, T={T}')
found = []
for p in range(1, 9):
    for b in range(1, 9):
        if gcd(p, b) == 1:
            for d in ((-p, b), (-p, -b)):
                res, pt, steps, log = trace(V, S, d, T, max_steps=400)
                if res == 'T':
                    found.append((d, len(log)))
print('directions with |p|,|b|<=8 from S lighting T in the L room:', found[:6])
check(len(found) > 0, 'L room has at least one lighting direction in the small box')
for (d, nref) in found[:3]:
    p, b = abs(d[0]), abs(d[1])
    for kx, ky in ((1, 1), (2, 1), (1, 3)):
        Dx, Dy = kx * 2 * p * Lc, ky * 2 * b * Lc
        # x grid 0,1,3,20,40: long gaps (3,20),(20,40); lengthen (3,20) by Dx and y gap (3,20) by Dy
        V2 = lroom(X + Dx, Y + Dy, w); S2, T2 = (20 + Dx, 1), (1, 20 + Dy)
        res, pt, _, log2 = trace(V2, S2, d, T2)
        # the lemma preserves signed strip exits, not the number of transverse reflections inside a strip
        check(res == 'T',
              f'L room dir {d}: lengthen x gap by {Dx}, y gap by {Dy} simultaneously -> {res}, reflections {len(log2)} (orig {nref}; count may grow inside strips)')
    V2 = lroom(X + 1, Y, w); S2, T2 = (21, 1), (1, 20)
    res, _, _, _ = trace(V2, S2, d, T2)
    print(f'     control: dir {d} after x-gap +1 (not a period) -> {res}')

# 4c strip claim inside long gaps of the L room: components are full-width rectangles of height <= tau0
def slab_components(V, x0, x1):
    xm = F(x0 + x1, 2)
    ys = sorted(set(y for _, y in V))
    occ = [(ys[i], ys[i + 1]) for i in range(len(ys) - 1) if strictly_inside(V, (xm, F(ys[i] + ys[i + 1], 2)))]
    comps = []
    for lo, hi in occ:
        if comps and comps[-1][1] == lo:
            comps[-1] = (comps[-1][0], hi)
        else:
            comps.append((lo, hi))
    # full width: no vertical wall strictly inside (x0,x1)
    full = all(not (x0 < ax < x1) for (ax, _), (bx, _) in edges(V) if ax == bx)
    return comps, full
for (x0, x1) in ((3, 20), (20, 40)):
    comps, full = slab_components(V, x0, x1)
    check(full and all(hi - lo <= tau0 for lo, hi in comps), f'L room x gap ({x0},{x1}): components {comps}, no interior vertical wall={full}')
gaps = [3, 20 - 3, 40 - 20]
print('L room x grid gaps (with mark line x=1):', [1, 2, 17, 20], '-> 4 gaps; bound 11*max holds trivially')

print(f'elapsed {time.time() - T0:.1f}s; overall', 'PASS' if ok_all else 'FAIL')
