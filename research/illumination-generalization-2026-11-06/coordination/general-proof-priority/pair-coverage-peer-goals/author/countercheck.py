"""One prescribed peer countercontrol; no discovery or group enumeration."""
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
import ast
import hashlib
import json

HERE = Path(__file__).resolve().parent
source = HERE.parents[3] / 'review/resumed-exact-check.py'
needed = {'vec', 'det', 'dot', 'edges', 'on', 'location', 'intersect', 'simple', 'path_check'}
tree = ast.parse(source.read_text())
ns = {'Q': Q}
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in needed], type_ignores=[]), str(source), 'exec'), ns)
P = [(0,0), (8,0), (8,4), (4,4), (4,8), (0,8)]
p, q = (6,2), (2,6)
ns['simple'](P)
assert ns['location'](P,p) == ns['location'](P,q) == 1
assert all(v % 2 == 0 for z in (p,q) for v in z)
regular = [(0,0), (8,0), (8,4), (4,8), (0,8)]
assert Counter(tuple(v % 8 for v in z) for z in regular) == Counter({(0,0):3, (0,4):1, (4,0):1})
assert tuple(v % 8 for v in (4,4)) == (4,4)
assert all(2*v % 8 == 0 for z in P for v in z)
periods = [(8,0), (0,8)]
assert ns['det'](*periods) == 64
C, R, U = (2,2), (6,2), (2,6)
assert all(ns['location'](P,z) == 1 for z in (C,R,U))
assert ns['location'](P,(6,6)) == -1
assert tuple((q[i]-p[i]) % 8 for i in (0,1)) == (4,4)
assert tuple((C[i]-R[i]) % 8 for i in (0,1)) == (4,0)
assert tuple((C[i]-U[i]) % 8 for i in (0,1)) == (0,4)
assert tuple((U[i]-R[i]) % 8 for i in (0,1)) == (4,4)
assert ns['on'](R,U,(4,4))
contact = (0,5)
checked = ns['path_check'](P,[p,contact,q])
assert checked == {'wall_leg_guards':12, 'reflections':1}
assert ns['vec'](p,contact) == (-6,3)
assert ns['vec'](contact,q) == (2,1)
assert ns['on'](p,contact,(2,4))
out = {
    'status':'PASS_ONE_PRESCRIBED_AUTHOR_COUNTERCHECK',
    'scope':'Hand full-group obstruction plus prescribed pure geometry/path check; no orbit enumeration',
    'room':P, 'source':p, 'target':q, 'path':[p,contact,q], **checked,
    'period_basis_determinant':64,
    'period_lattice':'exact8Z2 by hand gluing/core proof, not by determinant check alone',
    'candidate_positions':[C,R,U],
    'new_discovery':False, 'qualifying_dark_pair':False,
    'full_universal_goal_complete':False,
    'checker_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
}
(HERE / 'countercheck.json').write_text(json.dumps(out,indent=2) + '\n')
print(json.dumps(out,indent=2))
