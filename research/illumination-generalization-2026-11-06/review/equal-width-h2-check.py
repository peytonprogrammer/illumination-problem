"""R54 prescribed exact all-real-phase implication controls and actual paths."""
from pathlib import Path
from fractions import Fraction as Q
import ast,importlib.util,json,hashlib,itertools
R=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('g',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
ns={'Q':Q,'g':g}
for f,names in [('minimal-prefix-physical-check.py',{'events'}),('unequal-seam-phase-check.py',{'phase','fararm','candidates','endfold'})]:
 tree=ast.parse((R/f).read_text());exec(compile(ast.Module(body=[z for z in tree.body if isinstance(z,ast.FunctionDef) and z.name in names],type_ignores=[]),'own phase/far definitions','exec'),ns)
arith=0
for p,r in itertools.product(range(1,51),repeat=2):
 q=Q(p,r);m2=ns['phase'](Q(1),q,Q(2))[2];m5=ns['phase'](Q(1),q,Q(5))[2]
 assert (m2==m5==0)==(q==1);arith+=1
rows=[]
for c,q in itertools.product([Q(1),Q(7,3),Q(100003)],[Q(1,1000),Q(1,3),Q(2,5),Q(1,2),Q(3,5),Q(2,3),Q(999,1000),Q(1),Q(1001,1000),Q(2),Q(17)]):
 w=c*q;a,b=Q(1,179),Q(100057)
 V=[(0,0),(c,0),(c,1),(c+w,1),(c+w,3),(c,3),(c,5),(c+w,5),(c+w,7),(c,7),(c,9),(0,9),(0,7),(-b,7),(-b,5),(0,5),(0,4),(-a,4),(-a,2),(0,2)]
 V=[tuple(map(Q,z)) for z in V];g.simple(V)
 if q==1:
  path=[(c*x,y) for x,y in [(1,2),(0,Q(14,3)),(1,Q(22,3)),(Q(3,8),9),(0,8),(Q(9,8),5),(Q(15,8),7),(2,Q(20,3)),(Q(11,8),5),(1,6)]];H='q1 eight'
 else:
  H=2 if ns['phase'](c,w,Q(2))[2] else 5
  aa,bb=(Q(2),Q(6)) if H==2 else(Q(2),Q(12))
  opts=ns['candidates'](c,aa,bb,w,w);paths=[ns['endfold'](path,Q(9)) for path,turn,name in opts if g.fold(turn,Q(9))>(4 if H==2 else 7)]
  assert len(paths)==1;path=paths[0]
 assert path[0]==(c,2) and path[-1]==(c,6)
 assert not any(g.on(A,B,path[-1]) for A,B in zip(path[:-2],path[1:-1]));out=g.path_check(V,path)
 rows.append({'c':c,'w/c':q,'chart':H,**out})
out={'status':'R54_ALL_EXACT_PHASE_AND_ACTUAL_PATH_CONTROLS_PASS','whole_goal_complete':False,'discovery':False,'arithmetic_cases':arith,'actual_paths':len(rows),'reflections':sum(z['reflections'] for z in rows),'wall_leg_guards':sum(z['wall_leg_guards'] for z in rows),'rows':rows,'source_sha256':{f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ['unequal-seam-phase-proof.md','unequal-seam-phase-acceptance.json','h2-A1-proof.md','h2-A1-acceptance.json','resumed-exact-check.py']}}
(R/'equal-width-h2-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print({k:v for k,v in out.items() if k not in ['rows','source_sha256']})
