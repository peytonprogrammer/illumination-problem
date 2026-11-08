#!/usr/bin/env python3
"""Read frozen positive witnesses; verify finite physical paths, with no search/writes."""
from pathlib import Path
from fractions import Fraction as F
from datetime import datetime,timezone
import hashlib,json
R=Path(__file__).resolve().parent
raw=(R/'local-surgery-optics.json').read_bytes();data=json.loads(raw)
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def sub(a,b):return a[0]-b[0],a[1]-b[1]
def dot(a,b):return a[0]*b[0]+a[1]*b[1]
def on(a,b,c):return cross(sub(b,a),sub(c,a))==0 and all(min(a[k],b[k])<=c[k]<=max(a[k],b[k]) for k in (0,1))
def inside(p,z):
 assert not any(on(a,b,z) for a,b in zip(p,p[1:]+p[:1]))
 winding=0
 for a,b in zip(p,p[1:]+p[:1]):
  if a[1]<=z[1]<b[1] and cross(sub(b,a),sub(z,a))>0:winding+=1
  if b[1]<=z[1]<a[1] and cross(sub(b,a),sub(z,a))<0:winding-=1
 return winding!=0
checked=[]
assert data['status']=='ALL_FIVE_HAVE_POSITIVE_WITNESSES' and len(data['rows'])==5
assert {r['deleted_index'] for r in data['rows']}=={2,4,12,14,19}
for row in data['rows']:
 p=[tuple(map(F,z)) for z in row['polygon']];path=[tuple(map(F,z)) for z in row['witness']['path']];wallids=row['witness']['wall_indices']
 assert path[0]==tuple(map(F,row['S'])) and path[-1]==tuple(map(F,row['T']))
 assert inside(p,path[0]) and inside(p,path[-1])
 assert len(path)==len(wallids)+2 and len(wallids)==row['witness']['reflections']
 for j,z in enumerate(path[1:-1]):
  assert z not in p
  contacts=[i for i,(a,b) in enumerate(zip(p,p[1:]+p[:1])) if on(a,b,z)]
  assert contacts==[wallids[j]]
  i=wallids[j];a,b=p[i],p[(i+1)%len(p)];e=sub(b,a);normal=(-e[1],e[0])
  vin=sub(z,path[j]);vout=sub(path[j+2],z)
  reflected=tuple(vin[k]-2*dot(vin,normal)*normal[k]/dot(normal,normal) for k in (0,1))
  assert cross(reflected,vout)==0 and dot(reflected,vout)>0
  assert dot(vin,normal)*dot(vout,normal)<0
 for a,b in zip(path,path[1:]):
  assert a!=b
  mid=((a[0]+b[0])/2,(a[1]+b[1])/2)
  assert inside(p,mid)
  v=sub(b,a)
  for c,d in zip(p,p[1:]+p[:1]):
   e=sub(d,c);den=cross(v,e)
   if den:
    t=cross(sub(c,a),e)/den;u=cross(sub(c,a),v)/den
    assert not(0<t<1 and 0<=u<=1),('intermediate wall',row['deleted_index'],a,b,c,d,t,u)
   elif cross(sub(c,a),v)==0:
    k=0 if v[0] else 1
    t1=(c[k]-a[k])/v[k];t2=(d[k]-a[k])/v[k]
    lo,hi=sorted((t1,t2))
    assert max(lo,F(0))>=min(hi,F(1)),('wall overlap',row['deleted_index'])
  assert all(not on(a,b,z) or z==a or z==b for z in p)
 checked.append({'deleted_index':row['deleted_index'],'reflections':len(wallids),'complete_open_leg_and_all_corner_checks':True,'smooth_contact_and_specular_checks':True,'actual_endpoints':True})
print(json.dumps({'status':'ALL_PRESCRIBED_PATHS_EXACTLY_VERIFIED','kind':'Full finite-path validation; no direction/word search and no independent-peer claim','verified_utc':datetime.now(timezone.utc).isoformat(),'witness_sha256':hashlib.sha256(raw).hexdigest(),'paths':checked,'total_reflections':sum(x['reflections'] for x in checked),'darkness_claim':False,'whole_goal_complete':False},indent=2))
