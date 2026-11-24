"""Independent checks for the d211 general-collar note.

Run: nice -n 10 python3 -B checks.py
Rooms are sets of unit cells (x, y) = [x, x+1] x [y, y+1]; y is depth (down).
The tracer is exact: integer arithmetic in coordinates scaled by |q| (x) and
|p| (y), so every step moves one unit in each scaled axis.
"""
import json, math, os, sys, time
from fractions import Fraction as F
from math import gcd, ceil, floor

HERE = os.path.dirname(os.path.abspath(__file__))
PATHS = os.path.join(HERE, "..", "seed-profile-a21", "paths.json")
OUT = []


def say(*a):
    s = " ".join(str(x) for x in a)
    OUT.append(s)
    print(s, flush=True)


# ---------------------------------------------------------------- rooms
def strictly_simple(cells):
    cells = set(cells)
    xs = [c[0] for c in cells]; ys = [c[1] for c in cells]
    x0, x1, y0, y1 = min(xs) - 1, max(xs) + 1, min(ys) - 1, max(ys) + 1
    # connected
    st = [next(iter(cells))]; seen = {st[0]}
    while st:
        x, y = st.pop()
        for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if n in cells and n not in seen:
                seen.add(n); st.append(n)
    if len(seen) != len(cells):
        return False
    # complement connected (no holes)
    out = {(x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)} - cells
    st = [(x0, y0)]; seen = {st[0]}
    while st:
        x, y = st.pop()
        for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if n in out and n not in seen:
                seen.add(n); st.append(n)
    if len(seen) != len(out):
        return False
    # no diagonal pinch
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            a, b, c, d = (x - 1, y - 1) in cells, (x, y - 1) in cells, (x - 1, y) in cells, (x, y) in cells
            if (a and d and not b and not c) or (b and c and not a and not d):
                return False
    return True


def marks(cells):
    pts = set()
    for (x, y) in cells:
        for (u, v) in ((x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)):
            if all(c in cells for c in ((u - 1, v - 1), (u, v - 1), (u - 1, v), (u, v))):
                pts.add((u, v))
    return pts


# ---------------------------------------------------------------- tracer
def trace(cells, S, p, q, T, maxev=10 ** 6):
    """Return ('hit', axial_travel, transverse_travel) or ('corner', pt) / ('wall', pt) / ('timeout',)."""
    g = gcd(abs(p), abs(q)); p //= g; q //= g
    qx = abs(q) if q else 1
    py = abs(p) if p else 1
    X, Y = S[0] * qx, S[1] * py
    dX = (p > 0) - (p < 0); dY = (q > 0) - (q < 0)
    tx, ty = T[0] * qx, T[1] * py
    ticks = 0
    for _ in range(maxev):
        if dX:
            r = X % qx
            a = (qx - r) if dX > 0 else (r if r else qx)
        else:
            a = None
        if dY:
            r = Y % py
            b = (py - r) if dY > 0 else (r if r else py)
        else:
            b = None
        k = a if b is None else (b if a is None else min(a, b))
        X += dX * k; Y += dY * k; ticks += k
        onV = X % qx == 0; onH = Y % py == 0
        if onV and onH:
            x, y = X // qx, Y // py
            if (X, Y) == (tx, ty):
                return ('hit', F(ticks, py) if q else 0, F(ticks, qx) if p else 0)
            c00 = (x - 1, y - 1) in cells; c10 = (x, y - 1) in cells
            c01 = (x - 1, y) in cells; c11 = (x, y) in cells
            n = c00 + c10 + c01 + c11
            if n == 4:
                continue
            if n == 2 and c00 and c10 and dY:      # wall below, room above
                if dY > 0: dY = -dY
                else: return ('corner', (x, y))
            elif n == 2 and c01 and c11 and dY:    # wall above
                if dY < 0: dY = -dY
                else: return ('corner', (x, y))
            elif n == 2 and c00 and c01 and dX:    # wall right
                if dX > 0: dX = -dX
                else: return ('corner', (x, y))
            elif n == 2 and c10 and c11 and dX:    # wall left
                if dX < 0: dX = -dX
                else: return ('corner', (x, y))
            else:
                return ('corner', (x, y))
        elif onV:
            x = X // qx; j = Y // py
            nxt = (x, j) if dX > 0 else (x - 1, j)
            if nxt not in cells:
                dX = -dX
        else:
            y = Y // py; i = X // qx
            nxt = (i, y) if dY > 0 else (i, y - 1)
            if nxt not in cells:
                dY = -dY
    return ('timeout',)


