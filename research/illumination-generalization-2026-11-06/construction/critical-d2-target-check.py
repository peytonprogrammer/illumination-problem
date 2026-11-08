"""Prescribed original-G12 contour checks of both protected actual repairs."""
from pathlib import Path
from fractions import Fraction as Q
import ast,json
P=Path(__file__).resolve().parent;src=P.parent/'review/resumed-exact-check.py';ns={'Q':Q};names={'vec','det','dot','edges','on','location','intersect','simple','path_check'};a=ast.parse(src.read_text());exec(compile(ast.Module(body=[n for n in a.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[]),str(src),'exec'),ns);rows=[]
for q in (Q(1,3),Q(1)):
 for c,ws,a,b in [(Q(3,2),Q(1,37),Q(47,5),Q(1,29)),(Q(11),Q(1001),Q(1,17),Q(400)),(Q(1000),Q(2,19),Q(7,13),Q(11,23))]:
  wt=q*c;p=[(0,0),(c,0),(c,1),(c+ws,1),(c+ws,3),(c,3),(c,7),(c+wt,7),(c+wt,9),(c,9),(c,12),(0,12),(0,9),(-b,9),(-b,7),(0,7),(0,5),(-a,5),(-a,3),(0,3)]
  if q==Q(1,3):path=[(c,Q(2)),(0,Q(28,5)),(c,Q(46,5)),(2*c/9,Q(12)),(0,Q(56,5)),(7*c/6,Q(7)),(4*c/3,Q(38,5)),(c/9,Q(12)),(0,Q(58,5)),(c,Q(8))]
  else:path=[(c,Q(2)),(c/4,Q(0)),(0,Q(2,3)),(c,Q(10,3)),(0,Q(6)),(9*c/8,Q(9)),(15*c/8,Q(7)),(2*c,Q(22,3)),(11*c/8,Q(9)),(c,Q(8))]
  ns['simple'](p);z=ns['path_check'](p,path);assert z['reflections']==8
  for A,B in zip(path[:-2],path[1:-1]):assert not ns['on'](A,B,path[-1])
  rows.append({'upper_ratio':str(q),'c':str(c),'lower_width':str(ws),**z})
out={'status':'PRESCRIBED_G12_PROTECTED_EIGHTS_PASS','discovery':False,'rows':rows,'validator_reuse':str(src),'whole_goal_complete':False};(P/'critical-d2-target-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
