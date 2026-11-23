"""Independent cover and node counts for z = 2 (six poles), degrees 2, 3, 4."""
from itertools import permutations, product
def run(D, npoles, tmax):
    PERMS = list(permutations(range(D))); ID = tuple(range(D))
    mul = lambda a, b: tuple(a[b[k]] for k in range(D))
    def inv(a):
        r = [0] * D
        for i, x in enumerate(a): r[x] = i
        return tuple(r)
    def ctype(a):
        seen, out = set(), []
        for i in range(D):
            if i not in seen:
                n, j = 0, i
                while j not in seen: seen.add(j); n += 1; j = a[j]
                out.append(n)
        return tuple(sorted(out))
    CT = {p: ctype(p) for p in PERMS}
    ok = [p for p in PERMS if max(CT[p]) <= 3]
    classes = set(); 
    for a in product(ok, repeat=npoles - 1):
        pr = ID
        for x in a: pr = mul(pr, x)
        last = inv(pr)
        if max(CT[last]) > 3: continue
        t = a + (last,)
        if sum(D - len(CT[x]) for x in t) != 2 * D - 2: continue
        if sum(CT[x].count(3) for x in t) > tmax: continue
        comp = {0}; st = [0]
        while st:
            k = st.pop()
            for h in t:
                if h[k] not in comp: comp.add(h[k]); st.append(h[k])
        if len(comp) != D: continue
        classes.add(min(tuple(mul(mul(c, x), inv(c)) for x in t) for c in PERMS))
    p1 = p2 = 0
    for t in classes:
        n2 = [CT[x].count(2) for x in t]
        p1 += sum(n * (n - 1) // 2 for n in n2)
        p2 += sum(n2[i] * n2[j] for i in range(npoles) for j in range(i + 1, npoles))
    print("D", D, "poles", npoles, "covers", len(classes), "P1", p1, "P2", p2)
run(2, 6, 4); run(3, 6, 2); run(4, 6, 0); run(2, 7, 2); run(2, 8, 0)
