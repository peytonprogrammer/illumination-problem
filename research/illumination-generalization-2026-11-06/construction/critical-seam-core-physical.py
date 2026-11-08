"""Prescribed all-wall replay of two fixed core-only seam charts."""
from pathlib import Path
from fractions import Fraction as Q
import ast,json
P=Path(__file__).resolve().parent;src=P.parent/'review/resumed-exact-check.py';ns={'Q':Q};names={'vec','det','dot','edges','on','location','intersect','simple','path_check','fold'};m=ast.parse(src.read_text());exec(compile(ast.Module(body=[n for n in m.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[]),str(src),'exec'),ns);fold=ns['fold'];rows=[]
for d,K in [(7,108),(10,46)]:
 G=d+10
 for c,ws,wt,a,b in [(Q(3,2),Q(1,37),Q(1,43),Q(47,5),Q(1,29)),(Q(11),Q(1001),Q(1,19),Q(1,17),Q(400)),(Q(1000),Q(2,19),Q(12000),Q(7,13),Q(11,23))]:
  poly=[(0,0),(c,0),(c,1),(c+ws,1),(c+ws,3),(c,3),(c,7),(c+wt,7),(c+wt,9),(c,9),(c,G),(0,G),(0,d+7),(-b,d+7),(-b,d+5),(0,d+5),(0,5),(-a,5),(-a,3),(0,3)];tau=Q(K)/(8*c);ev={j*c for j in range(9)}
  for ell in range(1,(2+K)//G+1):ev.add((ell*G-2)/tau)
  path=[(fold(c-z,c),fold(2+tau*z,Q(G))) for z in sorted(ev)];assert path[0]==(c,2) and path[-1]==(c,8);ns['simple'](poly);z=ns['path_check'](poly,path);assert z['reflections']==(13 if d==7 else 9)
  for A,B in zip(path[:-2],path[1:-1]):assert not ns['on'](A,B,path[-1])
  rows.append({'d':d,'K':K,'c':str(c),'ws':str(ws),'wt':str(wt),**z})
out={'status':'PRESCRIBED_ACTUAL_CORE_ONLY_CHARTS_PASS','discovery':False,'rows':rows,'validator_reuse':str(src),'whole_goal_complete':False};(P/'critical-seam-core-physical.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
