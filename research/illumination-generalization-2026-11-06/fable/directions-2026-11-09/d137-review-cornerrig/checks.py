"""D137 checks for corner-orbit-rigidity.md (snapshot 2026-11-21 23:05).

Named rooms only; no searches over room families.  Exact Fraction arithmetic.
For each room the script
  * traces billiard rays from the source mark S in every primitive direction
    (p,q) with max(|p|,|q|) <= N that is not parallel to a wall,
  * at the first corner hit computes both one-sided continuations (limits of
    rays passing just left / just right of the corner) by an exact local
    simulation, and follows each continuation until the next corner, recording
    every passage through the target mark T (= one corner template S->C->T),
  * forms the corner row  grad det(dev C - S, dev T - dev C)  in the
    fixed-direction chart (wall-line offsets + mark coordinates),
  * reports rank / kernel in the chart and (axial rooms) in the weak-order cell,
    compared with the trivial motions (translations and admissible scalings),
  * replays the opening lemma: perturbs the room along a direction with nonzero
    row, both signs, and ray-traces the perturbed room exactly.
Run:  python3 -B checks.py > checks.log
"""
from fractions import Fraction as F
from math import gcd
import random
import time

T0 = time.process_time()
random.seed(137)
MAXSTEP = 4000          # reflections per leg (cap)


def out(*a):
    print(*a, flush=True)


# ------------------------------------------------------------------ linear algebra
def rank(rows, ncols):
    M = [list(r) for r in rows]
    r = 0
    for c in range(ncols):
        k = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if k is None:
            continue
        M[r], M[k] = M[k], M[r]
        pv = M[r][c]
        M[r] = [x / pv for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
    return r


def nullspace(rows, ncols):
    M = [list(r) for r in rows]
    piv, r = [], 0
    for c in range(ncols):
        k = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if k is None:
            continue
        M[r], M[k] = M[k], M[r]
        pv = M[r][c]
        M[r] = [x / pv for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        piv.append(c)
        r += 1
    free = [c for c in range(ncols) if c not in piv]
    basis = []
    for fc in free:
        v = [F(0)] * ncols
        v[fc] = F(1)
        for i, pc in enumerate(piv):
            v[pc] = -M[i][fc]
        basis.append(v)
    return basis


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def det(a, b):
    return a[0] * b[1] - a[1] * b[0]


# ------------------------------------------------------------------ rooms
class Room:
    """Fixed-direction chart: p = (c_0..c_{n-1}, Sx, Sy, Tx, Ty); edge i lies on n_i . x = c_i."""

    def __init__(self, name, V, S, T):
        self.name = name
        self.V = [(F(x), F(y)) for x, y in V]
        n = len(V)
        self.n = n
        if sum(det(self.V[i], self.V[(i + 1) % n]) for i in range(n)) < 0:
            raise ValueError("vertices must be counterclockwise")
        self.dim = n + 4
        self.nrm = []
        for i in range(n):
            a, b = self.V[i], self.V[(i + 1) % n]
            u = (b[0] - a[0], b[1] - a[1])
            g = gcd(int(abs(u[0])), int(abs(u[1])))
            u = (u[0] / g, u[1] / g)
            self.nrm.append((-u[1], u[0]))          # inward-pointing for ccw rooms
        self.p0 = [dot(self.nrm[i], self.V[i]) for i in range(n)] + [F(S[0]), F(S[1]), F(T[0]), F(T[1])]
        # vertex forms: v_i = line(i-1) cap line(i)
        self.vform = []
        for i in range(n):
            n1, n2 = self.nrm[i - 1], self.nrm[i]
            dd = det(n1, n2)
            fx = [F(0)] * self.dim
            fy = [F(0)] * self.dim
            # x = (c1*n2y - c2*n1y)/dd ; y = (n1x*c2 - n2x*c1)/dd
            fx[(i - 1) % n] += n2[1] / dd
            fx[i] += -n1[1] / dd
            fy[(i - 1) % n] += -n2[0] / dd
            fy[i] += n1[0] / dd
            self.vform.append((fx, fy))
        e = lambda k: [F(1) if j == k else F(0) for j in range(self.dim)]
        self.Sform = (e(n), e(n + 1))
        self.Tform = (e(n + 2), e(n + 3))
        for i in range(n):
            assert (dot(self.vform[i][0], self.p0), dot(self.vform[i][1], self.p0)) == self.V[i]
        self.wall_dirs = set()
        for nm in self.nrm:
            u = (nm[1], -nm[0])
            self.wall_dirs.add((u[0], u[1]))
            self.wall_dirs.add((-u[0], -u[1]))
        self.mixed = any(nm[0] != 0 and nm[1] != 0 for nm in self.nrm)
        # interior angle numerator a (angle = a*pi/4) and regularity of the lift in the unfolding
        DIR8 = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        self.anum, self.regular = [], []
        for i in range(n):
            ui = (self.nrm[i - 1][1], -self.nrm[i - 1][0])      # incoming edge direction
            uo = (self.nrm[i][1], -self.nrm[i][0])
            k1 = DIR8.index((int(ui[0]), int(ui[1])))
            k2 = DIR8.index((int(uo[0]), int(uo[1])))
            turn = (k2 - k1) % 8                              # left turn in units of 45 degrees
            a = 4 - turn if turn <= 4 else 4 + (8 - turn)
            self.anum.append(a)
            self.regular.append(a in ((1, 2, 4) if self.mixed else (2,)))

    def geometry(self, p):
        V = [(dot(fx, p), dot(fy, p)) for fx, fy in self.vform]
        S = (p[self.n], p[self.n + 1])
        T = (p[self.n + 2], p[self.n + 3])
        return V, S, T

    def refl(self, i):
        """reflection in line i: linear part R (2x2) and translation as 2 linear forms."""
        nx, ny = self.nrm[i]
        q = nx * nx + ny * ny
        R = ((1 - 2 * nx * nx / q, -2 * nx * ny / q), (-2 * nx * ny / q, 1 - 2 * ny * ny / q))
        tx = [F(0)] * self.dim
        ty = [F(0)] * self.dim
        tx[i] = 2 * nx / q
        ty[i] = 2 * ny / q
        return R, (tx, ty)


def mat_mul(A, B):
    return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)) for i in range(2))


