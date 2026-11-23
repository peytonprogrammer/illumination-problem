"""d199 referee checks: exact arithmetic for the three-chamber family X=Y=3k+1.

Standard library only. Named rooms only (the d152 three-chamber room for
k = 6..300, plus R22 numbers quoted from d154). No ray, direction, word or
room-size search, and no monodromy enumeration.
Run: python3 -B checks.py > checks.log
"""
import math
import time
from collections import Counter

T0 = time.process_time()


def rect(a, b, c, d):
    return {(i, j) for i in range(a, b) for j in range(c, d)}


def three(X, Y):  # identical to d152 checks.py
    return (rect(0, 3, 0, 3) | rect(3, 3 + X, 1, 2) | rect(3 + X, 6 + X, 0, 3)
            | rect(6 + X, 6 + X + Y, 1, 2) | rect(6 + X + Y, 9 + X + Y, 0, 3))


def classify(cells):
    """Lattice points by the 2x2 cell pattern around them."""
    pts = {(i + a, j + b) for (i, j) in cells for a in (0, 1) for b in (0, 1)}
    cnt = Counter()
    for (x, y) in pts:
        occ = [(x - 1 + a, y - 1 + b) in cells for a in (0, 1) for b in (0, 1)]
        s = sum(occ)
        if s == 4:
            cnt["interior"] += 1
        elif s == 3:
            cnt["reflex"] += 1
        elif s == 1:
            cnt["convex"] += 1
        elif s == 2:
            # occ order: (x-1,y-1),(x-1,y),(x,y-1),(x,y); diagonal pairs are pinches
            if (occ[0] and occ[3]) or (occ[1] and occ[2]):
                cnt["pinch"] += 1
            else:
                cnt["smooth"] += 1
    return cnt


def side_lengths(cells):
    """Trace the boundary (single cycle assumed) and return merged side lengths."""
    edges = {}
    for (i, j) in cells:
        for (p, q, nb) in (((i, j), (i + 1, j), (i, j - 1)), ((i + 1, j), (i + 1, j + 1), (i + 1, j)),
                           ((i + 1, j + 1), (i, j + 1), (i, j + 1)), ((i, j + 1), (i, j), (i - 1, j))):
            if nb not in cells:
                edges[p] = q  # counterclockwise orientation, no pinches so out-degree 1
    start = min(edges)
    cyc, p = [start], edges[start]
    while p != start:
        cyc.append(p)
        p = edges[p]
    # keep turning vertices only
    n = len(cyc)
    verts = [cyc[k] for k in range(n)
             if (cyc[k][0] - cyc[k - 1][0], cyc[k][1] - cyc[k - 1][1])
             != (cyc[(k + 1) % n][0] - cyc[k][0], cyc[(k + 1) % n][1] - cyc[k][1])]
    m = len(verts)
    h = [abs(verts[(k + 1) % m][0] - verts[k][0]) for k in range(m)]
    v = [abs(verts[(k + 1) % m][1] - verts[k][1]) for k in range(m)]
    return m, math.gcd(*[a for a in h if a]), math.gcd(*[b for b in v if b])


print("== Item 2: area, double, pillowcase degree, gcd with 6 (k = 6..300)")
bad = []
rows = []
for k in range(6, 301):
    X = Y = 3 * k + 1
    cells = three(X, Y)
    A = len(cells)
    c = classify(cells)
    W, hg, vg = side_lengths(cells)
    r, cv = c["reflex"], c["convex"]
    double_area = 2 * A            # two copies of P
    pillow_area = 2                # double of the unit square = R^2/2Z^2 mod +-1
    n = double_area // pillow_area
    regQ = 2 * c["interior"] + c["smooth"]   # regular Q-points over the four sites
    # Riemann-Hurwitz/Gauss-Bonnet for Q -> B of degree n (both spheres):
    #   fibre sum over 4 sites: 2*regQ + 1*convex + 3*reflex = 4n
    #   ramification: regQ + 2*reflex = 2n - 2
    ok = (A == 27 + X + Y and n == 29 + 6 * k and W == 20 and r == 8 and cv == 12
          and c["pinch"] == 0 and hg == 1 and vg == 1 and math.gcd(n, 6) == 1
          and 2 * regQ + cv + 3 * r == 4 * n and regQ + 2 * r == 2 * n - 2)
    rows.append((k, X, A, n, W, r, cv, regQ, hg, vg))
    if not ok:
        bad.append(k)
