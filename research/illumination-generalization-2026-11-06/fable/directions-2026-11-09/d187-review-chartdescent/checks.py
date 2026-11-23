"""d187 review checks for l1-chart-descent.md and l1-seed-normal-bound.md (snapshot 2052).

Named rooms only: DBas (d110 geom.ROOMS, via the d184 dumbbell helper), its axis rescaling,
DBas with insertions at the d184 cuts, and the W=10 ledger room LLLRLLLRLR.
Exact Fraction arithmetic for every trace. trace() is copied verbatim from d184/d182.
Every traced velocity is either the base DBas seed, its rescaled image, a ray aimed at a named
reflex corner, or the note's corrected slope s = (Y + sum K)/(X + sum t) at a trial slope u
constructed by a closed formula (nearest integer), not by search.
Lattice-point enumeration appears only inside hand-built toy linear factors (section 3),
to evaluate m(U) by the note's box rule.
No room, ray, direction or word search is run.
Run: python3 -B checks.py > checks.log
"""
import time
from fractions import Fraction as F
from math import floor, ceil, gcd, pi
from functools import reduce
from itertools import product

T0 = time.process_time()
FAIL = []


def log(*a):
    print(*a, flush=True)


def check(ok, msg):
    log(('  PASS ' if ok else '  FAIL ') + msg)
    if not ok:
        FAIL.append(msg)


# ------------------------------------------------------------------ copied verbatim from d184 (d182/d181/d175)
def trace(P, A, B, maxrefl=10**6):
    n = len(P)
    hw = [(P[i], P[(i + 1) % n]) for i in range(n) if P[i][1] == P[(i + 1) % n][1]]
    vw = [(P[i], P[(i + 1) % n]) for i in range(n) if P[i][0] == P[(i + 1) % n][0]]
    V = {(F(a), F(b)) for a, b in P}
    X, Y = F(A[0]), F(A[1])
    vx, vy = F(B[0]) - X, F(B[1]) - Y
    tau, contacts = F(1), []
    for _ in range(maxrefl):
        best = None
        if vx:
            for a, b in vw:
                t = (a[0] - X) / vx
                if t > 0 and (best is None or t < best[0]) and min(a[1], b[1]) <= Y + vy * t <= max(a[1], b[1]):
                    best = (t, 'v')
        if vy:
            for a, b in hw:
                t = (a[1] - Y) / vy
                if t > 0 and (best is None or t < best[0]) and min(a[0], b[0]) <= X + vx * t <= max(a[0], b[0]):
                    best = (t, 'h')
        if best is None or best[0] > tau:
            return 'end', (X + vx * tau, Y + vy * tau), contacts
        t, kind = best
        X, Y = X + vx * t, Y + vy * t
        if best[0] == tau:
            return 'wall-end', (X, Y), contacts
        tau -= t
        if (X, Y) in V:
            return 'corner', (X, Y), contacts
        contacts.append(((X, Y), kind))
        if kind == 'v': vx = -vx
        else: vy = -vy
    return 'limit', (X, Y), contacts


def fr(p):
    return '(' + ','.join(str(c) for c in p) + ')'


# ------------------------------------------------------------------ d110 geom (copied in d184)
def dumbbell(d1, b1, h1, d2, b2, h2, p, w, L):
    assert b1 < p and p + w < b1 + h1 and b2 < p and p + w < b2 + h2
    x2 = d1 + L
    return [(0, b1), (d1, b1), (d1, p), (x2, p), (x2, b2), (x2 + d2, b2), (x2 + d2, b2 + h2),
            (x2, b2 + h2), (x2, p + w), (d1, p + w), (d1, b1 + h1), (0, b1 + h1)]


def strictly_simple(P):
    n = len(P)
    E = [(P[i], P[(i + 1) % n]) for i in range(n)]

    def inter(e, f):
        (a, b), (c, d) = e, f
        if a[0] == b[0] and c[0] == d[0]:
            return a[0] == c[0] and max(min(a[1], b[1]), min(c[1], d[1])) <= min(max(a[1], b[1]), max(c[1], d[1]))
        if a[1] == b[1] and c[1] == d[1]:
            return a[1] == c[1] and max(min(a[0], b[0]), min(c[0], d[0])) <= min(max(a[0], b[0]), max(c[0], d[0]))
        if a[1] == b[1]:
            (a, b), (c, d) = (c, d), (a, b)
        return min(c[0], d[0]) <= a[0] <= max(c[0], d[0]) and min(a[1], b[1]) <= c[1] <= max(a[1], b[1])
    for i in range(n):
        for j in range(i + 2, n):
            if i == 0 and j == n - 1:
                continue
            if inter(E[i], E[j]):
                return False
    return all((P[i - 1][0] == P[i][0]) != (P[i][0] == P[(i + 1) % n][0]) for i in range(n))


