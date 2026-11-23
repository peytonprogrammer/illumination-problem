"""d166 checks for parallel-dent-frontier.2026-11-22-0758.md.

Run: python3 -B checks.py > checks.log
Named, explicit rooms only. No room search. trace() is copied verbatim from
d164-attack-combs/attack.py (itself from d162/d161): an exact Fraction ray tracer that
reflects off walls and stops at every vertex.
"""
import json, os, random, time
from fractions import Fraction as F
from math import floor, gcd

T0 = time.process_time()
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.dirname(HERE)


def log(*a):
    print(*a, flush=True)


# ------------------------------------------------------------------ copied from d164 attack.py
def trace(P, A, B, maxrefl=10**6):
    n = len(P)
    hw = [(P[i], P[(i + 1) % n]) for i in range(n) if P[i][1] == P[(i + 1) % n][1]]
    vw = [(P[i], P[(i + 1) % n]) for i in range(n) if P[i][0] == P[(i + 1) % n][0]]
    V = {(F(a), F(b)) for a, b in P}
    X, Y = F(A[0]), F(A[1])
    vx, vy = F(B[0]) - X, F(B[1]) - Y
    tau, contacts = F(1), []
    for _ in range(maxrefl):
        best = None
        if vx:
            for a, b in vw:
                t = (a[0] - X) / vx
                if t > 0 and (best is None or t < best[0]) and min(a[1], b[1]) <= Y + vy * t <= max(a[1], b[1]):
                    best = (t, 'v')
        if vy:
            for a, b in hw:
                t = (a[1] - Y) / vy
                if t > 0 and (best is None or t < best[0]) and min(a[0], b[0]) <= X + vx * t <= max(a[0], b[0]):
                    best = (t, 'h')
        if best is None or best[0] > tau:
            return 'end', (X + vx * tau, Y + vy * tau), contacts
        t, kind = best
        X, Y = X + vx * t, Y + vy * t
        if best[0] == tau:
            return 'wall-end', (X, Y), contacts
        tau -= t
        if (X, Y) in V:
            return 'corner', (X, Y), contacts
        contacts.append(((X, Y), kind))
        if kind == 'v': vx = -vx
        else: vy = -vy
    return 'limit', (X, Y), contacts


# ------------------------------------------------------------------ geometry helpers (own)
def clean(P):
    """Drop repeated and collinear vertices."""
    P = [tuple(map(F, p)) for p in P]
    Q = []
    for p in P:
        if not Q or Q[-1] != p: Q.append(p)
    if Q[0] == Q[-1]: Q.pop()
    changed = True
    while changed:
        changed = False
        n = len(Q)
        for i in range(n):
            a, b, c = Q[i - 1], Q[i], Q[(i + 1) % n]
            if (a[0] == b[0] == c[0]) or (a[1] == b[1] == c[1]):
                Q.pop(i); changed = True; break
    return Q


def turn_word(P):
    n = len(P); s = []
    for i in range(n):
        a, b, c = P[i - 1], P[i], P[(i + 1) % n]
        cr = (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])
        s.append('L' if cr > 0 else 'R')
    return ''.join(s)


def canon(w):
    rots = [w[i:] + w[:i] for i in range(len(w))]
    rv = w[::-1]
    rots += [rv[i:] + rv[:i] for i in range(len(w))]
    return min(rots)


def sections(P, axis, c):
    """Open sections of the polygon by the line coord[axis] = c (c not a vertex level)."""
    o = 1 - axis; n = len(P); xs = []
    for i in range(n):
        a, b = P[i], P[(i + 1) % n]
        if a[o] == b[o] and min(a[axis], b[axis]) < c < max(a[axis], b[axis]):
            xs.append(a[o])
    xs.sort()
    return [(xs[i], xs[i + 1]) for i in range(0, len(xs), 2)]


def dents(P, word):
    n = len(P); h = v = 0
    for i in range(n):
        j = (i + 1) % n
        if word[i] == 'R' and word[j] == 'R':
            if P[i][1] == P[j][1]: h += 1
            else: v += 1
    return h, v


