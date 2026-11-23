"""d22: pair structures P1, P2, P3 on covers of Q(1^z, -1^{z+4}), delta * z <= 8.

Usage: python3 -B d22.py z1 DEGREE | small | rooms | d21
Conventions follow d21 bipole.py: poles in CLOCKWISE boundary order, h_k = monodromy at
pole k in back-face sheet labels, wall after pole k glued by c_k = h_1 ... h_k.
LIT verdicts come from an exact ray tracer on the square complex (a concrete segment).
DARK verdicts come from hurwitz.marked_orbit with a complete orbit.
"""
import sys, json, time, itertools, math
from array import array
from fractions import Fraction
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'd6-hurwitz-census'))
sys.path.insert(0, str(HERE.parent / 'd21-bipole'))
import hurwitz as hz
import bipole as bp
mul, inv = hz.mul, hz.inv
DV = {'L': (-1, 0), 'R': (1, 0), 'B': (0, -1), 'T': (0, 1)}


def dirs(M):
    out = []
    for p in range(M + 1):
        for q in range(M + 1 - p):
            if p + q == 0 or math.gcd(p, q) != 1: continue
            ev = sorted([(Fraction(i, p), 'R') for i in range(1, p)] + [(Fraction(j, q), 'T') for j in range(1, q)])
            out.append((p, q, [e for _, e in ev]))
    return out
DIRS = {}


class Room:
    """Strictly simple polyomino. poles = convex corners in clockwise order from `start`."""
    def __init__(s, cells, start=None):
        s.cells = sorted(cells); cs = set(cells)
        E = {}
        for (x, y) in cs:
            for dr, a, dv in (('B', (x, y), (1, 0)), ('R', (x + 1, y), (0, 1)), ('T', (x + 1, y + 1), (-1, 0)), ('L', (x, y + 1), (0, -1))):
                if (x + DV[dr][0], y + DV[dr][1]) not in cs:
                    assert a not in E, 'not strictly simple'
                    E[a] = ((x, y), dr, dv)
        v0 = v = min(E); seq = []
        while True:
            c, dr, dv = E[v]; seq.append((v, c, dr, dv)); v = (v[0] + dv[0], v[1] + dv[1])
            if v == v0: break
        assert len(seq) == len(E), 'boundary not connected'
        n = len(seq)
        turn = [seq[i - 1][3][0] * seq[i][3][1] - seq[i - 1][3][1] * seq[i][3][0] for i in range(n)]
        conv = [i for i in range(n) if turn[i] == 1]
        i0 = conv[0] if start is None else next(i for i in conv if seq[i][0] == start)
        s.poles, s.zeros, s.wall = [seq[i0][0]], [], {}
        for j in range(1, n + 1):                 # clockwise: edge i-1 comes after vertex i
            i = (i0 - j) % n
            s.wall[(seq[i][1], seq[i][2])] = len(s.poles)
            if j < n:
                if turn[i] == 1: s.poles.append(seq[i][0])
                elif turn[i] == -1: s.zeros.append(seq[i][0])
        s.n, s.z = len(s.poles), len(s.zeros)
        assert s.n == s.z + 4


