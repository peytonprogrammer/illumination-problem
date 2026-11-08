"""Exhaustive fixed-cell replay after exact elimination of absent triangles.

A global case fixes its occupied outside cells. Every triangle belongs to one
A cell, so triangles outside mandatory|chosen are absent. Rebuild the unchanged
local-fan/Euler/rank/wall model on that remaining support. A global ray condition
requiring an absent triangle is impossible; its exclusion clause is tautological.
An absence literal outside the remaining support is automatically satisfied and
is removed. This gives the exact same ray exclusions on the remaining variables.
"""
from pathlib import Path
import argparse,hashlib,json,time,random
from ortools.sat.python import cp_model
from illumination_three_two_star_bound import complete_support,validate
from illumination_family_bound import triangles_in_cells
from illumination_three_star_model import build_model
from illumination_triple_cell_sets import outside_sets
from search_illumination_three_two_star import room_from
from functools import lru_cache
import illumination_three_star_model as geometry_builder
_original_owners=geometry_builder.owners_of
_original_sectors=geometry_builder.local_sectors
@lru_cache(maxsize=32768)
def cached_owners(triangles):return _original_owners(triangles)
@lru_cache(maxsize=32768)
def cached_sectors(triangles,point,opened):return _original_sectors(triangles,point,set(opened))
geometry_builder.owners_of=lambda triangles:cached_owners(tuple(triangles))
geometry_builder.local_sectors=lambda triangles,point,opened:cached_sectors(tuple(triangles),point,tuple(sorted(opened)))

BASE=Path(__file__).parent;OUT=BASE/'three-triples'

