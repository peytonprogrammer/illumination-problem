"""d220 referee checks. Plain Python; no rooms enumerated, no rays/directions/words searched.

Run: nice -n 10 python3 -B checks.py > checks.log
Permutations are 0-based tuples; mul(p, q) applies p then q (d208 convention).
"""
import importlib.util
import random
import time
from collections import Counter
from math import factorial, gcd
from pathlib import Path

HERE = Path(__file__).resolve().parent
T0 = time.process_time()
random.seed(220)

# Reuse d208's permutation helpers (module prints its own checks on import, so copy-load
# only the function definitions).
src = (HERE.parent / "d208-review-condition-i-low" / "checks.py").read_text()
src = src.split('print("== 1.')[0]
ns = {}
exec(compile(src, "d208_checks_defs", "exec"), ns)
mul, inv, ctype = ns["mul"], ns["inv"], ns["ctype"]

FAILS = []


def check(cond, msg):
    print(("ok   " if cond else "FAIL ") + msg)
    if not cond:
        FAILS.append(msg)


def ss_base(gens, n, prefix=()):
    """Deterministic Schreier-Sims with a prescribed base prefix.
    Returns base, S (strong gens per level), T (transversal dicts)."""
    e = tuple(range(n))
    strong = [g for g in gens if g != e]
    base = list(prefix)

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

    def sift(g, T, lvl):
        for i in range(lvl, len(base)):
            b = g[base[i]]
            if b not in T[i]:
                return g
            g = mul(g, inv(T[i][b]))
        return g

    S, T = levels()
    i = len(base) - 1
    while i >= 0:
        added = False
        for x, tx in T[i].items():
            for s in S[i]:
                h = sift(mul(mul(tx, s), inv(T[i][s[x]])), T, i + 1)
                if h != e:
                    strong.append(h)
                    added = True
                    break
            if added:
                break
        if added:
            S, T = levels()
            i = len(base) - 1
        else:
            i -= 1
    return base, S, T


def order(T):
    o = 1
    for t in T:
        o *= len(t)
    return o


def sign(p):
    s, seen = 0, set()
    for i in range(len(p)):
        if i in seen:
            continue
        L, j = 0, i
        while j not in seen:
            seen.add(j)
            j = p[j]
            L += 1
        s += L - 1
    return s % 2


# ---------------------------------------------------------------- claim 2: M22
print("== Claim 2. M22 / M22:2 in the natural degree-22 action ==")
P = 23
INF = 23  # points 0..22 and infinity
sq = {(x * x) % P for x in range(1, P)}


def pg(f):
    return tuple(f(x) for x in range(24))


def finv(x):
    return pow(x, P - 2, P)


alpha = pg(lambda x: INF if x == INF else (x + 1) % P)
beta = pg(lambda x: INF if x == INF else (2 * x) % P)
gamma = pg(lambda x: 0 if x == INF else (INF if x == 0 else (-finv(x)) % P))
delta = pg(lambda x: x if x in (INF, 0) else ((pow(x, 3, P) * finv(9)) % P if x in sq else (9 * pow(x, 3, P)) % P))
for g in (alpha, beta, gamma, delta):
    assert sorted(g) == list(range(24))
base, S, T = ss_base([alpha, beta, gamma, delta], 24, prefix=(INF, 0))
check(order(T) == 244823040, f"Conway generators give |M24| = {order(T)}")
# M22 = pointwise stabilizer of infinity and 0; restrict to the 22 points 1..22.
m22gens = [tuple(g[x] - 1 for x in range(1, 23)) for g in S[2]]
b22, S22, T22 = ss_base(m22gens, 22)
check(order(T22) == 443520, f"|M22| = {order(T22)} on 22 points")
# Enumerate all elements of M22 via the stabilizer chain and record cycle types.
levels = [list(t.values()) for t in T22]
elems = [tuple(range(22))]
for lv in reversed(levels):
    elems = [mul(x, t) for t in lv for x in elems]
check(len(set(elems)) == 443520, "chain enumeration gives 443520 distinct elements")
ct = Counter(ctype(g) for g in elems)
print("  M22 cycle types (natural action):")
for t, c in sorted(ct.items(), key=lambda kv: -kv[1]):
    print(f"    {t}: {c}")
