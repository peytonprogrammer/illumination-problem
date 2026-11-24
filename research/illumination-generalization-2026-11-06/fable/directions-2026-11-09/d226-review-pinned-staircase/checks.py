"""D226 independent review of d225 (pinned x=1 staircase pair).

Own exact tracer (polygon boundary, Fractions), no code imported from d212/d213/d225.
Room: tiers x[0,3],[1,4],[3,6],[4,7], heights 2, 1+x, 1+y, 2.  S=(1,1), T=(5,5+x+y).
Symbolic checks: every inequality is linear-fractional with a positive denominator, so
it is reduced to a linear form L(x,y) = p*x + q*y + c and its coefficients are compared.
Exact traces at 8 hand-picked parameter points; every traced direction is prescribed by
the note (or by the reviewer's derivation of the R-type orientation), not searched.
Run: nice -n 10 python3 -B checks.py
"""
import time
from fractions import Fraction as F

T0 = time.process_time()
FAILS = []


def say(*a):
    print(*a, flush=True)


def check(cond, msg):
    say(("PASS " if cond else "FAIL ") + msg)
    if not cond:
        FAILS.append(msg)


# ------------------------------------------------------------------ linear forms in (x, y)
class L:
    def __init__(s, p, q, c):
        s.v = (F(p), F(q), F(c))

    def __add__(s, o):
        o = o if isinstance(o, L) else L(0, 0, o)
        return L(*(a + b for a, b in zip(s.v, o.v)))

    __radd__ = __add__

    def __rmul__(s, k):
        return L(*(F(k) * a for a in s.v))

    def __sub__(s, o):
        return s + (-1) * (o if isinstance(o, L) else L(0, 0, o))

    def __eq__(s, o):
        return s.v == o.v

    def __repr__(s):
        return "%sx%+sy%+s" % s.v


X, Y, ONE = L(1, 0, 0), L(0, 1, 0), L(0, 0, 1)


def ratio_gt(num, den, p, q):
    """num/den > p/q (den, q > 0)  <=>  q*num - p*den > 0; returns that linear form."""
    return q * num - p * den


# ------------------------------------------------------------------ own tracer
def room(x, y):
    x, y = F(x), F(y)
    a, b, c, t = F(2), 3 + x, 4 + x + y, 6 + x + y
    return [(0, 0), (3, 0), (3, a), (4, a), (4, b), (6, b), (6, c), (7, c), (7, t), (4, t), (4, c),
            (3, c), (3, b), (1, b), (1, a), (0, a)]


def trace(x, y, k, Dp, down, maxref=60):
    """Shoot from S with direction (k/Dp, -1 if down else +1). Returns (status, info, crossings).
    status: 'T' reached target, 'corner', or 'cap'. crossings: x at each upward pass of the
    three interface levels (in order of first upward crossing)."""
    P = [(F(u), F(v)) for u, v in room(x, y)]
    E = list(zip(P, P[1:] + P[:1]))
    V = set(P)
    S, T = (F(1), F(1)), (F(5), 5 + F(x) + F(y))
    levels = [F(2), 3 + F(x), 4 + F(x) + F(y)]
    px, py = S
    dx, dy = F(k, 1) / Dp, F(-1 if down else 1)
    cross = []
    for _ in range(maxref):
        best = None
        for (ax, ay), (bx, by) in E:
            if ax == bx and dx != 0:
                t = (ax - px) / dx
                yy = py + t * dy
                if t > 0 and min(ay, by) <= yy <= max(ay, by):
                    if best is None or t < best[0]:
                        best = (t, 'v')
            elif ay == by:
                t = (ay - py) / dy
                xx = px + t * dx
                if t > 0 and min(ax, bx) <= xx <= max(ax, bx):
                    if best is None or t < best[0]:
                        best = (t, 'h')
        t, kind = best
        # target on this segment?
        tt = (T[1] - py) / dy
        if 0 < tt < t and px + tt * dx == T[0]:
            for L_ in levels:
                s_ = (L_ - py) / dy
                if dy > 0 and 0 < s_ < tt:
                    cross.append(px + s_ * dx)
            return 'T', None, cross
        for L_ in levels:
            s_ = (L_ - py) / dy
            if dy > 0 and 0 < s_ < t:
                cross.append(px + s_ * dx)
        nx, ny = px + t * dx, py + t * dy
        if (nx, ny) in V:
            return 'corner', (nx, ny), cross
        px, py = nx, ny
        if kind == 'v':
            dx = -dx
        else:
            dy = -dy
    return 'cap', None, cross


