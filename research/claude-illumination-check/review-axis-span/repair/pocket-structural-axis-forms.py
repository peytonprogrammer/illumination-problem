"""One frozen room's existing axis-period forms; no cylinder/path discovery."""
from pathlib import Path
from fractions import Fraction as F
import hashlib
import json

if not __debug__:
    raise RuntimeError('Exact certificate checks require assertions enabled')
b = Path(__file__).resolve().parent
pins = {
    'coupling.json': '9f81b7bf93b258958fa3d6347631e50f8165e57ad32166547431a3be9ed26bec',
    'twist-action.json': 'b500e3b59ba262a81655d60441f31d6c7da74e022d308761f171cc7459f81e27',
    'twist-pf.json': '0bbe693ff7e0e3e9a47541a253027cb433e6b301b52c152a469289356c71fd92',
}
for name, digest in pins.items():
    assert hashlib.sha256((b / name).read_bytes()).hexdigest() == digest
c = json.loads((b / 'coupling.json').read_text())
a = json.loads((b / 'twist-action.json').read_text())
assert c['tag'] == 'parity-W25-24'
vertices = c['room']['vertices']
assert vertices[1:6] == [[1,0],[1,1],[2,2],[1,2],[1,3]]
assert c['offset_normals'][1] == c['offset_normals'][4] == [-1,0]
dim = c['offset_dimension']
assert len(c['offset_normals']) == c['walls'] == dim - 4
base = list(map(F, c['offset_base_point']))
assert base[1] == base[4] == -1
for i, normal in enumerate(c['offset_normals']):
    for point in (vertices[i], vertices[(i + 1) % c['walls']]):
        assert sum(F(x)*F(y) for x,y in zip(normal, point)) == base[i]

forms = []
for orientation in ('horizontal', 'vertical'):
    cores = a['core_period_derivatives'][orientation]
    assert len(cores) == 20
    for core in cores:
        assert len(core) == 2 and all(len(row) == dim for row in core)
        assert all(isinstance(x, (int, str)) and not isinstance(x, bool)
                   for row in core for x in row)
        forms.append([F(x) for row in core for x in row])
assert len(forms) == 40
saved_pf = json.loads((b / 'twist-pf.json').read_text())
pf = next(room for room in saved_pf['rooms'] if room['tag'] == c['tag'])
assert pf['horizontal_rows'] == pf['vertical_columns'] == 20
assert sum(pf['row_widths']) == sum(pf['column_lengths']) == pf['squares'] == 112
assert [sum(row) for row in pf['intersection_matrix']] == pf['row_widths']
assert [sum(row[j] for row in pf['intersection_matrix']) for j in range(20)] == pf['column_lengths']

# Bind every saved form to its own ordered ledger period, not just a count.
base_periods = [[sum(form[k*dim+j]*base[j] for j in range(dim))
                 for k in (0,1)] for form in forms]
assert base_periods[:20] == [[F(width), F(0)] for width in pf['row_widths']]
assert base_periods[20:] == [[F(0), F(height)] for height in pf['column_lengths']]
# Completeness still comes from the frozen cycles(r)/cycles(u) construction.
# This replay neither rebuilds an origami nor enumerates a cylinder.

# Boundary-of-U orientation: the I-copy crosscut runs from wall 4 to wall 1.
# hol(b0)=(2*(c4-c1),0); b1 is its quarter-turn image.
targets = []
for component in (0,1):
    target = [F(0)]*(2*dim)
    target[component*dim+1] = -2
    target[component*dim+4] = 2
    targets.append(target)

basis = {}
for index, vector in enumerate(forms):
    row = vector[:]
    coeff = [F(j == index) for j in range(len(forms))]
    for pivot, (old, recombination) in sorted(basis.items()):
        factor = row[pivot]
        row = [x-factor*y for x,y in zip(row, old)]
        coeff = [x-factor*y for x,y in zip(coeff, recombination)]
    pivot = next((i for i,x in enumerate(row) if x), None)
    if pivot is not None:
        factor = row[pivot]
        basis[pivot] = ([x/factor for x in row], [x/factor for x in coeff])

# One supplied ACTUAL offset velocity; evaluate every scalar core derivative.
delta = [F(0)]*dim
delta[4], delta[20] = F(-1), F(1)
scalar_rows = [form[k*dim:(k+1)*dim] for form in forms for k in (0,1)]
assert all(row[4] == row[20] for row in scalar_rows)
scalar_zero = all(sum(x*y for x,y in zip(row, delta)) == 0 for row in scalar_rows)
marks_fixed = all(x == 0 for x in delta[c['walls']:])
assert scalar_zero and marks_fixed
scalar_basis = {}
for vector in scalar_rows:
    row = vector[:]
    for pivot, old in sorted(scalar_basis.items()):
        factor = row[pivot]
        row = [x-factor*y for x,y in zip(row, old)]
    pivot = next((i for i,x in enumerate(row) if x), None)
    if pivot is not None:
        factor = row[pivot]
        scalar_basis[pivot] = [x/factor for x in row]


