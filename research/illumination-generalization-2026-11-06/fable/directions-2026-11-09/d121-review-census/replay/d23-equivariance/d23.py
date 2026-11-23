"""d23: checks for the equivariance gap of d22.

Usage: python3 -B d23.py groups | validate | invol | one FAMILY INDEX SCALE CAP M all|lazy | run SCALE SECONDS CAP M WORKERS all|lazy [FAMILY ...]

groups:   braid-closes the three dark tuples; checks node counts, group order, 2-transitivity,
          and that each cover has exactly two 2-cycles (the family pair).
validate: pair_orbit (two labelled points) against hurwitz.marked_orbit (all points labelled).
run:      for every member over the base L(2,2), classifies EVERY pair of regular vertices of
          the scale-SCALE complex (scale 2 = all half-integer points): LIT by an explicit
          segment (d22 tracer, p + q <= M) or by pair_orbit, DARK by a complete pair_orbit
          (pairs over different pillowcase corners go to the doubled complex), else UNDECIDED. It then computes every isometry
          of the square complex and tests each orientation-reversing involution with a fixed
          vertex for the pattern: S, T, rho S, rho T distinct, (S,T) and (S, rho T) both not
          known lit. UNDECIDED counts as possibly dark, so "no pattern" needs LIT verdicts only.
"""
import sys, json, time, itertools
from collections import deque
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'd22-structured'))
import d22
hz, bp = d22.hz, d22.bp
mul, inv = hz.mul, hz.inv


def cyc(d, *cs):
    p = list(range(d))
    for c in cs:
        for i, a in enumerate(c): p[a] = c[(i + 1) % len(c)]
    return tuple(p)


FAM = {
    'P1_d4_A4': (4, (cyc(4), cyc(4), cyc(4, (1, 2, 3)), cyc(4, (0, 1, 2)), cyc(4, (0, 1), (2, 3)))),
    'P1_d5_A5': (5, (cyc(5), cyc(5, (2, 3, 4)), cyc(5, (1, 2, 3)), cyc(5, (0, 1, 2)), cyc(5, (0, 1), (3, 4)))),
    'P2_d5_S5': (5, (cyc(5), cyc(5), cyc(5, (0, 1), (2, 3, 4)), cyc(5, (0, 1, 2), (3, 4)), cyc(5, (0, 4, 2)))),
}


def prod(t):
    p = t[0]
    for g in t[1:]: p = mul(p, g)
    return p


def family(d, h):
    """Braid orbit of h up to simultaneous conjugation (same move as d22.braid_orbits)."""
    assert prod(h) == hz.ident(d)
    seen = {bp.canon(h, d)[0]: tuple(h)}; todo = [tuple(h)]
    while todo:
        t = todo.pop()
        for i in range(len(t) - 1):
            t2 = list(t); t2[i], t2[i + 1] = hz.conj_by(t[i + 1], inv(t[i])), t[i]; t2 = tuple(t2)
            assert prod(t2) == hz.ident(d)
            e = bp.canon(t2, d)[0]
            if e not in seen: seen[e] = t2; todo.append(t2)
    return [seen[e] for e in sorted(seen)]


def group(gens, d):
    G = {hz.ident(d)}; todo = [hz.ident(d)]
    while todo:
        x = todo.pop()
        for g in gens:
            y = mul(x, g)
            if y not in G: G.add(y); todo.append(y)
    return G


def groups():
    out = {}
    for name, (d, h) in FAM.items():
        mem = family(d, h); orders = set(); twotrans = True; ntwo = set()
        for t in mem:
            G = group(t, d); orders.add(len(G))
            twotrans &= len({(g[0], g[1]) for g in G}) == d * (d - 1)
            ntwo.add(len(d22.two_cycles(t)))
        out[name] = dict(members=len(mem), group_orders=sorted(orders), two_transitive_all=twotrans,
                         two_cycles_per_cover=sorted(ntwo))
    print(json.dumps(out, indent=1)); json.dump(out, open(HERE / 'result_groups.json', 'w'), indent=1)


# ------------------------------------------------------------ isometries of the square complex

DR = 'LRBT'
OPP = {'L': 'R', 'R': 'L', 'B': 'T', 'T': 'B'}
ROT = {'R': 'T', 'T': 'L', 'L': 'B', 'B': 'R'}
FLX = {'L': 'R', 'R': 'L', 'B': 'B', 'T': 'T'}


