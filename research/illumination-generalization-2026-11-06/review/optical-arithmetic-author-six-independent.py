#!/usr/bin/env python3
"""Independent prescribed six-wall replay and maximal guard derivation."""
from fractions import Fraction as F
from pathlib import Path
import json
P=[(-8,-200),(16,-200),(16,-400),(56,-400),(56,-200),(24,-200),(24,0),(16,0),(16,2),(0,2),(0,0),(-8,0)]
S=(F(4),F(-2));T=(F(54),F(-300))
def sub(a,b):return (a[0]-b[0],a[1]-b[1])
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def plus(a,t,v):return (a[0]+t*v[0],a[1]+t*v[1])
def hits(p,v):
 hs=[]
 for i,(a,b) in enumerate(zip(P,P[1:]+P[:1])):
  e=sub(b,a);d=cross(v,e)
  if not d:continue
  t=cross(sub(a,p),e)/d;u=cross(sub(a,p),v)/d
  if t>0 and 0<=u<=1:hs.append((t,i,u,plus(p,t,v)))
 t=min(z[0] for z in hs);return [z for z in hs if z[0]==t]
def reflect(v,i):
 a,b=P[i],P[(i+1)%len(P)]
 return (-v[0],v[1]) if a[0]==b[0] else (v[0],-v[1])
m=F(97,253);p=S;v=(m,F(1));events=[]
for expected in [8,5,11,3,2,1]:
 hh=hits(p,v);assert len(hh)==1 and hh[0][1]==expected and 0<hh[0][2]<1
 tv=sub(T,p)
 if cross(tv,v)==0:
  tau=tv[0]/v[0];assert not 0<tau<hh[0][0]
 p=hh[0][3];events.append({'wall_index':expected,'point':[str(x) for x in p]});v=reflect(v,expected)
tv=sub(T,p);assert cross(tv,v)==0
tau=tv[0]/v[0];assert tau>0 and tau<hits(p,v)[0][0]
# Independent composition to terminal mouth image: reverse evaluation of forward suffix.
def rx(x,c):return 2*c-x
x=F(54)
for c in [16,56,-8,24]:x=rx(x,F(c))
y=2*F(-400)-F(-300)
assert x==198 and y==-500
assert (198-4)/F(2+500+4)==m
constraints=[('mpositive',F(0),None),('source mouth',F(-2),F(6)),('T-left smooth and bottom-first order',F(19,50),None),('bottom point',F(19,50),F(39,50)),('B2 right point',F(13,50),F(39,50)),('seam',F(11,30),F(59,150)),('B1 left point',F(71,250),F(71,150)),('B1 right point',F(87,250),F(29,50)),('mouth',F(91,250),F(99,250))]
lo=max(c[1] for c in constraints);hi=min(c[2] for c in constraints if c[2] is not None)
assert (lo,hi)==(F(19,50),F(59,150)) and lo<m<hi
A=(506*lo-194)/32;B=(506*hi-194)/32
assert (A,B)==(F(-43,800),F(377,2400))
assert -1<A<0<B<1
# Lower endpoint first reverse hit is forbidden convex corner.
hh=hits(T,(-lo,F(-1)))
assert len(hh)==2 and all(z[3]==(16,-400) for z in hh)
# Upper endpoint reaches the forbidden reflex seam endpoint after three smooth hits.
p=T;v=(-hi,F(-1))
for idx in [1,2,3]:
 hh=hits(p,v);assert len(hh)==1 and hh[0][1]==idx and 0<hh[0][2]<1
 p=hh[0][3];v=reflect(v,idx)
hh=hits(p,v);assert len(hh)==2 and all(z[3]==(16,-200) for z in hh)
out={'status':'PASS_PRESCRIBED_AUTHOR_SIX_REFLECTION_CONTROL','method':'Own rational first-wall ray replay and independent hand inequality conversion; no author code','m':str(m),'events':events,'actual_target':[54,-300],'first_actual_target':True,'developed_target_image':['198','-500'],'a':2,'b':500,'K':506,'epsilon':1,'maximal_joint_guard_component':[str(lo),str(hi)],'guard_constraints':[{'name':name,'lo':str(l),'hi':str(u) if u is not None else None} for name,l,u in constraints],'normalized_residue_window':[str(A),str(B)],'only_winding_label':0,'K_width':'506/75','two_w':32,'lower_endpoint_corner':['16','-400'],'upper_endpoint_corner':['16','-200'],'global_C8_proved':False,'whole_goal_complete':False}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