def mat_vec(A, v):
    return (A[0][0] * v[0] + A[0][1] * v[1], A[1][0] * v[0] + A[1][1] * v[1])


def form_mat(A, f):
    """A (2x2) applied to a pair of linear forms."""
    return ([A[0][0] * a + A[0][1] * b for a, b in zip(*f)], [A[1][0] * a + A[1][1] * b for a, b in zip(*f)])


def form_add(f, g, s=1):
    return ([a + s * b for a, b in zip(f[0], g[0])], [a + s * b for a, b in zip(f[1], g[1])])


ID = ((F(1), F(0)), (F(0), F(1)))


def compose(room, g, i):
    """g o sigma_i, with g = (L, t)."""
    L, t = g
    R, tr = room.refl(i)
    return (mat_mul(L, R), form_add(form_mat(L, tr), t))


def apply(g, P):
    L, t = g
    return form_add(form_mat(L, P), t)


def ev(f, p):
    return (dot(f[0], p), dot(f[1], p))


# ------------------------------------------------------------------ exact tracing
def first_hit(V, P, d, skip_zero):
    """smallest t>0 where ray P+td meets the boundary; returns (t, edge, s)."""
    best = None
    n = len(V)
    for i in range(n):
        A, B = V[i], V[(i + 1) % n]
        e = (B[0] - A[0], B[1] - A[1])
        den = det(d, e)
        if den == 0:
            continue
        w = (A[0] - P[0], A[1] - P[1])
        t = det(w, e) / den
        s = det(w, d) / den
        if t < 0 or s < 0 or s > 1:
            continue
        if t == 0:
            continue                       # the point we start from (previous bounce / corner)
        if best is None or t < best[0]:
            best = (t, i, s)
    return best


def on_ray(P, d, X, t0, t1):
    """X = P + t d with t0 < t < t1 ?"""
    w = (X[0] - P[0], X[1] - P[1])
    if det(d, w) != 0:
        return None
    t = (w[0] * d[0] + w[1] * d[1]) / (d[0] * d[0] + d[1] * d[1])
    return t if t0 < t < t1 else None


