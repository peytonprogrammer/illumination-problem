"""d208 group-theory checks. Plain Python, no rooms, rays, directions or words.

Permutations are 0-based tuples. Run: python3 -B checks.py
"""
import itertools
import random
from collections import Counter

random.seed(208)


def mul(p, q):  # apply p then q
    return tuple(q[i] for i in p)


def inv(p):
    r = [0] * len(p)
    for i, j in enumerate(p):
        r[j] = i
    return tuple(r)


def cyc(n, cycles):
    p = list(range(n))
    for c in cycles:
        c = [x - 1 for x in c]
        for a, b in zip(c, c[1:] + c[:1]):
            p[a] = b
    return tuple(p)


def ctype(p):
    seen, out = set(), []
    for i in range(len(p)):
        if i in seen:
            continue
        L, j = 0, i
        while j not in seen:
            seen.add(j)
            j = p[j]
            L += 1
        out.append(L)
    return tuple(sorted(out, reverse=True))


def closure(gens, cap=None):
    e = tuple(range(len(gens[0])))
    seen, frontier = {e}, [e]
    while frontier:
        nxt = []
        for x in frontier:
            for g in gens:
                y = mul(x, g)
                if y not in seen:
                    seen.add(y)
                    nxt.append(y)
                    if cap and len(seen) > cap:
                        return seen
        frontier = nxt
    return seen


def schreier_sims(gens, n):
    """Plain Schreier-Sims. Returns (base, S, T): S[i] = strong gens fixing base[:i],
    T[i] = transversal of the level-i basic orbit."""
    e = tuple(range(n))
    strong = [g for g in gens if g != e]
    base = []

    def orbit_trans(b, gs):
        t = {b: e}
        fr = [b]
        while fr:
            nf = []
            for x in fr:
                for g in gs:
                    y = g[x]
                    if y not in t:
                        t[y] = mul(t[x], g)
                        nf.append(y)
            fr = nf
        return t

    def levels():
        while True:
            S = [[g for g in strong if all(g[b] == b for b in base[:i])] for i in range(len(base) + 1)]
            if S[-1]:
                g = S[-1][0]
                base.append(next(i for i in range(n) if g[i] != i))
                continue
            S.pop()
            return S, [orbit_trans(base[i], S[i]) for i in range(len(base))]

    def sift(g, S, T, lvl):
        for i in range(lvl, len(base)):
            b = g[base[i]]
            if b not in T[i]:
                return g
            g = mul(g, inv(T[i][b]))
        return g

    S, T = levels()
    changed = True
    while changed:
        changed = False
        for i in reversed(range(len(base))):
            for x, tx in T[i].items():
                for s in S[i]:
                    sg = mul(mul(tx, s), inv(T[i][s[x]]))
                    h = sift(sg, S, T, i + 1)
                    if h != e:
                        strong.append(h)
                        changed = True
                        break
                if changed:
                    break
            if changed:
                S, T = levels()
                break
    return base, S, T


def order_of_chain(T):
    o = 1
    for t in T:
        o *= len(t)
    return o


print("== 1. Burnside alternative at primes 23..47 ==")
for p in [23, 29, 31, 37, 41, 43, 47]:
    agl = p * (p - 1)
    print(f"p={p}: |AGL(1,p)|={agl}, 3 | |AGL|: {agl % 3 == 0}, "
          f"min fixed points of g_x^2 (z<=8, 3z<=p): {p - 3 * min(8, p // 3)}")
# In AGL(1,p) a nonidentity map x -> ax+b fixes <= 1 point (check p=29 exhaustively).
p = 29
mx = max(sum(1 for x in range(p) if (a * x + b) % p == x)
         for a in range(1, p) for b in range(p) if (a, b) != (1, 0))
print(f"AGL(1,29): max fixed points of a nonidentity element = {mx}")

print("\n== 2. Degree 11: M11 and PSL(2,11) cycle types ==")
M11 = closure([cyc(11, [list(range(1, 12))]), cyc(11, [[3, 7, 11, 8], [4, 10, 5, 6]])])
print("|M11| =", len(M11))
m11types = Counter(ctype(g) for g in M11)
for t, c in sorted(m11types.items()):
    print("  ", t, c)
