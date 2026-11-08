"""Independent fixed B-unit six certificate check. No discovery or room assembly."""
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
P=[S,(F(-2,7),F(-12,7)),(F(2,5),F(-8,5)),(F(5,6),F(1)),(F(6,5),F(-6,5)),(F(2),F(-4,3)),(F(10,7),F(-10,7)),T]
W=[((-1,-1),(0,-2)),((0,-2),(1,-1)),((0,1),(1,1)),((1,-1),(2,-2)),((2,-2),(2,-1)),((1,-1),(2,-2))]
minimum=H|fan('B',[1,2])|fan('D',[2])
maximum=minimum|set().union(*(fan(k,range(8)) for k in ['L','E','Tc','R']))|fan('N',[0,1,2,3,4,5,7])
result,U,Z=verify(P,W,minimum,maximum,(-2,-12))
d=F(1,6)
assert F(1,7)<d<F(1,5) and 12*d==2
Bentry=(-d,F(-1));Bexit=(3*d,F(-1));ceiling=(5*d,F(1))
Ba=(-2*d/(1+d),-2+2*d/(1+d))
Bb=(2*d/(1-d),-2+2*d/(1-d))
Dentry=(7*d,F(-1));Dexit=(9*d,F(-1))
Da=(6*d/(1-d),-6*d/(1-d));Db=(F(2),-8*d);Dc=(10*d/(1+d),-10*d/(1+d))
assert [Ba,Bb,ceiling,Da,Db,Dc]==P[1:-1]
assert 0<d<F(1,3) and 0<5*d<1 and 1<7*d<2 and 1<9*d<2
for a,b,v in [(S,Bentry,(-d,-1)),(Bentry,Ba,(-d,-1)),(Ba,Bb,(1,d)),(Bb,Bexit,(d,1)),(Bexit,ceiling,(d,1)),(ceiling,Dentry,(d,-1)),(Dentry,Da,(d,-1)),(Da,Db,(1,-d)),(Db,Dc,(-1,-d)),(Dc,Dexit,(d,1)),(Dexit,T,(d,1))]:
 change=sub(b,a);assert cross(change,v)==0 and dot(change,v)>0
# These are support-envelope inclusions, not completed room constructions.
# Both inward descriptions contain H+B12+D2. All additional support is
# L670, E4, Tc5, N5 and one of R3/R4, hence lies inside this maximum.
for k,sectors in [('L',[6,7,0]),('E',[4]),('Tc',[5]),('N',[5]),('R',[3,4])]:
 assert fan(k,sectors)<=maximum and not Z&fan(k,sectors)
assert Z&fan('N',[6])==fan('N',[6])
assert Z&fan('B',[0]) and Z&fan('B',[3])
assert Z&fan('D',[1]) and Z&fan('D',[3])
inputs=[ROOT/'surplus-four-local/e2-e1-b1/critical-L-continuation.txt',ROOT/'surplus-four-local/e2-e1-b1/critical-L.txt',ROOT/'triangle-composition/inputs/guard_checker.py',Path(__file__)]
out={'status':'INDEPENDENT_B_UNIT_SIX_AND_TWO_CONDITIONAL_INWARD_COVERS_PASS','fixed_six':result,
 'hand_parameter':{'d':'1/6','combined_strict_gate':'1/7<d<1/5','actual_endpoint':'12d=2','B_entry':list(map(str,Bentry)),'B_exit':list(map(str,Bexit)),'D_entry':list(map(str,Dentry)),'D_exit':list(map(str,Dexit))},
 'two_conditional_case_inclusions':'L670+B12+E4+Tc5+N5+D2 with either ordinary R3 or R4: same whole-envelope implication',
 'negative_controls':'N6, B0/B3, D1/D3 each violates a required mirror',
 'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},
 'limits':'Independent hand algebra and fixed-path verification; historically shared guard helper and reused own local verification functions. No peer checker execution, completed-room generation, ray/direction/word discovery, solver, archive or worker. Does not independently prove original thirteen-case classification or eleven-case remainder completeness.'}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: fixed B-unit six; strict B/D ports; actual target/unfold(-2,-12); reverse/sigma/full support; both conditional inward descriptions covered.')
