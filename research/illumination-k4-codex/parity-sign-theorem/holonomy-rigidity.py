"""Absolute-period rigidity of frozen wall systems, without billiard trajectories."""
from pathlib import Path
from fractions import Fraction as F
from collections import deque
import json
import math

if not __debug__:
    raise RuntimeError('Exact verification requires assertions; do not run with -O.')

ROOT = Path(__file__).resolve().parent
INP = ROOT/'inputs/holdouts'
dot = lambda a, b: sum(x*y for x, y in zip(a, b))
add = lambda a, b: tuple(x+y for x, y in zip(a, b))
sub = lambda a, b: tuple(x-y for x, y in zip(a, b))
scale = lambda a, v: tuple(a*x for x in v)
mm = lambda A, B: tuple(tuple(sum(A[i][k]*B[k][j] for k in (0, 1)) for j in (0, 1)) for i in (0, 1))
mf = lambda A, v: tuple(tuple(sum(A[i][k]*v[k][j] for k in (0, 1)) for j in range(len(v[0]))) for i in (0, 1))
I = ((F(1), F(0)), (F(0), F(1)))


def rank(rows):
    basis = {}
    for row in rows:
        a = list(map(F, row))
        for p, b in sorted(basis.items()):
            if a[p]:
                x = a[p]
                a = [v-x*w for v, w in zip(a, b)]
        p = next((i for i, v in enumerate(a) if v), None)
        if p is not None:
            x = a[p]
            basis[p] = [v/x for v in a]
    return len(basis)


