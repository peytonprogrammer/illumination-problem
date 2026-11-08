"""Two bounded source-ratio probes; same recorded aggregate deadline, exact walls."""
from pathlib import Path
from fractions import Fraction as Q
from datetime import datetime,timezone
import json,math,signal,ast
P=Path(__file__).resolve().parent;E=json.loads((P/'critical-five-source-effort.json').read_text());end=datetime.fromisoformat(E['deadline']);left=(end-datetime.now(timezone.utc)).total_seconds();assert left>0
signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('original deadline')));signal.setitimer(signal.ITIMER_REAL,left)
base=ast.parse((P/'critical-quarter-protected-search.py').read_text());body=[n for n in base.body if isinstance(n,ast.FunctionDef) and n.name in {'sub','det','trace'}];code=ast.unparse(ast.Module(body=body,type_ignores=[])).replace('if p[0] < 0:', 'if p[0] < 0 or (p[0] > c and p[1] >= 11):');exec(compile(code,'own-prescribed-trace','exec'),globals())
rows=[];status='BOUNDED_TWO_FIXTURE_RUN_FINISHED'
def save():
 out={'status':status,'rows':rows,'discovery':True,'deadline':E['deadline'],'darkness_claimed':False,'whole_goal_complete':False};(P/'critical-five-source-search.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
try:
 for c,ws in [(Q(28),Q(5)),(Q(1),Q(1))]:
  # Actual upper-width and opposite-width probes; candidates may use none of them.
  wt=c;a=b=Q(1);poly=[(0,0),(c,0),(c,1),(c+ws,1),(c+ws,3),(c,3),(c,11),(c+wt,11),(c+wt,13),(c,13),(c,14),(0,14),(0,11),(-b,11),(-b,9),(0,9),(0,7),(-a,7),(-a,5),(0,5)];edges=list(zip(poly,poly[1:]+poly[:1]));S=(c,Q(2));T=(c,Q(12));ans=None;count=0
  for L in range(2,129):
   for vx in range(1,L):
    vy=L-vx
    if math.gcd(vx,vy)!=1:continue
    for sx in (-1,1):
     for sy in (-1,1):
      pathv=(sx*vx,sy*vy);count+=1;ans=trace(pathv)
      if ans:break
     if ans:break
    if ans:break
   if ans:break
  row={'source_ratio':str(ws/c),'c':str(c),'directions_tried':count,'candidate':ans,'polygon':poly,'status':'PROTECTED_CANDIDATE_FOUND' if ans else 'BOUNDED_UNDECIDED'};rows.append(row);save();print(json.dumps({k:v for k,v in row.items() if k not in ['candidate','polygon']},default=str),flush=True)
except TimeoutError:
 status='STOPPED_AT_ORIGINAL_AGGREGATE_DEADLINE'
finally:
 signal.setitimer(signal.ITIMER_REAL,0);save()
