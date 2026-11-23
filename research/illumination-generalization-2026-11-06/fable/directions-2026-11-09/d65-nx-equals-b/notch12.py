"""d65: exact test of the per-class claim on the planar rooms found inside the d14 n = 10
non-transitive orbits (d14_reality.py), built here from their cells, not from the census.

Z12 : 2 x 6 rectangle minus the cells (2,1) and (5,0)  (12 walls, area 10, central symmetry)
S10 : the 10-cell staircase from the third planar orbit.

For each corner class a and target x it reuses d63 realize.test_level (B_x, N_x, the exact
x-lit orbit test, Rig/Cut over proper factors) and adds:
  - the lattice position and status (interior / smooth wall) of each mark;
  - Rig/Cut over every block system including DP itself;
  - the room-level verdict of each pair of distinct lattice points (d9 orbit.decide).
Run: python3 -B notch12.py
"""
import sys, json, time
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = HERE.parent
sys.path.insert(0, str(D / 'd63-realization'))
import realize as RZ                                       # noqa: E402  (imports d60/d61 helpers)
from realize import room_tuple, lattice_points, d4, U, cycles   # noqa: E402
from roomtools import status, is_strictly_simple, ledger   # noqa: E402
import orbit as O9                                         # noqa: E402

Z12 = {(1, 0), (1, 1), (2, 0), (3, 0), (3, 1), (4, 0), (4, 1), (5, 1), (6, 0), (6, 1)}
S10 = {(0, 2), (0, 3), (1, 1), (1, 2), (1, 3), (2, 0), (2, 1), (2, 2), (3, 0), (3, 1)}


def run(name, cells):
    out = []
    print('==', name, 'cells', len(cells), 'strictly simple', is_strictly_simple(cells), 'r', ledger(cells, min(cells))['r'])
    pts = lattice_points(cells)
    for off in ((0, 0), (1, 0), (1, 1), (0, 1)):
        origin = next(p for p in pts if (p[0] % 2, p[1] % 2) == off)
        room, t = room_tuple(cells, origin)
        n = len(t[0])
        where = {}
        for p in pts:
            if (p[0] % 2, p[1] % 2) != off:
                continue
            c, cyc = room.points_at((p[0] - origin[0], p[1] - origin[1]))
            for cy in cyc:
                if len(cy) == 2:
                    where[tuple(sorted(cy))] = (p, status(cells, p))
        rows, per_x, normalized, trans = RZ.test_level(name, str(off), 'DP', t)
        allf = [U.Factor(t, P) for P in d4.all_block_systems(list(t), n)]
        for r in rows:
            A, B = tuple(sorted(r['A'])), tuple(sorted(r['B']))
            pa, pb = where[A], where[B]
            x = 'abcd'.index(r['x'])
            r['rig_all'] = any(U.rig(F, x, A[0], B[0]) for F in allf)
            r['cut_all'] = any(U.cut(F, t, x, A[0], B[0]) for F in allf)
            r['par_all'] = any(U.par(F, x, A[0], B[0]) for F in allf)
            r['pA'], r['pB'] = pa, pb
            r['kind'] = 'interior' if pa[1] == pb[1] == 'interior' else 'wall'
            if not r['lit']:
                print('  a=%s x=%s degNx=%d N_x=%s %s(%s) - %s(%s) x-DARK  rig=%s cut=%s par=%s (all factors)'
                      % (off, r['x'], r['degNx'], 'B' if r['degNx'] == 1 else 'proper', pa[0], pa[1], pb[0], pb[1],
                         r['rig_all'], r['cut_all'], r['par_all']))
            out.append(r)
        for x in 'bcd':
            rx = [r for r in rows if r['x'] == x]
            print('  a=%s x=%s degNx=%s rows=%d (interior %d) lit=%d dark=%d uncertified dark=%d (interior %d) nontransitive=%d'
                  % (off, x, rx[0]['degNx'] if rx else '-', len(rx), sum(r['kind'] == 'interior' for r in rx),
                     sum(r['lit'] for r in rx), sum(not r['lit'] for r in rx),
                     sum(not r['lit'] and not (r['rig_all'] or r['cut_all'] or r['par_all']) for r in rx),
                     sum(not r['lit'] and not (r['rig_all'] or r['cut_all'] or r['par_all']) and r['kind'] == 'interior' for r in rx),
                     trans[x]))
    # room-level verdicts for every pair of regular lattice points (interior and smooth wall)
    reg = [p for p in pts if status(cells, p) in ('interior', 'smooth')]
    reach, st, complete = O9.decide(cells, reg)
    dark = [(S, T) for S, T in combinations(reg, 2) if T not in reach[S]]
    print('  room level: %d regular lattice points, dark pairs %s, states %d complete %s' % (len(reg), dark, st, complete))
    return out, dict(room=name, room_dark_pairs=dark, complete=complete)


def main():
    t0 = time.process_time()
    rows, rl = [], []
    for name, cells in (('Z12', Z12), ('S10', S10)):
        r, s = run(name, cells)
        rows += r
        rl.append(s)
    json.dump(dict(rows=rows, room_level=rl), open(HERE / 'notch12.json', 'w'), indent=1, default=str)
    print('CPU %.2f s' % (time.process_time() - t0))


if __name__ == '__main__':
    main()
