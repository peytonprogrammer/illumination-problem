"""d64 step 3: RL-fin test on every normalized room of covers.json.

For each room, each corner class a (origin = a lattice point of that class), and each target x
with 1 < deg N_x < n (N_x = DP / B_x, B_x from d10 class_congruence), the rows are the unordered
pairs of distinct regular a-points of DP (2-cycles of g_a: lifts of interior points and smooth
wall points) with one image in N_x. Per row:
  lit      d63 realize.orbit_lit (pure-braid orbit with two marks, d61 dp_joined), unchanged;
  rigRy    Rig(x) over DP / R_y for both y outside {a, x}           (d62 G3 quantifier);
  rig,cut  Rig(x), Cut(x) over every proper factor (d10 Theorem U)  (computed for dark rows);
  par      asserted absent on every proper factor for dark rows (R3).
COUNTEREXAMPLE: lit False, and no Rig (R_y or any factor) and no Cut.
Soundness: a lit row with rigRy True is a violation (Theorem U).
Usage: python3 -B rl_test.py start end out.json [max_states]
"""
import json
import resource
import sys
import time
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = HERE.parent
_set = resource.setrlimit
resource.setrlimit = lambda *a, **k: None          # fh_star caps CPU at 540 s on import
sys.path.insert(0, str(D / 'd63-realization'))
import realize as RZ  # noqa: E402
resource.setrlimit = _set
from realize import orbit_lit, U, d4, cycles, room_tuple, lattice_points  # noqa: E402
from roomtools import class_congruence, closure_partition, status  # noqa: E402

resource.setrlimit(resource.RLIMIT_CPU, (4000, 4000))


def R_y(t, y):
    n = len(t[0])
    seeds = [(c[i], c[i + 1]) for c in cycles(t[y]) for i in range(len(c) - 1)]
    return closure_partition(n, t, seeds)


def point_map(room, cells, origin):
    """2-cycle of g_a (frozenset of sheets) -> (lattice point, 'interior' | 'smooth')."""
    out = {}
    for p in lattice_points(cells):
        if ((p[0] - origin[0]) % 2, (p[1] - origin[1]) % 2) != (0, 0):
            continue
        s = status(cells, p)
        if s not in ('interior', 'smooth'):
            continue
        c, pts = room.points_at((p[0] - origin[0], p[1] - origin[1]))
        for cy in pts:
            out[frozenset(cy)] = (p, s)
    return out


def test_room(idx, cells, max_states):
    rows, summ = [], []
    pts = lattice_points(cells)
    for off in ((0, 0), (1, 0), (1, 1), (0, 1)):
        origin = next(p for p in pts if ((p[0] - pts[0][0]) % 2, (p[1] - pts[0][1]) % 2) == off)
        room, t = room_tuple(cells, origin)
        n = len(t[0])
        reg = [tuple(c) for c in cycles(t[0]) if len(c) == 2]
        pm = point_map(room, set(cells), origin)
        assert set(map(frozenset, reg)) == set(pm), 'regular a-points mismatch'
        rowsets = {}
        for x in (1, 2, 3):
            Nx = U.Factor(t, class_congruence(t, [x]))
            if not (1 < Nx.m < n):
                continue
            assert 2 not in Nx.nlen[x]
            zeros = sum(1 for y in range(4) for L in Nx.nlen[y] if L == 3)
            fib = {}
            for c in reg:
                fib.setdefault(Nx.a_point(c[0]), []).append(c)
            rs = [(A, B) for v in fib.values() for A, B in combinations(v, 2)]
            rowsets[x] = rs
            summ.append(dict(room=idx, a=off, x='abcd'[x], n=n, degNx=Nx.m, k=n // Nx.m, zerosNx=zeros,
                             rows=len(rs)))
        if not rowsets:
            continue
        Ry = {y: U.Factor(t, R_y(t, y)) for y in (1, 2, 3)}
        pairs = {}
        for x, rs in rowsets.items():
            for A, B in rs:
                pairs.setdefault((A, B), []).append(x)
        facs = None
        for (A, B), xs in pairs.items():
            verdict, states, complete = orbit_lit_capped(t, A, B, xs, max_states)
            for x in xs:
                lit, dep = verdict[x]
                rigRy = any(Ry[y].m < n and U.rig(Ry[y], x, A[0], B[0]) for y in (1, 2, 3) if y != x)
                row = dict(room=idx, a=off, x='abcd'[x], n=n, A=list(A), B=list(B),
                           pA=list(pm[frozenset(A)][0]), sA=pm[frozenset(A)][1],
                           pB=list(pm[frozenset(B)][0]), sB=pm[frozenset(B)][1],
                           lit=lit, depth=dep, states=states, complete=complete, rigRy=rigRy)
                if not lit:
                    if facs is None:
                        systems = d4.all_block_systems(list(t), n)
                        facs = [U.Factor(t, P) for P in systems if 1 < len(P) < n]
                    assert not any(U.par(F, x, A[0], B[0]) for F in facs), 'R3 violated'
                    row['rig'] = any(U.rig(F, x, A[0], B[0]) for F in facs)
                    row['cut'] = any(U.cut(F, t, x, A[0], B[0]) for F in facs)
                    row['counterexample'] = complete and not (rigRy or row['rig'] or row['cut'])
                    row['unresolved'] = not complete
                rows.append(row)
    return rows, summ