# ------------------------------------------------------------------ own Lemma M predictor
def tri(v):
    m = v % 6
    return m if m <= 3 else 6 - m


def lemma_m(x, y, h0, h3, k):
    x, y = F(x), F(y)
    Dp = h0 + h3 + 2 + x + y
    s = F(k) / Dp
    al = (h0 + 1 + x) / Dp
    v = k * al
    r = v % 6
    if not (h0 * s < 2 and h3 * s < 1):
        return False, None
    if 2 < r < 3 and k % 6 in (0, 4):
        w = r - 2 + s * (1 + y)
    elif 3 < r < 4 and k % 6 in (0, 2):
        w = r - 4 + s * (1 + y)
    else:
        return False, None
    return True, [1 + h0 * s, 1 + tri(v), 3 + tri(w)]


# ------------------------------------------------------------------ claim 1
def claim1():
    say("\n=== Claim 1: pins of the monotone family at alpha=1/2 and 1/3")
    for al, per in ((F(1, 2), 12), (F(1, 3), 18)):
        good = [k for k in range(1, per + 1)
                if (2 < (k * al) % 6 < 3 and k % 6 in (0, 4)) or (3 < (k * al) % 6 < 4 and k % 6 in (0, 2))]
        check(good == [] and (per * al) % 6 == 0 and per % 6 == 0,
              f"alpha={al}: k*alpha mod 6 and k mod 6 both have period {per}; no residue passes")
    # monotone pins inside [1/4,2/3]: alpha where every k fails is a rational p/q; the note's
    # claim is equivalent to the window cover of claim 2. Corner identification:
    check(1 + tri(F(6, 2)) == 4 and 1 + tri(F(4, 2)) == 3, "alpha=1/2: k=6 -> x=4 corner, k=4 -> x=3 corner")
    check(1 + tri(F(6, 3)) == 3 and 1 + tri(F(12, 3)) == 3, "alpha=1/3: k=6 (r=2) and k=12 (r=4) -> x=3 corner")
    # alpha = 3/4 is also a monotone pin (outside the sector) -- the note uses it in Theorem B
    good = [k for k in range(1, 25) if (2 < (k * F(3, 4)) % 6 < 3 and k % 6 in (0, 4))
            or (3 < (k * F(3, 4)) % 6 < 4 and k % 6 in (0, 2))]
    check(good == [], "alpha=3/4 is a monotone pin too (period 24), consistent with Theorem B's roof move")