def comp(a, b):
    return tuple(a[DR.index(x)] for x in b)          # a after b; elements are strings over DR


def _d4():
    I, r, f = tuple(DR), tuple(ROT[x] for x in DR), tuple(FLX[x] for x in DR)
    G = {I}; todo = [I]
    while todo:
        x = todo.pop()
        for g in (r, f):
            y = comp(g, x)
            if y not in G: G.add(y); todo.append(y)
    return sorted(G)
D4 = _d4()
REFL = {dr: tuple(OPP[x] if x in (dr, OPP[dr]) else x for x in DR) for dr in DR}


def reverses(A):
    a, b = d22.DV[A[DR.index('R')]], d22.DV[A[DR.index('T')]]
    return a[0] * b[1] - a[1] * b[0] < 0


def isometries(X):
    nb = X.nb; faces = sorted({k[:3] for k in nb}); f0 = faces[0]; out = []
    for f1 in faces:
        for A0 in D4:
            phi = {f0: (f1, A0)}; stack = [f0]; ok = True
            while stack and ok:
                f = stack.pop(); g1, A = phi[f]
                for i, dr in enumerate(DR):
                    g = nb[f + (dr,)]; dr2 = A[i]; g2 = nb[g1 + (dr2,)]
                    Ag = A
                    if g[0] == f[0]: Ag = comp(Ag, REFL[dr])          # wall crossing in the source
                    if g2[0] == g1[0]: Ag = comp(REFL[dr2], Ag)       # wall crossing in the image
                    if g in phi:
                        if phi[g] != (g2, Ag): ok = False; break
                    else:
                        phi[g] = (g2, Ag); stack.append(g)
            if ok and len({v[0] for v in phi.values()}) == len(faces): out.append(phi)
    return out


def vertex_map(X, phi):
    vm = {}
    for v, mem in X.members.items():
        f, pt = mem[0]; g, A = phi[f]
        h = 'R' if pt[0] - f[0][0] else 'L'; w = 'T' if pt[1] - f[0][1] else 'B'
        im = {A[DR.index(h)], A[DR.index(w)]}
        vm[v] = X.find((g, (g[0][0] + (1 if 'R' in im else 0), g[0][1] + (1 if 'T' in im else 0))))
    assert len(set(vm.values())) == len(vm)
    return vm


def describe(phi):
    rev = {reverses(A) != (f[1] != g[1]) for f, (g, A) in phi.items()}
    assert len(rev) == 1
    invol = all(phi[g][0] == f and comp(phi[g][1], A) == tuple(DR) for f, (g, A) in phi.items())
    return rev.pop(), invol


# ------------------------------------------------------------ one surface

CN = {(0, 0): 0, (1, 0): 1, (1, 1): 2, (0, 1): 3}


def build(h, sc):
    cells = [(0, 0), (1, 0), (0, 1)]; s = 1
    while s < sc: cells = d22.scale2(cells); s *= 2
    return d22.Cx(d22.Room(cells, start=(2 * sc, sc)), h)


def unit_saddles(h):
    """True iff the unscaled surface has a horizontal and a vertical unit saddle connection."""
    X = build(h, 1); got = set()
    for f in {k[:3] for k in X.nb}:
        x, y = f[0]
        sing = lambda p: len(X.members[X.find((f, p))]) != 4
        for b in (0, 1):
            if sing((x, y + b)) and sing((x + 1, y + b)): got.add('h')
            if sing((x + b, y)) and sing((x + b, y + 1)): got.add('v')
    return got == {'h', 'v'}


def connected(t_, pt_):
    """S (label 1) and T (label 2) joined along a tail arc a -> x through 2-cycle vertices only."""
    ca, la = hz.cycle_index(t_[0])
    AS, AT = ca[pt_.index(1)], ca[pt_.index(2)]
    starts = [i for i, x in enumerate(pt_) if x == 1]
    for j in (1, 2, 3):
        g = t_[j]; cx, lx = hz.cycle_index(g)
        for u in starts:
            while lx[cx[u]] == 2:
                w = g[u]; a2 = ca[w]
                if a2 == AT: return True
                if la[a2] != 2 or a2 == AS: break
                u = t_[0][w]
    return False


