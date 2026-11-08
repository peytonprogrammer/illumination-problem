"""Prescribed A38 physical end folds, including flush-tooth existing reflections."""
from pathlib import Path
from fractions import Fraction as Q
import importlib.util,json,hashlib
R=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('own',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
def polygon(c,left,right,G):
 p=[(Q(0),Q(0)),(c,Q(0))]
 for lo,hi,w in right:p.extend([(c,lo),(c+w,lo),(c+w,hi),(c,hi)])
 p.extend([(c,G),(Q(0),G)])
 for lo,hi,w in reversed(left):p.extend([(Q(0),hi),(-w,hi),(-w,lo),(Q(0),lo)])
 p=[z for i,z in enumerate(p) if i==0 or z!=p[i-1]]
 if p[-1]==p[0]:p.pop()
 while any(g.det(g.vec(p[i-1],z),g.vec(z,p[(i+1)%len(p)]))==0 for i,z in enumerate(p)):
  p=[z for i,z in enumerate(p) if g.det(g.vec(p[i-1],z),g.vec(z,p[(i+1)%len(p)]))!=0]
 g.simple(p);return p

def prefix(D,t,n):
 k=n//2;sgn=1 if n%2==0 else-1;r=sgn+D*t-4*k;assert 0<r<2
 p=[(D,Q(1))]
 for j in range(1 if sgn==1 else 0,2*k+1):p.append((D-(2*j-sgn)/t,Q(2 if j%2 else 0)))
 if D:p.append((Q(0),r))
 return p,r

def far_return(c,s,a,D):
 w=Q(1);tau=Q(0);gap=a-s;assert gap>0
 for _ in range(10000):
  ns=int((D*tau/2+Q(1,2))//1);nt=int((w*tau/2+Q(1,2))//1);nxt=(gap+2*ns+2*nt)/(c+D+w)
  if nxt==tau:break
  assert nxt>tau;tau=nxt
 else:raise AssertionError('control finite matching cap')
 ps,rs=prefix(D,tau,ns);pt,rt=prefix(w,tau,nt)
 half=[(c+x,s-1+y) for x,y in ps]+[(-x,a+1-y) for x,y in reversed(pt)]
 return half+[(x,2*a-y) for x,y in reversed(half[:-1])]

def fold_path(p,G):
 out=[(p[0][0],g.fold(p[0][1],G))]
 for a,b in zip(p,p[1:]):
  events=[]
  for k in range(int(min(a[1],b[1])//G)-1,int(max(a[1],b[1])//G)+2):
   y=k*G
   if min(a[1],b[1])<y<max(a[1],b[1]):
    f=(y-a[1])/(b[1]-a[1]);x=a[0]+f*(b[0]-a[0]);events.append((f,(x,g.fold(y,G))))
  out.extend(z for _,z in sorted(events));out.append((b[0],g.fold(b[1],G)))
 return[z for i,z in enumerate(out) if i==0 or z!=out[i-1]]
rows=[]
c=Q(4);G=Q(20);s=Q(4);t=Q(16)
for ti in (t,t+2*G,-t,2*G-t):
 a=(s+ti)/2;level=g.fold(a,G)
 if level==10:p=far_return(c,s,a,Q(0));kind='centered_far_return'
 else:p=[(c,s),(Q(0),a),(c,ti)];kind='smooth_turn'
 V=polygon(c,[(Q(9),Q(11),Q(1))],[(s-1,s+1,Q(1)),(t-1,t+1,Q(2))],G)
 actual=fold_path(p,G);assert actual[0]==(c,s) and actual[-1]==(c,t)
 result=g.path_check(V,actual);rows.append({'chart_image':ti,'level':level,'kind':kind,**result})
for D in map(Q,(0,1)):
 c=Q(2);s=Q(1);t=Q(19);G=Q(20);a=Q(30);p=far_return(c,s,a,D);V=polygon(c,[(Q(9),Q(11),Q(1))],[(Q(0),Q(2),D+1),(Q(18),Q(20),D+2)],G)
 actual=fold_path(p,G);assert actual[0]==(c+D,s) and actual[-1]==(c+D,t)
 result=g.path_check(V,actual);rows.append({'flush_source_and_target':True,'depth':D,'kind':'centered_far_return_through_actual_ends',**result})
out={'status':'SIX_PRESCRIBED_ACTUAL_END_FOLD_PATHS_PASS','rows':rows,'reflections':sum(r['reflections'] for r in rows),'wall_leg_guards':sum(r['wall_leg_guards'] for r in rows),'whole_goal_complete':False,'discovery':False,'source_sha256':{'resumed-exact-check.py':hashlib.sha256((R/'resumed-exact-check.py').read_bytes()).hexdigest()},'scope':'Four actual target-image charts and two flush-tooth cases, including existing end-line horizontal contacts, all actualT.'}
(R/'four-level-spine-independent-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='rows'}))
