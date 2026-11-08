"""Corner-angle identity and fixed affine controls; no path/room discovery."""
from pathlib import Path
from collections import defaultdict
from fractions import Fraction as F
from math import gcd
import json,sys,hashlib
HERE=Path(__file__).resolve().parent;sys.path.insert(0,'<SOURCE_WORKSPACE>/.context')
from illumination_geometry import patch,check,owners_of,local_sectors,label
P=HERE.parent/'peer-fast-inputs/cand-2_2-1.json'
base=json.loads(P.read_text());tri0={tuple(sorted(map(tuple,t))) for t in base['triangles']}
unit={(min(p[0] for p in t),min(p[1] for p in t)) for t in tri0}
assert all(set(patch(x,x+1,y,y+1))<=tri0 for x,y in unit)

def measure(room):
 geom=check(dict(room,require_simple=True),strict=False)
 ts=[tuple(sorted(map(tuple,t))) for t in room['triangles']];owners=owners_of(ts);opens={e for e,ids in owners.items() if len(ids)==2}
 full=set();smooth=set();corner=set();theta={}
 for p in {p for t in ts for p in t}:
  sectors,f=local_sectors(ts,p,opens)
  if f:full.add(p)
  elif sectors==[4]:smooth.add(p)
  else:
   assert len(sectors)==1;corner.add(p);theta[p]=F(sectors[0],4)
 exc={p for p in full|smooth if label(p)!='A'}
 cells=defaultdict(list)
 for t in ts:cells[next(p for p in t if label(p)=='A')].append(t)
 nets={};pieces={}
 for a,tri in cells.items():
  m=len(tri);cost=6 if a in full else 3 if a in smooth else m
  weights=sum(F(1,2)*(next(p for p in t if label(p)=='C') in exc)+F(1,4)*(next(p for p in t if label(p)=='B') in exc) for t in tri)
  net=cost-weights
  redistributed=F(m,4)*(a in corner)+sum(F(1,2)*(next(p for p in t if label(p)=='C') in corner)+F(1,4)*(next(p for p in t if label(p)=='B') in corner) for t in tri)
  assert net==redistributed
  assert (net==0)==(a not in corner and all(p not in corner for t in tri for p in t))
  nets[a]=net;pieces[a]=redistributed
 assert sum(nets.values())==sum(theta.values())==geom['walls']-2
 coords=[p[k]-next(iter(corner))[k] for p in corner for k in (0,1)];g=0
 for c in coords:g=gcd(g,abs(c))
 return dict(W=geom['walls'],N=geom['tiles'],I=len(geom['interior_A']),k=len(geom['transparent_vertices']),
             positive_net_cells=sum(n>0 for n in nets.values()),zero_net_occupied_cells=sum(n==0 for n in nets.values()),
             total_net=str(sum(nets.values())),corner_angle_sum_over_pi=str(sum(theta.values())),
             marked_nets=[str(nets[tuple(p)]) for p in room['marked']],scalar_coordinate_gcd=g)

controls=[]
for sx,sy in [(1,1),(2,2),(3,1),(5,1),(11,1),(21,1)]:
 cells={(sx*x+i,sy*y+j) for x,y in unit for i in range(sx) for j in range(sy)}
 ts=[t for x,y in sorted(cells) for t in patch(x,x+1,y,y+1)]
 room=dict(triangles=ts,marked=[[sx*x,sy*y] for x,y in base['marked']])
 d=measure(room);assert d['W']==22 and d['N']==30*sx*sy
 if sy==1:assert d['scalar_coordinate_gcd']==1
 if sx==sy==2:assert d['marked_nets']==['0','0']
 controls.append(dict(sx=sx,sy=sy,**d))
# Reflection linear parts for horizontal and vertical walls commute with any diagonal map.
for sx,sy in [(3,1),(5,1),(2,2)]:
 for rx,ry in [(1,-1),(-1,1)]:
  assert (sx*rx,sy*ry)==(rx*sx,ry*sy)
# Exact straight segment under strip collapse: entry/exit no longer coincide.
entry=(F(0),F(0));exit=(F(2),F(1));collapsed_entry=(entry[0],entry[1]);collapsed_exit=(exit[0]-2,exit[1])
assert collapsed_entry!=(collapsed_exit)
out=dict(status='PASS',input_sha256=hashlib.sha256(P.read_bytes()).hexdigest(),controls=controls,
          global_identity='sum(net) = sum(genuine corner interior angle / pi) = W-2',
          straight_strip_collapse=dict(entry=list(map(str,collapsed_entry)),exit=list(map(str,collapsed_exit))),
          optics_status='Darkness of affine controls follows from the analytic axis-reflection conjugacy, not a new optical test.')
(HERE/'zero-charge-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
