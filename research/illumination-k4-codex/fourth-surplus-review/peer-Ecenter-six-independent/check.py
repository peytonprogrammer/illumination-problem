"""Independent centered-E sigma-transfer check. No discovery or room assembly."""
from pathlib import Path
from fractions import Fraction as F
import sys, json, hashlib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
sys.path.insert(0,str(ROOT/'triangle-composition/inputs'))
from guard_checker import path_requirements
RAYS=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
CENTERS={'L':(-2,0),'B':(0,-2),'D':(2,-2),'R':(4,0),'E':(4,2),'Tc':(2,4),'N':(0,2)}
def tri(t):return tuple(sorted(map(tuple,t)))
def star(a, sectors):
 return {tri((a,(a[0]+RAYS[i%8][0],a[1]+RAYS[i%8][1]),(a[0]+RAYS[(i+1)%8][0],a[1]+RAYS[(i+1)%8][1]))) for i in sectors}
def fan(k,sectors):return star(CENTERS[k],sectors)
H=set().union(*(star(a,range(8)) for a in [(0,0),(2,0),(2,2)]))
sub=lambda a,b:(a[0]-b[0],a[1]-b[1])
dot=lambda a,b:a[0]*b[0]+a[1]*b[1]
cross=lambda a,b:a[0]*b[1]-a[1]*b[0]
sigma=lambda p:(2-p[1],2-p[0])
def transform(ts):return {tri(sigma(p) for p in t) for t in ts}
def reflect(v,a,b):
 e=sub(b,a)
 return tuple(2*F(dot(v,e),dot(e,e))*e[k]-v[k] for k in (0,1))
def on(p,a,b):return cross(sub(p,a),sub(b,a))==0 and dot(sub(p,a),sub(p,b))<=0

def local(path, mirrors):
 assert len(path)==len(mirrors)+2
 assert path[0]!=path[-1]
 for i,(a,b) in enumerate(mirrors,1):
  assert on(path[i],a,b) and path[i] not in (a,b)
  want=reflect(sub(path[i],path[i-1]),a,b)
  out=sub(path[i+1],path[i])
  assert cross(want,out)==0 and dot(want,out)>0
 for i,(a,b) in enumerate(zip(path,path[1:])):
  assert a!=b
  if i<len(path)-2:assert not on(path[-1],a,b)

def verify(path,mirrors,minimum,maximum,expected_unfold):
 local(path,mirrors)
 local(path[::-1],mirrors[::-1])
 sp=[sigma(p) for p in path[::-1]]
 sw=[(sigma(a),sigma(b)) for a,b in mirrors[::-1]]
 local(sp,sw)
 U,Z=path_requirements(path)
 assert U<=minimum and not Z&maximum
 Us,Zs=path_requirements(sp)
 assert Us==transform(U) and Zs==transform(Z)
 Ur,Zr=path_requirements(path[::-1]);assert Ur==U and Zr==Z
 q=path[-1]
 for a,b in mirrors[::-1]:
  v=reflect(sub(q,a),a,b);q=tuple(a[k]+v[k] for k in (0,1))
 assert q==expected_unfold
 launch=sub(path[1],path[0]);delta=sub(q,path[0])
 assert cross(launch,delta)==0 and dot(launch,delta)>0
 return {'path':[[str(x) for x in p] for p in path], 'finite_mirrors':mirrors,
         'required':sorted(U),'forbidden':sorted(Z),'minimum':sorted(minimum),
         'maximum':sorted(maximum),'unfolded_actual_target':list(map(str,q)),
         'strict_specular_contacts_first_target_reverse_sigma_and_whole_support':'PASS'},U,Z

S=(F(0),F(0));T=(F(2),F(2))
P=[S,(F(24,7),F(4,7)),(F(10,3),F(0)),(F(16,5),F(4,5)),(F(1),F(7,6)),(F(18,5),F(8,5)),(F(26,7),F(16,7)),T]
W=[((3,1),(4,0)),((3,0),(4,0)),((3,1),(4,0)),((1,1),(1,2)),((3,1),(4,2)),((3,3),(4,2))]
minimum=H|fan('E',[3,4])|fan('R',[3])
maximum=minimum|set().union(*(fan(k,range(8)) for k in ['L','B','Tc','D']))|fan('N',[0,1,2,3,4,5,6])
result,U,Z=verify(P,W,minimum,maximum,(12,2))
source=HERE.parent/'peer-Bunit-six-independent/check.json'
old=json.loads(source.read_text())['fixed_six']
oldP=[tuple(map(F,p)) for p in old['path']]
assert P==[sigma(p) for p in oldP[::-1]]
for key,new in [('minimum',minimum),('maximum',maximum),('required',U),('forbidden',Z)]:
 assert new==transform({tri(t) for t in old[key]}),key
