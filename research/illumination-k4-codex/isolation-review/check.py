"""Frozen geometry/endpoint and determinant-identity audit; no tracing."""
from pathlib import Path
from collections import Counter
from itertools import combinations
from fractions import Fraction as F
import json,math
B=Path(__file__).resolve().parent

def load(n):return json.loads((B/'inputs'/n).read_text())
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def census(room):
 tris=[tuple(map(tuple,t)) for t in room['triangles']];edges=Counter(tuple(sorted(e)) for t in tris for e in combinations(t,2));adj={}
 for (a,b),n in edges.items():
  if n==1:adj.setdefault(a,[]).append(b);adj.setdefault(b,[]).append(a)
 if 'vertices' in room:vertices=set(map(tuple,room['vertices']))
 else:vertices={p for p,ns in adj.items() if len(ns)!=2 or cross(sub(ns[0],p),sub(ns[1],p))}
 points={p for t in tris for p in t};bad=sorted(p for p in points if any(v%2 for v in p) and p not in vertices)
 return dict(non_A_noncorner_vertices=bad,parity_premise=not bad)

def main():
 cases=[];count=0
 for name,R in [('room-illumination-search-simple-unrestricted',12),('room-wolecki22-pinch',18),('room-tokarsky34',18),('room-jain28',18)]:
  room=load(name+'.json');c=census(room);assert c['parity_premise']
  rows=load(f'events-{name}-R{R}.json')['rows'];gcds=Counter()
  for e in rows:
   v=list(map(F,e['unfolded_target_minus_s']));assert all(a.denominator==1 and a.numerator%2==0 for a in v)
   w=[a.numerator//2 for a in v];g=math.gcd(*map(abs,w));gcds[g]+=1;assert g==1
  count+=len(rows);cases.append(dict(room=name,events=len(rows),half_endpoint_gcd=dict(gcds),**c))
 assert count==932
 known=census(load('known22.json'));assert not known['parity_premise']
 assert known['non_A_noncorner_vertices']==[(-1,0),(1,0),(2,1),(2,3)]
 # A = gamma1 + gamma2; C = gamma1. Exported determinant is cross(A,C).
 identities=0
 for w in [(1,0),(1,1),(2,-1),(-3,2)]:
  for dc in [(0,0),(1,0),(0,1),(2,-3)]:
   for dd in [(1,0),(0,1),(-2,3)]:
    dA=tuple(dc[i]+dd[i] for i in (0,1));A=tuple(2*v for v in w)
    derivative=cross(dA,w)+cross(A,dc)
    deta=sub(dd,dc)
    assert derivative==-cross(w,deta);identities+=1
 # Full rank and exact sqrt(length) growth do not force positive span.
 orthant=[tuple(m*int(i==j) for i in range(3)) for m in range(1,5) for j in range(3)]
 assert all(sum(row)>0 for row in orthant)
 assert {(1,0,0),(0,1,0),(0,0,1)}<=set(orthant)
 result=dict(status='PASS',orthant_control=dict(rows=len(orthant),rank=3,separating_covector=[1,1,1],growth='norm=m, length=m^2'),cases=cases,total_midpoint_endpoint_checks=count,known22=known,exported_sign_identity_checks=identities,identity='d cross(A,C) = -cross(w, delta gamma2 - delta gamma1)',scope='Finite endpoint/parity premises and exact algebra only. Event validity reused from accepted certificates; no homology growth, KZ or general-isolation conclusion.')
 (B/'check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
