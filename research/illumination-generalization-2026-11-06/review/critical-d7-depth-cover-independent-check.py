"""A66 prescribed TWO-chart exact interval union and own first-hit controls."""
from fractions import Fraction as Q
from pathlib import Path
import ast,json,hashlib,importlib.util
R=Path(__file__).resolve().parent;P=R.parent/'construction'
s=importlib.util.spec_from_file_location('g',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
ns={'Q':Q,'g':g};t=ast.parse((R/'tooth-free-core-independent-check.py').read_text());exec(compile(ast.Module(body=[n for n in t.body if isinstance(n,ast.FunctionDef) and n.name=='trace'],type_ignores=[]),'own trace','exec'),ns)
ints=[]
for K in [108,244]:
 for n in range(70):
  lo=Q(16*(3*n-1),3*K+4);hi=Q(8*(2*n+1),K-2)
  if lo<2 and hi>0:ints.append((max(Q(0),lo),min(Q(2),hi),lo<0,hi>2,K,n))
merged=[]
for a,b,ac,bc,K,n in sorted(ints):
 if merged and (a<merged[-1][1] or a==merged[-1][1] and (ac or merged[-1][3])):
  if b>merged[-1][1]:merged[-1][1]=b;merged[-1][3]=bc
  elif b==merged[-1][1]:merged[-1][3]|=bc
 else:merged.append([a,b,ac,bc])
assert merged==[[Q(0),Q(28,121),True,False],[Q(11,46),Q(2),False,True]]
assert len(ints)==45
for r in [Q(28,121),Q(11,46),Q(4,17)]:assert not any(a<r<b or r==a and ac or r==b and bc for a,b,ac,bc,_,_ in ints)
rows=[]
for r in [Q(0),Q(1,7),Q(1,4),Q(1),Q(2),Q(3),Q(100,3)]:
 choice=next(((K,n) for K in [108,244] for n in range(1000) if -Q(2,3)<(Q(K,2)*r-8*n)/(4+r)<1),None);assert choice
 K,n=choice;c=Q(5,7);D=c*r;tau=(Q(K,2)+2*n)/(4*c+D)
 V=[tuple(map(Q,z)) for z in [(0,0),(c,0),(c,1),(c+D+Q(1,131),1),(c+D+Q(1,131),3),(c,3),(c,7),(c+D+Q(1,137),7),(c+D+Q(1,137),9),(c,9),(c,17),(0,17),(0,14),(-Q(1,139),14),(-Q(1,139),12),(0,12),(0,5),(-Q(100003),5),(-Q(100003),3),(0,3)]]
 g.simple(V);path,_=ns['trace'](V,(c+D,Q(2)),(c+D,Q(8)),(Q(-1),(-1)**n*tau),2*n+(13 if K==108 else 21));z=g.path_check(V,path);rows.append({'r':str(r),'K':K,'n':n,**z})
req=json.loads((P/'critical-d7-depth-cover-review-request.json').read_text())
for f,h in req['source_sha256'].items():assert hashlib.sha256((P/f).read_bytes()).hexdigest()==h
out={'status':'EXACT_TWO_CHART_PARTIAL_UNION_AND_OWN_PATHS_PASS','whole_goal_complete':False,'author_code_executed':False,'source_sha256':req['source_sha256'],'interval_count':len(ints),'merged':[[str(a),str(b),ac,bc] for a,b,ac,bc in merged],'actual_paths':len(rows),'reflections':sum(z['reflections'] for z in rows),'wall_leg_guards':sum(z['wall_leg_guards'] for z in rows),'rows':rows}
(R/'critical-d7-depth-cover-independent-check.json').write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items() if k not in ['rows','source_sha256']})
