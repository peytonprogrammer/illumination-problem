"""Step 2 checks: residual table, tetromino smooth sites, staircase, and the
outer-degree-four permutation lemma by exhaustion over S4."""
from itertools import permutations, product
# 1. Residual table: q + 2z = 2m - 2, 2 <= q <= m/2 (q even sheets at a), r = k z + c3 <= 8,
#    c2 + 2 c3 = 2k - 2, k >= 2, m >= 2.
rows = set()
for z in range(0, 9):
    for m in range(2, 40):
        q = 2 * m - 2 - 2 * z
        if q < 2 or 2 * q > m: continue
        for k in range(2, 9):
            for c3 in range(0, k):
                c2 = 2 * k - 2 - 2 * c3
                if c2 >= 0 and k * z + c3 <= 8:
                    rows.add((z, m, k, q))
print('residual (z, m, k, q):', sorted(rows))
# 2. Polyomino stars
def stars(cells):
    cells = set(cells); pts = {(i+a, j+b) for i, j in cells for a in (0, 1) for b in (0, 1)}
    out = {}
    for x, y in pts:
        s = [c for c in ((x, y), (x-1, y), (x-1, y-1), (x, y-1)) if c in cells]
        out[(x, y)] = len(s)
    return out
def report(name, cells):
    st = stars(cells)
    reg = [(p, st[p]) for p in sorted(st) if st[p] in (2, 4)]
    print(name, 'reflex', sum(v == 3 for v in st.values()), 'regular sites', reg,
          'parities', [(x % 2, y % 2) for (x, y), _ in reg])
report('T', [(0, 0), (1, 0), (2, 0), (1, 1)])
report('skew', [(0, 0), (1, 0), (1, 1), (2, 1)])
report('L', [(0, 0), (1, 0), (2, 0), (0, 1)])
report('staircase (d93)', [(-1, 0), (0, 0), (0, 1), (1, 1), (1, 2)])
# all tetrominoes (free, by brute force on 4x4 grid) with two reflexes
import itertools
grid = [(i, j) for i in range(4) for j in range(4)]
seen = set(); found = []
for cs in itertools.combinations(grid, 4):
    s = set(cs); st = [s.pop()]; comp = {st[0]}
    while st:
        i, j = st.pop()
        for nb in ((i+1, j), (i-1, j), (i, j+1), (i, j-1)):
            if nb in cs and nb not in comp: comp.add(nb); st.append(nb)
    if len(comp) < 4: continue
    v = stars(cs)
    if sum(x == 3 for x in v.values()) == 2:
        reg = [p for p in v if v[p] in (2, 4)]
        par = {(x % 2, y % 2) for x, y in reg}
        found.append((len(reg), len(par)))
print('tetromino placements with 2 reflexes: (regular sites, distinct parities) ->', sorted(set(found)), 'count', len(found))
# 3. Outer degree 4 lemma: involutions h0,h1,v0,v1 in S4 with g_ij = h_i v_j,
#    g_00 of type (2,2), the other three each of type 1^4 or 3+1, exactly two 3-cycles.
S4 = list(permutations(range(4)))
inv = [p for p in S4 if all(p[p[i]] == i for i in range(4))]
def mul(a, b): return tuple(a[b[i]] for i in range(4))
def ctype(p):
    seen, t = set(), []
    for i in range(4):
        if i in seen: continue
        L, j = 0, i
        while j not in seen: seen.add(j); j = p[j]; L += 1
        t.append(L)
    return tuple(sorted(t, reverse=True))
sols = []
for h0, h1, v0, v1 in product(inv, repeat=4):
    g = {(0, 0): mul(h0, v0), (1, 0): mul(h1, v0), (0, 1): mul(h0, v1), (1, 1): mul(h1, v1)}
    if ctype(g[(0, 0)]) != (2, 2): continue
    ts = [ctype(g[x]) for x in ((1, 0), (0, 1), (1, 1))]
    if all(t in ((1, 1, 1, 1), (3, 1)) for t in ts) and ts.count((3, 1)) == 2:
        sols.append((h0, h1, v0, v1, ts))
print('degree-4 tuples with the required types:', len(sols))
# Of these, which allow both marks? The mark over the h0-support... test the cell-label lemma:
# x-adjacent class (1,0) and y-adjacent class (0,1) must both be identity for the two marks.
both = [s for s in sols if s[4][0] == (1, 1, 1, 1) and s[4][1] == (1, 1, 1, 1)]
print('tuples with identity at both (1,0) and (0,1):', len(both))
