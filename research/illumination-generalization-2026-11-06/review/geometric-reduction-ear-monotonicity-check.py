"""One prescribed ear removal from the accepted known22 room. Geometry only, no search.
Illumination/darkness are inherited from individually named accepted theorems.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
R=Path(__file__).resolve().parent;CTX=R.parents[1]
D=[(-1,-1),(0,-1),(0,-2),(1,-2),(1,-3),(2,-3),(2,-1),(1,-1),(1,1),(3,1),(3,0),(5,0),(5,1),(4,1),(4,2),(3,2),(3,3),(1,3),(1,2),(0,2),(0,1),(-1,1)]
Q=D[:11]+[(4,0)]+D[14:]
S=(0,0);T=(2,2)
def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def edges(p):return list(zip(p,p[1:]+p[:1]))
def on(p,a,b):return cross(a,b,p)==0 and all(min(a[k],b[k])<=p[k]<=max(a[k],b[k]) for k in (0,1))
def intersects(a,b,c,d):
 if any(on(p,x,y) for p,x,y in [(a,c,d),(b,c,d),(c,a,b),(d,a,b)]):return True
 return cross(a,b,c)*cross(a,b,d)<0 and cross(c,d,a)*cross(c,d,b)<0

def classify(p,xy):
 if any(on(xy,a,b) for a,b in edges(p)):return 'boundary'
 x,y=xy;count=0
 for a,b in edges(p):
  if (a[1]>y)!=(b[1]>y):
   xx=F(a[0])+F(y-a[1],b[1]-a[1])*(b[0]-a[0])
   if xx>x:count+=1
 return 'interior' if count%2 else 'outside'

def analyze(p):
 assert len(set(p))==len(p)
 assert all(a!=b and (a[0]==b[0] or a[1]==b[1]) for a,b in edges(p))
 assert all(cross(p[i-1],p[i],p[(i+1)%len(p)])!=0 for i in range(len(p)))
 for i,(a,b) in enumerate(edges(p)):
  for j,(c,d) in enumerate(edges(p)):
   if j<=i or j in ((i+1)%len(p),(i-1)%len(p)):continue
   assert not intersects(a,b,c,d),(i,j)
 a2=sum(a[0]*b[1]-a[1]*b[0] for a,b in edges(p));assert a2>0
 per=sum(abs(a[0]-b[0])+abs(a[1]-b[1]) for a,b in edges(p))
 reflex=sum(cross(p[i-1],p[i],p[(i+1)%len(p)])<0 for i in range(len(p)))
 points=[(x,y) for x in range(-1,6) for y in range(-3,4)]
 interior=[pt for pt in points if classify(p,pt)=='interior']
 smooth=[pt for pt in points if classify(p,pt)=='boundary' and pt not in p]
 assert len(interior)==F(a2,2)-F(per,2)+1
 assert len(smooth)==per-len(p)
 J=sum(x%2!=0 or y%2!=0 for x,y in interior)
 sN=sum(x%2!=0 or y%2!=0 for x,y in smooth)
 assert classify(p,S)==classify(p,T)=='interior'
 return dict(walls=len(p),reflex=reflex,area=str(F(a2,2)),perimeter=per,interior_points=interior,smooth_boundary_points=smooth,J=J,s_N=sN,k=J+sN)
a,b=analyze(D),analyze(Q)
assert (a['walls'],a['reflex'],a['area'],a['k'])==(22,9,'15',4)
assert (b['walls'],b['reflex'],b['area'],b['perimeter'],b['k'])==(20,8,'14',26,5)
assert b['interior_points']==[S,T]
# Vertical slab certificates prove the exact closure identity D=Q union([4,5]x[0,1]).
def vertical_intervals(p,x):
 ys=sorted(F(a[1]) for a,b in edges(p) if a[1]==b[1] and min(a[0],b[0])<x<max(a[0],b[0]))
 assert len(ys)%2==0
 return list(zip(ys[::2],ys[1::2]))
levels=sorted({x for x,y in D+Q});slabs=[]
for l,r in zip(levels,levels[1:]):
 x=F(l+r,2);d=vertical_intervals(D,x);q=vertical_intervals(Q,x)
 assert d==(q+[(F(0),F(1))] if 4<x<5 else q)
 slabs.append({'x_interval':[l,r],'D_intervals':[[str(x),str(y)] for x,y in d],'Q_intervals':[[str(x),str(y)] for x,y in q]})
assert classify(Q,(F(4),F(1,2)))=='boundary'
assert all(not (4<=x<=5 and 0<=y<=1) for x,y in [S,T])
source_paths=['review/fold-area-invariant.md','review/fold-area-invariant-acceptance.json','review/baseline-review.md','review/baseline-check.json','construction/baseline-and-gap.md','construction/baseline-receipts.json']
hashes={name:hashlib.sha256((R.parent/name).read_bytes()).hexdigest() for name in source_paths}
# Verify the existing accepted baseline's stated theorem source hash.
baseline=json.loads((R/'baseline-check.json').read_text())
for name,h in baseline['source_sha256'].items():
 if name.endswith('restricted-theorem-note/theorem.txt'):
  assert hashlib.sha256((CTX/name).read_bytes()).hexdigest()==h
  hashes[name]=h
# Verify actual-darkroom source pins named by its independent acceptance receipt.
acc=json.loads((R/'fold-area-invariant-acceptance.json').read_text())
for name,h in acc['source_sha256'].items():
 if name in ['fold-area-invariant.md','../../illumination-k4-codex/research-note.tex']:
  assert hashlib.sha256((R/name).read_bytes()).hexdigest()==h
  hashes[name]=h
out={'status':'PASS_PRESCRIBED_EAR_GEOMETRY_AND_ACCEPTED_DEPENDENCIES','original_D':D,'reduced_Q':Q,'S':S,'T':T,'ear_rectangle':[4,5,0,1],'shared_full_ear_side':[[4,0],[4,1]],'D_counts':a,'Q_counts':b,'vertical_slab_union_certificate':slabs,'D_actual_darkness':'Inherited accepted known22 hand proof; no finite ray failure used.','Q_actual_illumination':'Inherited accepted all-support W<=21,k<=6 theorem, applicable since W20,k5.','existential_transfer_implication':'FALSE without original-room r<=8 restriction: Q illuminated, D dark.','target_scope_limit':'D hasr9; this is NOT a counterexample to programme target or r<=8-only transfer.','source_sha256':hashes,'new_discovery_or_search':False,'whole_goal_complete':False}
(R/'geometric-reduction-ear-monotonicity-check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','D_counts','Q_counts','existential_transfer_implication','target_scope_limit']},indent=2))