def check(room):
    v = room['vertices']
    W = len(v)
    normals = []
    for a, b in zip(v, v[1:]+v[:1]):
        dx, dy = b[0]-a[0], b[1]-a[1]
        # Any nonzero normal scaling is valid for the supporting-line chart.
        normals.append((-dy, dx))
    h = tuple(F(dot(n, p)) for n, p in zip(normals, v))
    unit = lambda i: tuple(F(k == i) for k in range(W))
    reflect = []
    for i, n in enumerate(normals):
        R = tuple(tuple(F(a == b)-F(2*n[a]*n[b], dot(n, n)) for b in (0, 1)) for a in (0, 1))
        shift = tuple(scale(F(2*n[a], dot(n, n)), unit(i)) for a in (0, 1))
        reflect.append((R, shift))
    # One affine representative for each orientation. These are chamber-chart
    # paths, NOT straight billiard paths. Only reflection matrices are explored.
    zero = (F(0),)*W
    representatives = {I: (zero, zero)}
    tree = {I: []}
    queue = deque([I])
    while queue:
        O = queue.popleft()
        B = representatives[O]
        for i, (R, b) in enumerate(reflect):
            P = mm(O, R)
            if P not in representatives:
                representatives[P] = tuple(add(B[k], mf(O, b)[k]) for k in (0, 1))
                tree[P] = tree[O]+[i]
                queue.append(P)
    assert len(representatives) in (4, 8)
    periods = []
    for O, B in representatives.items():
        for i, (R, b) in enumerate(reflect):
            P = mm(O, R)
            L = tuple(sub(add(B[k], mf(O, b)[k]), representatives[P][k]) for k in (0, 1))
            periods.append({'sheet': O, 'wall': i, 'forms': L,
                            'value': tuple(dot(row, h) for row in L)})
    assert rank([p['value'] for p in periods]) == 2
    p_index = next(i for i, p in enumerate(periods) if any(p['value']))
    basis_p = periods[p_index]['value']
    q_index = next(i for i, r in enumerate(periods) if basis_p[0]*r['value'][1]-basis_p[1]*r['value'][0])
    basis_q = periods[q_index]['value']
    determinant = basis_p[0]*basis_q[1]-basis_p[1]*basis_q[0]
    coefficients = lambda r: ((r[0]*basis_q[1]-r[1]*basis_q[0])/determinant,
                              (basis_p[0]*r[1]-basis_p[1]*r[0])/determinant)
    relations = []
    for period in periods:
        a, b = coefficients(period['value'])
        relation = tuple(sub(sub(period['forms'][k], scale(a, periods[p_index]['forms'][k])),
                             scale(b, periods[q_index]['forms'][k])) for k in (0, 1))
        assert all(dot(r, h) == 0 for r in relation)
        relations.append(relation)
    relation_rows = [row for relation in relations for row in relation]
    relation_kernel = W-rank(relation_rows)
    period_denominator = math.lcm(*(x.denominator for p in periods for x in p['value']))
    integer_periods = [tuple(int(x*period_denominator) for x in p['value']) for p in periods]
    determinant_gcd = 0
    for i, a in enumerate(integer_periods):
        for b in integer_periods[i+1:]:
            determinant_gcd = math.gcd(determinant_gcd, abs(a[0]*b[1]-a[1]*b[0]))
    covolume = F(determinant_gcd, period_denominator**2)
    area = abs(F(sum(a[0]*b[1]-a[1]*b[0] for a, b in zip(v, v[1:]+v[:1])), 2))
    degree = len(representatives)*area/covolume
    assert degree > 0 and degree.denominator == 1
    isoperiodic_kernel = W-rank([row for p in periods for row in p['forms']])
    assert isoperiodic_kernel == 2
    eq = []
    for p in periods:
        x, y = p['value']
        eq.append(list(p['forms'][0])+[-x, -y, F(0), F(0)])
        eq.append(list(p['forms'][1])+[F(0), F(0), -x, -y])
    # Unknowns are (delta h, A11,A12,A21,A22).
    tx = [F(n[0]) for n in normals]+[F(0)]*4
    ty = [F(n[1]) for n in normals]+[F(0)]*4
    uniform = list(h)+[F(1), F(0), F(0), F(1)]
    kernel_dimension = W+4-rank(eq)
    assert all(dot(row, z) == 0 for row in eq for z in (tx, ty, uniform))
    assert rank([tx, ty, uniform]) == 3
    if len(representatives) == 8:
        assert kernel_dimension == 3
        # Prescribing a nonscalar A must be inconsistent, not merely yield a
        # different dimension. This tests the commuting-map restriction.
        fixed = [[F(k == W+a) for k in range(W+4)] for a in range(4)]
        augmented = [row+[F(0)] for row in eq]+[row+[F(a == 0)] for a, row in enumerate(fixed)]
        assert rank(augmented) == rank(eq+fixed)+1
    # Independently derive the centralizer constraints A R = R A.
    commutator = []
    matrices = [((1, 0), (0, 0)), ((0, 1), (0, 0)), ((0, 0), (1, 0)), ((0, 0), (0, 1))]
    for R in representatives:
        for a in (0, 1):
            for b in (0, 1):
                commutator.append([mm(M, R)[a][b]-mm(R, M)[a][b] for M in matrices])
    centralizer_dimension = 4-rank(commutator)
    assert kernel_dimension == centralizer_dimension+2
    assert relation_kernel == kernel_dimension
    # Add marked relative-period equations from the first physical vertex.
    n, m = normals[-1], normals[0]
    det = n[0]*m[1]-n[1]*m[0]
    vertex0 = (scale(1/F(det), sub(scale(m[1], unit(W-1)), scale(n[1], unit(0)))),
               scale(1/F(det), sub(scale(n[0], unit(0)), scale(m[0], unit(W-1)))))
    marked_eq = [row+[F(0)]*4 for row in eq]
    for mark, p in enumerate(room['marked']):
        x, y = p[0]-v[0][0], p[1]-v[0][1]
        for a in (0, 1):
            A = [-F(x), -F(y), F(0), F(0)] if a == 0 else [F(0), F(0), -F(x), -F(y)]
            row = [-z for z in vertex0[a]]+A+[F(0)]*4
            row[W+4+2*mark+a] = F(1)
            marked_eq.append(row)
    marked_kernel = W+8-rank(marked_eq)
    translations = [tx+[F(1), F(0), F(1), F(0)], ty+[F(0), F(1), F(0), F(1)]]
    marked_scale = uniform+[F(x) for p in room['marked'] for x in p]
    assert all(dot(row, z) == 0 for row in marked_eq for z in translations+[marked_scale])
    assert marked_kernel == kernel_dimension
    # A direct zero-period relation formulation eliminates the auxiliary A.
    marked_relations = [list(row)+[F(0)]*4 for row in relation_rows]
    for mark, point in enumerate(room['marked']):
        a, b = coefficients((F(point[0]-v[0][0]), F(point[1]-v[0][1])))
        for k in (0, 1):
            row = list(sub(sub(scale(-1, vertex0[k]), scale(a, periods[p_index]['forms'][k])),
                           scale(b, periods[q_index]['forms'][k])))+[F(0)]*4
            row[W+2*mark+k] = F(1)
            marked_relations.append(row)
    assert W+4-rank(marked_relations) == kernel_dimension
    physical_syms = [tx[:W]+[F(1), F(0), F(1), F(0)],
                     ty[:W]+[F(0), F(1), F(0), F(1)],
                     list(h)+[F(x) for point in room['marked'] for x in point]]
    assert all(dot(row, sym) == 0 for row in marked_relations for sym in physical_syms)
    ear_witness = None
    if room['tag'] == 'parity-W25-24':
        # The existing primitive-normal ear mode is h5+=2,h6-=(-1).
        # Here normals are the full edge normals, so convert their scale.
        ear = [F(0)]*W
        for index, value in ((5, 2), (6, -1)):
            ear[index] = F(value*math.gcd(*map(abs, normals[index])))
        residuals = [tuple(dot(row, ear) for row in relation) for relation in relations]
        index = next(i for i, r in enumerate(residuals) if any(r))
        a, b = coefficients(periods[index]['value'])
        ear_witness = {'basis_period_indices': [p_index, q_index],
                       'basis_periods': [[str(x) for x in basis_p], [str(x) for x in basis_q]],
                       'third_period_index': index,
                       'third_period': list(map(str, periods[index]['value'])),
                       'third_coefficients': [str(a), str(b)],
                       'relation_drift': list(map(str, residuals[index])),
                       'period_drifts': [list(map(str, (dot(row, ear) for row in periods[i]['forms']))) for i in (p_index, q_index, index)]}
    return {'tag': room['tag'], 'walls': W, 'orientation_group_size': len(representatives),
            'period_generators': len(periods), 'period_span_rank': 2,
            'polygon_area': str(area), 'absolute_lattice_covolume': str(covolume),
            'intrinsic_cover_degree': int(degree),
            'fixed_period_kernel_dimension': isoperiodic_kernel,
            'affine_period_kernel_dimension': kernel_dimension,
            'linear_centralizer_dimension': centralizer_dimension,
            'marked_profile_kernel_dimension': marked_kernel,
            'zero_period_relation_rank': rank(relation_rows),
            'marked_zero_period_relation_rank': rank(marked_relations),
            'period_basis': [[str(x) for x in basis_p], [str(x) for x in basis_q]],
            'ear_three_period_witness': ear_witness}


