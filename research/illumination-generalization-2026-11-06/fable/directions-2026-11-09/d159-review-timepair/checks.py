"""d159 referee checks for time-pairing (snapshot 2026-11-22 04:35).

Exact rational arithmetic. Tracer and cell->polygon builder copied from
d158-review-simdoor/checks.py (every vertex, convex or reflex, stops the ray).
Rooms: R22-base and R22-L1-005 (cells from d8 rooms.json), DB55 (d157 cells).
d8's tracer/decider are imported unchanged for the litness cross-check.

Chart model used here (column chart): cut the room by every line x = k. A chart
is the sequence, for u = 1..D (u = absolute horizontal travel), of the open
piece of x = k met by the ray (door piece, or wall piece for a vertical-wall
bounce) and the sheet map y = eps*v + c that relates developed height v to
physical height y. v is normalised so that v = physical y near S (eps_0 = +1),
hence s = dv/du is the initial physical dy/|dx|. Floor and ceiling bounces are
implied by consecutive windows on fixed sheets.
I_S = {s : s*u in W_u for u = 1..D}, W_D = final chamber cross-section.
I_T = {s : vT + s(u-D) in W_u for u = 0..D-1}, W_0 = first chamber cross-section.
Run: python3 -B checks.py > checks.log
"""
import json
import sys
import time
from fractions import Fraction as F
from math import gcd
from pathlib import Path

T0 = time.process_time()
HERE = Path(__file__).resolve().parent
ARCH = HERE.parent
sys.path.insert(0, str(ARCH / "d8-perturbation-test"))
from tracer import certify as d8_certify, trace as d8_trace   # noqa: E402
from decider import decide, regular_points                    # noqa: E402
from room import status                                       # noqa: E402

ROOMS = {r["id"]: {tuple(c) for c in r["cells"]} for r in
         json.load(open(ARCH / "d8-perturbation-test" / "rooms.json"))}


def log(*a):
    print(*a, flush=True)


# ------------------------------------------------------------ copied from d158
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


def trace(P, S, d, maxrefl=400):
    """Exact shot from lattice point S, integer direction d=(p,q), p,q != 0. Stops at any vertex."""
    p, q = d
    assert p and q
    kx, ky = abs(q), abs(p)
    V = [(kx * x, ky * y) for x, y in P]
    n = len(V)
    hw = [(V[i], V[(i + 1) % n]) for i in range(n) if V[i][1] == V[(i + 1) % n][1]]
    vw = [(V[i], V[(i + 1) % n]) for i in range(n) if V[i][0] == V[(i + 1) % n][0]]
    vset = set(V)
    X, Y = kx * S[0], ky * S[1]
    sx, sy = (1 if p > 0 else -1), (1 if q > 0 else -1)
    poly = [(F(X, kx), F(Y, ky))]
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
        X, Y = X + sx * t, Y + sy * t
        poly.append((F(X, kx), F(Y, ky)))
        if (X, Y) in vset:
            return dict(event='corner', stop=poly[-1], poly=poly)
        if kind == 'v': sx = -sx
        else: sy = -sy
    return dict(event='limit', stop=None, poly=poly)


