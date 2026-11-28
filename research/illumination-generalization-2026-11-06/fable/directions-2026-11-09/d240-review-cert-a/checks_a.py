"""Referee checks for cert-a on three named rooms (d237 dark row, folds-d237 lines 1-2).
1. foldtest.perms (monodromy) equals the edge-involution products, up to inverse per class.
2. Pi is invariant under all four edge involutions.
3. The vertical edge involution at the mark class swaps the two quotient points of each mark.
4. Quotient cycle lengths, k, m, q, z, r and the Riemann-Hurwitz identity q = 2m-2-2z."""
import sys, json, csv
from pathlib import Path
from itertools import combinations
D = Path(__file__).resolve().parent.parent / 'd239-lattice-lines'
sys.path.insert(0, str(D))
import foldtest as F, fp

def edges(cells):
    n = len(cells)
    # vertical edge at x = X separates cell with x = X-1 (east link) and x = X (west link)
    A = [[0]*n, [0]*n]; B = [[0]*n, [0]*n]
    for p in range(2):
        for i, c in enumerate(cells):
            j = c[2] if (c[0] + 1) % 2 == p else c[4]   # east edge at x+1, west edge at x
            A[p][i] = i if j < 0 else j
            j = c[3] if (c[1] + 1) % 2 == p else c[5]
            B[p][i] = i if j < 0 else j
    return A, B

def comp(p, q): return [p[q[i]] for i in range(len(p))]
def inv(p):
    r = [0]*len(p)
    for i, t in enumerate(p): r[t] = i
    return r

def cycles(p):
    seen, out = set(), []
    for i in range(len(p)):
        if i in seen: continue
        c = []; j = i
        while j not in seen: seen.add(j); c.append(j); j = p[j]
        out.append(c)
    return out

def quotient(p, part):
    q = {}
    for i, t in enumerate(p): q[part[i]] = part[t]
    return q

def qcycles(q):
    seen, out = set(), []
    for b in q:
        if b in seen: continue
        c = []; j = b
        while j not in seen: seen.add(j); c.append(j); j = q[j]
        out.append(frozenset(c))
    return out

def run(name, cells):
    n = len(cells); gens, _ = F.perms(cells)
    CLS = [(0, 0), (1, 0), (1, 1), (0, 1)]
    g = dict(zip(CLS, gens))
    A, B = edges(cells)
    ok1 = True
    for (x, y), p in g.items():
        cands = [comp(B[y], A[x]), comp(A[x], B[y])]
        if p not in cands and p not in [inv(c) for c in cands]: ok1 = False
    ms = fp.marks_of(cells)
    r = sum(1 for p in gens for c in cycles(p) if len(c) == 3)
    print(name, 'area', n, 'monodromy = edge products:', ok1, 'reflex r =', r)
    for S, T in combinations(ms, 2):
        if S[0] != T[0]: continue
        a = S[0]
        pairs = [(i, p[i]) for x in range(4) if x != a for p in [gens[x]] for i in range(n) if p[i] != i and p[p[i]] == i]
        part = fp.partition_from(gens, n, pairs) if pairs else tuple(range(n))
        part = fp.canon(part); m = len(set(part)); k = n // m
        inv_edges = all(len({(part[i], part[E[i]]) for i in range(n)}) == m for E in A + B)
        ax = CLS[a][0]; Aa = A[ax]
        qa = qcycles(quotient(gens[a], part))
        def qpts(M):
            return {c for c in qa if c & {part[i] for i in M[1]}}
        def swapped(M):
            pts = list(qpts(M))
            img = {frozenset(part[Aa[i]] for i in range(n) if part[i] in c) for c in pts}
            return img == set(pts)
        lens = {x: sorted(len(c) for c in qcycles(quotient(gens[x], part))) for x in range(4)}
        q2 = sum(l.count(2) for l in lens.values()); z = sum(l.count(3) for l in lens.values())
        off2 = sum(lens[x].count(2) for x in range(4) if x != a)
        print('  pair', sorted(S[1]), sorted(T[1]), 'class', CLS[a], 'm', m, 'k', k,
              '| Pi edge-invariant', inv_edges, '| A_a maps mark points to themselves', swapped(S), swapped(T),
              '| points S', len(qpts(S)), 'T', len(qpts(T)), 'disjoint', not (qpts(S) & qpts(T)),
              '| q', q2, 'z', z, 'off-class q', off2, 'RH q=2m-2-2z', q2 == 2*m - 2 - 2*z, 'kz<=r', k*z <= r)

with (D.parent / 'd237-dark-examples-w22-26/astra/dark.tsv').open() as f:
    run('d237 dark row', json.loads(next(csv.DictReader(f, delimiter='\t'))['complex']))
for t, line in enumerate((D / 'folds-d237.tsv').read_text().splitlines()[:2]):
    s = line.split(); nums = list(map(int, s[4:])); run('folds-d237 line %d' % (t + 1), [nums[i:i+6] for i in range(0, len(nums), 6)])