def trace(room, V, S, T, P, d, g, from_vertex, want):
    """Follow ray; yield ('T', g) at each T passage, stop at corner ('C', vertex, g, d) /
    'periodic' / 'cap'.  want: collect T passages."""
    events = []
    seen = set()
    skip = from_vertex
    tau = F(0)                              # cumulative ray parameter
    for step in range(MAXSTEP):
        h = first_hit(V, P, d, skip)
        skip = False
        if h is None:
            raise RuntimeError("ray escaped room")
        t, i, s = h
        if want:
            tt = on_ray(P, d, T, F(0), t)
            if tt is not None:
                events.append(('T', g, tau + tt))
        Q = (P[0] + t * d[0], P[1] + t * d[1])
        if s == 0 or s == 1:
            vi = i if s == 0 else (i + 1) % room.n
            events.append(('C', vi, g, d))
            return events
        key = (Q, d)
        if key in seen:
            events.append(('periodic',))
            return events
        seen.add(key)
        R, _ = room.refl(i)
        d = mat_vec(R, d)
        g = compose(room, g, i)
        P = Q
        tau += t
    events.append(('cap',))
    return events


def side_continuation(room, V, C, d, g, sigma):
    """Exact local simulation of a ray passing the corner C on developed side sigma
    (+1 = left of the developed direction).  Returns (d_out, g_out)."""
    L = g[0]
    ddev = mat_vec(L, d)
    wdev = (-ddev[1], ddev[0])
    LT = ((L[0][0], L[1][0]), (L[0][1], L[1][1]))
    w = mat_vec(LT, wdev)
    nd = max(abs(d[0]), abs(d[1]))
    lam = F(1, 100) / nd
    delta = F(1, 10 ** 7) / max(abs(w[0]), abs(w[1]))
    P = (C[0] - lam * d[0] + sigma * delta * w[0], C[1] - lam * d[1] + sigma * delta * w[1])
    r2 = F(1, 100)
    gg = g
    for _ in range(12):
        h = first_hit(V, P, d, False)
        t, i, s = h
        Q = (P[0] + t * d[0], P[1] + t * d[1])
        if (Q[0] - C[0]) ** 2 + (Q[1] - C[1]) ** 2 > r2:
            return d, gg
        if s == 0 or s == 1:
            raise RuntimeError("local sim hit a vertex")
        R, _ = room.refl(i)
        d = mat_vec(R, d)
        gg = compose(room, gg, i)
        P = Q
    raise RuntimeError("local sim did not leave the corner")


def primitive_dirs(N, room):
    D = []
    for p in range(-N, N + 1):
        for q in range(-N, N + 1):
            if (p, q) == (0, 0) or gcd(abs(p), abs(q)) != 1:
                continue
            if p == 0 or q == 0:
                continue                    # axis directions are wall-parallel
            if room.mixed and abs(p) == abs(q):
                continue                    # diagonal walls
            D.append((F(p), F(q)))
    return D


def templates(room, N):
    V, S, T = room.geometry(room.p0)
    gid = (ID, ([F(0)] * room.dim, [F(0)] * room.dim))
    tmpl, direct, stats = [], [], {'dirs': 0, 'periodic': 0, 'cap': 0, 'corner': 0}
    for d in primitive_dirs(N, room):
        stats['dirs'] += 1
        ev1 = trace(room, V, S, T, S, d, gid, False, True)
        for e in ev1:
            if e[0] == 'T':
                direct.append(d)
        last = ev1[-1]
        if last[0] != 'C':
            stats[last[0]] += 1
            continue
        stats['corner'] += 1
        _, vi, gC, dC = last
        C = V[vi]
        for sigma in (1, -1):
            d2, g2 = side_continuation(room, V, C, dC, gC, sigma)
            ev2 = trace(room, V, S, T, C, d2, g2, True, True)
            for e in ev2:
                if e[0] == 'T':
                    tmpl.append(dict(d=d, vi=vi, sigma=sigma, gC=gC, gT=e[1]))
    return tmpl, direct, stats


def row_of(room, tp):
    Cf = apply(tp['gC'], room.vform[tp['vi']])
    Tf = apply(tp['gT'], room.Tform)
    A = form_add(Cf, room.Sform, -1)
    B = form_add(Tf, Cf, -1)
    a, b = ev(A, room.p0), ev(B, room.p0)
    assert det(a, b) == 0 and a[0] * b[0] + a[1] * b[1] > 0, "template not collinear"
    rowv = [det((A[0][k], A[1][k]), b) + det(a, (B[0][k], B[1][k])) for k in range(room.dim)]
    rho = (b[0] / a[0]) if a[0] != 0 else (b[1] / a[1])
    return rowv, rho, (A, B)


