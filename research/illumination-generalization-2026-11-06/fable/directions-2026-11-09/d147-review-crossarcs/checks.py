"""d147: independent referee checks for cross-factor-arcs (snapshot 2026-11-22 00:30).

Named room only (the b = 7 odd cross). No search over rooms, no network.
Shares no code with roomtools / d4_monodromy / hurwitz.

Model.  Sheets are the 96 cells.  A piece is (cell, side); the piece of cell (i,j)
on side s lies over the pillowcase front iff i+j+s is even, so each cell has exactly
one front piece (its sheet).  Crossing the pillowcase edge X=e (e = 0,1) moves a piece
across the physical vertical side x = X with X = e (mod 2): into the neighbour cell
on the same side, or, at a wall, onto the other side of the same cell.  The site
permutation at corner (ex,ey) is tauY[ey] o tauX[ex] on sheets.  Sites are absolute
lattice parities; the mark origin selects which corner is called a.
"""
from collections import Counter
from itertools import combinations, product
from math import gcd, lcm
import sys, time

T0 = time.process_time()
CELLS = {(x, y) for x in range(-7, 7) for y in range(-7, 7) if -2 <= x < 2 or -2 <= y < 2}
CL = sorted(CELLS)
IDX = {c: k for k, c in enumerate(CL)}
N = len(CL)
assert N == 96


def status(p):
    x, y = p
    return sum((c in CELLS) for c in ((x-1, y-1), (x, y-1), (x-1, y), (x, y)))


PTS = sorted({(i+dx, j+dy) for (i, j) in CELLS for dx in (0, 1) for dy in (0, 1)})
INTERIOR = [p for p in PTS if status(p) == 4]
print('cells', N, 'lattice pts', len(PTS), 'interior', len(INTERIOR),
      'reflex', sum(status(p) == 3 for p in PTS), 'convex', sum(status(p) == 1 for p in PTS))


# ---------- monodromy ----------
def tau(axis, e):
    out = {}
    for (i, j) in CL:
        for s in (0, 1):
            k = i if axis == 0 else j
            side = k if k % 2 == e else k + 1
            step = -1 if side == k else 1
            nb = (i+step, j) if axis == 0 else (i, j+step)
            out[(i, j), s] = (nb, s) if nb in CELLS else ((i, j), 1 - s)
    return out


TX = [tau(0, 0), tau(0, 1)]
TY = [tau(1, 0), tau(1, 1)]
PIECE = [(c, (c[0]+c[1]) % 2) for c in CL]   # front piece of each cell


def on_sheets(*taus):          # apply taus left to right
    perm = []
    for pc in PIECE:
        for t in taus:
            pc = t[pc]
        assert (pc[0][0]+pc[0][1]+pc[1]) % 2 == 0
        perm.append(IDX[pc[0]])
    return tuple(perm)


G = {(ex, ey): on_sheets(TX[ex], TY[ey]) for ex in (0, 1) for ey in (0, 1)}
HV = on_sheets(TY[0], TY[1])   # vertical loop: boundary of a disk with the two sites of equal x-parity
HH = on_sheets(TX[0], TX[1])   # horizontal loop


def cycles(p):
    seen, out = set(), []
    for s in range(len(p)):
        if s not in seen:
            c, t = [], s
            while t not in seen:
                seen.add(t); c.append(t); t = p[t]
            out.append(c)
    return out


def compose(p, q):  # p then q
    return tuple(q[p[i]] for i in range(len(p)))


def inverse(p):
    r = [0]*len(p)
    for i, v in enumerate(p):
        r[v] = i
    return tuple(r)


def power(p, k):
    r = tuple(range(len(p)))
    k %= max(1, order(p))
    for _ in range(k):
        r = compose(r, p)
    return r


def order(p):
    return lcm(*(len(c) for c in cycles(p)))


def corner_of(cell, par):
    i, j = cell
    return (i if i % 2 == par[0] else i+1, j if j % 2 == par[1] else j+1)


