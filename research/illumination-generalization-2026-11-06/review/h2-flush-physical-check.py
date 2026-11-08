"""R48 actual-wall controls for all protected mechanisms; no discovery."""
from pathlib import Path
from fractions import Fraction as Q
import ast,importlib.util,json,hashlib
R=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('own',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
for file,names in [('minimal-prefix-physical-check.py',['events','arm']),('h2-A1-physical-check.py',['local'])]:
 a=ast.parse((R/file).read_text());exec(compile(ast.Module(body=[n for n in a.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[]),file+' defs only','exec'))
def poly(D,a,f,r):return [tuple(map(Q,z)) for z in [(-f,-3),(D+2,-3),(D+2,-1),(1,-1),(1,1),(D+2,1),(D+2,3),(1,3),(1,5),(-r,5),(-r,3),(0,3),(0,2),(-a,2),(-a,0),(0,0),(0,-1),(-f,-1)]]
short=[(1,-2),(Q(7,5),-3),(2,Q(-3,2)),(Q(9,5),-1),(1,-3),(0,Q(-1,2)),(1,2)]
rows=[]
for D in range(3):
 for a in [1,2,3,4,5,6,17,100]:
  path=short if D==0 else [(x,-y) for x,y in reversed(local(D,a))]
  for f,r in [(Q(1,3),100003),(100009,Q(2,7)),(1,1)]:
   V=poly(D,a,f,r);g.simple(V);assert len(V)==18 and path[0]==(1+D,-2) and path[-1]==(1+D,2)
   assert not any(g.on(u,v,path[-1]) for u,v in zip(path[:-2],path[1:-1]));res=g.path_check(V,path);rows.append({'D':D,'a':a,'floor_width':str(f),'roof_width':str(r),'polygon':V,'path':path,**res})
out={'status':'ALL_R48_PRESCRIBED_ACTUAL_PATHS_PASS','paths':len(rows),'rows':rows,'reflections':sum(r['reflections'] for r in rows),'wall_leg_guards':sum(r['wall_leg_guards'] for r in rows),'source_sha256':{f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ['h2-A1-proof.md','h2-A1-physical-check.py','minimal-prefix-physical-check.py','resumed-exact-check.py']},'discovery':False,'whole_goal_complete':False}
(R/'h2-flush-physical-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['rows','source_sha256']}))
