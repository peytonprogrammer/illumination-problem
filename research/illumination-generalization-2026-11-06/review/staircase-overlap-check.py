"""Prescribed independent actual-wall check of the peer overlap fixture."""
from pathlib import Path
from fractions import Fraction as F
import ast,json,hashlib
HERE=Path(__file__).resolve().parent
source=HERE/'staircase-floor-check.py';tree=ast.parse(source.read_text());ns={'F':F}
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef)],type_ignores=[]),str(source),'exec'),ns)
V=[tuple(map(F,p)) for p in [(0,0),(10,0),(10,3),(4,3),(4,4),(3,4),(3,10),(0,10)]]
path=[(F(9),F(1))]+[(F(x),F(y,11)) for x,y in [(10,13),(0,33),(4,41),(0,49),(3,55),(0,61),(3,67),(0,73),(3,79),(0,85),(3,91),(0,97)]]+[(F(1),F(9))]
result=ns['verify']('peer-new-overlap-geometry-fixed-witness',V,path)
assert result['contacts']==12 and result['horizontal_contacts']==0
out={'status':'INDEPENDENT_PRESCRIBED_OVERLAP_WITNESS_PASS','result':result,'whole_goal_complete':False,'verification':'Own pure finite-wall verifier; no peer code executed','source_sha256':{p:hashlib.sha256((HERE/p).read_bytes()).hexdigest() for p in ('staircase-overlap-check.py','staircase-floor-check.py','../construction/staircase-overlap-supplement.md')}}
(HERE/'staircase-overlap-check.json').write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in result.items() if k!='path'})