def trivial(room, axial_scalings):
    V, S, T = room.geometry(room.p0)
    out_ = []
    mats = [((1, 0), (0, 0)), ((0, 0), (0, 1))] if axial_scalings else [((1, 0), (0, 1))]
    # translations
    for tv in ((1, 0), (0, 1)):
        v = [dot(room.nrm[i], tv) for i in range(room.n)] + [F(tv[0]), F(tv[1]), F(tv[0]), F(tv[1])]
        out_.append(('transl' + str(tv), v))
    for A in mats:
        Av = lambda x: (A[0][0] * x[0] + A[0][1] * x[1], A[1][0] * x[0] + A[1][1] * x[1])
        v = [dot(room.nrm[i], Av(V[i])) for i in range(room.n)] + list(Av(S)) + list(Av(T))
        out_.append(('scale' + str(A), [F(x) for x in v]))
    return out_


def cell_basis(room):
    """axial weak-order cell: one parameter per distinct x value and per distinct y value."""
    V, S, T = room.geometry(room.p0)
    xs = sorted({v[0] for v in V} | {S[0], T[0]})
    ys = sorted({v[1] for v in V} | {S[1], T[1]})
    k = len(xs) + len(ys)
    cols = []
    for j in range(k):
        v = [F(0)] * room.dim
        for i in range(room.n):
            nx, ny = room.nrm[i]
            if j < len(xs) and nx != 0 and V[i][0] == xs[j]:
                v[i] = F(nx)
            if j >= len(xs) and ny != 0 and V[i][1] == ys[j - len(xs)]:
                v[i] = F(ny)
        for m, P in ((room.n, S), (room.n + 2, T)):
            if j < len(xs) and P[0] == xs[j]:
                v[m] = F(1)
            if j >= len(xs) and P[1] == ys[j - len(xs)]:
                v[m + 1] = F(1)
        cols.append(v)
    return cols, len(xs), len(ys)


def positive_dependence(G):
    """exact phase-1 simplex: is there y > 0 (all entries) with sum_i y_i G_i = 0 ?
    Equivalent (Farkas/Gordan) to: {v : G v <= 0} equals ker G."""
    m, d = len(G), len(G[0])
    # y = 1 + w, w >= 0 :  G^T w = -G^T 1
    A = [[G[i][j] for i in range(m)] for j in range(d)]
    b = [-sum(G[i][j] for i in range(m)) for j in range(d)]
    for j in range(d):
        if b[j] < 0:
            A[j] = [-x for x in A[j]]
            b[j] = -b[j]
    # tableau with artificials
    nv = m + d
    tab = [A[j] + [F(1) if k == j else F(0) for k in range(d)] + [b[j]] for j in range(d)]
    basis = [m + j for j in range(d)]
    cost = [F(0)] * m + [F(1)] * d
    while True:
        # reduced costs
        red = []
        for c in range(nv):
            red.append(cost[c] - sum(cost[basis[r]] * tab[r][c] for r in range(d)))
        enter = next((c for c in range(nv) if red[c] < 0), None)
        if enter is None:
            break
        ratios = [(tab[r][-1] / tab[r][enter], basis[r], r) for r in range(d) if tab[r][enter] > 0]
        if not ratios:
            return None
        _, _, r = min(ratios)
        pv = tab[r][enter]
        tab[r] = [x / pv for x in tab[r]]
        for rr in range(d):
            if rr != r and tab[rr][enter] != 0:
                f = tab[rr][enter]
                tab[rr] = [a - f * bb for a, bb in zip(tab[rr], tab[r])]
        basis[r] = enter
    val = sum(cost[basis[r]] * tab[r][-1] for r in range(d))
    return val == 0


