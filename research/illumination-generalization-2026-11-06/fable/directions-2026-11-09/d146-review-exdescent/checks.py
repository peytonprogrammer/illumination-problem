"""d146 checks for exclusion-descent.md (snapshot 2026-11-22 02:40).

Named rooms only, no searches: cov4181 (d144/d145 cell list), and the
normalized BBBB controls DB55, DBas, U2, c4181s (d69 decomp.py constructors)
plus the odd cross b=7 (every-direction.md / canonical-transfer.md).
Exact integer / Fraction arithmetic.

Model. Q = room double, squares (x, y, c), c in {0 top, 1 bottom}.  Front
squares over the pillowcase B are those with x+y+c even (n of them).  For
each pillowcase edge e in {L, R, Bo, T} the crossing involution tau_e sends a
square to the square across its side lying over e (neighbour cell, same copy;
or same cell, other copy at a wall).  The local monodromy at site (i, j) is
g_ij = tau_{V_i} o tau_{H_j} on front squares, V_0=L, V_1=R, H_0=Bo, H_1=T.
"""
from collections import Counter
from fractions import Fraction as Fr
from itertools import permutations, product
from math import floor, ceil, gcd
import time

t0 = time.process_time()


def hdr(s):
    print('=' * 78); print(s); print('=' * 78)


def rect(x0, x1, y0, y1):
    return {(i, j) for i in range(x0, x1) for j in range(y0, y1)}


def stretch(cells, axis, at, times):  # copied from d69 decomp.py
    out = set()
    for c in cells:
        z = c[axis]
        if z < at:
            out.add(c)
        elif z == at:
            for t in range(times + 1):
                out.add((c[0] + t, c[1]) if axis == 0 else (c[0], c[1] + t))
        else:
            out.add((c[0] + times, c[1]) if axis == 0 else (c[0], c[1] + times))
    return out


def cov4181():
    cov = set()
    for x, ys in enumerate([range(6), (2, 3), (2, 3), range(6), range(6), (2, 3), (2,), range(3)]):
        for y in ys:
            cov.add((x, y))
    assert len(cov) == 28
    return cov


from pathlib import Path
ROOM_FILE = [int(t) for t in (Path(__file__).resolve().parents[4] / 'qclass-closure' / 'offgrid'
                              / 'cov4181.room').read_text().split()[:58]]


def counts(cells):
    return Counter((x + i, y + j) for x, y in cells for i in (0, 1) for j in (0, 1))


def wall_gcds(cells):
    hs, vs = set(), set()
    for x, y in cells:
        for dy in (-1, 1):
            if (x, y + dy) not in cells:
                hs.add((y + (dy > 0), x, dy))
        for dx in (-1, 1):
            if (x + dx, y) not in cells:
                vs.add((x + (dx > 0), y, dx))

    def lens(units):
        out = []
        for (line, a, s) in units:
            if (line, a - 1, s) in units:
                continue
            L = 1
            while (line, a + L, s) in units:
                L += 1
            out.append(L)
        return out
    hl, vl = lens(hs), lens(vs)
    gh = gv = 0
    for L in hl: gh = gcd(gh, L)
    for L in vl: gv = gcd(gv, L)
    return len(hl) + len(vl), gh, gv


# ---------------------------------------------------------------- monodromy
class Double:
    def __init__(self, cells):
        self.cells = cells
        self.front = sorted((x, y, c) for (x, y) in cells for c in (0, 1) if (x + y + c) % 2 == 0)
        self.idx = {s: i for i, s in enumerate(self.front)}
        self.n = len(self.front)
        assert self.n == len(cells)
        g = {}
        for i in (0, 1):
            for j in (0, 1):
                g[(i, j)] = [self.idx[self.tau('V', i, self.tau('H', j, s))] for s in self.front]
        self.g = g

    def tau(self, axis, k, s):
        x, y, c = s
        if axis == 'V':   # side on vertical line X with X % 2 == k
            nb = (x - 1, y) if x % 2 == k else (x + 1, y)
        else:
            nb = (x, y - 1) if y % 2 == k else (x, y + 1)
        return (nb[0], nb[1], c) if nb in self.cells else (x, y, 1 - c)

    def cycles(self, perm):
        seen, out = set(), []
        for i in range(len(perm)):
            if i in seen:
                continue
            cyc = [i]; seen.add(i); j = perm[i]
            while j != i:
                cyc.append(j); seen.add(j); j = perm[j]
            out.append(tuple(cyc))
        return out

    def qpoint(self, P, copy=None):
        """Front sheets of the Q-point at physical lattice point P (copy for interior P)."""
        X, Y = P
        around = [(X - 1, Y - 1), (X, Y - 1), (X - 1, Y), (X, Y)]
        inside = [a for a in around if a in self.cells]
        if len(inside) == 4:
            sq = [(a[0], a[1], copy) for a in inside if (a[0] + a[1] + copy) % 2 == 0]
        else:
            sq = [(a[0], a[1], c) for a in inside for c in (0, 1) if (a[0] + a[1] + c) % 2 == 0]
        sh = frozenset(self.idx[s] for s in sq)
        site = (X % 2, Y % 2)
        cyc = [frozenset(cy) for cy in self.cycles(self.g[site]) if sh <= set(cy)]
        assert len(cyc) == 1 and cyc[0] == sh, (P, copy, sh)
        return sh


