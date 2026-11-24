"""D210 referee checks: one-row re-aiming and all-pair cap thresholds.

Own exact integer-scaled grid tracer (independent of the d209 tracer).
Rooms: a21 rank 11 (shard 48, room 1156563) and rank 18 (shard 21, room
4136869), with row 1 (y in [1,2], cut y=3/2) replaced by a row of height 1+E.
Run: nice -n 10 python3 -B checks.py
"""
from fractions import Fraction as F
from math import gcd, floor, ceil
import subprocess, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
A21 = HERE.parent / "seed-profile-a21"
DIRS = [(x, s - x) for s in range(1, 41) for x in range(s, -1, -1) if gcd(x, s - x) == 1]
T0 = time.process_time()
J = 1  # selected row y in [1,2]
FAILS = []


def say(*a):
    print(*a, flush=True)


def check(cond, msg):
    say(("PASS " if cond else "FAIL ") + msg)
    if not cond:
        FAILS.append(msg)


# ------------------------------------------------------------------ rooms
def cells_of(rows):
    return {(x, y) for y, r in enumerate(rows) for x in range(r.bit_length()) if r >> x & 1}


def marks_of(rows):
    c = cells_of(rows)
    return sorted([(x, y) for x, y in c if {(x - 1, y), (x, y - 1), (x - 1, y - 1)} <= c],
                  key=lambda p: (p[1], p[0]))


def inserted(rows, E):
    return rows[:J + 1] + [rows[J]] * E + rows[J + 1:]


def shift(m, E):
    return (m[0], m[1] + E) if m[1] > J else m


def decode(word):
    p, q = DIRS[word & 511]
    sh = word >> 9 & 3
    return p * (1 - 2 * (sh & 1)), q * (1 - 2 * (sh >> 1)), word >> 11 & 127


def archive(shard, room):
    raw = subprocess.check_output([str(A21 / 'extract'), str(A21 / 'a21' / f'{shard}.bin'), str(room)],
                                  text=True).splitlines()
    rows = list(map(int, raw[0].split()))
    marks = marks_of(rows)
    words = list(map(int, raw[1].split()))
    pairs, k = {}, 0
    for i in range(len(marks)):
        for jj in range(i + 1, len(marks)):
            pairs[marks[i], marks[jj]] = decode(words[k]); k += 1
    assert k == len(words)
    return rows, marks, pairs


