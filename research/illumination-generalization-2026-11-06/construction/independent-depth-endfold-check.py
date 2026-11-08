"""Prescribed exact all-wall checks of the endfold supplement. No discovery."""
from pathlib import Path
from fractions import Fraction as Q
import ast,json
P=Path(__file__).resolve().parent;src=P.parent/'review/resumed-exact-check.py';names={'vec','det','dot','edges','on','location','intersect','simple','path_check','fold'};ns={'Q':Q};mod=ast.parse(src.read_text());exec(compile(ast.Module(body=[n for n in mod.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[]),str(src),'exec'),ns);fold=ns['fold']
# Reuse only our frozen prescribed arm constructor, not its controls or execution.
a=ast.parse((P/'independent-depth-zigzag-check.py').read_text());exec(compile(ast.Module(body=[n for n in a.body if isinstance(n,ast.FunctionDef) and n.name=='arm'],type_ignores=[]),'own-arm','exec'),{'Q':Q,'fold':fold},ns);arm=ns['arm']
def run(kind,h,d,c,ds,dt):
 c,ds,dt=map(Q,(c,ds,dt));G=2*h+4 if kind=='A0' else 2*h+d+4;second=h+4 if kind=='A0' else h+d+2
 if kind=='A0':assert h>=6
 else:assert h>=3 and (h>=d+2 or d>=3*h+6)
 K=2*h+2*G;L=4*c+ds+dt;N=0
 while True:
  tau=(K+2*N)/L;n=[(D*tau/2+Q(1,2))//1 for D in (ds,dt)];M=sum(n);assert M>=N
  if M==N:break
  N=M
 delta=[D*tau-2*k for D,k in zip((ds,dt),n)];assert all(-1<x<1 for x in delta)
 start=2+delta[0];events={Q(0),c,2*c,3*c,4*c}
 for j in (1,2):events.add((j*G-start)/tau)
 core=[(fold(c-z,c),fold(start+tau*z,Q(G))) for z in sorted(events)]
 assert core[-1]==(c,2*h+2-delta[1])
 path=arm(c,ds,tau,n[0])+core[1:]+[(x,2*h+4-y) for x,y in reversed(arm(c,dt,tau,n[1]))][1:]
 ws=ds+Q(1,13);wt=dt+Q(2,17);a=Q(4,7);b=Q(3,11)
 poly=[(0,0),(c,0),(c,1),(c+ws,1),(c+ws,3),(c,3),(c,2*h+1),(c+wt,2*h+1),(c+wt,2*h+3),(c,2*h+3),(c,G),(0,G),(0,second+2),(-b,second+2),(-b,second),(0,second),(0,h+2),(-a,h+2),(-a,h),(0,h)]
 ns['simple'](poly);z=ns['path_check'](poly,path);assert z['reflections']==N+5
 assert path[0]==(c+ds,2) and path[-1]==(c+dt,2*h+2)
 for A,B in zip(path[:-2],path[1:-1]):assert not ns['on'](A,B,path[-1])
 return {'kind':kind,'h':h,'d':d,'c':str(c),'Ds':str(ds),'Dt':str(dt),**z}
rows=[]
for kind,h,d in [('A0',6,0),('A0',7,0),('A0',10,0),('A1',3,1),('A1',4,2),('A1',5,3),('A1',6,4),('A1',19,17),('A1',3,15),('A1',4,18),('A1',5,21),('A1',3,1000)]:
 for c,ds,dt in [(Q(3,2),0,Q(11,7)),(11,1,3),(Q(7,3),Q(17,5),Q(29,7)),(121,0,0)]:rows.append(run(kind,h,d,c,ds,dt))
out={'status':'PRESCRIBED_ENDFOLD_ALL_WALL_CHECKS_PASS','discovery':False,'validator_reuse':str(src),'rows':rows,'reflections':sum(z['reflections'] for z in rows),'guards':sum(z['wall_leg_guards'] for z in rows),'whole_goal_complete':False};(P/'independent-depth-endfold-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='rows'}))
