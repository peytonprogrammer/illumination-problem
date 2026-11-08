#!/usr/bin/env python3
"""Prescribed Q0/Q100 straight metric-curve checks, no author code/search."""
from pathlib import Path
from fractions import Fraction as F
import ast,json,hashlib
base=Path(__file__).parents[1]
request=json.loads((base/'construction/availability-review-request-01.json').read_text())
pins=[]
for item in request['pins']:
 actual=hashlib.sha256((base/item['path']).read_bytes()).hexdigest();assert actual==item['sha256'];pins.append({**item,'actual':actual,'pass':True})
# Read the explicit polygon literal from own frozen arithmetic check without executing it.
module=ast.parse(Path(__file__).with_name('availability-arithmetic-check.py').read_text())
P=next(ast.literal_eval(n.value) for n in module.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='P' for t in n.targets))
def inside(poly,p):
 count=0
 for a,b in zip(poly,poly[1:]+poly[:1]):
  if (a[1]>p[1])!=(b[1]>p[1]):
   hit=F(a[0])+F((p[1]-a[1])*(b[0]-a[0]),b[1]-a[1])
   count+=hit>p[0]
 return count%2==1
rows=[]
for N in [1,100]:
 poly=[(N*x,y) for x,y in P];events=set()
 for a,b in zip(poly,poly[1:]+poly[:1]):
  if a[0]==b[0]:
   t=F(a[0],N)
   if min(a[1],b[1])<=t<=max(a[1],b[1]) and 0<=t<=2:events.add(t)
  else:
   t=F(a[1])
   if min(a[0],b[0])<=N*t<=max(a[0],b[0]) and 0<=t<=2:events.add(t)
 assert events=={F(1)}
 assert inside(poly,(F(N,2),F(1,2))) and inside(poly,(F(3*N,2),F(3,2)))
 assert inside(poly,(0,0)) and inside(poly,(2*N,2))
 C=(N,1);i=poly.index(C);a=poly[i-1];b=poly[(i+1)%len(poly)]
 assert (a[0]-C[0],a[1]-C[1])==(0,-2)
 assert (b[0]-C[0],b[1]-C[1])==(2*N,0)
 turn=(C[0]-a[0])*(b[1]-C[1])-(C[1]-a[1])*(b[0]-C[0]);assert turn<0
 rows.append({'stretch':N,'source':[0,0],'target':[2*N,2],'only_boundary_event_time':1,'boundary_point':C,'genuine_reflex':True,'missing_quadrant':'SE','opposite_radial_directions':[[-N,-1],[N,1]],'NW_sector_angle':'pi','euclidean_distance_squared':4*(N*N+1),'two_half_metric_length_squared':4*(N*N+1),'first_times_not_normalized':True})
out={'status':'PASS','pins':pins,'prescribed_controls':rows,'method':'Exact line/axial-edge intersections; no boundary intersections on either open half plus interior witnesses; exact cone turn and opposite rays; metric lower bound proved by hand','darkness_inherited_not_reproved':True,'search_used':False,'whole_goal_complete':False}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'PASS','source_pins':len(pins),'prescribed_controls':len(rows),'new_search':False}))
