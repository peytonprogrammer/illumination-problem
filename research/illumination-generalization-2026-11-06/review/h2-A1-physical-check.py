"""R47 prescribed actual paths and protected R46 transfer, no discovery."""
from pathlib import Path
from fractions import Fraction as Q
import importlib.util,json,ast,hashlib
R=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('own',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
a=ast.parse((R/'minimal-prefix-physical-check.py').read_text());exec(compile(ast.Module(body=[n for n in a.body if isinstance(n,ast.FunctionDef) and n.name in ['events','arm','construct']],type_ignores=[]),'frozen R46 definitions only','exec'))
def poly(D,d,a,b):return [tuple(map(Q,z)) for z in [(0,-4),(1,-4),(1,-3),(D+2,-3),(D+2,-1),(1,-1),(1,1),(D+2,1),(D+2,3),(1,3),(1,d+4),(0,d+4),(0,d+2),(-b,d+2),(-b,d),(0,d),(0,0),(-a,0),(-a,-2),(0,-2)]]
def local(D,a):
 if D==1:
  es,et,n,ns,nt= (3,1,1,-1,0) if a==1 else (1,1,1,0,0)
  if a==1:k=0;tau=Q(3,5)
  else:j=(a+3)//4+1;k=j-1;tau=Q(2*j,a+3);assert Q(1,2)<tau<1
 else:
  if a==2:es,et,n,ns,nt,k,tau=4,2,1,-1,0,0,Q(3,7)
  elif a==4:es,et,n,ns,nt,k,tau=2,4,0,-2,3,3,Q(13,8)
  else:es,et,n,ns,nt=4,2,1,-2,1;k=a//2+1;tau=Q(5+2*k,a+5);assert 1<tau<Q(6,5)
 sy=-2+2*ns+es*tau;ty=2+2*nt-et*tau;p1=sy+tau;p2=ty-(2*n+1)*tau
 assert -3<sy<-1 and 1<ty<3 and -2<p1<0 and -2<p2<0
 assert p1+2*a*tau==p2+4*k
 assert not(tau.denominator==1 and tau.numerator%2==1)
 phase=p1+2+a*tau;assert not(phase.denominator==1 and phase.numerator%2==0)
 path=list(reversed(arm(sy,es,D+1,tau,-1,-3)));path.append((Q(0),p1))
 for r in events(p1+2,tau,2*a,a)[1:]:path.append((-r if r<=a else r-2*a,-2+g.fold(p1+2+tau*r,Q(2))))
 assert path[-1]==(0,p2)
 for i in range(1,2*n+1):
  y=p2+i*tau
  assert (-1<y<1) if i%2 else (0<y<1)
  path.append((Q(1 if i%2 else 0),y))
 path.append((Q(1),ty));path.extend(arm(ty,et,D+1,tau,1,1)[1:]);return path
rows=[]
def check(D,d,a,b,path,kind):
 p=poly(D,d,a,b);g.simple(p);assert len(p)==20
 assert path[0]==(1+D,-2) and path[-1]==(1+D,2)
 assert not any(g.on(u,v,path[-1]) for u,v in zip(path[:-2],path[1:-1]))
 res=g.path_check(p,path);rows.append({'D':D,'d':d,'a':str(a),'b':str(b),'kind':kind,'polygon':p,'path':path,**res})
# D0 adjacent room: one path ignores BOTH entire opposite tooth interiors.
p0=[(1,-2),(0,Q(2,3)),(1,Q(10,3)),(Q(3,8),5),(0,4),(Q(9,8),1),(Q(15,8),3),(2,Q(8,3)),(Q(11,8),1),(1,2)]
for a,b in [(1,1),(2,8),(Q(1,3),100003),(100003,Q(2,7))]:check(0,1,a,b,p0,'D0 universal8')
for D in [1,2]:
 for a in [1,2,3,4,5,6,7,13,100]:
  path=local(D,a)
  for b in [Q(1,3),100003]:check(D,1,a,b,path,'D1/2 lower-return')
# Every finite R46 row transferred to an actual A1 room at d2 and large d.
cases=json.loads((R/'minimal-prefix-chart-check.json').read_text())['rows']
for c in cases:
 basepath=construct(c,0);path=[(x,-y) for x,y in reversed(basepath)]
 for d in [2,1000000]:check(c['D'],d,c['w'],Q(100003,7),path,'R46 protected vertical reverse')
out={'status':'R47_ALL_PRESCRIBED_ACTUAL_PATHS_PASS','discovery':False,'rows':rows,'paths':len(rows),'reflections':sum(r['reflections'] for r in rows),'wall_leg_guards':sum(r['wall_leg_guards'] for r in rows),'source_sha256':{f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ['minimal-prefix-proof.md','minimal-prefix-chart-check.json','minimal-prefix-physical-check.py','resumed-exact-check.py']},'whole_goal_complete':False}
(R/'h2-A1-physical-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['rows','source_sha256']}))
