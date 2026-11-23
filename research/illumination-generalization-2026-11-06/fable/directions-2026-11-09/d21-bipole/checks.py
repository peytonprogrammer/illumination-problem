"""Sanity checks and candidate analysis for bipole.py.  Usage: python3 -B checks.py"""
import sys, json, time, itertools
from fractions import Fraction
from collections import Counter, deque
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'd0-dictionary'))
import bipole as bp
import hurwitz as hz
import d0lib as L0
out = {}

# ---- 1. composition against d0lib.room_tuple (rooms that are reflected unions of the base)
def same(t1, t2):
    return hz.canon_plain(t1) == hz.canon_plain(t2)
tro = [(0, 0), (1, 0), (0, 1)]
I1 = ((0,),) * 5
tau, e = (1, 0), (0, 1)
chk = {}
chk['tromino_d1'] = same(bp.compose(2, 2, I1)[0], L0.room_tuple(tro, (0, 0))[1])
chk['L32_d1'] = same(bp.compose(3, 2, I1)[0], L0.room_tuple([(0, 0), (1, 0), (2, 0), (0, 1)], (0, 0))[1])
chk['U_room_d2_mirror_x=2'] = same(bp.compose(2, 2, (tau, tau, e, e, e))[0],
                                   L0.room_tuple(tro + [(3, 0), (2, 0), (3, 1)], (0, 0))[1])
chk['room_d2_mirror_y=0'] = same(bp.compose(2, 2, (e, tau, tau, e, e))[0],
                                 L0.room_tuple(tro + [(0, -1), (1, -1), (0, -2)], (0, 0))[1])
out['composition_vs_d0lib'] = chk
print(chk, flush=True)

# ---- 2. the 22-wall room is DARK under hurwitz.marked_orbit
V = [(0, 2), (0, 4), (1, 4), (1, 5), (2, 5), (2, 6), (4, 6), (4, 5), (5, 5), (5, 4), (6, 4), (6, 3),
     (4, 3), (4, 4), (2, 4), (2, 2), (3, 2), (3, 0), (2, 0), (2, 1), (1, 1), (1, 2)]
S, T = (1, 3), (3, 5)
cells = L0.cells_from_vertices(V)
sheets, t = L0.room_tuple(cells, S)
idx = {c: k for k, c in enumerate(sheets)}
cid, plen = hz.initial_pt(t[0])
ident = {u: cid[idx[c]] for u, c in L0.a_lifts(cells, S).items()}
r = hz.marked_orbit(t)
pairs = [frozenset((ident[(S, a)], ident[(T, b)])) for a in (1, -1) for b in (1, -1)]
out['room22'] = dict(states=r['states'], complete=r['complete'], ST_lift_pairs_lit=[p in r['lit'] for p in pairs],
                     other_lit_pairs=len(r['lit']))
print(out['room22'], flush=True)

# ---- 3. independent ray tracer on the square complex (no Hurwitz moves, no pillowcase tuple)
def tracer(A, B, h):
    d = len(h[0])
    c = [hz.ident(d)]
    for k in range(4): c.append(hz.mul(c[-1], h[k]))
    ci = [hz.inv(x) for x in c]
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
    par = {}
    def find(u):
        while par.setdefault(u, u) != u:
            par[u] = par[par[u]]; u = par[u]
        return u
    EP = {'L': ((0, 0), (0, 1)), 'R': ((1, 0), (1, 1)), 'B': ((0, 0), (1, 0)), 'T': ((0, 1), (1, 1))}
    faces = [(cl, s, m) for cl in cells for s in (0, 1) for m in range(d)]
    for f in faces:
        for dr, eps in EP.items():
            g = nb(f, dr)
            for ex, ey in eps:
                pt = (f[0][0] + ex, f[0][1] + ey)
                par[find((f, pt))] = find((g, pt))
    members = {}
    for u in list(par): members.setdefault(find(u), []).append(u)
    poles = [((A, 1), (A - 1, 0)), ((A, 0), (A - 1, 0)), ((0, 0), (0, 0)), ((0, B), (0, B - 1)), ((1, B), (0, B - 1))]
    def step(f, fx, fy, dr):
        act = ('L' if fx else 'R') if dr == 'R' else ('B' if fy else 'T')
        g = nb(f, act)
        if g[0] == f[0]:
            if dr == 'R': fx ^= 1
            else: fy ^= 1
        return g, fx, fy
    def lit(P, Q, M):
        """P, Q = (pole position, sheet). True iff a ray from P of direction (p,q), p+q<=M, reaches Q."""
        vs = find((((poles[P[0]][1]), 1, P[1]), poles[P[0]][0]))
        vt = find((((poles[Q[0]][1]), 1, Q[1]), poles[Q[0]][0]))
        assert len(members[vs]) == 4 and len(members[vt]) == 4 and vs != vt
        for (f0, pt) in members[vs]:
            for p in range(M + 1):
                for q in range(M + 1 - p):
                    if p + q == 0 or __import__('math').gcd(p, q) != 1: continue
                    ev = [dr for _, dr in sorted([(Fraction(i, p), 'R') for i in range(1, p)] + [(Fraction(j, q), 'T') for j in range(1, q)])]
                    f, fx, fy = f0, pt[0] - f0[0][0], pt[1] - f0[0][1]
                    seen = set()
                    while (f, fx, fy) not in seen:
                        seen.add((f, fx, fy))
                        for dr in ev: f, fx, fy = step(f, fx, fy, dr)
                        v = find((f, (f[0][0] + ((1 if p else 0) ^ fx), f[0][1] + ((1 if q else 0) ^ fy))))
                        if v == vt: return (p, q)
                        if len(members[v]) != 4: break
                        if p: f, fx, fy = step(f, fx, fy, 'R')
                        if q: f, fx, fy = step(f, fx, fy, 'T')
        return None
    return lit

