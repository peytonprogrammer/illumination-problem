"""Prescribed controls of the arbitrary-real construction, exact finite actual walls."""
from pathlib import Path
from fractions import Fraction as F
from math import floor,ceil
import json,hashlib,datetime,time,sys
HERE=Path(__file__).resolve().parent
DEADLINE=datetime.datetime.fromisoformat(json.loads((HERE/'wide-middle-onepass-effort.json').read_text())['deadline_utc']).timestamp()
def guard():
 if '--original-effort' in sys.argv:assert time.time()<DEADLINE,'original aggregate effort deadline reached'
def fold(z,L):
 u=z%(2*L)
 return u if u<=L else 2*L-u
def sub(p,q):return p[0]-q[0],p[1]-q[1]
def cross(p,q):return p[0]*q[1]-p[1]*q[0]
def strp(p):return [str(x) for x in p]
fixtures=[
 ('thin-offset',(3,1,2,F(1,2),1,F(1,2),F(1,2),F(5,2))),
 ('both-smooth-portals',(3,1,2,F(1,2),1,F(1,6),F(1,2),F(5,2))),
 ('rounding-tie-and-target-boundary',(3,1,2,F(5,6),1,F(1,2),F(1,2),F(5,2))),
 ('unequal-widths',(10,7,8,F(2,3),F(3,5),F(4,7),F(5,3),9))]
results=[];allchecks=0
for name,raw in fixtures:
 guard();A,B,a,Hs,g,Ht,xs,xt=map(F,raw);W=A-a;D=Hs+g+Ht
 assert B>=W and 0<xs<B and a<xt<A
 k=max(0,ceil(((2*B*g-g*xs)/Hs/A-1)/2));K=(2*k+1)*A
 ratio=(Hs*K+g*xs)/(2*B*g);assert ratio>=1
 n=floor(ratio+F(1,2));assert n>=1
 I=((2*n*B-xs-B)/Hs,(2*n*B-xs+B)/Hs)
 J=((2*n*B+K-xs-W)/(Hs+g),(2*n*B+K-xs+W)/(Hs+g))
 assert 0<I[0]<=J[0]<J[1]<=I[1]
 Y=A-xt;Zlo=xs+D*J[0]-2*n*B-K;Zhi=xs+D*J[1]-2*n*B-K
 assert Zhi-Zlo>2*W
 m=floor((Zlo-Y)/(2*W))+1;image=Y+2*m*W
 assert Zlo<image<Zhi
 tau=(2*n*B+K+image-xs)/D;assert J[0]<tau<J[1]
 z=xs+Hs*tau-2*n*B;w=xs+(Hs+g)*tau-2*n*B-K
 assert abs(z)<B and abs(w)<W
 # Realize the fixed heights; the theorem depends only on these positive distances.
 ys=F(1,2);b=ys+Hs;c=b+g;yt=c+Ht;C=yt+F(1,2)
 vertices=[(0,0),(B,0),(B,b),(A,b),(A,C),(a,C),(a,c),(0,c)]
 vertices=[tuple(map(F,p)) for p in vertices]
 def xat(y):
  if y<=b:return fold(xs+tau*(y-ys),B)
  if y<=c:return fold(z+tau*(y-b),A)
  return A-fold(w+tau*(y-c),W)
 assert xat(ys)==xs and xat(yt)==xt
 assert fold(xs+Hs*tau,B)==fold(z,A)
 assert fold(z+g*tau,A)==A-fold(w,W)
 times={ys,b,c,yt}
 stages=[(ys,b,xs,B),(b,c,z,A),(c,yt,w,W)]
 for lo,hi,base,width in stages:
  for line in range(floor(base/width)-1,ceil((base+tau*(hi-lo))/width)+2):
   t=lo+(line*width-base)/tau
   if lo<t<hi:times.add(t)
 # A portal fold exactly at b/c is already included.
 path=[(xat(y),y) for y in sorted(times)]
 def inside(p):
  x,y=p
  return (0<x<B and 0<y<b) or (0<x<A and b<y<c) or (a<x<A and c<y<C) or (y==b and 0<x<B) or (y==c and a<x<A)
 contact_at={};checks=0
 for index,(p,q) in enumerate(zip(path,path[1:])):
  guard();delta=sub(q,p);assert delta[1]>0 and abs(delta[0]/delta[1])==tau
  for j,u in enumerate(vertices):
   v=vertices[(j+1)%8];e=sub(v,u);det=cross(delta,e)
   assert det!=0 # All actual walls are axial and both components of each leg are nonzero.
   t=cross(sub(u,p),e)/det;s=cross(sub(u,p),delta)/det
   if 0<=t<=1 and 0<=s<=1:
    assert s not in (0,1),'genuine corner'
    assert t in (0,1),'unlisted actual wall'
    assert e[0]==0,'horizontal contact'
    vertex_index=index if t==0 else index+1
    assert vertex_index not in (0,len(path)-1),'actual endpoint on boundary'
    contact_at[vertex_index]=j;checks+=1
  midpoint=((p[0]+q[0])/2,(p[1]+q[1])/2);assert inside(midpoint);checks+=1
 for j,p in enumerate(path[1:-1],1):
  incoming=sub(p,path[j-1]);outgoing=sub(path[j+1],p)
  if j in contact_at:reflected=(-incoming[0],incoming[1])
  else:reflected=incoming
  assert cross(reflected,outgoing)==0 and sum(x*y for x,y in zip(reflected,outgoing))>0
  checks+=1
 if name=='both-smooth-portals':assert z==w==0 and any(p==(0,b) for p in path) and any(p==(A,c) for p in path)
 if name=='rounding-tie-and-target-boundary':assert ratio.denominator==2 and J[0]==I[0] and Zlo==Y and m==1
 allchecks+=checks
 results.append({'name':name,'input_keys':['A','B','a','Hs','g','Ht','xs','xt'],'input':list(map(str,raw)),'k':k,'n':n,'m':m,'slope':str(tau),'source_gate':str(z),'target_gate':str(w),'reflections':len(contact_at),'checks':checks,'S':strp(path[0]),'T':strp(path[-1]),'vertices':[strp(p) for p in vertices],'path':[{'point':strp(p),'wall':contact_at.get(i),'transparent_portal':i not in contact_at and 0<i<len(path)-1} for i,p in enumerate(path)]})
out={'status':'EXACT_WIDE_MIDDLE_CONSTRUCTOR_AND_ACTUAL_WALLS_PASS','fixed_fixtures':len(results),'checks':allchecks,'reflections':sum(x['reflections'] for x in results),'fixtures':results,'whole_goal_complete':False,'kind':'prescribed exact fixture verification; arbitrary-real theorem remains a hand proof awaiting independent review','source_sha256':{n:hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in ('wide-middle-onepass.md','wide-middle-constructor-check.py')}}
(HERE/'wide-middle-constructor-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='fixtures'}))
