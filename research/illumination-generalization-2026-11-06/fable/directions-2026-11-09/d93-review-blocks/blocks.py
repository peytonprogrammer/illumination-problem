"""d93: independent recomputation of the R22 block test (small-orbit-blocks.md).
Own code. Exact permutations on the 15 cells of R22 (sorted order = rooms.json order)."""
import json, itertools, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
rooms = json.load(open(os.path.join(HERE, '..', 'd8-perturbation-test', 'rooms.json')))
room = [r for r in rooms if r['id'] == 'R22-base'][0]
cells = sorted(tuple(c) for c in room['cells'])
assert [tuple(c) for c in room['cells']] == cells
idx = {c: i for i, c in enumerate(cells)}
n = len(cells)

def sig(axis, p):
    """reflection across the cell edge on the line coord == p (mod 2); wall -> fixed."""
    out = []
    for (i, j) in cells:
        k = (i, j)[axis]
        d = -1 if k % 2 == p else +1          # left/bottom edge at k, else right/top at k+1
        nb = (i + d, j) if axis == 0 else (i, j + d)
        out.append(idx.get(nb, idx[(i, j)]))
    return tuple(out)

S = {(ax, p): sig(ax, p) for ax in (0, 1) for p in (0, 1)}
def comp(f, g):  # f after g
    return tuple(f[g[i]] for i in range(n))
g = {(p, q): comp(S[(0, p)], S[(1, q)]) for p in (0, 1) for q in (0, 1)}
def cycles(perm):
    seen, cs = set(), []
    for i in range(n):
        if i in seen: continue
        c = [i]; seen.add(i); j = perm[i]
        while j != i: c.append(j); seen.add(j); j = perm[j]
        cs.append(tuple(c))
    return cs
for k in sorted(g):
    print('g', k, 'cycles', [c for c in cycles(g[k]) if len(c) > 1],
          'fixed', sum(len(c) == 1 for c in cycles(g[k])))
# sanity: corner counts
conv = sum(len(c) == 1 for k in g for c in cycles(g[k])); refl = sum(len(c) == 3 for k in g for c in cycles(g[k]))
print('poles (convex corners) =', conv, ' zeros (reflex) =', refl, ' walls =', conv + refl)

def cycle_at(pt):
    """2-cycle of g_class(pt) on the cells around lattice point pt."""
    x, y = pt
    around = {idx[c] for c in [(x-1, y-1), (x-1, y), (x, y-1), (x, y)] if c in idx}
    gg = g[(x % 2, y % 2)]
    cs = [c for c in cycles(gg) if set(c) & around]
    return cs

gens = list(g.values())
def closure(merge):
    """finest G-invariant partition merging the given set (union-find closure)."""
    par = list(range(n))
    def f(a):
        while par[a] != a:
            par[a] = par[par[a]]; a = par[a]
        return a
    def un(a, b):
        a, b = f(a), f(b)
        if a != b: par[a] = b; return True
        return False
    m = list(merge)
    for a in m[1:]: un(m[0], a)
    changed = True
    while changed:
        changed = False
        for gg in gens:
            for a in range(n):
                if un(gg[a], gg[f(a)]): changed = True
    parts = {}
    for a in range(n): parts.setdefault(f(a), []).append(a)
    return sorted(sorted(p) for p in parts.values())

A_pts = [(0, 0), (4, 0)]
B_pts = [(2, 2), (2, -2)]
A = [c for p in A_pts for c in cycle_at(p)]
B = [c for p in B_pts for c in cycle_at(p)]
print('A cycles', A, ' B cycles', B)
assert all(len(c) == 2 for c in A + B)
A = sorted(tuple(sorted(c)) for c in A); B = sorted(tuple(sorted(c)) for c in B)
results = []
for choice in itertools.product(*[(c[0], c[1]) if i else (c[0],) for i, c in enumerate(A)]):
    P = closure(choice)
    sizes = sorted(set(map(len, P)))
    blk = {a: bi for bi, part in enumerate(P) for a in part}
    ja = {frozenset((blk[u], blk[v])) for u, v in A}
    jb = {frozenset((blk[u], blk[v])) for u, v in B}
    ok = (sizes == [3] and len(ja) == 1 and len(jb) == 1 and all(len(s) == 2 for s in ja | jb) and ja != jb)
    print('choice', choice, 'block sizes', sizes, 'nblocks', len(P),
          'A joins', [sorted(s) for s in ja], 'B joins', [sorted(s) for s in jb], 'ACCEPT' if ok else '')
    results.append((choice, P, ok))
