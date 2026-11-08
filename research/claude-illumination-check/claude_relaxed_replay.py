"""Independent relaxed replay of the seven two-exception placements. Uses no Codex code.

Every simple canonical room with <=23 walls, <=2 transparent B/C points, and
interior A marks at (0,0) and 2*target satisfies these necessary conditions:
- tiles lie in the analytic support (claude_ray_guard_check.support);
- each lattice vertex is empty, full, or one contiguous sector;
- a full B/C vertex or a 180-degree B/C sector is a transparent exception (<=2);
- every other nonempty, nonfull vertex is a wall corner (walls = corners <=23);
- the closed tile complex has Euler characteristic V - E + F = 1;
- the marks are full A stars;
- no verified illuminating ray guard holds (soundness: claude_ray_guard_check).

Connectivity, the triangle-count bound, and the counting identity are omitted,
so INFEASIBLE here implies INFEASIBLE for the real family.
"""
import json
import math
import sys
from fractions import Fraction as F
from ortools.sat.python import cp_model
from claude_ray_guard_check import BASE, support, cell_tiles, square_tiles, label

TARGETS = [(1, 1), (2, 0), (2, 1), (3, 0), (2, 2), (3, 1), (4, 0)]
GUARDS = {(1, 1): ['two-global-1-1', 'two-pair-search-1-1'],
          (2, 0): ['two-global-2-0', 'two-pair-search-2-0'],
          (2, 1): ['two-global-2-1', 'two-pair-search-2-1'],
          (2, 2): ['two-global-2-2']}


def incident(v):
    out = set()
    for i in (v[0]-1, v[0]):
        for j in (v[1]-1, v[1]):
            out |= {t for t in square_tiles(i, j) if v in t}
    return out


def angle_units(t, v):
    """Angle of tile t at vertex v in 45-degree units."""
    return 2 if label(v) == 'C' else 1


def around(v, tiles):
    def key(t):
        cx = sum(p[0] for p in t)/3 - v[0]; cy = sum(p[1] for p in t)/3 - v[1]
        return math.atan2(cy, cx)
    return sorted(tiles, key=key)


def vertex_table(v, ring):
    """Allowed (mask..., corner, exception) rows for the cyclic ring of tiles at v."""
    n = len(ring)
    rows = []
    for mask in range(1 << n):
        bits = [mask >> k & 1 for k in range(n)]
        k = sum(bits)
        if k == 0:
            rows.append(bits + [0, 0]); continue
        if k == n:
            rows.append(bits + [0, int(label(v) != 'A')]); continue
        runs = sum(1 for i in range(n) if bits[i] and not bits[i-1])
        if runs != 1:
            continue  # contact or pinch: not a simple boundary
        units = sum(angle_units(ring[i], v) for i in range(n) if bits[i])
        smooth = units == 4
        if smooth:
            rows.append(bits + [0, int(label(v) != 'A')])
        else:
            rows.append(bits + [1, 0])
    return rows


def replay(target, seconds=600, fixed=None, max_walls=23, use_cuts=True, exact_exceptions=None):
    full, mandatory, allowed = support(target)
    ts = sorted({t for c in allowed for t in cell_tiles(*c)})
    index = {t: i for i, t in enumerate(ts)}
    m = cp_model.CpModel()
    x = [m.new_bool_var(f't{i}') for i in range(len(ts))]
    zero = m.new_constant(0)
    def var(t):
        return x[index[t]] if t in index else zero
    for c in full:
        for t in cell_tiles(*c):
            m.add(var(t) == 1)
    verts = sorted({p for t in ts for p in t})
    corners, exceptions, vused = [], [], []
    for v in verts:
        ring = around(v, incident(v))
        corner = m.new_bool_var(''); exc = m.new_bool_var('')
        m.add_allowed_assignments([var(t) for t in ring] + [corner, exc], vertex_table(v, ring))
        corners.append(corner); exceptions.append(exc)
        u = m.new_bool_var('')
        m.add_max_equality(u, [var(t) for t in ring])
        vused.append(u)
    edges = {}
    for t in ts:
        for a in range(3):
            for b in range(a+1, 3):
                edges.setdefault(tuple(sorted((t[a], t[b]))), []).append(t)
    eused = []
    for e, owners in edges.items():
        u = m.new_bool_var('')
        m.add_max_equality(u, [var(t) for t in owners])
        eused.append(u)
    m.add(sum(corners) <= max_walls)
    if fixed is not None:
        for t in ts:
            m.add(var(t) == int(t in fixed))
    m.add(sum(exceptions) <= 2)
    if exact_exceptions is not None:
        m.add(sum(exceptions) == exact_exceptions)
    m.add(sum(vused) - sum(eused) + sum(x) == 1)
    cuts = 0
    for name in (GUARDS.get(target, []) if use_cuts else []):
        data = json.loads((BASE/f'{name}.json').read_text())
        for rec in data['records']:
            for g in rec['derived_guards']:
                m.add_bool_or([x[i].Not() if v else x[i] for i, v in g['tile_facts']])
                cuts += 1
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = seconds
    s.parameters.num_search_workers = 8
    status = s.solve(m)
    out = dict(target=target, support_triangles=len(ts), cuts=cuts, status=s.status_name(status),
               seconds=round(s.wall_time, 1))
    if status in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        out['room'] = [[list(p) for p in t] for t in ts if s.value(x[index[t]])]
        out['walls'] = sum(s.value(c) for c in corners)
        out['exceptions'] = [list(v) for v, e in zip(verts, exceptions) if s.value(e)]
    return out


if __name__ == '__main__':
    which = [tuple(map(int, a.split(','))) for a in sys.argv[1:]] or TARGETS
    results = []
    for tgt in which:
        r = replay(tgt, exact_exceptions=2)
        results.append(r)
        print(json.dumps({k: v for k, v in r.items() if k != 'room'}), flush=True)
    (BASE/'claude-relaxed-replay.json').write_text(json.dumps(results, indent=1)+'\n')
