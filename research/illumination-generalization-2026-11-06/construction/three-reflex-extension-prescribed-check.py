"""Prescribed TR04 formula checks; no search, disabled assertion, or frozen edit."""
from pathlib import Path
from fractions import Fraction as F
import ast
import hashlib
import json
import runpy


base = Path(__file__).with_name('three-reflex-tall-prescribed-check.py')
namespace = runpy.run_path(str(base), run_name='tr03_frozen_dependency')
tree = ast.parse(base.read_text())
function = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == 'phases')
geometry_assert = next(node for node in function.body if isinstance(node, ast.Assert))
old_guard = ast.unparse(geometry_assert.test)
assert old_guard == '0 < a < ell < w < A and 0 < b < c < h < H'
new_guard = '0 < a < w < A and 0 < ell < w and 0 < b < h < H and 0 < c < h and (a < ell or c < b)'
geometry_assert.test = ast.parse(new_guard, mode='eval').body
# Only widen the one explicitly proved geometry precondition. Every fold,
# interval, actual-wall, corner, velocity and first-target assertion remains.
module = ast.fix_missing_locations(ast.Module(body=[function], type_ignores=[]))
exec(compile(module, str(Path(__file__)) + ':generalized_geometry', 'exec'), namespace)
construct = namespace['phases']

fixtures = [
    ('b-above-c', (4,12,20,28,12,8,20,680), (2,14), (14,2)),
    ('bottom-left-of-source', (12,4,20,28,12,8,20,680), (10,14), (6,2)),
    ('equal-a-l-disjoint-heights', (8,8,20,28,12,8,20,680), (6,14), (10,2)),
    ('equal-b-c-disjoint-columns', (4,12,20,28,8,8,20,680), (2,10), (14,2)),
    ('upper-cut-new-order', (12,4,20,28,12,8,20,680), (20,679), (6,7)),
]
rows = []
for label, geometry, source, target in fixtures:
    result = construct(geometry, source, target)
    result['label'] = label
    rows.append(result)

# A new sufficiently-wide original room, evaluated in its exact transpose.
original = tuple(map(F, (4,12,20,680,4,8,20,28)))
a, ell, w, A, b, c, h, H = original
transposed = (c,b,h,H,ell,a,w,A)
source, target = (F(2),F(6)), (F(14),F(2))
R, L = A-w, (A-w)/(2*c)
Nv = namespace['ceil'](L*h/(2*a))+namespace['ceil'](L*h/(2*R))+3
delta_v = L/Nv
assert H < c+2*A/delta_v  # The old original-orientation tall condition fails.
Rt, Lt = H-h, (H-h)/(2*a)
Nh = namespace['ceil'](Lt*w/(2*c))+namespace['ceil'](Lt*w/(2*Rt))+3
delta_h = Lt/Nh
assert A >= a+2*H/delta_h
# Swap labels after transposition to use the lower/lowest cross chart.
result = construct(transposed, (target[1],target[0]), (source[1],source[0]))
result.update(label='new-wide-room-via-transposition', original_geometry=original,
              original_source=source, original_target=target,
              old_tall_condition=False, transposed_tall_condition=True,
              label_order_reversed=True)
rows.append(result)

output = {
    'status':'PASS',
    'method':'Reused frozen prescribed formula and ALL physical guards; replaced only its geometry precondition in memory with the explicitly proved TR04 guard. No author source was modified or assertion disabled.',
    'frozen_dependency_sha256':hashlib.sha256(base.read_bytes()).hexdigest(),
    'old_geometry_guard':old_guard,
    'new_geometry_guard':new_guard,
    'prescribed_cases':rows,
    'independent_implementation':False,
    'search_used':False,
    'whole_r3_complete':False,
    'whole_goal_complete':False,
}
Path(__file__).with_suffix('.json').write_text(json.dumps(output, indent=2, default=str)+'\n')
print(json.dumps({'status':'PASS','prescribed_cases':len(rows),
                  'actual_reflections':sum(row['reflections'] for row in rows),
                  'new_wide_discriminator':True}))
