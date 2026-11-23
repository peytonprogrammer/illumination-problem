"""d63: test the realization lemma (d61 section 5) on NAMED rooms and on their factors.

For a cover M -> B (M = DP of a named room, or M = DP / Pi for a proper block system Pi of
DP, treated as its own pillowcase cover), each choice of corner class a, and each target x:

  B_x(M)   finest block system of M merging every 2-cycle of g_x (d10 R3);
  N_x      M / B_x(M);
  rows     unordered pairs of distinct regular a-points of M with one image in N_x.

Per row the script records
  rig, cut   Theorem U certificates at x over every factor of M (R3 makes Par impossible
             here; asserted);
  lit        ground truth: some state of the pure-braid orbit joins the two points along
             the tail arc a -> x through regular vertices (d61 dp_joined);
  depth      BFS depth of the first witness state.
A COUNTEREXAMPLE is a row with lit = False, rig = False, cut = False.

It also reports, per (M, a, x): deg N_x, block size k, the zero count of N_x, and whether the
x-lit relation is transitive on each N_x-fibre.

Levels whose cover has a pillowcase factor other than B (non-normalized: the L-room) are
run and reported apart, because the lemma is not claimed there.

Run: python3 -B realize.py [room ...]      Writes realize[_rooms].json and prints a log.
"""
import sys, json, time
from collections import deque
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = HERE.parent
sys.path.insert(0, str(D / 'd60-fh-star-test'))
sys.path.insert(0, str(D / 'd61-fold-converse'))
import fh_star as F  # noqa: E402  (sets RLIMIT_CPU 540 s)
from fh_star import pure_move, canon, LABELS, U, d4, cycles, room_tuple, lattice_points, load, \
    cells_from_vertices  # noqa: E402
from fh_tower import quotient  # noqa: E402
from fold_converse import dp_joined  # noqa: E402
from hurwitz import PURE_GENS  # noqa: E402
from roomtools import class_congruence  # noqa: E402


def rooms():
    R22 = [(-1, -1), (-1, 1), (0, 1), (0, 2), (1, 2), (1, 3), (3, 3), (3, 2), (4, 2), (4, 1),
           (5, 1), (5, 0), (3, 0), (3, 1), (1, 1), (1, -1), (2, -1), (2, -3), (1, -3), (1, -2),
           (0, -2), (0, -1)]
    Qp = {(0, 0), (1, 0), (1, 1), (2, 1), (2, 2)}
    P6 = Qp | {(i, -j - 1) for i, j in Qp} | {(5 - i, -j - 1) for i, j in Qp} | {(i, 5 - j) for i, j in Qp}
    f = json.load(open(D / 'd31-run-dark-min' / 'found.json'))[0]
    P6b = {tuple(c) for c in f['cells']}
    L = {(i, j) for i in range(4) for j in range(2)} | {(i, j) for i in range(2) for j in range(2, 4)}
    rd = D / 'd41-two-param-cover' / 'rooms'
    return [('cross12', load(rd / 'cross12.txt')), ('dumb12', load(rd / 'dumb12.txt')),
            ('R22', cells_from_vertices(R22)), ('P6', P6), ('P6found', P6b), ('Lroom', L)]


def orbit_lit(t, A, B, xs):
    """Per x in xs: (lit, BFS depth of the first witness, states walked)."""
    n = len(t[0])
    mk = [0] * n
    for s in A:
        mk[s] = 1
    for s in B:
        mk[s] = 2
    marks = {'a': tuple(mk)}
    where = [0] * n
    roots = lambda m: [s for s in range(n) if m['a'][s] == 1]
    seen = {canon(t, marks, where, roots(marks))}
    queue = deque([(t, marks, 0)])
    found = {}
    states = 0
    while queue:
        t_, m, dep = queue.popleft()
        states += 1
        Si = {s for s in range(n) if m['a'][s] == 1}
        Ti = {s for s in range(n) if m['a'][s] == 2}
        for x in xs:
            if x not in found and dp_joined(t_[0], t_[x], Si, Ti):
                found[x] = dep
        if len(found) == len(xs):
            break
        for (i_, sg) in PURE_GENS:
            t2, m2 = pure_move(t_, LABELS, m, i_, sg)
            c = canon(t2, m2, where, roots(m2))
            if c not in seen:
                seen.add(c)
                queue.append((t2, m2, dep + 1))
    return {x: (x in found, found.get(x)) for x in xs}, states, not queue


