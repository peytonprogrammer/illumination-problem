"""Per-class congruences B_b, B_c, B_d of the 22-wall room (one saved room, no search)."""
from roomtools import *

R22 = [(-1, -1), (-1, 1), (0, 1), (0, 2), (1, 2), (1, 3), (3, 3), (3, 2), (4, 2), (4, 1), (5, 1), (5, 0),
       (3, 0), (3, 1), (1, 1), (1, -1), (2, -1), (2, -3), (1, -3), (1, -2), (0, -2), (0, -1)]
cells = cells_from_vertices(R22)
assert is_strictly_simple(cells)
led = ledger(cells)
print('ledger', {k: v for k, v in led.items() if k not in ('reflex', 'convex')})
room, t = room_tuple(cells)
print('types', [cycle_type(g) for g in t])
S, T = lifts(room, t, (0, 0)), lifts(room, t, (2, 2))
for name, cl in (('b', [1]), ('c', [2]), ('d', [3]), ('bcd', [1, 2, 3])):
    part = class_congruence(t, cl)
    print('B_%s: %d blocks; induced types %s; S images %s; T images %s' % (
        name, len(part), [cycle_type(induced(g, part)) for g in t],
        [a_image(t, part, s[0]) for s in S], [a_image(t, part, s[0]) for s in T]))
res, states, _ = decide_pairs(t, S, T)
print('decider', res, 'states', states)