# sanity: each site cycle sits over one lattice point; lengths match physical status
for par, g in G.items():
    for c in cycles(g):
        pts = {corner_of(CL[s], par) for s in c}
        assert len(pts) == 1
        p = pts.pop()
        st = status(p)
        assert len(c) == {1: 1, 2: 2, 3: 3, 4: 2}[st], (par, p, st, len(c))
    tally = Counter(status(p) for p in PTS if (p[0] % 2, p[1] % 2) == par)
    assert len(cycles(g)) == tally[1]+tally[2]+tally[3]+2*tally[4]
ident = tuple(range(N))
from itertools import permutations as _perms
rel = [o for o in _perms(sorted(G)) if compose(compose(compose(G[o[0]], G[o[1]]), G[o[2]]), G[o[3]]) == ident]
assert rel
print('orders with product identity', len(rel), rel[0])
print('site cycle types', {par: sorted(Counter(map(len, cycles(g))).items()) for par, g in G.items()})
print('ord(HV)', order(HV), 'ord(HH)', order(HH))


# ---------- block systems ----------
def closure(seeds, gens):
    par = list(range(N))
    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]; a = par[a]
        return a
    todo = list(seeds)
    while todo:
        a, b = todo.pop()
        ra, rb = find(a), find(b)
        if ra == rb:
            continue
        par[ra] = rb
        for g in gens:
            todo.append((g[a], g[b]))
    bl = {}
    for a in range(N):
        bl.setdefault(find(a), []).append(a)
    return tuple(sorted(tuple(b) for b in bl.values()))


GENS = list(G.values())
systems = {closure([(0, s)], GENS) for s in range(1, N)}
while True:
    new = {closure([(b[0], x) for b in A for x in b] + [(b[0], x) for b in B for x in b], GENS)
           for A in systems for B in systems} - systems
    if not new:
        break
    systems |= new
proper = sorted((s for s in systems if 1 < len(s) < N), key=len)
print('nontrivial block systems by #blocks', sorted(len(s) for s in systems))
FACT = [s for s in proper if len(s) in (24, 48)]
assert sorted(map(len, FACT)) == [24, 48, 48, 48]
FACT.append(tuple((i,) for i in range(N)))


def name(bl):
    here = next(b for b in bl if IDX[(-7, -2)] in b)
    return f"{len(bl)} {sorted(CL[s] for s in here)}"


def induced(g, bl):
    w = {s: k for k, b in enumerate(bl) for s in b}
    return tuple(w[g[b[0]]] for b in bl)


# ---------- twist pencils ----------
def classes(o):
    return {'a': o, 'b': ((o[0]+1) % 2, o[1]), 'c': ((o[0]+1) % 2, (o[1]+1) % 2), 'd': (o[0], (o[1]+1) % 2)}


def pencils_for(o, D):
    """Adjacent non-source partners in cyclic order a,b,c,d -> boundary loop h."""
    cl = classes(o)
    partners = {'b': ['c'], 'c': ['b', 'd'], 'd': ['c']}[D]
    out = []
    for E in partners:
        same_x = cl[D][0] == cl[E][0]
        out.append((E, HV if same_x else HH))
    return out


class UF:
    def __init__(s, n): s.p = list(range(n))
    def f(s, a):
        while s.p[a] != a:
            s.p[a] = s.p[s.p[a]]; a = s.p[a]
        return a
    def u(s, a, b): s.p[s.f(a)] = s.f(b)


def slice_labels(A, Dj, regular=False):
    """Components of the bipartite (A-cycle, Dj-cycle) graph with sheets as edges; per sheet."""
    n = len(A)
    ac = {s: k for k, c in enumerate(cycles(A)) for s in c}
    dc = {s: k for k, c in enumerate(cycles(Dj)) for s in c}
    alen = {k: len(c) for k, c in enumerate(cycles(A))}
    dlen = {k: len(c) for k, c in enumerate(cycles(Dj))}
    na = len(alen)
    uf = UF(na + len(dlen))
    for s in range(n):
        if regular and (alen[ac[s]] != 2 or dlen[dc[s]] != 2):
            continue
        uf.u(ac[s], na + dc[s])
    return [uf.f(ac[s]) for s in range(n)]


