"""Exact check of one hand-derived 32-reflection candidate; no discovery."""
from pathlib import Path
from fractions import Fraction as F
import json,runpy,hashlib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
sub=lambda a,b:(a[0]-b[0],a[1]-b[1])
cross=lambda a,b:a[0]*b[1]-a[1]*b[0]
dot=lambda a,b:a[0]*b[0]+a[1]*b[1]
tri=lambda t:tuple(sorted(map(tuple,t)))
raw="""0,0
-1,-9/20
22/29,-36/29
-1/4,1
-1,-2/3
-17/20,-1
10/29,48/29
0,3/2
10/11,12/11
2,-4/3
52/29,-52/29
2,-17/10
16/11,-16/11
0,16/9
2/29,56/29
0,19/10
2/11,20/11
20/11,-20/11
2,-19/10
56/29,-56/29
2,-16/9
6/11,16/11
0,17/10
6/29,52/29
0,4/3
12/11,-12/11
2,-3/2
48/29,-48/29
33/10,2
102/29,44/29
1,53/20
2,31/10
40/29,98/29
2,2"""
P=[tuple(map(F,line.split(','))) for line in raw.splitlines()]
def physical(path,V):
 walls=list(zip(V,V[1:]+V[:1]))
 def inside(p):
  value=False
  for a,b in walls:
   e,v=sub(b,a),sub(p,a)
   assert cross(e,v) or not(min(a[0],b[0])<=p[0]<=max(a[0],b[0]) and min(a[1],b[1])<=p[1]<=max(a[1],b[1]))
   if (a[1]>p[1])!=(b[1]>p[1]):
    x=a[0]+(p[1]-a[1])*(b[0]-a[0])/(b[1]-a[1])
    if p[0]<x:value=not value
  return value
 assert inside(path[0]) and inside(path[-1])
 for prev,p,nxt in zip(path,path[1:],path[2:]):
  hits=[(a,b) for a,b in walls if cross(sub(b,a),sub(p,a))==0 and 0<dot(sub(p,a),sub(b,a))<dot(sub(b,a),sub(b,a))]
  assert len(hits)==1,('nonstrict',p)
  a,b=hits[0];e,v,out=sub(b,a),sub(p,prev),sub(nxt,p)
  reflected=tuple(2*dot(v,e)*e[k]/dot(e,e)-v[k] for k in [0,1])
  assert cross(reflected,out)==0 and dot(reflected,out)>0
 for p,q in zip(path,path[1:]):
  assert inside(tuple((p[k]+q[k])/2 for k in [0,1]))
  v=sub(q,p)
  for a,b in walls:
   w,ap=sub(b,a),sub(a,p);den=cross(v,w)
   if den:
    t,s=cross(ap,w)/den,cross(ap,v)/den
    assert not(0<t<1 and 0<=s<=1),('earlier boundary',p,q,a,b)
   elif cross(ap,v)==0:
    aa,bb=dot(ap,v)/dot(v,v),dot(sub(b,p),v)/dot(v,v)
    assert max(min(aa,bb),F(0))>=min(max(aa,bb),F(1))


guardfile=ROOT/'lower-bound-proof-audit/full-replay/guard-checker.py'
g=runpy.run_path(str(guardfile))
U,Z=g['path_requirements'](P)
rows={}
sigma=lambda p:(2-p[1],2-p[0])
for name,row in json.loads((HERE/'geometry.json').read_text()).items():
 V=[tuple(map(F,p)) for p in row['vertices']];room={tri(t) for t in row['triangles']}
 physical(P,V);physical(P[::-1],V);physical([sigma(p) for p in reversed(P)],[sigma(p) for p in V])
 assert U<=room and not Z&room
 rows[name]={'status':'PASS','reflections':len(P)-2,'forward_reverse_sigma':'PASS','ledger':row['ledger']}
out={'status':'PASS','scope':'Only one hand-derived prescribed candidate on two frozen supplied rooms','initial_direction':[-20,-9],'reflections':len(P)-2,'path':[[str(c) for c in p] for p in P],'required':sorted(U),'forbidden':sorted(Z),'controls':rows,'geometry_sha256':hashlib.sha256((HERE/'geometry.json').read_bytes()).hexdigest()}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'reflections':out['reflections'],'rooms':list(rows)}))
