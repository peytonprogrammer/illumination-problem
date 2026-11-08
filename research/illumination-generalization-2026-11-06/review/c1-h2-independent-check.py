"""Independent two prescribed certificates and seven whole-formula controls; no discovery."""
from pathlib import Path
from fractions import Fraction as Q
import importlib.util,json,hashlib
R=Path(__file__).resolve().parent;P=R.parent/'construction'
s=importlib.util.spec_from_file_location('own',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
def polygon(G,left,right):
 V=[(0,0),(1,0)]
 for a,b in right:V.extend([(1,a),(2,a),(2,b),(1,b)])
 V.extend([(1,G),(0,G)])
 for a,b in reversed(left):V.extend([(0,b),(-1,b),(-1,a),(0,a)])
 while True:
  for i in range(len(V)):
   if V[i]==V[i-1] or g.det(g.vec(V[i-1],V[i]),g.vec(V[i],V[(i+1)%len(V)]))==0:V.pop(i);break
  else:break
 return [tuple(map(Q,z)) for z in V]
def room(case,p=0):
 if case=='A1':G=p+8;mu=4;left=[(1,3),(5,7)];right=[(2,4),(p+4,p+6)];S=(0,2);T=(0,6)
 elif case=='D':G=8;mu=3;left=[(0,2),(4,6)];right=[(0,2),(3,5),(6,8)];S=(0,1);T=(0,5)
 else:
  mu=4 if case=='B' else p;G=8 if case=='B' else 2*mu+(2 if case=='C1' else 0)
  left=[(mu-3,mu-1),(mu+1,mu+3)];right=[(0,2),(mu,mu+2)]+([] if case=='B' else[(G-2,G)]);S=(0,mu-2);T=(0,mu+2)
 return polygon(G,left,right),S,T,mu

def check(V,S,T,path,raw=None):
 g.simple(V);path=[tuple(map(Q,z)) for z in path];assert path[0]==S and path[-1]==T
 assert not any(g.on(a,b,T) for a,b in zip(path[:-2],path[1:-1]))
 if raw:
  pv=[tuple(map(Q,z)) for z in raw['polygon']];g.simple(pv)
  assert {frozenset(e) for e in g.edges(V)}=={frozenset(e) for e in g.edges(pv)}
  v=tuple(map(Q,raw['actual']['direction']));e=g.vec(path[0],path[1]);assert g.det(v,e)==0 and g.dot(v,e)>0
  assert len(raw['actual']['walls'])==len(path)-2
  for z,i in zip(path[1:-1],raw['actual']['walls']):assert g.on(pv[i],pv[(i+1)%len(pv)],z)
 res=g.path_check(V,path)
 if raw:assert res['reflections']==raw['actual']['reflections']
 return res
raw=json.loads((P/'c1-h2-check.json').read_text());rows=[]
for name in('A1d1','D'):
 rr=[r for r in raw['rows'] if r['case']==name];assert len(rr)==1;z=rr[0];V,S,T,mu=room('A1',1) if name=='A1d1' else room('D')
 rows.append({'case':name,**check(V,S,T,z['actual']['path'],z)})
 if name=='D':
  # Same original actual A points under the required odd-floor interpretation.
  p=[tuple(map(Q,a)) for a in z['actual']['path']];V2=[(x,y+1) for x,y in V];p2=[(x,y+1) for x,y in p]
  assert all(int(x)%2==int(y)%2==0 for x,y in(p2[0],p2[-1]));g.path_check(V2,p2)
for case,p in[('B',0),('C1',4),('C1',1000000),('C2',5),('C2',1000000),('A1',2),('A1',1000000)]:
 V,S,T,mu=room(case,p);mu=Q(mu)
 if case=='A1':path=[S,(-1,Q(7,3)),(2,Q(10,3)),(0,4),(1,Q(13,3)),(0,Q(14,3)),(1,5),(-1,Q(17,3)),T]
 else:path=[S,(-1,mu-Q(5,3)),(1,mu-1),(0,mu-Q(2,3)),(1,mu-Q(1,3)),(0,mu),(2,mu+Q(2,3)),(-1,mu+Q(5,3)),T]
 rows.append({'case':case,'parameter':p,**check(V,S,T,path)})
out={'status':'A50_PRESCRIBED_CERTIFICATES_AND_FORMULAS_PASS','rows':rows,'paths':len(rows),'exception_reflections':sum(r['reflections'] for r in rows[:2]),'exception_wall_leg_guards':sum(r['wall_leg_guards'] for r in rows[:2]),'reflections':sum(r['reflections'] for r in rows),'wall_leg_guards':sum(r['wall_leg_guards'] for r in rows),'discovery':False,'whole_goal_complete':False,'source_sha256':{f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ['../construction/c1-h2-check.json','resumed-exact-check.py']}}
(R/'c1-h2-independent-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in('rows','source_sha256')}))
