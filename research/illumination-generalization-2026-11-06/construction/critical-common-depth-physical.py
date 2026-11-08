"""Prescribed exact COMMON-depth paths on the original three exceptional rooms."""
from pathlib import Path
from fractions import Fraction as Q
import ast,json
P=Path(__file__).resolve().parent;src=P.parent/'review/resumed-exact-check.py';ns={'Q':Q};names={'vec','det','dot','edges','on','location','intersect','simple','path_check','fold'};mod=ast.parse(src.read_text());exec(compile(ast.Module(body=[n for n in mod.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[]),str(src),'exec'),ns);fold=ns['fold']
a=ast.parse((P/'independent-depth-zigzag-check.py').read_text());exec(compile(ast.Module(body=[n for n in a.body if isinstance(n,ast.FunctionDef) and n.name=='arm'],type_ignores=[]),'own-arm','exec'),{'Q':Q,'fold':fold},ns);arm=ns['arm'];rows=[]
for kind,h,d,G,m,K,sigma in [('A0',5,0,14,2,38,1),('A1',3,6,16,2,22,-1),('A1',3,10,20,4,46,1)]:
 for c,D in [(Q(3,2),Q(0)),(Q(11),Q(1,3)),(Q(7,3),Q(13,5)),(Q(1),Q(50,7))]:
  n=(D*K/(4*m*c)+Q(1,2))//1;tau=(Q(K,2)+2*n)/(m*c+D);delta=D*tau-2*n;assert -1<delta<1;start=2+delta;ev={j*c for j in range(2*m+1)};end=start+2*m*c*tau
  for j in range(1,int(end//G)+1):
   z=(j*G-start)/tau
   if 0<z<2*m*c:ev.add(z)
  core=[(fold(c-z,c),fold(start+tau*z,Q(G))) for z in sorted(ev)];t=2*h+2;assert core[-1]==(c,t-sigma*delta)
  ev={Q(0),D};a=1-sigma*delta;b=a+sigma*tau*D
  for j in range(int(min(a,b)//2)-1,int(max(a,b)//2)+2):
   rr=(2*j-a)/(sigma*tau)
   if 0<rr<D:ev.add(rr)
  target=[(c+rr,t-1+fold(a+sigma*tau*rr,Q(2))) for rr in sorted(ev)];path=arm(c,D,tau,n)+core[1:]+target[1:];ws=D+Q(1,37);wt=D+Q(1,43);aa=Q(47,5);bb=Q(1,29);second=h+4 if kind=='A0' else h+d+2
  poly=[(0,0),(c,0),(c,1),(c+ws,1),(c+ws,3),(c,3),(c,t-1),(c+wt,t-1),(c+wt,t+1),(c,t+1),(c,G),(0,G),(0,second+2),(-bb,second+2),(-bb,second),(0,second),(0,h+2),(-aa,h+2),(-aa,h),(0,h)];ns['simple'](poly);r=ns['path_check'](poly,path);assert r['reflections']==2*n+2*m-1+(2+K)//G
  for A,B in zip(path[:-2],path[1:-1]):assert not ns['on'](A,B,path[-1])
  rows.append({'kind':kind,'h':h,'d':d,'c':str(c),'D':str(D),'delta':str(delta),**r})
out={'status':'PRESCRIBED_ORIGINAL_COMMON_DEPTH_CONTROLS_PASS','discovery':False,'rows':rows,'validator_reuse':str(src),'whole_goal_complete':False};(P/'critical-common-depth-physical.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
