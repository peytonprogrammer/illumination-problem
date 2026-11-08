from pathlib import Path
from fractions import Fraction as Q
from types import SimpleNamespace
from datetime import datetime,timezone
import ast,json,hashlib
R=Path(__file__).resolve().parent;P=R.parent/'review';E=json.loads((R/'small-depth-far-repair-effort.json').read_text());assert datetime.now(timezone.utc)<datetime.fromisoformat(E['deadline'])
# Import ONLY definitions from frozen accepted formula sources: no top-level writers or census.
def loaddefs(path,names,ns):
 tree=ast.parse(path.read_text());nodes=[z for z in tree.body if isinstance(z,ast.FunctionDef) and z.name in names];assert len(nodes)==len(names);exec(compile(ast.Module(body=nodes,type_ignores=[]),str(path),'exec'),ns)
ns={'Q':Q};names={'vec','det','dot','edges','on','location','intersect','simple','path_check','fold'};loaddefs(P/'resumed-exact-check.py',names,ns);g=SimpleNamespace(**{k:ns[k] for k in names})
fn={'Q':Q,'g':g};loaddefs(P/'unequal-depth-phase-check.py',{'phase','residues','polygon','prefix','physical'},fn)
rows=[]
for p,q,w,h,label in [(0,2,3,3,'mean'),(0,2,4,4,'bottom'),(1,3,4,3,'top'),(1,3,6,4,'mean'),(2,4,5,3,'bottom'),(2,4,8,4,'top')]:
 qp=2*w-q;v=fn['physical'](p,qp,h,label);tau=Q(v['tau']);N=w*tau;assert N.denominator==1;farphase=(w-q)*tau;assert not(farphase.denominator==1 and farphase.numerator%2)
 G=2*h+18;s=6;t=s+2*h;level={'mean':h+6,'bottom':h,'top':G-h}[label]
 left=[(level,level+2),(level+4,level+6)] if label!='top' else[(level-4,level-2),(level,level+2)]
 shift=0 if (1+p)%2==0 else 1;V=[(x+shift,y) for x,y in fn['polygon'](G,s,t,p+1,w,left)];g.simple(V)
 B=Q(1+w+shift);virtual=[tuple(map(Q,z)) for z in v['path']];expanded=[virtual[0]]
 for a,b in zip(virtual,virtual[1:]):
  if (a[0]-B)*(b[0]-B)<0:
   frac=(B-a[0])/(b[0]-a[0]);expanded.append((B,a[1]+frac*(b[1]-a[1])))
  expanded.append(b)
 actual=[(x if x<=B else 2*B-x,y) for x,y in expanded];S=(Q(1+p+shift),Q(s));T=(Q(1+q+shift),Q(t));assert actual[0]==S and actual[-1]==T
 for j,(a,b) in enumerate(zip(actual,actual[1:])):
  if g.on(a,b,T):actual=actual[:j+1]+[T];break
 check=g.path_check(V,actual)
 rows.append({'original_depths':[p,q],'w':w,'virtual_target_depth':qp,'h':h,'chart':label,'tau':tau,'N':N,'farphase':farphase,'polygon':V,'S':S,'T':T,'path':actual,**check})
assert datetime.now(timezone.utc)<datetime.fromisoformat(E['deadline'])
out={'status':'ALL_SIX_PRESCRIBED_FARFOLD_CONTROLS_PASS','rows':rows,'reflections':sum(r['reflections'] for r in rows),'all_wall_leg_guards':sum(r['wall_leg_guards'] for r in rows),'source_sha256':{str(q):hashlib.sha256(q.read_bytes()).hexdigest() for q in[P/'resumed-exact-check.py',P/'unequal-depth-phase-check.py']},'accepted_source_definitions_reused':True,'peer_writers_or_census_executed':False,'discovery':False,'whole_goal_complete':False,'original_deadline':E['deadline'],'finished_utc':datetime.now(timezone.utc).isoformat()}
(R/'small-depth-far-repair-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in('rows','source_sha256')}))
