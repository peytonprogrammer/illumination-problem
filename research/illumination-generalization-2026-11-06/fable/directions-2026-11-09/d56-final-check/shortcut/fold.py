"""d52 core: W-sets (rooms and fold targets) as actions of W = <V0, V1, H0, H1>.

Self-contained; shares no code with d4/d6/d10/d44/d46.

A cell (X, Y) is [X, X+1] x [Y, Y+1]. V_e crosses the vertical cell edge on the line
x = X with X = e mod 2; H_e crosses the horizontal edge on y = Y with Y = e mod 2. A wall
edge is a fixed point. A lattice point of parity class (i, j) has star = one orbit of
<V_i, H_j>; the pillowcase monodromy at corner (i, j) is g = V_i H_j.

Orbit types of <V_i, H_j> (cells in alternating order):
  cvx    path of 1   g-cycles [1]     pole on the seam (convex corner)
  smooth path of 2   [2]              regular point on the seam
  rfx    path of 3   [3]              zero on the seam (reflex corner)
  cone   cycle of 2  [1, 1]           conjugate pair of off-seam poles (interior pi-cone)
  int    cycle of 4  [2, 2]           conjugate pair of regular points (interior point)
Anything else (path >= 4, cycle 6, ...) has a g-cycle of length >= 4 or an off-seam zero and
is excluded for rooms and for their class quotients (Fact L; zeros lie on the seam).
"""
from collections import deque

CLASSES = [(0, 0), (1, 0), (0, 1), (1, 1)]
CYC = {'cvx': [1], 'smooth': [2], 'rfx': [3], 'cone': [1, 1], 'int': [2, 2]}


def cg(cls):
    return cls[0], 2 + cls[1]


def from_cells(cells):
    cells = sorted(cells)
    idx = {c: k for k, c in enumerate(cells)}
    n = len(cells)
    G = [[0] * n for _ in range(4)]
    for (X, Y), k in idx.items():
        G[X % 2][k] = idx.get((X - 1, Y), k)
        G[(X + 1) % 2][k] = idx.get((X + 1, Y), k)
        G[2 + Y % 2][k] = idx.get((X, Y - 1), k)
        G[2 + (Y + 1) % 2][k] = idx.get((X, Y + 1), k)
    return G, cells


def cells_from_polygon(verts):
    xs = [v[0] for v in verts]
    ys = [v[1] for v in verts]
    out = set()
    m = len(verts)
    for X in range(min(xs), max(xs)):
        for Y in range(min(ys), max(ys)):
            px, py = X + 0.5, Y + 0.5
            inside = False
            for k in range(m):
                (x1, y1), (x2, y2) = verts[k], verts[(k + 1) % m]
                if (y1 > py) != (y2 > py):
                    xi = x1 + (py - y1) * (x2 - x1) / (y2 - y1)
                    if xi > px:
                        inside = not inside
            if inside:
                out.add((X, Y))
    return out


def trace(G, a, b, c0):
    """Alternating walk of <G[a], G[b]> from c0 in a complete or partial W-set.
    Returns (cells, kind) with kind 'closed' or (endF, endB), each end 'fixed' or 'open'."""
    cells = [c0]
    cur, g = c0, a
    endF = None
    while True:
        nxt = G[g][cur]
        if nxt == -1:
            endF = 'open'
            break
        if nxt == cur:
            endF = 'fixed'
            break
        if nxt == c0:
            return cells, 'closed'
        cells.append(nxt)
        cur = nxt
        g = b if g == a else a
    back = []
    cur, g = c0, b
    while True:
        nxt = G[g][cur]
        if nxt == -1:
            endB = 'open'
            break
        if nxt == cur:
            endB = 'fixed'
            break
        back.append(nxt)
        cur = nxt
        g = b if g == a else a
    return back[::-1] + cells, (endF, endB)


def orbit_type(cells, kind):
    L = len(cells)
    if kind == 'closed':
        return {2: 'cone', 4: 'int'}.get(L)
    if kind == ('fixed', 'fixed'):
        return {1: 'cvx', 2: 'smooth', 3: 'rfx'}.get(L)
    return 'partial'


