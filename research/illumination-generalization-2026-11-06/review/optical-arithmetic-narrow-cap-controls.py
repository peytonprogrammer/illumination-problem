#!/usr/bin/env python3
"""Two hand-prescribed actual chamber paths, no room/direction search."""
from fractions import Fraction as F
from pathlib import Path
import json

def sub(a,b):return (a[0]-b[0],a[1]-b[1])
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def plus(a,t,v):return (a[0]+t*v[0],a[1]+t*v[1])
def fp(p):return tuple(F(x) for x in p)
def first(p,v,P):
 hh=[]
 for i,(a,b) in enumerate(zip(P,P[1:]+P[:1])):
  e=sub(b,a);den=cross(v,e)
  if not den:continue
  t=cross(sub(a,p),e)/den;u=cross(sub(a,p),v)/den
  if t>0 and 0<=u<=1:hh.append((t,i,u,plus(p,t,v)))
 t=min(x[0] for x in hh)
 return [x for x in hh if x[0]==t]
def path(P,ps):
 ps=[fp(p) for p in ps];events=[]
 for j,(p,q) in enumerate(zip(ps,ps[1:])):
  v=sub(q,p);hh=first(p,v,P)
  if j<len(ps)-2:
   assert len(hh)==1 and hh[0][0]==1 and 0<hh[0][2]<1
   a,b=P[hh[0][1]],P[(hh[0][1]+1)%len(P)]
   reflected=(-v[0],v[1]) if a[0]==b[0] else (v[0],-v[1])
   outgoing=sub(ps[j+2],q)
   assert cross(reflected,outgoing)==0
   assert reflected[0]*outgoing[0]+reflected[1]*outgoing[1]>0
   events.append({'point':[str(z) for z in q],'wall_index':hh[0][1]})
  else:assert hh[0][0]>1
  # No earlier occurrence of actual target, so final path is first-arrival.
  tv=sub(ps[-1],p)
  if cross(tv,v)==0:
   idx=0 if v[0] else 1;t=tv[idx]/v[idx]
   assert not (0<t<1)
 return events

P2=[(-8,-200),(24,-200),(24,0),(16,0),(16,2),(0,2),(0,0),(-8,0)]
P4=[(-8,-200),(16,-200),(16,-400),(56,-400),(56,-200),(24,-200),(24,0),(16,0),(16,2),(0,2),(0,0),(-8,0)]
p2=[(4,-2),(F(216,53),2),(6,-100)]
p4=[(4,-2),(F(1512,353),2),(F(11562,353),-400),(F(16562,353),-200),(54,-300)]
E2=path(P2,p2);E4=path(P4,p4)
assert [x['wall_index'] for x in E4]==[8,2,4]
# Whole-interval access: extrema suffice for each affine coordinate on a convex band.
J2=(F(1,100),F(3,100));J4=(F(7,100),F(9,125))
for m in J2:
 assert 0<4+2*m<16 and 0<6-100*m<16
 # Entire two exterior straight prefixes lie in convex B.
 assert -8<min(4,4+2*m) and max(4,4+2*m)<24
 assert -8<min(6,6-100*m) and max(6,6-100*m)<24
for m in J4:
 assert 0<4+2*m<16
 assert 24<54-100*m<56     # first upper-wall bounce in B2
 assert 16<54-300*m<56     # bottom bounce
 assert 16<54-500*m<24     # transparent seam
 assert 0<54-700*m<16      # first mouth arrival
m2=F(1,53);m4=F(25,353)
assert 106*m2==6-4 and 706*m4==54-4
assert J2[0]<m2<J2[1] and J4[0]<m4<J4[1]
assert 106*(J2[1]-J2[0])<32 and 706*(J4[1]-J4[0])<32
assert 4+2*m4+4*m4==54-700*m4
assert F(1512,353)+202*m4==F(6562,353) and 16<F(6562,353)<24
out={'status':'PASS_TWO_PRESCRIBED_ACTUAL_NARROW_CAP_PATHS','method':'Own exact finite-wall first-hit/specularity and affine whole-interval guard proof; no author imports or discovery','r2':{'room':P2,'path':[[str(z) for z in p] for p in p2],'events':E2,'m':'1/53','a':2,'b':100,'h':2,'K':106,'alpha':4,'beta':6,'epsilon':1,'J':['1/100','3/100'],'K_width':'53/25','two_w':32,'first_actual_target':True},'r4':{'room':P4,'path':[[str(z) for z in p] for p in p4],'events':E4,'m':'25/353','a':2,'b':700,'h':2,'K':706,'alpha':4,'beta':54,'epsilon':1,'J':['7/100','9/125'],'K_width':'353/250','two_w':32,'ear_exit_x':'1562/353','transparent_seam_x':'6562/353','reverse_target_word':['y=-200','y=-400'],'first_actual_target':True},'old_all_word_width_obstructions_preserved':True,'global_selection_proved':False,'whole_goal_complete':False}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
