"""d61: test the fibre (fold-converse) lemma on NAMED rooms only.

Setting.  Q -> N -> B, N = Q / Pi.  S~, T~ are regular points of Q over a with the same image
u in N.  For a basis and a tail arc alpha : a -> x, let K be the component of u in the
subgraph of Gamma_alpha(N) induced on LIVE vertices (some regular point of Q above).

H_alpha on the fibre.  Nodes: sheets of Q in the blocks of u (= edges of Gamma_alpha(Q) at
the fibre F_u).  Edges:
  A-edge     s -- g_a s   when the Q-point {s, g_a s} over u is regular (a light path may
             pass through it);
  excursion  s -- s'      leave F_u along sheet s, follow K: through N-regular vertices
             (Q-regular by Fact L, asserted), bounce at an N-pole of K iff the Q-point
             reached there is regular (local monodromy restricted to its 2-cycles), stop
             at a non-live vertex; s' is the sheet on which the walk returns to F_u.
             Kind 'wrap' (returns without bouncing: K is a regular cycle) or 'bounce'.
Lemma verdict along alpha: some sheet of S~ and some sheet of T~ are in one component.
Ground truth along alpha: S~, T~ joined in Gamma_alpha(Q) through Q-regular vertices.

Variant FULL (no corner avoidance over N-poles): bounce with the full local permutation and
A-edges for every s, whatever the Q-cycle length.

Per (room, factor, lift pair with equal images, target x) the script ORs over the pure-braid
orbit and compares with the Theorem U certificates at x (d10 unified_test, all factors).

Run: python3 -B fold_converse.py [--wall] [--tower] [room ...]
"""
import sys, json, time
from collections import deque, Counter
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'd60-fh-star-test'))
import fh_star as F  # noqa: E402  (sets RLIMIT_CPU 540 s)
from fh_star import (pure_move, canon, points_of, minimal_systems, LABELS, U, d4, O9, cycles,
                     cycle_index, room_tuple, lattice_points, status, load, cells_from_vertices, D)
from hurwitz import PURE_GENS  # noqa: E402


def cyc_len(g):
    L = [0] * len(g)
    for c in cycles(g):
        for s in c:
            L[s] = len(c)
    return L


def h_graph(ga, gx, where, na_cid, na_len, nx_cid, nx_len, liveA, liveX, u, full=False):
    """Return (V, adjacency with edge kinds) of H_alpha on the fibre over u."""
    n = len(ga)
    La, Lx = cyc_len(ga), cyc_len(gx)
    # K: live component of ('a', u) in Gamma_alpha(N)
    adj = {}
    for b in set(where):
        va, vx = ('a', na_cid[b]), ('x', nx_cid[b])
        if liveA[va[1]] and liveX[vx[1]]:
            adj.setdefault(va, set()).add(vx)
            adj.setdefault(vx, set()).add(va)
    K = {('a', u)}
    st = [('a', u)]
    while st:
        v = st.pop()
        for w in adj.get(v, ()):
            if w not in K:
                K.add(w)
                st.append(w)
    V = [s for s in range(n) if na_cid[where[s]] == u]
    E = {s: [] for s in V}
    for s in V:
        if full or La[s] == 2:
            E[s].append((ga[s], 'A'))
    for s in V:
        cur, kinds, steps = s, set(), 0
        while True:
            steps += 1
            assert steps <= 4 * n + 4
            vx = nx_cid[where[cur]]
            if ('x', vx) not in K:
                cur = None
                break
            if nx_len[vx] == 1:
                if not full and Lx[cur] != 2:
                    cur = None
                    break
                kinds.add('bounce@x')
            else:
                assert nx_len[vx] == 2 and Lx[cur] == 2, 'Fact L violated'
            cur = gx[cur]
            va = na_cid[where[cur]]
            if va == u:
                break
            if ('a', va) not in K:
                cur = None
                break
            if na_len[va] == 1:
                if not full and La[cur] != 2:
                    cur = None
                    break
                kinds.add('bounce@a')
            else:
                assert na_len[va] == 2 and La[cur] == 2, 'Fact L violated'
            cur = ga[cur]
        if cur is not None:
            E[s].append((cur, '+'.join(sorted(kinds)) or 'wrap'))
    shape = ('cycle' if all(len(adj.get(v, ())) == 2 and all(w in K for w in adj[v]) for v in K)
             else 'path')
    return V, E, shape


def connected(E, A, B):
    """Kinds of the edges on a shortest path from A to B (None if not joined)."""
    prev = {a: None for a in A}
    q = deque(A)
    while q:
        s = q.popleft()
        if s in B:
            kinds = []
            while prev[s] is not None:
                s, k = prev[s]
                kinds.append(k)
            return kinds
        for t_, k in E[s]:
            if t_ not in prev:
                prev[t_] = (s, k)
                q.append(t_)
    return None