class Cx:
    """Square complex of the degree-d cover of the double of `room` with pole tuple h."""
    def __init__(s, room, h):
        d = len(h[0]); s.d, s.room = d, room
        assert len(h) == room.n
        c = [hz.ident(d)]
        for g in h: c.append(mul(c[-1], g))
        assert c[-1] == hz.ident(d)
        c[-1] = c[0]; ci = [inv(x) for x in c]
        cs = set(room.cells); nb = {}
        for cl in room.cells:
            for dr, (dx, dy) in DV.items():
                n = (cl[0] + dx, cl[1] + dy)
                k = None if n in cs else room.wall[(cl, dr)]
                for m in range(d):
                    if k is None: nb[(cl, 0, m, dr)] = (n, 0, m); nb[(cl, 1, m, dr)] = (n, 1, m)
                    else: nb[(cl, 0, m, dr)] = (cl, 1, c[k][m]); nb[(cl, 1, m, dr)] = (cl, 0, ci[k][m])
        s.nb = nb
        par = {}
        def find(u):
            while par.setdefault(u, u) != u:
                par[u] = par[par[u]]; u = par[u]
            return u
        s.find = find
        EP = {'L': ((0, 0), (0, 1)), 'R': ((1, 0), (1, 1)), 'B': ((0, 0), (1, 0)), 'T': ((0, 1), (1, 1))}
        for (cl, sd, m, dr), g in nb.items():
            for ex, ey in EP[dr]:
                pt = (cl[0] + ex, cl[1] + ey)
                par[find(((cl, sd, m), pt))] = find((g, pt))
        s.members = {}
        for u in list(par): s.members.setdefault(find(u), []).append(u)
        s.cellat = {}
        for cl in room.cells:
            for ex in (0, 1):
                for ey in (0, 1): s.cellat.setdefault((cl[0] + ex, cl[1] + ey), cl)

    def vpt(s, y, j):
        """Vertex over lattice point y through back-face sheet j."""
        return s.find(((s.cellat[y], 1, j), y))

    def vpole(s, k, j):
        return s.vpt(s.room.poles[k], j)

    def step(s, f, fx, fy, dr):
        if dr == 'R':
            g = s.nb[f + ('L' if fx else 'R',)]
            if g[0] == f[0]: fx ^= 1
        else:
            g = s.nb[f + ('B' if fy else 'T',)]
            if g[0] == f[0]: fy ^= 1
        return g, fx, fy

    def visible(s, vs, M):
        """Vertices hit by a straight segment from vs of direction (p,q), p+q <= M, through regular points."""
        if M not in DIRS: DIRS[M] = dirs(M)
        out = set(); mem = s.members
        for (f0, pt) in mem[vs]:
            for (p, q, ev) in DIRS[M]:
                f, fx, fy = f0, pt[0] - f0[0][0], pt[1] - f0[0][1]
                seen = set()
                while (f, fx, fy) not in seen:
                    seen.add((f, fx, fy))
                    for dr in ev: f, fx, fy = s.step(f, fx, fy, dr)
                    v = s.find((f, (f[0][0] + ((1 if p else 0) ^ fx), f[0][1] + ((1 if q else 0) ^ fy))))
                    out.add(v)
                    if len(mem[v]) != 4: break
                    if p: f, fx, fy = s.step(f, fx, fy, 'R')
                    if q: f, fx, fy = s.step(f, fx, fy, 'T')
        return out

    def pillow(s):
        cells, d = s.room.cells, s.d
        def cdir(pe, cell):
            x, y = cell
            if pe in 'LR': return pe if x % 2 == 0 else ('R' if pe == 'L' else 'L')
            return pe if y % 2 == 0 else ('T' if pe == 'B' else 'B')
        sheets = [(cl, sd, m) for cl in cells for sd in (0, 1) for m in range(d) if (sd ^ ((cl[0] + cl[1]) & 1)) == 0]
        idx = {f: i for i, f in enumerate(sheets)}
        t = []
        for (e1, e2) in (('L', 'B'), ('B', 'R'), ('R', 'T'), ('T', 'L')):
            g = []
            for f in sheets:
                f1 = s.nb[f + (cdir(e1, f[0]),)]
                g.append(idx[s.nb[f1 + (cdir(e2, f1[0]),)]])
            t.append(tuple(g))
        t = tuple(t)
        assert mul(mul(mul(t[0], t[1]), t[2]), t[3]) == hz.ident(len(sheets))
        return t, idx, [hz.cycle_index(g) for g in t]

    def complete(s, vs, vt, max_states=2000000):
        """Complete decider (marked_orbit). vs, vt regular vertices over the same pillowcase corner."""
        t, idx, cidx = s.pillow()
        def cyc(v):
            pt = s.members[v][0][1]
            cn = {(0, 0): 0, (1, 0): 1, (1, 1): 2, (0, 1): 3}[(pt[0] % 2, pt[1] % 2)]
            ids = {cidx[cn][0][idx[f]] for (f, _) in s.members[v] if f in idx}
            assert len(ids) == 1
            cy = ids.pop()
            assert cidx[cn][1][cy] * 2 == len(s.members[v]) == 4
            return cn, cy
        (v1, c1), (v2, c2) = cyc(vs), cyc(vt)
        assert v1 == v2 and c1 != c2
        r = hz.marked_orbit(t[v1:] + t[:v1], targets={frozenset((c1, c2))}, max_states=max_states)
        return ('LIT' if r.get('stopped_lit') else 'DARK' if r['complete'] else 'CAP'), r['states']


