"""d221 referee checks: cylinder levels, open saddle connections, counts, twist/CRT test.

Named rooms only (cov446, cov4181, R22). Reuses d72's origami code (cyl.py, orbit.py).
No room enumeration; directions are fixed lists or the named rooms' own SL2(Z) orbits.
Run: nice -n 10 python3 -B checks.py > checks.log
"""
import sys
import time
from collections import deque
from itertools import product
from math import comb, gcd
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'd72-cylinder-test'))
import importlib.util  # noqa: E402
import cyl  # noqa: E402
# d72's orbit.py by path: cyl's imports put another directory's orbit.py first on sys.path
_spec = importlib.util.spec_from_file_location('d72orbit', HERE.parent / 'd72-cylinder-test' / 'orbit.py')
orbit = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(orbit)

T0 = time.process_time()
FAIL = []


def check(cond, msg):
    print(('PASS ' if cond else 'FAIL ') + msg, flush=True)
    if not cond:
        FAIL.append(msg)


ROOMS = dict(cyl.rooms())
C446 = set(map(tuple, ROOMS['cov446']))
C4181 = set(map(tuple, ROOMS['cov4181']))
R22 = set(map(tuple, ROOMS['R22']))
D66_4181 = set([(0, y) for y in range(6)] + [(1, 2), (1, 3), (2, 2), (2, 3)] + [(3, y) for y in range(6)]
               + [(4, y) for y in range(6)] + [(5, 2), (5, 3), (6, 2)] + [(7, y) for y in range(3)])


def show(cells):
    X = max(x for x, _ in cells) + 1
    Y = max(y for _, y in cells) + 1
    mx = min(x for x, _ in cells)
    my = min(y for _, y in cells)
    for y in range(Y - 1, my - 1, -1):
        print('   y=%d ' % y + ''.join('#' if (x, y) in cells else '.' for x in range(mx, X)))


def nreflex(cells):
    pts = {(x + dx, y + dy) for x, y in cells for dx in (0, 1) for dy in (0, 1)}
    return sum(cyl.incid(cells, p) == 3 for p in pts)


# ------------------------------------------------------------------ state analysis
def state_data(O, r, u, marked):
    """Cylinders (w, h), saddle-connection lengths, components of regular sites."""
    N = len(r)
    Dc = cyl.Decomp(type('M', (), {'marked': marked})(), r, u)
    rows = cyl.cycles(r)
    cylrows = {}
    for k, c in enumerate(rows):
        cylrows.setdefault(Dc.cyl[k], []).append(k)
    cyls = []
    for key, ks in cylrows.items():
        w = {len(rows[k]) for k in ks}
        ncrit = sum(not Dc.reg[k] for k in ks)
        cyls.append((w.pop() if len(w) == 1 else None, len(ks), ncrit))
    sc = []          # saddle connection lengths
    comp = {}        # regular square -> component id
    for k, c in enumerate(rows):
        if Dc.reg[k]:
            for i in c:
                comp[i] = ('circ', k)
            continue
        m = [p for p, i in enumerate(c) if marked[c[p]]]
        L = len(c)
        for a_, p in enumerate(m):
            q = m[(a_ + 1) % len(m)]
            ell = (q - p) % L or L
            sc.append(ell)
            for s in range(1, ell):
                comp[c[(p + s) % L]] = ('sc', k, p)
    return cyls, sc, comp, Dc


print('== Rooms (cells from d72 rooms(), d66 rows) ==')
for nm, cells in (('cov446', C446), ('cov4181', C4181), ('R22', R22)):
    print(nm, 'n', len(cells), 'r', nreflex(cells))
    show(cells)
check(C4181 == D66_4181, 'cov4181 from covers.json equals the d66 cell rows')

