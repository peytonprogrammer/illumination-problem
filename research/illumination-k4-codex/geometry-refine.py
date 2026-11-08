"""Refine unresolved geometry supports using cell charges and flow, no rays."""
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
spec = importlib.util.spec_from_file_location('first_pass', HERE/'geometry-first-pass.py')
first = importlib.util.module_from_spec(spec)
spec.loader.exec_module(first)
from geometry_model import build_model
from illumination_geometry import owners_of
from ortools.sat.python import cp_model


def main():
    start = time.monotonic()
    original = json.loads((HERE/'geometry-first-pass.json').read_text())
    supports = {c['tag']: c for c in json.loads((HERE/'branch-support.json').read_text())['cases']}
    paths = {c['tag']: c for c in json.loads((HERE/'cell-path.json').read_text())['records']}
    rows = first.local_rows()
    table = json.loads((HERE/'table.json').read_text())
    allowed = {(c['I'], c['J'], c['s_N'], c['Q'], c['N'])
               for t in table['tables'] if t['k'] == 4 for c in t['cells'] if c['status'] in ('OPTIMAL', 'FEASIBLE')}
    result = dict(status='RUNNING', records=[], positive_charge_controls=0,
                  scope='Complete k=4 geometry supports; no ray guards or darkness claims.', dependencies_sha256={})
    for p in [Path(__file__), HERE/'geometry-first-pass.py', HERE/'geometry_model.py', HERE/'geometry-first-pass.json',
              HERE/'branch-support.json', HERE/'cell-path.json', HERE/'table.json']:
        result['dependencies_sha256'][str(p.relative_to(BASE))] = hashlib.sha256(p.read_bytes()).hexdigest()

    def save():
        result['seconds'] = time.monotonic()-start
        p = HERE/'geometry-refine.json'
        tmp = p.with_suffix('.tmp')
        tmp.write_text(json.dumps(result, indent=2)+'\n')
        tmp.replace(p)

    for previous in original['records']:
        case = supports[previous['tag']]
        if previous['status'] in ('OPTIMAL', 'FEASIBLE'):
            row = dict(previous, proof='independently checked physical room from first pass')
            if case['I'] == 2:
                cells = {(p[0]//2, p[1]//2) for t in row['room']['triangles'] for p in t if not p[0]%2 and not p[1]%2}
                missing = len(set(map(tuple, case['mandatory']))-cells)
                assert row['cell']['Q']+missing >= paths[case['tag']]['Q_plus_missing_lower']
                result['positive_charge_controls'] += 1
        elif previous['status'] == 'INFEASIBLE':
            row = dict(previous, proof='first-pass whole-support geometric infeasibility')
        elif case['I'] == 2 and paths[case['tag']]['wall_lower'] > 23:
            row = dict(previous, status='EXCLUDED_BY_CELL_PATH_BOUND', proof=paths[case['tag']])
        else:
            b = first.bounded(case)
            m, ts, x, _, terms = build_model((0, 0), 23, 4, b)
            j = m.new_int_var(0, 4, 'J')
            sn = m.new_int_var(0, 4, 's_N')
            q = m.new_int_var(0, 17, 'Q')
            n = m.new_int_var(1, 37, 'N')
            m.add(j == sum(terms['defects'])-4)
            m.add(sn == 4-j)
            m.add(q == sum(terms['charges']))
            m.add(n == sum(x))
            m.add_allowed_assignments([j, sn, q, n], [v[1:] for v in sorted(allowed) if v[0] == case['I']])
            if case['I'] == 2:
                missing = sum(1-terms['used'][2*a, 2*b] for a, b in set(map(tuple, case['mandatory']))-set(map(tuple, case['full'])))
                m.add(q+missing >= paths[case['tag']]['Q_plus_missing_lower'])
            incoming = [[] for _ in ts]
            outgoing = [[] for _ in ts]
            root = next(i for i, tri in enumerate(ts) if (0, 0) in tri)
            for ids in owners_of(ts).values():
                if len(ids) == 2:
                    for a, b in (ids, ids[::-1]):
                        flow = m.new_int_var(0, 37, f'flow{a}_{b}')
                        m.add(flow <= 37*x[a])
                        m.add(flow <= 37*x[b])
                        outgoing[a].append(flow)
                        incoming[b].append(flow)
            for index in range(len(ts)):
                if index == root:
                    m.add(sum(outgoing[index])-sum(incoming[index]) == n-1)
                else:
                    m.add(sum(incoming[index])-sum(outgoing[index]) == x[index])
            solver, status = first.solve(m, 45)
            row = dict(tag=case['tag'], I=case['I'], full=case['full'], status=solver.status_name(status),
                       seconds=solver.wall_time, available_triangles=len(ts))
            if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                a, b = case['mark_pairs'][0]
                room = dict(triangles=[t for t, var in zip(ts, x) if solver.value(var)],
                            marked=[[2*a[0], 2*a[1]], [2*b[0], 2*b[1]]], slits=[])
                values, _, geometry = first.physical_inventory(room, rows)
                assert values in allowed
                row.update(cell=dict(zip(('I', 'J', 's_N', 'Q', 'N'), values)), walls=geometry['walls'], room=room)
        result['records'].append(row)
        save()
        print(json.dumps({k: v for k, v in row.items() if k not in ('room', 'proof')}), flush=True)
    result['status'] = 'COMPLETE' if len(result['records']) == len(supports) and all(r['status'] != 'UNKNOWN' for r in result['records']) else 'INCOMPLETE'
    save()


if __name__ == '__main__':
    main()