def label_closure(A, D, h):
    """The note's residue-label transitive closure, reimplemented with Python sets."""
    L = order(h)
    pos = {}
    for c in cycles(h):
        for k, x in enumerate(c):
            pos[x] = (tuple(c), k)
    acs, dcs = cycles(A), cycles(D)
    inc = {}
    for ui, U in enumerate(acs):
        for ci, C in enumerate(dcs):
            lab = set()
            for x in U:
                cyc, kx = pos[x]
                l = len(cyc)
                for y in C:
                    cy, ky = pos[y]
                    if cy == cyc:
                        lab |= {r for r in range(L) if r % l == (ky-kx) % l}
            if lab:
                inc[ui, ci] = frozenset(lab)
    m = len(acs)
    P = [[frozenset(range(L)) if i == j else frozenset() for j in range(m)] for i in range(m)]
    for i in range(m):
        for j in range(m):
            if i != j:
                s = set()
                for ci in range(len(dcs)):
                    s |= inc.get((i, ci), frozenset()) & inc.get((j, ci), frozenset())
                P[i][j] = frozenset(s)
    for k in range(m):
        for i in range(m):
            if P[i][k]:
                for j in range(m):
                    P[i][j] = P[i][j] | (P[i][k] & P[k][j])
    ai = {s: k for k, c in enumerate(acs) for s in c}
    return P, ai


def lifts(p, par):
    """Site-cycles (sheet sets) over lattice point p."""
    return [c for c in cycles(G[par]) if corner_of(CL[c[0]], par) == p]


