"""Prescribed interior-pi opposite-pocket event: exact room/segment control."""
from pathlib import Path
from fractions import Fraction as F
import importlib.util,json
base=Path(__file__).resolve().parent
ring=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
def fan(a,start,count):
 return [tuple(sorted((a,(a[0]+ring[j%8][0],a[1]+ring[j%8][1]),(a[0]+ring[(j+1)%8][0],a[1]+ring[(j+1)%8][1])))) for j in range(start,start+count)]
room=[]
for args in [((0,0),0,8),((4,0),0,8),((2,0),0,4),((2,2),5,1),
 ((6,0),4,2),((4,-2),1,1),((4,2),4,2),((-2,0),7,1),((0,2),5,1),((0,-2),1,1)]:room+=fan(*args)
def load(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
geom=load('frozen_geometry',base.parent/'k5-proof-pilot/inputs/illumination_geometry.py')
receipt=geom.check({'triangles':room,'marked':[(0,0),(4,0)],'require_simple':True},strict=True)
assert receipt['walls']==26 and receipt['tiles']==29 and receipt['sectors']['(5, -1)']==[5]
a=load('fixed_guard_checker',base.parent/'persisted-replay/audit.py')
def p(x,y):return(F(x),F(y))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def mul(k,a):return tuple(k*x for x in a)
def ref(a,n,c):return sub(a,mul(2*(dot(n,a)-c)/dot(n,n),n))
def V(x):return(p(1,0),F(x))
def H(y):return(p(0,1),F(y))
S=p(0,0);T=p(4,0);B=p(5,-1);w=p(7,3);u=p(1,0)
first=[S,p(F(7,3),1),p(6,F(-4,7)),B];prefix=[H(1),V(6)]
second=[B,p(4,F(-10,7)),p(F(22,5),F(-8,5)),p(3,F(5,3)),p(F(22,7),2),T]
post=[V(4),(p(1,-1),F(6)),V(3),H(2)]
v=w
for pts,mirrors,times in [(first,prefix,[F(1,3),F(11,21),F(1,7)]),
 (second,post,[F(1,7),F(2,35),F(7,15),F(1,21),F(2,7)])]:
 assert sum(times)==1
 for i,t in enumerate(times):
  assert sub(pts[i+1],pts[i])==mul(t,v)
  if i<len(mirrors):
   n,c=mirrors[i];assert dot(n,pts[i+1])==c;v=ref(v,n,F(0))
 # Midpoint continuation is straight: do NOT reflect v here.
R=frozenset(room);path=first+second[1:]
for x,y in zip(path,path[1:]):assert a.segment(x,y)<=R
for pts in [first,second]:
 for x,y,z in zip(pts,pts[1:],pts[2:]):
  used,absent=a.bounce(x,y,z);assert used<=R and not absent&R
assert a.incident(S)<=R and a.incident(T)<=R
# Purely affine development for the transported path class; ordinary moving
# mirrors are post[0] and post[1], no corner mirror is inserted.
def images(t):
 moved_post=[V(F(4)+t),(p(1,-1),F(6)+t),post[2],post[3]]
 image=T
 for n,c in reversed(prefix+moved_post):image=ref(image,n,c)
 corner=p(F(5)+t,-1)
 for n,c in reversed(prefix):corner=ref(corner,n,c)
 return image,corner
image,corner=images(F(0));assert image==p(14,6) and corner==p(7,3)
assert sub(corner,S)==sub(image,corner)==w
eps=F(1,100);im1,c1=images(eps)
target_velocity=mul(1/eps,sub(im1,image));corner_velocity=mul(1/eps,sub(c1,corner))
assert target_velocity==p(-1,1) and corner_velocity==p(-1,0)
Q=sub(target_velocity,mul(2,corner_velocity));assert Q==p(1,1)
assert w[0]*Q[1]-w[1]*Q[0]==4
# Prescribed upper portal coordinates and fixed right-cap entry.
assert sub(p(F(23,7),1),second[2])==mul(F(13,35),p(-3,7))
assert sub(p(F(25,7),1),second[4])==mul(F(1,7),p(3,-7))
assert sub(p(5,F(-1,7)),first[1])==mul(F(8,21),p(7,-3))
out=dict(status='PRESCRIBED_SQUARE_CAP_OPPOSITE_EVENT_PASS',geometry=receipt,prescribed_triangles=room,
 first_half=first,second_half=second,developed_actual_target=image,developed_corner=corner,
 target_velocity=target_velocity,corner_velocity=corner_velocity,defect=Q,determinant=4,
 scope='Connected-H opposite pocket with Nleft AND upperTleftm2; nonempty rawW26 fixture.',
 independent_review='ACCEPTED_SCOPED_HAND_PROOF',universal_goal='OPEN',discovery_runs=0)
(base/'pocket-opposite-square.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['geometry','prescribed_triangles']},indent=2,default=str))
