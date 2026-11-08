"""Prescribed local stars and the frozen8-case W9 classification, not discovery."""
from pathlib import Path
from collections import Counter
from fractions import Fraction as F
from itertools import product
import json,hashlib
B=Path(__file__).resolve().parent
D=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
def star(a):return [frozenset((a,(a[0]+D[i][0],a[1]+D[i][1]),(a[0]+D[(i+1)%8][0],a[1]+D[(i+1)%8][1]))) for i in range(8)]
def mixed(v):return (v[0]%2)!=(v[1]%2)
def tri_mixed(t):
 p=[v for v in t if mixed(v)];assert len(p)==1;return p[0]
A=(0,0);source=set(star(A));neighbors={(1,0),(-1,0),(0,1),(0,-1)}
assert Counter(tri_mixed(t) for t in source)=={p:2 for p in neighbors}
assert all(len([v for v in t if v[0]%2==v[1]%2==0])==1 for t in source)
controls=[]
# The four axial near positions are the only A positions sharing a mixed
# neighbor, by difference of axial vectors. Diagonal/far cases are controls.
positions=[(2,0),(-2,0),(0,2),(0,-2),(2,2),(-2,2),(2,-2),(-2,-2),(4,0),(0,4)]
for b in positions:
 st=star(b)
 for start in range(8):
  target={st[(start+i)%8] for i in range(4)};assert not source&target
  U=source|target;c=Counter(tri_mixed(t) for t in U)
  if any(c[p]>3 for p in neighbors):
   controls.append(dict(b=b,start=start,status='FORBIDDEN_INTERIOR_MIXED'));continue
  missing=sum(3-c[p] for p in neighbors)
  assert missing>=3;assert len(U)+missing>=15
  controls.append(dict(b=b,start=start,triangles_with_required_fill=len(U)+missing,status='PASS_LOWER_BOUND'))
# All possible shared-neighbor separations, algebraically complete.
diffs={(u[0]-v[0],u[1]-v[1]) for u in neighbors for v in neighbors if u!=v}
even={v for v in diffs if v[0]%2==v[1]%2==0};assert even==set(positions[:4])

prototype=[(0,0),(1,1),(2,1),(2,3),(1,3),(1,2),(-1,2),(-1,1),(0,1)]
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def sub(a,b):return(a[0]-b[0],a[1]-b[1])
def on(a,b,p):return not cross(sub(b,a),sub(p,a)) and all(min(a[j],b[j])<=p[j]<=max(a[j],b[j]) for j in (0,1))
def inside(V,p):
 if any(on(a,b,p) for a,b in zip(V,V[1:]+V[:1])):return False
 w=0
 for a,b in zip(V,V[1:]+V[:1]):
  if a[1]<=p[1]<b[1] and cross(sub(b,a),sub(p,a))>0:w+=1
  if b[1]<=p[1]<a[1] and cross(sub(b,a),sub(p,a))<0:w-=1
 return bool(w)
def noncorners(V):
 out=[]
 for x in range(min(x for x,y in V),max(x for x,y in V)+1):
  for y in range(min(y for x,y in V),max(y for x,y in V)+1):
   if (x,y) not in V and (inside(V,(x,y)) or any(on(a,b,(x,y)) for a,b in zip(V,V[1:]+V[:1]))):out.append((x,y))
 return out
assert noncorners(prototype)==[(0,2),(2,2)]
def cyclic(C,V):return any(C==V[i:]+V[:i] or C==V[::-1][i:]+V[::-1][:i] for i in range(len(V)))
classifications=[]
for line in (B/'base-replay.txt').read_text().splitlines():
 z=line.split();w=int(z[0]);assert w>=9
 if w!=9:continue
 V=[tuple(map(int,p.split(','))) for p in z[2:]];matches=[]
 for swap,sx,sy in product((False,True),(-1,1),(-1,1)):
  def lin(p):x,y=p[::-1] if swap else p;return sx*x,sy*y
  T=list(map(lin,V))
  for p in prototype:
   tx,ty=p[0]-T[0][0],p[1]-T[0][1];C=[(x+tx,y+ty) for x,y in T]
   if cyclic(C,prototype):
    assert tx%2==ty%2==0
    mapped=sorted((lin(p)[0]+tx,lin(p)[1]+ty) for p in noncorners(V));assert mapped==[(0,2),(2,2)]
    matches.append(dict(swap=swap,sx=sx,sy=sy,translation=(tx,ty)))
 assert matches;classifications.append(dict(vertices=V,noncorners=noncorners(V),maps_to_prototype=matches))
assert len(classifications)==8
# A fixed rational disk/box around(3/2,2) lies in the arm and its reflection.
box=[(F(5,4),F(7,4)),(F(7,4),F(7,4)),(F(7,4),F(9,4)),(F(5,4),F(9,4))]
for p in box:assert inside(prototype,p) and inside(prototype,(p[0],4-p[1]))
assert {(x,4-y) for x,y in box}==set(box)
result=dict(status='PASS',local_halfstar_cases=len(controls),forbidden_local_cases=sum(c['status'].startswith('FORBIDDEN') for c in controls),minimum_required_triangle_count=min(c['triangles_with_required_fill'] for c in controls if c['status']=='PASS_LOWER_BOUND'),base_wall_bound=14,classification_cases=len(classifications),classification_parity_preserving=True,non_supporting_wall='y=2 passes through interior at(3/2,2)',controls=controls,scope='Local fan counts and frozen W9 classification only; Euler/topology and supporting-line lemmas are written arguments, not proven by this script.')
# Necessary wall inequalities, not room enumeration. m=1 uses prior W<=22
# exclusion; m=2 uses the new topological+14-wall lemma; others need c>=10.
equality=[]
for m in range(1,7):
 for c in range(9,24):
  if m==1 or (m==2 and c<14) or (m>=2 and c==9):continue
  lower=m*(c-4)+4
  if lower<=22:equality.append((m,c,lower))
assert equality==[(3,10,22)]
replay=json.loads((B/'replay.json').read_text())
assert all(r['copies']==3 and r['base_walls']==10 for r in replay['positive_controls'])
result['only_possible_22_equality_parameters']=equality
result['saved_positive_equality_controls']=len(replay['positive_controls'])
(B/'base-nine-classification.json').write_text(json.dumps(classifications,indent=2)+'\n');(B/'short-proof-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='controls'},indent=2))
