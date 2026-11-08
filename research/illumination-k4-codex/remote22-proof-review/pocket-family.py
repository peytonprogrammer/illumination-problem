"""Symbolic specialization of the proved path as the pocket height varies.
Root isolation partitions exact sign predicates, not sampled optical discovery.
"""
from pathlib import Path
from fractions import Fraction as F
import json,sys
import sympy as s
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE/'inputs'))
from boundary_replay import replay
h=s.Symbol('h',real=True);d=(9+h)/13
P=[(0,0),(2*d/(1+d),-2/(1+d)),(-2,4*d-2),(-1,5*d-2),
   (4-(3+h)/d,1+h),(-2,4+2*h-6*d),((5+2*h)/d-8,-1),
   (3,11*d-6-2*h),(1,13*d-6-2*h),((9+2*h)/d-12,3),
   (3,12+2*h-15*d),((18*d-14-2*h)/(1+d),(12+2*h-20*d)/(1+d)),
   (21*d-14-2*h,1),(23*d-14-2*h,-1),(3,(17+2*h)/d-24),(2,2)]
P=[tuple(map(s.cancel,p)) for p in P]
V=[(-3,1),(-1,-1),(0,-1),(0,-2),(1,-1),(3,-1),(4,0),(3,0),(3,1),(4,2),(3,2),(3,3),(2,3),(2,4),(1,3),(1,1),(-1,1),(-1,1+h),(-2,1+h),(-2,1)]
V=[tuple(map(s.sympify,p)) for p in V];E=list(zip(V,V[1:]+V[:1]))
lo,hi=s.Rational(19,20),s.Rational(21,20)
def sub(a,b):return a[0]-b[0],a[1]-b[1]
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def dot(a,b):return a[0]*b[0]+a[1]*b[1]
def orient(a,b,c):return cross(sub(b,a),sub(c,a))
polys={};roots=set()
def track(expr):
    n,de=s.fraction(s.cancel(expr))
    assert s.Poly(de,h).count_roots(lo,hi)==0
    if n==0:return
    poly=s.Poly(n,h).monic();polys[str(poly.as_expr())]=poly
for a,b in zip(P,P[1:]):
 for c,e in E:
  for expr in (orient(a,b,c),orient(a,b,e),orient(c,e,a),orient(c,e,b)):
   track(expr)
  # Coordinate ordering resolves identically-collinear segment predicates.
  for p in (a,b):
   for q in (c,e):
    for k in (0,1):track(p[k]-q[k])
wall_indices=[3,18,16,17,18,4,7,14,11,10,0,15,4,7]
for i,j in enumerate(wall_indices,1):
 w=sub(E[j][1],E[j][0]);v=sub(P[i],P[i-1]);nxt=sub(P[i+1],P[i])
 r=tuple(s.cancel(2*dot(v,w)*w[k]/dot(w,w)-v[k]) for k in (0,1))
 assert s.cancel(cross(r,nxt))==0
 assert s.cancel(orient(*E[j],P[i]))==0
 track(dot(r,nxt))
for poly in polys.values():
 rr={r for r in s.polys.polytools.ground_roots(poly) if lo<=r<=hi}
 assert poly.count_roots(lo,hi)==len(rr),('nonrational critical root',poly)
 roots.update(rr)
breaks=sorted({lo,hi}|roots)
tests=set(roots)|{(a+b)/2 for a,b in zip(breaks,breaks[1:])}
def frac(v):return F(int(v.p),int(v.q))
for x in sorted(tests):
 if not lo<x<hi:continue
 vv=[tuple(frac(s.cancel(q.subs(h,x))) for q in p) for p in V]
 pp=[tuple(frac(s.cancel(q.subs(h,x))) for q in p) for p in P]
 assert replay(vv,(0,0),(2,2),pp)==14
result={'status':'PASS','theorem':'For every real h in (19/20,21/20), changing only the remote square roof height from y=2 to y=1+h preserves a legal14-reflection S/T connection with launch (h+9,-13).',
 'method':'Exact rational symbolic reflection identities plus complete rational-root isolation for all segment/wall orientation and endpoint-order predicates. Predicate signs are constant between isolated roots; boundary replay verifies each open sign cell and each interior critical root. This certifies a continuum, not a finite sample inference.',
 'distinct_nonzero_predicate_polynomials':len(polys),'critical_heights':[str(r) for r in sorted(roots)],
 'replayed_sign_cell_representatives_and_critical_heights':[str(r) for r in sorted(tests) if lo<r<hi],
 'parameter':'d=(9+h)/13','endpoint_equation':'x=20+2h-26d at y=2',
 'contact_formulas':[[str(q) for q in p] for p in P], 'scope':'Continuous family near the supplied room only. Fixed angle directions and20walls; most h are outside the original canonical lattice. Does not prove illumination for arbitrary pocket shapes or other cap arrangements.'}
(HERE/'pocket-family.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='contact_formulas'},indent=2))
