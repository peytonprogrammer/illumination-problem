"""Compose the complete k=4 support eligibility receipts; no solving or rays."""
import hashlib
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    partitions = load_module('partitions', HERE/'geometry-partitions.py')
    path_module = load_module('cell_path', HERE/'cell-path.py')
    first = partitions.first
    rows = first.local_rows()
    supports = json.loads((HERE/'branch-support.json').read_text())['cases']
    initial = {r['tag']: r for r in json.loads((HERE/'geometry-first-pass.json').read_text())['records']}
    negatives = {r['tag']: r for r in json.loads((HERE/'geometry-partitions.json').read_text())['records']}
    bounds = {r['tag']: r for r in json.loads((HERE/'cell-path.json').read_text())['records']}
    data = json.loads((HERE/'table.json').read_text())
    dp = json.loads((HERE/'dp-audit.json').read_text())
    assert dp['status'] == 'PASS' and dp['table_sha256'] == hashlib.sha256((HERE/'table.json').read_bytes()).hexdigest()
    inventories = {(c['I'], c['J'], c['s_N'], c['Q'], c['N']) for t in data['tables'] if t['k'] == 4
                   for c in t['cells'] if c['status'] in ('OPTIMAL', 'FEASIBLE')}
    result = dict(status='PASS', scope='Complete k=4 geometric-support eligibility only. No full two-star tuple projection or darkness conclusion.',
                  records=[], negative_fixed_cell_checks=0, physical_positive_checks=0, dependencies_sha256={})
    for p in [Path(__file__), HERE/'branch-support.json', HERE/'geometry-first-pass.json', HERE/'geometry-partitions.json',
              HERE/'cell-path.json', HERE/'table.json', HERE/'dp-audit.json', HERE/'three-star-cells.json']:
        result['dependencies_sha256'][p.name] = hashlib.sha256(p.read_bytes()).hexdigest()
    for case in supports:
        tag = case['tag']
        previous = initial[tag]
        row = dict(tag=tag, I=case['I'], full=case['full'])
        if previous['status'] in ('OPTIMAL', 'FEASIBLE'):
            values, _, geometry = first.physical_inventory(previous['room'], rows)
            assert values in inventories and geometry['walls'] <= 23
            row.update(status='GEOMETRY_FEASIBLE', cell=dict(zip(('I', 'J', 's_N', 'Q', 'N'), values)),
                       walls=geometry['walls'], room=previous['room'])
            result['physical_positive_checks'] += 1
        elif previous['status'] == 'INFEASIBLE':
            row.update(status='GEOMETRY_INFEASIBLE', proof='whole-support first-pass model')
        elif case['I'] == 2 and bounds[tag]['wall_lower'] > 23:
            lower, _ = path_module.path_bound(case)
            assert lower == bounds[tag]['Q_plus_missing_lower']
            assert 6+lower > 23
            row.update(status='GEOMETRY_INFEASIBLE', proof='cell-path wall bound', wall_lower=6+lower)
        else:
            neg = negatives[tag]
            expected = set(partitions.choices(case))
            observed = {tuple(map(tuple, r['outside_cells'])) for r in neg['partition']}
            assert neg['status'] == 'INFEASIBLE'
            assert observed == expected and len(neg['partition']) == len(expected)
            assert all(r['status'] == 'INFEASIBLE' for r in neg['partition'])
            result['negative_fixed_cell_checks'] += len(expected)
            row.update(status='GEOMETRY_INFEASIBLE', proof='complete fixed-outside-cell partition', cases=len(expected))
        result['records'].append(row)
    three = json.loads((HERE/'three-star-cells.json').read_text())
    assert three['status'] == 'COMPLETE'
    expected_three = {c for c in inventories if c[0] == 3}
    assert len(expected_three) == 22
    for group in three['records']:
        observed = {tuple(c[k] for k in ('I', 'J', 's_N', 'Q', 'N')) for c in group['cells']}
        assert observed == expected_three and len(group['cells']) == 22
        for c in group['cells']:
            assert c['status'] in ('OPTIMAL', 'FEASIBLE', 'INFEASIBLE')
            if 'room' in c:
                actual, _, _ = first.physical_inventory(c['room'], rows)
                assert actual == tuple(c[k] for k in ('I', 'J', 's_N', 'Q', 'N'))
                result['physical_positive_checks'] += 1
    assert {g['tag'] for g in three['records']} == {'I3_4', 'I3_6', 'I3_7'}
    result['support_counts'] = dict(Counter(r['status'] for r in result['records']))
    result['three_star_projected_queries'] = 66
    result['directly_illuminated_full_chain'] = dict(tag='I3_6',
        proof='Three adjacent full cells form the rectangle [-5,1] x [-1,1]. The only nonadjacent marks (-4,0),(0,0) lie in it; their connecting segment is interior. Similarities transfer the statement.')
    result['potential_dark_shapes'] = [r['tag'] for r in result['records']
                                      if r['status']=='GEOMETRY_FEASIBLE' and r['tag'] != 'I3_6']
    result['potential_dark_marked_families'] = sum(len(c['mark_pairs']) for c in supports if c['tag'] in result['potential_dark_shapes'])
    assert len(result['records']) == 22 and len(result['potential_dark_shapes']) == 9
    (HERE/'geometry-summary.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('records', 'dependencies_sha256')}, indent=2))


if __name__ == '__main__':
    main()
