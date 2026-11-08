"""Exact prescribed formula controls for the all-real guarded shuttle and B/C joins."""
from pathlib import Path
from fractions import Fraction as Q
import importlib.util,json,hashlib
R=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('own',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
raw=json.loads((R/'c2-BC-closure-check.json').read_text());rows=[]
def path(mu):return[(Q(2),mu-2),(Q(3),mu-Q(5,3)),(Q(0),mu-Q(2,3)),(Q(2),mu),(Q(-1),mu+1),(Q(2),mu+2)]
def check(V,mu,family,r):
 V=[tuple(map(Q,z))for z in V];g.simple(V);p=path(mu)
 assert g.location(V,p[0])==g.location(V,p[-1])==1
 res=g.path_check(V,p);assert res['reflections']==4
 assert not any(g.on(a,b,p[-1])for a,b in zip(p[:-2],p[1:-1]))
 return{'family':family,'r':r,'mu':mu,**res}
for r in raw['rows']:
 assert r['first_path'];mu=(Q(r['source'][1])+Q(r['target'][1]))/2;rows.append(check(r['polygon'],mu,r['family'],r['r']))
for family in('C1','C2'):
 r=1000000;G=(10 if family=='C1'else 12)+4*r;mu=Q(G//2-(family=='C1'))
 V=[(-1,0),(2,0),(2,mu-3),(3,mu-3),(3,mu-1),(2,mu-1),(2,mu+1),(3,mu+1),(3,mu+3),(2,mu+3),(2,G),(-1,G),(-1,G-2),(0,G-2),(0,mu+2),(-1,mu+2),(-1,mu),(0,mu),(0,2),(-1,2)]
 rows.append(check(V,mu,family,r))
out={'status':'ALL_SIXTEEN_PRESCRIBED_FOUR_BOUNCE_FORMULAS_PASS','rows':rows,'reflections':sum(r['reflections']for r in rows),'wall_leg_guards':sum(r['wall_leg_guards']for r in rows),'whole_goal_complete':False,'discovery':False,'source_sha256':{f:hashlib.sha256((R/f).read_bytes()).hexdigest()for f in ['c2-BC-closure-check.json','resumed-exact-check.py']},'scope':'All14 original finite bases plus2 large-r prescribed formula controls; general proof uses exact all-r inequalities, not sampling.'}
(R/'c2-BC-four-bounce-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items()if k not in('rows','source_sha256')}))
