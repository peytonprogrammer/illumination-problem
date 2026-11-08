from pathlib import Path
from fractions import Fraction as F
import json,hashlib
R=Path(__file__).resolve().parent;P=R.parent/'review'
src=P/'c1-critical-final-check.json';data=json.loads(src.read_text());rows=[]
def sub(a,b):return a[0]-b[0],a[1]-b[1]
def det(a,b):return a[0]*b[1]-a[1]*b[0]
def dot(a,b):return a[0]*b[0]+a[1]*b[1]
def inside(V,z):
 n=0
 for a,b in zip(V,V[1:]+V[:1]):
  if det(sub(b,a),sub(z,a))==0 and all(min(a[k],b[k])<=z[k]<=max(a[k],b[k]) for k in(0,1)):return False
  if min(a[1],b[1])<=z[1]<max(a[1],b[1]):
   x=a[0]+F(z[1]-a[1],b[1]-a[1])*(b[0]-a[0]);n+=x>z[0]
 return bool(n%2)
for h in(5,7):
 d=next(z for z in data['rows'] if z['h']==h)
 V=[(0,0),(1,0),(1,h),(2,h),(2,h+2),(1,h+2),(1,h+4),(2,h+4),(2,h+6),(1,h+6),(1,2*h+4),(0,2*h+4),(0,2*h+3),(-1,2*h+3),(-1,2*h+1),(0,2*h+1),(0,3),(-1,3),(-1,1),(0,1)]
 saved=[tuple(map(F,z)) for z in d['polygon']];assert any(saved==V[i:]+V[:i] for i in range(len(V)))
 A=d['first_path'];path=[tuple(map(F,z)) for z in A['path']];S=(0,2);T=(0,2*h+2)
 assert path[0]==S and path[-1]==T and inside(V,S) and inside(V,T)
 velocity=tuple(map(F,A['velocity']));assert det(sub(path[1],S),velocity)==0 and dot(sub(path[1],S),velocity)>0
 edges=list(zip(V,V[1:]+V[:1]));walls=[];guards=0
 for j,(a,b) in enumerate(zip(path,path[1:])):
  v=sub(b,a);hits=[];assert inside(V,tuple((a[k]+b[k])/2 for k in(0,1)))
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
  vin=sub(path[j],path[j-1]);out=sub(path[j+1],path[j]);a,b=edges[i];ref=(-vin[0],vin[1]) if a[0]==b[0] else(vin[0],-vin[1]);assert det(ref,out)==0 and dot(ref,out)>0
 assert len(walls)==A['reflections'] and guards==A['wall_leg_guards']
 rows.append({'h':h,'reflections':len(walls),'all_wall_leg_guards':guards,'actual_velocity':A['velocity']})
out={'status':'BOTH_PRESCRIBED_PEER_PREFIX_CERTIFICATES_INDEPENDENTLY_VERIFIED','rows':rows,'reflections':sum(r['reflections'] for r in rows),'all_wall_leg_guards':sum(r['all_wall_leg_guards'] for r in rows),'source_sha256':{str(src):hashlib.sha256(src.read_bytes()).hexdigest()},'discovery':False,'executed_peer_optical_code':False,'whole_goal_complete':False}
(R/'c1-variable-angle-prefix-independent.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
