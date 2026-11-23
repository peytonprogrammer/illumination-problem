"""Exact tools for checking dictionary D0 (room billiards <-> pillowcase tuples).

Everything here is integer arithmetic. Three independent pieces:

1. Room geometry and the tuple (g_a, g_b, g_c, g_d) built from the definition in
   dictionary.md, section 1 (no code shared with d4_monodromy).
2. The tuple side: breadth-first search over the pure-braid orbit with the
   Hurwitz primitives of d6-hurwitz-census/hurwitz.py, plus a matrix in the
   level-2 group that names the three slopes of every state.
3. The room side: the 4-fold unfolding X (one unit square per cell and sign
   pair), a straight-line walker in X, and an SL(2,Z) orbit decider written
   here (no code shared with d8-perturbation-test).

Classes relative to an origin o: a = o + 2Z^2, b = a + (1,0), c = a + (1,1),
d = a + (0,1).  Tuple positions 0, 1, 2, 3 are a, b, c, d.
"""
import sys
from collections import deque
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'd6-hurwitz-census'))
import hurwitz as hz                      # noqa: E402

# ---------------------------------------------------------------- rooms


def status(cells, p):
    x, y = p
    ll, lr = (x - 1, y - 1) in cells, (x, y - 1) in cells
    ul, ur = (x - 1, y) in cells, (x, y) in cells
    n = ll + lr + ul + ur
    if n == 2 and ((ll and ur) or (lr and ul)):
        return 'pinch'
    return ('outside', 'convex', 'flat', 'reflex', 'interior')[n]


def lattice_points(cells):
    return sorted({(i + a, j + b) for (i, j) in cells for a in (0, 1) for b in (0, 1)})


def regular_points(cells):
    return [p for p in lattice_points(cells) if status(cells, p) in ('interior', 'flat')]


def wall_axis(cells, p):
    """For a flat point: 'H' if the wall through p is horizontal, else 'V'."""
    x, y = p
    below = (x - 1, y - 1) in cells and (x, y - 1) in cells
    above = (x - 1, y) in cells and (x, y) in cells
    return 'H' if (below or above) else 'V'


def strictly_simple(cells):
    cells = set(cells)
    start = next(iter(cells))
    seen, st = {start}, [start]
    while st:
        i, j = st.pop()
        for nb in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if nb in cells and nb not in seen:
                seen.add(nb)
                st.append(nb)
    if len(seen) != len(cells):
        return False
    xs = [c[0] for c in cells]
    ys = [c[1] for c in cells]
    box = {(i, j) for i in range(min(xs) - 1, max(xs) + 2)
           for j in range(min(ys) - 1, max(ys) + 2)} - cells
    start = (min(xs) - 1, min(ys) - 1)
    seen, st = {start}, [start]
    while st:
        i, j = st.pop()
        for nb in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if nb in box and nb not in seen:
                seen.add(nb)
                st.append(nb)
    if len(seen) != len(box):
        return False
    return all(status(cells, p) != 'pinch' for p in lattice_points(cells))


def normalize(cells):
    mx = min(c[0] for c in cells)
    my = min(c[1] for c in cells)
    return frozenset((i - mx, j - my) for (i, j) in cells)


def fixed_polyominoes(nmax):
    """All fixed polyominoes (translation classes) with 1..nmax cells, by size."""
    level = {frozenset({(0, 0)})}
    out = {1: sorted(level, key=sorted)}
    for n in range(2, nmax + 1):
        nxt = set()
        for poly in level:
            for (i, j) in poly:
                for nb in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                    if nb not in poly:
                        nxt.add(normalize(poly | {nb}))
        level = nxt
        out[n] = sorted(level, key=sorted)
    return out


def symmetries(cells):
    outs = []
    cur = list(cells)
    for _ in range(4):
        cur = [(-j, i) for (i, j) in cur]
        outs.append(normalize(cur))
        outs.append(normalize([(-i, j) for (i, j) in cur]))
    return outs


def is_free_rep(cells):
    key = sorted(cells)
    return all(key <= sorted(s) for s in symmetries(cells))


