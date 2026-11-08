"""Same bounded cap-chart effort: exact centered failure graph, no rays."""
from fractions import Fraction as F
from pathlib import Path
from math import gcd
import json,time
B=Path(__file__).parent;E=json.loads((B/'cap-chart-effort.json').read_text())
def guard():
    if time.time()>=E['deadline']:raise TimeoutError('same original840s deadline')
def works(A,C,q):
    # alpha=A/q,beta=C/q. Full period2q of all odd target lifts.
    for n in range(2*q):
        guard();x=(q+2*n*A)%(4*q);y=(q+2*n*C)%(4*q)
        if q<x<2*q and (0<y<q or q<y<2*q):return True
        if 2*q<x<3*q and (2*q<y<3*q or 3*q<y<4*q):return True
    return False
edges=set();pairs=[]
for q in range(3,65):
 for A in range(1,q-1):
  for C in range(A+1,q):
   if gcd(gcd(A,C),q)!=1:continue
   if not works(A,C,q):
    a,b=F(A,C-A),F(q-C,C-A)
    edges.add((a,b));pairs.append({'a':str(a),'b':str(b),'q':q,'A':A,'C':C})
rect=[];neighbors={}
for a,b in edges:neighbors.setdefault(a,set()).add(b)
xs=sorted(neighbors)
for i,a in enumerate(xs):
 for A in xs[i+1:]:
  guard();bs=sorted(neighbors[a]&neighbors[A])
  if len(bs)>=2:
   rect.append(list(map(str,[a,A,bs[0],bs[1]])))
   break
 if rect:break
special=[p for p in pairs if abs(F(p['a'])-F(p['b']))!=1]
out={'status':'CLASSIFIED_FINITE_CONTROLS','phase_denominator_max':64,
     'failing_center_pairs':len(edges),'non_unit_difference_pairs':special,
     'first_NE_rectangle':rect,'effort':E,
     'scope':'Exact all odd lifts for each rational control; no universal classification or darkness.'}
(B/'center-failure-graph.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ('non_unit_difference_pairs','effort')}))
print(json.dumps(special[:30]))