# ---------- Check 1 and 2: reproduce table; test dictionary ----------
print('\n== check 1: table ==')
dict_tests = Counter()
identity_rows = {}   # (o, D, s, t) -> dict with per-pencil restricted/unrestricted j-sets
results = {}
for bl in FACT:
    nm = name(bl)
    w = {s: k for k, b in enumerate(bl) for s in b}
    cnt = Counter()
    resid = []
    ident_cover = len(bl) == N
    for o in product((0, 1), repeat=2):
        cl = classes(o)
        A = induced(G[o], bl)
        pts = [p for p in INTERIOR if (p[0] % 2, p[1] % 2) == o]
        marks = {p: {w[s] for c in lifts(p, o) for s in c} for p in pts}
        liftsets = {p: [{w[s] for s in c} for c in lifts(p, o)] for p in pts}
        for D in 'bcd':
            Dp = induced(G[cl[D]], bl)
            pens = []
            for E, h in pencils_for(o, D):
                hq = induced(h, bl)
                L = order(hq)
                sl = [slice_labels(A, compose(compose(power(hq, -j), Dp), power(hq, j))) for j in range(L)]
                Dc = [cycles(compose(compose(power(hq, -j), Dp), power(hq, j))) for j in range(L)]
                reg = [slice_labels(A, compose(compose(power(hq, -j), Dp), power(hq, j)), True)
                       for j in range(L)] if ident_cover else None
                # dictionary: D_j-cycles meeting U == D-cycles meeting h^j U (as sets after h^-j)
                for U in cycles(A)[:6]:
                    for j in (1, 2, L-1):
                        j %= L
                        lhs = {frozenset(c) for c in Dc[j] if set(c) & set(U)}
                        # my slice uses D_j = h^j D h^-j, whose cycles are h^j C; U meets h^j C
                        # iff h^-j U meets C.  (The note's h^j U is the same statement for -j.)
                        hjU = {power(hq, -j)[x] for x in U}
                        rhs = {frozenset(power(hq, j)[y] for y in C) for C in cycles(Dp) if set(C) & hjU}
                        dict_tests['dict ok' if lhs == rhs else 'dict FAIL'] += 1
                # label closure exactness against slices
                P, ai = label_closure(A, Dp, hq)
                for x in range(len(A)):
                    for y in range(x+1, len(A)):
                        # note's label r means h^r x = y, i.e. my slice -r
                        js = frozenset((-j) % L for j in range(L) if sl[j][x] == sl[j][y])
                        dict_tests['closure ok' if P[ai[x]][ai[y]] == js else 'closure FAIL'] += 1
                pens.append((E, L, sl, Dc, reg))
            # ordinary components (zero slice cross-check)
            uf = UF(len(A))
            for g in (A, Dp):
                for c in cycles(g):
                    for x in c[1:]:
                        uf.u(c[0], x)
            for E, L, sl, Dc, reg in pens:
                ok = all((uf.f(x) == uf.f(y)) == (sl[0][x] == sl[0][y]) for x in range(len(A)) for y in range(len(A)))
                dict_tests['zero slice ok' if ok else 'zero slice FAIL'] += 1
            for s, t in combinations(pts, 2):
                cnt['rows'] += 1
                ms, mt = marks[s], marks[t]
                base = any(uf.f(x) == uf.f(y) for x in ms for y in mt)
                one = any(set(C) & ms and set(C) & mt for E, L, sl, Dc, reg in pens for Dcj in Dc for C in Dcj)
                clo = any(sl[j][x] == sl[j][y] for E, L, sl, Dc, reg in pens for j in range(L) for x in ms for y in mt)
                if base:
                    cnt['base'] += 1
                elif one:
                    cnt['one contact'] += 1
                elif clo:
                    cnt['closure'] += 1
                else:
                    cnt['remaining'] += 1
                    resid.append((o, D, s, t))
                assert not (base and not clo) and not (one and not clo)
                if ident_cover:
                    rec = {}
                    for E, L, sl, Dc, reg in pens:
                        un = frozenset(j for j in range(L) if any(sl[j][x] == sl[j][y] for x in ms for y in mt))
                        rg = frozenset(j for j in range(L) if any(reg[j][x] == reg[j][y] for x in ms for y in mt))
                        assert rg <= un
                        # per-lift split, for the physical comparison
                        per = [[frozenset(j for j in range(L) if any(reg[j][x] == reg[j][y] for x in ls for y in lt))
                                for lt in liftsets[t]] for ls in liftsets[s]]
                        rec[E] = (L, un, rg, per)
                    identity_rows[o, D, s, t] = rec
    results[nm] = (cnt, resid)
    print(nm, dict(cnt))
    for r in resid:
        print('   residual', len(bl), r)
print('dictionary/closure tests', dict(dict_tests))

ir = identity_rows
print('identity: rows with unrestricted pencil hit', sum(any(v[1] for v in r.values()) for r in ir.values()),
      ' restricted hit', sum(any(v[2] for v in r.values()) for r in ir.values()),
      ' rows where restricted != unrestricted', sum(any(v[1] != v[2] for v in r.values()) for r in ir.values()))
lit_pairs = {(k[0], k[2], k[3]) for k, r in ir.items() if any(v[2] for v in r.values())}
print('identity restricted: physical pairs covered', len(lit_pairs), 'of', len({(k[0], k[2], k[3]) for k in ir}))
print('CPU so far %.1fs' % (time.process_time() - T0))


