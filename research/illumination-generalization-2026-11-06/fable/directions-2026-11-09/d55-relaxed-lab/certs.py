"""Theorem U certificates for relaxed rooms (slits, pinches), adapted from d10 unified_test.py.

DP is built by d4_monodromy.Room (copied from d6) with the slit edges as walls; its sheets are
the cells, t = (g_a, g_b, g_c, g_d) in the roomtools convention (class origin at S).

Over the base B, for each lift pair (sigma over S, tau over T) and each target corner x:
  Par(x)   c_s = c_t; phi(sigma) != phi(tau); N has no regular point over x.      (unchanged)
  Rig(x)   N has identity monodromy at a corner y outside {c_s, x}; phi(tau) is outside the
           live component of phi(sigma) along the tail arc c_s -> x.               (unchanged;
           for c_s != c_t, tau's x-point is tested)
  Cut+(x)  d10 Cut(x) plus: phi is branched only over poles of N (every Q-point over a non-pole
           of N has e = 1).  Needed because a slit tip is a 4-cycle and may lie with e = 2 over
           a regular point of N; the d10 Cut proof uses Fact L at exactly this step.
  Cut(x)   the unadapted d10 rule, recorded separately (never counted as a certificate).
Relative bases P' (pillowcase factors other than B, d10 ParRel / RigRel) are used only when
H0 holds: every Q-point over a regular (non-corner) point of P' is regular, so Lemma 0 holds.
Factors N are all block systems of the monodromy group (d4.all_block_systems), so the search
is exhaustive over factors of DP.

Canonical cross-check (theory.md R3, adapted): Par(x) holds for some factor iff some C_M
separates, where C_M = closure of the 2-cycles of g_x plus the full 4-cycles of g_x in M,
M any subset of the 4-cycles over x, keeping only C_M with no regular point over x.
Rig(x) with identity at y holds iff it holds for R_y.
"""
import sys
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'lib'))
import d4_monodromy as d4                    # noqa: E402
from hurwitz import mul, inv, ident, cycles, cycle_index, marked_orbit, initial_pt  # noqa: E402

OFFS = {(0, 0): 0, (1, 0): 1, (1, 1): 2, (0, 1): 3}


class Factor:
    def __init__(self, t, part):
        n = len(t[0])
        self.part = part
        self.m = len(part)
        self.where = [0] * n
        for b, blk in enumerate(part):
            for s in blk:
                self.where[s] = b
        self.ig = [d4.induced(g, part) for g in t]
        self.ncid, self.nlen, self.live = [], [], []
        for y in range(4):
            cid = [0] * self.m
            lens = []
            for k, cy in enumerate(cycles(self.ig[y])):
                lens.append(len(cy))
                for b in cy:
                    cid[b] = k
            live = [False] * len(lens)
            for c in cycles(t[y]):
                if len(c) == 2:
                    live[cid[self.where[c[0]]]] = True
            self.ncid.append(cid)
            self.nlen.append(lens)
            self.live.append(live)

    def point(self, y, sheet):
        return self.ncid[y][self.where[sheet]]

    def live_component(self, x, start, cs=0):
        """Vertices ('s', k) / ('x', k) in the live component of the cs-point `start` along the
        tail arc cs -> x (edges: one per block, joining its cs-point and its x-point)."""
        if not self.live[cs][start]:
            return {('s', start)}
        adj = {}
        for b in range(self.m):
            u, v = ('s', self.ncid[cs][b]), ('x', self.ncid[x][b])
            if self.live[cs][u[1]] and self.live[x][v[1]]:
                adj.setdefault(u, set()).add(v)
                adj.setdefault(v, set()).add(u)
        seen = {('s', start)}
        stack = [('s', start)]
        while stack:
            u = stack.pop()
            for v in adj.get(u, ()):
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        return seen


def qlen_table(t):
    n = len(t[0])
    out = []
    for y in range(4):
        L = [0] * n
        for c in cycles(t[y]):
            for i in c:
                L[i] = len(c)
        out.append(L)
    return out


def par(F, x, s, q):
    return F.point(0, s) != F.point(0, q) and 2 not in F.nlen[x]


def rig(F, x, s, q, xt=0):
    """xt = corner of tau (0 for same class, then the a-point of tau is tested)."""
    if not any(all(l == 1 for l in F.nlen[y]) for y in (1, 2, 3) if y not in (x, xt)):
        return False
    comp = F.live_component(x, F.point(0, s))
    tgt = ('s', F.point(0, q)) if xt == 0 else ('x', F.point(xt, q))
    return tgt not in comp


def cut_d10(F, t, x, s, q):
    if F.point(0, s) != F.point(0, q):
        return False
    for y in (0, x):
        for c in cycles(t[y]):
            if len(c) == 2 and F.nlen[y][F.ncid[y][F.where[c[0]]]] != 2:
                return False
    return any(len(F.nlen[y]) == 1 for y in (1, 2, 3) if y != x)


