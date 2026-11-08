"""R37 focused exact first-candidate search on FOUR prescribed base inputs only."""
from pathlib import Path
from fractions import Fraction as Q
from datetime import datetime,timezone
from math import gcd
import importlib.util,json,signal,hashlib
R=Path(__file__).resolve().parent
end=datetime.fromisoformat(json.loads((R/'c1-critical-family-effort.json').read_text())['deadline_utc'])
signal.setitimer(signal.ITIMER_REAL,max(.001,(end-datetime.now(timezone.utc)).total_seconds()))
def deadline():assert datetime.now(timezone.utc)<end
sp=importlib.util.spec_from_file_location('own',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
def polygon(h):return list(map(lambda z:tuple(map(Q,z)),[(0,0),(1,0),(1,h),(2,h),(2,h+2),(1,h+2),(1,h+4),(2,h+4),(2,h+6),(1,h+6),(1,2*h+4),(0,2*h+4),(0,2*h+3),(-1,2*h+3),(-1,2*h+1),(0,2*h+1),(0,3),(-1,3),(-1,1),(0,1)]))
def trace(V,S,T,velocity):
 p=S;v=velocity;path=[p];seen=set()
 for _ in range(3000):
  deadline();events=[]
  for i,(a,b) in enumerate(g.edges(V)):
   e=g.vec(a,b);den=g.det(v,e)
   if not den:continue
   t=Q(g.det(g.vec(p,a),e),den);r=Q(g.det(g.vec(p,a),v),den)
   if t>0 and 0<=r<=1:events.append((t,i,r))
  if not events:return None,'no_next_wall'
  dt=min(x[0] for x in events);hit=[x for x in events if x[0]==dt]
  tt=Q(T[0]-p[0],v[0]) if v[0] else Q(T[1]-p[1],v[1])
  if tt>0 and p[0]+tt*v[0]==T[0] and p[1]+tt*v[1]==T[1] and tt<dt:
   path.append(T);return path,'actual_target'
  if len(hit)!=1 or hit[0][2] in(0,1):return None,'actual_corner'
  p=tuple(p[k]+dt*v[k] for k in(0,1));path.append(p);a,b=g.edges(V)[hit[0][1]]
  v=(-v[0],v[1]) if a[0]==b[0] else(v[0],-v[1]);state=(p,v)
  if state in seen:return None,'periodic_without_target'
  seen.add(state)
 return None,'direction_event_cap_UNDECIDED'
if __name__=='__main__':
 rows=[]
 for h in(5,7,9,11):
  deadline();V=polygon(h);g.simple(V);assert len(V)==20
  area=abs(sum(g.det(a,b) for a,b in g.edges(V)))/2;assert area==2*h+12
  S=(Q(0),Q(2));T=(Q(0),Q(2*h+2));A=[(Q(x),Q(y)) for x in(0,2) for y in range(0,2*h+5,2) if g.location(V,(x,y))==1];assert set(A)=={S,T}
  trials=[];found=None
  for p in range(1,36):
   if found:break
   for q in(1,3):
    if gcd(p,q)!=1:continue
    if found:break
    for sx,sy in((-1,1),(1,1),(-1,-1),(1,-1)):
     v=(Q(sx*p),Q(sy*q));path,why=trace(V,S,T,v);trials.append({'velocity':v,'result':why})
     if path:
      result=g.path_check(V,path);assert not any(g.on(a,b,T) for a,b in zip(path[:-2],path[1:-1]))
      found={'velocity':v,'path':path,**result};break
  rows.append({'h':h,'polygon':V,'source':S,'target':T,'area':area,'actual_A_count':2,'first_path':found,'trials':trials,'status':'FIRST_ACTUAL_PATH_VERIFIED' if found else'UNDECIDED_PACK_EXHAUSTED'})
  if not found:break
 out={'status':'ALL_FOUR_PRESCRIBED_FIRST_ACTUAL_PATHS_VERIFIED' if len(rows)==4 and all(r['first_path'] for r in rows) else'INCOMPLETE_BASE_PACK_NO_DARKNESS_INFERRED','rows':rows,'whole_goal_complete':False,'discovery':True,'original_deadline':end.isoformat(),'finished_utc':datetime.now(timezone.utc).isoformat(),'source_sha256':{'resumed-exact-check.py':hashlib.sha256((R/'resumed-exact-check.py').read_bytes()).hexdigest()}}
 deadline();(R/'c1-critical-family-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in('rows','source_sha256')}));print(json.dumps([{'h':r['h'],'trials':len(r['trials']),'first_path':{k:v for k,v in r['first_path'].items() if k!='path'} if r['first_path'] else None} for r in rows],default=str))
