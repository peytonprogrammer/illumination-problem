"""D225 checks: pinned x=1 staircase pair, two-scale blow-up at the pins.

Room: offset staircase, tiers x[0,3],[1,4],[3,6],[4,7], heights 2, 1+x, 1+y, 2
(d213 stair_room; y-scaled copy from d215 for rational gains).
Pair: S=(1,1), T=(5, top-1).  alpha=(2+x)/D, D=4+x+y.

Exact traces only at 5 hand-picked parameter points, all in the strip/band:
  P1=(10,10) [alpha=1/2], P2=(10,22) [alpha=1/3], P3=(10,30) [alpha=3/11],
  P4=(10,34) [alpha=1/4], P5=(1/2,1/2) [alpha=1/2, rational gains, q=2].
Every traced ray is a direction prescribed by the note (Lemma M with stated
h0,h3,k).  No direction, word, room-size or parameter search.
Everything else is exact rational arithmetic on the inequalities the note uses.
Run: nice -n 10 python3 -B checks.py
"""
import importlib.util
import os
import time
from fractions import Fraction as F
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, "..", rel, "checks.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


K = load("d212checks", "d212-review-descent-skeleton")
M13 = load("d213checks", "d213-review-marked-selection")
rects, trace = K.rects, K.trace
stair_room = M13.stair_room

T0 = time.process_time()
FAILS = []


def say(*a):
    print(*a, flush=True)


def check(cond, msg):
    say(("PASS " if cond else "FAIL ") + msg)
    if not cond:
        FAILS.append(msg)


def stair_q(p, r, q):
    """Gains p/q, r/q; y-axis scaled by q (as in d215)."""
    h = [2 * q, q + p, q + r, 2 * q]
    ys = [0, h[0], h[0] + h[1], h[0] + h[1] + h[2], sum(h)]
    xs = [(0, 3), (1, 4), (3, 6), (4, 7)]
    return rects(*[(xs[i][0], xs[i][1], ys[i], ys[i + 1]) for i in range(4)])


def tri(v):
    """Fold of an unfolded offset v into [0,3] (reflection group of a width-3 tier)."""
    m = v % 6
    return m if m <= 3 else 6 - m


# ------------------------------------------------------------------ Lemma M predictor
def lemma_m(x, y, h0, h3, k):
    """Predicted legality of the Lemma M chord and its three interface abscissae.
    h0 = 1 (straight up) or 3 (floor bounce); h3 = 1 (straight) or 3 (roof bounce)."""
    Dp = h0 + h3 + 2 + x + y
    s = F(k, Dp)
    a = F(h0 + 1 + x, Dp)               # alpha'
    v = k * a                           # unfolded offset from x=1 at the middle interface
    r = v % 6
    ok = 0 < s and h0 * s < 2 and h3 * s < 1
    if 2 < r < 3:
        ok = ok and k % 6 in (0, 4)
    elif 3 < r < 4:
        ok = ok and k % 6 in (0, 2)
    else:
        ok = False
    p1, p2 = 1 + h0 * s, 1 + tri(v)
    # tier-2 offset from its left wall 3, then fold
    w = (r - 2 if r < 3 else r - 4) + s * (1 + y)
    p3 = 3 + tri(w)
    return ok, (p1, p2, p3), a, s


def crossing_x(r, level):
    xs = [e[1] for e in r['lv'] if e[3] == level]
    return xs[-1] if xs else None