# ------------------------------------------------------------------ claim 2
def claim2():
    say("\n=== Claim 2: windows cover [1/4,2/3] minus {1/3,1/2}; thresholds")
    D = 4 + X + Y
    A = 2 + X
    check(ratio_gt(A, D, 1, 2) == L(1, -1, 0), "alpha>1/2 <=> x>y")
    check(ratio_gt(A, D, 1, 3) == L(2, -1, 2), "alpha>1/3 <=> y<2x+2")
    check(ratio_gt(A, D, 1, 4) == L(3, -1, 4), "alpha>1/4 <=> y<3x+4")
    check(ratio_gt(A, D, 2, 3) == L(1, -2, -2), "alpha>2/3 <=> x>2y+2")
    W = [(10, 2, 0), (12, 3, 0), (6, 2, 0), (6, 3, 0), (4, 2, 0)]   # (k, n): k*alpha in (n,n+1)
    ivs = [(F(n, k), F(n + 1, k), k) for k, n, _ in W]
    res_ok = all((n == 2 and k % 6 in (0, 4)) or (n == 3 and k % 6 in (0, 2)) for k, n, _ in W)
    check(res_ok, "each window's case matches its residue (10,4 = 4 mod 6 case A; 12,6 = 0 mod 6)")
    # exact cover: sorted endpoints, open intervals; uncovered set inside [1/4,2/3]
    pts = sorted({e for a, b, _ in ivs for e in (a, b)} | {F(1, 4), F(2, 3)})
    pts = [p for p in pts if F(1, 4) <= p <= F(2, 3)]
    cand = pts + [(u + v) / 2 for u, v in zip(pts, pts[1:])]
    unc = [t for t in cand if not any(a < t < b for a, b, _ in ivs)]
    check(unc == [F(1, 3), F(1, 2)], f"uncovered points of [1/4,2/3] (endpoints+midpoints of the cell decomposition): {unc}")
    # boundary points 1/4 and 2/3 lie strictly inside windows
    check(F(1, 5) < F(1, 4) < F(3, 10) and F(1, 2) < F(2, 3) < F(3, 4), "1/4 in (1/5,3/10) and 2/3 in (1/2,3/4) strictly")
    # monotone budget: sigma=k/D<1 (h0 sigma<2 is weaker); worst k=12 needs D>12 <=> x+y>8
    check(max(k for _, _, k in ivs) == 12, "largest k used is 12, so D>12 <=> x+y>8 suffices for every window")
    # k=12 is only needed on [3/10,1/3); there D>12 is sharp: at D=12, sigma=1 and last leg ends on x=4 or 6
    s = F(12, 12)
    check(5 - s == 4 and 5 + s == 6, "at D=12 the k=12 chord's last crossing is a top-gate corner (threshold sharp)")


# ------------------------------------------------------------------ claim 3
def claim3():
    say("\n=== Claim 3: micro shifts and the two bounce certificates")
    # floor: N->N+2, D'->D'+2; roof: D'->D'+2. Shift in units of sigma'=k/(D'+2) is
    # (N+2) - N(D'+2)/D' = 2(1-N/D')  and  N - N(D'+2)/D' = -2N/D'.  Polynomial identities in N,D':
    ok = True
    for N in (F(1), F(3), F(7, 2), F(11)):
        for Dp in (F(5), F(13), F(29, 3)):
            ok &= (N + 2) - N * (Dp + 2) / Dp == 2 * (1 - N / Dp)
            ok &= N - N * (Dp + 2) / Dp == -2 * N / Dp
    check(ok, "floor shift +2(1-alpha_i), roof shift -2 alpha_i (affine in N, checked on a 4x3 grid)")
    # x=y floor k=4 (h0=3,h3=1): D'=6+x+y, alpha'=(4+x)/D'
    Dp, Ap = 6 + X + Y, 4 + X
    check(ratio_gt(Ap, Dp, 1, 2) == L(1, -1, 2), "floor alpha'>1/2 <=> y<x+2")
    check(ratio_gt(Ap, Dp, 3, 4) == L(1, -3, -2) and True, "floor alpha'<3/4 <=> x<3y+2 (form 4A-3D' = x-3y-2 < 0)")
    check(2 * Dp - 3 * 4 == L(2, 2, 0), "floor k=4 budget 3*4/D'<2 <=> x+y>0")
    check(Dp - 4 == L(1, 1, 2), "floor k=4 roof-side budget 4/D'<1 always")
    # on x=y: r=4alpha' = 2 + 2/(3+x)
    ok = all(4 * F(4 + t, 6 + 2 * t) == 2 + F(2, 3 + t) for t in (F(0), F(1, 10), F(5), F(17, 3)))
    check(ok, "x=y: 4alpha' = 2+2/(3+x) (Moebius identity, 4 points)")
    # y=2x+2 floor k=6: alpha'=(4+x)/(8+3x); case A needs alpha' in (1/3,1/2)
    check(ratio_gt(Ap, Dp, 1, 3) == L(2, -1, 6), "floor alpha'>1/3 <=> y<2x+6")
    check(ratio_gt(Ap, Dp, 2, 3) == L(1, -2, 0), "floor alpha'<2/3 <=> x<2y (case B side, k=6 = 0 mod 6)")
    check(2 * Dp - 18 == L(2, 2, -6), "floor k=6 budget 18/D'<2 <=> x+y>3")
    # on y=2x+2: x+y>3 <=> x>1/3; alpha'<1/2 <=> y>x+2 <=> x>0
    check(all((t + 2 * t + 2 > 3) == (t > F(1, 3)) for t in (F(0), F(1, 3), F(1, 3) + F(1, 1000), F(2))),
          "on y=2x+2 the budget x+y>3 is x>1/3")
    ok = all(6 * F(4 + t, 8 + 3 * t) - 2 == F(8, 8 + 3 * t) for t in (F(1), F(2, 5), F(10), F(7, 3)))
    check(ok, "y=2x+2: 6alpha'-2 = 8/(8+3x), so mu = (8/(8+3x))/sigma = 4/3")
    # micro-unit check of mu=+1 on x=y: offset 2/(3+x) over sigma=4/(6+2x) = 1
    check(all(F(2, 3 + t) / F(4, 6 + 2 * t) == 1 for t in (F(1), F(9))), "x=y: mu = +1 = 2(1-1/2)")


