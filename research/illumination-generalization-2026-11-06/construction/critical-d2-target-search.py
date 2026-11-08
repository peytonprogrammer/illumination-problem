"""One protected upper-tooth repair search, exact original-wall first hits."""
from pathlib import Path
from fractions import Fraction as Q
from datetime import datetime,timezone
import json,math,signal,ast
P=Path(__file__).resolve().parent;E=json.loads((P/'critical-d2-target-effort.json').read_text());end=datetime.fromisoformat(E['deadline']);left=(end-datetime.now(timezone.utc)).total_seconds();assert left>0;signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('original deadline')));signal.setitimer(signal.ITIMER_REAL,left)
c=Q(3);ws=Q(3);wt=Q(1);a=b=Q(1);poly=[(0,0),(c,0),(c,1),(c+ws,1),(c+ws,3),(c,3),(c,7),(c+wt,7),(c+wt,9),(c,9),(c,12),(0,12),(0,9),(-b,9),(-b,7),(0,7),(0,5),(-a,5),(-a,3),(0,3)];edges=list(zip(poly,poly[1:]+poly[:1]));S=(c,Q(2));T=(c,Q(8))
base=ast.parse((P/'critical-quarter-protected-search.py').read_text());body=[n for n in base.body if isinstance(n,ast.FunctionDef) and n.name in {'sub','det','trace'}];code=ast.unparse(ast.Module(body=body,type_ignores=[])).replace('if p[0] < 0:', 'if p[0] < 0 or (p[0] > c and p[1] <= 3):');exec(compile(code,'own-prescribed-trace','exec'),globals());ans=None;count=0;status='BOUNDED_UNDECIDED'
try:
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
  if ans:status='EXACT_PROTECTED_UPPER_CANDIDATE_FOUND';break
except TimeoutError:status='STOPPED_AT_ORIGINAL_AGGREGATE_DEADLINE'
finally:
 signal.setitimer(signal.ITIMER_REAL,0);out={'status':status,'directions_tried':count,'candidate':ans,'polygon':poly,'discovery':True,'deadline':E['deadline'],'darkness_claimed':False,'whole_goal_complete':False};(P/'critical-d2-target-search.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['candidate','polygon']},default=str))
