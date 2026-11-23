"""Marked valencies for existing D72 pairs; no direction enumeration."""
import json
import sys
from collections import Counter
from pathlib import Path

base = next(Path(__file__).resolve().parents[2].glob('illumination-generalization*/fable/directions*'))
sys.path.insert(0, str(base / 'd72-cylinder-test'))
import cyl


def marked_table(cells, origin):
    room, perms = cyl.PL.room_tuple(cells, origin)
    n = len(cells)
    orbit = {}
    valencies = {}
    for i in range(n):
        for j in range(n):
            key = i, j
            if i == j or key in orbit:
                continue
            queue = [key]
            orbit[key] = key
            size = 0
            while queue:
                a, b = queue.pop()
                size += 1
                for p in perms:
                    z = p[a], p[b]
                    if z not in orbit:
                        orbit[z] = key
                        queue.append(z)
            assert size % n == 0
            valencies[key] = size // n
    assert sum(valencies.values()) == n-1

    def sheets(P):
        coords = tuple(x-y for x, y in zip(P, origin))
        return [i for cycle in room.points_at(coords)[1] for i in cycle]

    def marked(S, T):
        keys = {orbit[i,j] for i in sheets(S) for j in sheets(T)}
        return sum(valencies[key] for key in keys)
    return marked, sorted(valencies.values())


data = json.loads((base / 'd72-cylinder-test/cyl_H40.json').read_text())
rooms = dict(cyl.rooms())
for name, rec in data.items():
    if rec['group'] != 'BBBB':
        continue
    counts = Counter()
    tables = {}
    examples = {}
    for p in rec['pairs']:
        S, T = tuple(p['S']), tuple(p['T'])
        a = tuple(x % 2 for x in S)
        if a not in tables:
            tables[a], degrees = marked_table(rooms[name], S)
        d = tables[a](S, T)
        counts[d] += 1
        examples.setdefault(d,(S,T,p['lit']))
    print(name, rec['n'], degrees, sorted(counts.items()), 'first low:',
          next((ex for d,ex in examples.items() if 3*d < 2*rec['n']), None))
