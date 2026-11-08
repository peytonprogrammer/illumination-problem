"""Forward/reverse pairing of frozen affine events. No ray tracing or discovery."""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
import importlib.util
import json

if not __debug__:
    raise RuntimeError('Exact verification requires assertions; do not run with -O.')

import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('repair_structure', ROOT/'repair-structure.py')
repair = importlib.util.module_from_spec(spec)
spec.loader.exec_module(repair)
solve, dot = repair.solve, repair.dot
j = json.loads((ROOT/'coupling.json').read_text())
W, dim = j['walls'], j['offset_dimension']
unit = lambda i: tuple(F(k == i) for k in range(dim))
add = lambda a, b: tuple(x+y for x, y in zip(a, b))
scale = lambda a, v: tuple(a*x for x in v)
sub = lambda a, b: add(a, scale(-1, b))
mv = lambda A, v: tuple(sum(A[a][b]*v[b] for b in (0, 1)) for a in (0, 1))
mf = lambda A, v: tuple(tuple(sum(A[a][b]*v[b][k] for b in (0, 1)) for k in range(dim)) for a in (0, 1))
matmul = lambda A, B: tuple(tuple(sum(A[a][c]*B[c][b] for c in (0, 1)) for b in (0, 1)) for a in (0, 1))
cross = lambda a, b: a[0]*b[1]-a[1]*b[0]
fcross = lambda w, v: tuple(w[0]*v[1][k]-w[1]*v[0][k] for k in range(dim))
source = (unit(W), unit(W+1))
target = (unit(W+2), unit(W+3))
theta = tuple(map(F, j['offset_base_point']))
normal = list(map(tuple, j['offset_normals']))
I = ((F(1), F(0)), (F(0), F(1)))
reflect = [tuple(tuple(F(a == b)-F(2*n[a]*n[b], dot(n, n)) for b in (0, 1)) for a in (0, 1)) for n in normal]
forms = lambda x: tuple(tuple(map(F, row)) for row in x)
records = []
for e in j['events']:
    O = I
    for wall in e['word']:
        O = matmul(O, reflect[wall])
    Ot = tuple(zip(*O))
    det = cross(O[0], O[1])
    T, C = forms(e['target_image_forms']), forms(e['corner_image_forms'])
    b = tuple(sub(T[k], mf(O, target)[k]) for k in (0, 1))
    reverse_target = mf(Ot, tuple(sub(source[k], b[k]) for k in (0, 1)))
    reverse_corner = mf(Ot, tuple(sub(C[k], b[k]) for k in (0, 1)))
    wr = tuple(-v for v in mv(Ot, tuple(e['direction'])))
    sr = -e['side']*det
    Ar = tuple(sub(reverse_target[k], target[k]) for k in (0, 1))
    Cr = tuple(sub(reverse_corner[k], target[k]) for k in (0, 1))
    Er = tuple(sub(scale(2, Cr[k]), Ar[k]) for k in (0, 1))
    row = tuple(map(F, e['offset_gradient']))
    assert scale(sr, fcross(wr, Er)) == row
    assert tuple(dot(v, theta) for v in Ar) == tuple(2*x for x in wr)
    assert tuple(dot(v, theta) for v in Cr) == wr
    # Normalization identity; this line alone is not a quadratic-polynomial test.
    # The nontrivial row identity and the pair identities are checked above/below.
    assert -sr*det == e['side']
    records.append({'index': e['index'], 'corner': tuple(e['corner']),
                    'forward': {'w': tuple(e['direction']), 'side': e['side'], 'C': C, 'T': T},
                    'reverse': {'w': wr, 'side': sr, 'C': reverse_corner, 'T': reverse_target},
                    'row': row})


def paired(which):
    groups = defaultdict(dict)
    for r in records:
        f = r[which]
        key = (f['w'], r['corner'], f['C'])
        assert f['side'] not in groups[key], ('duplicate', which, r['index'])
        groups[key][f['side']] = r
    result = []
    for key, sides in groups.items():
        if set(sides) != {-1, 1}:
            continue
        plus, minus = sides[1], sides[-1]
        Tp, Tm = plus[which]['T'], minus[which]['T']
        g = add(plus['row'], minus['row'])
        assert g == fcross(key[0], tuple(sub(Tm[k], Tp[k]) for k in (0, 1)))
        lost = (W, W+1) if which == 'forward' else (W+2, W+3)
        assert all(g[k] == 0 for k in lost)
        result.append({'indices': [plus['index'], minus['index']], 'row': g,
                       'direction': key[0], 'corner': key[1], 'family': which})
    return result


