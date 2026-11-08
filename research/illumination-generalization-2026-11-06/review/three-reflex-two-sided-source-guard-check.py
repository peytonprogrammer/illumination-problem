"""Prescribed K1R01 prefix interval audit; no other room/direction replay."""
import ast,hashlib,json
from pathlib import Path
from fractions import Fraction as Q
ROOT=Path('.context/illumination-generalization-2026-11-06')
OUT=ROOT/'review/three-reflex-two-sided-source-guard-check.json'
geo=ROOT/'review/resumed-exact-check.py'
rep=ROOT/'review/three-reflex-coprime-independent-check.py'
pinned=[geo,rep,ROOT/'review/three-reflex-two-sided-return-independent.json',ROOT/'review/three-reflex-two-sided-source-crossing.md']
pins={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in pinned}
names={'vec','det','dot','edges','on','location','intersect','simple','path_check','fold'}
ns={'Q':Q,'F':Q}
exec(compile(ast.Module(body=[f for f in ast.parse(geo.read_text()).body if isinstance(f,ast.FunctionDef) and f.name in names],type_ignores=[]),'<existing reviewer geometry>','exec'),ns)
fn=next(f for f in ast.parse(rep.read_text()).body if isinstance(f,ast.FunctionDef) and f.name=='replay_actual')
removed=[n for n in fn.body if isinstance(n,ast.Assert) and ast.unparse(n.test)=='len(roofs) == len(horizontal) == 1']
assert len(removed)==1
fn.body=[n for n in fn.body if n not in removed]
runner={'Q':Q,'ns':ns}
exec(compile(ast.Module(body=[fn],type_ignores=[]),'<existing reviewer replay; single-roof scope assertion omitted>','exec'),runner)
poly=[(12,1),(12,4),(28,4),(28,3),(20,3),(20,0),(32,0),(32,5),(0,5),(0,1)]
S=(8,4);T=(24,2);h=4;c=3;H=5;w=28;G=h-c;period=192
slope=Q(369232,1923);eps=slope-period;D=Q(3846)
result=runner['replay_actual'](poly,S,T,slope,D)
path=result['path'];events=result['events']
pathhash=hashlib.sha256(json.dumps(path,default=str,separators=(',',':')).encode()).hexdigest()
assert pathhash=='a4f18c0022a6ed0149887720e05bf978f25c69a9251a0b0e128d02b4bc706e12'
elapsed=Q(0);cap=[]
for p0,p1 in zip(path,path[1:]):
 if p0[1]>h>=p1[1]:
  when=elapsed+p0[1]-h
  x=p0[0]+(h-p0[1])*(p1[0]-p0[0])/(p1[1]-p0[1])
  if w<x<32:cap.append((when,x,1 if p1[0]>p0[0] else -1))
 elapsed+=abs(p1[1]-p0[1])
DS,xh,sign=cap[-1]
assert DS.denominator==1 and sign==-1
C=xh+eps*DS;alpha=C-w
assert C.denominator==1 and alpha>0
q0=(xh-w)/eps-G
assert 0<q0<2*c
z0=1/eps;gate_lo=(DS+G)/alpha;gate_hi=(DS+G+2*c)/alpha
assert 2*H<gate_lo<z0<gate_hi
elo=1/gate_hi;ehi=1/gate_lo
lower=elo;upper=ehi;lower_info={'kind':'future_gate_boundary'};upper_info={'kind':'future_gate_boundary'}
sx=sy=1;ox=oy=0;entry=('h',S[1]);prefix_events=0;roots=0
walls=ns['edges'](poly)
def boundary_time(boundary,tau):
 kind,val=boundary
 return (val-S[0])/tau if kind=='v' else val-S[1]
for event in [e for e in events if e['time']<DS]+[None]:
 if event is None:
  exit_boundary=('h',S[1]+DS)
 else:
  p=event['point']
  wall=next((a,b) for a,b in walls if ns['on'](a,b,p))
  vertical=wall[0][0]==wall[1][0]
  exit_boundary=('v',sx*p[0]+ox) if vertical else ('h',sy*p[1]+oy)
 for j,(cx,cy) in enumerate(poly):
  X=sx*cx+ox;Y=sy*cy+oy;tv=Q(Y-S[1])
  if tv<=0 or tv>DS:continue
  tau=Q(X-S[0],tv);e=tau-period
  if not elo<e<ehi:continue
  if not boundary_time(entry,tau)<=tv<=boundary_time(exit_boundary,tau):continue
  assert e!=eps,'Accepted witness cannot pass a true corner'
  roots+=1
  info={'kind':'developed_true_corner','physical_corner_index':j,'physical_corner':poly[j],'prefix_reflections_before_copy':prefix_events,'developed_corner':[X,Y],'developed_time':tv,'slope':tau,'epsilon':e,'z':1/e}
  if e<eps and e>lower:lower=e;lower_info=info
  if e>eps and e<upper:upper=e;upper_info=info
 if event is None:break
 if vertical:
  X=exit_boundary[1];sx=-sx;ox=2*X-ox
 else:
  Y=exit_boundary[1];sy=-sy;oy=2*Y-oy
 entry=exit_boundary;prefix_events+=1
# Reciprocal coordinate reverses parameter order.
zlo,zhi=1/upper,1/lower
qlo,qhi=alpha*zlo-DS-G,alpha*zhi-DS-G
L=w-T[0];M=2*max(T[1],c-T[1]);theta_span=(alpha+L)*(zhi-zlo)
for p in pinned:assert hashlib.sha256(p.read_bytes()).hexdigest()==pins[str(p)]
out={'status':'PASS_ONE_PRESCRIBED_PREFIX_GUARD_PROFILE','scope':'One existing accepted ray, no parameter or room replay scan. Exact corner-root analysis of its fixed prefix; not universal source availability.','slope':slope,'epsilon':eps,'first_target_time':D,'path_sha256':pathhash,'reflections':result['reflections'],'final_negative_cap_time':DS,'final_negative_cap_x':xh,'source_C':C,'alpha':alpha,'q_at_witness':q0,'z_at_witness':z0,'full_gate_z_interval':[gate_lo,gate_hi],'prefix_reflections':prefix_events,'qualified_corner_roots_inside_gate':roots,'epsilon_component':[lower,upper],'z_component':[zlo,zhi],'q_component':[qlo,qhi],'lower_epsilon_obstruction':lower_info,'upper_epsilon_obstruction':upper_info,'paired_target_max_gap':M,'source_component_theta_span':theta_span,'SC01_sufficient_width_passes':theta_span>M,'source_pins':pins,'full_goal_complete':False}
OUT.write_text(json.dumps(out,default=str,indent=2)+'\n')
print(json.dumps(out,default=str,indent=2))