def dp_joined(ga, gx, A, B):
    """Ground truth along the arc: Q-walk from the sheets of A, interior vertices regular."""
    La, Lx = cyc_len(ga), cyc_len(gx)
    seen = set(A)
    q = deque(A)
    while q:
        s = q.popleft()
        if s in B:
            return True
        # cross the x-end, then the a-end, of the edge s
        if Lx[s] == 2:
            s2 = gx[s]
            if s2 not in seen:
                seen.add(s2)
                if s2 in B:
                    return True
                if La[s2] == 2:
                    s3 = ga[s2]
                    if s3 not in seen:
                        seen.add(s3)
                        q.append(s3)
    return False


def run(t, part, LS, LT, max_states=200000):
    """BFS over the pure-braid orbit; per equal-image lift pair and target x, OR the verdicts."""
    n = len(t[0])
    where = [0] * n
    for b, blk in enumerate(part):
        for s in blk:
            where[s] = b
    nS = len(LS)
    mA = [0] * n
    for k, cy in enumerate(LS):
        for s in cy:
            mA[s] = 1 + k
    for k, cy in enumerate(LT):
        for s in cy:
            mA[s] = nS + 1 + k
    marks = {'a': tuple(mA)}
    roots = lambda mk: [s for s in range(n) if mk['a'][s] == 1]
    seen = {canon(t, marks, where, roots(marks))}
    queue = deque([(t, marks)])
    res = {}
    disagree = Counter()
    states = 0
    while queue:
        t_, mk = queue.popleft()
        states += 1
        ga = t_[0]
        ig0 = d4.induced(ga, part)
        na_cid, na_len = cycle_index(ig0)
        La = cyc_len(ga)
        liveA = [False] * len(na_len)
        for s in range(n):
            if La[s] == 2:
                liveA[na_cid[where[s]]] = True
        lifts = {}
        for s in range(n):
            if mk['a'][s]:
                lifts.setdefault(mk['a'][s], set()).add(s)
        for i in range(1, nS + 1):
            for k in range(nS + 1, len(LS) + len(LT) + 1):
                Si, Tk = lifts[i], lifts[k]
                u = na_cid[where[next(iter(Si))]]
                if na_cid[where[next(iter(Tk))]] != u:
                    continue
                for j in (1, 2, 3):
                    gx = t_[j]
                    igj = d4.induced(gx, part)
                    nx_cid, nx_len = cycle_index(igj)
                    Lx = cyc_len(gx)
                    liveX = [False] * len(nx_len)
                    for s in range(n):
                        if Lx[s] == 2:
                            liveX[nx_cid[where[s]]] = True
                    truth = dp_joined(ga, gx, Si, Tk)
                    V, E, shape = h_graph(ga, gx, where, na_cid, na_len, nx_cid, nx_len, liveA, liveX, u)
                    w = connected(E, Si, Tk)
                    Vf, Ef, _ = h_graph(ga, gx, where, na_cid, na_len, nx_cid, nx_len, liveA, liveX, u,
                                        full=True)
                    wf = connected(Ef, Si, Tk)
                    r = res.setdefault((i, k - nS, j), dict(truth=False, H=False, Hfull=False,
                                                            witness_kinds=Counter(), shapes=Counter()))
                    r['truth'] |= truth
                    r['H'] |= w is not None
                    r['Hfull'] |= wf is not None
                    r['shapes'][shape] += 1
                    if w is not None:
                        r['witness_kinds']['|'.join(sorted(set(k_ for k_ in w if k_ != 'A')))] += 1
                    disagree['H'] += truth != (w is not None)
                    disagree['Hfull'] += truth != (wf is not None)
                    disagree['arcs'] += 1
        for (i_, sg) in PURE_GENS:
            t2, mk2 = pure_move(t_, LABELS, mk, i_, sg)
            c = canon(t2, mk2, where, roots(mk2))
            if c not in seen:
                seen.add(c)
                if len(seen) > max_states:
                    raise RuntimeError('orbit cap')
                queue.append((t2, mk2))
    return res, disagree, states


def certs(t, factors, s, q, P):
    """Per x: list of (kind, blocks or 'self' for the tested factor P, images equal there)."""
    out = {}
    for x in (1, 2, 3):
        L = []
        for Fc in factors:
            if Fc.m == 1:
                continue
            eq = Fc.a_point(s) == Fc.a_point(q)
            lab = 'Q' if Fc.m == len(t[0]) else 'self' if sorted(map(sorted, Fc.part)) == sorted(map(sorted, P)) else Fc.m
            if U.par(Fc, x, s, q):
                L.append(('Par', lab, eq))
            if U.rig(Fc, x, s, q):
                L.append(('Rig', lab, eq))
            if U.cut(Fc, t, x, s, q):
                L.append(('Cut', lab, eq))
        out[x] = L
    return out


