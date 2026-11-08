"""Prescribed exact checks of the proved variable-portal formula. No discovery."""
import ast,json
from pathlib import Path
from fractions import Fraction as Q
P=Path(__file__).resolve().parent
src=P.parent/'review/resumed-exact-check.py';names={'vec','det','dot','edges','on','location','intersect','simple','path_check','fold'}
ns={'Q':Q};mod=ast.parse(src.read_text());exec(compile(ast.Module(body=[n for n in mod.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[]),str(src),'exec'),ns);fold=ns['fold']
def arm(c,D,tau,n):
 ev={Q(0),D};lo=1-2*n;hi=lo+tau*D
 for j in range(int(lo//2)-1,int(hi//2)+2):
  r=(2*j-lo)/tau
  if 0<r<D:ev.add(r)
 return [(c+D-r,1+fold(lo+tau*r,Q(2))) for r in sorted(ev)]
def run(c,ds,dt):
 c,ds,dt=map(Q,(c,ds,dt));L=4*c+ds+dt;N=0;steps=0
 while True:
  tau=(28+2*N)/L;n=[(d*tau/2+Q(1,2))//1 for d in (ds,dt)];M=sum(n);assert M>=N
  if M==N:break
  N=M;steps+=1
 delta=[d*tau-2*k for d,k in zip((ds,dt),n)];assert all(-1<v<1 for v in delta)
 events={Q(0),c,2*c,3*c,4*c};start=2+delta[0]
 for j in (1,2):events.add((11*j-start)/tau)
 core=[(fold(c-z,c),fold(start+tau*z,Q(11))) for z in sorted(events)]
 path=arm(c,ds,tau,n[0])+core[1:]+[(x,10-y) for x,y in reversed(arm(c,dt,tau,n[1]))][1:]
 ws=ds+Q(1,7);wt=dt+Q(3,11);a=Q(2,3);b=Q(1,2)
 poly=[(0,0),(c,0),(c,1),(c+ws,1),(c+ws,3),(c,3),(c,7),(c+wt,7),(c+wt,9),(c,9),(c,11),(0,11),(0,8),(-b,8),(-b,6),(0,6),(0,5),(-a,5),(-a,3),(0,3)]
 ns['simple'](poly);out=ns['path_check'](poly,path);assert out['reflections']==N+5
 assert path[0]==(c+ds,2) and path[-1]==(c+dt,8)
 for A,B in zip(path[:-2],path[1:-1]):assert not ns['on'](A,B,path[-1])
 return {'c':str(c),'Ds':str(ds),'Dt':str(dt),'tau':str(tau),'delta':list(map(str,delta)),'iteration_steps':steps,**out}
rows=[run(c,ds,dt) for c in [Q(1),Q(3,2),Q(11),Q(22),Q(121)] for ds,dt in [(0,0),(0,1),(1,0),(1,3),(Q(2,3),Q(5,7)),(11,1),(Q(29,2),Q(7,3))]]
out={'status':'PRESCRIBED_ALL_FORMULA_CONTROLS_PASS','discovery':False,'validator_reuse':str(src),'rows':rows,'reflections':sum(r['reflections'] for r in rows),'guards':sum(r['wall_leg_guards'] for r in rows),'whole_goal_complete':False}
(P/'tooth-free-variable-portals-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='rows'}))
