"""D108: independent exact check of qclass-closure/bbbb/twist-overlap.md.

Own region tracer for DB55 stretches  [0,5]^2 u [5,5+l]x[2,3] u [5+l,10+l]x[0,5],
cross-checked against d8-perturbation-test/tracer.py (cell tracer) at short l.
Sheets: a lift is (sh, sv, x, y), Q-chart coordinates (sh*x, sv*y) up to translation.
V (least rim-fixing vertical multitwist, shear 2) has derivative [[1,0],[2,1]] and
moves a chamber lattice lift at offset d from its chamber's left side by
Y -> Y + 2*sh*d (mod 10).  Everything is Fraction / int.
"""
import sys
import functools
print = functools.partial(print, flush=True)
from fractions import Fraction as F
from math import gcd, floor
from itertools import product
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'd8-perturbation-test'))
import tracer as d8  # noqa: E402


def cells(l):
    r = lambda x0, x1, y0, y1: {(i, j) for i in range(x0, x1) for j in range(y0, y1)}
    return r(0, 5, 0, 5) | r(5, 5 + l, 2, 3) | r(5 + l, 10 + l, 0, 5)


def fold(y, lo, hi):
    """Fold real y into [lo,hi] by reflection; return (folded, sign of velocity)."""
    P = 2 * (hi - lo)
    z = (y - lo) % P
    return (lo + z, 1) if z <= hi - lo else (lo + P - z, -1)


def region_trace(l, S, v):
    """Billiard from S with velocity v for unit time. Return (end, ok)."""
    x, y = F(S[0]), F(S[1])
    vx, vy = F(v[0]), F(v[1])
    t = F(0)
    assert vx != 0
    def region(x, y):
        if x < 5 or (x == 5 and (vx < 0 or not (2 < y < 3))):
            return 'L'
        if x > 5 + l or (x == 5 + l and (vx > 0 or not (2 < y < 3))):
            return 'R'
        return 'C'
    while True:
        reg = region(x, y)
        lo, hi = (2, 3) if reg == 'C' else (0, 5)
        xl, xr = {'L': (0, 5), 'C': (5, 5 + l), 'R': (5 + l, 10 + l)}[reg]
        nx = xr if vx > 0 else xl
        dt = (nx - x) / vx
        if t + dt >= 1:  # end inside this region
            dt = 1 - t
            yy, sg = fold(y + vy * dt, lo, hi)
            ex = x + vx * dt
            # corner at end?
            ok = not (yy in (lo, hi) and ex in (xl, xr))
            if ex in (5, 5 + l) and yy in (2, 3):
                ok = False  # reflex corner reached exactly at t = 1
            return (ex, yy), ok
        yy, sg = fold(y + vy * dt, lo, hi)
        vy = vy * sg
        t += dt
        x, y = nx, yy
        # event at vertical line x=nx, height y
        if y in (lo, hi):
            return (x, y), False  # corner of this region's rectangle
        if reg == 'C':
            continue  # mouth open for 2<y<3: pass into chamber
        mouth = (reg == 'L' and x == 5) or (reg == 'R' and x == 5 + l)
        if mouth and 2 < y < 3:
            continue
        if mouth and y in (2, 3):
            return (x, y), False
        vx = -vx  # smooth vertical wall


def band(lower, upper, sh_lo, sh_up, l):
    """Two-band test for physical marks lower=(x0,y0), upper=(x1,y1), y1=y0+2, seam y0+1.
    Returns (p, c) with p>0 solving the congruences, or None."""
    (x0, y0), (x1, y1) = lower, upper
    h = y0 + 1
    a = b = 1
    def run(x, yrange):
        ylo, yhi = yrange
        if ylo >= 2 and yhi <= 3:
            return (0, 10 + l)
        return (0, 5) if x < 5 else (5 + l, 10 + l)
    R0 = run(x0, (y0, h)); R1 = run(x1, (h, y1))
    I = (max(R0[0], R1[0]), min(R0[1], R1[1]))
    P0, P1 = 2 * (R0[1] - R0[0]), 2 * (R1[1] - R1[0])
    X0 = x0 if sh_lo > 0 else 2 * R0[0] - x0
    X1 = x1 if sh_up > 0 else 2 * R1[0] - x1
    g = gcd(b * P0, a * P1)
    base = F(b * X0 + a * X1, a + b)
    step = F(g, a + b)
    k = floor((I[0] - base) / step) + 1
    c = base + k * step
    if not (I[0] < c < I[1]):
        return None
    # solve a p = c - X0 (mod P0), b p = X1 - c (mod P1), a=b=1
    for m in range(P1):
        p = c - X0 + P0 * m
        if (X1 - c - p) % P1 == 0:
            if p <= 0:
                p += P0 * P1 // gcd(P0, P1)
            return p, c, g, R0, R1, I
    return None