for row in rows[:4] + rows[-2:]:
    print("  k=%d X=Y=%d area=%d n=%d W=%d r=%d convex=%d regQ=%d gcd=(%d,%d)" % row)
print("  all k=6..300: area=27+X+Y, n=2*area/2=29+6k, W=20, r=8, no pinch, gcd 1, gcd(n,6)=1,"
      " RH fibre identities hold:", not bad, "failures:", bad)
print("  n mod 6 values:", sorted({row[3] % 6 for row in rows}))
print("  cross-check d153: k=9 (X=Y=28) n =", 29 + 6 * 9, "; X=Y=26 area =", 27 + 52)

print("\n== Item 3: admissible block sizes d (1<d<n, d|n, d<=r=8)")
adm = {}
for (k, X, A, n, W, r, *_ ) in rows:
    ds = [d for d in range(2, n) if n % d == 0 and d <= r]
    adm[k] = ds
allds = sorted({d for ds in adm.values() for d in ds})
print("  union of admissible d over k=6..300:", allds)
c5 = all((5 in adm[k]) == (k % 5 == 1) for k in adm)
c7 = all((7 in adm[k]) == (k % 7 == 1) for k in adm)
print("  d=5 admissible iff k=1 mod 5:", c5, "; d=7 admissible iff k=1 mod 7:", c7)
print("  max zeros on N, floor(r/d), for admissible d:", sorted({8 // d for d in allds}))
both = [k for k in adm if set(adm[k]) == {5, 7}]
print("  k with both 5 and 7 admissible (k=1 mod 35):", both[:5], "...")
# block size vs number of blocks: blocks m = n/d. The bounded quantity is d.
print("  number of blocks m=n/d when d admissible (first five):",
      [(k, d, (29 + 6 * k) // d) for k in adm for d in adm[k]][:5])
# a mistaken bound on the number of blocks m<=8 would need d=n/m >= n/8:
wrong = [(k, m) for k in adm for m in range(2, 9) if (29 + 6 * k) % m == 0]
print("  (if m<=8 were the bound instead) k with some m in 2..8 dividing n, count:", len(wrong),
      "same set of k as d-bound:", sorted({k for k, _ in wrong}) == sorted(k for k in adm if adm[k]))

print("\n== Item 4: primitivity (no admissible d), no darkness hypothesis")
prim = [k for k in adm if not adm[k]]
print("  k=35j (j=1..8) all primitive:", all(not adm[35 * j] for j in range(1, 9)))
print("  primitive k in 6..300:", len(prim), "of", len(adm),
      "; density 24/35 =", round(24 / 35, 4), "observed", round(len(prim) / len(adm), 4))
print("  first primitive k:", prim[:10])
print("  primitive iff k!=1 mod 5 and k!=1 mod 7:",
      all((not adm[k]) == (k % 5 != 1 and k % 7 != 1) for k in adm))
primes = [k for k in prim if all((29 + 6 * k) % p for p in range(2, math.isqrt(29 + 6 * k) + 1))]
print("  primitive k whose n is prime (primitive for trivial reasons), first:", primes[:8])
print("  k=6: n=%d, admissible d=%s; k=7: n=%d, admissible d=%s" % (65, adm[6], 71, adm[7]))

print("\n== Item 1: R22 numbers (quoted from d154 log)")
n22, r22, d22, sumq = 15, 9, 3, 2 + 2 + 0
print("  n=15, inner degree d=3, outer degree m=%d; RH budget 2d-2=%d; sum q over J=%d; saturated: %s"
      % (n22 // d22, 2 * d22 - 2, sumq, sumq == 2 * d22 - 2))
print("  zeros on N = r/d =", r22 // d22, "; poles on N by Gauss-Bonnet = 4+zeros =", 4 + r22 // d22)
print("  proposal bound r >= 3d >= 9 vs W<=20 (r<=8): conclusion unsatisfiable:", 3 * 3 > 8)

print("\nCPU seconds: %.2f" % (time.process_time() - T0))
