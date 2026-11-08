"""Check the new peer tail and independently replay the whole (1,1) parent."""
from pathlib import Path
import hashlib,json,time
from ortools.sat.python import cp_model
from search_illumination_forced_c_cases import load_base
from search_illumination_three_two_star import add_guard,room_from
from search_illumination_one_exception import orbit,tile_facts
from illumination_sector_paths import verify
from illumination_three_two_star_bound import validate
from illumination_geometry import owners_of
from audit_illumination_three_two_star import touched_tiles
from illumination_triple_cell_sets import outside_sets
BASE=Path(__file__).parent;OUT=BASE/'three-triples';PATH=OUT/'peer-1-1-final-audit.json';start=time.monotonic()
prior=json.loads((OUT/'peer-1-1-audit.json').read_text());assert prior['status']=='RAYS_PASS' and prior['exact_rays']==516
oldpath=OUT/'peer-1-1-rays.jsonl';assert hashlib.sha256(oldpath.read_bytes()).hexdigest()==prior['source_sha256']
old=[json.loads(s) for s in oldpath.read_text().splitlines() if s];old_live=[r for r in old if r['origin']=='live']
source=OUT/'peer-1-1-final-rays.jsonl';rows=[json.loads(s) for s in source.read_text().splitlines() if s]
for a,b in zip(old_live,rows):assert {k:v for k,v in a.items() if k!='origin'}==b
assert len(rows)>=len(old_live)
model,ts,x,bounded,terms,keys,*_=load_base();assert len(keys)==3379
for name in ['forced-c-cases-1-1.json','thin-tip-cover-1-1.json','thin-tip-extension-1-1.json','interior-fans-1-1.json','remainder-types-1-1.json']:
 d=json.loads((OUT/name).read_text())
 for r in d['records']:
  for g in r['derived_guards']:
   key=tuple(map(tuple,g['tile_facts']));assert key not in keys;keys.add(key);add_guard(model,x,key)
assert len(keys)==3987
for g in prior['derived_guards']:
 key=tuple(map(tuple,g['tile_facts']));assert key not in keys;keys.add(key);add_guard(model,x,key)
assert len(keys)==prior['total_guards']==4459
before=set(keys);owners=owners_of(ts);new=[];checked=0
for n,r in enumerate(rows[len(old_live):],1):
 room=dict(triangles=r['room'],marked=[[0,0],[2,2]],require_simple=True);w=dict(status='illuminated',direction=r['direction'],path=r['path'],bounces=len(r['path'])-2);validate(room,(1,1))
 for changed,ray in orbit(room,w):
  verify(changed,ray);checked+=1
  compiled=dict(tile_facts(ts,owners,ray,changed));required=touched_tiles(ts,ray);selected={tuple(sorted(map(tuple,t))) for t in changed['triangles']}
  assert required<=compiled.keys() and all(compiled[i]==int(ts[i] in selected) for i in required)
  key=tuple(sorted((i,int(ts[i] in selected)) for i in required))
  if key not in keys:keys.add(key);add_guard(model,x,key);new.append(dict(room=changed,witness=ray,tile_facts=key))
 if n%10==0:print(json.dumps(dict(event='tail_rays',records=n,paths=checked,guards=len(keys))),flush=True)
result=dict(status='RAYS_PASS',source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),previous_audit_sha256=hashlib.sha256((OUT/'peer-1-1-audit.json').read_bytes()).hexdigest(),tail_records=len(rows)-len(old_live),tail_paths=checked,total_peer_paths=516+checked,total_guards=len(keys),derived_guards=new,partition=[])
def save(event):
 result['seconds']=time.monotonic()-start;tmp=PATH.with_suffix('.tmp');tmp.write_text(json.dumps(result,indent=2)+'\n');tmp.replace(PATH);print(json.dumps(dict(event=event,seconds=result['seconds'],guards=len(keys),partition=len(result['partition']),monolithic=result.get('monolithic'))),flush=True)
def solve(m,cap):
 s=cp_model.CpSolver();s.parameters.cp_model_presolve=False;s.parameters.num_search_workers=2;s.parameters.max_time_in_seconds=cap;s.parameters.random_seed=733;st=s.solve(m);return s,st
save('paths_complete')
s,st=solve(model,180);result['monolithic']=dict(status=s.status_name(st),seconds=s.wall_time);save('monolithic')
if st==cp_model.INFEASIBLE:result.update(status='PASS',placement_excluded=True)
elif st in (cp_model.OPTIMAL,cp_model.FEASIBLE):result.update(status='OPEN',placement_excluded=False,survivor=room_from((1,1),ts,x,s))
else:
 choices,levels=outside_sets((1,1));assert len(choices)==2530;outside=sorted(bounded['allowed']-bounded['mandatory'])
 for n,cells in enumerate(choices,1):
  branch=model.clone()
  for a,b in outside:branch.add(terms['used'][2*a,2*b]==int((a,b) in cells))
  s,st=solve(branch,3)
  if st==cp_model.UNKNOWN:s,st=solve(branch,30)
  result['partition'].append(dict(cells=cells,status=s.status_name(st),seconds=s.wall_time))
  if n%100==0:save('partition')
 result['placement_excluded']=all(r['status']=='INFEASIBLE' for r in result['partition']);result['status']='PASS' if result['placement_excluded'] else 'OPEN'
save('complete')
