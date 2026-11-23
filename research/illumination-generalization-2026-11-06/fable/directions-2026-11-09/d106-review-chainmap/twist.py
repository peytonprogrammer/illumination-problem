"""D106 claim 2: exact arithmetic checks of the twist-overlap test.
Leaves are circles R/Z (circumference normalised to 1); F rotates s's leaf by p/u
and t's leaf by p'/v with gcd(p,u)=gcd(p',v)=1. Arcs are open, with rational ends."""
from fractions import Fraction as Fr
from math import gcd, lcm
import random
random.seed(106)

def inarc(x, a, L):            # open arc (a, a+L) on R/Z, 0 < L < 1
    return 0 < (x - a) % 1 < L

def run(u, p, v, q, s0, t0, aI, LI, aJ, LJ):
    g = gcd(u, v)
    A = {i % g for i in range(u) if inarc(s0 + Fr(p*i, u), aI, LI)}
    B = {j % g for j in range(v) if inarc(t0 + Fr(q*j, v), aJ, LJ)}
    brute = any(inarc(s0 + Fr(p*k, u), aI, LI) and inarc(t0 + Fr(q*k, v), aJ, LJ) for k in range(lcm(u, v)))
    return bool(A & B), brute, A, B, g

def rnd(den=60):
    return Fr(random.randrange(den), den)

# 1. "iff": residue test equals brute-force search for a common power.
mism = 0; trials = 0; growth_fail = 0; one_side_fail = 0; growth_cases = 0
for _ in range(40000):
    u = random.randint(1, 18); v = random.randint(1, 18)
    p = random.choice([x for x in range(1, u+1) if gcd(x, u) == 1])
    q = random.choice([x for x in range(1, v+1) if gcd(x, v) == 1])
    LI = Fr(random.randint(1, 59), 60); LJ = Fr(random.randint(1, 59), 60)
    test, brute, A, B, g = run(u, p, v, q, rnd(), rnd(), rnd(), LI, rnd(), LJ)
    trials += 1; mism += (test != brute)
    # 2. growth consequence: both arcs longer than g/u, g/v  => witness
    if LI > Fr(g, u) and LJ > Fr(g, v):
        growth_cases += 1; growth_fail += (not brute)
    # 3. one arc beats spacing, other meets its orbit at least once => witness
    if LI > Fr(g, u) and B:
        one_side_fail += (not brute)
print(f"iff test: {trials} random instances, mismatches residue-test vs brute force: {mism}")
print(f"growth (both arcs beat spacing): {growth_cases} instances, failures: {growth_fail}")
print(f"one-sided growth: failures: {one_side_fail}")

# 4. Equality case: an open arc of length exactly g/u can miss a residue.
u, v = 6, 4; g = gcd(u, v)
test, brute, A, B, _ = run(u, 1, v, 1, Fr(0), Fr(0), Fr(0), Fr(g, u), Fr(0), Fr(g, v))
print(f"equality case u=6,v=4,g=2, arcs (0,g/u),(0,g/v) from phase 0: A={A} B={B} witness={brute}")

# 5. Large equal periods: u = v = N, s and t rotate in lockstep (A, B disjoint for every N).
for N in (10, 100, 1000):
    test, brute, A, B, g = run(N, 1, N, 1, Fr(0), Fr(1, 2), Fr(0), Fr(1, 4), Fr(0), Fr(1, 4))
    print(f"u=v={N}: |A|={len(A)} |B|={len(B)} overlap={test} brute={brute}")
# Also coprime-free large periods with g large: u=N, v=2N.
for N in (10, 100, 1000):
    test, brute, A, B, g = run(N, 1, 2*N, 1, Fr(0), Fr(1, 2), Fr(0), Fr(1, 5), Fr(0), Fr(1, 5))
    print(f"u={N}, v={2*N}, g={g}: overlap={test} brute={brute}")
