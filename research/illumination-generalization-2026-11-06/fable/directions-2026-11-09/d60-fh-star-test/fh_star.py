"""d60: exact falsification test of FH* (d59 memo, section 4, route 1) on NAMED rooms only.

For each named room, each pair {S, T} of lattice points (interior by default; all classes),
and each proper block system Pi of G (N = DP / Pi, 1 < |Pi| < n), a BFS walks the pure-braid
orbit of the marked cover (DP, lifts of S, lifts of T, Pi).  Pi is part of the canonical form,
so every basis is evaluated with the SAME factor.  In each basis and each admissible tail arc
a -> x_j (j in {b, c, d} if S, T are in one class; j = class of T otherwise) it records:

  Nlit     images phi(S~), phi(T~) are distinct and joined in the N arc graph; interior vertices
           must be 2-cycles of N; endpoints may be N-regular or N-poles.
  Nlit_reg the same with both endpoints N-regular (the d6 marked_orbit rule applied to N).
  Qlit     some S~, T~ joined in the DP arc graph, interior vertices 2-cycles of DP (ground truth).
  Qadm     some S~, T~ joined in DP with every interior vertex a 2-cycle of DP whose image is a
           2-cycle of N.  Such a path is exactly a lift of an N-lighting path (a straight N-path
           whose interior vertices are N-regular; over N-regular points DP -> N is unramified, so
           the lift is unique once the starting sheet is fixed).

Readings of "some lift of an N-lighting path joins lifts of S and T":
  STRONG  every N-witness (basis, arc) with Nlit lifts: Qadm holds in that same basis and arc.
  WEAK    some (basis, arc) has Qadm (a lift of SOME N-lighting path, any basis, any arc).
  ANY     Qlit somewhere (= the pair is lit in DP; no factor condition).

Certificates (same-class pairs only; d10 unified_test.analyse_pair over all block systems,
Par / Cut / Rig over B plus ParRel / RigRel over intermediate pillowcases), per lift pair.
Ground truth: d6 marked_orbit (same class) and d9 orbit.decide (all classes).

Run: python3 -B fh_star.py [--wall]      (--wall adds smooth wall points as marks)
"""
import sys, json, time, resource
from collections import deque
from itertools import combinations
from pathlib import Path

resource.setrlimit(resource.RLIMIT_CPU, (540, 540))
HERE = Path(__file__).resolve().parent
D = HERE.parent
for sub in ('d6-hurwitz-census', 'd10-mechanisms', 'd9-census-w22', 'd59-strategy'):
    sys.path.insert(0, str(D / sub))
from roomtools import (room_tuple, cells_from_vertices, lattice_points, status, OFFS,  # noqa: E402
                       ledger, decide_pairs)
from hurwitz import inv, conj_by, cycles, cycle_index, PURE_GENS  # noqa: E402
import d4_monodromy as d4  # noqa: E402
import unified_test as U  # noqa: E402
import orbit as O9  # noqa: E402
from axis_twist import load  # noqa: E402

LABELS = ('a', 'b', 'c', 'd')
EARLY_MIXED = False


def move(t, marks, i, sign):
    """hurwitz.move with point marks tracked over every corner (pt' = pt o k^-1 on the moved one)."""
    t = list(t)
    a, b = t[i], t[i + 1]
    if sign > 0:
        k = inv(a)
        t[i], t[i + 1] = conj_by(b, k), a
        moved = i + 1
    else:
        k = b
        t[i], t[i + 1] = b, conj_by(a, k)
        moved = i
    return tuple(t), moved, k


def pure_move(t, labels, marks, i, sign):
    labels = list(labels)
    marks = dict(marks)
    for _ in range(2):
        t, pos, k = move(t, marks, i, sign)
        lab = labels[pos]
        labels[i], labels[i + 1] = labels[i + 1], labels[i]
        if lab in marks:
            kinv = inv(k)
            m = marks[lab]
            marks[lab] = tuple(m[kinv[x]] for x in range(len(m)))
    assert tuple(labels) == LABELS
    return t, marks


