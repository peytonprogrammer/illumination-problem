"""Prescribed full-contour validation of the universal core-only four-reflection formula."""
from pathlib import Path
from fractions import Fraction as Q
import ast,json
P=Path(__file__).resolve().parent;src=P.parent/'review/resumed-exact-check.py';ns={'Q':Q};names={'vec','det','dot','edges','on','location','intersect','simple','path_check'};a=ast.parse(src.read_text());exec(compile(ast.Module(body=[n for n in a.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[]),str(src),'exec'),ns)
rows=[]
for c,ws,wt,a,b in [(Q(28),Q(5),Q(28),Q(1),Q(1)),(Q(3,2),Q(1,37),Q(1,43),Q(47,5),Q(1,29)),(Q(11),Q(1001),Q(1,19),Q(1,17),Q(400)),(Q(1000),Q(2,19),Q(12000),Q(7,13),Q(11,23))]:
 p=[(0,0),(c,0),(c,1),(c+ws,1),(c+ws,3),(c,3),(c,11),(c+wt,11),(c+wt,13),(c,13),(c,14),(0,14),(0,11),(-b,11),(-b,9),(0,9),(0,7),(-a,7),(-a,5),(0,5)];path=[(c,Q(2)),(3*c/7,Q(0)),(Q(0),Q(3,2)),(c,Q(5)),(Q(0),Q(17,2)),(c,Q(12))]
 ns['simple'](p);z=ns['path_check'](p,path);assert z['reflections']==4
 for A,B in zip(path[:-2],path[1:-1]):assert not ns['on'](A,B,path[-1])
 rows.append({'c':str(c),'ws':str(ws),'wt':str(wt),'a':str(a),'b':str(b),**z})
out={'status':'PRESCRIBED_CORE_ONLY_FOUR_ALL_WALL_PASS','discovery':False,'rows':rows,'validator_reuse':str(src),'whole_goal_complete':False};(P/'critical-five-source-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
