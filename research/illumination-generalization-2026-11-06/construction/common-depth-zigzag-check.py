from pathlib import Path
from fractions import Fraction as F
from math import floor,ceil
import json,hashlib
R=Path(__file__).resolve().parent
E=json.loads((R/'common-depth-zigzag-effort.json').read_text())
from datetime import datetime,timezone
assert datetime.now(timezone.utc)<datetime.fromisoformat(E['deadline'])
def sub(a,b):return a[0]-b[0],a[1]-b[1]
def det(a,b):return a[0]*b[1]-a[1]*b[0]
def dot(a,b):return a[0]*b[0]+a[1]*b[1]
def fold(z):z=z%4;return min(z,4-z)
def prefix(c,D,s,tau,n,delta):
 S=(c+D,F(s))
 if not D:return[S]
 sign=(-1)**n;last=1+sign*tau*D;times=[]
 for j in range(floor(min(F(1),last)/2)-1,ceil(max(F(1),last)/2)+2):
  time=F(2*j-1,sign*tau)
  if 0<time<D:times.append(time)
 times.sort();P=[S]+[(c+D-x,F(s-1)+fold(1+sign*tau*x)) for x in times]+[(c,F(s)+delta)]
 assert len(times)==n and fold(last)==1+delta
 return P
cases=[('A1',5,6,F(1),F(0),F(1),F(2),F(1,2),F(3,2)),('A1',12,6,F(1,2),F(3),F(4),F(7,2),F(3,4),F(7,3)),('A1',13,6,F(3,2),F(5,2),F(3),F(5),F(4,3),F(5,4)),('A0',9,0,F(2,3),F(7,2),F(4),F(9,2),F(2),F(3))]
rows=[]
for name,h,d,c,D,ws,wt,w1,w2 in cases:
 assert ws>D and wt>D
 m=4 if name=='A1' and 2*d<=h<=2*d+4 else 2
 n=floor(D*h/(2*m*c)+F(1,2));tau=F(h+2*n,m*c+D);delta=D*tau-2*n;assert abs(delta)<1 and h==delta+m*c*tau
 G=2*h+(d if name=='A1' else 0)+4;upper=h+d+2 if name=='A1' else h+4
 V=[(0,0),(c,0),(c,1),(c+ws,1),(c+ws,3),(c,3),(c,2*h+1),(c+wt,2*h+1),(c+wt,2*h+3),(c,2*h+3),(c,G),(0,G),(0,upper+2),(-w2,upper+2),(-w2,upper),(0,upper),(0,h+2),(-w1,h+2),(-w1,h),(0,h)]
 V=[tuple(map(F,z)) for z in V];edges=list(zip(V,V[1:]+V[:1]));S=(c+D,F(2));T=(c+D,F(2*h+2));P=prefix(c,D,2,tau,n,delta)
 core=[(F(0) if j%2 else c,F(2)+delta+j*c*tau) for j in range(1,2*m)]
 H=lambda a:(a[0],F(2*h+4)-a[1]);tail=[H(a) for a in reversed(P)]
 path=([S] if D==0 else P[:-1])+core+([T] if D==0 else tail[1:]);assert path[0]==S and path[-1]==T
 velocity=(-1,((-1)**n)*tau);assert det(sub(path[1],S),velocity)==0 and dot(sub(path[1],S),velocity)>0
 guards=0;walls=[]
 for j,(a,b) in enumerate(zip(path,path[1:])):
  v=sub(b,a);hits=[]
  for i,(x,y) in enumerate(edges):
   guards+=1;e=sub(y,x);den=det(v,e)
   if not den:
    if det(sub(x,a),v)==0:
     axis=0 if v[0] else 1;lo,hi=sorted((F(x[axis]-a[axis],v[axis]),F(y[axis]-a[axis],v[axis])));assert max(lo,0)>=min(hi,1)
    continue
   t=F(det(sub(x,a),e),den);z=F(det(sub(x,a),v),den)
   assert not(0<t<1 and 0<=z<=1)
   if t==1 and 0<=z<=1:hits.append((i,z))
  if j<len(path)-2:assert len(hits)==1 and 0<hits[0][1]<1;walls.append(hits[0][0])
  else:assert not hits
  tt=F(T[0]-a[0],v[0]) if v[0] else F(T[1]-a[1],v[1])
  if 0<tt<=1 and tuple(a[k]+tt*v[k] for k in(0,1))==T:assert j==len(path)-2 and tt==1
 for j,i in enumerate(walls,1):
  a,b=edges[i];v=sub(path[j],path[j-1]);o=sub(path[j+1],path[j]);ref=(-v[0],v[1]) if a[0]==b[0] else(v[0],-v[1]);assert det(ref,o)==0 and dot(ref,o)>0
 assert len(walls)==2*n+2*m-1
 rows.append({'case':name,'h':h,'d':d,'c':c,'D':D,'widths':[ws,wt,w1,w2],'m':m,'n':n,'tau':tau,'delta':delta,'polygon':V,'S':S,'T':T,'path':path,'walls':walls,'reflections':len(walls),'all_wall_leg_guards':guards})
assert datetime.now(timezone.utc)<datetime.fromisoformat(E['deadline'])
out={'status':'ALL_FOUR_PRESCRIBED_COMMONDEPTH_FORMULAS_PASS','rows':rows,'reflections':sum(z['reflections'] for z in rows),'all_wall_leg_guards':sum(z['all_wall_leg_guards'] for z in rows),'discovery':False,'whole_goal_complete':False,'original_deadline':E['deadline'],'finished_utc':datetime.now(timezone.utc).isoformat()}
(R/'common-depth-zigzag-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='rows'}))
