"""Complete finite support reduction for the first k=4 geometry branch.

The earlier cell-degree proof parameterizes: P+m <= floor((23-4I+2k)/2).
For I=2 this is 11, giving nonadjacent mark distance <=6. For I=3 it
is 9, so b<=9; disconnected full-cell overlap components need b>=10.
Hence the three full cells are distance-two-overlap connected, within
distance four of a full root. This is a support list, not feasibility.
"""
import hashlib
import importlib.util
import itertools
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
sys.path.insert(0, str(BASE))
from illumination_family_bound import NEIGHBORS, support
from illumination_two_exception_bound import canonical


def main():
    result = dict(status='COMPLETE_NECESSARY_SUPPORT', k=4, wall_cap=23,
                  scope='Complete potential-dark-family supports; adjacent marked cells omitted by the direct-segment theorem. No ray discovery or geometry feasibility.',
                  cases=[], dependencies_sha256={})
    for p in [Path(__file__), BASE/'illumination_family_bound.py', BASE/'illumination_two_exception_bound.py']:
        result['dependencies_sha256'][str(p.relative_to(BASE))] = hashlib.sha256(p.read_bytes()).hexdigest()
    for distance in range(2, 7):
        for x in range((distance+1)//2, distance+1):
            target = (x, distance-x)
            bounded = support(target, 11)
            result['cases'].append(dict(I=2, tag='I2_'+str(x)+'_'+str(target[1]),
                full=sorted(bounded['full']), mandatory=sorted(bounded['mandatory']),
                allowed=sorted(bounded['allowed']), b=bounded['partial_required'],
                partial_plus_missing_cap=11, outside_cell_cap=bounded['extra_budget'],
                mark_pairs=[[(0, 0), target]]))
    diamond = [(x, y) for x in range(-4, 5) for y in range(-4, 5) if 0 < abs(x)+abs(y) <= 4]
    found = {}
    checked = 0
    for a, b in itertools.combinations(diamond, 2):
        full = {(0, 0), a, b}
        reached, todo = {(0, 0)}, [(0, 0)]
        for p in todo:
            for q in full-reached:
                if abs(p[0]-q[0])+abs(p[1]-q[1]) <= 2:
                    reached.add(q)
                    todo.append(q)
        if reached != full:
            continue
        checked += 1
        ext = {(x+dx, y+dy) for x, y in full for dx, dy in NEIGHBORS}-full
        if len(ext) <= 9:
            normalized = canonical(full)
            found[normalized] = len(ext)
    for index, (shape, b) in enumerate(sorted(found.items())):
        full = set(shape)
        required = full | {(x+dx, y+dy) for x, y in full for dx, dy in NEIGHBORS}
        allowed = set(required)
        for _ in range(9-b):
            allowed |= {(x+dx, y+dy) for x, y in allowed for dx, dy in NEIGHBORS}
        pairs = [(a, b) for a, b in itertools.combinations(shape, 2)
                 if abs(a[0]-b[0])+abs(a[1]-b[1]) > 1]
        assert pairs and (0, 0) in full
        result['cases'].append(dict(I=3, tag='I3_'+str(index), full=shape,
            mandatory=sorted(required), allowed=sorted(allowed), b=b,
            partial_plus_missing_cap=9, outside_cell_cap=9-b, mark_pairs=pairs))
    result['three_full_rooted_patterns_checked'] = checked
    result['case_counts'] = {str(i): sum(c['I']==i for c in result['cases']) for i in (2, 3)}
    (HERE/'branch-support.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(status=result['status'], case_counts=result['case_counts'],
                          rooted_triples=checked, total_allowed_cells=sum(len(c['allowed']) for c in result['cases']))))


if __name__ == '__main__':
    main()
