"""d65: per-lift-pair versus room-pair form of the N_x = B claim, on named rooms.

Rooms: cross12, dumb12, R22, P6, P6found, Lroom (d63 list, Lroom non-normalized) and the
two rooms realizing d14 relations, Z12 and S10.  For every corner class a and target x with
N_x = B (B_x one block) it takes every pair of distinct regular a-points of DP (d63
realize.test_level: exact orbit verdict, Par/Rig/Cut), adds Par/Rig/Cut over every block
system including DP, and reports:

  RL-B (lift pairs) : x-dark lift pairs without a certificate;
  RL-room           : room pairs {S, T}, S != T lattice points, all of whose lift pairs are
                      x-dark, and at least one lift pair has no certificate;
  deck test         : for each uncertified x-dark lift pair, whether a deck involution delta
                      of DP -> B maps one mark to the other, and over which corner classes
                      delta has fixed points.
Run: python3 -B rl_room.py
"""
import sys, json, time
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import notch12 as NZ                                       # noqa: E402
from notch12 import RZ, room_tuple, lattice_points, d4, U, cycles, status   # noqa: E402


def centraliser(t):
    n = len(t[0])
    out = []
    for v in range(n):
        phi = [-1] * n
        phi[0] = v
        q, ok = [0], True
        for x in q:
            for g in t:
                y, fy = g[x], g[phi[x]]
                if phi[y] < 0:
                    phi[y] = fy
                    q.append(y)
                elif phi[y] != fy:
                    ok = False
                    break
            if not ok:
                break
        if ok and sorted(phi) == list(range(n)):
            out.append(tuple(phi))
    return out


def fixed_classes(t, dl):
    out = set()
    for y in range(4):
        for c in cycles(t[y]):
            if sorted(dl[s] for s in c) == sorted(c):
                out.add('abcd'[y])
    return sorted(out)


def main():
    t0 = time.process_time()
    # T8, Z8, R24: planar rooms of the n = 8 non-transitive census relations (d14_reality --all)
    T8 = {(0, 0), (1, 0), (2, 0), (2, 1), (3, 0), (3, 1), (4, 0), (5, 0)}
    Z8 = {(0, 0), (1, 0), (2, 0), (2, 1), (3, 0), (3, 1), (4, 1), (5, 1)}
    R24 = {(i, j) for i in range(4) for j in range(2)}
    rooms = [r for r in RZ.rooms()] + [('Z12', NZ.Z12), ('S10', NZ.S10), ('T8', T8), ('Z8', Z8), ('R24', R24)]
    summary, detail = [], []
    for name, cells in rooms:
        pts = lattice_points(cells)
        tot = defaultdict(int)
        for off in ((0, 0), (1, 0), (1, 1), (0, 1)):
            origin = next(p for p in pts if (p[0] % 2, p[1] % 2) == off)
            room, t = room_tuple(cells, origin)
            n = len(t[0])
            cen = centraliser(t)
            invs = [c for c in cen if c != tuple(range(n)) and all(c[c[i]] == i for i in range(n))]
            for dl in invs:     # Lemma M: exactly two fixed points over corners, both regular
                fp = [len(c) for y in range(4) for c in cycles(t[y]) if sorted(dl[s] for s in c) == sorted(c)]
                assert fp == [2, 2], (name, off, fp)
                tot['deck involutions checked (2 regular fixed points)'] += 1
            where = {}
            for p in pts:
                if (p[0] % 2, p[1] % 2) != off:
                    continue
                _, cyc = room.points_at((p[0] - origin[0], p[1] - origin[1]))
                for cy in cyc:
                    if len(cy) == 2:
                        where[tuple(sorted(cy))] = (p, status(cells, p))
            rows, per_x, normalized, trans = RZ.test_level(name, str(off), 'DP', t)
            tot['normalized' if normalized else 'NOT normalized'] = 1
            allf = [U.Factor(t, P) for P in d4.all_block_systems(list(t), n)]
            groups = defaultdict(list)
            for r in rows:
                if r['degNx'] != 1:
                    continue
                A, B = tuple(sorted(r['A'])), tuple(sorted(r['B']))
                x = 'abcd'.index(r['x'])
                cert = any(f(F, x, A[0], B[0]) for F in allf for f in (U.rig, U.par)) or \
                    any(U.cut(F, t, x, A[0], B[0]) for F in allf)
                pa, pb = where[A], where[B]
                kind = 'interior' if pa[1] == pb[1] == 'interior' else 'wall'
                tot['lift rows N_x=B'] += 1
                if not r['lit'] and not cert:
                    dls = [dl for dl in invs if {dl[s] for s in A} == set(B)]
                    fc = [fixed_classes(t, dl) for dl in dls]
                    expl = any(r['x'] not in f and 'a' not in f for f in fc)
                    tot['uncertified dark lift pairs (%s, %s)' % (kind, 'same point' if pa[0] == pb[0] else 'distinct points')] += 1
                    tot['  of these, delta-pair with no delta-fixed point over a or x: %s' % expl] += 1
                    detail.append(dict(room=name, a=str(off), x=r['x'], A=pa, B=pb, delta_fixed_classes=fc,
                                       explained=expl, normalized=normalized))
                if pa[0] != pb[0]:
                    key = (r['x'], tuple(sorted((pa[0], pb[0]))))
                    groups[key].append((r['lit'], cert, kind))
            for (x, pq), g in groups.items():
                kind = g[0][2]
                tot['room pairs N_x=B (%s)' % kind] += 1
                if not any(l for l, c, k in g):
                    tot['room pairs x-dark (%s)' % kind] += 1
                    if not all(c for l, c, k in g):
                        tot['room pairs x-dark, uncertified (%s)' % kind] += 1
                        detail.append(dict(room=name, a=str(off), x=x, room_pair=pq, kind=kind, normalized=normalized,
                                           lift_pairs=[(l, c) for l, c, k in g]))
            tot['deck group order (a=%s)' % (off,)] = len(cen)
        summary.append(dict(room=name, **tot))
        print(name, dict(tot), flush=True)
    for d in detail:
        print('  ', d)
    json.dump(dict(summary=summary, detail=detail), open(HERE / 'rl_room.json', 'w'), indent=1, default=str)
    print('CPU %.2f s' % (time.process_time() - t0))


if __name__ == '__main__':
    main()