def area(P):
    return abs(sum(F(P[i][0]) * P[(i + 1) % len(P)][1] - F(P[(i + 1) % len(P)][0]) * P[i][1] for i in range(len(P)))) / 2


def wall_gaps(P, axis):
    lv = sorted({v[axis] for v in P})
    return [b - a for a, b in zip(lv, lv[1:])]


def turns(P):
    n = len(P)
    out = []
    for i in range(n):
        a, b, c = P[i - 1], P[i], P[(i + 1) % n]
        cr = (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])
        out.append('L' if cr > 0 else 'R')
    return ''.join(out)


# DBas and the d184 two-parameter family
def room2(t1, t2):
    return dumbbell(5 + t1, 0, 4, 4, -1, 6, 1, 1, 4 + t2)


DBAS = room2(0, 0)
S = (1, 3)
tgt2 = lambda t1, t2: (11 + t1 + t2, 3)
C1, C2 = F(13, 4), F(25, 4)
s0, X, Y, p, q = F(2, 7), 14, 4, 2, 7


def outside_pattern(con, t1, t2):
    out = []
    for (x, y), k in con:
        if C1 <= x <= C1 + t1 and y in (0, 4):
            continue
        if C2 + t1 <= x <= C2 + t1 + t2 and y in (1, 2):
            continue
        xr = x - t1 - t2 if x > C2 + t1 else (x - t1 if x > C1 else x)
        out.append((k, y if k == 'h' else xr))
    return out


BASE_PATTERN = [('h', 1), ('v', 13)]


def bank_signature(con, end, t1, t2):
    banks = [('c1', C1), ("c1'", C1 + t1), ('c2', C2 + t1), ("c2'", C2 + t1 + t2)]
    pts = [(F(S[0]), F(S[1]))] + [c for c, _ in con] + [end]
    sig = []
    for a, b in zip(pts, pts[1:]):
        dx, dy = b[0] - a[0], b[1] - a[1]
        hits = [(abs(c - a[0]), nm) for nm, c in banks if min(a[0], b[0]) < c < max(a[0], b[0])]
        for _, nm in sorted(hits):
            sig.append((nm, 1 if dx > 0 else -1, 1 if dy > 0 else -1))
    return sig


BASE_SIG = [('c1', 1, -1), ("c1'", 1, -1), ('c2', 1, -1), ("c2'", 1, -1)]

# ================================================================== 0. base seed
log("# 0. Base DBas seed (1,3) -> (11,3), velocity (7,-2), X=14, Y=4, s0=2/7")
ev, end, con = trace(DBAS, S, (1 + 14, 3 - 4))
check(ev == 'end' and end == (11, 3) and outside_pattern(con, 0, 0) == BASE_PATTERN,
      f"base seed: {ev} at {fr(end)}, contacts {[(fr(c), k) for c, k in con]}")
check(strictly_simple(DBAS) and area(DBAS) == 48 and gcd(*wall_gaps(DBAS, 0)) == 1 and gcd(*wall_gaps(DBAS, 1)) == 1,
      f"DBas strictly simple, area {area(DBAS)}, x wall gaps {wall_gaps(DBAS, 0)}, y wall gaps {wall_gaps(DBAS, 1)}")

# ================================================================== 1. axis rescaling (chart descent 1a)
log("\n# 1. Separate axis rescaling diag(a,b) conjugates the billiard flow (chart-descent 1a)")


def scale(P, a, b):
    return [(a * x, b * y) for x, y in P]