def analyse(name, t, LS, LT, systems, truth_pair, label=''):
    n = len(t[0])
    factors = [U.Factor(t, P) for P in systems]
    proper = [P for P in systems if 1 < len(P) < n]
    mins = minimal_systems(proper, n)
    tested = [(P, m) for P, m in zip(proper, mins)] + [([list(range(n))], False)]
    rows = []
    for fid, (P, is_min) in enumerate(tested):
        res, dis, states = run(t, P, LS, LT)
        assert dis['H'] == 0, (name, label, len(P), dis)
        for (i, k, j), r in sorted(res.items()):
            s, q = LS[i - 1][0], LT[k - 1][0]
            C = certs(t, factors, s, q, P)[j]
            perx = U.analyse_pair(t, factors, s, q)[2][j]
            row = dict(room=name, tag=label, fid=fid, blocks=len(P), minimal=is_min, lift=(i, k), x='abcd'[j],
                       truth_pair=truth_pair, lit_x=r['truth'], H=r['H'], Hfull=r['Hfull'],
                       cert_x=sorted(perx), cert_detail=C, shapes=dict(r['shapes']),
                       witness=dict(r['witness_kinds']), arcs=dis['arcs'], states=states,
                       Hfull_disagree_arcs=dis['Hfull'])
            rows.append(row)
            print('%-7s %-22s N=%2d%s lift%s x=%s pair=%-4s lit_x=%-5s H=%-5s Hfull=%-5s cert=%-12s'
                  ' wit=%s shapes=%s' % (name, label, len(P), '*' if is_min else ' ', (i, k), row['x'],
                                          truth_pair, r['truth'], r['H'], r['Hfull'],
                                          '+'.join(row['cert_x']) or '-', row['witness'], row['shapes']),
                  flush=True)
    return rows


def rooms():
    R22 = [(-1, -1), (-1, 1), (0, 1), (0, 2), (1, 2), (1, 3), (3, 3), (3, 2), (4, 2), (4, 1),
           (5, 1), (5, 0), (3, 0), (3, 1), (1, 1), (1, -1), (2, -1), (2, -3), (1, -3), (1, -2),
           (0, -2), (0, -1)]
    Qp = {(0, 0), (1, 0), (1, 1), (2, 1), (2, 2)}
    P6 = Qp | {(i, -j - 1) for i, j in Qp} | {(5 - i, -j - 1) for i, j in Qp} | {(i, 5 - j) for i, j in Qp}
    rd = D / 'd41-two-param-cover' / 'rooms'
    return [('cross12', load(rd / 'cross12.txt')), ('dumb12', load(rd / 'dumb12.txt')),
            ('R22', cells_from_vertices(R22)), ('P6', P6)]


def main_rooms(names, wall):
    allrows = []
    for name, cells in rooms():
        if names and name not in names:
            continue
        t0 = time.process_time()
        kinds = ('interior', 'smooth') if wall else ('interior',)
        pts = [p for p in lattice_points(cells) if status(cells, p) in kinds]
        for S, T in combinations(pts, 2):
            room, t = room_tuple(cells, S)
            n = len(t[0])
            _, LS = points_of(room, t, S, S)
            y_T, LT = points_of(room, t, T, S)
            if y_T != 0:
                continue                      # equal images need one class
            reach, _, _ = O9.decide(cells, [S, T], wanted={frozenset((S, T))})
            truth = 'lit' if T in reach[S] else 'dark'
            systems = d4.all_block_systems(list(t), n)
            allrows += analyse(name, t, LS, LT, systems, truth, label='%s-%s' % (S, T))
        print('== %s CPU %.2f s' % (name, time.process_time() - t0), flush=True)
    return allrows


def main_tower(wall):
    """cross12: N' = N6 plays Q, N = N3 the factor (marks are N6-images)."""
    from fh_tower import refines, quotient, images
    cells = dict(rooms())['cross12']
    kinds = ('interior', 'smooth') if wall else ('interior',)
    pts = [p for p in lattice_points(cells) if status(cells, p) in kinds]
    allrows = []
    for S, T in combinations(pts, 2):
        room, t = room_tuple(cells, S)
        n = len(t[0])
        _, LS = points_of(room, t, S, S)
        y_T, LT = points_of(room, t, T, S)
        if y_T != 0:
            continue
        systems = [P for P in d4.all_block_systems(list(t), n) if 1 < len(P) < n]
        for lo in systems:
            tq, wh = quotient(t, lo)
            IS, IT = images(tq[0], wh, LS), images(tq[0], wh, LT)
            if {tuple(c) for c in IS} & {tuple(c) for c in IT}:
                continue
            if any(len(c) != 2 for c in IS + IT):
                continue   # a mark lands on an N'-pole; the regular-endpoint lemma does not apply
            qsys = d4.all_block_systems(list(tq), len(lo))
            # restrict to factors of N' above which N = N3 sits (handled by analyse over all of N')
            allrows += analyse('cross12^', tq, IS, IT, qsys, 'n/a', label="N'%d %s-%s" % (len(lo), S, T))
    return allrows


if __name__ == '__main__':
    wall = '--wall' in sys.argv
    names = [a for a in sys.argv[1:] if not a.startswith('--')]
    t0 = time.process_time()
    rows = main_tower(wall) if '--tower' in sys.argv else main_rooms(names, wall)
    tag = ('_tower' if '--tower' in sys.argv else '') + ('_wall' if wall else '') + \
          ('_' + '_'.join(names) if names else '')
    json.dump(rows, open(HERE / ('fc%s.json' % tag), 'w'), indent=1, default=str)
    print('total CPU %.2f s' % (time.process_time() - t0))
