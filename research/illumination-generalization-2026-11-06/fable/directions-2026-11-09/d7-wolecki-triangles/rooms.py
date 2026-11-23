"""Exact tools for rooms tiled by a Wolecki triangle with angles (1, b, c) * pi/n.

Points are elements of Z[zeta], zeta = exp(i*pi/n), stored as integer tuples in the
power basis modulo the cyclotomic polynomial Phi_{2n}. Equality and collinearity
tests are exact. A sign is read from a float only after the exact zero test fails,
and the code raises if the float is within 1e-9 of zero.

No third-party imports.
"""
import cmath
import math
from collections import defaultdict


def _polymul(p, q):
    r = [0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        if a:
            for j, b in enumerate(q):
                r[i + j] += a * b
    return r


def _polydiv(p, q):
    p = p[:]
    out = [0] * (len(p) - len(q) + 1)
    for i in range(len(out) - 1, -1, -1):
        f = p[i + len(q) - 1] // q[-1]
        out[i] = f
        for j, b in enumerate(q):
            p[i + j] -= f * b
    assert not any(p), "inexact polynomial division"
    return out


def _mobius(m):
    res, p = 1, 2
    while p * p <= m:
        if m % p == 0:
            m //= p
            if m % p == 0:
                return 0
            res = -res
        p += 1
    return -res if m > 1 else res


def cyclotomic(N):
    num, den = [1], [1]
    for d in range(1, N + 1):
        if N % d == 0:
            mu = _mobius(N // d)
            f = [-1] + [0] * (d - 1) + [1]
            if mu == 1:
                num = _polymul(num, f)
            elif mu == -1:
                den = _polymul(den, f)
    return _polydiv(num, den)


class Geo:
    """Arithmetic in Z[zeta_{2n}] and the base tile for the triangle (1, b, c)."""

    def __init__(self, n, b):
        assert n % 2 == 0 and 1 <= b <= n - 2
        self.n, self.b, self.c = n, b, n - 1 - b
        self.N = 2 * n
        self.phi = cyclotomic(self.N)
        self.d = len(self.phi) - 1
        self.unit = [None] * self.N
        v = [1] + [0] * (self.d - 1)
        for k in range(self.N):
            self.unit[k] = tuple(v)
            w = [0] + v                      # multiply by x
            top = w[self.d]
            v = [w[i] - top * self.phi[i] for i in range(self.d)]
        assert tuple(v) == self.unit[0]
        self.zero = tuple([0] * self.d)
        self.roots = [cmath.exp(1j * math.pi * k / n) for k in range(self.d)]
        self.ang = {'A': 1, 'B': self.b, 'C': self.c}
        # 2 sin(k pi/n) = zeta^(n/2-k) - zeta^(n/2+k)
        s = lambda k: self.sub(self.zeta(n // 2 - k), self.zeta(n // 2 + k))
        A = self.zero
        B = s(self.c)
        C = self.mul(s(self.b), self.zeta(1))
        self.base = (A, B, C)
        fa, fb, fc = (self.cx(p) for p in self.base)
        assert abs(cmath.phase((fc - fa) / (fb - fa)) - math.pi / n) < 1e-12
        assert abs(cmath.phase((fa - fb) / (fc - fb)) - self.b * math.pi / n) < 1e-12

    def zeta(self, k):
        return self.unit[k % self.N]

    @staticmethod
    def add(a, b):
        return tuple(x + y for x, y in zip(a, b))

    @staticmethod
    def sub(a, b):
        return tuple(x - y for x, y in zip(a, b))

    def mul(self, a, b):
        out = [0] * self.d
        for i, x in enumerate(a):
            if x:
                for j, y in enumerate(b):
                    if y:
                        xy = x * y
                        for t, u in enumerate(self.unit[(i + j) % self.N]):
                            if u:
                                out[t] += xy * u
        return tuple(out)

    def conj(self, a):
        out = [0] * self.d
        for i, x in enumerate(a):
            if x:
                for t, u in enumerate(self.unit[(self.N - i) % self.N]):
                    if u:
                        out[t] += x * u
        return tuple(out)

    def cx(self, a):
        return sum(x * r for x, r in zip(a, self.roots))

    # ---- exact predicates -------------------------------------------------
    def cross_sign(self, u, v):
        """Sign of Im(conj(u) * v), exact zero test."""
        w = self.mul(self.conj(u), v)
        if w == self.conj(w):
            return 0
        f = self.cx(w).imag
        if abs(f) < 1e-9:
            raise ArithmeticError("nonzero cross product too small for float sign")
        return 1 if f > 0 else -1

    def orient(self, p, q, r):
        return self.cross_sign(self.sub(q, p), self.sub(r, p))

    def dot(self, u, v):
        return (self.cx(u).conjugate() * self.cx(v)).real

    def twice_area_i(self, p, q, r):
        """conj(q-p)(r-p) - its conjugate = 2i * (signed double area), exact."""
        w = self.mul(self.conj(self.sub(q, p)), self.sub(r, p))
        return self.sub(w, self.conj(w))

    # ---- reflections -------------------------------------------------------
    def reflect_point(self, z, p, q):
        e = self.sub(q, p)
        ce = self.conj(e)
        k = round(2 * cmath.phase(self.cx(e)) / (math.pi / self.n)) % self.N
        w = self.zeta(k)
        assert self.mul(w, ce) == e, "edge direction is not a multiple of pi/n"
        return self.add(p, self.mul(w, self.conj(self.sub(z, p))))

    def reflect_tile(self, t, i):
        """Mirror tile t across the edge opposite vertex index i (0=A, 1=B, 2=C)."""
        p, q = [t[j] for j in range(3) if j != i]
        z = self.reflect_point(t[i], p, q)
        s = list(t)
        s[i] = z
        return tuple(s)

    def fan(self, t, v, first=None):
        """All tiles of the full rosette around vertex index v of tile t, in rotational order."""
        others = [j for j in range(3) if j != v]
        if first is not None:
            others = [first] + [j for j in others if j != first]
        out = [t]
        i = 0
        while True:
            nxt = self.reflect_tile(out[-1], others[i % 2])
            i += 1
            if nxt == t or len(out) > 4 * self.n:
                break
            out.append(nxt)
        return out

    def star(self, t, first=2):
        """The 2n tiles around the A vertex of t. first=2 reflects across AB first."""
        s = self.fan(t, 0, first)
        assert len(s) == 2 * self.n
        return s


LABELS = 'ABC'


class Invalid(Exception):
    pass


def tiles_overlap(g, t1, t2):
    """True if the open triangles intersect (separating-axis test, exact signs)."""
    for a, b in ((t1, t2), (t2, t1)):
        for i in range(3):
            p, q, r = a[i], a[(i + 1) % 3], a[(i + 2) % 3]
            side = g.orient(p, q, r)
            if all(g.orient(p, q, x) * side <= 0 for x in b):
                return False
    return True


def _far(g, t1, t2, rad2):
    c1 = sum(g.cx(p) for p in t1) / 3
    c2 = sum(g.cx(p) for p in t2) / 3
    return abs(c1 - c2) ** 2 > rad2


def any_overlap(g, tiles, others=None):
    tiles = list(tiles)
    f = [g.cx(p) for p in g.base]
    rad2 = (2.1 * max(abs(f[i] - f[j]) for i in range(3) for j in range(3))) ** 2
    if others is None:
        pairs = ((tiles[i], tiles[j]) for i in range(len(tiles)) for j in range(i))
    else:
        pairs = ((s, t) for s in tiles for t in others)
    for s, t in pairs:
        if s != t and not _far(g, s, t, rad2) and tiles_overlap(g, s, t):
            return True
    return False


def _segments_touch(g, p1, p2, p3, p4):
    o1, o2 = g.orient(p1, p2, p3), g.orient(p1, p2, p4)
    o3, o4 = g.orient(p3, p4, p1), g.orient(p3, p4, p2)
    if o1 * o2 < 0 and o3 * o4 < 0:
        return True

    def on(p, q, r):
        d = g.dot(g.sub(r, p), g.sub(q, p))
        return r == p or r == q or (1e-9 < d < g.dot(g.sub(q, p), g.sub(q, p)) - 1e-9)
    return ((o1 == 0 and on(p1, p2, p3)) or (o2 == 0 and on(p1, p2, p4)) or
            (o3 == 0 and on(p3, p4, p1)) or (o4 == 0 and on(p3, p4, p2)))


def analyze(g, tiles, clean_classes=None):
    """Full exact check of a tile set. Raises Invalid, or returns a report dict.

    clean_classes: vertex classes whose points must all be genuine corners.
    Default: the obstruction classes E of theorem.md (angle pi/q, q even).
    """
    n = g.n
    tiles = list(dict.fromkeys(tiles))
    if clean_classes is None:
        clean_classes = obstruction_classes(n, g.b)
    cls, at = {}, defaultdict(list)
    edges = defaultdict(list)
    for t in tiles:
        if len(set(t)) != 3:
            raise Invalid("degenerate tile")
        for i, p in enumerate(t):
            if cls.setdefault(p, LABELS[i]) != LABELS[i]:
                raise Invalid("fold conflict: a point has two vertex classes")
            at[p].append(t)
        for i in range(3):
            edges[frozenset((t[i], t[(i + 1) % 3]))].append(t)
    if any(len(v) > 2 for v in edges.values()):
        raise Invalid("an edge lies in more than two tiles")
    if any_overlap(g, tiles):
        raise Invalid("two tiles overlap")
    # edge-connectivity of the tiling
    nb = defaultdict(list)
    for v in edges.values():
        if len(v) == 2:
            nb[v[0]].append(v[1])
            nb[v[1]].append(v[0])
    seen, todo = {tiles[0]}, [tiles[0]]
    while todo:
        for u in nb[todo.pop()]:
            if u not in seen:
                seen.add(u)
                todo.append(u)
    if len(seen) != len(tiles):
        raise Invalid("tiles are not edge-connected")
    # boundary: one cycle, every boundary vertex of degree 2
    bnd = [tuple(e) for e, v in edges.items() if len(v) == 1]
    adj = defaultdict(list)
    for p, q in bnd:
        adj[p].append(q)
        adj[q].append(p)
    if any(len(v) != 2 for v in adj.values()):
        raise Invalid("pinch point: a boundary vertex has boundary degree != 2")
    start = bnd[0][0]
    cyc, prev, cur = [start], None, start
    while True:
        nxt = [x for x in adj[cur] if x != prev] if prev is not None else adj[cur][:1]
        nxt = nxt[0] if nxt else adj[cur][0]
        if nxt == start:
            break
        cyc.append(nxt)
        prev, cur = cur, nxt
        if len(cyc) > len(bnd):
            raise Invalid("boundary walk does not close")
    if len(cyc) != len(bnd):
        raise Invalid("boundary has more than one component (hole)")
    m = len(cyc)
    segs = [(cyc[i], cyc[(i + 1) % m]) for i in range(m)]
    for i in range(m):
        for j in range(i):
            if j == i - 1 or (i == m - 1 and j == 0):
                continue
            if _segments_touch(g, *segs[i], *segs[j]):
                raise Invalid("boundary is not strictly simple")
    # exact area identity: shoelace over the boundary equals the sum of tile areas
    zero = g.zero
    tot = zero
    for t in tiles:
        a = g.twice_area_i(*t)
        tot = g.add(tot, a if g.orient(*t) > 0 else g.sub(zero, a))
    sh = zero
    for p, q in segs:
        w = g.mul(g.conj(p), q)
        sh = g.add(sh, g.sub(w, g.conj(w)))
    if sh != tot and g.sub(zero, sh) != tot:
        raise Invalid("area mismatch")
    # vertex data
    onb = set(cyc)
    verts = {}
    for p, ts in at.items():
        k, v = len(ts), g.ang[cls[p]]
        if p in onb:
            if k * v >= 2 * n:
                raise Invalid("boundary vertex with angle >= 2 pi")
            kind = 'flat' if k * v == n else 'corner'
        else:
            if k * v != 2 * n or k % 2:
                raise Invalid("interior vertex with a bad fan")
            kind = 'interior'
        verts[p] = (cls[p], k, kind)
    corners = [p for p in cyc if verts[p][2] == 'corner']
    turning = sum(n - verts[p][1] * g.ang[verts[p][0]] for p in corners)
    if turning != 2 * n:
        raise Invalid("turning sum is not 2 pi")
    # independent wall count: merge collinear boundary edges by exact cross products
    walls = sum(1 for i in range(m) if g.orient(cyc[i - 1], cyc[i], cyc[(i + 1) % m]) != 0)
    assert walls == len(corners)
    dirty = [p for p, (c, k, kind) in verts.items() if c in clean_classes and kind != 'corner']
    hist = defaultdict(int)
    for p in corners:
        hist["%s%d" % verts[p][:2]] += 1
    return dict(n=n, b=g.b, c=g.c, tiles=len(tiles), walls=walls,
                interior_A=[p for p, (c, k, kind) in verts.items() if c == 'A' and kind == 'interior'],
                clean=not dirty, dirty=len(dirty), clean_classes=sorted(clean_classes),
                corner_types=dict(sorted(hist.items())),
                flat={c: sum(1 for x in verts.values() if x[0] == c and x[2] == 'flat') for c in LABELS},
                interior={c: sum(1 for x in verts.values() if x[0] == c and x[2] == 'interior') for c in LABELS},
                verts=verts, cycle=cyc, tileset=tiles)


def obstruction_classes(n, b):
    """Classes V in {B, C} with angle pi/q, q even: the only classes that must be forced to be corners."""
    out = set()
    for lab, v in (('B', b), ('C', n - 1 - b)):
        if n % v == 0 and (n // v) % 2 == 0:
            out.add(lab)
    return out


def tau_fixed_classes(n, b):
    """Classes V in {B, C} whose lifts are fixed by rotation by pi: reduced denominator even."""
    return {lab for lab, v in (('B', b), ('C', n - 1 - b)) if (n // math.gcd(n, v)) % 2 == 0}


# ---- exact billiard shooter ------------------------------------------------
def shoot(g, rep, S, X, target):
    """Trace the billiard ray from interior A point S toward the unfolded point X.

    The ray stays straight and the room is unfolded along it. Returns one of
      ('LIT', room_point)      the ray reaches X and X unfolds the room point `target`
      ('BLOCKED', cls, frac)   the ray meets a genuine corner at fraction frac of |X-S|
      ('MISS',)                the ray passes distance |X-S| without ending on `target`
    Transparent vertices (interior or flat) are passed legally.
    """
    verts, tiles = rep['verts'], set(rep['tileset'])
    d = g.sub(X, S)
    L2 = g.dot(d, d)

    def side(p):
        return g.cross_sign(d, g.sub(p, S))

    def along(p):
        return g.dot(d, g.sub(p, S))

    def step(room_t, unf_t, i):
        """Cross the edge opposite vertex index i."""
        nu = g.reflect_tile(unf_t, i)
        nr = g.reflect_tile(room_t, i)
        return (nr if nr in tiles else room_t), nu

    def enter_at_vertex(room_t, unf_t, v):
        """Rotate around vertex index v until the forward ray lies in the tile's closed sector.

        Returns (room_t, unf_t, hit) where hit is the index of a vertex the ray runs
        straight into along an edge, or None if the ray enters the tile interior.
        """
        o = [j for j in range(3) if j != v]
        for turn in range(4 * g.n + 4):
            P = unf_t[v]
            u1, u2 = g.sub(unf_t[o[0]], P), g.sub(unf_t[o[1]], P)
            s1, s2 = g.cross_sign(u1, d), g.cross_sign(d, u2)
            orient = g.cross_sign(u1, u2)
            if s1 == 0 and g.dot(u1, d) > 0:
                return room_t, unf_t, o[0]
            if s2 == 0 and g.dot(u2, d) > 0:
                return room_t, unf_t, o[1]
            if s1 * orient > 0 and s2 * orient > 0:
                return room_t, unf_t, None
            room_t, unf_t = step(room_t, unf_t, o[turn % 2])
        raise ArithmeticError("rosette search failed")

    def vertex_event(room_t, unf_t, v):
        P = unf_t[v]
        rp = room_t[v]
        frac = along(P) / L2
        if P == X:
            return ('LIT', rp) if rp == target else ('MISS',)
        if frac > 1:
            return ('MISS',)
        if verts[rp][2] == 'corner':
            return ('BLOCKED', verts[rp][0], frac)
        return None

    t0 = next(t for t in tiles if t[0] == S)
    pivot = 0
    room_t, unf_t, hit = enter_at_vertex(t0, t0, pivot)
    entry = None                       # index of the vertex opposite the entry edge
    for _ in range(100000):
        if hit is not None:            # ray runs along an edge into vertex `hit`
            ev = vertex_event(room_t, unf_t, hit)
            if ev:
                return ev
            pivot = hit
            room_t, unf_t, hit = enter_at_vertex(room_t, unf_t, pivot)
            entry = None
            continue
        if entry is None:
            exit_i = pivot             # entered at vertex `pivot`, leaves through the opposite edge
        else:
            s = side(unf_t[entry])     # entered through the edge opposite `entry`
            if s == 0:
                ev = vertex_event(room_t, unf_t, entry)
                if ev:
                    return ev
                pivot = entry
                room_t, unf_t, hit = enter_at_vertex(room_t, unf_t, pivot)
                entry = None
                continue
            o = [j for j in range(3) if j != entry]
            exit_i = next(j for j in o if side(unf_t[j]) == s)
        if min(along(p) for p in unf_t) > L2:
            return ('MISS',)
        room_t, unf_t = step(room_t, unf_t, exit_i)
        entry = exit_i
    raise ArithmeticError("shooter did not terminate")


def a_images(g, depth, radius):
    """A-class points of all images of the base tile under at most `depth` side reflections."""
    seen = {g.base}
    frontier = [g.base]
    pts = {g.base[0]}
    for _ in range(depth):
        nxt = []
        for t in frontier:
            for i in range(3):
                u = g.reflect_tile(t, i)
                if u not in seen and abs(g.cx(u[0])) <= radius:
                    seen.add(u)
                    nxt.append(u)
                    pts.add(u[0])
        frontier = nxt
    return pts
