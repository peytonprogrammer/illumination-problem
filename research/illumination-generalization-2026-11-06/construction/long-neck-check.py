#!/usr/bin/env python3
"""Read-only exact controls for the prescribed two-end-beam neck formula; no search."""
from fractions import Fraction as F
from datetime import datetime,timezone
import json

def cr(v,w):return v[0]*w[1]-v[1]*w[0]
def sub(v,w):return v[0]-w[0],v[1]-w[1]
def dot(v,w):return v[0]*w[0]+v[1]*w[1]
def on(a,b,z):return cr(sub(b,a),sub(z,a))==0 and all(min(a[k],b[k])<=z[k]<=max(a[k],b[k]) for k in (0,1))
def edges(p):return list(zip(p,p[1:]+p[:1]))
def inside(p,z):
 if any(on(a,b,z) for a,b in edges(p)):return False
 wind=0
 for a,b in edges(p):
  if a[1]<=z[1]<b[1] and cr(sub(b,a),sub(z,a))>0:wind+=1
  if b[1]<=z[1]<a[1] and cr(sub(b,a),sub(z,a))<0:wind-=1
 return wind!=0

def boundary(rects):
 xs=sorted({r[k] for r in rects for k in (0,1)});ys=sorted({r[k] for r in rects for k in (2,3)})
 sides=set()
 for a,b in zip(xs,xs[1:]):
  for c,d in zip(ys,ys[1:]):
   if not any(x0<(a+b)/2<x1 and y0<(c+d)/2<y1 for x0,x1,y0,y1 in rects):continue
   cell=[(a,c),(b,c),(b,d),(a,d)]
   for e in edges(cell):
    rev=(e[1],e[0])
    if rev in sides:sides.remove(rev)
    else:sides.add(e)
 nxt={a:b for a,b in sides};assert len(nxt)==len(sides)
 start=min(nxt);p=[start];z=nxt[start]
 while z!=start:
  assert z not in p;p.append(z);z=nxt[z]
 assert len(p)==len(sides)
 while True:
  q=[z for j,z in enumerate(p) if cr(sub(z,p[j-1]),sub(p[(j+1)%len(p)],z))!=0]
  if len(q)==len(p):return p
  p=q

def verify(p,path,S,T):
 assert path[0]==S and path[-1]==T and inside(p,S) and inside(p,T)
 for a,b in zip(path,path[1:]):
  assert a!=b
  mid=((a[0]+b[0])/2,(a[1]+b[1])/2);assert inside(p,mid)
  d=sub(b,a)
  for v,w in edges(p):
   e=sub(w,v);den=cr(d,e)
   if den:
    t=cr(sub(v,a),e)/den;u=cr(sub(v,a),d)/den
    assert not(0<t<1 and 0<=u<=1),('interior boundary',a,b,v,w,t,u)
   elif cr(sub(v,a),d)==0:
    k=0 if d[0] else 1;lo,hi=sorted(((v[k]-a[k])/d[k],(w[k]-a[k])/d[k]))
    assert max(lo,F(0))>=min(hi,F(1))
  assert all(z==a or z==b or not on(a,b,z) for z in p)
 for j,z in enumerate(path[1:-1]):
  assert z not in p
  wall=[(a,b) for a,b in edges(p) if on(a,b,z)];assert len(wall)==1
  a,b=wall[0];e=sub(b,a);n=(-e[1],e[0]);vin=sub(z,path[j]);vout=sub(path[j+2],z)
  reflected=tuple(vin[k]-2*dot(vin,n)*n[k]/dot(n,n) for k in (0,1))
  assert cr(reflected,vout)==0 and dot(reflected,vout)>0
  assert dot(vin,n)*dot(vout,n)<0
 return len(path)-2

def ser(p):return [[str(x),str(y)] for x,y in p]
rows=[];w=F(2);u=F(-3,5);v=F(-1,3);delta=v-u;a=b=F(5);alpha=F(3);C=a+b
assert max(F(0),2*w/delta-C)==5
for sigma in (-1,1):
 beta=F(3 if sigma==-1 else -1);c=sigma*beta-alpha
 for length in (6,100):
  L=F(length);left=(L+C)*u-c
  n=(left/(2*w)).numerator//(left/(2*w)).denominator+1
  tau=(c+2*n*w)/(L+C);assert u<tau<v
  zleft=alpha+a*tau;zright=beta-b*sigma*tau
  assert 0<zleft<w and 0<zright<w
  Yright=alpha+tau*(a+L);assert Yright==2*n*w+sigma*zright
  rects=[tuple(map(F,z)) for z in [(-4,0,0,2),(-4,-2,2,4),(-6,-4,0,1),(0,length,0,2),(length,length+4,0,2),(length+2,length+4,2,4) if sigma==-1 else (length+2,length+4,-2,0)]]
  poly=boundary(rects)
  S=(F(-3),F(3));T=(L+3,beta)
  neck=[]
  for k in range(int(min(zleft,Yright)//w)-1,int(max(zleft,Yright)//w)+2):
   x=(k*w-zleft)/tau
   if 0<x<L:neck.append((x,F(0) if k%2==0 else w))
  neck.sort()
  path=[S,(F(-4),alpha+tau)]+neck+[(L+4,beta-sigma*tau),T]
  count=verify(poly,path,S,T)
  assert all((2*z).denominator==1 and int(2*z)%2==0 for z in (*S,*T))
  rows.append({'sigma':sigma,'L':str(L),'w':str(w),'I':[str(u),str(v)],'threshold':'5','n':n,'tau':str(tau),'entry_y':str(zleft),'exit_y':str(zright),'polygon':ser(poly),'actual_S':list(map(str,S)),'actual_T':list(map(str,T)),'path':ser(path),'maximal_walls':len(poly),'reflections':count,'all_actual_leg_corner_specular_guards':True,'factor2_gives_canonical45_interior_A_marks':True})
print(json.dumps({'status':'FOUR_PRESCRIBED_PHASE_AND_PHYSICAL_PATH_CONTROLS_PASS','kind':'exact finite prescribed verification, no discovery and no independent-peer claim','checked_utc':datetime.now(timezone.utc).isoformat(),'rows':rows,'total_reflections':sum(r['reflections'] for r in rows),'whole_goal_complete':False},indent=2))
