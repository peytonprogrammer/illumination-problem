"""Review code for d15-small-r/theorems.md (r <= 2).

Written from the lemma statements in theorems.md, not from lemmas.py.

Contents
- field(D): exact arithmetic in Q(sqrt D), with exact comparison.
- Room: an order type (cell set) with real grid coordinates in one field.
- trace(): a wall-by-wall billiard tracer in exact arithmetic. It knows
  nothing about unfolding or lemmas. It takes a start point, an unfolded
  displacement D, and an end point.
- instances(): for a pair of points, every instance of Lemmas A, A2, B, B',
  B2, C (par, perp, same), D whose hypotheses hold, with the candidate paths
  that the proof prescribes.
"""
import math
from fractions import Fraction as Fr

# ----------------------------------------------------------------- field
_FIELDS = {}


def field(D):
    """Class of numbers a + b*sqrt(D), a and b rational, D a non-square integer."""
    if D in _FIELDS:
        return _FIELDS[D]
    sq = math.sqrt(D)
    assert int(sq) ** 2 != D

    class Q:
        __slots__ = ('a', 'b')

        def __init__(self, a=0, b=0):
            self.a = a if type(a) is Fr else Fr(a)
            self.b = b if type(b) is Fr else Fr(b)

        @staticmethod
        def c(o):
            return o if type(o) is Q else Q(o)

        def __add__(s, o):
            o = Q.c(o)
            return Q(s.a + o.a, s.b + o.b)
        __radd__ = __add__

        def __neg__(s):
            return Q(-s.a, -s.b)

        def __sub__(s, o):
            o = Q.c(o)
            return Q(s.a - o.a, s.b - o.b)

        def __rsub__(s, o):
            o = Q.c(o)
            return Q(o.a - s.a, o.b - s.b)

        def __mul__(s, o):
            o = Q.c(o)
            if not s.b:
                return Q(s.a * o.a, s.a * o.b)
            if not o.b:
                return Q(s.a * o.a, s.b * o.a)
            return Q(s.a * o.a + D * s.b * o.b, s.a * o.b + s.b * o.a)
        __rmul__ = __mul__

        def inv(s):
            if not s.b:
                return Q(1 / s.a, 0)
            n = s.a * s.a - D * s.b * s.b
            return Q(s.a / n, -s.b / n)

        def __truediv__(s, o):
            return s * Q.c(o).inv()

        def __rtruediv__(s, o):
            return Q.c(o) * s.inv()

        def sign(s):
            a, b = s.a, s.b
            if not b:
                return (a > 0) - (a < 0)
            if not a:
                return (b > 0) - (b < 0)
            sa = 1 if a > 0 else -1
            sb = 1 if b > 0 else -1
            if sa == sb:
                return sa
            c = a * a - D * b * b          # never 0: D is not a square
            return sa if c > 0 else sb

        def __eq__(s, o):
            o = Q.c(o)
            return s.a == o.a and s.b == o.b

        def __ne__(s, o):
            return not s.__eq__(o)

        def __lt__(s, o):
            return (s - o).sign() < 0

        def __le__(s, o):
            return (s - o).sign() <= 0

        def __gt__(s, o):
            return (s - o).sign() > 0

        def __ge__(s, o):
            return (s - o).sign() >= 0

        def __hash__(s):
            return hash((s.a, s.b))

        def __float__(s):
            return float(s.a) + float(s.b) * sq

        def __abs__(s):
            return s if s.sign() >= 0 else -s

        def floor(s):
            if not s.b:
                return math.floor(s.a)
            f = math.floor(float(s))
            while Q(f) > s:
                f -= 1
            while Q(f + 1) <= s:
                f += 1
            return f

        def ceil(s):
            return -((-s).floor())

        def __repr__(s):
            if not s.b:
                return str(s.a)
            return f"({s.a}{'+' if s.b > 0 else '-'}{abs(s.b)}*sqrt{D})"

    Q.D = D
    _FIELDS[D] = Q
    return Q


def fmax(a, b):
    return a if a >= b else b


def fmin(a, b):
    return a if a <= b else b


# ----------------------------------------------------------------- rooms
TRANSFORMS = [(tr, fx, fy) for tr in (0, 1) for fx in (0, 1) for fy in (0, 1)]