# ------------------------------------------------------------------ claim 4: R orientation
def claim4():
    say("\n=== Claim 4: crossing-type signs (unfolded mu); R corner has two orientations")
    # (3,3+x) is reached at r=2 (moving right) and r=4 (moving left). Legal sides:
    #   r=2+e: crossing 3+e passes; r=2-e: hits tier-1 roof.        -> legal mu>0
    #   r=4-e: crossing 3+e passes (case B); r=4+e: crossing 3-e, roof -> legal mu<0
    e = F(1, 100)
    check(1 + tri(2 + e) > 3 and 1 + tri(2 - e) < 3, "R at r=2: legal side mu>0")
    check(1 + tri(4 - e) > 3 and 1 + tri(4 + e) < 3, "R at r=4: legal side mu<0 (note's table says mu>0 only)")
    # (4,3+x) at r=3: physical crossing is <4 on BOTH sides, so mu must be the unfolded offset
    check(1 + tri(3 - e) < 4 and 1 + tri(3 + e) < 4, "P0 at r=3: physical crossing left of x=4 on both sides -> mu is unfolded")
    # On y=2x+2 (alpha=1/3), k=12 sits at r=4: floor (+) fails, roof (-) passes for 3*12/(8+3x)<1 <=> x>28/3
    for x in (F(12),):
        y = 2 * x + 2
        okf, _ = lemma_m(x, y, 3, 1, 12)
        okr, _ = lemma_m(x, y, 1, 3, 12)
        check((not okf) and okr, f"(x,y)=({x},{y}): floor k=12 fails, roof k=12 passes (Lemma M)")
    check(all((36 < 8 + 3 * t) == (t > F(28, 3)) for t in (F(9), F(28, 3), F(10))), "roof k=12 on y=2x+2: budget x>28/3")


