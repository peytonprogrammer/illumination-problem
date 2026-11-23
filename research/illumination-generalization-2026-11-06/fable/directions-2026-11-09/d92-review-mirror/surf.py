"""Square-tiled model of the 4-copy unfolding M of a lattice room, and the
full affine group of the corner-marked room double Q = M / tau.

Independent implementation for the d92 review. Exact integer arithmetic only.

Labels: squares (sheet, cell), sheet = (e1, e2) in {+1,-1}^2.
h[k] = right neighbour, v[k] = top neighbour (developed coordinates).
tau = deck map with derivative -I: (e, c) -> (-e, c).
Vertices: classes of square corners. A structure in the SL(2,Z) orbit of M is
(h, v, tau, p) where p[k] is the M-vertex at the bottom-left corner of label k.
"""
from array import array
from collections import deque

SHEETS = [(1, 1), (1, -1), (-1, 1), (-1, -1)]


class Room:
    def __init__(self, cells):
        self.cells = set(map(tuple, cells))
        labels = [(e, c) for e in SHEETS for c in sorted(self.cells)]
        self.labels = labels
        idx = {l: i for i, l in enumerate(labels)}
        N = len(labels)
        h = [0] * N
        v = [0] * N
        tau = [0] * N
        for i, ((e1, e2), (x, y)) in enumerate(labels):
            nx = (x + e1, y)
            h[i] = idx[((e1, e2), nx)] if nx in self.cells else idx[((-e1, e2), (x, y))]
            ny = (x, y + e2)
            v[i] = idx[((e1, e2), ny)] if ny in self.cells else idx[((e1, -e2), (x, y))]
            tau[i] = idx[((-e1, -e2), (x, y))]
        self.N, self.h, self.v, self.tau = N, h, v, tau
        # corners: 0 BL, 1 BR, 2 TL, 3 TR
        par = list(range(4 * N))

        def f(a):
            while par[a] != a:
                par[a] = par[par[a]]
                a = par[a]
            return a

        def u(a, b):
            a, b = f(a), f(b)
            if a != b:
                par[a] = b
        for k in range(N):
            u(4 * k + 1, 4 * h[k] + 0)
            u(4 * k + 3, 4 * h[k] + 2)
            u(4 * k + 2, 4 * v[k] + 0)
            u(4 * k + 3, 4 * v[k] + 1)
        roots = {}
        corner = [0] * (4 * N)
        for a in range(4 * N):
            corner[a] = roots.setdefault(f(a), len(roots))
        self.V = len(roots)
        self.corner = corner  # corner[4k+c] -> vertex id
        # physical position and sheets of each vertex
        self.vphys = [None] * self.V
        self.key = {}  # (sheet, P) -> vertex
        self.vsheets = [set() for _ in range(self.V)]
        for k, ((e1, e2), (x, y)) in enumerate(labels):
            for c, (dx, dy) in enumerate([(0, 0), (1, 0), (0, 1), (1, 1)]):
                # developed corner offset (dx,dy) -> physical
                px = x + (dx if e1 == 1 else 1 - dx)
                py = y + (dy if e2 == 1 else 1 - dy)
                w = corner[4 * k + c]
                assert self.vphys[w] in (None, (px, py))
                self.vphys[w] = (px, py)
                self.key[((e1, e2), (px, py))] = w
                self.vsheets[w].add((e1, e2))
        # corner type of physical lattice points
        def ncell(P):
            X, Y = P
            return sum((X - a, Y - b) in self.cells for a in (0, 1) for b in (0, 1))
        self.ncell = ncell
        self.convex = [ncell(self.vphys[w]) == 1 for w in range(self.V)]
        self.reflex = [ncell(self.vphys[w]) == 3 for w in range(self.V)]
        # square-corner multiplicity = 4 * (cone angle / 2pi)
        mult = [0] * self.V
        for a in range(4 * N):
            mult[corner[a]] += 1
        self.mult = mult
        self.forbidden = [self.convex[w] or mult[w] != 4 for w in range(self.V)]
        for w in range(self.V):
            assert (mult[w] == 12) == self.reflex[w]
            assert not (self.convex[w] and mult[w] != 4)
        self.p0 = [corner[4 * k] for k in range(N)]
        self.blsq = {}
        for k in range(N):
            if mult[self.p0[k]] == 4:
                self.blsq[self.p0[k]] = k
        self.hinv = inv(h)
        self.vinv = inv(v)
        # vertex-level tau
        self.vtau = [None] * self.V
        for (e, P), w in self.key.items():
            self.vtau[w] = self.key[((-e[0], -e[1]), P)]
        # physical mirror iota on M vertices: (e1,e2) -> (e1,-e2); descends to Q
        self.viota = [None] * self.V
        for (e, P), w in self.key.items():
            self.viota[w] = self.key[((e[0], -e[1]), P)]

    def vert(self, sheet, P):
        return self.key[(tuple(sheet), tuple(P))]

    def qclass(self, w):
        return min(w, self.vtau[w])

    # ---- straight segments on M from a regular vertex ----
    def step(self, w, a, b):
        """Endpoint vertex of the developed primitive vector (a,b) from regular
        vertex w. Interior of the segment contains no vertex."""
        k = self.blsq[w]
        h, v, hi, vi, cor = self.h, self.v, self.hinv, self.vinv, self.corner
        if b == 0:
            return cor[4 * k + 1] if a > 0 else self.p0[hi[k]]
        if a == 0:
            return cor[4 * k + 2] if b > 0 else self.p0[vi[k]]
        if a < 0:
            k = hi[k]
        if b < 0:
            k = vi[k]
        A, B = abs(a), abs(b)
        i = j = 1
        while i < A or j < B:
            if j >= B or (i < A and i * B < j * A):
                k = h[k] if a > 0 else hi[k]
                i += 1
            else:
                k = v[k] if b > 0 else vi[k]
                j += 1
        c = (1 if a > 0 else 0) + (2 if b > 0 else 0)
        return cor[4 * k + c]

    def ray(self, w, a, b):
        """Vertices met along direction (a,b) (primitive) from regular w until a
        forbidden vertex (excluded) or return to w."""
        out = []
        x = w
        while True:
            x = self.step(x, a, b)
            if x == w or self.forbidden[x]:
                return out
            out.append(x)


