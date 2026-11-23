"""d181 review checks for l1-open-collar-gluing.md and l1-remote-wall-return.md (snapshot 1921).

Named rooms only (DBas, DB55 from d110 geom.ROOMS; the d161 six-wall L(3,3,3) hall), exact Fraction
arithmetic, no room/ray/direction/word searches. Every traced velocity is the one the notes'
constructions prescribe. trace() is copied verbatim from d175-review-windinglimits/checks.py.
Run: python3 -B checks.py > checks.log
"""
import time
from fractions import Fraction as F
from math import ceil, floor

T0 = time.process_time()
FAIL = []


def log(*a):
    print(*a, flush=True)


def check(ok, msg):
    log(('  PASS ' if ok else '  FAIL ') + msg)
    if not ok:
        FAIL.append(msg)


# ------------------------------------------------------------------ copied verbatim from d175
def trace(P, A, B, maxrefl=10**6):
    n = len(P)
    hw = [(P[i], P[(i + 1) % n]) for i in range(n) if P[i][1] == P[(i + 1) % n][1]]
    vw = [(P[i], P[(i + 1) % n]) for i in range(n) if P[i][0] == P[(i + 1) % n][0]]
    V = {(F(a), F(b)) for a, b in P}
    X, Y = F(A[0]), F(A[1])
    vx, vy = F(B[0]) - X, F(B[1]) - Y
    tau, contacts = F(1), []
    for _ in range(maxrefl):
        best = None
        if vx:
            for a, b in vw:
                t = (a[0] - X) / vx
                if t > 0 and (best is None or t < best[0]) and min(a[1], b[1]) <= Y + vy * t <= max(a[1], b[1]):
                    best = (t, 'v')
        if vy:
            for a, b in hw:
                t = (a[1] - Y) / vy
                if t > 0 and (best is None or t < best[0]) and min(a[0], b[0]) <= X + vx * t <= max(a[0], b[0]):
                    best = (t, 'h')
        if best is None or best[0] > tau:
            return 'end', (X + vx * tau, Y + vy * tau), contacts
        t, kind = best
        X, Y = X + vx * t, Y + vy * t
        if best[0] == tau:
            return 'wall-end', (X, Y), contacts
        tau -= t
        if (X, Y) in V:
            return 'corner', (X, Y), contacts
        contacts.append(((X, Y), kind))
        if kind == 'v': vx = -vx
        else: vy = -vy
    return 'limit', (X, Y), contacts


def fr(p):
    return '(' + ','.join(str(c) for c in p) + ')'


def fl(q, k=6):
    return f"{float(q):.{k}f}"


# ------------------------------------------------------------------ d110 geom (copied data)
ROOMS = {  # d69-bbbb/decomp.py base rooms; the corridor length L is free
    'DBas': (5, 0, 4, 4, -1, 6, 1, 1),
    'DB55': (5, 0, 5, 5, 0, 5, 2, 1),
}


def dumbbell(d1, b1, h1, d2, b2, h2, p, w, L):  # copied from d110 geom.py
    assert b1 < p and p + w < b1 + h1 and b2 < p and p + w < b2 + h2
    x2 = d1 + L
    V = [(0, b1), (d1, b1), (d1, p), (x2, p), (x2, b2), (x2 + d2, b2), (x2 + d2, b2 + h2),
         (x2, b2 + h2), (x2, p + w), (d1, p + w), (d1, b1 + h1), (0, b1 + h1)]
    return dict(d1=d1, b1=b1, h1=h1, d2=d2, b2=b2, h2=h2, p=p, w=w, L=L, V=V)


