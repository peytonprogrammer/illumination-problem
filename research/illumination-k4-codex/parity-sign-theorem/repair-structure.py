"""Test single-row diagonal repairs of fixed saved cones; no optical search."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter, defaultdict
import importlib.util
import json
import math
import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parent
INP = ROOT / 'inputs/holdouts'
spec = importlib.util.spec_from_file_location('ear_family', ROOT / 'ear-family.py')
family = importlib.util.module_from_spec(spec)
spec.loader.exec_module(family)
solve, dot = family.solve, family.dot


def frozen_rows(tag):
    room = json.loads((INP / (tag + '.json')).read_text())
    old = json.loads((INP / ('funcs-' + tag + '-R12.json')).read_text())
    events = json.loads((INP / ('events-' + tag + '-R12.json')).read_text())['rows']
    vertices = list(map(tuple, room['vertices']))
    W = len(vertices)
    dim = W + 4
    unit = lambda k: tuple(F(i == k) for i in range(dim))
    dirs = []
    for a, b in zip(vertices, vertices[1:] + vertices[:1]):
        d = (b[0] - a[0], b[1] - a[1])
        length = math.gcd(*map(abs, d))
        dirs.append(tuple(v // length for v in d))
    normals = [(-d[1], d[0]) for d in dirs]
    B = []
    for i in range(W):
        p = (i - 1) % W
        a, b = normals[p], normals[i]
        det = a[0] * b[1] - a[1] * b[0]
        B.append((tuple((b[1]*unit(p)[k]-a[1]*unit(i)[k])/det for k in range(dim)),
                  tuple((-b[0]*unit(p)[k]+a[0]*unit(i)[k])/det for k in range(dim))))
    ell = [tuple(sum(F(d[a], dot(d, d)) * (B[(i+1)%W][a][k]-B[i][a][k])
                     for a in (0, 1)) for k in range(dim)) for i, d in enumerate(dirs)]
    T = list(B[0]) + ell + [unit(W+k) for k in range(4)]
    rows = [tuple(sum(F(row[k])*T[k][c] for k in range(W+6)) for c in range(dim))
            for row in old['funcs']]
    theta = tuple(F(dot(n, v)) for n, v in zip(normals, vertices)) + tuple(F(x) for p in room['marked'] for x in p)
    trans = [tuple(F(n[a]) for n in normals) + tuple(F(k%2 == a) for k in range(4)) for a in (0, 1)]
    assert all(dot(g, v) == 0 for g in rows for v in [theta] + trans)
    axis = [i for i, e in enumerate(events) if any(sorted(abs(e['corner'][a]-p[a]) for a in (0, 1)) == [0, 1] for p in room['marked'])]
    return room, events, rows, axis


def positive_stress(rows):
    """LP proposes weights; rational reconstruction proves the result."""
    dim = len(rows[0])
    scales = [max(map(abs, row)) for row in rows]
    R = [tuple(v/s for v in row) for row, s in zip(rows, scales)]
    lp = linprog(np.ones(len(rows)), A_eq=np.array(R, dtype=float).T,
                 b_eq=np.zeros(dim), bounds=[(1, None)]*len(rows), method='highs')
    assert lp.status in (0, 2)
    if lp.status == 2:
        return None  # A proposal failure, never an exact exclusion.
    active = [i for i, v in enumerate(lp.x) if abs(v-1) < 1e-8]
    free = [i for i in range(len(rows)) if i not in active]
    x, _ = solve([[R[i][c] for i in free] for c in range(dim)],
                 [-sum(R[i][c] for i in active) for c in range(dim)], unique=True) if free else ([], 0)
    mu = [F(1)]*len(rows)
    for i, v in zip(free, x):
        mu[i] = v
    weights = [v/s for v, s in zip(mu, scales)]
    assert all(v > 0 for v in weights)
    assert all(sum(v*row[c] for v, row in zip(weights, rows)) == 0 for c in range(dim))
    return weights


def main():
    cones = json.loads((ROOT / 'ear-family.json').read_text())['cases']
    selection = {x['tag']: x for x in json.loads((INP / 'selection.json').read_text())}
    grouped = defaultdict(Counter)
    results = []
    for cone in cones:
        tag = cone['tag']
        room, events, rows, axis = frozen_rows(tag)
        W = len(room['vertices'])
        s, t = room['marked']
        displacement = tuple(sorted(abs(x-y) for x, y in zip(s, t)))
        grouped[cone['cone_dimension_mod_symmetries']][str(displacement)] += 1
        # Existing repair corners only, in their frozen order. Stop at a verified witness.
        corners = list(map(tuple, selection[tag]['diagonal_repairs']))
        candidates = [i for c in corners for i, e in enumerate(events) if tuple(e['corner']) == c]
        found = None
        for i in candidates:
            indices = axis + [i]
            weights = positive_stress([rows[j] for j in indices])
            if weights is None:
                continue
            rank = solve(list(zip(*[rows[j] for j in indices])), [F(0)]*(W+4))[1]
            assert rank == W+1
            found = {'index': i, 'corner': events[i]['corner'], 'direction': events[i]['dir'],
                     'indices': indices, 'weights': list(map(str, weights)), 'rank': rank}
            break
        result = {'tag': tag, 'displacement_D4': displacement,
                  'axis_cone_dimension': cone['cone_dimension_mod_symmetries'],
                  'single_diagonal_exact_certificate': found,
                  'single_event_attempts': candidates.index(found['index'])+1 if found else len(candidates),
                  'failure_scope': None if found else 'No LP proposal succeeded; no exact impossibility conclusion.'}
        results.append(result)
        print(json.dumps({'tag': tag, 'single_diagonal_verified': found is not None,
                          'attempts': result['single_event_attempts']}), flush=True)
    out = {'status': 'EXACT_WITNESSES_CHECKED', 'displacement_by_cone_dimension': dict(grouped),
           'single_event_verified': sum(r['single_diagonal_exact_certificate'] is not None for r in results),
           'cases': results, 'scope': 'Frozen34packets only; no new event discovery. LP failures do not prove exclusions.'}
    (ROOT / 'repair-structure.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({k: v for k, v in out.items() if k != 'cases'}, indent=2), flush=True)


if __name__ == '__main__':
    main()
