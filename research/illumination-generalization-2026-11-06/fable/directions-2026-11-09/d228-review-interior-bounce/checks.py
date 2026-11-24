"""D228 independent review of l1-interior-bounce (note-snapshot.md).

Reuses the exact Fraction tracer, R22 and the six-reflex room builder from ../d227-review-pinned-pairs/checks.py.
Named rooms only (R22, six-reflex family). Every traced direction is hand-chosen and listed; no sweeps.
Claim 4 brute force is a combinatorial self-test on random abstract instances (no rooms).
Run: nice -n 10 python3 -B checks.py
"""
import os
import random
import sys
import time
from fractions import Fraction as F
from itertools import product

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'd227-review-pinned-pairs'))
import checks as d227  # noqa: E402  (main guarded by __name__)

trace, six, R22, inside, fmt = d227.trace, d227.six, d227.R22, d227.inside, d227.fmt

T0 = time.process_time()
FAILS = []


def say(*a):
    print(*a, flush=True)


def check(cond, msg):
    say(("PASS " if cond else "FAIL ") + msg)
    if not cond:
        FAILS.append(msg)


# ------------------------------------------------------------------ slab geometry
def comps(P, y, sgn):
    """open x-components of the slab just above (sgn=+1) or below (-1) level y."""
    xs = sorted({v[0] for v in P})
    ys = sorted({v[1] for v in P})
    nb = [v for v in ys if (v > y if sgn > 0 else v < y)]
    yy = (y + min(nb)) / 2 if sgn > 0 else (y + max(nb)) / 2
    ivs = []
    for a, b in zip(xs, xs[1:]):
        if inside(P, ((a + b) / 2, yy)):
            if ivs and ivs[-1][1] == a:
                ivs[-1] = (ivs[-1][0], b)
            else:
                ivs.append((a, b))
    return ivs


def overlaps(A, B):
    return [(max(a, c), min(b, d)) for a, b in A for c, d in B if max(a, c) < min(b, d)]


def exposed(comp, other):
    """relative-interior pieces of comp not covered by the closure of any interval in other."""
    pieces = [comp]
    for c, d in other:
        nxt = []
        for a, b in pieces:
            if c >= b or d <= a:
                nxt.append((a, b))
                continue
            if a < c:
                nxt.append((a, c))
            if d < b:
                nxt.append((d, b))
        pieces = nxt
    return pieces


def visit_interval(P, y, kind, prev_comp, X):
    """Interval of the note's chain test that contains X, for a visit at level y.
    kind: 'up' / 'dn' transmission, 'roof' / 'floor' turn. prev_comp = component of the incoming leg.
    Returns (interval, next_comp) or (None, None) if X lies in no open admissible interval."""
    if kind in ('up', 'roof'):
        here, there = comps(P, y, -1), comps(P, y, +1)
    else:
        here, there = comps(P, y, +1), comps(P, y, -1)
    inc = [c for c in here if c[0] < X < c[1]]
    if prev_comp is not None:
        inc = [c for c in inc if c == prev_comp]
    if not inc:
        return None, None
    c = inc[0]
    if kind in ('up', 'dn'):
        for iv in overlaps([c], there):
            if iv[0] < X < iv[1]:
                return iv, [d for d in there if d[0] <= iv[0] and iv[1] <= d[1]][0]
        return None, None
    for iv in exposed(c, there):
        if iv[0] < X < iv[1]:
            return iv, c
    return None, None


def chain_test(P, S, K, plan):
    """Note's interval-chain test along a planned vertical itinerary with no vertical-wall hits.
    plan: list of (level, kind, s); last entry is the target (s=H). Returns (ok, min clearance, rows)."""
    H = plan[-1][2]
    X0 = S[0]
    comp = [c for c in comps(P, S[1], +1 if plan[0][1] in ('up', 'roof') else -1) if c[0] < X0 < c[1]][0]
    rows, clear = [], None
    for y, kind, s in plan[:-1]:
        X = X0 + K * s / H
        # strict-clearance value from the note: min{K s - H(l - X0), H(u - X0) - K s} / H
        iv, nxt = visit_interval(P, y, kind, comp, X)
        if iv is None:
            # report the zero/negative clearance against the nearest boundary of the incoming component
            rows.append((y, kind, s, X, None))
            return False, F(0) if any(X == v[0] for v in P if v[1] == y) else None, rows
        cl = min(K * s - H * (iv[0] - X0), H * (iv[1] - X0) - K * s) / H
        clear = cl if clear is None else min(clear, cl)
        rows.append((y, kind, s, X, iv))
        comp = nxt
    ok = comp[0] < X0 + K < comp[1]
    return ok and clear > 0, clear, rows