def lemma_replay(room, tp, rowv, AB, vdir, eps):
    """perturb p0 + s*eps*vdir for s=+-1, trace the developed chord in the perturbed room."""
    res = []
    for s in (1, -1):
        p = [a + s * eps * b for a, b in zip(room.p0, vdir)]
        V, S, T = room.geometry(p)
        A, B = AB
        a, b = ev(A, p), ev(B, p)
        Dv = det(a, b)
        chord = (a[0] + b[0], a[1] + b[1])
        # trace in the perturbed room from S along chord; legal iff T reached before any corner
        gid = (ID, ([F(0)] * room.dim, [F(0)] * room.dim))
        evs = trace(room, V, S, T, S, chord, gid, False, True)
        hitT = any(e[0] == 'T' and e[2] == 1 for e in evs)       # along the template itinerary
        other = any(e[0] == 'T' and e[2] != 1 for e in evs)
        # also the T hit must precede the stop; trace() records T only before the stopping hit
        res.append((s, Dv, tp['sigma'] * Dv > 0, hitT, other))
    return res


# ------------------------------------------------------------------ named rooms
ROOMS = []
# lit control: L-room, direct segment S-T passes the reflex corner (2,2)
ROOMS.append(Room("Lroom 4x4 notch 2 (lit control)", [(0, 0), (4, 0), (4, 2), (2, 2), (2, 4), (0, 4)], (1, 3), (3, 1)))
# r=4 dumbbell of length-periodicity.md: widths U, U+1, height 5, unit door y in (2,3), corridor L
def dumbbell(U, L):
    a, b, c = U, U + L, 2 * U + L + 1
    V = [(0, 0), (a, 0), (a, 2), (b, 2), (b, 0), (c, 0), (c, 5), (b, 5), (b, 3), (a, 3), (a, 5), (0, 5)]
    return Room(f"dumbbell U={U} L={L}, S=(2,1), T=(U+L+2,3)", V, (2, 1), (U + L + 2, 3))
ROOMS.append(dumbbell(4, 1))
# R22 / room Q (RESULTS R24): 22 walls, area 15, dark pair (0,0),(2,2)
R22V = [(-1, -1), (-1, 1), (0, 1), (0, 2), (1, 2), (1, 3), (3, 3), (3, 2), (4, 2), (4, 1), (5, 1), (5, 0), (3, 0), (3, 1),
        (1, 1), (1, -1), (2, -1), (2, -3), (1, -3), (1, -2), (0, -2), (0, -1)]
R22 = None
try:
    R22 = Room("R22 (room Q, dark pair (0,0),(2,2))", R22V, (0, 0), (2, 2))
except ValueError:
    R22 = Room("R22 (room Q, dark pair (0,0),(2,2))", R22V[::-1], (0, 0), (2, 2))
ROOMS.append(R22)
# mixed control (d135 room B, V-notch): S-T segment passes the 270-degree corner (2,2)
ROOMS.append(Room("mixed V-notch (d135 B), S=(1,2), T=(3,2)", [(0, 0), (4, 0), (4, 4), (2, 2), (0, 4)], (1, 2), (3, 2)))

# self-test of the exact positive-dependence LP
_t = lambda G: positive_dependence([[F(x) for x in r] for r in G])
assert _t([[1, 0], [-1, 0], [0, 1], [0, -1]]) is True
assert _t([[1, 0], [0, 1]]) is False
assert _t([[1, 0], [-1, 0], [0, 1]]) is False
assert _t([[1, 1], [-1, 0], [0, -1]]) is True
out("LP self-test passed (4 cases)")

