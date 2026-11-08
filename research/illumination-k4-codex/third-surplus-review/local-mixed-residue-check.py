"""Exact geometry of three hand-forced single-fan residual fixtures."""
from pathlib import Path
from collections import Counter,defaultdict
import json
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
project=json.loads((HERE/'local-mixed-project.json').read_text())['families']
tri=lambda t:tuple(sorted(map(tuple,t)))
slots={n:tri(t) for n,t in json.loads((ROOT/'zero-surplus-L/guard-incidence-check.json').read_text())['cap_options'].items()}
cases={'BD_join_Bouter3_Nrplus_Rminus':('BDjoin_Bouter3',['Nr+','R-'])}
records={}
for name,(family,extras) in cases.items():
 room={tri(t) for t in project[family]['fixed_triangles']}|{slots[n] for n in extras}
 edges=Counter();at=defaultdict(list)
 for t in room:
  for v in t:at[v].append(t)
  for i in range(3):edges[tuple(sorted((t[i],t[(i+1)%3])))]+=1
 adj=defaultdict(list)
 for (a,b),m in edges.items():
  assert m in (1,2)
  if m==1:adj[a].append(b);adj[b].append(a)
 assert all(len(v)==2 for v in adj.values())
 cur=min(adj);start=cur;prev=None;boundary=[cur]
 while True:
  nxt=next(v for v in adj[cur] if v!=prev)
  if nxt==start:break
  assert nxt not in boundary
  boundary.append(nxt);prev,cur=cur,nxt
 assert len(boundary)==len(adj)
 cross=lambda a,b:a[0]*b[1]-a[1]*b[0]
 W=sum(cross((v[0]-boundary[i-1][0],v[1]-boundary[i-1][1]),(boundary[(i+1)%len(boundary)][0]-v[0],boundary[(i+1)%len(boundary)][1]-v[1]))!=0 for i,v in enumerate(boundary))
 typ=lambda v:'A' if v[0]%2==v[1]%2==0 else ('B' if v[0]%2==v[1]%2==1 else 'C')
 interiorA=[v for v,t in at.items() if typ(v)=='A' and len(t)==8]
 assert sorted(interiorA)==[(0,0),(2,0),(2,2)]
 J=sum(typ(v)!='A' and len(t)==(8 if typ(v)=='B' else 4) for v,t in at.items())
 sN=[v for v,t in at.items() if typ(v)!='A' and len(t)==(4 if typ(v)=='B' else 2)]
 sA=sum(typ(v)=='A' and len(t)==4 for v,t in at.items())
 Q=sum(3 if len(t)==4 else len(t) for v,t in at.items() if typ(v)=='A' and len(t)<8)
 delta=Q+len(sN)-8;k=J+len(sN)
 assert delta==3 and W<=21 and k<=6
 records[name]={'triangles':sorted(room),'strict_simple':'PASS_single_boundary_cycle','W':W,'k':k,'Delta':delta,'Q':Q,'J':J,'s_N':len(sN),'s_A':sA,'N':len(room),'smoothN':sorted(sN),'in_active_class':True}
assert tuple(records['BD_join_Bouter3_Nrplus_Rminus'][v] for v in ['W','k','N','Q','J','s_N','s_A','Delta'])==(21,5,33,9,3,2,0,3)
(HERE/'local-mixed-residue-check.json').write_text(json.dumps({'status':'PASS','records':records,'scope':'One hand-forced final mixed-partition residue, no room discovery.'},indent=2)+'\n')
print(json.dumps({n:{k:v[k] for k in ['W','k','Delta','N','Q','J','s_N']} for n,v in records.items()}))