def unbranched_off_poles(F, t, QL):
    for y in range(4):
        for c in cycles(t[y]):
            k = F.ncid[y][F.where[c[0]]]
            if F.nlen[y][k] >= 2 and F.nlen[y][k] != len(c):
                return False
    return True


def cut_plus(F, t, x, s, q, QL):
    return cut_d10(F, t, x, s, q) and unbranched_off_poles(F, t, QL)


def is_pillowcase(F):
    lens = [l for y in range(4) for l in F.nlen[y]]
    return max(lens) <= 2 and lens.count(1) == 4


def h0(Pp, t):
    """Q -> P' unbranched off the P'-corners: a Q-cycle over a regular P'-point is a 2-cycle."""
    for y in range(4):
        for c in cycles(t[y]):
            if Pp.nlen[y][Pp.ncid[y][Pp.where[c[0]]]] == 2 and len(c) != 2:
                return False
    return True


def refines(small, big):
    return all(len({big.where[s] for s in blk}) == 1 for blk in small.part)


def corners_of(Pp):
    return [(y, b) for y in range(4) for b in range(Pp.m) if Pp.ig[y][b] == b]


def n_points_over(N, Pp, corner):
    y, beta = corner
    return {N.ncid[y][sb] for sb in range(N.m) if Pp.where[N.part[sb][0]] == beta}


def tail_end(Pp, j, beta):
    side, cur = j, beta
    while True:
        nxt = Pp.ig[side][cur]
        if nxt == cur:
            return (side, cur)
        cur = nxt
        side = 0 if side == j else j


def relative(t, factors, s, q, xt):
    """d10 ParRel / RigRel over a proper pillowcase factor satisfying H0.  Returns (kind, deg P'->B)."""
    n = len(t[0])
    for Pp in factors:
        if Pp.m == 1 or Pp.m == n or not is_pillowcase(Pp) or not h0(Pp, t):
            continue
        bs, bq = Pp.where[s], Pp.where[q]
        if Pp.ig[0][bs] != bs or Pp.ig[xt][bq] != bq:
            continue
        mids = [N for N in factors if N.m >= Pp.m and refines(N, Pp)]
        cs, ct = (0, bs), (xt, bq)
        if cs == ct:
            ok = True
            for c in [c for c in corners_of(Pp) if c != cs]:
                if not any(N.point(0, s) != N.point(0, q)
                           and all(N.nlen[c[0]][k] != 2 for k in n_points_over(N, Pp, c))
                           for N in mids):
                    ok = False
                    break
            if ok:
                return ('ParRel', Pp.m)
        else:
            arcs = [j for j in (1, 2, 3) if tail_end(Pp, j, bs) == ct]
            if not arcs:
                continue
            j = arcs[0]
            third = [c for c in corners_of(Pp) if c not in (cs, ct)]
            for N in mids:
                if not any(all(N.nlen[c[0]][k] == 1 for k in n_points_over(N, Pp, c)) for c in third):
                    continue
                tgt = ('s', N.point(0, q)) if xt == 0 else ('x', N.point(j, q))
                if tgt not in N.live_component(j, N.point(0, s)):
                    return ('RigRel', Pp.m)
    return None


def build(cells, slits, S):
    ox, oy = S
    sc = sorted((i - ox, j - oy) for (i, j) in cells)
    ss = [((p[0] - ox, p[1] - oy), (q[0] - ox, q[1] - oy)) for (p, q) in slits]
    room = d4.Room('room', 'square', sc, [], slits=ss)
    g = room.gen
    t = (g[(0, 0)], inv(g[(1, 0)]), g[(1, 1)], inv(g[(0, 1)]))
    assert mul(mul(mul(t[0], t[1]), t[2]), t[3]) == ident(room.degree)
    return room, t


def lifts_at(room, p, S):
    """Regular points (2-cycles) of DP over room point p; returns (corner index, [sheet lists])."""
    q = (p[0] - S[0], p[1] - S[1])
    c, pts = room.points_at(q)
    return OFFS[c], [sorted(cy) for cy in pts if len(cy) == 2]


