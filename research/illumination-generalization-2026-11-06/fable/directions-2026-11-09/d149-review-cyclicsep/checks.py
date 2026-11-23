"""d149 referee checks for cyclic-separation.md (snapshot 2026-11-22-0050).

Named room DB55 only; no room search.  Three independent computations:
  (A) a direct billiard tracer in the room (reflect at flat walls, stop at every corner);
  (B) the note's single-arc test  L^k I meets J,  L = A^3 X^3, on the reference arcs,
      using the archived roomtools pillowcase tuple;
  (C) the 4-copy unfolding as a labelled square-tiled surface, its SL(2,Z) orbit,
      the stabilizer H (and H cap Gamma(2)), its cusps, and a per-direction cusp label.
Then: lit status is constant on cusps, and the cusp representatives decide each class.
"""
import sys, time
from math import gcd
from itertools import product, combinations
from pathlib import Path

T0 = time.process_time()
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'd10-mechanisms'))
import roomtools as rt  # noqa: E402

def rect(a, b, c, d):
    return set(product(range(a, b), range(c, d)))

CELLS = rect(0, 5, 0, 5) | rect(5, 8, 2, 3) | rect(8, 13, 0, 5)   # DB55, as in deletion-check.py
assert rt.is_strictly_simple(CELLS)
S, T = (2, 2), (10, 2)
N = int(sys.argv[1]) if len(sys.argv) > 1 else 40          # height bound for directions
LIMIT = int(sys.argv[2]) if len(sys.argv) > 2 else 200000
PARTS = sys.argv[3] if len(sys.argv) > 3 else 'BC'

def kind(p):
    return rt.status(CELLS, p)

# ---------------------------------------------------------------- (A) direct billiard
def walls_at(p):
    """For a smooth boundary point: 'h' if the wall through p is horizontal, else 'v'."""
    x, y = p
    below = ((x - 1, y - 1) in CELLS, (x, y - 1) in CELLS)
    return 'h' if below in ((True, True), (False, False)) else 'v'

def trace(P, d, maxsteps=200000):
    """Interior lattice points visited (in order) from P in signed primitive direction d."""
    sx, sy = (1 if d[0] > 0 else -1), (1 if d[1] > 0 else -1)
    ax, ay = abs(d[0]), abs(d[1])
    start = (P, sx, sy)
    seen = []
    for _ in range(maxsteps):
        if ax == 0 or ay == 0:        # axis direction: unit steps along a grid line
            Q = (P[0] + (sx if ax else 0), P[1] + (sy if ay else 0))
        else:
            cx, cy = P[0] - (sx < 0), P[1] - (sy < 0)
            assert (cx, cy) in CELLS
            i = j = 1
            while i < ax or j < ay:      # merge crossing times i/ax (vertical) and j/ay (horizontal)
                if j >= ay or (i < ax and i * ay < j * ax):
                    if (cx + sx, cy) in CELLS: cx += sx
                    else: sx = -sx
                    i += 1
                else:
                    if (cx, cy + sy) in CELLS: cy += sy
                    else: sy = -sy
                    j += 1
            Q = (cx + (sx > 0), cy + (sy > 0))
        k = kind(Q)
        if k in ('convex', 'reflex'):
            return seen, 'stop'
        if k == 'smooth':
            if walls_at(Q) == 'h': sy = -sy
            else: sx = -sx
        else:
            seen.append(Q)
        P = Q
        if (P, sx, sy) == start:
            return seen, 'periodic'
    raise RuntimeError('no closure')

def lit_billiard(s, t, v):
    return any(t in trace(s, (ex * v[0], ey * v[1]))[0] for ex in (1, -1) for ey in (1, -1))

def directions(n):
    out = []
    for p in range(0, n + 1):
        for q in range(-n, n + 1):
            if gcd(p, q) == 1 and (p > 0 or q == 1):
                out.append((p, q))
    return out

def cls(v):
    return (v[0] % 2, v[1] % 2)

# ------------------------------------------------- (B) single-arc criterion, reference arcs
def power3(p):
    return rt.mul(rt.mul(p, p), p)

