from pathlib import Path
from fractions import Fraction as F
from math import floor,ceil
from datetime import datetime,timezone
import ast,json,hashlib
ROOT=Path(__file__).resolve().parent;E=json.loads((ROOT/'tooth-return-grid-effort.json').read_text())
def alive():assert datetime.now(timezone.utc)<datetime.fromisoformat(E['deadline'])
source=ROOT.parent/'review'/'resumed-exact-check.py';tree=ast.parse(source.read_text());names={'vec','det','dot','edges','on','location','intersect','simple','path_check','fold'};ns={'Q':F};exec(compile(ast.Module(body=[z for z in tree.body if isinstance(z,ast.FunctionDef) and z.name in names],type_ignores=[]),str(source),'exec'),ns)
def fold(z):z=z%4;return min(z,4-z)
def loadv(v):return {k:(F(x) if k in ('lo','hi','tau','far_phase') else x) for k,x in v.items()}
def select(v,D,w):
 v=loadv(v);den=w+D+v['l']+v['r']-1;n=v['n'];H=v['H'];k0=max(0,floor((v['lo']*den-H-2*n)/2)+1)
 for k in (k0,k0+1):
  tau=F(H+2*n+2*k,den);far=v['far_phase_constant']+2*k+(v['l']-v['r'])*tau
  if not v['lo']<tau<v['hi']:continue
  if far.denominator==1 and far.numerator%2==0:continue
  return dict(v,k=k,tau=tau,w=w,far_phase=far)
 raise AssertionError(('tail selection failed',v,D,w))
def build(z,v,other=1):
 alive();h,d,D=z['h'],z['d'],z['D'];t=2*h+2;G=v['G'];ys=(h,h+(4 if d is None else d+2));w=v['w'];tooth=v['tooth'];a,b=(w,other) if tooth==0 else(other,w)
 V=[(0,0),(1,0),(1,1),(D+2,1),(D+2,3),(1,3),(1,t-1),(D+2,t-1),(D+2,t+1),(1,t+1),(1,G),(0,G),(0,ys[1]+2),(-b,ys[1]+2),(-b,ys[1]),(0,ys[1]),(0,ys[0]+2),(-a,ys[0]+2),(-a,ys[0]),(0,ys[0])];V=[tuple(map(F,q)) for q in V];ns['simple'](V)
 tau=v['tau'];n=v['n'];sign=(-1)**n;C=2-2*n;L=v['target_copy']+2*n;l,r=v['l'],v['r'];Y=v['Y']
 # Explicit source prefix; all intermediate contacts are physical tooth horizontals.
 times=[]
 for j in range(-n-2,n+3):
  u=F(2*j-1,sign*tau)
  if 0<u<D:times.append(u)
 prefix=[(F(1+D),F(2))]+[(1+D-u,1+fold(1+sign*tau*u)) for u in sorted(times)]+[(F(1),C+D*tau)]
 assert len(times)==n
 path=prefix+[(F(0) if j%2 else F(1),C+(D+j)*tau) for j in range(1,2*l)]
 A=path[-1][1]-Y;B=L-(D+2*r-1)*tau-Y
 assert 0<A<2 and 0<B<2 and A+2*w*tau==B+4*v['k']
 far=A+w*tau;assert not(far.denominator==1 and far.numerator%2==0)
 stop=A+2*w*tau;times={F(w)}
 for j in range(floor(A/2)-1,ceil(stop/2)+2):
  u=F(2*j-A,tau)
  if 0<u<2*w:times.add(u)
 path +=[(-u if u<=w else u-2*w,Y+fold(A+tau*u)) for u in sorted(times)]
 path +=[(F(0),Y+B)]
 path +=[(F(0) if j%2 else F(1),L-(D+j)*tau) for j in range(2*r-2,0,-1)]
 path +=[(F(1),L-D*tau)]
 path +=[(x,2+v['target_copy']-y) for x,y in reversed(prefix[:-1])]
 # Insert actual roof contacts in open core legs before global folding.
 developed=[path[0]]
 for p,q in zip(path,path[1:]):
  if min(p[1],q[1])<G<max(p[1],q[1]):
   rho=F(G-p[1],q[1]-p[1]);x=p[0]+rho*(q[0]-p[0]);assert 0<x<1;developed.append((x,F(G)))
  developed.append(q)
 def Fend(y):yy=y%(2*G);return min(yy,2*G-yy)
 actual=[(x,Fend(y)) for x,y in developed];S=(F(1+D),F(2));T=(F(1+D),F(t));assert actual[0]==S and actual[-1]==T
 for j,(p,q) in enumerate(zip(actual,actual[1:])):
  if ns['on'](p,q,T):actual=actual[:j+1]+[T];break
 result=ns['path_check'](V,actual)
 return {'kind':z['kind'],'h':h,'d':d,'D':D,'a':a,'b':b,'choice':v,'polygon':V,'S':S,'T':T,'path':actual,**result}