# ------------------------------------------------------------------ claim 3: counts
print('\n== Claim 3. Site, saddle-connection, and pair counts ==')
DIRS = [(1, 0), (0, 1), (1, 1), (-1, 1), (2, 1), (3, 2), (-3, 8), (1, 4)]
for nm, cells in (('cov4181', C4181), ('R22', R22), ('cov446', C446)):
    O = cyl.Origami(cells)
    n, rr = len(cells), nreflex(cells)
    N = 4 * n
    # points of X = commutator cycles (fixed under the SL2 action, which keeps LL corners)
    ri, ui = cyl.inv(O.r), cyl.inv(O.u)
    com = [O.r[O.u[ri[ui[i]]]] for i in range(N)]
    pid = [0] * N
    cy = cyl.cycles(com)
    for k, c in enumerate(cy):
        for i in c:
            pid[i] = k
    nsites = len(cy)
    nF = sum(O.marked[c[0]] for c in cy)
    nreg = nsites - nF
    lens3 = sum(len(c) == 3 for c in cy)
    check(nsites == 4 * n - 2 * rr and lens3 == rr,
          f'{nm}: {N} incidences, {nsites} sites = 4n-2r, {lens3} triple sites = r')
    check(nF == 2 * rr + 4 and nreg == 4 * n - 4 * rr - 4,
          f'{nm}: |F| = {nF} = 2r+4, M = {nreg} = 4n-4r-4')
    check(sum(O.marked) == 4 * rr + 4, f'{nm}: marked incidences {sum(O.marked)} = E = 4r+4')
    for v in DIRS:
        r, u = cyl.act(O.r, O.u, cyl.word(*v))
        cyls, sc, comp, Dc = state_data(O, r, u, O.marked)
        L = sum(w for w, h, _ in cyls)
        ok = all(w is not None and nc == 1 for w, h, nc in cyls)
        ok &= sum(w * h for w, h, _ in cyls) == N
        ok &= len(sc) == 4 * rr + 4 and sum(sc) == L
        reg_circ = sum(w * (h - 1) for w, h, _ in cyls)
        reg_sc = sum(ell - 1 for ell in sc)
        ok &= reg_circ == N - L and reg_sc == L - (4 * rr + 4) and reg_circ + reg_sc == nreg
        crit_sites = len({pid[i] for i in range(N) if not Dc.reg[Dc.row[i]]})
        ok &= crit_sites == L - 2 * rr
        # brute-force pair count over distinct regular sites
        groups = {}
        for i, c in comp.items():
            groups.setdefault(c, set()).add(pid[i])
        assert all(len(g) == sum(1 for i in comp if comp[i] == c) for c, g in groups.items())
        brute = sum(comb(len(g), 2) for g in groups.values())
        formula = sum((h - 1) * comb(w, 2) for w, h, _ in cyls) + sum(comb(ell - 1, 2) for ell in sc)
        ok &= brute == formula
        check(ok, f'{nm} v={v}: cyl (w,h)={sorted((w, h) for w, h, _ in cyls)} L={L} '
                  f'E={len(sc)} circ sites={reg_circ} sc sites={reg_sc} crit sites={crit_sites} '
                  f'pairs brute={brute} formula={formula}')
print('   n=22, r=8 arithmetic: incidences 88, sites', 88 - 16, 'F', 20, 'M', 88 - 36, 'E', 36,
      'L range [36, 88]; circles 88-L, intervals L-36')
check(88 - 16 == 72 and 72 - 20 == 52 and 4 * 22 - 4 * 8 - 4 == 52, 'n=22 r=8 site numbers 72, 20, 52')


# ------------------------------------------------------------------ claims 1,2: full orbits
def orbit_scan(cells, S, T, cap=60000):
    """BFS the coloured orbit; per state record (I) same regular row, CC, (II) same open saddle conn."""
    O = cyl.Origami(cells)
    N = len(O.sq)
    col = [1 if O.marked[i] else 2 if O.ll[i] == S else 3 if O.ll[i] == T else 0 for i in range(N)]
    k0 = orbit.canon(O.r, O.u, col)
    seen = {k0}
    dq = deque([k0])
    tally = dict(I=0, CC=0, II=0, states=0)
    first = {}
    while dq:
        key = dq.popleft()
        r, u, c = orbit.unpack(key, N)
        tally['states'] += 1
        mk = [x == 1 for x in c]
        Dc = cyl.Decomp(orbit.Marked(c), r, u)
        ss = [i for i in range(N) if c[i] == 2]
        ts = [i for i in range(N) if c[i] == 3]
        I = any(Dc.row[s] == Dc.row[t] and Dc.reg[Dc.row[s]] for s in ss for t in ts)
        CC = any(Dc.cc(s, t) for s in ss for t in ts)
        II = any(Dc.lit(s, t) and not Dc.reg[Dc.row[s]] for s in ss for t in ts)
        lit_any = any(Dc.lit(s, t) for s in ss for t in ts)
        assert lit_any == (I or II)
        assert not I or CC
        for nmk, val in (('I', I), ('CC', CC), ('II', II)):
            if val:
                tally[nmk] += 1
                first.setdefault(nmk, tally['states'])
        for g in (('T', 1),), (('V', 1),):
            r2, u2 = cyl.act(r, u, g)
            k2 = orbit.canon(r2, u2, c)
            if k2 not in seen:
                if len(seen) >= cap:
                    return 'CAP', tally
                seen.add(k2)
                dq.append(k2)
    return 'CLOSED', tally


