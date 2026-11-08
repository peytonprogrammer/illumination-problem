"""Two prescribed lower-end events plus a rejected left-triangle suffix; no scans."""
from pathlib import Path
from fractions import Fraction as F
import importlib.util,json
base=Path(__file__).resolve().parent
ring=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
def fan(a,start,count):
 return [tuple(sorted((a,(a[0]+ring[j%8][0],a[1]+ring[j%8][1]),(a[0]+ring[(j+1)%8][0],a[1]+ring[(j+1)%8][1])))) for j in range(start,start+count)]
room=[]
for args in [((0,0),0,8),((4,0),0,8),((2,0),0,4),((2,2),6,1),
 ((6,0),4,1),((4,2),5,1),((4,-2),0,2),((-2,0),7,1),((0,2),6,1),((0,-2),1,1)]:room+=fan(*args)
def load(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
geom=load('frozen_geometry',base.parent/'k5-proof-pilot/inputs/illumination_geometry.py')
a=load('fixed_guard_checker',base.parent/'persisted-replay/audit.py')
def p(x,y):return(F(x),F(y))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def mul(k,a):return tuple(k*x for x in a)
def ref(a,n,c):return sub(a,mul(2*(dot(n,a)-c)/dot(n,n),n))
def V(x):return(p(1,0),F(x))
def H(y):return(p(0,1),F(y))
S=p(0,0);T=p(4,0);B=p(5,-1);w=p(5,3);u=p(0,-1)
first=[S,p(F(5,3),1),B];fm=[H(1)];ft=[F(1,3),F(2,3)]
triangle_geometry=geom.check({'triangles':room,'marked':[(0,0),(4,0)],'require_simple':True},strict=True)
assert triangle_geometry['walls']==25 and triangle_geometry['tiles']==28
# Prescribed triangular-cap negative control: its affine endpoint matches,
# but its return crosses an absent upper-right triangle.
missing=a.segment(p(F(7,2),F(3,2)),p(5,F(3,5)))-frozenset(room)
assert missing==frozenset({((4,1),(4,2),(5,1))})
# The one prescribed square substitution gives a different physical suffix.
fixtures=[('square',list(set(room)-set(fan((4,2),5,1))|set(fan((4,2),4,2))),
 [B,p(F(16,5),2),p(3,F(5,3)),T],[H(2),V(3)],[F(3,5),F(1,15),F(1,3)],26),
 ('right_triangle',list(set(room)-set(fan((4,2),5,1))|set(fan((4,2),6,1))),
 [B,p(F(19,5),1),p(3,F(-1,3)),p(F(17,5),-1),T],
 [H(1),V(3),H(-1)],[F(2,5),F(4,15),F(2,15),F(1,5)],25)]
results=[]
for name,tiles,second,sm,st,walls in fixtures:
 receipt=geom.check({'triangles':tiles,'marked':[(0,0),(4,0)],'require_simple':True},strict=True)
 assert receipt['walls']==walls and receipt['tiles']==walls+3
 assert receipt['sectors']['(5, -1)']==[5] and receipt['sectors']['(5, 0)']==[6]
 if name=='right_triangle':assert receipt['sectors']['(5, 1)']==[3]
 v=w
 for pts,mirrors,times in [(first,fm,ft),(second,sm,st)]:
  assert sum(times)==1
  for i,t in enumerate(times):
   assert sub(pts[i+1],pts[i])==mul(t,v)
   if i<len(mirrors):
    n,c=mirrors[i];assert dot(n,pts[i+1])==c;v=ref(v,n,F(0))
  if pts is first:
   assert v==p(5,-3)
   v=ref(v,p(1,-1),F(0));assert v==p(-3,5)
 R=frozenset(tiles)
 for pts in [first,second]:
  for x,y in zip(pts,pts[1:]):assert a.segment(x,y)<=R,(name,x,y,a.segment(x,y)-R)
  for x,y,z in zip(pts,pts[1:],pts[2:]):
   used,absent=a.bounce(x,y,z);assert used<=R and not absent&R
 assert a.incident(S)<=R and a.incident(T)<=R
 image=T
 for n,c in reversed(sm):image=ref(image,n,c)
 assert image==p(2,4)
 def images(t):
  return ref(ref(image,p(1,-1),F(6)+t),*H(1)),ref(p(5,-1-t),*H(1))
 for t in [F(-1,100),F(0),F(1,100)]:
  developed,corner=images(t)
  assert developed==p(10+t,6+t) and corner==p(5,3+t)
 developed,corner=images(F(0));eps=F(1,100);im1,c1=images(eps)
 target_velocity=mul(1/eps,sub(im1,developed))
 corner_velocity=mul(1/eps,sub(c1,corner))
 Q=sub(target_velocity,mul(2,corner_velocity));det=w[0]*Q[1]-w[1]*Q[0]
 assert Q==p(1,-1) and det==-8
 results.append(dict(cap=name,geometry=receipt,prescribed_triangles=tiles,first_half=first,
  second_half=second,developed_actual_target=developed,developed_corner=corner,
  target_velocity=target_velocity,corner_velocity=corner_velocity,
  half_vector=w,defect=Q,determinant=det))
out=dict(status='PRESCRIBED_LOWER_END_SQUARE_AND_RIGHT_CAP_PASS',cases=results,
 rejected_triangle_suffix=dict(status='INVALID_EARLIER_VERTICAL_WALL_HIT',missing_tiles=sorted(missing),geometry=triangle_geometry),
 scope='Connected-H lower end with Nright and either upperTleft m2 or upperTright m1; pi/forcing require hand proof.',
 independent_review=dict(square='ACCEPTED_SCOPED_HAND_REVIEW31817',right_triangle='ACCEPTED_SCOPED_HAND_REVIEW57809'),universal_pocket_detection='OPEN',discovery_runs=0)
(base/'pocket-end-lower.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps(dict(status=out['status'],caps=[dict(cap=r['cap'],walls=r['geometry']['walls'],
 first_half=r['first_half'],second_half=r['second_half'],defect=r['defect'],determinant=r['determinant'])
 for r in results]),indent=2,default=str))
