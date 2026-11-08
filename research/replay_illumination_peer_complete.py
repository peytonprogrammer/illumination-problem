"""Complete independent fixed-cell replay; keep caps and finite misses open.

The outside-set allowed table is redundant in a branch fixing every outside
cell to one of its enumerated rows, so it is omitted from this fresh builder.
All local geometry, rank connectivity, Euler, exception and wall constraints
remain in the own model. No peer model builder or peer tile index is used.
"""
from pathlib import Path
import argparse,hashlib,json,time
from ortools.sat.python import cp_model
from search_illumination_three_two_star import make_model,room_from
from illumination_triple_cell_sets import outside_sets
from illumination_geometry import owners_of
from illumination_sector_paths import verify
from illumination_three_two_star_bound import validate
from search_illumination_one_exception import orbit,tile_facts
from audit_illumination_three_two_star import touched_tiles
BASE=Path(__file__).parent;OUT=BASE/'three-triples'

def run(target):
 tag='-'.join(map(str,target));path=OUT/f'peer-complete-replay-{tag}.json';start=time.monotonic();inputs={}
 def read(name):
  p=OUT/name;inputs[str(p.relative_to(BASE.parent))]=hashlib.sha256(p.read_bytes()).hexdigest();return json.loads(p.read_text())
 model,ts,x,bounded,terms=make_model(target);extras=[]
 if target==(2,0):
  audit=read('peer-2-0-audit.json');assert audit['stats']['exact_paths']==6997
  keys={tuple(map(tuple,f)) for f in audit['cuts']};assert len(keys)==5710
  old=read('peer-2-0-replay.json');expected=699
 else:
  from search_illumination_forced_c_cases import load_base
  _,ots,_,_,_,keys,*_=load_base();assert ots==ts and len(keys)==3379
  for name in ['forced-c-cases-1-1.json','thin-tip-cover-1-1.json','thin-tip-extension-1-1.json','interior-fans-1-1.json','remainder-types-1-1.json']:
   for r in read(name)['records']:
    for g in r['derived_guards']:
     key=tuple(map(tuple,g['tile_facts']));assert key not in keys;keys.add(key)
  assert len(keys)==3987
  for name in ['peer-1-1-audit.json','peer-1-1-final-audit.json']:
   a=read(name)
   for g in a['derived_guards']:
    key=tuple(map(tuple,g['tile_facts']));assert key not in keys;keys.add(key)
  assert len(keys)==4663
  owners=owners_of(ts)
  for r in read('peer-1-1-followup-rays.json'):
   validate(r['room'],target)
   for room,w in orbit(r['room'],r['witness']):
    verify(room,w);compiled=dict(tile_facts(ts,owners,w,room));required=touched_tiles(ts,w);selected={tuple(sorted(map(tuple,t))) for t in room['triangles']}
    assert required<=compiled.keys() and all(compiled[i]==int(ts[i] in selected) for i in required)
    key=tuple(sorted((i,int(ts[i] in selected)) for i in required));extras.append(dict(room=room,witness=w,tile_facts=key));keys.add(key)
  old=read('peer-1-1-final-audit.json');expected=2530
 for f in sorted(keys):model.add_bool_or([x[i].Not() if value else x[i] for i,value in f])
 choices,levels=outside_sets(target);assert len(choices)==expected;outside=sorted(bounded['allowed']-bounded['mandatory'])
 previous={tuple(map(tuple,r['cells'])):r for r in old['partition'] if r['status']=='INFEASIBLE'}
 assert set(previous)<=set(choices)
 result=dict(status='RUNNING',target=target,guard_count=len(keys),previous_negative_leaves=len(previous),source_sha256=inputs,additional_checked_paths=extras,complete_partition_size=expected,partition=[],seconds=0)
 def save(event):
  result['seconds']=time.monotonic()-start;tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(result,indent=2)+'\n');tmp.replace(path)
  print(json.dumps(dict(event=event,leaves=len(result['partition']),counts={s:sum(r['status']==s for r in result['partition']) for s in {r['status'] for r in result['partition']}},seconds=round(result['seconds'],2))),flush=True)
 def solve(m,cap):
  s=cp_model.CpSolver();s.parameters.cp_model_presolve=False;s.parameters.num_search_workers=2;s.parameters.random_seed=733;s.parameters.max_time_in_seconds=cap;st=s.solve(m);return s,st
 save('start')
 for n,cells in enumerate(choices,1):
  if cells in previous:row=dict(previous[cells],reused=True)
  else:
   branch=model.clone()
   for a,b in outside:branch.add(terms['used'][2*a,2*b]==int((a,b) in cells))
   s,st=solve(branch,3)
   if st==cp_model.UNKNOWN:s,st=solve(branch,30)
   row=dict(cells=cells,status=s.status_name(st),seconds=s.wall_time)
   if st in (cp_model.FEASIBLE,cp_model.OPTIMAL):row['room']=room_from(target,ts,x,s)
  result['partition'].append(row)
  if n%25==0:save('partition')
 result['placement_excluded']=len(result['partition'])==expected and all(r['status']=='INFEASIBLE' for r in result['partition']);result['status']='PASS' if result['placement_excluded'] else 'OPEN';save('complete')

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('target',choices=['1-1','2-0']);a=p.parse_args();run(tuple(map(int,a.target.split('-'))))