def test_level(name, cls, level, t):
    n = len(t[0])
    systems = d4.all_block_systems(list(t), n)
    factors = [U.Factor(t, P) for P in systems]
    proper = [Fc for Fc in factors if 1 < Fc.m < n]
    normalized = not any(U.is_pillowcase(Fc) for Fc in proper)
    reg = [c for c in cycles(t[0]) if len(c) == 2]
    out = []
    per_x = {}
    rowsets = {}
    for x in (1, 2, 3):
        Bx = class_congruence(t, [x])
        Nx = U.Factor(t, Bx)
        k = n // Nx.m
        zeros = sum(1 for y in range(4) for L in Nx.nlen[y] if L == 3)
        assert 2 not in Nx.nlen[x]
        fib = {}
        for c in reg:
            fib.setdefault(Nx.a_point(c[0]), []).append(c)
        per_x[x] = dict(degNx=Nx.m, k=k, zerosNx=zeros, types=[sorted(Nx.nlen[y], reverse=True) for y in range(4)],
                        fibres=sorted(len(v) for v in fib.values()))
        rowsets[x] = [(A, B) for v in fib.values() for A, B in combinations(v, 2)]
    pairs = {}
    for x, rs in rowsets.items():
        for A, B in rs:
            pairs.setdefault((tuple(A), tuple(B)), []).append(x)
    for (A, B), xs in pairs.items():
        verdict, states, complete = orbit_lit(t, A, B, xs)
        for x in xs:
            par = any(U.par(Fc, x, A[0], B[0]) for Fc in proper)
            assert not par, 'R3 violated'
            rig = any(U.rig(Fc, x, A[0], B[0]) for Fc in proper)
            cut = any(U.cut(Fc, t, x, A[0], B[0]) for Fc in proper)
            lit, dep = verdict[x]
            if not lit:
                assert complete
            row = dict(room=name, a=cls, level=level, n=n, normalized=normalized, x='abcd'[x],
                       A=A, B=B, lit=lit, depth=dep, rig=rig, cut=cut, states=states,
                       counterexample=(not lit and not rig and not cut), sound_violation=(lit and (rig or cut)),
                       **per_x[x])
            out.append(row)
    # transitivity of x-lit on each fibre
    trans = {}
    for x in (1, 2, 3):
        lit = {(r['A'], r['B']) for r in out if r['x'] == 'abcd'[x] and r['lit']}
        lit |= {(b, a) for a, b in lit}
        pts = {p for e in lit for p in e}
        bad = 0
        for p in pts:
            for q in pts:
                for s in pts:
                    if p != s and (p, q) in lit and (q, s) in lit and (p, s) not in lit:
                        bad += 1
        trans['abcd'[x]] = bad // 2
    return out, per_x, normalized, trans


def main(names):
    allrows, summary = [], []
    t_all = time.process_time()
    for name, cells in rooms():
        if names and name not in names:
            continue
        t0 = time.process_time()
        pts = lattice_points(cells)
        for cls_off in ((0, 0), (1, 0), (1, 1), (0, 1)):
            origin = next(p for p in pts if ((p[0] - pts[0][0]) % 2, (p[1] - pts[0][1]) % 2) == cls_off)
            room, t = room_tuple(cells, origin)
            n = len(t[0])
            systems = [P for P in d4.all_block_systems(list(t), n) if 1 < len(P) < n]
            levels = [('DP', t)] + [('DP/%d' % len(P), quotient(t, P)[0]) for P in systems]
            for level, tM in levels:
                rows, per_x, normalized, trans = test_level(name, str(cls_off), level, tM)
                allrows += rows
                for x in (1, 2, 3):
                    rx = [r for r in rows if r['x'] == 'abcd'[x]]
                    s = dict(room=name, a=str(cls_off), level=level, n=len(tM[0]), normalized=normalized,
                             x='abcd'[x], rows=len(rx), lit=sum(r['lit'] for r in rx),
                             dark_rig=sum((not r['lit']) and r['rig'] for r in rx),
                             dark_cut=sum((not r['lit']) and r['cut'] and not r['rig'] for r in rx),
                             counterexamples=sum(r['counterexample'] for r in rx),
                             sound_violations=sum(r['sound_violation'] for r in rx),
                             nontransitive=trans['abcd'[x]],
                             max_depth=max([r['depth'] for r in rx if r['lit']] or [None], key=lambda v: -1 if v is None else v),
                             **per_x[x])
                    summary.append(s)
                    print('%-8s a=%s %-7s n=%3d %s x=%s degNx=%2d k=%2d Z(Nx)=%d fibres=%s rows=%3d lit=%3d '
                          'darkRig=%d darkCut=%d CE=%d soundviol=%d nontrans=%d maxdepth=%s'
                          % (name, s['a'], level, s['n'], 'norm' if normalized else 'NONNORM', s['x'],
                             s['degNx'], s['k'], s['zerosNx'], s['fibres'], s['rows'], s['lit'], s['dark_rig'],
                             s['dark_cut'], s['counterexamples'], s['sound_violations'], s['nontransitive'],
                             s['max_depth']), flush=True)
        print('== %s CPU %.2f s' % (name, time.process_time() - t0), flush=True)
    tag = '_' + '_'.join(names) if names else ''
    json.dump(dict(rows=allrows, summary=summary), open(HERE / ('realize%s.json' % tag), 'w'), indent=1,
              default=str)
    print('total CPU %.2f s' % (time.process_time() - t_all))


if __name__ == '__main__':
    main(sys.argv[1:])
