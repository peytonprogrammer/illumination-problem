"""Observation (i): the flagged n = 10 "room" is the five-square staircase stretched by 2.

One fixed polygon, no search.  The script builds the stretched staircase, compares its
cycle types with the flagged census class, runs the exact decider on the two wall marks,
and repeats the darkness check for the un-stretched staircase in its own unit lattice.
"""
from roomtools import *
import unified_test as U

BASE = [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2)]                 # five-square staircase
STRETCHED = {(2 * i + e, j) for (i, j) in BASE for e in (0, 1)}  # x -> 2x
FLAGGED = [[3, 2, 2, 1, 1, 1], [2] * 5, [2] * 5, [3, 3, 1, 1, 1, 1]]


def report(name, cells, marks, origin=(0, 0)):
    assert is_strictly_simple(cells)
    led = ledger(cells, origin)
    room, t = room_tuple(cells, origin)
    types = [cycle_type(g) for g in t]
    xs = sorted({p[0] for p in led['reflex'] + led['convex']})
    ys = sorted({p[1] for p in led['reflex'] + led['convex']})
    print(name, 'area', led['area'], 'W', led['W'], 'types', types)
    print('   vertex x-coordinates', xs, 'vertex y-coordinates', ys)
    print('   corner classes', sorted({((p[0] - origin[0]) % 2, (p[1] - origin[1]) % 2) for p in led['reflex'] + led['convex']}))
    S, T = lifts(room, t, marks[0], origin), lifts(room, t, marks[1], origin)
    print('   marks', marks, [status(cells, m) for m in marks])
    res, states, _ = decide_pairs(t, S, T)
    print('   decider', res, 'states', states)
    factors = [U.Factor(t, part) for part in d4.all_block_systems(list(t), len(t[0]))]
    for s in S:
        for q in T:
            desc, _, perx, rel = U.analyse_pair(t, factors, s[0], q[0])
            print('   certificate:', desc, '| per corner over B:', {('abcd'[x]): sorted(v) for x, v in perx.items()},
                  '| relative:', rel)
    return types


types = report('stretched staircase', STRETCHED, [(2, 0), (6, 2)])
assert types == FLAGGED, types
print('cycle types equal the flagged census class:', types == FLAGGED)
report('unit staircase, class origin (1, 0)', set(BASE), [(1, 0), (3, 2)], origin=(1, 0))
