from pathlib import Path
from fractions import Fraction as F
import json,runpy,hashlib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
sub=lambda a,b:(a[0]-b[0],a[1]-b[1])
cross=lambda a,b:a[0]*b[1]-a[1]*b[0]
dot=lambda a,b:a[0]*b[0]+a[1]*b[1]
tri=lambda t:tuple(sorted(map(tuple,t)))
def physical(path,V):
 walls=list(zip(V,V[1:]+V[:1]))
 def inside(p):
  value=False
  for a,b in walls:
   e,v=sub(b,a),sub(p,a)
   assert cross(e,v) or not(min(a[0],b[0])<=p[0]<=max(a[0],b[0]) and min(a[1],b[1])<=p[1]<=max(a[1],b[1]))
   if (a[1]>p[1])!=(b[1]>p[1]):
    x=a[0]+(p[1]-a[1])*(b[0]-a[0])/(b[1]-a[1])
    if p[0]<x:value=not value
  return value
 assert inside(path[0]) and inside(path[-1])
 for prev,p,nxt in zip(path,path[1:],path[2:]):
  hits=[(a,b) for a,b in walls if cross(sub(b,a),sub(p,a))==0 and 0<dot(sub(p,a),sub(b,a))<dot(sub(b,a),sub(b,a))]
  assert len(hits)==1,('nonstrict',p)
  a,b=hits[0];e,v,out=sub(b,a),sub(p,prev),sub(nxt,p)
  reflected=tuple(2*dot(v,e)*e[k]/dot(e,e)-v[k] for k in [0,1])
  assert cross(reflected,out)==0 and dot(reflected,out)>0
 for p,q in zip(path,path[1:]):
  assert inside(tuple((p[k]+q[k])/2 for k in [0,1]))
  v=sub(q,p)
  for a,b in walls:
   w,ap=sub(b,a),sub(a,p);den=cross(v,w)
   if den:
    t,s=cross(ap,w)/den,cross(ap,v)/den
    assert not(0<t<1 and 0<=s<=1),('earlier boundary',p,q,a,b)
   elif cross(ap,v)==0:
    aa,bb=dot(ap,v)/dot(v,v),dot(sub(b,p),v)/dot(v,v)
    assert max(min(aa,bb),F(0))>=min(max(aa,bb),F(1))



source=ROOT/'surplus-four-local/backward-gate-check.json'
rooms=ROOT/'surplus-four-local/single-e2-check.json'
d=json.loads(source.read_text());geometry=json.loads(rooms.read_text())['residues']
g=runpy.run_path(str(ROOT/'lower-bound-proof-audit/full-replay/guard-checker.py'))
sigma=lambda p:(2-p[1],2-p[0])
results={}
for name,row in d['paths'].items():
 P=[tuple(map(F,p)) for p in row['path']]; V=[tuple(map(F,p)) for p in geometry[name]['vertices']]
 assert P[0]==(0,0) and P[-1]==(2,2) and cross(sub(P[1],P[0]),(4,25))==0 and dot(sub(P[1],P[0]),(4,25))>0
 physical(P,V);physical(P[::-1],V);physical([sigma(p) for p in reversed(P)],[sigma(p) for p in V])
 U,Z=g['path_requirements'](P);room={tri(t) for t in geometry[name]['triangles']}
 assert U<=room and not Z&room
 assert U=={tri(t) for t in row['required_triangles']} and Z=={tri(t) for t in row['forbidden_triangles']}
 assert len(P)-2==row['reflections']
 results[name]={'status':'PASS','reflections':len(P)-2,'full_guard_equality':'PASS','actual_boundary_forward_reverse_sigma':'PASS'}
(HERE/'check.json').write_text(json.dumps({'status':'PASS','scope':'Independent exact fixed-path boundary replay; full parameter interval not recertified','results':results,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest()},indent=2)+'\n')
print('PASS: independent R-minus 21/19 fixed paths, actual boundary, reverse/sigma and full guards')
