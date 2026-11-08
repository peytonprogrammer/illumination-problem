from pathlib import Path
from fractions import Fraction as F
from datetime import datetime,timezone
import json,math,signal
P=Path(__file__).resolve().parent
E=json.loads((P/'c1-q2-effort.json').read_text());end=datetime.fromisoformat(E['deadline'])
signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('original aggregate deadline')))
signal.setitimer(signal.ITIMER_REAL,max(0.001,(end-datetime.now(timezone.utc)).total_seconds()))
S=(0,2);T=(0,8)
# The artificial ceiling is a rejection boundary, never an allowed mirror.
V=[(0,0),(1,0),(1,3),(2,3),(2,5),(1,5),(1,100),(0,100),(0,9),(-1,9),(-1,7),(0,7),(0,3),(-1,3),(-1,1),(0,1)]
def sub(a,b):return a[0]-b[0],a[1]-b[1]
def det(a,b):return a[0]*b[1]-a[1]*b[0]
def trace(v):
 p=tuple(map(F,S));path=[p];walls=[];seen=set();guards=0;v0=v
 for _ in range(1000):
  if datetime.now(timezone.utc)>=end:raise TimeoutError()
  if (p,v) in seen:return None
  seen.add((p,v));events=[]
  for i,a in enumerate(V):
   b=V[(i+1)%len(V)];e=sub(b,a);den=det(v,e);guards+=1
   if den:
    t=F(det(sub(a,p),e),den);z=F(det(sub(a,p),v),den)
    if t>0 and 0<=z<=1:events.append((t,i,z))
  if not events:return None
  first=min(e[0] for e in events)
  t=F(T[0]-p[0],v[0])
  if 0<t<first and (p[0]+t*v[0],p[1]+t*v[1])==T:
   path.append(tuple(map(F,T)));return {'direction':v0,'path':path,'walls':walls,'reflections':len(walls),'all_wall_leg_guards':guards,'maxY':max(q[1] for q in path)}
  hits=[e for e in events if e[0]==first]
  if len(hits)!=1 or not 0<hits[0][2]<1:return None
  _,i,z=hits[0];a=V[i];b=V[(i+1)%len(V)]
  if a[1]==b[1]==100:return None
  p=(p[0]+first*v[0],p[1]+first*v[1]);path.append(p);walls.append(i)
  v=(-v[0],v[1]) if a[0]==b[0] else(v[0],-v[1])
 return None
result=None;trials=0;status='FINITE_PACK_UNRESOLVED_NO_DARKNESS'
try:
 for m in range(2,51):
  for a in range(1,26):
   b=m-a
   if not 1<=b<=25 or math.gcd(a,b)!=1:continue
   for sx in(-1,1):
    for sy in(-1,1):
     trials+=1;result=trace((sx*a,sy*b))
     if result:break
    if result:break
   if result:break
  if result:break
 if result:status='FIRST_LOCAL_ACTUAL_PATH_VERIFIED'
except TimeoutError:status='ORIGINAL_DEADLINE_UNDECIDED'
finally:
 signal.setitimer(signal.ITIMER_REAL,0)
 out={'status':status,'trials':trials,'polygon':V,'S':S,'T':T,'actual':result,'original_deadline':E['deadline'],'finished_utc':datetime.now(timezone.utc).isoformat(),'whole_goal_complete':False}
 (P/'c1-q2-cap-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps(out,default=str),flush=True)