def cells_from_vertices(verts):
    xs = [x for x, _ in verts]
    ys = [y for _, y in verts]
    out = set()
    m = len(verts)
    for i in range(min(xs), max(xs)):
        for j in range(min(ys), max(ys)):
            cx, cy = 2 * i + 1, 2 * j + 1
            inside = False
            for k in range(m):
                (x1, y1), (x2, y2) = verts[k], verts[(k + 1) % m]
                if x1 == x2 and (2 * y1 > cy) != (2 * y2 > cy) and 2 * x1 > cx:
                    inside = not inside
            if inside:
                out.add((i, j))
    return frozenset(out)


# ---------------------------------------------------------------- tuple of a room

def room_tuple(cells, origin):
    """(sheets, t): sheets = sorted cells, t = (g_a, g_b, g_c, g_d) as in dictionary.md.

    kappa_V^e crosses the vertical edge of the cell whose x-coordinate is e mod 2
    (relative to the origin); kappa_H^e likewise.  A wall fixes the cell.
    r_(e,f) = kappa_V^e then kappa_H^f.  The counter-clockwise corner monodromies are
    g_a = r_00, g_b = r_10^-1, g_c = r_11, g_d = r_01^-1.
    """
    cells = set(cells)
    sheets = sorted(cells)
    idx = {c: k for k, c in enumerate(sheets)}
    ox, oy = origin

    def kv(c, e):
        i, j = c
        nb = (i - 1, j) if (i - ox) % 2 == e else (i + 1, j)
        return nb if nb in cells else c

    def kh(c, f):
        i, j = c
        nb = (i, j - 1) if (j - oy) % 2 == f else (i, j + 1)
        return nb if nb in cells else c

    r = {(e, f): tuple(idx[kh(kv(c, e), f)] for c in sheets) for e in (0, 1) for f in (0, 1)}
    t = (r[0, 0], hz.inv(r[1, 0]), r[1, 1], hz.inv(r[0, 1]))
    assert hz.mul(hz.mul(hz.mul(t[0], t[1]), t[2]), t[3]) == hz.ident(len(sheets))
    return sheets, t


def a_lifts(cells, origin):
    """Regular points of DP over class a: dict (P, face) -> a cell of its 2-cycle.

    Interior P: face +1 (front) has the cycle {NE, SW}, face -1 (back) has {NW, SE}.
    Flat P: one lift, face 0.
    """
    out = {}
    for p in regular_points(cells):
        if (p[0] - origin[0]) % 2 or (p[1] - origin[1]) % 2:
            continue
        x, y = p
        if status(cells, p) == 'interior':
            out[(p, 1)] = (x, y)
            out[(p, -1)] = (x - 1, y)
        else:
            out[(p, 0)] = next(c for c in ((x - 1, y - 1), (x, y - 1), (x - 1, y), (x, y)) if c in cells)
    return out


# ---------------------------------------------------------------- unfolding X

