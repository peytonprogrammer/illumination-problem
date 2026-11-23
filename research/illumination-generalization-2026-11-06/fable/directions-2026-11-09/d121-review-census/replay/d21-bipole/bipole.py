"""Bi-pole families over Q(1,-1^5): enumerate covers, families, and decide LIT/DARK.

Usage: python3 -B bipole.py DEGREE [stage2_seconds]
Conventions: hurwitz.py (right action, mul(p,q) = p first).  A cover of the L-shaped
base L(A,B) = [0,A]x[0,1] u [0,1]x[0,B] is a 5-tuple (h_1..h_5), product 1, for the
poles p_1=(A,1), p_2=(A,0), p_3=(0,0), p_4=(0,B), p_5=(1,B) in boundary order.
"""
import sys, json, time, itertools, math
from array import array
from collections import deque
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'd6-hurwitz-census'))
import hurwitz as hz
mul, inv = hz.mul, hz.inv


def ptype(p):
    n2 = n3 = 0
    for c in hz.cycles(p):
        if len(c) == 2: n2 += 1
        elif len(c) == 3: n3 += 1
        elif len(c) > 3: return None
    return (n2, n3)


def classes(d):
    cls = {}
    for p in itertools.permutations(range(d)):
        ty = ptype(p)
        if ty is not None:
            cls.setdefault(ty, []).append(p)
    return cls


def canon(t, d):
    """Canonical encoding under simultaneous conjugation, and all relabellings achieving it."""
    k = len(t) - 1
    best, labs = None, []
    for r in range(d):
        lab = [-1] * d
        order = [r]
        lab[r] = 0
        for x in order:
            for g in t[:k]:
                y = g[x]
                if lab[y] < 0:
                    lab[y] = len(order)
                    order.append(y)
        if len(order) != d:
            return None, None
        e = tuple(lab[g[s]] for s in order for g in t[:k])
        if best is None or e < best:
            best, labs = e, [lab]
        elif e == best:
            labs.append(lab)
    return best, labs


def decode(enc, d, k=4):
    t = [tuple(enc[k * i + j] for i in range(d)) for j in range(k)]
    p = t[0]
    for g in t[1:]:
        p = mul(p, g)
    t.append(inv(p))
    return tuple(t)


def seed_tuples(d, cls, typeof, seq, cent_cache):
    """All tuples with type sequence seq and h1 = fixed representative, h2 up to the
    centralizer of h1 (weight = orbit size). Yields (tuple, weight); transitive only."""
    T1, T2, T3, T4, T5 = seq
    h1 = cls[T1][0]
    key = (T1, T2)
    if key not in cent_cache:
        if T1 not in cent_cache:
            cent_cache[T1] = [g for g in itertools.permutations(range(d)) if mul(g, h1) == mul(h1, g)]
        C = cent_cache[T1]
        seen, reps = set(), []
        for x in cls[T2]:
            if x in seen: continue
            orb = {hz.conj_by(x, g) for g in C}
            seen |= orb
            reps.append((x, len(orb)))
        cent_cache[key] = reps
    for h2, w in cent_cache[key]:
        p2 = mul(h1, h2)
        for h3 in cls[T3]:
            p3 = mul(p2, h3)
            for h4 in cls[T4]:
                p4 = mul(p3, h4)
                if typeof.get(p4) == T5:
                    t = (h1, h2, h3, h4, inv(p4))
                    if hz.is_transitive(t, d):
                        yield t, w


