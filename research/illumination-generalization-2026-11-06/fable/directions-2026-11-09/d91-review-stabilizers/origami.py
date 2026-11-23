"""Independent check of axial-stabilizers.md and stabilizer-orbits.md (D91).

The room double Q of an integer orthogonal room is handled through its
orientation cover M (the four-copy unfolding), built as an origami (r, u)
on unit squares. Q = M / sigma, sigma the deck involution (derivative -I).
Convex-corner lifts are regular on M and are kept as marked points.

For gamma in SL(2,Z) the origami gamma.M is built by elementary shears that
keep the label of every square's lower-left vertex, so the affine map
M -> gamma.M sends LL(q) to LL(q). An element of the full stabilizer of the
direction gamma^{-1}(1,0) is then a permutation phi with
    phi o r' = r o phi,  phi o u'' = u o phi,
where (r', u'') = T^lam . (gamma.M); its vertex action is LL(q) -> LL(phi q).
Only maps commuting with sigma and preserving the marked set descend to G.
All arithmetic is on integers and permutations.
"""
import sys
from math import gcd
from itertools import product


def lcm(a, b):
    return a * b // gcd(a, b)


# ---------------------------------------------------------------- rooms
def cross_cells(b):
    cells = set()
    for i in range(-b, b):
        for j in range(-2, 2):
            cells.add((i, j))
            cells.add((j, i))
    return cells


def staircase_cells(m):
    bands = [((0, m), (0, m)), ((m, m + 1), (m - 1, m + 2)),
             ((m + 1, m + 2), (m, m + 3)), ((m + 2, 2 * m + 2), (m + 2, 2 * m + 2))]
    cells = set()
    for (y0, y1), (x0, x1) in bands:
        for j in range(y0, y1):
            for i in range(x0, x1):
                cells.add((i, j))
    return cells


# ---------------------------------------------------------------- surface
class Surface:
    def __init__(self, cells):
        self.cells = cells
        copies = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        self.sq = [(c, x) for c in copies for x in sorted(cells)]
        self.idx = {s: k for k, s in enumerate(self.sq)}
        N = len(self.sq)
        r = [0] * N
        u = [0] * N
        for k, ((e1, e2), (i, j)) in enumerate(self.sq):
            nb = (i + e1, j)
            r[k] = self.idx[((e1, e2), nb)] if nb in cells else self.idx[((-e1, e2), (i, j))]
            nb = (i, j + e2)
            u[k] = self.idx[((e1, e2), nb)] if nb in cells else self.idx[((e1, -e2), (i, j))]
        self.r, self.u, self.N = r, u, N
        # vertex labels
        self.vtype = {}
        self.LL = [self.vlabel(c, (i if c[0] > 0 else i + 1, j if c[1] > 0 else j + 1))
                   for (c, (i, j)) in self.sq]
        self.verts = sorted(set(self.LL))
        self.marked = {v for v in self.verts if self.vtype[v[0]] in ('convex', 'reflex')}

    def ptype(self, p):
        x, y = p
        sw, se, nw, ne = [(c in self.cells) for c in
                          ((x - 1, y - 1), (x, y - 1), (x - 1, y), (x, y))]
        k = sw + se + nw + ne
        if k == 4:
            return 'int'
        if k == 3:
            return 'reflex'
        if k == 1:
            return 'convex'
        assert k == 2
        if (nw and ne) or (sw and se):
            return 'hwall'
        assert (ne and se) or (nw and sw), 'pinch'
        return 'vwall'

    def vlabel(self, c, p):
        t = self.ptype(p)
        self.vtype[p] = t
        key = {'int': c, 'hwall': (c[0],), 'vwall': (c[1],)}.get(t, ())
        return (p, key)

    @staticmethod
    def sigma(v):
        p, key = v
        return (p, tuple(-e for e in key))

    def qpoint(self, v):
        return min(v, self.sigma(v))


def inv(p):
    q = [0] * len(p)
    for i, x in enumerate(p):
        q[x] = i
    return q


