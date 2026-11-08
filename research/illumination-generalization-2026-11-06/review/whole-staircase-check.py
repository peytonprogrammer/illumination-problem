"""Prescribed exact identities and earlier-target roof-corner controls; no search."""
from pathlib import Path
from fractions import Fraction as F
from math import floor,ceil
import ast,json,hashlib
HERE=Path(__file__).resolve().parent
src=HERE/'staircase-floor-check.py';tree=ast.parse(src.read_text());ns={'F':F}
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef)],type_ignores=[]),str(src),'exec'),ns)
verify=ns['verify']
def fold(z,L):return L-abs(z%(2*L)-L)
# Exact symbolic polynomial arithmetic, not sampling the factor identities.
def add(a,b):
 out=dict(a)
 for e,c in b.items():out[e]=out.get(e,0)+c
 return {e:c for e,c in out.items() if c}
def mul(a,b):
 out={}
 for e,c in a.items():
  for f,d in b.items():
   g=tuple(x+y for x,y in zip(e,f));out[g]=out.get(g,0)+c*d
 return {e:c for e,c in out.items() if c}
def scale(a,c):return {e:v*c for e,v in a.items() if v*c}
O={(0,0):1};X={(1,0):1};Y={(0,1):1};p=mul(X,Y);s=add(X,Y)
onep=add(O,scale(p,-1))
E1=add(mul(onep,add(add(p,O),scale(X,-1))),scale(mul(p,add(O,scale(Y,-1))),-2))
E2=add(mul(onep,add(add(p,O),scale(Y,-1))),scale(mul(p,add(O,scale(X,-1))),-2))
formula=add(add(scale(O,2),scale(s,-1)),add(mul(p,add(scale(s,3),scale(O,-4))),scale(mul(p,p),-2)))
assert add(E1,E2)==formula
# Substitute p=x²,s=2x and compare with2(1-x)²(1+x-x²), symbolically.
u={(0,):1};x={(1,):1};x2=mul(x,x)
f=add(add(scale(u,2),scale(x,-2)),add(mul(x2,add(scale(x,6),scale(u,-4))),scale(mul(x2,x2),-2)))
fact=scale(mul(mul(add(u,scale(x,-1)),add(u,scale(x,-1))),add(add(u,x),scale(x2,-1))),2)
assert f==fact
# Substitute s=1+p and compare with(1-p)².
t={(1,):1};st=add(u,t)
f2=add(add(scale(u,2),scale(st,-1)),add(mul(t,add(scale(st,3),scale(u,-4))),scale(mul(t,t),-2)))
assert f2==mul(add(u,scale(t,-1)),add(u,scale(t,-1)))
metric_controls=0
for alpha in (F(1,10),F(1,2),F(3,4),F(9,10),F(99,100)):
 for beta in (F(1,10),F(1,2),F(3,4),F(9,10),F(99,100)):
  for lam in (F(11,10),F(3,2),F(2),F(3),F(10)):
   for mu in (F(11,10),F(3,2),F(2),F(3),F(10)):
    Fv=(lam-1)*(1-beta)<=beta*(1-alpha)
    Ft=(mu-1)*(1-alpha)<=alpha*(1-beta)
    Rv=mu*min(2,1+(1-beta)/(alpha*beta))>=2
    Rh=lam*min(2,1+(1-alpha)/(alpha*beta))>=2
    assert Fv or Ft or Rv or Rh
    metric_controls+=1
# Deliberate raw corner candidates: BOTH kinds of roof corner and actual seam target.
results=[]
for name,tau,yt in [('right-roof-corner',F(38,7),F(5)),('left-roof-corner',F(5),F(11,2)),('roof-corner-seam-target',F(38,7),F(4))]:
 A,b,a,c,d,H=map(F,(8,4,3,3,4,8));S=(F(7),F(1));xs,ys=S;Hs=c-ys;g=d-c;Ht=yt-d;h=H-d;K=F(8)
 z=xs+Hs*tau-2*A;w=xs+(Hs+g)*tau-2*A-K
 assert abs(z)<b and abs(w)<a
 roof=w+tau*h;assert (roof/a).denominator==1
 endpoint=fold(w+tau*(2*h-Ht),a);upward=fold(w+tau*Ht,a)
 assert endpoint==upward and 0<endpoint<a
 T=(endpoint,yt)
 times={ys,c,d,yt}
 stages=[(ys,c,xs,A),(c,d,z,b),(d,yt,w,a)]
 for lo,hi,start,width in stages:
  for j in range(floor(start/width)-1,ceil((start+tau*(hi-lo))/width)+2):
   yy=lo+(j*width-start)/tau
   if lo<yy<hi:times.add(yy)
 def pt(y):
  if y<=c:return fold(xs+tau*(y-ys),A),y
  if y<=d:return fold(z+tau*(y-c),b),y
  return fold(w+tau*(y-d),a),y
 path=[pt(y) for y in sorted(times) if y<=yt];assert path[-1]==T
 V=[tuple(map(F,p)) for p in [(0,0),(A,0),(A,c),(b,c),(b,d),(a,d),(a,H),(0,H)]]
 r=verify(name,V,path);r.update(raw_roof_corner=[str(fold(roof,a)),str(H)],earlier_target=list(map(str,T)),slope=str(tau));results.append(r)
out={'status':'EXACT_CANDIDATE_IDENTITIES_AND_EARLIER_TARGET_CONTROLS_PASS','symbolic_polynomial_identities':3,'prescribed_metric_controls':metric_controls,'roof_corner_prefix_controls':3,'actual_contacts':sum(x['contacts'] for x in results),'actual_wall_checks':sum(x['checks'] for x in results),'results':results,'whole_goal_complete':False,'independently_accepted':False,'limits':'Supporting checks only. Whole arbitrary-real staircase theorem remains unreviewed candidate; not mainW21 resolution.','source_sha256':{p:hashlib.sha256((HERE/p).read_bytes()).hexdigest() for p in ('whole-staircase-candidate.md','whole-staircase-check.py','staircase-floor-check.py')}}
(HERE/'whole-staircase-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='results'}))