def canon(t, marks, part_where, roots):
    n = len(t[0])
    best = None
    mk = list(zip(*(marks[L] for L in sorted(marks))))
    for r in roots:
        lab = [-1] * n
        order = [r]
        lab[r] = 0
        for x in order:
            for g in t[:3]:
                y = g[x]
                if lab[y] < 0:
                    lab[y] = len(order)
                    order.append(y)
        bmin = [n] * n
        for s in range(n):
            b = part_where[s]
            if lab[s] < bmin[b]:
                bmin[b] = lab[s]
        enc = tuple(v for s in order for v in (lab[t[0][s]], lab[t[1][s]], lab[t[2][s]],
                                                 bmin[part_where[s]], mk[s]))
        if best is None or enc < best:
            best = enc
    return best


def joined(vertices_ok, edges, A, B):
    """A, B: sets of endpoint vertices. Interior vertices must satisfy vertices_ok.
    Returns True iff some a in A, b in B (a != b) are joined by a path whose interior is ok."""
    par = {}

    def find(u):
        while par.setdefault(u, u) != u:
            par[u] = par[par[u]]
            u = par[u]
        return u

    nb = {}
    for u, v in edges:
        nb.setdefault(u, set()).add(v)
        nb.setdefault(v, set()).add(u)
        if vertices_ok(u) and vertices_ok(v):
            ru, rv = find(u), find(v)
            if ru != rv:
                par[ru] = rv

    def ends(u):
        if vertices_ok(u):
            return {find(u)}
        return {find(w) for w in nb.get(u, ()) if vertices_ok(w)}

    for a in A:
        ea = ends(a)
        for b in B:
            if a == b:
                continue
            if b in nb.get(a, ()) or (ea & ends(b)):
                return True
    return False


def evaluate(t, marks, part, where, y_T, nS):
    """One basis: per arc j, flags (Nlit, Nlit_reg, Qlit, Qadm)."""
    n = len(t[0])
    m = len(part)
    out = {}
    js = (1, 2, 3) if y_T == 0 else (y_T,)
    qa_cid, qa_len = cycle_index(t[0])
    ig0 = d4.induced(t[0], part)
    na_cid, na_len = cycle_index(ig0)
    mA = marks['a']
    mT = marks['a'] if y_T == 0 else marks[LABELS[y_T]]
    S_q = {('a', qa_cid[s]) for s in range(n) if 1 <= mA[s] <= nS}
    for j in js:
        qx_cid, qx_len = cycle_index(t[j])
        igj = d4.induced(t[j], part)
        nx_cid, nx_len = cycle_index(igj)
        if y_T == 0:
            T_q = {('a', qa_cid[s]) for s in range(n) if mT[s] > nS}
        else:
            T_q = {('x', qx_cid[s]) for s in range(n) if mT[s] > 0}
        # image map Q-vertex -> N-vertex
        def img(v):
            tag, c = v
            s = next(s for s in range(n) if (qa_cid if tag == 'a' else qx_cid)[s] == c)
            b = where[s]
            return (tag, na_cid[b] if tag == 'a' else nx_cid[b])
        qlen = lambda v: (qa_len if v[0] == 'a' else qx_len)[v[1]]
        nlen = lambda v: (na_len if v[0] == 'a' else nx_len)[v[1]]
        qedges = [(('a', qa_cid[s]), ('x', qx_cid[s])) for s in range(n)]
        nedges = [(('a', na_cid[b]), ('x', nx_cid[b])) for b in range(m)]
        imgs = {}
        def im(v):
            if v not in imgs:
                imgs[v] = img(v)
            return imgs[v]
        S_n = {im(v) for v in S_q}
        T_n = {im(v) for v in T_q}
        Nlit = joined(lambda v: nlen(v) == 2, nedges, S_n, T_n)
        Nlit_reg = joined(lambda v: nlen(v) == 2, nedges,
                          {v for v in S_n if nlen(v) == 2}, {v for v in T_n if nlen(v) == 2})
        Qlit = joined(lambda v: qlen(v) == 2, qedges, S_q, T_q)
        Qadm = joined(lambda v: qlen(v) == 2 and nlen(im(v)) == 2, qedges, S_q, T_q)
        out[j] = (Nlit, Nlit_reg, Qlit, Qadm)
    return out, (S_n, T_n)


