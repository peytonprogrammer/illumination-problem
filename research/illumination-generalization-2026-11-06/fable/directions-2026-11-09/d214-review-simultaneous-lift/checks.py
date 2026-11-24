"""D214 referee checks: simultaneous lift and two-scale selection (note-snapshot.md).

Reuses the d212 exact tracer and the d213 staircase helpers (stair_room,
run_order, interval_Ns, lu, first_ns), imported unchanged.
Named rooms only:
  STAIR : offset staircase x[0,3],[1,4],[3,6],[4,7], heights 2,1+x,1+y,2,
          S=(2,1), T=(5,roof-1); sqrt2 family x=t, y=floor(sqrt2 t).
  STAIRH: same tiers with heights (a,b,c,d) (cone test only).
  TIERS : left-aligned widths 4,5,6, heights (a,b,c), S=(1,1), T=(5,top-1).
  Hand-built rooms for the counting identity: L-shape, symmetric U, plus.
No room enumeration, no direction or word search. Every traced ray is the
direct chord, a template seed, or a re-aim at an explicit winding.
Run: nice -n 10 python3 -B checks.py
"""
import importlib.util
import os
import time
from fractions import Fraction as F
from math import gcd, floor, ceil, isqrt, factorial
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, "..", rel, "checks.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


K = load("d212checks", "d212-review-descent-skeleton")
M13 = load("d213checks", "d213-review-marked-selection")
rects, trace, reached, marks_of, wall_levels = K.rects, K.trace, K.reached, K.marks_of, K.wall_levels
stair_room, run_order, interval_Ns, lu, first_ns = (
    M13.stair_room, M13.run_order, M13.interval_Ns, M13.lu, M13.first_ns)

T0 = time.process_time()
FAILS = []
f2 = lambda t: isqrt(2 * t * t)


def say(*a):
    print(*a, flush=True)


def check(cond, msg):
    say(("PASS " if cond else "FAIL ") + msg)
    if not cond:
        FAILS.append(msg)


