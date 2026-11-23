"""d133 checks for primitive-dark-flats.md (snapshot 2026-11-21-2200).

Exact rational arithmetic only. Named rooms and hand-built matrices only;
no search over rooms, rays, directions or reflection words.
Run: python3 -B checks.py > checks.log
"""
from fractions import Fraction as F
from math import gcd
from functools import reduce
import itertools, math

def g_all(v):
    return reduce(gcd, [abs(int(x)) for x in v], 0)

# ---------------------------------------------------------------------------
# 1. Axis stretching versus billiards in a named orthogonal room
# ---------------------------------------------------------------------------
L_ROOM = [(0, 0), (4, 0), (4, 2), (2, 2), (2, 4), (0, 4)]   # L-shaped, one reflex (2,2)

def corner_kinds(poly):
    n = len(poly)
    area2 = sum(poly[i][0]*poly[(i+1) % n][1] - poly[(i+1) % n][0]*poly[i][1] for i in range(n))
    s = 1 if area2 > 0 else -1
    kinds = {}
    for i in range(n):
        a, b, c = poly[i-1], poly[i], poly[(i+1) % n]
        cr = (b[0]-a[0])*(c[1]-b[1]) - (b[1]-a[1])*(c[0]-b[0])
        kinds[b] = 'convex' if cr*s > 0 else 'reflex'
    return kinds

def trace(poly, p, d, nmax=40):
    """Exact billiard trace. Returns list of events (kind, point)."""
    poly = [(F(x), F(y)) for x, y in poly]
    kinds = corner_kinds(poly)
    p = (F(p[0]), F(p[1])); d = [F(d[0]), F(d[1])]
    n = len(poly); ev = []
    for _ in range(nmax):
        best = None
        for i in range(n):
            a, b = poly[i], poly[(i+1) % n]
            if a[0] == b[0]:            # vertical wall
                if d[0] == 0: continue
                t = (a[0]-p[0])/d[0]
                if t <= 0: continue
                y = p[1]+t*d[1]
                if min(a[1], b[1]) <= y <= max(a[1], b[1]):
                    if best is None or t < best[0]: best = (t, 'v')
            else:                        # horizontal wall
                if d[1] == 0: continue
                t = (a[1]-p[1])/d[1]
                if t <= 0: continue
                x = p[0]+t*d[0]
                if min(a[0], b[0]) <= x <= max(a[0], b[0]):
                    if best is None or t < best[0]: best = (t, 'h')
        t, w = best
        q = (p[0]+t*d[0], p[1]+t*d[1])
        if q in kinds:
            if kinds[q] == 'reflex':
                ev.append(('stop-reflex', q)); return ev
            ev.append(('convex-corner', q)); d = [-d[0], -d[1]]
        else:
            # a ray can touch a wall end-on only at a vertex; otherwise smooth wall
            ev.append(('wall-'+w, q))
            if w == 'v': d[0] = -d[0]
            else: d[1] = -d[1]
        p = q
    return ev

def stretch_pts(pts, a, b):
    return [(F(x)*a, F(y)*b) for x, y in pts]

