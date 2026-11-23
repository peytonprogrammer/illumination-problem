"""Cross-check: the Jordan-theorem shortcut in group_order agrees with plain Schreier-Sims.

Runs both methods on Tokarsky 26, Castro 24, the 34-wall room, all 327 census rooms, and the
31 orthogonal k7 lit rooms (both frameworks). Run: python3 -B check_orders.py (about 3 minutes).
"""
import ast
import json
from pathlib import Path

from monodromy import Room, all_block_systems, group_order, schreier_sims, tris_from_polygon, squares_from_polygon

HERE = Path(__file__).resolve().parent
INP = HERE / 'inputs'


def rooms():
    tree = ast.parse((INP / 'peyton-worksheet-build.py.txt').read_text())
    k = {n.targets[0].id: ast.literal_eval(n.value) for n in tree.body
         if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name)
         and n.targets[0].id in ('TOKARSKY26', 'CASTRO24', 'PUBLISHED_ST')}
    for name in ('TOKARSKY26', 'CASTRO24'):
        yield Room(name, 'tri', tris_from_polygon(k[name]), k['PUBLISHED_ST'])
    h = json.loads((INP / 'historical34-room.json').read_text())
    yield Room('orourke34', 'tri', [tuple(map(tuple, t)) for t in h['triangles']], h['marked'])
    for f in sorted((INP / 'census').glob('parity-W*.json')):
        d = json.loads(f.read_text())
        yield Room(d['tag'], 'tri', tris_from_polygon(d['vertices']), d['marked'])
    for f in sorted((INP / 'k7-models').glob('model-*.json')):
        d = json.loads(f.read_text())
        cells = [tuple(c) for c in d['cells']]
        yield Room(f.stem, 'square', cells, d['marks'])
        yield Room(f.stem + '_tri', 'tri', [tuple(map(tuple, t)) for t in d['triangles']], d['marks'])


def main():
    count = jordan = 0
    for room in rooms():
        gens = room.gens_list()
        prim = len(all_block_systems(gens, room.degree)) == 2
        o1, method = group_order(gens, room.degree, prim)
        o2 = schreier_sims(gens, room.degree)[2]
        assert o1 == o2, (room.name, o1, o2)
        count += 1
        jordan += method == 'jordan'
    print(json.dumps({'rooms_checked': count, 'jordan_shortcut_used': jordan, 'all_agree': True}))


if __name__ == '__main__':
    main()
