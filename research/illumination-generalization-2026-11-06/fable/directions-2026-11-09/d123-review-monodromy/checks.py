"""Referee checks for three-zero-monodromy.snapshot.md (2026-11-20).

Run: python3 -B checks.py > checks.log
No room, ray, direction or reflection-word searches.  Only explicit
linear algebra, an explicit hyperelliptic hexagon model, and the explicit
sphere family q_s from the note.
"""
from fractions import Fraction as F
from itertools import product
from math import gcd
import cmath, math

def mat_mul(A, B):
    return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def T(A): return [list(r) for r in zip(*A)]
def mv(A, x): return [sum(A[i][k]*x[k] for k in range(len(x))) for i in range(len(A))]
def det3(M):
    return (M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1]) - M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0])
            + M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0]))
I = [[1,0,0],[0,1,0],[0,0,1]]
R = [[0,1,0],[0,0,1],[1,0,0]]          # R(x,y,z) = (y,z,x)
def add(A, B, s=1): return [[A[i][j]+s*B[i][j] for j in range(3)] for i in range(3)]
IpR, ImR = add(I, R), add(I, R, -1)

print("== 1. Linear algebra of the dichotomy ==")
assert mv(R, [1,2,3]) == [2,3,1]
for name, C in (("I+R", IpR), ("I-R", ImR)):
    G = mat_mul(C, T(C)); G2 = mat_mul(T(C), C)
    assert G == G2
    const = mv(G, [1,1,1]); plane = [mv(G, [1,-1,0]), mv(G, [0,1,-1])]
    print(f"{name}: CC^T = C^TC = {G}; on (1,1,1) -> {const}; on sum-zero basis -> {plane}; det C = {det3(C)}")

# 1a. Every +-1 array with six-cycle support is sign-equivalent to I+R or I-R,
#     decided by the product of the six nonzero entries.
supp = [(i, j) for i in range(3) for j in range(3) if IpR[i][j]]
counts = {}
for signs in product([1,-1], repeat=6):
    C = [[0]*3 for _ in range(3)]
    for (i, j), s in zip(supp, signs): C[i][j] = s
    target = IpR if math.prod(signs) == 1 else ImR
    ok = any([[r[i]*C[i][j]*c[j] for j in range(3)] for i in range(3)] == target
             for r in product([1,-1], repeat=3) for c in product([1,-1], repeat=3))
    assert ok
    counts[math.prod(signs)] = counts.get(math.prod(signs), 0) + 1
print("1a. all 64 sign arrays reduce by row/column signs; cycle-sign counts:", counts)

# 1b. Exhaustive integer check of the dichotomy for nonzero primitive a,b with |entries|<=B.
B = 12
def prim(v): return gcd(gcd(abs(v[0]), abs(v[1])), abs(v[2])) == 1
def parallel(x, y):  # x = lam*y for some rational lam (allowing x = 0)
    if all(t == 0 for t in x): return True
    k = next(i for i in range(3) if y[i] != 0)
    lam = F(x[k], y[k])
    return all(F(x[i]) == lam*y[i] for i in range(3))
