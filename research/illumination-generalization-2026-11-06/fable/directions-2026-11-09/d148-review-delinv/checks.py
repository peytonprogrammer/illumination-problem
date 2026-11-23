"""Independent checks for deletion-invariance.2026-11-22-0040.md (d148 review).

Physical side: an exact lattice billiard tracer written here (cells only, no cover).
Algebraic side: monodromy tuples from roomtools.room_tuple (shared infrastructure),
but pencil connectivity recomputed here by union-find / <U,V> orbits, not by the
note's pencil_components.  Named rooms only.  Run: python3 -B checks.py
"""
import sys, time
from collections import Counter
from itertools import product, combinations
from math import gcd, lcm
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'd10-mechanisms'))
import roomtools as rt  # noqa: E402

T0 = time.process_time()

# ---------------------------------------------------------------- rooms (copied from the note's checker)
def rect(a, b, c, d):
    return set(product(range(a, b), range(c, d)))

def stretch(cells, axis, at, extra):
    out = set()
    for p in cells:
        k = p[axis]
        for s in (range(extra + 1) if k == at else [extra if k > at else 0]):
            q = list(p); q[axis] += s; out.add(tuple(q))
    return out

_cols = [range(6), (2, 3), (2, 3), range(6), range(6), (2, 3), (2,), range(3)]
_cov = {(x, y) for x, col in enumerate(_cols) for y in col}
ROOMS = {
    'DB55': rect(0, 5, 0, 5) | rect(5, 8, 2, 3) | rect(8, 13, 0, 5),
    'DBas': rect(0, 5, 0, 4) | rect(5, 9, 1, 2) | rect(9, 13, -1, 5),
    'c4181s': stretch(stretch(_cov, 0, 1, 2), 1, 4, 3),
    'U2': rect(0, 9, 0, 2) | rect(0, 2, 2, 9) | rect(7, 9, 2, 7) | rect(5, 7, 5, 7),
}

# ---------------------------------------------------------------- physical tracer
def ncells(cells, p):
    x, y = p
    return sum(c in cells for c in ((x-1, y-1), (x, y-1), (x-1, y), (x, y)))

CORNER = (1, 3)  # convex, reflex

def pattern(p, q):
    p, q = abs(p), abs(q)
    ev = [(k / p, 'V') for k in range(1, p)] + [(l / q, 'H') for l in range(1, q)]
    return [c for _, c in sorted(ev)]

def trace(cells, S, dx, dy, p, q, full=False):
    """Lattice points hit by the ray from S heading (dx|p|, dy|q|); stops at a corner or on
    return to an earlier state.  If full, also return the blocking corner (or None)."""
    out = []
    if p == 0 or q == 0:
        horiz = q == 0
        P, d, seen = S, (dx if horiz else dy), set()
        while True:
            for _ in range(2):
                n = (P[0]+d, P[1]) if horiz else (P[0], P[1]+d)
                lo = min(P[0], n[0]) if horiz else min(P[1], n[1])
                e = [(lo, P[1]), (lo, P[1]-1)] if horiz else [(P[0], lo), (P[0]-1, lo)]
                if any(c in cells for c in e):
                    break
                d = -d
            P = n
            if ncells(cells, P) in CORNER:
                return (out, P) if full else out
            out.append(P)
            if (P, d) in seen:
                return (out, None) if full else out
            seen.add((P, d))
    pat = pattern(p, q)
    cell = (S[0] - (dx < 0), S[1] - (dy < 0))
    assert cell in cells
    seen = set()
    while True:
        for c in pat:
            if c == 'V':
                nb = (cell[0]+dx, cell[1])
                if nb in cells: cell = nb
                else: dx = -dx
            else:
                nb = (cell[0], cell[1]+dy)
                if nb in cells: cell = nb
                else: dy = -dy
        P = (cell[0] + (dx > 0), cell[1] + (dy > 0))
        if ncells(cells, P) in CORNER:
            return (out, P) if full else out
        out.append(P)
        if (cell[0]+dx, cell[1]+dy) in cells: cell = (cell[0]+dx, cell[1]+dy)
        elif (cell[0]+dx, cell[1]) in cells: cell, dy = (cell[0]+dx, cell[1]), -dy
        elif (cell[0], cell[1]+dy) in cells: cell, dx = (cell[0], cell[1]+dy), -dx
        else: raise RuntimeError(P)
        if (cell, dx, dy) in seen:
            return (out, None) if full else out
        seen.add((cell, dx, dy))

