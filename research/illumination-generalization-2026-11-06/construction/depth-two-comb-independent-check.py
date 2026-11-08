from pathlib import Path
from fractions import Fraction as F
import json,hashlib
R=Path(__file__).resolve().parent;P=R.parent/'review';req=json.loads((P/'depth-two-comb-review-request.json').read_text())
for name,h in req['source_sha256'].items():assert hashlib.sha256((P/name).read_bytes()).hexdigest()==h,name
d=json.loads((R/'c2-A0-prefix-check.json').read_text());V=[(2*F(x),F(y)) for x,y in d['polygon']];path=[(2*F(x),F(y)) for x,y in d['actual']['path']];edges=list(zip(V,V[1:]+V[:1]));S=(4,2);T=(4,10);assert path[0]==S and path[-1]==T
assert len(V)==20 and all(q.denominator==1 for z in V for q in z)
def sub(a,b):return a[0]-b[0],a[1]-b[1]
def det(a,b):return a[0]*b[1]-a[1]*b[0]
def dot(a,b):return a[0]*b[0]+a[1]*b[1]
guards=0;walls=[]
for j,(a,b) in enumerate(zip(path,path[1:])):
 v=sub(b,a);hits=[]
 for i,(x,y) in enumerate(edges):
  guards+=1;e=sub(y,x);den=det(v,e)
  if not den:assert det(sub(x,a),v)!=0;continue
  t=F(det(sub(x,a),e),den);z=F(det(sub(x,a),v),den)
  assert not(0<t<1 and 0<=z<=1)
  if t==1 and 0<=z<=1:hits.append((i,z))
 if j<len(path)-2:assert len(hits)==1 and 0<hits[0][1]<1;walls.append(hits[0][0])
 else:assert not hits
 tt=F(T[0]-a[0],v[0]) if v[0] else F(T[1]-a[1],v[1])
 if 0<tt<=1 and tuple(a[k]+tt*v[k] for k in(0,1))==T:assert j==len(path)-2 and tt==1
for j,i in enumerate(walls,1):
 a,b=edges[i];v=sub(path[j],path[j-1]);o=sub(path[j+1],path[j]);ref=(-v[0],v[1]) if a[0]==b[0] else(v[0],-v[1]);assert det(ref,o)==0 and dot(ref,o)>0
out={'status':'PRESCRIBED_ACTUAL_C4_D0_AXIAL_PULLBACK_PASS','reflections':len(walls),'all_wall_leg_guards':guards,'source':S,'target':T,'actual_primitive_direction':[-5,-1],'source_sha256':{'c2-A0-prefix-check.json':hashlib.sha256((R/'c2-A0-prefix-check.json').read_bytes()).hexdigest()},'peer_pins_checked':len(req['source_sha256']),'peer_optical_code_executed':False,'discovery':False,'whole_goal_complete':False}
(R/'depth-two-comb-independent-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
