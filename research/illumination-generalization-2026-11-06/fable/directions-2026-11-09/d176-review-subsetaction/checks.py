"""d176 checks for l1-primitive-subset-action.md (exact, pure Python).

1. Faithfulness of S_m on k-subsets (brute force, m <= 7).
2. For every cycle type of S_m, m <= 14, and every 2 <= k <= m-2: the cycle
   lengths of the induced k-subset permutation. Reports every type whose
   k-subset cycles lie in {1,2,3} and every order-6 type without a k-subset
   orbit of length 6. Also replays the note's two explicit constructions.
3. Formal (not geometric) feasibility of the branch for small m: 4-tuples of
   letter permutations with product 1, transitive on k-subsets, every site's
   k-subset cycles in {1,2,3}, sum z = r in [1,8], sum f = r+4.
"""
import itertools, math, sys
from functools import reduce

def partitions(n, maxp=None):
    if maxp is None: maxp = n
    if n == 0: yield (); return
    for p in range(min(n, maxp), 0, -1):
        for rest in partitions(n - p, p): yield (p,) + rest

def perm_from_type(t):
    perm, start = [], 0
    for c in t:
        perm += [start + (i + 1) % c for i in range(c)]
        start += c
    return perm

def lcm(xs): return reduce(lambda a, b: a * b // math.gcd(a, b), xs, 1)

def kset_cycles(perm, k):
    m = len(perm)
    def img(mask):
        out = 0
        while mask:
            b = mask & -mask; out |= 1 << perm[b.bit_length() - 1]; mask ^= b
        return out
    seen, lens = set(), {}
    for c in itertools.combinations(range(m), k):
        s = sum(1 << i for i in c)
        if s in seen: continue
        L, x = 0, s
        while True:
            seen.add(x); L += 1; x = img(x)
            if x == s: break
        lens[L] = lens.get(L, 0) + 1
    return lens  # length -> number of cycles

def period(perm, S):
    S0, x, t = frozenset(S), frozenset(S), 0
    while True:
        x = frozenset(perm[i] for i in x); t += 1
        if x == S0: return t

log = print

# ---- 1. faithfulness
log("== 1. faithfulness (brute force, all permutations, m<=7)")
for m in range(4, 8):
    for k in range(2, m - 1):
        sets = [frozenset(c) for c in itertools.combinations(range(m), k)]
        bad = sum(1 for p in itertools.permutations(range(m))
                  if any(p[i] != i for i in range(m))
                  and all(frozenset(p[i] for i in s) == s for s in sets))
        log(f"m={m} k={k}: nonidentity perms acting trivially = {bad}")

# ---- 2. cycle types
log("\n== 2. every cycle type, m<=14, 2<=k<=m-2")
small_types, order6_fail, cons_fail, checked = [], [], [], 0
for m in range(4, 15):
    for t in partitions(m):
        perm = perm_from_type(t)
        for k in range(2, m - 1):
            lens = kset_cycles(perm, k); checked += 1
            if set(lens) <= {1, 2, 3}:
                small_types.append((m, k, t))
            if lcm(t) == 6:
                if 6 not in lens: order6_fail.append((m, k, t))
                # replay the note's construction
                start, cyc = 0, {}
                for c in t:
                    cyc.setdefault(c, []).append(list(range(start, start + c))); start += c
                if 6 in cyc:
                    C = cyc[6][0]; outside = [i for i in range(m) if i not in C]
                    js = range(max(1, k - (m - 6)), min(5, k) + 1)
                    if not js: cons_fail.append((m, k, t, "empty j range"))
                    for j in js:
                        S = C[:j] + outside[:k - j]
                        if len(S) != k or period(perm, S) != 6:
                            cons_fail.append((m, k, t, "6cyc", j))
                else:
                    T2, T3 = cyc[2][0], cyc[3][0]
                    outside = [i for i in range(m) if i not in T2 + T3]
                    ok = False
                    for a in (1, 2):
                        rest = k - 1 - a
                        if 0 <= rest <= len(outside):
                            S = [T2[0]] + T3[:a] + outside[:rest]
                            if period(perm, S) != 6: cons_fail.append((m, k, t, "2+3", a))
                            ok = True
                    if not ok: cons_fail.append((m, k, t, "no size fits"))
log(f"(m,k,type) triples checked: {checked}")
log(f"order-6 types with no k-subset 6-cycle: {order6_fail if order6_fail else 'none'}")
log(f"construction failures: {cons_fail if cons_fail else 'none'}")
mixed = [x for x in small_types if 2 in x[2] and 3 in x[2]]
other = [x for x in small_types if not (set(x[2]) <= {1, 2} or set(x[2]) <= {1, 3})]
log(f"types with all k-subset cycles in {{1,2,3}}: {len(small_types)}; "
    f"of these mixing 2- and 3-cycles on letters: {len(mixed)}; outside 1^a2^b / 1^a3^c: {len(other)}")
# reflex-bearing (has a 3-cycle on letters) => k-subset action has no 2-cycle
ro = [x for x in small_types if 3 in x[2] and 2 in kset_cycles(perm_from_type(x[2]), x[1])]
log(f"letter types 1^a3^c whose k-subset action has a 2-cycle (would break corner-only): {len(ro)}")
log("contrast k=1 (natural action), type 3+2: cycles", kset_cycles(perm_from_type((3, 2)), 1))

# ---- 3. formal feasibility, small m
log("\n== 3. formal tuple feasibility (product 1, transitive on k-sets), small m")
def compose(p, q): return tuple(q[p[i]] for i in range(len(p)))   # p then q
def ctype(p):
    seen, t = set(), []
    for i in range(len(p)):
        if i in seen: continue
        L, j = 0, i
        while j not in seen: seen.add(j); j = p[j]; L += 1
        t.append(L)
    return tuple(sorted(t, reverse=True))
def fkz(t, k):
    l = kset_cycles(perm_from_type(t), k); return l.get(1, 0), l.get(2, 0), l.get(3, 0)
def transitive(gens, k, m):
    sets = [frozenset(c) for c in itertools.combinations(range(m), k)]
    start = sets[0]; seen = {start}; stack = [start]
    while stack:
        s = stack.pop()
        for g in gens:
            x = frozenset(g[i] for i in s)
            if x not in seen: seen.add(x); stack.append(x)
    return len(seen) == len(sets)

for m, k in [(4, 2), (5, 2), (6, 2), (6, 3), (7, 2), (7, 3), (8, 2)]:
    allowed = [t for t in partitions(m) if set(t) <= {1, 2} or set(t) <= {1, 3}]
    data = {t: fkz(t, k) for t in allowed}
    n = math.comb(m, k)
    type_quads = []
    for q in itertools.combinations_with_replacement(allowed, 4):
        z = sum(data[t][2] for t in q); f = sum(data[t][0] for t in q)
        if 1 <= z <= 8 and f == z + 4: type_quads.append(q)
    log(f"m={m} k={k} n={n}: cycle-type quadruples passing R-H, r<=8, r>=1: {len(type_quads)}")
    perms = list(itertools.permutations(range(m)))
    bytype = {}
    for p in perms: bytype.setdefault(ctype(p), []).append(p)
    found = []
    for q in type_quads:
        for order in set(itertools.permutations(q)):
            a = tuple(perm_from_type(order[0]))
            hit = None
            for b in bytype[order[1]]:
                ab = compose(a, b)
                for c in bytype[order[2]]:
                    abc = compose(ab, c)
                    d = tuple(sorted(range(m), key=lambda i: abc[i]))  # inverse
                    if ctype(d) == order[3] and transitive([a, b, c], k, m):
                        hit = (a, b, c, d); break
                if hit: break
            if hit:
                found.append((order, hit)); break
    for order, hit in found:
        r = sum(data[t][2] for t in order)
        log(f"   realizable formally: letter types {order}, r={r}, W=2r+4={2*r+4}, "
            f"(f,k2,z) per site {[data[t] for t in order]}")
    if not found: log("   no formal tuple")
