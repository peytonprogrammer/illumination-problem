"""One named uniform-width-fiber discovery. Exact finite actual-wall traces."""
from fractions import Fraction as Q
from pathlib import Path
from datetime import datetime,timezone
import json,signal,math,time
P=Path(__file__).resolve().parent;effort=json.loads((P/'critical-quarter-protected-effort.json').read_text());end=datetime.fromisoformat(effort['deadline']);remaining=(end-datetime.now(timezone.utc)).total_seconds();assert remaining>0
signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('ORIGINALaggregate deadline')));signal.setitimer(signal.ITIMER_REAL,remaining)
poly=[(0,0),(4,0),(4,1),(5,1),(5,3),(4,3),(4,7),(8,7),(8,9),(4,9),(4,10),(0,10),(0,9),(-1,9),(-1,7),(0,7),(0,5),(-1,5),(-1,3),(0,3)];edges=list(zip(poly,poly[1:]+poly[:1]));S=(Q(4),Q(2));T=(Q(4),Q(8))
def sub(a,b):return (a[0]-b[0],a[1]-b[1])
def det(a,b):return a[0]*b[1]-a[1]*b[0]
def trace(v):
 p=S;path=[p];walls=[];seen=set()
 for _ in range(512):
  if datetime.now(timezone.utc)>=end:raise TimeoutError
  if (p,v) in seen:return None
  seen.add((p,v));events=[]
  for k,(a,b) in enumerate(edges):
   e=sub(b,a);den=det(v,e)
   if not den:continue
   t=det(sub(a,p),e)/den;r=det(sub(a,p),v)/den
   if t>0 and 0<=r<=1:events.append((t,k,r))
  if not events:return None
  first=min(z[0] for z in events);dt=(T[0]-p[0])/v[0]
  if 0<dt<first and (p[0]+dt*v[0],p[1]+dt*v[1])==T:return {'initial_direction':pathv,'path':path+[T],'walls':walls,'reflections':len(walls)}
  hits=[z for z in events if z[0]==first]
  if len(hits)!=1 or hits[0][2] in (0,1):return None
  p=(p[0]+first*v[0],p[1]+first*v[1])
  if p[0]<0:return None
  walls.append(hits[0][1]);path.append(p);a,b=edges[hits[0][1]];v=(-v[0],v[1]) if a[0]==b[0] else(v[0],-v[1])
 return None
answer=None;count=0;status='BOUNDED_SEARCH_UNDECIDED'
try:
 for L in range(2,81):
  for vx in range(1,L):
   vy=L-vx
   if math.gcd(vx,vy)!=1:continue
   for sx in (-1,1):
    for sy in (-1,1):
     pathv=(sx*vx,sy*vy);count+=1;answer=trace(pathv)
     if answer:break
    if answer:break
   if answer:break
  if answer:status='EXACT_PROTECTED_CANDIDATE_FOUND';break
except TimeoutError:status='STOPPED_AT_ORIGINAL_DEADLINE'
finally:
 signal.setitimer(signal.ITIMER_REAL,0)
 out={'status':status,'directions_tried':count,'candidate':answer,'polygon':poly,'source':S,'target':T,'discovery':True,'opposite_widths_not_entered':bool(answer),'deadline':effort['deadline'],'finished_utc':datetime.now(timezone.utc).isoformat(),'darkness_claimed':False,'whole_goal_complete':False};(P/'critical-quarter-protected-search.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['candidate','polygon']},default=str))