def orbit_lit_capped(t, A, B, xs, max_states):
    if max_states is None:
        verdict, states, done = orbit_lit(t, A, B, xs)
        return verdict, states, True
    # same walk as realize.orbit_lit with a state cap
    from collections import deque
    from realize import canon, pure_move, LABELS, PURE_GENS, dp_joined
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
    while queue and states < max_states:
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
    complete = len(found) == len(xs) or not queue
    return {x: (x in found, found.get(x)) for x in xs}, states, complete


if __name__ == '__main__':
    lo, hi, outp = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    max_states = int(sys.argv[4]) if len(sys.argv) > 4 else None
    rooms = [r for r in json.load(open(HERE / 'data' / 'covers.json'))['rooms'] if r['normalized']]
    rooms.sort(key=lambda r: (r['n'], r['cells']))
    t0 = time.process_time()
    allrows, allsum = [], []
    for i in range(lo, min(hi, len(rooms))):
        cells = [tuple(c) for c in rooms[i]['cells']]
        t1 = time.process_time()
        rows, summ = test_room(i, cells, max_states)
        allrows += rows
        allsum += summ
        dark = [r for r in rows if not r['lit']]
        ce = sum(r.get('counterexample', False) for r in rows)
        un = sum(r.get('unresolved', False) for r in rows)
        if dark or time.process_time() - t1 > 5:
            print('room %d n=%d rows=%d dark=%d CE=%d unresolved=%d cpu=%.1f' % (
                i, len(cells), len(rows), len(dark), ce, un, time.process_time() - t1), flush=True)
    keep = [r for r in allrows if not r['lit'] or r['rigRy']]
    json.dump(dict(range=[lo, hi], nrows=len(allrows), nlit=sum(r['lit'] for r in allrows),
                   lit_interior_pairs=sum(r['lit'] and r['sA'] == r['sB'] == 'interior' for r in allrows),
                   rows_interior=sum(r['sA'] == r['sB'] == 'interior' for r in allrows),
                   max_states=max([r['states'] for r in allrows] or [0]),
                   max_depth=max([r['depth'] for r in allrows if r['lit']] or [0]),
                   special_rows=keep, summary=allsum), open(outp, 'w'), default=str)
    print('rooms %d..%d rows %d lit %d dark %d CE %d unresolved %d soundviol %d CPU %.1f' % (
        lo, hi, len(allrows), sum(r['lit'] for r in allrows), sum(not r['lit'] for r in allrows),
        sum(r.get('counterexample', False) for r in allrows), sum(r.get('unresolved', False) for r in allrows),
        sum(r['lit'] and r['rigRy'] for r in allrows), time.process_time() - t0), flush=True)
