"""Exact geometry for rooms tiled by a Wolecki triangle (1, b, c) * pi/n.

Independent of d7-wolecki-triangles. Points are elements of Z[zeta], zeta =
exp(i pi / n), stored as integer tuples in the power basis modulo the
cyclotomic polynomial Phi_{2n}. Zero tests are exact. Signs of nonzero real
algebraic integers come from a float evaluation that is certified against
the norm bound |x| >= L^-(phi/2 - 1) (L = l1 norm of the coefficients); when
the float is not conclusive, a 80-digit Decimal evaluation is used and must
clear the same bound.
"""
import math
from decimal import Decimal, getcontext
from functools import lru_cache


def cyclotomic(N):
    """Integer coefficients (low to high) of Phi_N."""
    # x^N - 1 = prod_{d | N} Phi_d
    def polydiv(a, b):
        a = a[:]
        q = [0] * (len(a) - len(b) + 1)
        for i in range(len(a) - len(b), -1, -1):
            c = a[i + len(b) - 1] // b[-1]
            q[i] = c
            for j, bj in enumerate(b):
                a[i + j] -= c * bj
        assert all(v == 0 for v in a)
        return q
    p = [-1] + [0] * (N - 1) + [1]
    for d in range(1, N):
        if N % d == 0:
            p = polydiv(p, cyclotomic(d))
    return p


