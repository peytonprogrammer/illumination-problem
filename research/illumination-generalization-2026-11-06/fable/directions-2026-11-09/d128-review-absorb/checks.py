"""D128 referee checks for band-absorption.snapshot.md.

Own code. It doesn't import the author's replay. Exact integers and Fraction only.
Every path is a prescribed certificate built from the note's formulas, then
traced by a generic polygon billiard tracer. No search over directions or words.
Run: python3 -B checks.py
"""
from fractions import Fraction as Fr
from math import gcd
from functools import reduce
import time

T0 = time.process_time()


def lcm(a, b):
    return a * b // gcd(a, b)


def rgcd(a, b):
    """Positive generator of aZ + bZ for rationals."""
    a, b = Fr(a), Fr(b)
    n = lcm(a.denominator, b.denominator)
    return Fr(gcd(int(a * n), int(b * n)), n)


def rlcm(xs):
    """Positive generator of the intersection of x_i Z for positive rationals."""
    xs = [Fr(x) for x in xs]
    n = reduce(lcm, (x.denominator for x in xs), 1)
    return Fr(reduce(lcm, (int(x * n) for x in xs), 1), n)


def vp(x, p):
    x = Fr(x)
    if x == 0:
        return 10**9
    v, a, b = 0, x.numerator, x.denominator
    while a % p == 0:
        a //= p; v += 1
    while b % p == 0:
        b //= p; v -= 1
    return v


# ---------------------------------------------------------------- tracer
def edges_of(poly):
    out = []
    for (x1, y1), (x2, y2) in zip(poly, poly[1:] + poly[:1]):
        if x1 == x2:
            out.append(('v', x1, min(y1, y2), max(y1, y2)))
        else:
            assert y1 == y2
            out.append(('h', y1, min(x1, x2), max(x1, x2)))
    return out


def trace(edges, S, v, T, max_vert):
    """Billiard from S with integer direction v. Returns (vertical travel at T, events) or raises."""
    px, py = Fr(S[0]), Fr(S[1])
    a, b = v
    vert = Fr(0)
    events = []
    while True:
        best = None
        for kind, c, lo, hi in edges:
            if kind == 'v' and a:
                t = (c - px) / a
                if t > 0:
                    y = py + t * b
                    if lo <= y <= hi and (best is None or t < best[0]):
                        best = (t, kind, y in (lo, hi))
            elif kind == 'h' and b:
                t = (c - py) / b
                if t > 0:
                    x = px + t * a
                    if lo <= x <= hi and (best is None or t < best[0]):
                        best = (t, kind, x in (lo, hi))
        t, kind, corner = best
        dx, dy = T[0] - px, T[1] - py
        if dx * b == dy * a:
            tau = dx / a if a else dy / b
            if 0 < tau < t:
                return vert + abs(b) * tau, events
        if corner:
            raise AssertionError('corner hit')
        px, py = px + t * a, py + t * b
        vert += abs(b) * t
        if vert > max_vert:
            raise AssertionError('target not reached within vertical travel %s' % max_vert)
        if kind == 'v':
            a = -a
        else:
            b = -b
            events.append((px, py))


def direction(s, up, sheet=1):
    s = Fr(s)
    return (sheet * s.numerator, (1 if up else -1) * s.denominator)


# ---------------------------------------------------------------- cov279 room
def cov_poly(q):
    return [(0, 0), (2*q, 0), (2*q, 2), (4*q, 2), (4*q, 3), (5*q, 3), (5*q, 4), (6*q, 4),
            (6*q, 6), (4*q, 6), (4*q, 4), (2*q, 4), (2*q, 3), (2*q-3, 3), (2*q-3, 2), (0, 2)]


def bands(q):   # (left end, width) for y-bands (0,2),(2,3),(3,4),(4,6)
    return [(0, 2*q), (2*q-3, 2*q+3), (2*q, 3*q), (4*q, 2*q)]


def rows(q):    # open interval of interior lattice abscissas at heights 1..5
    return {1: (0, 2*q), 2: (2*q-3, 2*q), 3: (2*q, 4*q), 4: (4*q, 5*q), 5: (4*q, 6*q)}


def fold(z, l, u):
    r = (z - l) % (2*u)
    return (l + r, 1) if r <= u else (l + 2*u - r, -1)


def E(l, e, x):
    return l + e*(x - l)