def criterion_reference(origin, pts):
    """Return {(s,t,partner_index): bool} for the reference arc a -> partner."""
    room, tup = rt.room_tuple(CELLS, origin)
    A = tup[0]
    marks = {p: {x for cy in rt.lifts(room, tup, p, origin) for x in cy} for p in pts}
    out = {}
    for idx in (1, 2, 3):
        L = rt.mul(power3(A), power3(tup[idx]))
        Lr = rt.mul(A, tup[idx])                       # relaxed control: corners not deleted
        for s, t in combinations(pts, 2):
            for name, M in (('legal', L), ('relaxed', Lr)):
                cur, hit = set(marks[s]), False
                for _ in range(len(A) + 1):
                    if cur & marks[t]:
                        hit = True; break
                    cur = {M[x] for x in cur}
                out[(s, t, idx, name)] = hit
    return out

print('== DB55: cells', len(CELLS), ' pair', S, T)
interior = [p for p in rt.lattice_points(CELLS) if kind(p) == 'interior']
ref_dirs = {1: [(1, 0)], 2: [(1, 1), (1, -1)], 3: [(0, 1)]}    # partner b, c, d
agree = disagree = relaxed_extra = 0
bad = []
for origin in (product(range(2), repeat=2) if 'B' in PARTS else []):
    pts = [p for p in interior if (p[0] % 2, p[1] % 2) == origin]
    crit = criterion_reference(origin, pts)
    for s, t in combinations(pts, 2):
        for idx, vs in ref_dirs.items():
            bil = [lit_billiard(s, t, v) for v in vs]
            c = crit[(s, t, idx, 'legal')]
            ok = c in bil if len(vs) > 1 else c == bil[0]
            agree += ok; disagree += not ok
            relaxed_extra += crit[(s, t, idx, 'relaxed')] and not c
            if not ok and len(bad) < 3: bad.append((origin, s, t, idx, c, bil))
print('(B) reference-arc criterion vs billiard over all same-parity interior pairs:',
      'agree', agree, 'disagree', disagree, bad)
print('    rows where the relaxed product A*X connects but L=A^3X^3 does not:', relaxed_extra)

# --------------------------------------------- (C) unfolding as labelled square-tiled surface
cl = sorted(CELLS)
ci = {c: k for k, c in enumerate(cl)}
COPIES = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
n = 4 * len(cl)
def sq(c, e): return 4 * ci[c] + COPIES.index(e)
r0, u0, lab_set, lab_pt = [0] * n, [0] * n, [0] * n, [0] * n
CODE = {'-': 0, 'X': 1, 'S': 2, 'T': 3}
for c in cl:
    for e in COPIES:
        i = sq(c, e)
        nx = (c[0] + e[0], c[1])
        r0[i] = sq(nx, e) if nx in CELLS else sq(c, (-e[0], e[1]))
        ny = (c[0], c[1] + e[1])
        u0[i] = sq(ny, e) if ny in CELLS else sq(c, (e[0], -e[1]))
        ll = (c[0] + (e[0] < 0), c[1] + (e[1] < 0))
        k = kind(ll)
        code = 'X' if k in ('convex', 'reflex') else 'S' if ll == S else 'T' if ll == T else '-'
        lab_set[i] = CODE[code]
        lab_pt[i] = CODE[code] if code in '-X' else 4 + 4 * (code == 'T') + COPIES.index(e)
assert sorted(r0) == list(range(n)) and sorted(u0) == list(range(n))

def inverse(p):
    q = [0] * len(p)
    for i, x in enumerate(p): q[x] = i
    return q

def shearT(O, k=1):          # derivative [[1,k],[0,1]]
    r, u, lab = O
    m = inverse(r) if k > 0 else list(r)
    rp = list(range(len(r)))
    for _ in range(abs(k)): rp = [m[x] for x in rp]
    return (r, [u[rp[i]] for i in range(len(r))], lab)

def shearV(O, k=1):          # derivative [[1,0],[k,1]]
    r, u, lab = O
    m = inverse(u) if k > 0 else list(u)
    up = list(range(len(u)))
    for _ in range(abs(k)): up = [m[x] for x in up]
    return ([r[up[i]] for i in range(len(r))], u, lab)