class Unfolding:
    """4-fold unfolding X.  Square (c, sx, sy): developing +x is room direction sx.

    The lower-left corner of square (c, sx, sy) is the room point
    (i + [sx < 0], j + [sy < 0]).  h = right neighbour, v = upper neighbour.
    """

    def __init__(self, cells):
        self.cells = cells = set(cells)
        self.sq = [(c, sx, sy) for c in sorted(cells) for sx in (1, -1) for sy in (1, -1)]
        self.idx = {s: k for k, s in enumerate(self.sq)}
        h, v, ll = [], [], []
        for (c, sx, sy) in self.sq:
            i, j = c
            nb = (i + sx, j)
            h.append(self.idx[(nb, sx, sy)] if nb in cells else self.idx[(c, -sx, sy)])
            nb = (i, j + sy)
            v.append(self.idx[(nb, sx, sy)] if nb in cells else self.idx[(c, sx, -sy)])
            ll.append((i + (sx < 0), j + (sy < 0)))
        self.h, self.v, self.ll = h, v, ll
        self.hi = [0] * len(h)
        self.vi = [0] * len(v)
        for k in range(len(h)):
            self.hi[h[k]] = k
            self.vi[v[k]] = k
        self.st = {p: status(cells, p) for p in lattice_points(cells)}

    def dp_point(self, k):
        """DP point under the lower-left corner of square k: (room point, face)."""
        p = self.ll[k]
        _, sx, sy = self.sq[k]
        return (p, sx * sy) if self.st[p] == 'interior' else (p, 0)

    def squares_at(self, p):
        return [k for k in range(len(self.sq)) if self.ll[k] == p]

    def step(self, k, d):
        """Straight segment with developing vector d (coprime) from the lower-left
        corner of square k (a regular point).  Returns the square whose lower-left
        corner is the end point.  The interior of the segment has no lattice point."""
        dx, dy = d
        h, v, hi, vi = self.h, self.v, self.hi, self.vi
        if dy == 0:
            assert abs(dx) == 1
            return h[k] if dx > 0 else hi[k]
        if dx == 0:
            assert abs(dy) == 1
            return v[k] if dy > 0 else vi[k]
        P, Q = abs(dx), abs(dy)
        fx = h if dx > 0 else hi
        fy = v if dy > 0 else vi
        cur = k
        if dx < 0:
            cur = hi[cur]
        if dy < 0:
            cur = vi[cur]            # the start is regular, so hi and vi commute here
        i, j = 1, 1
        while i < P or j < Q:
            # next crossing: vertical line i at time i/P, horizontal line j at time j/Q
            if j >= Q or (i < P and i * Q < j * P):
                cur = fx[cur]
                i += 1
            else:
                cur = fy[cur]
                j += 1
        # end point = far corner of `cur`; return the square with that lower-left corner
        if dx > 0:
            cur = h[cur]
        if dy > 0:
            cur = v[cur]
        return cur


def geo_components(U, origin, slope):
    """Components (size >= 2) of the regular a-points of DP joined by straight
    segments of the given slope through regular points only.

    Returns a set of frozensets of (P, face).  Edges at a regular a-point are the
    walks of developing vector `slope` from its two lifts to X.
    """
    parent = {}

    def find(u):
        while parent.setdefault(u, u) != u:
            parent[u] = parent[parent[u]]
            u = parent[u]
        return u

    ox, oy = origin
    for k in range(len(U.sq)):
        p = U.ll[k]
        if (p[0] - ox) % 2 or (p[1] - oy) % 2 or U.st[p] not in ('interior', 'flat'):
            continue
        u = U.dp_point(k)
        find(u)
        m = U.step(k, slope)
        if U.st[U.ll[m]] not in ('interior', 'flat'):
            continue
        e = U.step(m, slope)
        if U.st[U.ll[e]] not in ('interior', 'flat'):
            continue
        ru, rv = find(u), find(U.dp_point(e))
        if ru != rv:
            parent[ru] = rv
    comp = {}
    for u in list(parent):
        comp.setdefault(find(u), set()).add(u)
    return {frozenset(c) for c in comp.values() if len(c) > 1}


def ray(U, k, slope, limit=100000):
    """Regular lattice points met by the ray of developing direction `slope` from
    the lower-left corner of square k, in order, as (steps, dp_point), until a
    vertex is met or the ray returns to its start."""
    out = []
    cur = k
    for s in range(1, limit):
        cur = U.step(cur, slope)
        if U.st[U.ll[cur]] not in ('interior', 'flat'):
            return out
        if cur == k:
            return out
        out.append((s, U.dp_point(cur)))
    raise RuntimeError('ray did not close')


# ---------------------------------------------------------------- tuple side

# Matrices of the two pure generators on slopes, as columns (p, q).  The signs are
# fixed by calibrate() on one room and then checked on every state of every room.
def gen_matrix(i, s, eps):
    e = eps[i] * s
    return ((1, 2 * e), (0, 1)) if i == 0 else ((1, 0), (2 * e, 1))


def matmul(A, B):
    return ((A[0][0] * B[0][0] + A[0][1] * B[1][0], A[0][0] * B[0][1] + A[0][1] * B[1][1]),
            (A[1][0] * B[0][0] + A[1][1] * B[1][0], A[1][0] * B[0][1] + A[1][1] * B[1][1]))


BASE_SLOPES = {1: (1, 0), 2: (1, 1), 3: (0, 1)}