# ---------- physical tracer (exact integers, in the room itself) ----------
def trace(S, v, graze=False, max_arcs=20000, want_path=False):
    """Billiard ray from lattice point S in primitive direction v.  Returns (visited lattice
    points in order, stop reason).  Stops at convex/reflex corners."""
    sx, sy = (v[0] > 0) - (v[0] < 0), (v[1] > 0) - (v[1] < 0)
    ax, ay = abs(v[0]), abs(v[1])
    P = S
    seen_states = set()
    out = []
    if ax and ay:
        cell = (S[0] - (sx < 0), S[1] - (sy < 0))
        if cell not in CELLS:
            return out, 'blocked'
        for _ in range(max_arcs):
            st = (cell, sx, sy)
            if st in seen_states:
                return out, 'periodic'
            seen_states.add(st)
            # events: vertical-line crossings at u = k*ay, horizontal at u = k*ax, 0<u<ax*ay
            ev = sorted([(k*ay, 0) for k in range(1, ax)] + [(k*ax, 1) for k in range(1, ay)])
            for _, kind in ev:
                i, j = cell
                if kind == 0:
                    nb = (i+sx, j)
                    if nb in CELLS: cell = nb
                    else: sx = -sx
                else:
                    nb = (i, j+sy)
                    if nb in CELLS: cell = nb
                    else: sy = -sy
            i, j = cell
            P = (i + (sx > 0), j + (sy > 0))
            out.append(P)
            k = status(P)
            if k == 4:
                cell = (i+sx, j+sy)
            elif k == 2:
                if (i+sx, j) in CELLS:
                    sy = -sy; cell = (i+sx, j)
                else:
                    assert (i, j+sy) in CELLS
                    sx = -sx; cell = (i, j+sy)
            else:
                return out, 'corner'
        return out, 'cap'
    # axial ray along a lattice line
    d = (sx, sy)
    def edge_cells(P, d):
        x, y = P
        if d[1] == 0:
            cx = x if d[0] > 0 else x-1
            return [(cx, y-1), (cx, y)]
        cy = y if d[1] > 0 else y-1
        return [(x-1, cy), (x, cy)]
    if sum(c in CELLS for c in edge_cells(S, d)) < (1 if graze else 2):
        return out, 'blocked'
    for _ in range(max_arcs):
        st = (P, d)
        if st in seen_states:
            return out, 'periodic'
        seen_states.add(st)
        P = (P[0]+d[0], P[1]+d[1])
        out.append(P)
        k = status(P)
        if k in (1, 3):
            return out, 'corner'
        ahead = sum(c in CELLS for c in edge_cells(P, d))
        if ahead == 2 or (graze and ahead == 1):
            continue
        if ahead == 0:
            d = (-d[0], -d[1])          # head-on reflection at a smooth wall point
            continue
        return out, 'graze'
    return out, 'cap'


def lit_by(S, v, graze=False):
    seen = set()
    for w in ((v[0], v[1]), (-v[0], -v[1])):
        pts, _ = trace(S, w, graze)
        seen.update(pts)
    return seen


# ---------- Check 3: physical comparison of every identity pencil slice ----------
print('\n== check 3: identity pencil slices vs physical rays ==')
def slope(o, D, E, j):
    if D == 'b': return (1, 2*j)               # twist of (1,0) about the vertical loop
    if D == 'd': return (2*j, 1)               # twist of (0,1) about the horizontal loop
    return (1, 1+2*j) if E == 'b' else (1+2*j, 1)


cache = {}
def phys(S, v, graze=False):
    key = (S, v, graze)
    if key not in cache:
        cache[key] = lit_by(S, v, graze)
    return cache[key]


def reflect_j(D, E, j):
    # (p,q) -> (p,-q) maps the pencil to itself: j -> -j for b,d; c/b: 1+2j -> -(1+2j): j -> -1-j
    if D in 'bd': return -j
    return -1 - j


cmp = Counter()
mismatch = []
for (o, D, s, t), rec in ir.items():
    if D == 'c':
        continue        # reference diagonal is (1,1) or (1,-1) by origin; fitted exactly below
    for E, (L, un, rg, per) in rec.items():
        half = L // 2
        js = range(-half, L - half)
        for sg in (1, -1):
            P = frozenset(j % L for j in js if t in phys(s, slope(o, D, E, sg*j)))
            M = frozenset(j % L for j in js if t in phys(s, slope(o, D, E, reflect_j(D, E, sg*j))))
            ok_row = rg == (P | M)
            l0 = frozenset().union(*per[0])
            l1 = frozenset().union(*per[1])
            ok_lift = {l0, l1} == {P, M}
            cmp[D, E, sg, 'row', ok_row] += 1
            cmp[D, E, sg, 'per-lift', ok_lift] += 1
            if sg == 1 and not ok_row:
                mismatch.append((o, D, E, s, t, sorted(rg), sorted(P | M)))
