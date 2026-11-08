"""A64 independent fixed core seam charts and original FIRST-HIT rays."""
from pathlib import Path
from fractions import Fraction as Q
import ast,importlib.util,json,hashlib
R=Path(__file__).resolve().parent;P=R.parent/'construction'
s=importlib.util.spec_from_file_location('g',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
ns={'Q':Q,'g':g};tree=ast.parse((R/'tooth-free-core-independent-check.py').read_text());exec(compile(ast.Module(body=[z for z in tree.body if isinstance(z,ast.FunctionDef) and z.name=='trace'],type_ignores=[]),'own firsthit','exec'),ns)
table={}
for line in (P/'critical-seam-core-proof.md').read_text().splitlines():
 if line.startswith('|'):
  f=line.split('|')[1:-1]
  if len(f)==2 and f[0].isdigit():table[int(f[0])]=[Q(x) for x in f[1].split(',')]
assert set(table)=={7,10};rows=[]
for d,K in [(7,108),(10,46)]:
 G=d+10;side=[g.fold(2+Q(j*K,8),Q(G)) for j in range(1,8)];assert side==table[d]
 assert (2+K)%(2*G)==8 and all(0<y<G for y in side)
 for j,y in enumerate(side,1):
  mouths=[(3,5),(d+5,d+7)] if j%2 else [(1,3),(7,9)]
  assert all(not a<=y<=b for a,b in mouths)
 for c,ws,wt,a,b in [(Q(1,31),Q(1,307),Q(100333),Q(1,311),Q(100343)),(Q(7,3),Q(100357),Q(1,313),Q(100361),Q(1,317)),(Q(100363),Q(1,331),Q(1,337),Q(1,347),Q(1,349))]:
  V=[(0,0),(c,0),(c,1),(c+ws,1),(c+ws,3),(c,3),(c,7),(c+wt,7),(c+wt,9),(c,9),(c,G),(0,G),(0,d+7),(-b,d+7),(-b,d+5),(0,d+5),(0,5),(-a,5),(-a,3),(0,3)];V=[tuple(map(Q,z)) for z in V];g.simple(V)
  path,_=ns['trace'](V,(c,Q(2)),(c,Q(8)),(Q(-1),Q(K,8*c)),7+(2+K)//G);z=g.path_check(V,path);rows.append({'d':d,'c':c,'K':K,**z})
pins=json.loads((P/'critical-seam-core-review-request.json').read_text())['source_sha256']
for f,h in pins.items():assert hashlib.sha256((P/f).read_bytes()).hexdigest()==h
out={'status':'A64_INDEPENDENT_EXACT_SIDE_TABLE_AND_FIRST_HIT_PASS','whole_goal_complete':False,'author_code_executed':False,'actual_paths':len(rows),'reflections':sum(z['reflections'] for z in rows),'wall_leg_guards':sum(z['wall_leg_guards'] for z in rows),'side_table':table,'source_pins':pins,'rows':rows}
(R/'critical-seam-core-independent-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print({k:v for k,v in out.items() if k not in ['rows','source_pins','side_table']})
