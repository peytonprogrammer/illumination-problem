"""d160 referee checks for skeleton-decidability (snapshot 2026-11-22 04:55)
and the chart-coverage section of time-pairing (snapshot 2026-11-22 04:55).

Exact rational arithmetic throughout. The polygon builder, d159 tracer, piece()
and build_chart() are loaded unchanged from d159-review-timepair/checks.py
(everything above its section-2 driver). Named rooms only: R22-base,
R22-L1-005 (d8 rooms.json) and the note's 6-wall L family L(x,y,z).
Run: python3 -B checks.py > checks.log
"""
import time
from fractions import Fraction as F
from itertools import combinations
from math import gcd
from pathlib import Path

T0 = time.process_time()
D159 = Path(__file__).resolve().parent.parent / "d159-review-timepair" / "checks.py"
src = D159.read_text()
cut = src.index('log("# 2. R22 chart')
G = {"__file__": str(D159), "__name__": "d159lib"}
exec(compile(src[:cut], str(D159), "exec"), G)
polygon, trace, piece, status, ROOMS = G["polygon"], G["trace"], G["piece"], G["status"], G["ROOMS"]
build_chart, I_S = G["build_chart"], G["I_S"]


def log(*a):
    print(*a, flush=True)


def fr(p):
    return f"({p[0]}, {p[1]})"


# ---------------------------------------------------------------- exact tracer that also detects T
def walls_of(P):
    n = len(P)
    return [(P[i], P[(i + 1) % n]) for i in range(n)]


def trace_to(P, S, T, d, maxrefl):
    """Ray from S in integer direction d (p,q both nonzero). Returns (outcome, reflections, wall list).
    outcome: 'T' (reaches T before any further event), 'corner', 'limit'."""
    p, q = d
    assert p and q
    W = walls_of(P)
    V = set(P)
    X, Y = F(S[0]), F(S[1])
    vx, vy = F(p), F(q)
    hit_walls = []
    for k in range(maxrefl + 1):
        best = None
        for i, (a, b) in enumerate(W):
            if a[0] == b[0]:                       # vertical wall x = a0
                if vx == 0: continue
                t = (a[0] - X) / vx
                yy = Y + vy * t
                if t > 0 and min(a[1], b[1]) <= yy <= max(a[1], b[1]) and (best is None or t < best[0]):
                    best = (t, i, 'v')
            else:
                if vy == 0: continue
                t = (a[1] - Y) / vy
                xx = X + vx * t
                if t > 0 and min(a[0], b[0]) <= xx <= max(a[0], b[0]) and (best is None or t < best[0]):
                    best = (t, i, 'h')
        t, i, kind = best
        # does the open segment reach T first?
        tT = None
        if vx != 0:
            tT = (T[0] - X) / vx
        if tT is not None and 0 < tT < t and Y + vy * tT == T[1]:
            return 'T', k, hit_walls
        X, Y = X + vx * t, Y + vy * t
        if (X, Y) in V:
            return 'corner', k, hit_walls
        hit_walls.append(i)
        if kind == 'v': vx = -vx
        else: vy = -vy
    return 'limit', maxrefl, hit_walls


# ================================================================== 1. chart coverage, R22 replay
log("# 1. Chart coverage: R22 launch (2,3) from (0,0)")
R22, L105 = ROOMS["R22-base"], ROOMS["R22-L1-005"]
PR, PL = polygon(R22), polygon(L105)
r = trace(PR, (0, 0), (2, 3), maxrefl=6)
log(f"   d159 tracer poly: {[fr(p) for p in r['poly']]}  end event: {r['event']}")
for pt in r['poly'][1:3]:
    log(f"   contact {fr(pt)}: lattice status {status(R22, (int(pt[0]), int(pt[1])))}; "
        f"vertex of R22: {(int(pt[0]), int(pt[1])) in set(PR)}")
p3 = r['poly'][3]
on_h = [(a, b) for a, b in walls_of(PR) if a[1] == b[1] == p3[1] and min(a[0], b[0]) < p3[0] < max(a[0], b[0])]
log(f"   third contact {fr(p3)} lies in the open horizontal wall {on_h}")
# events on vertical cuts x = k along the first three legs; flips of vertical velocity at contacts
poly = r['poly']
for j, (A, B) in enumerate(zip(poly[:3], poly[1:4])):
    for k in range(int(A[0]) + 1, int(B[0]) + 1):
        yk = A[1] + (B[1] - A[1]) * (k - A[0]) / (B[0] - A[0])
        pc = piece(R22, k, yk)
        flip = ""
        if (F(k), yk) == B:
            C = poly[j + 2]
            flip = f"; vertical velocity {'+' if B[1] > A[1] else '-'} -> {'+' if C[1] > B[1] else '-'}"
        log(f"   x={k}: y={yk}  " + (f"cut interior (piece {str(pc[0])},{str(pc[1])})" if pc else "cut endpoint") + flip)
