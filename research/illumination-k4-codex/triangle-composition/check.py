"""Only analytically derived6/7 paths and five prescribed budget controls."""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
import json,sys
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE/'inputs'))
import illumination_geometry as g
from boundary_replay import replay
from exact import run
from guard_checker import path_requirements
D=g.DIRS;tri=lambda t:tuple(sorted(map(tuple,t)))
def fan(a,st,m):return {tri((a,(a[0]+D[i%8][0],a[1]+D[i%8][1]),(a[0]+D[(i+1)%8][0],a[1]+D[(i+1)%8][1]))) for i in range(st,st+m)}
H=set().union(*(fan(a,0,8) for a in [(0,0),(2,0),(2,2)]))
caps={n:tri(t) for n,t in json.loads((HERE/'inputs/caps.json').read_text())['cap_options'].items()}
leaf=fan((-2,2),6,1);root=fan((-2,0),7,4)
P=[(F(0),F(0)),(F(10,11),F(-12,11)),(F(-2),F(4,3)),(F(-18,11),F(18,11)),(F(-2),F(6,5)),(F(-1,6),F(-1)),(F(3),F(14,5)),(F(17,6),F(3)),(F(2),F(2))]
P6=P[:6]+[(F(34,11),F(32,11)),P[-1]]
paths={'seven':P,'six':P6};guards={n:path_requirements(p) for n,p in paths.items()}
# Enough for a universal sufficient condition, no fixed room required.
fixed=H|fan((-2,0),7,3)|leaf|{caps['B+']}
for name,(u,z) in guards.items():
 need=fixed|({caps['E+']} if name=='six' else set())
 assert u<=need and not z&need
 rows={'direction':[5,-6],'reflections':len(paths[name])-2,'path':[[str(q) for q in p] for p in paths[name]],'required_triangles':sorted(u),'forbidden_triangles':sorted(z),'forbidden_cap_labels':[n for n,t in caps.items() if t in z]}
 (HERE/(name+'-path.json')).write_text(json.dumps(rows,indent=2)+'\n')
def polygon(ts):
 edges=set()
 for t in ts:
  p=list(t)
  if sum(p[i][0]*p[(i+1)%3][1]-p[(i+1)%3][0]*p[i][1] for i in range(3))<0:p.reverse()
  for a,b in zip(p,p[1:]+p[:1]):
   if (b,a) in edges:edges.remove((b,a))
   else:edges.add((a,b))
 out={a:b for a,b in edges};assert len(out)==len(edges)
 start=min(out);p=start;cycle=[]
 while True:
  cycle.append(p);p=out[p]
  if p==start:break
 assert len(cycle)==len(edges)
 def cr(a,b,c):return (b[0]-a[0])*(c[1]-b[1])-(b[1]-a[1])*(c[0]-b[0])
 return [p for i,p in enumerate(cycle) if cr(cycle[i-1],p,cycle[(i+1)%len(cycle)])]
fixtures={
 'row2101_fullH':(root,None,['B+','E-','T-','D+','R-'],'seven',1),
 'row2101_Hupper3':(fan((-2,0),7,3),None,['B+','E-','T-','D-','R+'],'seven',1),
 'row2110_Dcenter':(root,fan((2,-2),1,2),['B+','E-','T-','R+'],'seven',0),
 'row2110_Ecenter':(root,fan((4,2),3,2),['B+','T-','D-','R+'],'six',0),
 'row2110_Touter':(root,fan((2,4),4,2),['B+','E-','Nr+'],'seven',0),
 # These two are geometric obstructions to the proposed fixed prefix/suffix,
 # not claims of darkness or failures of every possible connecting path.
 'unresolved_Bquarter':(root,fan((0,-2),0,2),['E-','T-','R+'],None,0),
 'unresolved_Tcenter':(root,fan((2,4),5,2),['B+','E-','D-','R+'],None,0),
}
results={}
for n,(rt,unit,labels,key,budgetb) in fixtures.items():
 ts=H|rt|leaf|(unit or set())|{caps[x] for x in labels}
 geom=g.check({'triangles':sorted(ts),'marked':[(0,0),(2,2)],'require_simple':True},strict=False)
 assert geom['walls']==20 and len(geom['transparent_vertices'])==6,(n,geom)
 owners=g.owners_of(list(ts));opens={e for e,os in owners.items() if len(os)==2}
 fullN=[];smoothN=[];Q=0
 for p in {p for t in ts for p in t}:
  sizes,full=g.check_fan_angles(list(ts),p,owners,opens)
  if g.label(p)=='A':
   if not full:Q+=3 if sizes==[4] else sum(sizes)
  elif full:fullN.append(p)
  elif sizes==[4]:smoothN.append(p)
 assert Q+len(smoothN)==12
 # Baseline smooth H-facing C points missing a cap are exactly those whose
 # entire incident room fan equals the original core fan.
 missing={p for p in smoothN if g.label(p)=='C' and {t for t in ts if p in t}=={t for t in H if p in t}}
 assert len(set(smoothN)-missing)==budgetb
 V=polygon(ts)
 if key:
  u,z=guards[key];assert u<=ts and not z&ts
  assert replay(V,(0,0),(2,2),paths[key])==len(paths[key])-2
  dd,traced=run(V,(0,0),(2,2),B=20,dirs=[(5,-6)])
  assert traced==paths[key]
 conflicts={k:sorted(z&ts) for k,(u,z) in guards.items()}
 missing={k:sorted(u-ts) for k,(u,z) in guards.items()}
 if key is None:assert all(conflicts[k] or missing[k] for k in guards)
 results[n]={'status':'PATH_PASS' if key else 'OUTSIDE_NEW_GUARDS','ledger':{'W':20,'k':6,'Delta':4,'b':budgetb,'J':len(fullN),'sN':len(smoothN),'Q':Q},'selected_path':key,'blocked_mirror_triangles':conflicts,'missing_required_triangles':missing,'triangles':sorted(ts),'vertices':V}
out={'status':'PASS','scope':'Seven hand-prescribed controls of the derived universal paths and their two residual mirror obstructions. No direction/word/room discovery scan. Not closure of either entire charge row.','controls':results}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({n:{k:v[k] for k in ('status','ledger','selected_path')} for n,v in results.items()},indent=2))
