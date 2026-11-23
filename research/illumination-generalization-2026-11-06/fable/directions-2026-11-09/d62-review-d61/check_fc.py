"""d62: independent check of d61 Lemma FC in its stated (point-level, algebraic) form.

Differences from d61 fold_converse.h_graph:
  * K's shape uses multigraph degrees (a double edge is a 2-cycle).
  * Ends of K are found from N-data only; tau_p is L_p at the end, conjugated by transport.
  * The verdict is an orbit of POINTS of F_u under <tau_1, tau_2> (u N-regular), or of sheets
    of the pole block under <tau_u, tau_p> (u an N-pole), or under <mu> (cycle).
  * Every pair of regular a-points with equal image is tested, not just marked lifts.
  * Asserts: tau_p fixed-point-free involution, single bounce per excursion, Fact L,
    and FC part 5 in the weak form "mu != id => >= 2 branched poles of Q -> N".
Ground truth: own BFS in Gamma_alpha(Q) with regular interior vertices.
Infrastructure reused (not under test): room_tuple, pure_move, all_block_systems.
"""
import sys, time
from collections import deque, Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'd60-fh-star-test'))
sys.path.insert(0, str(HERE.parent / 'd61-fold-converse'))
import fh_star as F  # noqa: E402
from fold_converse import rooms  # noqa: E402
from hurwitz import PURE_GENS  # noqa: E402


def cycles(g):
    seen, out = set(), []
    for s in range(len(g)):
        if s not in seen:
            c, x = [], s
            while x not in seen:
                seen.add(x); c.append(x); x = g[x]
            out.append(c)
    return out


def pt_index(g):
    cid, ln = [0] * len(g), []
    for k, c in enumerate(cycles(g)):
        ln.append(len(c))
        for s in c:
            cid[s] = k
    return cid, ln


def truth(ga, gx, S, T):
    """Direct walk: S, T sets of sheets (Q-points over a). Interior vertices regular."""
    _, la = pt_index(ga); _, lx = pt_index(gx)
    la_s = [la[c] for c in pt_index(ga)[0]]; lx_s = [lx[c] for c in pt_index(gx)[0]]
    seen, q = set(S), deque(S)
    while q:
        s = q.popleft()
        if lx_s[s] != 2:
            continue
        s2 = gx[s]
        if s2 in T:
            return True
        if la_s[s2] != 2:
            continue
        s3 = ga[s2]
        for v in (s2, s3):
            if v not in seen:
                seen.add(v); q.append(v)
    return False


def fc_verdict(ga, gx, where, nb, S, T, stats, allg):
    n = len(ga)
    ia = tuple(where[ga[min(b)]] for b in nb)  # induced on blocks
    ix = tuple(where[gx[min(b)]] for b in nb)
    acid, alen = pt_index(ia); xcid, xlen = pt_index(ix)
    qa, qal = pt_index(ga); qx, qxl = pt_index(gx)
    La = [qal[qa[s]] for s in range(n)]; Lx = [qxl[qx[s]] for s in range(n)]
    liveA = [False] * len(alen); liveX = [False] * len(xlen)
    for s in range(n):
        if La[s] == 2: liveA[acid[where[s]]] = True
        if Lx[s] == 2: liveX[xcid[where[s]]] = True
        # Fact L
        if alen[acid[where[s]]] == 2: assert La[s] == 2
        if xlen[xcid[where[s]]] == 2: assert Lx[s] == 2
        if alen[acid[where[s]]] == 3: assert La[s] == 3
        if xlen[xcid[where[s]]] == 3: assert Lx[s] == 3
    u = acid[where[S[0]]]
    assert acid[where[T[0]]] == u
    # multigraph K: edges = blocks with both ends live
    edges = [b for b in range(len(nb)) if liveA[acid[b]] and liveX[xcid[b]]]
    inc = defaultdict(list)
    for b in edges:
        inc[('a', acid[b])].append(b); inc[('x', xcid[b])].append(b)
    K, st = {('a', u)}, [('a', u)]
    while st:
        v = st.pop()
        for b in inc[v]:
            for w in (('a', acid[b]), ('x', xcid[b])):
                if w not in K:
                    K.add(w); st.append(w)
    deg = {v: len(inc[v]) for v in K}
    assert max(deg.values()) <= 2
    is_cycle = all(d == 2 for d in deg.values())
    if is_cycle:
        assert all((alen[v[1]] if v[0] == 'a' else xlen[v[1]]) == 2 for v in K)

    def run_out(s, side='x'):
        """Leave u along sheet s; pass N-regular vertices of K. Return (end kind, sheet, steps)."""
        cur = s
        while True:
            v = ('x', xcid[where[cur]]) if side == 'x' else ('a', acid[where[cur]])
            if v == ('a', u):
                return 'home', cur
            if v not in K:
                return 'wall', None
            ln = xlen[v[1]] if side == 'x' else alen[v[1]]
            g = gx if side == 'x' else ga
            if ln == 1:
                return ('pole', side, cur)
            cur = g[cur]
            side = 'a' if side == 'x' else 'x'

    def excursion(s):
        r = run_out(s)
        if r[0] == 'home':
            return ('wrap', r[1])
        if r[0] == 'wall':
            return None
        _, side, cur = r
        g, L = (gx, Lx) if side == 'x' else (ga, La)
        if L[cur] != 2:            # L_p restricted to 2-cycles
            return None
        back = run_out(g[cur], 'a' if side == 'x' else 'x')     # transport back along K
        assert back[0] == 'home', 'second bounce'   # single bounce
        return ('bounce', back[1])

    pts_u = [c for c in cycles(ga) if acid[where[c[0]]] == u]
    if alen[u] == 2:
        beta = where[S[0]]
        side_of = lambda s: where[s] == beta
        # points <-> beta-sheets
        bsheet = {}
        for c in pts_u:
            if len(c) != 2: raise AssertionError('Fact L at u')
            sb = c[0] if side_of(c[0]) else c[1]
            bsheet[frozenset(c)] = sb
        pt_of = {s: frozenset(c) for c in pts_u for s in c}
        if is_cycle:
            mu = {}
            for P, sb in bsheet.items():
                e = excursion(sb)
                assert e and e[0] == 'wrap'
                mu[P] = pt_of[e[1]]
            gens = [mu, {v: k for k, v in mu.items()}]
            stats['cycle'] += 1
            if len(K) == 2:
                stats['cycle_2vertex'] += 1
            if any(k != v for k, v in mu.items()):
                stats['mu_nontrivial'] += 1
                assert branched_poles(allg, where, nb) >= 2, 'part 5 weak form'
        else:
            gens = []
            for pick in (lambda P: bsheet[P], lambda P: ga[bsheet[P]]):
                tau = {}
                for P in bsheet:
                    e = excursion(pick(P))
                    if e is None:
                        continue
                    assert e[0] == 'bounce'
                    tau[P] = pt_of[e[1]]
                for k, v in tau.items():
                    assert k != v and tau[v] == k, 'tau not a fpf involution'
                gens.append(tau)
            stats['path_reg'] += 1
        start, goal = frozenset(S), frozenset(T)
    else:
        assert alen[u] == 1 and not is_cycle
        blk = set(nb[where[S[0]]])
        tau_u = {s: ga[s] for s in blk if La[s] == 2}
        tau_p = {}
        for s in blk:
            e = excursion(s)
            if e is None:
                continue
            assert e[0] == 'bounce'
            tau_p[s] = e[1]
        for k, v in tau_p.items():
            assert k != v and tau_p[v] == k, 'tau_p not fpf involution'
        gens = [tau_u, tau_p]
        stats['path_pole'] += 1
        start, goal = S[0], set(T)
        # S~ regular: sheets S; orbit from either sheet
        seen, q = set(S), deque(S)
        while q:
            x = q.popleft()
            for g in gens:
                if x in g and g[x] not in seen:
                    seen.add(g[x]); q.append(g[x])
        return bool(seen & goal)
    seen, q = {start}, deque([start])
    while q:
        x = q.popleft()
        for g in gens:
            if x in g and g[x] not in seen:
                seen.add(g[x]); q.append(g[x])
    return goal in seen


