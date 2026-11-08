"""One analytic replacement prefix plus supplied fixed R3/N7 tail; no search."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
sys.path.insert(0,str(ROOT/'triangle-composition/inputs'))
from guard_checker import path_requirements,incident,segment,bounce
from boundary_replay import on,sub,cross,dot
R=((1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1))
C={'L':(-2,0),'B':(0,-2),'D':(2,-2),'R':(4,0),'E':(4,2),'Tc':(2,4),'N':(0,2)}
def fan(k,ss):
 a=C[k] if isinstance(k,str) else k
 return {tuple(sorted((a,tuple(a[j]+R[i%8][j] for j in (0,1)),tuple(a[j]+R[(i+1)%8][j] for j in (0,1))))) for i in ss}
def full(k):return fan(k,range(8))
H=set().union(*(full(p) for p in ((0,0),(2,0),(2,2))))
P=[(F(0),F(0)),(F(1,4),F(1)),(F(4,5),F(-6,5)),(F(-4,3),F(-2,3)),(F(-8,5),F(2,5)),(F(3),F(-3,4)),(F(-1),F(-7,4)),(F(0),F(-2)),(F(-3,4),F(1)),(F(-6,5),F(-4,5)),(F(18,5),F(2,5)),(F(7,2),F(0)),(F(10,3),F(2,3)),(F(2,3),F(4,3)),(F(1,2),F(2)),(F(2,5),F(8,5)),(F(2),F(2))]
walls=[((0,1),(1,1)),((0,-2),(1,-1)),((-2,0),(-1,-1)),((-2,0),(-1,1)),((3,-1),(3,0)),((-1,-2),(-1,-1)),((-1,-3),(1,-1)),((-1,1),(0,1)),((-2,0),(-1,-1)),((3,1),(4,0)),((3,0),(4,0)),((3,1),(4,0)),((0,2),(1,1)),((0,2),(1,2)),((0,2),(1,1))]
minimum=H|fan('B',(1,2,3,4))|fan('L',(7,0))|fan('R',(3,))|fan('N',(7,))
maximum=minimum|full('D')|full('E')|full('Tc')
needed=set();forbidden=set();leg_need={};bounce_forbid={}
for i,(a,b) in enumerate(zip(P,P[1:])):
 leg_need[i]=set(segment(a,b));needed.update(leg_need[i])
for i,(a,p,b) in enumerate(zip(P,P[1:],P[2:]),1):
 u,z=bounce(a,p,b);needed.update(u);forbidden.update(z);bounce_forbid[i]=set(z)
overlap=needed&forbidden
assert overlap and fan('B',(0,))&overlap
assert on((2,-1),P[5],P[6])
def local_angle(ts,p):
 total=0
 for t in ts:
  if p in t:
   a,b=[sub(v,p) for v in t if v!=p];total+=90 if dot(a,b)==0 else 45
 return total
for cap in (1,2):assert local_angle(H|fan('D',(cap,)),(2,-1))==270
rejection={'status':'REJECTED_WEST_N7_PREFIX_CANDIDATE','path':[[str(x) for x in p] for p in P],'reason':'Requires B0 on an open leg and forbids it at a diagonal mirror; earlier true corner(2,-1).','contradictory_triangles':sorted(overlap),'required_on_legs':{str(i):sorted(ts&overlap) for i,ts in leg_need.items() if ts&overlap},'forbidden_at_bounces':{str(i):sorted(ts&overlap) for i,ts in bounce_forbid.items() if ts&overlap},'earlier_decisive_corner':{'point':[2,-1],'segment_index':5,'angle_either_ordinary_Dcap':270},'limits':'One rejected prescribed path, NO legal actualST or whole-envelope result. No room/discovery. WestTc6R3N7D1or2 remains open.','checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(HERE/'N7-prefix-check.json').write_text(json.dumps(rejection,indent=2)+'\n')
print('REJECTED: true270 corner(2,-1) for eitherDcap, contradictory B0 requirements; no path/closure.')