def closure(n, gens, pairs):
    par = list(range(n))

    def f(a):
        while par[a] != a:
            par[a] = par[par[a]]; a = par[a]
        return a
    stack = list(pairs)
    while stack:
        u, v = stack.pop()
        ru, rv = f(u), f(v)
        if ru == rv:
            continue
        par[ru] = rv
        for g in gens:
            stack.append((g[u], g[v]))
    # fixpoint check: closure rule applied to class representatives
    blocks = {}
    for i in range(n):
        blocks.setdefault(f(i), []).append(i)
    part = frozenset(frozenset(b) for b in blocks.values())
    bl = {i: b for b in part for i in b}
    for g in gens:
        for b in part:
            assert len({bl[g[i]] for i in b}) == 1
    return part


def block_systems(D):
    gens = list(D.g.values())
    n = D.n
    atoms = {closure(n, gens, [(0, s)]) for s in range(1, n)}
    systems = set(atoms)
    frontier = set(atoms)
    while frontier:
        new = set()
        for P in frontier:
            for A in atoms:
                pairs = [(min(b), i) for b in P for i in b] + [(min(b), i) for b in A for i in b]
                J = closure(n, gens, pairs)
                if J not in systems:
                    new.add(J)
        systems |= new
        frontier = new
    return sorted(systems, key=lambda P: -len(P))


def quotient(D, part):
    blocks = sorted(part, key=min)
    lab = {i: k for k, b in enumerate(blocks) for i in b}
    q = {}
    for x, g in D.g.items():
        q[x] = tuple(lab[g[min(b)]] for b in blocks)
    return blocks, lab, q


def ctype(perm):
    seen, out = set(), []
    for i in range(len(perm)):
        if i in seen: continue
        L = 0; j = i
        while j not in seen:
            seen.add(j); j = perm[j]; L += 1
        out.append(L)
    return tuple(sorted(out, reverse=True))


def cyc_str(perm):
    cs = []
    seen = set()
    for i in range(len(perm)):
        if i in seen or perm[i] == i:
            seen.add(i); continue
        c = [i]; seen.add(i); j = perm[i]
        while j != i:
            c.append(j); seen.add(j); j = perm[j]
        cs.append('(' + ''.join(map(str, c)) + ')')
    return ''.join(cs) or 'id'


def canonical(D, x):
    pairs = [c for c in D.cycles(D.g[x]) if len(c) == 2]
    if not pairs:
        return None
    return closure(D.n, list(D.g.values()), pairs)


