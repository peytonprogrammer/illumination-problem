from pathlib import Path
from fractions import Fraction as Q
from math import floor,ceil
from datetime import datetime,timezone
import ast,json,hashlib
R=Path(__file__).resolve().parent;P=R.parent/'review';E=json.loads((R/'critical-tooth-return-effort.json').read_text());assert datetime.now(timezone.utc)<datetime.fromisoformat(E['deadline'])
source=P/'resumed-exact-check.py';tree=ast.parse(source.read_text());names={'vec','det','dot','edges','on','location','intersect','simple','path_check','fold'};ns={'Q':Q};exec(compile(ast.Module(body=[z for z in tree.body if isinstance(z,ast.FunctionDef) and z.name in names],type_ignores=[]),str(source),'exec'),ns)
def fold(z):z=z%4;return min(z,4-z)
def excursion(width,base,entry,tau):
 a=entry-base;stop=a+2*width*tau;times={Q(width)}
 for j in range(floor(a/2)-1,ceil(stop/2)+2):
  x=Q(2*j-a,tau)
  if 0<x<2*width:times.add(x)
 assert (a+width*tau).denominator!=1
 out=[(Q(0),entry)]+[(-x if x<=width else x-2*width,base+fold(a+tau*x)) for x in sorted(times)]+[(Q(0),base+fold(stop))]
 return out
rows=[]
for aa,bb in[(1,2),(7,5),(4,1),(5,1),(6,1),(8,1),(25,1)]:
 V=[(0,0),(1,0),(1,1),(3,1),(3,3),(1,3),(1,13),(3,13),(3,15),(1,15),(1,16),(0,16),(0,12),(-bb,12),(-bb,10),(0,10),(0,8),(-aa,8),(-aa,6),(0,6)];V=[tuple(map(Q,z)) for z in V];ns['simple'](V)
 upper=bb>=2;w=bb if upper else aa;den=w+(3 if upper else 5);low=Q(5,2) if upper else Q(3,2);high=Q(3) if upper else Q(5,3)
 k=floor((low*den-8)/2)+1;tau=Q(8+2*k,den);assert low<tau<high
 path=[(Q(2),Q(2)),(2-1/tau,Q(1)),(Q(1),tau),(Q(0),2*tau),(Q(1),3*tau)]
 ext=excursion(w,10 if upper else 6,4*tau,tau);path+=ext
 if upper:assert ext[-1]==(0,16-2*tau)
 else:
  assert ext[-1]==(0,16-6*tau);path +=[(Q(1),16-5*tau),(Q(0),16-4*tau),(Q(1),16-3*tau),(Q(0),16-2*tau)]
 path +=[(Q(1),16-tau),(2-1/tau,Q(15)),(Q(2),Q(14))]
 assert path[0]==(2,2) and path[-1]==(2,14)
 for j,(a,b) in enumerate(zip(path,path[1:])):
  if ns['on'](a,b,path[-1]):assert j==len(path)-2
 result=ns['path_check'](V,path);assert result['reflections']==(5 if upper else 9)+2*k
 rows.append({'a':aa,'b':bb,'branch':'upper' if upper else'lower','k':k,'tau':tau,'polygon':V,'S':[2,2],'T':[2,14],'path':path,**result})
assert datetime.now(timezone.utc)<datetime.fromisoformat(E['deadline'])
out={'status':'ALL_SEVEN_PRESCRIBED_TOOTH_RETURN_FORMULAS_PASS','rows':rows,'reflections':sum(z['reflections'] for z in rows),'all_wall_leg_guards':sum(z['wall_leg_guards'] for z in rows),'accepted_validator_definitions_reused':True,'source_sha256':{str(source):hashlib.sha256(source.read_bytes()).hexdigest()},'discovery':False,'whole_goal_complete':False,'original_deadline':E['deadline'],'finished_utc':datetime.now(timezone.utc).isoformat()}
(R/'critical-tooth-return-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in('rows','source_sha256')}))