cases = []
selections = json.loads((INP/'selection.json').read_text())
assert len(selections) == len({selection['tag'] for selection in selections}) == 34
for selection in selections:
    result = check(json.loads((INP/(selection['tag']+'.json')).read_text()))
    cases.append(result)
    print(json.dumps(result), flush=True)
rectangle = check({'tag': 'prescribed-rectangle-control',
    'vertices': [[0, 0], [3, 0], [3, 2], [0, 2]], 'marked': [[1, 1], [2, 1]]})
assert rectangle['orientation_group_size'] == 4
assert rectangle['affine_period_kernel_dimension'] == 4
assert rectangle['linear_centralizer_dimension'] == 2
print(json.dumps(rectangle), flush=True)
first = json.loads((INP/(cases[0]['tag']+'.json')).read_text())
scaled = {**first, 'tag': first['tag']+'-prescribed-scale2',
          'vertices': [[2*x for x in p] for p in first['vertices']],
          'marked': [[2*x for x in p] for p in first['marked']]}
scaled_result = check(scaled)
assert scaled_result['intrinsic_cover_degree'] == cases[0]['intrinsic_cover_degree']
assert F(scaled_result['absolute_lattice_covolume']) == 4*F(cases[0]['absolute_lattice_covolume'])
assert F(scaled_result['polygon_area']) == 4*F(cases[0]['polygon_area'])
print(json.dumps(scaled_result), flush=True)
out = {'status': 'EXACT_PASS', 'rooms_checked': len(cases), 'cases': cases, 'prescribed_control': rectangle,
       'prescribed_scale_control': scaled_result,
       'scope': 'Conditional affine-period/profile rigidity only. Does not prove darkness preserves periods or the cover, and does not prove the sign theorem. No billiard tracing.'}
(ROOT/'holonomy-rigidity.json').write_text(json.dumps(out, indent=2)+'\n')
