"""D232 claims 1, 5, 7, 8: exact randomized identity checks (fractions only).
Passage equations a_j s = z_{j+1} - z_j + b_j + P_j k_j, j=0..m-1, z_0=z_m=0."""
import random, time, math
from fractions import Fraction as F
random.seed(232)
t0 = time.process_time()
def rq(lo=1, hi=30, den=7): return F(random.randint(lo, hi), random.randint(1, den))
def solve(a, P, b, k):
    m = len(a); H = sum(a)
    s = (sum(b) + sum(P[j]*k[j] for j in range(m))) / H
    z = [F(0)]
    for j in range(m - 1):
        z.append(z[-1] + a[j]*s - b[j] - P[j]*k[j])
    # closure check z_m = 0
    assert z[-1] + a[m-1]*s - b[m-1] - P[m-1]*k[m-1] == 0
    return z[1:]
def vA(a, P, b):
    m = len(a); H = sum(a); Y = [sum(a[:i]) for i in range(m + 1)]
    v = [Y[i]*sum(b)/H - sum(b[:i]) for i in range(1, m)]
    A = [[P[j]*(Y[i]/H - (1 if j < i else 0)) for j in range(m)] for i in range(1, m)]
    return v, A, Y, H
bad = dict(elim=0, tau=0, char=0, inv=0, rel=0, offset=0, kern=0, rank=0, pot=0)
trials = 0
for trial in range(400):
    m = random.randint(2, 7); g = m - 1
    a = [rq() for _ in range(m)]; P = [rq(1, 20, 3) for _ in range(m)]; b = [F(random.randint(-20, 20), random.randint(1, 5)) for _ in range(m)]
    v, A, Y, H = vA(a, P, b)
    k = [random.randint(-5, 5) for _ in range(m)]
    z = solve(a, P, b, k)
    if z != [v[i] + sum(A[i][j]*k[j] for j in range(m)) for i in range(g)]: bad['elim'] += 1
    # claim 7: real (here non-integer rational) middle winding tau
    M = random.randrange(m); tau = F(random.randint(-50, 50), 13)
    k2 = k[:]; k2[M] = tau
    z2 = solve(a, P, b, k2)
    k0 = k[:]; k0[M] = 0
    if z2 != [v[i] + sum(A[i][j]*k0[j] for j in range(m)) + tau*A[i][M] for i in range(g)]: bad['tau'] += 1
    # characters: arbitrary real (rational) ell
    ell = [F(random.randint(-9, 9), random.randint(1, 6)) for _ in range(g)]
    L = sum(ell[i]*Y[i+1] for i in range(g)) / H
    n = [P[j]*(sum(ell[i] for i in range(g) if i + 1 > j) - L) for j in range(m)]
    if any(sum(ell[i]*A[i][j] for i in range(g)) != -n[j] for j in range(m)): bad['char'] += 1
    if any(ell[i-1] != n[i-1]/P[i-1] - n[i]/P[i] for i in range(1, m)): bad['inv'] += 1
    if sum(n[j]*a[j]/P[j] for j in range(m)) != 0: bad['rel'] += 1
    if sum(ell[i]*v[i] for i in range(g)) != -sum(n[j]*b[j]/P[j] for j in range(m)): bad['offset'] += 1
    # claim 5: kernel line (a_j/P_j)
    kap = [a[j]/P[j] for j in range(m)]
    if any(sum(A[i][j]*kap[j] for j in range(m)) != 0 for i in range(g)): bad['kern'] += 1
    # rank of A = g (row reduce)
    Mx = [r[:] for r in A]; rk = 0; col = 0
    while rk < g and col < m:
        piv = next((r for r in range(rk, g) if Mx[r][col] != 0), None)
        if piv is None: col += 1; continue
        Mx[rk], Mx[piv] = Mx[piv], Mx[rk]
        for r in range(g):
            if r != rk and Mx[r][col] != 0:
                f = Mx[r][col]/Mx[rk][col]; Mx[r] = [x - f*y for x, y in zip(Mx[r], Mx[rk])]
        rk += 1; col += 1
    if rk != g: bad['rank'] += 1
    # claim 8 potential bound |n_j| <= P_j * sum|ell| <= P_j sqrt(g) |ell|
    s1 = sum(abs(x) for x in ell); nrm = math.sqrt(sum(float(x*x) for x in ell))
    if any(abs(n[j]) > P[j]*s1 or float(abs(n[j])) > float(P[j])*math.sqrt(g)*nrm + 1e-12 for j in range(m)): bad['pot'] += 1
    trials += 1
print("trials", trials, "failures", bad)
print(f"CPU {time.process_time()-t0:.2f}s")