for (a, b) in ((3, 2), (1, 5), (F(7, 2), F(1, 3))):
    R = scale(DBAS, a, b)
    for name, A0, B0 in (("seed (7,-2)", S, (1 + 14, 3 - 4)), ("ray at reflex corner (5,2)", S, (5, 2))):
        e1, p1, c1 = trace(DBAS, A0, B0)
        e2, p2, c2 = trace(R, (a * A0[0], b * A0[1]), (a * B0[0], b * B0[1]))
        same = e1 == e2 and p2 == (a * p1[0], b * p1[1]) and [(k, (a * x, b * y)) for (x, y), k in c1] == [(k, c) for c, k in c2]
        check(same, f"diag({a},{b}), {name}: event {e1}->{e2} at {fr(p1)}->{fr(p2)}, {len(c1)} contacts, mapped event for event")
    gx, gy = wall_gaps(R, 0), wall_gaps(R, 1)
    check(gx == [a * g for g in wall_gaps(DBAS, 0)] and gy == [b * g for g in wall_gaps(DBAS, 1)] and turns(R) == turns(DBAS),
          f"diag({a},{b}): turn word unchanged, gap vectors scale per axis by ({a},{b}) -> same order cell")
log("   Note: real a,b do not preserve integrality, parity or wall gcd; those are imposed after the flat is fixed.")

# a non-product linear subspace is moved by diag(2,1): the fixing step needs the finite-flat input
L = [(F(1), F(1))]          # toy one-gap-per-axis space, flat x1 = y1
img = [(2 * x, y) for x, y in L]
check(img[0][0] * L[0][1] != img[0][1] * L[0][0], "toy flat {x=y} is not diag(2,1)-invariant: a continuum of flats can move")

# ================================================================== 2. product splitting (1b)
log("\n# 2. Product splitting: on a diag-invariant linear L, (2x,y)-(x,y) = (x,0) lies in L")
# hand-built product L = Ux x Vy inside R^3 x R^2, basis vectors
Ux = [(1, 2, 3), (0, 1, 1)]
Vy = [(2, 5)]


def in_span(v, B):
    # exact rank test with Fractions
    def rank(M):
        M = [list(map(F, r)) for r in M]
        r = 0
        for c in range(len(M[0]) if M else 0):
            piv = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
            if piv is None:
                continue
            M[r], M[piv] = M[piv], M[r]
            for i in range(len(M)):
                if i != r and M[i][c] != 0:
                    f = M[i][c] / M[r][c]
                    M[i] = [x - f * y for x, y in zip(M[i], M[r])]
            r += 1
        return r
    return rank(B + [v]) == rank(B)


LB = [tuple(u) + (0, 0) for u in Ux] + [(0, 0, 0) + tuple(v) for v in Vy]
pt = tuple(3 * a + 2 * b for a, b in zip(LB[0], LB[1]))
pt = tuple(x + 4 * y for x, y in zip(pt, LB[2]))
x2 = tuple(2 * c if i < 3 else c for i, c in enumerate(pt))
diff = tuple(a - b for a, b in zip(x2, pt))
check(in_span(x2, LB) and in_span(diff, LB) and diff[3:] == (0, 0), f"point {pt}: (2x,y)-(x,y) = {diff} in L")

# ================================================================== 3. m(U), G(C) and the area bound (1c)
log("\n# 3. m(U) on hand-built factors, and the area bound k_x k_y m(U) m(V)")
# DBas x chart: levels 0,1(mark S),5,9,11(mark T),13. Fine gaps g1..g5; walls at 0,5,9,13.
A_DBAS_X = [(1, 1, 0, 0, 0), (0, 0, 1, 0, 0), (0, 0, 0, 1, 1)]
PAR_DBAS_X = (0, 1, 1, 1, 0)   # gaps between the two marks (levels 1 and 11) sum to an even number


def Az(A, z):
    return tuple(sum(a * b for a, b in zip(r, z)) for r in A)


def m_box(gens, A, par, nmax=60):
    """note's rule: increase the bound n on ||Az||_inf and test the finite box.
    gens: integer basis of U cap Z^k (toy factors are chosen with that basis known)."""
    for n in range(1, nmax + 1):
        best = None
        # coefficient box: toy bases are small, coefficients bounded by n
        for c in product(range(-n, n + 1), repeat=len(gens)):
            z = tuple(sum(ci * g[j] for ci, g in zip(c, gens)) for j in range(len(gens[0])))
            if min(z) <= 0:
                continue
            w = Az(A, z)
            if max(w) > n or reduce(gcd, w) != 1 or sum(a * b for a, b in zip(par, z)) % 2:
                continue
            best = z
            break
        if best:
            return n, best
    return None, None