def scale2(cells):
    return [(2 * x + a, 2 * y + b) for (x, y) in cells for a in (0, 1) for b in (0, 1)]


def L(A, B):
    return Room([(x, 0) for x in range(A)] + [(0, y) for y in range(1, B)], start=(A, 1))


def two_cycles(h):
    """[(pole, a, b)] for every 2-cycle, bipole pts convention."""
    return [(k, c[0], c[1]) for k, g in enumerate(h) for c in hz.cycles(g) if len(c) == 2]


def nodes_of(h, d):
    pts = two_cycles(h)
    P1 = [(p, q) for p, q in itertools.combinations(pts, 2) if p[0] == q[0]]
    P2 = [(p, q) for p, q in itertools.combinations(pts, 2) if p[0] != q[0]]
    return P1, P2, list(itertools.combinations(range(d), 2))


def verdict(room, h, kind, node, y, M):
    """True iff the tracer finds a segment (p+q <= M)."""
    X = Cx(room, h)
    if kind == 'P3': a, b = X.vpt(y, node[0]), X.vpt(y, node[1])
    else: a, b = X.vpole(node[0][0], node[0][1]), X.vpole(node[1][0], node[1][1])
    assert a != b and len(X.members[a]) == 4 and len(X.members[b]) == 4
    return b in X.visible(a, M)


def full_verdict(cells, start, h, kind, node, y, cap=400000):
    """Complete decider; rescales by 2 only if the two points sit over different pillowcase corners."""
    for sc in (1, 2):
        R = Room(cells if sc == 1 else scale2(cells), start=(sc * start[0], sc * start[1]))
        X = Cx(R, h)
        if kind == 'P3': a, b = X.vpt((sc * y[0], sc * y[1]), node[0]), X.vpt((sc * y[0], sc * y[1]), node[1])
        else: a, b = X.vpole(node[0][0], node[0][1]), X.vpole(node[1][0], node[1][1])
        pa, pb = X.members[a][0][1], X.members[b][0][1]
        if (pa[0] - pb[0]) % 2 == 0 and (pa[1] - pb[1]) % 2 == 0: return X.complete(a, b, cap)


# ------------------------------------------------------------ z >= 2: brute force, every node

def brute(n, d, tcap):
    els = [p for p in itertools.permutations(range(d)) if bp.ptype(p) is not None and bp.ptype(p)[1] <= tcap]
    out = {}
    for t in itertools.product(els, repeat=n - 1):
        pr = t[0]
        for g in t[1:]: pr = mul(pr, g)
        full = t + (inv(pr),)
        tys = [bp.ptype(g) for g in full]
        if tys[-1] is None or sum(a + 2 * b for a, b in tys) != 2 * d - 2 or sum(b for a, b in tys) > tcap: continue
        if not hz.is_transitive(full, d): continue
        enc, labs = bp.canon(full, d)
        out.setdefault(enc, full)
    return out


