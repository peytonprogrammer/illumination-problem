"""Double covers Q -> N (blocks of size 2): test of the transport lemma (Lemma D2).

For every saved imprimitive orbit, every block system with blocks of size 2, every state
of the plain orbit and every corner x, the script builds
  the chain graph of Q : regular a-points, joined by 2-cycles of g_x between two regular
                         a-points;
  the live graph of N  : a-points and x-points of N that are regular or are poles under a
                         regular point of Q, joined by the sheets of N.
Per state it checks, for each regular a-point u of N with fibre {s1, s2}:
  if the live component of u is a path:  s1 and s2 are chain-connected in Q
                                          <=>  the component contains a live pole.
Per (orbit, block system, corner) it records whether some state has a live pole or an odd
cycle in the live component of a regular a-point of N, and compares with x-lit transitivity.
The orbit-level comparison with the saved x-lit verdicts is made only when the orbit has
one block system with blocks of size 2 (then every relabelling preserves the fibres).

Run: python3 -B double.py 6 8 10
"""
import json
import sys
from collections import Counter, deque
from pathlib import Path

HERE = Path(__file__).resolve().parent
D6 = HERE.parent / 'd6-hurwitz-census'
D12 = HERE.parent / 'd12-lit-side'
sys.path.insert(0, str(D6))
import d4_monodromy as d4                                        # noqa: E402
from hurwitz import cycles, initial_pt, pure_move, canon_plain, PURE_GENS  # noqa: E402

LABELS = ('a', 'b', 'c', 'd')


def uf(k):
    par = list(range(k))

    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x

    def union(a, b):
        par[find(a)] = find(b)
    return find, union


def cyc_index(g):
    idx = [0] * len(g)
    lens = []
    for k, cy in enumerate(cycles(g)):
        lens.append(len(cy))
        for s in cy:
            idx[s] = k
    return idx, lens


def state_check(t, part, x, S):
    """returns (same-fibre pair joined in Q through a live pole, through an odd cycle)"""
    n = len(t[0])
    m = len(part)
    where = [0] * n
    for b, blk in enumerate(part):
        for s in blk:
            where[s] = b
    ga, gx = t[0], t[x]
    ia, la = cyc_index(ga)
    ix, lx = cyc_index(gx)
    na, nx = d4.induced(ga, part), d4.induced(gx, part)
    ja, ma = cyc_index(na)
    jx, mx = cyc_index(nx)
    # liveness of the points of N
    live_a = [False] * len(ma)
    live_x = [False] * len(mx)
    for s in range(n):
        if la[ia[s]] == 2:
            live_a[ja[where[s]]] = True
        if lx[ix[s]] == 2:
            live_x[jx[where[s]]] = True
    for k in range(len(ma)):
        assert ma[k] != 2 or live_a[k]
        assert ma[k] != 3 or not live_a[k]
    # live graph of N: vertices ('a', k), ('x', k); edges = sheets of N between live vertices
    A, X = len(ma), len(mx)
    find, union = uf(A + X)
    deg = [0] * (A + X)
    for b in range(m):
        if live_a[ja[b]] and live_x[jx[b]]:
            union(ja[b], A + jx[b])
            deg[ja[b]] += 1
            deg[A + jx[b]] += 1
    comp_has_pole = Counter()
    comp_edges = Counter()
    comp_verts = Counter()
    for v in range(A + X):
        live = live_a[v] if v < A else live_x[v - A]
        if not live:
            continue
        comp_verts[find(v)] += 1
        comp_edges[find(v)] += deg[v]
        ln = ma[v] if v < A else mx[v - A]
        if ln == 1:
            comp_has_pole[find(v)] += 1
    # chain graph of Q on cycles of g_a and g_x that are 2-cycles
    QA, QX = len(la), len(lx)
    qfind, qunion = uf(QA + QX)
    for s in range(n):
        if la[ia[s]] == 2 and lx[ix[s]] == 2:
            qunion(ia[s], QA + ix[s])
    pole_join = odd_cycle = False
    for k in range(A):
        if ma[k] != 2:
            continue
        fib = sorted({ia[s] for s in range(n) if ja[where[s]] == k})
        assert len(fib) == 2 and all(la[f] == 2 for f in fib)
        joined = qfind(fib[0]) == qfind(fib[1])
        c = find(k)
        is_cycle = comp_edges[c] == 2 * comp_verts[c]
        if is_cycle:
            S['states x fibres: live component is a cycle'] += 1
            if joined:
                odd_cycle = True
                S['  of these, the lift is not closed (fibre joined)'] += 1
        else:
            pole = comp_has_pole[c] > 0
            S['states x fibres: live component is a path'] += 1
            S['  path: joined %s, live pole %s' % (joined, pole)] += 1
            assert joined == pole, 'Lemma D2 fails'
            pole_join = pole_join or pole
    return pole_join, odd_cycle


def main():
    for n in [int(a) for a in sys.argv[1:]]:
        mine = json.loads((D12 / f'mine_n{n}.json').read_text())['orbits']
        S = Counter()
        for o in mine:
            if o['primitive']:
                continue
            t0 = tuple(tuple(g) for g in o['rep'])
            systems = [p for p in d4.all_block_systems(list(t0), n) if len(p) * 2 == n]
            if not systems:
                continue
            cid, plen = initial_pt(t0[0])
            ids = sorted({c for c in cid if plen[c] == 2})
            pos = {p: k for k, p in enumerate(ids)}
            q = len(ids)
            pt0 = tuple(c if plen[c] == 2 else -1 for c in cid)
            seen = {canon_plain(t0)}
            queue = deque([(t0, pt0)])
            states = [t0]
            while queue:
                t, pt = queue.popleft()
                for (i, s) in PURE_GENS:
                    t2, _, pt2 = pure_move(t, LABELS, pt, i, s)
                    c = canon_plain(t2)
                    if c not in seen:
                        seen.add(c)
                        queue.append((t2, pt2))
                        states.append(t2)
            assert len(states) == o['plain']
            for part in systems:
                na = d4.induced(t0[0], part)
                ja, ma = cyc_index(na)
                where = {s: b for b, blk in enumerate(part) for s in blk}
                u = [ja[where[next(i for i in range(n) if cid[i] == p)]] for p in ids]
                for x in (1, 2, 3):
                    pole_join = odd = False
                    for t in states:
                        pj, od = state_check(t, part, x, S)
                        pole_join = pole_join or pj
                        odd = odd or od
                    lit = {(pos[p['P']], pos[p['Q']]) for p in o['pairs'] if p['lit_x'][x - 1]}
                    same = [(i, j) for i in range(q) for j in range(i + 1, q) if u[i] == u[j]]
                    find, union = uf(q)
                    for i, j in lit:
                        union(i, j)
                    trans = all((i, j) in lit for i in range(q) for j in range(i + 1, q) if find(i) == find(j))
                    S['corner relations'] += 1
                    if same and len(systems) == 1:
                        any_same_lit = any(pr in lit for pr in same)
                        S['relations with a same-fibre pair: same-fibre x-lit %s, mechanism present %s'
                          % (any_same_lit, pole_join or odd)] += 1
                    if not trans:
                        S['NOT transitive: live pole %s, odd cycle %s, |G| %d, size-2 systems %d'
                          % (pole_join, odd, o['order'], len(systems))] += 1
        print(n)
        for k, v in sorted(S.items()):
            print('   ', k, v)


if __name__ == '__main__':
    main()
