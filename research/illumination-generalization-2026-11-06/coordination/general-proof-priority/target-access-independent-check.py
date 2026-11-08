"""Eight predeclared formula controls in ONE old room. No discovery or scan."""
import ast,json,hashlib
from pathlib import Path
from fractions import Fraction as Q
from math import floor
ROOT=Path('.context/illumination-generalization-2026-11-06');HERE=ROOT/'coordination/general-proof-priority'
inputs=json.loads((HERE/'target-access-independent-inputs.json').read_text())
for p in inputs['pins']:assert hashlib.sha256(Path(p['path']).read_bytes()).hexdigest()==p['sha256'],p['path']
geometry=ROOT/'review/resumed-exact-check.py';replay=ROOT/'review/three-reflex-coprime-independent-check.py'
ns={'Q':Q,'F':Q}
names={'vec','det','dot','edges','on','location','intersect','simple','path_check','fold'}
exec(compile(ast.Module(body=[f for f in ast.parse(geometry.read_text()).body if isinstance(f,ast.FunctionDef) and f.name in names],type_ignores=[]),str(geometry),'exec'),ns)
f=next(f for f in ast.parse(replay.read_text()).body if isinstance(f,ast.FunctionDef) and f.name=='replay_actual')
removed=[n for n in f.body if isinstance(n,ast.Assert) and ast.unparse(n.test)=='len(roofs) == len(horizontal) == 1'];assert len(removed)==1
f.body=[n for n in f.body if n not in removed]
runner={'Q':Q,'ns':ns};exec(compile(ast.Module(body=[f],type_ignores=[]),str(replay)+' [pure first-hit function; one-roof assertion omitted]','exec'),runner)
poly=[(12,1),(12,4),(28,4),(28,3),(20,3),(20,0),(32,0),(32,5),(0,5),(0,1)]
# A single actual Euclidean reflection preserves every wall and specular law.
reflected=[(Q(x),Q(-y)) for x,y in poly]
G=1;c=3;h=4;w=28;l=20;P=192;v=2
cases=[('safe_down',24,Q(1,16),-1,-1),('down_alignment_other_up',24,Q(4,43),-1,1),('up_alignment_other_down',24,Q(4,47),-1,-1),('equal_w_floor',28,Q(1,16),None,1),('right_positive_floor',30,Q(1,16),None,1),('right_negative_floor',30,Q(1,16),None,-1),('postturn_legal_up',24,Q(1,16),1,1),('postturn_corner_down',24,Q(1,16),1,-1)]
rows=[]
for label,t,e,kappa,sigma in cases:
 assert 0<e<Q(1,10)
 if t<w:
  L=(w-l)+kappa*(t-l)
  z=(Q(L)/e-c-sigma*v)/(2*c)
  assert z.denominator!=1
  m=floor(z)+1
  F=2*c*m+c+sigma*v
  d=e*F-L;xe=Q(w)+d;xh=xe+G*e
  assert 0<d<2*c*e
  horizontal=-1;D=G+F
  if label=='down_alignment_other_up':assert ((Q(w-t)/e-c+v)/(2*c)).denominator==1
  if label=='up_alignment_other_down':assert ((Q(w-t)/e-c-v)/(2*c)).denominator==1
 else:
  horizontal=-1 if t==w else sigma
  D=h+v
  xh=Q(t)-horizontal*D*e
  m=0
 S=(xh,Q(-h));T=(Q(t),Q(-v));slope=horizontal*(P+e)
 expected_corner=label=='postturn_corner_down'
 try:
  result=runner['replay_actual'](reflected,S,T,slope,Q(D))
  assert not expected_corner,'Excluded branch unexpectedly reached target'
  row={'label':label,'status':'EXACT_FIRST_TARGET_AND_ALL_ORIGINAL_WALL_GUARDS_PASS','epsilon':str(e),'target':[t,v],'x_h':str(xh),'incoming_vx_sign':horizontal,'m':m,'actual_first_target_time':str(result['actual_target_time']),'reflections':result['reflections'],'finite_wall_leg_guards':result.get('clauses',None),'bottom_floor_contacts':sum(x['point'][1]==0 for x in result['events']),'path_sha256':hashlib.sha256(json.dumps(result['path'],default=str,separators=(',',':')).encode()).hexdigest()}
 except AssertionError as exc:
  if not expected_corner:raise
  tb=exc.__traceback__
  while tb.tb_next:tb=tb.tb_next
  local=tb.tb_frame.f_locals
  assert tb.tb_frame.f_code.co_name=='replay_actual'
  # This same gate coincides with a safe branch: FIRST T is before the
  # corner in the nominated later postturn continuation. Keep that prefix.
  assert local['path'][-1]==T and local['elapsed']==66
  earlier=runner['replay_actual'](reflected,S,T,slope,Q(66))
  # Continue the SAME physical ray after its first T. Its actual arrival
  # velocity is (-tau,+1) in the original coordinates.
  try:
   runner['replay_actual'](poly,(Q(24),Q(2)),(Q(8),Q(4)),slope,Q(65))
   raise AssertionError('Predicted continuation corner was not detected')
  except AssertionError as continuation:
   tb2=continuation.__traceback__
   while tb2.tb_next:tb2=tb2.tb_next
   loc2=tb2.tb_frame.f_locals
   assert tb2.tb_frame.f_code.co_name=='replay_actual'
   assert loc2['p']==(Q(20),Q(0))
   assert loc2['elapsed']+loc2['dt']==64
  row={'label':label,'status':'EARLIER_LEGAL_TARGET_RETAINED_LATER_POSTTURN_CORNER_CONFIRMED','epsilon':str(e),'target':[t,v],'x_h':str(xh),'actual_first_target_time':'66','first_target_reflections':earlier['reflections'],'excluded_later_continuation_corner':[20,0],'actual_corner_time_from_gate':'130','nominated_later_target_time':str(D),'clarification':'Only the literal later postturn branch is corner-invalid. The same incoming state already succeeds via a safe branch; do not discard that entry state.'}
 rows.append(row)
for p in inputs['pins']:assert hashlib.sha256(Path(p['path']).read_bytes()).hexdigest()==p['sha256'],p['path']
out={'status':'PASS_EIGHT_PRESCRIBED_CONTROLS_WITH_POSTTURN_EARLIER_TARGET_QUALIFICATION','rows':rows,'scope':'One existing integral room, eight predeclared symbolic boundary controls. Universal claims rest on independent hand proof, not samples.','input_pins_unchanged':True,'shared_computational_dependency':'Existing reviewer pure exact earliest-wall and path_check functions; only their obsolete one-roof assertion omitted. Whole y-reflection is a genuine isometry. Historical main blocks and coordinator prior checker not run.','geometry_pin':{'path':str(geometry),'sha256':hashlib.sha256(geometry.read_bytes()).hexdigest()},'replay_pin':{'path':str(replay),'sha256':hashlib.sha256(replay.read_bytes()).hexdigest()},'new_search':False,'new_room':False,'new_engine':False,'harness_correction':'The last predeclared ray first reaches T at66, then its continued trajectory reaches the predicted corner at130 before the nominated later T at194. Initial exact-D194 assertion failed because it ignored the earlier success; same eight inputs retained, with one same-ray continuation check.'}
(HERE/'target-access-independent-check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