def shoot(c, S, k, Dp, down, T, levels):
    g = gcd(k, Dp)
    d = (k // g, (-Dp if down else Dp) // g)
    r = trace(c, S, d, g, levels=True)
    reached = r['ok'] and r['end'] == (T[0], T[1])
    xs = [crossing_x(r, L) for L in levels]
    return reached, r['corner'], xs


# ------------------------------------------------------------------ 1. pins: no monotone chord
def pins():
    say("\n=== 1. Pins: alpha = 1/2 and 1/3 admit no monotone (h0=h3=1) chord")
    for al, per in ((F(1, 2), 12), (F(1, 3), 18)):
        bad = [k for k in range(1, per + 1)
               if (2 < (k * al) % 6 < 3 and k % 6 in (0, 4)) or (3 < (k * al) % 6 < 4 and k % 6 in (0, 2))]
        check(not bad, f"alpha={al}: every residue k mod {per} fails the Lemma M test "
                       f"(k*alpha mod 6 depends only on k mod {per})")
    # which corner each candidate hits at alpha = 1/2 (k=4,6) and 1/3 (k=6,12)
    check(1 + tri(F(6, 2)) == 4 and 1 + tri(F(4, 2)) == 3, "alpha=1/2: k=6 lands on corner x=4, k=4 on corner x=3")
    check(1 + tri(F(6, 3)) == 3 and 1 + tri(F(12, 3)) == 3, "alpha=1/3: k=6 and k=12 both land on corner x=3")


# ------------------------------------------------------------------ 2. windows cover [1/4, 2/3]
def windows():
    say("\n=== 2. Macro windows (monotone, h0=h3=1)")
    def win(k, lo_case):
        """alpha-interval where k*alpha lies in (n, n+1) with the given n."""
        n = lo_case
        return (F(n, k), F(n + 1, k))
    W = {"k=6 A": win(6, 2), "k=6 B": win(6, 3), "k=12 B": win(12, 3), "k=10 A": win(10, 2), "k=4 A": win(4, 2)}
    check(W["k=6 A"] == (F(1, 3), F(1, 2)) and W["k=6 B"] == (F(1, 2), F(2, 3)), "k=6: A on (1/3,1/2), B on (1/2,2/3)")
    check(W["k=12 B"] == (F(1, 4), F(1, 3)) and 12 % 6 == 0, "k=12 (=0 mod 6): B on (1/4,1/3)")
    check(W["k=10 A"] == (F(1, 5), F(3, 10)) and 10 % 6 == 4, "k=10 (=4 mod 6): A on (1/5,3/10), contains 1/4")
    check(W["k=4 A"] == (F(1, 2), F(3, 4)) and 4 % 6 == 4, "k=4 (=4 mod 6): A on (1/2,3/4), contains 2/3")
    # cover of [1/4,2/3]: open windows plus the two pin points 1/3, 1/2 handled by bounces
    opens = [W["k=10 A"], W["k=12 B"], W["k=6 A"], W["k=6 B"], W["k=4 A"]]
    pts = [F(1, 3), F(1, 2)]
    ends = sorted({e for iv in opens for e in iv} | set(pts) | {F(1, 4), F(2, 3)})
    probe = [e for e in ends if F(1, 4) <= e <= F(2, 3)]
    probe += [(u + v) / 2 for u, v in zip(probe, probe[1:])]
    cov = lambda t: t in pts or any(a < t < b for a, b in opens)
    check(all(cov(t) for t in probe), "windows + {1/3,1/2} cover [1/4,2/3] (all endpoints and gap midpoints tested)")
    check([t for t in ends if F(1, 4) <= t <= F(2, 3) and not any(a < t < b for a, b in opens)] == pts,
          "the only points of [1/4,2/3] outside every open window are 1/3 and 1/2")
    # region translations (a=1): alpha in (1/4,1/3) <=> 2x+2 < y < 3x+4 etc., checked as linear identities
    D = lambda x, y: 4 + x + y
    al = lambda x, y: F(2 + x, D(x, y))
    pts3 = [(F(0), F(0)), (F(1), F(0)), (F(0), F(1)), (F(3, 7), F(5, 2))]
    check(all((3 * (2 + x) - D(x, y)) == (2 * x + 2 - y) for x, y in pts3), "3(2+x)-D = 2x+2-y (alpha>1/3 <=> y<2x+2)")
    check(all((4 * (2 + x) - D(x, y)) == (3 * x + 4 - y) for x, y in pts3), "4(2+x)-D = 3x+4-y (alpha>1/4 <=> y<3x+4)")
    check(all((2 * (2 + x) - D(x, y)) == (x - y) for x, y in pts3), "2(2+x)-D = x-y (alpha=1/2 <=> x=y)")
    check(all((2 * D(x, y) - 3 * (2 + x)) == (2 - x + 2 * y) for x, y in pts3), "2D-3(2+x) = 2+2y-x (alpha<2/3 <=> x<2y+2)")


# ------------------------------------------------------------------ 3. pin lines via end bounces
def pin_lines():
    say("\n=== 3. Pin lines: micro shift by an end-tier bounce")
    xs = [F(0), F(1), F(5, 3), F(10), F(97, 4)]     # degree-<=2 identities: 3+ points suffice
    # alpha=1/2 (x=y): floor bounce alpha' = (4+x)/(6+2x) = 1/2 + 1/(6+2x)
    check(all(F(4 + x, 6 + 2 * x) == F(1, 2) + 1 / (6 + 2 * x) for x in xs), "x=y: alpha' = 1/2 + 1/(6+2x)")
    check(all(F(1, 2) < F(4 + x, 6 + 2 * x) < F(3, 4) for x in xs), "x=y: alpha' in (1/2,3/4) for x>=0 (k=4, case A)")
    check(all((F(4, 6 + 2 * x) < F(2, 3)) == (x > 0) for x in xs), "x=y: sigma=4/(6+2x) < 2/3 <=> x>0")
    check(all((1 + 4 * F(4 + x, 6 + 2 * x)) - 3 == F(2, 3 + x) for x in xs),
          "x=y, floor k=4: middle crossing = 3 + 2/(3+x), clearance 2/(3+x) from corner (3,3+x)")
    # alpha=1/3 (y=2x+2): floor alpha' = (4+x)/(8+3x)
    check(all(F(4 + x, 6 + x + (2 * x + 2)) == F(4 + x, 8 + 3 * x) for x in xs), "y=2x+2: alpha' = (4+x)/(8+3x)")
    check(all(F(1, 3) < F(4 + x, 8 + 3 * x) < F(1, 2) for x in xs if x > 0), "y=2x+2, x>0: alpha' in (1/3,1/2) (k=6, A)")
    check(all((F(6, 8 + 3 * x) < F(2, 3)) == (x > F(1, 3)) for x in xs + [F(1, 3)]), "y=2x+2: sigma=6/(8+3x)<2/3 <=> x>1/3")
    check(all(6 * F(4 + x, 8 + 3 * x) - 2 == F(8, 8 + 3 * x) for x in xs),
          "y=2x+2, floor k=6: crossing offset past corner (3,3+x) = 8/(8+3x)")
    # micro shift formulas: floor adds 2 to N and D, roof adds 2 to D only
    ok_f = ok_r = True
    for N, D in ((F(3), F(7)), (F(5), F(11)), (F(12), F(36)), (F(7, 2), F(9)), (F(40), F(41))):
        for k in (4, 6, 10):
            sp = F(k) / (D + 2)
            ok_f &= (k * (N + 2) / (D + 2) - k * N / D) / sp == 2 * (1 - N / D)
            ok_r &= (k * N / (D + 2) - k * N / D) / sp == -2 * N / D
    check(ok_f, "floor bounce shifts every interface crossing by +2(1-alpha_i) micro units (sigma'=k/(D+2))")
    check(ok_r, "roof bounce shifts every interface crossing by -2 alpha_i micro units")
    # micro coordinate at the 1/2 pin, k=6: offset = 3(h0-h3+x-y)/D'
    ok = True
    for x, y in ((F(10), F(10)), (F(3), F(5)), (F(7, 3), F(1, 2))):
        for h0, h3 in ((1, 1), (3, 1), (1, 3), (3, 3)):
            Dp = h0 + h3 + 2 + x + y
            ok &= 6 * F(h0 + 1 + x) / Dp - 3 == 3 * (h0 - h3 + x - y) / Dp
    check(ok, "k=6 at the 1/2 pin: offset from x=4 is 3(h0-h3+x-y)/D', so mu=(x-y+h0-h3)/2")


# ------------------------------------------------------------------ 4. Theorem B (alpha > 2/3) inequalities
def theorem_b():
    say("\n=== 4. Theorem B inequalities (alpha in (2/3,1); proof only, no traces)")
    check((F(9, 12), F(10, 12)) == (F(3, 4), F(5, 6)), "k=12, B (12 alpha in (9,10)): (3/4,5/6)")
    check((F(8, 10), F(9, 10)) == (F(4, 5), F(9, 10)), "k=10, A (10 alpha in (8,9)): (4/5,9/10) contains 5/6")
    # k = 4 mod 6, k*beta in (1,2), beta<1/6: (4 - k beta) mod 6 in (2,3) and sigma < 2/(2+y) <= 1
    ok = True
    for kb in (F(11, 10), F(3, 2), F(19, 10)):
        ok &= 2 < (4 - kb) % 6 < 3
    check(ok, "k=4 mod 6 with k*beta in (1,2): k*alpha mod 6 = (4-k*beta) mod 6 in (2,3)")
    check(F(1) / F(1, 6) == 6, "beta<1/6 => interval (1/beta,2/beta) longer than 6, contains every residue")
    xs = [F(0), F(1), F(3), F(20)]
    # alpha = 3/4: x = 3y+4; roof alpha'' = (2+x)/(6+x+y) = (6+3y)/(10+4y)
    check(all(F(1, 2) < F(6 + 3 * y, 10 + 4 * y) < F(3, 4) for y in xs), "alpha=3/4, roof: alpha'' in (1/2,3/4)")
    check(all((3 * F(4, 10 + 4 * y) < 1) == (y > F(1, 2)) for y in xs + [F(1, 2)]), "alpha=3/4, roof: 3 sigma < 1 <=> y > 1/2")
    # small x, alpha<1/4: floor bounce, k = 0,4 mod 6 in (2/a', (8+2x)/(3a')), length >= 2/(3a') > 4 iff a'<1/6
    check(all((F(4 + x, 6 + x + y) < F(1, 6)) == (y > 18 + 5 * x) for x in (F(0), F(1, 2)) for y in (F(18), F(19), F(23), F(24))),
          "floor alpha' < 1/6 <=> y > 18+5x")
    check(max(b - a for a, b in ((0, 4), (4, 6))) == 4, "max gap of residues {0,4} mod 6 is 4")


# ------------------------------------------------------------------ 5. small-room bookkeeping in Z (no traces)
def small():
    say("\n=== 5. Lattice points of Z with x+y<=8: rule bookkeeping (inequalities only, no traces)")
    def rules(x, y):
        out = []
        for h0, h3, k in ((1, 1, 6), (1, 1, 12), (1, 1, 10), (1, 1, 4), (3, 1, 4), (3, 1, 6)):
            if lemma_m(F(x), F(y), h0, h3, k)[0]:
                out.append((h0, h3, k))
        return out
    Z = [(x, y) for x in range(9) for y in range(9 - x) if y <= 3 * x + 4 and x <= 2 * y + 2]
    resid = [p for p in Z if not rules(*p)]
    check(resid == [(0, 0), (0, 2), (0, 3)],
          f"{len(Z)} lattice points; uncovered by the note's rules: {resid} (areas {[3 * (6 + x + y) for x, y in resid]})")


# ------------------------------------------------------------------ 6. exact traces at 5 points
def traces():
    say("\n=== 6. Exact traces (5 hand-picked points)")
    cases = [
        # (label, x, y, h0, h3, k, expect_legal)
        ("P1 (10,10) floor k=4", 10, 10, 3, 1, 4, True),
        ("P1 (10,10) roof k=6", 10, 10, 1, 3, 6, True),
        ("P1 (10,10) monotone k=6", 10, 10, 1, 1, 6, False),
        ("P1 (10,10) monotone k=4", 10, 10, 1, 1, 4, False),
        ("P2 (10,22) floor k=6", 10, 22, 3, 1, 6, True),
        ("P2 (10,22) monotone k=6", 10, 22, 1, 1, 6, False),
        ("P2 (10,22) monotone k=12", 10, 22, 1, 1, 12, False),
        ("P3 (10,30) monotone k=12", 10, 30, 1, 1, 12, True),
        ("P4 (10,34) monotone k=10", 10, 34, 1, 1, 10, True),
    ]
    for lab, x, y, h0, h3, k, exp in cases:
        c = stair_room(x, y)
        S, T = (1, 1), (5, 5 + x + y)
        Dp = h0 + h3 + 2 + x + y
        ok, pred, a, s = lemma_m(F(x), F(y), h0, h3, k)
        reached, corner, xs = shoot(c, S, k, Dp, h0 == 3, T, (2, 3 + x, 4 + x + y))
        match = (not exp) or xs == list(pred)
        check(ok == exp and reached == exp and match,
              f"{lab}: alpha'={a}, sigma={s}; Lemma M {ok}, trace reaches T {reached}"
              + (f", crossings {[str(v) for v in xs]} = predicted" if exp else f", corner hit {corner}"))
    # P5: rational gains x=y=1/2 via y-scaling q=2; floor bounce k=4; scaled D' = 2*(6+1/2+1/2) = 14
    q, p, r = 2, 1, 1
    c = stair_q(p, r, q)
    S, T = (1, q), (5, 5 * q + p + r)
    ok, pred, a, s = lemma_m(F(p, q), F(r, q), 3, 1, 4)
    reached, corner, xs = shoot(c, S, 4, 14, True, T, (2 * q, 3 * q + p, 4 * q + p + r))
    check(ok and reached and xs == list(pred),
          f"P5 (1/2,1/2) floor k=4 (y scaled by 2): alpha'={a}, sigma={s}; reaches T {reached}; crossings {[str(v) for v in xs]}")
    check(len(c) == 3 * 2 * (6 * q + p + r) // 2 and len(stair_room(10, 10)) == 78, "room areas: P5 scaled 42 cells, P1 78")


if __name__ == '__main__':
    pins()
    windows()
    pin_lines()
    theorem_b()
    small()
    traces()
    say(f"\ncpu {time.process_time() - T0:.1f}s")
    say(f"FAILURES: {len(FAILS)}" + (f" ({FAILS})" if FAILS else ""))
