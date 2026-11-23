"""Witness mining core (d57).

Order type = cell set on an nx x ny index grid (d15 convention: mask bit
i + nx*j is cell (i, j), row j = 0 at the bottom). A realization assigns real
grid coordinates 0 = x_0 < ... < x_nx and 0 = y_0 < ... < y_ny. Position types
use d15 doubled coordinates: even 2i = on grid line i, odd 2i+1 = strictly
between lines i and i+1.

Parameters theta: grid gaps gx0.., gy0.. and, for every odd point coordinate,
its offset from the lower grid line of its gap (see Param). Every geometric
quantity below is a linear form in theta with integer coefficients and no
constant.

Itinerary = tuple of wall indices (maximal walls of the order type). Its
validity is a conjunction of disjunctions of strict sign conditions, each
sign * sum_k P_k * Q_k > 0 with P, Q linear forms (Q may be absent). On a box
with integer endpoints (theta scaled by 2^N) the conditions are evaluated by
exact integer interval arithmetic (naive product bounds, then a mean-value
form), so "certified on a box" means the itinerary is valid at every real
point of the closed box. A degenerate box is an exact point check."""
import math, random

# ---------------------------------------------------------------- order type
class OT:
    def __init__(self, nx, ny, cells):
        self.nx, self.ny, self.cells = nx, ny, frozenset(cells)
        self._walls()

    @staticmethod
    def from_mask(nx, ny, mask):
        return OT(nx, ny, [(i, j) for j in range(ny) for i in range(nx) if (mask >> (i + nx * j)) & 1])

    def ins(self, i, j):
        return (i, j) in self.cells

    def npt(self, i, j):
        return self.ins(i - 1, j - 1) + self.ins(i, j - 1) + self.ins(i - 1, j) + self.ins(i, j)

    def _walls(self):
        W = []
        for i in range(self.nx + 1):          # vertical walls on line x_i
            j = 0
            while j < self.ny:
                if self.ins(i - 1, j) != self.ins(i, j):
                    j0 = j
                    while j < self.ny and self.ins(i - 1, j) != self.ins(i, j): j += 1
                    W.append(('v', i, j0, j))
                else: j += 1
        for j in range(self.ny + 1):
            i = 0
            while i < self.nx:
                if self.ins(i, j - 1) != self.ins(i, j):
                    i0 = i
                    while i < self.nx and self.ins(i, j - 1) != self.ins(i, j): i += 1
                    W.append(('h', j, i0, i))
                else: i += 1
        self.walls = W


# ---------------------------------------------------------------- linear forms
def F(d):
    return tuple(sorted((k, v) for k, v in d.items() if v))

def fadd(*terms):          # terms: (coef, form)
    d = {}
    for c, f in terms:
        for k, v in f: d[k] = d.get(k, 0) + c * v
    return F(d)