print('\n== Claims 1-2. Complete coloured orbits: (I), CC, (II) ==')
st, t = orbit_scan(C446, (1, 2), (3, 2))
print('   cov446 (1,2)-(3,2):', st, t)
check(st == 'CLOSED' and t['states'] == 9072 and t['I'] == 0 and t['CC'] == 0 and t['II'] > 0,
      'cov446: orbit closes at 9,072; no (I), no common open cylinder, (II) in %d states' % t['II'])
O = cyl.Origami(C446)
Dc = cyl.Decomp(O, O.r, O.u)
s, tt = O.lift((1, 2), (1, 1)), O.lift((3, 2), (1, 1))
check(Dc.lit(s, tt) and not Dc.reg[Dc.row[s]] and cyl.incid(C446, (4, 2)) == 3
      and all(cyl.incid(C446, p) == 4 for p in ((1, 2), (2, 2), (3, 2))),
      'cov446: horizontal chord (1,2)-(2,2)-(3,2) on a critical leaf; (4,2) is reflex')
st, t = orbit_scan(R22, (0, 0), (2, 2))
print('   R22 (0,0)-(2,2):', st, t)
check(st == 'CLOSED' and t['I'] == 0 and t['II'] == 0 and t['CC'] == 0,
      'R22: complete orbit (%d states) has neither (I) nor (II)' % t['states'])
st, t = orbit_scan(C4181, (2, 3), (4, 3))
print('   cov4181 (2,3)-(4,3):', st, t)
check(st == 'CLOSED' and t['I'] > 0 and t['II'] > 0, 'cov4181: complete orbit has both (I) and (II) states')

# Gamma(2): three cusps, so each parity class of P^1(Q) is one Gamma(2) orbit (sample check)
print('\n== Claim 1. Gamma(2) reduction to (1,0),(0,1),(1,1) (bounded sample) ==')


def g2_reduce(p, q):
    steps = 0
    while not ((abs(p), abs(q)) in ((1, 0), (0, 1), (1, 1))):
        if abs(p) > abs(q):
            k = round(p / (2 * q))
            p -= 2 * k * q
        else:
            k = round(q / (2 * p))
            q -= 2 * k * p
        steps += 1
        assert steps < 200
    return (abs(p), abs(q))


bad = 0
cnt = 0
for p in range(-40, 41):
    for q in range(-40, 41):
        if gcd(p, q) == 1:
            cnt += 1
            bad += g2_reduce(p, q) != ((p % 2), (q % 2))
check(bad == 0, f'Gamma(2) shears reduce {cnt} primitive vectors (|p|,|q|<=40) to their parity representative')

# ------------------------------------------------------------------ claim 4: cov4181 witness
print('\n== Claim 4. cov4181 type-(I) witness in direction (-3,8) ==')
claimed_pos = [(2, 3), (1, 3), (4, 1), (3, 5), (4, 3), (5, 1), (4, 5), (5, 3), (2, 3)]
claimed_sg = ['-+', '++', '+-', '+-', '-+', '--', '+-', '-+', '-+']


def sg(v):
    return ('+' if v[0] > 0 else '-') + ('+' if v[1] > 0 else '-')