ord3 = {t: c for t, c in ct.items() if set(t) <= {1, 3} and 3 in t}
check(ord3 == {(3,) * 6 + (1,) * 4: 12320}, f"order-3 elements: {ord3} (only 3^6 1^4, 12320 = 443520/36)")
# Types with all cycle lengths in {1,2,3}: their squares are identity or 3^z.
sq_types = Counter()
for t in ct:
    if set(t) <= {1, 2, 3}:
        sq_types[t.count(3)] += ct[t]
check(set(sq_types) <= {0, 6}, f"M22 elements with cycles in {{1,2,3}}: z values {sorted(sq_types)}")
# M22:2: setwise stabilizer of {inf, 0}; gamma swaps them.
check(gamma[INF] == 0 and gamma[0] == INF, "gamma swaps infinity and 0, so <S[2], gamma'> realises M22:2")
# Build M22:2 restricted to 22 points: generators S[2] plus a coset element swapping inf,0.
sw = gamma
m222gens = m22gens + [tuple(sw[x] - 1 for x in range(1, 23))]
check(all(sw[x] not in (INF, 0) for x in range(1, 23)), "gamma preserves the 22 other points")
_, _, T222 = ss_base(m222gens, 22)
check(order(T222) == 887040, f"|M22:2| = {order(T222)} on 22 points")
outer = [mul(x, m222gens[-1]) for x in elems]
ct_out = Counter(ctype(g) for g in outer)
outer_123 = {t: c for t, c in ct_out.items() if set(t) <= {1, 2, 3}}
print("  outer-coset types with cycle lengths in {1,2,3}:", outer_123)
check(all(t.count(3) == 0 for t in outer_123),
      "no outer element of M22:2 with cycles in {1,2,3} has a 3-cycle (squares lie in M22 anyway)")
# z-sum argument: sums of four values in {0,6} never equal 8.
check(8 not in {a + b + c + d for a in (0, 6) for b in (0, 6) for c in (0, 6) for d in (0, 6)},
      "four z_x in {0,6} cannot sum to 8")
check(6 in {a + b + c + d for a in (0, 6) for b in (0, 6) for c in (0, 6) for d in (0, 6)},
      "at r=6 the distribution 6+0+0+0 survives (note's caveat)")

# ---------------------------------------------------------------- claim 4
print("\n== Claim 4. Hurwitz formulas, relabeling, shears ==")


def rp(n):
    p = list(range(n))
    random.shuffle(p)
    return tuple(p)


ok = True
for _ in range(2000):
    g, h = rp(9), rp(9)
    # sigma: (g,h) -> (h, h^-1 g h); product written left-to-right (apply g then h).
    g1, h1 = h, mul(mul(inv(h), g), h)
    g2_, h2 = h1, mul(mul(inv(h1), g1), h1)
    k = mul(g, h)
    ok &= (g2_, h2) == (mul(mul(inv(k), g), k), mul(mul(inv(k), h), k))
    ok &= mul(g1, h1) == k and mul(g2_, h2) == k
check(ok, "sigma^2 sends (g,h) to (k^-1 g k, k^-1 h k), k = gh; gh preserved (2000 random pairs, S9)")
# Same check in the right-to-left (functional) composition convention.
ok = True
for _ in range(2000):
    g, h = rp(9), rp(9)
    comp = lambda p, q: mul(q, p)  # p o q: apply q then p
    g1, h1 = h, comp(comp(inv(h), g), h)
    g2_, h2 = h1, comp(comp(inv(h1), g1), h1)
    k = comp(g, h)
    ok &= (g2_, h2) == (comp(comp(inv(k), g), k), comp(comp(inv(k), h), k))
    ok &= comp(g1, h1) == k
check(ok, "same identities hold with functional composition (convention-independent)")
# Relabeling: g -> k g k^-1 (functional), cycle label m -> m o k^-1.
ok = True
for _ in range(500):
    g, kk = rp(9), rp(9)
    comp = lambda p, q: mul(q, p)
    gk = comp(comp(kk, g), inv(kk))
    # m(s) = min element of s's g-cycle (a cycle label)
    def lab(p):
        out = {}
        for s in range(9):
            c, j = {s}, p[s]
            while j != s:
                c.add(j)
                j = p[j]
            out[s] = frozenset(c)
        return out
    m, mk = lab(g), lab(gk)
    ki = inv(kk)
    # the new cycle through s is k applied to the old cycle through k^-1(s)
    ok &= all(mk[s] == frozenset(kk[x] for x in m[ki[s]]) for s in range(9))
check(ok, "under g -> k g k^-1 the cycle through s is k(cycle of k^-1 s): labels m o k^-1")

