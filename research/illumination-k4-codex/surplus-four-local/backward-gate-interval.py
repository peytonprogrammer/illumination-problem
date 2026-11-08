"""Prove one predeclared itinerary over its whole rational interval.
This partitions boundary-predicate signs, not a search for optical paths.
"""
from pathlib import Path
from fractions import Fraction as F
import json,runpy,sys
import sympy as s
HERE=Path(__file__).resolve().parent
setup=runpy.run_path(str(HERE/'backward-gate-check.py'))
replay=setup['replay'];cross=setup['cross'];sub=setup['sub'];dot=setup['dot']
d=s.Symbol('d',real=True);lo=s.Rational(7,44);hi=s.Rational(5,31)
rows={}
for kind in ['Louter3','Louter4']:
 word=setup['base']+[setup['Rdiag'],((0,1),0),setup['Rdiag']]+setup['Rleft'][kind]+setup['Rtail']
 p=(s.Integer(0),s.Integer(0));v=(d,s.Integer(1));P=[p]
 for normal,k in word:
  t=s.cancel((k-dot(normal,p))/dot(normal,v))
  p=tuple(s.cancel(p[i]+t*v[i]) for i in (0,1));P.append(p)
  q=s.cancel(2*dot(normal,v)/dot(normal,normal))
  v=tuple(s.cancel(v[i]-q*normal[i]) for i in (0,1))
 t=s.cancel((2-p[0])/v[0]);p=tuple(s.cancel(p[i]+t*v[i]) for i in (0,1));P.append(p)
 assert s.cancel(p[0]-2)==0 and s.cancel(p[1]-(10-50*d))==0
 rr=setup['rooms'][kind+'_Nbplus_Rminus'];V=[tuple(map(s.Rational,q)) for q in rr['vertices']];E=list(zip(V,V[1:]+V[:1]))
 polys={}
 def track(expr):
  num,den=s.fraction(s.cancel(expr))
  assert s.Poly(den,d).count_roots(lo,hi)==0
  if num==0:return
  poly=s.Poly(num,d).monic();polys[str(poly.as_expr())]=poly
 for a,b in zip(P,P[1:]):
  for c,e in E:
   for expr in (cross(sub(b,a),sub(c,a)),cross(sub(b,a),sub(e,a)),cross(sub(e,c),sub(a,c)),cross(sub(e,c),sub(b,c))):track(expr)
   for pp in (a,b):
    for qq in (c,e):
     for k in (0,1):track(pp[k]-qq[k])
 roots=set()
 for poly in polys.values():
  rr={q for q in s.polys.polytools.ground_roots(poly) if lo<=q<=hi}
  assert poly.count_roots(lo,hi)==len(rr),('nonrational interior critical point',poly)
  roots.update(rr)
 breaks=sorted({lo,hi}|roots)
 tests=(set(roots)|{(a+b)/2 for a,b in zip(breaks,breaks[1:])})-{lo,hi}
 frac=lambda q:F(int(q.p),int(q.q))
 VV=[tuple(frac(q) for q in p) for p in V]
 for q in sorted(tests):
  PP=[tuple(frac(s.cancel(v.subs(d,q))) for v in p) for p in P]
  assert replay(VV,(0,0),PP[-1],PP)==len(word)
 # Source, mirror and terminal coordinates are now valid across every sign cell
 # and at every interior breakpoint. Specular identities hold by construction.
 rows[kind]={'status':'FULL_INTERVAL_PASS','reflections':len(word),'target_line_endpoint':['2','10-50*d'],'predicate_polynomials':len(polys),'interior_critical_parameters':[str(q) for q in sorted(roots) if lo<q<hi],'exact_sign_cells_and_breakpoints_checked':len(tests)}
 print(kind,'full interval PASS',len(polys),'polynomials',len(tests),'exact sign checks',flush=True)
(HERE/'backward-gate-interval.json').write_text(json.dumps({'status':'PASS','interval':['7/44','5/31'],'actual_target_parameter':'4/25','proof_method':'Symbolic segment/boundary predicate root partition and exact replay of every sign cell and interior breakpoint for two predeclared paths; not trajectory discovery.','families':rows},indent=2)+'\n')
