"""Prescribed exact original-contour validation of the d-regime four-reflection formula."""
from pathlib import Path
from fractions import Fraction as Q
import ast,json
P=Path(__file__).resolve().parent;src=P.parent/'review/resumed-exact-check.py';ns={'Q':Q};names={'vec','det','dot','edges','on','location','intersect','simple','path_check'};a=ast.parse(src.read_text());exec(compile(ast.Module(body=[n for n in a.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[]),str(src),'exec'),ns);rows=[]
for d in (3,6,12,1000):
 for c,ws,wt,a,b in [(Q(3,2),Q(1,37),Q(1,43),Q(47,5),Q(1,29)),(Q(11),Q(1001),Q(1,19),Q(1,17),Q(400))]:
  G=d+10;p=[(0,0),(c,0),(c,1),(c+ws,1),(c+ws,3),(c,3),(c,7),(c+wt,7),(c+wt,9),(c,9),(c,G),(0,G),(0,d+7),(-b,d+7),(-b,d+5),(0,d+5),(0,5),(-a,5),(-a,3),(0,3)];path=[(c,Q(2)),(0,Q(d+9,2)),(c,Q(d+7)),(c*Q(d-1,d+5),Q(d+10)),(0,Q(d+21,2)),(c,Q(8))]
  ns['simple'](p);z=ns['path_check'](p,path);assert z['reflections']==4
  for A,B in zip(path[:-2],path[1:-1]):assert not ns['on'](A,B,path[-1])
  rows.append({'d':d,'c':str(c),'ws':str(ws),'wt':str(wt),**z})
out={'status':'PRESCRIBED_ORIGINAL_WALL_FOUR_PASS','discovery':False,'rows':rows,'validator_reuse':str(src),'whole_goal_complete':False};(P/'critical-d6-core-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