def pair_orbit(t, cS, cT, cap):
    """Complete decider for one pair: pure-braid orbit of (t, S, T) with only S and T labelled.
    Same rule as hurwitz.marked_orbit; the orbit is smaller because other points are unlabelled."""
    cid, lens = hz.cycle_index(t[0]); assert lens[cS] == 2 == lens[cT] and cS != cT
    pt = tuple(1 if c == cS else 2 if c == cT else 0 for c in cid)
    labels = ('a', 'b', 'c', 'd')
    roots = lambda p: [i for i, x in enumerate(p) if x == 1]
    seen = {hz.canon_marked(t, pt, roots(pt))}; queue = deque([(t, pt)])
    while queue:
        t_, pt_ = queue.popleft()
        if connected(t_, pt_): return 'LIT', len(seen)
        for (i, sg) in hz.PURE_GENS:
            t2, lab2, pt2 = hz.pure_move(t_, labels, pt_, i, sg)
            c = hz.canon_marked(t2, pt2, roots(pt2))
            if c not in seen:
                seen.add(c)
                if len(seen) > cap: return 'CAP', len(seen)
                queue.append((t2, pt2))
    return 'DARK', len(seen)


def regular_by_class(X, t, idx, cidx):
    reg = {}
    for v, mem in X.members.items():
        if len(mem) != 4: continue
        cn = CN[(mem[0][1][0] % 2, mem[0][1][1] % 2)]
        ids = {cidx[cn][0][idx[f]] for (f, _) in mem if f in idx}
        assert len(ids) == 1
        cy = ids.pop(); assert cidx[cn][1][cy] == 2
        reg[v] = (cn, cy)
    return reg


def validate(nmax=6):
    """pair_orbit against hurwitz.marked_orbit (all points labelled) on integer points, scale 2."""
    out = {}
    for name, (d, h) in FAM.items():
        agree = dis = 0
        for hh in family(d, h)[:nmax if d == 4 else 1]:
            X = build(hh, 2); t, idx, cidx = X.pillow(); reg = regular_by_class(X, t, idx, cidx)
            r = hz.marked_orbit(t, max_states=400000); assert r['complete']
            cys = sorted(cy for (cn, cy) in reg.values() if cn == 0)
            for a, b in itertools.combinations(cys, 2):
                v = pair_orbit(t, a, b, 400000)[0]
                if (v == 'LIT') == (frozenset((a, b)) in r['lit']) and v != 'CAP': agree += 1
                else: dis += 1
        out[name] = dict(agree=agree, disagree=dis)
    print(json.dumps(out)); json.dump(out, open(HERE / 'result_validate.json', 'w'), indent=1)


