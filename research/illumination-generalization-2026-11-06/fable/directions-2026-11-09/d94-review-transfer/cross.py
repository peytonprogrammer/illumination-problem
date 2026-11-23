"""d94: exact checks of canonical-transfer.md section 2 on the odd cross
[-b,b]x[-2,2] U [-2,2]x[-b,b], b = 7, 9, 11. Own code, exact permutations on unit cells."""
import sys
from collections import Counter

def room(b):
    cells = {(i, j) for i in range(-b, b) for j in range(-2, 2)} | {(i, j) for i in range(-2, 2) for j in range(-b, b)}
    return sorted(cells)

def setup(cells):
    idx = {c: k for k, c in enumerate(cells)}; n = len(cells)
    def sig(ax, p):
        out = []
        for (i, j) in cells:
            d = -1 if (i, j)[ax] % 2 == p else 1
            nb = (i + d, j) if ax == 0 else (i, j + d)
            out.append(idx.get(nb, idx[(i, j)]))
        return out
    S = {(ax, p): sig(ax, p) for ax in (0, 1) for p in (0, 1)}
    g = {(p, q): [S[(0, p)][S[(1, q)][a]] for a in range(n)] for p in (0, 1) for q in (0, 1)}
    return idx, n, S, g

def cycles(perm):
    seen, cs = set(), []
    for i in range(len(perm)):
        if i in seen: continue
        c = [i]; seen.add(i); j = perm[i]
        while j != i: c.append(j); seen.add(j); j = perm[j]
        cs.append(c)
    return cs

def closure(n, gens, pairs):
    lab = list(range(n))
    def f(a):
        while lab[a] != a: lab[a] = lab[lab[a]]; a = lab[a]
        return a
    def un(a, b):
        a, b = f(a), f(b)
        if a != b: lab[a] = b; return True
        return False
    for u, v in pairs: un(u, v)
    ch = True
    while ch:
        ch = False
        for gg in gens:
            for a in range(n):
                if un(gg[a], gg[f(a)]): ch = True
    parts = {}
    for a in range(n): parts.setdefault(f(a), []).append(a)
    return sorted(parts.values())

def intertwiners(n, src, dst):
    """all bijections phi with phi(src_k(a)) = dst_k(phi(a)) for all k (src, dst lists of perms)."""
    out = []
    for j in range(n):
        phi = {0: j}; st = [0]; ok = True
        while st and ok:
            a = st.pop()
            for s, d in zip(src, dst):
                x, y = s[a], d[phi[a]]
                if x in phi:
                    if phi[x] != y: ok = False; break
                else: phi[x] = y; st.append(x)
        if ok and len(phi) == n and len(set(phi.values())) == n: out.append([phi[a] for a in range(n)])
    return out

def main(bs):
  for b in bs:
      cells = room(b); idx, n, S, g = setup(cells)
      gens = [g[k] for k in sorted(g)]
      poles = sum(len(c) == 1 for k in g for c in cycles(g[k])); zeros = sum(len(c) == 3 for k in g for c in cycles(g[k]))
      print(f'== cross b={b}: n={n} (16b-16={16*b-16}), poles={poles}, zeros(r)={zeros}')
      # canonical factors
      for k in sorted(g):
          two = [c for c in cycles(g[k]) if len(c) == 2]
          P = closure(n, gens, two)
          print(f'  class {k}: #2-cycles={len(two)}, B_x has {len(P)} block(s)')
      # deck group (centralizer of G) and pole-permuting derivative-kernel candidates
      for t in [(0, 0), (1, 0), (0, 1), (1, 1)]:
          dst = [g[((p + t[0]) % 2, (q + t[1]) % 2)] for (p, q) in sorted(g)]
          print(f'  sheet maps intertwining g_x with g_(x+{t}):', len(intertwiners(n, gens, dst)))
      # K: positive lifts of x->-x, y->-y, half-turn, as cell permutations
      K = {'rx': [idx[(-1 - i, j)] for (i, j) in cells], 'ry': [idx[(i, -1 - j)] for (i, j) in cells],
           'rot': [idx[(-1 - i, -1 - j)] for (i, j) in cells]}
      for nm, k in K.items():
          assert all(k[gg[a]] == gg[k[a]] for gg in gens for a in range(n)), nm
          assert all(k[a] != a for a in range(n))
      print('  K = {1, rx, ry, rot} centralizes G and acts freely on cells: True')
      Pi = closure(n, gens, [(a, K[nm][a]) for nm in K for a in range(n)])
      assert all(len(p) == 4 for p in Pi) and len(Pi) == n // 4
      blk = {a: bi for bi, p in enumerate(Pi) for a in p}
      # N = Q/K: point counts over each pole, crossing 2-cycles
      zN = 0; tot = Counter()
      for k in sorted(g):
          bp = [blk[g[k][p[0]]] for p in Pi]
          ct = Counter(len(c) for c in cycles(bp)); tot.update({1: ct[1]})
          zN += ct[3]
          cross = sum(1 for c in cycles(g[k]) if len(c) == 2 and blk[c[0]] != blk[c[1]])
          print(f'  class {k}: N=Q/K over pole has (poles,regular,zeros)=({ct[1]},{ct[2]},{ct[3]}); '
                f'crossing 2-cycles={cross} = 4*u_x {cross == 4*ct[2]}; bound (n-4r-4k)/2={(n-16-16)//2}')
      print(f'  N: degree {n//4} over B, zeros z={zN}, poles={tot[1]} (z+4={zN+4})')
      # marks S=(6,0), T=(0,6): 2-cycles (lifts), K-orbits
      def lifts(pt):
          x, y = pt; around = {idx[c] for c in [(x-1, y-1), (x-1, y), (x, y-1), (x, y)] if c in idx}
          return [tuple(sorted(c)) for c in cycles(g[(x % 2, y % 2)]) if set(c) & around]
      for pt in [(6, 0), (0, 6)]:
          L = lifts(pt)
          orb = {tuple(sorted(K[nm][a] for a in c)) for c in L for nm in K} | set(L)
          imgs = {frozenset(blk[a] for a in c) for c in orb}
          print(f'  mark {pt}: lifts {[[cells[a] for a in c] for c in L]}; K-orbit has {len(orb)} two-cycles; '
                f'image in N = block pair(s) {[sorted(s) for s in imgs]}')
      # block systems of G
      syst = {tuple(map(tuple, closure(n, gens, [(0, j)]))) for j in range(1, n)}
      print('  minimal G-block systems containing 0 (nblocks, size):', sorted(Counter((len(P), len(P[0])) for P in syst).items()))

if __name__ == '__main__':
    main(map(int, sys.argv[1:] or ['7', '9', '11']))
