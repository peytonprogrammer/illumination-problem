from pathlib import Path
from fractions import Fraction as F
from datetime import datetime,timezone
import json,hashlib
R=Path(__file__).resolve().parent;P=R.parent/'review';req=json.loads((P/'h2-flush-review-request.json').read_text())
for n,h in req['source_sha256'].items():assert hashlib.sha256((P/n).read_bytes()).hexdigest()==h,n
# Independently replay the literal D0 five at unequal real widths.
f,a,g=F(1,3),F(7,2),F(100009,7)
V=[(-f,-3),(2,-3),(2,-1),(1,-1),(1,1),(2,1),(2,3),(1,3),(1,5),(-g,5),(-g,3),(0,3),(0,2),(-a,2),(-a,0),(0,0),(0,-1),(-f,-1)];V=[tuple(map(F,v)) for v in V]
path=[(1,-2),(F(7,5),-3),(2,-F(3,2)),(F(9,5),-1),(1,-3),(0,-F(1,2)),(1,2)];path=[tuple(map(F,v)) for v in path];edges=list(zip(V,V[1:]+V[:1]))
def sub(a,b):return(a[0]-b[0],a[1]-b[1])
def det(a,b):return a[0]*b[1]-a[1]*b[0]
def dot(a,b):return a[0]*b[0]+a[1]*b[1]
wall_ids=[];guards=0
for j,(x,y) in enumerate(zip(path,path[1:])):
 v=sub(y,x);hits=[]
 for i,(p,q) in enumerate(edges):
  guards+=1;e=sub(q,p);den=det(v,e);assert den
  t=F(det(sub(p,x),e),den);u=F(det(sub(p,x),v),den)
  assert not(0<t<1 and 0<=u<=1)
  if t==1 and 0<=u<=1:hits.append((i,u))
 if j<len(path)-2:assert len(hits)==1 and 0<hits[0][1]<1;wall_ids.append(hits[0][0])
 else:assert not hits
 target=(F(1),F(2));tt=F(target[0]-x[0],v[0])
 if 0<tt<=1 and tuple(x[k]+tt*v[k] for k in(0,1))==target:assert j==len(path)-2 and tt==1
for j,i in enumerate(wall_ids,1):
 e=sub(edges[i][1],edges[i][0]);v=sub(path[j],path[j-1]);vout=sub(path[j+1],path[j]);ref=(-v[0],v[1]) if not e[0] else(v[0],-v[1]);assert det(ref,vout)==0 and dot(ref,vout)>0
assert len(wall_ids)==5
out={'status':'LITERAL_D0_FIVE_UNSPLIT_ACTUAL_FLOOR_PATH_PASS','actual_D0_path':path,'polygon':V,'reflections':5,'all_wall_leg_guards':guards,'peer_pins_checked':len(req['source_sha256']),'peer_optical_code_executed':False,'peer_controls_replayed':False,'discovery':False,'finished_utc':datetime.now(timezone.utc).isoformat(),'whole_goal_complete':False}
(R/'h2-flush-independent-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in('exceptional_rows','actual_D0_path','polygon')}))