def V_lift(sh, sv, x, y, j, l):
    d = x if x < 5 else x - (5 + l)
    Y = (sv * y + 2 * sh * d * j) % 10
    return (sh, 1, Y) if 0 < Y < 5 else (sh, -1, 10 - Y)  # (sh, sv', physical y)


def pull_and_trace(l, S, T, ls, lt, j, use_cell):
    """ls, lt = (sh, sv) lifts. Apply V^j, band-test, pull back, trace. Return status."""
    shs, svs = ls; sht, svt = lt
    _, svs2, ys2 = V_lift(shs, svs, S[0], S[1], j, l)
    _, svt2, yt2 = V_lift(sht, svt, T[0], T[1], j, l)
    if svs2 != svt2:
        return 'sheet-mismatch'
    if abs(ys2 - yt2) != 2 or ys2 in (0, 5) or yt2 in (0, 5):
        return 'heights'
    s2, t2 = (S[0], ys2), (T[0], yt2)
    if ys2 < yt2:
        lo, up, shl, shu = s2, t2, shs, sht
    else:
        lo, up, shl, shu = t2, s2, sht, shs
    r = band(lo, up, shl, shu, l)
    if r is None:
        return 'band-fail'
    p = r[0]
    # physical upward path from lower: velocity (shl*p, 1) over rise 2 -> displacement 2*(shl*p, 1)
    vlow = (2 * shl * p, 2)
    end, ok = region_trace(l, lo, vlow)
    assert ok and end == (F(up[0]), F(up[1])), ('band path', l, lo, up, p, end, ok)
    # physical velocity at s' (reverse if s' is upper): final horizontal sign at upper is shu*sign
    if ys2 < yt2:
        vs = vlow
    else:
        vs = (-2 * shu * p, -2)
    # Q displacement of sigma at s' (sheet shs, svs2), then pull back by V^-j
    w1, w2 = shs * vs[0], svs2 * vs[1]
    w2 = w2 - 2 * j * w1
    vphys = (shs * w1, svs * w2)
    end, ok = region_trace(l, S, vphys)
    if not (ok and end == (F(S[0] if False else T[0]), F(T[1]))):
        return 'pullback-miss %s %s' % (end, ok)
    if use_cell:
        e2, ok2, _ = d8.trace(cells(l), S, vphys)
        assert ok2 and e2 == (F(T[0]), F(T[1])), ('cell tracer disagrees', l, S, T, vphys, e2, ok2)
    return ('lit', vphys)


def witness():
    print('== Claim 2: DB55 witness (l=3) ==')
    l = 3
    print('V lift of S=(1,1) sheet (+,-):', V_lift(1, -1, 1, 1, 1, l))
    print('V lift of T=(9,1) sheet (+,+):', V_lift(1, 1, 9, 1, 1, l))
    r = band((1, 1), (9, 3), 1, 1, l)
    print('band: p=%s c=%s g=%s runs %s %s I=%s' % r)
    # note's choice c=3, p=32
    p = 32
    assert p % 10 == 2 and p % 26 == 6
    end, ok, vis = d8.trace(cells(l), (1, 1), (2 * p, 2))
    print('d8 tracer sigma (1,1)+(64,2): end', end, 'ok', ok, 'lattice sites', vis)
    nref = []
    # count vertical-wall reflections per leg with region tracer by splitting at y=2
    e1, ok1 = region_trace(l, (1, 1), (p, 1))
    print('lower leg end', e1, ok1)
    # the note's own choice: sigma displacement (64,2) on sheet (+,+); V^-1 pullback
    w = (64, 2 - 2 * 1 * 64)
    vphys = (w[0], -w[1])  # S lift (+,-)
    e1, o1 = region_trace(l, (1, 1), vphys)
    e2, o2, vis2 = d8.trace(cells(l), (1, 1), vphys)
    print('note p=32 pullback: physical velocity', vphys, 'region ->', e1, o1, '; d8 ->', e2, o2, 'sites', vis2)
    st = pull_and_trace(l, (1, 1), (9, 1), (1, -1), (1, 1), 1, True)
    print('pullback V^-1 sigma: physical velocity from S', st[1], '-> reaches (9,1) legally (both tracers)')
    end, ok, vis = d8.trace(cells(l), (1, 1), st[1])
    print('  d8 tracer lattice sites on pulled-back path:', vis)


