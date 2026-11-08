from pathlib import Path
from fractions import Fraction as F
from datetime import datetime,timezone
import ast,json,hashlib
R=Path(__file__).resolve().parent;P=R.parent/'review';source=P/'resumed-exact-check.py';tree=ast.parse(source.read_text());names={'vec','det','dot','edges','on','location','intersect','simple','path_check'};ns={'Q':F};exec(compile(ast.Module(body=[z for z in tree.body if isinstance(z,ast.FunctionDef) and z.name in names],type_ignores=[]),str(source),'exec'),ns)
a=json.loads((R/'tooth-return-grid-seeds.json').read_text());rows=[]
for z in a['rows']:
 assert (z['h'],z['d'],z['D'])==(4,2,1)
 # The roof vertices are the only changes. Reconstruct expected contour directly.
 aa,bb=z['a'],z['b'];V=[(0,0),(1,0),(1,1),(3,1),(3,3),(1,3),(1,9),(3,9),(3,11),(1,11),(1,14),(0,14),(0,10),(-bb,10),(-bb,8),(0,8),(0,6),(-aa,6),(-aa,4),(0,4)];V=[tuple(map(F,p)) for p in V];ns['simple'](V)
 path=[tuple(map(F,p)) for p in z['actual']['path']];assert path[0]==(2,2) and path[-1]==(2,10);assert max(p[1] for p in path)<=11
 check=ns['path_check'](V,path)
 for i,(p,q) in enumerate(zip(path,path[1:])):
  if ns['on'](p,q,(F(2),F(10))):assert i==len(path)-2
 rows.append({'a':aa,'b':bb,'required_roof':14,'original_roof':16,'maximum_used_height':max(p[1] for p in path),'polygon':V,'S':[2,2],'T':[2,10],'path':path,**check})
assert len(rows)==16 and {(z['a'],z['b']) for z in rows}=={(a,b) for a in(2,3,4,8) for b in(2,3,4,8)}
out={'status':'ALL_SIXTEEN_REQUIRED_G14_ORIGINAL_PATHS_PASS','rows':rows,'reflections':sum(z['reflections'] for z in rows),'all_wall_leg_guards':sum(z['wall_leg_guards'] for z in rows),'source_sha256':{n:hashlib.sha256((R/n).read_bytes()).hexdigest() for n in('tooth-return-grid-seeds.json','tooth-return-grid-proof.md')},'accepted_validator_definitions_reused':True,'discovery':False,'finished_utc':datetime.now(timezone.utc).isoformat(),'whole_goal_complete':False};(R/'tooth-return-grid-roof-repair.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in('rows','source_sha256')}))
