"""One prescribed upper-end event and raw room; no discovery scans."""
from pathlib import Path
from fractions import Fraction as F
import importlib.util,json
base=Path(__file__).resolve().parent
ring=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
def fan(a,start,count):
 return [tuple(sorted((a,(a[0]+ring[j%8][0],a[1]+ring[j%8][1]),(a[0]+ring[(j+1)%8][0],a[1]+ring[(j+1)%8][1])))) for j in range(start,start+count)]
room=[]
for args in [((0,0),0,8),((4,0),0,8),((2,0),0,4),((2,2),6,1),
             ((6,0),3,1),((4,2),6,2),((4,-2),2,1),((-2,0),0,1),
             ((0,2),6,1),((0,-2),2,1)]:room+=fan(*args)
def load(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
geom=load('frozen_geometry',base.parent/'k5-proof-pilot/inputs/illumination_geometry.py')
receipt=geom.check({'triangles':room,'marked':[(0,0),(4,0)],'require_simple':True},strict=True)
assert receipt['walls']==25 and receipt['tiles']==28
assert receipt['sectors']['(5, 1)']==[5] and receipt['sectors']['(5, 0)']==[6]
a=load('fixed_guard_checker',base.parent/'persisted-replay/audit.py')
def p(x,y):return(F(x),F(y))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def mul(k,a):return tuple(k*x for x in a)
def ref(a,n,c):return sub(a,mul(2*(dot(n,a)-c)/dot(n,n),n))
def V(x):return(p(1,0),F(x))
def H(y):return(p(0,1),F(y))
S=p(0,0);T=p(4,0);B=p(5,1);w=p(-9,1);u=p(0,1)
D=(p(1,-1),F(-2));corner_D=(p(1,1),F(6))
first=[S,p(F(-9,5),F(1,5)),p(F(-16,9),0),p(F(-7,4),F(1,4)),B]
fm=[D,H(0),D];ft=[F(1,5),F(1,45),F(1,36),F(3,4)]
second=[B,p(F(43,9),-1),p(F(40,9),2),p(F(37,9),-1),T]
sm=[H(-1),H(2),H(-1)];st=[F(2,9),F(1,3),F(1,3),F(1,9)]
v=w
for pts,mirrors,times in [(first,fm,ft),(second,sm,st)]:
 assert sum(times)==1
 for i,t in enumerate(times):
  assert sub(pts[i+1],pts[i])==mul(t,v)
  if i<len(mirrors):
   n,c=mirrors[i];assert dot(n,pts[i+1])==c;v=ref(v,n,F(0))
 if pts is first:
  assert v==p(9,1)
  v=ref(v,corner_D[0],F(0));assert v==p(-1,-9)
R=frozenset(room)
for pts in [first,second]:
 for x,y in zip(pts,pts[1:]):assert a.segment(x,y)<=R
 for x,y,z in zip(pts,pts[1:],pts[2:]):
  used,absent=a.bounce(x,y,z);assert used<=R and not absent&R
assert a.incident(S)<=R and a.incident(T)<=R
suffix=T
for n,c in reversed(sm):suffix=ref(suffix,n,c)
assert suffix==p(4,-8)
corner=B
for n,c in reversed(fm):corner=ref(corner,n,c)
assert corner==w
# Derive derivatives from the affine image function, not output literals.
def images(t):
 target=ref(suffix,corner_D[0],F(6)+t)
 assert target==p(14+t,2+t)
 for n,c in reversed(fm):target=ref(target,n,c)
 moved_corner=p(5,1+t)
 for n,c in reversed(fm):moved_corner=ref(moved_corner,n,c)
 return target,moved_corner
for t in [F(-1,100),F(0),F(1,100)]:
 target,moved_corner=images(t)
 assert target==p(-18-t,2+t) and moved_corner==p(-9,1+t)
image,corner=images(F(0));eps=F(1,100);im1,c1=images(eps)
target_velocity=mul(1/eps,sub(im1,image))
corner_velocity=mul(1/eps,sub(c1,corner))
Q=sub(target_velocity,mul(2,corner_velocity));det=w[0]*Q[1]-w[1]*Q[0]
assert Q==p(-1,-1) and det==10
out=dict(status='PRESCRIBED_UPPER_END_SOURCE_CAP_PASS',geometry=receipt,prescribed_triangles=room,
 first_half=first,second_half=second,half_vector=w,developed_corner=corner,
 developed_actual_target=image,target_velocity=target_velocity,corner_velocity=corner_velocity,defect=Q,determinant=det,
 scope='Connected-H upper end, opposite Tdown LEFT, Sleft UPPER; pi and forcing require hand proof.',
 independent_review='ACCEPTED_SCOPED_HAND_PROOF_WITH_FRAME_AND_COVERAGE_CORRECTIONS',universal_pocket_detection='OPEN',discovery_runs=0)
(base/'pocket-end-upper.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['geometry','prescribed_triangles']},indent=2,default=str))