# ------------------------------------------------------------------ tracer
def trace(cells, S, d, m, T=None, stop_at_T=False, levels=False):
    """Exact trace from lattice point S, primitive direction d=(p,q), for m
    primitive steps (time m). Integer coordinates scaled by Sc=|p||q|.
    Returns dict: ok (no corner), end, hit (first time index in steps where T
    is reached, as Fraction), lv (list of (axial, x, sign_x) at integer y),
    ylv (list of y at those visits)."""
    p, q = d
    ap, aq = abs(p), abs(q)
    Sc = (ap or 1) * (aq or 1)
    X, Y = S[0] * Sc, S[1] * Sc
    dx, dy = (p > 0) - (p < 0), (q > 0) - (q < 0)
    total = m * Sc
    tick = 0
    lv = [] if levels else None
    out = dict(ok=True, hit=None, corner=None)
    if levels:
        lv.append((0, F(S[0]), dx, S[1]))
    while tick < total:
        tx = ((Sc - X % Sc) if dx > 0 else (X % Sc or Sc)) // ap if ap else 1 << 62
        ty = ((Sc - Y % Sc) if dy > 0 else (Y % Sc or Sc)) // aq if aq else 1 << 62
        st = min(tx, ty, total - tick)
        X += dx * ap * st; Y += dy * aq * st; tick += st
        onx, ony = X % Sc == 0, Y % Sc == 0
        if onx and ony:
            x, y = X // Sc, Y // Sc
            bl, br, tl, tr = (x - 1, y - 1) in cells, (x, y - 1) in cells, (x - 1, y) in cells, (x, y) in cells
            n = bl + br + tl + tr
            if n == 4:
                pass
            elif n == 2 and bl and br:      # wall above
                if dy == 0: out.update(ok=False, corner=(x, y, F(tick, Sc))); break
                if dy > 0: dy = -dy
            elif n == 2 and tl and tr:      # wall below
                if dy == 0: out.update(ok=False, corner=(x, y, F(tick, Sc))); break
                if dy < 0: dy = -dy
            elif n == 2 and bl and tl:      # wall to the right
                if dx == 0: out.update(ok=False, corner=(x, y, F(tick, Sc))); break
                if dx > 0: dx = -dx
            elif n == 2 and br and tr:      # wall to the left
                if dx == 0: out.update(ok=False, corner=(x, y, F(tick, Sc))); break
                if dx < 0: dx = -dx
            else:
                out.update(ok=False, corner=(x, y, F(tick, Sc))); break
            if T is not None and out['hit'] is None and (x, y) == tuple(T):
                out['hit'] = F(tick, Sc)
                if stop_at_T: break
        elif onx:
            x, cy = X // Sc, Y // Sc
            if dx > 0 and (x, cy) not in cells: dx = -dx
            elif dx < 0 and (x - 1, cy) not in cells: dx = -dx
        elif ony:
            y, cx = Y // Sc, X // Sc
            if dy > 0 and (cx, y) not in cells: dy = -dy
            elif dy < 0 and (cx, y - 1) not in cells: dy = -dy
        if levels and ony and aq:
            lv.append((tick * aq // Sc, F(X, Sc), dx, Y // Sc))
    out['end'] = (F(X, Sc), F(Y, Sc))
    out['lv'] = lv
    out['ticks'] = F(tick, Sc)
    return out


def reached(r, T):
    return r['ok'] and r['end'] == (T[0], T[1])


def prim(a, b):
    g = gcd(a, b)
    return a // g, b // g, g


# ------------------------------------------------------------------ seed data
def seed_data(cells, S, T, d, m):
    """Level sequence, selected steps, D, k, b(t), s0 from an exact base trace."""
    if d[1] == 0:  # horizontal seed: never meets the cut, carries over on its side
        assert reached(trace(cells, S, d, m), T)
        return dict(D=0, k=0)
    r = trace(cells, S, d, m, levels=True)
    assert reached(r, T), (S, T, r)
    ys = [e[3] for e in r['lv']]
    D = len(ys) - 1
    assert D == m * abs(d[1])
    sel = [t for t in range(1, D + 1) if {ys[t - 1], ys[t]} == {J, J + 1}]
    for t in range(1, D + 1):
        assert abs(ys[t] - ys[t - 1]) == 1 or (ys[t] == ys[t - 1]), (t, ys)
    b = [sum(1 for x in sel if x <= t) for t in range(D + 1)]
    u, v, _ = prim(abs(d[0]), abs(d[1]))
    return dict(D=D, k=len(sel), sel=sel, b=b, s0=F(u, v), u=u, v=v, lv=r['lv'], ys=ys)


def window(sd):
    """Open delta window from the sharpened gate (nearest strictly lower and higher integers)."""
    D, k, b, s0 = sd['D'], sd['k'], sd['b'], sd['s0']
    lo, hi = None, None
    for t in range(1, D):
        z = s0 * t
        B = F(t) - F(D * b[t], k)
        if B == 0: continue
        L, U = F(ceil(z) - 1) - z, F(floor(z) + 1) - z   # L < B*delta < U
        a, c = (L / B, U / B) if B > 0 else (U / B, L / B)
        lo = a if lo is None else max(lo, a)
        hi = c if hi is None else min(hi, c)
    return lo, hi


def reaim(sd, w, E, N):
    D, k, s0 = sd['D'], sd['k'], sd['s0']
    s = (D * s0 + 2 * w * k * N) / (D + k * E)
    return s, s - s0


def trace_reaimed(cells, S, T, d, s, D, k, E):
    P, Q = s.numerator, s.denominator
    tot = D + k * E
    assert tot % Q == 0
    dd = (P if d[0] > 0 else -P, Q if d[1] > 0 else -Q)
    return trace(cells, S, dd, tot // Q, levels=True)


# ------------------------------------------------------------------ claim 1 algebra
def claim1_algebra():
    say("\n=== Claim 1: identity E s - 2wN = -(D/k) delta, e(t), e(D)=0 (exact over a grid)")
    bad = 0
    for D in range(1, 13):
        for k in range(1, D + 1):
            for w in (1, 2, 3):
                for E in range(0, 9):
                    for N in range(-2, 4):
                        for s0 in (F(1, 2), F(3, 5), F(7, 4)):
                            s = (D * s0 + 2 * w * k * N) / (D + k * E)
                            dl = s - s0
                            if E * s - 2 * w * N != -F(D, k) * dl: bad += 1
                            # e(t) = s(t + E b) - 2wN b - s0 t at b=k, t=D must vanish
                            if s * (D + E * k) - 2 * w * N * k - s0 * D != 0: bad += 1
    check(bad == 0, "re-aim identity and e(D)=0 over 4,104x... grid cases")


# ------------------------------------------------------------------ main checks
def room_setup(name, shard, room):
    rows, marks, pairs = archive(shard, room)
    say(f"\n##### {name}: rows {rows}, marks {marks}, area {sum(bin(r).count('1') for r in rows)}")
    return rows, marks, pairs


def claim1_measured(name, rows, pairs, w, Es):
    """Trace every crossing seed re-aimed; compare measured developed errors
    at each old level with e(t) = (t - D b/k) delta; tally gate predictions."""
    say(f"\n=== Claims 1-3 on {name}: every crossing seed, re-aimed, E in {Es[0]}..{Es[-1]}")
    base = cells_of(rows)
    tally = dict(pred_ok=0, pred_ok_fail=0, pred_bad=0, pred_bad_legal=0, err_checked=0, err_bad=0,
                 bound_cases=0, bound_fail=0)
    seeds = {}
    for (S, T), (p, q, m) in pairs.items():
        sd = seed_data(base, S, T, (p, q), m)
        if sd['k'] == 0: continue
        M = max(abs(F(t) - F(sd['D'] * sd['b'][t], sd['k'])) for t in range(sd['D'] + 1))
        lo, hi = window(sd)
        thr = w * sd['v'] * M - F(sd['D'], sd['k'])
        seeds[S, T] = (sd, M, lo, hi)
        say(f"  seed {S}->{T} dir ({p},{q}) m={m}: s0={sd['s0']} D={sd['D']} k={sd['k']} "
            f"selected t={sd['sel']} M={M} window=({lo},{hi}) generic E>{thr}")
    for E in Es:
        cells = cells_of(inserted(rows, E))
        for (S, T), (sd, M, lo, hi) in seeds.items():
            p, q, m = pairs[S, T]
            S2, T2 = shift(S, E), shift(T, E)
            N0 = round(E * sd['s0'] / (2 * w))
            for N in range(max(0, N0 - 1), N0 + 2):
                s, dl = reaim(sd, w, E, N)
                if s <= 0: continue
                pred = lo < dl < hi
                r = trace_reaimed(cells, S2, T2, (p, q), s, sd['D'], sd['k'], E)
                ok = reached(r, T2)
                if pred:
                    tally['pred_ok'] += 1
                    if not ok:
                        tally['pred_ok_fail'] += 1
                        say("   COUNTEREXAMPLE gate", S, T, E, N, dl, r['corner'])
                else:
                    tally['pred_bad'] += 1; tally['pred_bad_legal'] += ok
                if E > w * sd['v'] * M - F(sd['D'], sd['k']) and N == N0:
                    tally['bound_cases'] += 1
                    if not (abs(dl) <= w / (E + F(sd['D'], sd['k'])) and ok): tally['bound_fail'] += 1
                if ok and pred:
                    # measured errors at old levels
                    old = [(a, x, sx) for (a, x, sx, y) in r['lv'] if not (J + 1 <= y <= J + E)]
                    base_lv = sd['lv']
                    assert len(old) == len(base_lv), (len(old), len(base_lv))
                    for t, ((_, x1, s1), (_, x0, s0_, _y)) in enumerate(zip(old, base_lv)):
                        pred_e = (F(t) - F(sd['D'] * sd['b'][t], sd['k'])) * dl
                        if s1 == s0_ and s1 != 0 and floor(x0) == floor(x1) and x0 != floor(x0):
                            meas = (x1 - x0) * s1
                            tally['err_checked'] += 1
                            if meas != pred_e: tally['err_bad'] += 1
    say("  tally", tally, f"cpu {time.process_time()-T0:.1f}s")
    check(tally['pred_ok_fail'] == 0, f"{name}: no window-predicted re-aim fails ({tally['pred_ok']} traced)")
    check(tally['err_bad'] == 0, f"{name}: measured developed error equals (t-Db/k)delta at {tally['err_checked']} level visits")
    check(tally['bound_fail'] == 0, f"{name}: |delta|<=w/(E+D/k) and legal whenever E>wvM-D/k, nearest N ({tally['bound_cases']} cases)")
    return seeds


def claim2_break(rows, pairs, w):
    """Probe the window edges: pick delta just outside the window at the
    binding level and show the trace can fail there; and a downward-traversal check."""
    say("\n=== Claim 2: probing the window edges on rank-18 (3,3)->(4,6)")
    base = cells_of(rows)
    for (S, T) in [((3, 3), (4, 6)), ((3, 3), (1, 5))]:
        p, q, m = pairs[S, T]
        sd = seed_data(base, S, T, (p, q), m)
        lo, hi = window(sd)
        dirs = [sd['ys'][t] - sd['ys'][t - 1] for t in sd['sel']]
        say(f"  {S}->{T}: selected traversal directions (+1 up, -1 down): {dirs}")
        # integer base coordinates where the sharpened (+-1) window applies
        ints = [t for t in range(1, sd['D']) if (sd['s0'] * t).denominator == 1]
        say(f"  levels with integral base coordinate (sharpened window used): {ints}")
        # scan E to find cases with delta outside window, trace them
        outside_fail, outside_ok = [], []
        for E in range(1, 200):
            cells = cells_of(inserted(rows, E))
            N0 = round(E * sd['s0'] / (2 * w))
            for N in (N0, N0 + 1, N0 - 1):
                s, dl = reaim(sd, w, E, N)
                if s <= 0 or lo < dl < hi: continue
                r = trace_reaimed(cells, shift(S, E), shift(T, E), (p, q), s, sd['D'], sd['k'], E)
                (outside_ok if reached(r, shift(T, E)) else outside_fail).append((E, N, dl, r['corner']))
        # sharpening: predicted-legal deltas that move an integral base coordinate off itself,
        # by more than 1/v, on either side (these traces are among the legal ones in claim 1)
        sides = {1: 0, -1: 0}; big = 0
        for E in range(1, 161):
            N0 = round(E * sd['s0'] / (2 * w))
            for N in range(max(0, N0 - 1), N0 + 2):
                s, dl = reaim(sd, w, E, N)
                if s <= 0 or not (lo < dl < hi): continue
                for t in ints:
                    e = (F(t) - F(sd['D'] * sd['b'][t], sd['k'])) * dl
                    if e: sides[1 if e > 0 else -1] += 1
                    if abs(e) >= F(1, sd['v']): big += 1
        say(f"  integral-level displacements in predicted-legal cases: +side {sides[1]}, -side {sides[-1]}, |e|>=1/v {big}")
        say(f"  delta outside window: {len(outside_fail)} illegal, {len(outside_ok)} still legal; "
            f"first illegal {outside_fail[:2]}")


def persistent_interval(s0, D1):
    lo = max(F(i, t) for t in range(1, D1 + 1) for i in range(0, 10 * t + 1) if F(i, t) < s0)
    hi = min(F(i, t) for t in range(1, D1 + 1) for i in range(0, 10 * t + 2) if F(i, t) > s0)
    return lo, hi


def cap_data(name, rows, marks, pairs, a, w, mouth, claimed):
    say(f"\n=== Claim 4 cap table for {name}")
    base = cells_of(rows)
    lower = [mk for mk in marks if mk[1] < 2]
    upper = [mk for mk in marks if mk[1] > 2]
    assert len(lower) == 1
    L0 = lower[0]
    out = {}
    for U in upper:
        p, q, m = pairs[L0, U]
        fw = trace(base, L0, (p, q), m)
        assert reached(fw, U)
        # the reversed seed is the unique sign choice whose level list is fw's reversed
        # pick the reversal that is the true time-reverse: the one whose level list reverses fw's
        fwl = trace(base, L0, (p, q), m, levels=True)['lv']
        cands = []
        for sx in (1, -1):
            for sy in (1, -1):
                r = trace(base, U, (sx * abs(p), sy * abs(q)), m, levels=True)
                if reached(r, L0) and [(e[1], e[3]) for e in r['lv']] == [(e[1], e[3]) for e in fwl[::-1]]:
                    cands.append((sx * abs(p), sy * abs(q), r))
        assert len(cands) == 1
        rp, rq, r = cands[0]
        ent = [e for e in r['lv'] if e[3] == 2 and mouth[0] < e[1] < mouth[1]]
        D1 = ent[0][0]
        # confirm downward: previous level visit above
        idx = r['lv'].index(ent[0])
        assert r['lv'][idx - 1][3] == 3
        u, v, _ = prim(abs(rp), abs(rq))
        s0 = F(u, v)
        lo, hi = persistent_interval(s0, D1)
        Dl = hi - lo
        # smallest E with (D1 + 2 + E) * Dl > 3
        E = 0
        while (D1 + 2 + E) * Dl <= 3: E += 1
        out[U] = dict(d=(rp, rq), s0=s0, D1=D1, lo=lo, hi=hi, thr=E)
        cl = claimed[U]
        say(f"  upper {U}: reversed dir ({rp},{rq}) s0={s0} D1={D1} interval ({lo},{hi}) width {Dl} threshold E>={E}"
            f"  [note: {cl}]")
        check((s0, D1, lo, hi, E) == cl, f"{name} {U} cap row matches note")
    return L0, upper, out


def window_table(rows, pairs, w, claimed):
    say("\n=== Claim 4: upper-pair windows and last missed E (rank 18)")
    base = cells_of(rows)
    res = {}
    for T, (D_c, M_c, A_c, C_c, last_c) in claimed.items():
        S = (3, 3)
        p, q, m = pairs[S, T]
        sd = seed_data(base, S, T, (p, q), m)
        M = max(abs(F(t) - F(sd['D'] * sd['b'][t], sd['k'])) for t in range(sd['D'] + 1))
        lo, hi = window(sd)
        D, k = sd['D'], sd['k']
        # last missed E by brute force over E (nearest two N on each side)
        def legal_pred(E):
            for N in range(0, E + 2):
                s, dl = reaim(sd, w, E, N)
                if s > 0 and lo < dl < hi: return True
            return False
        missed = [E for E in range(0, 400) if not legal_pred(E)]
        last = max(missed)
        # residue formula from the note
        A, C = -1 / lo, 1 / hi
        best = None
        for e in range(20):
            R = (F(3 * e, 5)) % 4
            Uv = min(A * R, C * (4 - R)) - F(D, 4)
            if Uv >= e:
                cand = e + 20 * floor((Uv - e) / 20)
                if best is None or cand > best[0]: best = (cand, e)
        say(f"  {S}->{T}: s0={sd['s0']} D={D} k={k} sel={sd['sel']} M={M} window=({lo},{hi}) "
            f"last missed (brute) {last}, (residue formula) {best}; generic bound E>{w*sd['v']*M-F(D,k)}")
        check((D, M, lo, hi, last) == (D_c, M_c, F(-1, A_c), F(1, C_c), last_c) and best[0] == last_c,
              f"rank 18 {T}: D, M, window, last missed E match note")
        res[S, T] = (sd, lo, hi)
    return res


def all_pairs(name, rows, marks, pairs, a, w, mouth, capd, L0, upper, E, reaim_seeds):
    """Witness for every lattice pair of the room with row 1 stretched to 1+E."""
    cells = cells_of(inserted(rows, E))
    allm = marks_of(inserted(rows, E))
    H = 2 + E
    new = [(a + 1, y) for y in range(2, H)]
    capm = [L0] + new
    up2 = [shift(U, E) for U in upper]
    assert sorted(allm) == sorted(capm + up2)
    lit, kinds, rays, persist_bad = 0, {}, 0, 0
    npairs = 0
    unlit = []
    # cap-cap: vertical segment
    for i in range(len(capm)):
        for jj in range(i + 1, len(capm)):
            A_, B_ = capm[i], capm[jj]
            r = trace(cells, A_, (0, 1), B_[1] - A_[1])
            npairs += 1; rays += 1
            if reached(r, B_): lit += 1; kinds['cap-cap direct'] = kinds.get('cap-cap direct', 0) + 1
            else: unlit.append((A_, B_))
    # cap-upper: note's two-leg construction
    for U in upper:
        cd = capd[U]; U2 = shift(U, E)
        sx, sy = (1 if cd['d'][0] > 0 else -1), (1 if cd['d'][1] > 0 else -1)
        for Tg in capm:
            y = Tg[1]
            npairs += 1
            got = None
            for kind, Lax in (('direct', cd['D1'] + H - y), ('floor', cd['D1'] + H + y)):
                for n in range(floor(cd['lo'] * Lax), ceil(cd['hi'] * Lax) + 1):
                    if not (cd['lo'] < F(n, Lax) < cd['hi']): continue
                    pp, qq, g = prim(n, Lax)
                    r = trace(cells, U2, (sx * pp, sy * qq), g, levels=True)
                    rays += 1
                    # persistence: first level-H visit in the mouth at axial D1, no corner before
                    ent = [e for e in r['lv'] if e[3] == H and mouth[0] < e[1] < mouth[1]]
                    if not ent or ent[0][0] != cd['D1']:
                        persist_bad += 1
                    if reached(r, Tg) and got is None:
                        got = kind
                        # direct leg must not touch the floor; floor leg must touch once
                        if kind == 'direct': assert all(e[3] > 0 for e in r['lv'])
            if got: lit += 1; kinds['cap-upper ' + got] = kinds.get('cap-upper ' + got, 0) + 1
            else: unlit.append((U2, Tg))
    # upper-upper
    for i in range(len(upper)):
        for jj in range(i + 1, len(upper)):
            S, T = upper[i], upper[jj]
            p, q, m = pairs[S, T]
            S2, T2 = shift(S, E), shift(T, E)
            npairs += 1
            if (S, T) not in reaim_seeds:
                r = trace(cells, S2, (p, q), m); rays += 1
                if reached(r, T2): lit += 1; kinds['upper-upper replay'] = kinds.get('upper-upper replay', 0) + 1
                else: unlit.append((S2, T2))
                continue
            sd, lo, hi = reaim_seeds[S, T]
            N0 = floor(E * sd['s0'] / (2 * w))
            got = False
            for N in (N0, N0 + 1):
                s, dl = reaim(sd, w, E, N)
                if not (lo < dl < hi): continue
                r = trace_reaimed(cells, S2, T2, (p, q), s, sd['D'], sd['k'], E); rays += 1
                if reached(r, T2): got = (N, s); break
            if got: lit += 1; kinds['upper-upper re-aim'] = kinds.get('upper-upper re-aim', 0) + 1
            else: unlit.append((S2, T2))
    say(f"  {name} E={E} area {sum(bin(r).count('1') for r in inserted(rows, E))}: "
        f"{lit}/{npairs} pairs lit, rays {rays}, persistence failures {persist_bad}, kinds {kinds}, "
        f"unlit {unlit[:4]}  cpu {time.process_time()-T0:.1f}s")
    check(lit == npairs and len(allm) * (len(allm) - 1) // 2 == npairs and persist_bad == 0,
          f"{name} E={E}: every lattice pair lit by the note's constructions; window rays persist")


def search_pair(cells, S, T, area, bound=40):
    for s_ in range(1, bound + 1):
        for (p, q) in [(x, s_ - x) for x in range(s_, -1, -1) if gcd(x, s_ - x) == 1]:
            for sx, sy in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
                if (p == 0 and sx < 0) or (q == 0 and sy < 0): continue
                r = trace(cells, S, (sx * p, sy * q), 4 * area, T=T, stop_at_T=True)
                if r['hit'] is not None and (r['ok'] or r['corner'][2] > r['hit']):
                    return (sx * p, sy * q, r['hit'])
    return None


def small_E_rank11(rows, marks, pairs, capd, L0, upper, w):
    say("\n=== Claim 5b: rank 11 at E=1..6 (areas 23..33), every lattice pair")
    allok = True
    for E in range(1, 7):
        R = inserted(rows, E)
        cells = cells_of(R)
        area = sum(bin(r).count('1') for r in R)
        ms = marks_of(R)
        res, maxsteps, cons = [], 0, 0
        H = 2 + E
        up2 = {shift(U, E): U for U in upper}
        for i in range(len(ms)):
            for jj in range(i + 1, len(ms)):
                S, T = ms[i], ms[jj]
                wit = None
                # note's constructions first: cap-cap vertical, cap-upper window, upper-upper replay
                if S[0] == T[0] == 1 and max(S[1], T[1]) < H:
                    wit = (0, 1, T[1] - S[1])
                elif T in up2 and S[1] < H:
                    cd = capd[up2[T]]
                    sx, sy = (1 if cd['d'][0] > 0 else -1), (1 if cd['d'][1] > 0 else -1)
                    for Lax in (cd['D1'] + H - S[1], cd['D1'] + H + S[1]):
                        for n in range(floor(cd['lo'] * Lax), ceil(cd['hi'] * Lax) + 1):
                            if wit or not (cd['lo'] < F(n, Lax) < cd['hi']): continue
                            pp, qq, g = prim(n, Lax)
                            if reached(trace(cells, T, (sx * pp, sy * qq), g), S):
                                wit = (sx * pp, sy * qq, g); cons += 1
                    if wit:  # orient from S to T for the re-verification below
                        S, T = T, S
                elif S in up2 and T in up2:
                    p, q, m = pairs[up2[S], up2[T]]
                    if reached(trace(cells, S, (p, q), m), T): wit = (p, q, m)
                if wit is None:
                    wit = search_pair(cells, S, T, area)
                res.append(wit is not None)
                if wit:
                    maxsteps = max(maxsteps, wit[2])
                    # re-verify the witness as a full exact trace ending at T
                    r = trace(cells, S, (wit[0], wit[1]), int(wit[2]))
                    assert reached(r, T)
        n_ok = sum(res)
        allok &= n_ok == len(res)
        say(f"  E={E} area={area} marks={len(ms)} pairs lit {n_ok}/{len(res)}, cap-window witnesses {cons}, max steps {maxsteps}"
            f" (4*area={4*area})  cpu {time.process_time()-T0:.1f}s")
    check(allok, "rank 11 lattice-lit at every E=1..6")


def claim6(rows_list):
    say("\n=== Claim 6: lattice states on the four-sheet surface")
    for name, rows in rows_list:
        c = cells_of(rows); area = len(c)
        pts = {(x, y) for (cx, cy) in c for x in (cx, cx + 1) for y in (cy, cy + 1)}
        st = 0; refl = 0
        for (x, y) in pts:
            n = sum(((x - 1, y - 1) in c, (x, y - 1) in c, (x - 1, y) in c, (x, y) in c))
            if n == 4: st += 4
            elif n == 2: st += 2
            elif n == 3: refl += 1
        say(f"  {name}: area {area}, nonsingular non-corner lattice states {st}, reflex corners {refl}, "
            f"4*area-2r = {4*area-2*refl}")
        check(st <= 4 * area, f"{name}: states <= 4*area")


def main():
    claim1_algebra()
    r11 = room_setup("rank 11", 48, 1156563)
    r18 = room_setup("rank 18", 21, 4136869)
    rows11, marks11, pairs11 = r11
    rows18, marks18, pairs18 = r18

    claim1_measured("rank 11", rows11, pairs11, 2, list(range(1, 61)))
    claim1_measured("rank 18", rows18, pairs18, 2, list(range(1, 161)))
    claim2_break(rows18, pairs18, 2)

    L011, up11, cap11 = cap_data("rank 11", rows11, marks11, pairs11, 0, 2, (0, 1), {
        (4, 3): (F(7, 4), 3, F(5, 3), F(2), 5), (3, 6): (F(24, 5), 4, F(19, 4), F(5), 7)})
    L018, up18, cap18 = cap_data("rank 18", rows18, marks18, pairs18, 1, 2, (2, 3), {
        (3, 3): (F(1, 2), 1, F(0), F(1), 1), (1, 5): (F(3, 8), 15, F(4, 11), F(5, 13), 127),
        (4, 6): (F(14, 9), 8, F(3, 2), F(11, 7), 33), (5, 6): (F(23, 5), 12, F(55, 12), F(37, 8), 59)})
    rs18 = window_table(rows18, pairs18, 2, {(1, 5): (20, 9, 35, 40, 57), (4, 6): (35, 18, 85, 90, 150)})
    # which upper-upper seeds cross the cut
    for name, rows, marks, pairs, up in (("rank 11", rows11, marks11, pairs11, up11),
                                         ("rank 18", rows18, marks18, pairs18, up18)):
        cr = []
        for i in range(len(up)):
            for jj in range(i + 1, len(up)):
                sd = seed_data(cells_of(rows), up[i], up[jj], pairs[up[i], up[jj]][:2], pairs[up[i], up[jj]][2])
                cr.append((up[i], up[jj], sd['k']))
        say(f"  {name} upper-upper seeds (S,T,k): {cr}")

    say("\n=== Claim 5: all pairs at named lengths")
    for E in (7, 8, 9, 10, 13):
        all_pairs("rank 11", rows11, marks11, pairs11, 0, 2, (0, 1), cap11, L011, up11, E, {})
    for E in (151, 152, 157):
        all_pairs("rank 18", rows18, marks18, pairs18, 1, 2, (2, 3), cap18, L018, up18, E, rs18)
    small_E_rank11(rows11, marks11, pairs11, cap11, L011, up11, 2)
    claim6([("rank 11", rows11), ("rank 18", rows18)])
    say(f"\nFAILS: {FAILS}\nTOTAL CPU {time.process_time()-T0:.1f}s")


if __name__ == '__main__':
    main()
