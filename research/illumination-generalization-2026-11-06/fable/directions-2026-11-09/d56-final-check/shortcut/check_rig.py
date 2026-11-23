"""d56 shortcut: d48 item 2 steps 2-6 on every room in rooms.json, using d10 roomtools + Factor.

For each room: recompute W and area from cells (roomtools.ledger), strict simplicity.
For each interior pair S, T with T - S not in 2Z^2 (a = [S], t = [T]) and each y not in {a, t}:
R_y = closure of 'merge every cycle of g_y'; N_y = Q / R_y; record (delta, d, z); then for each of
the 4 lift pairs test whether phi(tau) is in the live component of phi(sigma) in the graph of the
basic arc a -> t (edges = sheets of N_y; live rule of d10 Factor = d48 item 2 step 4).
Also checks that R_y is W-invariant (fold.congruence on the merged cycles gives the same partition).
Usage: python3 -B check_rig.py
"""
import json
import resource
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import roomtools as rt                      # noqa: E402
from unified_test import Factor             # noqa: E402
from hurwitz import cycles                  # noqa: E402
import fold                                 # noqa: E402

resource.setrlimit(resource.RLIMIT_CPU, (120, 120))


def reach(F, x, start, target):
    """Is x-point `target` in the live component of a-point `start` (tail arc a -> x)?"""
    if not F.live[0][start] or not F.live[x][target]:
        return False
    adj = {}
    for b in range(F.m):
        u, v = ('a', F.ncid[0][b]), ('x', F.ncid[x][b])
        if F.live[0][u[1]] and F.live[x][v[1]]:
            adj.setdefault(u, set()).add(v)
            adj.setdefault(v, set()).add(u)
    seen, stack = {('a', start)}, [('a', start)]
    while stack:
        u = stack.pop()
        for v in adj.get(u, ()):
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return ('x', target) in seen


def R(t, y):
    n = len(t[0])
    seeds = [(c[k], c[k + 1]) for c in cycles(t[y]) for k in range(len(c) - 1)]
    return rt.closure_partition(n, t, seeds)


def blocks(blk):
    out = {}
    for u, b in enumerate(blk):
        out.setdefault(b, []).append(u)
    return out.values()


def shape(F, n):
    z = sum(l == 3 for y in range(4) for l in F.nlen[y])
    return (n // F.m, F.m, z)


def main():
    rooms = json.load(open(HERE / 'rooms.json'))
    tot = Counter()
    shapes_seen = Counter()
    for ri, R0 in enumerate(rooms):
        cells = set(map(tuple, R0['cells']))
        led = rt.ledger(cells)
        ss = rt.is_strictly_simple(cells)
        print('room %d: area %d, r %d, W %d, strictly simple %s' % (ri, led['area'], led['r'], led['W'], ss))
        # (delta, d, z) and W-invariance of R_y per class, with the origin at a cell corner
        room, t = rt.room_tuple(cells, (0, 0))
        n = len(t[0])
        for y in range(4):
            part = R(t, y)
            F = Factor(t, part)
            print('  y=%s: (delta, d, z) = %s, poles only over y: %s' % (
                'abcd'[y], shape(F, n), all(l == 1 for l in F.nlen[y])))
        # W-invariance of R_y (iota-invariance): in fold's W-set model, closing the g_y-cycle
        # relation under the rotations alone gives the same partition as closing under V0..H1.
        G, _ = fold.from_cells(cells)
        for cls in fold.CLASSES:
            a, b = fold.cg(cls)
            g = [G[a][G[b][u]] for u in range(len(cells))]
            seeds = [(u, g[u]) for u in range(len(cells))]
            same = sorted(map(sorted, blocks(fold.congruence(G, seeds)))) == \
                sorted(map(sorted, blocks(fold.congruence_G(G, seeds))))
            tot['R_y_W_invariant' if same else 'R_y_NOT_W_invariant'] += 1
        interior = [p for p in rt.lattice_points(cells) if rt.status(cells, p) == 'interior']
        for i, S in enumerate(interior):
            for T in interior:
                dx, dy = (T[0] - S[0]) % 2, (T[1] - S[1]) % 2
                if (dx, dy) == (0, 0) or T < S:
                    continue
                room, t = rt.room_tuple(cells, S)
                n = len(t[0])
                x = rt.OFFS[(dx, dy)]
                Sl = rt.lifts(room, t, S, S)
                c, Tl = room.points_at((T[0] - S[0], T[1] - S[1]))
                assert len(Sl) == 2 and len(Tl) == 2
                sep = [[False] * 2 for _ in range(2)]
                for y in (1, 2, 3):
                    if y == x:
                        continue
                    F = Factor(t, R(t, y))
                    assert all(l == 1 for l in F.nlen[y])
                    sh = shape(F, n)
                    tot["lift_pair_tests_with_%d%d%d" % sh] += 4
                    for a_ in range(2):
                        for b_ in range(2):
                            s0 = F.a_point(Sl[a_][0])
                            t0 = F.ncid[x][F.where[Tl[b_][0]]]
                            if not reach(F, x, s0, t0):
                                sep[a_][b_] = True
                                shapes_seen[sh] += 1
                                if sh != (4, 5, 2):
                                    tot['separation_with_other_shape'] += 1
                nsep = sum(map(sum, sep))
                tot['pairs'] += 1
                tot['lift_pairs_separated_%d_of_4' % nsep] += 1
                if nsep == 4:
                    tot['certified'] += 1
                    print('  CERTIFIED pair S=%s T=%s' % (S, T))
    print('separations by (delta, d, z):', dict(shapes_seen))
    print('TOTAL', dict(tot))
    print('CPU s %.2f' % resource.getrusage(resource.RUSAGE_SELF).ru_utime)


main()