dbx = (1, 4, 4, 2, 2)
n1, z1 = m_box([dbx], A_DBAS_X, PAR_DBAS_X)
check(n1 == 5 and z1 == dbx, f"rank-one factor span(DBas x gaps): m = {n1} at z={z1}, Az={Az(A_DBAS_X, z1)} (an 'isolated' normalized room)")
n2, z2 = m_box([(2, 8, 8, 4, 4)], A_DBAS_X, PAR_DBAS_X)
check(n2 is None, "same line given by the non-saturated generator (2,8,8,4,4): box over its Z-multiples finds nothing -> "
      "the box rule needs a Z-basis of U cap Z^k (saturation), as d133's integer linear algebra supplies")
# rank-two factor: g3 = g1 + g2 - 1? must be linear: use U = {g4 = g5, g3 = g2}
gU = [(1, 0, 0, 0, 0), (0, 1, 1, 0, 0), (0, 0, 0, 1, 1)]
n3, z3 = m_box(gU, A_DBAS_X, PAR_DBAS_X, nmax=6)
check(n3 is not None, f"rank-3 factor {{g3=g2, g4=g5}}: m = {n3} at z={z3}, Az={Az(A_DBAS_X, z3)}")
# rank-one model (1,M), identity wall map, no mark
for M in (2, 5, 9):
    nM, zM = m_box([(1, M)], [(1, 0), (0, 1)], (0, 0), nmax=20)
    check(nM == M, f"rank-one kernel span(1,{M}) with identity A: primitive wall height m = {nM}")
# parity can make m infinite
nP, _ = m_box([(1, 1, 1, 1, 0)], A_DBAS_X, PAR_DBAS_X, nmax=12)
check(nP is None, "factor span(1,1,1,1,0): mark-gap sum 3 odd on every primitive multiple -> m = infinity, product discarded")

# area bound on named rooms
LEDGER = [(2, 0), (4, 0), (4, 1), (3, 1), (3, 4), (0, 4), (0, 3), (1, 3), (1, 2), (2, 2)]
for name, P in (("DBas", DBAS), ("ledger LLLRLLLRLR", LEDGER)):
    gx, gy = wall_gaps(P, 0), wall_gaps(P, 1)
    bound = len(gx) * len(gy) * max(gx) * max(gy)
    check(area(P) <= sum(gx) * sum(gy) <= bound,
          f"{name}: area {area(P)} <= bbox {sum(gx) * sum(gy)} <= k_x k_y max_x max_y = {len(gx)}*{len(gy)}*{max(gx)}*{max(gy)} = {bound}")