NS = (4, 6, 8, 10)
summary = []
for room in ROOMS:
    out("=" * 78)
    out("ROOM", room.name, "| walls", room.n, "| mixed" if room.mixed else "| axial", "| chart dim", room.dim)
    triv = trivial(room, not room.mixed)
    out("  trivial motions (translations + admissible scalings):", len(triv))
    allrows = {}
    for N in NS:
        t1 = time.process_time()
        tm, direct, st = templates(room, N)
        rows = []
        for tp in tm:
            rv, rho, AB = row_of(room, tp)
            rows.append((tp, rv, rho, AB))
        rk = rank([r[1] for r in rows], room.dim) if rows else 0
        bad = [(nm, max(abs(dot(r[1], v)) for r in rows)) for nm, v in triv] if rows else []
        out(f"  N={N:2d}: dirs {st['dirs']}, corner-first {st['corner']}, periodic {st['periodic']}, cap {st['cap']}, "
            f"direct legal dirs {len(direct)}, templates {len(tm)}, chart rank {rk}, kernel dim {room.dim - rk}"
            f"  [{time.process_time() - t1:.1f}s]")
        if bad:
            out("        max |row . trivial| =", max(b for _, b in bad))
        allrows[N] = rows
    rows = allrows[NS[-1]]
    R = [r[1] for r in rows]
    kd = room.dim - rank(R, room.dim) if R else room.dim
    tdim = rank([v for _, v in triv], room.dim)
    joint = rank(R + [v for _, v in triv], room.dim) if R else tdim
    out(f"  chart: kernel dim {kd}; trivial dim {tdim}; kernel == trivial span: {kd == tdim and room.dim - joint == 0 or kd == tdim}")
    if R:
        K = nullspace(R, room.dim)
        extra = rank(K + [v for _, v in triv], room.dim) - tdim
        out(f"  chart: kernel directions beyond trivial: {extra}")
    if not room.mixed:
        cols, nx, ny = cell_basis(room)
        Rc = [[dot(r, c) for c in cols] for r in R]
        k = len(cols)
        rc = rank(Rc, k) if Rc else 0
        out(f"  weak-order cell: {nx} x-values + {ny} y-values = {k} params (unanchored); rank {rc}; "
            f"kernel dim {k - rc} (trivial = 4: two translations + two axis scalings)")
    nz = [r for r in rows if any(x != 0 for x in r[1])]
    out(f"  templates with nonzero row: {len(nz)} of {len(rows)}; distinct rho values: "
        f"{sorted(set(r[2] for r in rows))[:8]}{' ...' if len(set(r[2] for r in rows)) > 8 else ''}")
    summary.append((room.name, room.dim, kd, tdim))
    # ------------------------------------------------ opening-lemma replay
    rng = random.Random(7)
    picks = nz[:: max(1, len(nz) // 12)][:12]
    out("  opening-lemma replay (perturb along v, eps=1/4000, both signs; legal-by-sign? / template itinerary reaches T before any corner?):")
    agree = 0
    tot = 0
    reg_both = reg_tot = 0
    for tp, rv, rho, AB in picks:
        # v: random small integer direction with nonzero pairing
        for _ in range(20):
            v = [F(rng.randint(-2, 2)) for _ in range(room.dim)]
            if dot(rv, v) != 0:
                break
        res = lemma_replay(room, tp, rv, AB, v, F(1, 4000))
        line = []
        for s, Dv, pred, hit, other in res:
            if room.regular[tp['vi']]:
                reg_tot += 1
                reg_both += hit
            else:
                tot += 1
                agree += (pred == hit)
            line.append(f"s={s:+d}: sign(sigma*D)={'+' if pred else '-'} itinerary={'LEGAL' if hit else 'blocked'}"
                        + (" (T also hit at another time)" if other else ""))
        kind = f"regular a={room.anum[tp['vi']]}" if room.regular[tp['vi']] else f"singular a={room.anum[tp['vi']]}"
        out(f"    dir {tuple(int(x) for x in tp['d'])} corner v{tp['vi']} ({kind}) side {tp['sigma']:+d} rho {rho}: " + " | ".join(line))
    out(f"  lemma replay, singular corners: predicted legal == itinerary legal in {agree}/{tot}")
    out(f"  lemma replay, regular forbidden corners: itinerary legal in {reg_both}/{reg_tot} (both signs expected)")
    # ------------------------------------------------ one-sided (cone) upgrade
    G = []
    for tp, rv, rho, AB in rows:
        if room.regular[tp['vi']]:
            G.append(rv)
            G.append([-x for x in rv])
        else:
            G.append([tp['sigma'] * x for x in rv])
    if G:
        pd = positive_dependence(G)
        out(f"  one-sided dark tangent cone {{v: sigma_i l_i(v) <= 0}} equals the kernel: {pd} "
            f"({len(G)} sign rows; True means no one-sided nontrivial first-order dark direction, any cell)")

out("=" * 78)
out("SUMMARY (chart = wall offsets + marks, unanchored; trivial = translations + admissible scalings)")
for nm, dim, kd, td in summary:
    out(f"  {nm}: chart dim {dim}, kernel dim {kd}, trivial dim {td}")
out(f"CPU seconds: {time.process_time() - T0:.1f}")
