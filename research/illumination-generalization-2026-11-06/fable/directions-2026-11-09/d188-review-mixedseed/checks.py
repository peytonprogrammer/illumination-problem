"""d188 review checks for l1-mixed-seed-normals.md (snapshot 2114).

Named rooms only: the st279 (m=5) crossing slice R(a,D) at the note's seed (7,5) and on the note's ray
a = 7+2n, D = 3a at named n. Every traced velocity comes from a gate formula (direct ascent: the note's
v = 57/2; floor route: d186's gate with A = a+2). Oscillatory integrals use fixed quadrature, not a search.
No room, ray, direction, slope or word search.
Helpers trace(), shoot(), st(), gate(), direct(), trace_direct() are copied verbatim from d186 checks.py.
Run: python3 -B checks.py > checks.log
"""
import time
from fractions import Fraction as F
from math import floor, gcd

T0 = time.process_time()
FAIL = []


def log(*a):
    print(*a, flush=True)


def check(ok, msg):
    log(('  PASS ' if ok else '  FAIL ') + msg)
    if not ok:
        FAIL.append(msg)


def fr(p):
    return '(' + ','.join(str(c) for c in p) + ')'


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


# ------------------------------------------------------------------ d109 path.py shoot(), adapted: polygon vertex list
def shoot(P, s, d, t, maxev=100000):
    """Events (kind, point) from s in direction d until t is reached; raises on corner hit."""
    n = len(P)
    E = [((F(P[i][0]), F(P[i][1])), (F(P[(i + 1) % n][0]), F(P[(i + 1) % n][1]))) for i in range(n)]
    V = {a for a, _ in E}
    p, d, t, ev = (F(s[0]), F(s[1])), (F(d[0]), F(d[1])), (F(t[0]), F(t[1])), []
    for _ in range(maxev):
        best = None
        for (a, b) in E:
            if a[0] == b[0]:
                if d[0] == 0: continue
                tt = (a[0] - p[0]) / d[0]
                if tt <= 0: continue
                y = p[1] + tt * d[1]
                if min(a[1], b[1]) <= y <= max(a[1], b[1]) and (best is None or tt < best[0]):
                    best = (tt, 'x', (a[0], y))
            else:
                if d[1] == 0: continue
                tt = (a[1] - p[1]) / d[1]
                if tt <= 0: continue
                x = p[0] + tt * d[0]
                if min(a[0], b[0]) <= x <= max(a[0], b[0]) and (best is None or tt < best[0]):
                    best = (tt, 'y', (x, a[1]))
        tt, kind, q = best
        ttT = (t[0] - p[0]) / d[0] if d[0] != 0 else (t[1] - p[1]) / d[1]
        if 0 < ttT < tt and p[0] + ttT * d[0] == t[0] and p[1] + ttT * d[1] == t[1]:
            ev.append(('reach', t)); return ev
        if q in V:
            raise RuntimeError(f"corner hit at {q}")
        ev.append(('v' if kind == 'x' else 'h', q))
        d = (-d[0], d[1]) if kind == 'x' else (d[0], -d[1])
        p = q
    raise RuntimeError("no arrival")


# ------------------------------------------------------------------ d184 geometry (copied)
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


def room2(t1, t2):
    return dumbbell(5 + t1, 0, 4, 4, -1, 6, 1, 1, 4 + t2)


# ------------------------------------------------------------------ st279 (m=5) crossing slice of the note
def st(a, D):
    """Bands: y in (4-a,5) x [5-D,5]; (5,6) x [4,7]; (6,7) x [5,8]; (7,12) x [7,12]."""
    return [(5 - D, 4 - a), (5, 4 - a), (5, 5), (7, 5), (7, 6), (8, 6), (8, 7), (12, 7), (12, 12), (7, 12),
            (7, 7), (5, 7), (5, 6), (4, 6), (4, 5), (5 - D, 5)]


S_st = lambda a: (4, 5 - a)
T_st = (6, 6)


def area(P):
    n = len(P)
    return abs(sum(F(P[i][0]) * P[(i + 1) % n][1] - F(P[(i + 1) % n][0]) * P[i][1] for i in range(n))) / 2


def wall_gcds(P):
    n = len(P)
    gh = gv = 0
    for i in range(n):
        (x0, y0), (x1, y1) = P[i], P[(i + 1) % n]
        if y0 == y1: gh = gcd(gh, abs(x1 - x0))
        else: gv = gcd(gv, abs(y1 - y0))
    return gh, gv


def inv(x, m):
    return pow(x, -1, m) if m > 1 else 0


