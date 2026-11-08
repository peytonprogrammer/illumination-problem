"""Independent, non-search audit of saved peer findings and enumeration mechanics.

No ray generation, ray tracing, origami-orbit generation, or room enumeration.
"""
import ast
import hashlib
import heapq
import importlib.util
import json
import math
import random
import sys
from collections import Counter, deque
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
SNAP = HERE/'peer-fast-inputs'
sys.path.insert(0, str(BASE))
from illumination_geometry import patch, label, local_sectors, owners_of, check
from illumination_transparent_bound import counts


def extracted_functions(path, names, namespace):
    tree = ast.parse(path.read_text())
    tree.body = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
    assert {n.name for n in tree.body} == set(names)
    exec(compile(ast.fix_missing_locations(tree), str(path), 'exec'), namespace)
    return namespace


def reflect_vertex(v, edge):
    a, b = edge
    dx, dy = b[0]-a[0], b[1]-a[1]
    dot = (v[0]-a[0])*dx+(v[1]-a[1])*dy
    length = dx*dx+dy*dy
    p = (a[0]+F(2*dot*dx, length)-(v[0]-a[0]),
         a[1]+F(2*dot*dy, length)-(v[1]-a[1]))
    assert all(x.denominator == 1 for x in p)
    return tuple(map(int, p))


def placements(nmax):
    start = {tri for tri in patch(-1, 1, -1, 1) if (0, 0) in tri}
    assert len(start) == 8
    limit = nmax-15
    dist = {tri: 0 for tri in start}
    queue = deque(start)
    while queue:
        tri = queue.popleft()
        if dist[tri] == limit:
            continue
        for edge in combinations(tri, 2):
            v = next(p for p in tri if p not in edge)
            nxt = tuple(sorted((*edge, reflect_vertex(v, edge))))
            if nxt not in dist:
                dist[nxt] = dist[tri]+1
                queue.append(nxt)
    marks = {next(p for p in tri if label(p)=='A') for tri in dist}
    return sorted(p for p in marks if p != (0, 0) and 0 <= p[1] <= p[0]), len(dist)


