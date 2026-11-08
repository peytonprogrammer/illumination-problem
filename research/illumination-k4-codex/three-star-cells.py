"""Project all k=4,I=3 local-inventory cells onto actual geometric shapes."""
import hashlib
import importlib.util
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
spec = importlib.util.spec_from_file_location('first_pass', HERE/'geometry-first-pass.py')
first = importlib.util.module_from_spec(spec)
spec.loader.exec_module(first)
from geometry_model import build_model
from ortools.sat.python import cp_model


def main():
    initial = json.loads((HERE/'geometry-first-pass.json').read_text())
    supports = {c['tag']: c for c in json.loads((HERE/'branch-support.json').read_text())['cases']}
    eligible = [r for r in initial['records'] if r['I']==3 and r['status'] in ('OPTIMAL', 'FEASIBLE')]
    assert len(eligible) == 3
    table = json.loads((HERE/'table.json').read_text())
    cells = sorted({(c['I'], c['J'], c['s_N'], c['Q'], c['N']) for t in table['tables'] if t['k']==4
                    for c in t['cells'] if c['I']==3 and c['status'] in ('OPTIMAL', 'FEASIBLE')})
    assert len(cells) == 22
    fan_rows = first.local_rows()
    result = dict(status='RUNNING', scope='Exact geometric eligibility of k=4,I=3 tuples over complete supports. No illumination or darkness claims.', records=[], dependencies_sha256={})
    for p in [Path(__file__), HERE/'geometry_model.py', HERE/'geometry-first-pass.json', HERE/'branch-support.json', HERE/'table.json']:
        result['dependencies_sha256'][p.name] = hashlib.sha256(p.read_bytes()).hexdigest()
    def save():
        p = HERE/'three-star-cells.json'
        temp = p.with_suffix('.tmp')
        temp.write_text(json.dumps(result, indent=2)+'\n')
        temp.replace(p)
    for old in eligible:
        case = supports[old['tag']]
        m, ts, x, _, terms = build_model((0, 0), 23, 4, first.bounded(case))
        j = m.new_int_var(0, 4, 'J')
        sn = m.new_int_var(0, 4, 's_N')
        q = m.new_int_var(0, 17, 'Q')
        n = m.new_int_var(1, 37, 'N')
        projection = [j, sn, q, n]
        m.add(j == sum(terms['defects'])-4)
        m.add(sn == 4-j)
        m.add(q == sum(terms['charges']))
        m.add(n == sum(x))
        m.add_allowed_assignments(projection, [c[1:] for c in cells])
        group = dict(tag=case['tag'], cells=[])
        result['records'].append(group)
        for values in cells:
            query = m.clone()
            for var, value in zip(projection, values[1:]):
                query.add(query.get_int_var_from_proto_index(var.index) == value)
            solver, status = first.solve(query, 10)
            row = dict(zip(('I', 'J', 's_N', 'Q', 'N'), values))
            row.update(status=solver.status_name(status), seconds=solver.wall_time)
            if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                a, b = case['mark_pairs'][0]
                room = dict(triangles=[t for t, var in zip(ts, x)
                                       if solver.value(query.get_int_var_from_proto_index(var.index))],
                            marked=[[2*a[0], 2*a[1]], [2*b[0], 2*b[1]]], slits=[])
                actual, _, geometry = first.physical_inventory(room, fan_rows)
                assert actual == values
                row.update(walls=geometry['walls'], room=room)
            group['cells'].append(row)
            save()
            print(json.dumps(dict(tag=case['tag'], cell=values, status=row['status'])), flush=True)
    result['status'] = 'COMPLETE' if all(c['status'] != 'UNKNOWN' for r in result['records'] for c in r['cells']) else 'INCOMPLETE'
    save()


if __name__ == '__main__':
    main()
