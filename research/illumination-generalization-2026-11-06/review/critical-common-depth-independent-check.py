"""A65 independent actual first-hit controls; no author optical code."""
from pathlib import Path
from fractions import Fraction as Q
import ast,importlib.util,json,hashlib
R=Path(__file__).resolve().parent;P=R.parent/'construction'
s=importlib.util.spec_from_file_location('g',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
ns={'Q':Q,'g':g};tr=ast.parse((R/'tooth-free-core-independent-check.py').read_text());exec(compile(ast.Module(body=[n for n in tr.body if isinstance(n,ast.FunctionDef) and n.name=='trace'],type_ignores=[]),'own trace','exec'),ns)
rows=[]
for h,d,G,m,K,sig,core in [(5,0,14,2,38,1,5),(3,6,16,2,22,-1,4),(3,10,20,4,46,1,9)]:
 for c,D in [(Q(1),Q(0)),(Q(2,7),Q(1,83)),(Q(13,5),Q(100,7)),(Q(1),Q(2*m,K)),(Q(7,3),Q(31,17))]:
  n=(D*K/(4*m*c)+Q(1,2))//1;tau=(Q(K,2)+2*n)/(m*c+D);delta=D*tau-2*n;assert -1<delta<1
  t=2*h+2;left2=h+4 if not d else h+d+2;ws=D+Q(1,101);wt=D+Q(1,103);a=Q(1,107);b=Q(100003)
  V=[tuple(map(Q,z)) for z in [(0,0),(c,0),(c,1),(c+ws,1),(c+ws,3),(c,3),(c,t-1),(c+wt,t-1),(c+wt,t+1),(c,t+1),(c,G),(0,G),(0,left2+2),(-b,left2+2),(-b,left2),(0,left2),(0,h+2),(-a,h+2),(-a,h),(0,h)]]
  g.simple(V);path,_=ns['trace'](V,(c+D,Q(2)),(c+D,Q(t)),(Q(-1),(-1)**int(n)*tau),2*int(n)+core);z=g.path_check(V,path);rows.append({'h':h,'d':d,'c':str(c),'D':str(D),'n':int(n),'delta':str(delta),**z})
req=json.loads((P/'critical-common-depth-review-request.json').read_text())
for f,h in req['source_sha256'].items():assert hashlib.sha256((P/f).read_bytes()).hexdigest()==h
out={'status':'ALL_OWN_ACTUAL_FIRST_HIT_CONTROLS_PASS','author_code_executed':False,'whole_goal_complete':False,'source_sha256':req['source_sha256'],'rows':rows,'actual_paths':len(rows),'reflections':sum(z['reflections'] for z in rows),'wall_leg_guards':sum(z['wall_leg_guards'] for z in rows)}
(R/'critical-common-depth-independent-check.json').write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items() if k not in ['rows','source_sha256']})
