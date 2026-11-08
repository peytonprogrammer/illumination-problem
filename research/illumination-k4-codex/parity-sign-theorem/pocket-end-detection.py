"""One hand-prescribed moving-diagonal actual event, no discovery scan."""
from pathlib import Path
from fractions import Fraction as F
from math import gcd
import importlib.util,json
base=Path(__file__).resolve().parent
def p(x,y):return (F(x),F(y))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def mul(k,a):return tuple(k*x for x in a)
def ref(a,n,c):return sub(a,mul(2*(dot(n,a)-c)/dot(n,n),n))
def det(a,b):return a[0]*b[1]-a[1]*b[0]
S=p(0,0);T=p(4,0);B=p(5,1);w=p(5,1);u=p(0,1)
path=[S,B,p(F(9,2),F(-3,2)),p(4,F(-8,5)),p(F(13,3),F(-5,3)),T]
fixed_D=(p(1,-1),F(6));fixed_V=(p(1,0),F(4));corner_D=(p(1,1),F(6))
mirrors=[fixed_D,fixed_V,fixed_D];times=[F(1,2),F(1,10),F(1,15),F(1,3)]
assert sub(B,S)==w and gcd(5,1)==1 and sum(times)==1
v=ref(w,corner_D[0],F(0));assert v==p(-1,-5)
for i,t in enumerate(times):
 assert sub(path[i+2],path[i+1])==mul(t,v)
 if i<len(mirrors):
  n,c=mirrors[i];hit=path[i+2];assert dot(n,hit)==c
  assert 4<=hit[0]<5 and -2<hit[1]<-1
  v=ref(v,n,F(0))
# The supplied complete raw room makes this conditional geometry nonvacuous.
control=json.loads((base/'pocket-diagonal-load.json').read_text())
room=frozenset(tuple(sorted((x+4,y) for x,y in tri)) for tri in control['room']['triangles'])
sp=importlib.util.spec_from_file_location('saved_exact_checker',base.parent/'persisted-replay/audit.py')
a=importlib.util.module_from_spec(sp);sp.loader.exec_module(a)
segment_receipts=[]
for x,y in zip(path,path[1:]):
 need=a.segment(x,y);assert need<=room
 segment_receipts.append(len(need))
for prev,hit,nxt in zip(path[1:],path[2:],path[3:]):
 need,forbid=a.bounce(prev,hit,nxt);assert need<=room and not forbid&room
assert a.incident(S)<=room and a.incident(T)<=room
# Verify the actual target's fixed-cap development and moving-flank derivative.
image=T
for n,c in reversed(mirrors):image=ref(image,n,c)
assert image==p(4,-4)
assert ref(image,*corner_D)==p(10,2)
assert sub(ref(image,*corner_D),B)==w
for t in [F(-1,100),F(0),F(1,100)]:
 moved=ref(image,corner_D[0],F(6)+t)
 assert moved==p(10+t,2+t)
# Those three values are controls for a stated affine formula, not trajectories.
eps=F(1,100)
target_derivative=mul(1/eps,sub(ref(image,corner_D[0],F(6)+eps),ref(image,*corner_D)))
assert target_derivative==p(1,1)
Q=sub(target_derivative,mul(2,u));assert Q==p(1,-1) and det(w,Q)==-6
# Portal crossings are prescribed, not reflection events.
assert sub(p(F(23,5),-1),B)==mul(F(2,5),p(-1,-5))
assert sub(p(F(21,5),-1),path[-2])==mul(F(2,15),p(-1,5))
out=dict(status='PRESCRIBED_MOVING_DIAGONAL_END_EVENT_PASS',actual_source=S,actual_target=T,
 physical_path=path,half_vector=w,opening_defect=Q,determinant=-6,
 segment_tile_counts=segment_receipts,ordinary_reflections=3,
 source_room='Section33 fixed analytic25wall room shifted by(4,0)',
 scope='Connected-H upper end pocket AND opposite lower RIGHT portal only; intrinsic-pi needs hand review.',
 independent_review='ACCEPTED_SCOPED_WITH_MOVING_FLANK_TERM',universal_detection='OPEN',discovery_runs=0)
(base/'pocket-end-detection.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps(out,indent=2,default=str))