# local germ rule at the two cut-endpoint contacts
for (P0, inc, out) in (((2, 3), (1, 2), (2, 2)), ((4, 0), (3, 0), (4, 0))):
    log(f"   germ rule at {P0}: incoming cell {inc} in room {inc in R22}; outgoing cell {out} in room "
        f"{out in R22}; reflected cells above/below wall: {(P0[0]-1, P0[1]) in R22 or (P0[0], P0[1]) in R22}"
        f"/{(P0[0]-1, P0[1]-1) in R22 or (P0[0], P0[1]-1) in R22}")
ch, why = build_chart(R22, PR, (0, 0), (2, 3), 4)
log(f"   strict column chart for this ray: {why}")

# small consistency sweep in the named room R22: every contact of a traced ray is classified by
# the note's local rule exactly as the tracer treats it, and some smooth contacts end a cut.
n_smooth, n_cutend, n_vertex, bad = 0, 0, 0, []
Vs = set(PR)
for p in range(-3, 4):
    for q in range(-4, 5):
        if not p or not q or gcd(p, q) != 1: continue
        rr = trace(PR, (0, 0), (p, q), maxrefl=8)
        for j, pt in enumerate(rr['poly'][1:], 1):
            lat = pt[0].denominator == 1 and pt[1].denominator == 1
            st = status(R22, (int(pt[0]), int(pt[1]))) if lat else None
            is_last = j == len(rr['poly']) - 1
            if lat and st in ("convex", "reflex"):
                n_vertex += 1
                if not (is_last and rr['event'] == 'corner'): bad.append((p, q, pt, st))
            else:
                n_smooth += 1
                if lat and st == "smooth": n_cutend += 1
                if is_last and rr['event'] == 'corner': bad.append((p, q, pt, st))
log(f"   sweep from (0,0) in R22, |p|<=3, |q|<=4, 8 reflections: smooth contacts {n_smooth} "
    f"(of which at lattice smooth points, i.e. cut endpoints, {n_cutend}); vertex stops {n_vertex}; "
    f"disagreements with local rule {bad}")

# side check: the 'Comparison at the edited door' interval claim in R22-L1-005
log("\n# 1c. Physical-word slope intervals in R22-L1-005: archived word (18,-12) and d159 witness (-24,-16)")


def wall_word(P, S, d, D):
    rr = trace(P, S, d, maxrefl=200)
    poly, u, word = rr['poly'], F(0), []
    for A, B in zip(poly, poly[1:]):
        du = abs(B[0] - A[0])
        if u + du >= D:
            return word, True
        u += du
        if B == poly[-1] and rr['event'] == 'corner':
            return word, False
        wl = [i for i, (a, b) in enumerate(walls_of(P))
              if (a[0] == b[0] == B[0] and min(a[1], b[1]) < B[1] < max(a[1], b[1]))
              or (a[1] == b[1] == B[1] and min(a[0], b[0]) < B[0] < max(a[0], b[0]))]
        word.append(wl[0])
    return word, False


for d0, D0 in (((3, -2), 18), ((-3, -2), 24)):
    w0, ok0 = wall_word(PL, (0, 0), d0, D0)
    chw, why = build_chart(L105, PL, (0, 0), d0, D0)
    log(f"   direction {d0}, D={D0}: physical word length {len(w0)}, reaches section: {ok0}; "
        f"column-chart I_S = {I_S(chw) if chw else why}")
    sg = 1 if d0[0] > 0 else -1
    for s in (F(-11, 16), F(-11, 16) + F(1, 1000), F(-15, 22), F(-15, 22) + F(1, 10000),
              F(-15, 23) - F(1, 10000), F(-15, 23), F(-11, 17) - F(1, 1000), F(-11, 17)):
        d = (sg * s.denominator, s.numerator)
        w, ok = wall_word(PL, (0, 0), d, D0)
        log(f"     slope {s} ({float(s):.5f}): reaches section {ok}, same physical word {ok and w == w0}")
    rR = trace(PR, (0, 0), d0, maxrefl=60)
    log(f"     same direction in R22 ends: {rR['event']} at {fr(rR['poly'][-1])}")