def minusI(O):
    r, u, lab = O
    return (inverse(r), inverse(u), [lab[u[r[i]]] for i in range(len(r))])

def canon(O, start_codes):
    r, u, lab = O
    best = None
    for s in range(len(r)):
        if lab[s] not in start_codes: continue
        order, pos = [s], {s: 0}
        k = 0
        while k < len(order):
            x = order[k]; k += 1
            for y in (r[x], u[x]):
                if y not in pos: pos[y] = len(order); order.append(y)
        if len(order) != len(r): raise RuntimeError('disconnected')
        form = (tuple(pos[r[x]] for x in order), tuple(pos[u[x]] for x in order),
                tuple(lab[x] for x in order))
        if best is None or form < best: best = form
    return best

def horiz_lit(O, scode, tcodes):
    r, u, lab = O
    for s in range(len(r)):
        if lab[s] not in scode: continue
        i = r[s]
        while i != s:
            if lab[i] in tcodes: return True
            if lab[i] == 1: break
            i = r[i]
    return False

def mat_mod2(M): return tuple(x % 2 for row in M for x in row)
def mmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]

def orbit(O, starts, track2):
    """BFS on SL(2,Z)-orbit of labelled surface; states (canon, g mod 2 if track2)."""
    G = {'T': [[1, 1], [0, 1]], 'V': [[1, 0], [1, 1]], 'm': [[-1, 0], [0, -1]]}
    first = (canon(O, starts), (1, 0, 0, 1) if track2 else None)
    index, edges, todo = {first: 0}, {}, [first]
    while todo:
        st = todo.pop()
        form, m2 = st
        Ox = (list(form[0]), list(form[1]), list(form[2]))
        for name, f in (('T', shearT), ('V', shearV), ('m', minusI)):
            img = f(Ox)
            M2 = None
            if track2:
                M = mmul(G[name], [[m2[0], m2[1]], [m2[2], m2[3]]])
                M2 = mat_mod2(M)
            new = (canon(img, starts), M2)
            if new not in index:
                index[new] = len(index); todo.append(new)
            edges[(index[st], name)] = index[new]
        if len(index) % 5000 == 0 and len(todo): print('      ...states', len(index), flush=True)
        if len(index) > LIMIT: raise RuntimeError('orbit too large (>%d states)' % LIMIT)
    # cusps = orbits of <T, -I> on states
    parent = list(range(len(index)))
    def find(a):
        while parent[a] != a: parent[a] = parent[parent[a]]; a = parent[a]
        return a
    for (i, name), j in edges.items():
        if name in 'Tm': parent[find(i)] = find(j)
    return index, find