def run_pair_factor(t, LS, LT, y_T, part, max_states=200000, early=False):
    """early=True: stop at the first basis with Qadm (WEAK decided; STRONG then not computed)."""
    n = len(t[0])
    where = [0] * n
    for b, blk in enumerate(part):
        for s in blk:
            where[s] = b
    mA = [0] * n
    for k, cy in enumerate(LS):
        for s in cy:
            mA[s] = 1 + k
    nS = len(LS)
    marks = {}
    if y_T == 0:
        for k, cy in enumerate(LT):
            for s in cy:
                mA[s] = nS + 1 + k
        marks['a'] = tuple(mA)
    else:
        mY = [0] * n
        for k, cy in enumerate(LT):
            for s in cy:
                mY[s] = 1 + k
        marks['a'] = tuple(mA)
        marks[LABELS[y_T]] = tuple(mY)
    roots = lambda mk: [s for s in range(n) if mk['a'][s] == 1]
    c0 = canon(t, marks, where, roots(marks))
    seen = {c0}
    queue = deque([(t, marks)])
    stats = dict(states=0, witnesses=0, witness_lifts=0, witness_no_lift=0, Nlit=False, Nlit_reg=False,
                 Qlit=False, Qadm=False, Qadm_without_Nwit=0)
    eq = None
    while queue:
        t_, mk = queue.popleft()
        stats['states'] += 1
        res, (S_n, T_n) = evaluate(t_, mk, part, where, y_T, nS)
        if eq is None:
            eq = bool(y_T == 0 and (S_n & T_n))
        for j, (Nl, Nr, Ql, Qa) in res.items():
            stats['Nlit'] |= Nl
            stats['Nlit_reg'] |= Nr
            stats['Qlit'] |= Ql
            stats['Qadm'] |= Qa
            if Nl:
                stats['witnesses'] += 1
                if Qa:
                    stats['witness_lifts'] += 1
                else:
                    stats['witness_no_lift'] += 1
            elif Qa:
                stats['Qadm_without_Nwit'] += 1
        if early and stats['Qadm']:
            stats['early_stop'] = True
            break
        for (i, sg) in PURE_GENS:
            t2, mk2 = pure_move(t_, LABELS, mk, i, sg)
            c = canon(t2, mk2, where, roots(mk2))
            if c not in seen:
                seen.add(c)
                if len(seen) > max_states:
                    raise RuntimeError('orbit cap')
                queue.append((t2, mk2))
    stats['equal_images'] = eq
    return stats


def points_of(room, t, p, origin):
    q = (p[0] - origin[0], p[1] - origin[1])
    c, pts = room.points_at(q)
    return OFFS[c], [sorted(cy) for cy in pts]


def minimal_systems(systems, n):
    """Pi is minimal above DP iff no proper block system other than the discrete one refines it."""
    out = []
    for P in systems:
        sets = [frozenset(b) for b in P]
        finer = [Q for Q in systems if len(Q) != len(P) and len(Q) < n and len(Q) > len(P)
                 and all(any(set(b) <= s for s in sets) for b in Q)]
        out.append(not finer)
    return out