vecs = [v for v in product(range(-B, B+1), repeat=3) if 0 not in v and prim(v)]
for name, C in (("I+R", IpR), ("I-R", ImR)):
    Ct = T(C); sols = []
    for a in vecs:
        Cta = mv(Ct, a)
        if any(Cta):
            gg = gcd(gcd(abs(Cta[0]), abs(Cta[1])), abs(Cta[2]))
            cands = [[x//gg for x in Cta], [-x//gg for x in Cta]]
            cands = [v for v in cands if 0 not in v and max(map(abs, v)) <= B]
        else:
            cands = vecs
        for b in cands:
            if parallel(Cta, b) and parallel(mv(C, b), a):
                sols.append((tuple(a), tuple(b)))
    consts = [s for s in sols if len(set(s[0])) == 1 and len(set(s[1])) == 1]
    plane = [s for s in sols if sum(s[0]) == 0 and sum(s[1]) == 0]
    assert len(consts) + len(plane) == len(sols), "dichotomy fails"
    for a, b in plane:
        for v in (a, b):
            m = sorted(map(abs, v)); assert m[2] == m[0] + m[1]
            assert sum(x % 2 for x in v) == 2
    eq_multiset = all(sorted(map(abs, a)) == sorted(map(abs, b)) for a, b in plane)
    has_112 = any(sorted(map(abs, a)) == [1,1,2] for a, b in plane)
    distinct = all(len(set(map(abs, a))) == 3 for a, b in plane)
    print(f"1b. {name}, |entries|<={B}: {len(sols)} solutions = {len(consts)} constant + {len(plane)} sum-zero;"
          f" additive weights same multiset in both triples: {eq_multiset};"
          f" 1:1:2 occurs: {has_112}; all additive triples have distinct |weights|: {distinct}")
    ex = [p for p in plane if sorted(map(abs, p[0])) in ([1,1,2], [1,2,3])][:2]
    print("    sample additive pairs:", ex)

a = [1,1,-2]; b = mv(T(IpR), a)
print("1c. note's example: C=I+R, a=(1,1,-2): C^T a =", b, " C b =", mv(IpR, b))
assert b == [-1,2,-1] and mv(IpR, b) == a
print("    same a with C=I-R: C^T a =", mv(T(ImR), a), "(has a zero entry, so excluded)")

print("\n== 2. Explicit hyperelliptic hexagon: which normal form occurs? ==")
def csqrt_near(w, ref):
    r = cmath.sqrt(w); return r if abs(r-ref) <= abs(-r-ref) else -r
def prod(xs):
    p = 1
    for x in xs: p *= x
    return p
def doubled_arc_tangents(A, Bp, pts, N=3000, eps=1e-6):
    """Tangents at the lifts of A and B of the doubled arc delta = g+ - g-,
    in the local coordinate z with z^2 = x - endpoint, for the straight arc A->B."""
    f = lambda x: prod(x-b for b in pts)
    mid = (A+Bp)/2; y0 = cmath.sqrt(f(mid)); out = {}
    for end in (A, Bp):
        y = y0
        for k in range(1, N+1):
            x = mid + (1-2*eps)*k/N*(end-mid)
            y = csqrt_near(f(x), y)
        G = cmath.sqrt(prod(end-b for b in pts if b != end))
        g = csqrt_near(prod(x-b for b in pts if b != end), G)
        z = y/g
        assert abs(z*z-(x-end)) < 1e-6*abs(x-end)
        out[end] = z/abs(z)            # outward direction of g+ at the lift of end
    return {A: out[A], Bp: -out[Bp]}   # g+ leaves A~, arrives at B~
def hexagon_C(w, poles):
    pts = list(w)+list(poles)
    arcs = [(w[k], w[(k+1) % 6]) for k in range(6)]
    tan = [doubled_arc_tangents(A, Bp, pts) for A, Bp in arcs]
    def inter(i, j):
        tot = 0
        for p in set(arcs[i]) & set(arcs[j]):
            v = (tan[i][p].conjugate()*tan[j][p]).imag
            assert abs(v) > 1e-6
            tot += 1 if v > 0 else -1
        return tot
    # Sanity: arcs in the same triple are disjoint, so intersect zero.
    return [[inter(i, j) for j in (1, 3, 5)] for i in (0, 2, 4)]
w = [cmath.exp(1j*math.pi*k/3) for k in range(6)]   # Z,P,Z,P,Z,P alternate
w = [complex(round(z.real, 12), round(z.imag, 12)) for z in w]
inside = [0.11+0.07j, -0.13+0.05j, 0.04-0.17j, -0.06-0.09j]
outside = [3.1+0.4j, -2.7+1.9j, 0.3-3.3j, -2.2-2.6j]
for k in range(5):
    poles = inside[:k] + outside[k:]
    C = hexagon_C(w, poles)
    nz = [C[i][j] for i in range(3) for j in range(3) if C[i][j]]
    form = "I+R" if math.prod(nz) == 1 else "I-R"
    print(f"poles inside hexagon = {k}: C = {C}, |det C| = {abs(det3(C))}, normal form {form}")
# A nonconvex embedded hexagon with the same vertex order, as a robustness check.
w2 = [1+0j, 0.5+0.9j, -0.2+0.3j, -1+0.2j, -0.4-0.8j, 0.6-0.7j]
for k, poles in ((0, outside), (1, [0.3+0.0j]+outside[1:]), (2, [0.3+0.0j, 0.1-0.4j]+outside[2:])):
    C = hexagon_C(w2, poles)
    nz = [C[i][j] for i in range(3) for j in range(3) if C[i][j]]
    print(f"nonconvex hexagon, poles inside = {k}: |det C| = {abs(det3(C))}, normal form {'I+R' if math.prod(nz)==1 else 'I-R'}")

print("\n== 3. Sphere family q_s in Q(1^3,-1^7) with vanishing periods (t,t,2t) ==")
c = [F(0), F(3), complex(0, 3)]
cq = [(F(0), F(0)), (F(3), F(0)), (F(0), F(3))]      # Gaussian rationals (re, im)
pq = [(F(10), F(0)), (F(-10), F(0)), (F(0), F(10)), (F(-7), F(-9))]
p = [complex(float(a), float(b)) for a, b in pq]
c = [complex(float(a), float(b)) for a, b in cq]
def h(x, i, s):
    num = prod((x-c[k]-s[k])/(x-c[k]) for k in range(3) if k != i)
    return num / prod(x-pj for pj in p)
def period(i, s, n=200):
    """2 * integral of sqrt(q) along the straight arc c_i -> c_i+s_i, via x = c_i + s_i sin^2(th)."""
    if s[i] == 0: return 0j
    H0 = cmath.sqrt(h(c[i], i, s)); tot = 0j; hv = H0
    # Gauss-Legendre on [0, pi/2]
    xs, ws = gl_nodes(n)
    for xg, wg in zip(xs, ws):
        th = (xg+1)*math.pi/4
        x = c[i] + s[i]*math.sin(th)**2
        hv = csqrt_near(h(x, i, s), H0)
        tot += wg*math.pi/4 * 2*math.cos(th)**2 * hv
    return 2 * 1j * s[i] * tot        # sqrt((u-1)/u) = i*cot(th)
def gl_nodes(n):
    xs, ws = [], []
    for k in range(1, n+1):
        x = math.cos(math.pi*(k-0.25)/(n+0.5))
        for _ in range(100):
            p0, p1 = 1.0, x
            for m in range(2, n+1): p0, p1 = p1, ((2*m-1)*x*p1-(m-1)*p0)/m
            dp = n*(x*p1-p0)/(x*x-1); dx = p1/dp; x -= dx
            if abs(dx) < 1e-16: break
        xs.append(x); ws.append(2/((1-x*x)*dp*dp))
    return xs, ws
lead = [1j*math.pi/2*2*cmath.sqrt(h(c[i], i, [0,0,0])) for i in range(3)]
print("leading coefficients dPer_i/ds_i at s=0 (nonzero):", [f"{abs(L):.6g}" for L in lead])
def solve(t):
    target = [t, t, 2*t]
    s = [target[i]/lead[i] for i in range(3)]
    for _ in range(30):
        Pv = [period(i, s) for i in range(3)]
        r = [Pv[i]-target[i] for i in range(3)]
        if max(abs(x) for x in r) < 1e-15*abs(t): break
        d = 1e-7*abs(t)
        J = [[(period(i, [s[k]+(d if k == j else 0) for k in range(3)]) - Pv[i])/d for j in range(3)] for i in range(3)]
        # solve J dx = r by Cramer
        D = det3(J)
        dx = []
        for j in range(3):
            Jj = [row[:] for row in J]
            for i in range(3): Jj[i][j] = r[i]
            dx.append(det3(Jj)/D)
        s = [s[k]-dx[k] for k in range(3)]
    return s, [period(i, s) for i in range(3)]
for t in (1e-2, 1e-3, 1e-4*(1+1j)):
    s, Pv = solve(t)
    print(f"t={t}: s = {[complex(round(z.real,10), round(z.imag,10)) for z in s]}")
    print(f"   Per2/Per1 - 1 = {abs(Pv[1]/Pv[0]-1):.2e}, Per3/Per1 - 2 = {abs(Pv[2]/Pv[0]-2):.2e}, Per1/t - 1 = {abs(Pv[0]/t-1):.2e}")
    assert all(abs(z) > 0 for z in s)
    # exact stratum check at a Gaussian-rational rounding of s
    sq = [(F(round(z.real*1e12), 10**12), F(round(z.imag*1e12), 10**12)) for z in s]
    zeros = [(cq[i][0]+sq[i][0], cq[i][1]+sq[i][1]) for i in range(3)]
    poles = cq + pq
    pts = zeros + poles
    assert len(set(pts)) == 10
    print("   exact: 3 simple zeros, 7 simple poles, all 10 points distinct;"
          " deg(den)-deg(num) = 7-3 = 4 so q is regular and nonzero at infinity; orders sum to",
          3 - 7, "= -4")
# Limit s -> 0: q_0 = dx^2 / prod(x-p_j) is in Q(-1^4); its area is finite and positive.
# Crude area estimate of |q_0| on a large disk (simple poles are integrable).
def area_est(Rr=60.0, n=600):
    tot = 0.0; hstep = 2*Rr/n
    for a_ in range(n):
        for b_ in range(n):
            x = complex(-Rr+(a_+0.5)*hstep, -Rr+(b_+0.5)*hstep)
            tot += hstep*hstep/abs(prod(x-pj for pj in p))
    return tot
print("limit area estimate on [-60,60]^2 (positive, finite):", f"{area_est():.4f}")

print("\n== 4. Dimension count for Q(1^s,-1^(s+4)) and a counterexample to the broad wording ==")
for s_ in range(1, 7):
    n_pts = 2*s_+4; g = (n_pts-2)//2
    dim_stratum = n_pts-2; abs_minus = 2*g; rel_minus = 0   # all zeros odd => J-fixed
    assert dim_stratum == abs_minus + rel_minus
    print(f"s={s_}: dim Q = {dim_stratum}, cover genus {g}, dim H^1_- = {abs_minus}, rel = {rel_minus}")
# Q(2,-1^6): even zero has two J-swapped preimages -> one anti-invariant relative class.
n_pts = 6; g = 2; dim_stratum = 7-2
print(f"Q(2,-1^6): dim Q = {dim_stratum}, dim H^1_-(abs) = {2*g}, rel = {dim_stratum-2*g} (nonzero)")
print("\nall assertions passed")
