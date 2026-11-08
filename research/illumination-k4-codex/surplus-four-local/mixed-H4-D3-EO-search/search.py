"""Authorized ONE fixed-room bounded exact path discovery, 300s maximum."""
from pathlib import Path
from fractions import Fraction as F
from math import gcd
from collections import defaultdict,Counter
import time,json,sys,hashlib,signal,ast
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
sys.path.insert(0,str(ROOT/'triangle-composition/inputs'))
import illumination_geometry as g
RAYS=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
CENTERS={'L':(-2,0),'B':(0,-2),'D':(2,-2),'R':(4,0),'E':(4,2),'Tc':(2,4),'N':(0,2)}
def fan(a,ss):return {tuple(sorted((a,(a[0]+RAYS[i%8][0],a[1]+RAYS[i%8][1]),(a[0]+RAYS[(i+1)%8][0],a[1]+RAYS[(i+1)%8][1])))) for i in ss}
H=set().union(*(fan(a,range(8)) for a in [(0,0),(2,0),(2,2)]))
spec={'L':[0],'E':[4,5],'B':[7,0,1,2],'Tc':[],'N':[7],'D':[3],'R':[3]}
room=H|set().union(*(fan(CENTERS[k],ss) for k,ss in spec.items()))
S=(0,0);T=(2,2)
geo=g.check({'triangles':sorted(room),'marked':[S,T],'require_simple':True},strict=False)
if not (geo['simple_polygon'] and geo['walls']==20 and set(map(tuple,geo['interior_A']))=={S,(2,0),T}):
 (HERE/'room.json').write_text(json.dumps({'status':'GEOMETRY_REJECTED_NO_SEARCH','spec':spec,'geometry':geo},indent=2)+'\n')
 print('GEOMETRY REJECTED: no search, no replacement room.',flush=True)
 sys.exit(0)
owners=g.owners_of(sorted(room));atomic=[e for e,own in owners.items() if len(own)==1]
adj=defaultdict(list)
for a,b in atomic:adj[a].append(b);adj[b].append(a)
assert all(len(v)==2 for v in adj.values())
cycle=[min(adj)];prev=None;current=cycle[0]
while True:
 nxt=next(p for p in adj[current] if p!=prev)
 if nxt==cycle[0]:break
 assert nxt not in cycle
 cycle.append(nxt);prev,current=current,nxt