for k in sorted(cmp):
    print('  class %s pencil %s twist sign %+d %-8s match=%-5s %d' % (k[0], k[1], k[2], k[3], k[4], cmp[k]))
for m in mismatch[:4]:
    print('  mismatch', m)

# class c: fit the slice-to-slope map j -> slope(eps*j + c0) per origin
fit = Counter()
for o in product((0, 1), repeat=2):
    for E in 'bd':
        rows = [(s, t, rec[E]) for (oo, D, s, t), rec in ir.items() if oo == o and D == 'c']
        L = rows[0][2][0]
        good = []
        for eps in (1, -1):
            for c0 in range(L):
                def jj(j): return ((eps*j + c0 + L//2) % L) - L//2
                ok = all(rg == frozenset(j for j in range(L) if t in phys(s, slope(o, 'c', E, jj(j))) or
                                         t in phys(s, slope(o, 'c', E, reflect_j('c', E, jj(j)))))
                         for s, t, (L, un, rg, per) in rows)
                if ok:
                    good.append((eps, c0 if c0 <= L//2 else c0 - L))
        print('  class c, origin %s, pencil %s: exact maps (eps, offset) = %s' % (o, E, good))

# periodicity in j: slopes j and j+L light the same targets
per_ok = Counter()
for o in [(0, 0), (1, 1)]:
    pts = [p for p in INTERIOR if (p[0] % 2, p[1] % 2) == o]
    for D, E, L in (('b', 'c', order(HV)), ('d', 'c', order(HH))):
        for j in (1, 2, 3):
            for S in pts[:6]:
                a = phys(S, slope(o, D, E, j)) & set(pts)
                b = phys(S, slope(o, D, E, j + L)) & set(pts)
                per_ok['same' if a == b else 'differ'] += 1
print('periodicity j vs j+ord(h) on marks:', dict(per_ok))

# explicit witnesses: rows with no reference-arc lift but a restricted hit at a nonzero power
print('\n-- explicit witnesses --')
shown = 0
for (o, D, s, t), rec in sorted(ir.items()):
    E, (L, un, rg, per) = next(iter(rec.items()))
    if 0 in rg or not rg or shown >= 3:
        continue
    if shown and D == prev_D:
        continue
    j = min(rg, key=lambda r: min(r, L - r))
    jj = j if j <= L // 2 else j - L
    for jt in (jj, reflect_j(D, E, jj)):
        v = slope(o, D, E, jt)
        for w in (v, (-v[0], -v[1])):
            pts, why = trace(s, w)
            if t in pts:
                k = pts.index(t)
                path = [s] + pts[:k+1]
                bad = [p for p in path[1:-1] if status(p) in (1, 3)]
                print(f'row origin={o} class={D} pencil={E} power j={jj}: {s} -> {t} along {w}, '
                      f'{k+1} arcs, corners on path={bad}')
                print('   lattice points:', path)
                shown += 1; prev_D = D
                break
        else:
            continue
        break

# ---------- Check 4: Riemann-Hurwitz bound ----------
print('\n== check 4: Riemann-Hurwitz ==')
for bl in FACT[:4]:
    m = len(bl)
    ft = {}
    for par, g in G.items():
        cs = Counter(map(len, cycles(induced(g, bl))))
        ft[par] = (cs[1], cs[3], cs[2])
    print(name(bl), 'per site (fixed, 3-cycles, 2-cycles):', ft)
    for i, j in combinations(sorted(G), 2):
        bound = (ft[i][0] + ft[j][0] - ft[i][1] - ft[j][1]) / 2
        A, B = induced(G[i], bl), induced(G[j], bl)
        h = induced(HV if i[0] == j[0] else HH, bl) if (i[0] == j[0] or i[1] == j[1]) else None
        comps = []
        for k in range(order(h) if h else 1):
            Bk = compose(compose(power(h, -k), B), power(h, k)) if h else B
            comps.append(len(set(slice_labels(A, Bk))))
        assert min(comps) >= bound
        if bound >= 1 or m == 24:
            print(f'   sites {i},{j}: bound {bound:g}, components over pencil {sorted(set(comps))}')

# ---------- Check 5: residual chords ----------
print('\n== check 5: residuals ==')
allres = results[name(FACT[-1])][1]
for (o, D, s, t) in allres:
    dv = (t[0]-s[0], t[1]-s[1]); g = gcd(*dv); prim = (dv[0]//g, dv[1]//g)
    cls = {(1, 0): 'b', (1, 1): 'c', (0, 1): 'd'}[(prim[0] % 2, prim[1] % 2)]
    pts, why = trace(s, prim)
    chord = t in pts[:g] and all(status(p) == 4 for p in pts[:g])
    # does any slope of the SPECIFIED class light it physically?
    hit = None
    for M in range(1, 16):
        for p in range(-M, M+1):
            for q in (M, -M) if abs(p) < M else range(-M, M+1):
                if gcd(p, q) != 1 or (abs(p) % 2, abs(q) % 2) != {'b': (1, 0), 'c': (1, 1), 'd': (0, 1)}[D]:
                    continue
                if t in phys(s, (p, q)):
                    hit = (p, q); break
            if hit: break
        if hit: break
    print(f'  {o} class {D} {s}-{t}: straight chord {prim} class {cls} interior={chord};'
          f' specified-class witness {hit}')

# ---------- Check 6: full physical illumination of interior lattice pairs ----------
print('\n== check 6: physical illumination, all interior pairs ==')
DIRS = [(p, q) for p in range(0, 13) for q in range(-12, 13) if gcd(p, q) == 1 and (p > 0 or q == 1)]
reach = {S: set() for S in INTERIOR}
for S in INTERIOR:
    for v in DIRS:
        reach[S] |= phys(S, v)
same = [(s, t) for s, t in combinations(INTERIOR, 2) if (s[0]-t[0]) % 2 == 0 and (s[1]-t[1]) % 2 == 0]
mixed = [(s, t) for s, t in combinations(INTERIOR, 2) if (s, t) not in set(same)]
dark_same = [(s, t) for s, t in same if t not in reach[s]]
dark_mixed = [(s, t) for s, t in mixed if t not in reach[s]]
print('same-parity pairs', len(same), 'unlit with |p|,|q|<=12:', len(dark_same))
print('mixed-parity pairs', len(mixed), 'unlit with |p|,|q|<=12:', len(dark_mixed), dark_mixed[:5])
asym = sum((t in reach[s]) != (s in reach[t]) for s, t in combinations(INTERIOR, 2))
print('reversibility violations', asym)
CLS = {(1, 0): 'b', (1, 1): 'c', (0, 1): 'd'}
by_class = Counter()
for s_, t_ in same:
    for D in 'bcd':
        ok = any(t_ in phys(s_, v) for v in DIRS if CLS[(abs(v[0]) % 2, abs(v[1]) % 2)] == D)
        by_class[D, ok] += 1
print('same-parity rows physically lit in their specified class (|p|,|q|<=12):', dict(by_class))
pts, why = trace((-5, 0), (-2, 5))
k = pts.index((1, 0))
print('residual (-5,0)->(1,0), class d, direction (-2,5):', [(-5, 0)] + pts[:k+1],
      'statuses', [status(p) for p in pts[:k+1]])
print('\nCPU total %.1fs' % (time.process_time() - T0))