def excursion_plan(levels, k_at, start=F(0)):
    """Upward passage through interfaces `levels` (ascending, last = target level), with k_at[j] roof-floor
    excursions in the slab between levels[j-1] and levels[j] (j>=1). Returns the plan with accumulated s."""
    plan, s, prev = [], F(0), start
    for j, y in enumerate(levels):
        L = y - prev
        for _ in range(k_at.get(j, 0)):
            s += L; plan.append((y, 'roof', s))
            s += L; plan.append((prev, 'floor', s))
        s += L
        plan.append((y, 'up' if j < len(levels) - 1 else 'T', s))
        prev = y
    return plan


# ------------------------------------------------------------------ claim 1
def claim1():
    say("\n=== Claim 1: q = s - H alpha, one- and two-reflection formulas")
    ok = True
    for D in (F(3), F(4), F(7)):
        for K in (F(2), F(5)):
            for y in (D / 5, D / 2, 4 * D / 5):
                al = y / D
                # generic identity: developed X - unbounced X = (K/H)(s - H alpha)
                for H, s in ((D + 3, y + 1), (2 * D, y)):
                    ok &= (K * s / H - K * al) == (K / H) * (s - H * al)
                # one reflection, upward start, U > D
                U = D + F(3, 2)
                H = 2 * U - D
                ok &= y - H * al == -2 * (U - D) * al
                # one reflection, downward start, V < 0
                V = -F(5, 4)
                H = D - 2 * V
                ok &= (y - 2 * V) - H * al == (-2 * V) * (1 - al)
                # two reflections, up-down-up (U > 0, V < D, V < U); include U < D and U > D
                for U, V in ((D * F(2, 3), D / 7), (D + 1, D / 3), (D + 2, -F(1, 2))):
                    L = U - V
                    H = U + (U - V) + (D - V)
                    ok &= H == D + 2 * L
                    ok &= y - H * al == -2 * L * al
                    ok &= (2 * U - y) - H * al == 2 * (U - (D + L) * al)
                    ok &= (y + 2 * L) - H * al == 2 * L * (1 - al)
                    ok &= (U - (D + L) * al == 0) == (al == U / (D + L))
                # two reversals starting downward: V < 0, U > D
                V, U = -F(2, 3), D + F(5, 4)
                H = -V + (U - V) + (U - D)
                ok &= H == 2 * (U - V) - D
                ok &= (y - 2 * V) - H * al == -2 * V - (H - D) * al and H - D > 0
    check(ok, "q identity, one-reflection q=-2(U-D)alpha and (-2V)(1-alpha), two-reflection table and the "
              "down-up variant (3 D x 2 K x 3 heights x 3 (U,V) pairs, exact)")
    # traversal-order sign sequence for the up-down-up table on a concrete instance
    D, U, V = F(4), F(3), F(1)
    L = U - V
    seq = []
    for y in (F(1, 2), F(2), F(5, 2)):
        seq.append(('asc1', -2 * L * y / D))
    for y in (F(5, 2), F(2), F(3, 2)):
        seq.append(('desc', 2 * (U - (D + L) * y / D)))
    for y in (F(3, 2), F(3)):
        seq.append(('asc2', 2 * L * (1 - y / D)))
    sg = [(x > 0) - (x < 0) for _, x in seq]
    check(sg == [-1, -1, -1, -1, 0, 1, 1, 1] and all(b >= a for a, b in zip(sg, sg[1:])),
          f"U=3,V=1,D=4: signs in travel order {sg} (minus, one zero on the descent at alpha=U/(D+L)=1/2, plus)")
    # one interior reflection cannot be the only reversal: up then down never reaches D>U
    check(all(U < D for U in (F(1), F(2), F(3))),
          "a single turn at 0<U<D leaves the ray below U<D forever (no further vertical reversal), so the target "
          "level is never reached: trivial, recorded")


