"""Task 2: monodromy and block systems of every other dark room with explicit coordinates.

Rooms: Tokarsky 26 and Castro 24 (vertex lists in the peyton worksheet build.py, read with ast,
not executed), O'Rourke's orthogonal 34-wall Tokarsky room (historical-rigidity34/room.json), and
all 327 parity-census classes (parity-cert-review/inputs). All copied into ./inputs.

Run: python3 -B task2_dark_rooms.py   -> writes task2_dark_rooms.json
"""
import ast
import json
from collections import Counter
from pathlib import Path

from monodromy import Room, analyse_room, tris_from_polygon, squares_from_polygon

HERE = Path(__file__).resolve().parent
INP = HERE / 'inputs'


def build_py_constants():
    tree = ast.parse((INP / 'peyton-worksheet-build.py.txt').read_text())
    out = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if name in ('TOKARSKY26', 'CASTRO24', 'PUBLISHED_ST', 'ROOM22'):
                out[name] = ast.literal_eval(node.value)
    return out


def brief(r):
    """Compact per-room summary."""
    return dict(
        name=r['name'], framework=r['framework'], degree=r['degree'], order=r.get('order'),
        is_symmetric=r.get('is_symmetric'), is_alternating=r.get('is_alternating'), primitive=r['primitive'],
        walls=r['ledger']['walls'], reflex=r['ledger']['reflex'], area=r['ledger']['area'],
        k_transparent=len(r['ledger']['transparent_nonA']), marks=r['marks'],
        mark_lift_angles=r['mark_lift_angles'],
        block_systems=[{k: v for k, v in b.items() if k != 'partition'} for b in r['block_systems']])


def main():
    k = build_py_constants()
    rooms = []
    for name in ('TOKARSKY26', 'CASTRO24'):
        poly = k[name]
        rooms.append(Room(name.lower(), 'tri', tris_from_polygon(poly), k['PUBLISHED_ST'], meta={'vertices': poly}))
    # ROOM22 from build.py: cross-check against the manuscript construction (task 1)
    sq22 = squares_from_polygon(k['ROOM22'])
    h = json.loads((INP / 'historical34-room.json').read_text())
    tris = [tuple(map(tuple, t)) for t in h['triangles']]
    rooms.append(Room('orourke34_tri', 'tri', tris, h['marked']))
    # orthogonal: recover unit squares (pairs of triangles filling a unit square)
    cells = Counter()
    for t in tris:
        xs = [p[0] for p in t]
        ys = [p[1] for p in t]
        cells[(min(xs), min(ys))] += 1
    assert all(v == 2 for v in cells.values()), 'historical 34 room is not orthogonal'
    rooms.append(Room('orourke34_square', 'square', list(cells), h['marked']))

    out = {'room22_from_build_py_squares': sorted(sq22), 'rooms': {}, 'census': {}}
    for room in rooms:
        r = analyse_room(room)
        out['rooms'][room.name] = brief(r)
        print(room.name, 'W', r['ledger']['walls'], 'r', r['ledger']['reflex'], 'k', len(r['ledger']['transparent_nonA']),
              'deg', r['degree'], '|G|', r['order'], 'S_n', r['is_symmetric'], 'A_n', r['is_alternating'],
              'prim', r['primitive'], 'marks', r['mark_lift_angles'])
        for b in r['block_systems']:
            print('   size', b['block_size'], 'blocks', b['blocks'], 'cone', b['cone_angles_over_corner'],
                  'parity', b['parity_property'], 'S!=T', b['phiS_disjoint_phiT'], b.get('kernel_order'))

    # census
    certs = {}
    for line in (INP / 'census' / 'certs-W26.jsonl').read_text().splitlines():
        row = json.loads(line)
        certs[row['tag']] = row
    stats = Counter()
    per = {}
    for f in sorted((INP / 'census').glob('parity-W*.json')):
        d = json.loads(f.read_text())
        assert certs[d['tag']]['lit'] == 0
        room = Room(d['tag'], 'tri', tris_from_polygon(d['vertices']), d['marked'])
        r = analyse_room(room)
        assert r['ledger']['walls'] == len(d['vertices']) and r['transitive']
        b = brief(r)
        per[d['tag']] = b
        proper = [x for x in r['block_systems'] if x['trivial'] == 'proper']
        disc = r['block_systems'][0]
        stats['rooms'] += 1
        stats['k=%d' % b['k_transparent']] += 1
        stats['primitive'] += r['primitive']
        stats['G_is_S_n'] += bool(r['is_symmetric'])
        stats['G_is_A_n'] += bool(r['is_alternating'])
        stats['discrete_factor_parity_and_separates'] += disc['parity_property'] and disc['phiS_disjoint_phiT']
        stats['rooms_with_proper_block_system'] += bool(proper)
        stats['rooms_with_proper_parity_separating_factor'] += any(x['parity_property'] and x['phiS_disjoint_phiT']
                                                                  for x in proper)
        stats['block_size_profile ' + str([x['block_size'] for x in proper])] += 1
    out['census'] = {'stats': dict(sorted(stats.items())), 'rooms': per}
    print(json.dumps(dict(sorted(stats.items())), indent=1))
    (HERE / 'task2_dark_rooms.json').write_text(json.dumps(out, indent=1, default=str) + '\n')


if __name__ == '__main__':
    main()
