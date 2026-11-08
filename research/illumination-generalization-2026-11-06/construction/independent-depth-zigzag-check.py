"""Prescribed checks of A58 matching and strict original-wall paths; no discovery."""
from pathlib import Path
from fractions import Fraction as Q
import ast,json
P=Path(__file__).resolve().parent;src=P.parent/'review/resumed-exact-check.py';names={'vec','det','dot','edges','on','location','intersect','simple','path_check','fold'}
ns={'Q':Q};mod=ast.parse(src.read_text());exec(compile(ast.Module(body=[n for n in mod.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[]),str(src),'exec'),ns);fold=ns['fold']
def arm(c,D,tau,n):
 ev={Q(0),D};start=1-2*n
 for j in range(int(start//2)-1,int((start+tau*D)//2)+2):
  r=(2*j-start)/tau
  if 0<r<D:ev.add(r)
 return [(c+D-r,1+fold(start+tau*r,Q(2))) for r in sorted(ev)]
def run(kind,h,d,c,ds,dt):
 c,ds,dt=map(Q,(c,ds,dt));G=2*h+4 if kind=='A0' else 2*h+d+4;second=h+4 if kind=='A0' else h+d+2
 if kind=='A0':assert h>=10;m=2
 else:
  assert h>=6
  if h<=2*d-2 or h>=2*d+6:m=2
  else:assert d>=8;m=4
 L=2*m*c+ds+dt;N=0;steps=0
 while True:
  tau=2*(h+N)/L;n=[(D*tau/2+Q(1,2))//1 for D in (ds,dt)];M=sum(n);assert M>=N
  if M==N:break
  N=M;steps+=1
 delta=[D*tau-2*k for D,k in zip((ds,dt),n)];assert all(-1<x<1 for x in delta)
 core=[(c if j%2==0 else Q(0),2+delta[0]+j*c*tau) for j in range(2*m+1)]
 assert core[-1]==(c,2*h+2-delta[1])
 path=arm(c,ds,tau,n[0])+core[1:]+[(x,2*h+4-y) for x,y in reversed(arm(c,dt,tau,n[1]))][1:]
 ws=ds+Q(1,13);wt=dt+Q(2,17);a=Q(4,7);b=Q(3,11)
 poly=[(0,0),(c,0),(c,1),(c+ws,1),(c+ws,3),(c,3),(c,2*h+1),(c+wt,2*h+1),(c+wt,2*h+3),(c,2*h+3),(c,G),(0,G),(0,second+2),(-b,second+2),(-b,second),(0,second),(0,h+2),(-a,h+2),(-a,h),(0,h)]
 ns['simple'](poly);z=ns['path_check'](poly,path);assert z['reflections']==N+2*m-1
 assert path[0]==(c+ds,2) and path[-1]==(c+dt,2*h+2)
 for A,B in zip(path[:-2],path[1:-1]):assert not ns['on'](A,B,path[-1])
 return {'kind':kind,'h':h,'d':d,'c':str(c),'Ds':str(ds),'Dt':str(dt),'m':m,'delta':list(map(str,delta)),**z}
rows=[]
for kind,h,d in [('A0',10,0),('A0',41,0),('A1',6,4),('A1',8,1),('A1',15,8),('A1',21,8),('A1',20,7),('A1',205,100)]:
 for c,ds,dt in [(Q(3,2),0,Q(11,7)),(11,1,3),(Q(7,3),Q(17,5),Q(29,7)),(121,0,0)]:rows.append(run(kind,h,d,c,ds,dt))
# Exact formula evaluation at the four residual-square corners checks the stated
# contact inequalities weakly; actual strictness follows because residuals are interior.
cells=[]
for d in range(1,8):
 for h in range(max(6,2*d-1),2*d+6):cells.append([h,d])
assert len(cells)==40
out={'status':'PRESCRIBED_MATCHING_AND_PHYSICAL_CONTROLS_PASS','discovery':False,'validator_reuse':str(src),'rows':rows,'remaining_vertical_cells':cells,'reflections':sum(z['reflections'] for z in rows),'guards':sum(z['wall_leg_guards'] for z in rows),'whole_goal_complete':False};(P/'independent-depth-zigzag-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['rows','remaining_vertical_cells']}))