def surface(name, i, h, sc, cap, M, cross='all'):
    """All regular vertices of the scale-sc complex. LIT = explicit segment (tracer, p+q <= M) or
    pair_orbit; DARK = pair_orbit complete; else UNDECIDED. Pairs over different pillowcase corners are
    decided on the doubled complex: all of them (cross='all'), or only those that occur in a candidate
    interior-interior or wall-interior pattern (cross='lazy')."""
    T0 = time.time()
    X = build(h, sc); t, idx, cidx = X.pillow(); reg = regular_by_class(X, t, idx, cidx)
    vs = sorted(reg, key=str)
    fam_pair = frozenset(X.vpole(k, a) for (k, a, b) in d22.two_cycles(h))
    assert len(fam_pair) == 2 and fam_pair <= set(vs)
    vis = {v: X.visible(v, M) for v in vs}
    nonvis = {frozenset((a, b)) for a, b in itertools.combinations(vs, 2) if b not in vis[a] and a not in vis[b]}
    dark, und, st = set(), set(), dict(deep_lit=0, maxst=0, X4=None)

    def up(v):
        (cl, sd, m), pt = X.members[v][0]
        return st['X4'].find((((2 * cl[0] + pt[0] - cl[0], 2 * cl[1] + pt[1] - cl[1]), sd, m), (2 * pt[0], 2 * pt[1])))

    def decide(p, allow_cross):
        a, b = tuple(p)
        if reg[a][0] == reg[b][0]:
            cn = reg[a][0]
            v, n = pair_orbit(t[cn:] + t[:cn], reg[a][1], reg[b][1], cap)
        elif not allow_cross: und.add(p); return
        else:                                          # doubled complex: every vertex of X sits over corner 0
            if st['X4'] is None:
                st['X4'] = X4 = build(h, 2 * sc); t4, idx4, cidx4 = X4.pillow()
                st['t4'], st['reg4'] = t4, regular_by_class(X4, t4, idx4, cidx4)
            (ca, ya), (cb, yb) = st['reg4'][up(a)], st['reg4'][up(b)]; assert ca == cb == 0
            v, n = pair_orbit(st['t4'], ya, yb, cap)
        st['maxst'] = max(st['maxst'], n); und.discard(p)
        if v == 'DARK': dark.add(p)
        elif v == 'LIT': st['deep_lit'] += 1
        else: und.add(p)

    for p in sorted(nonvis, key=str): decide(p, cross == 'all')
    isos = [(vertex_map(X, phi),) + describe(phi) for phi in isometries(X)]
    cnt = dict(isometries=len(isos), reversing_involutions_with_fixed_vertex=0, of_those_moving_family_pair=0,
               share_exactly_one_point=0, nonvisible_set_not_invariant=0)
    for vm, rev, invol in isos:
        img = frozenset(vm[v] for v in fam_pair)
        if len(img & fam_pair) == 1: cnt['share_exactly_one_point'] += 1
        if {frozenset((vm[a], vm[b])) for a, b in (tuple(p) for p in nonvis)} != nonvis: cnt['nonvisible_set_not_invariant'] += 1
        if rev and invol and any(vm[v] == v for v in vm):
            cnt['reversing_involutions_with_fixed_vertex'] += 1
            if img != fam_pair: cnt['of_those_moving_family_pair'] += 1

    def patterns():
        pd = dark | und; pats = dict(interior_interior=[], wall_interior=[], wall_wall=[])
        for vm, rev, invol in isos:
            if not (rev and invol and any(vm[v] == v for v in vm)): continue
            for p in pd:
                a, b = tuple(p)
                fa, fb = vm[a] == a, vm[b] == b
                if vm[a] == b: continue
                if fa and fb: pats['wall_wall'].append((p,)); continue
                if fa or fb:
                    s, u = (a, b) if fa else (b, a)
                    q = frozenset((s, vm[u]))
                    if q in pd and str(u) < str(vm[u]): pats['wall_interior'].append((p, q))
                else:
                    q = frozenset((a, vm[b]))
                    if q in pd: pats['interior_interior'].append((p, q))
        return pats

    pats = patterns()
    if cross == 'lazy':
        need = {q for k in ('interior_interior', 'wall_interior') for pp in pats[k] for q in pp if q in und}
        for p in sorted(need, key=str): decide(p, True)
        pats = patterns()
    npairs = len(vs) * (len(vs) - 1) // 2
    out = dict(family=name, index=i, tuple=h, scale=sc, M=M, cap=cap, cross=cross, faces=len(X.nb) // 4, unit_saddles=unit_saddles(h),
               regular=len(vs), pairs=npairs, lit_tracer=npairs - len(nonvis), lit_complete=st['deep_lit'], dark=len(dark),
               undecided=len(und), undecided_same_class=sum(reg[tuple(p)[0]][0] == reg[tuple(p)[1]][0] for p in und),
               family_pair_dark=fam_pair in dark, max_states=st['maxst'])
    out.update(cnt)
    out['patterns'] = {k: dict(count=len(v), all_pairs_proved_dark=sum(all(q in dark for q in pp) for pp in v)) for k, v in pats.items()}
    out['dark_pairs'] = [sorted(str(X.members[v][0][1]) + ('w' if len({f[1] for f, _ in X.members[v]}) == 2 else 'i') for v in p) for p in sorted(dark, key=str)]
    out['seconds'] = round(time.time() - T0, 1)
    return out


def _job(a):
    return surface(*a)