class RoomCert:
    def __init__(self, cells, slits, S):
        self.S = S
        self.room, self.t = build(cells, slits, S)
        n = len(self.t[0])
        self.QL = qlen_table(self.t)
        self.systems = d4.all_block_systems(list(self.t), n)
        self.factors = [Factor(self.t, p) for p in self.systems]

    def lift_pair(self, s, q, xt):
        """Certificate data for one lift pair; xt = corner index of tau."""
        t, QL = self.t, self.QL
        proper = [F for F in self.factors if F.m > 1]
        targets = (1, 2, 3) if xt == 0 else (xt,)
        perx = {}
        degs = {}
        cutd10 = {}
        for x in targets:
            kinds = set()
            dset = set()
            cd = False
            for F in proper:
                k = set()
                if xt == 0 and par(F, x, s, q):
                    k.add('Par')
                if rig(F, x, s, q, xt):
                    k.add('Rig')
                if xt == 0 and cut_d10(F, t, x, s, q):
                    cd = True
                    if cut_plus(F, t, x, s, q, QL):
                        k.add('Cut')
                if k:
                    kinds |= k
                    dset.add(F.m)
            perx[x] = kinds
            degs[x] = sorted(dset)
            cutd10[x] = cd
        over_b = all(perx[x] for x in targets)
        rel = None if over_b else relative(t, self.factors, s, q, xt)
        return dict(perx=perx, degs=degs, over_b=over_b, rel=rel, cutd10=cutd10)

    def canonical(self, s, q, xt):
        """R3-style canonical verdicts per target: (Par via C_M, Rig via R_y)."""
        t = self.t
        n = len(t[0])
        out = {}
        targets = (1, 2, 3) if xt == 0 else (xt,)
        for x in targets:
            cp = False
            if xt == 0:
                two = [tuple(c) for c in cycles(t[x]) if len(c) == 2]
                four = [c for c in cycles(t[x]) if len(c) == 4]
                for k in range(len(four) + 1):
                    for M in combinations(range(len(four)), k):
                        seeds = list(two)
                        for i in M:
                            seeds += [(four[i][0], z) for z in four[i][1:]]
                        part = closure(n, t, seeds)
                        F = Factor(t, part)
                        if F.m > 1 and par(F, x, s, q):
                            cp = True
            cr = False
            for y in (1, 2, 3):
                if y in (x, xt):
                    continue
                seeds = [(c[0], z) for c in cycles(t[y]) for z in c[1:]]
                part = closure(n, t, seeds)
                F = Factor(t, part)
                if F.m > 1 and rig(F, x, s, q, xt):
                    cr = True
            out[x] = (cp, cr)
        return out


def closure(n, gens, seeds):
    par_ = list(range(n))

    def find(a):
        while par_[a] != a:
            par_[a] = par_[par_[a]]
            a = par_[a]
        return a

    queue = []
    for a, b in seeds:
        ra, rb = find(a), find(b)
        if ra != rb:
            par_[ra] = rb
            queue.append((a, b))
    allg = list(gens) + [inv(g) for g in gens]
    while queue:
        a, b = queue.pop()
        for g in allg:
            ra, rb = find(g[a]), find(g[b])
            if ra != rb:
                par_[ra] = rb
                queue.append((g[a], g[b]))
    blocks = {}
    for a in range(n):
        blocks.setdefault(find(a), []).append(a)
    return sorted(blocks.values())


def certify_pair(cells, slits, S, T, want_canonical=True):
    """Classify the pair (S, T): returns dict with per-lift-pair data and an overall class."""
    rc = RoomCert(cells, slits, S)
    xs, LS = lifts_at(rc.room, S, S)
    xt, LT = lifts_at(rc.room, T, S)
    assert xs == 0 and len(LS) == 2 and len(LT) == 2
    res = []
    for a in LS:
        for b in LT:
            d = rc.lift_pair(a[0], b[0], xt)
            if want_canonical:
                d['canon'] = rc.canonical(a[0], b[0], xt)
            d['full'] = d['over_b'] or d['rel'] is not None
            res.append(d)
    nfull = sum(d['full'] for d in res)
    cls = 'full' if nfull == 4 else ('partial' if (nfull or any(d['perx'][x] for d in res for x in d['perx']))
                                     else 'none')
    return dict(xt=xt, n=len(rc.t[0]), lifts=res, cls=cls, nblocksystems=len(rc.systems))


def hurwitz_dark(cells, slits, S, T, max_states=2_000_000):
    """Independent exact check (d6 marked_orbit on the pillowcase cover DP).  Same-class pairs are
    tested directly; a different-class pair is tested in the room scaled by 2, where both marks
    are in the class of 2S.  Returns (dark, states, complete)."""
    if (S[0] - T[0]) % 2 or (S[1] - T[1]) % 2:
        cells2 = {(2 * i + u, 2 * j + v) for (i, j) in cells for u in (0, 1) for v in (0, 1)}
        slits2 = set()
        for (p, q) in slits:
            m = (p[0] + q[0], p[1] + q[1])
            slits2.add(((2 * p[0], 2 * p[1]), m) if (2 * p[0], 2 * p[1]) < m else (m, (2 * p[0], 2 * p[1])))
            slits2.add((m, (2 * q[0], 2 * q[1])) if m < (2 * q[0], 2 * q[1]) else ((2 * q[0], 2 * q[1]), m))
        cells, slits, S, T = cells2, slits2, (2 * S[0], 2 * S[1]), (2 * T[0], 2 * T[1])
    room, t = build(cells, slits, S)
    _, LS = lifts_at(room, S, S)
    xt, LT = lifts_at(room, T, S)
    assert xt == 0
    pt, plen = initial_pt(t[0])
    targets = {frozenset((pt[a[0]], pt[b[0]])) for a in LS for b in LT}
    res = marked_orbit(t, max_states=max_states, targets=targets)
    lit = bool(res['lit'] & targets)
    return (not lit), res['states'], res['complete'] or lit