def type_multisets(d, tcap):
    cls_types = [(n2, n3) for n3 in range(d // 3 + 1) for n2 in range((d - 3 * n3) // 2 + 1)]
    for ms in itertools.combinations_with_replacement(sorted(cls_types), 5):
        if sum(a + 2 * b for a, b in ms) != 2 * d - 2: continue
        if sum(b for a, b in ms) > tcap: continue
        yield ms


class Census:
    def __init__(self, d, tcap):
        self.d, self.tcap = d, tcap
        self.cls = classes(d)
        self.typeof = {p: ty for ty, L in self.cls.items() for p in L}
        self.ids = {}
        self.tup, self.aut, self.pts, self.ptidx, self.trans = [], [], [], [], []

    def add(self, enc):
        i = self.ids.get(enc)
        if i is not None: return i, False
        i = len(self.tup)
        self.ids[enc] = i
        t = decode(enc, self.d)
        self.tup.append(t)
        pts, idx = [], bytearray([255]) * (5 * self.d)
        for pos in range(5):
            for c in hz.cycles(t[pos]):
                if len(c) == 2:
                    idx[pos * self.d + min(c)] = len(pts)
                    pts.append((pos, min(c), max(c)))
        self.pts.append(pts); self.ptidx.append(bytes(idx)); self.trans.append(None); self.aut.append(None)
        return i, True

    def close(self, t):
        """Add the full B_5 orbit of t (generators s_0..s_3)."""
        d = self.d
        enc, _ = canon(t, d)
        c, new = self.add(enc)
        if not new: return
        q = deque([c])
        while q:
            c = q.popleft()
            t = self.tup[c]
            _, labs = canon(t, d)
            self.aut[c] = labs
            tr = []
            for i in range(4):
                a, b = t[i], t[i + 1]
                k = inv(a)
                t2 = list(t)
                t2[i], t2[i + 1] = hz.conj_by(b, k), a      # s_i: (a,b) -> (a b a^-1, a)
                enc2, labs2 = canon(t2, d)
                c2, new = self.add(enc2)
                if new: q.append(c2)
                lab = labs2[0]
                pm = []
                for (pos, x, y) in self.pts[c]:
                    if pos == i: pos2 = i + 1
                    elif pos == i + 1: pos2, x, y = i, k[x], k[y]   # cycle map C -> k(C)
                    else: pos2 = pos
                    pm.append(self.ptidx[c2][pos2 * d + min(lab[x], lab[y])])
                assert 255 not in pm
                tr.append((c2, bytes(pm)))
            self.trans[c] = tr

    def cheap_lit(self, c, k):
        """Pairs (p over pos k, q over pos k+1) joined by a chain of lifts of the edge e_k
        through 2-cycle vertices only. Returns set of (p, q) point indices."""
        d = self.d
        ix = self.ptidx[c]
        par = {}
        def find(u):
            while par.setdefault(u, u) != u:
                par[u] = par[par[u]]; u = par[u]
            return u
        t = self.tup[c]
        cyc = []
        for pos in (k, k + 1):
            g = t[pos]
            m = [255] * d
            for j in range(d):
                if g[j] != j and g[g[j]] == j:
                    m[j] = ix[pos * d + min(j, g[j])]
            cyc.append(m)
        for j in range(d):
            p, q = cyc[0][j], cyc[1][j]
            if p != 255: find(p)
            if q != 255: find(q)
            if p != 255 and q != 255:
                par[find(p)] = find(q)
        out = set()
        P = sorted({x for x in cyc[0] if x != 255}); Q = sorted({x for x in cyc[1] if x != 255})
        for p in P:
            for q in Q:
                if find(p) == find(q): out.add((p, q))
        return out


# ------------------------------------------------------------ composition with L(A,B) -> pillowcase

def compose(A, B, h):
    """Pillowcase 4-tuple of X -> L(A,B) double -> pillowcase, plus point lookup.
    Returns (t, vert) with t = (t_a,t_b,t_c,t_d), corners a=(0,0), b=(1,0), c=(1,1), d=(0,1);
    vert(k, j) = (corner index, cycle index in cycles(t[corner])) of the point over pole p_(k+1)
    at the corner of the back face of copy j.  Asserts that these points are the cycles of h_k."""
    d = len(h[0])
    c = [hz.ident(d)]
    for k in range(4): c.append(mul(c[-1], h[k]))
    assert mul(c[4], h[4]) == hz.ident(d)
    ci = [inv(x) for x in c]
    cells = [(x, 0) for x in range(A)] + [(0, y) for y in range(1, B)]
    cs = set(cells)
    DV = {'L': (-1, 0), 'R': (1, 0), 'B': (0, -1), 'T': (0, 1)}

    def nb(f, dr):
        (x, y), s, m = f
        n = (x + DV[dr][0], y + DV[dr][1])
        if n in cs: return (n, s, m)
        k = None
        if dr == 'R' and (x, y) == (A - 1, 0): k = 1
        elif dr == 'B' and y == 0: k = 2
        elif dr == 'L' and x == 0: k = 3
        elif dr == 'T' and (x, y) == (0, B - 1): k = 4
        if k is None: return ((x, y), 1 - s, m)
        return ((x, y), 1, c[k][m]) if s == 0 else ((x, y), 0, ci[k][m])

    def cdir(pe, cell):                       # pillowcase edge -> direction in this cell
        x, y = cell
        if pe in 'LR': return pe if x % 2 == 0 else ('R' if pe == 'L' else 'L')
        return pe if y % 2 == 0 else ('T' if pe == 'B' else 'B')

    sheets = [(cl, s, m) for cl in cells for s in (0, 1) for m in range(d) if (s ^ ((cl[0] + cl[1]) & 1)) == 0]
    idx = {f: i for i, f in enumerate(sheets)}
    t = []
    for (e1, e2) in (('L', 'B'), ('B', 'R'), ('R', 'T'), ('T', 'L')):
        g = []
        for f in sheets:
            f1 = nb(f, cdir(e1, f[0]))
            f2 = nb(f1, cdir(e2, f1[0]))
            g.append(idx[f2])
        assert sorted(g) == list(range(len(sheets)))
        t.append(tuple(g))
    t = tuple(t)
    assert mul(mul(mul(t[0], t[1]), t[2]), t[3]) == hz.ident(len(sheets))
    poles = [((A, 1), (A - 1, 0), 'R'), ((A, 0), (A - 1, 0), 'R'), ((0, 0), (0, 0), 'L'),
             ((0, B), (0, B - 1), 'L'), ((1, B), (0, B - 1), 'T')]
    cidx = [hz.cycle_index(g) for g in t]
    table = {}
    for k, (p, cell, dr) in enumerate(poles):
        v = {(0, 0): 0, (1, 0): 1, (1, 1): 2, (0, 1): 3}[(p[0] % 2, p[1] % 2)]
        grp = {}
        for j in range(d):
            f = (cell, 1, j)
            if f not in idx: f = nb(f, dr)
            cy = cidx[v][0][idx[f]]
            table[(k, j)] = (v, cy)
            grp.setdefault(cy, set()).add(j)
        hc = {frozenset(cc) for cc in hz.cycles(h[k])}
        assert {frozenset(s) for s in grp.values()} == hc, (k, grp, hc)
        for cy, s in grp.items():
            assert cidx[v][1][cy] == len(s)
    return t, (lambda k, j: table[(k, j)])


def pillow_lit(A, B, h, pairs, max_states=None):
    """pairs: list of ((k, j), (k2, j2)) = points by (pole position, a sheet of the cycle), both
    poles over the same pillowcase corner. Returns (dict pair -> 'LIT'/'DARK'/'CAP', max states)."""
    t, vert = compose(A, B, h)
    v = vert(*pairs[0][0])[0]
    tt = t[v:] + t[:v]
    want = {}
    for pr in pairs:
        (v1, c1), (v2, c2) = vert(*pr[0]), vert(*pr[1])
        assert v1 == v and v2 == v and c1 != c2
        want[pr] = frozenset((c1, c2))
    res, states = {}, 0
    rem = set(want.values())
    while rem:
        r = hz.marked_orbit(tt, targets=rem, max_states=max_states)
        states = max(states, r['states'])
        rem -= r['lit']
        if r.get('stopped_lit'): continue
        verdict = 'DARK' if r['complete'] else 'CAP'
        for pr, fs in want.items():
            if fs in rem: res[pr] = verdict
        break
    for pr, fs in want.items():
        res.setdefault(pr, 'LIT')
    return res, states


# ------------------------------------------------------------ main

def run(d, stage2_seconds=0):
    T0 = time.time()
    tcap = 8 - d if d >= 5 else 99
    cen = Census(d, tcap)
    cache = {}
    mass, nseeds = {}, 0
    mss = list(type_multisets(d, tcap))
    for ms in mss:
        o = sorted(ms, key=lambda ty: -len(cen.cls[ty]))
        seqs = [(o[0], o[2], o[3], o[4], o[1])]
        if d <= 5: seqs = sorted(set(itertools.permutations(ms)))
        for seq in seqs:
            w = 0
            for t, wt in seed_tuples(d, cen.cls, cen.typeof, seq, cache):
                w += wt; nseeds += 1
                cen.close(t)
            mass[seq] = w * len(cen.cls[seq[0]])
    N = len(cen.tup)
    # mass check: sum over covers with a given type sequence of d!/|Aut| = raw tuple count
    got = {}
    for c in range(N):
        seq = tuple(cen.typeof[g] for g in cen.tup[c])
        got[seq] = got.get(seq, 0) + math.factorial(d) // len(cen.aut[c])
    mass_ok = all(got.get(seq, 0) == m for seq, m in mass.items())
    seqs_all = len(got)
    t_enum = time.time() - T0
    # unordered-branch-point orbits (B_5 orbits of covers)
    par = list(range(N))
    def findc(u):
        while par[u] != u:
            par[u] = par[par[u]]; u = par[u]
        return u
    for c in range(N):
        for c2, _ in cen.trans[c]:
            a, b = findc(c), findc(c2)
            if a != b: par[a] = b
    orbit_sizes = {}
    for c in range(N): orbit_sizes[findc(c)] = orbit_sizes.get(findc(c), 0) + 1
    # nodes = (cover, p, q), p < q point indices at different poles
    off, tot = [], 0
    for c in range(N):
        off.append(tot); n = len(cen.pts[c]); tot += n * n
    up = array('i', range(tot))
    def find(u):
        r = u
        while up[r] != r: r = up[r]
        while up[u] != r: up[u], u = r, up[u]
        return r
    npairs = 0
    lit = bytearray(tot)
    for c in range(N):
        pts = cen.pts[c]; n = len(pts); o = off[c]
        maps = [(off[c2], len(cen.pts[c2]), pm) for c2, pm in cen.trans[c]]
        d_ = d
        for lab in cen.aut[c][1:]:
            pm = bytes(cen.ptidx[c][pos * d_ + min(lab[x], lab[y])] for (pos, x, y) in pts)
            maps.append((o, n, pm))
        for p in range(n):
            for q in range(p + 1, n):
                if pts[p][0] == pts[q][0]: continue
                npairs += 1
                u = find(o + p * n + q)
                for o2, n2, pm in maps:
                    p2, q2 = pm[p], pm[q]
                    if p2 > q2: p2, q2 = q2, p2
                    v = find(o2 + p2 * n2 + q2)
                    if u != v: up[v] = u
        for k in range(4):
            for (p, q) in cen.cheap_lit(c, k):
                lit[o + p * n + q] = 1
    fam = {}
    for c in range(N):
        pts = cen.pts[c]; n = len(pts); o = off[c]
        for p in range(n):
            for q in range(p + 1, n):
                if pts[p][0] == pts[q][0]: continue
                u = o + p * n + q
                r = find(u)
                e = fam.setdefault(r, [0, 0, None, None])     # size, lit count, witness at k=2, any member
                e[0] += 1
                if lit[u]:
                    e[1] += 1
                    if e[2] is None and pts[p][0] == 2 and pts[q][0] == 3: e[2] = (c, p, q)
                if e[3] is None and pts[p][0] == 2 and pts[q][0] == 3: e[3] = (c, p, q)
    dark = [(r, e) for r, e in fam.items() if e[1] == 0]
    out = dict(degree=d, tcap=tcap, type_multisets=len(mss), type_sequences=seqs_all, covers=N,
               covers_with_bipole_pair=sum(1 for c in range(N) if len({p[0] for p in cen.pts[c]}) > 1),
               cover_orbits_B5=len(orbit_sizes), max_cover_orbit=max(orbit_sizes.values()) if orbit_sizes else 0,
               mass_check=mass_ok, seeds=nseeds, bipole_nodes=npairs, nodes_lit_by_edge=sum(lit),
               families=len(fam), families_with_edge_lit_member=len(fam) - len(dark),
               families_dark_candidates=len(dark), family_sizes_minmax=[min(e[0] for e in fam.values()), max(e[0] for e in fam.values())] if fam else None,
               seconds_enum=round(t_enum, 1), seconds_families=round(time.time() - T0, 1))
    out['dark_candidates'] = [dict(size=e[0], member=(cen.tup[e[3][0]], cen.pts[e[3][0]][e[3][1]], cen.pts[e[3][0]][e[3][2]]) if e[3] else None)
                              for r, e in dark[:5000]]
    # stage 1b: one witness per family through the pillowcase decider on three bases
    bases = [(2, 2), (3, 2), (3, 4)]
    wit = {str(b): dict(LIT=0, other=0, max_states=0) for b in bases}
    nowit = 0
    for r, e in fam.items():
        if e[1] == 0: continue
        if e[2] is None: nowit += 1; continue
        c, p, q = e[2]
        pr = ((2, cen.pts[c][p][1]), (3, cen.pts[c][q][1]))
        for b in bases:
            res, st = pillow_lit(b[0], b[1], cen.tup[c], [pr])
            w = wit[str(b)]
            w['LIT' if res[pr] == 'LIT' else 'other'] += 1
            w['max_states'] = max(w['max_states'], st)
    out['family_witness_pillowcase'] = wit
    out['lit_families_without_k2_witness'] = nowit
    out['seconds_witness'] = round(time.time() - T0, 1)
    print(json.dumps({k: v for k, v in out.items() if k != 'dark_candidates'}), flush=True)
    # stage 2 (tracking-free): EVERY cover of the tromino double, every pair over poles p_3, p_4
    if stage2_seconds:
        T1 = time.time()
        s2 = dict(covers_done=0, nodes=0, edge_lit=0, pillow_lit=0, dark=0, cap=0, max_states=0, complete=True, dark_list=[])
        for c in range(N):
            if time.time() - T1 > stage2_seconds:
                s2['complete'] = False; break
            pts = cen.pts[c]
            P = [i for i, p in enumerate(pts) if p[0] == 2]; Q = [i for i, p in enumerate(pts) if p[0] == 3]
            s2['covers_done'] += 1
            if not P or not Q: continue
            cl = cen.cheap_lit(c, 2)
            todo = [((2, pts[p][1]), (3, pts[q][1])) for p in P for q in Q if (p, q) not in cl]
            s2['nodes'] += len(P) * len(Q); s2['edge_lit'] += len(P) * len(Q) - len(todo)
            if todo:
                res, st = pillow_lit(2, 2, cen.tup[c], todo, max_states=200000)
                s2['max_states'] = max(s2['max_states'], st)
                for pr, v in res.items():
                    if v == 'LIT': s2['pillow_lit'] += 1
                    elif v == 'DARK':
                        s2['dark'] += 1
                        if len(s2['dark_list']) < 5000: s2['dark_list'].append((cen.tup[c], pr))
                    else: s2['cap'] += 1
        # nodes dark on the tromino: same tuple on other L(A,B) (same family: the boundary-path basis deforms continuously)
        s2['dark_nodes_other_bases'] = {}
        still = list(s2['dark_list'])
        for b in ((3, 2), (3, 4), (5, 2)):
            nxt = []
            for (tp, pr) in still:
                res, st = pillow_lit(b[0], b[1], tp, [pr], max_states=200000)
                if res[pr] != 'LIT': nxt.append((tp, pr))
            s2['dark_nodes_other_bases'][str(b)] = dict(tested=len(still), not_lit=len(nxt))
            still = nxt
        s2['dark_on_all_bases'] = still
        s2['seconds'] = round(time.time() - T1, 1)
        out['stage2_tromino_all_covers_poles_p3_p4'] = s2
        print(json.dumps({k: v for k, v in s2.items() if k != 'dark_list'}, default=list), flush=True)
    with open(HERE / f'result_d{d}.json', 'w') as f:
        json.dump(out, f, indent=1, default=list)
    return out


if __name__ == '__main__':
    run(int(sys.argv[1]), float(sys.argv[2]) if len(sys.argv) > 2 else 0)
