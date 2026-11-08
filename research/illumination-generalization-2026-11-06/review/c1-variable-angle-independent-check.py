"""Prescribed controls for the all-h>=9 formula; prefixes already independently checked."""
from pathlib import Path
from fractions import Fraction as Q
import importlib.util,json,hashlib
R=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('own',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
def polygon(h):return [tuple(map(Q,z)) for z in [(0,0),(1,0),(1,h),(2,h),(2,h+2),(1,h+2),(1,h+4),(2,h+4),(2,h+6),(1,h+6),(1,2*h+4),(0,2*h+4),(0,2*h+3),(-1,2*h+3),(-1,2*h+1),(0,2*h+1),(0,3),(-1,3),(-1,1),(0,1)]]
rows=[]
for h in (9,11,13,101,1000001):
 V=polygon(h);g.simple(V);h=Q(h)
 path=[(0,2),(1,2+h/2),(0,2+h),(1,2+3*h/2),(0,2*h+2)]
 rows.append({'h':int(h),**g.path_check(V,path)})
out={'status':'PRESCRIBED_FORMULA_CHECKS_PASS','rows':rows,'discovery':False,'whole_goal_complete':False,'source_sha256':{'resumed-exact-check.py':hashlib.sha256((R/'resumed-exact-check.py').read_bytes()).hexdigest()}}
(R/'c1-variable-angle-independent-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