def compose(a, b):  # a o b
    return [a[x] for x in b]


def power(p, k):
    if k < 0:
        p, k = inv(p), -k
    res = list(range(len(p)))
    base = p
    while k:
        if k & 1:
            res = compose(base, res)
        base = compose(base, base)
        k >>= 1
    return res


def shearT(r, u, k):  # derivative [[1,k],[0,1]]; labels = bottom edges
    return r, compose(u, power(r, -k))


def shearV(r, u, k):  # derivative [[1,0],[k,1]]; labels = left edges
    return compose(r, power(u, -k)), u


def to_horizontal(p, q):
    """Word of (kind, k) with gamma (p,q) = (+-1, 0)."""
    word = []
    while q != 0:
        if p != 0:
            k = -(p // q) if abs(p) >= abs(q) else 0
            if k:
                word.append(('T', k))
                p = p + k * q
        if p == 0:
            # (0,q) with q=+-1 ; V^0 no help: use T^1 then V
            word.append(('T', 1))
            p = q
        k = -(q // p)
        word.append(('V', k))
        q = q + k * p
    assert abs(p) == 1
    return word


def apply_word(r, u, word):
    for kind, k in word:
        r, u = (shearT if kind == 'T' else shearV)(r, u, k)
    return r, u


def isomorphisms(r1, u1, r2, u2):
    """All phi with phi o r1 = r2 o phi and phi o u1 = u2 o phi."""
    N = len(r1)
    out = []
    for start in range(N):
        phi = [-1] * N
        phi[0] = start
        stack = [0]
        ok = True
        while stack and ok:
            x = stack.pop()
            for a, b in ((r1, r2), (u1, u2)):
                y, z = a[x], b[phi[x]]
                if phi[y] == -1:
                    phi[y] = z
                    stack.append(y)
                elif phi[y] != z:
                    ok = False
                    break
        if ok and -1 not in phi and len(set(phi)) == N:
            out.append(phi)
    return out


def descend(S, phi):
    """Vertex map of phi; None unless well defined, mark-preserving, sigma-commuting."""
    vm = {}
    for q in range(S.N):
        a, b = S.LL[q], S.LL[phi[q]]
        if vm.setdefault(a, b) != b:
            raise AssertionError('vertex map not well defined (convention error)')
    if len(set(vm.values())) != len(vm):
        raise AssertionError('vertex map not injective')
    for v, w in vm.items():
        if (v in S.marked) != (w in S.marked):
            return None
        if vm[S.sigma(v)] != S.sigma(w):
            return None
    return vm


def cylinders(S, r, u):
    """Horizontal cylinders of the origami (r,u): list of (circumference, height, rows)."""
    sing = {v for v in S.verts if v in S.marked}
    rowid = [-1] * S.N
    rows = []
    for q in range(S.N):
        if rowid[q] == -1:
            row, x = [], q
            while rowid[x] == -1:
                rowid[x] = len(rows)
                row.append(x)
                x = r[x]
            rows.append(row)
    # a row's bottom is singular if any LL vertex on it is singular
    bot_sing = [any(S.LL[q] in sing for q in row) for row in rows]
    above = [rowid[u[row[0]]] for row in rows]
    cyls = []
    for k, row in enumerate(rows):
        if not bot_sing[k]:
            continue
        h, j = 1, above[k]
        while not bot_sing[j]:
            h += 1
            j = above[j]
        cyls.append((len(row), h, k))
    assert sum(c * h for c, h, _ in cyls) == S.N
    return cyls


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def direction_stabilizer(S, word, autos):
    """Q-permutations generating the full stabilizer of the direction sent to horizontal."""
    r, u = apply_word(S.r, S.u, word)
    cyl = cylinders(S, r, u)
    lam_mt = 1
    for c, h, _ in cyl:
        lam_mt = lcm(lam_mt, c // gcd(c, h))
    found = None
    for d in divisors(lam_mt):
        r2, u2 = shearT(r, u, d)
        maps = [vm for phi in isomorphisms(r2, u2, r, u)
                for vm in [descend(S, phi)] if vm is not None]
        if maps:
            found = (d, maps)
            break
    assert found is not None, 'multitwist missing'
    return cyl, lam_mt, found


def qperm(S, vm, qpts, qidx):
    return [qidx[S.qpoint(vm[v])] for v in qpts]


def orbits(n, gens):
    parent = list(range(n))

    def f(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for g in gens:
        for i in range(n):
            a, b = f(i), f(g[i])
            if a != b:
                parent[a] = b
    out = {}
    for i in range(n):
        out.setdefault(f(i), set()).add(i)
    return list(out.values())


def stabilizer_gens(n, gens, s):
    """Schreier generators of the point stabilizer of s."""
    trans = {s: list(range(n))}
    queue = [s]
    while queue:
        x = queue.pop()
        for g in gens:
            y = g[x]
            if y not in trans:
                trans[y] = compose(g, trans[x])
                queue.append(y)
    sg = []
    for x, tx in trans.items():
        for g in gens:
            y = g[x]
            h = compose(inv(trans[y]), compose(g, tx))
            assert h[s] == s
            if h != list(range(n)):
                sg.append(h)
    return sg, len(trans)


def dedupe(perms):
    seen, out = set(), []
    for p in perms:
        t = tuple(p)
        if t not in seen:
            seen.add(t)
            out.append(p)
    return out


# ---------------------------------------------------------------- full Veech group
def sigma_squares(S):
    return [S.idx[((-c[0], -c[1]), x)] for (c, x) in S.sq]


def stepT(state, k):
    r, u, sg = state
    rk = power(r, k)
    return r, compose(u, power(r, -k)), compose(rk, sg)


def stepV(state, k):
    r, u, sg = state
    uk = power(u, k)
    return compose(r, power(u, -k)), u, compose(uk, sg)


def canon(state, mk, starts):
    r, u, sg = state
    N = len(r)
    best, bestlab = None, None
    for s0 in starts:
        lab = [-1] * N
        order = [s0]
        lab[s0] = 0
        i = 0
        while i < len(order):
            x = order[i]
            i += 1
            for y in (r[x], u[x]):
                if lab[y] == -1:
                    lab[y] = len(order)
                    order.append(y)
        if len(order) != N:
            raise AssertionError('disconnected')
        key = (tuple(lab[r[x]] for x in order), tuple(lab[u[x]] for x in order),
               tuple(lab[sg[x]] for x in order), tuple(mk[x] for x in order))
        if best is None or key < best:
            best, bestlab = key, lab
    return best, bestlab


def full_affine_group(S, max_index=20000):
    """Q-Veech group orbit in SL(2,Z) and lifts of its Schreier generators.

    Returns (index, list of vertex maps)."""
    sg = sigma_squares(S)
    for q in range(S.N):  # sigma reverses r and u
        assert sg[S.r[sg[q]]] == inv(S.r)[q] and sg[S.u[sg[q]]] == inv(S.u)[q]
    mk = [1 if S.vtype[S.LL[q][0]] == 'convex' else 0 for q in range(S.N)]
    starts = [q for q in range(S.N) if mk[q]]
    st0 = (S.r, S.u, sg)
    k0, lab0 = canon(st0, mk, starts)
    states = [(st0, lab0)]
    index = {k0: 0}
    edges = []
    i = 0
    while i < len(states):
        st, lab = states[i]
        for step in (stepT, stepV):
            nst = step(st, 1)
            key, nlab = canon(nst, mk, starts)
            if key not in index:
                index[key] = len(states)
                states.append((nst, nlab))
                assert len(states) <= max_index
            j = index[key]
            jlab = states[j][1]
            # psi: nst -> states[j]: psi = jlab^{-1} o nlab
            jinv = inv(jlab)
            psi = [jinv[nlab[q]] for q in range(S.N)]
            edges.append(psi)
        i += 1
    maps = []
    for psi in edges:
        vm = descend(S, psi)
        assert vm is not None
        maps.append(vm)
    return len(states), maps
