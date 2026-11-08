"""Independent fixed centered-N certificate check. No discovery or room assembly."""
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
P=[S,(F(-2,5),F(8,5)),(F(2,3),F(4,3)),(F(5,4),F(-1)),T]
W=[((-1,1),(0,2)),((0,2),(1,1)),((1,-1),(2,-1))]
minimum=H|fan('N',[5,6])
maximum=minimum|set().union(*(fan(k,range(8)) for k in ['L','B','E','Tc','R']))|fan('D',[0,1,3,4,5,6,7])
three,U3,Z3=verify(P,W,minimum,maximum,(-2,8))
d=F(1,4)
assert 0<d<F(1,3) and 1<5*d<2 and 8*d==2
entry=(-d,F(1));exit=(3*d,F(1));floor=(5*d,F(-1))
a=(-2*d/(1+d),2-2*d/(1+d))
b=(2*d/(1-d),2-2*d/(1-d))
assert [a,b,floor]==P[1:-1]
for start,end,v in [(S,entry,(-d,1)),(entry,a,(-d,1)),(a,b,(1,-d)),(b,exit,(d,-1)),(exit,floor,(d,-1)),(floor,T,(d,1))]:
 change=sub(end,start);assert cross(change,v)==0 and dot(change,v)>0
assert Z3&fan('D',[2])==fan('D',[2])
# Independently recheck the accepted six-path complement. Its D fan is
# ordinary sector2 ONLY; the three-path maximum must not be reused here.
P6=[S,(F(-1,6),F(-1)),(F(-4,7),F(10,7)),(F(4,5),F(6,5)),(F(6,5),F(-6,5)),(F(2),F(-4,3)),(F(10,7),F(-10,7)),T]
W6=[((-1,-1),(0,-1)),((-1,1),(0,2)),((0,2),(1,1)),((1,-1),(2,-2)),((2,-2),(2,-1)),((1,-1),(2,-2))]
min6=minimum|fan('D',[2])
max6=min6|fan('B',[1])|set().union(*(fan(k,range(8)) for k in ['L','E','Tc','R']))
six,U6,Z6=verify(P6,W6,min6,max6,(-2,-12))
assert Z6&fan('B',[2])==fan('B',[2])
# Exact cap-set exhaustion, no room geometries or cap assignments generated:
# an ordinary D cell has states empty, {1}, or {2}.
ordinary_D=[set(),fan('D',[1]),fan('D',[2])]
assert all((not state&fan('D',[2]) and state<=fan('D',[0,1,3,4,5,6,7])) or state==fan('D',[2]) for state in ordinary_D)
# Negative controls guard the complement's explicit restrictions.
assert Z6&fan('D',[1])
assert Z3&fan('N',[4]) and Z3&fan('N',[7])
inputs=[ROOT/'surplus-four-local/e2-e1-b1/critical-L-continuation.txt', ROOT/'surplus-four-local/e2-e1-b1/critical-L.txt',ROOT/'triangle-composition/inputs/guard_checker.py',Path(__file__)]
out={'status':'INDEPENDENT_CENTERED_N_THREE_AND_ORDINARY_D_COMPLEMENT_PASS','three':three,'accepted_six_rechecked':six,
     'hand_parameter':{'d':'1/4','roof_strict':'0<d<1/3','floor_strict':'1<5d<2','actual_endpoint':'8d=2'},
     'ordinary_D_partition':'empty or D1: three; D2 only: six; ordinary B1 assumed, or inherited one-bounce if B1 absent',
     'negative_controls':'D2 spoils three; B2 or D1 spoils six; N4/N7 spoils three',
     'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},
     'scope':'Only continuation sections1–3 conditional optical cover. No independent global seven-L classification, count tables, B-unit-six result, or full surplus-four theorem. Shared historically derived guard helper; not formal verification.'}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: three fixed finite reflections; first actual target; reverse/sigma; whole-support guard; unfolding(-2,8); ordinary-D complement with accepted six.')
