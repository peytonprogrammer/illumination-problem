"""Reproduce the exact rectangle countercontrol; no optical search."""
from fractions import Fraction
from math import lcm
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
marks = []
for name, point, expected_order in [('S', (2, 2), 60), ('T', (4, 4), 30)]:
    coordinates = (Fraction(point[0], 20), Fraction(point[1], 24))
    order = lcm(*(v.denominator for v in coordinates))
    two_torsion = all((2*v).denominator == 1 for v in coordinates)
    assert order == expected_order and not two_torsion
    marks.append({'mark': name, 'primitive_torus_coordinates':
                  [str(v) for v in coordinates], 'order': order,
                  'two_torsion': two_torsion})
area = 4*10*12
primitive_degree = area // (20*24)
integer_degree = area
genus = 1
assert primitive_degree == 1 and 2*(primitive_degree-genus) == 0
result = {'status': 'EXACT_PRIMITIVE_MARK_COUNTERCONTROL_PASS',
          'primitive_degree': primitive_degree, 'genus': genus,
          'integer_torus_degree': integer_degree,
          'integer_torus_n2': 2*(integer_degree-genus), 'marks': marks,
          'source_sha256': hashlib.sha256(
              (HERE/'pillowcase-marked-guard.md').read_bytes()).hexdigest(),
          'whole_goal_complete': False}
(HERE/'pillowcase-marked-guard-check.json').write_text(
    json.dumps(result, indent=2)+'\n')
print(json.dumps(result))
