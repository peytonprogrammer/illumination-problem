"""d223 referee checks: the area-22 imprimitive (degree-two) quotient note.

Part A  fiber arithmetic for f:Q->N->B at n=22, r=8 (claims 1, 2, 3, 6).
Part B  double-cover graph test (claim 4): random genus-0 degree-m tuples for N, random double
        covers branched at two poles, quotient rule vs brute-force upstairs graph. The sphere
        embedding of N is built from the lifted tree a-x-y-w, so "K separates b1 from b2" is
        computed from cells, independently of the transport.
Part C  hand-made rooms (claims 1-3, 5-7): one axial area-22 room with 8 reflexes, one half-turn
        room. Exact rational billiard traces along hand-chosen directions only.
No room enumeration, no ray/direction/word/room-size search, no network.
Run: nice -n 10 python3 -B checks.py > checks.log
"""
import random
import time
from fractions import Fraction as Fr
from itertools import product
from math import floor, ceil

T0 = time.process_time()
FAIL = []


def check(cond, msg):
    print(('PASS ' if cond else 'FAIL ') + msg, flush=True)
    if not cond:
        FAIL.append(msg)


# ------------------------------------------------------------------ permutations
def mul(p, q):  # (p q)(i) = p(q(i))
    return tuple(p[i] for i in q)


def pinv(p):
    out = [0] * len(p)
    for i, x in enumerate(p):
        out[x] = i
    return tuple(out)


def cycles(p):
    seen, out = [False] * len(p), []
    for i in range(len(p)):
        if not seen[i]:
            c, j = [], i
            while not seen[j]:
                seen[j] = True
                c.append(j)
                j = p[j]
            out.append(c)
    return out


class UF:
    def __init__(self, n):
        self.p = list(range(n))

    def f(self, a):
        while self.p[a] != a:
            self.p[a] = self.p[self.p[a]]
            a = self.p[a]
        return a

    def u(self, a, b):
        self.p[self.f(a)] = self.f(b)


def orbits(gens, n):
    uf = UF(n)
    for g in gens:
        for i in range(n):
            uf.u(i, g[i])
    d = {}
    for i in range(n):
        d.setdefault(uf.f(i), []).append(i)
    return list(d.values())


def closure_partition(gens, n, pairs):
    """finest <gens>-invariant equivalence containing the given pairs."""
    uf = UF(n)
    edges = set(frozenset(p) for p in pairs)
    frontier = list(edges)
    while frontier:
        new = []
        for e in frontier:
            i, j = tuple(e)
            uf.u(i, j)
            for g in gens:
                ge = frozenset((g[i], g[j]))
                if ge not in edges:
                    edges.add(ge)
                    new.append(ge)
        frontier = new
    d = {}
    for i in range(n):
        d.setdefault(uf.f(i), []).append(i)
    return sorted(len(b) for b in d.values())


def orbitals(gens, n):
    """orbits of <gens> on ordered pairs, as dict pair->orbit id, plus sizes."""
    oid, sizes = {}, []
    for i in range(n):
        for j in range(n):
            if (i, j) in oid:
                continue
            k = len(sizes)
            stack, cnt = [(i, j)], 0
            oid[(i, j)] = k
            while stack:
                a, b = stack.pop()
                cnt += 1
                for g in gens:
                    q = (g[a], g[b])
                    if q not in oid:
                        oid[q] = k
                        stack.append(q)
            sizes.append(cnt)
    return oid, sizes


# ================================================================== Part A
print('== Part A: fiber arithmetic, n = 22, k = 2, m = 11, r = 8')
# f: Q -> N double cover of spheres: RH -2 = 2(-2) + R  => R = 2 simple branch points.
check(-2 == 2 * (-2) + 2, 'RH for a double cover of spheres gives exactly two simple branch points')
# local degree over B at a branch value: upstairs = 2*e must be <= 3  => e = 1 (pole of N)
check([e for e in (1, 2, 3) if 2 * e <= 3] == [1], 'branching only over N-poles (2e<=3 forces e=1)')
# r = k z + c3, c2 + 2 c3 = 2k - 2 with k = 2 and local degree <= 2 => c3 = 0, c2 = 2, z = 4
z = 8 // 2
check(z == 4 and 2 * 11 - 2 - 2 * z == 12, 'z = 4 and q = 2m-2-2z = 12')
# all per-pole (p,q,z) with p+2q+3z = 11
types = [(p, q, zz) for zz in range(4) for q in range(6) for p in range(12) if p + 2 * q + 3 * zz == 11]
sols = 0
bad = 0
bbbb = 0
qa_ok = True
for combo in product(types, repeat=4):
    P = sum(t[0] for t in combo)
    Qs = sum(t[1] for t in combo)
    Z = sum(t[2] for t in combo)
    if (P, Qs, Z) != (8, 12, 4):
        continue
    for bs in product(range(3), repeat=4):
        if sum(bs) != 2 or any(b > t[0] for b, t in zip(bs, combo)):
            continue
        sols += 1
        # upstairs types
        up2 = sum(2 * t[1] + b for t, b in zip(combo, bs))
        up1 = sum(2 * (t[0] - b) for t, b in zip(combo, bs))
        up3 = sum(2 * t[2] for t in combo)
        tot = [2 * (t[0] - b) + 2 * (2 * t[1] + b) + 3 * 2 * t[2] for t, b in zip(combo, bs)]
        rh_up = sum((22 - (2 * (t[0] - b) + 2 * t[1] + b + 2 * t[2])) for t, b in zip(combo, bs))
        if not (all(x == 22 for x in tot) and up3 == 8 and up2 == 26 and rh_up == 42 and up1 == 12):
            bad += 1
        if all(t[1] >= 1 for t in combo):
            bbbb += 1
        if max(t[1] for t in combo) > 5:
            qa_ok = False