def four_band(q, X, Y):
    """Note steps 1-4 for S=(X,1), T=(Y,5). Returns slope s and diagnostics."""
    B = bands(q)
    c = 2*q - 1 if (3*Y + 2*X - 2*(2*q - 1)) % (2*q) else 2*q + 1
    assert (3*Y + 2*X - 2*c) % (2*q)
    s0 = Fr(c - X, 3)
    # step 2: phase of T traced back one unit, relative to 4q, mod 4q; shifts by -4q/3 per i
    best = None
    for i in range(3):
        s = s0 + Fr(4*q*i, 3)
        ph = (Y - 4*q - s) % (4*q)
        ph = ph - 4*q if ph > 2*q else ph
        if best is None or abs(ph) < abs(best[0]):
            best = (ph, s)
    ph, s = best
    assert ph != 0 and abs(ph) <= Fr(2*q, 3)
    x4, e4 = fold(Y - s, 4*q, 2*q)
    assert 4*q < x4 < 5*q
    # step 3: choose s + 4q t, t=0,1,2, with band-2 phase rel 2q within q of zero
    opts = []
    for t in range(3):
        st = s + 4*q*t
        ph3 = (E(2*q, e4, x4) - st - 2*q) % (6*q)
        ph3 = ph3 - 6*q if ph3 > 3*q else ph3
        opts.append((abs(ph3), t, st))
    chosen = min(o for o in opts if o[0] <= q)
    s3 = chosen[2]
    x3, e3 = fold(E(2*q, e4, x4) - s3, 2*q, 3*q)
    assert 2*q < x3 <= 3*q
    x2, e2 = fold(X + 3*s3, 0, 2*q)
    assert x2 == 2*q - 1
    l1, u1 = B[1]
    Fm = E(l1, e3, x3) - E(l1, e2, x2) - s3
    assert Fm.denominator == 1 and Fm % 2 == 0
    P = 12*q
    g = rgcd(P, 2*u1)
    assert g == 2
    m = u1  # solve 12q k = Fm mod 2u1  <=>  6q k = Fm/2 mod u1
    k = (int(Fm) // 2) * pow(6*q, -1, m) % m
    s_final = s3 + P*k
    return s_final, dict(s3=s3, x2=x2, e2=e2, x3=x3, e3=e3, x4=x4, e4=e4, opts=opts, t=chosen[1])


def two_band(q, y, X, Y):
    """Heights y -> y+2, one unit in each of two bands. Note's rule with flips."""
    B = bands(q)
    if (y, X, Y) == (3, 3*q, 5*q):
        return Fr(3*q, 2), 1, 4, 'cap'
    l, u = B[y - 1]
    r, v = B[y]
    lo, hi = max(l, r), min(l + u, r + v)
    g = gcd(u, v)
    for label, (U, sheet, V) in (('plain', (X, 1, Y)), ('flipS', (2*l - X, -1, Y)), ('flipT', (X, 1, 2*r - Y))):
        c = Fr(U + V, 2)
        x = c + g * ((lo - c) // g + 1)
        if not lo < x < hi:
            continue
        # s = x - U + 2u m with x + s = V mod 2v
        j = int(x - c) // g          # 2x - U - V = 2 g j
        mm = (-j) * pow(u // g, -1, v // g) % (v // g) if v // g > 1 else 0
        s = x - U + 2*u*mm
        assert (x + s - V) % (2*v) == 0
        return s, sheet, 2, label
    raise AssertionError('no two-band certificate')


def replay(q, do_trace=True):
    R = rows(q)
    pts = [(x, y) for y in range(1, 6) for x in range(R[y][0] + 1, R[y][1])]
    edges = edges_of(cov_poly(q))
    stats = {}
    for i, (X, y) in enumerate(pts):
        for (Y, w) in pts[i+1:]:
            if (w - y) % 2 or (Y - X) % 2:
                continue
            key = (y, w)
            stats.setdefault(key, [0, 0])
            stats[key][0] += 1
            if y == w:
                lo, hi = R[y]
                assert lo < min(X, Y) and max(X, Y) < hi   # open chord at one height
                stats[key][1] += 1
                continue
            if not do_trace:
                continue
            if (y, w) == (1, 5):
                s, info = four_band(q, X, Y)
                assert 0 <= s < 12*q*(2*q + 3)
                D, ev = trace(edges, (X, 1), direction(s, up=False), (Y, 5), 6)
                assert D == 6 and len(ev) == 1 and ev[0][1] == 0, (X, Y, s, D, ev)
            else:
                s, sheet, D0, label = two_band(q, y, X, Y)
                stats.setdefault(label, 0)
                stats[label] += 1
                D, ev = trace(edges, (X, y), direction(s, up=True, sheet=sheet), (Y, w), D0)
                assert D == D0, (X, Y, s, D)
            stats[key][1] += 1
    return stats


def log(*a):
    print(*a, flush=True)


# ================================================================ claim 1
log('== Claim 1: absorbing-band choice in cov279, route travels (1,2,1,1,1) ==')
for q in (4, 8, 10, 14, 16, 20, 22, 28, 40, 52, 64):
    B = bands(q)
    u = [w for _, w in B]
    legs = [(0, 1), (0, 2), (1, 1), (2, 1), (3, 1)]
    res = {}
    for mid in (1, 2):
        outer = [(u[b], d) for b, d in legs if b != mid]
        P = rlcm([Fr(2*w, d) for w, d in outer])
        g = rgcd(1 * P, 2*u[mid])
        res[mid] = (P, g)
    log('q=%3d  mid width 2q+3: P=%d g=%s | mid width 3q: P=%d g=%s  g/2q=%s'
        % (q, res[1][0], res[1][1], res[2][0], res[2][1], res[2][1] / (2*q)))
    if q % 3:
        assert res[1][1] == 2 and res[2][1] == 2*q
log('For 3 | q (e.g. q=6, 12): gcd(12q,4q+6) =', [rgcd(12*q, 4*q + 6) for q in (6, 12, 18)])

log('\nExplicit legal outer placements where the width-3q band cannot absorb F:')
for q in (8, 10, 14, 16, 20):
    B = bands(q)
    shown = 0
    R = rows(q)
    for X in range(1, 2*q, 3):
        for Y in [y for y in range(4*q + 1, 6*q) if (y - X) % 2 == 0][::3]:
            s, info = four_band(q, X, Y)
            x4, e4 = info['x4'], info['e4']
            x2, e2 = info['x2'], info['e2']
            for ab, t, st in info['opts']:
                # band-1 leg forward from y=2 to y=3 at slope st
                x3, e3 = fold(E(B[1][0], e2, x2) + st, *B[1])
                if not (2*q < x3 < 4*q):
                    continue
                Fm = E(2*q, e4, x4) - E(2*q, e3, x3) - st       # middle band 2, depth 1
                g = 2*q
                if Fm % g:
                    shown += 1
                    if shown <= 2:
                        log('  q=%d S=(%d,1) T=(%d,5) slope %s: x2=%s x3=%s x4=%s all legal; F=%s, F mod 2q=%s -> no shift absorbs'
                            % (q, X, Y, st, x2, x3, x4, Fm, Fm % g))
    log('  q=%d: %d such placements among the step-3 alternatives of the sampled pairs' % (q, shown))
    assert shown > 0

log('\nUninterrupted upward route S=(2q-1,1), T=(6q-1,5): exact window test')
for q in (4, 5, 6, 8, 16, 28):
    # first unit step: X+s folded in (0,2q) must lie in the opening (2q-3,2q)
    # allowed s mod 4q: X+s in (2q-3,2q) U (2q,2q+3)  =>  s in (-2,1) U (1,4)
    # last backward unit step: Y-s folded in (4q,6q) must lie in (4q,5q)
    # Y-s ranges over (6q-5,6q+1) mod 4q; fold about 6q
    lo_img = 6*q - 5
    ok = lo_img < 5*q
    log('  q=%2d  backward images lie in (%d,%d); intersect (4q,5q)=(%d,%d): %s'
        % (q, 6*q - 5, 6*q, 4*q, 5*q, ok))
    assert ok == (q < 5)

# ================================================================ claim 2
log('\n== Claim 2: P = lcm(2u_i/d_i), absorption iff F in gcd(dP,2u)Z ==')


def preserving_group_bruteforce(outer, N, bound):
    """Smallest j/N > 0 with d_i j/N in 2u_i Z for all i (j up to bound)."""
    for j in range(1, bound + 1):
        ds = Fr(j, N)
        if all((d * ds) % (2*w) == 0 for w, d in outer):
            return ds
    return None


cases = [
    ([(6, 4), (10, 3)], (15, 2)),
    ([(9, 2), (4, 3), (5, 5)], (12, 3)),
    ([(14, 4), (21, 6)], (35, 2)),
    ([(8, 1), (11, 1)], (24, 1)),
    ([(7, 3), (7, 2)], (14, 5)),
    ([(6, 2), (6, 4), (15, 3)], (10, 4)),
    ([(4, 1)], (3, 1)),
    ([(2, 3)], (5, 1)),
]
for outer, (u, d) in cases:
    P = rlcm([Fr(2*w, dd) for w, dd in outer])
    N = reduce(lcm, (dd for _, dd in outer), 1)
    bf = preserving_group_bruteforce(outer, N, int(P * N) + 5)
    assert bf == P, (outer, P, bf)
    g = rgcd(d * P, 2*u)
    # p-adic formula
    for p in (2, 3, 5, 7, 11, 13):
        pred = min(vp(2*u, p), vp(d, p) + max(vp(2*w, p) - vp(dd, p) for w, dd in outer))
        assert vp(g, p) == pred, (outer, u, d, p)
    # solvability of d P k = F mod 2u over F in a range of rationals with the right denominator
    den = (d * P).denominator
    period = int(2*u / g) if (2*u / g).denominator == 1 else None
    agree = 0
    for Fnum in range(-4*u*den, 4*u*den + 1):
        Fv = Fr(Fnum, den)
        solv = any((d * P * k - Fv) % (2*u) == 0 for k in range(int(2*u*den) + 1))
        assert solv == (Fv % g == 0), (outer, u, d, Fv)
        agree += 1
    log('  outer %-28s mid (u=%d,d=%d): P=%s (brute force %s), g=%s, 2/g integral: %s, %d F values agree'
        % (outer, u, d, P, bf, g, (2 / g).denominator == 1, agree))

log('  Folding check: one run of width u, travel d; phase shift dDs preserves (x,e) iff dDs in 2uZ')
for u, d in ((5, 2), (6, 3), (7, 1)):
    for num in range(0, 4*u*d + 1):
        ds = Fr(num, d)
        for z in (Fr(1, 3), Fr(7, 2), Fr(u, 2)):
            same = fold(z + d*ds, 0, u) == fold(z, 0, u)
            assert same == ((d*ds) % (2*u) == 0), (u, d, ds, z)
log('  ok')

log('  Parity telescoping: F in 2Z on the actual sheets of the cov279 four-band certificates')
for q in (8, 14):
    cnt = 0
    R = rows(q)
    for X in range(1, 2*q):
        for Y in range(4*q + 1, 6*q):
            if (X - Y) % 2:
                continue
            s, info = four_band(q, X, Y)    # asserts F in 2Z with 6 s3 in 2Z
            assert (6 * info['s3']) % 2 == 0
            cnt += 1
    log('  q=%d: %d pairs, F in 2Z and 6s in 2Z each time' % (q, cnt))

# ================================================================ claim 3
log('\n== Claim 3: CRT placement on a pairwise-coprime monotone chain ==')
# staircase: bands [l, l+u] x [y0, y1]
chain = [(0, 5, 0, 3), (2, 7, 3, 5), (5, 9, 5, 7), (11, 4, 7, 10)]
poly = [(0, 0), (5, 0), (5, 3), (9, 3), (9, 5), (14, 5), (14, 7), (15, 7), (15, 10),
        (11, 10), (11, 7), (5, 7), (5, 5), (2, 5), (2, 3), (0, 3)]
widths = [u for _, u, _, _ in chain]
assert all(gcd(a, b) == 1 for i, a in enumerate(widths) for b in widths[i+1:])
edges = edges_of(poly)


def crt_cert(S, T, sites):
    xs = [S[0]] + sites + [T[0]]
    heights = [S[1]] + [c[3] for c in chain[:-1]] + [T[1]]
    k, M = 0, 1
    for i, (l, u, y0, y1) in enumerate(chain):
        d = heights[i+1] - heights[i]
        assert gcd(d, u) == 1
        a = (xs[i+1] - xs[i]) // 2
        ki = a * pow(d, -1, u) % u
        # combine k = k mod M, k = ki mod u
        t = (ki - k) * pow(M, -1, u) % u
        k, M = k + M*t, M*u
    k = k % M or M
    return 2*k, M


log('  widths', widths, 'overlaps (2,5),(5,9),(11,14)')
for S, T, sites in (((1, 1), (13, 8), [3, 7, 13]), ((3, 2), (13, 8), [3, 7, 13]),
                    ((4, 1), (12, 8), [4, 6, 12]), ((2, 2), (14, 8), [4, 8, 12])):
    s, M = crt_cert(S, T, sites)
    D, ev = trace(edges, S, (s, 1), T, 100)
    assert D == T[1] - S[1] and ev == []
    # check seam crossings at the chosen sites, positive sheet
    x = Fr(S[0]); y = S[1]
    for i, ((l, u, y0, y1), site) in enumerate(zip(chain, sites + [T[0]])):
        top = T[1] if i == len(chain) - 1 else y1
        z, e = fold(x + (top - y) * s, l, u)
        assert z == site and e == 1
        x, y = z, y1
    log('  S=%s T=%s sites=%s: k=%d <= prod u = %d, slope %d; traced, vertical travel %s, hits T, no corner'
        % (S, T, sites, s // 2, M, s, D))
log('  Polynomial bound: k <= prod u_i <= U^m; m <= 9 bands gives slope <= 2 U^9')

# generalized CRT with repeated / non-coprime moduli: brute-force agreement
log('  Generalized CRT test against brute force:')
tests = [([(2, 6, 4), (3, 9, 3)]), ([(1, 6, 1), (1, 10, 3)]), ([(4, 6, 2), (2, 9, 4)]), ([(3, 12, 6), (5, 8, 1)])]
for sysm in tests:
    L = reduce(lcm, (u for _, u, _ in sysm), 1)
    brute = any(all((d*k - a) % u == 0 for d, u, a in sysm) for k in range(L))
    pred = True
    res = []
    for d, u, a in sysm:
        t = gcd(d, u)
        if a % t:
            pred = False; break
        m = u // t
        res.append(((a // t) * pow(d // t, -1, m) % m if m > 1 else 0, m))
    if pred:
        pred = all((ki - kj) % gcd(mi, mj) == 0 for i, (ki, mi) in enumerate(res) for kj, mj in res[i+1:])
    assert pred == brute, sysm
    log('   ', sysm, 'solvable:', brute)

# ================================================================ claim 4
log('\n== Claim 4: cov279 replays, own certificates, own tracer ==')
for q in (8, 10, 14, 20):
    st = replay(q, do_trace=q in (8, 14))
    tot = sum(v[0] for k, v in st.items() if isinstance(k, tuple))
    lit = sum(v[1] for k, v in st.items() if isinstance(k, tuple))
    log('  q=%2d coprime to 3: %s | same-parity pairs %d, (1,5) pairs %d, traced lit %s, labels %s'
        % (q, q % 3 != 0, tot, st[(1, 5)][0], lit if q in (8, 14) else 'not traced',
           {k: v for k, v in st.items() if isinstance(k, str)}))
    if q in (8, 14):
        assert lit == tot

# ================================================================ claim 5
log('\n== Claim 5: odd cross, bands 4x(b-2), 2bx4, 4x(b-2) ==')
for b in (5, 7, 9, 11):
    def inside(x0, x1, y0, y1):
        # cross: |x|<=2, |y|<=b  union  |y|<=2, |x|<=b ; a rectangle lies inside iff it lies in one arm
        in_v = -2 <= x0 and x1 <= 2 and -b <= y0 and y1 <= b
        in_h = -2 <= y0 and y1 <= 2 and -b <= x0 and x1 <= b
        # union is not convex; check sample of all lattice cells of the rectangle
        for cx in range(x0, x1):
            for cy in range(y0, y1):
                if not ((-2 <= cx and cx + 1 <= 2 and -b <= cy and cy + 1 <= b) or
                        (-2 <= cy and cy + 1 <= 2 and -b <= cx and cx + 1 <= b)):
                    return False
        return True
    worst = 0
    for x0 in range(-b, b):
        for x1 in range(x0 + 1, b + 1):
            for y0 in range(-b, b):
                for y1 in range(y0 + 1, b + 1):
                    if min(x1 - x0, y1 - y0) > worst and inside(x0, x1, y0, y1):
                        worst = min(x1 - x0, y1 - y0)
    hb = [(4, b - 2), (2*b, 4), (4, b - 2)]
    log('  b=%2d bands %s, max band height %d, max shorter side over contained lattice rectangles %d'
        % (b, hb, max(h for _, h in hb), worst))
    assert worst == 4
cross9 = [(2, -9), (2, -2), (9, -2), (9, 2), (2, 2), (2, 9), (-2, 9), (-2, 2), (-9, 2), (-9, -2),
          (-2, -2), (-2, -9)]
D, ev = trace(edges_of(cross9), (6, 0), (-1, -1), (0, 6), 20)
log('  cross b=9: shot from (6,0) direction (-1,-1) reaches (0,6), vertical travel %s, horizontal-wall events %s' % (D, ev))

log('\nCPU seconds: %.1f' % (time.process_time() - T0))