def analyse(name, cells, verbose=True):
    D = Double(cells)
    W, gh, gv = wall_gcds(cells)
    c = counts(cells)
    r = sum(k == 3 for k in c.values())
    print(f'[{name}] n={D.n} W={W} r={r} gcd(h)={gh} gcd(v)={gv} normalized={gh == gv == 1}')
    # product relation and local cycle types
    for x in sorted(D.g):
        ct = Counter(ctype(D.g[x]))
        assert set(ct) <= {1, 2, 3}
    types = {x: dict(Counter(ctype(D.g[x]))) for x in sorted(D.g)}
    print(f'   site cycle types (length: count): {types}')
    canon = {}
    for x in sorted(D.g):
        Bx = canonical(D, x)
        canon[x] = 'Q (no 2-cycles)' if Bx is None else ('B (universal)' if len(Bx) == 1 else f'proper, {len(Bx)} blocks')
    print(f'   canonical B_x: {canon}')
    bbbb = all(v == 'B (universal)' for v in canon.values())
    systems = block_systems(D)
    proper = [P for P in systems if 1 < len(P) < D.n]
    print(f'   block systems: {len(systems)}; outer degrees present: {sorted({len(P) for P in systems})}; '
          f'proper: {len(proper)}; BBBB={bbbb}')
    for P in proper:
        _, _, q = quotient(D, P)
        print(f'     proper quotient outer degree {len(P)} (inner {D.n // len(P)}): types '
              f'{ {x: ctype(q[x]) for x in sorted(q)} }')
    return D, systems, proper, bbbb, r


# ================================================================== 1
hdr('1. cov4181: monodromy over the pillowcase, block systems, the unique proper quotient')
cells = cov4181()
assert ROOM_FILE[0] == 28 and ROOM_FILE[1] == 20
file_cells = {(ROOM_FILE[2 + 2 * k], ROOM_FILE[3 + 2 * k]) for k in range(28)}
print('cell list == qclass-closure/offgrid/cov4181.room:', file_cells == cells)
assert file_cells == cells
D, systems, proper, bbbb, r = analyse('cov4181', cells)
S, T = (2, 3), (4, 3)
cS, cT = counts(cells)[S], counts(cells)[T]
print(f'S={S} count {cS}, T={T} count {cT} (4 = interior)')
site = {'a': (S[0] % 2, S[1] % 2)}
site['b'] = ((site['a'][0] + 1) % 2, site['a'][1])
site['d'] = (site['a'][0], (site['a'][1] + 1) % 2)
site['c'] = ((site['a'][0] + 1) % 2, (site['a'][1] + 1) % 2)
print('site labels relative to S:', site)
assert len(proper) == 1
P = proper[0]
blocks, lab, q = quotient(D, P)
print('block sizes:', sorted(len(b) for b in blocks))
for k in 'abcd':
    print(f'   N over {k}={site[k]}: {cyc_str(q[site[k]])}  type {ctype(q[site[k]])}')
# product relation of the edge model: (tL tBo)(tBo tR)(tR tT)(tT tL) = id, i.e.
# g00 . g10^-1 . g11 . g01^-1 = id, upstairs and on the blocks
def inv(p):
    out = [0] * len(p)
    for i, j in enumerate(p):
        out[j] = i
    return out


def rel(g):
    comp = list(range(len(g[(0, 0)])))
    for h in (inv(g[(0, 1)]), g[(1, 1)], inv(g[(1, 0)]), g[(0, 0)]):  # rightmost first
        comp = [h[i] for i in comp]
    return comp == list(range(len(comp)))


print('   relation g00 g10^-1 g11 g01^-1 = id upstairs:', rel(D.g), '; in N:', rel(q))
Npoint = {}
for name_, Pt in (('S', S), ('T', T)):
    for cp in (0, 1):
        sh = D.qpoint(Pt, cp)
        letters = {lab[i] for i in sh}
        Npoint[(name_, cp)] = letters
        print(f'   {name_} copy {cp}: Q-point sheets {sorted(sh)} -> N letters {letters}; '
              f'fixed by A: {all(q[site["a"]][l] == l for l in letters)}; fixed by D: {all(q[site["d"]][l] == l for l in letters)}')
# regular point over d in N and in Q
print('   N has a 2-cycle over d:', 2 in ctype(q[site['d']]))
Bd = canonical(D, site['d'])
print('   canonical closure of all upstairs d-transpositions: blocks', len(Bd))
# c fiber: zero and pole of N
zero_letters = [l for l in range(4) if q[site['c']][l] != l]
pole_letter = [l for l in range(4) if q[site['c']][l] == l]
zsheets = {i for i in range(D.n) if lab[i] in zero_letters}
c_cycles = [cy for cy in D.cycles(D.g[site['c']]) if set(cy) <= zsheets]
print(f'   N zero over c = letters {zero_letters}: upstairs cycles {[len(cy) for cy in c_cycles]}')
reflex_c = sorted(p for p, k in counts(cells).items() if k == 3 and (p[0] % 2, p[1] % 2) == site['c'])
zero_pts = set()
for p in reflex_c:
    sh = D.qpoint(p)
    if sh <= zsheets:
        zero_pts.add(p)