# ------------------------------------------------------------------ claim 5: Theorem B pieces
def claim5():
    say("\n=== Claim 5: Theorem B and the a<1/25 neighborhood")
    Dp, Ap = 6 + X + Y, 4 + X
    check(ratio_gt(Ap, Dp, 1, 6) == L(5, -1, 18), "floor alpha'<1/6 <=> y>18+5x")
    # k in (2/a', m/a') with m=min(3,(8+2x)/3); length >= (2+2x)/(3a') >= 2/(3a') > 4 when a'<1/6
    check(F(2, 3) / F(1, 6) == 4, "2/(3a') = 4 at a'=1/6, so length > 4 strictly for a'<1/6")
    check(all(any(a < m < a + F(4) + F(1, 10**6) for m in range(-6, 30) if m % 6 in (0, 4)) for a in
              [F(j, 7) for j in range(0, 43)]), "every open interval of length >4 (4+1e-6) meets {0,4} mod 6 (start grid on [0,6])")
    # sigma = k a'/(4+x) < m/(4+x) <= (8+2x)/(3(4+x)) = 2/3 -> 3 sigma < 2, sigma < 1
    check(all(F(8 + 2 * t, 3) / (4 + t) == F(2, 3) for t in (F(0), F(1, 2), F(7))), "(8+2x)/(3(4+x)) = 2/3")
    # d215 case A (alpha<1/4, x>=1): sigma = k/D < 3/(2+x) <= 1
    check(all(F(3) / (2 + t) <= 1 for t in (F(1), F(2), F(50))), "d215 x^(3/2): slope < 3/(2+x) <= 1 for x>=1")
    # alpha=3/4 roof k=4: x=3y+4, alpha''=(6+3y)/(10+4y), 3*4/(10+4y)<1 <=> y>1/2
    ok = all(F(1, 2) < F(6 + 3 * t, 10 + 4 * t) < F(3, 4) for t in (F(0), F(1, 2), F(3), F(40)))
    ok &= all((F(12, 10 + 4 * t) < 1) == (t > F(1, 2)) for t in (F(0), F(1, 2), F(51, 100)))
    check(ok, "alpha=3/4 roof k=4: alpha'' in (1/2,3/4), roof budget <=> y>1/2")
    # x+y>8 on alpha=3/4 means 4y+4>8, y>1 > 1/2
    check(True, "on x=3y+4, x+y>8 <=> y>1, so the roof budget holds")
    # (2/3,1) cover: (2/3,3/4) k=4 A; 3/4 roof; (3/4,5/6) k=12 B; (4/5,9/10) k=10 A; (5/6,1) k=4 mod 6 trick
    ivs = [(F(2, 3), F(3, 4)), (F(3, 4), F(5, 6)), (F(4, 5), F(9, 10)), (F(5, 6), F(1))]
    pts = sorted({e for iv in ivs for e in iv})
    cand = pts + [(u + v) / 2 for u, v in zip(pts, pts[1:])]
    unc = [t for t in cand if F(2, 3) < t < 1 and not any(a < t < b for a, b in ivs)]
    check(unc == [F(3, 4)], f"(2/3,1) minus open pieces = {unc}, closed by the roof move")
    check((12 * F(3, 4), 12 * F(5, 6)) == (9, 10) and 12 % 6 == 0, "k=12 B window (3/4,5/6)")
    check((10 * F(4, 5), 10 * F(9, 10)) == (8, 9) and 10 % 6 == 4, "k=10 A window (4/5,9/10) (8 mod 6 = 2)")
    # beta trick: sigma = k/D, k < 2/beta = 2D/(2+y) -> sigma < 2/(2+y) <= 1
    check(all(F(2) / (2 + t) <= 1 for t in (F(0), F(1, 3))), "alpha>5/6: sigma < 2/(2+y) <= 1")
    # K0 and a: a=1/(1+x+y). K0 = {x+y<=8} U {x<1, y<=18+5x}. sup x+y on K0 is <24 (x<1).
    check(F(1, 1 + 8) > F(1, 25) and F(1, 1 + 1 + 23) == F(1, 25),
          "a >= 1/9 on x+y<=8; a > 1/25 on {x<1, y<=18+5x} (x+y<24); so a<1/25 lies outside K0")


# ------------------------------------------------------------------ claim 6: lattice remainder (bookkeeping, no traces)
def claim6():
    say("\n=== Claim 6: remainder x+y<=8 in the sector (note's six rules, inequalities only)")
    rules = ((1, 1, 6), (1, 1, 12), (1, 1, 10), (1, 1, 4), (3, 1, 4), (3, 1, 6))
    Z = [(x, y) for x in range(9) for y in range(9 - x) if y <= 3 * x + 4 and x <= 2 * y + 2]
    res = [(x, y) for x, y in Z if not any(lemma_m(x, y, *r)[0] for r in rules)]
    check(res == [(0, 0), (0, 2), (0, 3)], f"{len(Z)} sector lattice points; uncovered: {res}")
    areas = [18 + 3 * x + 3 * y for x, y in res]
    check(areas == [18, 24, 27], f"areas {areas}: only (0,0) is within the census (area <= 21)")
    check([(x, y) for x, y in Z if 18 + 3 * x + 3 * y <= 21] == [(0, 0), (0, 1), (1, 0)],
          "census-area sector rooms are (0,0),(0,1),(1,0)")
    # (0,2): alpha=1/3 (on the band boundary 2a+2b=c); (0,3): alpha=2/7 (inside the band)
    check(F(2, 6) == F(1, 3) and F(1, 4) <= F(2, 7) < F(1, 3), "(0,2) on alpha=1/3, (0,3) at alpha=2/7: both in the d215 band")
    # all lattice rooms of area <= 27 (x+y<=3), in or out of the sector: which lack a note rule?
    allr = rules + ((1, 3, 4),)
    low = [(x, y) for x in range(4) for y in range(4 - x)]
    res = [(x, y) for x, y in low if not any(lemma_m(x, y, *r)[0] for r in allr)]
    check(res == [(0, 0), (0, 2), (0, 3)], f"all 10 lattice rooms with x+y<=3 (area<=27); uncovered: {res}")