def spanning(P, axis):
    """Is there a strip between consecutive levels (coord[axis]) whose section spans the bbox?"""
    o = 1 - axis
    lev = sorted({p[axis] for p in P}); lo, hi = min(p[o] for p in P), max(p[o] for p in P)
    return any(sections(P, axis, (lev[i] + lev[i + 1]) / 2) == [(lo, hi)] for i in range(len(lev) - 1))


# ------------------------------------------------------------------ 1. ledger bookkeeping
def part1():
    log('## 1. Ledger bookkeeping (ledger.json, original d163 statuses)')
    d = json.load(open(os.path.join(D, 'd163-pattern-ledger', 'ledger.json')))
    W = d['words']
    t1, bad = [], 0
    for w, e in W.items():
        P = clean(e['realization'])
        tw = turn_word(P)
        if canon(tw) != canon(w): bad += 1
        h, v = dents(P, tw)
        if (h, v) != tuple(sorted(e['dent_profile'])) and (v, h) != tuple(e['dent_profile']) and (h, v) != tuple(e['dent_profile']):
            bad += 1
        if e['status'] == 'OPEN' and (h == 0 or v == 0):
            t1.append((w, e, P, h, v))
    log(f'realization word / dent-count mismatches: {bad}')
    dented = [x for x in t1 if x[3] + x[4] > 0]
    log(f'target 1 (OPEN, all dents parallel): {len(t1)} = {len(dented)} dented + {len(t1) - len(dented)} undented')
    byW = {}
    for x in t1: byW[x[1]["W"]] = byW.get(x[1]["W"], 0) + 1
    log(f'  by W: {dict(sorted(byW.items()))}')
    # hall direction: horizontal dents -> columns are intervals -> need a full-width horizontal strip
    noh, noh_any = [], []
    for w, e, P, h, v in dented:
        ax = 1 if h else 0  # axis=1: strip between y-levels (horizontal band)
        if not spanning(P, ax): noh.append((e['W'], w, P))
        if not spanning(P, 0) and not spanning(P, 1): noh_any.append(w)
    log(f'dented target-1 words whose ledger realization has no spanning hall strip '
        f'(strip parallel to the dents): {len(noh)}')
    log(f'  ... with no spanning strip in either direction: {len(noh_any)}')
    first = [x for x in noh if x[0] == min(y[0] for y in noh)]
    log(f'  smallest W = {first[0][0]}, words there: {[x[1] for x in first]}')
    log(f'  first in ledger order: {first[0][1]} {[(int(a), int(b)) for a, b in first[0][2]]}')
    want = [(0, 2), (0, 0), (1, 0), (1, 1), (5, 1), (5, 5), (4, 5), (4, 4), (2, 4), (2, 3), (3, 3), (3, 2)]
    e = W['LLLRLLLRLLRR']
    log(f'  LLLRLLLRLLRR: W={e["W"]}, status={e["status"]}, coords match note: {[tuple(p) for p in e["realization"]] == want}, '
        f'word check {canon(turn_word(clean(want))) == canon("LLLRLLLRLLRR")}')
    opens = sorted((e['W'], w) for w, e in W.items() if e['status'] == 'OPEN')
    minW = opens[0][0]
    log(f'smallest OPEN W = {minW}; OPEN words there: {len([1 for x in opens if x[0] == minW])}; '
        f'all in target 1: {all(any(t[0] == w for t in t1) for Wd, w in opens if Wd == minW)}')
    want = [(2, 0), (4, 0), (4, 1), (3, 1), (3, 4), (0, 4), (0, 3), (1, 3), (1, 2), (2, 2)]
    e = W['LLLRLLLRLR']
    log(f'  LLLRLLLRLR: W={e["W"]}, status={e["status"]}, polygon matches note: {[tuple(p) for p in e["realization"]] == want}, '
        f'first in ledger order among W=10 OPEN: {[w for w in W if W[w]["W"] == 10 and W[w]["status"] == "OPEN"][0]}')
    s10 = d['named_rooms']['S10 (d65)']
    e = W[s10['word']]
    log(f'S10 word {s10["word"]}: status {e["status"]}, in target 1: {any(t[0] == s10["word"] for t in t1)}, '
        f'W={s10["W"]}, area={s10["area"]}')
    return s10