def direct_orthogonal_unfold(room):
    """Four orientation sheets of whole unit squares; no peer cover helpers."""
    physical = {tuple(sorted(map(tuple, t))) for t in room['triangles']}
    unit_cells = {(min(p[0] for p in t), min(p[1] for p in t)) for t in physical}
    assert physical == set(patch(min(c[0] for c in unit_cells), max(c[0] for c in unit_cells)+1,
                                 min(c[1] for c in unit_cells), max(c[1] for c in unit_cells)+1)) & physical
    for x, y in unit_cells:
        assert set(patch(x, x+1, y, y+1)) <= physical
    sheets = [(sx, sy) for sx in (1, -1) for sy in (1, -1)]
    squares = [(x, y, sx, sy) for x, y in sorted(unit_cells) for sx, sy in sheets]
    index = {s: i for i, s in enumerate(squares)}
    r, u, tags = [], [], []
    marks = list(map(tuple, room['marked']))
    for x, y, sx, sy in squares:
        next_r = (x+sx, y, sx, sy) if (x+sx, y) in unit_cells else (x, y, -sx, sy)
        next_u = (x, y+sy, sx, sy) if (x, y+sy) in unit_cells else (x, y, sx, -sy)
        r.append(index[next_r]); u.append(index[next_u])
        p = (x if sx == 1 else x+1, y if sy == 1 else y+1)
        incident = {(p[0]+dx, p[1]+dy) for dx in (-1, 0) for dy in (-1, 0)} & unit_cells
        if p == marks[0]:
            assert len(incident) == 4
            tag = 'S'
        elif p == marks[1]:
            assert len(incident) == 4
            tag = 'T'
        elif len(incident) in (1, 3):
            tag = 'B'
        else:
            assert len(incident) in (2, 4)
            tag = '.'
        tags.append(tag)
    assert sorted(r) == sorted(u) == list(range(len(squares)))
    visited = {0}; queue = [0]
    for i in queue:
        for j in (r[i], u[i]):
            if j not in visited:
                visited.add(j); queue.append(j)
    assert len(visited) == len(squares)
    parent = list(range(len(squares)))
    def root(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]; i = parent[i]
        return i
    for i in range(len(squares)):
        parent[root(u[r[i]])] = root(r[u[i]])
    vertex_sizes = Counter(root(i) for i in range(len(squares)))
    return dict(r=r, u=u, label=''.join(tags), square_count=len(squares),
                corner_label_counts=dict(Counter(tags)), vertex_multiplicities=dict(Counter(vertex_sizes.values())),
                genus=1+(len(squares)-len(vertex_sizes))//2)


def local_rule_check():
    total = 0
    for kind, p in [('A', (0, 0)), ('B', (1, 1)), ('C', (1, 0))]:
        tris = [tri for tri in patch(p[0]-1, p[0]+1, p[1]-1, p[1]+1) if p in tri]
        tris.sort(key=lambda t: math.atan2(sum(q[1] for q in t)/3-p[1], sum(q[0] for q in t)/3-p[0]))
        g = dict(ring=[list(range(len(tris)))], role={p: kind}, verts=[p],
                 CORNER={'B': {1, 2, 3, 5, 6, 7}, 'C': {1, 3}},
                 EXCEPT={'B': {4, 8}, 'C': {2, 4}})
        extracted_functions(SNAP/'claude_k_enum_fast.py', ['patterns'], g)
        peer = g['patterns'](0)
        for mask in range(1 << len(tris)):
            selected = [t for i, t in enumerate(tris) if mask >> i & 1]
            own = owners_of(selected)
            sectors, full = local_sectors(selected, p, {e for e, ids in own.items() if len(ids)==2})
            expected = None
            if full or len(sectors) == 1:
                corner = int(not full and sectors != [4])
                exception = int(kind != 'A' and (full or sectors == [4]))
                expected = (corner, exception, int(kind == 'A' and full))
            assert peer.get(mask) == expected, (kind, mask, peer.get(mask), expected)
            total += 1
    return total


def bookkeeping_check():
    n = 8
    g = dict(tid={i: i for i in range(n)}, assign=[-1]*n, rem=[], sat=[0], watch={},
             tot={'n': 0}, tverts=[[] for _ in range(n)])
    extracted_functions(SNAP/'claude_k_enum_fast.py', ['learn', 'set_tile', 'undo'], g)
    randomizer = random.Random(50231)
    trail, stack, clauses = [], [], []
    for step in range(10000):
        free = [i for i, a in enumerate(g['assign']) if a == -1]
        if step%23 == 0:
            requirements = {i: randomizer.randrange(2) for i in range(n) if randomizer.randrange(3)==0}
            g['learn']({i for i,v in requirements.items() if v}, {i for i,v in requirements.items() if not v})
            clauses.append(requirements)
        elif stack and (not free or randomizer.randrange(3)==0):
            g['undo'](trail, stack.pop())
        elif free:
            tile = randomizer.choice(free)
            stack.append(len(trail))
            assert g['set_tile'](tile, randomizer.randrange(2), trail)
        remaining = [sum(g['assign'][i] != v for i,v in req.items()) for req in clauses]
        assert g['rem'] == remaining
        assert g['sat'][0] == sum(count == 0 for count in remaining)
        assert g['tot']['n'] == g['assign'].count(1)
    return dict(transitions=10000, learned_clauses=len(clauses), all_checks_pass=True,
                scope='Exact peer certificate bookkeeping functions with unrelated vertex updates disabled; not an audit of the full undo trail.')


def main():
    result = dict(status='RUNNING', scope='Read-only independent audit; no rays or orbit generation.',
                  snapshot_manifest=json.loads((SNAP/'manifest.json').read_text()))
    room = json.loads((SNAP/'cand-2_2-1.json').read_text())
    result['candidate_geometry'] = check(room, strict=False)
    result['candidate_counts'] = counts(room)
    result['independent_four_sheet_unfolding'] = direct_orthogonal_unfold(room)
    candidates, visited = placements(38)
    peer = json.loads((SNAP/'placements-38.json').read_text())
    assert candidates == list(map(tuple, peer['placements']))
    result['placement_check'] = dict(status='PASS', count=len(candidates), placements=candidates,
        dual_triangles_visited=visited, maximum_dual_distance=23,
        window_coordinate_bound_n38=str(F(2*(38-8)+4, 3)),
        note='Infinite tiling BFS matches saved 20 placements. Independently, every vertex of any <=38-tile room with a full root star has |x|,|y|<=64/3, inside the fast window [-24,24].')
    result['local_patterns_checked'] = local_rule_check()
    result['bookkeeping'] = bookkeeping_check()
    result['saved_room_equivalence'] = []
    for k, w in [(2, 20), (3, 18), (4, 18)]:
        def rooms(name):
            return {tuple(sorted(tuple(sorted(map(tuple, t))) for t in json.loads(line)['triangles']))
                    for line in (SNAP/name).read_text().splitlines() if line.strip()}
        old = rooms(f'val-claude-k{k}-w{w}-rooms.jsonl')
        new = rooms(f'val-claude-k{k}-w{w}-rooms-new.jsonl')
        assert old == new
        result['saved_room_equivalence'].append(dict(k=k, walls=w, identical_rooms=len(old)))
    spec = importlib.util.spec_from_file_location('peer_lit_certs_snapshot', SNAP/'claude_lit_certs.py')
    lit = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(lit)
    try:
        lit.around(F(0), F(1, 1000))
        result['probe_robustness'] = 'No failure at tested point'
    except AssertionError:
        result['probe_robustness'] = dict(status='REPRODUCED_ASSERTION', point=['0','1/1000'],
            impact='Fixed-epsilon probing can fail at a valid rational edge point. This is a completeness/runtime issue, not by itself an unsound emitted certificate.')
    result['cached_certificates'] = []
    for p in sorted(SNAP.glob('certs-*.json')):
        certs = json.loads(p.read_text())
        for used, absent in certs:
            u = {tuple(sorted(map(tuple,t))) for t in used}
            z = {tuple(sorted(map(tuple,t))) for t in absent}
            assert not u & z
        result['cached_certificates'].append(dict(file=p.name, count=len(certs),
            status='DISJOINTNESS_ONLY', limitation='Cached U/Z entries do not contain paths or source hashes; per-entry proof replay requested from peer.'))
    result['darkness_status'] = 'PENDING independent verification of a complete finite closed-orbit certificate'
    result['status'] = 'PARTIAL_AUDIT_PASS_WITH_LIMITATIONS'
    (HERE/'peer-fast-audit.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('snapshot_manifest','independent_four_sheet_unfolding','candidate_geometry')}, indent=2), flush=True)


if __name__ == '__main__':
    main()
