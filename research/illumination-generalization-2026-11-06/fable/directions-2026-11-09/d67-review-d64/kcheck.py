"""d67: partial completeness test of d64's quotient list (d54 item 1 style, own code).
For every in-scope room of d64 covers.json and every class y with 1 < deg N_y < n, build
K_y = P / B_y as a W-set on blocks, relabel generators so y becomes (0,0) (a unit translation),
take the canonical form of enum_K.c (BFS from every start, generator order V0 V1 H0 H1,
lexicographic minimum of the 4 rows), and look it up in data/K_z4_d18.txt and data/K_adm.json.
Also checks d <= 4z + 2 and delta * z <= 8 on each K_y. Usage: python3 -B kcheck.py"""
import json
import time
from collections import Counter
from indep import wset, D64


def blocks(G, p, q):
    n = len(G[0])
    par = list(range(n))

    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a
    gx = [G[p][G[2 + q][u]] for u in range(n)]
    todo = [(u, gx[u]) for u in range(n) if gx[u] != u and gx[gx[u]] == u]
    while todo:
        a, b = todo.pop()
        ra, rb = find(a), find(b)
        if ra != rb:
            par[ra] = rb
            todo += [(g[a], g[b]) for g in G]
    roots = sorted({find(u) for u in range(n)})
    lab = {r: k for k, r in enumerate(roots)}
    return [lab[find(u)] for u in range(n)]


def quotient(G, blk, p, q):
    d = max(blk) + 1
    K = [[None] * d for _ in range(4)]
    perm = [p, 1 - p, 2 + q, 3 - q]          # new generator g = old generator perm[g]
    for g in range(4):
        for u in range(len(blk)):
            v = blk[G[perm[g]][u]]
            assert K[g][blk[u]] in (None, v)
            K[g][blk[u]] = v
    return K


def canon(K):
    d = len(K[0])
    best = None
    for s in range(d):
        lab = {s: 0}
        order = [s]
        k = 0
        while k < len(order):
            u = order[k]
            k += 1
            for g in range(4):
                v = K[g][u]
                if v not in lab:
                    lab[v] = len(order)
                    order.append(v)
        form = tuple(tuple(lab[K[g][order[i]]] for i in range(d)) for g in range(4))
        if best is None or form < best:
            best = form
    return best


def ztype(K):
    """number of reflex (3-path) orbits of <V_i, H_j> over all classes"""
    d = len(K[0])
    z = 0
    for i in (0, 1):
        for j in (0, 1):
            seen = set()
            for c in range(d):
                if c in seen:
                    continue
                orb = {c}
                st = [c]
                while st:
                    u = st.pop()
                    for g in (i, 2 + j):
                        if K[g][u] not in orb:
                            orb.add(K[g][u])
                            st.append(K[g][u])
                seen |= orb
                fixed = sum(K[g][u] == u for u in orb for g in (i, 2 + j))
                if len(orb) == 3 and fixed == 2:
                    z += 1
    return z


t0 = time.process_time()
allK = set()
for line in open(D64 / 'data' / 'K_z4_d18.txt'):
    d, rest = line.split('|')
    allK.add(tuple(tuple(int(v) for v in r.split()) for r in rest.split(';')))
adm = {tuple(tuple(r) for r in k['canon']) for k in json.load(open(D64 / 'data' / 'K_adm.json'))}
c = Counter()
for r in json.load(open(D64 / 'data' / 'covers.json'))['rooms']:
    if not r['normalized']:
        continue
    cells = [tuple(x) for x in r['cells']]
    n = len(cells)
    G = wset(cells)
    for p in (0, 1):
        for q in (0, 1):
            blk = blocks(G, p, q)
            d = max(blk) + 1
            if not 1 < d < n:
                continue
            K = quotient(G, blk, p, q)
            f = canon(K)
            z = ztype(K)
            c['proper_quotients'] += 1
            c['in_full_list'] += f in allK
            c['in_admissible'] += f in adm
            c['d<=4z+2'] += d <= 4 * z + 2
            c['delta*z<=8'] += (n // d) * z <= 8
print(dict(c), 'distinct shapes list', len(allK), 'admissible', len(adm), 'CPU %.1f' % (time.process_time() - t0))