# ---------------------------------------------------------------- (A) rooms
def upper_A(a, w):
    c = set()
    for x in range(a - 1, a + w + 1): c.add((x, -1))
    for x in range(a, a + w + 2): c.add((x, -2))
    for x in range(a + 1, a + w + 2): c.add((x, -3))
    return c


def foot_stepped(a, w):        # column a+j has first-wall depth j+2; column a-1 depth 1
    c = set()
    for k in range(0, w + 2):
        for x in range(max(a - 1, a + k - 1), a + w + 1):
            c.add((x, k))
    return c


def foot_overhang(a, w):       # mouth columns closed on the left, room continues under them
    c = set()
    lo = a + 2 if w >= 4 else a + 1
    for k in (0, 1):
        for x in range(lo, a + w + 2): c.add((x, k))
    for k in (2, 3):
        for x in range(a - 3, a + w + 2): c.add((x, k))
    for x in range(a + w - 1, a + w + 2): c.add((x, 4))
    return c


def foot_notch(a, w):          # two floor notches of depth 2 and 1
    c = set()
    for k in range(4):
        for x in range(a - 1, a + w + 1): c.add((x, k))
    c.discard((a + 1, 2)); c.discard((a + 1, 3)); c.discard((a + w - 1, 3))
    return c


def build(upper, foot_rel, a, w, L):
    cells = set(upper)
    for x in range(a, a + w):
        for y in range(L): cells.add((x, y))
    for (x, k) in foot_rel: cells.add((x, L + k))
    return cells


def first_depth(cells, c, L):
    h = 0
    while (c, L + h) in cells: h += 1
    return h


def vertical_entry(cells, S, a, w, dirn):
    """D for a regular vertical first entry into the open mouth, or None."""
    x0, y = S
    if not (a < x0 < a + w): return None
    D = 0
    for _ in range(1000):
        y += dirn; D += 1
        if y == 0 and dirn > 0:
            ok = all(c in cells for c in ((x0 - 1, -1), (x0, -1), (x0 - 1, 0), (x0, 0)))
            return D if ok else None
        c = [(x0 - 1, y - 1) in cells, (x0, y - 1) in cells, (x0 - 1, y) in cells, (x0, y) in cells]
        if all(c): continue
        if c == [True, True, False, False] and dirn > 0: dirn = -1; continue
        if c == [False, False, True, True] and dirn < 0: dirn = 1; continue
        return None
    return None


def collar_dir(cells, a, w, L, H, x0, D, dirn, x, d, tie='right', wrong_side=False):
    """Note's construction. Returns (p, q, predicted axial travel, info)."""
    d0 = w * (D + 1)
    if x == x0: return 0, dirn, D + d, 'vert'
    if d >= d0: return x - x0, dirn * (D + d), D + d, 'deep'
    m2 = x0 + x
    if m2 % 2:
        c = (m2 - 1) // 2; h = first_depth(cells, c, L); sig = 1 if x > x0 else -1
        n = 0
    else:
        m = m2 // 2
        hl = first_depth(cells, m - 1, L); hr = first_depth(cells, m, L)
        if hl < hr or (hl == hr and tie == 'left'): sig, h = -1, hl
        else: sig, h = 1, hr
        if wrong_side:
            sig, h = (1, hr) if sig == -1 else (-1, hl)
        n = 0
    for n in (0, 1, -1):
        Dl = x - x0 + 4 * n * w
        if Dl != 0 and (Dl > 0) == (sig > 0) and abs(Dl) < 4 * w: break
    else:
        raise RuntimeError
    den = D + 2 * L + 2 * h - d
    return Dl, dirn * den, den, ('half' if m2 % 2 else 'int')


def run_A(name, foot_fn, a, w, Ls, tag, full=True, extra=False):
    upper = upper_A(a, w)
    res = []
    for L in Ls:
        footr = foot_fn(a, w)
        H = max(k for (_, k) in footr) + 1
        cells = build(upper, footr, a, w, L)
        assert strictly_simple(cells), name
        srcs = []
        for (sx, sy) in sorted(marks(cells)):
            if sy < 0:
                for dirn in (1, -1):
                    D = vertical_entry(cells, (sx, sy), a, w, dirn)
                    if D: srcs.append(((sx, sy), dirn, D))
        yield L, H, cells, srcs


