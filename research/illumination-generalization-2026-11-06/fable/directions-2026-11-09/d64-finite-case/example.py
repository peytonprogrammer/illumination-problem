"""d64: full data for one counterexample row. Usage: python3 -B example.py room_index"""
import json
import sys
import rl_test
from rl_test import U, d4, cycles, room_tuple, lattice_points, R_y
from roomtools import class_congruence, status
from dark_pairs import lift_pair_lit

idx = int(sys.argv[1])
rooms = [r for r in json.load(open('data/covers.json'))['rooms'] if r['normalized']]
rooms.sort(key=lambda r: (r['n'], r['cells']))
cells = [tuple(c) for c in rooms[idx]['cells']]
cs = set(cells)
r = sum(1 for p in lattice_points(cells) if status(cs, p) == 'reflex')
print('room', idx, 'n =', len(cells), 'r =', r, 'W =', 2 * r + 4, 'cells', cells)
rows, summ = rl_test.test_room(idx, cells, None)
for row in rows:
    if row['lit'] or row['pA'] == row['pB'] or row['sA'] != 'interior' or row['sB'] != 'interior':
        continue
    off = row['a']
    pts = lattice_points(cells)
    origin = next(p for p in pts if ((p[0] - pts[0][0]) % 2, (p[1] - pts[0][1]) % 2) == off)
    room, t = room_tuple(cells, origin)
    x = 'abcd'.index(row['x'])
    print('\nrow: a-class origin', origin, 'x =', row['x'], 'S =', row['pA'], 'T =', row['pB'],
          'lifts', row['A'], row['B'], 'orbit states', row['states'])
    print(' cycle types g_a,g_b,g_c,g_d:', [sorted((len(c) for c in cycles(g)), reverse=True) for g in t])
    Bx = class_congruence(t, [x])
    Nx = U.Factor(t, Bx)
    print(' N_x: degree', Nx.m, 'cycle types', [sorted(L, reverse=True) for L in Nx.nlen], 'blocks', Bx)
    for y in (1, 2, 3):
        if y == x:
            continue
        F = U.Factor(t, R_y(t, y))
        print(' R_%s: %d blocks, identity at %s: %s, rig: %s' % ('abcd'[y], F.m, 'abcd'[y],
              all(L == 1 for L in F.nlen[y]), U.rig(F, x, row['A'][0], row['B'][0])))
    systems = [P for P in d4.all_block_systems(list(t), len(t[0])) if 1 < len(P) < len(t[0])]
    print(' proper block systems:', [len(P) for P in systems])
    for P in systems:
        F = U.Factor(t, P)
        if F.m <= 3:
            same = F.a_point(row['A'][0]) == F.a_point(row['B'][0])
            regs = all(F.nlen[y][F.ncid[y][F.where[c[0]]]] == 2 for y in (0, x) for c in cycles(t[y]) if len(c) == 2)
            single = [('abcd'[y], len(F.nlen[y]) == 1) for y in (1, 2, 3) if y != x]
            print('  factor deg %d: equal a-image %s, all regular a/x points stay regular %s, single cycle %s -> cut %s'
                  % (F.m, same, regs, single, U.cut(F, t, x, row['A'][0], row['B'][0])))
    # the point pair is lit through another target or another lift pair
    S, T = tuple(row['pA']), tuple(row['pB'])
    LS = room.points_at((S[0] - origin[0], S[1] - origin[1]))[1]
    LT = room.points_at((T[0] - origin[0], T[1] - origin[1]))[1]
    for A in LS:
        for B in LT:
            print('  lift pair', A, B, '-> lit (x, depth):', lift_pair_lit(t, tuple(A), tuple(B))[:3])