class Field:
    def __init__(self, n):
        self.n = n
        self.N = 2 * n
        phi = cyclotomic(self.N)
        self.deg = d = len(phi) - 1
        assert phi[-1] == 1
        # reduced vectors of zeta^k for 0 <= k < 2N
        pw = []
        cur = [1] + [0] * (d - 1)
        for k in range(2 * self.N + 2 * d):
            pw.append(tuple(cur))
            # multiply by zeta
            top = cur[-1]
            nxt = [0] + cur[:-1]
            if top:
                for j in range(d):
                    nxt[j] -= top * phi[j]
            cur = nxt
        self.pw = pw
        assert pw[self.N] == pw[0]
        self.zero = tuple([0] * d)
        self.one = pw[0]
        self.cos = [math.cos(math.pi * k / n) for k in range(d)]
        self.sin = [math.sin(math.pi * k / n) for k in range(d)]
        getcontext().prec = 90
        pi = _dec_pi()
        self.dcos = [_dec_cos(pi * k / n) for k in range(d)]
        self.dsin = [_dec_cos(pi * k / n - pi / 2) for k in range(d)]

    def z(self, k):
        return self.pw[k % self.N]

    def add(self, a, b):
        return tuple(x + y for x, y in zip(a, b))

    def sub(self, a, b):
        return tuple(x - y for x, y in zip(a, b))

    def neg(self, a):
        return tuple(-x for x in a)

    def smul(self, s, a):
        return tuple(s * x for x in a)

    def mul(self, a, b):
        d = self.deg
        acc = [0] * (2 * d - 1)
        for i, x in enumerate(a):
            if x:
                for j, y in enumerate(b):
                    if y:
                        acc[i + j] += x * y
        res = list(acc[:d])
        for k in range(d, 2 * d - 1):
            c = acc[k]
            if c:
                v = self.pw[k]
                for j in range(d):
                    res[j] += c * v[j]
        return tuple(res)

    def conj(self, a):
        res = [0] * self.deg
        for k, x in enumerate(a):
            if x:
                v = self.pw[(self.N - k) % self.N]
                for j in range(self.deg):
                    res[j] += x * v[j]
        return tuple(res)

    def cval(self, a):
        re = math.fsum(x * c for x, c in zip(a, self.cos))
        im = math.fsum(x * s for x, s in zip(a, self.sin))
        return complex(re, im)

    def _sign_part(self, a, part):
        """Exact sign of Re(a) (part=0) or Im(a) (part=1)."""
        # 2 Re a = a + conj a ; 2 i Im a = a - conj a
        ca = self.conj(a)
        w = self.add(a, ca) if part == 0 else self.sub(a, ca)
        if not any(w):
            return 0
        tab = self.cos if part == 0 else self.sin
        v = math.fsum(x * c for x, c in zip(a, tab))
        L = sum(abs(x) for x in w) + 1
        if abs(v) > L * 1e-12:
            return 1 if v > 0 else -1
        dtab = self.dcos if part == 0 else self.dsin
        dv = sum(Decimal(x) * c for x, c in zip(a, dtab))
        bound = Decimal(L) ** (-(self.deg // 2))
        assert abs(dv) > bound * Decimal("1e-3"), (a, dv)
        return 1 if dv > 0 else -1

    def sign_re(self, a):
        return self._sign_part(a, 0)

    def sign_im(self, a):
        return self._sign_part(a, 1)

    def cross_sign(self, p, q):
        """sign of Im(conj(p) q) = sign of the 2D cross product p x q."""
        return self.sign_im(self.mul(self.conj(p), q))

    def dot_sign(self, p, q):
        return self.sign_re(self.mul(self.conj(p), q))

    def two_sin(self, j):
        """2 sin(j pi / n) as an element of Z[zeta]."""
        n = self.n
        return self.sub(self.z(3 * n // 2 + j), self.z(3 * n // 2 - j))


def _dec_pi():
    getcontext().prec += 2
    three = Decimal(3)
    lasts, t, s, n, na, d, da = 0, three, 3, 1, 0, 0, 24
    while s != lasts:
        lasts = s
        n, na = n + na, na + 8
        d, da = d + da, da + 32
        t = (t * n) / d
        s += t
    getcontext().prec -= 2
    return +s


def _dec_cos(x):
    getcontext().prec += 2
    i, lasts, s, fact, num, sign = 0, 0, 1, 1, 1, 1
    while s != lasts:
        lasts = s
        i += 2
        fact *= i * (i - 1)
        num *= x * x
        sign *= -1
        s += num / fact * sign
    getcontext().prec -= 2
    return +s


@lru_cache(None)
def field(n):
    return Field(n)


class Triangle:
    """Angles (1, b, c) * pi/n at A, B, C. A at 0, B = R on the real axis,
    C = r * zeta. R = 2 sin(c u), r = 2 sin(b u), |BC| = 2 sin u."""

    def __init__(self, n, b):
        self.n, self.b = n, b
        self.c = n - 1 - b
        assert 0 < self.b and 0 < self.c
        self.F = F = field(n)
        self.R = F.two_sin(self.c)
        self.r = F.two_sin(self.b)
        self.ang = {"A": 1, "B": self.b, "C": self.c}
        # obstruction set E: angle pi/q with q even
        self.E = {V for V in "BC" if n % self.ang[V] == 0 and (n // self.ang[V]) % 2 == 0}
        self.Rc = F.cval(self.R).real
        self.rc = F.cval(self.r).real


class Tile:
    """Image of the base triangle under z -> zeta^k z + t (s=+1) or
    z -> zeta^k conj(z) + t (s=-1). Hashable by (s, k mod 2n, t)."""
    __slots__ = ("s", "k", "t", "V", "key", "fl", "box")

    def __init__(self, tri, s, k, t):
        F = tri.F
        self.s, self.k, self.t = s, k % F.N, t
        A = t
        B = F.add(F.mul(F.z(k), tri.R), t)
        C = F.add(F.mul(F.z(k + s), tri.r), t)
        self.V = {"A": A, "B": B, "C": C}
        self.key = (s, self.k, t)
        self.fl = [F.cval(A), F.cval(B), F.cval(C)]
        xs = [p.real for p in self.fl]
        ys = [p.imag for p in self.fl]
        self.box = (min(xs), max(xs), min(ys), max(ys))

    def edge_dir_index(self, tri, e):
        """Index j with the edge line of e ('AB','AC','BC') parallel to zeta^j."""
        n = tri.n
        if e == "AB":
            return self.k
        if e == "AC":
            return self.k + self.s
        return self.k + self.s * (n - tri.b)

    def __hash__(self):
        return hash(self.key)

    def __eq__(self, o):
        return self.key == o.key


EDGES = ("AB", "AC", "BC")


def reflect_point(F, z, p, j):
    """Reflect z across the line through p parallel to zeta^j."""
    return F.add(p, F.mul(F.z(2 * j), F.conj(F.sub(z, p))))


def mirror(tri, tile, e):
    """The tile obtained by reflecting `tile` across its edge e."""
    F = tri.F
    j = tile.edge_dir_index(tri, e)
    p = tile.V[e[0]]
    t2 = reflect_point(F, tile.t, p, j)
    return Tile(tri, -tile.s, 2 * j - tile.k, t2)


def star(tri, center):
    """The 2n tiles around an A point at `center`."""
    F = tri.F
    tiles = []
    for k in range(0, tri.n * 2, 2):
        tiles.append(Tile(tri, +1, k, center))
        tiles.append(Tile(tri, -1, k + 2, center))
    # s=+1, k even: AB at angle k, AC at k+1; s=-1, k+2: AB at k+2, AC at k+1
    return tiles


def boxes_meet(b1, b2, eps=1e-9):
    return not (b1[1] < b2[0] - eps or b2[1] < b1[0] - eps or b1[3] < b2[2] - eps or b2[3] < b1[2] - eps)


def _on_open_segment(F, p, a, b):
    d = F.sub(b, a)
    w = F.sub(p, a)
    if F.cross_sign(d, w) != 0:
        return False
    s1 = F.dot_sign(d, w)
    s2 = F.dot_sign(d, F.sub(p, b))
    return s1 > 0 and s2 < 0


def compatible(tri, t1, t2):
    """True iff t1 and t2 can both be tiles of one room: interiors disjoint,
    labels agree at coincident vertices, and no vertex of one lies in the
    relative interior of an edge of the other."""
    if t1.key == t2.key:
        return True
    if not boxes_meet(t1.box, t2.box):
        return True
    F = tri.F
    pos1 = {v: l for l, v in t1.V.items()}
    pos2 = {v: l for l, v in t2.V.items()}
    for v, l in pos1.items():
        if v in pos2 and pos2[v] != l:
            return False
    for (ta, tb) in ((t1, t2), (t2, t1)):
        for l, p in ta.V.items():
            for e in EDGES:
                a, b = tb.V[e[0]], tb.V[e[1]]
                if p == a or p == b:
                    continue
                if _on_open_segment(F, p, a, b):
                    return False
    # separating axis test on the 6 edge directions
    P1 = list(t1.V.values())
    P2 = list(t2.V.values())
    for ta in (t1, t2):
        for e in EDGES:
            d = F.sub(ta.V[e[1]], ta.V[e[0]])
            sg = set()
            for p in P1:
                for q in P2:
                    sg.add(F.cross_sign(d, F.sub(p, q)))
            if not (1 in sg and -1 in sg):
                return True
    return False


class Room:
    """Analysis of a finite tile set. Call valid() first."""

    def __init__(self, tri, tiles):
        self.tri = tri
        self.tiles = list(tiles)

    def analyze(self, check_pairs=True):
        tri, F = self.tri, self.tri.F
        tiles = self.tiles
        self.err = None
        if check_pairs:
            for i in range(len(tiles)):
                for j in range(i + 1, len(tiles)):
                    if not compatible(tri, tiles[i], tiles[j]):
                        self.err = "incompatible pair"
                        return False
        vlabel = {}
        vang = {}
        vtiles = {}
        edges = {}
        for idx, t in enumerate(tiles):
            for l, p in t.V.items():
                if vlabel.setdefault(p, l) != l:
                    self.err = "label clash"
                    return False
                vang[p] = vang.get(p, 0) + tri.ang[l]
                vtiles.setdefault(p, []).append(idx)
            for e in EDGES:
                a, b = t.V[e[0]], t.V[e[1]]
                key = (a, b) if a < b else (b, a)
                edges.setdefault(key, []).append(idx)
        # edge multiplicity and adjacency
        adj = {i: set() for i in range(len(tiles))}
        bnd = []
        for key, lst in edges.items():
            if len(lst) > 2:
                self.err = "edge multiplicity"
                return False
            if len(lst) == 2:
                adj[lst[0]].add(lst[1])
                adj[lst[1]].add(lst[0])
            else:
                bnd.append(key)
        # connectivity
        seen = {0}
        stack = [0]
        while stack:
            i = stack.pop()
            for j in adj[i]:
                if j not in seen:
                    seen.add(j)
                    stack.append(j)
        if len(seen) != len(tiles):
            self.err = "not edge-connected"
            return False
        # boundary: one simple cycle
        deg = {}
        nbr = {}
        for a, b in bnd:
            deg[a] = deg.get(a, 0) + 1
            deg[b] = deg.get(b, 0) + 1
            nbr.setdefault(a, []).append(b)
            nbr.setdefault(b, []).append(a)
        if any(d != 2 for d in deg.values()):
            self.err = "pinch"
            return False
        start = bnd[0][0]
        cyc = [start]
        prev, cur = None, start
        while True:
            a, b = nbr[cur]
            nxt = a if a != prev else b
            if nxt == start:
                break
            cyc.append(nxt)
            prev, cur = cur, nxt
            if len(cyc) > len(bnd) + 1:
                break
        if len(cyc) != len(bnd):
            self.err = "boundary not one cycle"
            return False
        n = tri.n
        bset = set(deg)
        for p, a in vang.items():
            if p in bset:
                if a >= 2 * n:
                    self.err = "boundary angle >= 2pi"
                    return False
            elif a != 2 * n:
                self.err = "interior angle != 2pi"
                return False
        # orientation and area identity (float, as a cross-check only)
        pts = [F.cval(p) for p in cyc]
        area = 0.5 * sum((pts[i].conjugate() * pts[(i + 1) % len(pts)]).imag for i in range(len(pts)))
        tarea = 0.5 * tri.Rc * tri.rc * math.sin(math.pi / n) * len(tiles)
        if abs(abs(area) - tarea) > 1e-6 * tarea:
            self.err = "area mismatch"
            return False
        self.cycle = cyc
        self.vlabel, self.vang, self.vtiles = vlabel, vang, vtiles
        self.bset = bset
        self.corners = [p for p in cyc if vang[p] != n]
        self.W = len(self.corners)
        turning = sum(n - vang[p] for p in self.corners)
        if turning != 2 * n:
            self.err = "turning sum"
            return False
        self.interiorA = [p for p, l in vlabel.items() if l == "A" and p not in bset]
        self.transparentE = [p for p, l in vlabel.items() if l in tri.E and (p not in bset or vang[p] == n)]
        self.clean = not self.transparentE
        self.edges = edges
        return True

    def walls(self):
        """List of walls as (P, Q, j) with the line parallel to zeta^j."""
        tri, F = self.tri, self.tri.F
        cyc = self.cycle
        cs = set(self.corners)
        idx = [i for i, p in enumerate(cyc) if p in cs]
        res = []
        for a in range(len(idx)):
            i0, i1 = idx[a], idx[(a + 1) % len(idx)]
            P, Q = cyc[i0], cyc[i1]
            # direction index from the boundary tile edge at P
            nxt = cyc[(i0 + 1) % len(cyc)]
            key = (P, nxt) if P < nxt else (nxt, P)
            t = self.tiles[self.edges[key][0]]
            lab = {t.V[e]: e for e in "ABC"}
            e = "".join(sorted(lab[P] + lab[nxt]))
            j = t.edge_dir_index(tri, e)
            res.append((P, Q, j))
        return res

    def summary(self):
        from collections import Counter
        ct = Counter(self.vlabel[p] + str(self.vang[p] // self.tri.ang[self.vlabel[p]]) for p in self.corners)
        return dict(sorted(ct.items()))