def partial_ok(cells, kind, allowed):
    """Can this (partial) orbit still complete to an allowed type?"""
    L = len(cells)
    if kind == 'closed':
        t = {2: 'cone', 4: 'int'}.get(L)
        return t is not None and t in allowed
    nf = (kind[0] == 'fixed') + (kind[1] == 'fixed')
    if nf == 2:
        t = {1: 'cvx', 2: 'smooth', 3: 'rfx'}.get(L)
        return t is not None and t in allowed
    if nf == 1:
        return any(t in allowed for t, l in (('cvx', 1), ('smooth', 2), ('rfx', 3)) if l >= L)
    return any(t in allowed for t, l in (('cvx', 1), ('smooth', 2), ('rfx', 3), ('cone', 2), ('int', 4))
               if l >= L)


def orbits(G, cls):
    a, b = cg(cls)
    n = len(G[0])
    seen = [False] * n
    out = []
    for c in range(n):
        if not seen[c]:
            cells, kind = trace(G, a, b, c)
            for u in cells:
                seen[u] = True
            out.append((cells, kind, orbit_type(cells, kind)))
    return out


def profile(G):
    """Per class: list of orbit types. None if some orbit is invalid."""
    prof = {}
    for cls in CLASSES:
        ts = [t for (_, _, t) in orbits(G, cls)]
        if any(t is None or t == 'partial' for t in ts):
            return None
        prof[cls] = ts
    return prof


def summary(prof):
    z = sum(ts.count('rfx') for ts in prof.values())
    cvx = sum(ts.count('cvx') for ts in prof.values())
    cone = sum(ts.count('cone') for ts in prof.values())
    p = cvx + 2 * cone
    sing = [cls for cls, ts in prof.items() if any(t in ('cvx', 'rfx', 'cone') for t in ts)]
    return dict(z=z, cvx=cvx, cone=cone, p=p, genus0=(p - z == 4), sing=sing)


def transitive(G):
    n = len(G[0])
    seen = {0}
    st = [0]
    while st:
        u = st.pop()
        for g in range(4):
            v = G[g][u]
            if v not in seen:
                seen.add(v)
                st.append(v)
    return len(seen) == n


def canon(G):
    """Canonical form of a transitive W-set: min over start cells of the BFS relabelling."""
    n = len(G[0])
    best = None
    for s in range(n):
        lab = {s: 0}
        order = [s]
        k = 0
        while k < len(order):
            u = order[k]
            k += 1
            for g in range(4):
                v = G[g][u]
                if v not in lab:
                    lab[v] = len(order)
                    order.append(v)
        form = tuple(tuple(lab[G[g][u]] for u in order) for g in range(4))
        if best is None or form < best:
            best = form
    return best


def congruence(G, pairs):
    """Finest W-invariant partition merging the given pairs. Returns block id per cell."""
    n = len(G[0])
    par = list(range(n))

    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x
    q = deque(pairs)
    while q:
        u, v = q.popleft()
        ru, rv = find(u), find(v)
        if ru == rv:
            continue
        par[ru] = rv
        for g in range(4):
            q.append((G[g][u], G[g][v]))
    roots = {}
    return [roots.setdefault(find(u), len(roots)) for u in range(n)]


def congruence_G(G, pairs):
    """Same, closed only under the rotation monodromy g_x = V_i H_j (check of d10 R3.3)."""
    n = len(G[0])
    gs = []
    for cls in CLASSES:
        a, b = cg(cls)
        gs.append([G[a][G[b][u]] for u in range(n)])
    par = list(range(n))

    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x
    q = deque(pairs)
    while q:
        u, v = q.popleft()
        ru, rv = find(u), find(v)
        if ru == rv:
            continue
        par[ru] = rv
        for g in gs:
            q.append((g[u], g[v]))
    roots = {}
    return [roots.setdefault(find(u), len(roots)) for u in range(n)]


def two_cycle_pairs(G, cls):
    """Pairs of cells forming the 2-cycles of g_cls (smooth stars, opposite cells of int stars)."""
    out = []
    for cells, kind, t in orbits(G, cls):
        if t == 'smooth':
            out.append((cells[0], cells[1]))
        elif t == 'int':
            out.append((cells[0], cells[2]))
            out.append((cells[1], cells[3]))
    return out