def analyse_room(name, cells, wall=False):
    t0 = time.process_time()
    kinds = ('interior', 'smooth') if wall else ('interior',)
    pts = [p for p in lattice_points(cells) if status(cells, p) in kinds]
    ostates = 0
    led = ledger(cells, pts[0])
    rows = []
    for S, T in combinations(pts, 2):
        room, t = room_tuple(cells, S)
        n = len(t[0])
        _, LS = points_of(room, t, S, S)
        y_T, LT = points_of(room, t, T, S)
        reach, st9, complete = O9.decide(cells, [S, T], wanted={frozenset((S, T))})
        truth = T in reach[S]
        ostates += st9
        systems = d4.all_block_systems(list(t), n)
        proper = [P for P in systems if 1 < len(P) < n]
        mins = minimal_systems(proper, n)
        cert = None
        if y_T == 0:
            if n <= 15:  # d6 marked_orbit labels every regular a-point; affordable on small n only
                dec, _, _ = decide_pairs(t, LS, LT)
                assert any(x[2] for x in dec) == truth, (name, S, T)
            factors = [U.Factor(t, P) for P in systems]
            cert = []
            for s in LS:
                for q in LT:
                    desc, _, perx, rel = U.analyse_pair(t, factors, s[0], q[0])
                    cert.append(dict(desc=desc, perx={'abcd'[x]: sorted(v) for x, v in perx.items()}))
        certified = bool(cert) and all(c['desc'] for c in cert)
        for P, is_min in zip(proper, mins):
            st = run_pair_factor(t, LS, LT, y_T, P, early=(y_T != 0 and EARLY_MIXED))
            assert st['Qlit'] == truth or st.get('early_stop'), (name, S, T, len(P))
            hyp = st['equal_images'] or st['Nlit']
            if not hyp:
                cls = 'n/a (not lit in N)'
            elif certified:
                cls = 'certified'
            else:
                cls = 'lifts' if st['Qadm'] else 'VIOLATION'
            strong = (st['witness_no_lift'] == 0) if st['Nlit'] and not st.get('early_stop') else None
            rows.append(dict(room=name, S=S, T=T, cls_T='abcd'[y_T], n=n, blocks=len(P), deg=n // len(P),
                             minimal=is_min, truth='lit' if truth else 'dark', certified=certified,
                             cert=cert, **st, hyp=hyp, verdict_weak=cls, strong=strong))
            r = rows[-1]
            print('%-8s S=%-8s T=%-8s %s  N:%2d blk%s  truth=%-4s eq=%-5s Nlit=%-5s Nreg=%-5s'
                  ' wit=%d/%d  WEAK=%-5s STRONG=%-5s cert=%-5s -> %s  (%d states)'
                  % (name, S, T, r['cls_T'], len(P), '*' if is_min else ' ', r['truth'], st['equal_images'],
                     st['Nlit'], st['Nlit_reg'], st['witness_lifts'], st['witnesses'], st['Qadm'], strong,
                     certified, cls, st['states']), flush=True)
    print('== %s: n %d W %d, %d marks, d9 per-pair orbits %d states, CPU %.2f s'
          % (name, len(cells), led['W'], len(pts), ostates, time.process_time() - t0), flush=True)
    return rows


if __name__ == '__main__':
    wall = '--wall' in sys.argv
    EARLY_MIXED = '--early-mixed' in sys.argv
    R22 = [(-1, -1), (-1, 1), (0, 1), (0, 2), (1, 2), (1, 3), (3, 3), (3, 2), (4, 2), (4, 1),
           (5, 1), (5, 0), (3, 0), (3, 1), (1, 1), (1, -1), (2, -1), (2, -3), (1, -3), (1, -2),
           (0, -2), (0, -1)]
    Qp = {(0, 0), (1, 0), (1, 1), (2, 1), (2, 2)}
    P6 = Qp | {(i, -j - 1) for i, j in Qp} | {(5 - i, -j - 1) for i, j in Qp} | {(i, 5 - j) for i, j in Qp}
    rooms = D / 'd41-two-param-cover' / 'rooms'
    named = [('cross12', load(rooms / 'cross12.txt')), ('dumb12', load(rooms / 'dumb12.txt')),
             ('R22', cells_from_vertices(R22)), ('P6', P6)]
    if len(sys.argv) > 1 and sys.argv[-1] in dict(named):
        named = [x for x in named if x[0] == sys.argv[-1]]
    allrows = []
    for name, cells in named:
        allrows += analyse_room(name, cells, wall)
    tag = ('_wall' if wall else '') + ('_' + named[0][0] if len(named) == 1 else '')
    json.dump(allrows, open(HERE / ('fh_star%s.json' % tag), 'w'), indent=1, default=str)
    print('total CPU %.2f s' % time.process_time())