# ------------------------------------------------------------------ 2. the joint criterion
def fgcd(x, y):
    x, y = F(x), F(y)
    den = x.denominator * y.denominator // gcd(x.denominator, y.denominator)
    return F(gcd(int(x * den), int(y * den)), den)


class Joint:
    """Lower band [l,l+u] x [0,h1], upper band [m,m+v] x [h1,h1+h2]; joint at y = h1."""

    def __init__(self, name, l, u, m, v, h1, h2):
        self.name = name
        self.l, self.u, self.m, self.v, self.h1, self.h2 = map(F, (l, u, m, v, h1, h2))
        l, u, m, v, h1, h2 = self.l, self.u, self.m, self.v, self.h1, self.h2
        self.P = clean([(l, 0), (l + u, 0), (l + u, h1), (m + v, h1), (m + v, h1 + h2), (m, h1 + h2), (m, h1), (l, h1)])
        self.I = (max(l, m), min(l + u, m + v))
        self.flush = set()
        if l == m: self.flush.add(l)
        if l + u == m + v: self.flush.add(l + u)
        xs = [p[0] for p in self.P]
        st = F(0)
        for x in xs: st = fgcd(st, x) if st else abs(x) or st
        self.lam = st  # x-orbit of any point under the room's vertical mirrors lies in +-x + 2*lam*Z
        self.kind = ('flush ' if self.flush else 'staggered ') + str(sorted(self.flush))

    def inI(self, X, flush):
        return self.I[0] < X < self.I[1] or (flush and X in self.flush)

    def params(self, a, b, xi, eta):
        Dd = a + b
        return Dd, (b * self.l + a * self.m) / Dd, b * xi / Dd, a * eta / Dd, 2 * b * self.u / Dd, 2 * a * self.v / Dd

    def crit(self, a, b, xi, eta, flush=False):
        """Exact (unbounded) criterion by residues mod g."""
        Dd, om, p, q, P1, P2 = self.params(a, b, xi, eta)
        g = fgcd(P1, P2)
        for r in (om + p + q, om + p - q, om - p + q, om - p - q):
            n = floor((self.I[0] - r) / g)
            for k in (n, n + 1, n + 2):
                if self.inI(r + k * g, flush): return True
        return False

    def crit_bounded(self, a, b, xi, eta, dmax, flush=False):
        """Enumerate developed images s', t' with |t'-s'| <= dmax and test the crossing."""
        Dd = a + b
        l, u, m, v = self.l, self.u, self.m, self.v
        K = int(dmax / (2 * min(u, v))) + 3
        for s in (l + xi, l - xi):
            for t in (m + eta, m - eta):
                for k in range(-K, K + 1):
                    sp = s + 2 * k * u
                    for j in range(-K, K + 1):
                        tp = t + 2 * j * v
                        if abs(tp - sp) <= dmax and self.inI((b * sp + a * tp) / Dd, flush):
                            return True
        return False

    def tracer(self, S, T, dmax):
        """Independent: aim at every +-T.x + 2*lam*n with |dx| <= dmax, trace physically."""
        hits = []
        for sg in (1, -1):
            base = sg * T[0]
            n0 = floor((S[0] - dmax - base) / (2 * self.lam))
            n1 = floor((S[0] + dmax - base) / (2 * self.lam)) + 1
            for n in range(n0, n1 + 1):
                tx = base + 2 * self.lam * n
                if abs(tx - S[0]) > dmax: continue
                st, end, con = trace(self.P, S, (tx, T[1]), maxrefl=10**4)
                if st == 'end' and end == T and all(k == 'v' for _, k in con):
                    hits.append((tx, con))
        return hits


def joints():
    return [
        Joint('J1 S-tetromino (note example)', 0, 2, 1, 2, 1, 1),
        Joint('J2 staggered, punctured mouth |I|=g at a=b', 0, 2, 1, 3, 2, F(3, 2)),
        Joint('J3 T-nested, v=17/12', 0, 3, 1, F(17, 12), 2, F(3, 2)),
        Joint('J4 flush L', 0, 2, 0, 1, 2, F(3, 2)),
        Joint('J5 flush right, v=99/70', 0, 3, 3 - F(99, 70), F(99, 70), F(3, 2), 2),
        Joint('J6 staggered S, u=7/5', 0, F(7, 5), F(1, 2), 1, F(3, 2), 1),
    ]