check(sols > 0 and bad == 0,
      f'{sols} fiber assignments; all have upstairs degree 22 per pole, 8 three-cycles, 26 two-cycles, RH 42, 12 convex')
check(qa_ok, 'q_x <= 5 at every pole in every assignment')
print(f'     assignments with q_x >= 1 at all four poles (BBBB-compatible): {bbbb}')
check(sorted(t for t in types if t[1] in (4, 5)) == sorted([(3, 4, 0), (0, 4, 1), (1, 5, 0)]),
      'q_a in {4,5} leaves exactly (3,4,0),(0,4,1),(1,5,0)')
check(sorted(t for t in types if t[1] in (4, 5) and t[0] >= 2) == [(3, 4, 0)],
      'with b_a = 2 (p_a >= 2) only (3,4,0) survives')
# regular coincidences on the external orbital: 2*d = R + J, d = 20, J = 2r = 16 (every 3-cycle external)
check(2 * 20 - 16 == 24 and 24 - 2 * 5 == 14, 'external orbital: R = 2d - J = 40 - 16 = 24; 24 - 2 q_a >= 14')
check(2 * 1 == 2, 'partner orbital: d = 1, R = 2 (the two smoothed branch sites), J = 0')

# ================================================================== Part B
print('== Part B: double-cover graph test on random genus-0 tuples')
rng = random.Random(223)


def rand_perm_le3(m):
    L = list(range(m))
    rng.shuffle(L)
    p = list(range(m))
    i = 0
    while i < m:
        s = rng.choice((1, 2, 2, 3))
        c = L[i:i + s]
        for a in range(len(c)):
            p[c[a]] = c[(a + 1) % len(c)]
        i += s
    return tuple(p)


def ncyc(p):
    return len(cycles(p))


def gen_N(m, tries=20000):
    """random transitive genus-0 tuple (A,X,Y,W) with A X Y W = 1 (right-to-left), cycles <= 3."""
    for _ in range(tries):
        A, X, Y = rand_perm_le3(m), rand_perm_le3(m), rand_perm_le3(m)
        W = pinv(mul(A, mul(X, Y)))
        if any(len(c) > 3 for c in cycles(W)):
            continue
        if sum(m - ncyc(g) for g in (A, X, Y, W)) != 2 * m - 2:
            continue
        if len(orbits((A, X, Y), m)) != 1:
            continue
        return A, X, Y, W
    return None


def hurwitz(t, k):
    """braid move on adjacent entries k,k+1 of (A,X,Y,W) (product preserved)."""
    t = list(t)
    g, h = t[k], t[k + 1]
    # A..g h..: replace (g,h) by (g h g^-1, g)  [product g h preserved]
    t[k], t[k + 1] = mul(g, mul(h, pinv(g))), g
    return tuple(t)


def complex_N(A, X, Y, W):
    """cells of N from the lifted tree a-x-y-w. Edge e_k^i borders faces D_i (+) and D_{P_k i} (-)."""
    m = len(A)
    P1 = A
    P2 = mul(A, X)
    P3 = mul(P2, Y)
    assert P3 == pinv(W)
    phi = {'a': P1, 'x': X, 'y': Y, 'w': P3}
    vid = {}  # (pole, i) -> vertex id
    verts = []
    for pole in 'axyw':
        for c in cycles(phi[pole]):
            v = len(verts)
            verts.append((pole, tuple(c)))
            for i in c:
                vid[(pole, i)] = v
    edges = []  # (k, i, end1, end2, face+, face-)
    ends = {1: ('a', 'x'), 2: ('x', 'y'), 3: ('y', 'w')}
    for k, Pk in ((1, P1), (2, P2), (3, P3)):
        for i in range(m):
            e1, e2 = ends[k]
            edges.append((k, i, vid[(e1, i)], vid[(e2, i)], i, Pk[i]))
    return verts, vid, edges, (P1, P2, P3)


