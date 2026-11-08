"""Complete fixed-cell eligibility partitions for unresolved k=4 supports."""
import hashlib
import importlib.util
import json
import sys
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
spec = importlib.util.spec_from_file_location('compact_witness', HERE/'geometry-local-witness.py')
compact = importlib.util.module_from_spec(spec)
spec.loader.exec_module(compact)
first = compact.first
from geometry_model import build_model
from illumination_family_bound import NEIGHBORS
from ortools.sat.python import cp_model


def choices(case):
    required = set(map(tuple, case['mandatory']))
    allowed = set(map(tuple, case['allowed']))
    found = set(compact.outside_candidates(case))
    queue = list(found)
    for cells in queue:
        if len(cells) >= case['outside_cell_cap']:
            continue
        occupied = required | set(cells)
        adjacent = {(x+dx, y+dy) for x, y in occupied for dx, dy in NEIGHBORS} & allowed - occupied
        for q in adjacent:
            enlarged = tuple(sorted((*cells, q)))
            if enlarged not in found:
                found.add(enlarged)
                queue.append(enlarged)
    return sorted(found, key=lambda s: (len(s), s))


def main():
    supports = {c['tag']: c for c in json.loads((HERE/'branch-support.json').read_text())['cases']}
    path_bounds = {r['tag']: r for r in json.loads((HERE/'cell-path.json').read_text())['records']}
    table = json.loads((HERE/'table.json').read_text())
    cells = {(c['I'], c['J'], c['s_N'], c['Q'], c['N']) for t in table['tables'] if t['k'] == 4
             for c in t['cells'] if c['status'] in ('OPTIMAL', 'FEASIBLE')}
    rows = first.local_rows()
    result = dict(status='RUNNING', scope='Complete fixed-outside-cell geometric eligibility partitions, no ray cuts or darkness claims.', records=[], dependencies_sha256={})
    for p in [Path(__file__), HERE/'geometry_model.py', HERE/'geometry-local-witness.py', HERE/'branch-support.json', HERE/'cell-path.json', HERE/'table.json']:
        result['dependencies_sha256'][p.name] = hashlib.sha256(p.read_bytes()).hexdigest()
    def save():
        p = HERE/'geometry-partitions.json'
        tmp = p.with_suffix('.tmp')
        tmp.write_text(json.dumps(result, indent=2)+'\n')
        tmp.replace(p)
    for tag in ['I2_3_3', 'I2_4_2', 'I2_4_1', 'I2_4_0']:
        case = supports[tag]
        candidates = choices(case)
        record = dict(tag=tag, complete_outside_cell_cases=len(candidates), partition=[], status='RUNNING')
        result['records'].append(record)
        print(json.dumps(dict(event='partition_start', tag=tag, cases=len(candidates))), flush=True)
        for index, outside in enumerate(candidates):
            b = first.bounded(case)
            b['allowed'] = b['mandatory'] | set(outside)
            m, ts, x, _, terms = build_model((0, 0), 23, 4, b)
            for a, bb in outside:
                m.add(terms['used'][2*a, 2*bb] == 1)
            q = m.new_int_var(0, 17, 'Q')
            j = m.new_int_var(0, 4, 'J')
            sn = m.new_int_var(0, 4, 's_N')
            n = m.new_int_var(1, 37, 'N')
            m.add(q == sum(terms['charges']))
            m.add(j == sum(terms['defects'])-4)
            m.add(sn == 4-j)
            m.add(n == sum(x))
            m.add_allowed_assignments([j, sn, q, n], [v[1:] for v in sorted(cells) if v[0] == 2])
            missing = sum(1-terms['used'][2*a, 2*bb] for a, bb in b['mandatory']-b['full'])
            m.add(q+missing >= path_bounds[tag]['Q_plus_missing_lower'])
            solver = cp_model.CpSolver()
            solver.parameters.num_search_workers = 1
            solver.parameters.max_time_in_seconds = 2
            status = solver.solve(m)
            if status == cp_model.UNKNOWN:
                solver.parameters.max_time_in_seconds = 10
                status = solver.solve(m)
            assert status in (cp_model.OPTIMAL, cp_model.FEASIBLE, cp_model.INFEASIBLE, cp_model.UNKNOWN)
            row = dict(outside_cells=outside, status=solver.status_name(status), seconds=solver.wall_time)
            if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                a, bb = case['mark_pairs'][0]
                room = dict(triangles=[t for t, var in zip(ts, x) if solver.value(var)],
                            marked=[[2*a[0], 2*a[1]], [2*bb[0], 2*bb[1]]], slits=[])
                values, _, geometry = first.physical_inventory(room, rows)
                assert values in cells
                row.update(cell=dict(zip(('I', 'J', 's_N', 'Q', 'N'), values)), walls=geometry['walls'], room=room)
            record['partition'].append(row)
            if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                record['status'] = 'FEASIBLE'
                save()
                break
            if (index+1)%50 == 0:
                save()
                print(json.dumps(dict(tag=tag, done=index+1, total=len(candidates),
                                      statuses=dict(Counter(r['status'] for r in record['partition'])))), flush=True)
        if record['status'] != 'FEASIBLE':
            record['status'] = 'INFEASIBLE' if len(record['partition']) == len(candidates) and all(r['status']=='INFEASIBLE' for r in record['partition']) else 'OPEN'
        save()
        print(json.dumps(dict(tag=tag, status=record['status'], checked=len(record['partition']), total=len(candidates))), flush=True)
    result['status'] = 'COMPLETE' if all(r['status'] in ('FEASIBLE', 'INFEASIBLE') for r in result['records']) else 'INCOMPLETE'
    save()


if __name__ == '__main__':
    main()
