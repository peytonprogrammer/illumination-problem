"""Independent prescribed contour checks of R55's two literal repairs."""
from fractions import Fraction as Q
from pathlib import Path
import ast,json,hashlib
P=Path(__file__).resolve().parent;R=P.parent/'review';req=json.loads((R/'unequal-width-h2-review-request.json').read_text());pins={f:hashlib.sha256((R/f).read_bytes()).hexdigest()==h for f,h in req['source_sha256'].items()};assert all(pins.values())
ns={'Q':Q};src=R/'resumed-exact-check.py';names={'vec','det','dot','edges','on','location','intersect','simple','path_check'};m=ast.parse(src.read_text());exec(compile(ast.Module(body=[n for n in m.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[]),str(src),'exec'),ns)
paths={Q(1,3):[(1,2),(0,Q(2,7)),(Q(1,6),0),(Q(4,3),2),(0,Q(30,7)),(1,6)],Q(1):[(1,2),(Q(14,11),1),(Q(20,11),3),(2,Q(7,3)),(Q(18,11),1),(Q(12,11),3),(Q(3,11),0),(0,1),(1,Q(14,3)),(0,Q(25,3)),(Q(2,11),9),(1,6)]};rows=[]
for q,path in paths.items():
 for c,wt,a,b in [(Q(3,2),Q(1,37),Q(47,5),Q(1,29)),(Q(11),Q(1001),Q(1,17),Q(400))]:
  ws=c*q;poly=[(0,0),(c,0),(c,1),(c+ws,1),(c+ws,3),(c,3),(c,5),(c+wt,5),(c+wt,7),(c,7),(c,9),(0,9),(0,7),(-b,7),(-b,5),(0,5),(0,4),(-a,4),(-a,2),(0,2)];p=[(c*Q(x),Q(y)) for x,y in path];ns['simple'](poly);z=ns['path_check'](poly,p)
  for A,B in zip(p[:-2],p[1:-1]):assert not ns['on'](A,B,p[-1])
  rows.append({'source_ratio':str(q),'c':str(c),'target_width':str(wt),**z})
out={'status':'INDEPENDENT_PRESCRIBED_REPAIR_CHECKS_PASS','source_pins_current':pins,'rows':rows,'validator_reuse':str(src),'author_code_executed':False,'whole_goal_complete':False};(P/'unequal-width-h2-independent-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'paths':len(rows),'reflections':sum(r['reflections'] for r in rows),'guards':sum(r['wall_leg_guards'] for r in rows)}))
