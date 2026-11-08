"""Positive-only compact geometry witnesses for unresolved k=4 placements."""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
spec = importlib.util.spec_from_file_location('first_pass', HERE/'geometry-first-pass.py')
first = importlib.util.module_from_spec(spec)
spec.loader.exec_module(first)
from geometry_model import build_model
from illumination_family_bound import NEIGHBORS
from ortools.sat.python import cp_model


def outside_candidates(case):
    full = set(map(tuple, case['full']))
    source, target = sorted(full)
    required = set(map(tuple, case['mandatory']))
    allowed = set(map(tuple, case['allowed']))
    cap = 17-case['b']
    found = set()
    def visit(path, cost, outside):
        current = path[-1]
        if current == target:
            found.add(tuple(sorted(outside)))
            return
        for dx, dy in NEIGHBORS:
            nxt = current[0]+dx, current[1]+dy
            if nxt not in allowed or nxt in path:
                continue
            new_out = outside | ({nxt} if nxt not in required else set())
            if len(new_out) > case['outside_cell_cap']:
                continue
            extra = 0
            if len(path) > 1:
                previous = path[-2]
                straight = (current[0]-previous[0], current[1]-previous[1]) == (dx, dy)
                extra = 2+int(straight)-int(current in required)
            if cost+extra <= cap:
                visit(path+(nxt,), cost+extra, new_out)
    visit((source,), 0, set())
    return sorted(found, key=lambda cells: (len(cells), cells))


def main():
    supports = json.loads((HERE/'branch-support.json').read_text())['cases']
    prior = {r['tag']: r for r in json.loads((HERE/'geometry-first-pass.json').read_text())['records']}
    path_bounds = {r['tag']: r for r in json.loads((HERE/'cell-path.json').read_text())['records']}
    table = json.loads((HERE/'table.json').read_text())
    cells = {(c['I'], c['J'], c['s_N'], c['Q'], c['N']) for t in table['tables'] if t['k'] == 4
             for c in t['cells'] if c['status'] in ('OPTIMAL', 'FEASIBLE')}
    rows = first.local_rows()
    result = dict(status='RUNNING', scope='Positive geometry witness search only; failed restricted supports do not exclude a full case. No rays.', records=[], dependencies_sha256={})
    for p in [Path(__file__), HERE/'geometry_model.py', HERE/'branch-support.json', HERE/'cell-path.json', HERE/'table.json']:
        result['dependencies_sha256'][p.name] = hashlib.sha256(p.read_bytes()).hexdigest()
    for case in supports:
        if case['I'] != 2 or prior[case['tag']]['status'] != 'UNKNOWN' or path_bounds[case['tag']]['wall_lower'] > 23:
            continue
        candidates = outside_candidates(case)
        row = dict(tag=case['tag'], candidate_supports=len(candidates), attempted=0, status='OPEN')
        for outside in candidates:
            b = first.bounded(case)
            b['allowed'] = b['mandatory'] | set(outside)
            m, ts, x, _, terms = build_model((0, 0), 23, 4, b)
            m.add(sum(x) <= 37)
            solver = cp_model.CpSolver()
            solver.parameters.num_search_workers = 1
            solver.parameters.max_time_in_seconds = 2
            status = solver.solve(m)
            row['attempted'] += 1
            if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                a, b = case['mark_pairs'][0]
                room = dict(triangles=[t for t, var in zip(ts, x) if solver.value(var)],
                            marked=[[2*a[0], 2*a[1]], [2*b[0], 2*b[1]]], slits=[])
                values, _, geometry = first.physical_inventory(room, rows)
                assert values in cells and values[0] == 2
                row.update(status='FEASIBLE', outside_cells=outside, cell=dict(zip(('I', 'J', 's_N', 'Q', 'N'), values)),
                           walls=geometry['walls'], room=room)
                break
            if row['attempted'] >= 100:
                break
        result['records'].append(row)
        (HERE/'geometry-local-witness.json').write_text(json.dumps(result, indent=2)+'\n')
        print(json.dumps({k: v for k, v in row.items() if k != 'room'}), flush=True)
    result['status'] = 'COMPLETE_POSITIVE_CHECKS'
    (HERE/'geometry-local-witness.json').write_text(json.dumps(result, indent=2)+'\n')


if __name__ == '__main__':
    main()
