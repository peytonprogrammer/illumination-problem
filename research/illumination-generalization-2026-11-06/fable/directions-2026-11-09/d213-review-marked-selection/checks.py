"""D213 referee checks: marked band selection (note-snapshot.md).

Reuses the d212 exact integer-scaled tracer, seed_data, signed gate and re-aim
(imported from ../d212-review-descent-skeleton/checks.py). Named rooms only:
  TIERS : left-aligned tiers widths 4,5,6 on y [0,2],[2,3],[3,5]; S=(1,1), T=(3,4).
  TWO   : two rows width 4, two rows width 5, left aligned; S=(1,1), T=(2,3).
  STAIR : offset staircase x[0,3],[1,4],[3,6],[4,7], heights 2,1+x,1+y,2;
          S=(2,1), T=(5, roof-1). Sqrt2 family: gains t (lower), floor(sqrt2 t) (upper).
No room enumeration and no direction search: every traced ray is a template seed,
a re-aim of it at an explicit winding, or the direct chord.
Run: nice -n 10 python3 -B checks.py
"""
import importlib.util
import os
import time
from fractions import Fraction as F
from math import gcd, floor, ceil, isqrt

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    "d212checks", os.path.join(HERE, "..", "d212-review-descent-skeleton", "checks.py"))
K = importlib.util.module_from_spec(spec)
spec.loader.exec_module(K)
rects, trace, reached, seed_data, gate, reaim = K.rects, K.trace, K.reached, K.seed_data, K.gate, K.reaim
insert_row, shiftm, vertex_counts, strictly_simple, wall_levels = (
    K.insert_row, K.shiftm, K.vertex_counts, K.strictly_simple, K.wall_levels)
trace_reaimed, e_of = K.trace_reaimed, K.e_of

T0 = time.process_time()
FAILS = []


def say(*a):
    print(*a, flush=True)


def check(cond, msg):
    say(("PASS " if cond else "FAIL ") + msg)
    if not cond:
        FAILS.append(msg)


class Seed:
    """A legal seed in a room: cells, S, T, primitive direction d, steps."""
    def __init__(self, c, S, T, d, steps):
        self.c, self.S, self.T, self.d, self.steps = c, S, T, d, steps
        assert reached(trace(c, S, d, steps), T)