def invol():
    """Isometries only, all members over L(2,2): what each reversing involution with a fixed vertex does."""
    out = {}
    for name, (d, h) in FAM.items():
        e = out[name] = dict(members=0, isometries=0, reversing_involutions_with_fixed_vertex=0, fixing_family_pair_pointwise=0,
                             swapping_family_pair=0, moving_family_pair=0, fixing_every_cone_point=0, members_with_involution=0,
                             cone_points_moved_min=None)
        for hh in family(d, h):
            X = build(hh, 2); e['members'] += 1; got = False
            fam = [X.vpole(k, a) for (k, a, b) in d22.two_cycles(hh)]
            cone = [v for v, m in X.members.items() if len(m) != 4]
            ram = [X.vpole(k, c[0]) for k, g in enumerate(hh) for c in hz.cycles(g) if len(c) == 3] + fam
            for phi in isometries(X):
                e['isometries'] += 1
                vm = vertex_map(X, phi); rev, inv_ = describe(phi)
                keeps = {vm[v] for v in fam} == set(fam)
                e['all_isometries_moving_family_pair'] = e.get('all_isometries_moving_family_pair', 0) + (not keeps)
                if any(vm[v] == v for v in ram):          # lemma: a fixed ramification point forces equivariance
                    e['fixing_a_ramification_point'] = e.get('fixing_a_ramification_point', 0) + 1
                    e['lemma_violations'] = e.get('lemma_violations', 0) + (not keeps)
                if not (rev and inv_ and any(vm[v] == v for v in vm)): continue
                got = True; e['reversing_involutions_with_fixed_vertex'] += 1
                if all(vm[v] == v for v in fam): e['fixing_family_pair_pointwise'] += 1
                elif vm[fam[0]] == fam[1]: e['swapping_family_pair'] += 1
                else: e['moving_family_pair'] += 1
                moved = sum(vm[v] != v for v in cone)
                e['fixing_every_cone_point'] += moved == 0
                e['cone_points_moved_min'] = moved if e['cone_points_moved_min'] is None else min(moved, e['cone_points_moved_min'])
            e['members_with_involution'] += got
    print(json.dumps(out, indent=1)); json.dump(out, open(HERE / 'result_invol.json', 'w'), indent=1)


SUMKEYS = ('pairs', 'lit_tracer', 'lit_complete', 'dark', 'undecided', 'undecided_same_class', 'family_pair_dark', 'unit_saddles',
           'isometries', 'reversing_involutions_with_fixed_vertex', 'of_those_moving_family_pair', 'share_exactly_one_point',
           'nonvisible_set_not_invariant')


def run(sc, seconds, cap, M, workers, cross, only=None):
    from multiprocessing import Pool
    T0 = time.time(); jobs = []
    for name, (d, h) in FAM.items():
        if only and name not in only: continue
        jobs += [(name, i, t, sc, cap, M, cross) for i, t in enumerate(family(d, h))]
    res = []; tag = f's{sc}' + ('_' + '_'.join(only) if only else ''); log = open(HERE / f'log_run_{tag}.txt', 'w')
    with Pool(workers) as pool:
        for r in pool.imap_unordered(_job, jobs):
            res.append(r)
            print(json.dumps({k: v for k, v in r.items() if k != 'tuple'}, default=str), file=log, flush=True)
            if time.time() - T0 > seconds: pool.terminate(); break
    summ = {}
    for r in res:
        s = summ.setdefault(r['family'], dict(surfaces=0, max_states=0, **{k: 0 for k in SUMKEYS},
                                              patterns={k: dict(count=0, all_pairs_proved_dark=0) for k in r['patterns']}))
        s['surfaces'] += 1; s['max_states'] = max(s['max_states'], r['max_states'])
        for k in SUMKEYS: s[k] += r[k]
        for k, v in r['patterns'].items():
            for kk in v: s['patterns'][k][kk] += v[kk]
    out = dict(scale=sc, M=M, cap=cap, cross=cross, jobs=len(jobs), done=len(res), seconds=round(time.time() - T0, 1),
               summary=summ, surfaces=sorted(res, key=lambda r: (r['family'], r['index'])))
    json.dump(out, open(HERE / f'result_run_{tag}.json', 'w'), indent=1, default=str)
    print(json.dumps({k: v for k, v in out.items() if k != 'surfaces'}, indent=1))


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'groups': groups()
    elif cmd == 'validate': validate()
    elif cmd == 'invol': invol()
    elif cmd == 'one':      # one FAMILY INDEX SCALE CAP M all|lazy
        d, h = FAM[sys.argv[2]]
        r = surface(sys.argv[2], int(sys.argv[3]), family(d, h)[int(sys.argv[3])], int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), sys.argv[7])
        r.pop('tuple'); print(json.dumps(r, default=str))
    elif cmd == 'run':      # run SCALE SECONDS CAP M WORKERS all|lazy [FAMILY ...]
        run(int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), sys.argv[7], sys.argv[8:] or None)