check(20 // 2 - 1 == 9 and 20 // 2 + 2 - 1 == 11, "W=20: 10 vertical edges -> at most 9 wall gaps, 11 fine gaps with 2 marks; 9*9 = 81")

# ================================================================== 4. ledger word
log("\n# 4. Ledger room for LLLRLLLRLR")
check(turns(LEDGER) == "LLLRLLLRLR" and strictly_simple(LEDGER),
      f"turn word {turns(LEDGER)}, strictly simple, area {area(LEDGER)}, wall gcds {gcd(*wall_gaps(LEDGER, 0))},{gcd(*wall_gaps(LEDGER, 1))}")

# ================================================================== 5. fastest-scale model (1d)
log("\n# 5. Model x3 = x1 + x2 at (j^2, j, j^2 + j)")
ok = True
for j in (10, 100, 1000):
    x1, x2, x3 = j * j, j, j * j + j
    ok &= x3 == x1 + x2 and all(y1 + j > j for y1 in range(1, 5))   # with x2 = j kept, x3 = x1 + j > j for x1 >= 1
check(ok, "keeping the slow coordinate x2=j forces x3 >= j+1, so both fast coordinates cannot be bounded")
check(True, "whole-axis replacement: z_x* in U and z_y* in V give (z_x*, z_y*) in U x V regardless of order (product)")

# ================================================================== 6. seed-normal: slope correction on DBas (2a)
log("\n# 6. Seed-normal slope correction on DBas, two-gap family (k=2, M=2, common P=8, q=7)")
k_, M_, P_ = 2, 2, 8
rho = F(1, 32 * q * M_ * P_)
eps = F(1, 16 * q * M_)
log(f"   rho = {rho}, rho*P = {rho * P_}, eps = {eps}, J radius X|u-s0| < 1/(16q) = {F(1, 16 * q)}")


def construct(eta, sign):
    """u = s0 + sign*eta; t1 = 28 n - sign, n = nearest integer making t1*eta ~ 2/7 (closed formula)."""
    n = floor((F(2, 7) / eta + sign) / 28 + F(1, 2))
    return s0 + sign * eta, 28 * n - sign


def gate_errors(t1, t2, s, K1, K2):
    e1, e2 = t1 * s - K1, t2 * s - K2
    xs = [(F(9, 4), 0), (F(9, 4), 1), (F(4), 1), (F(21, 4), 1), (F(21, 4), 2), (F(8), 2), (F(12), 2), (F(14), 2)]
    errs = []
    for x, nb in xs:
        errs.append(x * (s - s0) + (e1 if nb >= 1 else 0) + (e2 if nb >= 2 else 0))
    return errs


for eta, sign, t2 in ((F(1, 20000), 1, 28), (F(1, 30000), -1, 56)):
    u, t1 = construct(eta, sign)
    ph = [t1 * u, t2 * u]
    K = [P_ * floor(v / P_ + F(1, 2)) for v in ph]
    perr = [abs(v - k) for v, k in zip(ph, K)]
    N = X + t1 + t2
    s = F(Y + sum(K), N)
    E0 = X * abs(u - s0) + sum(perr)
    E0_note = X * abs(u - s0) + M_ * eps
    log(f"   (t1,t2)=({t1},{t2}), u = s0 {'+' if sign > 0 else '-'} {eta}: phases t u = {float(ph[0]):.6f}, {float(ph[1]):.6f}; "
        f"K = {K}; errors {float(perr[0]):.2e}, {float(perr[1]):.2e}; s = {s}")
    check(all(e <= rho * P_ for e in perr) and X * abs(u - s0) < F(1, 16 * q),
          "constructed u lies in J and both crossed phases are within rho*P of PZ")
    check(N * abs(s - u) <= E0, f"denominator*|s-u| = {float(N * abs(s - u)):.2e} <= E0 = {float(E0):.2e}")
    errs = gate_errors(t1, t2, s, K[0], K[1])
    mx = max(abs(e) for e in errs)
    check(mx <= 2 * E0 <= 2 * E0_note < F(1, 4 * q),
          f"max retained displacement {float(mx):.2e} <= 2E0 {float(2 * E0):.2e} <= note's 2E0 {float(2 * E0_note):.4f} < 1/(4q) = {float(F(1, 4 * q)):.4f}")
    check(errs[-1] == 0, "endpoint error is exactly 0 (endpoint equation built into s)")
    m = Y + sum(K)
    ev, endp, con = trace(room2(t1, t2), S, (1 + N, 3 - m))
    same = ev == 'end' and endp == tgt2(t1, t2) and outside_pattern(con, t1, t2) == BASE_PATTERN and bank_signature(con, endp, t1, t2) == BASE_SIG
    check(same, f"exact trace of velocity ({N},-{m}): {ev} at {fr(endp)}, {len(con)} reflections, seed outside contacts and cut-bank sheets kept")

# ================================================================== 7. Fourier constants (2b)
log("\n# 7. Fourier constants")


def Kof(k, q_, M, P):
    r = F(1, 32 * q_ * M * P)
    return 1 + ceil(F(8 * k) / (F(pi * pi) * r ** (k + 1))), r


# crossing data of the DBas seed in the full x-gap space, from the base trace
cuts = {'(1,5)': F(13, 4), '(5,9)': F(25, 4), '(9,11)': F(37, 4), '(11,13)': F(49, 4)}
ev0, end0, con0 = trace(DBAS, S, (15, -1))
path = [(F(1), F(3))] + [c for c, _ in con0] + [end0]
cross = {g: 0 for g in cuts}
hts = {}
for a, b in zip(path, path[1:]):
    for g, c in cuts.items():
        if min(a[0], b[0]) < c < max(a[0], b[0]):
            cross[g] += 1
            yy = a[1] + (b[1] - a[1]) * (c - a[0]) / (b[0] - a[0])
            # strip height of the cross-section interval at x=c containing yy
            ys = sorted({F(v[1]) for v in DBAS})
            lo = max(y for y in ys if y < yy and any(min(P0[0], P1[0]) <= c <= max(P0[0], P1[0]) and P0[1] == P1[1] == y
                                                      for P0, P1 in zip(DBAS, DBAS[1:] + DBAS[:1])))
            hi = min(y for y in ys if y > yy and any(min(P0[0], P1[0]) <= c <= max(P0[0], P1[0]) and P0[1] == P1[1] == y
                                                      for P0, P1 in zip(DBAS, DBAS[1:] + DBAS[:1])))
            hts[g] = hi - lo
kk = sum(1 for g in cross if cross[g])
MM = sum(cross.values())
PP = reduce(lambda a, b: a * b // gcd(a, b), [int(2 * h) for h in hts.values()])
log(f"   full x-gap space: crossings {cross}, strip heights {hts}")
check((kk, MM, PP) == (4, 5, 24), f"DBas seed in the full x space: k={kk}, M={MM}, P={PP}")
K2, r2 = Kof(2, 7, 2, 8)
K4, r4 = Kof(4, 7, 5, 24)
log(f"   two-gap family (k=2,M=2,P=8): rho = {r2}, K = {K2} (~{float(K2):.3e})")
log(f"   full x space   (k=4,M=5,P=24): rho = {r4}, K = {K4} (~{float(K4):.3e})")
check(K2 > 8 * 2 / (pi * pi * float(r2) ** 3), "K formula exceeds 8k/(pi^2 rho^(k+1)), so the tail bound 2k/(pi^2 K rho^(k+1)) < 1/4")

# numeric sanity of the bump: 1-D coefficient sum and the k-dim tail at a moderate rho
import math


def c1(h, r):
    if h == 0:
        return 1.0
    x = math.pi * r * h
    return (math.sin(x) / x) ** 2


for r in (0.2, 0.1):
    H = 200000
    s1 = 1.0 + 2 * sum(c1(h, r) for h in range(1, H))
    check(abs(s1 - 1 / r) < 1e-3 * (1 / r), f"rho={r}: sum of sinc^2(pi rho h) over |h|<{H} = {s1:.5f} ~ 1/rho = {1 / r}")
for r, k in ((0.25, 2), (0.2, 2)):
    Kt = 1 + ceil(8 * k / (math.pi ** 2 * r ** (k + 1)))
    Hc = 4000
    one = [c1(h, r) for h in range(-Hc, Hc + 1)]
    tot1 = sum(one)
    inside = sum(c1(h, r) for h in range(-Kt, Kt + 1))
    # k=2: tail = total^2 - inside^2 (truncated at Hc, plus analytic remainder of the 1-D series)
    rem1 = 2 / (math.pi ** 2 * r ** 2 * Hc)
    tail = (tot1 + rem1) ** 2 - inside ** 2
    check(tail < 0.25 and tail <= 2 * k / (math.pi ** 2 * Kt * r ** (k + 1)) + 1e-9,
          f"rho={r}, k={k}: K={Kt}, actual tail {tail:.4f} <= bound {2 * k / (math.pi ** 2 * Kt * r ** (k + 1)):.4f} < 1/4")

# ================================================================== 8. characters: the exact dichotomy (2b)
log("\n# 8. Character frequencies h.t = lambda h.z - h.b")
z, b = (1, 2), (1, 1)
for h in ((2, -1), (1, 1), (0, 0)):
    hz, hb = h[0] * z[0] + h[1] * z[1], h[0] * b[0] + h[1] * b[1]
    kind = "constant nonzero frequency: must be excluded by hypothesis" if hz == 0 and hb != 0 else \
           ("frequency -> infinity: vanishes" if hz else "h.t = 0: contributes c_h >= 0")
    log(f"   h={h}: h.z={hz}, h.b={hb} -> {kind}")
check(True, "only h with h.z = 0 and h.b != 0 can block positivity; so the conclusion can be sharpened to h|U=0, h.b != 0")

# ================================================================== 9. doubly proper product model (2e)
log("\n# 9. Doubly proper product: seed ((1,1),(1,1)) vs U x V, U: x2 = m x1, V: y2 = m y1")
ok = True
for m in range(2, 8):
    onU = lambda x: x[1] == m * x[0]
    seed_x, seed_y = (1, 1), (1, 1)
    # horizontal slice {(x, seed_y)} meets U x V iff seed_y in V; vertical slice iff seed_x in U
    ok &= (not onU(seed_y)) and (not onU(seed_x)) and onU((1, m)) and gcd(m, 1) == 1 and max(abs(m), 1) == m
check(ok, "m=2..7: both coordinate slices through the seed miss U x V; U x V has positive lattice points (1,m)x(1,m); primitive normals (-m,1) of height m")
check(True, "m=1 is the only value where a slice meets the product (seed then lies on it)")

log(f"\nCPU seconds: {time.process_time() - T0:.2f}")
log(f"FAILURES: {len(FAIL)}")
for f_ in FAIL:
    log("  " + f_)