# ================================================================== 2. six-wall L family
log("\n# 2. Six-wall L(x,y,z): rectangle [-x-2,z+1]x[-2,y+1] minus open NE quadrant, S=(-x,y), T=(z,-1)")


def Lcells(x, y, z):
    return {(i, j) for i in range(-x - 2, z + 1) for j in range(-2, y + 1) if not (i >= 0 and j >= 0)}


def Lpoly(x, y, z):
    P = polygon(Lcells(x, y, z))
    assert len(P) == 6
    return P


def reflect(T, a, b):
    if a[0] == b[0]: return (2 * a[0] - T[0], T[1])
    return (T[0], 2 * a[1] - T[1])


NAMES = None


def wall_name(a, b, x, y, z):
    if a[1] == b[1] == -2: return "bottom"
    if a[1] == b[1] == y + 1: return "top"
    if a[0] == b[0] == -x - 2: return "left"
    if a[0] == b[0] == z + 1: return "right"
    if a[1] == b[1] == 0: return "notch-h"
    return "notch-v"


def le1(x, y, z):
    """All <=1-reflection shots S->T by direct tracing toward T and its 6 wall images."""
    P = Lpoly(x, y, z)
    S, T = (-x, y), (z, -1)
    res = {}
    cands = [("direct", T)] + [(wall_name(a, b, x, y, z), reflect(T, a, b)) for a, b in walls_of(P)]
    for name, Ti in cands:
        dx, dy = Ti[0] - S[0], Ti[1] - S[1]
        if dx == 0 or dy == 0:
            res[name] = False; continue
        g = gcd(abs(dx), abs(dy))
        out, k, hw = trace_to(P, S, T, (dx // g, dy // g), maxrefl=1)
        if name == "direct":
            res[name] = out == 'T' and k == 0
        else:
            res[name] = out == 'T' and k == 1 and wall_name(*walls_of(P)[hw[0]], x, y, z) == name
    return res


cond = {
    "direct": lambda x, y, z: z * y < x,
    "bottom": lambda x, y, z: z * y < 3 * x,
    "left": lambda x, y, z: z * y < x + 4,
    "right": lambda x, y, z: (z + 2) * y < x,
    "top": lambda x, y, z: z * (y + 2) < x,
}
odd = range(1, 16, 2)
n, mism, nec_fail, notch_lit, newbeyond = 0, [], [], [], []
exact_iff = {k: True for k in cond}
for x in range(3, 16, 2):
    for y in odd:
        for z in odd:
            n += 1
            rs = le1(x, y, z)
            lit = any(rs.values())
            if lit != (z * y < 3 * x): mism.append((x, y, z, rs))
            for k, f in cond.items():
                if rs[k] != f(x, y, z): exact_iff[k] = False
                if rs[k] and not (z * y < 3 * x): nec_fail.append((k, x, y, z))
            if rs["notch-h"] or rs["notch-v"]: notch_lit.append((x, y, z))
            if lit and not rs["bottom"]: newbeyond.append((x, y, z, rs))
log(f"   grid x in 3..15, y,z in 1..15 (odd): {n} rooms; lit(<=1 refl) <=> zy<3x fails in {len(mism)}: {mism[:3]}")
log(f"   shots lit by a wall other than bottom where bottom fails: {newbeyond[:3]} (count {len(newbeyond)})")
log(f"   notch walls ever give a shot: {notch_lit[:3]}; a wall condition outside zy<3x: {nec_fail[:3]}")
log(f"   stated wall condition is the exact iff on the grid: {exact_iff}")
# boundary cases singled out by the note
for (x, y, z, why) in ((9, 3, 3, "zy = x: chord through reflex"), (15, 5, 3, "zy = x"),
                       (3, 3, 3, "zy = 3x: bottom image chord through reflex"), (5, 3, 5, "zy = 3x"),
                       (3, 1, 1, "x = z(y+2): bottom bounce at x=0"), (15, 3, 3, "x = z(y+2)")):
    rs = le1(x, y, z)
    log(f"   L({x},{y},{z}) [{why}]: {dict((k, v) for k, v in rs.items() if v) or 'no <=1 shot'}")
# is x >= 3 needed?
x1 = [(y, z, le1(1, y, z)) for y in odd for z in odd]
bad1 = [(y, z, [k for k, v in rs.items() if v]) for y, z, rs in x1 if any(rs.values()) != (z * y < 3)]
log(f"   x = 1 (excluded by the note): rooms where lit != (zy<3): {bad1}")

# ================================================================== 3. Presburger slices
log("\n# 3. Slices")
rows = []
for y in range(1, 42, 2):
    xs = [x for x in range(max(3, y * y // 3 - 6) | 1, y * y // 3 + 8, 2) if x >= 3]
    lit = [x for x in xs if any(le1(x, y, y).values())]
    dark = [x for x in xs if not any(le1(x, y, y).values())]
    xmin = min(lit)
    ok = all(xx < xmin for xx in dark) and all(xx >= xmin for xx in lit)
    rows.append((y, xmin, ok, xmin == min(x for x in range(3, 10**6, 2) if y * y < 3 * x)))
log("   z=y: least odd x>=3 with a <=1-reflection shot (traced near the threshold), monotone, equals least odd x with y^2<3x")
log("   " + "; ".join(f"y={y}:{xm}" for y, xm, _, _ in rows))
log(f"   threshold monotone in x for all y<=41: {all(r[2] for r in rows)}; equals y^2<3x formula: {all(r[3] for r in rows)}")
# note's slice y=z=6b+3, x=2c+1: least c = 6b^2+6b+2
sl = []
for b in range(0, 4):
    y = 6 * b + 3
    xs = [x for x in range(3, y * y // 3 + 8, 2)]
    lo = (y * y // 3 - 6) | 1
    xs = [x for x in xs if x >= max(3, lo)]
    lit = [x for x in xs if any(le1(x, y, y).values())]
    cmin = (min(lit) - 1) // 2
    sl.append((b, y, cmin, 6 * b * b + 6 * b + 2))
log(f"   y=z=6b+3: (b, y, traced least c, 6b^2+6b+2) = {sl}")
# direct-shot slice z=y=2b+1: least c with zy<x is 2b^2+2b+1
ds = []
for b in range(0, 5):
    y = 2 * b + 1
    xs = range(max(3, y * y - 6) | 1, y * y + 8, 2)
    lit = [x for x in xs if le1(x, y, y)["direct"]]
    ds.append((b, (min(lit) - 1) // 2, 2 * b * b + 2 * b + 1))
log(f"   direct shot, y=z=2b+1: (b, traced least c, 2b^2+2b+1) = {ds}")
# no three collinear points on the graph c(b) = 6b^2+6b+2 (second difference 12), hence no infinite AP
sd = {(6 * (b + 2) ** 2 + 6 * (b + 2) + 2) - 2 * (6 * (b + 1) ** 2 + 6 * (b + 1) + 2) + (6 * b * b + 6 * b + 2)
      for b in range(1000)}
log(f"   second differences of 6b^2+6b+2 over b<1000: {sd}")

# ================================================================== 4. turn-skeleton count
log("\n# 4. Turn skeletons: binary bracelets of length n=2r+4, weight r")


def burnside(r):
    n = 2 * r + 4
    # coefficient of u^r in the note's formula
    def coeff_pow(k, e, m):          # [u^m] (1+u^k)^e
        return 0 if m % k else (lambda j: __import__('math').comb(e, j) if 0 <= j <= e else 0)(m // k)
    tot = 0
    for i in range(n):
        g = gcd(n, i)
        tot += coeff_pow(n // g, g, r)
    tot += (n // 2) * coeff_pow(2, n // 2, r)
    # (1+u)^2 (1+u^2)^((n-2)/2)
    e = (n - 2) // 2
    tot += (n // 2) * sum(__import__('math').comb(2, a) * coeff_pow(2, e, r - a) for a in range(3) if r - a >= 0)
    assert tot % (2 * n) == 0
    return tot // (2 * n)


def brute(r):
    n = 2 * r + 4
    seen = set()
    for pos in combinations(range(n), r):
        w = [0] * n
        for p in pos: w[p] = 1
        forms = []
        for s in range(n):
            rot = tuple(w[s:] + w[:s])
            forms.append(rot); forms.append(rot[::-1])
        seen.add(min(forms))
    return len(seen)


bc = [burnside(r) for r in range(9)]
bf = [brute(r) for r in range(9)]
log(f"   Burnside r=0..8: {bc}, total {sum(bc)}; brute force: {bf}, total {sum(bf)}")

log(f"\nTotal CPU: {time.process_time() - T0:.1f}s")