def state_slope(M, j):
    p, q = BASE_SLOPES[j]
    return (M[0][0] * p + M[0][1] * q, M[1][0] * p + M[1][1] * q)


def tuple_orbit(t, eps=(1, 1), on_state=None, max_states=None):
    """Marked pure-braid orbit of t.  Point IDs = cycle index of g_a in the base state.

    Returns dict(states, complete, lit, witness, pt0, plen) with
      lit      set of frozenset({P, Q}) of regular a-point IDs joined by a chain
      witness  pair -> (word, j, M) for the first state found; M names the slopes
    on_state(t, pt, word, M) is called for every state.
    """
    labels = ('a', 'b', 'c', 'd')
    cid, plen = hz.initial_pt(t[0])
    pt = tuple(c if plen[c] == 2 else -1 for c in cid)
    n = len(t[0])
    root_id = min((c for c in cid if plen[c] == 2), default=-1)
    if root_id < 0:
        return dict(states=1, complete=True, lit=set(), witness={}, pt0=cid, plen=plen)

    def canon(t_, pt_):
        return hz.canon_marked(t_, pt_, [i for i in range(n) if pt_[i] == root_id])

    I = ((1, 0), (0, 1))
    seen = {canon(t, pt)}
    queue = deque([(t, pt, (), I)])
    lit, witness = set(), {}
    while queue:
        t_, pt_, word, M = queue.popleft()
        if on_state:
            on_state(t_, pt_, word, M)
        for j in (1, 2, 3):
            for comp in hz.arc_components(t_[0], pt_, plen, t_[j]):
                cl = sorted(comp)
                for x in range(len(cl)):
                    for y in range(x + 1, len(cl)):
                        pr = frozenset((cl[x], cl[y]))
                        if pr not in lit:
                            lit.add(pr)
                            witness[pr] = (word, j, M)
        for (i, s) in hz.PURE_GENS:
            t2, lab2, pt2 = hz.pure_move(t_, labels, pt_, i, s)
            assert lab2 == labels
            c = canon(t2, pt2)
            if c not in seen:
                seen.add(c)
                if max_states and len(seen) > max_states:
                    return dict(states=len(seen), complete=False, lit=lit, witness=witness,
                                pt0=cid, plen=plen)
                queue.append((t2, pt2, word + ((i, s),), matmul(M, gen_matrix(i, s, eps))))
    return dict(states=len(seen), complete=True, lit=lit, witness=witness, pt0=cid, plen=plen)


# ---------------------------------------------------------------- room side decider

