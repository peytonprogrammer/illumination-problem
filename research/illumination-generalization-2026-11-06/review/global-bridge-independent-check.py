"""B01 own prescribed first-hit/facet and geometry checks; no discovery."""
from pathlib import Path
from fractions import Fraction as Q
import json,hashlib,importlib.util
R=Path(__file__).resolve().parent;P=R.parent/'construction';s=importlib.util.spec_from_file_location('g',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
rows=[]
for e in [Q(1),Q(2,3),Q(1,3),Q(1,11),Q(1,101),Q(1,999)]:
 V=[(Q(0),Q(0)),(Q(8),Q(0)),(Q(8),Q(6)),(4+e,Q(6)),(Q(4),6-e),(4-e,Q(6)),(Q(0),Q(6))];g.simple(V)
 S=(Q(2),Q(2));T=(Q(6),Q(2));assert g.location(V,S)==g.location(V,T)==1;assert g.location(V,(Q(4),Q(6)))==-1
 v=(Q(1),Q(2));hits=[]
 for i,(a,b) in enumerate(g.edges(V)):
  ed=g.vec(a,b);den=g.det(v,ed)
  if den:
   tt=g.det(g.vec(S,a),ed)/den;rr=g.det(g.vec(S,a),v)/den
   if tt>0 and 0<=rr<=1:hits.append((tt,i,rr))
 tt,i,rr=min(hits);assert i==4 and 0<rr<1
 H=tuple(S[k]+tt*v[k] for k in [0,1]);assert H==(4-e/3,6-2*e/3)
 n=(1,1);refl=tuple(v[k]-2*Q(g.dot(v,n),g.dot(n,n))*n[k] for k in [0,1]);assert refl==(-2,-1) and g.det(refl,g.vec(H,T))!=0
 X=2+(6-e)**2/(8-2*e);assert X>4 and 8-X<4
 rows.append({'e':str(e),'first_hit_wall':i,'first_hit':list(map(str,H)),'left_candidate':str(X),'right_candidate':str(8-X),'direct':g.path_check(V,[S,T])})
for n in [1,3,11,101]:
 V=[(0,0),(16*n,0),(16*n,12*n),(8*n+2,12*n),(8*n,12*n-2),(8*n-2,12*n),(0,12*n)];g.simple(V);assert len(V)==7
 for a,b in g.edges(V):
  dx,dy=g.vec(a,b);assert not dx or not dy or abs(dx)==abs(dy)
  if dx and dy:assert (a[0]+a[1])%2==0
 for Z in [(4*n,4*n),(12*n,4*n)]:assert Z[0]%2==Z[1]%2==0 and g.location(V,Z)==1
limit=[(0,0),(8,0),(8,6),(0,6)];lr=g.path_check(limit,[(2,2),(4,6),(6,2)])
req=json.loads((P/'global-bridge-review-request.json').read_text())
for f,h in req['sources'].items():assert hashlib.sha256((P/f).read_bytes()).hexdigest()==h
out={'status':'B01_ALL_OWN_PRESCRIBED_EXACT_CONTROLS_PASS','whole_goal_complete':False,'author_code_executed':False,'source_sha256':req['sources'],'rows':rows,'canonical_n_controls':[1,3,11,101],'limit_roof_path':lr,'hand_identity':'X-4=(e^2-8e+20)/(8-2e)>0 for0<e<=1; numerator>=13, denominator>=6'}
(R/'global-bridge-independent-check.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
