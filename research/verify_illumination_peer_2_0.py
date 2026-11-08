"""Independently check peer rays and replay Codex's complete (2,0) model."""
from collections import Counter
import hashlib,json,time
from pathlib import Path
from ortools.sat.python import cp_model
from illumination_geometry import owners_of
from illumination_sector_paths import verify
from illumination_three_two_star_bound import validate
from audit_illumination_three_two_star import touched_tiles
from search_illumination_three_two_star import make_model,add_guard,room_from
from search_illumination_one_exception import tile_facts
from illumination_triple_cell_sets import outside_sets,refine_connected_cells

BASE=Path(__file__).parent
OUT=BASE/'three-triples'
PATH=OUT/'peer-2-0-audit.json'
TARGET=(2,0)

def main():
 start=time.monotonic();data=json.loads((OUT/'peer-2-0-rays.json').read_text())
 model,ts,x,bounded,terms=make_model(TARGET);owners=owners_of(ts)
 refine_connected_cells(TARGET,model,terms)
 keys=set();base_keys=set();pass1_keys=set();stats=Counter();cache={};witness_by_key={}
 result=dict(status='RUNNING',stats={},partition=[],source_sha256=hashlib.sha256((OUT/'peer-2-0-rays.json').read_bytes()).hexdigest())
 def save(event):
  result.update(stats=dict(stats),guards=len(keys),seconds=time.monotonic()-start)
  tmp=PATH.with_suffix('.tmp');tmp.write_text(json.dumps(result,indent=2)+'\n');tmp.replace(PATH)
  print(json.dumps(dict(event=event,stats=dict(stats),guards=len(keys),seconds=round(time.monotonic()-start,2))),flush=True)
 def checked(room,w,kind):
  verify(room,w);stats['exact_paths']+=1
  selected={tuple(sorted(map(tuple,t))) for t in room['triangles']};assert selected<=set(ts)
  compiled=dict(tile_facts(ts,owners,w,room))
  pk=json.dumps(w['path']);required=cache.get(pk)
  if required is None:required=touched_tiles(ts,w);cache[pk]=required
  assert required<=compiled.keys()
  assert all(compiled[i]==int(ts[i] in selected) for i in required)
  facts=tuple(sorted((i,int(ts[i] in selected)) for i in required));assert facts
  # The independently intersected closed triangles themselves are sufficient:
  # every cell touched by a segment (including absent wall-side cells) is fixed.
  if stats['mutations']<12:
   for i in [j for j in range(len(ts)) if j not in required][:2]:
    verify(dict(room,triangles=sorted(selected^{ts[i]})),w);stats['mutations']+=1
  if stats['corrupt_checks']<12:
   i=next(iter(required));bad=dict(facts);del bad[i];assert not required<=bad.keys();stats['corrupt_checks']+=1
   bad=dict(facts);bad[i]=1-bad[i];assert bad[i]!=int(ts[i] in selected);stats['corrupt_checks']+=1
  if kind=='base':base_keys.add(facts)
  if kind in ('base','pass1'):pass1_keys.add(facts)
  witness_by_key.setdefault(facts,w)
  if facts not in keys:keys.add(facts);add_guard(model,x,facts)
 for n,r in enumerate(data['base'],1):
  checked(r['room'],r['witness'],'base')
  if n%100==0:save('base_paths')
 save('base_complete');assert len(base_keys)==1910,len(base_keys)
 for n,r in enumerate(data['peer'],1):
  room=dict(triangles=r['room'],marked=[[0,0],[4,0]],require_simple=True);w=r['witness']
  validate(room,TARGET);stats['peer_geometry']+=1
  checked(room,w,'pass1' if n<=1259 else 'pass2')
  mirror=dict(room,triangles=[[[a,-b] for a,b in t] for t in room['triangles']])
  mw=dict(w,direction=[w['direction'][0],-w['direction'][1]],path=[[[a,ad],[-b,bd]] for (a,ad),(b,bd) in w['path']])
  checked(mirror,mw,'pass1' if n<=1259 else 'mirror')
  if n%100==0:save('peer_paths')
 result['cuts']=[list(k) for k in sorted(keys)];save('rays_complete')
 def solver(cap):
  s=cp_model.CpSolver();s.parameters.num_search_workers=2;s.parameters.cp_model_presolve=False;s.parameters.random_seed=733;s.parameters.max_time_in_seconds=cap;return s
 # Positive drop-pass-2 control uses this model's own variable/index schema.
 control=make_model(TARGET);cm,ct,cx,cb,ce=control;refine_connected_cells(TARGET,cm,ce)
 for f in pass1_keys:add_guard(cm,cx,f)
 for a,b in sorted(cb['allowed']-cb['mandatory']):cm.add(ce['used'][2*a,2*b]==int((a,b)==(1,-1)))
 ss=solver(60);st=ss.solve(cm);result['drop_pass2_control']=dict(status=ss.status_name(st),seconds=ss.wall_time)
 if st in (cp_model.OPTIMAL,cp_model.FEASIBLE):
  room=room_from(TARGET,ct,cx,ss);result['drop_pass2_control']['room']=room
  bits={i for i,t in enumerate(ct) if ss.value(cx[i])}
  hit=next(f for f in keys-pass1_keys if all(int(i in bits)==v for i,v in f))
  w=witness_by_key[hit];verify(room,w);result['drop_pass2_control']['dropped_witness']=w;stats['drop_control_lit']+=1
 save('control_complete')
 ss=solver(240);st=ss.solve(model);result['monolithic']=dict(status=ss.status_name(st),seconds=ss.wall_time);save('monolithic_complete')
 if st==cp_model.INFEASIBLE:
  result.update(status='PASS',placement_excluded=True,proof='Codex complete parent monolithic INFEASIBLE')
 else:
  choices,levels=outside_sets(TARGET);assert len(choices)==699
  outside=sorted(bounded['allowed']-bounded['mandatory'])
  for n,chosen in enumerate(choices,1):
   branch=model.clone()
   for a,b in outside:branch.add(terms['used'][2*a,2*b]==int((a,b) in chosen))
   ss=solver(5);st=ss.solve(branch)
   if st==cp_model.UNKNOWN:ss=solver(60);st=ss.solve(branch)
   result['partition'].append(dict(cells=chosen,status=ss.status_name(st),seconds=ss.wall_time))
   if n%25==0:save('partition_replay')
  result['placement_excluded']=all(r['status']=='INFEASIBLE' for r in result['partition'])
  result['status']='PASS' if result['placement_excluded'] else 'OPEN'
  result['proof']='Complete699 outside-cell partition' if result['placement_excluded'] else 'Incomplete exclusion'
 save('complete')

if __name__=='__main__':main()
