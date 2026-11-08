#!/usr/bin/env python3
"""One analytically specified r4 control; no room/direction search."""
from pathlib import Path
from fractions import Fraction as F
import json
P=[(-8,-200),(16,-200),(16,-400),(56,-400),(56,-200),(24,-200),(24,0),(16,0),(16,2),(0,2),(0,0),(-8,0)]
S=(F(4),F(-2));T=(F(54),F(-300));B=(F(10946,249),F(-400))
def sub(a,b):return (a[0]-b[0],a[1]-b[1])
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def plus(a,t,v):return (a[0]+t*v[0],a[1]+t*v[1])
def meet(a,b,c,d):
 if a[0]==b[0] and c[0]==d[0]:return a[0]==c[0] and max(min(a[1],b[1]),min(c[1],d[1]))<=min(max(a[1],b[1]),max(c[1],d[1]))
 if a[1]==b[1] and c[1]==d[1]:return a[1]==c[1] and max(min(a[0],b[0]),min(c[0],d[0]))<=min(max(a[0],b[0]),max(c[0],d[0]))
 if a[1]==b[1]:return meet(c,d,a,b)
 return min(c[0],d[0])<=a[0]<=max(c[0],d[0]) and min(a[1],b[1])<=c[1]<=max(a[1],b[1])
def hits(p,v):
 out=[]
 for i,(a,b) in enumerate(zip(P,P[1:]+P[:1])):
  e=sub(b,a);d=cross(v,e)
  if not d:continue
  t=cross(sub(a,p),e)/d;u=cross(sub(a,p),v)/d
  if t>0 and 0<=u<=1:out.append((t,i,u,plus(p,t,v)))
 t=min(h[0] for h in out)
 return [h for h in out if h[0]==t]
E=list(zip(P,P[1:]+P[:1]))
for i,(a,b) in enumerate(E):
 for j,(c,d) in enumerate(E):
  if j>i and j-i not in (1,len(E)-1):assert not meet(a,b,c,d)
turns=[cross(sub(P[i],P[i-1]),sub(P[(i+1)%len(P)],P[i])) for i in range(len(P))]
assert all(turns) and sum(x<0 for x in turns)==4
assert -8<S[0]<24 and -200<S[1]<0
assert 16<T[0]<56 and -400<T[1]<-200
assert all(x.denominator==1 and x.numerator%2==0 for p in [S,T] for x in p)
direct=hits(S,sub(T,S))
assert len(direct)==1 and direct[0][0]==F(2,5) and direct[0][3]==(24,F(-606,5))
first=hits(S,sub(B,S)); assert len(first)==1 and first[0][0]==1 and first[0][1]==2 and 0<first[0][2]<1
second=hits(B,sub(T,B)); assert second[0][0]>1
v=sub(B,S);vv=(v[0],-v[1]);u=sub(T,B)
assert cross(vv,u)==0 and vv[0]*u[0]+vv[1]*u[1]>0
seam_x=4+F(50)*F(198,498)
assert seam_x==F(1982,83) and 16<seam_x<24
# All exterior horizontal supports before the roof cap lie in200Z.
ys=sorted(set(a[1] for a,b in E if a[1]==b[1] and a[1]!=2))
assert ys==[-400,-200,0]
res=sorted({(s*2+t*300)%400 for s in [-1,1] for t in [-1,1]})
assert res==[98,102,298,302] and min(min(x,400-x) for x in res)==98
out={'status':'PASS_ONE_PRESCRIBED_NONDIRECT_R4_CONTROL','room':P,'r':4,'S':[4,-2],'T':[54,-300],'direct_visibility':False,'first_direct_obstruction':['24','-606/5'],'actual_one_bounce_witness':[['4','-2'],['10946/249','-400'],['54','-300']],'strict_internal_seam_crossing_x':'1982/83','roof_ear':{'x':[0,16],'y':[0,2]},'exterior_horizontal_supports':ys,'all_word_image_group':'sign*y+400n','all_depth_difference_residues':res,'minimum_abs_difference':98,'two_h_max':4,'all_ear_cuts':'0<=c<2, c cancels from differences','fixed_ear_OR01_C_possible':False,'other_chambers_excluded':False,'G8_refuted':False,'whole_goal_complete':False}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
