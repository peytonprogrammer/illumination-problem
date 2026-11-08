"""Prescribed certificate replay and formula controls; no direction or room search."""
from pathlib import Path
from fractions import Fraction as Q
import importlib.util,json,hashlib
R=Path(__file__).resolve().parent;P=R.parent/'construction'
s=importlib.util.spec_from_file_location('own',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
def polygon(c,G,right,left):
 V=[(0,0),(c,0)]
 for a,b in right:V.extend([(c,a),(c+1,a),(c+1,b),(c,b)])
 V.extend([(c,G),(0,G)])
 for a,b in reversed(left):V.extend([(0,b),(-1,b),(-1,a),(0,a)])
 return [tuple(map(Q,z)) for z in V]
def room(h,d=None):
 return polygon(2,2*h+4 if d is None else 2*h+d+4,[(1,3),(2*h+1,2*h+3)],[(h,h+2),(h+4,h+6) if d is None else (h+d+2,h+d+4)])
def verify(V,path,S,T,raw=None):
 g.simple(V);assert len(V)==20
 path=[tuple(map(Q,z)) for z in path];assert path[0]==S and path[-1]==T
 assert not any(g.on(a,b,T) for a,b in zip(path[:-2],path[1:-1]))
 if raw:
  pv=[tuple(map(Q,z)) for z in raw['polygon']];g.simple(pv)
  assert {frozenset(z) for z in g.edges(V)}=={frozenset(z) for z in g.edges(pv)}
  v=tuple(map(Q,raw['actual']['direction']));leg=g.vec(path[0],path[1]);assert g.det(v,leg)==0 and g.dot(v,leg)>0
  for z,i in zip(path[1:-1],raw['actual']['walls']):assert g.on(pv[i],pv[(i+1)%20],z)
 res=g.path_check(V,path)
 if raw:assert res['reflections']==raw['actual']['reflections']
 return res
rows=[]
a=json.loads((P/'c2-A0-prefix-check.json').read_text());rows.append({'case':'A0_h4',**verify(room(4),a['actual']['path'],(2,2),(2,10),a)})
a=json.loads((P/'c2-A1-below-check.json').read_text())
for h,d in [(6,2),(8,2),(8,4),(10,4),(12,4)]:
 rr=[z for z in a['rows'] if (z['h'],z['d'])==(h,d)];assert len(rr)==1
 z=rr[0];rows.append({'case':f'A1_exception_{h}_{d}',**verify(room(h,d),z['actual']['path'],(2,2),(2,2*h+2),z)})
for h,d,chart in [(4,2,'floor'),(4,1000000,'floor'),(6,6,'three'),(100,2,'three'),(12,6,'seven'),(14,6,'seven'),(16,6,'seven'),(2000000,1000000,'seven'),(2,2,'h2'),(2,1000000,'h2')]:
 h,d=Q(h),Q(d);S=(2,2);T=(2,2*h+2)
 if chart=='floor':path=[S,(Q(2,3),0),(0,1),(2,4),(0,7),T]
 elif chart=='three':path=[S,(0,2+h/2),(2,2+h),(0,2+3*h/2),T]
 elif chart=='seven':
  path=[S]
  for j in range(1,5):
   path.append((0,2+(2*j-1)*h/4))
   if j<4:path.append((2,2+j*h/2))
  path.append(T)
 else:path=[S,(-1,3),(2,4),(0,Q(14,3)),(3,Q(17,3)),T]
 rows.append({'case':f'A1_formula_{chart}_{h}_{d}',**verify(room(h,d),path,S,T)})
files=['../construction/c2-A0-prefix-check.json','../construction/c2-A1-below-check.json','resumed-exact-check.py']
out={'status':'PRESCRIBED_INDEPENDENT_CHECKS_PASS','rows':rows,'reflections':sum(z['reflections'] for z in rows),'wall_leg_guards':sum(z['wall_leg_guards'] for z in rows),'discovery':False,'whole_goal_complete':False,'source_sha256':{f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in files}}
(R/'c2-completion-independent-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('rows','source_sha256')}))