def marks(J, rng, nrand):
    """Half-lattice marks plus random rational marks, one in each band."""
    lo = [(J.l + F(i, 2), F(j, 2)) for i in range(1, 2 * int(J.u) + 4) for j in range(1, int(2 * J.h1))
          if J.l < J.l + F(i, 2) < J.l + J.u and 0 < F(j, 2) < J.h1]
    up = [(J.m + F(i, 2), J.h1 + F(j, 2)) for i in range(1, 2 * int(J.v) + 4) for j in range(1, int(2 * J.h2) + 1)
          if J.m < J.m + F(i, 2) < J.m + J.v and 0 < F(j, 2) < J.h2]
    pairs = [(S, T) for S in lo for T in up]
    for _ in range(nrand):
        S = (J.l + J.u * F(rng.randint(1, 96), 97), J.h1 * F(rng.randint(1, 88), 89))
        T = (J.m + J.v * F(rng.randint(1, 82), 83), J.h1 + J.h2 * F(rng.randint(1, 78), 79))
        pairs.append((S, T))
    return pairs


def part3():
    log('\n## 3. Criterion vs exact tracer on explicit two-band joints')
    log('tracer: every target image +-T.x + 2*lam*n (lam = gcd of wall abscissas), |dx| <= dmax, '
        'physical exact trace; a hit must end at T with vertical-wall contacts only.')
    rng = random.Random(166)
    tot = {}
    for J in joints():
        dmax = F(8) if J.lam < F(1, 20) else F(12)
        pairs = marks(J, rng, 40 if J.lam < F(1, 20) else 60)
        c = dict(n=0, open_vs_tr=0, flush_vs_tr=0, bounded_vs_exact=0, lit=0, flushonly=0)
        ex = []
        for S, T in pairs:
            a, b = J.h1 - S[1], T[1] - J.h1
            xi, eta = S[0] - J.l, T[0] - J.m
            tr = bool(J.tracer(S, T, dmax))
            co = J.crit_bounded(a, b, xi, eta, dmax, False)
            cf = J.crit_bounded(a, b, xi, eta, dmax, True)
            ce = J.crit(a, b, xi, eta, bool(J.flush))
            c['n'] += 1; c['lit'] += tr
            c['open_vs_tr'] += (co != tr); c['flush_vs_tr'] += (cf != tr)
            c['bounded_vs_exact'] += (cf != ce)
            if tr and not co:
                c['flushonly'] += 1
                if len(ex) < 2: ex.append((S, T))
        log(f'{J.name}: {J.kind}, I={tuple(map(str, J.I))}, lam={J.lam}, dmax={dmax}, P={[(str(x), str(y)) for x, y in J.P]}')
        log(f'   pairs {c["n"]}, tracer-lit {c["lit"]}; disagreements: open criterion {c["open_vs_tr"]}, '
            f'open+flush-endpoint criterion {c["flush_vs_tr"]}; bounded vs exact(residue) criterion {c["bounded_vs_exact"]}; '
            f'lit only through a flush endpoint {c["flushonly"]} e.g. {[(tuple(map(str, s)), tuple(map(str, t))) for s, t in ex]}')
        for k, x in c.items(): tot[k] = tot.get(k, 0) + x
    log(f'TOTAL {tot}   cpu {time.process_time() - T0:.1f}s')


