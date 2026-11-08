"""Six prescribed actual-wall controls: rotations and actual interior seam marks."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
HERE=Path(__file__).resolve().parent
base=json.loads((HERE/'wide-middle-constructor-check.json').read_text())
def sub(a,b):return a[0]-b[0],a[1]-b[1]
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def parse(p):return tuple(map(F,p))
def stringify(p):return list(map(str,p))
def validate(name,V,path):
 walls=list(zip(V,V[1:]+V[:1]));hits={};checks=0
 for i,(p,q) in enumerate(zip(path,path[1:])):
  d=sub(q,p);assert d[1]>0 and d[0]!=0
  for w,(u,v) in enumerate(walls):
   e=sub(v,u);den=cross(d,e);assert den!=0
   t=cross(sub(u,p),e)/den;s=cross(sub(u,p),d)/den
   if 0<=t<=1 and 0<=s<=1:
    assert s not in (0,1),'actual corner'
    assert t in (0,1),'unexpected actual boundary'
    j=i if t==0 else i+1
    assert 0<j<len(path)-1,'endpoint on actual boundary'
    assert e[0]==0,'horizontal contact'
    hits[j]=w;checks+=1
  # Exact parity interior test away from boundaries; midpoint cannot be a node contact.
  x,y=(p[0]+q[0])/2,(p[1]+q[1])/2
  crossings=0
  for u,v in walls:
   if (u[1]>y)!=(v[1]>y):
    xhit=u[0]+(y-u[1])*(v[0]-u[0])/(v[1]-u[1])
    if xhit>x:crossings+=1
  assert crossings%2==1;checks+=1
 for j,p in enumerate(path[1:-1],1):
  v=sub(p,path[j-1]);w=sub(path[j+1],p)
  reflected=(-v[0],v[1]) if j in hits else v
  assert cross(reflected,w)==0 and sum(x*y for x,y in zip(reflected,w))>0
  checks+=1
 return {'name':name,'checks':checks,'contacts':len(hits),'path':[stringify(p) for p in path]}
results=[]
for fixture in base['fixtures']:
 V=[parse(p) for p in fixture['vertices']];path=[parse(p['point']) for p in fixture['path']]
 A=max(x for x,y in V);C=max(y for x,y in V)
 rotate=lambda p:(A-p[0],C-p[1])
 newV=[rotate(p) for p in V];newpath=[rotate(p) for p in reversed(path)]
 assert len(set(newV))==8
 results.append(validate('rotated-'+fixture['name'],newV,newpath))
V=list(map(parse,[(0,0),(1,0),(1,1),(3,1),(3,3),(2,3),(2,2),(0,2)]))
path=list(map(parse,[(F(1,2),1),(3,F(31,16)),(2,F(37,16)),(F(5,2),F(5,2))]))
assert path[0][1]==1 and 0<path[0][0]<1
results.append(validate('interior-mark-on-Qup-base',V,path))
rot=lambda p:(F(3)-p[0],F(3)-p[1])
results.append(validate('interior-mark-on-Qlow-top',[rot(p) for p in V],[rot(p) for p in reversed(path)]))
out={'status':'EXACT_ROTATION_AND_INTERIOR_SEAM_CONTROLS_PASS','fixed_controls':len(results),'contacts':sum(x['contacts'] for x in results),'checks':sum(x['checks'] for x in results),'results':results,'whole_goal_complete':False,'kind':'prescribed finite actual-wall checks; no discovery or arbitrary-real proof','source_sha256':{n:hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in ('wide-middle-constructor-check.json','wide-middle-boundary-controls.py','wide-middle-onepass.md')}}
(HERE/'wide-middle-boundary-controls.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='results'}))
