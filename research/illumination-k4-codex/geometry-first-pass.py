"""First geometry-only feasibility pass on complete k=4 branch supports."""
import hashlib
import importlib.util
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
sys.path.insert(0, str(BASE))
sys.path.insert(0, str(HERE))
from ortools.sat.python import cp_model
from geometry_model import build_model
from illumination_family_bound import NEIGHBORS
spec = importlib.util.spec_from_file_location('codex_local_inventory', HERE/'local-inventory.py')
inventory_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inventory_module)
local_rows = inventory_module.local_rows
physical_inventory = inventory_module.physical_inventory


def bounded(case):
    return {key: set(map(tuple, case[key])) for key in ('full', 'mandatory', 'allowed')}


def solve(model, seconds=10):
    assert not model.validate()
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 4
    solver.parameters.max_time_in_seconds = seconds
    status = solver.solve(model)
    assert status in (cp_model.OPTIMAL, cp_model.FEASIBLE, cp_model.INFEASIBLE, cp_model.UNKNOWN)
    return solver, status


def main():
    start = time.monotonic()
    support_path = HERE/'branch-support.json'
    table_path = HERE/'table.json'
    cases = json.loads(support_path.read_text())['cases']
    inventories = json.loads(table_path.read_text())
    allowed = {(c['I'], c['J'], c['s_N'], c['Q'], c['N'])
               for t in inventories['tables'] if t['k'] == 4 for c in t['cells']
               if c['status'] in ('OPTIMAL', 'FEASIBLE')}
    rows = local_rows()
    result = dict(status='RUNNING', k=4, records=[], controls=[],
                  scope='Per-vertex geometric eligibility, connectivity, Euler and counts on complete supports. No ray guards, orbit runs or darkness claims.',
                  dependencies_sha256={})
    for p in [Path(__file__), HERE/'geometry_model.py', HERE/'branch-support.py', support_path, table_path,
              BASE/'illumination_geometry.py', BASE/'illumination_family_bound.py']:
        result['dependencies_sha256'][str(p.relative_to(BASE))] = hashlib.sha256(p.read_bytes()).hexdigest()

    def save():
        result['seconds'] = time.monotonic()-start
        p = HERE/'geometry-first-pass.json'
        tmp = p.with_suffix('.tmp')
        tmp.write_text(json.dumps(result, indent=2)+'\n')
        tmp.replace(p)

    control = json.loads((BASE/'three-triples/peer-2-0-control.json').read_text())['room']
    selected = {tuple(sorted(map(tuple, t))) for t in control['triangles']}
    full = {(p[0]//2, p[1]//2) for p in control['marked']}
    required = full | {(x+dx, y+dy) for x, y in full for dx, dy in NEIGHBORS}
    cells = {(p[0]//2, p[1]//2) for t in selected for p in t if not p[0]%2 and not p[1]%2}
    m, ts, x, _, _ = build_model((2, 0), 23, 3, dict(full=full, mandatory=required, allowed=cells|required))
    for var, tri in zip(x, ts):
        m.add(var == int(tri in selected))
    solver, status = solve(m)
    assert status in (cp_model.OPTIMAL, cp_model.FEASIBLE)
    result['controls'].append(dict(name='fixed_saved_k3_room', status=solver.status_name(status)))
    save()
    for case in cases:
        b = bounded(case)
        m, ts, x, _, terms = build_model((0, 0), 23, 4, b)
        j = m.new_int_var(0, 4, 'J')
        sn = m.new_int_var(0, 4, 's_N')
        q = m.new_int_var(0, 17, 'Q')
        n = m.new_int_var(1, 37, 'N')
        m.add(j == sum(terms['defects'])-4)
        m.add(sn == 4-j)
        m.add(q == sum(terms['charges']))
        m.add(n == sum(x))
        m.add_allowed_assignments([j, sn, q, n], [values[1:] for values in sorted(allowed) if values[0] == case['I']])
        solver, status = solve(m)
        record = dict(tag=case['tag'], I=case['I'], full=case['full'],
                      status=solver.status_name(status), seconds=solver.wall_time,
                      available_triangles=len(ts))
        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            a, b = case['mark_pairs'][0]
            room = dict(triangles=[t for t, var in zip(ts, x) if solver.value(var)],
                        marked=[[2*a[0], 2*a[1]], [2*b[0], 2*b[1]]], slits=[])
            values, _, geometry = physical_inventory(room, rows)
            assert values in allowed and values[0] == case['I']
            record.update(cell=dict(zip(('I', 'J', 's_N', 'Q', 'N'), values)),
                          walls=geometry['walls'], room=room)
        result['records'].append(record)
        save()
        print(json.dumps({key: value for key, value in record.items() if key != 'room'}), flush=True)
    result['status'] = 'COMPLETE' if all(r['status'] != 'UNKNOWN' for r in result['records']) else 'INCOMPLETE'
    save()


if __name__ == '__main__':
    main()