# cross-validation: tracer vs (edge test + pillowcase decider) on tromino, pairs over p_3, p_4
for d, stride, M in ((4, 1, 16), (5, 5, 16)):
    cen = bp.Census(d, 8 - d if d >= 5 else 99)
    cache = {}
    for ms in bp.type_multisets(d, cen.tcap):
        o = sorted(ms, key=lambda ty: -len(cen.cls[ty]))
        for t, _ in bp.seed_tuples(d, cen.cls, cen.typeof, (o[0], o[2], o[3], o[4], o[1]), cache):
            cen.close(t)
    st = Counter()
    for c in range(0, len(cen.tup), stride):
        pts = cen.pts[c]
        P = [i for i, p in enumerate(pts) if p[0] == 2]; Q = [i for i, p in enumerate(pts) if p[0] == 3]
        if not P or not Q: continue
        prs = [((2, pts[p][1]), (3, pts[q][1])) for p in P for q in Q]
        res, _ = bp.pillow_lit(2, 2, cen.tup[c], prs)
        tr = tracer(2, 2, cen.tup[c])
        for pr in prs:
            w = tr(pr[0], pr[1], M)
            st[(res[pr], 'ray' if w else 'noray')] += 1
    out[f'tracer_vs_decider_d{d}'] = {f'{a}/{b}': n for (a, b), n in st.items()}
    print(d, out[f'tracer_vs_decider_d{d}'], flush=True)
    if d == 5: cen5 = cen

# ---- 4. the degree-5 candidate family
cand = json.load(open(HERE / 'result_d5.json'))['dark_candidates']
out['candidates'] = []
for cd in cand:
    t = tuple(tuple(g) for g in cd['member'][0])
    cen = cen5
    c0 = cen.ids[bp.canon(t, 5)[0]]
    p0 = cen.ptidx[c0][cd['member'][1][0] * 5 + cd['member'][1][1]]
    q0 = cen.ptidx[c0][cd['member'][2][0] * 5 + cd['member'][2][1]]
    nodes = {(c0, min(p0, q0), max(p0, q0))}
    dq = deque(nodes)
    while dq:
        c, p, q = dq.popleft()
        for c2, pm in cen.trans[c]:
            n2 = (c2, min(pm[p], pm[q]), max(pm[p], pm[q]))
            if n2 not in nodes: nodes.add(n2); dq.append(n2)
    G = {hz.ident(5)}
    fr = [hz.ident(5)]
    for g in fr:
        for h in t:
            x = hz.mul(g, h)
            if x not in G: G.add(x); fr.append(x)
    rec = dict(tuple=t, cycle_types=[hz.cycle_type(g) for g in t], S=cd['member'][1], T=cd['member'][2],
               family_nodes=len(nodes), covers_in_family=len({n[0] for n in nodes}),
               branched_poles=sum(1 for g in t if g != hz.ident(5)), monodromy_group_order=len(G),
               two_cycle_points_per_cover=len(cen.pts[c0]), decider={}, tracer={})
    for (A, B) in ((2, 2), (3, 2), (3, 4), (2, 4)):
        fold = [(A % 2, 1), (A % 2, 0), (0, 0), (0, B % 2), (1, B % 2)]
        dec, trc, mx = Counter(), Counter(), 0
        for (c, p, q) in sorted(nodes):
            P, Q = cen.pts[c][p], cen.pts[c][q]
            pr = ((P[0], P[1]), (Q[0], Q[1]))
            if fold[P[0]] == fold[Q[0]]:
                res, stt = bp.pillow_lit(A, B, cen.tup[c], [pr])
                dec[res[pr]] += 1; mx = max(mx, stt)
            trc['ray' if tracer(A, B, cen.tup[c])(pr[0], pr[1], 30) else 'noray'] += 1
        rec['decider'][f'L({A},{B})'] = dict(dec, max_orbit_states=mx)
        rec['tracer'][f'L({A},{B})'] = dict(trc)
        print((A, B), dict(dec), mx, dict(trc), flush=True)
    out['candidates'].append(rec)
    print({k: v for k, v in rec.items() if k not in ('decider', 'tracer')}, flush=True)
json.dump(out, open(HERE / 'checks.json', 'w'), indent=1, default=list)