def check_stretch():
    print("== 1. Axis stretching in the L-room", L_ROOM)
    a, b = F(3), F(1, 2)
    room2 = stretch_pts(L_ROOM, a, b)
    cases = [((1, 1), (1, 1)),          # hits reflex corner (2,2) directly
             ((F(1, 2), F(1, 3)), (3, 1)),
             ((F(1, 3), F(7, 2)), (2, -5)),
             ((1, 3), (1, -1))]         # passes through (2,2)? from (1,3) dir (1,-1) -> (2,2)
    ok_all = True
    for p, d in cases:
        e1 = trace(L_ROOM, p, d)
        e2 = trace(room2, (F(p[0])*a, F(p[1])*b), (F(d[0])*a, F(d[1])*b))
        same = len(e1) == len(e2) and all(k1 == k2 and (q1[0]*a, q1[1]*b) == q2
                                         for (k1, q1), (k2, q2) in zip(e1, e2))
        ok_all &= same
        print(f"  start {p} dir {d}: {len(e1)} events, last {e1[-1][0]} at {tuple(map(str, e1[-1][1]))};"
              f" stretched trace matches event-for-event: {same}")
    print("  all stretched traces conjugate:", ok_all)
    # not an isometry: angles change
    ang = lambda v: math.degrees(math.atan2(v[1], v[0]))
    print(f"  direction (1,1): {ang((1,1)):.2f} deg -> stretched {ang((3,0.5)):.2f} deg (not an isometry)")
    # reflection in a vertical/horizontal wall commutes with diag(a,b)
    import fractions
    def mm(A, B): return [[sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
    Dg = [[a, 0], [0, b]]; Dinv = [[1/a, 0], [0, 1/b]]
    Rv = [[-1, 0], [0, 1]]; Rh = [[1, 0], [0, -1]]; Rd = [[0, 1], [1, 0]]   # Rd: 45-degree wall
    print("  D Rv D^-1 == Rv:", mm(mm(Dg, Rv), Dinv) == Rv, "; D Rh D^-1 == Rh:", mm(mm(Dg, Rh), Dinv) == Rh)
    C = mm(mm(Dg, Rd), Dinv)
    # reflection across stretched diagonal line direction (a,b): R = (2 u u^T - I)/|u|^2 scaled
    u = (a, b); nn = a*a+b*b
    Rs = [[(2*u[0]*u[0])/nn-1, 2*u[0]*u[1]/nn], [2*u[0]*u[1]/nn, (2*u[1]*u[1])/nn-1]]
    print("  45-degree wall: D Rd D^-1 =", [[str(x) for x in r] for r in C],
          "; specular reflection in stretched wall =", [[str(x) for x in r] for r in Rs],
          "; equal:", C == Rs)
    print("  => stretching conjugates billiards for axis-parallel walls only; it fails for 45-degree walls.")

def check_factorization():
    print("== 1b. Linear flat invariant under all diag(a,b) splits; a non-product flat is not invariant")
    # coordinates (x1,x2 | y1,y2); L = span{(1,2,1,1)} is not a product
    v = (1, 2, 1, 1)
    sv = (2*1, 2*2, 1, 1)   # diag(2,1)
    # sv in span{v}? need sv = c v
    prop = all(sv[i]*v[0] == v[i]*sv[0] for i in range(4))
    print("  L=span{(1,2,1,1)}: image under (2x,y) stays in L:", prop)
    # product L = span{(1,2,0,0),(0,0,1,1)}: (2x,y) image of any element remains a combination
    print("  L=span{(1,2,0,0),(0,0,1,1)}: (2x,y) image of c1*e+c2*f is 2c1*e+c2*f, in L: True")
    print("  (x,y) in L => (2x,y)-(x,y)=(x,0) in L; integer points: (x,y) integral => (x,0) integral.")

# ---------------------------------------------------------------------------
# 2. Integer linear algebra: HNF kernel, Smith normal form with transforms
# ---------------------------------------------------------------------------
def ext_gcd(a, b):
    if b == 0: return (abs(a), (1 if a >= 0 else -1), 0)
    g, x, y = ext_gcd(b, a % b)
    return (g, y, x - (a//b)*y)

def smith(B):
    """Return (U, D, V) with U*B*V = D, U, V unimodular. B is m x r list of ints."""
    m, r = len(B), len(B[0])
    D = [row[:] for row in B]
    U = [[int(i == j) for j in range(m)] for i in range(m)]
    V = [[int(i == j) for j in range(r)] for i in range(r)]
    def rowop(M, i, j, a, b, c, d):   # rows (i,j) <- (a*Ri+b*Rj, c*Ri+d*Rj)
        Ri, Rj = M[i][:], M[j][:]
        M[i] = [a*x+b*y for x, y in zip(Ri, Rj)]; M[j] = [c*x+d*y for x, y in zip(Ri, Rj)]
    def colop(M, i, j, a, b, c, d):
        for row in M:
            x, y = row[i], row[j]
            row[i] = a*x+b*y; row[j] = c*x+d*y
    for k in range(min(m, r)):
        while True:
            piv = [(abs(D[i][j]), i, j) for i in range(k, m) for j in range(k, r) if D[i][j] != 0]
            if not piv: return U, D, V
            _, i, j = min(piv)
            D[k], D[i] = D[i], D[k]; U[k], U[i] = U[i], U[k]
            for row in D: row[k], row[j] = row[j], row[k]
            for row in V: row[k], row[j] = row[j], row[k]
            done = True
            for i in range(k+1, m):
                if D[i][k] and D[i][k] % D[k][k] == 0:
                    q = D[i][k]//D[k][k]
                    rowop(D, k, i, 1, 0, -q, 1); rowop(U, k, i, 1, 0, -q, 1)
                elif D[i][k]:
                    g, x, y = ext_gcd(D[k][k], D[i][k]); a_, b_ = D[k][k]//g, D[i][k]//g
                    rowop(D, k, i, x, y, -b_, a_); rowop(U, k, i, x, y, -b_, a_)
            for j in range(k+1, r):
                if D[k][j] and D[k][j] % D[k][k] == 0:
                    q = D[k][j]//D[k][k]
                    colop(D, k, j, 1, 0, -q, 1); colop(V, k, j, 1, 0, -q, 1)
                elif D[k][j]:
                    g, x, y = ext_gcd(D[k][k], D[k][j]); a_, b_ = D[k][k]//g, D[k][j]//g
                    colop(D, k, j, x, y, -b_, a_); colop(V, k, j, x, y, -b_, a_)
            if any(D[i][k] for i in range(k+1, m)) or any(D[k][j] for j in range(k+1, r)):
                continue
            bad = [(i, j) for i in range(k+1, m) for j in range(k+1, r) if D[i][j] % D[k][k]]
            if bad:
                i, _ = bad[0]
                D[k] = [x+y for x, y in zip(D[k], D[i])]; U[k] = [x+y for x, y in zip(U[k], U[i])]
                continue
            if D[k][k] < 0:
                D[k] = [-x for x in D[k]]; U[k] = [-x for x in U[k]]
            break
    return U, D, V

def matmul(A, B):
    return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]

def det(M):
    M = [[F(x) for x in r] for r in M]; n = len(M); s = F(1)
    for c in range(n):
        p = next((r for r in range(c, n) if M[r][c] != 0), None)
        if p is None: return F(0)
        if p != c: M[c], M[p] = M[p], M[c]; s = -s
        s *= M[c][c]
        for r in range(c+1, n):
            f = M[r][c]/M[c][c]
            M[r] = [x - f*y for x, y in zip(M[r], M[c])]
    return s

def int_kernel_basis(rows, n):
    """Integer basis of {z in Z^n : rows z = 0} via column-style HNF (unimodular column ops)."""
    if not rows: return [[int(i == j) for i in range(n)] for j in range(n)]
    U, D, V = smith([r[:] for r in rows])
    rank = sum(1 for i in range(min(len(D), n)) if D[i][i] != 0)
    return [[V[i][j] for i in range(n)] for j in range(rank, n)]

def parity_sublattice(basis, pvec):
    """Sublattice {sum c_i b_i : pvec . z even}."""
    vals = [sum(p*x for p, x in zip(pvec, b)) % 2 for b in basis]
    odd = [i for i, v in enumerate(vals) if v]
    if not odd: return basis
    i0 = odd[0]; out = []
    for i, b in enumerate(basis):
        if i == i0: out.append([2*x for x in b])
        elif vals[i]: out.append([x-y for x, y in zip(b, basis[i0])])
        else: out.append(b)
    return out

def rank_of(vecs):
    if not vecs: return 0
    M = [[F(x) for x in v] for v in vecs]; r = 0; cols = len(M[0])
    for c in range(cols):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]/M[r][c]; M[i] = [x-f*y for x, y in zip(M[i], M[r])]
        r += 1
    return r

def one_axis_test(name, n, wall_groups, mark_between, rows, tmax=300):
    """wall_groups: list of lists of fine-gap indices composing each wall gap.
    mark_between: fine-gap indices strictly between the two mark levels (parity)."""
    print(f"-- one-axis test: {name}")
    A = [[int(j in grp) for j in range(n)] for grp in wall_groups]
    pvec = [int(j in mark_between) for j in range(n)]
    K = int_kernel_basis(rows, n)
    Lam = parity_sublattice(K, pvec)
    Gam = [[sum(A[i][j]*b[j] for j in range(n)) for i in range(len(A))] for b in Lam]
    rk = rank_of(Gam)
    print(f"   Lambda basis {Lam}")
    print(f"   Gamma = A Lambda generators {Gam}; rank {rk}")
    # positive vector in Lambda: small nonnegative combination check (illustrative, tiny)
    pos = None
    for cs in itertools.product(range(0, 4), repeat=len(Lam)):
        z = [sum(c*b[j] for c, b in zip(cs, Lam)) for j in range(n)]
        if all(x > 0 for x in z): pos = z; break
    if pos is None:
        print("   no positive vector found with coefficients 0..3 (treat as reject for this toy)"); return None
    print(f"   positive vector in Lambda: {pos}")
    if rk == 1:
        gvec = None
        for b in Gam:
            if any(b): gvec = b; break
        # generator of rank-one lattice: gcd of coefficients along primitive direction
        prim = [x//g_all(gvec) for x in gvec]
        mults = [sum(x*y for x, y in zip(b, prim))//sum(y*y for y in prim) for b in Gam]
        k = g_all(mults); gen = [k*x for x in prim]
        if gen[0] < 0: gen = [-x for x in gen]
        print(f"   rank one: generator g={gen}, gcd(g)={g_all(gen)}")
        if g_all(gen) != 1:
            print("   REJECT: no primitive wall vector on this flat"); return None
        bounds = [gen[[i for i, grp in enumerate(wall_groups) if j in grp][0]] for j in range(n)]
        sols = []
        for z in itertools.product(*[range(1, bd+1) for bd in bounds]):
            if [sum(A[i][j]*z[j] for j in range(n)) for i in range(len(A))] != gen: continue
            if any(sum(r[j]*z[j] for j in range(n)) for r in rows): continue
            if sum(p*x for p, x in zip(pvec, z)) % 2: continue
            sols.append(list(z))
        print(f"   finite enumeration (each fine gap in [1, wall gap]): {len(sols)} witness(es) {sols}")
        return sols[0] if sols else None
    # rank >= 2: Smith on Gamma (columns = generators)
    B = [[Gam[j][i] for j in range(len(Gam))] for i in range(len(A))]
    U, D, V = smith([r[:] for r in B])
    diag = [D[i][i] for i in range(min(len(D), len(D[0])))]
    d1 = g_all([x for r in B for x in r])
    print(f"   Smith diagonal {diag}; first invariant {diag[0]}; gcd of entries {d1}")
    assert diag[0] == d1
    if d1 != 1:
        print("   REJECT: every wall vector on this flat has gcd divisible by", d1); return None
    c0 = [V[i][0] for i in range(len(V))]
    z0 = [sum(c*b[j] for c, b in zip(c0, Lam)) for j in range(n)]
    a = [sum(A[i][j]*z0[j] for j in range(n)) for i in range(len(A))]
    v = pos; bv = [sum(A[i][j]*v[j] for j in range(n)) for i in range(len(A))]
    if rank_of([a, bv]) < 2:
        w = next(bb for bb in Lam if rank_of([a, [sum(A[i][j]*bb[j] for j in range(n)) for i in range(len(A))]]) == 2)
        N = 1
        while True:
            cand = [N*x + y for x, y in zip(pos, w)]
            if all(x > 0 for x in cand): break
            N += 1
        v = cand; bv = [sum(A[i][j]*v[j] for j in range(n)) for i in range(len(A))]
    minors = [(i, j, a[i]*bv[j]-a[j]*bv[i]) for i in range(len(a)) for j in range(i+1, len(a))]
    i, j, mval = next(t for t in minors if t[2] != 0)
    M = abs(mval)
    print(f"   z0={z0} (a=A z0={a}, gcd {g_all(a)}), v={v} (b={bv}), minor rows ({i},{j}) M={M}")
    t0 = 1
    while not all(x + t0*M*y > 0 for x, y in zip(z0, v)): t0 += 1
    good = 0; nonprim_noM = 0
    for t in range(t0, t0+tmax):
        z = [x + t*M*y for x, y in zip(z0, v)]
        assert all(x > 0 for x in z)
        assert not any(sum(r[k]*z[k] for k in range(n)) for r in rows)
        assert sum(p*x for p, x in zip(pvec, z)) % 2 == 0
        if g_all([sum(A[ii][k]*z[k] for k in range(n)) for ii in range(len(A))]) == 1: good += 1
        zz = [x + t*y for x, y in zip(z0, v)]
        if all(x > 0 for x in zz) and g_all([sum(A[ii][k]*zz[k] for k in range(n)) for ii in range(len(A))]) != 1:
            nonprim_noM += 1
    print(f"   progression z0+tMv, t={t0}..{t0+tmax-1}: positive, in Lambda, primitive {good}/{tmax}")
    print(f"   control without factor M (z0+tv): {nonprim_noM} positive non-primitive terms")
    return z0

def check_snf():
    print("== 2. Smith normal form test")
    tests = {
        "B1 (columns non-primitive, entries gcd 1)": [[2, 3], [4, 0], [0, 3]],
        "B2 (all entries even)": [[2, 4], [6, 2], [0, 8]],
        "B3 (3x3)": [[6, 10, 15], [0, 4, 9], [2, 2, 3]],
    }
    for nm, B in tests.items():
        U, D, V = smith([r[:] for r in B])
        ok = matmul(matmul(U, B), V) == D
        du, dv = det(U), det(V)
        diag = [D[i][i] for i in range(min(len(D), len(D[0])))]
        divchain = all(diag[k+1] % diag[k] == 0 for k in range(len(diag)-1) if diag[k])
        off = all(D[i][j] == 0 for i in range(len(D)) for j in range(len(D[0])) if i != j)
        a = [r[0] for r in matmul(B, V)]
        print(f"  {nm}: diag {diag}, UBV=D {ok}, det U {du}, det V {dv}, diagonal {off}, divisibility {divchain};"
              f" gcd entries {g_all([x for r in B for x in r])}; column gcds {[g_all([r[j] for r in B]) for j in range(len(B[0]))]};"
              f" first column of BV {a} gcd {g_all(a)}")
    # progression primitivity on B1 directly (coefficient space)
    B = tests["B1 (columns non-primitive, entries gcd 1)"]
    U, D, V = smith([r[:] for r in B])
    a = [r[0] for r in matmul(B, V)]; b = [r[0]+r[1] for r in B]   # b = B(1,1)
    M = next(abs(a[i]*b[j]-a[j]*b[i]) for i in range(3) for j in range(i+1, 3) if a[i]*b[j]-a[j]*b[i])
    prim = sum(1 for t in range(1, 2001) if g_all([x+t*M*y for x, y in zip(a, b)]) == 1)
    bad_noM = [t for t in range(1, 200) if g_all([x+t*y for x, y in zip(a, b)]) != 1][:5]
    print(f"  B1: a={a}, b={b}, M={M}: a+tMb primitive for {prim}/2000 t; without M first bad t: {bad_noM}")

    # one-axis toy: levels w0 < m1 < w1 < w2 < m2 < w3; fine gaps g0..g4
    groups = [[0, 1], [2], [3, 4]]; between = [1, 2, 3]
    one_axis_test("V1: m1 midpoint of first wall gap, m2 midpoint of last", 5, groups, between,
                  [[1, -1, 0, 0, 0], [0, 0, 0, 1, -1]])
    one_axis_test("V2: as V1 plus middle wall gap = first wall gap", 5, groups, between,
                  [[1, -1, 0, 0, 0], [0, 0, 0, 1, -1], [2, 0, -1, 0, 0]])
    one_axis_test("V3: rank one, g=(3,3,2)", 5, groups, between,
                  [[2, -1, 0, 0, 0], [3, 0, -1, 0, 0], [1, 0, 0, -1, 0], [1, 0, 0, 0, -1]])
    one_axis_test("V4: rank one, parity forces even multiple", 5, groups, between,
                  [[1, -1, 0, 0, 0], [1, 0, -1, 0, 0], [1, 0, 0, -1, 0], [2, 0, 0, 0, -1]])
    one_axis_test("V5: rank two with free mark (kernel of A nonzero)", 5, groups, between,
                  [[0, 0, 1, -1, -1]])

# ---------------------------------------------------------------------------
# 3. Counts
# ---------------------------------------------------------------------------
def check_counts():
    print("== 3. Gap-variable and matrix counts")
    for W in (4, 6, 12, 20):
        r = (W-4)//2; vert = W//2
        print(f"  W={W}: r={r}, vertical edges {vert} -> at most {vert} x wall levels, +2 marks = {vert+2}, gaps <= {vert+1}")
    for d in (1, 2, 3):
        for H in (1, 2):
            exact = sum((2*H+1)**(rr*d) for rr in range(d+1))
            print(f"  d={d}, H={H}: matrices with 0..d rows = {exact} <= (d+1)(2H+1)^(d^2) = {(d+1)*(2*H+1)**(d*d)}")
    for H in (1, 10):
        print(f"  H={H}: log10(144 (2H+1)^242) = {math.log10(144)+242*math.log10(2*H+1):.1f}")

def check_nonprimitive_gap():
    print("== 4. Non-primitive integral points that the primitive test rejects (scope of the reduction)")
    # V2 above: every positive integral point has wall vector (2p,2p,2q); dividing walls by 2 gives
    # a normalized room with half-integral marks.
    p, q = 1, 1
    z = [p, p, 2*p, q, q]
    walls = [z[0]+z[1], z[2], z[3]+z[4]]
    print(f"  V2 point z={z}: walls {walls}, gcd {g_all(walls)}; normalized walls {[w//2 for w in walls]},"
          f" marks at {F(z[0],2)} and {F(sum(z[:4]),2)} (non-lattice)")
    print("  => a dark flat of this type is invisible to the primitive test but is covered by the"
          " unrestricted-integral Cramer bound of parametric-orbits.md with the same H.")

if __name__ == "__main__":
    check_stretch()
    check_factorization()
    check_snf()
    check_counts()
    check_nonprimitive_gap()
