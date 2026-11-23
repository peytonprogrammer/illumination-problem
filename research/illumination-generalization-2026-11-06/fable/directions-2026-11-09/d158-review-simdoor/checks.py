"""d158 referee checks for simultaneous-door-fractions (snapshot 2026-11-22 04:20).

Exact rational arithmetic only. Tracer and cell->polygon builder copied from
d157-review-doorway/checks.py (every vertex, convex or reflex, stops the ray).
Named rooms only: the normalized 12-wall dumbbell with corridor length L
(cells [0,5]x[0,5], [5,5+L]x[2,3], [5+L,10+L]x[0,5]) for L = 12, 22, 32, and R22
(15 manuscript cells). Shot enumerations are over directions in a fixed room.
Run: python3 -B checks.py > checks.log
"""
from fractions import Fraction as F
from math import floor
import time

T0 = time.process_time()


def log(*a):
    print(*a, flush=True)


# ------------------------------------------------------------ copied from d157
def cells_rect(a, b, c, d):
    return {(x, y) for x in range(a, b) for y in range(c, d)}


def polygon(cells):
    E = {}
    for x, y in cells:
        if (x, y - 1) not in cells: E[(x, y)] = (x + 1, y)
        if (x + 1, y) not in cells: E[(x + 1, y)] = (x + 1, y + 1)
        if (x, y + 1) not in cells: E[(x + 1, y + 1)] = (x, y + 1)
        if (x - 1, y) not in cells: E[(x, y + 1)] = (x, y)
    s = min(E)
    pts, p = [s], E[s]
    while p != s:
        pts.append(p); p = E[p]
    n = len(pts)
    V = []
    for i in range(n):
        a, b, c = pts[i - 1], pts[i], pts[(i + 1) % n]
        if (b[0] - a[0], b[1] - a[1]) != (c[0] - b[0], c[1] - b[1]):
            V.append(b)
    assert len(E) == n, "not strictly simple"
    return V


def interior(cells, pt):
    x, y = pt
    return all(c in cells for c in ((x - 1, y - 1), (x, y - 1), (x - 1, y), (x, y)))


def trace(P, S, d, targets=(), maxrefl=10 ** 5):
    """Exact shot from lattice point S, integer direction d=(p,q), p,q != 0."""
    p, q = d
    assert p and q
    kx, ky = abs(q), abs(p)
    V = [(kx * x, ky * y) for x, y in P]
    n = len(V)
    hw = [(V[i], V[(i + 1) % n]) for i in range(n) if V[i][1] == V[(i + 1) % n][1]]
    vw = [(V[i], V[(i + 1) % n]) for i in range(n) if V[i][0] == V[(i + 1) % n][0]]
    vset = set(V)
    tg = {(kx * t[0], ky * t[1]): t for t in targets}
    X, Y = kx * S[0], ky * S[1]
    sx, sy = (1 if p > 0 else -1), (1 if q > 0 else -1)
    poly = [(F(X, kx), F(Y, ky))]
    bounces = []
    for refl in range(maxrefl + 1):
        best = None
        for a, b in vw:
            t = (a[0] - X) * sx
            if t > 0 and (best is None or t < best[0]) and min(a[1], b[1]) <= Y + sy * t <= max(a[1], b[1]):
                best = (t, 'v')
        for a, b in hw:
            t = (a[1] - Y) * sy
            if t > 0 and (best is None or t < best[0]) and min(a[0], b[0]) <= X + sx * t <= max(a[0], b[0]):
                best = (t, 'h')
        t, kind = best
        for Z, name in tg.items():
            tz = (Z[0] - X) * sx
            if 0 < tz <= t and (Z[1] - Y) * sy == tz:
                poly.append((F(Z[0], kx), F(Z[1], ky)))
                return dict(event='target', refl=refl, poly=poly, bounces=bounces)
        X, Y = X + sx * t, Y + sy * t
        poly.append((F(X, kx), F(Y, ky)))
        if (X, Y) in vset:
            return dict(event='corner', stop=poly[-1], refl=refl, poly=poly, bounces=bounces)
        if refl == maxrefl:
            break
        bounces.append((poly[-1], kind))
        if kind == 'v': sx = -sx
        else: sy = -sy
    return dict(event='limit', refl=maxrefl, poly=poly, bounces=bounces)