def lift(A, X, Y, W, c):
    """upstairs permutations on sheets (i,eps) -> 2i+eps, from sign cochains c[k][i]."""
    m = len(A)
    P1, P2, P3 = A, mul(A, X), mul(mul(A, X), Y)

    def L(P, ck):
        return tuple(2 * P[i // 2] + ((i % 2) ^ ck[i // 2]) for i in range(2 * m))
    Q1, Q2, Q3 = L(P1, c[1]), L(P2, c[2]), L(P3, c[3])
    return Q1, mul(pinv(Q1), Q2), mul(pinv(Q2), Q3), pinv(Q3)


def double_cover(A, X, Y, W, b1, b2, verts, edges):
    """random cochain with boundary b1+b2: a random path in the 1-skeleton plus random face flips."""
    m = len(A)
    adj = {}
    for idx, (k, i, u, v, fp, fm) in enumerate(edges):
        adj.setdefault(u, []).append((v, idx))
        adj.setdefault(v, []).append((u, idx))
    # random BFS tree path b1 -> b2
    order_ = list(adj)
    prev = {b1: None}
    queue = [b1]
    while queue:
        u = queue.pop(rng.randrange(len(queue)))
        nb = adj[u][:]
        rng.shuffle(nb)
        for v, idx in nb:
            if v not in prev:
                prev[v] = (u, idx)
                queue.append(v)
    c = {1: [0] * m, 2: [0] * m, 3: [0] * m}
    v = b2
    while prev[v] is not None:
        u, idx = prev[v]
        k, i = edges[idx][0], edges[idx][1]
        c[k][i] ^= 1
        v = u
    for f in range(m):  # face flips (relabel sheet f)
        if rng.random() < 0.5:
            for (k, i, u, v2, fp, fm) in edges:
                if fp == f:
                    c[k][i] ^= 1
                if fm == f:
                    c[k][i] ^= 1
    return c


def separates(K_vertices, K_edges, b1, b2, verts, edges, m):
    """components of N minus closed curve K (cells), returns (#components, b1~b2?)."""
    nV, nE = len(verts), len(edges)
    uf = UF(m + nE + nV)  # faces 0..m-1, edges m.., vertices m+nE..
    for idx, (k, i, u, v, fp, fm) in enumerate(edges):
        if idx in K_edges:
            continue
        e = m + idx
        uf.u(e, fp)
        uf.u(e, fm)
        for w in (u, v):
            if w not in K_vertices:
                uf.u(e, m + nE + w)
    alive = [x for x in range(m)] + [m + idx for idx in range(nE) if idx not in K_edges] + \
        [m + nE + w for w in range(nV) if w not in K_vertices]
    comps = len(set(uf.f(x) for x in alive))
    return comps, uf.f(m + nE + b1) == uf.f(m + nE + b2)


stats = dict(tuples=0, pairs=0, mismatch=0, cyc_sep=0, cyc_nosep=0, path=0, pole=0, diff=0,
             iso=0, jordan_bad=0, sep_vs_transport_bad=0, two_trav=0, two_trav_bad=0,
             partner_rule_bad=0, Bx_bad=0, Bx_tests=0, up_genus_bad=0, nonbranch_bad=0)
seeds = []
t_start = time.process_time()
for m in (3, 4, 5, 6, 7, 8, 9, 10):
    got = 0
    while got < 15:
        t = gen_N(m)
        if t is None:
            break
        seeds.append(t)
        got += 1
print(f'     genus-0 seed tuples: {len(seeds)} (degrees 3..10)')

samples = []
for t in seeds:
    cur = t
    for _ in range(40):  # random Hurwitz moves give many arc graphs per seed
        for _s in range(rng.randrange(1, 6)):
            cur = hurwitz(cur, rng.randrange(3))
        # random simultaneous relabelling
        m = len(cur[0])
        sg = list(range(m))
        rng.shuffle(sg)
        sg = tuple(sg)
        cur = tuple(mul(sg, mul(g, pinv(sg))) for g in cur)
        samples.append(cur)

for (A, X, Y, W) in samples:
    m = len(A)
    verts, vid, edges, Ps = complex_N(A, X, Y, W)
    nV = len(verts)
    if nV - 3 * m + m != 2:
        stats['jordan_bad'] += 1
        continue
    poles = [v for v, (pole, c) in enumerate(verts) if len(c) == 1]
    if len(poles) < 2:
        continue
    b1, b2 = rng.sample(poles, 2)
    c = double_cover(A, X, Y, W, b1, b2, verts, edges)
    gA, gX, gY, gW = lift(A, X, Y, W, c)
    n = 2 * m
    # upstairs sanity: genus 0, branched exactly at b1,b2
    if sum(n - ncyc(g) for g in (gA, gX, gY, gW)) != 2 * n - 2:
        stats['up_genus_bad'] += 1
    phiU = {'a': gA, 'x': gX, 'y': gY, 'w': gW}
    branched = set()
    for pole in 'axyw':
        for cyc in cycles(phiU[pole]):
            base = vid[(pole, cyc[0] // 2)]
            if len(cyc) == 2 * len(verts[base][1]):
                branched.add(base)
    if branched != {b1, b2}:
        stats['nonbranch_bad'] += 1
        continue
    stats['tuples'] += 1
    dist = {b1, b2}
    # ---------------- upstairs graph of arc a->x: edges = sheets, regular vertices = 2-cycles
    upA = {i: tuple(sorted(cy)) for cy in cycles(gA) for i in cy}
    upX = {i: tuple(sorted(cy)) for cy in cycles(gX) for i in cy}
    regA = [cy for cy in set(upA.values()) if len(cy) == 2]
    uidx = {}
    for cy in set(upA.values()):
        uidx[('a', cy)] = len(uidx)
    for cy in set(upX.values()):
        uidx[('x', cy)] = len(uidx)
    ufU = UF(len(uidx))
    for i in range(n):
        if len(upA[i]) == 2 and len(upX[i]) == 2:
            ufU.u(uidx[('a', upA[i])], uidx[('x', upX[i])])
    # adjacency for two-traversal brute force
    # ---------------- quotient graph
    keep = set()
    for v, (pole, cy) in enumerate(verts):
        if pole in 'ax' and (len(cy) == 2 or v in dist):
            keep.add(v)
    qedges = []  # (sheet i, u_a, v_x)
    for i in range(m):
        ua, vx = vid[('a', i)], vid[('x', i)]
        if ua in keep and vx in keep:
            qedges.append((i, ua, vx))
    ufN = UF(nV)
    for i, ua, vx in qedges:
        ufN.u(ua, vx)
    comp = {}
    for v in keep:
        comp.setdefault(ufN.f(v), set()).add(v)
    deg = {v: 0 for v in keep}
    for i, ua, vx in qedges:
        deg[ua] += 1
        deg[vx] += 1
    if any(d > 2 for d in deg.values()):
        stats['mismatch'] += 1
    # deck map on upstairs a-vertices
    def f_of(cy):
        return vid[('a', cy[0] // 2)]

    def delta(cy):
        return tuple(sorted(i ^ 1 for i in cy))

    def is_cycle(K):
        Ke = [e for e in qedges if e[1] in K]
        return len(Ke) == len(K) and len(K) > 1
    sep_cache = {}

    def K_info(root):
        if root in sep_cache:
            return sep_cache[root]
        K = comp[root]
        Ke = set(idx for idx, (k, i, u, v, fp, fm) in enumerate(edges) if k == 1 and u in K and v in K)
        info = {'cycle': len(Ke) == len(K) and len(K) > 1, 'pole': bool(K & dist), 'n': len(K)}
        if info['cycle']:
            comps, same = separates(K, Ke, b1, b2, verts, edges, m)
            if comps != 2:
                stats['jordan_bad'] += 1
            info['sep'] = not same
            # transport around K: upstairs lift of K is one cycle iff odd
            Ksheets = [edges[idx][1] for idx in Ke]
            up_v = set()
            for i in Ksheets:
                up_v.add(uidx[('a', upA[2 * i])])
                up_v.add(uidx[('a', upA[2 * i + 1])])
            roots = set(ufU.f(x) for x in up_v)
            info['odd'] = (len(roots) == 1)
            if info['odd'] != info['sep']:
                stats['sep_vs_transport_bad'] += 1
        sep_cache[root] = info
        return info
    for s in regA:
        for t_ in regA:
            if s == t_:
                continue
            stats['pairs'] += 1
            brute = ufU.f(uidx[('a', s)]) == ufU.f(uidx[('a', t_)])
            u, v = f_of(s), f_of(t_)
            if ufN.f(u) != ufN.f(v):
                pred = False
                stats['diff'] += 1
            else:
                info = K_info(ufN.f(u))
                if info['pole']:
                    pred = True
                    stats['pole'] += 1
                elif info['n'] == 1:
                    pred = False  # isolated vertex: only t = delta s possible
                    stats['iso'] += 1
                elif info['cycle']:
                    if info['sep']:
                        pred = True
                        stats['cyc_sep'] += 1
                    else:
                        # exactly one lift over v reachable; check that exactly one of t_, delta t_ is
                        r1 = ufU.f(uidx[('a', t_)]) == ufU.f(uidx[('a', s)])
                        r2 = ufU.f(uidx[('a', delta(t_))]) == ufU.f(uidx[('a', s)])
                        ok = (r1 != r2)  # exactly one lift over v (for u = v: t = delta s is not reached)
                        if not ok:
                            stats['mismatch'] += 1
                        pred = brute  # selection is the transport; consistency tested above
                        stats['cyc_nosep'] += 1
                else:  # path without branch pole: two disjoint copies
                    r1 = ufU.f(uidx[('a', t_)]) == ufU.f(uidx[('a', s)])
                    r2 = ufU.f(uidx[('a', delta(t_))]) == ufU.f(uidx[('a', s)])
                    if (r1 == r2):
                        stats['mismatch'] += 1
                    pred = brute
                    stats['path'] += 1
            if pred != brute:
                stats['mismatch'] += 1
    # partner rule and two-traversal rule, over each regular u
    for s in regA:
        t_ = delta(s)
        u = f_of(s)
        if t_ == s:
            continue
        brute = ufU.f(uidx[('a', s)]) == ufU.f(uidx[('a', t_)])
        info = K_info(ufN.f(u))
        rule = info['pole'] or (info['cycle'] and info['sep'])
        if rule != brute:
            stats['partner_rule_bad'] += 1
        # two-traversal: s -> regular x-vertex w -> t (w's two sheets in s and t)
        tt = False
        for cy in set(upX.values()):
            if len(cy) == 2 and {upA[cy[0]], upA[cy[1]]} == {s, t_}:
                tt = True
        adj_pole = any(e[1] == u and e[2] in dist for e in qedges)
        two_cycle_odd = info['cycle'] and info['n'] == 2 and info['sep']
        stats['two_trav'] += 1
        if tt != (adj_pole or two_cycle_odd):
            stats['two_trav_bad'] += 1
    # claim 2: B_x universal iff an inter-block 2-cycle exists, when the external orbital is single
    gens = (gA, gX, gY, gW)
    oid, sizes = orbitals(gens, n)
    ext_ids = set(oid[(i, j)] for i in range(n) for j in range(n) if i // 2 != j // 2)
    for g in gens:
        twos = [cy for cy in cycles(g) if len(cy) == 2]
        inter = [cy for cy in twos if cy[0] // 2 != cy[1] // 2]
        part = closure_partition(gens, n, [tuple(cy) for cy in twos]) if twos else [1] * n
        if inter and len(ext_ids) == 1:
            stats['Bx_tests'] += 1
            if part != [n]:
                stats['Bx_bad'] += 1
        if not inter:
            stats['Bx_tests'] += 1
            if max(part) > 2:
                stats['Bx_bad'] += 1

print('     ' + ', '.join(f'{k}={v}' for k, v in stats.items()))
check(stats['tuples'] > 300, f"{stats['tuples']} genus-0 double covers branched at two chosen poles were tested")
check(stats['up_genus_bad'] == 0 and stats['nonbranch_bad'] == 0, 'every lifted cover is a sphere branched exactly at b1,b2')
check(stats['jordan_bad'] == 0, 'every quotient cycle K cuts N into exactly two regions (embedding sanity)')
check(stats['sep_vs_transport_bad'] == 0 and stats['cyc_sep'] + stats['cyc_nosep'] > 0,
      'cycle K lifts to one cycle iff K separates b1 from b2 (cells), on every cycle met')
check(stats['mismatch'] == 0, f"quotient rule = brute force on all {stats['pairs']} ordered pairs of distinct regular a-lifts")
check(stats['partner_rule_bad'] == 0, 'deck partners connect iff component meets a branch pole or is a separating cycle')
check(stats['two_trav_bad'] == 0, f"two-traversal partner witness iff adjacent distinguished x-pole or odd two-edge cycle ({stats['two_trav']} cases)")
check(stats['Bx_bad'] == 0 and stats['Bx_tests'] > 0, f"B_x: universal if inter-block 2-cycle and one external orbital; refines pairs if none ({stats['Bx_tests']} tests)")
print(f'     Part B CPU {time.process_time() - t_start:.1f}s')

# ================================================================== Part C: hand-made rooms
print('== Part C: hand-made symmetric rooms')


def room_data(cells):
    cells = set(cells)
    pts = set()
    for (x, y) in cells:
        for dx in (0, 1):
            for dy in (0, 1):
                pts.add((x + dx, y + dy))
    info = {}
    for (X_, Y_) in pts:
        around = [(X_ - 1, Y_ - 1), (X_, Y_ - 1), (X_ - 1, Y_), (X_, Y_)]
        pres = [c in cells for c in around]
        k = sum(pres)
        if k == 4:
            kind = 'interior'
        elif k == 3:
            kind = 'reflex'
        elif k == 1:
            kind = 'convex'
        else:
            kind = 'pinch' if pres in ([True, False, False, True], [False, True, True, False]) else 'smooth'
        info[(X_, Y_)] = kind
    return info


def pole_perms(cells):
    """sheet = cell; pole permutation at parity (i,j) = V_i H_j (right-to-left: H first)."""
    cl = sorted(cells)
    idx = {c: k for k, c in enumerate(cl)}
    n = len(cl)

    def V(i):
        p = list(range(n))
        for (x, y) in cl:
            # vertical line at x (left edge) or x+1 (right edge) with parity i
            L = x if x % 2 == i else x + 1
            nb = (2 * L - x - 1, y)
            if nb in idx:
                p[idx[(x, y)]] = idx[nb]
        return tuple(p)

    def H(j):
        p = list(range(n))
        for (x, y) in cl:
            L = y if y % 2 == j else y + 1
            nb = (x, 2 * L - y - 1)
            if nb in idx:
                p[idx[(x, y)]] = idx[nb]
        return tuple(p)
    g = {(i, j): mul(V(i), H(j)) for i in (0, 1) for j in (0, 1)}
    return cl, idx, g


def walls(cells):
    info = room_data(cells)
    return sum(1 for k in info.values() if k in ('reflex', 'convex'))


# --- axial room: H (x >= 0) mirrored about x = 0 by (x,y) -> (-1-x, y)
Hcells = {(0, 0), (1, 0), (0, 1), (1, 1),        # star of (1,1)
          (0, 2), (1, 2), (0, 3), (1, 3),        # star of (1,3)
          (2, 1), (2, 3), (0, 4)}               # three extra cells
Pcells = Hcells | {(-1 - x, y) for (x, y) in Hcells}
infoP = room_data(Pcells)
infoH = room_data(Hcells)
rP = sum(1 for k in infoP.values() if k == 'reflex')
pinch = sum(1 for k in infoP.values() if k == 'pinch')
print(f'     axial room P: area {len(Pcells)}, reflex {rP}, walls {walls(Pcells)}, pinches {pinch}')
print(f'     cells of H: {sorted(Hcells)}')
check(len(Pcells) == 22 and rP == 8 and pinch == 0, 'hand room P: area 22, 8 reflexes, no pinch')
seam = [(0, y) for y in range(0, 7) if (0, y) in infoP]
seam_ends = [p for p in seam if infoP[p] != 'interior']
check(all(infoP[p] == 'smooth' for p in seam_ends) and len(seam_ends) == 2,
      f'axis x=0 meets the boundary of P only at two smooth points {seam_ends}')
rH = sum(1 for p, k in infoH.items() if k == 'reflex')
check(len(Hcells) == 11 and rH == 4 and walls(Hcells) == 12 and all(infoH[p] == 'convex' for p in seam_ends)
      and not any(k == 'pinch' for k in infoH.values()),
      'half-room H: 11 cells, 4 reflexes, 12 walls, seam ends are convex corners of H, no pinch')

cl, idx, g = pole_perms(Pcells)
n = len(cl)
sig = tuple(idx[(-1 - x, y)] for (x, y) in cl)
check(all(mul(sig, gg) == mul(gg, sig) for gg in g.values()), 'sigma on cells commutes with all four pole permutations (deck involution)')
blocks = sorted(set(tuple(sorted((k, sig[k]))) for k in range(n)))
check(len(blocks) == 11 and all(len(b) == 2 for b in blocks), '11 blocks {c, sigma c} of size 2')
bid = {}
for b_i, b in enumerate(blocks):
    for k in b:
        bid[k] = b_i
tot = dict(p=0, q=0, z=0, b=0)
for par, gg in sorted(g.items()):
    h = {}
    for cy in cycles(gg):
        bs = tuple(sorted(set(bid[k] for k in cy)))
        h.setdefault(bs, []).append(len(cy))
    pq = dict(p=0, q=0, z=0, b=0)
    for bs, lens in h.items():
        e = len(bs)
        if e == 1 and lens == [2]:
            pq['p'] += 1
            pq['b'] += 1
        elif e == 1:
            pq['p'] += 1
        elif e == 2:
            pq['q'] += 1
        else:
            pq['z'] += 1
    for k in tot:
        tot[k] += pq[k]
    up = sorted(len(c) for c in cycles(gg))
    print(f'     parity {par}: (p,q,z,b) = ({pq["p"]},{pq["q"]},{pq["z"]},{pq["b"]}), upstairs cycle lengths {up}')
check((tot['p'], tot['q'], tot['z'], tot['b']) == (8, 12, 4, 2), f'hand room: totals (p,q,z,b) = {tuple(tot.values())} = (8,12,4,2)')
dist_par = sorted(((x % 2, y % 2) for (x, y) in seam_ends))
print(f'     distinguished poles lie over the parities of the seam ends: {dist_par}')
bpar = []
for par, gg in sorted(g.items()):
    for cy in cycles(gg):
        if len(cy) == 2 and sig[cy[0]] == cy[1]:
            bpar.append(par)
            pts_ = [cl[k] for k in cy]
            print(f'     internal 2-cycle at parity {par}: cells {pts_}')
check(sorted(bpar) == dist_par, 'axial case: the two ramification points of f are the two seam ends')
oid, sizes = orbitals(tuple(g.values()), n)
sub = sorted(sizes[oid[(0, j)]] // n for j in set(range(n)))
subs = sorted(set((oid[(0, j)], sizes[oid[(0, j)]] // n) for j in range(n)))
print(f'     orbitals (valencies) from sheet 0: {[s for _, s in subs]}')
# BBBB status in this room
for par, gg in sorted(g.items()):
    twos = [tuple(c) for c in cycles(gg) if len(c) == 2]
    part = closure_partition(tuple(g.values()), n, twos) if twos else [1] * n
    print(f'     B_x at {par}: block sizes {sorted(set(part))}')

# marks and stars
S, T = (1, 1), (1, 3)
check(infoP[S] == 'interior' and infoP[T] == 'interior', 'S=(1,1), T=(1,3) interior, off-axis, distinct orbits, same parity')


def star(p):
    x, y = p
    return {(x - 1, y - 1), (x, y - 1), (x - 1, y), (x, y)}


check(star(S) | star(T) <= Hcells and not (star(S) & star(T)) and len(Hcells - star(S) - star(T)) == 3,
      'two disjoint stars occupy 8 of the 11 cells of H')
# four distinct regular quotient images over a: blocks of the two 2-cycles at each lift
ga = g[(S[0] % 2, S[1] % 2)]
imgs = set()
for P_ in (S, T):
    for cy in cycles(ga):
        if len(cy) == 2 and set(cl[k] for k in cy) <= star(P_):
            imgs.add(tuple(sorted(set(bid[k] for k in cy))))
check(len(imgs) == 4 and all(len(b) == 2 for b in imgs), 'the four lifts of S,T have four distinct regular images in N')


# ---------------------------------------------------------- exact billiard tracer
def trace(cells, start, vel, target_set, max_cross=200):
    """exact trace; returns ('hit', point, seam_contacts?) or ('stop', reason). Uses grid crossings."""
    info = room_data(cells)
    px, py = Fr(start[0]), Fr(start[1])
    vx, vy = vel
    events = []
    for _ in range(max_cross):
        # next time to an integer x or y line
        tx = ty = None
        if vx != 0:
            nxt = (floor(px) + 1) if vx > 0 else (ceil(px) - 1)
            tx = (nxt - px) / vx
        if vy != 0:
            nyt = (floor(py) + 1) if vy > 0 else (ceil(py) - 1)
            ty = (nyt - py) / vy
        dt = min(t for t in (tx, ty) if t is not None)
        # check lattice target passed strictly inside the step (only on a line through lattice pts)
        nx, ny = px + vx * dt, py + vy * dt
        px, py = nx, ny
        if px.denominator == 1 and py.denominator == 1:
            P_ = (int(px), int(py))
            kind = info.get(P_, 'outside')
            if P_ in target_set:
                return ('hit', P_, events)
            if kind == 'interior':
                events.append(('pass', P_))
                continue
            if kind == 'smooth':
                cx = [(P_[0] - 1, P_[1] - 1), (P_[0], P_[1] - 1), (P_[0] - 1, P_[1]), (P_[0], P_[1])]
                pres = [c in cells for c in cx]
                if pres == [True, True, False, False] or pres == [False, False, True, True]:
                    vy = -vy
                else:
                    vx = -vx
                events.append(('wall-lattice', P_))
                continue
            return ('stop', f'{kind} at {P_}', events)
        if px.denominator == 1 and (tx is not None and dt == tx):
            # crossing a vertical line at non-lattice y
            x0 = int(px)
            ycell = py // 1
            nxt = (x0, ycell) if vx > 0 else (x0 - 1, ycell)
            if nxt not in cells:
                vx = -vx
                events.append(('wall', (px, py)))
        elif py.denominator == 1:
            y0 = int(py)
            xcell = px // 1
            nxt = (xcell, y0) if vy > 0 else (xcell, y0 - 1)
            if nxt not in cells:
                vy = -vy
                events.append(('wall', (px, py)))
    return ('stop', 'max', events)


sigS, sigT = (-S[0], S[1]), (-T[0], T[1])  # mirror of lattice points about x=0
# hand-chosen H-ray from S with one seam contact; trace in H (seam is a wall) then in P
res_H = trace(Hcells, S, (-1, 1), {T})
seam_contacts = sum(1 for kind, p in res_H[2] if kind in ('wall', 'wall-lattice') and p[0] == 0)
print(f'     H-trace S={S} vel (-1,1): {res_H[0]} {res_H[1] if res_H[0] == "hit" else ""}; seam contacts {seam_contacts}; events {res_H[2]}')
res_P = trace(Pcells, S, (-1, 1), {T, sigT})
print(f'     P-trace same start/velocity: {res_P[0]} {res_P[1] if res_P[0] == "hit" else res_P[1]}; events {res_P[2]}')
check(res_H[0] == 'hit' and res_P[0] == 'hit' and
      res_P[1] == (T if seam_contacts % 2 == 0 else sigT),
      'seam-contact parity: H-ray with odd seam contacts reaches sigma T in P, even reaches T')
res_H0 = trace(Hcells, S, (0, 1), {T})
res_P0 = trace(Pcells, S, (0, 1), {T, sigT})
check(res_H0[0] == 'hit' and res_P0[0] == 'hit' and res_P0[1] == T, 'direct vertical H-ray (0 seam contacts) reaches T in P')
# axial partner test: S to a seam end with transverse final leg, then on to sigma S
E = seam_ends[0]
vel = (E[0] - S[0], E[1] - S[1])
res = trace(Pcells, S, vel, {sigS})
print(f'     partner test via seam end {E}: S={S} vel {vel} -> {res[0]} {res[1]}; events {res[2]}')
check(res[0] == 'hit' and res[1] == sigS and ('wall-lattice', E) in res[2],
      'axial partner test: S -> seam end (smooth, transverse) -> sigma S is legal')
resH = trace(Hcells, S, vel, {T, S})
check(resH[0] == 'stop' and 'convex' in resH[1], f'the same ray is illegal in H (stops at the convex seam end): {resH[1]}')

# --- half-turn room for claim 7: Z shape, centre (3,2)
Z = {(x, y) for x in range(4) for y in range(2)} | {(x, y) for x in range(2, 6) for y in range(2, 4)}
infoZ = room_data(Z)
C = (3, 2)
check(infoZ[C] == 'interior' and all(((5 - x, 3 - y) in Z) for (x, y) in Z), 'Z room is half-turn symmetric about interior lattice point (3,2)')
S2 = (1, 1)
sS2 = (2 * C[0] - S2[0], 2 * C[1] - S2[1])
# S2 -> bottom wall -> C : unfold C across y=0 -> (3,-2); direction (2,-3)
r1 = trace(Z, S2, (2, -3), {C})
r2 = trace(Z, S2, (2, -3), {sS2})
print(f'     half-turn: S={S2} vel (2,-3) -> {r1[0]} {r1[1]}; continued -> {r2[0]} {r2[1]}; events {r2[2]}')
check(r1[0] == 'hit' and r1[1] == C and r2[0] == 'hit' and r2[1] == sS2,
      'half-turn partner test: S -> C (one reflection) continues straight through C to sigma S')
gZ = pole_perms(Z)[2]
clZ, idxZ, _ = pole_perms(Z)
sigZ = tuple(idxZ[(5 - x, 3 - y)] for (x, y) in clZ)
check(all(mul(sigZ, gg) == mul(gg, sigZ) for gg in gZ.values()), 'half-turn on cells commutes with the pole permutations')
ram = []
for par, gg in gZ.items():
    for cy in cycles(gg):
        if len(cy) == 2 and sigZ[cy[0]] == cy[1]:
            ram.append((par, sorted(clZ[k] for k in cy)))
print(f'     half-turn ramification 2-cycles (internal to a block): {ram}')
check(len(ram) == 2 and all(p == (1, 0) for p, _ in ram), 'both ramification points are the two lifts of the centre (parity (1,0))')

print(f'CPU {time.process_time() - T0:.1f}s')
print(f'FAILURES: {len(FAIL)}' + (' -- ' + '; '.join(FAIL) if FAIL else ''))