assert len(cycle)==len(atomic)
def sub(a,b):return(a[0]-b[0],a[1]-b[1])
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def dot(a,b):return a[0]*b[0]+a[1]*b[1]
V=[p for i,p in enumerate(cycle) if cross(sub(p,cycle[i-1]),sub(cycle[(i+1)%len(cycle)],p))]
if sum(cross(a,b) for a,b in zip(V,V[1:]+V[:1]))<0:V.reverse()
assert len(V)==20
full_nonA=[p for p in geo['transparent_vertices'] if str(p) not in geo['sectors']]
smooth_nonA=[p for p in geo['transparent_vertices'] if geo['sectors'].get(str(p))==[4]]
J=len(full_nonA);sN=len(smooth_nonA)
Q=sum(3 if m[0]==4 else m[0] for p,m in geo['sectors'].items() if g.label(ast.literal_eval(p))=='A')
assert (J,sN,Q,J+sN,Q+sN-8)==(3,3,9,6,4),(J,sN,Q)
frozen={'description':'ONLY fixed mixed H+B7012+D3+E45+L0+N7+R3,Tcempty','spec':spec,'triangles':sorted(room),'vertices':V,'marked':[S,T],'geometry':geo,'ledger':{'W':20,'I':3,'J':J,'s_N':sN,'Q':Q,'k':J+sN,'Delta':Q+sN-8}}
(HERE/'room.json').write_text(json.dumps(frozen,indent=2)+'\n')
room_hash=hashlib.sha256((HERE/'room.json').read_bytes()).hexdigest()
MAX_COMPONENT=512;MAX_REFLECTIONS=400;LIMIT_SECONDS=300
edges=[]
for a,b in zip(V,V[1:]+V[:1]):
 w=sub(b,a);normal=(-w[1],w[0]);div=gcd(abs(normal[0]),abs(normal[1]));normal=tuple(x//div for x in normal)
 edges.append((a,b,w,normal,dot(normal,a),dot(normal,normal)))
def ratio(n,d):return(n,d) if d>0 else(-n,-d)
def less(a,b):return a[0]*b[1]<b[0]*a[1]
def reflect_int(p,n,c,norm2,point):
 top=2*(dot(n,p)-(c if point else 0));assert top%norm2==0
 k=top//norm2;return(p[0]-k*n[0],p[1]-k*n[1])
class BudgetExpired(Exception):pass
start=time.monotonic();deadline=start+LIMIT_SECONDS
signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(BudgetExpired()))
signal.setitimer(signal.ITIMER_REAL,LIMIT_SECONDS)
counters=Counter();found=None
print('FIXED ROOM:',frozen['description'],'ledger',frozen['ledger'],flush=True)
print('BOUNDS: primitive integer directions maxcomponent512, all signs; <=400 reflections; hard300 seconds; stopfirstpath.',flush=True)
def trace(v0):
 O=S;v=v0;clock=(0,1);contacts=[];walls=[]
 for reflection_count in range(MAX_REFLECTIONS+1):
  if time.monotonic()>=deadline:raise BudgetExpired
  best=None;best_wall=None;at_corner=False
  for j,(a,b,w,n,c,norm2) in enumerate(edges):
   den=cross(v,w)
   if not den:continue
   delta=sub(a,O);tn=cross(delta,w);un=cross(delta,v)
   if den<0:den=-den;tn=-tn;un=-un
   if not 0<=un<=den:continue
   tau=(tn,den)
   if not less(clock,tau):continue
   if best is None or less(tau,best):best=tau;best_wall=j;at_corner=(un==0 or un==den)
   elif not less(best,tau):at_corner=True
  assert best is not None,('no boundary',O,v,clock)
  target_delta=sub(T,O)
  if cross(target_delta,v)==0:
   target=ratio(target_delta[0],v[0]) if v[0] else ratio(target_delta[1],v[1])
   if less(clock,target) and less(target,best):
    return {'initial_direction':v0,'reflections':len(contacts),'contacts':contacts,'walls':walls,'terminal_time':target,'final_reflected_source':O,'final_velocity':v},'found'
  if at_corner:return None,'corner'
  if reflection_count==MAX_REFLECTIONS:return None,'reflection_bound'
  contacts.append((O,v,best));walls.append(best_wall)
  a,b,w,n,c,norm2=edges[best_wall]
  O=reflect_int(O,n,c,norm2,True);v=reflect_int(v,n,c,norm2,False);clock=best
 return None,'reflection_bound'
def directions():
 for m in range(1,MAX_COMPONENT+1):
  for q in range(m+1):
   if gcd(m,q)!=1:continue
   for x,y in sorted({(sx*a,sy*b) for a,b in [(m,q),(q,m)] for sx in [-1,1] for sy in [-1,1]}):
    yield(x,y)
status='EXHAUSTED_FINITE_BOUNDS'
try:
 for vector in directions():
  candidate,why=trace(vector);counters['directions']+=1;counters[why]+=1
  if candidate is not None:found=candidate;status='FOUND_EXACT_PATH_PENDING_INDEPENDENT_VERIFICATION';break
  if counters['directions']%10000==0:print('PROGRESS',dict(counters),'seconds',round(time.monotonic()-start,3),flush=True)
except BudgetExpired:status='TIME_LIMIT_NO_PATH_INCONCLUSIVE'
finally:signal.setitimer(signal.ITIMER_REAL,0)
result={'status':status,'seconds':time.monotonic()-start,'bounds':{'max_primitive_component':MAX_COMPONENT,'max_reflections':MAX_REFLECTIONS,'hard_seconds':LIMIT_SECONDS},'stats':dict(counters),'room_sha256':room_hash,'search_source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'ONE fixed room only; bounded discovery authorized by Daniel. No darkness conclusion from failure.'}
if found:
 path=[(F(0),F(0))]
 for O,v,(num,den) in found.pop('contacts'):
  path.append(tuple(F(O[k]*den+v[k]*num,den) for k in range(2)))
 path.append(tuple(map(F,T)))
 found['path']=[[[x.numerator,x.denominator] for x in p] for p in path]
 result['candidate']=found
(HERE/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print('RESULT',status,'directions',counters['directions'],'seconds',round(result['seconds'],3),flush=True)
if found:print('DIRECTION',found['initial_direction'],'REFLECTIONS',found['reflections'],flush=True)
