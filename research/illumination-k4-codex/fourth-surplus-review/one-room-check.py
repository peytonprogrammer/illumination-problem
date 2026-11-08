"""Exactly one algebraically derived trajectory, no tracing or search."""
from pathlib import Path
from fractions import Fraction as F
import json,runpy,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
geom=HERE/'one-room-geometry.json';fixture=HERE/'remote22-residue-check.json'
vertices=[tuple(map(F,p)) for p in json.loads(geom.read_text())['vertices']]
room={tuple(sorted(map(tuple,t))) for t in json.loads(fixture.read_text())['triangles']}
sub=lambda a,b:(a[0]-b[0],a[1]-b[1])
cross=lambda a,b:a[0]*b[1]-a[1]*b[0]
dot=lambda a,b:a[0]*b[0]+a[1]*b[1]
wall=list(zip(vertices,vertices[1:]+vertices[:1]))
def interior(p):
 hit=False
 for a,b in wall:
  w=sub(b,a);v=sub(p,a)
  assert cross(w,v) or not (min(a[0],b[0])<=p[0]<=max(a[0],b[0]) and min(a[1],b[1])<=p[1]<=max(a[1],b[1])),('boundary',p)
  if (a[1]>p[1])!=(b[1]>p[1]):
   x=a[0]+(p[1]-a[1])*(b[0]-a[0])/(b[1]-a[1])
   if p[0]<x:hit=not hit
 return hit

d=F(10,13);assert F(13,17)<d<F(7,9)
# Prescribed analytic formulas, not outputs of a first-hit tracer.
path=[(F(0),F(0)),(2*d/(1+d),-2/(1+d)),
      (F(-2),4*d-2),(F(-1),5*d-2),(4-4/d,F(2)),(F(-2),6-6*d),
      (7/d-8,F(-1)),(F(3),11*d-8),(F(1),13*d-8),(11/d-12,F(3)),
      (F(3),14-15*d),((18*d-16)/(1+d),(14-20*d)/(1+d)),
      (21*d-16,F(1)),(23*d-16,F(-1)),(F(3),19/d-24),(22-26*d,F(2))]
assert path[0]==(0,0) and path[-1]==(2,2)
assert interior(path[0]) and interior(path[-1])
contacts=[]
for j,q in enumerate(path[1:-1],1):
 containing=[]
 for i,(a,b) in enumerate(wall):
  e=sub(b,a);f=sub(q,a)
  if cross(e,f)==0 and 0<dot(f,e)<dot(e,e):containing.append(i)
 assert len(containing)==1,(j,q,containing)
 i=containing[0];e=sub(wall[i][1],wall[i][0]);v=sub(q,path[j-1]);out=sub(path[j+1],q)
 reflected=tuple(2*dot(v,e)*x/dot(e,e)-v[k] for k,x in enumerate(e))
 assert cross(reflected,out)==0 and dot(reflected,out)>0,(j,'reflection')
 contacts.append({'index':j,'wall_index':i,'point':[[x.numerator,x.denominator] for x in q]})
for j,(p,q) in enumerate(zip(path,path[1:])):
 v=sub(q,p);assert dot(v,v)>0
 assert interior(tuple((p[k]+q[k])/2 for k in range(2)))
 for a,b in wall:
  w=sub(b,a);ap=sub(a,p);den=cross(v,w)
  if den:
   t=cross(ap,w)/den;s=cross(ap,v)/den
   assert not (0<t<1 and 0<=s<=1),(j,'intermediate boundary',a,b,t,s)
  elif cross(ap,v)==0:
   aa=dot(ap,v)/dot(v,v);bb=dot(sub(b,p),v)/dot(v,v)
   assert max(min(aa,bb),F(0))>=min(max(aa,bb),F(1)),(j,'boundary overlap')
checker=runpy.run_path(str(ROOT/'lower-bound-proof-audit/full-replay/guard-checker.py'))
U,Z=checker['path_requirements'](path)
assert U<=room and not Z&room,('guard',U-room,Z&room)
out={'status':'PASS','scope':'One explicitly algebraically derived14-reflection path; independent exact boundary/reflection/interior verification plus complete tile guards. No ray/direction/word discovery, tracer, archive or solver.','initial_direction':[10,-13],'parameter':[10,13],'strict_interval':[[13,17],[7,9]],'endpoint_formula':'x=22-26d at y=2','reflections':len(path)-2,'path':[[[x.numerator,x.denominator] for x in p] for p in path],'contacts':contacts,'required_triangles':sorted(U),'forbidden_triangles':sorted(Z),'inputs':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [geom,fixture]}}
(HERE/'one-room-check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'PASS','reflections':len(path)-2,'initial_direction':[10,-13],'endpoint':[2,2],'independent_boundary_checks':'PASS','full_tile_guards':'PASS'}))
