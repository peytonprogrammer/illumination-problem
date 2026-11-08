"""Prescribed validation of generic signed-target charts and nine literal h3 rows."""
from fractions import Fraction as Q
from pathlib import Path
import ast,json
P=Path(__file__).resolve().parent;src=P.parent/'review/resumed-exact-check.py';ns={'Q':Q};names={'vec','det','dot','edges','on','location','intersect','simple','path_check','fold'};mod=ast.parse(src.read_text());exec(compile(ast.Module(body=[n for n in mod.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[]),str(src),'exec'),ns);fold=ns['fold']
a=ast.parse((P/'independent-depth-zigzag-check.py').read_text());exec(compile(ast.Module(body=[n for n in a.body if isinstance(n,ast.FunctionDef) and n.name=='arm'],type_ignores=[]),'own-arm','exec'),{'Q':Q,'fold':fold},ns);arm=ns['arm']
def allowed(y,G,mouths):return 1<=y<=G-1 and all(y<=a-1 or y>=b+1 for a,b in mouths)
def run(kind,h,d,m,sigma,K,c,ds,dt):
 c,ds,dt=map(Q,(c,ds,dt));G=2*h+4 if kind=='A0' else 2*h+d+4;second=h+4 if kind=='A0' else h+d+2;t=2*h+2
 assert (2+K-sigma*t)%(2*G)==0 and K>0
 nominal=[fold(2+Q(j*K,2*m),G) for j in range(1,2*m)]
 assert all(allowed(y,G,[(h,h+2),(second,second+2)] if j%2 else [(1,3),(2*h+1,2*h+3)]) for j,y in enumerate(nominal,1))
 L=2*m*c+ds+dt;N=0
 while True:
  tau=(K+2*N)/L;n=[(D*tau/2+Q(1,2))//1 for D in (ds,dt)];M=sum(n);assert M>=N
  if M==N:break
  N=M
 delta=[D*tau-2*k for D,k in zip((ds,dt),n)];assert all(-1<x<1 for x in delta)
 start=2+delta[0];end=start+2*m*c*tau;events={j*c for j in range(2*m+1)}
 for j in range(1,int(end//G)+1):
  z=(j*G-start)/tau
  if 0<z<2*m*c:events.add(z)
 core=[(fold(c-z,c),fold(start+tau*z,Q(G))) for z in sorted(events)]
 assert core[-1]==(c,t-sigma*delta[1])
 ev={Q(0),dt};a=1-sigma*delta[1];b=a+sigma*tau*dt
 for j in range(int(min(a,b)//2)-1,int(max(a,b)//2)+2):
  r=(2*j-a)/(sigma*tau)
  if 0<r<dt:ev.add(r)
 target=[(c+r,t-1+fold(a+sigma*tau*r,Q(2))) for r in sorted(ev)]
 path=arm(c,ds,tau,n[0])+core[1:]+target[1:]
 ws=ds+Q(1,13);wt=dt+Q(2,17);aa=Q(4,7);bb=Q(3,11)
 poly=[(0,0),(c,0),(c,1),(c+ws,1),(c+ws,3),(c,3),(c,2*h+1),(c+wt,2*h+1),(c+wt,2*h+3),(c,2*h+3),(c,G),(0,G),(0,second+2),(-bb,second+2),(-bb,second),(0,second),(0,h+2),(-aa,h+2),(-aa,h),(0,h)]
 ns['simple'](poly);z=ns['path_check'](poly,path);assert z['reflections']==N+2*m-1+(2+K)//G
 assert path[0]==(c+ds,2) and path[-1]==(c+dt,t)
 for A,B in zip(path[:-2],path[1:-1]):assert not ns['on'](A,B,path[-1])
 return {'kind':kind,'h':h,'d':d,'m':m,'sigma':sigma,'K':K,'c':str(c),'Ds':str(ds),'Dt':str(dt),'nominal_sides':list(map(str,nominal)),**z}
profiles=[('A0',4,0,2,-1,84)]
for h,d in [(4,2),(4,3),(4,1000),(5,3),(5,100),(20,10),(101,51)]:
 G=2*h+d+4;profiles.append(('A1',h,d,2,-1,8*G-2*h-4))
for d,m,sg,K in [(3,2,-1,16),(4,2,-1,18),(5,2,-1,20),(8,4,1,114),(9,4,1,120),(11,4,1,48),(12,4,1,50),(13,2,-1,36),(14,2,-1,38)]:profiles.append(('A1',3,d,m,sg,K))
rows=[run(*p,c,ds,dt) for p in profiles for c,ds,dt in [(Q(3,2),0,Q(11,7)),(11,1,3),(Q(7,3),Q(17,5),Q(29,7)),(121,0,0)]]
out={'status':'PRESCRIBED_FULL_GUARD_AND_ACTUAL_PATH_CHECKS_PASS','discovery':False,'validator_reuse':str(src),'rows':rows,'reflections':sum(r['reflections'] for r in rows),'guards':sum(r['wall_leg_guards'] for r in rows),'whole_goal_complete':False};(P/'low-band-robust-core-physical.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='rows'}))