def stage(sd0, J, E, N, do_trace=True):
    """One parallel lift of unit row J by E with winding N. Returns dict."""
    sd = seed_data(sd0.c, sd0.S, sd0.T, sd0.d, sd0.steps, J)
    s, dl = reaim(sd, E, N, sd['Q'])
    out = dict(sd=sd, s=s, dl=dl, pos=s > 0)
    if s <= 0:
        out.update(g=False, ok=False)
        return out
    out['g'] = gate(sd, dl)
    D, m, Q = sd['D'], sd['m'], sd['Q']
    U = sd['s0'] * D
    R = 2 * Q * N * D - E * U
    Dp = D + m * E
    out.update(U=U, D=D, m=m, Q=Q, R=R, Dp=Dp, test1=m * D * abs(R) < Dp * gcd(int(U), D))
    if do_trace:
        ch = insert_row(sd0.c, J, E)
        S2, T2 = shiftm(sd0.S, J, E), shiftm(sd0.T, J, E)
        r = trace_reaimed(ch, S2, sd, s, E)
        out['ok'] = reached(r, T2)
        p, q = sd['d']
        d2 = (s.numerator if p > 0 else -s.numerator, s.denominator if q > 0 else -s.denominator)
        out['next'] = Seed(ch, S2, T2, d2, Dp // s.denominator) if out['ok'] else None
        out['room'] = (ch, S2, T2)
    return out


# ------------------------------------------------------------------ claim 1
def claim1():
    say("\n=== Claim 1: template bound")
    check(all(r + 3 <= 11 for r in range(9)) and 11 * 11 == 121,
          "r<=8: <= r+4 cut levels, <= 11 refined gaps per axis; all-unit template box <= 11x11 = 121")
    # staircase all-unit template: x cut levels 0..7 all unit; y gaps 1,1,1,1,1,1
    c = stair_room(0, 0)
    check(len(c) == 18 and wall_levels(c, 0) == [0, 1, 3, 4, 6, 7],
          "offset staircase: compressing both middle bands gives area 18; x walls 0,1,3,4,6,7 + marks 2,5")


# ------------------------------------------------------------------ claim 2
def claim2(stages):
    say("\n=== Claim 2: e(t) = [mt - D b(t)] R/(D D'), test (1) sufficiency")
    bad = n = 0; t1 = t1g = 0
    for st in stages:
        sd = st['sd']
        if not st['pos']: continue
        for t in range(sd['D'] + 1):
            n += 1
            lhs = e_of(sd, t, st['dl'])
            rhs = F((st['m'] * t - st['D'] * sd['b'][t]) * st['R'], st['D'] * st['Dp'])
            bad += lhs != rhs
        if st['test1']:
            t1 += 1; t1g += st['g']
    check(bad == 0, f"e(t) identity on {n} (stage, level) pairs from the named-room stages")
    check(t1 == t1g, f"test (1) passing implies the signed gate in all {t1} stages where (1) holds")
    # U=1: two-tier N=0 twice, several height pairs (named room only)
    allok = True; k = 0
    for E1, E2 in ((1, 1), (5, 37), (40, 3), (90, 170), (170, 90)):
        s0 = Seed(two_tier(), (1, 1), (2, 3), (1, 2), 1)
        a = stage(s0, 1, E1, 0)
        b = stage(a['next'], 2 + E1, E2, 0)
        k += 1; allok &= a['g'] and a['ok'] and b['g'] and b['ok']
    check(allok, f"U=1 two-tier seed: N=0 on both lifts passes gate and is legal for {k} height pairs")


# ------------------------------------------------------------------ claim 3: tiers 4,5,6
def tiers():
    return rects((0, 4, 0, 2), (0, 5, 2, 3), (0, 6, 3, 5))


def claim3():
    say("\n=== Claim 3: tiers 4,5,6, S=(1,1), T=(3,4); lift [2,3] by E0 (N0=0), then [3,4] by 6T+1 (N=1)")
    c = tiers()
    rx, cv, pin = vertex_counts(c)
    check(strictly_simple(c) and rx == 2 and wall_levels(c, 1) == [0, 2, 3, 5],
          "tiers room strictly simple, r=2, y walls 0,2,3,5 (marks 1,4 => all y gaps unit)")
    base = Seed(c, (1, 1), (3, 4), (2, 3), 1)
    allok = True; Rs = set(); stg = []
    for E0 in list(range(1, 31)) + [57, 100]:
        T = 3 + E0
        a = stage(base, 2, E0, 0)
        b = stage(a['next'], 3 + E0, 6 * T + 1, 1)
        Rs.add(b['R'])
        sd = a['sd']
        off_ok = (a['s'] == F(2, T))
        t2 = (2 * T < 7 * T + 1)
        allok &= a['g'] and a['ok'] and b['g'] and b['ok'] and off_ok and t2 and b['test1']
        stg += [a, b]
    check(allok and Rs == {-2},
          "for E0=1..30,57,100: first lift gate+legal with slope 2/T; second lift R=-2, test (2) 2T<7T+1, "
          "test (1), gate, and exact trace legal")
    # threshold formula with A=1,B=0,m=1,c=6,b=1,U=2: (mB|R|-B')/(A'-mA|R|) = -1/5 < 0 -> all T
    A, B, m, cc, bb, U = 1, 0, 1, 6, 1, 2
    R = U * (cc * B - bb * A); Ap, Bp = A + m * cc, B + m * bb
    check(R == -2 and m * A * abs(R) < Ap and F(m * B * abs(R) - Bp, Ap - m * A * abs(R)) < 0,
          "determinant formula R=U(cB-bA)=-2 and threshold negative: every T admissible")
    # symbolic identity R_j = U(c_j B - b_j A) on a grid
    bad = 0; n = 0
    for U in (1, 2, 3, 5):
        for A in (1, 2, F(7, 3)):
            for B in (-3, 0, 4):
                for c_ in (F(1, 2), 2, 6):
                    for b_ in (-2, 0, 1, 5):
                        for T in (10, 33):
                            Dc, Uc = A * T + B, U * A
                            E = c_ * T + b_
                            R1 = c_ * U * Dc - E * Uc   # 2QN = cU
                            n += 1; bad += R1 != U * (c_ * B - b_ * A)
    check(bad == 0, f"R_j = U(c_j B - b_j A) identity on {n} grid cases")
    return stg


# ------------------------------------------------------------------ claim 4: two-tier
def two_tier():
    return rects((0, 4, 0, 2), (0, 5, 2, 4))


def claim4():
    say("\n=== Claim 4: two-tier widths 4,5, S=(1,1), T=(2,3); gains 80n, 80n+10")
    stg = []
    for n in (1, 2, 3):
        base = Seed(two_tier(), (1, 1), (2, 3), (1, 2), 1)
        a = stage(base, 1, 80 * n, 5 * n)
        check(a['dl'] == 0 and a['g'] and a['ok'] and a['next'] is not None,
              f"n={n}: exact replay through lower band (N=5n) legal, U={a['U']+80*n*0}")
        sd1 = seed_data(a['next'].c, a['next'].S, a['next'].T, a['next'].d, a['next'].steps, 2 + 80 * n)
        Uc = sd1['s0'] * sd1['D']
        tI = sd1['sel'][0] - 1
        check(Uc == 1 + 40 * n and sd1['D'] == 2 + 80 * n and tI == 1 + 80 * n
              and (sd1['s0'] * tI).denominator == 2 and sd1['Q'] == 5 and sd1['m'] == 1,
              f"n={n}: replayed parent U={Uc}, D={sd1['D']}, interface t={tI} half-integral, Q=5, m=1")
        Ns = range(-(40 * n) // 10 - 2, (2 * (40 * n + 5)) // 10 + 6)
        gp = leg = tested = 0; mind = None
        for N in Ns:
            b = stage(a['next'], 2 + 80 * n, 80 * n + 10, N)
            if not b['pos']: continue
            tested += 1; gp += b['g']; leg += b['ok']
            d = abs(b['dl']); mind = d if mind is None else min(mind, d)
            stg.append(b)
        check(gp == 0 and mind >= F(5, 12 + 160 * n) and mind * (1 + 80 * n) > F(1, 2),
              f"n={n}: {tested} windings with s'>0: none passes the gate; min|delta|={mind} >= 5/(12+160n); "
              f"|t delta| at interface > 1/2")
        say(f"    n={n}: of those {tested} re-aimed replayed seeds, {leg} are legal by exact trace")
        a0 = stage(base, 1, 80 * n, 0)
        b0 = stage(a0['next'], 2 + 80 * n, 80 * n + 10, 0)
        check(a0['g'] and a0['ok'] and b0['g'] and b0['ok'],
              f"n={n}: N=0 on both lifts passes the gate and is legal (direct chord)")
        stg += [a, a0, b0]
    return stg


# ------------------------------------------------------------------ claim 5
def claim5(pairs):
    say("\n=== Claim 5: ratio condition |1/s' - 1/s| <= 2 on gate-passing last stages")
    viol = 0
    for s, sp in pairs:
        viol += abs(1 / sp - 1 / s) > 2
    check(viol == 0, f"all {len(pairs)} gate-passing staircase last stages satisfy (3)")
    # sqrt2 obstruction algebra: leading coefficients m1/U1 vs (m1+m2 sqrt2)/U2 -- exact: no rational fix
    say("  (3) obstruction: sqrt2*U1 = 2*Q2*m1*N2 has no solution with U1>0 integral (sqrt2 irrational)")


# ------------------------------------------------------------------ claim 6: offset staircase
def stair_room(x_lower, y_upper):
    """Heights 2, 1+x_lower, 1+y_upper, 2."""
    h = [2, 1 + x_lower, 1 + y_upper, 2]
    ys = [0, h[0], h[0] + h[1], h[0] + h[1] + h[2], sum(h)]
    xs = [(0, 3), (1, 4), (3, 6), (4, 7)]
    return rects(*[(xs[i][0], xs[i][1], ys[i], ys[i + 1]) for i in range(4)])


def stair_template_seed():
    return Seed(stair_room(0, 0), (2, 1), (5, 5), (3, 4), 1)


def lu(s, H):
    l = max(F(ceil(j * s) - 1, j) for j in range(1, H + 1))
    u = min(F(floor(j * s) + 1, j) for j in range(1, H + 1))
    return l, u


def interval_Ns(x, y, n):
    """Note's last-gate criterion: windings N with 3+6n+6N in ((D+y)l,(D+y)u)."""
    D = 4 + x; s = F(3 + 6 * n, D); H = x + 2
    l, u = lu(s, H)
    lo, hi = (D + y) * l, (D + y) * u
    k = floor(lo) + 1
    k += (3 - k) % 6
    out = []
    while k < hi:
        out.append((k - 3 - 6 * n) // 6); k += 6
    return out


def first_ns(x):
    D = 4 + x
    return [n for n in range(0, D) if F(1, 2) < F(3 + 6 * n, D) < 1]


def run_order(order, t_low, t_up, n, N, do_trace=True):
    """order 'L': lower band (gain t_low) first. 'U': upper band first."""
    base = stair_template_seed()
    if order == 'L':
        a = stage(base, 2, t_low, n, do_trace)
        if not do_trace: return a, None
        b = stage(a['next'], 3 + t_low, t_up, N, do_trace) if a['ok'] else None
    else:
        a = stage(base, 3, t_up, n, do_trace)
        if not do_trace: return a, None
        b = stage(a['next'], 2, t_low, N, do_trace) if a['ok'] else None
    return a, b


def claim6():
    say("\n=== Claim 6: offset four-tier staircase")
    f = lambda t: isqrt(2 * t * t)
    ok = True
    for t in (1, 2, 5, 17, 100, 200):
        c = stair_room(t, f(t))
        rx, cv, pin = vertex_counts(c)
        ok &= strictly_simple(c) and rx == 6 and wall_levels(c, 0) == [0, 1, 3, 4, 6, 7]
    check(ok, "staircase t in {1,2,5,17,100,200}: strictly simple, 6 reflex, x walls 0,1,3,4,6,7")

    # first stage: (1/2,1) is exactly the gate set, both orders, and traced legal
    base = stair_template_seed()
    sdL = seed_data(base.c, base.S, base.T, base.d, base.steps, 2)
    sdU = seed_data(base.c, base.S, base.T, base.d, base.steps, 3)
    okf = True; cnt = 0
    for x in (1, 5, 17, 40, 100):
        D = 4 + x
        for k in range(1, 2 * D):
            s = F(k, D)
            for sd in (sdL, sdU):
                g = gate(sd, s - F(3, 4))
                okf &= g == (F(1, 2) < s < 1)
        for n in first_ns(x):
            for order in 'LU':
                a, _ = run_order(order, x if order == 'L' else 1, 1 if order == 'L' else x, n, 0, True)
                cnt += 1; okf &= a['g'] and a['ok']
    check(okf, f"first-stage gate set equals (1/2,1) on both orders; {cnt} first lifts s=(3+6n)/D traced legal")
    # bounded winding fails for large first gain (fixed template seed)
    okb = all(not (F(1, 2) < F(3 + 6 * n, 4 + x) < 1) for n in range(-3, 6) for x in range(2 * (3 + 30), 2 * 33 + 5))
    check(okb, "fixed template seed, n in -3..5: no first-lift slope passes for x=66..70 (and beyond: slope decreases in x)")

    # direct chord
    leg = []
    for t in range(1, 201):
        c = stair_room(t, f(t))
        P, Qd = 3, 4 + t + f(t)
        g = gcd(P, Qd)
        leg.append(reached(trace(c, (2, 1), (P // g, Qd // g), g), (5, 5 + t + f(t))))
    bad = [t for t in range(1, 201) if not leg[t - 1]]
    check(all(leg[t - 1] for t in range(max(bad, default=0) + 1, 201)),
          f"direct chord legal for t=1..200 except t in {bad}")

    # criterion equivalence with the generic signed gate (and traces) on a few t
    eq = True; leg_fail = 0; ntest = 0; pairs = []; parity_bad = 0; trlog = []
    for t in range(1, 81):
        y = f(t)
        for order in 'LU':
            x, yy = (t, y) if order == 'L' else (y, t)
            for n in first_ns(x):
                a, _ = run_order(order, t, y, n, 0, True)
                D = 4 + x
                Ncrit = set(interval_Ns(x, yy, n))
                Nrange = range(-(3 + 6 * n) // 6 - 1, (D + yy) // 6 + 2)
                sdn = a['next']
                J = 3 + t if order == 'L' else 2
                sd = seed_data(sdn.c, sdn.S, sdn.T, sdn.d, sdn.steps, J)
                Ngate = set()
                for N in Nrange:
                    s2, dl = reaim(sd, yy, N, sd['Q'])
                    if s2 > 0 and gate(sd, dl): Ngate.add(N)
                eq &= Ngate == Ncrit
                for N in sorted(Ngate):
                    b = stage(sdn, J, yy, N)
                    ntest += 1; leg_fail += not b['ok']
                    pairs.append((a['s'], b['s']))
                    if t % 2 == 1 and y % 2 == 1:
                        parity_bad += b['next'].d[0] % 2 == 0
    check(eq, "for t=1..80, both orders, every first-stage n: the generic signed gate's passing "
              "windings equal the note's interval set exactly")
    check(leg_fail == 0, f"all {ntest} gate-passing last lifts are legal by exact trace")

    # sweep t=1..200: interval criterion, both orders
    say("  sweep t=1..200 (arithmetic only): interval test, exact-replay gcd test, mod-42 class")
    passL, passU, anyp, replay_any = [], [], [], []
    gcd_bad = 0
    for t in range(1, 201):
        y = f(t)
        res = {}
        for order in 'LU':
            x, yy = (t, y) if order == 'L' else (y, t)
            hits = [(n, interval_Ns(x, yy, n)) for n in first_ns(x)]
            res[order] = [(n, Ns) for n, Ns in hits if Ns]
            # exact replay brute vs gcd criterion
            D = 4 + x
            brute = any((yy * F(3 + 6 * n, D)) % 6 == 0 for n in first_ns(x))
            g = gcd(D, yy)
            crit = (D // g) % 2 == 1 and (yy // g) % 2 == 0 and any(z % 2 == 1 for z in range(g // 6, g // 3 + 2)
                                                                     if F(g, 6) < z < F(g, 3))
            gcd_bad += brute != crit
            if brute: replay_any.append((t, order))
        if res['L']: passL.append(t)
        if res['U']: passU.append(t)
        if res['L'] or res['U']: anyp.append(t)
    fail = [t for t in range(1, 201) if t not in anyp]
    check(gcd_bad == 0, "exact-replay gcd criterion equals brute force over n,N for t=1..200, both orders")
    say(f"    interval test passes (some n) lower-first: {len(passL)}/200, upper-first: {len(passU)}/200, "
        f"either: {len(anyp)}/200")
    say(f"    t<=200 where it fails in BOTH orders ({len(fail)}): {fail}")
    say(f"    t<=200 with exact replay available (t,order): {len(replay_any)} -> "
        f"{sorted(set(t for t, _ in replay_any))[:40]}")
    rep_t = set(t for t, _ in replay_any)
    say(f"    t<=200 passing only by non-replay windings: {len([t for t in anyp if t not in rep_t])}")
    both_odd_fail = [t for t in fail if t % 2 == 1 and f(t) % 2 == 1]
    say(f"    of the failing t, both gains odd: {both_odd_fail}")

    big = [t for t in fail if 18 + 3 * (t + f(t)) > 121]
    say(f"    first failing t with area 18+3(t+f) > 121: t={big[0]}, f={f(big[0])}, area {18 + 3 * (big[0] + f(big[0]))}")
    for order in 'LU':
        x, yy = (big[0], f(big[0])) if order == 'L' else (f(big[0]), big[0])
        for n in first_ns(x):
            s1 = F(3 + 6 * n, 4 + x); l, u = lu(s1, x + 2)
            say(f"      order {order}: n={n}, s={s1}, (l,u)=({l},{u}), window for 3+6n+6N: "
                f"({float((4 + x + yy) * l):.3f}, {float((4 + x + yy) * u):.3f}) -> {interval_Ns(x, yy, n)}")
    # calibration: at three failing t, trace the nearest winding (and neighbours) for every first-stage n
    for t in (5, 17, 100):
        y = f(t); tot = leg = 0
        for order in 'LU':
            x, yy = (t, y) if order == 'L' else (y, t)
            for n in first_ns(x):
                a, _ = run_order(order, t, y, n, 0, True)
                J = 3 + t if order == 'L' else 2
                N0 = round(F(yy * (3 + 6 * n), 6 * (4 + x)))
                for N in (N0 - 1, N0, N0 + 1):
                    b = stage(a['next'], J, yy, N)
                    if not b['pos']: continue
                    tot += 1; leg += b['ok']
        say(f"    t={t} (fails interval test): nearest-winding re-aims traced {tot}, legal {leg}")
    # mod-42 class
    say("  mod-42 non-replay selection theorem")
    bad42 = 0; n42 = 0
    for x in range(17, 17 + 42 * 30, 42):
        for y in list(range(17, 17 + 42 * 6, 42)) + list(range(25, 25 + 42 * 6, 42)):
            D = 4 + x; s = F(5, 7); n = (D * s - 3) / 6
            l, u = lu(s, x + 2)
            Ns = interval_Ns(x, y, int(n))
            N = round((y * s) / 6)
            n42 += 1
            bad42 += not (n.denominator == 1 and abs(6 * N - y * s) == F(1, 7) and N in Ns and F(1, 2) < s < 1)
    check(bad42 == 0, f"{n42} arithmetic (x,y) in class: n integral, |6N - ys| = 1/7, N passes the interval test")
    trok = True; members = []
    for (tl, tu, order) in ((17, 17, 'L'), (17, 25, 'L'), (67, 59, 'U'), (101, 59, 'L')):
        x = tl if order == 'L' else tu; yy = tu if order == 'L' else tl
        n = (4 + x) * 5 // 7 // 6
        N = round(F(5 * yy, 7) / 6)
        a, b = run_order(order, tl, tu, n, N)
        sp = b['s']
        trok &= a['s'] == F(5, 7) and a['g'] and a['ok'] and b['g'] and b['ok'] and \
            abs(sp - F(5, 7)) == F(1, 7 * (4 + x + yy)) and b['next'].d[0] % 2 == 1
        members.append((tl, tu, order, sp))
    check(trok, f"traced class members (lower,upper,order,s'): {members}: gate + legal, |s'-5/7|=1/(7(D+y)), odd p")
    cls = [t for t in range(1, 3000) if t % 42 == 17 and f(t) % 42 in (17, 25)]
    say(f"    sqrt2 members t<3000 (t=17, f=+-17 mod 42): {cls}")
    trok = True
    for t in cls[:2]:
        y = f(t); n = (4 + t) * 5 // 7 // 6; N = round(F(5 * y, 7) / 6)
        a, b = run_order('L', t, y, n, N)
        trok &= a['g'] and a['ok'] and b['g'] and b['ok'] and b['next'].d[0] % 2 == 1
        say(f"    t={t}, f={y}: s=5/7 (n={n}), N={N}, s'={b['s']}, gate {b['g']}, legal {b['ok']}")
    check(trok, f"sqrt2 members t={cls[:2]} traced: gate passes and exact trace reaches T")
    k17 = [k for k in range(2000) if f(42 * k + 17) % 42 == 17]
    say(f"    density check: {len(k17)} of k<2000 have f(42k+17) = 17 mod 42 (window length 1/42 -> ~{2000/42:.0f})")
    check(parity_bad == 0, "parity: legal last-stage seeds in odd/odd sqrt2 rooms have odd primitive x-component")
    return pairs, fail


if __name__ == '__main__':
    claim1()
    s3 = claim3()
    s4 = claim4()
    claim2(s3 + s4)
    pairs, fail = claim6()
    claim5(pairs)
    say(f"\nTOTAL FAIL {len(FAILS)}; cpu {time.process_time()-T0:.1f}s")
