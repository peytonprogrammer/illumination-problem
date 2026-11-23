"""d44 validation: named rooms through check_rooms (C) and roomtools (Python).

Rooms: 22-wall room (r = 9, area 15), P6 (r = 12, area 20), the 12-wall cross and
the cross scaled by 2 and 3.  For each room and each mark class with >= 2 interior
points, compares the B_b, B_c, B_d block counts from both implementations, then
prints check_rooms' positives.  No ray or direction search.
"""
import subprocess, sys, resource
from pathlib import Path
resource.setrlimit(resource.RLIMIT_CPU, (60, 60))
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'd10-mechanisms'))
from roomtools import cells_from_vertices, room_tuple, class_congruence, ledger, status  # noqa

R22 = [(-1, -1), (-1, 1), (0, 1), (0, 2), (1, 2), (1, 3), (3, 3), (3, 2), (4, 2), (4, 1), (5, 1),
       (5, 0), (3, 0), (3, 1), (1, 1), (1, -1), (2, -1), (2, -3), (1, -3), (1, -2), (0, -2), (0, -1)]
Q = {(0, 0), (1, 0), (1, 1), (2, 1), (2, 2)}
P6 = Q | {(i, -j - 1) for i, j in Q} | {(5 - i, -j - 1) for i, j in Q} | {(i, 5 - j) for i, j in Q}
cross = {(i, j) for i in range(4) for j in range(1, 3)} | {(i, j) for i in range(1, 3) for j in range(4)}
def scale(c, k):
    return {(k * i + u, k * j + v) for (i, j) in c for u in range(k) for v in range(k)}
rooms = [('22-wall', cells_from_vertices(R22)), ('P6', P6), ('cross', cross),
         ('cross x2', scale(cross, 2)), ('cross x3', scale(cross, 3))]

lines = []
for name, cells in rooms:
    lines.append(' '.join([str(len(cells))] + ['%d %d' % c for c in sorted(cells)]))
    led = ledger(cells, (0, 0))
    pts = {p for c in cells for p in [(c[0], c[1]), (c[0] + 1, c[1]), (c[0], c[1] + 1), (c[0] + 1, c[1] + 1)]}
    interior = [p for p in pts if status(cells, p) == 'interior']
    print('==', name, 'area', len(cells), 'r', led['r'], 'W', led['W'])
    for ox in (0, 1):
        for oy in (0, 1):
            marks = [p for p in interior if (p[0] - ox) % 2 == 0 and (p[1] - oy) % 2 == 0]
            if len(marks) < 2:
                continue
            _, t = room_tuple(cells, (ox, oy))
            nb = [len(class_congruence(t, [x])) for x in (1, 2, 3)]
            print('  roomtools origin parity (%d,%d) marks %d blocks b c d = %s' % (ox, oy, len(marks), nb))
out = subprocess.run([str(HERE / 'check_rooms'), 'v'], input='\n'.join(lines) + '\n',
                     capture_output=True, text=True)
print(out.stdout, end='')
print(out.stderr, end='')