_line_cache = {}
def lit_line(name, S, p, q):
    """Points legally reached along the full line through S with direction (p,q)."""
    key = (name, S, p, q)
    if key not in _line_cache:
        cells = ROOMS[name]
        sx, sy = (1 if p >= 0 else -1), (1 if q >= 0 else -1)
        _line_cache[key] = set(trace(cells, S, sx, sy, p, q)) | set(trace(cells, S, -sx, -sy, p, q))
    return _line_cache[key]

def klass(p, q):
    return {(1, 0): 1, (1, 1): 2, (0, 1): 3}[(p % 2, q % 2)]  # 1=b horizontal, 2=c diagonal, 3=d vertical

def interior_pts(cells, origin):
    return sorted(x for x in rt.lattice_points(cells) if ncells(cells, x) == 4
                  and (x[0] % 2, x[1] % 2) == origin)

# ---------------------------------------------------------------- algebra: own pencil evaluation
def power(h, j):
    r = list(range(len(h)))
    for _ in range(j):
        r = [h[k] for k in r]
    return r

def cyc_len(perm):
    return {x: len(c) for c in rt.cycles(perm) for x in c}

def orbit_hits(gens, I, J):
    seen, todo = set(I), list(I)
    while todo:
        x = todo.pop()
        for g in gens:
            y = g[x]
            if y not in seen:
                seen.add(y); todo.append(y)
    return bool(seen & J)

def arc_gens(A, D, hj, regular):
    """Sheet i lies over the A-cycle of i and the D-cycle of hj[i].
    regular: U=A^3, V=hj^-1 D^3 hj (swap only across 2-cycles); else full A and hj^-1 D hj."""
    n = len(A)
    hinv = [0]*n
    for i, x in enumerate(hj): hinv[x] = i
    LA, LD = cyc_len(A), cyc_len(D)
    if regular:
        U = [A[i] if LA[i] == 2 else i for i in range(n)]
        V = [hinv[D[hj[i]]] if LD[hj[i]] == 2 else i for i in range(n)]
    else:
        U = list(A)
        V = [hinv[D[hj[i]]] for i in range(n)]
    return U, V

PENCILS = {1: [(1, 2)], 2: [(1, 2), (2, 3)], 3: [(2, 3)]}

def pencil_direction(d, pen, m):
    """Physical direction for twist power m of class d's reference arc.  Found empirically: among
    (1,2m),(1,4m),(1,1+-2m),(1+-2m,1),(2m,1),(4m,1) only these give zero mismatches in part 3."""
    if d == 1: return (1, 2*m)
    if d == 3: return (2*m, 1)
    return (1, 1 - 2*m) if pen == (1, 2) else (1 + 2*m, 1)

class Setup:
    def __init__(self, name, origin):
        self.cells = ROOMS[name]
        self.room, self.t = rt.room_tuple(self.cells, origin)
        self.pts = interior_pts(self.cells, origin)
        self.sheets = {x: set(s for l in rt.lifts(self.room, self.t, x, origin) for s in l)
                       for x in self.pts}
        self.h = {pen: rt.mul(self.t[pen[0]], self.t[pen[1]]) for pen in ((1, 2), (2, 3))}
        self.order = {pen: lcm(*map(len, rt.cycles(h))) for pen, h in self.h.items()}
        self._g = {}

    def gens(self, d, pen, j, regular):
        key = (d, pen, j % self.order[pen], regular)
        if key not in self._g:
            hj = power(self.h[pen], key[2])
            self._g[key] = arc_gens(self.t[0], self.t[d], hj, regular)
        return self._g[key]

    def connected(self, d, pen, j, S, T, regular):
        return orbit_hits(self.gens(d, pen, j, regular), self.sheets[S], self.sheets[T])

log = []
def out(*a):
    s = ' '.join(str(x) for x in a)
    print(s); log.append(s)

