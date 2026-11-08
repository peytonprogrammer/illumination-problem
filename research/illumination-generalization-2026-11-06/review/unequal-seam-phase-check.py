"""R50 exact stationary formula, periodicity and prescribed physical three-chart witnesses."""
from fractions import Fraction as Q
from pathlib import Path
from math import gcd
import importlib.util,json,ast
R=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('own',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
a=ast.parse((R/'minimal-prefix-physical-check.py').read_text());exec(compile(ast.Module(body=[n for n in a.body if isinstance(n,ast.FunctionDef) and n.name=='events'],type_ignores=[]),'own events only','exec'))
def phase(c,w,H):
 n=int((Q(w,c)*(H-Q(1,2))+Q(1,2))//1);tau=Q(H+n,c+w);m=w*tau-n;assert -Q(1,2)<m<Q(1,2)
 return n,tau,m
arith=0
for c in range(1,25):
 for w in range(1,2*c+1):
  for H in range(2,26):
   n,tau,m=phase(Q(c),Q(w),Q(H));x=Q(0);seen=set()
   while x not in seen:
    seen.add(x);nn=int((w*x+Q(1,2))//1);y=Q(H+nn,c+w)
    if y==x:break
    assert y>x;x=y
   assert x==tau and nn==n
   period=c//gcd(c,w);assert phase(Q(c),Q(w),Q(H+period))[2]==m;arith+=1

def polygon(c,G,s,t,ws,wt,Y,v):
 p=[(Q(0),Q(0)),(c,Q(0))]
 for mid,w in [(s,ws),(t,wt)]:p.extend([(c,mid-1),(c+w,mid-1),(c+w,mid+1),(c,mid+1)])
 p.extend([(c,G),(0,G),(0,Y+2),(-v,Y+2),(-v,Y),(0,Y)])
 while True:
  if p[-1]==p[0]:p.pop()
  drop=next((i for i in range(len(p)) if p[i]==p[i-1] or g.det(g.vec(p[i-1],p[i]),g.vec(p[i],p[(i+1)%len(p)]))==0),None)
  if drop is None:break
  p.pop(drop)
 p=[tuple(map(Q,z)) for z in p];g.simple(p);return p

def fararm(c,w,mid,y,tau,sign):
 path=[]
 for r in events(y-(mid-1),sign*tau,2*w,w):path.append((c+(r if r<=w else 2*w-r),mid-1+g.fold(y-(mid-1)+sign*tau*r,Q(2))))
 return path

def candidates(c,a,b,wa,wb):
 H=(b-a)/2;mean=(a+b)/2;na,ta,ma=phase(c,wa,H);nb,tb,mb=phase(c,wb,H);assert ma*mb>0
 source=list(reversed(fararm(c,wa,a,a+2*ma,ta,-1)))+[(Q(0),mean+ma),(c,b)]
 target=[(c,a),(Q(0),mean-mb),(c,b-2*mb)]+fararm(c,wb,b,b-2*mb,tb,1)[1:]
 return [(source,mean+ma,'sourcefar'),(target,mean-mb,'targetfar')]

def endfold(path,G):
 out=[(path[0][0],g.fold(path[0][1],G))]
 for a,b in zip(path,path[1:]):
  times={Q(1)}
  if a[1]!=b[1]:
   lo,hi=sorted([a[1],b[1]])
   for j in range(int(lo//G)-1,int(hi//G)+2):
    z=j*G;r=(z-a[1])/(b[1]-a[1])
    if 0<r<1:times.add(r)
  for r in sorted(times):
   x=a[0]+r*(b[0]-a[0]);y=a[1]+r*(b[1]-a[1]);out.append((x,g.fold(y,G)))
 return out
fixtures=[(3,1,2,4),(3,1,2,7),(4,1,3,5),(4,1,3,10),(5,1,3,3),(5,1,3,8),(6,1,2,11),(7,1,4,5),(Q(7,3),Q(1,4),Q(2,5),3)]
rows=[]
for cc,wws,wwt,HH in fixtures:
 c,ws,wt,H=map(Q,[cc,wws,wwt,HH])
 for chart in ['normal','bottom','roof']:
  if chart=='normal':s=Q(2);t=2*H+2;G=t+4;a,b,wa,wb=s,t,ws,wt;ell=(s+t)/2
  elif chart=='bottom':s=H-2;t=H+2;G=t+3;a,b,wa,wb=-t,s,wt,ws;ell=Q(2)
  else:s=Q(2);t=Q(6);G=H+4;a,b,wa,wb=s,2*G-t,ws,wt;ell=G-2
  for start in [True,False]:
   Y=ell if start else ell-2
   for v in [Q(1,3),Q(17)]:
    V=polygon(c,G,s,t,ws,wt,Y,v)
    options=[]
    for path,turn,name in candidates(c,a,b,wa,wb):
     yy=g.fold(turn,G)
     if (yy<ell)==start:options.append((path,name))
    assert len(options)==1
    path,name=options[0];path=endfold(path,G)
    if path[0]!=(c,s):path=list(reversed(path))
    assert path[0]==(c,s) and path[-1]==(c,t)
    assert not any(g.on(u,v,path[-1]) for u,v in zip(path[:-2],path[1:-1]));res=g.path_check(V,path)
    rows.append({'c':str(c),'source_width':str(ws),'target_width':str(wt),'H':str(H),'chart':chart,'opening_starts':start,'opposite_width':str(v),'chosen':name,'polygon':V,'path':path,**res})
out={'status':'R50_FORMULA_PERIODICITY_AND_ACTUAL_THREE_CHART_WITNESSES_PASS','arithmetic_cases':arith,'paths':len(rows),'reflections':sum(r['reflections'] for r in rows),'wall_leg_guards':sum(r['wall_leg_guards'] for r in rows),'rows':rows,'discovery':False,'whole_goal_complete':False}
(R/'unequal-seam-phase-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='rows'}))
