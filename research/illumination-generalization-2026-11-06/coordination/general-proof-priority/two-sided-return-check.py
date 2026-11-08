"""One predeclared K1R01 affine-image replay. No direction or room search."""
import ast, hashlib, json
from fractions import Fraction as Q
from pathlib import Path

ROOT=Path('.context/illumination-generalization-2026-11-06')
HERE=ROOT/'coordination/general-proof-priority'
geometry=ROOT/'review/resumed-exact-check.py'
replay=ROOT/'review/three-reflex-coprime-independent-check.py'
sources=[geometry,replay,ROOT/'construction/weighted-return-argument-01.md',ROOT/'review/weighted-return-wr01-independent.md',ROOT/'construction/general-spiral-existence-left-return-proof.md',ROOT/'review/three-reflex-nonemptiness-control-union.md']
pins={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
names={'vec','det','dot','edges','on','location','intersect','simple','path_check','fold'}
ns={'Q':Q,'F':Q}
tree=ast.parse(geometry.read_text())
exec(compile(ast.Module(body=[f for f in tree.body if isinstance(f,ast.FunctionDef) and f.name in names],type_ignores=[]),str(geometry),'exec'),ns)
fn=next(f for f in ast.parse(replay.read_text()).body if isinstance(f,ast.FunctionDef) and f.name=='replay_actual')
removed=[n for n in fn.body if isinstance(n,ast.Assert) and ast.unparse(n.test)=='len(roofs) == len(horizontal) == 1']
assert len(removed)==1
fn.body=[n for n in fn.body if n not in removed]
runner={'Q':Q,'ns':ns}
exec(compile(ast.Module(body=[fn],type_ignores=[]),str(replay)+' [pure function; one-roof assertion omitted]','exec'),runner)
poly=[(12,1),(12,4),(28,4),(28,3),(20,3),(20,0),(32,0),(32,5),(0,5),(0,1)]
S=(8,4);T=(24,2);slope=Q(369232,1923);D=Q(3846)
assert slope-192==Q(16,1923)<Q(1,102)
result=runner['replay_actual'](poly,S,T,slope,D)
path=result['path'];events=result['events']
right_down=[];right_up=[]
for p0,p1 in zip(path,path[1:]):
 if p0[1]>4>=p1[1]:
  x=p0[0]+(4-p0[1])*(p1[0]-p0[0])/(p1[1]-p0[1])
  if 28<x<=32:right_down.append(x)
 if p0[1]<4<=p1[1]:
  x=p0[0]+(4-p0[1])*(p1[0]-p0[0])/(p1[1]-p0[1])
  if 28<x<=32:right_up.append(x)
floors=[e for e in events if e['point'][1]==0]
assert len(floors)>10 and len(right_down)>10
first=right_down[0];rho=first-28;eps=slope-192
assert 0<rho<2*eps
for j in range(11):assert right_down[j]==28+rho+10*j*eps
# Both bottom target-height crossings in the first ten lower excursions.
for j in range(10):
 assert 28<28+rho+(10*j+2)*eps<29
 assert 28<28+rho+(10*j+6)*eps<29
assert all(hashlib.sha256(p.read_bytes()).hexdigest()==pins[str(p)] for p in sources)
out={'status':'PASS_ONE_PREDECLARED_ACTUAL_PATH','source':S,'target':T,'slope':str(slope),'epsilon':str(eps),'actual_first_target_time':str(result['actual_target_time']),'actual_reflections':result['reflections'],'bottom_floor_reflections':len(floors),'right_down_entries':len(right_down),'right_up_entries':len(right_up),'first_right_x':str(first),'first_right_overshoot':str(rho),'first_10_right_circuit_phase_checks':'PASS','path_sha256':hashlib.sha256(json.dumps(path,default=str,separators=(',',':')).encode()).hexdigest(),'source_pins':pins,'extraction_change':'Removed only the assertion len(roofs)==len(horizontal)==1; all first-wall, corner, exact-first-target-time and full path_check guards retained. Historical main code not executed.','scope':'One previously illuminated room/pair and one exactly prescribed affine-image direction; no new room coverage or universal existence.'}
(HERE/'two-sided-return-check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='source_pins'},indent=2))