# ------------------------------------------------------------------ claims 2 and 3
def claim2_3():
    say("\n=== Claims 2-3: interval-chain test vs exact tracer; six-reflex closure table")
    S = (F(0), F(0))
    for m in (1, 2, 5):
        t = F(10 * m + 1)
        P = six(m)
        T = (4 * t, 4 * t)
        lv = [t, 3 * t, 4 * t]
        # note's table: one excursion in the middle tier
        plan = excursion_plan(lv, {1: 1})
        exp = [(t, 'up', t), (3 * t, 'roof', 3 * t), (t, 'floor', 5 * t), (3 * t, 'up', 7 * t), (4 * t, 'T', 8 * t)]
        ok, cl, rows = chain_test(P, S, 4 * t, plan)
        ivs = [r[4] for r in rows]
        check(plan == exp and ok and [r[3] for r in rows] == [t / 2, 3 * t / 2, 5 * t / 2, 7 * t / 2]
              and ivs == [(0, t), (0, 3 * t), (t, 4 * t), (3 * t, 4 * t)],
              f"m={m}, t={t}: table rows (s, x, interval) = "
              + "; ".join(f"({r[2]}, {r[3]}, {r[4]})" for r in rows) + f"; min clearance {cl} = t/2")
        top = comps(P, 4 * t, -1)
        check(top == [(3 * t, 6 * t)] and 3 * t < T[0] < 6 * t, f"m={m}: T in the upper-tier component {top}")
        st, _, path = trace(P, S, (1, 2), T)
        check(st == 'T' and path == [S, (3 * t / 2, 3 * t), (5 * t / 2, t), T],
              f"m={m}: tracer (1,2) reaches T with reflections exactly at the two middle-tier turns, "
              f"no vertical wall touched")
        check((rows[0][3] - t, rows[3][3] - 3 * t) == (-t / 2, t / 2),
              f"m={m}: shifts from x=y are -t/2 at y=t and +t/2 at y=3t")
    # iff test: theorem verdict vs tracer, on several planned chains (m=1)
    say("   -- chain theorem vs tracer, m=1, k middle-tier excursions, direction (1, k+1)")
    m, t = 1, F(11)
    P, T = six(1), (F(44), F(44))
    for k in (0, 1, 2, 3, 4, 5):
        plan = excursion_plan([t, 3 * t, 4 * t], {1: k})
        ok, cl, rows = chain_test(P, S, 4 * t, plan)
        st, info, path = trace(P, S, (1, k + 1), T, maxref=60)
        # planned reflection points (roof/floor) must equal tracer's reflection points when ok
        refl = [(r[3], r[0]) for r in rows if r[1] in ('roof', 'floor')]
        agree = (ok and st == 'T' and path[1:-1] == refl) or (not ok and not (st == 'T' and path[1:-1] == refl))
        check(agree, f"k={k}: theorem {'PASS' if ok else 'FAIL'} (min clearance {cl}); tracer {st} {fmt(info)}; "
                     f"{'same itinerary' if ok else 'planned chain not realized'}")
    # R22: direct winding, single excursion in slab 1<y<2 (claim 6 detail)
    say("   -- R22 single excursion chain")
    S, T = (F(0), F(0)), (F(2), F(2))
    plan = excursion_plan([F(1), F(2)], {1: 1})
    ok, cl, rows = chain_test(R22, S, F(2), plan)
    st, info, _ = trace(R22, S, (1, 2), T)
    check(not ok and cl == 0 and rows[0][3] == F(1, 2) and rows[1][3] == F(1) and st == 'corner'
          and info == (F(1), F(2)),
          f"R22: s=1 crossing at x={rows[0][3]} in {rows[0][4]}; roof turn at s=2, x={rows[1][3]}: "
          f"corner (1,2), clearance {cl}; tracer dies at {fmt(info)}")
    # also: in R22 at the visit x=1 the incoming component's roof faces are (0,1),(3,4), floor face (1,3)
    c12 = comps(R22, F(1), +1)
    check(c12 == [(0, 4)] and exposed((F(0), F(4)), comps(R22, F(2), +1)) == [(0, 1), (3, 4)]
          and exposed((F(0), F(4)), comps(R22, F(1), -1)) == [(1, 3)],
          "R22 slab 1<y<2: component (0,4), roof exposed (0,1),(3,4), floor exposed (1,3)")
    # turn face vs overlap: a planned roof turn over an opening is rejected even though X is interior to the slab
    iv, _ = visit_interval(R22, F(2), 'roof', (F(0), F(4)), F(2))
    iv2, _ = visit_interval(R22, F(2), 'up', (F(0), F(4)), F(2))
    check(iv is None and iv2 == (1, 3), "R22: x=2 at y=2 is an overlap (transmits), not a turn face")