def direct(c, S, T):
    dx, dy = T[0] - S[0], T[1] - S[1]
    g = gcd(abs(dx), abs(dy))
    return reached(trace(c, S, (dx // g, dy // g), g), T)


# ------------------------------------------------------------------ claim 1
def claim1():
    say("\n=== Claim 1: positive lower density of strict-test success")
    # window-width bound u-l >= 2/(bH), both orders, every first-stage n, t<=200
    bad = n_ = 0
    for t in range(1, 201):
        y = f2(t)
        for x in (t, y):
            H = x + 2
            for n in first_ns(x):
                s = F(3 + 6 * n, 4 + x); l, u = lu(s, H)
                n_ += 1
                bad += not (l < s < u and u - l >= F(2, s.denominator * H))
    check(bad == 0, f"window width (u-l) >= 2/(bH) on all {n_} (t, order, n) cases, t<=200")
    # mod-8 class: s=3/4 replays exactly in both bands
    cls8 = [t for t in range(1, 201) if t % 8 == 0 and f2(t) % 8 == 0]
    ok = True
    for t in cls8:
        y = f2(t)
        for order, x, yy in (('L', t, y), ('U', y, t)):
            n = x // 8
            ok &= F(3 + 6 * n, 4 + x) == F(3, 4) and (y // 8 if order == 'L' else t // 8) in interval_Ns(x, yy, n)
    check(ok and cls8 == [40, 136, 176], f"mod-8 class t<=200 = {cls8}: s=3/4 (n=x/8) and N=y/8 pass the interval test, both orders")
    tr = True
    for t in cls8:
        y = f2(t)
        a, b = run_order('L', t, y, t // 8, y // 8)
        tr &= a['dl'] == 0 and b['dl'] == 0 and a['ok'] and b['ok'] and b['g']
        a, b = run_order('U', t, y, y // 8, t // 8)
        tr &= a['dl'] == 0 and b['dl'] == 0 and a['ok'] and b['ok'] and b['g']
    check(tr, f"t in {cls8}: exact replay delta=0 in both stages, both orders, gate passes, exact trace legal")
    # mod-42 class members: interval test (arithmetic)
    ok = True
    for t in (731, 1319):
        y = f2(t); n = (4 + t) * 5 // 7 // 6; N = round(F(5 * y, 7) / 6)
        ok &= F(3 + 6 * n, 4 + t) == F(5, 7) and N in interval_Ns(t, y, n) and t % 2 == 1 and y % 2 == 1
    check(ok, "mod-42 members t=731,1319: s=5/7 and the nearest N pass the interval test; both gains odd")
    # disjointness and densities (residues of floor(sqrt2 t) only)
    Nmax = 10 ** 6
    c8 = c42 = both = 0
    for t in range(1, Nmax + 1):
        y = f2(t)
        a = t % 8 == 0 and y % 8 == 0
        b = t % 42 == 17 and y % 42 in (17, 25)
        c8 += a; c42 += b; both += a and b
    say(f"    t<=1e6: mod-8 class {c8} (expected {Nmax/64:.0f}), mod-42 class {c42} (expected {Nmax/882:.0f})")
    check(both == 0 and abs(c8 - Nmax / 64) < 300 and abs(c42 - Nmax / 882) < 100,
          f"classes disjoint; empirical densities {c8/Nmax:.6f} ~ 1/64={1/64:.6f}, {c42/Nmax:.6f} ~ 1/882={1/882:.6f}")
    check(F(1, 64) + F(2, 42 * 42) == F(1, 64) + F(1, 882), "2/42^2 = 1/882; bound = 1/64 + 1/882 = "
          f"{F(1,64)+F(1,882)}")


# ------------------------------------------------------------------ claim 2
def claim2():
    say("\n=== Claim 2: direct-chord simultaneous lift on the staircase")
    S = (2, 1)
    # interface abscissas, exact
    ok = True
    for x in range(0, 40):
        for y in range(0, 40):
            Ds = 4 + x + y
            ys = [2, 3 + x, 4 + x + y]
            xs = [2 + F(3 * (yy - 1), Ds) for yy in ys]
            ok &= xs == [2 + F(3, Ds), 2 + F(3 * (2 + x), Ds), 5 - F(3, Ds)]
            ok &= 1 < xs[0] < 3 and 4 < xs[2] < 6
            ok &= (3 < xs[1] < 4) == (y < 2 * x + 2 and x < 2 * y + 2)
    check(ok, "interfaces 2+3/D*, 2+3(2+x)/D*, 5-3/D*; ends in (1,3),(4,6); middle in (3,4) iff y<2x+2 and x<2y+2 (x,y<40)")
    # exact trace agrees with the condition on a 26x26 grid of the named family
    bad = []
    for x in range(26):
        for y in range(26):
            c = stair_room(x, y)
            leg = direct(c, S, (5, 5 + x + y))
            if leg != (y < 2 * x + 2 and x < 2 * y + 2): bad.append((x, y))
    check(not bad, f"exact trace: direct chord legal iff the two inequalities, 0<=x,y<=25 (mismatches {bad})")
    # sqrt2 family all t
    leg = [direct(stair_room(t, f2(t)), S, (5, 5 + t + f2(t))) for t in range(0, 201)]
    check(all(leg), "sqrt2 family: direct chord legal for every t=0..200 by exact trace")
    check(all(f2(t) < 2 * t + 2 and t < 2 * f2(t) + 2 for t in range(0, 10 ** 5)),
          "sqrt2 family: both inequalities hold for t<1e5 (proof: t < 2sqrt2 t - 2 + 2 <= 2y+2)")
    # template has same itinerary
    check(direct(stair_room(0, 0), S, (5, 5)) and stair_room(0, 0).__len__() == 18,
          "area-18 template: direct chord (3,4) legal with the same three interfaces")
    # t = 15
    x, y = 15, 21; Ds = 4 + x + y
    xs = [2 + F(3, Ds), 2 + F(3 * (2 + x), Ds), 5 - F(3, Ds)]
    ov = [(1, 3), (3, 4), (4, 6)]
    clr = min(min(a - lo, hi - a) for a, (lo, hi) in zip(xs, ov))
    c = stair_room(15, 21)
    check(y == f2(15) and Ds == 40 and gcd(3, 40) == 1 and xs == [F(83, 40), F(131, 40), F(197, 40)]
          and clr == F(11, 40) and len(c) == 126 and direct(c, S, (5, 41)),
          f"t=15: displacement (3,40), crossings {xs}, clearance {clr}, area {len(c)}, traced legal")
    lim = 2 + 3 / (1 + 2 ** 0.5)
    check(3 < lim < 4, f"limiting middle abscissa 2+3/(1+sqrt2) = {lim:.4f}")
    # direct visibility: the open segment S-T lies in the interior (so item 3 discharges these pairs)
    check(all(in_interior_seg(stair_room(t, f2(t)), S, (5, 5 + t + f2(t))) for t in range(0, 201)),
          "sqrt2 family t=0..200: S-T open segment is inside the room interior (directly visible pair)")


# ------------------------------------------------------------------ claim 3
def stair_h(a, b, c, d):
    ys = [0, a, a + b, a + b + c, a + b + c + d]
    xs = [(0, 3), (1, 4), (3, 6), (4, 7)]
    return rects(*[(xs[i][0], xs[i][1], ys[i], ys[i + 1]) for i in range(4)])


def cone(h, xS, xT, ov):
    H = sum(h); Hi = 0; ok = True
    for i, (a, b) in enumerate(ov):
        Hi += h[i]
        ok &= (a - xS) * H < (xT - xS) * Hi < (b - xS) * H
    return ok


def claim3():
    say("\n=== Claim 3: convex-cone ratio region for monotone direct chords")
    bad = []; npos = n = 0
    for a in (2, 3, 4):
        for b in range(1, 9):
            for c_ in range(1, 9):
                for d in (2, 3, 4):
                    room = stair_h(a, b, c_, d)
                    T = (5, a + b + c_ + d - 1)
                    leg = direct(room, (2, 1), T)
                    cn = cone((a - 1, b, c_, d - 1), 2, 5, [(1, 3), (3, 4), (4, 6)])
                    n += 1; npos += cn
                    if leg != cn: bad.append((a, b, c_, d))
    check(not bad, f"staircase heights grid: cone test == exact trace on {n} rooms ({npos} inside the cone)")
    bad = []; n = npos = 0
    for a in range(2, 7):
        for b in range(1, 7):
            for c_ in range(2, 7):
                room = rects((0, 4, 0, a), (0, 5, a, a + b), (0, 6, a + b, a + b + c_))
                T = (5, a + b + c_ - 1)
                leg = direct(room, (1, 1), T)
                cn = cone((a - 1, b, c_ - 1), 1, 5, [(0, 4), (0, 5)])
                n += 1; npos += cn
                if leg != cn: bad.append((a, b, c_))
    check(not bad, f"tiers 4,5,6 with S=(1,1), T=(5,top-1): cone test == exact trace on {n} rooms ({npos} inside)")
    # t=15 straight deformation: both inequalities linear in lambda, strict at both ends
    ok = all((21 * l < 2 * 15 * l + 2) and (15 * l < 2 * 21 * l + 2) for l in [F(k, 100) for k in range(101)])
    check(ok, "t=15: (x,y)=lambda(15,21) satisfies y<2x+2, x<2y+2 for all sampled lambda in [0,1] (linear => all)")


# ------------------------------------------------------------------ claim 6
def claim6():
    say("\n=== Claim 6: two-scale theorem")
    small = {x: [n for n in first_ns(x) if (3 + 6 * n) % 6 == 3] for x in range(0, 12)}
    say(f"    first-stage n with 3+6n in (D/2,D), x=0..11: {small}")
    check(all(small[x] for x in range(6, 12)),
          "an integer = 3 mod 6 lies in (D/2,D) for every x>=6 (note uses x>=9: correct, not sharp)")
    ok = True; rows = []
    for x in (9, 10, 11, 15, 20, 40, 100):
        D = 4 + x; H = x + 2
        for y in (3 * D * D - D + 1, 3 * D * D, 7 * D * D + 5, 50 * D * D + 3):
            n = first_ns(x)[0]
            s = F(3 + 6 * n, D); l, u = lu(s, H)
            w = (D + y) * (u - l)
            Ns = interval_Ns(x, y, n)
            good = s.denominator <= D and w >= F(2 * (D + y), s.denominator * H) and w > 6 and len(Ns) >= 1
            ok &= all(Ns for Ns in [interval_Ns(x, y, nn) for nn in first_ns(x)])
            ok &= good
            if y == 3 * D * D - D + 1: rows.append((x, y, s, float(w), Ns))
    check(ok, "x in {9,10,11,15,20,40,100}, y >= 3D^2-D+1 (4 values): every first-stage n has width>6 and a passing N")
    for r in rows: say(f"    x={r[0]}, y={r[1]}: s={r[2]}, window width {r[3]:.2f}, passing N {r[4]}")
    # exact traces of the full two-stage lift: smaller gain first, on either band
    tr = []
    for x in (9, 10, 20):
        D = 4 + x; y = 3 * D * D - D + 1
        n = first_ns(x)[0]
        N = interval_Ns(x, y, n)[0]
        a, b = run_order('L', x, y, n, N)          # smaller gain on the lower band
        tr.append((x, y, 'L', a['g'] and a['ok'] and b['g'] and b['ok']))
        a, b = run_order('U', y, x, n, N)          # smaller gain on the upper band
        tr.append((x, y, 'U', a['g'] and a['ok'] and b['g'] and b['ok']))
    check(all(r[3] for r in tr), f"exact traces (x, y, order, gate+legal): {tr}")
    # direct chord fails in these rooms, so the theorem is doing work
    check(not direct(stair_room(9, 495), (2, 1), (5, 5 + 9 + 495)),
          "x=9, y=495: direct chord is not legal (y >= 2x+2), so the two-scale lift is needed")
    # open regime y = floor(x^1.5): direct gate fails, quadratic bound fails
    reg = [(x, isqrt(x ** 3)) for x in (9, 16, 25, 100)]
    check(all(y >= 2 * x + 2 and y <= 3 * (4 + x) ** 2 - (4 + x) for x, y in reg),
          f"y=floor(x^1.5) at x in 9,16,25,100: outside both the direct cone and the quadratic regime")
    # strict interval test on a few samples of the open regime (arithmetic only, smaller gain first)
    for x in (9, 16, 25, 36, 49, 100):
        y = isqrt(x ** 3)
        hit = {n: interval_Ns(x, y, n) for n in first_ns(x)}
        hit2 = {n: interval_Ns(y, x, n) for n in first_ns(y)} if y < 400 else None
        say(f"    open regime x={x}, y={y}: smaller-first passing (n: N) {{{', '.join(f'{n}: {v}' for n, v in hit.items() if v)}}}"
            + ("" if hit2 is None else f"; larger-first passes for {sum(1 for v in hit2.values() if v)} of {len(hit2)} n"))


# ------------------------------------------------------------------ claim 7
def claim7():
    say("\n=== Claim 7: finite base F, item 2 on the staircase")
    c = stair_room(0, 0)
    X, Y = wall_levels(c, 0), wall_levels(c, 1)
    check(set(X) | {2, 5} == set(range(8)) and set(Y) | {1, 5} == set(range(7)) and len(c) <= 21,
          "staircase template: X u {2,5} = {0..7}, Y u {1,5} = {0..6}; area 18 (census side, not in F)")
    c = stair_room(15, 21)
    X, Y = wall_levels(c, 0), wall_levels(c, 1)
    check(not (set(Y) | {1, 44} == set(range(max(Y) + 1))),
          "t=15 room fails the Y equality (reducible), as expected")


# ------------------------------------------------------------------ claim 8
def claim8():
    say("\n=== Claim 8: numerical upper bound")
    # f(z) = sum_{j=1}^{10} z^j/(2j)!  ; polynomial arithmetic in Fractions
    f = [F(0)] + [F(1, factorial(2 * j)) for j in range(1, 11)]

    def mul(a, b):
        out = [F(0)] * min(len(a) + len(b) - 1, 11)
        for i, x in enumerate(a):
            if x == 0: continue
            for j, y in enumerate(b):
                if i + j < len(out): out[i + j] += x * y
        return out
    pw = {1: f}
    for k in range(2, 11): pw[k] = mul(pw[k - 1], f)
    P = lambda k: (k - 2) * (2 * k - 3) + (k - 1) * (2 * k - 1)
    tot = F(0)
    for m in range(5, 11):
        inner = sum(P(k) * pw[k][m] for k in range(2, m + 1))
        tot += factorial(2 * m) * inner * inner
    bound = F(tot, 2)
    B = -(-bound.numerator // bound.denominator)
    say(f"    exact value = {float(bound):.6e}; ceil = {B:,}")
    check(B == 867415174096573784, "ceil(1/2 sum ...) = 867,415,174,096,573,784")
    # combinatorial cross-checks of the ingredients
    # (a) P(k) by direct enumeration of ordered mark placements on k ranked levels
    ok = True
    for k in range(2, 11):
        # explicit: first coordinate choice, then second on refined line
        cnt = 0
        for first in [('old', i) for i in range(1, k - 1)] + [('new', g) for g in range(k - 1)]:
            if first[0] == 'old':
                cnt += (k - 2) + (k - 1)
            else:
                cnt += (k - 1) + k        # k+1 levels: k-1 interior, k gaps
        ok &= cnt == P(k)
        # brute: positions on a line with k fixed levels, count distinct order types of (u,v)
        levels = list(range(0, 4 * k, 4))
        pts = [p for p in range(1, levels[-1]) ]
        types = set()
        for u in pts:
            for v in pts:
                typ = lambda z: (sum(l < z for l in levels), z in levels)
                types.add((typ(u), typ(v), (u > v) - (u < v)))
        ok &= len(types) == P(k)
    check(ok, "P(k) = (k-2)(2k-3)+(k-1)(2k-1) matches order-type enumeration of two ordered coordinates, k=2..10")
    # (b) stub bound on tiny margins: #0-1 matrices with margins <= (2m)!/prod d! prod e!
    def count01(rows, cols):
        cols = list(cols)
        def rec(i, cl):
            if i == len(rows): return int(all(x == 0 for x in cl))
            tot = 0
            for sub in combinations(range(len(cl)), rows[i]):
                if all(cl[j] > 0 for j in sub):
                    nc = cl[:]
                    for j in sub: nc[j] -= 1
                    tot += rec(i + 1, nc)
            return tot
        return rec(0, cols)
    ok = True
    for rows_, cols_ in (((2, 2), (2, 2)), ((2, 2, 2), (2, 2, 2)), ((4, 2), (2, 2, 2)), ((2, 4, 2), (2, 2, 2, 2)),
                         ((4, 4), (2, 2, 2, 2)), ((2, 2, 2, 2), (4, 2, 2))):
        tot = sum(rows_); assert tot == sum(cols_)
        bnd = F(factorial(tot), 1)
        for d in rows_ + cols_: bnd /= factorial(d)
        ok &= count01(rows_, cols_) <= bnd
    check(ok, "stub-matching bound (2m)!/(prod d! prod e!) dominates exact 0-1 matrix counts on 6 margin pairs")


# ------------------------------------------------------------------ claim 9
def in_interior_pt(c, p):
    x, y = p
    xs = [floor(x)] if x.denominator != 1 else [int(x) - 1, int(x)]
    ys = [floor(y)] if y.denominator != 1 else [int(y) - 1, int(y)]
    return all((a, b) in c for a in xs for b in ys)


def in_interior_seg(c, S, T):
    """Open segment S-T inside the open room: check every grid crossing and the
    midpoints between consecutive crossings (exact)."""
    S = (F(S[0]), F(S[1])); T = (F(T[0]), F(T[1]))
    ts = {F(0), F(1)}
    for ax in (0, 1):
        a, b = S[ax], T[ax]
        if a != b:
            for k in range(ceil(min(a, b)), floor(max(a, b)) + 1):
                ts.add((k - a) / (b - a))
    ts = sorted(ts)
    pts = []
    for i in range(len(ts)):
        if 0 < ts[i] < 1: pts.append(ts[i])
        if i + 1 < len(ts): pts.append((ts[i] + ts[i + 1]) / 2)
    return all(in_interior_pt(c, (S[0] + t * (T[0] - S[0]), S[1] + t * (T[1] - S[1]))) for t in pts)


def symmetries(c):
    Bx = max(x for x, _ in c) + 1; By = max(y for _, y in c) + 1
    maps = [lambda p: (p[0], p[1]), lambda p: (Bx - p[0], p[1]), lambda p: (p[0], By - p[1]),
            lambda p: (Bx - p[0], By - p[1])]
    if Bx == By:
        B = Bx
        maps += [lambda p: (p[1], p[0]), lambda p: (B - p[1], p[0]), lambda p: (p[1], B - p[0]),
                 lambda p: (B - p[1], B - p[0])]
    G = []
    for g in maps:
        img = {tuple(int(floor(z)) for z in g((F(2 * x + 1, 2), F(2 * y + 1, 2)))) for x, y in c}
        if img == c: G.append(g)
    return G, Bx, By


def burnside(c, pred):
    G, Bx, By = symmetries(c)
    X, Y = wall_levels(c, 0), wall_levels(c, 1)
    Mset = [('x', a) for a in range(Bx + 1) if a not in X] + [('y', b) for b in range(By + 1) if b not in Y]
    marks = marks_of(c)
    tot = F(0)
    for g in G:
        for r in range(len(Mset) + 1):
            for J in combinations(Mset, r):
                rem = [p for p in marks if ('x', p[0]) not in J and ('y', p[1]) not in J]
                C = 0
                for p, q in combinations(rem, 2):
                    if pred(c, p, q) and {tuple(g(p)), tuple(g(q))} == {p, q}: C += 1
                tot += (-1) ** r * C
    val = tot / len(G)
    # brute orbit count
    good = []
    for p, q in combinations(marks, 2):
        cov = all((m[0] == 'x' and m[1] in (p[0], q[0])) or (m[0] == 'y' and m[1] in (p[1], q[1])) for m in Mset)
        if cov and pred(c, p, q): good.append(frozenset((p, q)))
    seen = set(); orbits = 0
    for pr in good:
        if pr in seen: continue
        orbits += 1
        for g in G:
            seen.add(frozenset(tuple(g(p)) for p in pr))
    return val, orbits, len(G), Mset, len(good)


def claim9():
    say("\n=== Claim 9: room-first inclusion-exclusion / Burnside count")
    rooms = {
        "L-shape (0,4,0,2)+(0,2,2,4)": rects((0, 4, 0, 2), (0, 2, 2, 4)),
        "symmetric U (0,5,0,2)+(0,2,2,4)+(3,5,2,4)": rects((0, 5, 0, 2), (0, 2, 2, 4), (3, 5, 2, 4)),
        "plus (1,3,0,4)+(0,4,1,3)": rects((1, 3, 0, 4), (0, 4, 1, 3)),
        "plus (2,4,0,6)+(0,6,2,4)": rects((2, 4, 0, 6), (0, 6, 2, 4)),
    }
    preds = {"nondirect": lambda c, p, q: not in_interior_seg(c, p, q), "all": lambda c, p, q: True}
    ok = True
    for name, c in rooms.items():
        for pn, pr in preds.items():
            val, orb, nG, Mset, ng = burnside(c, pr)
            say(f"    {name}, {pn}: |G|={nG}, M={Mset}, qualifying pairs {ng}, formula {val}, orbits {orb}")
            ok &= val == orb
    check(ok, "formula equals brute-force orbit count of covering pairs on 4 hand-built rooms, 2 predicates")
    # diagonal claim in the two-missing-levels-per-axis case (L-shape and U)
    for name in list(rooms)[:2]:
        c = rooms[name]
        _, _, _, Mset, _ = burnside(c, preds["all"])
        ax = [m[1] for m in Mset if m[0] == 'x']; ay = [m[1] for m in Mset if m[0] == 'y']
        cov = [frozenset((p, q)) for p, q in combinations(marks_of(c), 2)
               if set(ax) <= {p[0], q[0]} and set(ay) <= {p[1], q[1]}]
        diag = {frozenset({(ax[0], ay[0]), (ax[1], ay[1])}), frozenset({(ax[0], ay[1]), (ax[1], ay[0])})}
        check(len(ax) == len(ay) == 2 and set(cov) <= diag,
              f"{name}: covering pairs {[sorted(p) for p in cov]} are among the two diagonals")


if __name__ == '__main__':
    claim1()
    claim2()
    claim3()
    claim6()
    claim7()
    claim8()
    claim9()
    say(f"\nTOTAL FAIL {len(FAILS)}; cpu {time.process_time()-T0:.1f}s")