# ------------------------------------------------------------ helpers
def point_at_travel(poly, axis, t):
    """Physical point after cumulative travel t along coordinate `axis` (None if beyond poly)."""
    acc = F(0)
    for A, B in zip(poly, poly[1:]):
        seg = abs(B[axis] - A[axis])
        if acc + seg >= t:
            lam = (t - acc) / seg
            return (A[0] + lam * (B[0] - A[0]), A[1] + lam * (B[1] - A[1]))
        acc += seg
    return None


def total_travel(poly, axis):
    return sum(abs(B[axis] - A[axis]) for A, B in zip(poly, poly[1:]))


def fold(u, lo, hi):
    """Fold the real line onto [lo,hi] with period 2(hi-lo); returns (position, sheet sign)."""
    w = hi - lo
    r = (u - lo) % (2 * w)
    return (lo + r, 1) if r <= w else (lo + 2 * w - r, -1)


def reduce_dir(a, b):
    from math import gcd
    g = gcd(a, b)
    return (a // g, b // g)


# ================================================================== 1. dumbbell
log("# 1. Dumbbell: chambers [0,5]^2 and [5+L,10+L]x[0,5], corridor 2<y<3; S=(4,1), T=(6+L,3)")
for L in (12, 22, 32):
    D = L + 2
    cells = cells_rect(0, 5, 0, 5) | cells_rect(5, 5 + L, 2, 3) | cells_rect(5 + L, 10 + L, 0, 5)
    P = polygon(cells)
    S, T = (4, 1), (6 + L, 3)
    log(f"\n## L={L}, D={D}: walls={len(P)}, S interior={interior(cells, S)}, T interior={interior(cells, T)}")

    # 1a. positive-sheet placement identity: s=(2+10a+2b+10c)/D, h1=1+s-10a, h2=3+10c-s
    H1, H2, sums = set(), set(), set()
    for a in range(-3, 4):
        for b in range(-3 * D, 3 * D):
            for c in range(-3, 4):
                s = F(2 + 10 * a + 2 * b + 10 * c, D)
                h1, h2 = 1 + s - 10 * a, 3 + 10 * c - s
                sums.add((h1 + h2) % 10)
                if 2 < h1 % 10 < 3: H1.add(h1 % 10)
                if 2 < h2 % 10 < 3: H2.add(h2 % 10)
    gaps = lambda H: sorted({y - x for x, y in zip(sorted(H), sorted(H)[1:])})
    log(f"   positive sheets: (h1+h2) mod 10 = {sorted(sums)}; door-1 positions in (2,3): {len(H1)}, gaps {gaps(H1)};"
        f" door-2 positions: {len(H2)}, gaps {gaps(H2)}  (2/D = {F(2, D)})")

    # 1b. exact disjointness of the two one-unit-leg slope sets, all signs, via unit-interval midpoints
    def legset(y0):
        out = []
        for n in range(10):
            m = F(2 * n + 1, 2)
            if any(2 < fold(y0 + e * m, 0, 5)[0] < 3 for e in (1, -1)):
                out.append(n)
        return out
    A1, A3 = legset(1), legset(3)
    log(f"   |s| mod 10 lower ends: from height 1 {A1}, from height 3 {A3}, intersection {sorted(set(A1) & set(A3))}")

    # 1c. exhaustive rightward-monotone shots S->T: s in (1/D)Z, s mod 10 covered (|k| <= 10D)
    mono_hits, any_hits, door1_ok = [], 0, 0
    for k in range(-10 * D, 10 * D + 1):
        if k == 0:
            continue
        p, q = reduce_dir(D, k)
        r = trace(P, S, (p, q), targets=(T,), maxrefl=abs(k) + 20)
        if not any(kind == 'v' for _, kind in r['bounces']) and r['event'] == 'target':
            mono_hits.append(k)
        # does it legally clear door 1 (first point at x=5 inside the window)?
        pt = point_at_travel(r['poly'], 0, 1)
        if pt is not None and pt[0] == 5 and 2 < pt[1] < 3:
            door1_ok += 1
    log(f"   monotone shots tested: {20 * D}; monotone S->T hits: {mono_hits} (expect none); "
        f"slopes clearing door 1: {door1_ok}")

    # 1d. repair: one far-cap reflection, s in (2/(L+10))Z with 10/9 < s < 11/9
    ks = [k for k in range(0, 3 * (L + 10)) if F(10, 9) < F(2 * k, L + 10) < F(11, 9)]
    for k in ks:
        s = F(2 * k, L + 10)
        p, q = reduce_dir(s.denominator, s.numerator)
        r = trace(P, S, (p, q), targets=(T,), maxrefl=400)
        vb = [pt for pt, kind in r['bounces'] if kind == 'v']
        d1 = point_at_travel(r['poly'], 0, 1)
        d2 = point_at_travel(r['poly'], 0, 1 + L)
        log(f"   repair s={s}: event={r['event']}, refl={r['refl']}, vertical bounces={vb}, "
            f"door1 y={d1[1]}, door2 y={d2[1]} (note: 1+s={1 + s}, 13-9s={13 - 9 * s}), cap y=3-4s folded={fold(3 - 4 * s, 0, 5)[0]}")

# ================================================================== 2. R22
log("\n# 2. R22: S=(0,0), T=(2,2); word = bottom/top solid contacts at t=1,3,..,D-3, top opening at D-1, T at D")
R22c = {(-1, -1), (-1, 0), (0, -2), (0, -1), (0, 0), (0, 1), (1, -3), (1, -2), (1, 1), (1, 2), (2, 1), (2, 2),
        (3, 0), (3, 1), (4, 0)}
PR = polygon(R22c)
S, T = (0, 0), (2, 2)
log(f"   R22 walls={len(PR)}, S interior={interior(R22c, S)}, T interior={interior(R22c, T)}")
log(f"   y=1 openings: {[x for x in range(-1, 1) if (x, 0) in R22c and (x, 1) in R22c]} ; "
    f"y=-1 openings: {[x for x in range(-1, 1) if (x, -1) in R22c and (x, -2) in R22c]} (cell x index)")
log(f"   upper run cells y in [1,2]: {sorted(c for c in R22c if c[1] == 1)}")


def word_status(r, D):
    """Return ('prefix-fail', j) or ('prefix-ok', point at D-1, point at D, hitT)."""
    poly = r['poly']
    for j in range(1, D - 2, 2):
        pt = point_at_travel(poly, 1, j)
        want = -1 if j % 4 == 1 else 1
        if pt is None or pt[1] != want or not (-1 < pt[0] < 0):
            return ('prefix-fail', j)
    pt = point_at_travel(poly, 1, D - 1)
    if pt is None or pt[1] != 1 or not (0 < pt[0] < 1):
        return ('prefix-fail', D - 1)
    end = point_at_travel(poly, 1, D)
    hit = r['event'] == 'target' and total_travel(poly, 1) == D
    return ('prefix-ok', pt, end, hit)


for m in (3, 4, 5):
    D = 2 ** m
    log(f"\n## m={m}, D={D}")
    # 2a. the prescribed launch s0 = -4/(2D-3), plus two nearby slopes
    s0 = F(-4, 2 * D - 3)
    for s in (s0, s0 + F(1, 1000 * D), s0 - F(1, 1000 * D)):
        p, q = reduce_dir(s.numerator, -s.denominator)  # downward: dy<0, dx = s*|dy|
        p, q = -abs(p) if s < 0 else abs(p), -abs(q)
        r = trace(PR, S, (p, q), targets=(T,), maxrefl=4 * D)
        st = word_status(r, D)
        tag = 's0' if s == s0 else 's0+-eps'
        if st[0] == 'prefix-ok':
            log(f"   {tag} s={s}: prefix legal; x at D-1 = {st[1][0]} (claim 2/(2D-3)={F(2, 2 * D - 3)}), "
                f"point at D = {st[2]}, hits T = {st[3]}")
        else:
            log(f"   {tag} s={s}: prefix fails at t={st[1]}")
    tw = F(2 * D - 3, 4)
    log(f"   s0 lateral-wall time (2D-3)/4 = {tw} (integer: {tw.denominator == 1}); x=0 recrossing time "
        f"{2 * tw} = D-3/2: {2 * tw == D - F(3, 2)}")
    # 2b. exhaustive: every shot that can reach T at vertical travel D has s in (1/D)Z; s mod 8 suffices
    n_prefix, n_hitD, n_word_hit, n_positive, n_negative = 0, 0, 0, 0, 0
    for k in range(-8 * D, 8 * D + 1):
        if k == 0:
            continue  # vertical shot hits the corner (0,-1) at t=1
        s = F(k, D)
        p, q = reduce_dir(abs(k), D)
        p = p if k > 0 else -p
        r = trace(PR, S, (p, -q), targets=(T,), maxrefl=abs(k) + 2 * D + 10)
        if r['event'] == 'target' and total_travel(r['poly'], 1) == D:
            n_hitD += 1
        st = word_status(r, D)
        if st[0] == 'prefix-ok':
            n_prefix += 1
            n_word_hit += st[3]
            # which sign case would the note's argument use?
            z, sg = fold((D - 1) * s, -1, 1)
            if sg > 0: n_positive += 1
            else: n_negative += 1
            # sign-case consistency: positive needs Ds = 2 mod 4, negative Ds = 0 mod 4
    log(f"   slopes s=k/D, 0<|k|<=8D: {16 * D}; follow word prefix: {n_prefix} "
        f"(positive sheet at D-1: {n_positive}, negative: {n_negative}); reach T at vertical travel D by any route: {n_hitD}; "
        f"follow word AND reach T: {n_word_hit} (expect 0)")
    # 2c. sign-argument algebra on the candidate lattice: for s in (2/D)Z (necessary for T), check the
    # paired-visit contradiction directly
    bad = 0
    for k in range(-4 * D, 4 * D):
        s = F(2 * k, D)
        z, sg = fold((D - 1) * s, -1, 1)
        if not (0 < z < 1):
            continue
        tail = (z + sg * s) % 4
        if tail != 2:
            continue  # misses T images +-2 mod 8
        if sg > 0:
            ok = not (-1 < fold(s, -1, 1)[0] < 0)          # visit 1 must be negative but equals z
        else:
            a3, b3 = fold(3 * s, -1, 1)[0], fold((D - 3) * s, -1, 1)[0]
            ok = not (-1 < a3 < 0 and -1 < b3 < 0)          # visits 3 and D-3 opposite
        bad += not ok
    log(f"   candidates s in (2/D)Z with legal last crossing and tail on a T image that escape both sign "
        f"contradictions: {bad} (expect 0)")

# 2d. the argument does not use D = 2^m: repeat 2b for D = 12, 20 (D = 0 mod 4, not dyadic)
log("\n## non-dyadic D = 0 mod 4 (does the sign argument use 2^m?)")
for D in (12, 20):
    n_prefix = n_word_hit = 0
    for k in range(-8 * D, 8 * D + 1):
        if k == 0:
            continue
        p, q = reduce_dir(abs(k), D)
        p = p if k > 0 else -p
        r = trace(PR, S, (p, -q), targets=(T,), maxrefl=abs(k) + 2 * D + 10)
        st = word_status(r, D)
        if st[0] == 'prefix-ok':
            n_prefix += 1; n_word_hit += st[3]
    log(f"   D={D}: follow word prefix {n_prefix}; follow word AND reach T {n_word_hit}")

# 2e. extent of the near-s0 prefix branch: claimed s in -(2/(D-1), 2/(D-3)) minus the corner slope -2/(D-2)
log("\n## near-s0 prefix branch endpoints (reviewer derivation)")
for D in (8, 16):
    for s, lab in ((F(-2, D - 2), "-2/(D-2)"), (F(-2, D - 1), "-2/(D-1)"), (F(-2, D - 3), "-2/(D-3)"),
                   (F(-2, D - 1) - F(1, 10 ** 4), "just inside -2/(D-1)"), (F(-2, D - 3) + F(1, 10 ** 4), "just inside -2/(D-3)")):
        p, q = reduce_dir(-s.numerator, s.denominator)
        r = trace(PR, S, (-p, -q), targets=(T,), maxrefl=4 * D)
        st = word_status(r, D)
        log(f"   D={D} s={lab}={s}: event={r['event']}{' at ' + str(r.get('stop')) if r['event']=='corner' else ''}, word={st[0]}{'' if st[0]=='prefix-ok' else ' at t=' + str(st[1])}")

log(f"\nCPU seconds: {time.process_time() - T0:.1f}")
