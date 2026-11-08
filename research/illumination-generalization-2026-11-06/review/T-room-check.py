"""Prescribed exact T-room witness, no search. Writes only its own JSON receipt."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent
V=[(4,0),(5,0),(5,1),(10,1),(10,3),(0,3),(0,1),(4,1)]
V=[tuple(map(F,p)) for p in V]
S=(F(9,2),F(1,2));T=(F(1,2),F(2))
contacts=[(F(311-32*j,78),F(3 if j%2==0 else 1)) for j in range(9)]
path=[S,*contacts,T]
def sub(a,b):return(a[0]-b[0],a[1]-b[1])
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def add(a,d,t):return(a[0]+t*d[0],a[1]+t*d[1])
def inside(p):
 x,y=p
 return (0<x<10 and 1<y<3) or (4<x<5 and 0<y<3)
def strpt(p):return [str(x) for x in p]
checks=0;segments=[]
for i,(p,q) in enumerate(zip(path,path[1:])):
 d=sub(q,p); assert d[0]<0 and d[1]!=0
 assert abs(d[0]/d[1])==F(8,39);checks+=1
 events=[]
 for k,u in enumerate(V):
  v=V[(k+1)%len(V)];e=sub(v,u);det=cross(d,e)
  if det==0:
   assert cross(sub(u,p),d)!=0,'collinear boundary segment'
   continue
  t=cross(sub(u,p),e)/det;w=cross(sub(u,p),d)/det
  if 0<=t<=1 and 0<=w<=1:
   assert w not in (0,1),'actual polygon corner contact'
   assert t in (0,1),'unexpected wall in segment interior'
   point=add(p,d,t)
   assert point in contacts
   assert e[1]==0,'vertical wall contact'
   events.append({'wall':k,'time':str(t),'point':strpt(point)})
   checks+=1
 expected=(i>0)+(i<len(path)-2)
 assert len(events)==expected,(i,events,expected)
 cuts={F(0),F(1)}
 for axis in (0,1):
  if d[axis]:
   for value in {v[axis] for v in V}:
    t=(value-p[axis])/d[axis]
    if 0<t<1:cuts.add(t)
 cuts=sorted(cuts)
 for l,r in zip(cuts,cuts[1:]):
  assert inside(add(p,d,(l+r)/2));checks+=1
 segments.append({'from':strpt(p),'to':strpt(q),'boundary_events':events})
for j,p in enumerate(contacts,1):
 incoming=sub(p,path[j-1]);outgoing=sub(path[j+1],p)
 reflected=(incoming[0],-incoming[1])
 assert cross(reflected,outgoing)==0
 assert sum(x*y for x,y in zip(reflected,outgoing))>0
 assert 0<p[0]<4 and p[1] in (1,3);checks+=1
assert inside(S) and inside(T) and path[-1]==T
first=sub(contacts[0],S)
t=(1-S[1])/first[1];portal=add(S,first,t)
assert portal==(F(343,78),F(1)) and 4<portal[0]<5
t=(4-S[0])/first[0];cut=add(S,first,t)
assert cut==(F(4),F(47,16)) and 1<cut[1]<3
checks+=3
out={'status':'EXACT_PRESCRIBED_T_PATH_PASS','kind':'fixed rational witness verification, not discovery or arbitrary-real proof','reflections':len(contacts),'segments':len(segments),'checks':checks,'S':strpt(S),'T':strpt(T),'portal':strpt(portal),'reflex_support_crossing':strpt(cut),'path':segments,'source_sha256':{p:hashlib.sha256((HERE/p).read_bytes()).hexdigest() for p in ('T-room-theorem.md','T-room-check.py')},'whole_goal_complete':False}
(HERE/'T-room-check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='path'}))