U = lambda v: (v[0] + 2 * v[1], v[1])
V = lambda v: (v[0], v[1] + 2 * v[0])
check(U(V((1, 0))) == (5, 2) and V(U((1, 0))) == (1, 2), f"U(V(1,0))={U(V((1,0)))}, V(U(1,0))={V(U((1,0)))}")
check(all((U(v)[0] - v[0]) % 2 == 0 and (U(v)[1] - v[1]) % 2 == 0 and
          (V(v)[0] - v[0]) % 2 == 0 and (V(v)[1] - v[1]) % 2 == 0 for v in [(1, 0), (0, 1), (1, 1)]),
      "U, V are identity mod 2 (each fixes every 2-torsion point, i.e. each pole)")


def reduce_slope(p, q):
    """The note's algorithm. Returns final vector and step count; asserts the invariant."""
    steps = 0
    par0 = (p % 2, q % 2)
    while True:
        assert (p % 2, q % 2) == par0
        if (abs(p), abs(q)) in [(1, 0), (0, 1), (1, 1)]:
            break
        oldmax = max(abs(p), abs(q))
        if abs(p) > abs(q) > 0:
            m = round(p / (2 * q))  # nearest even multiple 2mq
            cands = [mm for mm in (m - 1, m, m + 1) if abs(p - 2 * mm * q) <= abs(q)]
            p = p - 2 * cands[0] * q  # U^{-m}
        elif abs(q) > abs(p) > 0:
            m = round(q / (2 * p))
            cands = [mm for mm in (m - 1, m, m + 1) if abs(q - 2 * mm * p) <= abs(p)]
            q = q - 2 * cands[0] * p  # V^{-m}
        else:
            raise AssertionError((p, q))
        steps += 1
        assert max(abs(p), abs(q)) < oldmax, (p, q)
    if abs(p) == 1 and abs(q) == 1 and p * q < 0:
        p, q = U((p, q))  # (1,-1) -> (-1,-1) ~ (1,1)
    return (abs(p), abs(q)), steps


bad, cnt, maxsteps = [], 0, 0
for p in range(-60, 61):
    for q in range(-60, 61):
        if gcd(p, q) != 1:
            continue
        cnt += 1
        end, st = reduce_slope(p, q)
        maxsteps = max(maxsteps, st)
        want = {(1, 0): (1, 0), (0, 1): (0, 1), (1, 1): (1, 1)}[(p % 2, q % 2)]
        if end != want:
            bad.append((p, q, end))
check(not bad, f"reduction reaches the parity base slope for all {cnt} primitive (p,q), |p|,|q|<=60 "
      f"(max {maxsteps} steps); failures {bad[:5]}")
# |p'| = |q| case only at |q| = 1
eq_cases = []
for p in range(-60, 61):
    for q in range(-60, 61):
        if gcd(p, q) == 1 and abs(p) > abs(q) > 0:
            r = (p + abs(q)) % (2 * abs(q)) - abs(q)  # in [-|q|, |q|)
            if abs(r) == abs(q):
                eq_cases.append((p, q))
check(all(abs(q) == 1 for _, q in eq_cases), f"tie |p'|=|q| occurs only with |q|=1 ({len(eq_cases)} cases)")

# ---------------------------------------------------------------- claim 5: cov4181
print("\n== Claim 5. cov4181 from the d66 cell rows ==")
cells = [(0, y) for y in range(6)] + [(1, 2), (1, 3), (2, 2), (2, 3)] + [(3, y) for y in range(6)] + \
        [(4, y) for y in range(6)] + [(5, 2), (5, 3), (6, 2)] + [(7, y) for y in range(3)]
cells = sorted(cells)
check(len(cells) == 28, "28 cells")
idx = {c: i for i, c in enumerate(cells)}


def Vi(i):  # exchange across vertical lines x = L with L % 2 == i
    p = list(range(28))
    for (x, y) in cells:
        if (x + 1) % 2 == i and (x + 1, y) in idx:
            a, b = idx[(x, y)], idx[(x + 1, y)]
            p[a], p[b] = b, a
    return tuple(p)


def Hj(j):
    p = list(range(28))
    for (x, y) in cells:
        if (y + 1) % 2 == j and (x, y + 1) in idx:
            a, b = idx[(x, y)], idx[(x, y + 1)]
            p[a], p[b] = b, a
    return tuple(p)