def rect(x0, x1, y0, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


# ================================================================== 1. thresholds
log("# 1. Open-collar thresholds: note's m = 4*ceil(D^2) against d124's m = 4*max(area)")
for name in ROOMS:
    d1, b1, h1, d2, b2, h2, p, w = ROOMS[name]
    areas = (d1 * h1, d2 * h2)
    D2 = max(d1 * d1 + h1 * h1, d2 * d2 + h2 * h2)
    m124 = 4 * max(areas)
    mnote = 4 * D2  # D^2 is an integer for lattice chambers
    check(max(areas) <= D2, f"{name}: max area {max(areas)} <= D^2 = {D2}; m(d124)={m124}, m(note)={mnote}")
    for lab, m in (('d124', m124), ('note', mnote)):
        H = 1 + 2 * fib(3 * m)
        Z = 36 * w * H * H
        log(f"   {name} {lab}: H = 1+2F_{3*m} has {len(str(H))} digits; Z = 36wH^2 has {len(str(Z))} digits")
    check(w <= D2 ** 0.5, f"{name}: w={w} <= D")
# one-leg interval arithmetic: |I| = 1/(6H^2); one removed slope leaves >= 1/(12H^2) >= 1/(18H^2)
Hs = F(10 ** 6)
I = 2 / (12 * Hs * Hs)
check(I / 2 >= 1 / (18 * Hs * Hs) and I / 3 == 1 / (18 * Hs * Hs),
      "one-leg component >= |I|/2 = 1/(12H^2) >= 1/(18H^2); two removals give |I|/3 = 1/(18H^2)")
check(all((z + a) / (18 * Hs * Hs) > 2 * w for w in (1, 2, 5) for a in (F(1, 10 ** 9),)
          for z in (36 * w * Hs * Hs,)), "(z+a)/(18H^2) > 2w at z = 36wH^2 for any a > 0")

# ================================================================== 2. d161 cap avoidance
log("\n# 2. d161 shots in the L(3,3,3) test domain with the right arm extended to a far cap")
# hall [-5,0]x[-2,0]; upper arm [-5,0]x[0,4] (cap y=4); right arm [0,R]x[-2,0] (cap x=R).
# Sealed chamber A = hall + upper arm + right arm up to x=1; the open mouth is x=1, the strip is x>1.
R = 1000
LP = [(-5, -2), (R, -2), (R, 0), (0, 0), (0, 4), (-5, 4)]
Wh, Hh = 5, 2


def first_above(a, r, period):
    j = (a - r) // period + 1
    return r + period * j


def d161_shot(S, T):
    """S=(X,-U) in the right arm, T=(-V,Y) in the upper arm; returns start, unfolded end, target, case."""
    X, U, V, Y = F(S[0]), -F(S[1]), -F(T[0]), F(T[1])
    if X * Y < U * V:
        return S, T, T, 'direct', None
    if X >= V:
        a, b = X * Y / V, X * Y / V + Hh * (1 + X / V)
        Z = min(first_above(a, U, 2 * Hh), first_above(a, -U, 2 * Hh))
        assert a < Z < b
        return T, (X, -Z), S, 'right', (a, b, Z)
    a, b = X * Y / U, X * Y / U + Wh * (1 + Y / U)
    Z = min(first_above(a, V, 2 * Wh), first_above(a, -V, 2 * Wh))
    assert a < Z < b
    return S, (-Z, Y), T, 'upper', (a, b, Z)


pairs = [((3, -1), (-3, 3)), ((50, F(-3, 2)), (-3, 3)), ((997, F(-1, 3)), (F(-1, 2), F(7, 2))),
         ((1, F(-1, 4)), (-4, 3)), ((F(3, 2), F(-1, 2)), (F(-9, 2), F(1, 2))), ((1, -1), (-1, F(1, 3)))]
for S, T in pairs:
    A0, B0, tgt, case, info = d161_shot(S, T)
    ev, end, con = trace(LP, A0, B0)
    ok = ev == 'end' and end == (F(tgt[0]), F(tgt[1]))
    capfree = all(c[0] != R and c[1] != 4 for c, _ in con)
    if case == 'right':
        sides = all(k == 'h' and c[1] in (0, -2) and 0 < c[0] < F(S[0]) for c, k in con)
    elif case == 'upper':
        sides = all(k == 'v' and c[0] in (0, -5) and 0 < c[1] < F(T[1]) for c, k in con)
    else:
        sides = not con
    check(ok and capfree and sides, f"strip mark {fr(S)} (depth {fl(F(S[0]) - 1, 3)}) <-> A mark {fr(T)}: "
          f"case {case}, {len(con)} contacts, reaches target, no cap contact, only parallel-side contacts")
log("   The direct-chord cases (bar pairs, seam points) have no contacts by convexity of the bar.")

# ================================================================== 3. remote-wall return
log("\n# 3. Remote-wall return: algebra, then exact traces on DBas and DB55 at several corridor lengths")


def sealed_chamber(r, side):
    x2 = r['d1'] + r['L']
    if side == 'left':
        return rect(0, r['d1'], r['b1'], r['b1'] + r['h1']), r['d1']
    return rect(x2, x2 + r['d2'], r['b2'], r['b2'] + r['h2']), x2


def remote(name, side, Srel, hx, vy, s0, X, Ls, label, below=()):
    """Reference sealed shot in chamber `side` from S (x relative to that chamber's left wall),
    horizontal sign hx, vertical sign vy, slope s0, horizontal travel X. B is the opposite rectangle;
    its far wall spans the whole corridor height, so J_i = (0,w) and d = B's depth."""
    log(f"\n## {label}: {name}, A = {side} chamber, S_rel={fr(Srel)}, signs ({hx},{vy}), s0={s0}, X={X}")
    s0, X = F(s0), F(X)
    for L in Ls:
        r = dumbbell(*ROOMS[name], L)
        w, p = F(r['w']), F(r['p'])
        SP, mx = sealed_chamber(r, side)
        xA = 0 if side == 'left' else r['d1'] + L
        S = (xA + F(Srel[0]), F(Srel[1]))
        ev, T, con = trace(SP, S, (S[0] + hx * X, S[1] + vy * s0 * X))
        assert ev == 'end', ev
        # mouth contacts of the sealed reference: vertical contacts on the sealed mouth line inside (p,p+w)
        mouth, vsign, cur = [], [], vy
        for (c, k) in con:
            if k == 'v' and c[0] == mx and p < c[1] < p + w:
                mouth.append(c[1] - p)
                vsign.append(cur)
            if k == 'h':
                cur = -cur
        m = len(mouth)
        d = F(r['d2'] if side == 'left' else r['d1'])
        clear = all(0 < y - d * s0 and y + d * s0 < w for y in mouth)
        if L == Ls[0]:
            log(f"   sealed reference ends at T={fr(T)} after {len(con)} contacts; mouth heights y_i={[str(y) for y in mouth]}"
                f" (m={m}), vertical signs {vsign}; d={d}, d*s0={d * s0}; return hypothesis "
                f"[y_i-d s0, y_i+d s0] in (0,w): {clear}")
        k = round((L + d) * s0 / (2 * w))
        s = (X * s0 + 4 * m * k * w) / (X + 2 * m * (L + d))
        e = (L + d) * s - 2 * k * w
        bound = 2 * m * w / (X + 2 * m * (L + d))
        ident = (2 * m * e == -X * (s - s0))
        Xt = X + 2 * m * (L + d)
        Pfull = dumbbell(*ROOMS[name], L)['V']
        ev2, end2, con2 = trace(Pfull, S, (S[0] + hx * Xt, S[1] + vy * s * Xt))
        reached = ev2 == 'end' and end2 == T
        far = r['d1'] + L + r['d2'] if side == 'left' else 0
        farhits = [c for c, kk in con2 if kk == 'v' and c[0] == far]
        if side == 'left':
            inB = [c for c, kk in con2 if c[0] > r['d1'] + L]
            Bh = [c for c, kk in con2 if kk == 'h' and c[0] > r['d1'] + L]
        else:
            inB = [c for c, kk in con2 if c[0] < r['d1']]
            Bh = [c for c, kk in con2 if kk == 'h' and c[0] < r['d1']]
        ok = reached and ident and abs(s - s0) <= bound and len(farhits) == m and not Bh and len(inB) == m
        bounce = [str(fl(c[1] - p)) for c in farhits]
        if L in below:
            log(f"   BELOW-THRESHOLD (recorded, not a failure) L={L}: reaches T: {reached}; |err| <= x|s-s0|+2m|e| "
                f"at the gate x=43 is {fl(43 * abs(s - s0), 4)} vs its lip margin 1/20")
            continue
        (check if clear else (lambda ok_, msg: log('  RECORD ' + msg)))(ok,
              f"L={L}: k={k}, s={s} (|s-s0|={fl(abs(s - s0), 8)} <= bound {fl(bound, 8)}: {abs(s - s0) <= bound}), "
              f"2me=-X(s-s0): {ident}; exact trace: {ev2}, reaches T: {reached}; "
              f"{len(con2)} contacts, far-wall bounces {len(farhits)} at rel. heights {bounce}, "
              f"B horizontal-wall contacts {len(Bh)}")
        if not clear:
            log(f"   (hypothesis fails; recorded only) far-wall bounces {len(farhits)}, B horizontal contacts {len(Bh)},"
                f" ends {ev2} at {fr(tuple(fl(c, 4) for c in end2))}")
        if clear and m and L == Ls[-1]:
            # predicted entrance/exit heights at B's mouth for the first excursion
            log(f"   predicted first-visit entrance/bounce/exit heights -> {fl(mouth[0] - vsign[0] * d * s0, 4)}, "
                f"{fl(mouth[0], 4)}, {fl(mouth[0] + vsign[0] * d * s0, 4)}; observed bounce {bounce[0]}")
        if clear and L == Ls[1]:
            ev3, end3, _ = trace(Pfull, S, (S[0] + hx * Xt, S[1] + vy * s0 * Xt))
            log(f"   control at L={L} keeping slope s0: {ev3} at {fr(tuple(fl(c, 4) for c in end3))}, "
                f"reaches T: {ev3 == 'end' and end3 == T}")


Ls = [30, 101, F(2003, 3), 5000]
remote('DBas', 'left', (1, F(6, 5)), 1, 1, F(1, 20), 6, Ls, "3a m=1")
remote('DBas', 'left', (1, F(13, 10)), 1, 1, F(1, 50), 17, Ls, "3b m=2 (mouth, left wall, mouth)")
remote('DBas', 'right', (2, F(3, 2)), -1, -1, F(1, 30), 7, Ls, "3c m=1, A = right chamber, B depth 5")
remote('DB55', 'left', (1, F(13, 5)), 1, -1, F(1, 25), 7, Ls, "3d m=1, downward vertical sign")
remote('DB55', 'left', (2, F(1, 5)), 1, -1, F(1, 20), 56, Ls, "3e m=1 after a floor reflection and 10 wall contacts",
       below=(30, 101))
# explicit sufficient length for 3e. In A the developed error is (s-s0)(x - jX/m), so |err_A| <= X|s-s0|
# <= 2mXw/N with N = X+2m(L+d). In B add |e| + d|s-s0| <= (X+2md)w/N. Margins: the sealed wall contact at
# height 39/20 lies 1/20 below the mouth lip (smallest A margin); the B clearance margin is 9/20-1/4 = 1/5.
mu_A, mu_B, X3e, m3e, d3e = F(1, 20), F(1, 5), 56, 1, 5
NA = 2 * m3e * X3e / mu_A
NB = (2 * m3e * X3e + X3e + 2 * m3e * d3e) / mu_B
Lstar = (max(NA, NB) - X3e) / (2 * m3e) - d3e
log(f"   3e: explicit sufficient length L > {Lstar} (N > max({NA}, {NB})); L=2003/3 already works, so the bound is conservative")
remote('DBas', 'left', (2, F(1, 2)), 1, 1, F(1, 4), 5, [30, 101, 5000], "3f steep control, hypothesis fails")

# ================================================================== 4. obstruction arithmetic
log("\n# 4. Obstruction families")
for b in (7, 9, 11, 101):
    area = 2 * (2 * b) * 4 - 16
    check(area == 16 * b - 16, f"odd cross b={b}: area {area} = 16b-16; arm width 4; wall lengths 4 and b-2, gcd "
          f"{__import__('math').gcd(4, b - 2)}")
for H in (5, 7, 9, 101):
    hl = [5, 3, 5]  # chamber floors/tops and corridor
    vl = [H, 2, H - 3]
    from math import gcd
    D2 = 25 + H * H
    check(gcd(gcd(5, 3), 5) == 1 and gcd(gcd(H, 2), H - 3) == 1,
          f"DB55 top-line stretch H={H}: 12 walls, horizontal lengths {{5,3}}, vertical {{{H},2,{H-3}}}, "
          f"gcds 1; chamber D^2 = {D2}; d112 needs L > 4*5 = 20 but L = 3")

log(f"\nCPU {time.process_time() - T0:.1f} s; failures: {len(FAIL)}")
for f_ in FAIL:
    log("  FAILED:", f_)
