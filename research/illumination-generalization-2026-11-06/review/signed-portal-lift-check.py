"""R56 prescribed new signed-source actual paths, independent first-hit tracing."""
from pathlib import Path
from fractions import Fraction as Q
import ast,importlib.util,json,hashlib
R=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('g',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
ns={'Q':Q,'g':g}
for f,fun in [('tooth-free-core-independent-check.py','trace'),('robust-portal-lift-check.py','match')]:
 tree=ast.parse((R/f).read_text());exec(compile(ast.Module(body=[z for z in tree.body if isinstance(z,ast.FunctionDef) and z.name==fun],type_ignores=[]),'own '+fun,'exec'),ns)
rows=[]
for c,v,hs,ht in [(Q(1),Q(1),Q(1,2),Q(1,2)),(Q(11),Q(7),Q(1),Q(3)),(Q(3,7),Q(2),Q(2,3),Q(1)),(Q(121),Q(13),Q(1,17),Q(5,3))]:
 for ds,dt in [(Q(0),Q(0)),(Q(0),Q(1)),(Q(1),Q(0)),(Q(1),Q(3)),(Q(7,3),Q(11,5)),(Q(11),Q(1))]:
  tau,n,delta,steps,bounds=ns['match'](4*c,14*v,hs,ht,ds,dt);ws,wt=ds+Q(1,233),dt+Q(3,239);a,b=Q(100193),Q(1,241)
  V=[(0,0),(c,0),(c,2*v-hs),(c+ws,2*v-hs),(c+ws,2*v+hs),(c,2*v+hs),(c,12*v-ht),(c+wt,12*v-ht),(c+wt,12*v+ht),(c,12*v+ht),(c,14*v),(0,14*v),(0,11*v),(-b,11*v),(-b,9*v),(0,9*v),(0,7*v),(-a,7*v),(-a,5*v),(0,5*v)]
  V=[tuple(map(Q,z)) for z in V];g.simple(V)
  path,_=ns['trace'](V,(c+ds,2*v),(c+dt,12*v),(Q(-1),-(-1)**n[0]*tau),sum(n)+4)
  z=g.path_check(V,path);rows.append({'c':c,'v':v,'hs':hs,'ht':ht,'Ds':ds,'Dt':dt,'tau':tau,'indices':n,'residuals':delta,'bound':4+sum(bounds),'path':path,**z})
out={'status':'R56_SIGNED_SOURCE_ORIGINAL_WALL_FIRST_HIT_PASS','whole_goal_complete':False,'discovery':False,'actual_paths':len(rows),'reflections':sum(z['reflections'] for z in rows),'wall_leg_guards':sum(z['wall_leg_guards'] for z in rows),'rows':rows,'source_sha256':{f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ['robust-portal-lift-proof.md','robust-portal-lift-acceptance.json','critical-five-source-independent-acceptance.json','resumed-exact-check.py']}}
(R/'signed-portal-lift-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print({k:v for k,v in out.items() if k not in ['rows','source_sha256']})