assert Z==fan('R',[2,4])|fan('E',[2,5])|fan('N',[7])
# Independent direct intersections and portal states, not peer helper execution.
d=F(1,6);assert F(1,7)<d<F(1,5) and 4-12*d==2
Ra=(4/(1+d),4-4/(1+d));Rb=(4-4*d,F(0));Rc=((4-8*d)/(1-d),4-(4-8*d)/(1-d))
left=(F(1),7*d)
c=(2+6*d)/(1-d);Ea=(c,c-2)
e=(2+14*d)/(1+d);Eb=(e,6-e)
assert [Ra,Rb,Rc,left,Ea,Eb]==P[1:-1]
Rentry=(F(3),3*d);Rexit=(F(3),5*d)
Eentry=(F(3),9*d);Eexit=(F(3),4-11*d)
assert 0<3*d<1 and 0<5*d<1 and 1<7*d<2
assert 1<9*d<3 and 1<4-11*d<3
for a,b,v in [(S,Rentry,(1,d)),(Rentry,Ra,(1,d)),(Ra,Rb,(-d,-1)),(Rb,Rc,(-d,1)),(Rc,Rexit,(-1,d)),(Rexit,left,(-1,d)),(left,Eentry,(1,d)),(Eentry,Ea,(1,d)),(Ea,Eb,(d,1)),(Eb,Eexit,(-1,-d)),(Eexit,T,(-1,-d))]:
 change=sub(b,a);assert cross(change,v)==0 and dot(change,v)>0
# Six SYMBOLIC support inclusions. No completed-room geometries generated.
common=[('B',[1]),('Tc',[5])]
rows=[('outside_L012',[('L',[0,1,2]),('N',[5])]),
      ('outside_L0123',[('L',[0,1,2,3]),('N',[5])]),
      ('outside_L7012_Dminus',[('L',[7,0,1,2]),('N',[5]),('D',[2])]),
      ('outside_L7012_Dplus',[('L',[7,0,1,2]),('N',[5]),('D',[1])]),
      ('inward_L6701',[('L',[6,7,0,1]),('N',[5]),('D',[2])]),
      ('inward_L701',[('L',[7,0,1]),('N',[6]),('D',[2])])]
checked=[]
for name,additions in rows:
 for k,sectors in common+additions:
  tiles=fan(k,sectors)
  assert tiles<=maximum and not tiles&Z,(name,k)
 checked.append(name)
# Every identified mirror blocker independently violates the absence guard.
for k,sectors in [('R',[2]),('R',[4]),('E',[2]),('E',[5]),('N',[7])]:
 assert fan(k,sectors)<=Z
inputs=[source,ROOT/'surplus-four-local/e2-e1-b1/centered-E-outside-C.txt',ROOT/'triangle-composition/inputs/guard_checker.py',Path(__file__)]
out={'status':'INDEPENDENT_ECENTER_SIX_SIGMA_TRANSFER_AND_SIX_INCLUSIONS_PASS','fixed_six':result,
     'sigma_transfer':'exact path with time reversal, complete required/forbidden/minimum/maximum equality',
     'symbolic_case_inclusions':checked,'parameter':'1/6, actual target 4-12d=2, strict 1/7<d<1/5',
     'negative_controls':'each of R2,R4,E2,E5,N7 independently removes a necessary mirror',
     'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},
     'scope':'Optical implication and six conditional applications only; no global classification/completeness or whole surplus-four theorem. Shared historically derived guard helper, own reused local verification functions. No peer checker execution, room/cap enumeration, ray/direction/word discovery, archive, solver or worker.'}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: exact sigma/time reversal and complete support transfer; direct fixed6 strict mirrors/firstT/reverse/unfold(12,2); all six symbolic case inclusions.')
