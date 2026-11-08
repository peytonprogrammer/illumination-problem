"""Cell-path charge lower bounds on complete k=4 supports; no rays."""
import hashlib
import heapq
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
sys.path.insert(0, str(BASE))
from illumination_family_bound import NEIGHBORS
from illumination_cell_path_bound import fan_charge_check


def path_bound(case):
    source, target = map(tuple, case['full'])
    required = set(map(tuple, case['mandatory']))
    allowed = set(map(tuple, case['allowed']))
    full = {source, target}
    external = len(required-full)
    distance = {}
    queue = []
    paths = {}
    for dx, dy in NEIGHBORS:
        q = source[0]+dx, source[1]+dy
        if q in allowed:
            distance[source, q] = 0
            paths[source, q] = (source, q)
            heapq.heappush(queue, (0, source, q))
    while queue:
        cost, previous, current = heapq.heappop(queue)
        if distance[previous, current] != cost:
            continue
        if current == target:
            return external+cost, paths[previous, current]
        for dx, dy in NEIGHBORS:
            nxt = current[0]+dx, current[1]+dy
            if nxt not in allowed or nxt == previous or nxt == source:
                continue
            straight = (current[0]-previous[0], current[1]-previous[1]) == (dx, dy)
            extra = 2+int(straight)-int(current in required)
            total = cost+extra
            key = current, nxt
            if total < distance.get(key, 10**9):
                distance[key] = total
                paths[key] = paths[previous, current]+(nxt,)
                heapq.heappush(queue, (total, current, nxt))
    raise AssertionError('No full-cell path even in the allowed relaxation')


def main():
    p = HERE/'branch-support.json'
    supports = json.loads(p.read_text())
    result = dict(status='PASS', k=4, local_fan_check=fan_charge_check(), records=[],
                  scope='Lower bound on Q+m from directed cell walks in the allowed support, a relaxation of simple occupied-cell paths. No ray or geometry search.',
                  dependencies_sha256={})
    for src in [Path(__file__), p, BASE/'illumination_cell_path_bound.py']:
        result['dependencies_sha256'][str(src.relative_to(BASE))] = hashlib.sha256(src.read_bytes()).hexdigest()
    for case in supports['cases']:
        if case['I'] != 2:
            continue
        lower, path = path_bound(case)
        row = dict(tag=case['tag'], Q_plus_missing_lower=lower,
                   wall_lower=6+lower, minimizing_relaxed_walk=path)
        result['records'].append(row)
        print(json.dumps(row), flush=True)
    (HERE/'cell-path.json').write_text(json.dumps(result, indent=2)+'\n')


if __name__ == '__main__':
    main()
