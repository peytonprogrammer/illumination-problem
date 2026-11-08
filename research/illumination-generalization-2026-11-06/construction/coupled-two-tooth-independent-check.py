"""Prescribed R51 original contour validation. No author discovery code executed."""
import ast,json,hashlib
from pathlib import Path
from fractions import Fraction as Q
P=Path(__file__).resolve().parent;R=P.parent/'review';request=json.loads((R/'coupled-two-tooth-review-request.json').read_text())
pins={f:hashlib.sha256((R/f).read_bytes()).hexdigest()==h for f,h in request['source_sha256'].items()};assert all(pins.values())
src=R/'resumed-exact-check.py';names={'vec','det','dot','edges','on','location','intersect','simple','path_check'};ns={'Q':Q};mod=ast.parse(src.read_text());exec(compile(ast.Module(body=[n for n in mod.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[]),str(src),'exec'),ns)
rows=[]
for a,b in [(Q(2,3),Q(2,3)),(Q(1,2),Q(7,12)),(Q(7,12),Q(1,2)),(Q(1,17),Q(1,31))]:
 assert 5*a-4*b<1 and 5*b-4*a<1
 q=9/(7+a+b)
 poly=[(0,0),(1,0),(1,1),(3,1),(3,3),(1,3),(1,13),(3,13),(3,15),(1,15),(1,16),(0,16),(0,12),(-b,12),(-b,10),(0,10),(0,8),(-a,8),(-a,6),(0,6)]
 path=[(2,2),(2-1/q,1),(0,2*q),(1,3*q),(0,4*q),(1,5*q),(-a,(6+a)*q),(1,(7+2*a)*q),(-b,(8+2*a+b)*q),(1,(9+2*a+2*b)*q),(0,(10+2*a+2*b)*q),(4-3/q,15),(3,12+q),(2+1/q,13),(2,14)]
 for c,v in [(Q(1),Q(1)),(Q(11),Q(7,3))]:
  p=[(c*x,v*y) for x,y in poly];t=[(c*x,v*y) for x,y in path];ns['simple'](p);z=ns['path_check'](p,t);assert z['reflections']==13
  for A,B in zip(t[:-2],t[1:-1]):assert not ns['on'](A,B,t[-1])
  rows.append({'a':str(a),'b':str(b),'c':str(c),'v':str(v),**z})
out={'status':'PRESCRIBED_ORIGINAL_CONTOUR_CHECKS_PASS','source_pins_current':pins,'rows':rows,'validator_reuse':str(src),'author_discovery_executed':False,'whole_goal_complete':False};(P/'coupled-two-tooth-independent-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'paths':len(rows),'reflections':sum(z['reflections'] for z in rows),'guards':sum(z['wall_leg_guards'] for z in rows)}))