gens = {nm: mul(Vi(v), Hj(h)) for nm, (v, h) in
        {"a": (0, 1), "b": (1, 1), "c": (1, 0), "d": (0, 0)}.items()}
B = [sorted([(x, y) for x in (0, 3, 4) for y in (i, 5 - i)] + [(7, i)]) for i in range(3)]
B.append(sorted([(x, y) for x in (1, 2, 5) for y in (2, 3)] + [(6, 2)]))
check(sorted(c for b in B for c in b) == cells and all(len(b) == 7 for b in B), "B0..B3 partition the 28 cells, 7 each")
blk = {c: k for k, b in enumerate(B) for c in b}
table = {"a": ((1, 0, 2, 3), "0010"), "b": ((1, 0, 3, 2), "0011"),
         "c": ((0, 2, 3, 1), "0000"), "d": ((0, 2, 1, 3), "0001")}
for nm, g in gens.items():
    dest, bits = [], ""
    okb = True
    for k, b in enumerate(B):
        imgs = [cells[g[idx[c]]] for c in b]
        ds = {blk[c] for c in imgs}
        okb &= len(ds) == 1
        d = ds.pop()
        dest.append(d)
        perm = tuple(B[d].index(c) for c in imgs)
        bits += str(sign(perm))
    check(okb and (tuple(dest), bits) == table[nm],
          f"{nm}: block map {tuple(dest)}, bits {bits}; table {table[nm]}; sign(g)={sign(g)}")
a2 = mul(gens["a"], gens["a"])
moved = sorted(cells[i] for i in range(28) if a2[i] != i)
check(moved == [(5, 2), (5, 3), (6, 2)] and ctype(a2).count(3) == 1, f"a^2 moves exactly {moved}")
abab = mul(mul(gens["a"], gens["b"]), mul(gens["a"], gens["b"]))
bits = "".join(str(sign(tuple(B[k].index(cells[abab[idx[c]]]) for c in B[k]))) for k in range(4))
check(all(blk[cells[abab[idx[c]]]] == blk[c] for c in cells) and bits == "0011",
      f"abab fixes blocks with bits {bits}")
# Inverses / other orderings generate the same group: check H_j V_i products lie in G later.
G4 = list(gens.values())
base, S, T = ss_base(G4, 28)
W = factorial(7) ** 4 * 24 // 2
check(order(T) == W, f"|G| = {order(T)}; |(S7 wr S4) n A28| = {W}")
check(all(sign(g) == 0 for g in G4), "all four generators are even")
# Alternative basis: H_j then V_i products, and same-axis products, lie in G.
_, _, T2 = ss_base(G4 + [mul(Hj(h), Vi(v)) for v in (0, 1) for h in (0, 1)] +
                   [mul(Vi(0), Vi(1)), mul(Hj(0), Hj(1))], 28)
check(order(T2) == W, "adding H_j V_i products and V0V1, H0H1 does not enlarge G")
# Point stabilizer of i = (0,0) in B0.
i0 = idx[(0, 0)]
base, S, T = ss_base(G4, 28, prefix=(i0,))
check(len(T[0]) == 28, "G transitive on 28 sheets")
Gi = S[1]
orb = {i0}
fr = [i0]
orbits = []
seen = {i0}
for s0 in range(28):
    if s0 in seen:
        continue
    o, fr = {s0}, [s0]
    while fr:
        x = fr.pop()
        for g in Gi:
            if g[x] not in o:
                o.add(g[x])
                fr.append(g[x])
    seen |= o
    orbits.append(sorted(o))
sizes = sorted(len(o) for o in orbits)
check(sizes == [6, 21], f"stabilizer of (0,0) has orbits of sizes {sizes} besides the fixed point")
ext = next(o for o in orbits if len(o) == 21)
check({blk[cells[x]] for x in ext} == {1, 2, 3}, "size-21 orbit = the three other blocks")
loc = {x: k for k, x in enumerate(ext)}
res = [tuple(loc[g[x]] for x in ext) for g in Gi]
_, _, Tr = ss_base(res, 21)
check(order(Tr) == factorial(7) ** 3 * 6, f"projection monodromy order {order(Tr)} = |S7 wr S3| = {factorial(7)**3*6}")
check(any(sign(g) == 1 for g in res), "restriction contains odd permutations (not inside A21)")
print(f"\nCPU {time.process_time() - T0:.1f} s; failures: {len(FAILS)}")
for f in FAILS:
    print("  FAIL:", f)