def run(target):
 start=time.monotonic();tag='-'.join(map(str,target));path=OUT/f'peer-local-final-{tag}.json';inputs={};bounded=complete_support(target);global_ts=triangles_in_cells(bounded['allowed'])
 def read(name):
  p=OUT/name;inputs[str(p.relative_to(BASE.parent))]=hashlib.sha256(p.read_bytes()).hexdigest();return json.loads(p.read_text())
 previous=read(f'peer-complete-replay-{tag}.json');keys=set()
 if target==(2,0):
  audit=read('peer-2-0-audit.json');assert audit['stats']['exact_paths']==6997;keys={tuple(map(tuple,f)) for f in audit['cuts']};assert len(keys)==5710
  controls=[read('peer-2-0-control.json')['room']]
 else:
  from search_illumination_forced_c_cases import load_base
  _,ts,_,_,_,keys,*_=load_base();assert ts==global_ts and len(keys)==3379
  for name in ['forced-c-cases-1-1.json','thin-tip-cover-1-1.json','thin-tip-extension-1-1.json','interior-fans-1-1.json','remainder-types-1-1.json']:
   for r in read(name)['records']:
    for g in r['derived_guards']:keys.add(tuple(map(tuple,g['tile_facts'])))
  for name in ['peer-1-1-audit.json','peer-1-1-final-audit.json']:
   for g in read(name)['derived_guards']:keys.add(tuple(map(tuple,g['tile_facts'])))
  for g in previous['additional_checked_paths']:keys.add(tuple(map(tuple,g['tile_facts'])))
  assert len(keys)==4671
  controls=[r['room'] for r in read('peer-1-1-followup-rays.json')]
 guards=[(frozenset(global_ts[i] for i,v in f if v),frozenset(global_ts[i] for i,v in f if not v)) for f in keys]
 def local(cells):
  allowed=bounded['mandatory']|set(cells);b=dict(bounded,allowed=allowed)
  m,ts,x,_,terms=build_model(target,23,3,b);idx={t:i for i,t in enumerate(ts)}
  for a,b in cells:m.add(terms['used'][2*a,2*b]==1)
  inc=[[] for _ in ts];out=[[] for _ in ts];bound=terms['max_tiles'];root=next(i for i,t in enumerate(ts) if (0,0) in t)
  for ids in _original_owners(ts).values():
   if len(ids)!=2:continue
   for a,b in (ids,ids[::-1]):
    flow=m.new_int_var(0,bound,f'local_flow{a}_{b}');m.add(flow<=bound*x[a]);m.add(flow<=bound*x[b]);out[a].append(flow);inc[b].append(flow)
  for i in range(len(ts)):
   m.add(sum(out[i])-sum(inc[i])==sum(x)-1) if i==root else m.add(sum(inc[i])-sum(out[i])==x[i])
  return m,ts,x,terms,idx
 def solve(m,cap):
  s=cp_model.CpSolver();s.parameters.cp_model_presolve=False;s.parameters.num_search_workers=6;s.parameters.max_time_in_seconds=cap;s.parameters.random_seed=733;st=s.solve(m);return s,st
 receipt_controls=[];rng=random.Random(733);projection_checks=0
 for room in controls:
  validate(room,target);selected={tuple(sorted(map(tuple,t))) for t in room['triangles']};cells={tuple(p[k]//2 for k in (0,1)) for t in selected for p in t if p[0]%2==0 and p[1]%2==0}-bounded['mandatory']
  assert cells in [set(s) for s in outside_sets(target)[0]]
  m,ts,x,terms,idx=local(cells);assert selected<=set(ts)
  for i,t in enumerate(ts):m.add(x[i]==int(t in selected))
  s,st=solve(m,10);assert st in (cp_model.OPTIMAL,cp_model.FEASIBLE)
  receipt_controls.append(dict(outside_cells=sorted(cells),status=s.status_name(st),triangles=len(ts)))
  for assignment in [selected]+[{t for t in ts if rng.randrange(2)} for _ in range(4)]:
   for present,absent in guards:
    direct=present<=assignment and not absent&assignment
    projected=False if not present<=idx.keys() else present<=assignment and not (absent&idx.keys())&assignment
    assert direct==projected;projection_checks+=1
 choices,levels=outside_sets(target);expected=699 if target==(2,0) else 2530;assert len(choices)==expected
 history=dict(partition=[])
 done={tuple(map(tuple,r['cells'])):r for r in history['partition'] if r['status']=='INFEASIBLE'};assert set(done)<=set(choices)
 result=dict(status='RUNNING',target=target,guard_count=len(keys),complete_partition_size=expected,source_sha256=inputs,positive_local_controls=receipt_controls,projection_control_checks=projection_checks,previous_negative_leaves=len(done),partition=[])
 def save(event):
  result['seconds']=time.monotonic()-start;tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(result,indent=2)+'\n');tmp.replace(path)
  print(json.dumps(dict(event=event,leaves=len(result['partition']),counts={s:sum(r['status']==s for r in result['partition']) for s in {r['status'] for r in result['partition']}},seconds=round(result['seconds'],2))),flush=True)
 save('controls_pass')
 for n,cells in enumerate(choices,1):
  if cells in done:row=dict(done[cells],reused=True)
  else:
   m,ts,x,terms,idx=local(cells);live=0
   for present,absent in guards:
    if not present<=idx.keys():continue
    m.add_bool_or([x[idx[t]].Not() for t in present]+[x[idx[t]] for t in absent&idx.keys()]);live+=1
   s,st=solve(m,3)
   if st==cp_model.UNKNOWN:s,st=solve(m,30)
   row=dict(cells=cells,status=s.status_name(st),seconds=s.wall_time,available_triangles=len(ts),applicable_ray_guards=live)
   if st in (cp_model.OPTIMAL,cp_model.FEASIBLE):row['room']=room_from(target,ts,x,s)
  result['partition'].append(row)
  if n%25==0:save('partition')
 result['placement_excluded']=len(result['partition'])==expected and all(r['status']=='INFEASIBLE' for r in result['partition']);result['status']='PASS' if result['placement_excluded'] else 'OPEN';save('complete')

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('target',choices=['1-1','2-0']);a=p.parse_args();run(tuple(map(int,a.target.split('-'))))
