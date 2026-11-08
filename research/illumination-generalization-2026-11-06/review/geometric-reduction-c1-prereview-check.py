"""One hand-constructed r3 spiral availability control, no enumeration/search."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
R=Path(__file__).resolve().parent
P=[(2,2),(2,10),(10,10),(10,4),(6,4),(6,0),(14,0),(14,14),(0,14),(0,2)]
S=(2,12);T=(12,2)
def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def on(p,a,b):return cross(a,b,p)==0 and all(min(a[k],b[k])<=p[k]<=max(a[k],b[k]) for k in (0,1))
def intersect(a,b,c,d):
 return any(on(p,x,y) for p,x,y in [(a,c,d),(b,c,d),(c,a,b),(d,a,b)]) or (cross(a,b,c)*cross(a,b,d)<0 and cross(c,d,a)*cross(c,d,b)<0)
def edges(p):return list(zip(p,p[1:]+p[:1]))
def inside(p):
 assert not any(on(p,a,b) for a,b in edges(P))
 x,y=p;count=0
 for a,b in edges(P):
  if (a[1]>y)!=(b[1]>y):
   xx=F(a[0])+F(y-a[1],b[1]-a[1])*(b[0]-a[0])
   count+=xx>x
 return bool(count%2)
for i,(a,b) in enumerate(edges(P)):
 assert a!=b and (a[0]==b[0] or a[1]==b[1])
 for j,(c,d) in enumerate(edges(P)):
  if j<=i or j in ((i+1)%len(P),(i-1)%len(P)):continue
  assert not intersect(a,b,c,d),(i,j)
a2=sum(a[0]*b[1]-a[1]*b[0] for a,b in edges(P));assert a2>0
turns=[cross(P[i-1],P[i],P[(i+1)%len(P)]) for i in range(len(P))]
assert all(turns)
kinds=['reflex' if a<0 else 'convex' for a in turns]
assert kinds==['convex','reflex','reflex','reflex','convex','convex','convex','convex','convex','convex']
assert all(not (kinds[i]=='reflex' and kinds[i-1]==kinds[(i+1)%10]=='convex') for i in range(10))
assert inside(S) and inside(T) and all(x%2==y%2==0 for x,y in P+[S,T])
source=R.parent/'construction/geometric-reduction-candidate-01.md'
out={'status':'PASS_PRESCRIBED_C1_AVAILABILITY_CONTROL','polygon':P,'S':S,'T':T,'strictly_simple':True,'canonical_orthogonal_lattice_disk':True,'walls':10,'reflex':3,'area':str(F(a2,2)),'turn_kinds':kinds,'convex_reflex_convex_subchains':0,'C1_geometric_move_available':False,'source_candidate_sha256_snapshot':hashlib.sha256(source.read_bytes()).hexdigest(),'source_is_frozen_review_packet':False,'optical_verdict':'NOT CLAIMED: this is availability failure only, not darkness or existential transfer rejection.','new_discovery_or_search':False,'whole_goal_complete':False}
(R/'geometric-reduction-c1-prereview-check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