# ------------------------------------------------------------------ note's explicit examples
def examples(s10):
    log('\n## 2b. The note\'s explicit examples')
    J = joints()[0]
    S, T = (F(3, 8), F(1, 2)), (F(11, 8), F(3, 2))
    Dd, om, p, q, P1, P2 = J.params(F(1, 2), F(1, 2), S[0], T[0] - 1)
    g = fgcd(P1, P2)
    res = sorted({(om + s * p + t * q) % g for s in (1, -1) for t in (1, -1)})
    log(f'S-tetromino: omega={om}, p={p}, q={q}, g={g}, residues {list(map(str, res))}, criterion {J.crit(F(1,2),F(1,2),S[0],T[0]-1)}, '
        f'tracer hits (|dx|<=12) {len(J.tracer(S, T, F(12)))}')
    st, end, con = trace(J.P, S, (F(11, 8), F(-3, 2)))
    log(f'   floor-bounce path: {st} at {tuple(map(str, end))}, contacts {[(tuple(map(str, x)), k) for x, k in con]}')
    P = clean(s10['vertices'])
    log(f'S10 polygon {[(int(x), int(y)) for x, y in P]}, word {canon(turn_word(P)) == canon("LLLRLRLLLRLR")}')
    for y in (F(1, 2), F(3, 2), F(5, 2), F(7, 2)):
        log(f'   runs at y={y}: {[(str(a), str(b)) for a, b in sections(P, 1, y)]}')
    Jx = Joint('S10 joint y=2', 1, 3, 0, 3, 1, 1)  # bands 2,3 of S10 shifted down by 1
    S, T = (F(5, 4), F(1, 2)), (F(1, 4), F(3, 2))
    Dd, om, p, q, P1, P2 = Jx.params(F(1, 2), F(1, 2), S[0] - 1, T[0])
    g = fgcd(P1, P2)
    log(f'   S10 joint: omega={om}, p={p}, q={q}, g={g}, criterion {Jx.crit(F(1,2),F(1,2),S[0]-1,T[0])}')
    # monotone tracer inside the full S10 room
    S, T = (F(5, 4), F(3, 2)), (F(1, 4), F(5, 2))
    mono = 0
    for sg in (1, -1):
        for n in range(-30, 31):
            tx = sg * T[0] + 2 * n
            st, end, con = trace(P, S, (tx, T[1]))
            mono += st == 'end' and end == T and all(k == 'v' for _, k in con)
    log(f'   S10 full room, monotone shots S->T with |n|<=30: {mono}')
    st, end, con = trace(P, S, (F(1, 4), F(11, 2)))
    log(f'   cap path direction {(F(1,4)-S[0], F(11,2)-S[1])}: {st} at {tuple(map(str, end))}, contacts '
        f'{[(tuple(map(str, x)), k) for x, k in con]}')
    hs = [sections(P, 1, y) for y in (F(1, 2), F(7, 2))]
    vs = [sections(P, 0, x) for x in (F(1, 2), F(7, 2))]
    log(f'   extreme horizontal sections {hs}, vertical sections {vs}')


# ------------------------------------------------------------------ 2c. all-abscissa corollary
def classify(J, a, b):
    Dd = a + b
    om = (b * J.l + a * J.m) / Dd
    g = fgcd(2 * b * J.u / Dd, 2 * a * J.v / Dd)
    lo, hi = J.I

    def inJ(r):
        n = floor((lo - r) / g) + 1
        return lo < r + n * g < hi

    def incl(r):
        n = floor((lo - r) / g)
        return any(lo <= r + k * g <= hi for k in (n, n + 1, n + 2))

    rs = [om, om + g / 2]
    if all(inJ(r) for r in rs): return 'all-clear', set(), g
    if not all(incl(r) for r in rs): return 'open-fail', None, g
    H = [r % g for r in rs if not inJ(r)]
    pred = set()
    pmax, qmax = b * J.u / Dd, a * J.v / Dd
    for i in range(4):
        for j in range(4):
            p0, q0 = i * g / 4, j * g / 4
            if (om + p0 + q0) % g in H and (om + p0 - q0) % g in H:
                for kp in range(0, int(pmax / g) + 2):
                    for kq in range(0, int(qmax / g) + 2):
                        p, q = p0 + kp * g, q0 + kq * g
                        if 0 < p < pmax and 0 < q < qmax: pred.add((p, q))
    return 'boundary', pred, g


