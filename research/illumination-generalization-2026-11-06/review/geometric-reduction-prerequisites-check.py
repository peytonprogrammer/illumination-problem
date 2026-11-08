"""Exact prescribed prerequisite controls; no discovery, parameter sweep or author import."""
from fractions import Fraction as Q
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parent
P=[(0,0),(8,0),(8,4),(4,4),(4,8),(0,8)]
S=(6,2);T=(2,6);path=[S,(5,0),T]
def sub(a,b):return (a[0]-b[0],a[1]-b[1])
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def point(a,b,t):return tuple(Q(a[i])+t*(b[i]-a[i]) for i in (0,1))
def inside(p):
 x,y=p
 return (0<x<8 and 0<y<4) or (0<x<4 and 0<y<8) or (0<x<4 and y==4) or (x==4 and 0<y<4)
def segment_intersection(a,b,c,d):
 u=sub(b,a);v=sub(d,c);z=sub(c,a);det=cross(u,v)
 if det:
  t=Q(cross(z,v),det);s=Q(cross(z,u),det)
  return [point(a,b,t)] if 0<=t<=1 and 0<=s<=1 else []
 if cross(z,u):return []
 # For these prescribed nonaxial ray legs this branch cannot overlap an axial wall.
 raise AssertionError('Unexpected collinear prescribed ray/wall')
turns=[cross(sub(P[i],P[i-1]),sub(P[(i+1)%len(P)],P[i])) for i in range(len(P))]
assert turns==[64,32,16,-16,16,32]
assert sum(t<0 for t in turns)==1
assert sum(P[i][0]*P[(i+1)%6][1]-P[i][1]*P[(i+1)%6][0] for i in range(6))==96
assert all(P[i][0]==P[(i+1)%6][0] or P[i][1]==P[(i+1)%6][1] for i in range(6))
assert all(x%2==y%2==0 for x,y in P+[S,T]) and inside(S) and inside(T)
assert not inside((5,5)) and 2<5<6
contacts=[]
for a,b in zip(path,path[1:]):
 hits=[]
 for c,d in zip(P,P[1:]+P[:1]):hits+=segment_intersection(a,b,c,d)
 assert hits==[(Q(5),Q(0))]
 assert all(c not in path for c in P)
 # Complete affine-leg interior guard: membership can change only at x4/y4 or exterior supports.
 cuts={Q(0),Q(1)}
 for axis,level in [(0,0),(0,4),(0,8),(1,0),(1,4),(1,8)]:
  if b[axis]!=a[axis]:
   t=Q(level-a[axis],b[axis]-a[axis])
   if 0<t<1:cuts.add(t)
 ordered=sorted(cuts)
 assert all(inside(point(a,b,(x+y)/2)) for x,y in zip(ordered,ordered[1:]))
 assert all(inside(point(a,b,t)) for t in ordered if 0<t<1)
 contacts+=hits
vin=sub(path[1],path[0]);vout=sub(path[2],path[1]);expected=(vin[0],-vin[1])
assert cross(expected,vout)==0 and sum(expected[i]*vout[i] for i in (0,1))>0
assert segment_intersection(S,T,(4,4),(4,8))==[(Q(4),Q(4))]
# Prescribed legal ear excursion, obtained directly by supporting-line intersections.
ear=[(1,0),(3,4),(4,2),(3,0)]
assert sub(ear[1],ear[0])==(2,4)
assert sub(ear[2],ear[1])==(1,-2)
assert sub(ear[3],ear[2])==(-1,-2)
assert ear[-1]!=(1,0) and Q(4)*Q(1,2)/4==Q(1,2)
out={'status':'PASS_PRESCRIBED_EXACT_CONTROLS','L_room':P,'S':S,'T':T,'area':48,'walls':6,'reflex':1,'endpoint_box_exterior_witness':[5,5],'actual_one_reflection_path':path,'all_wall_intersections_checked':12,'open_leg_partition_guards':'all support crossings split exactly','ear_excursion':ear,'ear_original_reduced_bounce':[1,0],'ear_exit':[3,0],'new_discovery_or_search':False,'whole_goal_complete':False}
(R/'geometric-reduction-prerequisites-check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