# ------------------------------------------------------------ column charts
def run_range(cells, col, y):
    """Open y-range of the chamber in column col (cells (col, m)) containing height y."""
    m = int(y) if y == int(y) else int(y // 1)
    if (col, m) not in cells:
        m -= 1
    assert (col, m) in cells
    lo, hi = m, m + 1
    while (col, lo - 1) in cells: lo -= 1
    while (col, hi) in cells: hi += 1
    return (F(lo), F(hi))


def piece(cells, k, y):
    """Open piece of the line x=k with constant (left, right) cell pattern containing y,
    or None if y is a vertex or the endpoint of a piece (e.g. smooth horizontal-wall point)."""
    pat = lambda m: ((k - 1, m) in cells, (k, m) in cells)
    if y.denominator == 1:
        yi = int(y)
        if pat(yi - 1) != pat(yi):
            return None
        m = yi
    else:
        m = int(y // 1)
    p0 = pat(m)
    lo, hi = m, m + 1
    while pat(lo - 1) == p0: lo -= 1
    while pat(hi) == p0: hi += 1
    return (F(lo), F(hi), p0)


def walk(poly, D):
    """Integer-x events up to horizontal travel D: list of (u, point, vy_sign, vx_sign_after)."""
    ev, u = [], F(0)
    segs = list(zip(poly, poly[1:]))
    for i, (A, B) in enumerate(segs):
        dx = B[0] - A[0]
        sxs = 1 if dx > 0 else -1
        vy = 1 if B[1] > A[1] else -1
        k = A[0]
        # integer x strictly after A up to and including B
        xs = []
        if k.denominator != 1:
            x = F(int(k // 1) + (1 if sxs > 0 else 0))
        else:
            x = k + sxs
        while (x - B[0]) * sxs <= 0:
            xs.append(x); x += sxs
        for x in xs:
            uu = u + abs(x - A[0])
            if uu > D:
                return ev
            lam = (x - A[0]) / dx
            pt = (x, A[1] + lam * (B[1] - A[1]))
            ev.append((uu, pt, vy, sxs))
        u += abs(dx)
        if u >= D:
            break
    return ev


def build_chart(cells, P, S, d, D):
    """Column chart of the ray from S in direction d, up to horizontal travel D.
    Returns dict or None (with reason) if the reference ray fails before D."""
    r = trace(P, S, d, maxrefl=60 * D + 50)
    ev = walk(r['poly'], D)
    if not ev or ev[-1][0] != D:
        return None, f"reference ray stops ({r['event']} {r['stop']}) before u={D}"
    s_ref = F(d[1], abs(d[0]))
    sg = 1 if s_ref > 0 else -1
    col0 = S[0] if d[0] > 0 else S[0] - 1
    W, sheets = {}, {}
    W0 = run_range(cells, col0, F(S[1]))           # first chamber cross-section, sheet eps=+1, c=S_y
    W[0] = (W0[0] - S[1], W0[1] - S[1]); sheets[0] = (1, F(S[1]))
    for (u, pt, vy, sxs) in ev:
        u = int(u)
        eps = vy * sg
        v = s_ref * u
        c = pt[1] - eps * v
        if u < D:
            pc = piece(cells, int(pt[0]), pt[1])
            if pc is None:
                return None, f"reference ray meets a piece endpoint at u={u}, point {pt}"
            lo, hi, pat = pc
        else:
            colD = int(pt[0]) - 1 if sxs > 0 else int(pt[0])
            lo, hi = run_range(cells, colD, pt[1]); pat = None
        a, b = eps * (lo - c), eps * (hi - c)
        W[u] = (min(a, b), max(a, b)); sheets[u] = (eps, c)
        if u == D:
            xD = pt[0]
    return dict(W=W, sheets=sheets, D=D, S=S, sx0=(1 if d[0] > 0 else -1), xD=xD), None


def isect(ivs):
    lo = max(i[0] for i in ivs); hi = min(i[1] for i in ivs)
    return (lo, hi) if lo < hi else None


def I_S(ch):
    return isect([(ch['W'][u][0] / u, ch['W'][u][1] / u) for u in range(1, ch['D'] + 1)])


def vT_of(ch, T):
    eps, c = ch['sheets'][ch['D']]
    return eps * (T[1] - c)


def I_T(ch, vT):
    D = ch['D']
    return isect([((vT - ch['W'][u][1]) / (D - u), (vT - ch['W'][u][0]) / (D - u)) for u in range(0, D)])


def inside(s, iv):
    return iv is not None and iv[0] < s < iv[1]


def fmt(iv):
    return "empty" if iv is None else f"({iv[0]}, {iv[1]})"


def ground_truth(cells, P, ch, T, s0):
    """Trace the chord direction; return (legal_at_D, same_chart)."""
    D = ch['D']
    d = (ch['sx0'] * s0.denominator, s0.numerator)
    r = trace(P, ch['S'], d, maxrefl=60 * D + 50)
    ev = walk(r['poly'], D)
    if not ev or ev[-1][0] != D or ev[-1][1] != (F(T[0]), F(T[1])):
        return False, False
    same = True
    for (u, pt, vy, sxs) in ev:
        u = int(u)
        eps, c = ch['sheets'][u]
        if u < D:
            pc = piece(cells, int(pt[0]), pt[1])
            if pc is None: return True, False      # smooth piece endpoint: legal but off-chart
            lo, hi = ch['W'][u]
            v = s0 * u
            if not (lo < v < hi) or eps * v + c != pt[1]: same = False
    return True, same


# ================================================================== 2. R22 example
log("# 2. R22 chart: S=(0,0) leftward, cap x=-1, upper opening (1,2) at x=1, T=(2,2), D=4")
R22, L105 = ROOMS["R22-base"], ROOMS["R22-L1-005"]
PR, PL = polygon(R22), polygon(L105)
S, T = (0, 0), (2, 2)
log(f"   R22 walls={len(PR)}; R22-L1-005 walls={len(PL)}; L1-005 minus R22 cells: {sorted(L105 - R22)}")
log(f"   status S,T in R22: {status(R22, S)}, {status(R22, T)}; in L1-005: {status(L105, S)}, {status(L105, T)}")
log(f"   vertex (1,2): R22 {status(R22, (1, 2))}, L1-005 {status(L105, (1, 2))}; "
    f"window endpoints (0,-1),(0,1),(1,1): {[status(R22, p) for p in ((0, -1), (0, 1), (1, 1))]}")
charts = {}
for name, cells, P in (("R22", R22, PR), ("R22-L1-005", L105, PL)):
    ch, why = build_chart(cells, P, S, (-8, 15), 4)
    assert ch, why
    charts[name] = ch
    vT = vT_of(ch, T)
    log(f"\n   [{name}] reference ray direction (-8,15) (s=15/8). windows W_u (developed v):")
    for u in range(0, 5):
        eps, c = ch['sheets'][u]
        log(f"     u={u}: W={fmt(ch['W'][u])}  sheet y = {eps:+d}*v + {c}")
    iS, iT = I_S(ch), I_T(ch, vT)
    s0 = vT / 4
    log(f"     vT = {vT}; s0 = {s0}; I_S = {fmt(iS)}; I_T = {fmt(iT)}; overlap = {isect([iS, iT]) if iS and iT else None}")
    log(f"     s0 in I_S: {inside(s0, iS)}, s0 in I_T: {inside(s0, iT)}; closures touch at 2: {iS[1] == iT[0] == 2}")
    # complementary windows (time pairing)
    for u in (1, 2):
        a, b = ch['W'][4 - u]
        refl = (vT - b, vT - a)
        log(f"     pairing u={u} vs {4 - u}: W_{u}={fmt(ch['W'][u])}, reflected W_{4 - u}={fmt(refl)}, "
            f"disjoint={isect([ch['W'][u], refl]) is None}")
    # broken line
    pts = [(0, F(0)), (1, F(9, 4)), (2, F(4)), (3, F(23, 4)), (4, F(8))]
    sym = all(pts[i][1] + pts[4 - i][1] == 8 for i in range(5))
    inw = all(ch['W'][u][0] < pts[u][1] < ch['W'][u][1] for u in range(1, 5))
    def cross(level, i):
        (t1, h1), (t2, h2) = pts[i], pts[i + 1]
        return t1 + (level - h1) / (h2 - h1)
    bt = [cross(1, 0), cross(3, 1), cross(7, 3)]
    log(f"     broken line symmetric about (2,4): {sym}; in all windows: {inw}; "
        f"bounce times at levels 1,3,7: {[str(x) for x in bt]} in (0,1),(1,2),(3,4): "
        f"{0 < bt[0] < 1 and 1 < bt[1] < 2 and 3 < bt[2] < 4}")
    # exact traces of the note's two displacements
    for d in ((-1, 2), (-8, 15)):
        r = trace(P, S, d)
        ev = walk(r['poly'], 4)
        at4 = [e[1] for e in ev if e[0] == 4]
        returns = [e[0] for e in walk(r['poly'], 4) if e[1] == (0, 0)]
        log(f"     own tracer d={d}: event {r['event']} stop {r['stop']}; point at u=4: {at4}; "
            f"back at S at u={[str(x) for x in returns]}; poly {[(str(a), str(b)) for a, b in r['poly'][:6]]}")
    for d in ((-4, 8), (-8, 15)):
        end, ok, vis = d8_trace(cells, S, d if d != (-8, 15) else (-4, F(15, 2)))
        log(f"     d8 tracer displacement {d if d != (-8, 15) else '(-4,15/2)'}: end {end}, ok {ok}, lattice pts visited {vis}")
log(f"\n   charts identical in both rooms: {charts['R22']['W'] == charts['R22-L1-005']['W'] and charts['R22']['sheets'] == charts['R22-L1-005']['sheets']}")
log("   physical column 0 range: R22 " + str(run_range(R22, 0, F(0))) + ", L1-005 " + str(run_range(L105, 0, F(0)))
    + " (note says (-2,2) for both; only the upper part is used)")

# ================================================================== 3. litness of L1-005
log("\n# 3. R22-L1-005 is lit for (0,0)-(2,2); R22 is dark")
wit = (24, -16)
log(f"   d8 certify L1-005 witness {wit}: {d8_certify(L105, S, T, wit)}; in R22: {d8_certify(R22, S, T, wit)}")
for name, cells in (("R22-L1-005", L105), ("R22", R22)):
    res = decide(cells, regular_points(cells), wanted=[(S, T)])
    lit = (S, T) in res['lit'] or (T, S) in res['lit']
    w = res['witness'].get((S, T)) or res['witness'].get((T, S))
    log(f"   d8 decider {name}: status {res['status']}, states {res['states']}, (0,0)-(2,2) lit {lit}, witness {w}")
wsg = d8_certify(L105, S, T, wit)
g = gcd(abs(wsg[0]), abs(wsg[1]))
dprim = (wsg[0] // g, wsg[1] // g)
for name, cells, P in (("R22-L1-005", L105, PL), ("R22", R22, PR)):
    r = trace(P, S, dprim)
    hitsT = [int(e[0]) for e in walk(r['poly'], 40) if e[1] == (F(2), F(2))]
    log(f"   own tracer {name} d={dprim}: event {r['event']} stop {r['stop']}; reaches T at u={hitsT[:3]}")
r = trace(PL, S, dprim)
Dw = [int(e[0]) for e in walk(r['poly'], 40) if e[1] == (F(2), F(2))][0]
newcell = [(str(a), str(b)) for a, b in r['poly'] if b == -3 and 0 < a < 1 and r['poly'].index((a, b)) <= 2 * Dw]
log(f"   L1-005 witness bounces on the new floor y=-3 with 0<x<1 (cell (0,-3)): {newcell[:3]}")
ch, why = build_chart(L105, PL, S, dprim, Dw)
log(f"   witness column chart, D={Dw}: {why or 'ok'}")
if ch:
    vT = vT_of(ch, T); s0 = vT / Dw
    iS, iT = I_S(ch), I_T(ch, vT)
    log(f"   vT={vT}, s0={s0}, I_S={fmt(iS)}, I_T={fmt(iT)}, s0 in both: {inside(s0, iS) and inside(s0, iT)}")
    ch2, why2 = build_chart(R22, PR, S, dprim, Dw)
    log(f"   same direction in R22: {why2 or 'chart ok'}")

# ================================================================== 1. lemma tests
log("\n# 1. Joint-interval lemma: three known DB55 shots, then an exhaustive chart/target check")
DB = cells_rect(0, 5, 0, 5) | cells_rect(5, 8, 2, 3) | cells_rect(8, 13, 0, 5)
PDB = polygon(DB)
S1, T1 = (1, 1), (9, 1)
known = []
for a in range(1, 13):
    for b in range(-40, 41):
        if b == 0 or gcd(a, b) != 1: continue
        for sx in (1, -1):
            d = (sx * a, b)
            r = trace(PDB, S1, d, maxrefl=300)
            ev = walk(r['poly'], 60)
            hit = [int(e[0]) for e in ev if e[1] == (F(9), F(1))]
            if hit:
                known.append((hit[0], d))
known.sort()
log(f"   DB55 S=(1,1) T=(9,1): legal shots with |dx-step|<=12, |dy-step|<=40 (first T arrival u): {len(known)}; "
    f"first five {known[:5]}; slope -37/8 present: {any(d == (8, -37) for _, d in known)}")
picks = [kd for kd in known if kd[1] == (8, -37)] + [kd for kd in known if kd[1] != (8, -37)][:2]
for D, d in picks:
    ch, why = build_chart(DB, PDB, S1, d, D)
    if not ch:
        log(f"   shot d={d} D={D}: chart not built: {why}"); continue
    vT = vT_of(ch, T1); s0 = vT / D
    iS, iT = I_S(ch), I_T(ch, vT)
    ov = isect([iS, iT]) if iS and iT else None
    log(f"   shot d={d}, D={D}: s0={s0} (= dy/|dx| {F(d[1], abs(d[0]))}); I_S={fmt(iS)}; I_T={fmt(iT)}; overlap={fmt(ov)}; "
        f"s0 in I_S {inside(s0, iS)}, in I_T {inside(s0, iT)}, in overlap {inside(s0, ov)}")

# exhaustive: reference rays from fixed sources, every D <= 10, every interior lattice target on the final section
def stress(name, cells, P, S, dirs, Dmax):
    n = agree = trivial = 0
    bad, offchart, nochart = [], 0, 0
    for d in dirs:
        for D in range(1, Dmax + 1):
            ch, why = build_chart(cells, P, S, d, D)
            if not ch:
                nochart += 1; continue
            eps, c = ch['sheets'][D]
            lo, hi = ch['W'][D]
            ys = [y for y in range(-20, 21) if status(cells, (int(ch['xD']), y)) == 'interior']
            for y in ys:
                Tt = (int(ch['xD']), y)
                vT = vT_of(ch, Tt)
                if not (lo < vT < hi) or vT == 0: continue
                s0 = vT / D
                iS, iT = I_S(ch), I_T(ch, vT)
                ov = isect([iS, iT]) if iS and iT else None
                legal, same = ground_truth(cells, P, ch, Tt, s0)
                a, b, cc, dd = ov is not None, inside(s0, iS), inside(s0, iT), legal and same
                n += 1
                if a == b == cc == dd: agree += 1
                else: bad.append((d, D, Tt, str(s0), a, b, cc, legal, same))
                if ov is not None and not inside(s0, ov): bad.append(("s0 not in overlap", d, D, Tt))
                if legal and not same: offchart += 1
    log(f"   [{name}] S={S}: (chart, target) instances {n}; overlap <=> s0 in I_S <=> s0 in I_T <=> chord legal on chart: "
        f"{agree}/{n}; mismatches {bad[:4]}; legal chords on another chart {offchart}; reference rays dead before D: {nochart}")

dirs = [(sx * a, b) for a in range(1, 5) for b in range(-9, 10) for sx in (1, -1) if b and gcd(a, b) == 1]
stress("DB55", DB, PDB, (1, 1), dirs, 10)
stress("R22", R22, PR, (0, 0), dirs, 8)
stress("R22-L1-005", L105, PL, (0, 0), dirs, 8)

# ================================================================== 1b. smooth endpoint of a column door
log("\n# 1b. Column cut x=4 in R22: door (0,1) between columns 3 and 4 ends at (4,0), which is "
    f"{status(R22, (4, 0))}, not a corner")
hits = []
for Sx in [p for p in regular_points(R22) if status(R22, p) == 'interior']:
    for a in range(1, 4):
        for b in range(-4, 5):
            if b == 0 or gcd(a, b) != 1: continue
            for sx in (1, -1):
                try:
                    r = trace(PR, Sx, (sx * a, b), maxrefl=12)
                except TypeError:
                    continue
                if r['poly'][1:4].count((F(4), F(0))):
                    hits.append((Sx, (sx * a, b)))
log(f"   rays from regular points of R22 whose first 3 bounces include the smooth point (4,0): {hits[:4]}")
if hits:
    Sx, d = hits[0]
    r = trace(PR, Sx, d, maxrefl=12)
    ch, why = build_chart(R22, PR, Sx, d, 6)
    log(f"   ray {Sx} d={d}: poly {[(str(a), str(b)) for a, b in r['poly'][:5]]}; column chart: {why}")
    log("   such rays are legal but belong to no strict column chart; maximal-rectangle charts avoid this only "
        "when every door endpoint is a vertex")

log(f"\nTotal CPU: {time.process_time() - T0:.1f}s")
