"""One old ray, one predeclared corner image; no alternate ray execution."""
from pathlib import Path
from fractions import Fraction as Q
import json,hashlib
R=Path('.context/illumination-generalization-2026-11-06');C=R/'coordination/general-proof-priority'
inputs=json.loads((C/'target-access-source-cut-inputs.json').read_text())
for p in inputs['pins']:assert hashlib.sha256(Path(p['path']).read_bytes()).hexdigest()==p['sha256']
# Reuse only the setup extracting the accepted pure reviewer geometry/ray
# routine. No target-tail cases or historical main code execute here.
driver=C/'target-access-independent-check.py';env={}
exec(compile(driver.read_text().split('poly=[',1)[0],str(driver)+' [pure setup only]','exec'),env)
run=env['runner']['replay_actual'];ns=env['ns']
poly=[(12,1),(12,4),(28,4),(28,3),(20,3),(20,0),(32,0),(32,5),(0,5),(0,1)]
tau=Q(369232,1923);eps=tau-192
result=run(poly,(8,4),(24,2),tau,Q(3846));events=result['events'];path=result['path']
last=None;elapsed=Q(0)
for start,end in zip(path,path[1:]):
 if start[1]>4>=end[1] and end[0]<start[0]:
  when=elapsed+start[1]-4
  x=start[0]+(4-start[1])*(end[0]-start[0])/(end[1]-start[1])
  if 28<x<32:last=(when,x)
 elapsed+=abs(end[1]-start[1])
assert last==(Q(3364),Q(53864,1923)),last
DS,xh=last;alpha=xh+eps*DS-28;assert alpha==28
sx=sy=1;ox=oy=0;entry=('h',4);matches=[];n=0
walls=ns['edges'](poly);corner_tau=Q(115397,601)
def moment(bound):return Q(bound[1]-8)/corner_tau if bound[0]=='v' else Q(bound[1]-4)
for event in [e for e in events if e['time']<DS]+[None]:
 if event is None:exit=('h',4+DS)
 else:
  point=event['point'];a,b=next((a,b) for a,b in walls if ns['on'](a,b,point))
  vertical=a[0]==b[0]
  exit=('v',sx*point[0]+ox) if vertical else ('h',sy*point[1]+oy)
 image=(sx*28+ox,sy*4+oy)
 if image==(461596,2408) and moment(entry)<=2404<=moment(exit):
  matches.append({'copy_after_reflections':n,'image':list(map(int,image)),'entry_time_at_corner_slope':str(moment(entry)),'corner_time':'2404','exit_time_at_corner_slope':str(moment(exit))})
 if event is None:break
 if vertical:sx=-sx;ox=2*exit[1]-ox
 else:sy=-sy;oy=2*exit[1]-oy
 entry=exit;n+=1
assert matches and n==39844
assert Q(461596-8,2408-4)==corner_tau
assert corner_tau-192==Q(5,601)
z0=1/eps;lo=(DS+1)/alpha;hi=(DS+1+6)/alpha;cut=Q(601,5)
assert lo<z0<cut<hi
span_bound=(alpha+4)*(cut-lo)
assert span_bound==Q(24,35)<4
assert (tau-corner_tau)*2404==Q(4,1923)
for p in inputs['pins']:assert hashlib.sha256(Path(p['path']).read_bytes()).hexdigest()==p['sha256']
out={'status':'PASS_KNOWN_SOURCE_PREFIX_CUT_AND_WIDTH_UPPER_BOUND','ray':'369232/1923','first_target_time':'3846','reflections':result['reflections'],'wall_leg_guards':result['wall_leg_guards'],'source_cap_time':str(DS),'source_cap_x':str(xh),'alpha':str(alpha),'prefix_reflections':n,'qualified_known_corner_occurrences':matches,'geometric_gate_z_interval':[str(lo),str(hi)],'witness_z':str(z0),'known_forbidden_z':str(cut),'source_component_theta_span_upper_bound':str(span_bound),'SC01_required_strict_span':'4','scope':'The connected fixed-word source component through the known witness is contained in (3365/28,601/5), so its span cannot meet SC01. Full maximal interval completeness is not claimed from this one cut. No other source word or ray excluded.','input_pins_unchanged':True,'new_direction_executed':False,'shared_dependency':'Existing exact reviewer replay/path_check reused; independent selected-corner unfolding and component upper-bound proof.','serialization_note':'The first identical run passed every mathematical assertion but failed to serialize integer-valued Fraction image coordinates; converted those coordinates to integers and reran the same prescribed input.'}
(C/'target-access-source-cut-check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