forward, reverse = paired('forward'), paired('reverse')
allpairs = forward+reverse
rank = lambda rows: solve(list(zip(*rows)), [F(0)]*dim)[1] if rows else 0
nonzero = [p for p in allpairs if any(p['row'])]
stress = repair.positive_stress([p['row'] for p in nonzero]) if nonzero else None
out = {'status': 'EXACT_IDENTITIES_PASS', 'tag': j['tag'], 'events_reversed_algebraically': len(records),
       'forward_pairs': len(forward), 'reverse_pairs': len(reverse),
       'forward_rank': rank([p['row'] for p in forward]),
       'reverse_rank': rank([p['row'] for p in reverse]),
       'combined_rank': rank([p['row'] for p in allpairs]), 'required_rank': W+1,
       'positive_stress': list(map(str, stress)) if stress else None,
       'pairs': [{**p, 'row': list(map(str, p['row'])), 'direction': list(map(str, p['direction']))} for p in allpairs],
       'scope': f'Exact affine reversal and paired-loop algebra on {len(records)} frozen events. A failed floating stress proposal is not an exact exclusion.'}
if stress is not None:
    expanded = [F(0)]*len(records)
    for pair, weight in zip(nonzero, stress):
        for index in pair['indices']:
            expanded[index] += weight
    used = [i for i, value in enumerate(expanded) if value]
    assert all(value >= 0 for value in expanded)
    assert all(sum(value*r['row'][k] for value, r in zip(expanded, records)) == 0 for k in range(dim))
    expanded_rank = rank([records[i]['row'] for i in used])
    assert expanded_rank >= out['combined_rank']
    out['expanded_pair_stress'] = {'indices': used, 'weights': [str(expanded[i]) for i in used],
                                   'rank': expanded_rank}
if stress is None and nonzero:
    # Produce an exact dual separator if possible; unlike an LP failure, this is a proof.
    scales = [max(map(abs, p['row'])) for p in nonzero]
    R = [tuple(v/s for v in p['row']) for p, s in zip(nonzero, scales)]
    M = np.array(R, dtype=float)
    proposal = linprog(-M.sum(axis=0), A_ub=-M, b_ub=np.zeros(len(R)),
                      bounds=[(-1, 1)]*dim, method='highs')
    assert proposal.success
    active = [i for i, value in enumerate(M@proposal.x) if abs(value) < 1e-8]
    bounds = [i for i, value in enumerate(proposal.x) if abs(abs(value)-1) < 1e-8]
    eq = [R[i] for i in active]+[unit(i) for i in bounds]
    rhs = [F(0)]*len(active)+[F(1 if proposal.x[i] > 0 else -1) for i in bounds]
    delta, _ = solve(eq, rhs, unique=True)
    values = [dot(p['row'], delta) for p in allpairs]
    assert all(v >= 0 for v in values) and any(v > 0 for v in values)
    out['exact_separator'] = list(map(str, delta))
    out['separator_pair_values'] = list(map(str, values))
    out['strictly_positive_stress_on_all_listed_pairs_impossible'] = True
    candidates = [e['index'] for e in j['events'] if any(
        sorted(abs(e['corner'][k]-p[k]) for k in (0, 1)) == [1, 1] for p in j['room']['marked'])]
    out['single_diagonal_repair'] = None
    for index in candidates:
        original = tuple(map(F, j['events'][index]['offset_gradient']))
        weights = repair.positive_stress([p['row'] for p in nonzero]+[original])
        if weights is not None:
            original_weights = [F(0)]*len(records)
            for pair, weight in zip(nonzero, weights[:-1]):
                for k in pair['indices']:
                    original_weights[k] += weight
            original_weights[index] += weights[-1]
            assert all(v >= 0 for v in original_weights)
            assert all(sum(v*r['row'][k] for v, r in zip(original_weights, records)) == 0 for k in range(dim))
            used = [i for i, v in enumerate(original_weights) if v]
            assert rank([records[i]['row'] for i in used]) == W+1
            out['single_diagonal_repair'] = {'index': index,
                'pair_indices': [p['indices'] for p in nonzero], 'weights': list(map(str, weights)),
                'original_event_indices': used, 'original_event_weights': [str(original_weights[i]) for i in used]}
            break
    out['single_diagonal_attempts'] = candidates.index(out['single_diagonal_repair']['index'])+1 if out['single_diagonal_repair'] else len(candidates)
    out['single_diagonal_failure_scope'] = 'No proposal succeeded; not an exact impossibility result.' if out['single_diagonal_repair'] is None else None
# Both pairing relations are matchings, so their union consists of alternating paths/cycles.
adj = defaultdict(list)
for p in allpairs:
    a, b = p['indices']
    adj[a].append((b, p['family']))
    adj[b].append((a, p['family']))
assert all(len(edges) <= 2 for edges in adj.values())
seen = set()
components = []
for start in range(len(records)):
    if start in seen:
        continue
    todo = [(start, 1)]
    colors = {}
    while todo:
        a, color = todo.pop()
        if a in colors:
            assert colors[a] == color
            continue
        colors[a] = color
        seen.add(a)
        todo.extend((b, -color) for b, _ in adj[a])
    components.append({'vertices': list(colors), 'bipartition': colors,
                       'edges': sum(len(adj[a]) for a in colors)//2})
out['pair_graph'] = components
(ROOT/'bidirectional-loops.json').write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps({k: v for k, v in out.items() if k not in ('pairs', 'exact_separator', 'separator_pair_values', 'pair_graph')}, indent=2))