class Param:
    """Variables and forms for (order type, S type, T type).
    Variables: grid gaps gx0..gx{nx-1}, gy0..gy{ny-1} (all > 0) and, for every
    odd point coordinate, its offset as1, as2, at1, at2 from the lower grid
    line of its gap (0 < offset < gap). Grid coordinates are partial sums."""
    def __init__(self, ot, S, T):
        self.ot, self.S, self.T = ot, S, T
        names = ['gx%d' % i for i in range(ot.nx)] + ['gy%d' % j for j in range(ot.ny)]
        for nm, v in (('as1', S[0]), ('as2', S[1]), ('at1', T[0]), ('at2', T[1])):
            if v % 2: names.append(nm)
        self.names = names
        self.ix = {n: k for k, n in enumerate(names)}
        self.xf = [tuple((self.ix['gx%d' % k], 1) for k in range(i)) for i in range(ot.nx + 1)]
        self.yf = [tuple((self.ix['gy%d' % k], 1) for k in range(j)) for j in range(ot.ny + 1)]
        def pf(v, nm, g):
            return g[v // 2] if v % 2 == 0 else fadd((1, g[v // 2]), (1, ((self.ix[nm], 1),)))
        self.Sf = (pf(S[0], 'as1', self.xf), pf(S[1], 'as2', self.yf))
        self.Tf = (pf(T[0], 'at1', self.xf), pf(T[1], 'at2', self.yf))

    def gapvar(self, nm):
        """Index of the gap variable that bounds offset variable nm."""
        P = self.S if nm[1] == 's' else self.T
        k = int(nm[2]) - 1
        return self.ix[('gx%d' if k == 0 else 'gy%d') % (P[k] // 2)]

    def region(self, dp=8):
        """Point constraints as (open form, truncated form): open form > 0 on
        the open type region; truncated form >= 0 iff the offset is at least
        gap/dp from both ends. Gap positivity is carried by the box."""
        out = []
        for nm in ('as1', 'as2', 'at1', 'at2'):
            if nm in self.ix:
                a, g = self.ix[nm], self.gapvar(nm)
                out.append((((a, 1),), F({a: dp, g: -1})))
                out.append((F({g: 1, a: -1}), F({g: dp - 1, a: -dp})))
        return out


# ---------------------------------------------------------------- conditions
def build(par, itin):
    """Return (conds, signs_needed) for itinerary itin. conds is a list of
    disjunctions; each alternative is (sign, [(P, Q or None), ...])."""
    ot, walls = par.ot, par.ot.walls
    xf, yf = par.xf, par.yf
    Sx, Sy = par.Sf
    ax, bx, ay, by = 1, (), 1, ()                    # copy map x -> ax*x + bx
    copies = []
    for w in itin:
        copies.append((ax, bx, ay, by))
        kind, i = walls[w][0], walls[w][1]
        if kind == 'v':
            c = fadd((ax, xf[i]), (1, bx)); ax, bx = -ax, fadd((2, c), (-1, bx))
        else:
            c = fadd((ay, yf[i]), (1, by)); ay, by = -ay, fadd((2, c), (-1, by))
    copies.append((ax, bx, ay, by))
    Tx = fadd((ax, par.Tf[0]), (1, bx)); Ty = fadd((ay, par.Tf[1]), (1, by))
    dx = fadd((1, Tx), (-1, Sx)); dy = fadd((1, Ty), (-1, Sy))
    return dict(copies=copies, dx=dx, dy=dy, Tstar=(Tx, Ty))


def wall_geom(par, cp, w):
    """Unfolded wall w in copy cp: (axis, line form, lo form, hi form)."""
    ax, bx, ay, by = cp
    kind, i, a, b = par.ot.walls[w]
    if kind == 'v':
        c = fadd((ax, par.xf[i]), (1, bx))
        e0, e1 = fadd((ay, par.yf[a]), (1, by)), fadd((ay, par.yf[b]), (1, by))
        return 'x', c, (e0, e1) if ay == 1 else (e1, e0)
    c = fadd((ay, par.yf[i]), (1, by))
    e0, e1 = fadd((ax, par.xf[a]), (1, bx)), fadd((ax, par.xf[b]), (1, bx))
    return 'y', c, (e0, e1) if ax == 1 else (e1, e0)


def conditions(par, itin, sx, sy):
    """All validity conditions given the direction signs sx, sy (+-1)."""
    B = build(par, itin)
    dx, dy = B['dx'], B['dy']
    Sx, Sy = par.Sf
    D = {'x': (dx, sx, Sx), 'y': (dy, sy, Sy)}
    conds = [[(sx, [(dx, None)])], [(sy, [(dy, None)])]]

    def tnum(axis, c):                       # time = num / d_axis
        return fadd((1, c), (-1, D[axis][2]))

    def less(A, Bt):                         # time A < time B as an alternative
        (na, aa), (nb, ab) = A, Bt
        if aa == ab:
            return (D[aa][1], [(fadd((1, nb), (-1, na)), None)])
        return (D[aa][1] * D[ab][1], [(nb, D[aa][0]), (fadd((-1, na),), D[ab][0])])

    def inside(axis, n, lo, hi):             # position across, at time n/d_axis
        d, s, P0 = D[axis]
        o = 'y' if axis == 'x' else 'x'
        od, _, O0 = D[o]
        # other coord = O0 + n * od / d ; > lo  <=>  s*((O0-lo)*d + n*od) > 0
        a1 = (s, [(fadd((1, O0), (-1, lo)), d), (n, od)])
        a2 = (s, [(fadd((1, hi), (-1, O0)), d), (fadd((-1, n),), od)])
        return a1, a2

    def outside(axis, n, lo, hi):
        a1, a2 = inside(axis, n, lo, hi)
        neg = lambda a: (-a[0], a[1])
        return neg(a1), neg(a2)              # strictly below lo / strictly above hi

    zero = ((), 'x')
    one = (dx, 'x')
    k = len(itin)
    walls = par.ot.walls
    prev = zero
    prevline = None
    for j in range(k + 1):
        cp = B['copies'][j]
        if j < k:
            axis, c, (lo, hi) = wall_geom(par, cp, itin[j])
            nxt = (tnum(axis, c), axis)
            a1, a2 = inside(axis, nxt[0], lo, hi)
            conds += [[a1], [a2]]
            line = (walls[itin[j]][0], walls[itin[j]][1])
        else:
            nxt, line = one, None
        conds.append([less(prev, nxt)])
        for w in range(len(walls)):
            wl = (walls[w][0], walls[w][1])
            if wl == line or wl == prevline: continue
            axis, c, (lo, hi) = wall_geom(par, cp, w)
            tw = (tnum(axis, c), axis)
            o1, o2 = outside(axis, tw[0], lo, hi)
            alts = [less(nxt, tw), o1, o2]
            alts.insert(0, less(tw, prev))
            conds.append(alts)
        prev, prevline = nxt, line
    return conds, B


# ---------------------------------------------------------------- evaluation
def iv(f, box):
    lo = hi = 0
    for v, c in f:
        l, h = box[v]
        if c > 0: lo += c * l; hi += c * h
        else: lo += c * h; hi += c * l
    return lo, hi


def grad(terms):
    """Gradient of sum P*Q (each component a linear form), memoised."""
    key = id(terms)
    g = _GRAD.get(key)
    if g is None:
        d = {}
        for P, Q in terms:
            for v, c in P:
                d.setdefault(v, {})
                for w, e in Q: d[v][w] = d[v].get(w, 0) + c * e
            for v, c in Q:
                d.setdefault(v, {})
                for w, e in P: d[v][w] = d[v].get(w, 0) + c * e
        g = _GRAD[key] = (terms, [(v, F(f)) for v, f in d.items()])
    return g[1]
_GRAD = {}


def alt_ok(alt, box, cache):
    s, terms = alt
    lo = hi = 0
    quad = False
    for P, Q in terms:
        a = cache.get(P)
        if a is None: a = cache[P] = iv(P, box)
        if Q is None:
            lo += a[0]; hi += a[1]
        else:
            quad = True
            b = cache.get(Q)
            if b is None: b = cache[Q] = iv(Q, box)
            p = (a[0] * b[0], a[0] * b[1], a[1] * b[0], a[1] * b[1])
            lo += min(p); hi += max(p)
    if (lo > 0 if s > 0 else hi < 0): return True
    if not quad: return False
    # mean-value form: f(c) + sum_k [df/dv_k](box) * [l_k - c_k, h_k - c_k]
    c = cache.get('c')
    if c is None: c = cache['c'] = [(l + h) // 2 for l, h in box]
    cb = cache.get('cb')
    if cb is None: cb = cache['cb'] = [(x, x) for x in c]
    f0 = 0
    for P, Q in terms:
        f0 += iv(P, cb)[0] * iv(Q, cb)[0]
    lo = hi = f0
    for v, gf in grad(terms):
        gl, gh = iv(gf, box)
        dl, dh = box[v][0] - c[v], box[v][1] - c[v]
        p = (gl * dl, gl * dh, gh * dl, gh * dh)
        lo += min(p); hi += max(p)
    return lo > 0 if s > 0 else hi < 0


LAST_FAIL = [None]


def certify(conds, box):
    """True iff every condition has an alternative that holds on the whole box.
    On failure LAST_FAIL[0] holds the first alternative of the failed condition."""
    cache = {}
    for alts in conds:
        for k, a in enumerate(alts):
            if alt_ok(a, box, cache):
                if k: alts.insert(0, alts.pop(k))      # move-to-front heuristic
                break
        else:
            LAST_FAIL[0] = alts[0]
            return False
    return True


def split_hint(alt, box):
    """Variable with the largest contribution |df/dv| * width to the range of
    the alternative's polynomial on the box."""
    s, terms = alt
    best, bv = -1, None
    if all(Q is None for P, Q in terms):
        for P, Q in terms:
            for v, c in P:
                w = abs(c) * (box[v][1] - box[v][0])
                if w > best: best, bv = w, v
        return bv
    for v, gf in grad(terms):
        gl, gh = iv(gf, box)
        w = max(abs(gl), abs(gh)) * (box[v][1] - box[v][0])
        if w > best: best, bv = w, v
    return bv


# ---------------------------------------------------------------- float discovery
def realize(par, vals):
    """vals: dict var index -> float. Returns float coords xs, ys, S, T."""
    ev = lambda f: sum(c * vals[v] for v, c in f)
    xs = [ev(f) for f in par.xf]; ys = [ev(f) for f in par.yf]
    return xs, ys, (ev(par.Sf[0]), ev(par.Sf[1])), (ev(par.Tf[0]), ev(par.Tf[1]))


def float_walls(ot, xs, ys):
    out = []
    for kind, i, a, b in ot.walls:
        if kind == 'v': out.append(('v', xs[i], ys[a], ys[b]))
        else: out.append(('h', ys[i], xs[a], xs[b]))
    return out


def shoot(fw, S, T, nang=2000, maxref=12, tol=None, seed=None):
    """Shoot rays from S; return candidate itineraries (tuples of wall ids) whose
    prefix brings a ray within tol of T."""
    Lsc = max(max(abs(w[2] - w[3]) for w in fw), 1e-9)
    cands = set()
    off = (seed or 0.123) * 2 * math.pi / nang
    for a in range(nang):
        phi = off + 2 * math.pi * a / nang
        vx, vy = math.cos(phi), math.sin(phi)
        x, y = S; seq = []; travelled = 0.0
        for step in range(maxref + 1):
            best, hit = 1e300, None
            for k, (kind, c, lo, hi) in enumerate(fw):
                if kind == 'v':
                    if vx == 0: continue
                    t = (c - x) / vx
                    if t > 1e-12 and t < best:
                        yy = y + t * vy
                        if lo - 1e-12 <= yy <= hi + 1e-12: best, hit = t, k
                else:
                    if vy == 0: continue
                    t = (c - y) / vy
                    if t > 1e-12 and t < best:
                        xx = x + t * vx
                        if lo - 1e-12 <= xx <= hi + 1e-12: best, hit = t, k
            if hit is None: break
            # near miss of T on this leg
            px, py = T[0] - x, T[1] - y
            u = px * vx + py * vy
            if 0 < u < best:
                dist = abs(px * vy - py * vx)
                tl = tol if tol else 2 * (travelled + u) * (2 * math.pi / nang) + 1e-9
                if dist < tl: cands.add(tuple(seq))
            kind, c, lo, hi = fw[hit]
            nx_, ny_ = x + best * vx, y + best * vy
            pos = ny_ if kind == 'v' else nx_
            if min(pos - lo, hi - pos) < 1e-9 * Lsc: break       # vertex
            x, y = nx_, ny_; travelled += best; seq.append(hit)
            if kind == 'v': vx = -vx
            else: vy = -vy
    return cands


def float_trace(fw, S, V, maxref=60):
    """Follow S + t V, t in [0, 1], in floats; return the wall sequence or None
    if the path comes within 1e-9 (relative) of a wall end."""
    x, y = S; vx, vy = V; left = 1.0; seq = []
    Lsc = max(max(abs(w[2] - w[3]) for w in fw), 1e-9)
    while len(seq) <= maxref:
        best, hit = left, None
        for k, (kind, c, lo, hi) in enumerate(fw):
            if kind == 'v':
                if vx == 0: continue
                t = (c - x) / vx
                if 1e-13 < t < best and lo - 1e-9 * Lsc <= y + t * vy <= hi + 1e-9 * Lsc: best, hit = t, k
            else:
                if vy == 0: continue
                t = (c - y) / vy
                if 1e-13 < t < best and lo - 1e-9 * Lsc <= x + t * vx <= hi + 1e-9 * Lsc: best, hit = t, k
        if hit is None: return tuple(seq)
        kind, c, lo, hi = fw[hit]
        x, y = x + best * vx, y + best * vy; left -= best
        pos = y if kind == 'v' else x
        if min(pos - lo, hi - pos) < 1e-9 * Lsc: return None
        seq.append(hit)
        if kind == 'v': vx = -vx
        else: vy = -vy
    return None


def mine(par, vals, nang=2000, maxref=12, seed=None):
    """Float discovery at a parameter point: candidate itineraries, re-traced
    along their own direction so the hit order is the true one. Returns a
    sorted list of (itin, sx, sy), shortest first. Not a validity claim."""
    xs, ys, S, T = realize(par, vals)
    fw = float_walls(par.ot, xs, ys)
    ev = lambda f: sum(c * vals[v] for v, c in f)
    out = set()
    for it in shoot(fw, S, T, nang, maxref, seed=seed):
        B = build(par, it)
        V = (ev(B['dx']), ev(B['dy']))
        if abs(V[0]) < 1e-12 or abs(V[1]) < 1e-12: continue
        tr = float_trace(fw, S, V, maxref=len(it) + 2)
        if tr is None or len(tr) != len(it): continue
        B2 = build(par, tr)
        if abs(ev(B2['dx']) - V[0]) + abs(ev(B2['dy']) - V[1]) > 1e-7 * (abs(V[0]) + abs(V[1])): continue
        out.add((tr, 1 if V[0] > 0 else -1, 1 if V[1] > 0 else -1))
    return sorted(out, key=lambda z: (len(z[0]), z))


def point_box(vals_int):
    return [(v, v) for v in vals_int]