def inv(p):
    q = [0] * len(p)
    for i, x in enumerate(p):
        q[x] = i
    return q


def compose(a, b):  # a after b
    return [a[x] for x in b]


# ---- SL(2,Z) action on structures (h, v, tau, p) ----
def act_T(st):
    h, v, t, p = st
    hi = inv(h)
    return (h, [v[hi[k]] for k in range(len(h))], [h[t[k]] for k in range(len(h))], p)


def act_R(st):
    h, v, t, p = st
    return (inv(v), h, t, [p[v[k]] for k in range(len(h))])


def invariant(st, mark):
    h, v, t, p = st
    out = []
    for perm in (h, v):
        seen = [False] * len(perm)
        cyc = []
        for k in range(len(perm)):
            if not seen[k]:
                L = m = 0
                x = k
                while not seen[x]:
                    seen[x] = True
                    L += 1
                    m += mark[p[x]]
                    x = perm[x]
                cyc.append((L, m))
        out.append(tuple(sorted(cyc)))
    return tuple(out)


def iso(st1, st2, mark, start2, cand1):
    """Find label bijection sigma: st1 -> st2 intertwining h, v, tau and marks,
    sending some candidate label of st1 to start2. Returns sigma or None."""
    h1, v1, t1, p1 = st1
    h2, v2, t2, p2 = st2
    N = len(h1)
    for s1 in cand1:
        sig = [-1] * N
        used = [False] * N
        sig[s1] = start2
        used[start2] = True
        dq = [s1]
        ok = True
        while dq and ok:
            k = dq.pop()
            for a1, a2 in ((h1, h2), (v1, v2), (t1, t2)):
                x1, x2 = a1[k], a2[sig[k]]
                if sig[x1] == -1:
                    if used[x2] or mark[p1[x1]] != mark[p2[x2]]:
                        ok = False
                        break
                    sig[x1] = x2
                    used[x2] = True
                    dq.append(x1)
                elif sig[x1] != x2:
                    ok = False
                    break
        if ok:
            return sig
    return None


def vertex_map(room, stY, stR, sig):
    """Affine map M -> M induced by iso sig: Y -> R: p_Y(k) -> p_R(sig k)."""
    f = [-1] * room.V
    pY, pR = stY[3], stR[3]
    for k in range(room.N):
        a, b = pY[k], pR[sig[k]]
        if f[a] == -1:
            f[a] = b
        else:
            assert f[a] == b
    assert -1 not in f
    return f


def full_group(room, log=print, cap=10**6):
    """Enumerate the SL(2,Z)-orbit of the marked, tau-equipped M. Return the list
    of distinct affine vertex maps (Schreier generators + automorphisms)."""
    mark = [1 if c else 0 for c in room.convex]
    base = (room.h, room.v, room.tau, room.p0)
    marked0 = [k for k in range(room.N) if mark[room.p0[k]]]
    reps = []
    byinv = {}
    gens = set()

    def find(st):
        I = invariant(st, mark)
        cand = [k for k in range(room.N) if mark[st[3][k]]]
        for ri in byinv.get(I, []):
            R = reps[ri]
            sig = iso(st, R[:4], mark, R[4], cand)
            if sig is not None:
                return ri, sig
        return None, I

    reps.append(base + (marked0[0],))
    byinv[invariant(base, mark)] = [0]
    # automorphisms of M (derivative I) compatible with marks and tau
    auts = []
    for s1 in marked0:
        sig = iso(base, base, mark, marked0[0], [s1])
        if sig is not None:
            f = vertex_map(room, base, base, sig)
            auts.append(f)
            gens.add(array('H', f).tobytes())
    q = deque([0])
    while q:
        i = q.popleft()
        st = reps[i][:4]
        for mv in (act_T, act_R):
            Y = mv(st)
            ri, sig = find(Y)
            if ri is None:
                reps.append(Y + ([k for k in range(room.N) if mark[Y[3][k]]][0],))
                byinv.setdefault(sig, []).append(len(reps) - 1)
                q.append(len(reps) - 1)
                if len(reps) > cap:
                    raise RuntimeError('orbit too large')
            else:
                f = vertex_map(room, Y, reps[ri], sig)
                gens.add(array('H', f).tobytes())
    log(f'  SL(2,Z)-orbit of marked M: {len(reps)}; |Aut| (deriv I, tau-compatible) = {len(auts)}; distinct generator maps {len(gens)}')
    out = [list(array('H', g)) for g in gens]
    return out, auts, len(reps)


def check_affine(room, f, deriv_guess=None):
    """Sanity: f preserves forbidden set and commutes with tau."""
    for w in range(room.V):
        assert room.forbidden[f[w]] == room.forbidden[w]
        assert room.convex[f[w]] == room.convex[w]
        assert f[room.vtau[w]] == room.vtau[f[w]]


def orbit_pairs(gens, start):
    seen = {start}
    dq = [start]
    while dq:
        a, b = dq.pop()
        for g in gens:
            y = (g[a], g[b])
            if y not in seen:
                seen.add(y)
                dq.append(y)
    return seen
