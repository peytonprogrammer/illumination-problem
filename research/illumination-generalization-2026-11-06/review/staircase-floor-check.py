"""Prescribed exact floor-corner rejection and actual-wall controls, no search."""
from pathlib import Path
from fractions import Fraction as F
from math import ceil,floor
import json,hashlib,datetime,time,sys
HERE=Path(__file__).resolve().parent
end=datetime.datetime.fromisoformat(json.loads((HERE/'staircase-floor-effort.json').read_text())['deadline_utc']).timestamp()
def guard():
 if '--original-effort' in sys.argv:assert time.time()<end,'original aggregate effort deadline'
def sub(p,q):return p[0]-q[0],p[1]-q[1]
def cross(p,q):return p[0]*q[1]-p[1]*q[0]
def fold(z,L):return L-abs(z%(2*L)-L)
def spt(p):return list(map(str,p))
def verify(name,V,path):
 hits={};checks=0
 for i,(p,q) in enumerate(zip(path,path[1:])):
  delta=sub(q,p);assert all(delta)
  for j,u in enumerate(V):
   v=V[(j+1)%8];e=sub(v,u);den=cross(delta,e);assert den
   t=cross(sub(u,p),e)/den;w=cross(sub(u,p),delta)/den
   if 0<=t<=1 and 0<=w<=1:
    assert w not in (0,1),'actual corner'
    assert t in (0,1),'unexpected wall'
    node=i if t==0 else i+1;assert 0<node<len(path)-1,'actual endpoint on wall'
    hits[node]='V' if e[0]==0 else 'H';checks+=1
  x,y=(p[0]+q[0])/2,(p[1]+q[1])/2
  crossings=0
  for j,u in enumerate(V):
   v=V[(j+1)%8]
   if (u[1]>y)!=(v[1]>y):
    xx=u[0]+(y-u[1])*(v[0]-u[0])/(v[1]-u[1])
    if xx>x:crossings+=1
  assert crossings%2;checks+=1
  if i<len(path)-2:
   T=path[-1]
   if cross(sub(T,p),delta)==0:
    t=(T[0]-p[0])/delta[0]
    assert not 0<=t<=1,'target already visited'
 for j,p in enumerate(path[1:-1],1):
  v=sub(p,path[j-1]);w=sub(path[j+1],p)
  reflected=(-v[0],v[1]) if hits.get(j)=='V' else (v[0],-v[1]) if hits.get(j)=='H' else v
  assert cross(reflected,w)==0 and sum(x*y for x,y in zip(reflected,w))>0;checks+=1
 return {'name':name,'checks':checks,'contacts':len(hits),'horizontal_contacts':sum(v=='H' for v in hits.values()),'path':[spt(p) for p in path]}
fixtures=[
 ('rounded-new-geometry',(6,4,3,3,4,6),(F(11,2),F(2)),(F(3,2),F(5)),None),
 ('reject-first-floor-corner',(6,4,3,3,4,6),(F(5),F(1,6)),(F(1),F(25,6)),(2,8)),
 ('floor-geometry-equality',(7,4,3,3,4,6),(F(6),F(1)),(F(1),F(5)),None),
 ('source-xs-b',(6,4,3,3,4,6),(F(4),F(1)),(F(1,2),F(11,2)),None)]
results=[];rawrecords=[]
for name,dims,S,T,manual in fixtures:
 guard();A,b,a,c,d,H=map(F,dims);xs,ys=S;xt,yt=T
 assert (A-b)*(d-c)<=c*(b-a)
 Hs=c+ys;g=d-c;Ht=yt-d;D=Hs+g+Ht;assert Ht>0
 if manual:n,K=map(F,manual);n=int(n)
 else:
  k=1+ceil(A*g/(b*Hs));K=2*k*b;n=floor((Hs*K+g*xs)/(2*A*g)+F(1,2))
 theta=(2*n*A-xs)/Hs;R=b*(Hs+g)/Hs;assert n>=1 and abs(K-g*theta)+a<=R
 J=((2*n*A+K-xs-a)/(Hs+g),(2*n*A+K-xs+a)/(Hs+g))
 Zlo=xs+D*J[0]-2*n*A-K;Zhi=xs+D*J[1]-2*n*A-K;assert Zhi-Zlo>2*a
 images=[];last=Zlo
 for j in range(2):
  image=min(sign*xt+2*a*(floor((last-sign*xt)/(2*a))+1) for sign in (-1,1))
  assert last<image<Zhi;images.append(image);last=image
 candidates=[]
 for image in images:
  tau=(2*n*A+K+image-xs)/D;phase=xs+ys*tau
  assert J[0]<tau<J[1]
  candidates.append({'image':image,'slope':tau,'floor_phase':phase,'bad':(phase/A).denominator==1})
 assert 0<images[1]-images[0]<2*a
 assert 0<candidates[1]['floor_phase']-candidates[0]['floor_phase']<a<A
 assert not all(v['bad'] for v in candidates)
 selected=next(v for v in candidates if not v['bad']);tau=selected['slope']
 if manual:assert candidates[0]['bad'] and not candidates[1]['bad'] and candidates[0]['slope']==6
 z=xs+Hs*tau-2*n*A;w=xs+(Hs+g)*tau-2*n*A-K
 assert abs(z)<b and abs(w)<a
 stages=[(-ys,c,xs,A),(c,d,z,b),(d,yt,w,a)];times={-ys,F(0),c,d,yt}
 for lo,hi,start,width in stages:
  for j in range(floor(start/width)-1,ceil((start+tau*(hi-lo))/width)+2):
   q=lo+(j*width-start)/tau
   if lo<q<hi:times.add(q)
 def point(q):
  if q<=c:return (fold(xs+tau*(q+ys),A),abs(q))
  if q<=d:return (fold(z+tau*(q-c),b),q)
  return (fold(w+tau*(q-d),a),q)
 path=[point(q) for q in sorted(times)];assert path[0]==S and path[-1]==T
 V=[tuple(map(F,p)) for p in [(0,0),(A,0),(A,c),(b,c),(b,d),(a,d),(a,H),(0,H)]]
 out=verify(name,V,path);assert out['horizontal_contacts']==1
 out['candidates']=[{k:str(v) if isinstance(v,F) else v for k,v in x.items()} for x in candidates]
 results.append(out);rawrecords.append((V,path))
# Seam target at artificial Qlow roof: exact L extension, no floor reflection needed.
V=[tuple(map(F,p)) for p in [(0,0),(6,0),(6,3),(4,3),(4,4),(3,4),(3,6),(0,6)]]
path=[(F(5),F(1)),(F(0),F(7,2)),(F(1),F(4))]
results.append(verify('actual-interior-target-on-L-narrow-roof',V,path))
# Euclidean transposition verifies the opposite sufficient geometric orientation.
V,path=rawrecords[0];results.append(verify('transposed-Ft-path',[(y,x) for x,y in V],[(y,x) for x,y in path]))
out={'status':'EXACT_SOURCE_FLOOR_TWO_IMAGES_AND_TRUE_WALLS_PASS','fixed_controls':len(results),'contacts':sum(x['contacts'] for x in results),'checks':sum(x['checks'] for x in results),'results':results,'whole_goal_complete':False,'kind':'prescribed exact fixtures; arbitrary-real proof requires independent hand review','source_sha256':{n:hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in ('staircase-floor-proof.md','staircase-floor-check.py')}}
(HERE/'staircase-floor-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='results'}))
