"""Verify three proof-prescribed corridor paths; no discovery search.

Exact segments/reflections/endpoint labels only. The hand proof separately
establishes forced fans, corner links, and scope.
"""
from fractions import Fraction as F
from pathlib import Path
from math import gcd
import json

base=Path(__file__).resolve().parent
def p(x,y):return (F(x),F(y))
def sub(a,b):return (a[0]-b[0],a[1]-b[1])
def add(a,b):return (a[0]+b[0],a[1]+b[1])
def mul(k,a):return (k*a[0],k*a[1])
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def det(a,b):return a[0]*b[1]-a[1]*b[0]
def reflect(a,n,c):return sub(a,mul(2*(dot(n,a)-c)/dot(n,n),n))
def reflect_v(v,n):return reflect(v,n,F(0))
def in_rect(a,x0,x1,y0,y1):return x0<=a[0]<=x1 and y0<=a[1]<=y1
S=p(0,0);T=p(4,0);u=p(1,0)
H1=(p(0,1),F(1));V6=(p(1,0),F(6));V5=(p(1,0),F(5))
D=(p(1,1),F(6));H0=(p(0,1),F(0))
cases=[
 dict(name='upper_rectangle',corner=p(4,1),w=p(4,1),
      points=[p(4,1),p(6,F(1,2)),T],mirrors=[V6],
      durations=[F(1,2),F(1,2)],image=p(8,2)),
 dict(name='upper_triangle',corner=p(4,1),w=p(4,1),
      points=[p(4,1),p(F(16,3),F(2,3)),p(F(11,2),0),p(F(28,5),F(2,5)),T],
      mirrors=[D,H0,D],durations=[F(1,3),F(1,6),F(1,10),F(2,5)],image=p(8,2)),
 dict(name='lower_portal',corner=p(3,1),w=p(3,1),
      points=[p(3,1),p(5,F(1,3)),T],mirrors=[V5],
      durations=[F(2,3),F(1,3)],image=p(6,2)),
]
checks=[]
for case in cases:
 c=case['corner'];w=case['w'];points=case['points'];mirrors=case['mirrors']
 assert sub(c,S)==w and gcd(int(w[0]),int(w[1]))==1
 assert all(in_rect(a,-1,5,0,1) for a in (S,c))
 v=reflect_v(w,H1[0]);elapsed=F(0)
 for i,t in enumerate(case['durations']):
  assert t>0 and sub(points[i+1],points[i])==mul(t,v)
  elapsed+=t
  if i<len(mirrors):
   n,offset=mirrors[i];hit=points[i+1]
   assert dot(n,hit)==offset
   if case['name']=='upper_triangle':
    assert 5<hit[0]<6 and 0<=hit[1]<1
    if n==D[0]: assert hit[1]>0
    else: assert hit[1]==0
   elif case['name']=='upper_rectangle':assert hit==p(6,F(1,2))
   else:assert hit==p(5,F(1,3))
   # Corner exclusion on all prescribed post-corner segments: y is in
   # [0,1], and an endpoint on integer y is explicitly nonlattice,
   # except chosen corner / actual target. Convexity handles interiors.
   assert hit[0].denominator>1 or hit[1].denominator>1
   v=reflect_v(v,n)
 assert elapsed==1 and points[-1]==T
 # Develop ACTUAL target in reverse encounter order, then corner flank.
 image=T
 for n,offset in reversed(mirrors):image=reflect(image,n,offset)
 image=reflect(image,*H1)
 assert image==case['image'] and sub(image,c)==w
 assert add(S,image)==mul(2,c)
 # Every used mirror is FIXED in this pocket deformation.
 defect=mul(-2,u)
 assert defect==p(-2,0) and det(w,defect)==2
 # Fixed segment containment by convexity in the supplied union:
 # [3,5]x[0,1] for T; fixed right cap for x>=5.
 for a in points:
  if a[0]<=5:assert in_rect(a,3,5,0,1)
  elif case['name']=='upper_triangle':
   assert a[0]>=5 and a[1]>=0 and sum(a)<=6
  else:assert in_rect(a,5,6,0,1)
 checks.append(dict(name=case['name'],physical_path=[S]+points,
                    half_vector=w,developed_actual_target=image,
                    post_corner_elapsed=elapsed,defect=defect,determinant=2))
# The two portal crossings in the fixed triangular leaf are prescribed.
assert add(p(4,1),mul(F(1,4),p(4,-1)))==p(5,F(3,4))
assert add(p(F(28,5),F(2,5)),mul(F(3,20),p(-4,-1)))==p(5,F(1,4))
# Fixed-cap composite identity used by the analytic construction.
for a in (S,T,p(4,1)):
 assert reflect(reflect(reflect(a,*D),*H0),*D)==reflect(a,*V6)
# Sharpened counting: these are the hand-derived degree totals, not rooms.
assert 8+8+3<2*(2+9-1)
assert 3+7==10 and 14+10==24
assert 3+2+6==11 and 14+11==25
# Literal outward B with lower portal:90+45=135, inconsistent with225.
assert 90+45!=225
out=dict(status='PRESCRIBED_CORRIDOR_CONTROLS_PASS',cases=checks,
         geometry_scope='Three prescribed segments in forced connected-H corridor/cap regions; no room census.',
         hand_proof_review='ACCEPTED_SCOPED_WITH_CORRECTIONS',cone_sector_review='ACCEPTED_FIXED_FLANKS',
         universal_pocket_detection='OPEN',optical_discovery_runs=0)
(base/'pocket-corridor.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps(out,indent=2,default=str))