def B(G, cls):
    return congruence(G, two_cycle_pairs(G, cls))


def quotient(G, blk):
    d = max(blk) + 1
    Q = [[-1] * d for _ in range(4)]
    for g in range(4):
        for u in range(len(blk)):
            Q[g][blk[u]] = blk[G[g][u]]
    return Q


def gcycle_id(Q, cls):
    """Cycle id of g_cls = V_i H_j on the quotient, per block."""
    a, b = cg(cls)
    d = len(Q[0])
    cid = [-1] * d
    k = 0
    for s in range(d):
        if cid[s] == -1:
            u = s
            while cid[u] == -1:
                cid[u] = k
                u = Q[a][Q[b][u]]
            k += 1
    return cid


def interior_points(G, cls):
    """Interior lattice points of class cls: list of (lift1 cell, lift2 cell)."""
    return [(cells[0], cells[1]) for cells, kind, t in orbits(G, cls) if t == 'int']


def separation_table(G, blk, acls):
    """For each interior a-point, the set of images of its two lifts in G/blk."""
    Q = quotient(G, blk)
    cid = gcycle_id(Q, acls)
    return [frozenset((cid[blk[u]], cid[blk[v]])) for (u, v) in interior_points(G, acls)]


def positives(G, prof=None):
    """All (a, S, T) with S < T interior a-points separated in every class y != a.
    S, T are orbit indices among interior a-points. Also returns per-class block counts."""
    n = len(G[0])
    blks = {cls: B(G, cls) for cls in CLASSES}
    found = []
    for a in CLASSES:
        pts = interior_points(G, a)
        if len(pts) < 2:
            continue
        tabs = [separation_table(G, blks[y], a) for y in CLASSES if y != a]
        for s in range(len(pts)):
            for t in range(s + 1, len(pts)):
                if all(not (tab[s] & tab[t]) for tab in tabs):
                    found.append((a, s, t))
    return found, {cls: max(b) + 1 for cls, b in blks.items()}


def develop(G):
    """Developing map of a W-set (base cell at (0,0)). Returns (coords, consistent, embedded)."""
    n = len(G[0])
    pos = {0: (0, 0)}
    st = [0]
    ok = True
    while st:
        u = st.pop()
        X, Y = pos[u]
        for g in range(4):
            v = G[g][u]
            if v == u:
                continue
            if g < 2:
                nb = (X - 1, Y) if X % 2 == g else (X + 1, Y)
            else:
                nb = (X, Y - 1) if Y % 2 == g - 2 else (X, Y + 1)
            if v in pos:
                if pos[v] != nb:
                    ok = False
            else:
                pos[v] = nb
                st.append(v)
    emb = ok and len(set(pos.values())) == n
    return pos, ok, emb


def is_room(G):
    """True when the W-set is a genuine strictly simple lattice room: the developing map is
    injective on cells, every wall faces a cell-free square and every glued edge faces a cell
    (no slits), and no pinch point."""
    pos, ok, emb = develop(G)
    if not emb:
        return False
    at = {p: u for u, p in pos.items()}
    for u, (X, Y) in pos.items():
        for g in range(4):
            if g < 2:
                nb = (X - 1, Y) if X % 2 == g else (X + 1, Y)
            else:
                nb = (X, Y - 1) if Y % 2 == g - 2 else (X, Y + 1)
            if (G[g][u] == u) != (nb not in at):
                return False
    return strictly_simple(list(pos.values()))


def strictly_simple(cells):
    """Room from cells: simply connected boundary and no lattice point where only two
    diagonal cells meet (pinch)."""
    cs = set(cells)
    pts = set()
    for (i, j) in cs:
        pts |= {(i, j), (i + 1, j), (i, j + 1), (i + 1, j + 1)}
    for (x, y) in pts:
        q = [(x - 1, y - 1) in cs, (x, y - 1) in cs, (x, y) in cs, (x - 1, y) in cs]
        if q == [True, False, True, False] or q == [False, True, False, True]:
            return False
    return True