def g_to_e1(v):
    p, q = v
    # extended Euclid a p + b q = 1
    def eg(x, y):
        if y == 0: return (1 if x > 0 else -1, 0)
        a, b = eg(y, x % y)
        return (b, a - (x // y) * b)
    a, b = eg(p, q)
    assert a * p + b * q == 1
    return [[a, b], [-q, p]]

def word(M):
    """Return list of ('T'|'V'|'m', k) with M = product in order (leftmost first)."""
    a, b, c, d = M[0][0], M[0][1], M[1][0], M[1][1]
    ops = []                         # left multiplications applied to reduce M
    while c != 0:
        if a == 0:
            a += c; b += d; ops.append(('T', 1))
        elif abs(c) >= abs(a):
            k = int(c / a); c -= k * a; d -= k * b; ops.append(('V', -k))
        else:
            k = int(a / c); a -= k * c; b -= k * d; ops.append(('T', -k))
    sign = 1 if a == 1 else -1
    a, b, d = a * sign, b * sign, d * sign
    assert a == 1 and d == 1
    ops.append(('T', -b))
    # ops_k...ops_1 * M = sign*I  =>  M = sign * ops_1^-1 ... ops_k^-1
    res = [(n_, -k) for n_, k in ops]
    if sign < 0: res.append(('m', 1))
    return res

def act(M, O):
    for name, k in reversed(word(M)):
        if k == 0: continue
        O = shearT(O, k) if name == 'T' else shearV(O, k) if name == 'V' else minusI(O)
    return O

O_set = (r0, u0, lab_set)
O_pt = (r0, u0, lab_pt)
# sanity: word() reproduces matrices
for v in [(3, 5), (2, -7), (0, 1), (1, 0), (5, 3)]:
    M = g_to_e1(v); P = [[1, 0], [0, 1]]
    for name, k in word(M):
        G = {'T': [[1, k], [0, 1]], 'V': [[1, 0], [k, 1]], 'm': [[-1, 0], [0, -1]]}[name]
        P = mmul(P, G)
    assert P == M, (v, P, M)

t1 = time.process_time()
if 'O' in PARTS:     # bounded attempt at the full orbit (index of H cap Gamma(2))
    try:
        idx_set, find_set = orbit(O_set, {2}, True)
        print('    [SL2Z : H cap Gamma(2)] =', len(idx_set))
    except RuntimeError as e:
        print('(C) full orbit of (labelled surface, g mod 2):', e, ' cpu %.1fs' % (time.process_time() - t1))

def cusp_label(v, maxw=5000):
    """Orbit of (g.O, g mod 2) under <T,-I>: equal labels <=> same cusp of H cap Gamma(2)."""
    M = g_to_e1(v)
    img = act(M, O_set)
    m2 = mat_mod2(M)
    forms, cur, cm = [], img, m2
    first = (canon(img, {2}), m2)
    for w in range(1, maxw):
        cur = shearT(cur)
        cm = mat_mod2(mmul([[1, 1], [0, 1]], [[cm[0], cm[1]], [cm[2], cm[3]]]))
        st = (canon(cur, {2}), cm)
        forms.append(st)
        if st == first: break
    else:
        raise RuntimeError('width > maxw')
    neg = minusI(img)
    negst = (canon(neg, {2}), m2)
    assert negst in forms or True
    return min(forms), w, negst in forms, img

dirs = directions(N)
rows, mismatch_flow, widths, negin = [], 0, [], 0
for v in dirs:
    lab, w, ni, img = cusp_label(v)
    b = lit_billiard(S, T, v)
    f = horiz_lit(img, {2}, {3})
    mismatch_flow += (b != f)
    widths.append(w); negin += ni
    rows.append((v, cls(v), lab, b))
print('(A vs C) directions with max(|p|,|q|) <=', N, ':', len(dirs),
      '| billiard vs horizontal flow on g.O mismatches:', mismatch_flow,
      '| -I in H (deck rotation) for', negin, 'of', len(dirs), ' cpu %.1fs' % (time.process_time() - t1))
print('    cusp widths (with g mod 2): min', min(widths), 'max', max(widths))
by_cusp = {}
for v, c, lab, b in rows: by_cusp.setdefault(lab, []).append((v, b))
multi = {k: L for k, L in by_cusp.items() if len(L) > 1}
nonconst = [k for k, L in by_cusp.items() if len({b for _, b in L}) > 1]
print('    distinct cusps of H cap Gamma(2) met:', len(by_cusp), '| cusps met by >=2 directions:', len(multi),
      '| cusps with non-constant lit status:', len(nonconst))
print('    multi-direction cusps that are lit (all members lit):', sum(all(b for _, b in L) for L in multi.values()))
for L in sorted(multi.values(), key=lambda L: (not L[0][1], L))[:6]:
    print('      same cusp:', [x[0] for x in L], 'lit', [x[1] for x in L])
for c in sorted({r[1] for r in rows}):
    sub = [r for r in rows if r[1] == c]
    labs = {r[2] for r in sub}
    lit = sorted((r[0] for r in sub if r[3]), key=lambda v: (max(map(abs, v)), v))
    print('    class', c, ': directions', len(sub), '| distinct cusps', len(labs),
          '| lit directions', len(lit), '| lit cusps', len({r[2] for r in sub if r[3]}), '| first lit', lit[:5])
print('cpu total %.1fs' % (time.process_time() - T0))