def first_in(r, g, lo, hi):
    """least element of r + gZ strictly inside (lo,hi), or None (closed form, no search)."""
    k = floor(F(lo - r, g)) + 1
    x = r + g * k
    return x if x < hi else None


def gate(A, D, c, e, a_for_window):
    """Note's gate: (A+1)z in c + A e + 2 gcd(D, 3A) Z, z in (0,1) (b=w=1, W=3). Returns (z, v) with
    z == c + A v (mod 2D), z == e - v (mod 6), or None."""
    g2 = 2 * gcd(D, 3 * A)
    N0 = first_in(c + A * e, g2, 0, A + 1)
    if N0 is None:
        return None
    z = F(N0, A + 1)
    N = (A + 1) * z - c - A * e          # integer, divisible by g2 = gcd(6A, 2D)
    assert N.denominator == 1 and N % g2 == 0
    m = 2 * D // g2
    l = (int(N) // g2) * inv((6 * A // g2) % m, m) % m if m > 1 else 0
    v = e - z + 6 * l
    assert ((z - c - A * v) / (2 * D)).denominator == 1 and ((z - e + v) / 6).denominator == 1
    return z, v


def route_kind(ev, a, D):
    floor_hits = [q for k, q in ev if k == 'h' and q[1] == 4 - a]
    far = [q for k, q in ev if k == 'v' and q[0] == 5 - D]
    hs = [q for k, q in ev if k == 'h']
    return floor_hits, far, hs


def direct(a, D):
    out = []
    for c in (1, -1):
        for e in (-1, -3):
            r = gate(a, D, c, e, a)
            if r: out.append((c, e) + r)
    return out


def trace_direct(a, D, c, z, v):
    dz = v if c == 1 else -v          # c=-1 is the reflected source image
    ev = shoot(st(a, D), S_st(a), (-dz, 1), T_st)
    fl, far, hs = route_kind(ev, a, D)
    nref = len(ev) - 1
    return ev[-1][0] == 'reach' and not hs, nref



# ================================================================== d188 checks
import cmath
from math import ceil, pi, sqrt


def dist_Z(x):
    return abs(x - round(x))


def osc_avg(alpha, beta, lam, J=(0.5, 2.0), N=400000):
    """Average over J of e(lam(alpha u + beta/u)), composite Simpson with N (even) panels."""
    a, b = J
    h = (b - a) / N
    s = 0j
    for i in range(N + 1):
        u = a + i * h
        w = 1 if i in (0, N) else (4 if i % 2 else 2)
        s += w * cmath.exp(2j * pi * lam * (alpha * u + beta / u))
    return abs(s * h / 3 / (b - a))


log("# 1. Fixed-period lemma")
# 1a. second derivative of alpha u + beta/u: exact second difference identity, then limit 2beta/u^3
for al, be, u, hh in [(F(3), F(2), F(3, 2), F(1, 7)), (F(0), F(-5), F(1, 3), F(1, 100)), (F(1, 2), F(7), F(4), F(1, 9))]:
    phi = lambda x: al * x + be / x
    sd = (phi(u + hh) - 2 * phi(u) + phi(u - hh)) / hh ** 2
    check(sd == 2 * be / (u * (u * u - hh * hh)),
          f"alpha={al}, beta={be}, u={u}: second difference = 2beta/(u(u^2-h^2)) -> 2beta/u^3 = {2*be/u**3}")
# 1b. decay rates on J=[1/2,2] (fixed quadrature, amplitude 1)
log("  decay of |avg_J e(lam(alpha u+beta/u))|, J=[1/2,2]:")
rows = []
for al, be, label in [(1.0, 1.0, "beta!=0, stationary point u=1"), (0.0, 1.0, "alpha=0, beta!=0"), (1.0, 0.0, "beta=0, alpha!=0")]:
    vals = [(lam, osc_avg(al, be, lam)) for lam in (30, 300, 3000)]
    rows.append((label, vals))
    log(f"    {label}: " + ", ".join(f"lam={l}: {v:.3e} (x sqrt(lam) {v*sqrt(l):.3f}, x lam {v*l:.3f})" for l, v in vals))
st_vals = rows[0][1]
check(max(v * sqrt(l) for l, v in st_vals) < 2 * min(v * sqrt(l) for l, v in st_vals) and st_vals[-1][1] * 3000 > 10,
      "stationary case: sqrt(lam)*|avg| stays within factor 2, lam*|avg| grows -> rate lam^(-1/2) is attained, not better")
lin = rows[2][1]
check(all(abs(v - abs(cmath.exp(2j * pi * l * 2) - cmath.exp(2j * pi * l * 0.5)) / (2 * pi * l * 1.5)) < 1e-6 for l, v in lin),
      "beta=0: average equals closed form |e(2lam)-e(lam/2)|/(2 pi lam |J|) = O(1/lam)")
# 1c. K constant
for k, rho in [(2, F(1, 4)), (2, F(1, 8)), (4, F(1, 4))]:
    K = 1 + ceil(8 * k / (pi ** 2 * float(rho) ** (k + 1)))
    tail = 2 * k / (pi ** 2 * K * float(rho) ** (k + 1))
    check(tail < 0.25, f"k={k}, rho={rho}: K={K}, d184 tail bound 2k/(pi^2 K rho^(k+1)) = {tail:.4f} < 1/4")
# 1d. sharpness example: b=(1,1), z=(1,2), h=(2,-1)
h, b, z = (2, -1), (1, 1), (1, 2)
dot = lambda p, q: sum(x * y for x, y in zip(p, q))
for lam in (2, 10, 1000, 10 ** 6 + 1):
    t = tuple(lam * zi - bi for zi, bi in zip(z, b))
    check(dot(h, z) == 0 and dot(h, t) == -1, f"lam={lam}: t={t}, h.z=0, h.t=-1 (mode frozen at -u/P)")
P, rho = F(1), F(1, 10)
for u in (F(2, 5), F(1, 2), F(3, 5)):
    ok = dist_Z(u / P) > 3 * rho
    for lam in (2, 10, 1000, 10 ** 6 + 1):
        t = (lam - 1, 2 * lam - 1)
        both = all(dist_Z(ti * u / P) <= rho for ti in t)
        ok = ok and not both
    check(ok, f"P=1, rho=1/10, u={u}: dist(u/P,Z)={dist_Z(u/P)} > 3rho and the two x phases never both match (lam=2,10,1000,10^6+1)")
check(3 * F(1, 6) >= F(1, 2), "rho >= 1/6 gives 3rho >= 1/2 >= dist(u/P,Z): the example needs rho < 1/6 (review Low 2)")
# 1e. U = V = span(1,m): primitive annihilator (m,-1)
for m in (3, 50, 10 ** 4):
    nrm = (m, -1)
    check(dot(nrm, (1, m)) == 0 and gcd(*nrm) == 1 and max(abs(x) for x in nrm) == m,
          f"m={m}: primitive annihilator of span(1,m) is (m,-1), height m; excluded iff m > K")

log("\n# 2. st279 occupied crossing")
a0, D0, c0, e0, v0 = 7, 5, 1, -1, F(57, 2)
P0 = st(a0, D0)
check(strictly_simple(P0) and wall_gcds(P0) == (1, 1) and S_st(a0)[0] % 2 == T_st[0] % 2 and (S_st(a0)[1] - T_st[1]) % 2 == 0,
      f"seed room st(7,5): strictly simple, wall gcds {wall_gcds(P0)}, S={fr(S_st(a0))}, T={fr(T_st)} same parity, area {area(P0)}")
low = (1 + a0 * v0) % (2 * D0)
up = (-1 - v0) % 6
check(low == F(1, 2) and up == F(1, 2), f"(1+7v) mod 10 = {low}, (-1-v) mod 6 = {up}")
check(((F(1, 2) - c0 - a0 * v0) / (2 * D0)).denominator == 1 and ((F(1, 2) - e0 + v0) / 6).denominator == 1,
      "z=1/2, v=57/2 satisfy both legs: z - c - a v in 2D Z and z - e + v in 6Z")
check(gcd(2 * D0, 6 * a0) == 2 and sorted(F(N, a0 + 1) for N in range(1, a0 + 1) if (N - (c0 + a0 * e0)) % 2 == 0) == [F(1, 4), F(1, 2), F(3, 4)],
      "seed gate (c,e)=(1,-1): spacing gcd(10,42)=2, gate values z in {1/4,1/2,3/4}; z=1/2 is the window midpoint")
check(min(l for l in range(1, 10) if ((F(1, 2) - 1 - 7 * (F(-3, 2) + 6 * l)) / 10).denominator == 1) == 5,
      "with v = -3/2 + 6l, the lower leg forces l in 5Z; l=0 gives v=-3/2 (rightward launch), l=5 gives v=57/2, the least positive solution")
ok, nref = trace_direct(a0, D0, c0, F(1, 2), v0)
ev = shoot(P0, S_st(a0), (-v0, 1), T_st)
pts = [F(4), F(5 - a0)], None
path = [(F(4), F(5 - a0))] + [q for _, q in ev]
seam = [(p, q) for p, q in zip(path, path[1:]) if p[1] < 5 <= q[1]]
(p, q), = seam
xs = p[0] + (q[0] - p[0]) * (5 - p[1]) / (q[1] - p[1])
lat_low = [q for k, q in ev if k == 'v' and q[1] < 5]
lat_up = [q for k, q in ev if k == 'v' and q[1] > 5]
check(ok and xs == F(9, 2) and not any(q[1] == 5 for _, q in ev),
      f"exact trace of the seed (-57/2,1) from S: reaches T with {nref} lateral reflections only; crosses y=5 once at x={xs} (z=5-x=1/2)")
log(f"  INFO seed: {len(lat_low)} lateral reflections in the lower box (horizontal travel a v = {a0*v0} over width 5), {len(lat_up)} in the (5,6) band; vertical rise {T_st[1]-S_st(a0)[1]}")
log(f"  INFO seed vertical-travel phase a/(2D u) = 7/(10u); on the ray it is a/(6a u) = 1/(6u)")

log("\n# 2b. Ray a=7+2n, D=3a: increments, direct-ascent failure, phase")
for n in (1, 5, 20, 44, 47, 100):
    a, D = 7 + 2 * n, 3 * (7 + 2 * n)
    P = st(a, D)
    g = gcd(2 * D, 6 * a)
    res = sorted({(c + a * e) % g for c in (1, -1) for e in (-1, -3)})
    check(strictly_simple(P) and wall_gcds(P) == (1, 1) and a % 2 == 1 and (D - D0, a - a0) == (16 + 6 * n, 2 * n)
          and g == 6 * a and res == sorted([3 * a - 1, 3 * a + 1, 5 * a - 1, 5 * a + 1]) and min(res) > a + 1 and direct(a, D) == []
          and F(a, 2 * D) == F(1, 6),
          f"n={n}: (a,D)=({a},{D}) strictly simple, gcds (1,1), increments (16+6n,2n)=({D-D0},{a-a0}), spacing 6a={g}, "
          f"residues {res} outside (0,{a+1}); direct gate closed; a/(2D)=1/6")
log("  (symbolic) gcd(2D,6a)=gcd(6a,6a)=6a for every a; 3a-1 > a+1 for a > 1, so no primality is needed")

log("\n# 2c. Phase matches exist on the ray (averaging, fixed seed periods P=2D0=10, P'=6, rho=1/4, J=[1,2])")


def bump(x, r):
    d = dist_Z(x)
    return max(0.0, 1 - d / r) / r


for n in (20, 100):
    t, tau = 16 + 6 * n, 2 * n
    N = 200000
    hgrid = 1.0 / N
    avg = sum(bump(t * (1 + (i + .5) * hgrid) / 10, .25) * bump(tau / ((1 + (i + .5) * hgrid) * 6), .25) for i in range(N)) * hgrid
    check(avg > 0.5, f"n={n}: average of the two-bump product over J = {avg:.4f} > 0, so some u in J matches both phases")

log("\n# 2d. d186 floor route (gate with A=a+2, (c,e)=(1,-1), launch (-v,-1)) on the ray")
for n in (0, 1, 5, 20, 31, 44, 47, 100):
    a, D = 7 + 2 * n, 3 * (7 + 2 * n)
    r = gate(a + 2, D, 1, -1, a)
    lo = F((a + 1) * (a + 3), 24)
    inbox = a <= 93 and lo <= D <= 4 * (a + 1)
    if r is None:
        check(False, f"n={n}: floor gate closed"); continue
    zf, vf = r
    evf = shoot(st(a, D), S_st(a), (-vf, -1), T_st)
    fl, far, hs = route_kind(evf, a, D)
    good = evf[-1][0] == 'reach' and len(fl) == 1 and hs == fl
    kpos = [i for i, (k, q) in enumerate(evf) if k == 'h'][0]
    check(good and gcd(2 * D, 6 * (a + 2)) == 6,
          f"n={n}: (a,D)=({a},{D}) floor spacing gcd(2D,6(a+2))=6, z={zf}, v={vf}; exact trace reaches T; the only horizontal contact is "
          f"the floor (event {kpos}); {len(evf)-1} reflections; in d186 residual box: {inbox}")
check(F(68 * 70, 24) <= 3 * 67 and F(70 * 72, 24) > 3 * 69,
      "D=3a lies in the d186 residual box only for a <= 67 (a=67: 595/3 <= 201; a=69: 210 > 207), so the cap theorem alone lights n >= 31")

log(f"\nCPU {time.process_time() - T0:.2f} s; failures: {len(FAIL)}")
for f_ in FAIL:
    log("  FAILED: " + f_)
