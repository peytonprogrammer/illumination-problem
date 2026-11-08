"""Independent fixed-candidate path/room validation; no discovery scans."""
from pathlib import Path
from fractions import Fraction as F
import importlib.util,json
base=Path(__file__).resolve().parent
ring=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
def fan(a,start,count):
 return [tuple(sorted((a,(a[0]+ring[j%8][0],a[1]+ring[j%8][1]),(a[0]+ring[(j+1)%8][0],a[1]+ring[(j+1)%8][1])))) for j in range(start,start+count)]
room=[]
for args in [((0,0),0,8),((4,0),0,8),((2,0),0,4),((2,2),6,1),
             ((6,0),3,1),((4,2),6,2),((4,-2),2,1),((-2,0),7,1),
             ((0,2),6,1),((0,-2),1,1)]:room+=fan(*args)
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
S=p(0,0);T=p(4,0);C=p(5,0);w=p(-7,2);u=p(0,1)
first=[S,p(-1,F(2,7)),p(F(3,2),1),C]
first_mirrors=[V(-1),H(1)];first_times=[F(1,7),F(5,14),F(1,2)]
second=[C,p(3,F(-4,7)),p(F(9,2),-1),p(5,F(-6,7)),p(3,F(-2,7)),T]
second_mirrors=[V(3),H(-1),V(5),V(3)];second_times=[F(2,7),F(3,14),F(1,14),F(2,7),F(1,7)]
v=w
for pts,mirrors,times in [(first,first_mirrors,first_times),(second,second_mirrors,second_times)]:
 assert sum(times)==1
 for i,t in enumerate(times):
  assert sub(pts[i+1],pts[i])==mul(t,v)
  if i<len(mirrors):
   n,c=mirrors[i];assert dot(n,pts[i+1])==c;v=ref(v,n,F(0))
 if pts is first:v=ref(v,V(5)[0],F(0))
R=frozenset(room);path=first+second[1:]
for x,y in zip(path,path[1:]):assert a.segment(x,y)<=R
for pts in [first,second]:
 for x,y,z in zip(pts,pts[1:],pts[2:]):
  used,absent=a.bounce(x,y,z);assert used<=R and not absent&R
assert a.incident(S)<=R and a.incident(T)<=R
image=T
for n,c in reversed(first_mirrors+[V(5)]+second_mirrors):image=ref(image,n,c)
corner=C
for n,c in reversed(first_mirrors):corner=ref(corner,n,c)
assert image==p(-14,4) and corner==w and sub(image,corner)==w
velocity=u
for n,c in reversed(first_mirrors):velocity=ref(velocity,n,F(0))
Q=mul(-2,velocity);assert Q==p(0,2)
assert w[0]*Q[1]-w[1]*Q[0]==-14
# One analytically prescribed negative control for the review's extra
# S-left-m1 assertion. It is not an orientation or room search.
room2=set(room)-set(fan((-2,0),7,1))-set(fan((0,-2),1,1))
room2.update(fan((-2,0),6,2));room2.update(fan((0,-2),2,1))
size_countercontrol=geom.check({'triangles':sorted(room2),'marked':[(0,0),(4,0)],'require_simple':True},strict=True)
assert size_countercontrol['walls']==26 and size_countercontrol['sectors']['(-1, -1)']==[5]
for x,y in zip(path,path[1:]):assert a.segment(x,y)<=room2
out=dict(status='PRESCRIBED_FIXED_FLANK_END_EVENT_PASS',geometry=receipt,
 prescribed_triangles=room,Sleft_size_countercontrol=size_countercontrol,first_half=first,second_half=second,
 developed_actual_target=image,developed_corner=corner,defect=Q,determinant=-14,
 scope='Upper end leaf with opposite LEFT portal and S-left LOWER portal only.',
 independent_review='ACCEPTED_SCOPED_PI_AND_FLANKS_HAND_VERIFIED',universal_goal='OPEN',discovery_runs=0)
(base/'pocket-end-fixed.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['geometry','prescribed_triangles']},indent=2,default=str))