def part2c():
    log('\n## 2c. All-abscissa corollary vs grid evaluation of the open criterion')
    rng = random.Random(7)
    for J in joints():
        levels = [(F(i, 4), F(j, 4)) for i in range(1, int(4 * J.h1)) for j in range(1, int(4 * J.h2))]
        levels += [(J.h1 * F(rng.randint(1, 30), 31), J.h2 * F(rng.randint(1, 30), 31)) for _ in range(4)]
        out = {}
        for a, b in levels:
            kind, pred, g = classify(J, a, b)
            Dd = a + b
            # grid in (p,q): step g/24, includes the quarter grid; p<b u/D, q<a v/D
            pmax, qmax = b * J.u / Dd, a * J.v / Dd
            st = g / 24
            ps = [st * i for i in range(1, int(pmax / st) + 1) if st * i < pmax]
            qs = [st * i for i in range(1, int(qmax / st) + 1) if st * i < qmax]
            if len(ps) * len(qs) > 6000:
                ps = ps[::max(1, len(ps) // 60)] + [x for x in ps if (x / (g / 4)).denominator == 1]
                qs = qs[::max(1, len(qs) // 60)] + [x for x in qs if (x / (g / 4)).denominator == 1]
            fails = {(p, q) for p in set(ps) for q in set(qs) if not J.crit(a, b, p * Dd / b, q * Dd / a)}
            ffl = {(p, q) for (p, q) in fails if not J.crit(a, b, p * Dd / b, q * Dd / a, True)} if J.flush else fails
            if kind == 'all-clear': ok = not fails
            elif kind == 'open-fail': ok = bool(fails)
            else: ok = fails == {x for x in pred if x[0] in set(ps) and x[1] in set(qs)}
            key = kind
            o = out.setdefault(key, [0, 0, 0, []])
            o[0] += 1; o[1] += ok; o[2] += (len(ffl) != len(fails))
            if kind == 'boundary' and len(o[3]) < 2: o[3].append((str(a), str(b), str(g), len(pred), len(ffl)))
        log(f'{J.name}: ' + '; '.join(f'{k}: {v[1]}/{v[0]} as predicted, flush endpoints change failures at {v[2]} levels'
                                     + (f', e.g. (a,b,g,#pred fails,#fails with flush) {v[3]}' if v[3] else '')
                                     for k, v in sorted(out.items())))
    # the punctured-circle example J2 at a=b=1: predicted single failing pair
    J = joints()[1]
    kind, pred, g = classify(J, F(1), F(1))
    log(f'J2 at a=b=1: {kind}, g={g}, predicted failing (p,q) {[(str(p), str(q)) for p, q in sorted(pred)]}')
    for p, q in sorted(pred):
        xi, eta = 2 * p, 2 * q
        S, T = (J.l + xi, J.h1 - 1), (J.m + eta, J.h1 + 1)
        log(f'   S={tuple(map(str, S))}, T={tuple(map(str, T))}: tracer monotone hits (|dx|<=16) {len(J.tracer(S, T, F(16)))}; '
            f'neighbour (xi+1/100) criterion {J.crit(F(1), F(1), xi + F(1, 100), eta)}')


# ------------------------------------------------------------------ 4. bank decomposition on named rooms
def part4():
    log('\n## 4. Greedy bank decomposition on named ledger realizations')
    d = json.load(open(os.path.join(D, 'd163-pattern-ledger', 'ledger.json')))
    rooms = {k: v['vertices'] for k, v in d['named_rooms'].items() if v['W'] <= 20}
    rooms['LLLRLLLRLLRR (ledger)'] = d['words']['LLLRLLLRLLRR']['realization']
    for name, V in rooms.items():
        P = clean(V); w = turn_word(P); h, v = dents(P, w)
        if h and v: continue
        ax = 1 if not h else 0  # sweep so that sections are intervals
        lev = sorted({p[ax] for p in P})
        runs = [sections(P, ax, (lev[i] + lev[i + 1]) / 2) for i in range(len(lev) - 1)]
        assert all(len(r) == 1 for r in runs)
        runs = [r[0] for r in runs]
        ov = all(max(runs[i][0], runs[i + 1][0]) < min(runs[i][1], runs[i + 1][1]) for i in range(len(runs) - 1))
        groups, cur = [], [runs[0]]
        for r in runs[1:]:
            if max(max(x[0] for x in cur), r[0]) < min(min(x[1] for x in cur), r[1]): cur.append(r)
            else: groups.append(cur); cur = [r]
        groups.append(cur)
        r_ = w.count('R')
        log(f'{name}: W={len(P)}, bands {len(runs)} (<= W/2-1={len(P)//2-1}), consecutive overlap {ov}, '
            f'groups {len(groups)} (<= ceil((r+1)/2)={-(-(r_ + 1) // 2)}), sizes {[len(g) for g in groups]}')


def egcd(x, y):
    if y == 0: return x, 1, 0
    g, s, t = egcd(y, x % y)
    return g, t, s - (x // y) * t


def witness(J, a, b, xi, eta):
    """Smallest |t'-s'| over developed images with crossing in the open mouth, by Bezout."""
    Dd, om, p, q, P1, P2 = J.params(a, b, xi, eta)
    g = fgcd(P1, P2); A, B = int(P1 / g), int(P2 / g)
    _, x, y = egcd(A, B)
    best = None
    for s1 in (1, -1):
        for s2 in (1, -1):
            r = om + s1 * p + s2 * q
            n0 = floor((J.I[0] - r) / g)
            for n in range(n0, n0 + int((J.I[1] - J.I[0]) / g) + 3):
                if not J.inI(r + n * g, False): continue
                k0, j0 = n * x, n * y  # k*A + j*B = n
                c = (J.m + s2 * eta) - (J.l + s1 * xi)
                slope = -2 * J.v * A - 2 * J.u * B  # Delta(t) = c + 2v(j0 - tA) - 2u(k0 + tB)
                c0 = c + 2 * J.v * j0 - 2 * J.u * k0
                t0 = floor(-c0 / slope)
                for t in (t0 - 1, t0, t0 + 1, t0 + 2):
                    dl = abs(c0 + slope * t)
                    if best is None or dl < best: best = dl
    return best


def part5():
    log('\n## 5. Supplement (run with --extra, appended): long witnesses and flush-endpoint probe')
    rng = random.Random(166)
    for J in joints():  # regenerate the same pairs as part 3
        pairs = marks(J, rng, 40 if J.lam < F(1, 20) else 60)
        dmax = F(8) if J.lam < F(1, 20) else F(12)
        for S, T in pairs:
            a, b = J.h1 - S[1], T[1] - J.h1
            xi, eta = S[0] - J.l, T[0] - J.m
            if J.crit(a, b, xi, eta, bool(J.flush)) and not J.crit_bounded(a, b, xi, eta, dmax, True):
                dw = witness(J, a, b, xi, eta)
                ok = []
                for sg in (1, -1):
                    st, end, con = trace(J.P, S, (S[0] + sg * dw, T[1]), maxrefl=10**4)
                    ok.append(st == 'end' and end == T and all(k == 'v' for _, k in con))
                log(f'{J.name}: S={tuple(map(str, S))} T={tuple(map(str, T))}: exact criterion lit, '
                    f'min witness |dx|={dw} > dmax={dmax}; physical trace of S.x+-|dx| reaches T monotonically: {ok}')
    probe = [Joint('J7 flush right (0,2)/(1,2)', 0, 2, 1, 1, 1, 1), Joint('J8 flush right (0,3)/(1,3)', 0, 3, 1, 2, 1, 1),
             joints()[4], joints()[3]]
    for J in probe:
        n = hit = 0
        for i in range(1, 8):
            for j in range(1, 8):
                a, b = J.h1 * F(i, 8), J.h2 * F(j, 8)
                for xi in [J.u * F(k, 48) for k in range(1, 48)]:
                    for eta in [J.v * F(k, 48) for k in range(1, 48)]:
                        n += 1
                        hit += (not J.crit(a, b, xi, eta)) and J.crit(a, b, xi, eta, True)
        log(f'{J.name}: {n} (level, mark) placements on a 1/8 x 1/48 grid; open criterion fails but a flush-endpoint '
            f'crossing exists: {hit}')
    log(f'supplement cpu {time.process_time() - T0:.1f}s')


if __name__ == '__main__':
    import sys
    if '--extra' in sys.argv:
        part5(); raise SystemExit
    s10 = part1()
    examples(s10)
    part2c()
    part4()
    part3()
    log(f'\ncpu {time.process_time() - T0:.1f}s')
