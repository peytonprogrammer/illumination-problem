"""Independent actual-wall controls for every A54 all-d local mechanism; no search."""
from pathlib import Path
from fractions import Fraction as Q
import importlib.util,json,ast
R=Path(__file__).resolve().parent;P=R.parent/'construction'
sp=importlib.util.spec_from_file_location('own',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
for file,names in [('minimal-prefix-physical-check.py',['events','arm']),('tooth-return-grid-independent-check.py',['dims','polygon'])]:
 a=ast.parse((R/file).read_text());exec(compile(ast.Module(body=[n for n in a.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[]),file+' defs only','exec'))
def formula(h,D,w,n,l,r,k,tau):
 t=2*h+2;C=2-2*n;B=t+2*n;sy=C+D*tau;ty=B-D*tau;Y=h;p1=C+(D+2*l-1)*tau;p2=B-(D+2*r-1)*tau
 assert -1<D*tau-2*n<1 and Y<p1<Y+2 and Y<p2<Y+2 and p1+2*w*tau==p2+4*k
 phase=p1-Y+w*tau;assert not(phase.denominator==1 and phase.numerator%2==0)
 path=list(reversed(arm(sy,D,D+1,tau,-1,1)))
 for j in range(1,2*l-1):path.append((Q(0 if j%2 else 1),sy+j*tau))
 path.append((Q(0),p1))
 for u in events(p1-Y,tau,2*w,w)[1:]:path.append((-u if u<=w else u-2*w,Y+g.fold(p1-Y+tau*u,Q(2))))
 for j in range(1,2*r-1):path.append((Q(1 if j%2 else 0),p2+j*tau))
 path.append((Q(1),ty));path.extend(arm(ty,D,D+1,tau,1,t-1)[1:]);return path
cap=json.loads((P/'tooth-return-grid-cap.json').read_text())['rows'];h3d1=[tuple(map(Q,z)) for z in cap[0]['actual']['path']];h3d2=[tuple(map(Q,z)) for z in cap[1]['actual']['path']]
h4d2=[tuple(map(Q,z)) for z in json.loads((P/'tooth-return-grid-cap-h4.json').read_text())['rows'][0]['actual']['path']]
rows=[]
def check(kind,h,d,D,a,b,path,mechanism):
 row={'kind':kind,'h':h,'d':d,'D':D,'a':a,'b':b};V=polygon(row);g.simple(V);assert path[0]==(D+1,2) and path[-1]==(D+1,2*h+2)
 assert not any(g.on(u,v,path[-1]) for u,v in zip(path[:-2],path[1:-1]));res=g.path_check(V,path);rows.append({**row,'mechanism':mechanism,**res})
for kind,d in [('A0',None),('A1',2),('A1',1000000)]:
 for a,b in [(1,1),(100003,100009)]:
  check(kind,3,d,1,a,b,h3d1,'h3D1 tooth-free')
  check(kind,4,d,2,a,b,h4d2,'h4D2 tooth-free')
 for b in [1,100009]:check(kind,3,d,2,1,b,h3d2,'h3D2 lowerw1 cap')
 for a in [2,3,8,101]:
  k=(a-1)//2+1;tau=Q(5+2*k,a+4);assert 1<tau<Q(7,5);path=formula(3,2,a,1,1,2,k,tau);check(kind,3,d,2,a,100009,path,'h3D2 lower-return')
for d in [3,1000000]:
 for a in [1,2,3,8,101]:
  if a==1:n,l,r,k,tau=0,2,4,0,Q(4,7)
  else:n,l,r=0,2,3;k=int(((Q(2,3)*(a+5)-4)/2)//1)+1;tau=Q(4+2*k,a+5);assert Q(2,3)<tau<1
  check('A1',4,d,1,a,100009,formula(4,1,a,n,l,r,k,tau),'h4D1 lower-return')
out={'status':'ALL_A54_LOCAL_MECHANISM_CONTROLS_INDEPENDENTLY_PASS','rows':rows,'paths':len(rows),'reflections':sum(r['reflections'] for r in rows),'wall_leg_guards':sum(r['wall_leg_guards'] for r in rows),'whole_goal_complete':False,'discovery':False}
(R/'tooth-return-grid-local-independent-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='rows'}))
