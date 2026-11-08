"""ONE fixed k2 control for a stated analytic all-k corridor theorem.
No k scan, ray/word/cylinder search or room enumeration.
"""
from pathlib import Path
from fractions import Fraction as F
import importlib.util,json
base=Path(__file__).resolve().parent
ring=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
def fan(a,start,count):
 return [tuple(sorted((a,(a[0]+ring[j%8][0],a[1]+ring[j%8][1]),(a[0]+ring[(j+1)%8][0],a[1]+ring[(j+1)%8][1])))) for j in range(start,start+count)]
# This single prescribed control k=2 checks nonvacuity beyond the W26 range.
k=2;D=4*k;M=D+1;room=[]
for j in range(k+1):
 room+=fan((4*j,0),0,8)
 room+=fan((4*j,-2),1,1)
 room+=fan((4*j,2),6,2 if j==k else 1)
for j in range(k):
 room+=fan((4*j+2,0),0,4);room+=fan((4*j+2,2),6,1)
room+=fan((-2,0),7,1);room+=fan((D+2,0),3,1)
def load(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
geom=load('frozen_geometry',base.parent/'k5-proof-pilot/inputs/illumination_geometry.py')
receipt=geom.check({'triangles':room,'marked':[(0,0),(D,0)],'require_simple':True},strict=True)
assert receipt['walls']==12*k+13==37 and receipt['tiles']==15*k+13==43
assert set(map(tuple,receipt['interior_A']))=={(0,0),(4,0),(8,0)}
assert receipt['sectors']['(9, 1)']==[5] and receipt['sectors']['(9, 0)']==[6]
a=load('fixed_guard_checker',base.parent/'persisted-replay/audit.py')
def p(x,y):return(F(x),F(y))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def mul(k,a):return tuple(k*x for x in a)
def ref(a,n,c):return sub(a,mul(2*(dot(n,a)-c)/dot(n,n),n))
S=p(0,0);T=p(8,0);B=p(9,1);w=p(9,1);u=p(0,1)
post=[B,p(F(35,4),F(-5,4)),p(8,F(-4,3)),p(F(43,5),F(-7,5)),p(F(74,9),2),T]
mirrors=[(p(1,-1),F(10)),(p(1,0),F(8)),(p(1,-1),F(10)),(p(0,1),F(2))]
times=[F(1,4),F(1,12),F(1,15),F(17,45),F(2,9)]
v=ref(w,p(1,1),F(0));assert v==p(-1,-9) and sum(times)==1
for i,t in enumerate(times):
 assert sub(post[i+1],post[i])==mul(t,v)
 if i<len(mirrors):
  n,c=mirrors[i];assert dot(n,post[i+1])==c;v=ref(v,n,F(0))
R=frozenset(room);path=[S]+post
for x,y in zip(path,path[1:]):assert a.segment(x,y)<=R
for x,y,z in zip(post,post[1:],post[2:]):
 used,absent=a.bounce(x,y,z);assert used<=R and not absent&R
assert a.incident(S)<=R and a.incident(T)<=R
image=T
for n,c in reversed(mirrors):image=ref(image,n,c)
assert image==p(D,-D)
base_target=ref(image,p(1,1),F(D+2));assert base_target==p(2*(D+1),2)
assert sub(base_target,B)==w
eps=F(1,100);target_velocity=mul(1/eps,sub(ref(image,p(1,1),F(D+2)+eps),base_target))
Q=sub(target_velocity,mul(2,u));assert Q==p(1,-1)
assert w[0]*Q[1]-w[1]*Q[0]==-(4*k+2)
# Fixed bottom-cap phase in this supplied event; the all-M lemma is hand-proved.
q=F(7,9);m=9
cap_times=[(1-q)/(m-1),(m*q-1)/(m*(m-1)),(q-F(1,m))/(m+1),(1-(m*q-1)/(m+1))/m]
assert q>F(2,m) and sum(cap_times)==F(2,m) and all(t>0 for t in cap_times)
assert q-F(2,m)==F(5,9)
out=dict(status='PRESCRIBED_K2_CORRIDOR_CONTROL_PASS',geometry=receipt,prescribed_triangles=room,
 fixed_k=k,first_half=[S,B],second_half=post,developed_actual_target=base_target,
 defect=Q,determinant=w[0]*Q[1]-w[1]*Q[0],cap_phase=q,cap_elapsed=sum(cap_times),
 all_k_proof='SCOPED_ALL_K_HAND_PROOF_ACCEPTED_NOT_ESTABLISHED_BY_THIS_FIXED_CONTROL',
 independent_review='ACCEPTED_SCOPED_WITH_CORRECTIONS_C1_C8',universal_pocket_detection='OPEN',discovery_runs=0)
(base/'pocket-corridor-chain.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({x:y for x,y in out.items() if x not in ['geometry','prescribed_triangles']},indent=2,default=str))