# ------------------------------------------------------------------ claim 4 brute force
def rules(eps, J, p):
    if eps[0] > 0 and 0 not in J:
        return False
    if eps[-1] < 0 and p not in J:
        return False
    return all(not (eps[i] < 0 and eps[i + 1] > 0) or (i + 1) in J for i in range(p - 1))


def signs_ok(h, al, eps):
    """h[c] = total delay at cut c (c=0..p). q_i = sum_{c<i} h_c - alpha_i E for pin i=1..p."""
    E = sum(h)
    if E == 0:
        return False
    acc = 0
    for i in range(len(al)):
        acc += h[i]
        q = acc - al[i] * E
        if q == 0 or (q > 0) != (eps[i] > 0):
            return False
    return True


def construct(al, J, eps, lam):
    """The note's sufficiency construction; returns integer counts (dict cut->count) or None."""
    p = len(al)
    cuts_int = [c for c in range(1, p) if c in J]
    bounds = [0] + cuts_int + [p]
    runs = [list(range(a, b)) for a, b in zip(bounds, bounds[1:])]  # pin indices 0-based
    G = []
    gaps = sorted(set([F(0), F(1)] + list(al)))
    eta = min(b - a for a, b in zip(gaps, gaps[1:])) / 4
    for r in runs:
        plus = [al[i] for i in r if eps[i] > 0]
        minus = [al[i] for i in r if eps[i] < 0]
        if plus and minus:
            g = (max(plus) + min(minus)) / 2
        elif minus:
            g = min(minus) - eta
        else:
            g = max(plus) + eta
        G.append(g)
    if 0 not in J:
        G[0] = F(0)
    if p not in J:
        G[-1] = F(1)
    if any(b <= a for a, b in zip(G, G[1:])) or not all(0 <= g <= 1 for g in G):
        return None
    w = {}
    if 0 in J:
        w[0] = G[0]
    for k, c in enumerate(cuts_int):
        w[c] = G[k + 1] - G[k]
    if p in J:
        w[p] = 1 - G[-1]
    if any(v < 0 for v in w.values()) or sum(w.values()) != 1:
        return None
    M = 1
    while M <= 2 ** 40:
        h = [0] * (p + 1)
        cnt = {}
        for c, v in w.items():
            cnt[c] = int(M * v // lam[c][0])
            h[c] = cnt[c] * lam[c][0]
        if signs_ok(h, al, eps):
            return cnt
        M *= 2
    return None


def claim4():
    say("\n=== Claim 4: three-cut sign-cone theorem, brute force on random abstract instances")
    # shift formula on the six-reflex (1,3) route: two excursions at cut 1, quantum 4t each, pins 1/4, 3/4
    t = F(11)
    E, H, K = 8 * t, 12 * t, 4 * t
    q = [0 - F(1, 4) * E, E - F(3, 4) * E]
    check((t + K / H * q[0], 3 * t + K / H * q[1]) == (t / 3, 11 * t / 3),
          f"q_i formula reproduces the traced (1,3) gate crossings t/3 and 11t/3 at t=11 (q={q})")
    rng = random.Random(228)
    B = 12
    n = {'inst': 0, 'rule_true': 0, 'rule_false': 0, 'found_true': 0, 'construct_ok': 0, 'found_false': 0,
         'miss_true': 0}
    bad = []
    for _ in range(600):
        p = rng.choice((1, 2, 3))
        al = sorted(rng.sample([F(k, 12) for k in range(1, 12)], p))
        J = {c for c in range(p + 1) if rng.random() < 0.55}
        lam = {c: [rng.choice((1, 2, 3, 4, 6)) for _ in range(rng.choice((1, 2)))] for c in J}
        eps = [rng.choice((-1, 1)) for _ in range(p)]
        n['inst'] += 1
        # attainable totals per cut: sum of m_g * lambda_g, 0 <= m_g <= B, capped at B
        att = []
        for c in range(p + 1):
            if c not in J:
                att.append([0])
                continue
            vals = {0}
            for l in lam[c]:
                vals = {v + k * l for v in vals for k in range(B + 1) if v + k * l <= B}
            att.append(sorted(vals))
        found = any(signs_ok(list(h), al, eps) for h in product(*att))
        r = rules(eps, J, p)
        if r:
            n['rule_true'] += 1
            n['found_true'] += found
            n['miss_true'] += not found
            cnt = construct(al, J, eps, lam)
            n['construct_ok'] += cnt is not None
            if cnt is None:
                bad.append(('construct', al, J, eps))
        else:
            n['rule_false'] += 1
            n['found_false'] += found
            if found:
                bad.append(('necessity', al, J, eps))
    say(f"   {n}")
    check(n['found_false'] == 0, f"necessity: {n['rule_false']} rule-violating instances, none has integer counts "
                                 f"(per-cut totals <= {B})")
    check(n['construct_ok'] == n['rule_true'], f"sufficiency: the note's run construction + floor(Mw/lambda) gives "
                                                f"valid integer counts on all {n['rule_true']} rule-satisfying instances")
    say(f"   bounded search found counts on {n['found_true']} / {n['rule_true']} rule-true instances "
        f"(the rest need totals > {B}; construction covers them)")
    if bad:
        say(f"   first bad instances: {bad[:3]}")
    # exhaustive: all demands and cut sets for p<=4 with fixed alphas, rules vs construction (unbounded) and
    # bounded necessity
    ok, tot = True, 0
    for p in (1, 2, 3, 4):
        al = [F(k, p + 1) for k in range(1, p + 1)]
        for Jbits in range(2 ** (p + 1)):
            J = {c for c in range(p + 1) if Jbits >> c & 1}
            lam = {c: [1] for c in J}
            for eps in product((-1, 1), repeat=p):
                tot += 1
                r = rules(list(eps), J, p)
                c = construct(al, J, list(eps), lam) if r else None
                if r and c is None:
                    ok = False
                if not r:
                    att = [list(range(0, 9)) if cc in J else [0] for cc in range(p + 1)]
                    if any(signs_ok(list(h), al, list(eps)) for h in product(*att)):
                        ok = False
    check(ok, f"exhaustive p<=4, equally spaced alphas, every cut set and demand ({tot} cases): rules <=> realizable")
    # examples stated in the note
    check(rules([-1, 1, -1], {1, 3}, 3) and not rules([-1, 1, -1], {1}, 3) and not rules([-1, 1, -1], {3}, 3)
          and rules([1, -1], {0, 2}, 2), "(-,+,-) needs cut 1 and cut p; (+,-) needs no internal cut")


# ------------------------------------------------------------------ claim 5
def claim5():
    say("\n=== Claim 5: repeated-excursion times and the clearance expression")
    s0, L = F(7), F(3)
    for mm in (1, 2, 4):
        s, ev = s0, []
        for _ in range(mm):
            s += L; ev.append(('roof', s))
            s += L; ev.append(('floor', s))
        s += L; ev.append(('up', s))
        exp = [x for h in range(1, mm + 1) for x in (('roof', s0 + (2 * h - 1) * L), ('floor', s0 + 2 * h * L))] \
            + [('up', s0 + (2 * mm + 1) * L)]
        check(ev == exp, f"m={mm}: roof at s0+(2h-1)L, floor at s0+2hL, transmit at s0+(2m+1)L")
    ok = True
    for K, H, X0, s, l, u in ((F(4), F(8), F(0), F(3), F(0), F(2)), (F(2), F(4), F(0), F(2), F(0), F(1)),
                              (F(5), F(9), F(-1), F(4), F(1), F(3))):
        X = X0 + K * s / H
        v = min(K * s - H * (l - X0), H * (u - X0) - K * s)
        ok &= (v > 0) == (l < X < u) and v / H == min(X - l, u - X)
    check(ok, "min{K s - H(l-X0), H(u-X0) - K s}/H = min(X-l, u-X): strict positivity <=> X in (l,u)")


# ------------------------------------------------------------------ claim 6
def claim6():
    say("\n=== Claim 6: R22 pair (0,0)->(2,2); <=20 hand-chosen count/winding combinations")
    S, T = (F(0), F(0)), (F(2), F(2))
    # sign cone: single pin at y=1 (alpha=1/2), demand minus; cut p=1 available (slab 1<y<2 roof/floor faces)
    check(rules([-1], {1}, 1), "single minus demand with cut p available: in the sign cone")
    # direct winding K=2: every excursion count vector gives direction (2, +-(2+E)); H=2+E with E even.
    # roof turn in slab (1,2) at x in (0,1) needs 4/H<1, floor turn at x in (1,3) needs 6/H>1: 4<H<6, no even H.
    Hs = [2 + E for E in range(0, 40, 2)]
    check(not any(4 < H < 6 for H in Hs), "direct winding: one excursion needs 4 < H < 6, but H = 2 + E is even")
    # clearance of the note's chains for E=2 (excursion) and E=2 (target-end delay), E=4 two excursions
    plans = {
        'E=2 slab(1,2) excursion': excursion_plan([F(1), F(2)], {1: 1}),
        'E=4 two slab(1,2) excursions': excursion_plan([F(1), F(2)], {1: 2}),
    }
    for lab, pl in plans.items():
        ok, cl, rows = chain_test(R22, S, F(2), pl)
        last = rows[-1]
        check(not ok, f"{lab}: chain fails at level {last[0]} ({last[1]}), s={last[2]}, x={last[3]}, "
                      f"clearance {cl}")
    # target-end delay (cut p, d3=1): cross y=2 at s=2, turn at y=3 roof, return to (2,2) at s=4
    H = F(4)
    x_cross = F(2) * 2 / H
    check(x_cross == 1, f"E=2 target-end delay: y=2 crossing at s=2, x={x_cross}: corner (1,2), zero clearance")
    # traced combinations: (direction, meaning)
    combos = [
        ((2, 2), "direct winding, no delay"),
        ((2, 4), "direct, one slab(1,2) excursion or one target-end delay (E=2)"),
        ((2, -4), "direct, source end delay downward (E=2)"),
        ((2, 6), "direct, E=4: two excursions / excursion+target delay"),
        ((2, -6), "direct, down-first E=4"),
        ((2, 8), "direct, E=6"),
        ((2, -8), "direct, down-first E=6"),
        ((2, 10), "direct, E=8"),
        ((2, 14), "direct, E=12"),
        ((-2, 2), "winding: target reflected in x=0, no delay"),
        ((-2, 4), "winding x=0, E=2"),
        ((-2, -4), "winding x=0, down-first E=2"),
        ((6, 2), "winding: target reflected in x=4, no delay"),
        ((6, 4), "winding x=4, E=2"),
        ((6, 6), "winding x=4, E=4"),
        ((4, 2), "winding: target reflected in x=3, no delay"),
        ((4, 4), "winding x=3, E=2"),
        ((4, 6), "winding x=3, E=4"),
        ((-6, 4), "winding: reflected in x=-1 then x=?, E=2"),
        ((2, 12), "direct, E=10"),
    ]
    check(len(combos) <= 20, f"{len(combos)} combinations (budget 20)")
    lit = []
    for d, why in combos:
        st, info, path = trace(R22, S, d, T, maxref=400)
        nref = len(path) - 2 if st == 'T' else len(path) - 1
        say(f"   d={d}: {st} {fmt(info)} after {nref} reflections  [{why}]")
        if st == 'T':
            lit.append(d)
    check(not lit, f"no traced combination reaches T (R22 darkness not contradicted); lit={lit}")


if __name__ == '__main__':
    claim1()
    claim2_3()
    claim4()
    claim5()
    claim6()
    say(f"\ncpu {time.process_time() - T0:.2f}s")
    say(f"FAILURES: {len(FAILS)}" + (f" ({FAILS})" if FAILS else ""))
