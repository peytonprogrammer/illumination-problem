"""Independent algebra/geometry readback of the supplied24-wall functional data.
No event reconstruction is claimed when directions/words are not supplied.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from itertools import combinations
from math import gcd
import json
B=Path(__file__).resolve().parent;I=B/'inputs'
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def diff(a,b):return tuple(x-y for x,y in zip(a,b))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def rank(rows):
 pivots={}
 for row in rows:
  r=list(map(F,row))
  for i,p in sorted(pivots.items()):
   if r[i]:r=[x-r[i]*y for x,y in zip(r,p)]
  if any(r):
   i=next(i for i,v in enumerate(r) if v);v=r[i];pivots[i]=[x/v for x in r]
 return len(pivots)
room=json.loads((I/'room-illumination-search-simple-unrestricted.json').read_text());tris=[tuple(map(tuple,t)) for t in room['triangles']];counts=Counter(tuple(sorted(e)) for t in tris for e in combinations(t,2));edges=[e for e,n in counts.items() if n==1];adj={}
for a,b in edges:adj.setdefault(a,[]).append(b);adj.setdefault(b,[]).append(a)
assert all(len(v)==2 for v in adj.values());start=min(adj);path=[start];old=None;p=start
while True:
 q=min(v for v in adj[p] if v!=old)
 if q==start:break
 path.append(q);old,p=p,q
vertices=[p for i,p in enumerate(path) if cross(diff(p,path[i-1]),diff(path[(i+1)%len(path)],p))]
assert len(vertices)==24
steps=[diff(b,a) for a,b in zip(vertices,vertices[1:]+vertices[:1])];directions=[(dx//gcd(abs(dx),abs(dy)),dy//gcd(abs(dx),abs(dy))) for dx,dy in steps];lengths=[gcd(abs(dx),abs(dy)) for dx,dy in steps]
D=30;closure=[tuple([0,0]+[d[axis] for d in directions]+[0,0,0,0]) for axis in (0,1)];syms=[]
for axis in (0,1):
 r=[0]*D;r[axis]=r[26+axis]=r[28+axis]=1;syms.append(tuple(r))
scale=vertices[0]+tuple(lengths)+tuple(room['marked'][0])+tuple(room['marked'][1]);syms.append(scale)
peer=json.loads((I/'funcs-room-illumination-search-simple-unrestricted-R12.json').read_text());rows=[tuple(map(F,r)) for r in peer['funcs']];assert all(len(r)==30 for r in rows)
assert set(closure)=={tuple(map(F,r)) for r in peer['clos']};assert syms==[tuple(map(F,r)) for r in peer['syms']]
cert=json.loads((I/'posspan-room-illumination-search-simple-unrestricted-R12.json').read_text());coeff={int(i):F(v) for i,v in cert['coefficients'].items()};assert set(coeff)==set(range(len(rows))) and all(c>0 for c in coeff.values())
weighted=[sum(coeff[i]*rows[i][j] for i in coeff) for j in range(D)];assert rank([*closure,weighted])==2
r=rank([*closure,*rows])-2;assert r==25 and rank(syms)==3 and all(dot(v,s)==0 for v in rows for s in syms)
result=dict(status='ALGEBRA_PASS',walls=len(vertices),directions=sorted(set(directions)),parameter_dimension=30,closure_dimension=28,functionals=len(rows),rank_on_closure=r,kernel_dimension=28-r,symmetry_dimension=rank(syms),strict_positive_dependency=True,event_geometry='Independent geometric association is checked separately by replay.py',verdict='The supplied rows certify a3-dimensional first-order survival subspace algebraically; the optical meaning of those rows still needs independent replay.')
(B/'check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