def braid_orbits(covers, d):
    ids = {e: i for i, e in enumerate(covers)}
    par = list(range(len(ids)))
    def find(u):
        while par[u] != u:
            par[u] = par[par[u]]; u = par[u]
        return u
    for e, t in covers.items():
        for i in range(len(t) - 1):
            t2 = list(t); t2[i], t2[i + 1] = hz.conj_by(t[i + 1], inv(t[i])), t[i]
            par[find(ids[e])] = find(ids[bp.canon(t2, d)[0]])
    return len({find(i) for i in range(len(ids))})


SMALL = {  # z: list of (cells, y) ; y = a regular lattice point of the double
    2: [([(0, 0), (1, 0), (2, 0), (1, 1)], (1, 0)), ([(0, 0), (1, 0), (1, 1), (2, 1)], (1, 0)),
        ([(0, 0), (1, 0), (2, 0), (0, 1), (2, 1), (0, 2)], (1, 0))],
    3: [([(0, 0), (1, 0), (2, 0), (3, 0), (0, 1), (2, 1)], (1, 0)), ([(0, 0), (1, 0), (1, 1), (2, 1), (1, 2)], (1, 0)),
        ([(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (0, 1), (0, 2), (3, 1)], (1, 0))],
    4: [([(1, 0), (0, 1), (1, 1), (2, 1), (3, 1), (1, 2)], (3, 1)), ([(0, 0), (1, 0), (1, 1), (2, 1), (2, 2), (3, 2)], (1, 0)),
        ([(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (0, 1), (2, 1), (4, 1)], (1, 0))],
}


def small():
    res = []
    for z, d in ((2, 2), (2, 3), (2, 4), (3, 2), (4, 2)):
        T0 = time.time()
        rooms = [(Room(c), y) for c, y in SMALL[z]]
        for R, y in rooms: assert R.z == z, (z, R.z, R.cells)
        covers = brute(z + 4, d, 8 - d * z)
        row = dict(z=z, delta=d, covers=len(covers), braid_orbits=braid_orbits(covers, d))
        for kind in ('P1', 'P2', 'P3'): row[kind] = dict(nodes=0, lit_base0=0, lit_other_base=0, survivors=[])
        for h in covers.values():
            P1, P2, P3 = nodes_of(h, d)
            for kind, nodes in (('P1', P1), ('P2', P2), ('P3', P3)):
                if not nodes: continue
                e = row[kind]; R, y = rooms[0]
                X = Cx(R, h); vis = {}
                for nd in nodes:
                    e['nodes'] += 1
                    if kind == 'P3': a, b = X.vpt(y, nd[0]), X.vpt(y, nd[1])
                    else: a, b = X.vpole(nd[0][0], nd[0][1]), X.vpole(nd[1][0], nd[1][1])
                    assert a != b and len(X.members[a]) == 4 == len(X.members[b])
                    if a not in vis: vis[a] = X.visible(a, 8)
                    if b in vis[a]: e['lit_base0'] += 1; continue
                    if any(verdict(R2, h, kind, nd, y2, 12) for R2, y2 in rooms): e['lit_other_base'] += 1; continue
                    fv = [full_verdict(c, Room(c).poles[0], h, kind, nd, y2) for c, y2 in SMALL[z]]
                    e['survivors'].append(dict(h=h, node=nd, complete=fv))
        row['seconds'] = round(time.time() - T0, 1)
        print(json.dumps(row, default=list), flush=True)
        res.append(row)
    json.dump(res, open(HERE / 'result_small.json', 'w'), indent=1, default=list)


# ------------------------------------------------------------ z = 1: d21 census + family tracking

def z1(d):
    T0 = time.time()
    tcap = 8 - d
    cen = bp.Census(d, tcap); cache = {}
    for ms in bp.type_multisets(d, tcap):
        o = sorted(ms, key=lambda ty: -len(cen.cls[ty]))
        seqs = [(o[0], o[2], o[3], o[4], o[1])]
        if d <= 5: seqs = sorted(set(itertools.permutations(ms)))
        for seq in seqs:
            for t, wt in bp.seed_tuples(d, cen.cls, cen.typeof, seq, cache): cen.close(t)
    N = len(cen.tup)
    out = dict(z=1, delta=d, covers=N, seconds_enum=round(time.time() - T0, 1))
    # moves: (target cover, sheet map, 2-cycle point map)
    def ptmap(c, c2, lab):
        return bytes(cen.ptidx[c2][pos * d + min(lab[x], lab[y])] for (pos, x, y) in cen.pts[c])
    braid, local = [], []
    for c in range(N):
        t = cen.tup[c]; mv = []
        for i in range(4):
            t2 = list(t); t2[i], t2[i + 1] = hz.conj_by(t[i + 1], inv(t[i])), t[i]
            enc2, labs2 = bp.canon(t2, d)
            c2, pm = cen.trans[c][i]
            assert cen.ids[enc2] == c2
            mv.append((c2, labs2[0], pm))
        braid.append(mv)
        local.append([(lab, ptmap(c, c, lab)) for lab in cen.aut[c][1:]])
    R0, y0 = L(2, 2), (1, 0)
    for kind in ('P1', 'P3'):
        if kind == 'P1':
            W = max(len(p) for p in cen.pts)
            def nodes(c):
                pts = cen.pts[c]
                return [(p, q) for p in range(len(pts)) for q in range(p + 1, len(pts)) if pts[p][0] == pts[q][0]]
            def nbrs(c, p, q):
                for c2, lab, pm in braid[c]: yield c2, pm[p], pm[q]
                for lab, pm in local[c]: yield c, pm[p], pm[q]
        else:
            W = d
            def nodes(c): return list(itertools.combinations(range(d), 2))
            def nbrs(c, p, q):
                for c2, lab, pm in braid[c]: yield c2, lab[p], lab[q]
                for lab, pm in local[c]: yield c, lab[p], lab[q]
                for g in cen.tup[c]: yield c, g[p], g[q]
        fam = array('i', [-1]) * (N * W * W)
        nf = 0; total = 0; sizes = []
        for c in range(N):
            for (p, q) in nodes(c):
                total += 1
                u = (c * W + p) * W + q
                if fam[u] >= 0: continue
                fam[u] = nf; st = [(c, p, q)]; sz = 0
                while st:
                    a, x, y = st.pop(); sz += 1
                    for a2, x2, y2 in nbrs(a, x, y):
                        if x2 > y2: x2, y2 = y2, x2
                        u2 = (a2 * W + x2) * W + y2
                        if fam[u2] < 0: fam[u2] = nf; st.append((a2, x2, y2))
                sizes.append(sz); nf += 1
        assert sum(sizes) == total
        lit = [False] * nf; tested = [0] * nf; sample = [[] for _ in range(nf)]; nl = 0
        for c in range(N):
            if nl == nf: break
            todo = [(p, q) for (p, q) in nodes(c) if not lit[fam[(c * W + p) * W + q]] and tested[fam[(c * W + p) * W + q]] < 60]
            if not todo: continue
            X = Cx(R0, cen.tup[c]); vis = {}
            for (p, q) in todo:
                f = fam[(c * W + p) * W + q]
                if lit[f]: continue
                if kind == 'P1': a, b = X.vpole(cen.pts[c][p][0], cen.pts[c][p][1]), X.vpole(cen.pts[c][q][0], cen.pts[c][q][1])
                else: a, b = X.vpt(y0, p), X.vpt(y0, q)
                assert a != b and len(X.members[a]) == 4 == len(X.members[b])
                if a not in vis: vis[a] = X.visible(a, 8)
                tested[f] += 1
                if b in vis[a]: lit[f] = True; nl += 1
                elif len(sample[f]) < 3: sample[f].append((c, p, q))
        cands = []
        for f in range(nf):
            if lit[f]: continue
            info = dict(family=f, size=sizes[f], tested_on_L22=tested[f], members=[])
            for (c, p, q) in sample[f]:
                h = cen.tup[c]
                nd = (cen.pts[c][p], cen.pts[c][q]) if kind == 'P1' else (p, q)
                v = {}
                for (A, B, y) in ((2, 2, (1, 0)), (3, 2, (1, 0)), (3, 2, (2, 0)), (3, 4, (0, 1)), (2, 3, (0, 2))):
                    key = f'L({A},{B}) y={y}'
                    if verdict(L(A, B), h, kind, nd, y, 14): v[key] = 'LIT(tracer)'; break
                    v[key] = full_verdict(L(A, B).cells, (A, 1), h, kind, nd, y, 150000)
                    if v[key][0] == 'LIT': break
                info['members'].append(dict(h=h, node=nd, verdicts=v))
            info['status'] = 'LIT' if any('LIT' in str(x) for m in info['members'] for x in m['verdicts'].values()) else 'DARK-CANDIDATE'
            cands.append(info)
        out[kind] = dict(nodes=total, families=nf, families_lit_by_tracer_on_L22=nl, unlit=cands,
                         dark_families=sum(1 for x in cands if x['status'] != 'LIT'))
        out[kind + '_seconds'] = round(time.time() - T0, 1)
        print(kind, json.dumps({k: v for k, v in out[kind].items() if k != 'unlit'}), flush=True)
    json.dump(out, open(HERE / f'result_z1_d{d}.json', 'w'), indent=1, default=list)
    print(json.dumps({k: v for k, v in out.items() if k not in ('P1', 'P3')}), flush=True)


# ------------------------------------------------------------ checks

def d21_check():
    idn = tuple(range(5))
    h = (idn, idn, (1, 0, 3, 4, 2), (1, 2, 0, 4, 3), (4, 1, 0, 3, 2))
    nd = ((2, 0, 1), (3, 3, 4))
    out = {}
    for (A, B) in ((2, 2), (3, 2), (2, 4)):
        out[f'L({A},{B})'] = dict(tracer_M20=verdict(L(A, B), h, 'P2', nd, None, 20),
                                  complete=full_verdict(L(A, B).cells, (A, 1), h, 'P2', nd, None, 400000))
    # regression on lit nodes: every bipole pair of a few degree-4 covers, tracer vs complete decider
    cen = bp.Census(4, 99); cache = {}; agree = dis = 0
    for ms in bp.type_multisets(4, 99):
        for seq in sorted(set(itertools.permutations(ms))):
            for t, wt in bp.seed_tuples(4, cen.cls, cen.typeof, seq, cache): cen.close(t)
    for c in range(0, len(cen.tup), 7):
        h4 = cen.tup[c]
        for kind, nodes in zip(('P1', 'P2', 'P3'), nodes_of(h4, 4)):
            for n4 in nodes[:3]:
                a = verdict(L(2, 2), h4, kind, n4, (1, 0), 16)
                b = full_verdict(L(2, 2).cells, (2, 1), h4, kind, n4, (1, 0))[0]
                if (b == 'LIT') == a: agree += 1
                else: dis += 1
    out['tracer_vs_complete_degree4'] = dict(agree=agree, disagree=dis)
    print(json.dumps(out), flush=True)
    json.dump(out, open(HERE / 'result_d21_check.json', 'w'), indent=1)


def rooms():
    """Coordinator deduction on two rooms tiled by reflected copies of L(2,2)."""
    base = [(0, 0), (1, 0), (0, 1)]
    bpoles = [(2, 1), (2, 0), (0, 0), (0, 2), (1, 2)]
    out = {}
    for name, sx, sy in (('two tiles (mirror in y=0)', (1,), (1, -1)), ('four tiles (mirrors in x=0, y=0)', (1, -1), (1, -1))):
        cells = sorted({((x if a > 0 else -1 - x) + 2, (y if b > 0 else -1 - y) + 2) for (x, y) in base for a in sx for b in sy})
        R = Room(cells); X = Cx(R, (hz.ident(1),) * R.n)
        rep = {}
        for v, mem in X.members.items():
            pt = mem[0][1]; fold = (abs(pt[0] - 2), abs(pt[1] - 2))
            if fold not in bpoles: continue
            sides = {f[1] for f, _ in mem}
            rep.setdefault(str(fold), []).append(dict(point=pt, cycle_length=len(mem) // 2,
                                                       fixed_by_reflection=len(sides) == 2, interior=pt not in R.poles and all(
                                                           (pt[0] - a, pt[1] - b) in set(cells) for a in (0, 1) for b in (0, 1))))
        out[name] = dict(cells=cells, walls=2 * R.z + 4, degree=len(cells) // 3, over_base_pole=rep)
    print(json.dumps(out, indent=1), flush=True)
    json.dump(out, open(HERE / 'result_rooms.json', 'w'), indent=1)


def exh(d, kinds=('P1', 'P3'), tmax=1e9):
    """Tracking-free control for z = 1: every cover, every P1 and P3 node, no family grouping."""
    T0 = time.time()
    cen = bp.Census(d, 8 - d); cache = {}
    for ms in bp.type_multisets(d, 8 - d):
        o = sorted(ms, key=lambda ty: -len(cen.cls[ty]))
        for seq in (sorted(set(itertools.permutations(ms))) if d <= 5 else [(o[0], o[2], o[3], o[4], o[1])]):
            for t, wt in bp.seed_tuples(d, cen.cls, cen.typeof, seq, cache): cen.close(t)
    others = ((3, 2, (1, 0)), (3, 2, (2, 0)), (2, 3, (0, 2)), (2, 2, (1, 0)))
    out = {}
    for kind in kinds:
        e = out[kind] = dict(covers_done=0, covers=len(cen.tup), nodes=0, lit_L22_M8=0, lit_other_tracer_M20=0, lit_complete=0, dark=[], cap=0)
        for h in cen.tup:
            if time.time() - T0 > tmax: break
            e['covers_done'] += 1
            nodes = nodes_of(h, d)[0 if kind == 'P1' else 2]
            if not nodes: continue
            X = Cx(L(2, 2), h); vis = {}
            for nd in nodes:
                e['nodes'] += 1
                if kind == 'P3': a, b = X.vpt((1, 0), nd[0]), X.vpt((1, 0), nd[1])
                else: a, b = X.vpole(nd[0][0], nd[0][1]), X.vpole(nd[1][0], nd[1][1])
                if a not in vis: vis[a] = X.visible(a, 8)
                if b in vis[a]: e['lit_L22_M8'] += 1; continue
                if any(verdict(L(A, B), h, kind, nd, y, 20) for A, B, y in others): e['lit_other_tracer_M20'] += 1; continue
                fv = [full_verdict(L(A, B).cells, (A, 1), h, kind, nd, y, 150000)[0] for A, B, y in others]
                if 'LIT' in fv: e['lit_complete'] += 1
                elif 'CAP' in fv: e['cap'] += 1; e['dark'].append((h, nd, fv))
                else: e['dark'].append((h, nd, fv))
        e['dark_nodes'] = len(e['dark'])
        e['dark_cycle_types'] = sorted({str(sorted(str(bp.ptype(g)) for g in h)) for h, nd, fv in e['dark']})
        e['dark'] = e['dark'][:5]
    out['seconds'] = round(time.time() - T0, 1)
    print(json.dumps(out, default=list), flush=True)
    json.dump(out, open(HERE / f'result_exh_d{d}{"" if len(kinds) > 1 else "_" + kinds[0]}.json', 'w'), indent=1, default=list)


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'z1': z1(int(sys.argv[2]))
    elif cmd == 'small': small()
    elif cmd == 'rooms': rooms()
    elif cmd == 'exh': exh(int(sys.argv[2]), *((tuple(sys.argv[3].split(',')), float(sys.argv[4])) if len(sys.argv) > 4 else ()))
    elif cmd == 'd21': d21_check()