def A_checks():
    say("\n=== (A) collar theorem: hand-made feet ===")
    a = 3
    feet = [("stepped", foot_stepped), ("overhang", foot_overhang), ("notch", foot_notch)]
    total = {'traced': 0, 'fail': 0, 'travel_mismatch': 0, 'kinds': {}}
    below = []
    for fname, ff in feet:
        for w in (2, 3, 4, 5):
            footr = ff(a, w)
            H = max(k for (_, k) in footr) + 1
            cols = [first_depth(build(upper_A(a, w), footr, a, w, 10), c, 10) for c in range(a, a + w)]
            # sources and D at a dummy length (upper part and mouth do not depend on L)
            cells10 = build(upper_A(a, w), footr, a, w, 10)
            srcs = []
            for (sx, sy) in sorted(marks(cells10)):
                if sy < 0:
                    for dirn in (1, -1):
                        D = vertical_entry(cells10, (sx, sy), a, w, dirn)
                        if D: srcs.append(((sx, sy), dirn, D))
            if w == 5:   # w = 5 only as an extra integral-midpoint case; keep the smallest-D sources
                srcs = [s for s in srcs if s[2] <= 2]
            say(f"\n{fname} foot, w={w}, H={H}, strip-column first depths {cols}, "
                f"{len(srcs)} regular vertical sources (S, dir, D): {srcs}")
            for (S, dirn, D) in srcs:
                x0 = S[0]
                d0 = w * (D + 1)
                K = 1 + ceil(4 * w * max(D + 1, D + d0 + 2 * H))
                stats = []
                for L in (K, K + 1):
                    cells = build(upper_A(a, w), footr, a, w, L)
                    assert strictly_simple(cells)
                    nt = nf = 0; kinds = {}
                    for x in range(a + 1, a + w):
                        for d in range(1, L):
                            p, q, ax, kind = collar_dir(cells, a, w, L, H, x0, D, dirn, x, d)
                            r = trace(cells, S, p, q, (x, d), maxev=20 * (ax + 50))
                            nt += 1; kinds[kind] = kinds.get(kind, 0) + 1
                            if r[0] != 'hit':
                                nf += 1; say("  FAIL", fname, w, S, dirn, D, L, (x, d), (p, q), r)
                            elif r[1] != ax:
                                total['travel_mismatch'] += 1
                    total['traced'] += nt; total['fail'] += nf
                    for k_, v in kinds.items(): total['kinds'][k_] = total['kinds'].get(k_, 0) + v
                    stats.append((L, nt, nf))
                say(f"  S={S} dir={dirn:+d} D={D} d0={d0} K={K}: (L, traced, fail) = {stats}")
                # below K: which constructed seeds fail, and the smallest L from which all succeed
                firstbad = None; lastbad = None; badkinds = {}
                Lgrid = sorted(set([2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 30, 40, 60] +
                                   list(range(max(2, K // 8), K, max(1, K // 40)))))
                for L in [l for l in Lgrid if l < K]:
                    cells = build(upper_A(a, w), footr, a, w, L)
                    bad = 0
                    for x in range(a + 1, a + w):
                        for d in range(1, min(L, d0)):
                            p, q, ax, kind = collar_dir(cells, a, w, L, H, x0, D, dirn, x, d)
                            r = trace(cells, S, p, q, (x, d), maxev=20 * (ax + 50))
                            if r[0] != 'hit':
                                bad += 1
                                badkinds[kind] = badkinds.get(kind, 0) + 1
                                if firstbad is None: firstbad = (L, (x, d), (p, q), r)
                    if bad: lastbad = L
                below.append((fname, w, S, dirn, D, K, lastbad, firstbad, badkinds))
                say(f"    below K (sampled L): largest L with a failing constructed seed = {lastbad}; "
                    f"failing kinds {badkinds}; first failure {firstbad}")
    say(f"\n(A) totals at L=K,K+1: {total}")
    return total, below


def A_wrong_side():
    """Show that the outgoing-side choice at an integral midpoint matters."""
    say("\n=== (A) control: aim into the deeper side at an integral midpoint ===")
    a = 3
    for fname, ff in (("stepped", foot_stepped), ("notch", foot_notch), ("overhang", foot_overhang)):
        for w in (4, 5):
            footr = ff(a, w); H = max(k for (_, k) in footr) + 1
            cells10 = build(upper_A(a, w), footr, a, w, 10)
            S, dirn = None, 1
            for x0 in range(a + 1, a + w):
                D = vertical_entry(cells10, (x0, -1), a, w, 1)
                if D:
                    K = 1 + ceil(4 * w * max(D + 1, D + w * (D + 1) + 2 * H))
                    cells = build(upper_A(a, w), footr, a, w, K)
                    good = badw = tot = 0; ex = None
                    for x in range(a + 1, a + w):
                        if (x - x0) % 2 or x == x0: continue
                        m = (x + x0) // 2
                        hl = first_depth(cells, m - 1, K); hr = first_depth(cells, m, K)
                        if hl == hr: continue
                        for d in range(1, w * (D + 1)):
                            p, q, ax, _ = collar_dir(cells, a, w, K, H, x0, D, 1, x, d, wrong_side=True)
                            r = trace(cells, (x0, -1), p, q, (x, d), maxev=20 * (ax + 50))
                            tot += 1
                            if r[0] != 'hit':
                                badw += 1; ex = ex or ((x, d), (p, q), r)
                    if tot:
                        say(f"  {fname} w={w} S=({x0},-1) L=K={K}: deeper-side seeds failing {badw}/{tot}; example {ex}")


def A_ties():
    say("\n=== (A) tie rule: both choices at equal-depth integral midpoints ===")
    a = 3; n = bad = 0
    for fname, ff in (("stepped", foot_stepped), ("notch", foot_notch), ("overhang", foot_overhang)):
        for w in (4, 5):
            footr = ff(a, w); H = max(k for (_, k) in footr) + 1
            cells10 = build(upper_A(a, w), footr, a, w, 10)
            for x0 in range(a + 1, a + w):
                D = vertical_entry(cells10, (x0, -1), a, w, 1)
                if not D: continue
                K = 1 + ceil(4 * w * max(D + 1, D + w * (D + 1) + 2 * H))
                cells = build(upper_A(a, w), footr, a, w, K)
                for x in range(a + 1, a + w):
                    if (x - x0) % 2 or x == x0: continue
                    m = (x + x0) // 2
                    if first_depth(cells, m - 1, K) != first_depth(cells, m, K): continue
                    for d in range(1, w * (D + 1)):
                        for tie in ('left', 'right'):
                            p, q, ax, _ = collar_dir(cells, a, w, K, H, x0, D, 1, x, d, tie=tie)
                            r = trace(cells, (x0, -1), p, q, (x, d), maxev=20 * (ax + 50))
                            n += 1; bad += r[0] != 'hit'
    say(f"  tie cases traced {n}, failures {bad}")


def A_inequalities():
    say("\n=== (A) exact inequality audit at L = K, K+1 (worst shallow case h = 0, d = d0 - 1) ===")
    worst = (0, 0); n = 0
    for w in range(2, 9):
        for D in range(1, 13):
            for H in range(0, 10):
                d0 = w * (D + 1); K = 1 + ceil(4 * w * max(D + 1, D + d0 + 2 * H))
                for L in (K, K + 1):
                    dmax = min(d0, L) - 1
                    Dmax = max(abs(x - x0 + 4 * nn * w) for x0 in range(1, w) for x in range(1, w)
                               for nn in (0, 1, -1) if 0 < abs(x - x0 + 4 * nn * w) < 4 * w) if w > 2 else 0
                    if not Dmax: continue
                    s = F(Dmax, D + 2 * L - dmax); C = F(D + dmax, 2)
                    assert s < F(4 * w, L) and s * (D + 1) < 1 and s * (C + H) < F(1, 2), (w, D, H, L)
                    assert F((w - 1) * (D + 1), D + d0) < 1
                    worst = max(worst, (float(s * (C + H)), float(s * (D + 1)))); n += 1
    say(f"  {n} parameter cases (w<=8, D<=12, H<=9) pass; max |s|(C+H) = {worst[0]:.4f}, max |s|(D+1) = {worst[1]:.4f}")
    say("  denominator: D+2L+2h-d <= D+2L+2H-1; with D <= 2U and U+L+H <= B_y this is <= 2B_y - 1 (note says 4B_y)")


# ---------------------------------------------------------------- (B)
def B_room(w, A, Lr, foot_rel):
    cells = set()
    for x in range(-3, w + 1):
        for y in range(-A, 0): cells.add((x, y))
    for x in range(w):
        for y in range(Lr): cells.add((x, y))
    for (x, k) in foot_rel: cells.add((x, Lr + k))
    return cells


def B_foot(w):
    # stepped with an overhang: col -2..-1 depth 1, col 0 depth 1, col 1 depth 3, col 2.. depth 2
    c = set()
    for x in range(-2, w + 1): c.add((x, 0))
    for x in range(1, w + 1): c.add((x, 1))
    c.add((1, 2)); c.add((w, 2)); c.add((w, 3))
    return c


def B_params(w, A, H, b, z):
    if b > 0:
        n = 1
        while not (z + 2 * A * n > A + F(A * b, w)): n += 1
        t0 = z + 2 * A * n
        J0 = (F(b, t0), F(b, t0 - A))
    else:
        t0 = z; J0 = (F(0), F(w, 2 * A))
    d1 = floor(2 * w / (J0[1] - J0[0])) + 1
    U = min(F(w, A), F(1, A + d1 + 2 * H))
    if b > 0:
        n = 1
        while not (z + 2 * A * n > A + b / U): n += 1
        t = z + 2 * A * n
        J = (F(b, t), F(b, t - A))
    else:
        t = z; J = (F(0), U / 2)
    Lmin = 1 + ceil(d1 + 2 * w / (J[1] - J[0]))
    return t0, J0, d1, U, t, J, Lmin


def B_seed(cells, w, L, H, b, z, t0, J0, d1, t, J, x, d):
    """Return (p, q) launch direction (right and down) or None."""
    if d >= d1:
        lo = floor((t0 + d) * J0[0]) + 1
        for N in range(max(lo, 1), lo + 2 * w + 1):     # N = v + b, developed target v = N - b
            if ((N - b - x) % (2 * w) == 0 or (N - b + x) % (2 * w) == 0) and J0[0] < F(N, t0 + d) < J0[1]:
                return N, t0 + d, 'deep'
        return None
    i = x; m2 = i
    if m2 % 2:
        sig = 1; h = first_depth(cells, (m2 - 1) // 2, L)
    else:
        m = m2 // 2
        hl = first_depth(cells, m - 1, L); hr = first_depth(cells, m, L)
        sig, h = (-1, hl) if hl < hr else (1, hr)
    den = t + 2 * L + 2 * h - d
    for n in range(-2, 10 ** 6):
        num = sig * i + 4 * w * n + b
        s = F(num, den)
        if s >= J[1]: return None
        if s > J[0]: return num, den, 'shallow'


def B_checks():
    say("\n=== (B) rectangular shoulder ===")
    for (w, A, b, z) in ((3, 2, 0, 1), (4, 3, 0, 2), (3, 2, 1, 1)):
        footr = B_foot(w); H = max(k for (_, k) in footr) + 1
        t0, J0, d1, U, t, J, Lmin = B_params(w, A, H, b, z)
        S = (-b, -z)
        say(f"\n w={w} A={A} H={H} source S={S} (b={b}, z={z}): t0={t0} J0=({J0[0]},{J0[1]}) d1={d1} "
            f"U={U} t={t} J=({J[0]},{J[1]}) L_min={Lmin}")
        for L in (Lmin, Lmin + 1):
            cells = B_room(w, A, L, footr)
            assert strictly_simple(cells)
            assert S in marks(cells)
            depths = list(range(1, L))
            if L > 3000:   # deep targets sampled for the b > 0 case (each is a direct sweep)
                depths = sorted(set(list(range(1, d1 + 120)) + list(range(d1, L, 97)) + list(range(L - 40, L))))
            nt = nf = 0; kinds = {}
            for x in range(1, w):
                for d in depths:
                    sd = B_seed(cells, w, L, H, b, z, t0, J0, d1, t, J, x, d)
                    if sd is None:
                        nf += 1; say("  NO SEED", x, d); continue
                    p, q, kind = sd
                    r = trace(cells, S, p, q, (x, d), maxev=50 * (q + 50))
                    nt += 1; kinds[kind] = kinds.get(kind, 0) + 1
                    if r[0] != 'hit':
                        nf += 1; say("  FAIL", (x, d), (p, q), r)
            say(f"  L={L}: traced {nt} ({kinds}), failures {nf}")
        # below the threshold: shallow seeds only, a few L
        for L in sorted(set([d1 + 1, d1 + 5, (d1 + Lmin) // 4, (d1 + Lmin) // 2])):
            if L >= Lmin or L <= d1: continue
            cells = B_room(w, A, L, footr)
            ns = nb = 0
            for x in range(1, w):
                for d in range(1, d1):
                    sd = B_seed(cells, w, L, H, b, z, t0, J0, d1, t, J, x, d)
                    if sd is None: ns += 1; continue
                    r = trace(cells, S, sd[0], sd[1], (x, d), maxev=50 * (sd[1] + 50))
                    nb += r[0] != 'hit'
            say(f"  below threshold L={L}: shallow targets with no s in J: {ns}; traced seeds failing: {nb}")


# ---------------------------------------------------------------- (C)
def C_checks():
    say("\n=== (C) shear on named rooms ===")
    P = json.load(open(PATHS))
    for e in P:
        if e['rank'] not in (11, 18): continue
        rows = e['rows']
        cells = {(x, y) for y, r in enumerate(rows) for x in range(r.bit_length()) if r >> x & 1}
        assert strictly_simple(cells)
        S = tuple(e['S']); T = tuple(e['T']); p, q = e['direction']
        hs = set()
        for x in {c[0] for c in cells}:
            ys = sorted(y for (xx, y) in cells if xx == x)
            run = 1
            for i in range(1, len(ys) + 1):
                if i < len(ys) and ys[i] == ys[i - 1] + 1: run += 1
                else: hs.add(run); run = 1
        lev = sorted({y for (x, y) in cells} | {y + 1 for (x, y) in cells})
        hw = set()
        for (x, y) in cells:
            if (x, y - 1) not in cells: hw.add(y)
            if (x, y + 1) not in cells: hw.add(y + 1)
        lcm = 1
        for h in hs: lcm = lcm * h // gcd(lcm, h)
        Lam = 2 * lcm
        By = max(y for (_, y) in cells) + 1 - min(y for (_, y) in cells)
        r0 = trace(cells, S, p, q, T)
        say(f"\n rank {e['rank']}: S={S} T={T} stored dir=({p},{q}); slice heights {sorted(hs)}; "
            f"Lambda={Lam}; B_y={By}; horizontal support levels {sorted(hw)}")
        say(f"  stored seed trace: {r0}")
        lam_tr = r0[2] / abs(p) if p else None
        for j in (1, -1, 2, -2, 3):
            q2 = q + j * Lam * p
            assert gcd(p, q2) == 1
            r = trace(cells, S, p, q2, T, maxev=10 ** 7)
            ok = r[0] == 'hit' and r[2] == r0[2]
            say(f"  j={j:+d}: dir ({p},{q2}) -> {r[0]}, transverse travel {r[2] if r[0]=='hit' else '-'} "
                f"(same developed segment: {ok})")
        # control: half of Lambda (shift = h, not 0 mod 2h, for odd multiples)
        for j in (1, -1):
            q2 = q + j * (Lam // 2) * p
            if gcd(p, q2) != 1: continue
            r = trace(cells, S, p, q2, T, maxev=10 ** 7)
            say(f"  control Lambda/2, j={j:+d}: dir ({p},{q2}) -> {r[0] if r[0]!='hit' else ('hit', r[2])}")
        # nearest j bound
        j = round(F(-q, Lam * p))
        say(f"  nearest j = {j}; |q + j Lam p| = {abs(q + j * Lam * p)} <= Lam|p|/2 = {Lam * abs(p) // 2}")


def main():
    t0 = time.process_time()
    parts = sys.argv[1:] or ["ineq", "A", "wrong", "ties", "B", "C"]
    table = {"ineq": A_inequalities, "A": A_checks, "wrong": A_wrong_side, "ties": A_ties,
             "B": B_checks, "C": C_checks}
    for part in parts:
        table[part]()
    say(f"\nCPU seconds: {time.process_time() - t0:.1f}")


if __name__ == "__main__":
    main()
