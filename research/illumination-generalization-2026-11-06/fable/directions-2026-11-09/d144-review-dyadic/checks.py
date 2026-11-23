"""d144: independent checks of dyadic-classes.2026-11-22-0145.md.

Builds only the named rooms (cov4181, R22's 22-gon Q, the 2x4 rectangle).
Independent of d66: the 4-copy unfolding is built here as an origami (h, v on 4n
unit squares), and the complete SL2(Z) orbit of the marked origami (squares
canonically relabelled, M mod 2 tracked) gives every primitive direction at once.
Vertical flow in state M.O is direction M^{-1} e2 in O. A direct straight-line tracer
on O cross-checks the shear machinery state by state for short directions.
Convention: a ray stops at every physical corner lift (convex or reflex).
Run: python3 -B checks.py
"""
import resource
import sys
import time
from math import gcd, floor, log2
from collections import deque

resource.setrlimit(resource.RLIMIT_CPU, (400, 400))
STATE_CAP = 200000


# ---------------------------------------------------------------- room geometry
def star(cells, p):
    x, y = p
    return [(x - i, y - j) for i in (0, 1) for j in (0, 1) if (x - i, y - j) in cells]


def site_kind(cells, p):
    st = star(cells, p)
    if len(st) == 4:
        return 'interior'
    if len(st) == 2:
        (a, b), (c, d) = st
        return 'smooth' if abs(a - c) + abs(b - d) == 1 else 'pinch'
    if len(st) == 1:
        return 'convex'
    if len(st) == 3:
        return 'reflex'
    return 'outside'


def room_report(name, cells):
    xs = [c[0] for c in cells] + [c[0] + 1 for c in cells]
    ys = [c[1] for c in cells] + [c[1] + 1 for c in cells]
    pts = [(x, y) for x in range(min(xs), max(xs) + 1) for y in range(min(ys), max(ys) + 1)]
    kinds = {p: site_kind(cells, p) for p in pts}
    # boundary unit edges
    E = []
    for (x, y) in cells:
        if (x, y - 1) not in cells: E.append(((x, y), (x + 1, y)))
        if (x, y + 1) not in cells: E.append(((x, y + 1), (x + 1, y + 1)))
        if (x - 1, y) not in cells: E.append(((x, y), (x, y + 1)))
        if (x + 1, y) not in cells: E.append(((x + 1, y), (x + 1, y + 1)))
    deg = {}
    for a, b in E:
        deg[a] = deg.get(a, 0) + 1; deg[b] = deg.get(b, 0) + 1
    adj = {}
    for a, b in E:
        adj.setdefault(a, []).append(b); adj.setdefault(b, []).append(a)
    # one cycle?
    start = E[0][0]; seen = {start}; st = [start]
    while st:
        u = st.pop()
        for w in adj[u]:
            if w not in seen: seen.add(w); st.append(w)
    one_cycle = len(seen) == len(deg)
    # cell connectivity
    c0 = next(iter(cells)); cs = {c0}; st = [c0]
    while st:
        x, y = st.pop()
        for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            w = (x + d[0], y + d[1])
            if w in cells and w not in cs: cs.add(w); st.append(w)
    # maximal edges and normalization
    hor = {e for e in E if e[0][1] == e[1][1]}
    ver = {e for e in E if e[0][0] == e[1][0]}
    def maximal(es, horiz):
        es = sorted(es); used = set(); L = []
        for e in es:
            if e in used: continue
            a, b = e; n = 1; used.add(e)
            while True:
                nb = (b[0] + 1, b[1]) if horiz else (b[0], b[1] + 1)
                if (b, nb) in es and kinds[b] not in ('convex', 'reflex'):
                    used.add((b, nb)); b = nb; n += 1
                else:
                    break
            L.append(n)
        return L
    hl = maximal(hor, True); vl = maximal(ver, False)
    gh = 0
    for l in hl: gh = gcd(gh, l)
    gv = 0
    for l in vl: gv = gcd(gv, l)
    conv = sum(1 for k in kinds.values() if k == 'convex')
    refl = sum(1 for k in kinds.values() if k == 'reflex')
    info = dict(n=len(cells), connected=len(cs) == len(cells), boundary_deg2=all(d == 2 for d in deg.values()),
                one_boundary_cycle=one_cycle, pinches=sum(1 for k in kinds.values() if k == 'pinch'),
                convex=conv, reflex=refl, W=conv + refl, maximal_edges=len(hl) + len(vl),
                gcd_h=gh, gcd_v=gv, normalized=(gh == 1 and gv == 1))
    print(f'[{name}] ' + ' '.join(f'{k}={v}' for k, v in info.items()))
    return kinds, info


