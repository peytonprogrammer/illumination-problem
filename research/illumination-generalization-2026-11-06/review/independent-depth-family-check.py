"""A58 prescribed independent all-wall first-hit, cutoff and complement checks."""
from pathlib import Path
from fractions import Fraction as Q
import ast,importlib.util,json,hashlib
R=Path(__file__).resolve().parent;P=R.parent/'construction'
s=importlib.util.spec_from_file_location('g',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
ns={'Q':Q,'g':g}
for f,func in [('tooth-free-core-independent-check.py','trace'),('robust-portal-lift-check.py','match')]:
 tree=ast.parse((R/f).read_text());exec(compile(ast.Module(body=[z for z in tree.body if isinstance(z,ast.FunctionDef) and z.name==func],type_ignores=[]),'own '+func,'exec'),ns)
def run(kind,h,d,c,ds,dt,mode,m=2):
 c,ds,dt=map(Q,(c,ds,dt));G=2*h+4 if kind=='A0' else 2*h+d+4;second=h+4 if kind=='A0' else h+d+2
 K=2*h+2*G if mode=='end' else 2*h;L0=4*c if mode=='end' else 2*m*c
 tau,n,delta,steps,bounds=ns['match'](L0,K,1,1,ds,dt)
 ws,wt=ds+Q(1,149),dt+Q(2,151);a,b=Q(100019),Q(1,157)
 V=[(0,0),(c,0),(c,1),(c+ws,1),(c+ws,3),(c,3),(c,2*h+1),(c+wt,2*h+1),(c+wt,2*h+3),(c,2*h+3),(c,G),(0,G),(0,second+2),(-b,second+2),(-b,second),(0,second),(0,h+2),(-a,h+2),(-a,h),(0,h)]
 V=[tuple(map(Q,z)) for z in V];g.simple(V)
 expected=sum(n)+(5 if mode=='end' else 2*m-1)
 path,_=ns['trace'](V,(c+ds,Q(2)),(c+dt,Q(2*h+2)),(Q(-1),(-1)**n[0]*tau),expected)
 out=g.path_check(V,path)
 return {'kind':kind,'h':h,'d':d,'c':c,'Ds':ds,'Dt':dt,'mode':mode,'m':m,'indices':n,'delta':delta,'path':path,**out}
shapes=[('A0',6,0,'end',2),('A0',10,0,'end',2),('A0',1000,0,'end',2),('A1',3,1,'end',2),('A1',4,2,'end',2),('A1',5,3,'end',2),('A1',6,4,'end',2),('A1',19,17,'end',2),('A1',3,15,'end',2),('A1',4,18,'end',2),('A1',5,21,'end',2),('A1',3,1000,'end',2),('A1',6,5,'direct',2),('A1',6,1000,'direct',2),('A0',10,0,'direct',2),('A1',15,8,'direct',4),('A1',21,8,'direct',4),('A1',100,50,'direct',4),('A1',6,10,'direct',2)]
rows=[]
for kind,h,d,mode,m in shapes:
 for c,ds,dt in [(Q(3,2),Q(0),Q(11,7)),(Q(11),Q(1),Q(3)),(Q(7,3),Q(17,5),Q(29,7)),(Q(121),Q(0),Q(0))]:rows.append(run(kind,h,d,c,ds,dt,mode,m))
old=[];new=[]
for h in range(3,101):
 for d in range(1,101):
  if h>=6 and not(h<=2*d-2 or h>=2*d+6 or d>=8):old.append((h,d))
  accepted=h>=6 or h>=d+2 or d>=3*h+6
  if not accepted:new.append((h,d))
assert set(old)==set((h,d) for d,lo,hi in [(1,6,7),(2,6,9),(3,6,11),(4,7,13),(5,9,15),(6,11,17),(7,13,19)] for h in range(lo,hi+1)) and len(old)==40
assert set(new)==set((h,d) for h,lo,hi in [(3,2,14),(4,3,17),(5,4,20)] for d in range(lo,hi+1)) and len(new)==45
pins={}
for f in ['independent-depth-zigzag-review-request.json','independent-depth-endfold-review-request.json']:
 for rel,h in json.loads((P/f).read_text())['source_sha256'].items():assert hashlib.sha256((P/rel).read_bytes()).hexdigest()==h;pins['../construction/'+rel]=h
out={'status':'A58_BOTH_FULL_FAMILY_INDEPENDENT_FIRST_HIT_PASS','whole_goal_complete':False,'author_optical_code_executed':False,'actual_paths':len(rows),'reflections':sum(z['reflections'] for z in rows),'wall_leg_guards':sum(z['wall_leg_guards'] for z in rows),'old_vertical_complement':old,'new_vertical_complement':new,'source_sha256':pins,'rows':rows}
(R/'independent-depth-family-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print({k:v for k,v in out.items() if k not in ['rows','source_sha256','old_vertical_complement','new_vertical_complement']})
