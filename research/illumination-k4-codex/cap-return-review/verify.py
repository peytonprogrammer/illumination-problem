"""Exact replay of one frozen saved witness; no trajectory generation."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import runpy

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
checker_path = ROOT/'lower-bound-proof-audit/full-replay/guard-checker.py'
checker = runpy.run_path(str(checker_path))
rec = json.loads((HERE/'lookup.json').read_text())
assert rec['status'] == 'MATCH'
path = [tuple(F(*v) for v in p) for p in rec['path']]
assert path[0] == (0,0) and path[-1] == (2,2)
room = checker['triangles'](rec['room'])
U,Z = checker['triangles'](rec['U']),checker['triangles'](rec['Z'])
assert U <= room and not Z & room
need,absent = checker['path_requirements'](path)
assert need <= room and not absent & room
assert checker['incident'](path[0]) <= room
assert checker['incident'](path[-1]) <= room
for p in path[1:-1]:
    if all(x.denominator == 1 for x in p):
        # Integer-point contacts must still be smooth, verified by bounce().
        assert p != (1,1)

# Independent closed-form description of this one itinerary.
d = F(2,11)
assert F(3,17) < d < F(4,21)
prefix = [(0,0),(-d,-1),(-3*d,1),(-5*d,-1),
          (-1,1/d-6),(7*d-2,1),(9*d-2,-1),(11*d-2,1)]
assert path[:8] == prefix
u = 13*d-2
assert 0 < u < 1-2*d
# Three lower-cap bounces: diagonal, vertical, diagonal.
lower = [((u+d)/(1+d),(u+d)/(1+d)-2),
         (F(0),u+d-2),
         ((u+d)/(1-d),(u+d)/(1-d)-2)]
assert path[8:11] == lower
lower_exit = (u+2*d,F(-1))
z = lower_exit[0]+4*d
assert z == 19*d-2 and 1 < z and z+2*d < 2
# Three upper-cap bounces: diagonal, vertical, diagonal.
upper = [((z-d)/(1-d),(z-d)/(1-d)+2),
         (F(2),2+z+d),
         ((z+3*d)/(1+d),(z+3*d)/(1+d)+2)]
assert path[11:14] == upper
assert z+3*d == 2
summary = dict(status='PASS',reflections=len(path)-2,
               required_triangles=len(need),absent_triangles=len(absent),
               required_tiles=sorted(need),forbidden_tiles=sorted(absent),
               endpoints=[[0,0],[2,2]],initial_direction=[-2,-11],
               cap_hits={'bottom':3,'top':3,'east':0,'left':0},
               parameter_interval=['3/17','4/21'],closing_parameter='2/11',
               closing_equation='22*d-2=2',
               checker_sha256=hashlib.sha256(checker_path.read_bytes()).hexdigest(),
               source_guard=rec['source'],source_guard_line=rec['line'],
               scope='One frozen witness replay and analytic itinerary identities, not new path discovery or all-completion theorem.')
(HERE/'verify.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
