"""Validate the four hand-forced half-fan combinations; no room search."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter,defaultdict
import json,runpy
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
check=runpy.run_path(str(ROOT/'lower-bound-proof-audit/full-replay/guard-checker.py'))
tri=lambda t:tuple(sorted(map(tuple,t)))
slots={n:tri(t) for n,t in json.loads((ROOT/'zero-surplus-L/guard-incidence-check.json').read_text())['cap_options'].items()}
core=set().union(*(check['incident']((F(x),F(y))) for x,y in ((0,0),(2,0),(2,2))))
root={slots['L+'],tri(((-2,0),(-2,1),(-1,1))),tri(((-2,0),(-2,1),(-3,1)))}
root.add(tri(((-2,0),(-3,0),(-3,1))))
base=core|root|{slots[n] for n in ['B+','E-','T-']}
records={}
for x,n in [(-3,'Nb-'),(-3,'Nb+'),(-1,'Nb-'),(-1,'Nb+')]:
 room=base|{tri(((-2,2),(-2,1),(x,1))),slots[n]}
 edges=Counter();at=defaultdict(list)
 for t in room:
  for v in t:at[v].append(t)
  for i in range(3):edges[tuple(sorted((t[i],t[(i+1)%3])))]+=1
 adj=defaultdict(list)
 for (a,b),count in edges.items():
  assert count in (1,2)
  if count==1:adj[a].append(b);adj[b].append(a)
 assert all(len(v)==2 for v in adj.values())
 start=min(adj);boundary=[start];prev=None;cur=start
 while True:
  nxt=next(v for v in adj[cur] if v!=prev)
  if nxt==start:break
  assert nxt not in boundary
  boundary.append(nxt);prev,cur=cur,nxt
 assert len(boundary)==len(adj)
 cross=lambda a,b:a[0]*b[1]-a[1]*b[0]
 W=sum(cross((v[0]-boundary[i-1][0],v[1]-boundary[i-1][1]),(boundary[(i+1)%len(boundary)][0]-v[0],boundary[(i+1)%len(boundary)][1]-v[1]))!=0 for i,v in enumerate(boundary))
 typ=lambda v:'A' if v[0]%2==v[1]%2==0 else ('B' if v[0]%2==v[1]%2==1 else 'C')
 interiorA=[v for v,ts in at.items() if typ(v)=='A' and len(ts)==8]
 interiorN=[v for v,ts in at.items() if typ(v)!='A' and len(ts)==(8 if typ(v)=='B' else 4)]
 smoothN=[v for v,ts in at.items() if typ(v)!='A' and len(ts)==(4 if typ(v)=='B' else 2)]
 sA=sum(typ(v)=='A' and len(ts)==4 for v,ts in at.items())
 Q=sum(3 if len(ts)==4 else len(ts) for v,ts in at.items() if typ(v)=='A' and len(ts)<8)
 delta=Q+len(smoothN)-8;k=len(interiorN)+len(smoothN)
 assert sorted(interiorA)==[(0,0),(2,0),(2,2)]
 name=('remote_left' if x==-3 else 'remote_right')+'_'+n
 records[name]={'triangles':sorted(room),'strict_simple':'PASS_single_boundary_cycle','N':len(room),'W':W,'Q':Q,'J':len(interiorN),'s_N':len(smoothN),'s_A':sA,'Delta':delta,'k':k,'smoothN':sorted(smoothN),'interiorN':sorted(interiorN),'in_active_class':delta==3 and W<=21 and k<=6}
assert {n for n,v in records.items() if v['in_active_class']}=={'remote_left_Nb-','remote_right_Nb-','remote_right_Nb+'}
assert records['remote_left_Nb+']['Delta']==4
for n,v in records.items():
 if v['in_active_class']:assert (v['W'],v['k'],v['N'],v['Q'],v['J'],v['s_N'])==(21,5,33,8,2,3)
(HERE/'half-fan-check.json').write_text(json.dumps({'status':'PASS','scope':'Four precisely hand-forced combinations for one named family only; no room search or path search.','records':records},indent=2)+'\n')
print(json.dumps({n:{k:v[k] for k in ['W','k','Delta','in_active_class']} for n,v in records.items()}))
