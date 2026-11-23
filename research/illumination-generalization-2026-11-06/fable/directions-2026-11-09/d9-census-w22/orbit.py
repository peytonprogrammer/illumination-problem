"""Complete LIT/DARK decider: SL(2,Z) orbit of the marked 4-fold unfolding.

Written for d9 without importing the record's deciders.

Unfolding M: one unit square per (cell, sheet), sheet (sx, sy) in {+-1}^2.
h = right neighbour, v = up neighbour in developing coordinates; in sheet
(sx, sy) developing +x is room direction sx.  Each square carries the room
lattice point at its developing bottom-left corner (its label).

Moves (derived in README):
  horizontal shear  [[1,1],[0,1]]:  h' = h,           v'(i) = v(h^-1(i))
  inverse                           h' = h,           v'(i) = v(h(i))
  vertical shear    [[1,0],[1,1]]:  h'(i) = h(v^-1(i)), v' = v
  inverse                           h'(i) = h(v(i)),    v' = v
Each move keeps the bottom-left corner of every square, so labels are
state-independent.  The four moves generate SL(2,Z), so the orbit contains
M' = A.M for every A; the horizontal direction of A.M is A^-1 (1,0) in M,
and every primitive vector is such an image.

Scan of a state: from every square whose label is a source, follow the
horizontal ray through the bottom-left corners of h(i), h^2(i), ...; stop at a
corner label (convex or reflex: illegal) or on return to i.  Every lattice
point the ray meets in between is reached by a legal billiard path.

States are stored up to label-preserving relabelling (canonical BFS
numbering from each square carrying the anchor label).  The orbit is finite,
so a full BFS is a complete decision: a pair never reached in any state is
joined by no billiard path.  Every billiard path between two lattice points
runs in a rational direction, its lattice points are the multiples of the
primitive step, and cone points of M sit only at lattice points.
"""
from collections import deque

SHEETS = ((1, 1), (-1, 1), (1, -1), (-1, -1))


def around(cells, p):
    x, y = p
    return sum(c in cells for c in ((x - 1, y - 1), (x, y - 1), (x - 1, y), (x, y)))


def unfolding(cells):
    cl = sorted(cells)
    sq = [(c, s) for c in cl for s in range(4)]
    ix = {t: k for k, t in enumerate(sq)}
    h, v, lab = [], [], []
    for (c, s) in sq:
        (i, j), (sx, sy) = c, SHEETS[s]
        nb = (i + sx, j)
        h.append(ix[(nb, s)] if nb in cells else ix[(c, SHEETS.index((-sx, sy)))])
        nb = (i, j + sy)
        v.append(ix[(nb, s)] if nb in cells else ix[(c, SHEETS.index((sx, -sy)))])
        lab.append((i + (1 if sx < 0 else 0), j + (1 if sy < 0 else 0)))
    return h, v, lab


def inverse(p):
    q = [0] * len(p)
    for a, b in enumerate(p):
        q[b] = a
    return q


def canon(h, v, dec, anchors):
    """Lexicographically least relabelling by BFS (h before v) from an anchor."""
    best = None
    n = len(h)
    for a in anchors:
        num = {a: 0}
        order = [a]
        k = 0
        while k < len(order):
            x = order[k]
            k += 1
            for y in (h[x], v[x]):
                if y not in num:
                    num[y] = len(order)
                    order.append(y)
        if len(order) != n:
            raise RuntimeError("unfolding not connected")
        key = (tuple(num[h[x]] for x in order), tuple(num[v[x]] for x in order),
               tuple(dec[x] for x in order))
        if best is None or key < best:
            best = key
    return best


def decide(cells, sources, wanted=None, cap=5_000_000):
    """Exact reachability among `sources` (regular lattice points).

    Returns (reach, nstates, complete).  reach[s] is the set of sources
    reached from s.  If `wanted` (a set of frozenset pairs) is given, the BFS
    stops as soon as all of them are reached (then complete=False but every
    wanted pair is certified lit by the state scan)."""
    cells = set(cells)
    h0, v0, lab = unfolding(cells)
    n = len(h0)
    src = sorted(set(sources))
    for s in src:
        assert around(cells, s) in (2, 4), s
    sid = {p: k for k, p in enumerate(src)}
    # decoration: source index, BLK = -1 for a corner, FREE = -2 otherwise
    dec = [sid[p] if p in sid else (-1 if around(cells, p) in (1, 3) else -2) for p in lab]
    anchor_pt = 0
    reach = {s: set() for s in src}
    todo = set(wanted) if wanted else None

    def scan(h, d):
        for i in range(n):
            a = d[i]
            if a < 0:
                continue
            cur = h[i]
            while cur != i and d[cur] != -1:
                b = d[cur]
                if b >= 0 and b != a:
                    p, q = src[a], src[b]
                    reach[p].add(q)
                    reach[q].add(p)
                    if todo is not None:
                        todo.discard(frozenset((p, q)))
                cur = h[cur]

    def state(h, v):
        anchors = [i for i in range(n) if dec[i] == anchor_pt]
        hh, vv, dd = canon(h, v, dec, anchors)
        return hh, vv, dd

    st0 = state(h0, v0)
    seen = {st0}
    queue = deque([st0])
    while queue:
        h, v, d = queue.popleft()
        scan(h, d)
        if todo is not None and not todo:
            return reach, len(seen), False
        hi, vi = inverse(h), inverse(v)
        moves = (
            (h, [v[hi[i]] for i in range(n)]),
            (h, [v[h[i]] for i in range(n)]),
            ([h[vi[i]] for i in range(n)], v),
            ([h[v[i]] for i in range(n)], v),
        )
        for a, b in moves:
            anchors = [i for i in range(n) if d[i] == anchor_pt]
            st = canon(a, b, d, anchors)
            if st not in seen:
                seen.add(st)
                queue.append(st)
                if len(seen) > cap:
                    raise RuntimeError("orbit cap exceeded")
    return reach, len(seen), True