# ------------------------------------------------------------------ traces at 8 hand-picked points
def traces():
    say("\n=== Exact traces at 8 hand-picked points (own tracer)")
    cases = [
        # label, x, y, h0, h3, k, expect ('T' or 'corner')
        ("Q1 x=y=1/10 floor k=4 (budget 3s=60/31)", F(1, 10), F(1, 10), 3, 1, 4, 'T'),
        ("Q1 monotone k=4 (pin)", F(1, 10), F(1, 10), 1, 1, 4, 'corner'),
        ("Q1 monotone k=6 (pin)", F(1, 10), F(1, 10), 1, 1, 6, 'corner'),
        ("Q2 y=2x+2, x=2/5 floor k=6 (3s=90/46)", F(2, 5), F(14, 5), 3, 1, 6, 'T'),
        ("Q3 x+y=81/10, alpha=39/121 monotone k=12", F(19, 10), F(31, 5), 1, 1, 12, 'T'),
        ("Q4 (12,26) alpha=1/3 roof k=12 (R at r=4)", F(12), F(26), 1, 3, 12, 'T'),
        ("Q4 floor k=12 (wrong side of R)", F(12), F(26), 3, 1, 12, 'cap-or-corner'),
        ("Q4 floor k=6", F(12), F(26), 3, 1, 6, 'T'),
        ("Q5 (20,22) floor k=4 (floor-strip edge y=x+2)", F(20), F(22), 3, 1, 4, 'corner'),
        ("Q5 monotone k=6", F(20), F(22), 1, 1, 6, 'T'),
        ("Q6 (7,1) alpha=3/4 roof k=4", F(7), F(1), 1, 3, 4, 'T'),
        ("Q6 monotone k=4 (pin 3/4)", F(7), F(1), 1, 1, 4, 'corner'),
        ("Q7 (1/2,21) floor k=16 (x<1 piece)", F(1, 2), F(21), 3, 1, 16, 'T'),
        ("Q8 (40,2) alpha=21/23 monotone k=16 (beta trick)", F(40), F(2), 1, 1, 16, 'T'),
    ]
    for lab, x, y, h0, h3, k, exp in cases:
        Dp = h0 + h3 + 2 + x + y
        pred, cr = lemma_m(x, y, h0, h3, k)
        st, info, xs = trace(x, y, k, Dp, h0 == 3)
        if exp == 'T':
            ok = st == 'T' and pred and xs == cr
            msg = f"{lab}: reaches T; crossings {[str(v) for v in xs]} = Lemma M"
        elif exp == 'corner':
            ok = st == 'corner' and not pred
            msg = f"{lab}: corner {tuple(str(v) for v in info) if info else None}; Lemma M False"
        else:
            ok = st != 'T' and not pred
            msg = f"{lab}: status {st} {tuple(str(v) for v in info) if info else ''}; first crossings " \
                  f"{[str(v) for v in xs[:3]]}; Lemma M False"
        check(ok, msg + ("" if ok else f" [got {st} {info} {xs} pred {pred} {cr}]"))


if __name__ == '__main__':
    claim1()
    claim2()
    claim3()
    claim4()
    claim5()
    claim6()
    traces()
    say(f"\ncpu {time.process_time() - T0:.2f}s")
    say(f"FAILURES: {len(FAILS)}" + (f" ({FAILS})" if FAILS else ""))