print(f'   physical reflexes of parity c: {len(reflex_c)} {reflex_c}; those over the N-zero: {len(zero_pts)}')
print(f'   all reflexes: {r}; reflexes over the c-zero = all parity-c reflexes: {zero_pts == set(reflex_c)}')
pole_cycles = [cy for cy in D.cycles(D.g[site['c']]) if set(cy) <= {i for i in range(D.n) if lab[i] in pole_letter}]
print(f'   N pole over c: upstairs cycle lengths {sorted(len(cy) for cy in pole_cycles)} (7 convex corners)')

# ================================================================== 2
hdr('2. Arc components: S4 lemma, then the actual preimage graphs in Q and N')
# 2a. Lemma: in S4, types A=(2,1,1) B=(2,2) C=(3,1) D=(2,1,1) with product 1 in any order
S4 = list(permutations(range(4)))


def mul(p, q_):  # p after q_
    return tuple(p[q_[i]] for i in range(4))


bad = 0; tot = 0
byT = {t: [p for p in S4 if ctype(p) == t] for t in {(2, 1, 1), (2, 2), (3, 1)}}
for A_, B_, C_, D_ in product(byT[(2, 1, 1)], byT[(2, 2)], byT[(3, 1)], byT[(2, 1, 1)]):
    for order in permutations((A_, B_, C_, D_)):
        pr = (0, 1, 2, 3)
        for g_ in order:
            pr = mul(g_, pr)
        if pr != (0, 1, 2, 3):
            continue
        tot += 1
        sa = {i for i in range(4) if A_[i] != i}; sd = {i for i in range(4) if D_[i] != i}
        if len(sa & sd) != 1:
            bad += 1
print(f'S4 lemma: {tot} (tuple, order) solutions of the product relation; A,D supports not meeting in exactly one letter: {bad}')

# 2b. arc = pillowcase edge L from d to a (direction (0,1)): components = orbits of <g_a, g_d>
ga, gd = D.g[site['a']], D.g[site['d']]


def orbits_of(n, gens):
    par = list(range(n))
    def f(a):
        while par[a] != a:
            par[a] = par[par[a]]; a = par[a]
        return a
    for g in gens:
        for i in range(n):
            par[f(i)] = f(g[i])
    out = {}
    for i in range(n):
        out.setdefault(f(i), set()).add(i)
    return list(out.values())


orb = orbits_of(D.n, [ga, gd])
print(f'arc L (direction (0,1)) in Q: {len(orb)} components, sizes {sorted(len(o) for o in orb)}')
for key, letters in Npoint.items():
    sh = D.qpoint(S if key[0] == 'S' else T, key[1])
    comp_id = [k for k, o in enumerate(orb) if sh <= o]
    print(f'   {key}: component {comp_id}')
sep_L = all(not any(D.qpoint(S, a) <= o and D.qpoint(T, b) <= o for o in orb) for a in (0, 1) for b in (0, 1))
print('   S lifts and T lifts in different components of the preimage of L:', sep_L)
orbN = orbits_of(4, [q[site['a']], q[site['d']]])
print('   in N, components = orbits of <A,D>:', [sorted(o) for o in orbN])


# 2c. general arcs of class (p even, q odd), p != 0: build preimage graph geometrically
def trace_first(cells, P, w):
    """Billiard from lattice point P, velocity w, to the first lattice point. Returns (R, arrival velocity)."""
    x, y = Fr(P[0]), Fr(P[1]); vx, vy = w
    while True:
        tx = (((floor(x) + 1) if vx > 0 else (ceil(x) - 1)) - x) / vx
        ty = (((floor(y) + 1) if vy > 0 else (ceil(y) - 1)) - y) / vy
        dt = min(tx, ty)
        x, y = x + vx * dt, y + vy * dt
        if x.denominator == 1 and y.denominator == 1:
            return (int(x), int(y)), (vx, vy)
        if dt == tx:
            col = int(x) if vx > 0 else int(x) - 1
            if (col, floor(y)) not in cells: vx = -vx
        else:
            row = int(y) if vy > 0 else int(y) - 1
            if (floor(x), row) not in cells: vy = -vy


