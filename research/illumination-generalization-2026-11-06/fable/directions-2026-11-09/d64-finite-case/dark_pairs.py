"""d64 step 4: direct darkness test of every same-class interior pair in RL-fin rooms.

Rooms: normalized rooms of covers.json with some class x having 1 < deg N_x < n. For each class
a and each pair S != T of interior a-points, the pair is LIT when some lift pair (S~, T~) is
x-lit for some x in {b, c, d}: some state of the pure-braid orbit with two marks joins them
along the tail arc a -> x (d61 dp_joined, the walk of d63 realize.orbit_lit, stopped at the
first witness for any x). The pair is DARK when all four lift pairs have complete orbits with
no witness. A dark pair here would be a dark room with W <= 20 (target statement).
Usage: python3 -B dark_pairs.py start end out.json
"""
import json
import sys
import time
from collections import deque
from itertools import combinations
from pathlib import Path

import rl_test  # noqa: F401  (path setup, rlimit bypass)
from realize import canon, pure_move, LABELS, PURE_GENS, dp_joined, U, cycles, room_tuple, lattice_points
from roomtools import class_congruence

HERE = Path(__file__).resolve().parent


def lift_pair_lit(t, A, B):
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
    states = 0
    while queue:
        t_, m, dep = queue.popleft()
        states += 1
        Si = {s for s in range(n) if m['a'][s] == 1}
        Ti = {s for s in range(n) if m['a'][s] == 2}
        for x in (1, 2, 3):
            if dp_joined(t_[0], t_[x], Si, Ti):
                return True, x, dep, states
        for (i_, sg) in PURE_GENS:
            t2, m2 = pure_move(t_, LABELS, m, i_, sg)
            c = canon(t2, m2, where, roots(m2))
            if c not in seen:
                seen.add(c)
                queue.append((t2, m2, dep + 1))
    return False, None, None, states


if __name__ == '__main__':
    lo, hi, outp = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    rooms = [r for r in json.load(open(HERE / 'data' / 'covers.json'))['rooms'] if r['normalized']]
    rooms.sort(key=lambda r: (r['n'], r['cells']))
    t0 = time.process_time()
    out = dict(rooms_in_scope=0, rooms_no_rlfin_class=0, pairs=0, lit=0, dark=[], max_states=0, max_depth=0)
    for i in range(lo, min(hi, len(rooms))):
        cells = [tuple(c) for c in rooms[i]['cells']]
        cs = set(cells)
        pts = lattice_points(cells)
        scope = False
        jobs = []
        for off in ((0, 0), (1, 0), (1, 1), (0, 1)):
            origin = next(p for p in pts if ((p[0] - pts[0][0]) % 2, (p[1] - pts[0][1]) % 2) == off)
            room, t = room_tuple(cells, origin)
            n = len(t[0])
            if not scope:
                scope = any(1 < len(class_congruence(t, [x])) < n for x in (1, 2, 3))
            ipts = [p for p in pts if ((p[0] - origin[0]) % 2, (p[1] - origin[1]) % 2) == (0, 0)
                    and sum(c in cs for c in ((p[0] - 1, p[1] - 1), (p[0], p[1] - 1), (p[0] - 1, p[1]), p)) == 4]
            jobs.append((room, t, origin, ipts))
        if not scope:
            out['rooms_no_rlfin_class'] += 1
            continue
        out['rooms_in_scope'] += 1
        for room, t, origin, ipts in jobs:
            for S, T in combinations(ipts, 2):
                out['pairs'] += 1
                LS = room.points_at((S[0] - origin[0], S[1] - origin[1]))[1]
                LT = room.points_at((T[0] - origin[0], T[1] - origin[1]))[1]
                lit = False
                for A in LS:
                    for Bq in LT:
                        ok, x, dep, st = lift_pair_lit(t, tuple(A), tuple(Bq))
                        out['max_states'] = max(out['max_states'], st)
                        if ok:
                            out['max_depth'] = max(out['max_depth'], dep)
                            lit = True
                            break
                    if lit:
                        break
                if lit:
                    out['lit'] += 1
                else:
                    out['dark'].append(dict(room=i, cells=cells, S=S, T=T))
                    print('DARK PAIR room %d S=%s T=%s' % (i, S, T), flush=True)
    out['cpu'] = round(time.process_time() - t0, 1)
    json.dump(out, open(outp, 'w'))
    print('rooms %d..%d in scope %d pairs %d lit %d dark %d max_states %d CPU %.1f' % (
        lo, hi, out['rooms_in_scope'], out['pairs'], out['lit'], len(out['dark']), out['max_states'], out['cpu']))
