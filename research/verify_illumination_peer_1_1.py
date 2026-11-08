"""Check a frozen batch of peer (1,1) paths against the own complete parent."""
from pathlib import Path
import hashlib,json,time
from ortools.sat.python import cp_model
from search_illumination_forced_c_cases import load_base
from search_illumination_three_two_star import add_guard
from search_illumination_one_exception import orbit,tile_facts
from illumination_sector_paths import verify
from illumination_three_two_star_bound import validate
from illumination_geometry import owners_of
from audit_illumination_three_two_star import touched_tiles
BASE=Path(__file__).parent;OUT=BASE/'three-triples';PATH=OUT/'peer-1-1-audit.json'
start=time.monotonic();model,ts,x,bounded,terms,keys,*_=load_base();assert len(keys)==3379
for name in ['forced-c-cases-1-1.json','thin-tip-cover-1-1.json','thin-tip-extension-1-1.json','interior-fans-1-1.json','remainder-types-1-1.json']:
 d=json.loads((OUT/name).read_text())
 for r in d['records']:
  for g in r['derived_guards']:
   key=tuple(map(tuple,g['tile_facts']));assert key not in keys;keys.add(key);add_guard(model,x,key)
assert len(keys)==3987
owners=owners_of(ts);source=OUT/'peer-1-1-rays.jsonl';all_rows=[json.loads(s) for s in source.read_text().splitlines() if s];rows=[r for r in all_rows if r.get('path')];skipped=len(all_rows)-len(rows);added=[];checked=0
for n,r in enumerate(rows,1):
 room=dict(triangles=r['room'],marked=[[0,0],[2,2]],require_simple=True);w=dict(status='illuminated',direction=r['direction'],path=r['path'],bounces=len(r['path'])-2)
 validate(room,(1,1))
 for changed,ray in orbit(room,w):
  verify(changed,ray);checked+=1
  facts=tile_facts(ts,owners,ray,changed);fixed=dict(facts);required=touched_tiles(ts,ray);selected={tuple(sorted(map(tuple,t))) for t in changed['triangles']}
  assert required<=fixed.keys() and all(fixed[i]==int(ts[i] in selected) for i in required)
  key=tuple(sorted((i,int(ts[i] in selected)) for i in required))
  if key not in keys:keys.add(key);add_guard(model,x,key);added.append(dict(room=changed,witness=ray,tile_facts=key))
 if n%25==0:print(json.dumps(dict(event='paths_checked',rows=n,exact_rays=checked,guards=len(keys))),flush=True)
result=dict(status='RAYS_PASS',non_witness_rows_skipped=skipped,rows=len(rows),exact_rays=checked,base_guards=3987,total_guards=len(keys),new_guards=len(added),derived_guards=added,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest())
tmp=PATH.with_suffix('.tmp');tmp.write_text(json.dumps(result,indent=2)+'\n');tmp.replace(PATH)
s=cp_model.CpSolver();s.parameters.cp_model_presolve=False;s.parameters.num_search_workers=2;s.parameters.max_time_in_seconds=30;s.parameters.random_seed=733
st=s.solve(model);result['monolithic']=dict(status=s.status_name(st),seconds=s.wall_time);result['placement_excluded']=st==cp_model.INFEASIBLE;result['seconds']=time.monotonic()-start
PATH.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='derived_guards'}),flush=True)