for label, cells in (('d66 rows', C4181), ('x-mirror', {(7 - x, y) for x, y in C4181}),
                     ('y-mirror', {(x, 5 - y) for x, y in C4181})):
    st = ((2, 3), (-3, 8))
    pos, sgs = [st[0]], [sg(st[1])]
    for _ in range(8):
        st = cyl.vertex_step(cells, *st) if st else None
        if not st:
            break
        pos.append(st[0])
        sgs.append(sg(st[1]))
    print(f'   {label}: positions {pos}')
    print(f'   {label}: signs     {sgs}')
    if label == 'd66 rows':
        check(pos == claimed_pos, 'positions match the note on the d66 cell rows (no reflection needed)')
        check(sgs == claimed_sg, 'outgoing velocity signs match the note')
        check(all(cyl.incid(cells, p) in (2, 4) for p in pos), 'all nine listed sites are regular')
        check(pos[4] == (4, 3) and sgs[4] == sgs[0] and pos[8] == (2, 3) and sgs[8] == sgs[0],
              'T at step 4 on the starting sheet; S at step 8 with the starting velocity')
        check(gcd(3, 8) == 1, 'internal crossing times 1/3,2/3 and j/8 never coincide (no grid-vertex hit)')
        check(pos[2] == (4, 1) and (pos[2][0] - 2) % 2 == 0 and (pos[2][1] - 3) % 2 == 0,
              'four-step witness midpoint (4,1) is in the source class')
O = cyl.Origami(C4181)
r, u = cyl.act(O.r, O.u, cyl.word(-3, 8))
Dc = cyl.Decomp(O, r, u)
s, tt = O.lift((2, 3), (1, 1)), O.lift((4, 3), (1, 1))
check(Dc.row[s] == Dc.row[tt] and Dc.reg[Dc.row[s]] and len(cyl.cycles(r)[0]) >= 1,
      'origami state for (-3,8): S~,T~ on sheet (1,1) share one regular row (row length %d)'
      % len([c for c in cyl.cycles(r) if s in c][0]))
seg = all(cyl.incid(C4181, p) == 4 for p in ((2, 3), (3, 3), (4, 3), (5, 3))) and cyl.incid(C4181, (6, 3)) == 3
Dc0 = cyl.Decomp(O, O.r, O.u)
check(seg and Dc0.lit(s, tt) and not Dc0.reg[Dc0.row[s]],
      'class-b horizontal chord (2,3)-(4,3) lies on a critical leaf ending at reflex (6,3)')


# ------------------------------------------------------------------ claims 5-6: tuple
def mul(p, q):  # (p*q)(i) = p(q(i)), right-to-left
    return tuple(p[i] for i in q)


def pinv(p):
    out = [0] * len(p)
    for i, x in enumerate(p):
        out[x] = i
    return tuple(out)


def pcycles(p):
    return cyl.cycles(list(p))


cells = sorted(C4181)
idx = {c: i for i, c in enumerate(cells)}
n = len(cells)


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


V, H = {i: Vi(i) for i in (0, 1)}, {j: Hj(j) for j in (0, 1)}
# poles in cyclic order (0,0),(1,0),(1,1),(0,1); loop at pole (i,j) = product of the two edge reflections
POLES = [(0, 0), (1, 0), (1, 1), (0, 1)]
tup = [mul(V[0], H[0]), mul(H[0], V[1]), mul(V[1], H[1]), mul(H[1], V[0])]
prod = tuple(range(n))
for g in tup:
    prod = mul(prod, g)
print('\n== Claim 5. Coincidence counts (Riemann-Hurwitz on Q) ==')
check(prod == tuple(range(n)), 'cov4181 pole tuple (V0H0, H0V1, V1H1, H1V0) has product 1')
t2 = sum(sum(len(c) == 2 for c in pcycles(g)) for g in tup)
t3 = sum(sum(len(c) == 3 for c in pcycles(g)) for g in tup)
check(t3 == 8 and t2 == 2 * n - 2 - 2 * t3 and 2 * t2 == 4 * n - 4 * 8 - 4,
      f'cov4181: 3-cycles {t3} = r, 2-cycles {t2} = 2n-2-2r, and 2*{t2} = M on X')
print('   n=22 primitive branch: 2d = 2*21 = 42, J = 2*8 = 16, R = 42-16 = 26 = 2*22-2-2*8;'
      ' t_a <= 11 so 26 - t_a >= 15')
check(42 - 16 == 2 * 22 - 2 - 16 == 26 and 26 - 11 == 15 and 2 * 26 == 52, 'area-22 arithmetic')


print('\n== Claim 6. Full-twist formula and CRT test on the cov4181 tuple ==')


def sigma(t, i):  # (g,h) -> (h, h^-1 g h) at positions i,i+1
    t = list(t)
    g, h = t[i], t[i + 1]
    t[i], t[i + 1] = h, mul(mul(pinv(h), g), h)
    return t


def order(p):
    o, q = 1, p
    while q != tuple(range(len(p))):
        q, o = mul(q, p), o + 1
    return o


