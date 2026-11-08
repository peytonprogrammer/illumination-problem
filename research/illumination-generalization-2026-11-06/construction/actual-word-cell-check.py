"""Prescribed A57 formula controls; no discovery. Reuses the stated rational validator."""
import ast,json
from fractions import Fraction as F
from pathlib import Path
P=Path(__file__).resolve().parent
src=P.parent/'review/resumed-exact-check.py'
names={'vec','det','dot','edges','on','location','intersect','simple','path_check','fold'}
mod=ast.parse(src.read_text()); ns={'Q':F}
exec(compile(ast.Module(body=[n for n in mod.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[]),str(src),'exec'),ns)
fold=ns['fold']
def polygon(c,ws,wt,a,b):
 return [(0,0),(c,0),(c,1),(c+ws,1),(c+ws,3),(c,3),(c,7),(c+wt,7),(c+wt,9),(c,9),(c,11),(0,11),(0,8),(-b,8),(-b,6),(0,6),(0,5),(-a,5),(-a,3),(0,3)]
def arm(c,D,tau):
 n=D*tau/2;assert n.denominator==1
 n=int(n);sg=(-1)**n
 events={F(0),D}
 if tau:
  lo,hi=sorted((F(1),1+sg*tau*D))
  for j in range(int(lo//2)-1,int(hi//2)+2):
   r=(2*j-1)/(sg*tau)
   if 0<r<D:events.add(r)
 return [(c+D-r,1+fold(1+sg*tau*r,F(2))) for r in sorted(events)]
def core(c,beta):
 tau=beta/c;events={F(0),c,2*c,3*c,4*c}
 for j in range(1,int((2+4*beta)//11)+1):
  z=(11*j-2)/tau
  if 0<z<4*c:events.add(z)
 return [(fold(c-z,c),fold(2+tau*z,F(11))) for z in sorted(events)]
def run(c,beta,Ds,Dt):
 c,beta,Ds,Dt=map(F,(c,beta,Ds,Dt));tau=beta/c
 p=polygon(c,Ds+F(2,3),Dt+F(5,7),F(1,13),F(17,5));ns['simple'](p)
 sa=arm(c,Ds,tau);ta=[(x,10-y) for x,y in reversed(arm(c,Dt,tau))]
 path=sa+core(c,beta)[1:]+ta[1:]
 assert path[0]==(c+Ds,2) and path[-1]==(c+Dt,8)
 for i,(x,y) in enumerate(path[:-1]):
  assert (x,y)!=path[-1]
 for A,B in zip(path[:-2],path[1:-1]):assert not ns['on'](A,B,path[-1])
 out=ns['path_check'](p,path)
 expected=int(Ds*tau/2+Dt*tau/2)+3+int((2+4*beta)//11)
 assert out['reflections']==expected
 return {'c':str(c),'beta':str(beta),'Ds':str(Ds),'Dt':str(Dt),**out}
rows=[]
for c in [F(1),F(3,2),F(6),F(11),F(121)]:
 for beta in [7,18,29,40]:rows.append(run(c,beta,0,0))
for c in [1,2,6,11,22,121,1000]:
 p=1
 while c%(11*p)==0:p*=11
 u=c//p;k=next(k for k in range(1,11) if u*k%11==9);beta=2*u*k
 for ds,dt in [(0,p),(p,3*p),(2*p,0)]:rows.append(run(c,beta,ds,dt))
report={'status':'PRESCRIBED_FORMULA_CONTROLS_PASS','discovery':False,'validator_reuse':str(src),'rows':rows,'reflections':sum(r['reflections'] for r in rows),'guards':sum(r['wall_leg_guards'] for r in rows),'whole_goal_complete':False}
(P/'actual-word-cell-check.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='rows'}))