acc = [r for r in results if r[2]]
assert len(acc) == 1
Sig = acc[0][1]
print('accepted partition (cells):', [[cells[a] for a in p] for p in Sig])

# all block systems of G (minimal blocks containing {0, j})
systems = {}
for j in range(1, n):
    P = closure([0, j]); systems[tuple(map(tuple, P))] = len(P[0])
print('block systems of G (from pairs {0,j}):', sorted(set((len(P), sz) for P, sz in systems.items())))
print('size-3 systems:', [P for P, sz in systems.items() if sz == 3])
# group order / transitivity
def order(gens):
    seen = {tuple(range(n))}; fr = [tuple(range(n))]
    while fr:
        h = fr.pop(); 
        for gg in gens:
            k = comp(gg, h)
            if k not in seen: seen.add(k); fr.append(k)
    return len(seen)
print('|G| =', order(gens), ' |W| =', order(list(S.values())))
# W-invariance of Sigma (a fold needs reflections, not just G)
blk = {a: bi for bi, part in enumerate(Sig) for a in part}
Winv = all(len({blk[s[a]] for a in part}) == 1 for s in S.values() for part in Sig)
print('Sigma W-invariant:', Winv)
# develop the quotient W-set: place block of cell (0,0) at (0,0); a fold maps each cell to a cell
# Explicit fold: F(cell) = reflection-folded position; check consistency
pos = {blk[idx[(0, 0)]]: (0, 0)}
fold = {idx[(0, 0)]: (0, 0)}
stack = [idx[(0, 0)]]
while stack:
    a = stack.pop()
    for (ax, p), s in S.items():
        b = s[a]
        if b == a: continue
        # crossing an edge of P: image moves across the corresponding edge downstairs (wall downstairs -> reflect = stay)
        fx, fy = fold[a]
        k = (fx, fy)[ax]
        # the edge crossed upstairs has parity p; downstairs the same parity edge of image cell
        d = -1 if k % 2 == p else +1
        cand = (fx + d, fy) if ax == 0 else (fx, fy + d)
        tgt = cand if blk[b] != blk[a] else (fx, fy)
        if b in fold:
            assert fold[b] == tgt or blk[b] == blk[a], (a, b, fold[b], tgt)
        else:
            fold[b] = tgt; stack.append(b)
img = {}
for a, c in fold.items(): img.setdefault(c, set()).add(blk[a])
print('fold image cells:', sorted(img), ' blocks per image cell:', {c: sorted(v) for c, v in sorted(img.items())})
print('fibres of fold:', sorted(sorted(cells[a] for a in fold if fold[a] == c) for c in img))

# B_x for each class: finest G-block system merging every 2-cycle of g_x
for k in sorted(g):
    par = None
    two = [c for c in cycles(g[k]) if len(c) == 2]
    # closure merging all 2-cycles: do iteratively
    P = [[i] for i in range(n)]
    lab = list(range(n))
    def f(a):
        while lab[a] != a: a = lab[a]
        return a
    def un(a, b):
        a, b = f(a), f(b)
        if a != b: lab[a] = b; return True
        return False
    for u, v in two: un(u, v)
    ch = True
    while ch:
        ch = False
        for gg in gens:
            for a in range(n):
                if un(gg[a], gg[f(a)]): ch = True
    parts = {}
    for a in range(n): parts.setdefault(f(a), []).append(a)
    print('B_x class', k, 'blocks', len(parts), 'size', len(next(iter(parts.values()))),
          '= Sigma' if sorted(map(sorted, parts.values())) == Sig else '')
# images of a-class points in N = Q/Sigma : regular?
for k in sorted(g):
    ind = {}
    for c in cycles(g[k]):
        pass
    # induced permutation on blocks
    bp = {bi: blk[g[k][part[0]]] for bi, part in enumerate(Sig)}
    cyc = []; seen = set()
    for b0 in bp:
        if b0 in seen: continue
        c = [b0]; seen.add(b0); j = bp[b0]
        while j != b0: c.append(j); seen.add(j); j = bp[j]
        cyc.append(len(c))
    print('induced g', k, 'on Sigma blocks: cycle type', sorted(cyc), ' (2 = regular point of N over this pole)')