def analyze_targets(test_targets):
    """Compute membership and the plane certificate for these exact targets."""
    results = []
    for target in test_targets:
        residual = target[:]
        coeff = [F(0)]*len(forms)
        for pivot, (row, recombination) in sorted(basis.items()):
            factor = residual[pivot]
            residual = [x-factor*y for x,y in zip(residual, row)]
            coeff = [x+factor*y for x,y in zip(coeff, recombination)]
        member = not any(residual)
        certificate = None
        if member:
            assert [sum(coeff[j]*forms[j][i] for j in range(len(forms)))
                    for i in range(2*dim)] == target
        else:
            free = next(i for i,x in enumerate(residual) if x and i not in basis)
            dual = [F(0)]*(2*dim)
            dual[free] = F(1)
            for pivot, (row, _) in sorted(basis.items(), reverse=True):
                dual[pivot] = -sum(row[j]*dual[j] for j in range(pivot+1, 2*dim))
            assert all(sum(x*y for x,y in zip(form, dual)) == 0 for form in forms)
            value = sum(x*y for x,y in zip(target, dual))
            assert value != 0
            certificate = dict(linear_functional=list(map(str, dual)),
                               on_every_saved_axis_form='0', on_neck_form=str(value))
        results.append(dict(in_period_image=member, residual=list(map(str, residual)),
                            coefficients=list(map(str, coeff)), nonmembership_certificate=certificate))
    response = [[sum(target[k*dim+j]*delta[j] for j in range(dim))
                 for k in (0,1)] for target in test_targets]
    assert len(response) == 2
    determinant = response[0][0]*response[1][1] - response[0][1]*response[1][0]
    refuted = bool(scalar_zero and marks_fixed and determinant != 0)
    if refuted:
        assert all(not result['in_period_image'] for result in results)
    return results, response, determinant, refuted


results, response, determinant, refuted = analyze_targets(targets)
# Regression: replacing BOTH targets by actual saved core forms must stop
# claiming a neck-plane exclusion. It uses the same analysis/report boolean.
negative_results, negative_response, negative_det, negative_refuted = analyze_targets([forms[0], forms[20]])
assert all(result['in_period_image'] for result in negative_results)
assert negative_det == 0 and negative_response == [[0,0],[0,0]]
assert negative_refuted is False
out = dict(
    status='FROZEN_AXIS_PERIOD_IMAGE_CHECK_COMPLETE', tag=c['tag'], saved_axis_cores=len(forms),
    axis_coverage_binding=dict(squares=pf['squares'], horizontal_unit_annuli=len(forms[:20]),
        vertical_unit_annuli=len(forms[20:]), ordered_base_periods_verified=True,
        base_periods=[[str(x) for x in period] for period in base_periods],
        provenance='frozen cycles(r)/cycles(u); all form periods bound to the ordered ledger; no new geometry'),
    image_rank=len(basis), boundary_period_form_results=results, input_sha256=pins,
    scalar_axis_form_rank=len(scalar_basis), zero_scalar_rows=sum(not any(row) for row in scalar_rows),
    rows_touching_both_columns=sum(row[4] != 0 for row in scalar_rows),
    actual_axis_isoperiodic_deformation=dict(offset_velocity=list(map(str, delta)),
        all_scalar_axis_derivatives_zero=scalar_zero, marks_fixed=marks_fixed,
        neck_vector_responses=[[str(x) for x in row] for row in response],
        response_determinant=str(determinant)),
    homology_membership_proved=False, neck_axis_inclusion_refuted=refuted,
    neck_plane_axis_span_intersection=('zero, by actual-deformation full-rank vector response'
                                      if refuted else 'not established by this certificate'),
    negative_control=dict(targets='one saved horizontal and one saved vertical core form',
        membership=[r['in_period_image'] for r in negative_results],
        neck_axis_inclusion_refuted=negative_refuted),
    independent_review='LIVE_PEER_ACCEPT_WITH_CORRECTIONS; sign/result/ledger fixes replayed locally',
    universal_detection_proved=False, discovery_runs=0,
    scope='One frozen room. Full-rank actual period derivative certifies zero neck/axis intersection; positive homology membership, all-cylinder inclusion and actual-event detection are not proved.')
(b / 'pocket-structural-axis-forms.json').write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps(dict(status=out['status'], image_rank=len(basis),
    membership=[r['in_period_image'] for r in results], scalar_axis_form_rank=len(scalar_basis),
    neck_axis_inclusion_refuted=refuted, response_determinant=str(determinant),
    negative_control=out['negative_control'], discovery_runs=0), indent=2))