def stretches(lengths):
    print('\n== Claim 3: stretches ==')
    for l in lengths:
        C = cells(l)
        L = [(x, y) for x in range(1, 5) for y in range(1, 5)]
        R = [(5 + l + x, y) for x in range(1, 5) for y in range(1, 5)]
        same = [(s, t) for s in L for t in R if (s[0] - t[0]) % 2 == 0 and (s[1] - t[1]) % 2 == 0]
        note_lit = note_mismatch = fixed_lit = fixed_fail = 0
        examples = []
        use_cell = l <= 9
        for S, T in same:
            y, y2 = S[1], T[1]
            # ---- the note's recipe: horizontal sheets front; vertical lifts as described
            if y != y2:
                st = pull_and_trace(l, S, T, (1, 1), (1, 1), 0, use_cell)
            else:
                d, d2 = S[0], T[0] - 5 - l
                j = next(j for j in range(1, 5) if (d * j - y) % 5 == 0)
                ystar = {1: 3, 3: 1, 2: 4, 4: 2}[y]
                sv2 = next(sv for sv in (1, -1) if (sv * y + 2 * d2 * j) % 10 in (ystar, 10 - ystar))
                st = pull_and_trace(l, S, T, (1, -1), (1, sv2), j, use_cell)
            if st[0] == 'lit':
                note_lit += 1
            else:
                note_mismatch += 1
                if len(examples) < 3:
                    examples.append((S, T, st))
            # ---- repaired recipe: any horizontal and vertical lifts, any j
            ok = False
            for shs, svs, sht, svt, j in product((1, -1), (1, -1), (1, -1), (1, -1), range(5)):
                st = pull_and_trace(l, S, T, (shs, svs), (sht, svt), j, False)
                if st[0] == 'lit':
                    ok = True
                    if use_cell:
                        e2, ok2, _ = d8.trace(C, S, st[1])
                        assert ok2 and e2 == (F(T[0]), F(T[1]))
                    break
            fixed_lit += ok
            fixed_fail += not ok
        print('l=%d gcd(5,l)=%d: %d same-class cross pairs; note recipe lit %d, not applicable %d; '
              'with free sheets lit %d, failed %d' % (l, gcd(5, l), len(same), note_lit, note_mismatch,
                                                       fixed_lit, fixed_fail))
        for e in examples:
            print('   note recipe gap:', e)


def negative_control():
    print('\n== Controls ==')
    l = 3
    # wrong pullback sign must miss
    st = pull_and_trace(l, (1, 1), (9, 1), (1, -1), (1, 1), 1, False)
    v = st[1]
    end, ok = region_trace(l, (1, 1), (v[0], -v[1] + 4))
    print('perturbed velocity', (v[0], -v[1] + 4), '->', end, ok, '(should not be (9,1) legal)')
    # region tracer vs cell tracer on random-free deterministic sample
    n = agree = 0
    for l in (3, 7):
        for vx in range(1, 30, 3):
            for vy in range(-40, 41, 7):
                for S in ((1, 1), (2, 3), (4, 4)):
                    e1, o1 = region_trace(l, S, (vx * 3, vy))
                    e2, o2, _ = d8.trace(cells(l), S, (vx * 3, vy))
                    n += 1
                    agree += (o1 == o2) and (not o1 or e1 == e2)
    print('region vs d8 cell tracer:', agree, '/', n, 'agree (ok flag and endpoint)')
    # l=5,10 (gcd 5): spacing g/2 = 5 equals |I|; report band failures
    for l in (5, 15):
        fails = 0; tot = 0
        for x0 in range(1, 5):
            for x1 in range(5 + l + 1, 10 + l):
                for s0, s1 in product((1, -1), repeat=2):
                    tot += 1
                    fails += band((x0, 1), (x1, 3), s0, s1, l) is None
        print('l=%d: band test fails in %d of %d (marks, sheets) at heights 1,3' % (l, fails, tot))


if __name__ == '__main__':
    witness()
    negative_control()
    stretches([3, 7, 9, 21, 451, 457])
