"""Prescribed exact checks of protected8 on independently varied unused widths."""
from pathlib import Path
from fractions import Fraction as Q
import ast,json
P=Path(__file__).resolve().parent;src=P.parent/'review/resumed-exact-check.py';ns={'Q':Q};names={'vec','det','dot','edges','on','location','intersect','simple','path_check'};a=ast.parse(src.read_text());exec(compile(ast.Module(body=[n for n in a.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[]),str(src),'exec'),ns)
rows=[]
for c,ws,a,b in [(Q(4),Q(1),Q(1),Q(1)),(Q(3,2),Q(1,37),Q(47,5),Q(1,29)),(Q(11),Q(1001),Q(1,17),Q(400)),(Q(1000),Q(2,19),Q(7,13),Q(11,23))]:
 p=[(0,0),(c,0),(c,1),(c+ws,1),(c+ws,3),(c,3),(c,7),(2*c,7),(2*c,9),(c,9),(c,10),(0,10),(0,9),(-b,9),(-b,7),(0,7),(0,5),(-a,5),(-a,3),(0,3)]
 path=[(c,Q(2)),(c/4,Q(0)),(Q(0),Q(2,3)),(c,Q(10,3)),(Q(0),Q(6)),(9*c/8,Q(9)),(15*c/8,Q(7)),(2*c,Q(22,3)),(11*c/8,Q(9)),(c,Q(8))]
 ns['simple'](p);z=ns['path_check'](p,path);assert z['reflections']==8
 for A,B in zip(path[:-2],path[1:-1]):assert not ns['on'](A,B,path[-1])
 rows.append({'c':str(c),'ws':str(ws),'a':str(a),'b':str(b),**z})
out={'status':'PRESCRIBED_PROTECTED_EIGHT_ALL_WALL_PASS','discovery':False,'rows':rows,'validator_reuse':str(src),'whole_goal_complete':False};(P/'critical-quarter-protected-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
