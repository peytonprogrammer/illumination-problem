"""Independent replay of prescribed A48 paths; no discovery."""
from pathlib import Path
from fractions import Fraction as Q
import importlib.util,json,hashlib
R=Path(__file__).resolve().parent;P=R.parent/'construction'
s=importlib.util.spec_from_file_location('own',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
def room(h,d):
 G=2*h+4+(d or 0);V=[(0,0),(1,0),(1,h),(2,h),(2,h+2),(1,h+2),(1,h+d+2 if d else h+4),(2,h+d+2 if d else h+4),(2,h+d+4 if d else h+6),(1,h+d+4 if d else h+6),(1,G),(0,G),(0,2*h+3),(-1,2*h+3),(-1,2*h+1),(0,2*h+1),(0,3),(-1,3),(-1,1),(0,1)]
 return [tuple(map(Q,z)) for z in V]
def check(V,path,h,raw=None):
 g.simple(V);assert len(V)==20;path=[tuple(map(Q,z)) for z in path];assert path[0]==(0,2) and path[-1]==(0,2*h+2)
 assert not any(g.on(a,b,path[-1]) for a,b in zip(path[:-2],path[1:-1]))
 if raw:
  pv=[tuple(map(Q,z)) for z in raw['polygon']];assert {frozenset(z) for z in g.edges(V)}=={frozenset(z) for z in g.edges(pv)}
  v=tuple(map(Q,raw['actual']['direction']));e=g.vec(path[0],path[1]);assert g.det(v,e)==0 and g.dot(v,e)>0
  assert len(raw['actual']['walls'])==len(path)-2
  for z,i in zip(path[1:-1],raw['actual']['walls']):assert g.on(pv[i],pv[(i+1)%20],z)
 res=g.path_check(V,path)
 if raw:assert res['reflections']==raw['actual']['reflections']
 return res
raw=json.loads((P/'c1-q2-check.json').read_text());rows=[]
expected={('A0',h,0) for h in(3,6,8)}|{('A1',4,1),('A1',3,1)}|{('A1',h,d) for d in range(1,5) for h in range(max(5,2*d),2*d+5)}
assert {(r['case'],r['h'],r['d']) for r in raw['rows']}==expected and len(raw['rows'])==21
for z in raw['rows']:
 h,d=z['h'],z['d'];rows.append({'case':z['case'],'h':h,'d':d,**check(room(h,d),z['actual']['path'],h,z)})
assert sum(r['reflections'] for r in rows)==672 and sum(r['wall_leg_guards'] for r in rows)==13860
cap=json.loads((P/'c1-q2-cap-check.json').read_text())
for d in(2,3,1000000):rows.append({'case':'actual_h3_cap_transport','h':3,'d':d,**check(room(3,d),cap['actual']['path'],3)})
for h,d,chart in [(4,0,'floor'),(4,2,'floor'),(4,1000,'floor'),(5,4,'three'),(9,0,'three'),(10,5,'seven'),(12,5,'seven'),(14,5,'seven'),(10000,5000,'seven')]:
 h=Q(h)
 if chart=='floor':path=[(0,2),(Q(2,3),0),(1,1),(0,4),(1,7),(0,10)]
 elif chart=='three':path=[(0,2),(1,2+h/2),(0,2+h),(1,2+3*h/2),(0,2*h+2)]
 else:
  path=[(0,2)]
  for j in range(1,5):
   path.append((1,2+(2*j-1)*h/4))
   if j<4:path.append((0,2+j*h/2))
  path.append((0,2*h+2))
 rows.append({'case':chart,'h':int(h),'d':d,**check(room(h,d),path,h)})
out={'status':'A48_PRESCRIBED_INDEPENDENT_CHECKS_PASS','rows':rows,'paths':len(rows),'reflections':sum(z['reflections'] for z in rows),'wall_leg_guards':sum(z['wall_leg_guards'] for z in rows),'exception_reflections':672,'exception_wall_leg_guards':13860,'discovery':False,'whole_goal_complete':False,'source_sha256':{f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ['../construction/c1-q2-check.json','../construction/c1-q2-cap-check.json','resumed-exact-check.py']}}
(R/'c1-q2-independent-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in('rows','source_sha256')}))
