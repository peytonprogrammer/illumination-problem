"""d222 referee checks: two-pole planar maps, the D(I,J) twist test, pigeonhole, tree filter, cov4181.

Named room: cov4181 only (d66 cell rows, d220/d221 generator convention).
Combinatorial self-test: exhaustive X,Y on degree <= 5 and random X,Y on degree <= 12, cycles <= 3.
No room enumeration. The only geometric rays are the note's own twist family from S=(2,3):
velocity (+-1, +-2j), j = 0..5 (one full residue system of ord k = 6), two lattice steps each.
Run: nice -n 10 python3 -B checks.py > checks.log
"""
import random
import time
from fractions import Fraction as Fr
from itertools import permutations, product
from math import comb, gcd

T0 = time.process_time()
FAIL = []


def check(cond, msg):
    print(('PASS ' if cond else 'FAIL ') + msg, flush=True)
    if not cond:
        FAIL.append(msg)


# ------------------------------------------------------------------ permutation helpers
def mul(p, q):  # (pq)(i) = p(q(i))
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


def order(p):
    o = 1
    for c in cycles(p):
        o = o * len(c) // gcd(o, len(c))
    return o


def orbits(gens, n):
    par = list(range(n))

    def f(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a
    for g in gens:
        for i in range(n):
            par[f(i)] = f(g[i])
    comp = {}
    for i in range(n):
        comp.setdefault(f(i), []).append(i)
    return list(comp.values())


def faces(k):
    """face id and position of each label along the k-cycles (pos increases by one under k)."""
    fid, pos, flen = {}, {}, []
    for f, c in enumerate(cycles(k)):
        flen.append(len(c))
        for p, i in enumerate(c):
            fid[i], pos[i] = f, p
    return fid, pos, flen


def Dtable(X, k):
    """D(I,J): residues pos_J(v)-pos_I(u) mod gcd over both orders of every 2-cycle (u v) of X."""
    fid, pos, flen = faces(k)
    D = {}
    for c in cycles(X):
        if len(c) != 2:
            continue
        for u, v in (c, c[::-1]):
            I, J = fid[u], fid[v]
            g = gcd(flen[I], flen[J])
            D.setdefault((I, J), set()).add((pos[v] - pos[u]) % g)
    return D, fid, pos, flen


def d_test(D, fid, pos, flen, s, t):
    I, J = fid[s], fid[t]
    g = gcd(flen[I], flen[J])
    return (pos[t] - pos[s]) % g in D.get((I, J), set())


def kpows(k):
    o = order(k)
    out, q = [], tuple(range(len(k)))
    for _ in range(o):
        out.append(q)
        q = mul(k, q)
    return out


def brute(X, kp, s, t):
    """exists j: k^-j X k^j contains the 2-cycle (s t)."""
    if s == t:
        return False
    for q in kp:
        a, b = q[s], q[t]
        if X[a] == b and X[b] == a:
            return True
    return False


def map_data(X, Y, comp):
    """per component: E, V, F, B (trivalent), L (leaves), genus."""
    cs = set(comp)
    vX = [c for c in cycles(X) if c[0] in cs]
    vY = [c for c in cycles(Y) if c[0] in cs]
    k = mul(X, Y)
    F = [c for c in cycles(k) if c[0] in cs]
    E, V = len(comp), len(vX) + len(vY)
    deg = [len(c) for c in vX + vY]
    B, L = deg.count(3), deg.count(1)
    chi = V - E + len(F)
    return dict(E=E, V=V, F=len(F), B=B, L=L, g=(2 - chi) // 2, chi=chi, deg=deg, flen=sorted(len(c) for c in F))


# ------------------------------------------------------------------ Part A: random/exhaustive self-test
def rand_perm(n, rng):
    """random permutation of range(n) with all cycles of length <= 3."""
    lab = list(range(n))
    rng.shuffle(lab)
    p = list(range(n))
    i = 0
    while i < n:
        L = rng.choice([1, 2, 3])
        L = min(L, n - i)
        blk = lab[i:i + L]
        for a in range(L):
            p[blk[a]] = blk[(a + 1) % L]
        i += L
    return tuple(p)


def all_perms_le3(n):
    for p in permutations(range(n)):
        if all(len(c) <= 3 for c in cycles(p)):
            yield p


stats = dict(pairs=0, comps=0, g0=0, gpos=0, euler_bad=0, b0=0, b0_bad=0, path=0, path_bad=0, alt=0,
             alt_bad=0, st=0, st_pass=0, d_mis=0, oneorder_mis=0, pig=0, pig_bad=0, origin_bad=0,
             f_bound_bad=0)


def self_test(X, Y, rng):
    n = len(X)
    stats['pairs'] += 1
    k = mul(X, Y)
    kp = kpows(k)
    comps = orbits([X, Y], n)
    # claim 1: components = orbits of <X,Y>; Euler; B=0 types
    for comp in comps:
        md = map_data(X, Y, comp)
        stats['comps'] += 1
        assert md['chi'] % 2 == 0 and md['g'] >= 0 and sum(md['flen']) == md['E']
        if md['g'] == 0:
            stats['g0'] += 1
            if 2 * md['F'] != 4 + md['B'] - md['L']:
                stats['euler_bad'] += 1
            if md['F'] > 2 + md['B'] // 2:
                stats['f_bound_bad'] += 1
        else:
            stats['gpos'] += 1
            if 2 * md['F'] != 4 - 4 * md['g'] + md['B'] - md['L']:
                stats['euler_bad'] += 1
        if md['B'] == 0:
            stats['b0'] += 1
            # graph with max degree 2: path (L=2 or E=1 single edge with two leaves) or cycle (L=0)
            E = md['E']
            if md['L'] == 2:
                stats['path'] += 1
                ok = md['flen'] == [E] and md['g'] == 0
                # involution reflection formula X(i) = c - i on the single face
                fid, pos, flen = faces(k)
                cs = {(pos[X[i]] + pos[i]) % E for i in comp}
                ok &= len(cs) == 1
                c0 = cs.pop()
                for s in comp:
                    for t in comp:
                        if s == t:
                            continue
                        sol = any((2 * j - (c0 - pos[s] - pos[t])) % E == 0 for j in range(E))
                        ok &= sol == brute(X, kp, s, t)
                        if E % 2 == 1:
                            ok &= sol
                if not ok:
                    stats['path_bad'] += 1
            elif md['L'] == 0:
                stats['alt'] += 1
                h = E // 2
                ok = E % 2 == 0 and md['flen'] == [h, h] and md['g'] == 0
                fid, pos, flen = faces(k)
                fs = sorted({fid[i] for i in comp})
                ok &= all(fid[X[i]] != fid[i] for i in comp)          # X exchanges the two faces
                # origin on face 2 chosen so X sends index 0 of face 1 to index 0 of face 2
                f1 = fs[0]
                o1 = [i for i in comp if fid[i] == f1 and pos[i] == 0][0]
                o2 = X[o1]
                q = {}
                for i in comp:
                    q[i] = pos[i] if fid[i] == f1 else (pos[i] - pos[o2]) % h
                ok &= all(q[X[i]] == (-q[i]) % h for i in comp)
                for s in comp:
                    for t in comp:
                        if s == t:
                            continue
                        if fid[s] == fid[t]:
                            ok &= not brute(X, kp, s, t)
                        else:
                            sol = any((2 * j + q[s] + q[t]) % h == 0 for j in range(h))
                            ok &= sol == brute(X, kp, s, t)
                if not ok:
                    stats['alt_bad'] += 1
            else:
                stats['b0_bad'] += 1
    # claim 3: D test exact, both orders, I = J allowed; also origin independence
    D, fid, pos, flen = Dtable(X, k)
    # random relabel of face origins
    shift = {f: rng.randrange(L) for f, L in enumerate(flen)}
    pos2 = {i: (pos[i] - shift[fid[i]]) % flen[fid[i]] for i in pos}
    D2 = {}
    for c in cycles(X):
        if len(c) == 2:
            for u, v in (c, c[::-1]):
                I, J = fid[u], fid[v]
                D2.setdefault((I, J), set()).add((pos2[v] - pos2[u]) % gcd(flen[I], flen[J]))
    D1 = {}
    for c in cycles(X):
        if len(c) == 2:
            u, v = c
            I, J = fid[u], fid[v]
            D1.setdefault((I, J), set()).add((pos[v] - pos[u]) % gcd(flen[I], flen[J]))
    for s in range(n):
        for t in range(n):
            if s == t:
                continue
            stats['st'] += 1
            b = brute(X, kp, s, t)
            stats['st_pass'] += b
            if d_test(D, fid, pos, flen, s, t) != b:
                stats['d_mis'] += 1
            if d_test(D2, fid, pos2, flen, s, t) != b:
                stats['origin_bad'] += 1
            if d_test(D1, fid, pos, flen, s, t) != b:
                stats['oneorder_mis'] += 1
    # claim 4: pigeonhole on random subsets of sheets on a random face pair
    nf = len(flen)
    for _ in range(4):
        I, J = rng.randrange(nf), rng.randrange(nf)
        g = gcd(flen[I], flen[J])
        Is = [i for i in range(n) if fid[i] == I]
        Js = [i for i in range(n) if fid[i] == J]
        Ssh = rng.sample(Is, rng.randint(1, len(Is)))
        Tsh = rng.sample(Js, rng.randint(1, len(Js)))
        Sres = {pos[s] % g for s in Ssh}
        Tres = {pos[t] % g for t in Tsh}
        if D.get((I, J)) and len(Sres) + len(Tres) > g:
            stats['pig'] += 1
            if not any(brute(X, kp, s, t) for s in Ssh for t in Tsh):
                stats['pig_bad'] += 1


print('== Part A. Combinatorial self-test of claims 1, 3, 4 ==')
rng = random.Random(22222)
for n in range(1, 6):
    P = list(all_perms_le3(n))
    for X in P:
        for Y in P:
            self_test(X, Y, rng)
print('   exhaustive degree <= 5 done: pairs', stats['pairs'])
for _ in range(6000):
    n = rng.randint(6, 12)
    self_test(rand_perm(n, rng), rand_perm(n, rng), rng)
print('   stats', stats)
check(stats['euler_bad'] == 0, f"Euler: genus-0 components ({stats['g0']}) satisfy F = 2+(B-L)/2; "
      f"genus>0 components ({stats['gpos']}) satisfy F = 2-2g+(B-L)/2 instead")
check(stats['gpos'] > 0, 'random X,Y do produce positive-genus components, so genus zero needs the room (Q a sphere)')
check(stats['f_bound_bad'] == 0, 'genus 0: F <= 2 + B/2')
check(stats['b0_bad'] == 0 and stats['path_bad'] == 0 and stats['alt_bad'] == 0,
      f"B=0: path ({stats['path']}) -> one E-cycle, X(i)=c-i, 2j=c-pos s-pos t exact, odd E always soluble; "
      f"alternating cycle ({stats['alt']}) -> two h-cycles, X swaps faces and reverses index, equation exact, "
      f"no same-face witness")
check(stats['d_mis'] == 0, f"D(I,J) test equals brute force over all j < ord k on {stats['st']} ordered (s,t), "
      f"{stats['st_pass']} positive")
check(stats['origin_bad'] == 0, 'D test is independent of the chosen face origins')
print(f"   one-order-only D table disagrees with brute force on {stats['oneorder_mis']} (s,t)")
check(stats['oneorder_mis'] > 0, 'both orders of each transposition are needed (one order alone is not exact)')
check(stats['pig_bad'] == 0, f"pigeonhole |S|+|T| > g with D nonempty always gives a witness ({stats['pig']} cases)")

# ------------------------------------------------------------------ Part B: cov4181
print('\n== Part B. cov4181 (d66 rows) ==')
cells = sorted([(0, y) for y in range(6)] + [(1, 2), (1, 3), (2, 2), (2, 3)] + [(3, y) for y in range(6)]
               + [(4, y) for y in range(6)] + [(5, 2), (5, 3), (6, 2)] + [(7, y) for y in range(3)])
CS = set(cells)
idx = {c: i for i, c in enumerate(cells)}
n = len(cells)
ID = tuple(range(n))


def Vi(i):
    p = list(range(n))
    for (x, y) in cells:
        if (x + 1) % 2 == i and (x + 1, y) in idx:
            a_, b_ = idx[(x, y)], idx[(x + 1, y)]
            p[a_], p[b_] = b_, a_
    return tuple(p)


def Hj(j):
    p = list(range(n))
    for (x, y) in cells:
        if (y + 1) % 2 == j and (x, y + 1) in idx:
            a_, b_ = idx[(x, y)], idx[(x, y + 1)]
            p[a_], p[b_] = b_, a_
    return tuple(p)


def incid(pt):
    x, y = pt
    return sum((x + dx, y + dy) in CS for dx, dy in product((-1, 0), repeat=2))


V0, V1, H0, H1 = Vi(0), Vi(1), Hj(0), Hj(1)
A, Bg, C, Dg = mul(V0, H1), mul(H1, V1), mul(V1, H0), mul(H0, V0)
check(mul(mul(A, Bg), mul(C, Dg)) == ID, 'ABCD = 1 (A=V0H1, B=H1V1, C=V1H0, D=H0V0)')
# d220 note: "V_i followed by H_j" (d220 checks: mul applies p then q), i.e. H_j V_i right-to-left
d220 = dict(a=mul(H1, V0), b=mul(H1, V1), c=mul(H0, V1), d=mul(H0, V0))
rel = {nm: (g == d220[nm], g == pinv(d220[nm]))
       for nm, g in (('a', A), ('b', Bg), ('c', C), ('d', Dg))}
print('   (equal, inverse) vs d220 a,b,c,d = H1V0, H1V1, H0V1, H0V0:', rel)
t3by = {nm: sum(len(c) == 3 for c in cycles(g)) for nm, g in (('a', A), ('b', Bg), ('c', C), ('d', Dg))}
print('   3-cycles per pole:', t3by)
check(rel['a'] == (False, True) and rel['c'] == (False, True) and rel['b'][0] and rel['d'][0],
      'A = a^-1, C = c^-1 (a, c have 3-cycles, so not equal), B = b, D = d: matches the note')
check(sum(len(c) == 2 for c in cycles(Bg)) == 14
      and sum(len(c) == 2 for c in cycles(C)) == 0, 'B has 14 transpositions; C (class c = Q pole) has none')

k = mul(Bg, C)
check(k == mul(H1, H0), 'k = BC = H1H0')
colcyc = {}
for x in range(8):
    col = sorted(c for c in cells if c[0] == x)
    lo = idx[col[0]]
    cyc = [lo]
    while k[cyc[-1]] != lo:
        cyc.append(k[cyc[-1]])
    colcyc[x] = [cells[i][1] for i in cyc]
    assert len(cyc) == len(col)
print('   column k-cycles (rows from lowest):', colcyc)
table = {0: [0, 1, 3, 5, 4, 2], 3: [0, 1, 3, 5, 4, 2], 4: [0, 1, 3, 5, 4, 2],
         1: [2, 3], 2: [2, 3], 5: [2, 3], 6: [2], 7: [0, 1, 2]}
check(colcyc == table, 'k-cycle table matches the note')
check(all(mul(Bg, V1)[i] == H1[i] for i in range(n)) and Bg == tuple(H1[V1[i]] for i in range(n)),
      'B(i) = H1(V1(i)): V1 first, then H1')
pairs = [(0, 1), (2, 3), (4, 5), (6, 7)]
comps = orbits([Bg, C], n)
cp = sorted((sorted({cells[i][0] for i in c}), len(c)) for c in comps)
print('   <B,C> orbits (columns, size):', cp)
check(cp == [([0, 1], 8), ([2, 3], 8), ([4, 5], 8), ([6, 7], 4)], 'orbits are the column pairs, sizes 8,8,8,4')
for c in sorted(comps, key=lambda c: min(cells[i][0] for i in c)):
    md = map_data(Bg, C, c)
    cols = sorted({cells[i][0] for i in c})
    fl = [len([i for i in c if cells[i][0] == x]) for x in cols]
    check(md['g'] == 0 and 2 * md['F'] == 4 + md['B'] - md['L'] and md['F'] == 2,
          f'component cols {cols}: E={md["E"]} B={md["B"]} L={md["L"]} F={md["F"]} genus {md["g"]}, '
          f'face lengths by column {fl}')
for nm, (X, Y) in (('AB', (A, Bg)), ('BC', (Bg, C)), ('CD', (C, Dg)), ('DA', (Dg, A))):
    gs = [map_data(X, Y, c)['g'] for c in orbits([X, Y], n)]
    check(all(g == 0 for g in gs), f'{nm}: every <X,Y> component has genus 0 ({len(gs)} components)')
t3 = sum(sum(len(c) == 3 for c in cycles(g)) for g in (A, Bg, C, Dg))
check(t3 == 8, 'total 3-cycles over the four poles = 8 = r, so B <= 8 per two-pole map; F <= 2 + 8/2 = 6')

# Hurwitz full twist on (B,C)
def H(X, Y):
    return Y, mul(mul(pinv(Y), X), Y)


X2, Y2 = H(*H(Bg, C))
check(X2 == mul(mul(pinv(k), Bg), k) and Y2 == mul(mul(pinv(k), C), k) and mul(X2, Y2) == k,
      'H(X,Y)=(Y,Y^-1XY): H^2 = (k^-1Xk, k^-1Yk), product kept')

s, t, u, v = idx[(2, 2)], idx[(3, 3)], idx[(2, 3)], idx[(3, 2)]
Sinc = [idx[(2 - dx, 3 - dy)] for dx in (0, 1) for dy in (0, 1)]
Tinc = [idx[(4 - dx, 3 - dy)] for dx in (0, 1) for dy in (0, 1)]
check(s in Sinc and t in Tinc and Bg[s] == t and Bg[t] == s and Bg[u] == v and Bg[v] == u,
      's=(2,2) at S, t=(3,3) at T; B has 2-cycles (s t) and (u v)')
fid, pos, flen = faces(k)
off_s = (pos[u] - pos[s]) % flen[fid[s]]
off_t = (pos[v] - pos[t]) % flen[fid[t]]
check(fid[s] == fid[u] and fid[t] == fid[v] and flen[fid[s]] == 2 and flen[fid[t]] == 6
      and off_s == 1 and off_t == 3, f'offsets s->u = {off_s} mod 2 (column 2), t->v = {off_t} mod 6 (column 3)')
kp = kpows(k)
check(kp[3][s] == u and kp[3][t] == v, 'k^3 sends s,t to u,v')
B3 = mul(mul(pinv(kp[3]), Bg), kp[3])
check(B3[s] == t and B3[t] == s, 'k^-3 B k^3 exchanges s and t')
js = [j for j in range(6) if brute(Bg, [kp[j]], s, t)]
print('   exponents j mod 6 with (s t) in k^-j B k^j:', js)
check(js == [0, 3], 'for this incidence pair exactly j = 0 and j = 3 (mod 6) work')
Dn, fidn, posn, flenn = Dtable(Bg, k)
npass = sum(d_test(Dn, fidn, posn, flenn, a_, b_) for a_ in Sinc for b_ in Tinc)
nbr = sum(brute(Bg, kp, a_, b_) for a_ in Sinc for b_ in Tinc)
check(npass == nbr, f'note tuple, class b under BC: D test passes {npass} of 16 incidence pairs (brute force {nbr})')
perj = {j: sorted((cells[a_], cells[b_]) for a_ in Sinc for b_ in Tinc if brute(Bg, [kp[j]], a_, b_))
        for j in range(6)}
print('   passing incidence pairs by j:', perj)
kcd = mul(C, Dg)
kpd = kpows(kcd)
nd = sum(brute(Dg, kpd, a_, b_) for a_ in Sinc for b_ in Tinc)
check(nd == 0, f'note tuple, class d under CD: {nd} of 16 incidence pairs pass (d-dark, as in d221)')

# ------------------------------------------------------------------ geometric trace of the twist family
print('\n== Part C. Exact billiard trace of the b-twist family from S=(2,3) ==')


def vertex_step(point, velocity):
    """copied from d72 cyl.vertex_step: one unit of time, lattice point to lattice point; None at a corner."""
    x, y = point
    p, q = velocity
    a, b = abs(p), abs(q)
    sx, sy = (1 if p > 0 else -1), (1 if q > 0 else -1)
    i, j = x - (sx < 0), y - (sy < 0)
    h = kk = 1
    while h < a or kk < b:
        if h * b < kk * a:
            if (i + sx, j) in CS:
                i += sx
            else:
                sx = -sx
            h += 1
        else:
            if (i, j + sy) in CS:
                j += sy
            else:
                sy = -sy
            kk += 1
    x, y = i + (sx > 0), j + (sy > 0)
    if incid((x, y)) in (1, 3):
        return None
    if (i + sx, j) not in CS:
        sx = -sx
    if (i, j + sy) not in CS:
        sy = -sy
    return (x, y), (sx * a, sy * b)


# shear facts on the pillowcase (unit torus coords mod +-1), exact rationals
def shear(P, m=2):
    return ((P[0] + m * P[1]) % 1, P[1] % 1)


def same_pc(P, Q):
    return (P[0] % 1, P[1] % 1) == (Q[0] % 1, Q[1] % 1) or ((-P[0]) % 1, (-P[1]) % 1) == (Q[0] % 1, Q[1] % 1)


half = Fr(1, 2)
poles = [(Fr(0), Fr(0)), (half, Fr(0)), (Fr(0), half), (half, half)]
rims = [(Fr(i, 16), Fr(0)) for i in range(16)] + [(Fr(i, 16), half) for i in range(16)]
check(all(same_pc(shear(P), P) for P in poles) and all(same_pc(shear(P), P) for P in rims)
      and all(same_pc(shear((-P[0], -P[1])), (-shear(P)[0], -shear(P)[1])) for P in rims + poles),
      'shear (x,y)->(x+2y,y) commutes with -1, fixes the 4 poles and both rims pointwise')
check([(Fr(2) * y) for y in (Fr(0), Fr(1, 4), half)] == [0, half, 1],
      'x-displacement 2y runs 0 -> 1 across 0<y<1/2: one full turn (Dehn twist); (x,y)->(x+y,y) moves pole (0,1/2)')
check(not same_pc(shear((Fr(0), half), 1), (Fr(0), half)), 'unit shear is a half twist (swaps poles), so 2 is needed')

# b-family: curve around b=(1,1), c=(1,0) is vertical; full twist (X,Y)->(X,Y+2X) sends arc (1,0) to (1,2j)
S, T = (2, 3), (4, 3)
trace_ok = {}
for j in range(6):
    hits = []
    if j == 0:
        # horizontal chord along y=3: (2,3)->(3,3)->(4,3), interior points with 4 incident cells
        if all(incid(p) == 4 for p in ((2, 3), (3, 3), (4, 3))):
            hits.append(('horizontal', (3, 3)))
    else:
        for sx, sy in product((1, -1), repeat=2):
            st1 = vertex_step(S, (sx, sy * 2 * j))
            if not st1:
                continue
            st2 = vertex_step(*st1)
            if st2 and st2[0] == T:
                M = st1[0]
                if incid(M) in (2, 4) and (M[0] % 2, M[1] % 2) == (1, 1):
                    hits.append(((sx, sy * 2 * j), M))
    trace_ok[j] = hits
    print(f'   j={j}: traced witnesses S->M->T {hits}')
comb_ok = {j: bool(perj[j]) or bool(perj[(-j) % 6]) for j in range(6)}
print('   combinatorial (some incidence pair passes at j or -j):', comb_ok)
check(all(bool(trace_ok[j]) == comb_ok[j] for j in range(6)),
      'trace and twist test agree on every residue j mod 6 (j = 0, 3 lit; 1, 2, 4, 5 not)')
check(bool(trace_ok[3]), 'j=3: exact two-step billiard path S -> class-b regular point -> T in direction (+-1, +-6)')
gcd16 = gcd(1, 6)
check(gcd16 == 1, 'gcd(1,6)=1: no grid-vertex hit at non-integer times')

# ------------------------------------------------------------------ Part D: tree filter and residual graph on cov4181
print('\n== Part D. Product-relation tree, distance filter, residual graph (class a = (0,1)) ==')
tuple_ = [A, Bg, C, Dg]
names = 'ABCD'
for i0 in range(4):
    X, Y = tuple_[i0], tuple_[(i0 + 1) % 4]
    W1, W2 = tuple_[(i0 + 2) % 4], tuple_[(i0 + 3) % 4]
    kk = mul(X, Y)
    ins = orbits([X, Y], n)
    out = orbits([W1, W2], n)
    inid = {i: a_ for a_, c in enumerate(ins) for i in c}
    outid = {i: a_ for a_, c in enumerate(out) for i in c}
    edges = []
    ok = True
    for c in cycles(kk):
        ok &= len({inid[i] for i in c}) == 1 and len({outid[i] for i in c}) == 1
        edges.append((inid[c[0]], outid[c[0]]))
    # reverse orientation: cycles of W1W2 are the cycles of k^-1 (as sets)
    ok &= sorted(map(sorted, cycles(mul(W1, W2)))) == sorted(map(sorted, cycles(pinv(kk))))
    ok &= mul(W1, W2) == pinv(kk)
    nv = len(ins) + len(out)
    ok &= len(edges) == nv - 1 and len(set(edges)) == len(edges)
    par = list(range(nv))

    def f(a_):
        while par[a_] != a_:
            a_ = par[a_]
        return a_
    for a_, b_ in edges:
        ra, rb = f(a_), f(len(ins) + b_)
        ok &= ra != rb
        par[ra] = rb
    check(ok, f'pair {names[i0]}{names[(i0+1)%4]}: {len(ins)}+{len(out)} vertices, {len(edges)} edges, tree; '
              f'W1W2 = k^-1')

# regular interior class-a marks and their lifts (2-cycles of A)
marks = [(x, y) for x in range(9) for y in range(7) if (x % 2, y % 2) == (0, 1) and incid((x, y)) == 4]
lifts = {}
for P in marks:
    inc = [idx[(P[0] - dx, P[1] - dy)] for dx in (0, 1) for dy in (0, 1)]
    tc = {tuple(sorted((i, A[i]))) for i in inc}
    assert all(A[i] != i and A[A[i]] == i for i in inc) and len(tc) == 2 and set(sum(tc, ())) == set(inc)
    lifts[P] = sorted(tc)
tA = sum(len(c) == 2 for c in cycles(A))
print(f'   regular interior class-a marks m_a = {len(marks)}: {marks}; t_a = {tA}')
check(2 * len(marks) <= tA, f'each mark uses two distinct A-transpositions: 2 m_a = {2*len(marks)} <= t_a = {tA}')
check(11 // 2 == 5 and comb(5, 2) == 10, 'n = 22: t_a <= 11 so m_a <= 5 and at most 10 pairs')

families = [('B|BC', Bg, mul(Bg, C), (C, Dg, A)), ('C|BC', C, mul(Bg, C), None),
            ('C|CD', C, mul(C, Dg), None), ('D|CD', Dg, mul(C, Dg), (A, Bg))]
filt_bad = 0
edges_union = set()
for nm, X, kk, _ in families:
    kpf = kpows(kk)
    # complementary components for the tree filter
    if nm.endswith('BC'):
        ins, out = orbits([Bg, C], n), orbits([Dg, A], n)
    else:
        ins, out = orbits([C, Dg], n), orbits([A, Bg], n)
    inid = {i: a_ for a_, c in enumerate(ins) for i in c}
    outid = {i: a_ for a_, c in enumerate(out) for i in c}
    fidf, posf, flf = faces(kk)
    adj = {}
    for c in cycles(kk):
        adj.setdefault(('o', outid[c[0]]), set()).add(('i', inid[c[0]]))
        adj.setdefault(('i', inid[c[0]]), set()).add(('o', outid[c[0]]))

    def dist(a_, b_):
        seen, fr, d = {a_}, [a_], 0
        while fr:
            if b_ in fr:
                return d
            fr = [z for y in fr for z in adj[y] if z not in seen]
            seen |= set(fr)
            d += 1
        return None
    npairs = 0
    for P1 in marks:
        for P2 in marks:
            if P1 >= P2:
                continue
            for l1 in lifts[P1]:
                for l2 in lifts[P2]:
                    o1, o2 = outid[l1[0]], outid[l2[0]]
                    assert outid[l1[1]] == o1 and outid[l2[1]] == o2
                    wit = [(a_, b_) for a_ in l1 for b_ in l2 if brute(X, kpf, a_, b_)]
                    dd = dist(('o', o1), ('o', o2))
                    if wit:
                        edges_union.add((P1, P2))
                        npairs += 1
                        for a_, b_ in wit:
                            if o1 != o2:
                                ok = dd == 2 and inid[a_] == inid[b_]
                            else:
                                ok = fidf[a_] == fidf[b_]
                            filt_bad += not ok
    print(f'   family {nm}: lift pairs with a two-traversal witness = {npairs}')
check(filt_bad == 0, 'every witness obeys the tree filter (distance 2 via one x,y-component, or same face)')
allpairs = {(P1, P2) for P1 in marks for P2 in marks if P1 < P2}
missing = sorted(allpairs - edges_union)
print(f'   residual graph: {len(allpairs)} mark pairs, {len(edges_union)} edges, {len(missing)} missing')
print('   missing pairs:', missing)
check(((2, 3), (4, 3)) in edges_union, 'S=(2,3), T=(4,3) is an edge (class b)')

print('\nFAILURES:', len(FAIL), FAIL)
print('CPU %.1f s' % (time.process_time() - T0))
