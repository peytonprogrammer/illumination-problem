"""Bounded off-A target pilot. Positive paths only; misses never imply darkness."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent))
import json,time
from fractions import Fraction as F
from ortools.sat.python import cp_model
from search_illumination_family import build_model
from illumination_geometry import owners_of,check_fan_angles,label
from illumination_paths import find_path
from verify_illumination_paths import verify

if '--audit' in sys.argv:
 result=json.loads((ROOT/'midpoint-pilot.json').read_text());checked=0
 for r in result['rooms']:
  ts=[tuple(map(tuple,t)) for t in r['triangles']]
  owners=owners_of(ts);opens={e for e,ids in owners.items() if len(ids)==2}
  graph={i:set() for i in range(len(ts))}
  for e in opens:
   a,b=owners[e];graph[a].add(b);graph[b].add(a)
  visited={0};todo=[0]
  for i in todo:
   for j in graph[i]:
    if j not in visited:visited.add(j);todo.append(j)
  assert len(visited)==len(ts)
  vertices={p for t in ts for p in t};interior=[];walls=0
  assert len(vertices)-len(owners)+len(ts)==1
  for p in vertices:
   fans,inside=check_fan_angles(ts,p,owners,opens);assert len(fans)<=1
   if inside:interior.append(p)
   if label(p)!='A':assert not inside and 4 not in fans
   walls+=sum(a!=4 for a in fans)
  assert set(interior)=={(0,0)} and walls==r['walls'] and walls<=23
  for t in r['targets']:
   e=tuple(map(tuple,t['edge']));target=tuple(F(*v) for v in t['target'])
   assert e in opens and target==tuple(F(e[0][k]+e[1][k],2) for k in (0,1))
   assert all((0,0) not in ts[i] for i in owners[e])
   if t['witness']['status']=='illuminated':
    assert verify(dict(triangles=ts,marked=[(0,0),target]),t['witness']);checked+=1
 assert checked==result['illuminated']
 result['audit']=dict(status='PASS',connected_simple_strict_rooms=len(result['rooms']),independently_verified_positive_paths=checked)
 (ROOT/'midpoint-pilot.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result['audit']),flush=True)
 raise SystemExit

if '--refine' in sys.argv:
 result=json.loads((ROOT/'midpoint-pilot.json').read_text())
 for r in result['rooms']:
  for t in r['targets']:
   if t['witness']['status']=='illuminated':continue
   target=tuple(F(*v) for v in t['target'])
   data=dict(triangles=r['triangles'],marked=[(0,0),target])
   t['initial_screen']=t['witness']
   t['witness']=find_path(data,bound=32,max_bounces=512)
   if t['witness']['status']=='illuminated':assert verify(data,t['witness'])
   print(json.dumps(dict(refined_target=t['target'],status=t['witness']['status'])),flush=True)
 result['illuminated']=sum(t['witness']['status']=='illuminated' for r in result['rooms'] for t in r['targets'])
 result['unresolved']=result['targets_checked']-result['illuminated']
 result['refinement']='Initial misses rechecked through primitive direction bound32 and512 bounces; positive paths independently verified. Remaining misses stay unresolved.'
 (ROOT/'midpoint-pilot.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k!='rooms'}),flush=True)
 raise SystemExit

full={(0,0)}
allowed={(a,b) for a in range(-2,3) for b in range(-2,3) if abs(a)+abs(b)<=2}
bounded=dict(full=full,mandatory={(0,0),(1,0),(-1,0),(0,1),(0,-1)},allowed=allowed)
model,tiles,x,_,terms=build_model((0,0),max_walls=23,bounded=bounded)
solver=cp_model.CpSolver();solver.parameters.num_search_workers=1
solver.parameters.max_time_in_seconds=5
rooms=[];started=time.monotonic();complete=False
model.maximize(sum(x))
for sample in range(64):
 status=solver.solve(model)
 if status==cp_model.INFEASIBLE:complete=True;break
 if status not in (cp_model.FEASIBLE,cp_model.OPTIMAL):break
 bits=[int(solver.value(v)) for v in x]
 ts=[t for t,b in zip(tiles,bits) if b]
 owners=owners_of(ts);opens={e for e,ids in owners.items() if len(ids)==2}
 vertices={p for t in ts for p in t};wall_count=0;interior=[]
 for p in vertices:
  fans,inside=check_fan_angles(ts,p,owners,opens)
  assert len(fans)<=1
  if inside:interior.append(p)
  if label(p)!='A':assert not inside and 4 not in fans
  wall_count+=sum(a!=4 for a in fans)
 assert interior==[(0,0)] or set(interior)=={(0,0)}
 assert len(vertices)-len(owners)+len(ts)==1
 assert wall_count==solver.value(terms['walls']) and wall_count<=23
 # Target only edges strictly inside, whose incident triangles lie outside
 # the source's original full eight-tile A star.
 target_edges=[e for e,ids in owners.items() if len(ids)==2 and all((0,0) not in ts[i] for i in ids)]
 targets=[]
 for e in sorted(target_edges):
  target=tuple(F(e[0][k]+e[1][k],2) for k in (0,1))
  data=dict(triangles=ts,marked=[(0,0),target])
  witness=find_path(data,bound=8,max_bounces=96)
  if witness['status']=='illuminated':assert verify(data,witness)
  targets.append(dict(edge=e,target=[[v.numerator,v.denominator] for v in target],witness=witness))
 rooms.append(dict(triangles=ts,walls=wall_count,targets=targets))
 print(json.dumps(dict(sample=sample,walls=wall_count,targets=len(targets),illuminated=sum(t['witness']['status']=='illuminated' for t in targets))),flush=True)
 model.add(sum(v if b else 1-v for v,b in zip(x,bits))<=len(x)-1)
 if time.monotonic()-started>50:break
result=dict(status='BOUNDED_POSITIVE_SCREEN',scope='At most64 single-source strict rooms in13 A cells, W<=23; interior edge midpoints outside source star; primitive directions bounded by8; not an exhaustive family or darkness test.',enumeration_complete_in_13_cells=complete,rooms_checked=len(rooms),targets_checked=sum(len(r['targets']) for r in rooms),illuminated=sum(t['witness']['status']=='illuminated' for r in rooms for t in r['targets']),unresolved=sum(t['witness']['status']!='illuminated' for r in rooms for t in r['targets']),seconds=time.monotonic()-started,rooms=rooms)
(ROOT/'midpoint-pilot.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='rooms'}),flush=True)
