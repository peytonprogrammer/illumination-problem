"""Independent full physical replay of eleven prescribed A53 certificates; no discovery."""
from pathlib import Path
from fractions import Fraction as Q
import importlib.util,json,hashlib
R=Path(__file__).resolve().parent;P=R.parent/'construction';sp=importlib.util.spec_from_file_location('own',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
def poly(a,b):return [tuple(map(Q,z)) for z in[(0,0),(1,0),(1,1),(3,1),(3,3),(1,3),(1,13),(3,13),(3,15),(1,15),(1,16),(0,16),(0,12),(-b,12),(-b,10),(0,10),(0,8),(-a,8),(-a,6),(0,6)]]
rows=[]
for file,seed in[('critical-tooth-return-seeds.json',True),('critical-tooth-return-check.json',False)]:
 a=json.loads((P/file).read_text())
 if seed:assert {(z['a'],z['b']) for z in a['rows']}=={(1,1),(2,1),(3,1),(7,1)}
 for z in a['rows']:
  V=poly(z['a'],z['b']);g.simple(V);saved=[tuple(map(Q,p)) for p in z['polygon']];assert {frozenset(e) for e in g.edges(V)}=={frozenset(e) for e in g.edges(saved)}
  data=z['actual'] if seed else z;path=[tuple(map(Q,p)) for p in data['path']];S=(2,2);T=(2,14);assert path[0]==S and path[-1]==T
  assert not any(g.on(u,v,T) for u,v in zip(path[:-2],path[1:-1]))
  if seed:
   vel=tuple(map(Q,data['direction']));e=g.vec(path[0],path[1]);assert g.det(vel,e)==0 and g.dot(vel,e)>0
   for p,i in zip(path[1:-1],data['walls']):assert g.on(saved[i],saved[(i+1)%len(saved)],p)
  else:
   tau=Q(z['tau']);k=z['k'];assert k>=0
   if z['branch']=='upper':assert tau==Q(8+2*k,z['b']+3) and Q(5,2)<tau<3
   else:assert tau==Q(8+2*k,z['a']+5) and Q(3,2)<tau<Q(5,3)
   vel=(-1,-tau);e=g.vec(path[0],path[1]);assert g.det(vel,e)==0 and g.dot(vel,e)>0
  res=g.path_check(V,path);assert res['reflections']==data['reflections']
  rows.append({'a':z['a'],'b':z['b'],'seed':seed,**res})
assert sum(r['reflections'] for r in rows if r['seed'])==86
assert sum(r['wall_leg_guards'] for r in rows if r['seed'])==1800
out={'status':'A53_ALL_PRESCRIBED_ACTUAL_CERTIFICATES_INDEPENDENTLY_PASS','rows':rows,'seed_reflections':86,'seed_wall_leg_guards':1800,'formula_reflections':sum(r['reflections'] for r in rows if not r['seed']),'formula_wall_leg_guards':sum(r['wall_leg_guards'] for r in rows if not r['seed']),'discovery':False,'whole_goal_complete':False,'source_sha256':{f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ['../construction/critical-tooth-return-seeds.json','../construction/critical-tooth-return-check.json','resumed-exact-check.py']}}
(R/'critical-tooth-return-independent-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in('rows','source_sha256')}))