def census(name, kinds):
    out = {}
    for par in ((0, 0), (0, 1), (1, 0), (1, 1)):
        ps = [p for p, k in kinds.items() if (p[0] % 2, p[1] % 2) == par and k != 'outside']
        reg = [p for p in ps if kinds[p] in ('interior', 'smooth')]
        cor = [p for p in ps if kinds[p] in ('convex', 'reflex')]
        out[par] = (len(reg), len(cor), len(ps))
        print(f'[{name}] parity {par}: regular {len(reg)} (interior {sum(kinds[p]=="interior" for p in reg)}, '
              f'smooth {sum(kinds[p]=="smooth" for p in reg)}), corners {len(cor)}, closed-room lattice pts {len(ps)}')
    return out


# ---------------------------------------------------------------- origami
def build_origami(cells, S, T):
    cl = sorted(cells)
    sq = [(c, ex, ey) for c in cl for ex in (0, 1) for ey in (0, 1)]
    idx = {s: i for i, s in enumerate(sq)}
    N = len(sq)
    h = [0] * N; v = [0] * N
    for i, (c, ex, ey) in enumerate(sq):
        dx = 1 if ex == 0 else -1
        nb = (c[0] + dx, c[1])
        h[i] = idx[(nb, ex, ey)] if nb in cells else idx[(c, 1 - ex, ey)]
        dy = 1 if ey == 0 else -1
        nb = (c[0], c[1] + dy)
        v[i] = idx[(nb, ex, ey)] if nb in cells else idx[(c, ex, 1 - ey)]
    assert sorted(h) == list(range(N)) and sorted(v) == list(range(N))
    # corners 0 BL 1 BR 2 TL 3 TR ; physical position
    def phys(i, k):
        (cx, cy), ex, ey = sq[i]
        rx = (k & 1); ry = (k >> 1) & 1
        return (cx + (rx ^ ex), cy + (ry ^ ey))
    par = list(range(4 * N))
    def f(a):
        while par[a] != a:
            par[a] = par[par[a]]; a = par[a]
        return a
    def u(a, b): par[f(a)] = f(b)
    for i in range(N):
        u(4 * i + 1, 4 * h[i] + 0); u(4 * i + 3, 4 * h[i] + 2)
        u(4 * i + 2, 4 * v[i] + 0); u(4 * i + 3, 4 * v[i] + 1)
    classes = {}
    for a in range(4 * N):
        classes.setdefault(f(a), []).append(a)
    lab = [None] * (4 * N)
    nreg = 0; nreg_noncorner = 0
    for r, mem in classes.items():
        P = {phys(a // 4, a % 4) for a in mem}
        assert len(P) == 1, P
        p = P.pop()
        k = site_kind(cells, p)
        if len(mem) == 4: nreg += 1
        if k in ('convex', 'reflex', 'pinch'):
            L = 'X'
        else:
            assert len(mem) == 4
            nreg_noncorner += 1
            L = 'S' if p == S else 'T' if p == T else '.'
        for a in mem: lab[a] = L
    corner_lab = [[lab[4 * i + k] for k in range(4)] for i in range(N)]
    return dict(N=N, h=h, v=v, corner=corner_lab, vclass=[f(a) for a in range(4 * N)],
                nvert=len(classes), nreg2pi=nreg, nreg_noncorner=nreg_noncorner)


def inv(p):
    q = [0] * len(p)
    for i, x in enumerate(p): q[x] = i
    return q


def compose(a, b):  # a after b
    return [a[b[i]] for i in range(len(b))]


def canon(h, v, bl):
    N = len(h); best = None
    for s0 in range(N):
        if bl[s0] != 'S': continue
        order = {s0: 0}; q = [s0]; k = 0
        while k < len(q):
            s = q[k]; k += 1
            for t in (h[s], v[s]):
                if t not in order: order[t] = len(q); q.append(t)
        assert len(q) == N
        key = (tuple(order[h[s]] for s in q), tuple(order[v[s]] for s in q), ''.join(bl[s] for s in q))
        if best is None or key < best: best = key
    return best


def vtrace(step, bl, s0, cap):
    """Iterate s -> step(s) from s0; return (T-hit step counts, end) with end ('stop', k) or ('cycle', C)."""
    hits = []; s = s0
    for k in range(1, cap + 2):
        s = step[s]
        if s == s0: return hits, ('cycle', k)
        L = bl[s]
        if L == 'T': hits.append(k)
        if L == 'X': return hits, ('stop', k)
    raise RuntimeError('trace overflow')


def mat_mul(A, B):
    return ((A[0][0] * B[0][0] + A[0][1] * B[1][0], A[0][0] * B[0][1] + A[0][1] * B[1][1]),
            (A[1][0] * B[0][0] + A[1][1] * B[1][0], A[1][0] * B[0][1] + A[1][1] * B[1][1]))


def minv_e2(M):  # M^{-1} e2 for det 1: M^{-1} = [[d,-b],[-c,a]] -> column 2 = (-b, a)
    return (-M[0][1], M[0][0])


def orbit(O, name, cap_states=STATE_CAP, crosscheck_H=12):
    N = O['N']
    bl0 = [O['corner'][i][0] for i in range(N)]
    h0, v0 = O['h'], O['v']
    A = ((1, 1), (0, 1)); B = ((1, 0), (1, 1))
    key0 = canon(h0, v0, bl0)
    seen = {(key0, ((1, 0), (0, 1)))}  # M mod 2
    q = deque([(h0, v0, bl0, ((1, 0), (0, 1)))])
    per_class = {(1, 0): [], (0, 1): [], (1, 1): []}
    xchecks = [0, 0]
    t0 = time.process_time()
    while q:
        h, v, bl, M = q.popleft()
        d = minv_e2(M)
        c = (d[0] % 2, d[1] % 2)
        vi = inv(v)
        for step in (v, vi):
            for s0 in range(N):
                if bl[s0] != 'S': continue
                hits, end = vtrace(step, bl, s0, N)
                per_class[c].append((hits, end))
        if max(abs(d[0]), abs(d[1])) <= crosscheck_H:
            xchecks[0] += 1
            mine = sorted(repr(vtrace(st, bl, s0, N)) for s0 in range(N) if bl[s0] == 'S' for st in (v, vi))
            direct = sorted(repr(x) for sg in (1, -1) for x in direct_trace(O, (sg * d[0], sg * d[1])))
            xchecks[1] += mine == direct
        for G, kind in ((A, 'A'), (B, 'B')):
            if kind == 'A':
                h2, v2 = h, compose(v, inv(h))
            else:
                h2, v2 = compose(h, inv(v)), v
            M2 = mat_mul(G, M)
            M2m = tuple(tuple(x % 2 for x in r) for r in M2)
            key = (canon(h2, v2, bl), M2m)
            if key in seen: continue
            seen.add(key)
            if len(seen) > cap_states:
                print(f'[{name}] STATE CAP {cap_states} reached; orbit incomplete'); return None
            q.append((h2, v2, bl, M2))
    cpu = time.process_time() - t0
    print(f'[{name}] complete orbit: {len(seen)} (origami, M mod 2) states, CPU {cpu:.1f}s; '
          f'shear-vs-direct cross-checks {xchecks[1]}/{xchecks[0]} agree (|dir| <= {crosscheck_H})')
    return per_class, len(seen), xchecks


def nu2(k):
    j = 0
    while k % 2 == 0: k //= 2; j += 1
    return j


def spectrum(rows, n):
    """Attainable j = nu2(travel count) per class; cycles contribute h + l*C."""
    js = set(); tail = None; first = None
    for hits, end in rows:
        for hh in hits:
            first = hh if first is None else min(first, hh)
            if end[0] == 'cycle':
                C = end[1]; b = nu2(C)
                if nu2(hh) < b: js.add(nu2(hh))
                else:
                    tail = b if tail is None else min(tail, b)
            else:
                js.add(nu2(hh))
    return js, tail, first


# ---------------------------------------------------------------- direct tracer on O
def direct_trace(O, d):
    """Straight-line trace in direction d (primitive) from every S lift on O, no shears."""
    p, q = d
    N = O['N']; h, v, corner, vclass = O['h'], O['v'], O['corner'], O['vclass']
    # quadrant flips: build (h', v', corner') with direction (|p|,|q|)
    hh, vv = h, v
    cmap = [0, 1, 2, 3]
    if p < 0:
        hh = inv(hh); cmap = [cmap[1], cmap[0], cmap[3], cmap[2]]
    if q < 0:
        vv = inv(vv); cmap = [cmap[2], cmap[3], cmap[0], cmap[1]]
    p, q = abs(p), abs(q)
    lab = [[corner[i][cmap[k]] for k in range(4)] for i in range(N)]
    vc = [[vclass[4 * i + cmap[k]] for k in range(4)] for i in range(N)]
    bl_of = {}
    for i in range(N): bl_of[vc[i][0]] = i
    # crossing word for one primitive step
    ev = sorted([(F(i, p), 'h') for i in range(1, p)] + [(F(j, q), 'v') for j in range(1, q)])
    word = [e[1] for e in ev]
    def step(s):
        if p == 0: return vv[s]
        if q == 0: return hh[s]
        for w in word:
            s = hh[s] if w == 'h' else vv[s]
        if lab[s][3] == 'X': return None
        return bl_of[vc[s][3]]
    out = []
    for s0 in range(N):
        if lab[s0][0] != 'S': continue
        hits = []; s = s0; end = None
        for k in range(1, N + 2):
            t = step(s)
            if t is None or lab[t][0] == 'X':
                end = ('stop', k); break
            if t == s0:
                end = ('cycle', k); break
            if lab[t][0] == 'T': hits.append(k)
            s = t
        out.append((hits, end))
    return out


from fractions import Fraction as F  # noqa: E402


# ---------------------------------------------------------------- main
def run_room(name, cells, S, T):
    kinds, info = room_report(name, cells)
    print(f'[{name}] S={S} {kinds[S]}  T={T} {kinds[T]}  parity S {(S[0]%2,S[1]%2)} T {(T[0]%2,T[1]%2)}')
    cen = census(name, kinds)
    O = build_origami(cells, S, T)
    print(f'[{name}] 4-copy origami: {O["N"]} squares (4n={4*len(cells)}), {O["nvert"]} vertices, '
          f'{O["nreg2pi"]} angle-2pi lattice points (<= 4n: {O["nreg2pi"] <= 4*len(cells)}), '
          f'{O["nreg_noncorner"]} regular non-corner lattice points')
    res = orbit(O, name)
    if res is None: return
    per_class, ns, xc = res
    n = len(cells); cut = floor(log2(4 * n))
    for c in ((1, 0), (1, 1), (0, 1)):
        rows = per_class[c]
        lit = any(r[0] for r in rows)
        js, tail, first = spectrum(rows, n)
        cyc = [r[1][1] for r in rows if r[1][0] == 'cycle']
        print(f'[{name}] primitive parity {c} -> target parity {((S[0]+c[0])%2,(S[1]+c[1])%2)}: '
              f'{"LIT" if lit else "dark"}; min travel count {first}; finite j set {sorted(js)}; '
              f'tail from j>={tail}; max cycle length {max(cyc) if cyc else None}; cutoff floor(log2 4n)={cut}')
        for hits, end in rows:
            for k in hits: assert k % 2 == 0, 'odd travel count to a same-parity target'


if __name__ == '__main__':
    t0 = time.process_time()
    # cov4181 (d66 README section 7)
    cov = set()
    for x, ys in enumerate([range(6), (2, 3), (2, 3), range(6), range(6), (2, 3), (2,), range(3)]):
        for y in ys: cov.add((x, y))
    assert len(cov) == 28
    readme = {(0, y) for y in range(6)} | {(1, 2), (1, 3), (2, 2), (2, 3)} | {(3, y) for y in range(6)} | \
             {(4, y) for y in range(6)} | {(5, 2), (5, 3), (6, 2)} | {(7, y) for y in range(3)}
    assert cov == readme
    for yy in range(5, -1, -1):
        print('   y=%d ' % yy + ''.join('#' if (xx, yy) in cov else '.' for xx in range(8)))
    S, T = (2, 3), (4, 3)
    print('[cov4181] chord (2,3)-(4,3): midpoint (3,3) kind', site_kind(cov, (3, 3)),
          '; unit edges y=3 x in [2,4] open:', all((x, 2) in cov and (x, 3) in cov for x in (2, 3)))
    run_room('cov4181', cov, S, T)

    # R22: Q = P0 u P1 u P2 from twenty-two-wall/manuscript.tex
    P = [(-1, -1), (0, -1), (0, -2), (1, -2), (1, -3)]
    Q = set(P) | {(x, -y - 1) for x, y in P} | {(3 - x, -y - 1) for x, y in P}
    assert len(Q) == 15
    run_room('R22', Q, (0, 0), (2, 2))

    # 2x4 rectangle, pair (1,1)-(1,3)
    R = {(x, y) for x in range(2) for y in range(4)}
    run_room('rect2x4', R, (1, 1), (1, 3))
    ys = sorted({(3 + 8 * m) - 1 for m in range(-3, 4)} | {(-3 + 8 * m) - 1 for m in range(-3, 4)})
    print('[rect2x4] developed vertical displacements to images of y=3, mod 8:', sorted({d % 8 for d in ys}),
          'nu2 set', sorted({nu2(abs(d)) for d in ys}))

    # Claim (2): algebraic identity on a grid of even D
    bad = 0; tot = 0
    for a in range(-40, 41, 2):
        for b in range(-40, 41, 2):
            if a == 0 and b == 0: continue
            k = gcd(abs(a), abs(b)); vv = (a // k, b // k); j = nu2(k)
            z = (a // 2 ** j, b // 2 ** j)
            tot += 1
            bad += not ((z[0] % 2, z[1] % 2) == (vv[0] % 2, vv[1] % 2) and (z[0] % 2 or z[1] % 2) and (k // 2 ** j) % 2 == 1)
    print(f'[claim2] D/2^nu2(k) parity == v parity and odd multiple: {tot - bad}/{tot} even D in [-40,40]^2')
    print(f'TOTAL CPU {time.process_time() - t0:.1f}s')