# ================================================================ 0. rooms
out('== 0. named rooms')
for name, cells in ROOMS.items():
    L = rt.ledger(cells)
    out(name, 'strictly simple', rt.is_strictly_simple(cells), 'walls', L['W'], 'reflex', L['r'],
        'cells', len(cells), 'same-parity interior pairs',
        sum(len(interior_pts(cells, o))*(len(interior_pts(cells, o))-1)//2 for o in product(range(2), repeat=2)))

# ================================================================ 1. DB55 counterexample
out('\n== 1. DB55, S=(2,2), T=(10,2), horizontal class')
S, T = (2, 2), (10, 2)
st = Setup('DB55', (0, 0))
pen = (1, 2)
out('order of h=g_b g_c:', st.order[pen], 'cycle lengths', sorted(map(len, rt.cycles(st.h[pen]))))
relaxed = [int(st.connected(1, pen, j, S, T, False)) for j in range(5)]
legal = [int(st.connected(1, pen, j, S, T, True)) for j in range(5)]
out('relaxed by residue', relaxed, ' legal by residue', legal)
assert relaxed == [1, 1, 0, 0, 1] and legal == [0]*5
# per lift pair
lifts = {x: [set(l) for l in rt.lifts(st.room, st.t, x, (0, 0))] for x in (S, T)}
per = [[int(orbit_hits(st.gens(1, pen, j, True), I, J)) for I in lifts[S] for J in lifts[T]] for j in range(5)]
out('legal per (residue, lift pair):', per)
seg, block = trace(ROOMS['DB55'], S, 1, 1, 1, 0, full=True)
out('residue-0 ray (1,0) from S: hits', seg, 'blocked at', block, 'status', ncells(ROOMS['DB55'], block),
    '| (8,2) status', ncells(ROOMS['DB55'], (8, 2)))
pm = [m for m in range(-60, 61) if T in lit_line('DB55', S, 1, 2*m) or T in lit_line('DB55', S, -1, 2*m)]
out('pencil lines (+-1, 2m), |m|<=60, reaching T:', pm)
B = 25
wit = Counter(); first = {}
for p in range(0, B+1):
    for q in range(-B, B+1):
        if gcd(p, q) != 1 or (p == 0 and q < 0): continue
        if T in lit_line('DB55', S, p, q):
            k = klass(p, q); wit[k] += 1
            if k not in first or abs(p)+abs(q) < sum(map(abs, first[k])): first[k] = (p, q)
out(f'all primitive directions |p|,|q|<={B}: lines reaching T per class', dict(wit), 'shortest', first)
zero = {v: T in lit_line('DB55', S, *v) for v in ((1, 0), (1, 1), (1, -1), (0, 1))}
out('zero-power reference lines (both diagonals for class c) reaching T:', zero)
st0 = Setup('DB55', (0, 0))
prods = [rt.mul(st0.t[i], st0.t[j]) for i, j in combinations((1, 2, 3), 2)]
orb, todo = {0}, [0]
while todo:
    x = todo.pop()
    for g in prods:
        if g[x] not in orb: orb.add(g[x]); todo.append(g[x])
out('orbit of sheet 0 under BC, BD, CD (even/even marking):', len(orb), '/', len(st0.t[0]))
path = trace(ROOMS['DB55'], S, 1, 1, 3, 2)
out('direction (3,2) from S, lattice points up to T:', path[:path.index(T)+1] if T in path else path)

# ================================================================ 3. single-arc test vs physics
out('\n== 3. <U,V> orbit test vs physical rays, all rooms, all pencils')
agree = Counter(); mism = []; nres = 0
for name in ROOMS:
    for origin in product(range(2), repeat=2):
        st = Setup(name, origin)
        for d, pens in PENCILS.items():
            for pen in pens:
                n = st.order[pen]
                for m in range(-(n//2), n - n//2):   # every residue, smallest slope representative
                    nres += 1
                    p, q = pencil_direction(d, pen, m)
                    for S_, T_ in combinations(st.pts, 2):
                        alg = st.connected(d, pen, m, S_, T_, True)
                        ph = T_ in lit_line(name, S_, p, q) or T_ in lit_line(name, S_, -p, q)
                        agree[(name, alg == ph)] += 1
                        if alg != ph and len(mism) < 5: mism.append((name, origin, d, pen, m, S_, T_, alg, ph))
out('agreement counts (room, agree):', dict(agree), '| residue slices tested:', nres, '(all residues)')
out('first mismatches:', mism)

out('\n== 3b. component bound: #<U,V> orbits - #<A,D_j> orbits <= 2(z_a+z_d), all slices')
def norbits(gens, n):
    seen, k = set(), 0
    for s0 in range(n):
        if s0 in seen: continue
        k += 1; todo = [s0]; seen.add(s0)
        while todo:
            x = todo.pop()
            for g in gens:
                if g[x] not in seen: seen.add(g[x]); todo.append(g[x])
    return k
worst = Counter(); viol = 0; tight = 0; total = 0
for name in ROOMS:
    for origin in product(range(2), repeat=2):
        st = Setup(name, origin)
        nsh = len(st.t[0])
        z = [sum(len(c) == 3 for c in rt.cycles(g)) for g in st.t]
        for d, pens in PENCILS.items():
            for pen in pens:
                for j in range(st.order[pen]):
                    inc = norbits(st.gens(d, pen, j, True), nsh) - norbits(st.gens(d, pen, j, False), nsh)
                    bound = 2*(z[0] + z[d]); total += 1
                    viol += inc > bound; tight += inc == bound
                    worst[name] = max(worst[name], inc / bound if bound else 0)
out('slices', total, 'violations', viol, 'tight', tight, 'max increase/bound by room', {k: round(v, 3) for k, v in worst.items()})

# ================================================================ 2 + 4. row table and physical witnesses
out('cycle lengths over sites, all rooms/origins:', sorted({len(c) for nm in ROOMS for o in product(range(2), repeat=2)
    for g in rt.room_tuple(ROOMS[nm], o)[1] for c in rt.cycles(g)}))
out('\n== 2. row table (own algebra) and physical class witnesses')
BW = 15
for name in ROOMS:
    tot = Counter(); pairs_classes = Counter(); phys_classes = Counter()
    lost_phys = Counter(); notelegal_unconfirmed = 0; fallback = 0
    for origin in product(range(2), repeat=2):
        st = Setup(name, origin)
        dirs = [(p, q) for p in range(0, BW+1) for q in range(-BW, BW+1)
                if gcd(p, q) == 1 and not (p == 0 and q < 0)]
        dirs.sort(key=lambda v: abs(v[0]) + abs(v[1]))
        phys = {}  # (S,T) -> set of classes with a physical witness
        for S_ in st.pts:
            for v in dirs:
                for T_ in lit_line(name, S_, *v):
                    if T_ in st.sheets and T_ != S_:
                        phys.setdefault(tuple(sorted((S_, T_))), set()).add(klass(*v))
        for S_, T_ in combinations(st.pts, 2):
            ncls = 0
            for d, pens in PENCILS.items():
                rel = any(st.connected(d, pn, j, S_, T_, False) for pn in pens for j in range(st.order[pn]))
                leg_j = [(pn, j) for pn in pens for j in range(st.order[pn]) if st.connected(d, pn, j, S_, T_, True)]
                key = 'legal' if leg_j else 'lost' if rel else 'absent'
                tot[key] += 1
                ncls += bool(leg_j)
                has = d in phys.get((S_, T_), set())
                if leg_j and not has:
                    # confirm the note's legal row on the cheapest residue physically
                    pn, j = min(leg_j, key=lambda x: min(x[1], st.order[x[0]] - x[1]))
                    m = j if j <= st.order[pn] // 2 else j - st.order[pn]
                    p, q = pencil_direction(d, pn, m)
                    if T_ in lit_line(name, S_, p, q) or T_ in lit_line(name, S_, -p, q):
                        has = True; fallback += 1
                    else:
                        notelegal_unconfirmed += 1
                if has: phys_classes[(S_, T_)] += 1
                if key != 'legal': lost_phys[(key, has)] += 1
            pairs_classes[ncls] += 1
    nphys = Counter(phys_classes[k] for k in phys_classes)
    out(name, 'rows', dict(tot), '| pairs by #pencil-legal classes', dict(pairs_classes))
    out('   physical classes per pair (|p|,|q|<=%d, plus pencil residues):' % BW, dict(nphys),
        '| pairs with no physical class:', sum(pairs_classes.values()) - len(phys_classes))
    out('   non-legal rows (kind, physically lit in that class by another arc):', dict(lost_phys),
        '| note-legal rows not confirmed physically:', notelegal_unconfirmed,
        '| rows needing the pencil-slope fallback:', fallback)

out('\nCPU seconds', round(time.process_time() - T0, 1))
(HERE / 'checks.log').write_text('\n'.join(log) + '\n')
