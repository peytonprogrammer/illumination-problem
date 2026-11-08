"""R55 exact five phase charts and actual repairs; no discovery in this script."""
from pathlib import Path
from fractions import Fraction as Q
import ast,importlib.util,json,hashlib,itertools
R=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('g',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
ns={'Q':Q,'g':g}
for f,names in [('minimal-prefix-physical-check.py',{'events'}),('unequal-seam-phase-check.py',{'fararm','endfold'})]:
 tree=ast.parse((R/f).read_text());exec(compile(ast.Module(body=[z for z in tree.body if isinstance(z,ast.FunctionDef) and z.name in names],type_ignores=[]),'own actual far definitions','exec'),ns)
def choose(q):
 if q in [Q(1,3),Q(1)]:return None
 if q>1:return 2,int((Q(3,2)*q+Q(1,2))//1)
 if q<Q(1,3):return 2,0
 if q>Q(1,2):return 2,1
 if q>Q(2,5):return 5,2
 return 4,2
four=[(1,2),(0,Q(2,7)),(Q(1,6),0),(Q(4,3),2),(0,Q(30,7)),(1,6)]
ten=[(1,2),(Q(14,11),1),(Q(20,11),3),(2,Q(7,3)),(Q(18,11),1),(Q(12,11),3),(Q(3,11),0),(0,1),(1,Q(14,3)),(0,Q(25,3)),(Q(2,11),9),(1,6)]
arith=0
for p,r in itertools.product(range(1,81),repeat=2):
 q=Q(p,r);ch=choose(q)
 if ch:
  H,n=ch;m=(q*H-n)/(1+q);assert -Q(1,2)<m<Q(1,2) and (m<0 if H==4 else m>0)
  assert q*H-(1+q)/2<n<q*H+(1+q)/2
 arith+=1
rows=[]
ratios=[Q(1,1000),Q(1,5),Q(1,3),Q(1,3)+Q(1,10000),Q(2,5),Q(2,5)+Q(1,10000),Q(1,2),Q(3,5),Q(999,1000),Q(1),Q(1001,1000),Q(2),Q(17)]
for c,q,qt in itertools.product([Q(1),Q(11,3)],ratios,[Q(1,1000),Q(1,5),Q(10003)]):
 w,wt=c*q,c*qt;a,b=Q(1,181),Q(100069)
 V=[(0,0),(c,0),(c,1),(c+w,1),(c+w,3),(c,3),(c,5),(c+wt,5),(c+wt,7),(c,7),(c,9),(0,9),(0,7),(-b,7),(-b,5),(0,5),(0,4),(-a,4),(-a,2),(0,2)]
 V=[tuple(map(Q,z)) for z in V];g.simple(V);ch=choose(q)
 if ch is None:path=[(c*x,y) for x,y in (four if q==Q(1,3) else ten)]
 else:
  H,n=ch;tau=Q(H+n,c+w);m=w*tau-n
  if H in [2,5]:
   aa,bb=Q(2),Q(6 if H==2 else 12);path=list(reversed(ns['fararm'](c,w,aa,aa+2*m,tau,-1)))+[(Q(0),(aa+bb)/2+m),(c,bb)];path=ns['endfold'](path,Q(9))
  else:
   path=[(c,Q(-6)),(Q(0),-2-m),(c,2-2*m)]+ns['fararm'](c,w,Q(2),2-2*m,tau,1)[1:];path=list(reversed(ns['endfold'](path,Q(9))))
 assert path[0]==(c,2) and path[-1]==(c,6)
 assert not any(g.on(A,B,path[-1]) for A,B in zip(path[:-2],path[1:-1]));z=g.path_check(V,path)
 rows.append({'c':c,'source_ratio':q,'target_ratio':qt,'chart':ch,'path':path,**z})
out={'status':'R55_FULL_SOURCE_WIDTH_PHASE_COVER_AND_ACTUAL_PATHS_PASS','whole_goal_complete':False,'discovery':False,'arithmetic_controls':arith,'actual_paths':len(rows),'reflections':sum(z['reflections'] for z in rows),'wall_leg_guards':sum(z['wall_leg_guards'] for z in rows),'rows':rows,'source_sha256':{f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ['unequal-seam-phase-proof.md','unequal-seam-phase-acceptance.json','resumed-exact-check.py','minimal-prefix-physical-check.py']}}
(R/'unequal-width-h2-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print({k:v for k,v in out.items() if k not in ['rows','source_sha256']})
