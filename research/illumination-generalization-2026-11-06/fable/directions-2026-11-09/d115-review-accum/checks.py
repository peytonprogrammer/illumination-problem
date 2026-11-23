"""d115 checks for accumulation.md: (1) minor/primitivity/parity arithmetic of step 3,
(2) the strip placement matrix G against direct folding, its kernel and row rank."""
from fractions import Fraction as F
from math import gcd
from functools import reduce
import random
random.seed(115)

def isprime(q):
    return q > 1 and all(q % d for d in range(2, int(q**0.5) + 1))

# (1) Step 3: e with gcd 1, u not proportional; q prime, q !| D, D | p, gcd(p,q)=1.
bad = trials = 0
for _ in range(4000):
    k = random.randint(3, 8)
    e = [random.choice([-1, 1]) * random.randint(1, 30) for _ in range(k)]
    if reduce(gcd, e) != 1:
        continue
    u = [random.randint(-20, 20) for _ in range(k)]
    minors = [(i, j, e[i]*u[j]-e[j]*u[i]) for i in range(k) for j in range(k) if e[i]*u[j]-e[j]*u[i]]
    if not minors:
        continue
    M = minors[0][2]; D = 2*abs(M)
    q = random.choice([x for x in range(3, 400) if isprime(x) and D % x])
    p = D * random.randint(-5, 5)
    if p == 0 or gcd(p, q) != 1:
        continue
    w = [q*a + p*b for a, b in zip(e, u)]
    xs, xt, ws, wt = 2*random.randint(0, 9), 2*random.randint(0, 9), random.randint(-9, 9), random.randint(-9, 9)
    trials += 1
    g = reduce(gcd, w)
    par = (q*xs + p*ws - (q*xt + p*wt)) % 2
    parity_all = all((q*a + p*b - a) % 2 == 0 for a, b in zip(e, u))  # every abscissa keeps its parity
    if g != 1 or par != 0 or not parity_all:
        bad += 1
print(f"(1) step-3 arithmetic: {trials} trials, {bad} failures of primitivity/parity")

# Without the hypothesis D | p the conclusion can fail; show one instance.
e, u = [1, 1], [1, -1]   # gcd(e)=1, M = -2, D = 4
q, p = 3, 1
print("(1b) control, p not a multiple of D:", [q*a+p*b for a, b in zip(e, u)],
      "gcd", reduce(gcd, [q*a+p*b for a, b in zip(e, u)]))

# (2) Strip chain: m runs [a_j,b_j] stacked, travels d_j, source in run 1, target in run m.
def fold(x, s, d, a, b):
    """Billiard in strip a<x<b over vertical travel d with slope dx/dy = s.
    Returns (physical exit, sheet sign, number of periods)."""
    w = b - a; P = 2*w
    y = x + s*d - a
    k = y // P            # floor for Fractions
    r = y - k*P
    if r < w:
        return a + r, +1, k
    return a + P - r, -1, k

runs = [(F(0), F(7)), (F(3), F(11)), (F(5), F(13)), (F(2), F(9))]
d = [F(3, 2), F(2), F(5), F(1, 2)]
m = len(runs); X = sum(d); A = [sum(d[:i+1]) for i in range(m)]
P = [2*(b-a) for a, b in runs]
xs, xt = F(1), F(8)
G = [[(A[i]/X - (1 if j <= i else 0))*P[j] for j in range(m)] for i in range(m-1)]
ker = [d[j]/P[j] for j in range(m)]
assert all(sum(G[i][j]*ker[j] for j in range(m)) == 0 for i in range(m-1))
ov = [(max(runs[i][0], runs[i+1][0]), min(runs[i][1], runs[i+1][1])) for i in range(m-1)]
import itertools
agree = hits = checked = 0
for n in itertools.product(range(-13, 14), repeat=m):
    n = list(n)
    s = (xt - xs + sum(n[j]*P[j] for j in range(m)))/X
    c = [xs + s*A[i] - sum(n[j]*P[j] for j in range(i+1)) for i in range(m-1)]
    # translate form: c - c(0) == G n
    c0 = [xs + (xt-xs)*A[i]/X for i in range(m-1)]
    assert all(c[i]-c0[i] == sum(G[i][j]*n[j] for j in range(m)) for i in range(m-1))
    if all(lo < ci < hi for ci, (lo, hi) in zip(c, ov)):
        hits += 1
        x, ok = xs, True
        for j in range(m):
            x, sg, k = fold(x, s, d[j], *runs[j])
            if sg != 1 or k != n[j]:
                ok = False
            if j < m-1 and x != c[j]:
                ok = False
        ok = ok and x == xt
        agree += ok
    checked += 1
# rank of G via consecutive differences
import itertools
def rank(Mx):
    Mx = [row[:] for row in Mx]; r = 0
    for col in range(len(Mx[0])):
        piv = next((i for i in range(r, len(Mx)) if Mx[i][col] != 0), None)
        if piv is None: continue
        Mx[r], Mx[piv] = Mx[piv], Mx[r]
        for i in range(len(Mx)):
            if i != r and Mx[i][col] != 0:
                f = Mx[i][col]/Mx[r][col]
                Mx[i] = [x - f*y for x, y in zip(Mx[i], Mx[r])]
        r += 1
    return r
print(f"(2) G: kernel (d_j/P_j) verified, rank {rank(G)} of {m-1}; translate form exact on {checked} vectors;"
      f" {hits} land in the open overlaps, {agree} of them replay as legal positive-sheet paths")
