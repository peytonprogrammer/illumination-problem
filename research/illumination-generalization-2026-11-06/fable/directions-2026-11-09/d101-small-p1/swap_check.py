"""d101 Q09: brute-force check of d81 Prop P, kappa = 2 bullets, for mu = 5, 6.
For every swap-type g = (a, b)tau on [mu]^2, (i, j) -> (a j, b i), whose cycle
lengths lie in {1, 2, 3}: check f + 3z = mu, and record the largest z.
Also for non-swap (a, b) with z >= 1: record the least z (d81 claims z >= mu).
Run: python3 -B swap_check.py > swap_check.log
"""
from itertools import permutations


def cyc(perm):
    n, seen, out = len(perm), [False] * len(perm), []
    for s in range(n):
        if not seen[s]:
            L, x = 0, s
            while not seen[x]:
                seen[x] = True
                x = perm[x]
                L += 1
            out.append(L)
    return out


for mu in (5, 6):
    P = list(permutations(range(mu)))
    swap_n = swap_bad = swap_maxz = 0
    ns_minz = None
    for a in P:
        for b in P:
            g = [0] * (mu * mu)
            h = [0] * (mu * mu)
            for i in range(mu):
                for j in range(mu):
                    g[i * mu + j] = a[j] * mu + b[i]
                    h[i * mu + j] = a[i] * mu + b[j]
            c = cyc(g)
            if max(c) <= 3:
                swap_n += 1
                f, z = c.count(1), c.count(3)
                swap_bad += f + 3 * z != mu
                swap_maxz = max(swap_maxz, z)
            c = cyc(h)
            if max(c) <= 3 and 3 in c:
                z = c.count(3)
                ns_minz = z if ns_minz is None else min(ns_minz, z)
    print(f"mu={mu}: swap-type generators with cycles in {{1,2,3}}: {swap_n}; "
          f"f+3z != mu: {swap_bad}; max z: {swap_maxz}; "
          f"non-swap with z>=1: min z = {ns_minz}")