ok_all = True
for i in range(3):
    k = mul(tup[i], tup[i + 1])
    ordk = order(k)
    t = list(tup)
    for j in range(1, 2 * ordk + 1):
        t = sigma(sigma(t, i), i)
        kj = tuple(range(n))
        for _ in range(j):
            kj = mul(kj, k)
        exp_x = mul(mul(pinv(kj), tup[i]), kj)
        exp_y = mul(mul(pinv(kj), tup[i + 1]), kj)
        pr = tuple(range(n))
        for g in t:
            pr = mul(pr, g)
        ok = t[i] == exp_x and t[i + 1] == exp_y and pr == tuple(range(n))
        ok &= all(t[m] == tup[m] for m in range(4) if m not in (i, i + 1))
        ok_all &= ok
    print(f'   positions {POLES[i]},{POLES[i+1]}: ord k = {ordk}, cycle type of k '
          f'{sorted((len(c) for c in pcycles(k)), reverse=True)}')
check(ok_all, 'j full twists give k^-j g k^j on both entries, other entries and product fixed (j <= 2 ord k)')

# CRT equivalence and the d-dark / b-lit verdicts for S=(2,3), T=(4,3), a=(0,1)
S, T = (2, 3), (4, 3)
inc = {P: [idx[(P[0] - dx, P[1] - dy)] for dx in (0, 1) for dy in (0, 1)] for P in (S, T)}
ga = tup[POLES.index((0, 1))]
check(all(ga[ga[s]] == s and ga[s] != s for s in inc[S] + inc[T]), 'sheets at S and T are 2-cycles of g_a')


def crt_ok(k, s, t, u, v):
    cs = [c for c in pcycles(k) if s in c][0]
    ct = [c for c in pcycles(k) if t in c][0]
    if u not in cs or v not in ct:
        return False
    i_s = (cs.index(u) - cs.index(s)) % len(cs)
    i_t = (ct.index(v) - ct.index(t)) % len(ct)
    return (i_s - i_t) % gcd(len(cs), len(ct)) == 0


mism = 0
hits = {}
for xi in range(4):
    if POLES[xi] == (0, 1):
        continue
    for yi in (xi - 1, xi + 1):
        if not 0 <= yi < 4 or POLES[yi] == (0, 1):
            continue
        i0 = min(xi, yi)
        k = mul(tup[i0], tup[i0 + 1])
        gx = tup[xi]
        trans = [tuple(c) for c in pcycles(gx) if len(c) == 2]
        ordk = order(k)
        found = 0
        for s, t in product(inc[S], inc[T]):
            brute = False
            for j in range(ordk):
                kj = tuple(range(n))
                for _ in range(j):
                    kj = mul(kj, k)
                hx = mul(mul(pinv(kj), gx), kj)
                brute |= hx[s] == t and hx[t] == s and s != t
            crt = any(crt_ok(k, s, t, u, v) or crt_ok(k, s, t, v, u) for u, v in trans)
            mism += brute != crt
            found += crt
        rel = ((POLES[xi][0] - 0) % 2, (POLES[xi][1] - 1) % 2)
        hits[(POLES[xi], POLES[yi])] = found
        print(f'   x={POLES[xi]} (rel {rel}) twisted with y={POLES[yi]}: '
              f'{len(trans)} transpositions, (s,t) incidence pairs passing CRT = {found} of 16')
check(mism == 0, 'CRT test agrees with brute force over all exponents j < ord k')
nt = {P: sum(len(c) == 2 for c in pcycles(tup[POLES.index(P)])) for P in POLES}
print('   2-cycles per pole', nt)
qpole = [P for P in POLES if nt[P] == 0]
check(qpole == [(1, 0)] or qpole == [(0, 0)], 'exactly one Q pole (no 2-cycles): %s' % qpole)
dpole = [P for P in POLES if P not in ((0, 1), (1, 1)) + tuple(qpole)][0]   # b = (1,1) is the lit class
print('   relative classes: a=(0,1), b=(1,1) [lit by (3,3)], c=%s (Q), d=%s' % (qpole[0], dpole))
check(all(v == 0 for (x, y), v in hits.items() if x == dpole),
      'no two-traversal witness at the d-dark class (consistent with d66 per-target darkness)')

print('\nFAILURES:', len(FAIL), FAIL)
print('CPU %.1f s' % (time.process_time() - T0))