def room_orbit(cells, max_states=None):
    """Complete decision by the SL(2,Z) orbit of the decorated unfolding X.

    Sources are all regular lattice points.  Returns dict(states, complete,
    lit, lit_noslide, witness) where
      lit          set of frozenset({dp_point, dp_point}) joined by a straight segment
                   in DP with regular interior (segments along the seam included)
      lit_noslide  the same without segments that run along a wall
      witness      pair -> (steps, (dx, dy)) developing vector steps * (dx, dy)
    """
    U = Unfolding(cells)
    N = len(U.sq)
    reg = {p for p, s in U.st.items() if s in ('interior', 'flat')}
    blocked = [U.ll[k] not in reg for k in range(N)]
    dp = [U.dp_point(k) if not blocked[k] else None for k in range(N)]
    srcs = sorted(reg)
    if not srcs:
        return dict(states=0, complete=True, lit=set(), lit_noslide=set(), witness={})
    lab = [(-1 if blocked[k] else srcs.index(U.ll[k])) for k in range(N)]
    roots = [k for k in range(N) if lab[k] == 0]
    flat_axis = {p: wall_axis(U.cells, p) for p in reg if U.st[p] == 'flat'}

    def canon(h, v):
        best = None
        for r in roots:
            new = [-1] * N
            order = [r]
            new[r] = 0
            for a in order:
                for b in (v[a], h[a]):
                    if new[b] < 0:
                        new[b] = len(order)
                        order.append(b)
            assert len(order) == N
            enc = tuple(new[h[a]] for a in order) + tuple(new[v[a]] for a in order) + \
                tuple(lab[a] for a in order)
            if best is None or enc < best:
                best = enc
        return best

    h0, v0 = tuple(U.h), tuple(U.v)
    seen = {canon(h0, v0)}
    queue = deque([(h0, v0, (1, 0, 0, 1))])
    lit, lit_ns, witness = set(), set(), {}
    while queue:
        h, v, M = queue.popleft()
        a, b, c, d = M
        dirv = (d, -c)                       # M^-1 (1, 0)
        axis = 'H' if dirv[1] == 0 else ('V' if dirv[0] == 0 else None)
        for k in range(N):
            if blocked[k]:
                continue
            slide = axis is not None and flat_axis.get(U.ll[k]) == axis
            cur, steps = h[k], 1
            while cur != k and not blocked[cur]:
                if dp[cur] != dp[k]:
                    pr = frozenset((dp[k], dp[cur]))
                    if pr not in lit:
                        lit.add(pr)
                        witness[pr] = (steps, dirv)
                    if not slide:
                        lit_ns.add(pr)
                cur = h[cur]
                steps += 1
        hi = [0] * N
        vi = [0] * N
        for k in range(N):
            hi[h[k]] = k
            vi[v[k]] = k
        for g in range(4):
            if g == 0:      # U: x' = x + y
                h2, v2, M2 = h, tuple(v[hi[k]] for k in range(N)), (a + c, b + d, c, d)
            elif g == 1:    # U^-1
                h2, v2, M2 = h, tuple(v[h[k]] for k in range(N)), (a - c, b - d, c, d)
            elif g == 2:    # L: y' = y + x
                h2, v2, M2 = tuple(h[vi[k]] for k in range(N)), v, (a, b, a + c, b + d)
            else:           # L^-1
                h2, v2, M2 = tuple(h[v[k]] for k in range(N)), v, (a, b, c - a, d - b)
            cf = canon(h2, v2)
            if cf not in seen:
                seen.add(cf)
                if max_states and len(seen) > max_states:
                    return dict(states=len(seen), complete=False, lit=lit, lit_noslide=lit_ns,
                                witness=witness)
                queue.append((h2, v2, M2))
    return dict(states=len(seen), complete=True, lit=lit, lit_noslide=lit_ns, witness=witness)


def calibrate(cells, origin):
    """Find the sign pair eps for which every state's three chain graphs equal the
    straight-segment graphs at the slopes named by its matrix.  Returns the list of
    sign pairs that pass on this room."""
    ok = []
    for eps in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
        bad = state_check(cells, origin, eps, max_norm=400)[1]
        if bad == 0:
            ok.append(eps)
    return ok


def state_check(cells, origin, eps, max_norm=400, max_states=None, check_cap=None):
    """Compare, in every state and for every arc, the tuple's chain components with
    the straight-segment components at the slope the matrix names.
    Returns (checked, mismatches, skipped, orbit result)."""
    sheets, t = room_tuple(cells, origin)
    idx = {c: k for k, c in enumerate(sheets)}
    U = Unfolding(cells)
    lifts = a_lifts(cells, origin)
    cid, plen = hz.initial_pt(t[0])
    ident = {u: cid[idx[c]] for u, c in lifts.items()}
    assert all(plen[i] == 2 for i in ident.values()) and len(set(ident.values())) == len(ident)
    assert sum(1 for L in plen if L == 2) == len(ident)
    counts = [0, 0, 0]

    seen_states = [0]

    def on_state(t_, pt_, word, M):
        seen_states[0] += 1
        if check_cap is not None and seen_states[0] > check_cap:
            counts[2] += 3
            return
        for j in (1, 2, 3):
            sl = state_slope(M, j)
            if abs(sl[0]) + abs(sl[1]) > max_norm:
                counts[2] += 1
                continue
            geo = {frozenset(ident[u] for u in comp) for comp in geo_components(U, origin, sl)}
            tup = set(hz.arc_components(t_[0], pt_, plen, t_[j]))
            counts[0] += 1
            if geo != tup:
                counts[1] += 1

    res = tuple_orbit(t, eps, on_state=on_state, max_states=max_states)
    res['ident'] = ident
    return counts[0], counts[1], counts[2], res