def arc_graph(D, p, q_):
    cells = D.cells
    cnt = counts(cells)
    par = {}
    def f(a):
        par.setdefault(a, a)
        while par[a] != a:
            par[a] = par[par[a]]; a = par[a]
        return a
    def vert(Pt, w):
        if cnt[Pt] == 4:
            cp = 0 if w in ((p, q_), (-p, -q_)) else 1
            return D.qpoint(Pt, cp)
        return D.qpoint(Pt)
    nedges = 0
    for Pt, k in cnt.items():
        if (Pt[0] % 2, Pt[1] % 2) != site['a']:
            continue
        for w in ((p, q_), (-p, q_), (p, -q_), (-p, -q_)):
            cell = (Pt[0] if w[0] > 0 else Pt[0] - 1, Pt[1] if w[1] > 0 else Pt[1] - 1)
            if cell not in cells:
                continue
            R, u = trace_first(cells, Pt, w)
            assert (R[0] % 2, R[1] % 2) == site['d']
            a_, b_ = vert(Pt, w), vert(R, (-u[0], -u[1]))
            par[f(a_)] = f(b_); nedges += 1
    return f, nedges


arcs = [(2, 1), (2, -1), (2, 3), (4, 1), (4, -3), (2, 5), (6, 1), (8, 3), (10, -7)]
allsep = True
for (p, q_) in arcs:
    f, ne = arc_graph(D, p, q_)
    sep = all(f(D.qpoint(S, a)) != f(D.qpoint(T, b)) for a in (0, 1) for b in (0, 1))
    allsep &= sep
    # count physical edges: each Q edge counted once from its a end; must be n (one per sheet)
    print(f'   arc class ({p},{q_}): Q edges {ne} (= n: {ne == D.n}); S-lifts separated from T-lifts: {sep}')
print('all tested arcs separate S from T in Q:', allsep)

# ================================================================== 3
hdr('3. Structural charge r >= k = n/4 for the four-sheet mechanism')
k = D.n // 4
print(f'   inner degree k = {k}; distinct reflexes over the c-zero = {len(zero_pts)}; r = {r} >= k: {r >= k}; '
      f'W = 2r+4 = {2 * r + 4} >= n/2+4 = {D.n // 2 + 4}')
print('   r <= 8 forces n = 4k <= 4r <= 32')

# ================================================================== 4
hdr('4. Named normalized BBBB rooms: all pillowcase factors')
COV279 = {(0, 0), (1, 0), (0, 1), (1, 1), (1, 2), (2, 2), (3, 2), (2, 3), (3, 3), (4, 3),
          (4, 4), (5, 4), (4, 5), (5, 5)}
named = {
    'DB55': rect(0, 5, 0, 5) | rect(5, 8, 2, 3) | rect(8, 13, 0, 5),
    'DBas': rect(0, 5, 0, 4) | rect(5, 9, 1, 2) | rect(9, 13, -1, 5),
    'U2': rect(0, 9, 0, 2) | rect(0, 2, 2, 9) | rect(7, 9, 2, 7) | rect(5, 7, 5, 7),
    'c4181s': stretch(stretch(cells, 0, 1, 2), 1, 4, 3),
    'cross7': rect(-7, 7, -2, 2) | rect(-2, 2, -7, 7),
}
summary = {}
for nm, cl in named.items():
    Dn, sy, pr, bb, rr = analyse(nm, cl)
    small = [len(P_) for P_ in pr if len(P_) in (2, 3, 4)]
    summary[nm] = (bb, sorted(len(P_) for P_ in pr), small)
print('summary (BBBB, proper outer degrees, small 2..4):', summary)

# cross7: check the zeros of its proper factor
Dc = Double(named['cross7'])
for P_ in [P_ for P_ in block_systems(Dc) if 1 < len(P_) < Dc.n]:
    _, _, qq = quotient(Dc, P_)
    z = sum(Counter(ctype(qq[x]))[3] for x in qq)
    po = sum(Counter(ctype(qq[x]))[1] for x in qq)
    mixed = [x for x in qq if 2 in ctype(qq[x]) and 3 in ctype(qq[x])]
    print(f'   cross7 factor outer {len(P_)}: zeros {z}, poles {po}, poles-zeros = {po - z}; sites with both 2- and 3-cycles {mixed}')

print(f'CPU seconds: {time.process_time() - t0:.2f}')