r=json.loads((ROOT/'tooth-return-grid-end-check.json').read_text());rows=[];cover=[]
for z in r['rows']:
 closed=[q for q in z['targets'] if q['best'] and not q['uncovered_widths']]
 chosen_targets=([min(closed,key=lambda q:q['best']['w_min'])] if closed else ([q for q in z['targets'] if q['best']] if z['h']>=5 else []))
 for target in chosen_targets:
  tooth=target['tooth'];best=loadv(target['best']);N=best['w_min'];record={'kind':z['kind'],'h':z['h'],'d':z['d'],'D':z['D'],'tooth':tooth,'tail_width_min':N,'tail':best,'prefix':target['small_width_witnesses'],'uncovered_widths':target['uncovered_widths']};cover.append(record)
  # Exact all-slope interval guards for every profile used below.
  def profile_guard(v):
   v=loadv(v);h=z['h'];d=z['d'];D=z['D'];G=v['G'];t=2*h+2;ys=(h,h+(4 if d is None else d+2));n=v['n'];C=2-2*n;L=v['target_copy']+2*n;lo=v['lo'];hi=v['hi']
   left=[(y,y+2) for y in ys]+[(2*G-y-2,2*G-y) for y in ys];right=[(1,3),(t-1,t+1),(2*G-3,2*G-1),(2*G-t-1,2*G-t+1)]
   assert lo<hi and max(F(0),F(2*n-1,D))<=lo and hi<=F(2*n+1,D)
   for a,b in ((D+2*v['l']-1,C),(-D-2*v['r']+1,L)):
    x,y=sorted((a*lo+b,a*hi+b));assert v['Y']<=x<y<=v['Y']+2
   for length,sgn,base in ((v['l'],1,C),(v['r'],-1,L)):
    for j in range(1,2*length-1):
     x,y=sorted((sgn*(D+j)*lo+base,sgn*(D+j)*hi+base));assert 0<=x<y<=2*G and not x<G<y
     for low,high in (left if j%2 else right):assert y<=low or x>=high,(z,v,j,x,y,low,high)
  profile_guard(best)
  for saved in target['small_width_witnesses']:
   chosen=loadv(saved);profile_guard(chosen);chosen['tooth']=tooth;rows.append(build(z,chosen))
  for w in (N,N+1,N+37):
   chosen=select(best,z['D'],w);chosen['tooth']=tooth;rows.append(build(z,chosen,17 if w==N+37 else 1))
alive();out={'status':'ALL_PRESCRIBED_ACTUAL_PATHS_PASS','rows':rows,'coverage':cover,'normal_form_tables':len(cover),'all_used_profile_intervals_exactly_guarded':True,'paths':len(rows),'reflections':sum(x['reflections'] for x in rows),'all_wall_leg_guards':sum(x['wall_leg_guards'] for x in rows),'accepted_validator_definitions_reused':True,'source_sha256':{str(source):hashlib.sha256(source.read_bytes()).hexdigest()},'discovery':False,'original_deadline':E['deadline'],'finished_utc':datetime.now(timezone.utc).isoformat(),'whole_goal_complete':False}
(ROOT/'tooth-return-grid-physical-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('rows','coverage','source_sha256')}))
