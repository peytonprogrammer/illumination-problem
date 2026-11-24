"""D212 referee checks: descent skeleton, parallel retained transfer (k >= 2).

Exact integer-scaled grid tracer (adapted from the d210 tracer, with the
pre-event x-direction recorded so the base chart is exact at wall bounces).
Named rooms only, all built here from rectangles:
  U21  : base row x[0,6); arms x[0,2) and x[3,6), y[1,4). Band row y[1,2), widths 2,3.
  H26  : bars x[0,2) and x[3,6), y[0,5); crossbar x[2,3), y[2,3). Band row y[3,4), widths 2,3.
  U29  : base row x[0,8); arms x[0,2) and x[3,8), y[1,4). Band row y[1,2), widths 2,5.
  STAIR: nine-row left-aligned staircase, widths 9..1, scaled by t.
The only direction search is a bounded first-hit seed search inside the
three named parents (|p|+|q| <= 13), used to obtain actual parent seeds.
Run: nice -n 10 python3 -B checks.py
"""
from fractions import Fraction as F
from math import gcd, floor, ceil
import time

T0 = time.process_time()
FAILS = []


def say(*a):
    print(*a, flush=True)


def check(cond, msg):
    say(("PASS " if cond else "FAIL ") + msg)
    if not cond:
        FAILS.append(msg)


# ------------------------------------------------------------------ rooms
def rects(*rs):
    return {(x, y) for (x0, x1, y0, y1) in rs for x in range(x0, x1) for y in range(y0, y1)}


def marks_of(c):
    return sorted({(x, y) for (x, y) in c if {(x - 1, y), (x, y - 1), (x - 1, y - 1)} <= c},
                  key=lambda p: (p[1], p[0]))


def vertex_counts(c):
    """(reflex, convex, pinch) lattice vertices."""
    pts = {(x + dx, y + dy) for (x, y) in c for dx in (0, 1) for dy in (0, 1)}
    rx = cv = pin = 0
    for (x, y) in pts:
        bl, br, tl, tr = (x - 1, y - 1) in c, (x, y - 1) in c, (x - 1, y) in c, (x, y) in c
        n = bl + br + tl + tr
        if n == 3: rx += 1
        elif n == 1: cv += 1
        elif n == 2 and (bl == tr): pin += 1
    return rx, cv, pin


def connected(c):
    c = set(c); st = [next(iter(c))]; seen = {st[0]}
    while st:
        x, y = st.pop()
        for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if n in c and n not in seen: seen.add(n); st.append(n)
    return len(seen) == len(c)


def no_holes(c):
    xs = [x for x, _ in c]; ys = [y for _, y in c]
    box = {(x, y) for x in range(min(xs) - 1, max(xs) + 2) for y in range(min(ys) - 1, max(ys) + 2)}
    return connected(box - c)


def strictly_simple(c):
    return connected(c) and no_holes(c) and vertex_counts(c)[2] == 0


def insert_row(c, J, E):
    """Replace row y in [J, J+1) by a row of height 1+E."""
    out = set()
    for (x, y) in c:
        if y < J: out.add((x, y))
        elif y == J: out.update((x, J + i) for i in range(E + 1))
        else: out.add((x, y + E))
    return out


def shiftm(m, J, E):
    return (m[0], m[1] + E) if m[1] > J else m


def row_section(c, y):
    xs = sorted(x for (x, yy) in c if yy == y)
    iv = []
    for x in xs:
        if iv and iv[-1][1] == x: iv[-1][1] = x + 1
        else: iv.append([x, x + 1])
    return [tuple(i) for i in iv]


def wall_levels(c, axis):
    """Distinct coordinates of walls perpendicular to `axis` (axis=1: horizontal walls, y-levels)."""
    lv = set()
    for (x, y) in c:
        if axis == 1:
            if (x, y - 1) not in c: lv.add(y)
            if (x, y + 1) not in c: lv.add(y + 1)
        else:
            if (x - 1, y) not in c: lv.add(x)
            if (x + 1, y) not in c: lv.add(x + 1)
    return sorted(lv)