def span(A0, A1):
    """Cell indices that meet the open interval between two distinct real
    values with doubled coordinates A0 <= A1."""
    return range(A0 // 2, (A1 + 1) // 2)


class Room:
    def __init__(self, nx, ny, cells, xs, ys):
        self.nx, self.ny = nx, ny
        self.cells = frozenset(cells)
        self.xs, self.ys = list(xs), list(ys)
        self.coord = (self.xs, self.ys)
        assert len(self.xs) == nx + 1 and len(self.ys) == ny + 1
        assert all(self.xs[i] < self.xs[i + 1] for i in range(nx))
        assert all(self.ys[i] < self.ys[i + 1] for i in range(ny))
        self._walls = None
        self._tf = {}

    def ins(self, i, j):
        return (i, j) in self.cells

    def loc(self, v, axis):
        """Doubled coordinate: 2i on grid line i, 2i+1 strictly between lines i and i+1."""
        arr = self.coord[axis]
        for i, c in enumerate(arr):
            if v == c:
                return 2 * i
            if v < c:
                return 2 * i - 1
        return 2 * len(arr) - 1

    def idx(self, axis, v):
        for i, c in enumerate(self.coord[axis]):
            if c == v:
                return i
        raise ValueError("not a grid value")

    def pt(self, P):
        return (P[0], P[1], self.loc(P[0], 0), self.loc(P[1], 1))

    def interior(self, P):
        X, Y = self.loc(P[0], 0), self.loc(P[1], 1)
        xs = [X // 2] if X % 2 else [X // 2 - 1, X // 2]
        ys = [Y // 2] if Y % 2 else [Y // 2 - 1, Y // 2]
        return all(self.ins(i, j) for i in xs for j in ys)

    def cells_in(self, cols, rows):
        cols, rows = list(cols), list(rows)
        return bool(cols) and bool(rows) and all((i, j) in self.cells for i in cols for j in rows)

    def vwall(self, i, rows):
        """Unit edges of vertical grid line i along the given rows all lie in the boundary."""
        rows = list(rows)
        return bool(rows) and all(self.ins(i - 1, j) != self.ins(i, j) for j in rows)

    def hwall(self, j, cols):
        cols = list(cols)
        return bool(cols) and all(self.ins(i, j - 1) != self.ins(i, j) for i in cols)

    def npt(self, i, j):
        return self.ins(i - 1, j - 1) + self.ins(i, j - 1) + self.ins(i - 1, j) + self.ins(i, j)

    def vertices(self):
        return [(self.xs[i], self.ys[j]) for i in range(self.nx + 1) for j in range(self.ny + 1)
                if self.npt(i, j) in (1, 3)]

    def walls(self):
        """Maximal boundary segments (axis, c, lo, hi). axis 0: the wall x = c, lo <= y <= hi."""
        if self._walls is None:
            out = []
            for i in range(self.nx + 1):
                j = 0
                while j < self.ny:
                    if self.ins(i - 1, j) != self.ins(i, j):
                        j0, side = j, self.ins(i, j)
                        while j < self.ny and self.ins(i - 1, j) != self.ins(i, j) and self.ins(i, j) == side:
                            j += 1
                        out.append((0, self.xs[i], self.ys[j0], self.ys[j]))
                    else:
                        j += 1
            for j in range(self.ny + 1):
                i = 0
                while i < self.nx:
                    if self.ins(i, j - 1) != self.ins(i, j):
                        i0, side = i, self.ins(i, j)
                        while i < self.nx and self.ins(i, j - 1) != self.ins(i, j) and self.ins(i, j) == side:
                            i += 1
                        out.append((1, self.ys[j], self.xs[i0], self.xs[i]))
                    else:
                        i += 1
            self._walls = out
        return self._walls

    def tf(self, g):
        if g not in self._tf:
            tr, fx, fy = g
            cells = []
            for (i, j) in self.cells:
                a = self.nx - 1 - i if fx else i
                b = self.ny - 1 - j if fy else j
                cells.append((b, a) if tr else (a, b))
            xs = [-x for x in reversed(self.xs)] if fx else list(self.xs)
            ys = [-y for y in reversed(self.ys)] if fy else list(self.ys)
            self._tf[g] = Room(self.ny, self.nx, cells, ys, xs) if tr else Room(self.nx, self.ny, cells, xs, ys)
        return self._tf[g]


def tpoint(g, P):
    tr, fx, fy = g
    x, y = P
    if fx:
        x = -x
    if fy:
        y = -y
    return (y, x) if tr else (x, y)


def fwd_line(g, axis, v):
    """Line {coordinate[axis] = v} of the original frame, in the transformed frame."""
    tr, fx, fy = g
    return axis ^ tr, (-v if (fx if axis == 0 else fy) else v)


def back_line(g, axis_t, v):
    """Line {coordinate[axis_t] = v} of the transformed frame, in the original frame."""
    tr, fx, fy = g
    axis = axis_t ^ tr
    return axis, (-v if (fx if axis == 0 else fy) else v)


# ----------------------------------------------------------------- tracer
MAXREF = 3000


def trace(room, S, D, T, maxref=None):
    """Shoot from the interior point S along D. The path has unfolded
    displacement D in total. Returns (status, reflections).
    status: 'ok' (ends at T, no vertex touched, T reached off the walls),
    'vertex', 'miss', 'end-on-wall', 'escape', 'too-long', 'not-interior'."""
    if maxref is None:
        maxref = MAXREF
    if not room.interior(S) or not room.interior(T):
        return 'not-interior', 0
    walls = room.walls()
    px, py = S
    dx, dy = D
    # A path cannot travel farther than the bounding box in x or in y without
    # a reflection. Skip paths that are certain to exceed the cap.
    wbox = float(room.xs[-1] - room.xs[0])
    hbox = float(room.ys[-1] - room.ys[0])
    if abs(float(dx)) / wbox + abs(float(dy)) / hbox - 2 > maxref * 1.01 + 2:
        return 'too-long', maxref
    one = (dx - dx) + 1
    sdx, sdy = dx.sign(), dy.sign()
    if sdx == 0 and sdy == 0:
        return 'miss', 0
    idx = dx.inv() if sdx else None
    idy = dy.inv() if sdy else None
    rem = one
    nref = 0
    while True:
        best = None
        bw = None
        bpt = None
        for w in walls:
            axis, c, lo, hi = w
            if axis == 0:
                if sdx == 0:
                    continue
                diff = c - px
                if diff.sign() != sdx:
                    continue
                tau = diff * idx
                if best is not None and tau > best:
                    continue
                y = py + tau * dy
                if y < lo or y > hi:
                    continue
                hit = (c, y)
                vert = (y == lo or y == hi)
            else:
                if sdy == 0:
                    continue
                diff = c - py
                if diff.sign() != sdy:
                    continue
                tau = diff * idy
                if best is not None and tau > best:
                    continue
                x = px + tau * dx
                if x < lo or x > hi:
                    continue
                hit = (x, c)
                vert = (x == lo or x == hi)
            if best is not None and tau == best:
                bw = (bw[0], True)          # two walls at one point: a vertex
            else:
                best, bw, bpt = tau, (axis, vert), hit
        if best is None:
            return 'escape', nref
        if best > rem:
            end = (px + rem * dx, py + rem * dy)
            return ('ok' if (end[0] == T[0] and end[1] == T[1]) else 'miss'), nref
        if bw[1]:
            return 'vertex', nref
        if best == rem:
            return 'end-on-wall', nref
        px, py = bpt
        rem = rem - best
        if bw[0] == 0:
            dx, idx, sdx = -dx, -idx, -sdx
        else:
            dy, idy, sdy = -dy, -idy, -sdy
        nref += 1
        if nref > maxref:
            return 'too-long', nref


# ----------------------------------------------------------------- arms
def canon_arms(R, P):
    """Canonical frame: the door is on the left side x = x_gd of the hub, the
    flat end is the bottom-left corner of the hub, the corridor runs to the
    left of the door and contains P. Returns index tuples (gd, g1, jb, jh, jt):
    hub = [x_gd, x_g1] x [y_jb, y_jh], door = {x_gd} x [y_jb, y_jt]."""
    x, y, X, Y = R.pt(P)
    out = []
    for gd in range(R.nx + 1):
        if not 2 * gd > X:                      # P is not on the door line and lies left of it
            continue
        for jb in range(R.ny + 1):
            if not 2 * jb < Y:
                continue
            for jt in range(jb + 1, R.ny + 1):
                if not 2 * jt > Y:              # P strictly between the corridor walls
                    continue
                ccols = span(X, 2 * gd)
                if not R.cells_in(ccols, range(jb, jt)):
                    continue                    # corridor [x_P, x_gd] x [y_jb, y_jt] inside P
                if not (R.hwall(jb, ccols) and R.hwall(jt, ccols)):
                    continue                    # both corridor walls in the boundary
                for g1 in range(gd + 1, R.nx + 1):
                    if not R.hwall(jb, range(gd, g1)):   # mirror side: the hub floor is wall
                        continue
                    for jh in range(jt, R.ny + 1):
                        if R.cells_in(range(gd, g1), range(jb, jh)):
                            out.append((gd, g1, jb, jh, jt))
    return out


def arms_all(R, P):
    """All arms of all hubs that contain P as an arm point, in the frame of R.
    Each arm: dict(ad, door, far, F, E, farF) with real values.
    ad = axis perpendicular to the door; the door line is coord[ad] = door; the
    opposite hub side is coord[ad] = far. Along the other axis the door is
    [F, E] (F the flat end) and the hub is [F, farF]."""
    out, seen = [], set()
    for g in TRANSFORMS:
        Rg = R.tf(g)
        Pg = tpoint(g, P)
        for (gd, g1, jb, jh, jt) in canon_arms(Rg, Pg):
            ad, door = back_line(g, 0, Rg.xs[gd])
            _, far = back_line(g, 0, Rg.xs[g1])
            _, F = back_line(g, 1, Rg.ys[jb])
            _, E = back_line(g, 1, Rg.ys[jt])
            _, farF = back_line(g, 1, Rg.ys[jh])
            key = (ad, door, far, F, E, farF)
            if key not in seen:
                seen.add(key)
                out.append(dict(ad=ad, door=door, far=far, F=F, E=E, farF=farF))
    return out


def arm_G(a):
    lo_d, hi_d = (a['door'], a['far']) if a['door'] < a['far'] else (a['far'], a['door'])
    lo_f, hi_f = (a['F'], a['farF']) if a['F'] < a['farF'] else (a['farF'], a['F'])
    return (lo_d, hi_d, lo_f, hi_f) if a['ad'] == 0 else (lo_f, hi_f, lo_d, hi_d)


def arm_flag(a):
    if a['ad'] == 0:
        side = 'L' if a['door'] < a['far'] else 'R'
    else:
        side = 'B' if a['door'] < a['far'] else 'T'
    return side, ('lo' if a['F'] < a['farF'] else 'hi')


def tarm(a, g):
    ad, door = fwd_line(g, a['ad'], a['door'])
    _, far = fwd_line(g, a['ad'], a['far'])
    _, F = fwd_line(g, 1 - a['ad'], a['F'])
    _, E = fwd_line(g, 1 - a['ad'], a['E'])
    _, farF = fwd_line(g, 1 - a['ad'], a['farF'])
    return dict(ad=ad, door=door, far=far, F=F, E=E, farF=farF)


def _canon_table():
    tab = {}
    for side in 'LRBT':
        for flat in ('lo', 'hi'):
            ad = 0 if side in 'LR' else 1
            door, far = (0, 5) if side in 'LB' else (5, 0)
            F, farF = (0, 7) if flat == 'lo' else (7, 0)
            a = dict(ad=ad, door=door, far=far, F=F, E=(F + farF) // 2 if False else (3 if flat == 'lo' else 4), farF=farF)
            for g in TRANSFORMS:
                if arm_flag(tarm(a, g)) == ('L', 'lo'):
                    assert (side, flat) not in tab
                    tab[(side, flat)] = g
    assert len(tab) == 8
    return tab


CANON = _canon_table()


# ----------------------------------------------------------------- lemma instances
FLAGS = []
import random as _random
RNG = _random.Random(12345)
KLIMIT = 8


def pick_ks(lo, hi):
    """Integers k with lo < k < hi. Returns (sample, count). When the window
    holds more than KLIMIT integers (a viewer very near the door line), the
    sample is the two extreme values, the values nearest 0, and random ones."""
    k0 = lo.floor() + 1
    k1 = hi.ceil() - 1
    n = k1 - k0 + 1
    if n <= 0:
        return [], 0
    if n <= KLIMIT:
        return list(range(k0, k1 + 1)), n
    ks = {k0, k1, k0 + 1, k1 - 1}
    c = min(max(0, k0), k1)
    ks.update(k for k in (c - 1, c, c + 1) if k0 <= k <= k1)
    while len(ks) < KLIMIT:
        ks.add(RNG.randint(k0, k1))
    return sorted(ks), n


def tpoint_inv(g, P):
    tr, fx, fy = g
    x, y = (P[1], P[0]) if tr else P
    if fx:
        x = -x
    if fy:
        y = -y
    return (x, y)


def fold(v, lo, hi):
    """Fold a real value into [lo, hi] by reflections in lo and hi."""
    w = hi - lo
    u = v - lo
    u = u - 2 * w * (u / (2 * w)).floor()
    if u > w:
        u = 2 * w - u
    return lo + u

def _vertex_on_open_segment(R, S, T):
    dx, dy = T[0] - S[0], T[1] - S[1]
    for (vx, vy) in R.vertices():
        ax, ay = vx - S[0], vy - S[1]
        if (ax * dy - ay * dx).sign() != 0:
            continue
        dot = ax * dx + ay * dy
        if dot.sign() > 0 and (dot - (dx * dx + dy * dy)).sign() < 0:
            return True
    return False


def inst_A(R, S, T):
    s, t = R.pt(S), R.pt(T)
    X0, X1 = sorted((s[2], t[2]))
    Y0, Y1 = sorted((s[3], t[3]))

    def opts(A0, A1, same):
        if not same:
            return [span(A0, A1)]
        if A0 % 2:
            return [[A0 // 2]]
        return [[A0 // 2 - 1], [A0 // 2]]
    co = opts(X0, X1, S[0] == T[0])
    ro = opts(Y0, Y1, S[1] == T[1])
    if not any(R.cells_in(c, r) for c in co for r in ro):
        return []
    if _vertex_on_open_segment(R, S, T):
        if S[0] != T[0] and S[1] != T[1]:
            FLAGS.append(('A: vertex on a non-axis-parallel segment inside a common rectangle', S, T))
        return []
    return [dict(lem='A', key=('A',), g=TRANSFORMS[0], a=S, b=T,
                 cands=[('seg', (T[0] - S[0], T[1] - S[1]))])]


def inst_A2(R, S, T):
    out = []
    for g in TRANSFORMS:
        Rg = R.tf(g)
        s, t = Rg.pt(tpoint(g, S)), Rg.pt(tpoint(g, T))
        if not (s[1] == t[1] and s[0] < t[0]):
            continue
        cols = span(s[2], t[2])
        for j in range(Rg.ny + 1):
            if not 2 * j < s[3]:
                continue
            if Rg.cells_in(cols, span(2 * j, s[3])) and Rg.hwall(j, cols):
                yw = Rg.ys[j]
                ax, val = back_line(g, 1, yw)
                out.append(dict(lem='A2', key=('A2', ax, val), g=g, a=s[:2], b=t[:2],
                                cands=[('V', (t[0] - s[0], 2 * (yw - s[1])))]))
    return out


def _corridor_up(Rg, s, t, need_flat):
    """Canonical frame of Lemmas B and B': corridor [p, q] x [d, t2] with its
    two sides in the boundary, T strictly between the sides and above the door
    line y = d, viewer S below the door line. Yields (ip, iq, jd)."""
    for ip in range(Rg.nx + 1):
        if not 2 * ip < t[2]:
            continue
        for iq in range(ip + 1, Rg.nx + 1):
            if not 2 * iq > t[2]:
                continue
            for jd in range(Rg.ny + 1):
                if not (s[3] < 2 * jd < t[3]):
                    continue
                rows = span(2 * jd, t[3])
                if not (Rg.cells_in(range(ip, iq), rows) and Rg.vwall(ip, rows) and Rg.vwall(iq, rows)):
                    continue
                yield ip, iq, jd


def inst_B(R, S, T):
    out = []
    for swap, (A, B) in enumerate(((S, T), (T, S))):       # A viewer, B corridor point
        for g in TRANSFORMS:
            Rg = R.tf(g)
            s, t = Rg.pt(tpoint(g, A)), Rg.pt(tpoint(g, B))
            for ip, iq, jd in _corridor_up(Rg, s, t, True):
                if not s[2] > 2 * ip:                       # hypothesis 3: s1 > p
                    continue
                rows2 = span(s[3], 2 * jd)
                if not Rg.cells_in(span(2 * ip, max(2 * iq, s[2])), rows2):   # hypothesis 4: Q*
                    continue
                if not Rg.vwall(ip, rows2):                 # hypothesis 5: flat end
                    continue
                p, q, d = Rg.xs[ip], Rg.xs[iq], Rg.ys[jd]
                w = q - p
                lam = (d - s[1]) / (t[1] - s[1])
                cands = []
                per_sign = {}
                for eps in (1, -1):
                    base = p + eps * (t[0] - p)
                    lo = ((p - w - s[0]) / lam + s[0] - base) / (2 * w)
                    hi = ((p + w - s[0]) / lam + s[0] - base) / (2 * w)
                    ks, per_sign[eps] = pick_ks(lo, hi)
                    for k in ks:
                        cands.append(((eps, k), (base + 2 * w * k - s[0], t[1] - s[1])))
                axp, pv = back_line(g, 0, p)
                _, qv = back_line(g, 0, q)
                _, dv = back_line(g, 1, d)
                out.append(dict(lem='B', key=('B', swap, axp, pv, qv, dv), g=g, a=s[:2], b=t[:2],
                                cands=cands, per_sign=per_sign, geo=dict(p=p, q=q, d=d)))
    return out


def inst_Bp(R, S, T):
    """Lemma B' (near viewer). Not used by certificates; tested as a statement."""
    out = []
    for swap, (A, B) in enumerate(((S, T), (T, S))):
        for g in TRANSFORMS:
            Rg = R.tf(g)
            s, t = Rg.pt(tpoint(g, A)), Rg.pt(tpoint(g, B))
            for ip, iq, jd in _corridor_up(Rg, s, t, False):
                p, q, d = Rg.xs[ip], Rg.xs[iq], Rg.ys[jd]
                # bounding box of S and the door [p, q] x {d}
                X0, X1 = min(2 * ip, s[2]), max(2 * iq, s[2])
                if not Rg.cells_in(span(X0, X1), span(s[3], 2 * jd)):
                    continue
                if not (d - s[1] <= t[1] - d):
                    continue
                strict = d - s[1] < t[1] - d
                w = q - p
                lam = (d - s[1]) / (t[1] - s[1])
                cands = []
                per_sign = {}
                for eps in (1, -1):
                    base = p + eps * (t[0] - p)
                    lo = ((p - s[0]) / lam + s[0] - base) / (2 * w)        # x* in the open door (p, q)
                    hi = ((q - s[0]) / lam + s[0] - base) / (2 * w)
                    ks, per_sign[eps] = pick_ks(lo, hi)
                    for k in ks:
                        cands.append(((eps, k), (base + 2 * w * k - s[0], t[1] - s[1])))
                axp, pv = back_line(g, 0, p)
                _, qv = back_line(g, 0, q)
                _, dv = back_line(g, 1, d)
                out.append(dict(lem="B'", key=("B'", swap, axp, pv, qv, dv), g=g, a=s[:2], b=t[:2],
                                cands=cands, per_sign=per_sign, strict=strict))
    return out


def inst_B2(R, S, T, arms):
    out = []
    for swap, (A, B) in enumerate(((S, T), (T, S))):       # A viewer in the hub, B arm point
        for arm in arms[B]:
            g = CANON[arm_flag(arm)]
            Rg = R.tf(g)
            ca = tarm(arm, g)
            gx0, gx1, gy0, gy1 = arm_G(ca)
            s, t = tpoint(g, A), tpoint(g, B)
            if not (gx0 <= s[0] <= gx1 and gy0 <= s[1] <= gy1):
                continue                                    # viewer in the closed hub
            i1 = Rg.idx(0, gx1)
            if not Rg.vwall(i1, range(Rg.idx(1, gy0), Rg.idx(1, gy1))):
                continue                                    # side opposite the door is wall
            w = ca['E'] - gy0
            assert w.sign() > 0 and ca['door'] == gx0 and ca['F'] == gy0 and t[0] < gx0
            XT = 2 * gx1 - t[0]
            lam = (2 * gx1 - gx0 - s[0]) / (XT - s[0])
            cands = []
            per_sign = {}
            corner = {}
            for eps in (1, -1):
                base = gy0 + eps * (t[1] - gy0)
                lo = ((gy0 - w - s[1]) / lam + s[1] - base) / (2 * w)
                hi = ((gy0 + w - s[1]) / lam + s[1] - base) / (2 * w)
                ks, per_sign[eps] = pick_ks(lo, hi)
                # the corner case of the proof: the segment passes through (gx1, gy0).
                # Always include that k if it is in the window.
                yc = s[1] + (gy0 - s[1]) * (XT - s[0]) / (gx1 - s[0]) if s[0] < gx1 else None
                if yc is not None:
                    kc = (yc - base) / (2 * w)
                    if kc.b == 0 and kc.a.denominator == 1 and lo < kc.a and hi > kc.a and int(kc.a) not in ks:
                        ks.append(int(kc.a))
                for k in ks:
                    Dv = (XT - s[0], base + 2 * w * k - s[1])
                    cands.append(((eps, k), Dv))
                    cr = (gx1 - s[0]) * Dv[1] - (gy0 - s[1]) * Dv[0]
                    corner[(eps, k)] = (cr.sign() == 0)
            al, Fv = back_line(g, 1, ca['F'])
            _, Ev = back_line(g, 1, ca['E'])
            _, oppv = back_line(g, 0, gx1)
            _, doorv = back_line(g, 0, gx0)
            out.append(dict(lem='B2', key=('B2', swap, al, Fv, Ev, oppv, doorv), g=g, a=s, b=t,
                            cands=cands, per_sign=per_sign, corner=corner,
                            geo=dict(gx0=gx0, gx1=gx1, gy0=gy0, gy1=gy1, w=w)))
    return out


CSTATS = {'bisect': 0, 'bisect-failed': 0}
_SQ = {}


def _ap(x):
    """Rational approximation of a field element, about 60 digits."""
    if not x.b:
        return x.a
    D = type(x).D
    if D not in _SQ:
        _SQ[D] = Fr(math.isqrt(D * 10 ** 120), 10 ** 60)
    return x.a + x.b * _SQ[D]


def _bisect(fun, lo, hi, rising):
    """Zero of a piecewise monotone function whose jumps all go against its
    trend (Lemma C). fun(k) returns (value, M, N) with M, N the integer branch
    indices. Keeps sign(fun(lo)) != sign(fun(hi)) and stops when both ends are
    on one branch. Returns (M, N) or None."""
    sg = 1 if rising else -1
    vl, vh = fun(lo), fun(hi)
    if not (sg * vl[0] < 0 < sg * vh[0]):
        return None
    for _ in range(4000):
        if vl[1:] == vh[1:]:
            return vl[1:]
        mid = (lo + hi) / 2
        vm = fun(mid)
        if vm[0] == 0:
            return vm[1:]
        if sg * vm[0] < 0:
            lo, vl = mid, vm
        else:
            hi, vh = mid, vm
    return None


def _par_window(sx, tx, gx0, gx1, f1, w1, f2, w2, sig):
    t1 = (gx0 - sx) / (tx - sx)
    t2 = (gx1 - sx) / (tx - sx)
    lo = fmax(sig + (f1 - w1 - sig) / t1, sig + (f2 - w2 - sig) / t2)
    hi = fmin(sig + (f1 + w1 - sig) / t1, sig + (f2 + w2 - sig) / t2)
    return lo, hi


def _par_fallback(sx, sy, tx, ty, gx0, gx1, f1, w1, f2, w2, eps1, eps2):
    """The zero of Phi from the proof of Lemma C, par form, found by bisection
    on rational approximations. The result (m, n) is then checked exactly."""
    s0 = f1 + eps1 * (sy - f1)
    t0 = f2 + eps2 * (ty - f2)
    A, B, L = _ap(gx0 - sx), _ap(tx - gx1), _ap(gx1 - gx0)
    S0, T0, F1, W1, F2, W2 = _ap(s0), _ap(t0), _ap(f1), _ap(w1), _ap(f2), _ap(w2)

    def phi(k):
        M = math.floor((S0 + A * k - (F1 - W1)) / (2 * W1))
        N = math.floor((F2 + W2 - (T0 - B * k)) / (2 * W2))
        a = S0 + A * k - 2 * W1 * M
        b = T0 - B * k + 2 * W2 * N
        return ((b - a) / L - k, M, N)

    K = (abs(F2 - F1) + W1 + W2) / L + 1
    r = _bisect(phi, -K, K, rising=False)
    if r is None:
        return None
    m, n = -r[0], r[1]
    sig = s0 + 2 * w1 * m
    th = t0 + 2 * w2 * n
    lo, hi = _par_window(sx, tx, gx0, gx1, f1, w1, f2, w2, sig)
    if lo < th and th < hi:
        return (m, n, (tx - sx, eps1 * (th - sig)))
    return None


def _perp_window(sx, ty, gx0, gx1, gy0, gy1, w1, w2, sig):
    t2 = (gy1 - sig) / (ty - sig)
    lo = sx + (gx1 - w2 - sx) / t2
    hi = sx + (gx1 + w2 - sx) / t2
    num = (gx0 - sx) * (ty - sig)
    lo = fmax(lo, sx + num / (gy0 + w1 - sig))
    dn = gy0 - w1 - sig
    if dn.sign() > 0:
        hi = fmin(hi, sx + num / dn)
    return lo, hi


def _perp_fallback(sx, sy, tx, ty, gx0, gx1, gy0, gy1, w1, w2, eps1, eps2):
    """The zero of F from the proof of Lemma C, perp form, by bisection."""
    s0 = gy0 + eps1 * (sy - gy0)
    t0 = gx1 + eps2 * (tx - gx1)
    A, B = _ap(gx0 - sx), _ap(ty - gy1)
    S0, T0, W1, W2 = _ap(s0), _ap(t0), _ap(w1), _ap(w2)
    GX0, GX1, GY0, GY1 = _ap(gx0), _ap(gx1), _ap(gy0), _ap(gy1)

    def F(k):
        M = math.floor((S0 + A * k - (GY0 - W1)) / (2 * W1))
        N = math.floor((T0 - B / k - (GX1 - W2)) / (2 * W2))
        a = S0 + A * k - 2 * W1 * M
        b = T0 - B / k - 2 * W2 * N
        return (k * (b - GX0) + a - GY1, M, N)

    klo = min((GY0 + W1 - S0) / A, (GY1 - S0) / (GX1 - GX0 + W2 + A)) / 2
    khi = 2 * max(B / (T0 - GX1 + W2), (B + W1 + GY1 - GY0) / (T0 - GX0)) + 1
    r = _bisect(F, klo, khi, rising=True)
    if r is None:
        return None
    m, n = -r[0], -r[1]
    sig = s0 + 2 * w1 * m
    th = t0 + 2 * w2 * n
    if not sig < gy0 + w1:
        return None
    lo, hi = _perp_window(sx, ty, gx0, gx1, gy0, gy1, w1, w2, sig)
    if lo < th and th < hi:
        return (m, n, (th - sx, eps1 * (ty - sig)))
    return None


def _solve_par(sx, sy, tx, ty, gx0, gx1, f1, w1, f2, w2, eps1, eps2, rng, cap=400):
    """All (m, n) such that the segment from the image of S to the image of T
    crosses x = gx0 inside (f1 - w1, f1 + w1) and x = gx1 inside
    (f2 - w2, f2 + w2). Returns (solutions sorted by m descending, complete)."""
    alpha = gx0 - sx
    s0 = f1 + eps1 * (sy - f1)
    t0 = f2 + eps2 * (ty - f2)
    t1 = alpha / (tx - sx)
    t2 = (gx1 - sx) / (tx - sx)
    kmax = (abs(f2 - f1) + w1 + w2) / (gx1 - gx0)
    Rr = w1 + alpha * kmax
    m_lo = ((f1 - Rr - s0) / (2 * w1)).ceil()
    m_hi = ((f1 + Rr - s0) / (2 * w1)).floor()
    complete = True
    if m_hi - m_lo + 1 <= cap:
        ms = range(m_hi, m_lo - 1, -1)
    else:
        complete = False
        q = cap // 3
        mid = sorted({rng.randint(m_lo + q, m_hi - q) for _ in range(q)}, reverse=True)
        ms = list(range(m_hi, m_hi - q, -1)) + mid + list(range(m_lo + q - 1, m_lo - 1, -1))
    sols = []
    for m in ms:
        sig = s0 + 2 * w1 * m
        lo = fmax(sig + (f1 - w1 - sig) / t1, sig + (f2 - w2 - sig) / t2)
        hi = fmin(sig + (f1 + w1 - sig) / t1, sig + (f2 + w2 - sig) / t2)
        if not lo < hi:
            continue
        for n in pick_ks((lo - t0) / (2 * w2), (hi - t0) / (2 * w2))[0]:
            th = t0 + 2 * w2 * n
            sols.append((m, n, (tx - sx, eps1 * (th - sig))))
    if not sols and not complete:
        r = _par_fallback(sx, sy, tx, ty, gx0, gx1, f1, w1, f2, w2, eps1, eps2)
        CSTATS['bisect' if r else 'bisect-failed'] += 1
        if r:
            sols.append(r)
    return sols, complete


def _solve_perp(sx, sy, tx, ty, gx0, gx1, gy0, gy1, w1, w2, eps1, eps2, cap=400, want=3):
    """Canonical perp frame: door 1 on x = gx0 with flat end (gx0, gy0), door 2
    on y = gy1 with flat end (gx1, gy1). Solutions in order of increasing
    slope (decreasing m). The first one is the solution of the proof."""
    s0 = gy0 + eps1 * (sy - gy0)
    t0 = gx1 + eps2 * (tx - gx1)
    m = ((gy0 + w1 - s0) / (2 * w1)).ceil() - 1            # largest m with sigma < gy0 + w1
    sols = []
    it = 0
    while it < cap and len(sols) < want:
        sig = s0 + 2 * w1 * m
        assert sig < gy0 + w1
        t2 = (gy1 - sig) / (ty - sig)
        lo = sx + (gx1 - w2 - sx) / t2
        hi = sx + (gx1 + w2 - sx) / t2
        num = (gx0 - sx) * (ty - sig)
        up = gy0 + w1 - sig
        lo = fmax(lo, sx + num / up)
        dn = gy0 - w1 - sig
        if dn.sign() > 0:
            hi = fmin(hi, sx + num / dn)
        if lo < hi:
            for n in pick_ks((lo - t0) / (2 * w2), (hi - t0) / (2 * w2))[0]:
                th = t0 + 2 * w2 * n
                sols.append((m, n, (th - sx, eps1 * (ty - sig))))
        m -= 1
        it += 1
    if not sols:
        r = _perp_fallback(sx, sy, tx, ty, gx0, gx1, gy0, gy1, w1, w2, eps1, eps2)
        CSTATS['bisect' if r else 'bisect-failed'] += 1
        if r:
            sols.append(r)
    return sols, len(sols) > 0


def inst_C(R, S, T, arms, rng):
    out = []
    for a1 in arms[S]:
        G1 = arm_G(a1)
        for a2 in arms[T]:
            if arm_G(a2) != G1:
                continue
            if a1['ad'] == a2['ad'] and a1['door'] == a2['door'] and \
                    {a1['F'], a1['E']} == {a2['F'], a2['E']}:
                continue                                    # the same corridor
            g = CANON[arm_flag(a1)]
            Rg = R.tf(g)
            c1, c2 = tarm(a1, g), tarm(a2, g)
            gx0, gx1, gy0, gy1 = arm_G(c1)
            s, t = tpoint(g, S), tpoint(g, T)
            side2, flat2 = arm_flag(c2)
            w1 = c1['E'] - gy0
            w2 = abs(c2['E'] - c2['F'])
            sols = {}
            opp = None
            if side2 == 'R':
                form = 'par'
                for e1 in (1, -1):
                    for e2 in (1, -1):
                        sols[(e1, e2)] = _solve_par(s[0], s[1], t[0], t[1], gx0, gx1, gy0, w1,
                                                    c2['F'], w2, e1, e2, rng)
            elif side2 == 'T':
                form = 'perp'
                # the proof says the flat end of door 2 must be (gx1, gy1)
                if flat2 != 'hi':
                    out.append(dict(lem='C', form='perp-impossible', key=None, g=g, a=s, b=t, sols={}))
                    continue
                for e1 in (1, -1):
                    for e2 in (1, -1):
                        sols[(e1, e2)] = _solve_perp(s[0], s[1], t[0], t[1], gx0, gx1, gy0, gy1,
                                                     w1, w2, e1, e2)
            elif side2 == 'B':
                out.append(dict(lem='C', form='perp-impossible', key=None, g=g, a=s, b=t, sols={}))
                continue
            else:                                           # same side
                if flat2 != 'hi':
                    continue
                i1 = Rg.idx(0, gx1)
                if not Rg.vwall(i1, range(Rg.idx(1, gy0), Rg.idx(1, gy1))):
                    continue
                form = 'same'
                opp = gx1
                for e1 in (1, -1):
                    for e2 in (1, -1):
                        sols[(e1, e2)] = _solve_par(s[0], s[1], 2 * gx1 - t[0], t[1], gx0,
                                                    2 * gx1 - gx0, gy0, w1, gy1, w2, e1, e2, rng)

            def desc(c):
                al, Fv = back_line(g, 1 - c['ad'], c['F'])
                _, Ev = back_line(g, 1 - c['ad'], c['E'])
                _, dv = back_line(g, c['ad'], c['door'])
                return (al, Fv, Ev, dv)
            oppv = back_line(g, 0, opp)[1] if opp is not None else None
            out.append(dict(lem='C', form=form, key=('C', form, desc(c1), desc(c2), oppv), g=g,
                            a=s, b=t, sols=sols,
                            geo=dict(gx0=gx0, gx1=gx1, gy0=gy0, gy1=gy1, w1=w1, w2=w2, F2=c2['F'], E2=c2['E'])))
    return out


def inst_D(R, S, T):
    """Lemma D. Canonical frame: V = (x_iv, y_jv); corridor 1 goes up from the
    door [x_ip, x_iv] x {y_jv} and contains A; corridor 2 goes right from the
    door {x_iv} x [y_jb, y_jv] and contains B."""
    out = []
    for swap, (A, B) in enumerate(((S, T), (T, S))):
        for g in TRANSFORMS:
            Rg = R.tf(g)
            s, t = Rg.pt(tpoint(g, A)), Rg.pt(tpoint(g, B))
            for iv in range(1, Rg.nx + 1):
                if not (s[2] < 2 * iv < t[2]):
                    continue
                for jv in range(1, Rg.ny + 1):
                    if not (t[3] < 2 * jv < s[3]):
                        continue
                    for ip in range(iv):
                        if not 2 * ip < s[2]:
                            continue
                        rows1 = span(2 * jv, s[3])
                        if not (Rg.cells_in(range(ip, iv), rows1) and Rg.vwall(ip, rows1) and Rg.vwall(iv, rows1)):
                            continue
                        for jb in range(jv):
                            if not 2 * jb < t[3]:
                                continue
                            cols2 = span(2 * iv, t[2])
                            if not (Rg.cells_in(cols2, range(jb, jv)) and Rg.hwall(jb, cols2) and Rg.hwall(jv, cols2)):
                                continue
                            if not Rg.cells_in(range(ip, iv), range(jb, jv)):
                                continue
                            vx, vy = Rg.xs[iv], Rg.ys[jv]
                            b_, e_ = vx - s[0], s[1] - vy
                            a_, c_ = t[0] - vx, vy - t[1]
                            w, h = vx - Rg.xs[ip], vy - Rg.ys[jb]
                            cands = []
                            case = None
                            if c_ <= e_:
                                # Lemma B', viewer B = T, corridor 1 (walls x = vx - w, x = vx), door y = vy
                                case = 'Bp-1'
                                lam = c_ / (c_ + e_)
                                for eps in (1, -1):
                                    base = (vx - w) + eps * (s[0] - (vx - w))
                                    lo = ((vx - w - t[0]) / lam + t[0] - base) / (2 * w)
                                    hi = ((vx - t[0]) / lam + t[0] - base) / (2 * w)
                                    for k in pick_ks(lo, hi)[0]:
                                        # path from B to an image of A
                                        cands.append((('rev', eps, k), (base + 2 * w * k - t[0], s[1] - t[1])))
                            elif b_ <= a_:
                                case = 'Bp-2'
                                lam = b_ / (a_ + b_)
                                for eps in (1, -1):
                                    base = (vy - h) + eps * (t[1] - (vy - h))
                                    lo = ((vy - h - s[1]) / lam + s[1] - base) / (2 * h)
                                    hi = ((vy - s[1]) / lam + s[1] - base) / (2 * h)
                                    for k in pick_ks(lo, hi)[0]:
                                        cands.append((('fwd', eps, k), (t[0] - s[0], base + 2 * h * k - s[1])))
                            else:
                                case = 'direct'
                                cands.append((('fwd', 0, 0), (t[0] - s[0], t[1] - s[1])))
                            out.append(dict(lem='D', key=('D', swap), g=g, a=s[:2], b=t[:2], cands=cands, case=case))
    return out


def all_instances(R, S, T, rng, which=('A', 'A2', 'B', "B'", 'B2', 'C', 'D')):
    arms = {S: arms_all(R, S), T: arms_all(R, T)}
    out = []
    if 'A' in which:
        out += inst_A(R, S, T)
    if 'A2' in which:
        out += inst_A2(R, S, T)
    if 'B' in which:
        out += inst_B(R, S, T)
    if "B'" in which:
        out += inst_Bp(R, S, T)
    if 'B2' in which:
        out += inst_B2(R, S, T, arms)
    if 'C' in which:
        out += inst_C(R, S, T, arms, rng)
    if 'D' in which:
        out += inst_D(R, S, T)
    return out


def evaluate(R, inst, rng, max_c_traces=6):
    """Trace the candidates of one instance. Returns (verdict, detail).
    verdict: 'ok', 'skip' (every decisive trace exceeded MAXREF reflections),
    or a failure label. A trace that exceeds MAXREF is counted in
    detail['skipped'] and is never counted as a success or a failure."""
    Rg = R.tf(inst['g'])
    a, b = inst['a'], inst['b']
    lem = inst['lem']
    det = dict(traces=0, maxref=0, skipped=0)

    def tr(p, Dv, q):
        st, nr = TRACER[0](Rg, p, Dv, q)
        det['traces'] += 1
        if st == 'too-long':
            det['skipped'] += 1
        else:
            det['maxref'] = max(det['maxref'], nr)
        return st

    if lem in ('A', 'A2'):
        st = tr(a, inst['cands'][0][1], b)
        if st == 'too-long':
            return 'skip', det
        return ('ok' if st == 'ok' else f'{lem}:{st}'), det
    if lem in ('B', "B'"):
        bad = []
        for lab, Dv in inst['cands']:
            st = tr(a, Dv, b)
            if st not in ('ok', 'too-long'):
                bad.append((lab, st))
        ps = inst['per_sign']
        det['per_sign'] = ps
        if lem == 'B' and (ps[1] == 0 or ps[-1] == 0):
            return 'B:sign-without-window-value', det
        if lem == "B'":
            need = 2 if inst['strict'] else 1
            if sum(1 for e in (1, -1) if ps[e] > 0) < need:
                return "B':too-few-signs", det
        if bad:
            det['bad'] = bad
            return f'{lem}:candidate-invalid', det
        return ('ok' if det['skipped'] < det['traces'] else 'skip'), det
    if lem == 'B2':
        good = {1: 0, -1: 0}
        skipped = {1: 0, -1: 0}
        bad = []
        ncorner = 0
        for lab, Dv in inst['cands']:
            st = tr(a, Dv, b)
            if st == 'too-long':
                skipped[lab[0]] += 1
            elif st == 'ok':
                good[lab[0]] += 1
                if inst['corner'][lab]:
                    bad.append((lab, 'corner-case-but-valid'))
            elif inst['corner'][lab] and st == 'vertex':
                ncorner += 1
            else:
                bad.append((lab, st))
        det['per_sign'] = inst['per_sign']
        det['corner'] = ncorner
        if bad:
            det['bad'] = bad
            return 'B2:candidate-invalid-outside-corner-case', det
        if good[1] == 0 and good[-1] == 0:
            if skipped[1] or skipped[-1]:
                return 'skip', det
            return 'B2:no-valid-sign', det
        det['one_sign_only'] = (good[1] == 0 and skipped[1] == 0) or (good[-1] == 0 and skipped[-1] == 0)
        return 'ok', det
    if lem == 'C':
        if inst['form'] == 'perp-impossible':
            return 'C:perp-configuration-the-proof-excludes', det
        bad = []
        nosol = []
        capped = 0
        for sg, (sols, complete) in inst['sols'].items():
            if not sols:
                if complete:
                    nosol.append(sg)
                else:
                    capped += 1
                continue
            if len(sols) <= max_c_traces:
                pick = sols
            else:
                pick = [sols[0], sols[-1]] + rng.sample(sols[1:-1], max_c_traces - 2)
            for (m, n, Dv) in pick:
                st = tr(a, Dv, b)
                if st not in ('ok', 'too-long'):
                    bad.append((sg, m, n, st))
        det['capped'] = capped
        if nosol:
            det['nosol'] = nosol
            return 'C:no-solution', det
        if bad:
            det['bad'] = bad
            return 'C:candidate-invalid', det
        if det['traces'] == 0 or det['skipped'] == det['traces']:
            return 'skip', det
        return 'ok', det
    if lem == 'D':
        bad = []
        det['case'] = inst['case']
        if not inst['cands']:
            return 'D:no-candidate', det
        for lab, Dv in inst['cands']:
            st = tr(b, Dv, a) if lab[0] == 'rev' else tr(a, Dv, b)
            if st not in ('ok', 'too-long'):
                bad.append((lab, st))
        if bad:
            det['bad'] = bad
            return 'D:candidate-invalid', det
        return ('ok' if det['skipped'] < det['traces'] else 'skip'), det
    raise ValueError(lem)


# ----------------------------------------------------------------- second tracer (integers, no division)
def _zsign(a, b, D):
    if b == 0:
        return (a > 0) - (a < 0)
    if a == 0:
        return (b > 0) - (b < 0)
    sa = 1 if a > 0 else -1
    sb = 1 if b > 0 else -1
    if sa == sb:
        return sa
    return sa if a * a > D * b * b else sb


def trace_fast(room, S, Dv, T, maxref=None):
    """Same contract as trace(). Works in Z[sqrt D] after clearing
    denominators, and never divides. The real position is kept as
    x = kx + ex * U and y = ky + ey * V, where U and V are the unfolded
    distances travelled in x and in y, and ex, ey are the current signs.
    A wall x = c is reached at U = ex * (c - kx), an exact ring element.
    Times U / A and V / B (A = |Dx|, B = |Dy|) are compared by cross
    multiplication."""
    if maxref is None:
        maxref = MAXREF
    if not room.interior(S) or not room.interior(T):
        return 'not-interior', 0
    wbox = float(room.xs[-1] - room.xs[0])
    hbox = float(room.ys[-1] - room.ys[0])
    if abs(float(Dv[0])) / wbox + abs(float(Dv[1])) / hbox - 2 > maxref * 1.01 + 2:
        return 'too-long', maxref
    D = type(S[0]).D
    vals = [S[0], S[1], T[0], T[1], Dv[0], Dv[1]] + room.xs + room.ys
    N = 1
    for v in vals:
        N = math.lcm(N, v.a.denominator, v.b.denominator)

    def z(q):
        return (int(q.a * N), int(q.b * N))
    walls = [(ax, z(c), z(lo), z(hi)) for (ax, c, lo, hi) in room.walls()]
    kxa, kxb = z(S[0])
    kya, kyb = z(S[1])
    Txa, Txb = z(T[0])
    Tya, Tyb = z(T[1])
    dxa, dxb = z(Dv[0])
    dya, dyb = z(Dv[1])
    ex = _zsign(dxa, dxb, D)
    ey = _zsign(dya, dyb, D)
    if ex == 0 and ey == 0:
        return 'miss', 0
    Aa, Ab = (dxa, dxb) if ex >= 0 else (-dxa, -dxb)
    Ba, Bb = (dya, dyb) if ey >= 0 else (-dya, -dyb)
    ck = 0 if ex != 0 else 1            # current time: kind 0 = value / A, kind 1 = value / B
    cva, cvb = 0, 0
    nref = 0
    while True:
        bk = None
        for (axis, (ca, cb), (la, lb), (ha, hb)) in walls:
            if axis == 0:
                if ex == 0:
                    continue
                ua, ub = ex * (ca - kxa), ex * (cb - kxb)
                # ahead of the current time?
                if ck == 0:
                    sg = _zsign(ua - cva, ub - cvb, D)
                else:
                    sg = _zsign(ua * Ba + D * ub * Bb - cva * Aa - D * cvb * Ab,
                                ua * Bb + ub * Ba - cva * Ab - cvb * Aa, D)
                if sg <= 0:
                    continue
                if bk is not None:
                    if bk == 0:
                        cmpb = _zsign(ua - bva, ub - bvb, D)
                    else:
                        cmpb = _zsign(ua * Ba + D * ub * Bb - bva * Aa - D * bvb * Ab,
                                      ua * Bb + ub * Ba - bva * Ab - bvb * Aa, D)
                    if cmpb > 0:
                        continue
                # A * y = A * ky + ey * U * B
                pa = Aa * kya + D * Ab * kyb + ey * (ua * Ba + D * ub * Bb)
                pb = Aa * kyb + Ab * kya + ey * (ua * Bb + ub * Ba)
                l = _zsign(pa - (Aa * la + D * Ab * lb), pb - (Aa * lb + Ab * la), D)
                if l < 0:
                    continue
                h = _zsign((Aa * ha + D * Ab * hb) - pa, (Aa * hb + Ab * ha) - pb, D)
                if h < 0:
                    continue
                if bk is not None and cmpb == 0:
                    bvert = True
                else:
                    bk, bva, bvb, bvert, bca, bcb = 0, ua, ub, (l == 0 or h == 0), ca, cb
            else:
                if ey == 0:
                    continue
                ua, ub = ey * (ca - kya), ey * (cb - kyb)
                if ck == 1:
                    sg = _zsign(ua - cva, ub - cvb, D)
                else:
                    sg = _zsign(ua * Aa + D * ub * Ab - cva * Ba - D * cvb * Bb,
                                ua * Ab + ub * Aa - cva * Bb - cvb * Ba, D)
                if sg <= 0:
                    continue
                if bk is not None:
                    if bk == 1:
                        cmpb = _zsign(ua - bva, ub - bvb, D)
                    else:
                        cmpb = _zsign(ua * Aa + D * ub * Ab - bva * Ba - D * bvb * Bb,
                                      ua * Ab + ub * Aa - bva * Bb - bvb * Ba, D)
                    if cmpb > 0:
                        continue
                # B * x = B * kx + ex * V * A
                pa = Ba * kxa + D * Bb * kxb + ex * (ua * Aa + D * ub * Ab)
                pb = Ba * kxb + Bb * kxa + ex * (ua * Ab + ub * Aa)
                l = _zsign(pa - (Ba * la + D * Bb * lb), pb - (Ba * lb + Bb * la), D)
                if l < 0:
                    continue
                h = _zsign((Ba * ha + D * Bb * hb) - pa, (Ba * hb + Bb * ha) - pb, D)
                if h < 0:
                    continue
                if bk is not None and cmpb == 0:
                    bvert = True
                else:
                    bk, bva, bvb, bvert, bca, bcb = 1, ua, ub, (l == 0 or h == 0), ca, cb
        if bk is None:
            return 'escape', nref
        if bk == 0:
            ce = _zsign(bva - Aa, bvb - Ab, D)
        else:
            ce = _zsign(bva - Ba, bvb - Bb, D)
        if ce > 0:
            ok = (kxa + ex * Aa == Txa and kxb + ex * Ab == Txb and
                  kya + ey * Ba == Tya and kyb + ey * Bb == Tyb)
            return ('ok' if ok else 'miss'), nref
        if bvert:
            return 'vertex', nref
        if ce == 0:
            return 'end-on-wall', nref
        if bk == 0:
            kxa, kxb = bca + ex * bva, bcb + ex * bvb
            ex = -ex
        else:
            kya, kyb = bca + ey * bva, bcb + ey * bvb
            ey = -ey
        ck, cva, cvb = bk, bva, bvb
        nref += 1
        if nref > maxref:
            return 'too-long', nref


TRACER = [trace]          # evaluate() uses TRACER[0]
