"""D114 exact orthogonal-room tracer (Fractions). Written for this review; shares no code
with d103, d109, d112 or d113."""
from fractions import Fraction as Fr


def rect(x0, x1, y0, y1):
    return {(x, y) for x in range(x0, x1) for y in range(y0, y1)}


def boundary(C):
    """Counter-clockwise vertex cycle of a union of unit cells. Asserts one cycle and no pinch."""
    nxt = {}
    for x, y in C:
        for a, b, nb in (((x, y), (x + 1, y), (x, y - 1)), ((x + 1, y), (x + 1, y + 1), (x + 1, y)),
                         ((x + 1, y + 1), (x, y + 1), (x, y + 1)), ((x, y + 1), (x, y), (x - 1, y))):
            if nb not in C:
                assert a not in nxt, ('pinch at', a)
                nxt[a] = b
    start = min(nxt)
    cyc = [start]
    while nxt[cyc[-1]] != start:
        cyc.append(nxt[cyc[-1]])
    assert len(cyc) == len(nxt), 'boundary has more than one component'
    n = len(cyc)
    V = [cyc[i] for i in range(n)
         if (cyc[i - 1][0] == cyc[i][0]) != (cyc[i][0] == cyc[(i + 1) % n][0])]
    return V


def reflex(V):
    n = len(V); out = []
    for i in range(n):
        a, b, c = V[i - 1], V[i], V[(i + 1) % n]
        cross = (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])
        if cross < 0:
            out.append(b)
    return out


class Corner(Exception):
    pass


class Room:
    def __init__(self, C):
        self.C = C
        self.V = boundary(C)
        Vf = [(Fr(x), Fr(y)) for x, y in self.V]
        self.Vset = set(Vf)
        E = list(zip(Vf, Vf[1:] + Vf[:1]))
        self.vert = [(a[0], min(a[1], b[1]), max(a[1], b[1])) for a, b in E if a[0] == b[0]]
        self.horz = [(a[1], min(a[0], b[0]), max(a[0], b[0])) for a, b in E if a[1] == b[1]]
        self.W = len(self.V)
        self.r = len(reflex(self.V))

    def next_hit(self, p, d):
        best = None
        if d[0]:
            for x, lo, hi in self.vert:
                t = (x - p[0]) / d[0]
                if t > 0 and (best is None or t < best[0]):
                    y = p[1] + t * d[1]
                    if lo <= y <= hi:
                        best = (t, 'v', (x, y))
        if d[1]:
            for y, lo, hi in self.horz:
                t = (y - p[1]) / d[1]
                if t > 0 and (best is None or t < best[0]):
                    x = p[0] + t * d[0]
                    if lo <= x <= hi:
                        best = (t, 'h', (x, y))
        return best

    def shoot(self, p, d, stop, maxev=200000):
        """Unit time = one copy of d. stop(p, q, d, t0) -> value or None per straight segment, where
        t0 is elapsed time at p. Returns (value, bounces, elapsed). Raises Corner(vertex, elapsed)."""
        p = (Fr(p[0]), Fr(p[1])); d = (Fr(d[0]), Fr(d[1])); t0 = Fr(0); nb = 0
        for _ in range(maxev):
            t, k, q = self.next_hit(p, d)
            r = stop(p, q, d, t0)
            if r is not None:
                return r, nb, t0
            if q in self.Vset:
                raise Corner(q, t0 + t)
            nb += 1; t0 += t
            d = (-d[0], d[1]) if k == 'v' else (d[0], -d[1])
            p = q
        return None, nb, t0


def reach(T):
    T = (Fr(T[0]), Fr(T[1]))
    def f(p, q, d, t0):
        if (T[0] - p[0]) * d[1] != (T[1] - p[1]) * d[0]:
            return None
        lam = (T[0] - p[0]) / d[0] if d[0] else (T[1] - p[1]) / d[1]
        lq = (q[0] - p[0]) / d[0] if d[0] else (q[1] - p[1]) / d[1]
        if 0 < lam <= lq:
            return ('reach', t0 + lam)
        return None
    return f


def cross_x(X, sense, count=1):
    """Stop at the count-th strict crossing of x=X with horizontal velocity sign `sense`.
    Returns (y, vertical sign, elapsed time at the crossing)."""
    X = Fr(X); seen = [0]
    def f(p, q, d, t0):
        if (p[0] - X) * (q[0] - X) < 0 and (d[0] > 0) == (sense > 0):
            seen[0] += 1
            if seen[0] == count:
                lam = (X - p[0]) / d[0]
                return (p[1] + lam * d[1], 1 if d[1] > 0 else -1, t0 + lam)
        return None
    return f


def path_points(room, S, d, T, maxev=200000):
    """Full trace S -> T. Returns list of turning points (S, bounces..., T) and elapsed time."""
    pts = [(Fr(S[0]), Fr(S[1]))]
    def f(p, q, dd, t0):
        r = reach(T)(p, q, dd, t0)
        if r:
            return r
        pts.append(q)
        return None
    r, nb, _ = room.shoot(S, d, f, maxev)
    if r is None:
        return None
    pts.append((Fr(T[0]), Fr(T[1])))
    return pts, r[1]


def crossings(pts, X):
    return sum(1 for a, b in zip(pts, pts[1:]) if (a[0] - X) * (b[0] - X) < 0)