# ------------------------------------------------------------------ tracer
def trace(cells, S, d, m, levels=False, hits=False):
    """Exact trace from lattice point S, primitive direction d=(p,q), m primitive steps.
    lv entries at integer-y crossings: (axial, x, dx_after, y, dx_before)."""
    p, q = d
    ap, aq = abs(p), abs(q)
    Sc = (ap or 1) * (aq or 1)
    X, Y = S[0] * Sc, S[1] * Sc
    dx, dy = (p > 0) - (p < 0), (q > 0) - (q < 0)
    total = m * Sc
    tick = 0
    lv = [(0, F(S[0]), dx, S[1], dx)] if levels else None
    hit = {} if hits else None
    out = dict(ok=True, corner=None)
    while tick < total:
        tx = ((Sc - X % Sc) if dx > 0 else (X % Sc or Sc)) // ap if ap else 1 << 62
        ty = ((Sc - Y % Sc) if dy > 0 else (Y % Sc or Sc)) // aq if aq else 1 << 62
        st = min(tx, ty, total - tick)
        X += dx * ap * st; Y += dy * aq * st; tick += st
        onx, ony = X % Sc == 0, Y % Sc == 0
        dx_before = dx
        if onx and ony:
            x, y = X // Sc, Y // Sc
            bl, br, tl, tr = (x - 1, y - 1) in cells, (x, y - 1) in cells, (x - 1, y) in cells, (x, y) in cells
            n = bl + br + tl + tr
            if n == 4:
                if hits and (x, y) not in hit: hit[x, y] = tick // Sc
            elif n == 2 and bl and br:
                if dy == 0: out.update(ok=False, corner=(x, y)); break
                if dy > 0: dy = -dy
            elif n == 2 and tl and tr:
                if dy == 0: out.update(ok=False, corner=(x, y)); break
                if dy < 0: dy = -dy
            elif n == 2 and bl and tl:
                if dx == 0: out.update(ok=False, corner=(x, y)); break
                if dx > 0: dx = -dx
            elif n == 2 and br and tr:
                if dx == 0: out.update(ok=False, corner=(x, y)); break
                if dx < 0: dx = -dx
            else:
                out.update(ok=False, corner=(x, y)); break
        elif onx:
            x, cy = X // Sc, Y // Sc
            if dx > 0 and (x, cy) not in cells: dx = -dx
            elif dx < 0 and (x - 1, cy) not in cells: dx = -dx
        elif ony:
            y, cx = Y // Sc, X // Sc
            if dy > 0 and (cx, y) not in cells: dy = -dy
            elif dy < 0 and (cx, y - 1) not in cells: dy = -dy
        if levels and ony and aq:
            lv.append((tick * aq // Sc, F(X, Sc), dx, Y // Sc, dx_before))
    out['end'] = (F(X, Sc), F(Y, Sc))
    out['lv'] = lv
    out['hit'] = hit
    return out


def reached(r, T):
    return r['ok'] and r['end'] == (T[0], T[1])


# ------------------------------------------------------------------ seed data
def comp_of(c, J, x0, x1):
    """Component of row J containing the open segment between x0 and x1."""
    xm = (x0 + x1) / 2
    for a, b in row_section(c, J):
        if a < xm < b: return (a, b)
    raise AssertionError((x0, x1))


def seed_data(c, S, T, d, m, J):
    r = trace(c, S, d, m, levels=True)
    assert reached(r, T), (S, T, d, m, r['corner'])
    lv = r['lv']
    ys = [e[3] for e in lv]
    D = len(ys) - 1
    assert D == m * abs(d[1])
    sel, comps = [], []
    for t in range(1, D + 1):
        assert abs(ys[t] - ys[t - 1]) == 1
        if {ys[t - 1], ys[t]} == {J, J + 1}:
            sel.append(t)
            comps.append(comp_of(c, J, lv[t - 1][1], lv[t][1]))
    b = [sum(1 for x in sel if x <= t) for t in range(D + 1)]
    g = gcd(abs(d[0]), abs(d[1]))
    u, v = abs(d[0]) // g, abs(d[1]) // g
    mm = len(sel)
    widths = sorted({bb - aa for aa, bb in comps})
    Q = 1
    for w in widths: Q = Q * w // gcd(Q, w)
    M = max(abs(F(t) - F(D * b[t], mm)) for t in range(D + 1)) if mm else 0
    return dict(D=D, m=mm, sel=sel, comps=comps, b=b, s0=F(u, v), u=u, v=v, lv=lv, ys=ys,
                Q=Q, M=M, widths=widths, d=d, steps=m)


def e_of(sd, t, dl):
    return (F(t) - F(sd['D'] * sd['b'][t], sd['m'])) * dl


def gate(sd, dl):
    """Signed gate: base developed X0(t)=s0 t (X0(0)=0 integral offset); for t=1..D-1
    the perturbed coordinate stays strictly between nearest strictly lower/higher integers."""
    for t in range(1, sd['D']):
        z = sd['s0'] * t
        e = e_of(sd, t, dl)
        if not (ceil(z) - 1 < z + e < floor(z) + 1): return False
    return True


def reaim(sd, E, N, P):
    D, m, s0 = sd['D'], sd['m'], sd['s0']
    s = (D * s0 + 2 * P * m * N) / (D + m * E)
    return s, s - s0


def trace_reaimed(cells, S, sd, s, E):
    tot = sd['D'] + sd['m'] * E
    assert tot % s.denominator == 0
    p, q = sd['d']
    dd = (s.numerator if p > 0 else -s.numerator, s.denominator if q > 0 else -s.denominator)
    return trace(cells, S, dd, tot // s.denominator, levels=True)


def state_matches(sd, r, E, dl, J):
    """At every old level t compare the child state with the base chart applied to
    X0(t)+e(t). Returns number of levels checked and number of mismatches."""
    s0 = sd['s0']
    chk = bad = 0
    for t in range(sd['D'] + 1):
        _, x0, dxa, y0, dxb = sd['lv'][t]
        ci = t + E * sd['b'][t]
        _, x1, dx1a, y1, dx1b = r['lv'][ci]
        if y1 != (y0 + E if y0 > J else y0):
            bad += 1; chk += 1; continue
        X = s0 * t + e_of(sd, t, dl)
        c = x0 - dxa * s0 * t
        cands = {(c + dxa * X, dxa)}
        if dxa != dxb:  # base bounced on a vertical wall exactly at this lattice point
            cands.add((2 * x0 - c - dxa * X, dxb))
        # child direction: before-event if it has not reached the wall, after otherwise
        chk += 1
        if (x1, dx1a) not in cands and (x1, dx1b) not in cands:
            bad += 1
    return chk, bad


def state_matches_alt(sd, r, E, dl, J):
    """Same as state_matches but with the uncorrected prediction e(t) = t*delta."""
    s0 = sd['s0']; chk = bad = 0
    for t in range(sd['D'] + 1):
        _, x0, dxa, y0, dxb = sd['lv'][t]
        _, x1, dx1a, y1, dx1b = r['lv'][t + E * sd['b'][t]]
        X = s0 * t + t * dl
        c = x0 - dxa * s0 * t
        cands = {(c + dxa * X, dxa)}
        if dxa != dxb: cands.add((2 * x0 - c - dxa * X, dxb))
        chk += 1
        if (x1, dx1a) not in cands and (x1, dx1b) not in cands: bad += 1
    return chk, bad


# ------------------------------------------------------------------ claim 1-2 structure
def structure(name, c, J):
    say(f"\n=== Claims 1-2 structure on {name}")
    rx, cv, pin = vertex_counts(c)
    A = len(c)
    hb = wall_levels(c, 1); vb = wall_levels(c, 0)
    secs = {y: row_section(c, y) for y in range(hb[0], hb[-1])}
    bands_h = len(hb) - 1; bands_v = len(vb) - 1
    kmax = max(len(s) for s in secs.values())
    say(f"  area {A}, reflex r={rx}, convex {cv}, pinch {pin}; walls W={2*rx+4}; "
        f"horizontal levels {hb}, vertical levels {vb}; bands {bands_h}+{bands_v}; max k {kmax}; "
        f"band row J={J} section {secs[J]}")
    check(strictly_simple(c) and cv == rx + 4, f"{name}: strictly simple, convex = r+4")
    check(bands_h <= rx + 1 and bands_v <= rx + 1 and kmax <= (rx + 2) // 2,
          f"{name}: bands per axis <= r+1, k <= floor((r+2)/2)")
    # constant section on each band (between consecutive levels)
    const = all(len({tuple(secs[y]) for y in range(hb[i], hb[i + 1])}) == 1 for i in range(len(hb) - 1))
    check(const, f"{name}: section constant within each horizontal band")
    w = [b - a for a, b in secs[J]]
    pm = set(marks_of(c))
    pts = {(x + dx, y + dy) for (x, y) in c for dx in (0, 1) for dy in (0, 1)}
    ncell = lambda P: sum(((P[0] - i, P[1] - j) in c) for i in (0, 1) for j in (0, 1))
    I = sum(1 for P in pts if ncell(P) == 4)
    Bw = sum(1 for P in pts if ncell(P) == 2)
    states = 4 * I + 2 * Bw
    check(states == 4 * A - 4 * rx - 4 and states <= 4 * A - 2 * rx,
          f"{name}: nonsingular lattice states {states} = 4A-4r-4 <= 4A-2r (first-hit D bound)")
    for E in (1, 2, 5, 9):
        ch = insert_row(c, J, E)
        cm = set(marks_of(ch))
        retained = {shiftm(mk, J, E) for mk in pm}
        new = cm - retained
        rx2, cv2, pin2 = vertex_counts(ch)
        ok = (retained <= cm and len(new) == E * sum(x - 1 for x in w) and all(J < mk[1] < J + 1 + E for mk in new)
              and len(ch) - A == E * sum(w) and (rx2, cv2, pin2) == (rx, cv, pin) and strictly_simple(ch))
        # compress back: remove E copies of the band row
        back = {(x, y) for (x, y) in ch if y <= J} | {(x, y - E) for (x, y) in ch if y > J + E}
        ok = ok and back == c
        check(ok, f"{name} E={E}: child area +E*sum(w)={E*sum(w)}, same turns, retained marks {len(retained)}, "
                  f"new marks {len(new)} = E*sum(w-1), compression returns the parent")


# ------------------------------------------------------------------ claim 3 seeds + re-aim
def find_seeds(c, J, maxl=13):
    """Bounded first-hit seed search inside one named parent."""
    A = len(c)
    rx = vertex_counts(c)[0]
    L = 4 * A - 2 * rx
    marks = marks_of(c)
    best = {}
    dirs = [(p, q) for s in range(2, maxl + 1) for p in range(1, s) for q in [s - p] if gcd(p, q) == 1]
    for S in marks:
        for (p, q) in dirs:
            for sx in (1, -1):
                for sy in (1, -1):
                    r = trace(c, S, (sx * p, sy * q), L, hits=True)
                    for T, steps in r['hit'].items():
                        if T == S: continue
                        sd = seed_data(c, S, T, (sx * p, sy * q), steps, J)
                        if len(sd['widths']) < 2: continue
                        key = (S, T)
                        # keep, per pair, the seed with most alternations then smallest D
                        alt = sum(1 for i in range(1, len(sd['comps'])) if sd['comps'][i] != sd['comps'][i - 1])
                        sc = (alt, -sd['D'])
                        if key not in best or sc > best[key][0]: best[key] = (sc, sd)
    return [v[1] for v in best.values()], L


def reaim_tests(name, c, J, nseeds=6, Emax=260):
    say(f"\n=== Claim 3 on {name}: parallel retained transfer, k=2 band, re-aimed actual seeds")
    seeds, L = find_seeds(c, J)
    seeds.sort(key=lambda sd: (-sum(1 for i in range(1, len(sd['comps'])) if sd['comps'][i] != sd['comps'][i - 1]),
                               sd['D']))
    seeds = seeds[:nseeds]
    check(len(seeds) >= 2, f"{name}: found {len(seeds)} parent seeds traversing both components")
    T = dict(gate_pass=0, gate_pass_illegal=0, gate_fail=0, gate_fail_legal=0, lv_checked=0, lv_bad=0,
             thr_cases=0, thr_fail=0, below_thr=0, below_thr_legal=0, wrongP=0, wrongP_legal=0, Dbound_bad=0,
             sens_cases=0, sens_detected=0, wrongP_gate=0, wrongP_gate_legal=0)
    for sd in seeds:
        S = tuple(map(int, (sd['lv'][0][1], sd['lv'][0][3])))
        Tm = None
        # recover target from the base trace end
        r0 = trace(c, S, sd['d'], sd['steps'])
        Tm = (int(r0['end'][0]), int(r0['end'][1]))
        sd['S'], sd['T'] = S, Tm
        thr = sd['Q'] * sd['v'] * sd['M'] - F(sd['D'], sd['m'])
        alt = [sd['comps'][i][0] for i in range(len(sd['comps']))]
        dirs = [sd['ys'][t] - sd['ys'][t - 1] for t in sd['sel']]
        if sd['D'] > L * sd['v']: T['Dbound_bad'] += 1
        say(f"  seed {S}->{Tm} dir {sd['d']} steps {sd['steps']}: s0={sd['s0']} D={sd['D']} m={sd['m']} "
            f"sel={sd['sel']} comp-left-ends={alt} up/down={dirs} widths={sd['widths']} Q={sd['Q']} "
            f"M={sd['M']} threshold E>{thr} (~{float(thr):.1f})")
        Etop = min(Emax, int(thr) + 25)
        for E in range(1, Etop + 1):
            ch = insert_row(c, J, E)
            S2, T2 = shiftm(S, J, E), shiftm(Tm, J, E)
            N0 = round(E * sd['s0'] / (2 * sd['Q']))
            for N in range(max(0, N0 - 1), N0 + 2):
                s, dl = reaim(sd, E, N, sd['Q'])
                if s <= 0: continue
                g = gate(sd, dl)
                r = trace_reaimed(ch, S2, sd, s, E)
                ok = reached(r, T2)
                if g:
                    T['gate_pass'] += 1
                    if not ok:
                        T['gate_pass_illegal'] += 1; say("   COUNTEREXAMPLE", S, Tm, E, N, dl, r['corner'])
                    else:
                        k_, b_ = state_matches(sd, r, E, dl, J)
                        T['lv_checked'] += k_; T['lv_bad'] += b_
                        # sensitivity: an uncorrected error t*delta must be rejected when delta != 0
                        if dl != 0:
                            sd2 = dict(sd, b=[0] * (sd['D'] + 1), m=1)
                            _, b2 = state_matches_alt(sd, r, E, dl, J)
                            T['sens_cases'] += 1; T['sens_detected'] += b2 > 0
                else:
                    T['gate_fail'] += 1; T['gate_fail_legal'] += ok
                if N == N0:
                    if E > thr:
                        T['thr_cases'] += 1
                        if not (abs(dl) <= sd['Q'] / (E + F(sd['D'], sd['m'])) and g and ok): T['thr_fail'] += 1
                    else:
                        T['below_thr'] += 1; T['below_thr_legal'] += ok
            # wrong period: shift 2*w1*N (one component's period only), N not a multiple of Q/w1
            w1 = sd['widths'][0]
            for N in range(1, 4):
                if (2 * w1 * N) % (2 * sd['widths'][1]) == 0: continue
                s, dl = reaim(sd, E, N, w1)
                if s <= 0: continue
                r = trace_reaimed(ch, S2, sd, s, E)
                T['wrongP'] += 1; T['wrongP_legal'] += reached(r, T2)
                if gate(sd, dl):
                    T['wrongP_gate'] += 1; T['wrongP_gate_legal'] += reached(r, T2)
    say("  tally", T, f"cpu {time.process_time()-T0:.1f}s")
    check(T['gate_pass_illegal'] == 0, f"{name}: every gate-passing re-aim is legal and ends at the target ({T['gate_pass']})")
    check(T['lv_bad'] == 0, f"{name}: child state equals base chart at X0(t)+e(t) at all {T['lv_checked']} old-level visits")
    check(T['thr_fail'] == 0, f"{name}: E > QvM - D/m with nearest N gives |delta|<=Q/(E+D/m), gate pass, legal ({T['thr_cases']})")
    check(T['Dbound_bad'] == 0, f"{name}: D <= (4*area-2r)*v for all chosen first-hit seeds")
    say(f"  below threshold (nearest N): {T['below_thr']} cases, {T['below_thr_legal']} legal; "
        f"gate-failing re-aims {T['gate_fail']}, of which legal {T['gate_fail_legal']}")
    say(f"  wrong period 2*w1*N (not a multiple of 2*w2): {T['wrongP']} traces, {T['wrongP_legal']} reach the target; "
        f"of those passing the same gate test {T['wrongP_gate']}, legal {T['wrongP_gate_legal']}")
    check(T['sens_detected'] == T['sens_cases'],
          f"{name}: state check rejects the uncorrected error t*delta in all {T['sens_cases']} cases with delta != 0")
    return seeds


def algebra():
    say("\n=== Claim 3 algebra: selected-step increment (1+E)s - s0 - 2QN = (1-D/m)delta, e(D)=0")
    bad = n = 0
    for D in range(1, 11):
        for m in range(1, D + 1):
            for Q in (1, 6, 10):
                for E in range(0, 7):
                    for N in range(-1, 3):
                        for s0 in (F(1, 3), F(5, 7), F(9, 4)):
                            s = (D * s0 + 2 * Q * m * N) / (D + m * E)
                            dl = s - s0
                            n += 1
                            if (1 + E) * s - s0 - 2 * Q * N != (1 - F(D, m)) * dl: bad += 1
                            if D * dl + m * ((1 - F(D, m)) * dl - dl) != 0: bad += 1  # sum of increments
    check(bad == 0, f"increment identity and e(D)=0 on {n} grid cases")


# ------------------------------------------------------------------ claim 5 staircase
def staircase():
    say("\n=== Claim 5: nine-row staircase scaled by t")
    for t in (1, 2, 3, 4):
        c = rects(*[(0, (9 - j) * t, j * t, (j + 1) * t) for j in range(9)])
        rx, cv, pin = vertex_counts(c)
        hb, vb = wall_levels(c, 1), wall_levels(c, 0)
        gh = {hb[i + 1] - hb[i] for i in range(len(hb) - 1)}
        gv = {vb[i + 1] - vb[i] for i in range(len(vb) - 1)}
        # compress each horizontal band (thickness t) to 1
        mins = []
        for i in range(len(hb) - 1):
            a, h = hb[i], hb[i + 1] - hb[i]
            E = h - 1
            par = {(x, y) for (x, y) in c if y < a + 1} | {(x, y - E) for (x, y) in c if y >= a + h}
            mins.append(len(par))
        check(rx == 8 and cv == 12 and pin == 0 and len(c) == 45 * t * t and gh == {t} and gv == {t}
              and min(mins) >= 36 * t * t,
              f"staircase t={t}: r=8, area {len(c)}=45t^2, all gaps {t}, min compressed area {min(mins)} >= 36t^2")
    c = rects(*[(0, 9 - j, j, j + 1) for j in range(9)])
    hb, vb = wall_levels(c, 1), wall_levels(c, 0)
    check(all(hb[i + 1] - hb[i] == 1 for i in range(9)) and all(vb[i + 1] - vb[i] == 1 for i in range(9)),
          "staircase t=1: no band of thickness >= 2 on either axis (area 45 > census 21)")


# ------------------------------------------------------------------ claim 1 bound
def pigeonhole():
    say("\n=== Claim 1 arithmetic")
    ok = all((r + 1) <= 9 and (r + 3) <= 11 for r in range(0, 9))
    check(ok and 9 * 9 == 81 and 11 * 11 == 121,
          "r<=8: <= r+1 <= 9 bands, <= r+3 <= 11 refined gaps; box <= 81(h0-1)^2 resp. 121(h0-1)^2")
    # nonnegative example check: a room's max band thickness >= ceil(sqrt(area)/(r+1))
    for name, c in ROOMS.items():
        rx = vertex_counts(c)[0]
        th = max(max(b - a for a, b in zip(L, L[1:])) for L in (wall_levels(c, 0), wall_levels(c, 1)))
        A = len(c)
        check(th * th * (rx + 1) ** 2 >= A, f"{name}: max thickness {th} >= sqrt(area {A})/(r+1)")


# ------------------------------------------------------------------ claim 6 scaling + perturbation
def scale_room(c, gx, gy):
    return {(x * gx + i, y * gy + j) for (x, y) in c for i in range(gx) for j in range(gy)}


def scaling_test(name, c, seeds):
    say(f"\n=== Claim 6a: axis scaling lifts seeds exactly ({name})")
    n = bad = 0
    for gx, gy in ((2, 1), (1, 3), (2, 3), (5, 2)):
        cs = scale_room(c, gx, gy)
        for sd in seeds:
            p, q = sd['d']
            P, Q_ = p * gx, q * gy
            g = gcd(abs(P), abs(Q_))
            S2 = (sd['S'][0] * gx, sd['S'][1] * gy); T2 = (sd['T'][0] * gx, sd['T'][1] * gy)
            r = trace(cs, S2, (P // g, Q_ // g), sd['steps'] * g)
            n += 1; bad += not reached(r, T2)
    check(bad == 0, f"{name}: {n} scaled seed lifts legal and exact")


def realize(xgaps, ygaps, rect_idx, mark_idx):
    xs = [0]
    for gg in xgaps: xs.append(xs[-1] + gg)
    ys = [0]
    for gg in ygaps: ys.append(ys[-1] + gg)
    c = rects(*[(xs[a], xs[b], ys[cc], ys[d]) for (a, b, cc, d) in rect_idx])
    return c, [(xs[i], ys[j]) for (i, j) in mark_idx], xs, ys


def hits_sequence(c, S, d, steps):
    """Wall hits (axis, coordinate) in order, for the unfolding."""
    p, q = d
    r = trace(c, S, d, steps, levels=False)
    assert r['ok']
    # replay with event capture
    ap, aq = abs(p), abs(q); Sc = ap * aq
    X, Y = S[0] * Sc, S[1] * Sc; dx, dy = (p > 0) - (p < 0), (q > 0) - (q < 0)
    tick, total, seq = 0, steps * Sc, []
    while tick < total:
        tx = ((Sc - X % Sc) if dx > 0 else (X % Sc or Sc)) // ap
        ty = ((Sc - Y % Sc) if dy > 0 else (Y % Sc or Sc)) // aq
        st = min(tx, ty, total - tick)
        X += dx * ap * st; Y += dy * aq * st; tick += st
        onx, ony = X % Sc == 0, Y % Sc == 0
        x, y = X // Sc, Y // Sc
        if onx:
            cy = Y // Sc if not ony else None
            if not ony:
                if (dx > 0 and (x, cy) not in c) or (dx < 0 and (x - 1, cy) not in c):
                    dx = -dx; seq.append((0, x))
            else:
                bl, br, tl, tr = (x - 1, y - 1) in c, (x, y - 1) in c, (x - 1, y) in c, (x, y) in c
                if (bl and tl and not br and not tr and dx > 0) or (br and tr and not bl and not tl and dx < 0):
                    dx = -dx; seq.append((0, x))
                if (bl and br and not tl and not tr and dy > 0) or (tl and tr and not bl and not br and dy < 0):
                    dy = -dy; seq.append((1, y))
                continue
        if ony and not onx:
            cx = X // Sc
            if (dy > 0 and (cx, y) not in c) or (dy < 0 and (cx, y - 1) not in c):
                dy = -dy; seq.append((1, y))
    return seq


def perturbation_test():
    say("\n=== Claim 6b: perturbation neighbourhood of a template seed (U21 marked chart)")
    # marked chart levels: x: 0,1,2,3,4,6 ; y: 0,1,3,4 ; pair (1,3)->(4,3)
    xg0, yg0 = [1, 1, 1, 1, 2], [1, 2, 1]
    R = [(0, 5, 0, 1), (0, 2, 1, 3), (3, 5, 1, 3)]   # index rectangles (x-index a..b, y-index c..d)
    MK = [(1, 2), (4, 2)]
    c0, (S0, T0_), xs0, ys0 = realize(xg0, yg0, R, MK)
    assert c0 == ROOMS['U21']
    # template seed: first hit in a small direction set
    seed = None
    for s in range(2, 14):
        for p in range(1, s):
            q = s - p
            if gcd(p, q) != 1: continue
            for sx in (1, -1):
                for sy in (1, -1):
                    r = trace(c0, S0, (sx * p, sy * q), 80, hits=True)
                    if T0_ in r['hit'] and seed is None:
                        seed = ((sx * p, sy * q), r['hit'][T0_])
    d, st = seed
    seq = hits_sequence(c0, S0, d, st)
    say(f"  template pair {S0}->{T0_}, seed dir {d}, steps {st}, wall hits {seq}")
    idx_x = {v: i for i, v in enumerate(xs0)}; idx_y = {v: i for i, v in enumerate(ys0)}
    res = []
    import itertools
    for t in (6, 7, 9, 12):
        for cx in itertools.product((-1, 0, 1), repeat=5):
            for cy in ((0, 0, 0), (1, -1, 0), (-1, 0, 1)):
                xg = [t * u + e for u, e in zip(xg0, cx)]; yg = [t * u + e for u, e in zip(yg0, cy)]
                c, (S, T), xs, ys = realize(xg, yg, R, MK)
                # unfold the target through the template's wall sequence, perturbed coordinates
                sgx, cx_, sgy, cy_ = 1, 0, 1, 0
                for ax, val in seq:
                    if ax == 0: cx_ = 2 * xs[idx_x[val]] - cx_; sgx = -sgx
                    else: cy_ = 2 * ys[idx_y[val]] - cy_; sgy = -sgy
                Xe, Ye = sgx * (T[0] - cx_), sgy * (T[1] - cy_)
                P, Q_ = Xe - S[0], Ye - S[1]
                g = gcd(abs(P), abs(Q_))
                r = trace(c, S, (P // g, Q_ // g), g)
                ok = reached(r, T)
                sameit = ok and len(hits_sequence(c, S, (P // g, Q_ // g), g)) == len(seq)
                rel = max(max(abs(e) for e in cx), max(abs(e) for e in cy)) / t
                res.append((t, rel, ok, sameit))
    for t in (6, 7, 9, 12):
        sub = [x for x in res if x[0] == t]
        say(f"  t={t}: {len(sub)} perturbed rooms (|c|<=1, rel err <= {1/t:.3f}); legal {sum(x[2] for x in sub)}, "
            f"same itinerary {sum(x[3] for x in sub)}")
    big = [x for x in res if x[0] >= 9]
    check(all(x[2] and x[3] for x in big), "perturbed rooms with t>=9 (rel err <= 1/9) keep the template itinerary and are lit")


# ------------------------------------------------------------------ main
ROOMS = {
    'U21': rects((0, 6, 0, 1), (0, 2, 1, 4), (3, 6, 1, 4)),
    'H26': rects((0, 2, 0, 5), (3, 6, 0, 5), (2, 3, 2, 3)),
    'U29': rects((0, 8, 0, 1), (0, 2, 1, 4), (3, 8, 1, 4)),
}
BAND = {'U21': 1, 'H26': 3, 'U29': 1}

if __name__ == '__main__':
    pigeonhole()
    for nm, c in ROOMS.items():
        structure(nm, c, BAND[nm])
    algebra()
    allseeds = {}
    for nm, c in ROOMS.items():
        allseeds[nm] = reaim_tests(nm, c, BAND[nm])
    staircase()
    scaling_test('H26', ROOMS['H26'], allseeds['H26'])
    perturbation_test()
    say(f"\nTOTAL FAIL {len(FAILS)}; cpu {time.process_time()-T0:.1f}s")