def branched_poles(allg, where, nb):
    """Number of N-poles (over any corner) where Q -> N branches."""
    cnt = 0
    for g in allg:
        ig = tuple(where[g[min(b)]] for b in nb)
        for k, b in enumerate(nb):
            if ig[k] == k and any(g[s] != s for s in b):
                cnt += 1
    return cnt


def main(name, cap):
    cells = dict(rooms())[name]
    pts = [p for p in F.lattice_points(cells) if F.status(cells, p) in ('interior', 'smooth')]
    origins = {}
    for p in pts:
        origins.setdefault((p[0] % 2, p[1] % 2), p)
    for origin in origins.values():
        main1(name, cells, origin, cap)


def main1(name, cells, origin, cap):
    room, t = F.room_tuple(cells, origin)
    n = len(t[0])
    systems = F.d4.all_block_systems(list(t), n)
    systems = [P for P in systems if len(P) < n]       # proper factors and B
    print(name, 'origin', origin, 'n =', n, 'factors', sorted(len(P) for P in systems), flush=True)
    seen, q = {tuple(t)}, deque([tuple(t)])
    states = []
    while q and len(states) < cap:
        s = q.popleft(); states.append(s)
        for (i, sg) in PURE_GENS:
            t2, _ = F.pure_move(s, F.LABELS, {}, i, sg)
            if t2 not in seen:
                seen.add(t2); q.append(t2)
    stats, agree, dis = Counter(), Counter(), []
    for P in systems:
        where = [0] * n
        nb = [sorted(b) for b in P]
        for k, b in enumerate(nb):
            for s in b:
                where[s] = k
        for st in states:
            ga = st[0]
            ia = tuple(where[ga[min(b)]] for b in nb)
            acid, _ = pt_index(ia)
            reg = [c for c in cycles(ga) if len(c) == 2]
            for j in (1, 2, 3):
                gx = st[j]
                for x in range(len(reg)):
                    for y in range(x + 1, len(reg)):
                        S, T = reg[x], reg[y]
                        if acid[where[S[0]]] != acid[where[T[0]]]:
                            continue
                        tr = truth(ga, gx, set(S), set(T))
                        fc = fc_verdict(ga, gx, where, nb, S, T, stats, st)
                        agree[(len(P), tr, fc)] += 1
                        if tr != fc:
                            dis.append((len(P), j, S, T))
    print(name, 'states', len(states), dict(stats))
    for k in sorted(agree):
        print('  blocks=%2d truth=%-5s FC=%-5s : %d' % (k + (agree[k],)))
    print('  DISAGREEMENTS', len(dis), dis[:3], flush=True)


if __name__ == '__main__':
    cap = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
    t0 = time.process_time()
    main(sys.argv[1], cap)
    print('CPU %.1f s' % (time.process_time() - t0))
