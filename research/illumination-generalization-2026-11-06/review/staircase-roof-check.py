"""Independent prescribed controls of peer roof proof; actual first arrival checked."""
from pathlib import Path
from fractions import Fraction as F
from math import floor,ceil
import ast,json,hashlib
HERE=Path(__file__).resolve().parent
p=HERE/'staircase-floor-check.py';mod=ast.parse(p.read_text());ns={'F':F}
exec(compile(ast.Module(body=[n for n in mod.body if isinstance(n,ast.FunctionDef)],type_ignores=[]),str(p),'exec'),ns)
verify=ns['verify'];sub=ns['sub'];cross=ns['cross']
def fold(z,L):return L-abs(z%(2*L)-L)
rows=[
 ('pair-v-equality',(6,4,3,2,3,6),(F(5),F(1)),(F(1),F(5))),
 ('whole-H-equality-four-conditions-fail',(10,4,3,3,4,12),(F(9),F(1)),(F(1),F(23,2))),
 ('both-endpoint-seams',(6,4,3,2,3,9),(F(4),F(1)),(F(1),F(3))),
 ('target-center',(7,3,1,1,2,6),(F(6),F(1,2)),(F(1,2),F(4)))]
results=[]
for name,dims,S,T in rows:
 A,b,a,c,d,H=map(F,dims);xs,ys=S;xt,yt=T;Hs=c-ys;g=d-c;h=H-d;Ht=yt-d;T0=Hs+g;v=2*h-Ht;D=T0+v
 assert v>=2*T0 and 0<=Ht<h
 theta=(2*A-xs)/Hs;K=2*b*floor(g*theta/(2*b)+F(1,2));R=b*T0/Hs
 Ulo=max(g*theta-R,K-a);Uhi=min(g*theta+R,K+a);ell=Uhi-Ulo
 assert ell>a
 J=((Ulo-xs+2*A)/T0,(Uhi-xs+2*A)/T0);assert 0<J[0]<J[1]
 Zlo=xs+D*J[0]-2*A-K;Zhi=xs+D*J[1]-2*A-K;assert Zhi-Zlo>3*a
 u=min(xt,a-xt);shift=0 if xt<=a/2 else a;mid=(Zlo+Zhi)/2
 center=shift+2*a*floor((mid-shift)/(2*a)+F(1,2));images=[center-u,center+u]
 candidates=[]
 for Y in images:
  assert Zlo<Y<Zhi and fold(Y,a)==xt
  tau=(2*A+K+Y-xs)/D;assert J[0]<tau<J[1]
  roof=xs+(T0+h)*tau-2*A-K
  candidates.append((tau,roof,(roof/a).denominator==1))
 assert 0<candidates[1][1]-candidates[0][1]<a
 tau,roof,bad=next(x for x in candidates if not x[2]);z=xs+Hs*tau-2*A;w=xs+T0*tau-2*A-K
 assert abs(z)<b and abs(w)<a
 end=d+v;times={ys,c,d,d+h,end}
 stages=[(ys,c,xs,A),(c,d,z,b),(d,end,w,a)]
 for lo,hi,start,width in stages:
  for j in range(floor(start/width)-1,ceil((start+tau*(hi-lo))/width)+2):
   eta=lo+(j*width-start)/tau
   if lo<eta<hi:times.add(eta)
 def point(eta):
  if eta<=c:return (fold(xs+tau*(eta-ys),A),eta)
  if eta<=d:return (fold(z+tau*(eta-c),b),eta)
  return (fold(w+tau*(eta-d),a),d+fold(eta-d,h))
 full=[point(e) for e in sorted(times)];assert full[0]==S and full[-1]==T
 # Independently resolve first actual T, including any upward visit before the roof.
 path=[full[0]];truncated=False
 for p,q in zip(full,full[1:]):
  delta=sub(q,p)
  if cross(sub(T,p),delta)==0:
   t=(T[0]-p[0])/delta[0]
   if 0<t<=1:
    path.append(T);truncated=q!=T or q!=full[-1];break
  path.append(q)
 assert path[-1]==T
 V=[tuple(map(F,p)) for p in [(0,0),(A,0),(A,c),(b,c),(b,d),(a,d),(a,H),(0,H)]]
 out=verify(name,V,path);out.update(slope=str(tau),overlap=str(ell),Ht=str(Ht),earlier_target_truncated=truncated,full_path_nodes=len(full),selected_roof_phase=str(roof));results.append(out)
out={'status':'INDEPENDENT_ROOF_WINDOWS_ACTUAL_WALLS_AND_FIRST_TARGET_PASS','fixed_controls':len(results),'contacts':sum(x['contacts'] for x in results),'checks':sum(x['checks'] for x in results),'results':results,'whole_goal_complete':False,'verification':'Independent constructor and own pure wall verifier; prescribed fixed inputs only; no peer script executed','source_sha256':{n:hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in ('staircase-roof-check.py','staircase-floor-check.py','../construction/staircase-roof-proof.md')}}
(HERE/'staircase-roof-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='results'}))
