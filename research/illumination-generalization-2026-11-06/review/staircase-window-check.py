"""Independent prescribed exact controls of the frozen peer staircase argument."""
from fractions import Fraction as F
from pathlib import Path
from math import floor,ceil
import ast,json,hashlib
HERE=Path(__file__).resolve().parent
# Reuse our own pure actual finite-wall verifier without executing its fixed driver.
p=HERE/'wide-middle-boundary-controls.py';tree=ast.parse(p.read_text());ns={'F':F}
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef)],type_ignores=[]),str(p),'exec'),ns)
validate=ns['validate']
def fold(z,L):return L-abs(z%(2*L)-L)
rows=[
 ('rho-small-threshold',5,3,1,F(1),F(1),F(1),F(4),F(1,2)),
 ('rho-large-threshold',5,2,1,F(1),F(1,2),F(1),F(4),F(1,2)),
 ('both-endpoint-seams',5,2,1,F(1),F(1),F(0),F(2),F(1,2)),
 ('two-thresholds-equal',9,3,1,F(1),F(1,3),F(1,2),F(8),F(2,3))]
results=[]
for name,*raw in rows:
 A,b,a,Hs,g,Ht,xs,xt=map(F,raw);rho=g/Hs;D=Hs+g+Ht
 if rho<=(b-a)/(A-b):
  k=1+ceil(A*g/(b*Hs));K=2*k*b
  ratio=(Hs*K+g*xs)/(2*A*g);n=floor(ratio+F(1,2));regime='source_round'
 else:
  assert rho>=a/b
  n=1;theta=(2*A-xs)/Hs;K=2*b*floor(g*theta/(2*b)+F(1,2));regime='exit_round'
 theta=(2*n*A-xs)/Hs;R=b*(1+rho)
 assert n>=1 and K>=0 and abs(K-g*theta)+a<=R
 I=((2*n*A-xs-b)/Hs,(2*n*A-xs+b)/Hs)
 J=((2*n*A+K-xs-a)/(Hs+g),(2*n*A+K-xs+a)/(Hs+g))
 assert 0<I[0]<=J[0]<J[1]<=I[1]
 Zlo=xs+D*J[0]-2*n*A-K;Zhi=xs+D*J[1]-2*n*A-K
 image=min(sign*xt+2*a*(floor((Zlo-sign*xt)/(2*a))+1) for sign in (-1,1))
 assert Zlo<image<Zhi
 tau=(2*n*A+K+image-xs)/D;assert J[0]<tau<J[1]
 z=xs+Hs*tau-2*n*A;w=xs+(Hs+g)*tau-2*n*A-K
 assert abs(z)<b and abs(w)<a and fold(image,a)==xt
 ys=F(1);c=ys+Hs;d=c+g;yt=d+Ht;H=yt+1
 vertices=[tuple(map(F,p)) for p in [(0,0),(A,0),(A,c),(b,c),(b,d),(a,d),(a,H),(0,H)]]
 stages=[(ys,c,xs,A),(c,d,z,b),(d,yt,w,a)]
 times={ys,c,d,yt}
 for lo,hi,start,width in stages:
  for j in range(floor(start/width)-1,ceil((start+tau*(hi-lo))/width)+2):
   yy=lo+(j*width-start)/tau
   if lo<yy<hi:times.add(yy)
 def xat(y):
  if y<=c:return fold(xs+tau*(y-ys),A)
  if y<=d:return fold(z+tau*(y-c),b)
  return fold(w+tau*(y-d),a)
 path=[(xat(y),y) for y in sorted(times)]
 assert path[0]==(xs,ys) and path[-1]==(xt,yt)
 result=validate(name,vertices,path)
 result.update(regime=regime,slope=str(tau),Ht=str(Ht),source_seam=xs==b,window_containment_equality=abs(K-g*theta)+a==R)
 results.append(result)
out={'status':'INDEPENDENT_STAIRCASE_WINDOWS_AND_ACTUAL_WALLS_PASS','fixed_controls':len(rows),'checks':sum(x['checks'] for x in results),'contacts':sum(x['contacts'] for x in results),'results':results,'whole_goal_complete':False,'verification':'Independent constructor choices and own preexisting pure finite-wall verifier; no peer script executed, no discovery','source_sha256':{p:hashlib.sha256((HERE/p).read_bytes()).hexdigest() for p in ('staircase-window-check.py','wide-middle-boundary-controls.py','../construction/staircase-window-proof.md')}}
(HERE/'staircase-window-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='results'}))