# find a transitive subgroup of order 660 (PSL(2,11)) inside M11
M11l = list(M11)
psl = None
for _ in range(4000):
    a, b = random.choice(M11l), random.choice(M11l)
    H = closure([a, b], cap=700)
    if len(H) == 660:
        psl = H
        break
print("found subgroup of order 660 in M11:", psl is not None,
      "transitive:", psl is not None and len({g[0] for g in psl}) == 11)
if psl:
    print("  its types:", sorted(Counter(ctype(g) for g in psl).items()))


def types_123(m):
    out = []
    for z in range(m // 3 + 1):
        for k in range((m - 3 * z) // 2 + 1):
            f = m - 3 * z - 2 * k
            out.append((z, k, f))
    return out


def as_ctype(z, k, f):
    return tuple([3] * z + [2] * k + [1] * f)


print("\n== 3. Quotient tuples at m=11 (n=22, k=2) ==")
# genus 0: sum(k+2z)=2m-2; sum f = Z+4; Z in 1..4 (kZ<=r<=8 with k=2)
m = 11
T11 = types_123(m)
cands, bad = 0, []
for tup in itertools.combinations_with_replacement(T11, 4):
    if sum(k + 2 * z for z, k, f in tup) != 2 * m - 2:
        continue
    Z = sum(z for z, k, f in tup)
    if Z < 1:
        continue
    assert sum(f for z, k, f in tup) == Z + 4
    cands += 1
    if all(as_ctype(*t) in m11types for t in tup):
        bad.append((tup, Z))
print("genus-0 multisets with Z>=1:", cands)
print("all four types realizable in M11 (so H could be M11/PSL(2,11)):", bad)
print("  -> with Z<=4 none remain" if all(Z > 4 for _, Z in bad) else "  -> SOME REMAIN")
zmax = max(z for z, k, f in T11)
print("max 3-cycles of an element of degree 11:", zmax, "(so z=4 at one pole is impossible)")

print("\n== 4. M23: order-3 elements have >= 6 three-cycles ==")
a = cyc(23, [list(range(1, 24))])
b = cyc(23, [[3, 17, 10, 7, 9], [4, 13, 14, 19, 5], [8, 18, 11, 12, 23], [15, 20, 22, 21, 16]])
base, S, T = schreier_sims([a, b], 23)
print("|M23| =", order_of_chain(T), "orbit lengths along base:", [len(t) for t in T])
# 4-point stabilizer: generators at level 4 of the chain
lvl4 = [g for g in S[4]] if len(S) > 4 else []
St4 = closure(lvl4) if lvl4 else {tuple(range(23))}
print("pointwise stabilizer of base[:4]: order", len(St4))
print("  max fixed points of a nonidentity element there:",
      max(ctype(g).count(1) for g in St4 if g != tuple(range(23))))
print("  order-3 types there:", sorted({ctype(g) for g in St4 if ctype(g)[0] == 3 and set(ctype(g)) <= {1, 3}}))
# random sample of order-3 elements as a cross-check
seen3 = Counter()
g = a
for _ in range(20000):
    g = mul(g, random.choice([a, b, inv(a), inv(b)]))
    t = ctype(g)
    from math import lcm
    o = 1
    for L in t:
        o = lcm(o, L)
    if o % 3 == 0:
        h = g
        pw = o // 3
        r = tuple(range(23))
        for _ in range(pw):
            r = mul(r, h)
        seen3[ctype(r)] += 1
print("  random order-3 element types:", dict(seen3))

print("\n== 5. Cauchy-Davenport sanity (|A|=|B|=4 in Z/23) ==")
mn = min(len({(y - x) % 23 for x in A for y in B})
         for A in itertools.combinations(range(23), 4) if A[0] == 0
         for B in [(0, 1, 2, 3), (0, 1, 2, 4), (0, 2, 4, 6), (0, 5, 10, 15)])
print("min |B-A| over A containing 0 and four sample B:", mn)
