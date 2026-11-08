"""R52 prescribed weighted-matching, exact irrational, and actual-path checks; no discovery."""
from pathlib import Path
from fractions import Fraction as Q
import ast,importlib.util,json,hashlib,itertools
R=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('g',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
ns={'Q':Q,'g':g};tree=ast.parse((R/'tooth-free-core-independent-check.py').read_text());exec(compile(ast.Module(body=[z for z in tree.body if isinstance(z,ast.FunctionDef) and z.name=='trace'],type_ignores=[]),'own actual firsthit','exec'),ns)
def match(L0,K,vs,vt,ds,dt):
 L=L0+ds+dt;vs,vt,ds,dt=map(Q,(vs,vt,ds,dt));Tbar=(K+vs+vt)/L0
 bounds=tuple(int(d*Tbar/(2*v)+Q(1,2)) for d,v in zip([ds,dt],[vs,vt]));n=(0,0);steps=0
 while True:
  tau=(K+2*vs*n[0]+2*vt*n[1])/L
  nn=tuple(int(d*tau/(2*v)+Q(1,2)) for d,v in zip([ds,dt],[vs,vt]));assert all(a<=b<=c for a,b,c in zip(n,nn,bounds))
  if n==nn:break
  n=nn;steps+=1;assert steps<=sum(bounds)
 delta=tuple(d*tau-2*v*k for d,v,k in zip([ds,dt],[vs,vt],n));assert all(-v<x<v for v,x in zip([vs,vt],delta))
 assert L0*tau==K-sum(delta)
 return tau,n,delta,steps,bounds
rows=[]
for c,v,hs,ht in [(Q(1),Q(1),Q(1,2),Q(1)),(Q(3),Q(5),Q(2),Q(3)),(Q(22),Q(7),Q(7),Q(1)),(Q(1,3),Q(2),Q(1),Q(2,3)),(Q(121),Q(13),Q(2,7),Q(5,3))]:
 for ds,dt in [(Q(0),Q(0)),(Q(0),Q(1)),(Q(1),Q(0)),(Q(1),Q(3)),(Q(2,3),Q(5,7)),(Q(11),Q(1))]:
  tau,n,delta,steps,bounds=match(4*c,28*v,hs,ht,ds,dt);ws,wt=ds+Q(1,127),dt+Q(3,131);a,b=Q(1,137),Q(100003)
  V=[(0,0),(c,0),(c,2*v-hs),(c+ws,2*v-hs),(c+ws,2*v+hs),(c,2*v+hs),(c,8*v-ht),(c+wt,8*v-ht),(c+wt,8*v+ht),(c,8*v+ht),(c,11*v),(0,11*v),(0,8*v),(-b,8*v),(-b,6*v),(0,6*v),(0,5*v),(-a,5*v),(-a,3*v),(0,3*v)]
  V=[tuple(map(Q,p)) for p in V];g.simple(V)
  path,_=ns['trace'](V,(c+ds,2*v),(c+dt,8*v),(Q(-1),(-1)**n[0]*tau),sum(n)+5);out=g.path_check(V,path)
  rows.append({'c':c,'v':v,'hs':hs,'ht':ht,'Ds':ds,'Dt':dt,'tau':tau,'indices':n,'deltas':delta,'bounds':bounds,'steps':steps,**out})
# Quadratic field a+b sqrt(2), compared EXACTLY using rational squares.
def A(x):return x if isinstance(x,tuple) else (Q(x),Q(0))
def plus(x,y):x,y=A(x),A(y);return(x[0]+y[0],x[1]+y[1])
def neg(x):x=A(x);return(-x[0],-x[1])
def sub(x,y):return plus(x,neg(y))
def mul(x,y):x,y=A(x),A(y);return(x[0]*y[0]+2*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def div(x,y):
 y=A(y);den=y[0]**2-2*y[1]**2;assert den;return mul(x,(y[0]/den,-y[1]/den))
def sign(x):
 a,b=A(x)
 if b==0:return (a>0)-(a<0)
 if a>=0 and b>0:return 1
 if a<=0 and b<0:return -1
 cmp=(a*a>2*b*b)-(a*a<2*b*b)
 return cmp if a>0 else -cmp
def floorq(x):
 a,b=A(x);lo=min(a+b,a+2*b)//1;hi=max(a+b,a+2*b)//1+1
 while hi-lo>1:
  m=(lo+hi)//2
  if sign(sub(x,m))>=0:lo=m
  else:hi=m
 assert sign(sub(x,lo))>=0 and sign(sub(x,lo+1))<0
 return int(lo)
surds=[]
for ds,dt in [(Q(0),Q(1)),(Q(1),Q(3)),(Q(7,3),Q(5,2)),(Q(11),Q(1))]:
 vs=(Q(0),Q(1,2));vt=A(1);L=4+ds+dt;n=(0,0);steps=0
 while True:
  tau=div(plus(28,plus(mul(mul(2,vs),n[0]),2*n[1])),L)
  nn=(floorq(plus(div(mul(ds,tau),mul(2,vs)),Q(1,2))),floorq(plus(div(mul(dt,tau),2),Q(1,2))))
  assert all(a<=b for a,b in zip(n,nn))
  if nn==n:break
  n=nn;steps+=1;assert steps<10000
 delta=[sub(mul(d,tau),mul(mul(2,h),k)) for d,h,k in zip([ds,dt],[vs,vt],n)]
 for de,h in zip(delta,[vs,vt]):assert sign(plus(de,h))>0 and sign(sub(h,de))>0
 assert sub(mul(4,tau),sub(28,plus(*delta)))==(Q(0),Q(0))
 surds.append({'Ds':ds,'Dt':dt,'half_heights':['sqrt(2)/2','1'],'tau_a_plus_b_sqrt2':tau,'indices':n,'deltas_a_plus_b_sqrt2':delta,'steps':steps,'actual_ray_replay':False})
out={'status':'R52_EXACT_WEIGHTED_MATCHING_AND_ACTUAL_PATHS_PASS','whole_goal_complete':False,'discovery':False,'actual_paths':len(rows),'reflections':sum(x['reflections'] for x in rows),'wall_leg_guards':sum(x['wall_leg_guards'] for x in rows),'rows':rows,'exact_incommensurable_arithmetic_controls':surds,'source_sha256':{f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ['resumed-exact-check.py','tooth-free-core-independent-check.py']}}
(R/'robust-portal-lift-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print({k:v for k,v in out.items() if k not in ['rows','source_sha256','exact_incommensurable_arithmetic_controls']})
