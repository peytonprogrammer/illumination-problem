from pathlib import Path
from fractions import Fraction as F
from datetime import datetime,timezone
import math,json,signal
R=Path(__file__).resolve().parent;E=json.loads((R/'tooth-return-grid-effort.json').read_text());end=datetime.fromisoformat(E['deadline']);remaining=(end-datetime.now(timezone.utc)).total_seconds();assert remaining>0
signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('original aggregate deadline')));signal.setitimer(signal.ITIMER_REAL,remaining)
def det(a,b):return a[0]*b[1]-a[1]*b[0]
def sub(a,b):return a[0]-b[0],a[1]-b[1]
def trace(V,S,T,v):
 edges=list(zip(V,V[1:]+V[:1]));p=tuple(map(F,S));path=[p];walls=[];seen=set();guards=0
 for _ in range(1000):
  if datetime.now(timezone.utc)>=end:raise TimeoutError('original aggregate deadline')
  state=(p,v)
  if state in seen:return None
  seen.add(state);events=[]
  for i,(a,b) in enumerate(edges):
   guards+=1;e=sub(b,a);den=det(v,e)
   if not den:continue
   tt=F(det(sub(a,p),e),den);z=F(det(sub(a,p),v),den)
   if tt>0 and 0<=z<=1:events.append((tt,i,z))
  first=min(e[0] for e in events);dt=F(T[0]-p[0],v[0]) if v[0] else F(T[1]-p[1],v[1])
  if 0<dt<first and tuple(p[k]+dt*v[k] for k in(0,1))==T:return {'path':path+[tuple(map(F,T))],'walls':walls,'reflections':len(walls),'all_wall_leg_guards':guards}
  hits=[e for e in events if e[0]==first]
  if len(hits)!=1 or not 0<hits[0][2]<1:return None
  _,i,_=hits[0];p=tuple(p[k]+first*v[k] for k in(0,1))
  if p[1]==10 or(p[0]==0 and p[1]>=8):return None
  path.append(p);walls.append(i);a,b=edges[i];v=(-v[0],v[1]) if a[0]==b[0] else(v[0],-v[1])
 return None
rows=[]
try:
 for D,a in ((1,2),(2,1)):
  V=[(0,0),(1,0),(1,1),(D+2,1),(D+2,3),(1,3),(1,7),(D+2,7),(D+2,9),(1,9),(1,10),(0,10),(0,5),(-a,5),(-a,3),(0,3)];S=(1+D,2);T=(1+D,8);result=None;tried=0
  for total in range(2,51):
   for p in range(1,26):
    q=total-p
    if not 1<=q<=25 or math.gcd(p,q)!=1:continue
    for sx in(-1,1):
     for sy in(-1,1):
      tried+=1;v=(sx*p,sy*q);result=trace(V,S,T,v)
      if result:result.update(direction=v);break
     if result:break
    if result:break
   if result:break
  rows.append({'status':'ACTUAL_LOCAL_CAP_PATH' if result else'NO_PATH_IN_PRESCRIBED_PACK','D':D,'a':a,'polygon':V,'S':S,'T':T,'actual':result,'directions_tried':tried});print(json.dumps({k:v for k,v in rows[-1].items() if k not in('polygon','actual')}),flush=True)
except TimeoutError:rows.append({'status':'ORIGINAL_DEADLINE_UNDECIDED'})
finally:
 signal.setitimer(signal.ITIMER_REAL,0);out={'status':'ALL_TWO_LOCAL_CAP_PATHS_PASS' if len(rows)==2 and all(z['status']=='ACTUAL_LOCAL_CAP_PATH' for z in rows) else'INCOMPLETE_NO_DARKNESS','rows':rows,'discovery':True,'original_deadline':E['deadline'],'finished_utc':datetime.now(timezone.utc).isoformat(),'whole_goal_complete':False};(R/'tooth-return-grid-cap.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(out['status'])
