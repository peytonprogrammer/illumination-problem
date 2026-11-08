from pathlib import Path
from fractions import Fraction as F
import json,hashlib
R=Path(__file__).resolve().parent;P=R.parent/'review';req=json.loads((P/'c2-BC-four-bounce-review-request.json').read_text())
for f,h in req['source_sha256'].items():assert hashlib.sha256((P/f).read_bytes()).hexdigest()==h,f
def sub(a,b):return a[0]-b[0],a[1]-b[1]
def det(a,b):return a[0]*b[1]-a[1]*b[0]
def dot(a,b):return a[0]*b[0]+a[1]*b[1]
def polygon(rects):
 cells={(x,y) for a,b,c,d in rects for x in range(a,b) for y in range(c,d)};edges=set()
 for x,y in cells:
  v=[(x,y),(x+1,y),(x+1,y+1),(x,y+1)]
  for a,b in zip(v,v[1:]+v[:1]):
   if(b,a) in edges:edges.remove((b,a))
   else:edges.add((a,b))
 n={}
 for a,b in edges:assert a not in n;n[a]=b
 a=min(n);cycle=[]
 while a not in cycle:cycle.append(a);a=n[a]
 assert a==cycle[0] and len(cycle)==len(edges)
 return [a for i,a in enumerate(cycle) if det(sub(a,cycle[i-1]),sub(cycle[(i+1)%len(cycle)],a))]
rows=[]
for name,G,mu,roof in [('B',8,4,False),('C1r0',10,4,True),('C2r0',12,6,True)]:
 rects=[(0,2,0,G),(2,3,mu-3,mu-1),(2,3,mu+1,mu+3),(-1,0,0,2),(-1,0,mu,mu+2)]
 if roof:rects.append((-1,0,G-2,G))
 V=polygon(rects);assert len(V)==(20 if roof else 18);E=list(zip(V,V[1:]+V[:1]))
 path=[(2,F(mu-2)),(3,F(mu)-F(5,3)),(0,F(mu)-F(2,3)),(2,F(mu)),(-1,F(mu+1)),(2,F(mu+2))]
 guards=0;walls=[]
 for j,(a,b) in enumerate(zip(path,path[1:])):
  v=sub(b,a);hits=[]
  for k,(x,y) in enumerate(E):
   guards+=1;e=sub(y,x);den=det(v,e)
   if not den:assert det(sub(x,a),v)!=0;continue
   t=F(det(sub(x,a),e),den);z=F(det(sub(x,a),v),den)
   assert not(0<t<1 and 0<=z<=1)
   if t==1 and 0<=z<=1:hits.append((k,z))
  if j<4:assert len(hits)==1 and 0<hits[0][1]<1;walls.append(hits[0][0])
  else:assert not hits
  target=path[-1];tt=F(target[0]-a[0],v[0])
  if 0<tt<=1 and tuple(a[k]+tt*v[k] for k in(0,1))==target:assert j==4 and tt==1
 for j,k in enumerate(walls,1):
  a,b=E[k];assert a[0]==b[0];v=sub(path[j],path[j-1]);o=sub(path[j+1],path[j]);ref=(-v[0],v[1]);assert det(ref,o)==0 and dot(ref,o)>0
 rows.append({'case':name,'walls':len(V),'reflections':len(walls),'all_wall_leg_guards':guards,'path':path})
out={'status':'ALL_THREE_PRESCRIBED_FORMULA_CHECKS_PASS','rows':rows,'reflections':12,'all_wall_leg_guards':sum(r['all_wall_leg_guards'] for r in rows),'peer_pins_checked':len(req['source_sha256']),'discovery':False,'peer_code_executed':False,'whole_goal_complete':False}
(R/'c2-BC-shuttle-independent-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps(out,default=str))
