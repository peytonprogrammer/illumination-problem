"""Independent exact signed-target chart and actual first-hit controls for A58 final."""
from pathlib import Path
from fractions import Fraction as Q
import ast,importlib.util,json,hashlib
R=Path(__file__).resolve().parent;P=R.parent/'construction'
s=importlib.util.spec_from_file_location('g',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
ns={'Q':Q,'g':g}
for f,fun in [('tooth-free-core-independent-check.py','trace'),('robust-portal-lift-check.py','match')]:
 tree=ast.parse((R/f).read_text());exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==fun],type_ignores=[]),'own '+fun,'exec'),ns)
def guards(kind,h,d,m,sg,K):
 G=2*h+4 if kind=='A0' else 2*h+d+4;sec=h+4 if kind=='A0' else h+d+2;t=2*h+2
 assert K>0 and (2+K-sg*t)%(2*G)==0
 physical=[g.fold(2+Q(j*K,2*m),Q(G)) for j in range(1,2*m)]
 for j,y in enumerate(physical,1):
  gaps=[(0,h),(h+2,sec),(sec+2,G)] if j%2 else [(0,1),(3,t-1),(t+1,G)]
  assert any(y-a>=1 and b-y>=1 for a,b in gaps),(kind,h,d,m,sg,K,j,y,gaps)
 return G,sec,physical
def run(kind,h,d,m,sg,K,c,ds,dt):
 G,sec,physical=guards(kind,h,d,m,sg,K);c,ds,dt=map(Q,[c,ds,dt]);tau,n,delta,steps,bounds=ns['match'](2*m*c,K,1,1,ds,dt)
 ws,wt=ds+Q(1,163),dt+Q(5,167);a,b=Q(100043),Q(1,173);t=2*h+2
 V=[(0,0),(c,0),(c,1),(c+ws,1),(c+ws,3),(c,3),(c,t-1),(c+wt,t-1),(c+wt,t+1),(c,t+1),(c,G),(0,G),(0,sec+2),(-b,sec+2),(-b,sec),(0,sec),(0,h+2),(-a,h+2),(-a,h),(0,h)]
 V=[tuple(map(Q,z)) for z in V];g.simple(V)
 expected=sum(n)+2*m-1+(2+K)//G
 path,_=ns['trace'](V,(c+ds,Q(2)),(c+dt,Q(t)),(Q(-1),(-1)**n[0]*tau),expected)
 out=g.path_check(V,path)
 return {'kind':kind,'h':h,'d':d,'m':m,'sigma':sg,'K':K,'c':c,'Ds':ds,'Dt':dt,'tau':tau,'indices':n,'residuals':delta,'nominal_physical':physical,**out}
table=[]
for line in (P/'low-band-robust-core-proof.md').read_text().splitlines():
 if line.startswith('|'):
  f=line.split('|')[1:-1]
  if len(f)==5 and f[0].isdigit():
   d,m,sg,K=map(int,f[:4]);side=[Q(x) for x in f[4].split(',')];actual=guards('A1',3,d,m,sg,K)[2];assert actual==side;table.append((d,m,sg,K))
assert len(table)==9 and {d for d,_,_,_ in table}=={3,4,5,8,9,11,12,13,14}
profiles=[('A1',3,d,m,sg,K) for d,m,sg,K in table]+[('A0',4,0,2,-1,84)]
for h,d in [(4,2),(4,3),(5,3),(6,3),(100,50),(101,51),(4,1000)]:
 G=2*h+d+4;profiles.append(('A1',h,d,2,-1,8*G-2*h-4))
rows=[]
for pp in profiles:
 for c,ds,dt in [(Q(2,5),Q(1,2),Q(7,3)),(Q(11),Q(0),Q(5,2)),(Q(121),Q(2),Q(0))]:rows.append(run(*pp,c,ds,dt))
arith=0
for h in range(4,101):
 for d in range(1,101):
  if 2*d>=h:
   G=2*h+d+4;guards('A1',h,d,2,-1,8*G-2*h-4);arith+=1
  else:assert h>=d+2
remaining=[]
for h in range(3,101):
 for d in range(1,101):
  covered=h>=4 or d==1 or d>=15 or d in {x[0] for x in table}
  if not covered:remaining.append((h,d))
assert remaining==[(3,2),(3,6),(3,7),(3,10)]
pins=json.loads((P/'low-band-robust-core-review-request.json').read_text())['source_sha256']
for f,h in pins.items():assert hashlib.sha256((P/f).read_bytes()).hexdigest()==h
out={'status':'A58_SIGNED_TARGET_FULL_GUARDS_AND_INDEPENDENT_FIRST_HIT_PASS','whole_goal_complete':False,'author_optical_code_executed':False,'literal_table_rows':len(table),'generic_arithmetic_controls':arith,'actual_paths':len(rows),'reflections':sum(z['reflections'] for z in rows),'wall_leg_guards':sum(z['wall_leg_guards'] for z in rows),'A1_remaining':remaining,'A0_remaining':[3,5],'source_pins':pins,'rows':rows}
(R/'signed-low-band-independent-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print({k:v for k,v in out.items() if k not in ['rows','source_pins']})
