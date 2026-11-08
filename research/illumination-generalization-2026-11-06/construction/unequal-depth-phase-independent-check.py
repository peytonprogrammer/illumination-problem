from pathlib import Path
from fractions import Fraction as F
import json,hashlib
R=Path(__file__).resolve().parent;P=R.parent/'review';req=json.loads((P/'unequal-depth-phase-review-request.json').read_text())
for k,h in req['source_sha256'].items():assert hashlib.sha256((P/k).read_bytes()).hexdigest()==h,k
data=json.loads((P/'unequal-depth-phase-check.json').read_text())
def sub(a,b):return a[0]-b[0],a[1]-b[1]
def det(a,b):return a[0]*b[1]-a[1]*b[0]
def dot(a,b):return a[0]*b[0]+a[1]*b[1]
def inside(V,z):
 n=0
 for a,b in zip(V,V[1:]+V[:1]):
  if det(sub(b,a),sub(z,a))==0 and all(min(a[k],b[k])<=z[k]<=max(a[k],b[k]) for k in(0,1)):return False
  if min(a[1],b[1])<=z[1]<max(a[1],b[1]):n+=a[0]+F(z[1]-a[1],b[1]-a[1])*(b[0]-a[0])>z[0]
 return bool(n%2)
rows=[]
for row in data['rows']:
 p,q=row['depths'];h=row['h'];label=row['chart'];G=2*h+18;s=6;t=6+2*h;ws=p+1;wt=q+1;level={'mean':h+6,'bottom':h,'top':G-h}[label]
 lo,hi=(level-4,level) if label=='top' else(level,level+4)
 V=[(0,0),(1,0),(1,s-1),(1+ws,s-1),(1+ws,s+1),(1,s+1),(1,t-1),(1+wt,t-1),(1+wt,t+1),(1,t+1),(1,G),(0,G),(0,hi+2),(-2,hi+2),(-2,hi),(0,hi),(0,lo+2),(-2,lo+2),(-2,lo),(0,lo)]
 shift=0 if (1+p)%2==0 else 1;V=[(F(x+shift),F(y)) for x,y in V];edges=list(zip(V,V[1:]+V[:1]));path=[tuple(map(F,z)) for z in row['path']];S=(1+p+shift,s);T=(1+q+shift,t)
 assert path[0]==S and path[-1]==T and inside(V,S) and inside(V,T);assert all(z%2==0 for v in(S,T) for z in v)
 guards=0;wallpoints={}
 for j,(a,b) in enumerate(zip(path,path[1:])):
  v=sub(b,a);assert v!=(0,0) and inside(V,tuple((a[k]+b[k])/2 for k in(0,1)));hits=[]
  for i,(x,y) in enumerate(edges):
   guards+=1;e=sub(y,x);den=det(v,e)
   if not den:
    if det(sub(x,a),v)==0:
     axis=0 if v[0] else 1;lo2,hi2=sorted((F(x[axis]-a[axis],v[axis]),F(y[axis]-a[axis],v[axis])));assert max(lo2,0)>=min(hi2,1)
    continue
   z=F(det(sub(x,a),e),den);u=F(det(sub(x,a),v),den)
   assert not(0<z<1 and 0<=u<=1)
   if z==1 and 0<=u<=1:hits.append((i,u))
  if j<len(path)-2 and hits:assert len(hits)==1 and 0<hits[0][1]<1;wallpoints[j+1]=hits[0][0]
  else:assert not hits
  tt=F(T[0]-a[0],v[0]) if v[0] else F(T[1]-a[1],v[1])
  if 0<tt<=1 and tuple(a[k]+tt*v[k] for k in(0,1))==T:assert j==len(path)-2 and tt==1
 for j in range(1,len(path)-1):
  vin=sub(path[j],path[j-1]);out=sub(path[j+1],path[j])
  if j in wallpoints:
   a,b=edges[wallpoints[j]];ref=(-vin[0],vin[1]) if a[0]==b[0] else(vin[0],-vin[1])
  else:ref=vin
  assert det(ref,out)==0 and dot(ref,out)>0
 assert len(wallpoints)==row['reflections'] and guards==row['wall_leg_guards']
 rows.append({'depths':[p,q],'h':h,'chart':label,'reflections':len(wallpoints),'all_wall_leg_guards':guards})
out={'status':'ALL_EIGHT_PRESCRIBED_ACTUAL_WITNESSES_INDEPENDENTLY_PASS','rows':rows,'reflections':sum(z['reflections'] for z in rows),'all_wall_leg_guards':sum(z['all_wall_leg_guards'] for z in rows),'source_pins_checked':len(req['source_sha256']),'peer_code_executed':False,'discovery':False,'whole_goal_complete':False}
(R/'unequal-depth-phase-independent-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='rows'}))
