"""Exact prescribed replay of a derived constructor; no room/direction discovery."""
from fractions import Fraction as F
from pathlib import Path
from math import gcd,floor,ceil
import ast,json,hashlib
HERE=Path(__file__).resolve().parent
CTX=HERE.parents[2]
BASE=CTX/'illumination-generalization-2026-11-06'
# Existing finite-wall predicates only; no top-level peer execution or writes.
pred=BASE/'review/resumed-exact-check.py'
tree=ast.parse(pred.read_text());names={'vec','det','dot','edges','on','location','intersect','simple','path_check','fold'}
ns={'Q':F}
exec(compile(ast.Module(body=[f for f in tree.body if isinstance(f,ast.FunctionDef) and f.name in names],type_ignores=[]),'<existing-exact-guards>','exec'),ns)
fold=ns['fold']

def tr06():
 request=json.loads((BASE/'construction/three-reflex-review-request-06.json').read_text());pins=[]
 for item in request['source_pins']:
  path=CTX/item['path'].removeprefix('.context/');actual=hashlib.sha256(path.read_bytes()).hexdigest();assert actual==item['sha256'];pins.append({'path':item['path'],'sha256':actual})
 rows=[]
 # Independently evaluate the exact nearest-period definitions without running author code.
 for tau in (F(499,420),F(501,420)):
  n=floor((2+14*tau+4)/8);left=2+14*tau-8*n
  m=floor((left+16*tau)/56);cap=left+16*tau-28*(2*m+1)
  k=floor((cap+12*tau+8)/16);right=cap+12*tau-16*k
  e=right+6*tau;j=floor((e-F(31,2)+16)/32)
  value=(8*n+28*(2*m+1)+16*k+32*j+F(31,2)-2)/48
  assert abs(left)<4 and abs(cap)<8 and abs(right)<8
  rows.append({'tau':tau,'indices':[n,m,k,j],'portal_residuals':[left,cap,right],'update':value})
 assert rows[0]['indices']==[2,0,0,0] and rows[1]['indices']==[2,0,1,-1]
 assert rows[0]['update']==F(115,96) and rows[1]['update']==F(83,96)
 return {'decision':'ACCEPT_EXACT_TR06_METHOD_COUNTERCONTROL_ONLY','pins':pins,'rows':rows,'illumination_refuted':False}

def select(a,N,b,c,h,H,S,T):
 a=F(a);s,u=map(F,S);t,v=map(F,T);l,w,A=(N-2)*a,(N-1)*a,N*a
 assert N>=5 and N%2 and 0<b<c<h<H and gcd(2*(H-h),N)==1
 assert 0<s<a and b<u<=h and l<t<A and 0<v<c
 assert u.denominator==v.denominator==1 and (c-v)%2==1
 d0,G,g1,d2=h-u,2*(H-h),h-c,c-v;D=int(d0+G+g1+d2);z=A-t
 chosen=None;forbidden=[]
 for q in range(D):
  tau=(A+z-s+2*a*q)/D
  phases=[s+d0*tau,s+(d0+G)*tau-A,s+(D-d2)*tau-A]
  bad=[(phase-a)%(2*a)==0 for phase in phases]
  forbidden.append(bad)
  if not any(bad) and chosen is None:chosen=(q,tau)
 assert chosen is not None
 q,tau0=chosen;n0=floor((s+d0*tau0+a)/(2*a));z0=s+d0*tau0-2*n0*a
 matches=[]
 for M in range(N):
  tau=tau0+2*a*M;X=z0+G*tau;m=floor(X/(2*A));z1=X-(2*m+1)*A
  if abs(z1)<a:matches.append((M,tau,m,z1))
 assert len(matches)==1
 M,tau,m,z1=matches[0];n=floor((s+d0*tau+a)/(2*a));k=floor((z1+g1*tau+a)/(2*a));z2=z1+g1*tau-2*k*a
 E=z2+d2*tau;J=(E-z)/(2*a);assert J.denominator==1
 parity_shift=bool(int(J)%2)
 if parity_shift:
  tau+=2*a*N;n+=N*int(d0);m+=int(G);k+=N*int(g1)
 z0=s+d0*tau-2*n*a;z1=z0+G*tau-(2*m+1)*A;z2=z1+g1*tau-2*k*a
 assert abs(z0)<a and abs(z1)<a and abs(z2)<a
 j=(z2+d2*tau-z)/(4*a);assert j.denominator==1
 assert D*tau==2*n*a+(2*m+1)*A+2*k*a+4*j*a+z-s
 return {'q':q,'q_period':D,'cap_M':M,'parity_shift':parity_shift,'tau':tau,'indices':[n,m,k,int(j)],'residuals':[z0,z1,z2],'forbidden_q_patterns':forbidden}

def replay(label,a,N,b,c,h,H,S,T):
 a=F(a);S=tuple(map(F,S));T=tuple(map(F,T));s,u=S;t,v=T;l,w,A=(N-2)*a,(N-1)*a,N*a
 selection=select(a,N,b,c,h,H,S,T);tau=selection['tau'];z0,z1,z2=selection['residuals']
 P=[(a,b),(a,h),(w,h),(w,c),(l,c),(l,0),(A,0),(A,H),(0,H),(0,b)];ns['simple'](P)
 E1,E2,end=2*H-h,2*H-c,2*H-v
 bands=[]
 if u<h:bands.append((u,F(h),a,s-tau*u,False))
 bands.extend([(F(h),F(E1),A,z0-tau*h,False),(F(E1),F(E2),a,z1-tau*E1,True),(F(E2),F(end),2*a,z2-tau*E2,True)])
 def at(eta):
  xs=[]
  for lo,hi,width,offset,mirror in bands:
   if lo<=eta<=hi:
    val=fold(tau*eta+offset,width);xs.append(A-val if mirror else val)
  assert xs and len(set(xs))==1
  return (xs[0],min(eta,2*H-eta))
 events={u,F(H),F(end)}
 for lo,hi,width,offset,mirror in bands:
  events.update((lo,hi))
  for k in range(floor((tau*lo+offset)/width)-1,ceil((tau*hi+offset)/width)+2):
   eta=(k*width-offset)/tau
   if lo<eta<hi:events.add(eta)
 times=sorted(events);path=[at(x) for x in times];assert path[0]==S and path[-1]==T
 result=ns['path_check'](P,path)
 velocities=[]
 for i,(p,r) in enumerate(zip(path,path[1:])):
  dt=times[i+1]-times[i];vel=((r[0]-p[0])/dt,(r[1]-p[1])/dt)
  assert abs(vel[0])==tau and abs(vel[1])==1
  if i<len(path)-2:
   time=(t-p[0])/vel[0];assert not (0<time<=dt and p[1]+time*vel[1]==v)
  velocities.append(vel)
 for i,p in enumerate(path[1:-1],1):
  contacts=[(x,y) for x,y in ns['edges'](P) if ns['on'](x,y,p)]
  vx,vy=velocities[i-1]
  expected=((-vx,vy) if contacts[0][0][0]==contacts[0][1][0] else (vx,-vy)) if contacts else (vx,vy)
  assert velocities[i]==expected
 roof=[p for p in path[1:-1] if p[1]==H];assert len(roof)==1 and 0<roof[0][0]<A
 return {'label':label,'geometry':[a,l,w,A,b,c,h,H],'S':S,'T':T,'selection':selection,'path':path,'roof_contact':roof[0],**result}

fixtures=[
 ('same-height',4,5,1,5,7,8,(2,2),(14,2)),
 ('low-to-high-target',4,5,1,5,7,8,(2,2),(18,4)),
 ('high-to-low-target',4,5,1,5,7,8,(2,6),(14,2)),
 ('target-on-w',4,5,1,5,7,8,(2,4),(16,2)),
 ('source-on-h',6,7,2,7,10,11,(4,10),(32,6)),
 ('non-prime-N',8,9,3,9,12,13,(6,8),(58,4)),
 ('two-unit-cap',4,5,1,5,10,12,(2,8),(18,2)),
 ('rational-x-near-ends',F(3,2),7,1,5,8,9,(F(1,101),6),(F(21,2)-F(1,103),4)),
 ('long-arm',4,5,1,5,40,41,(2,38),(14,2)),
]
if __name__=='__main__':
 old=tr06();rows=[replay(*item) for item in fixtures]
 out={'status':'PASS_PRESCRIBED_COPRIME_CONSTRUCTION','TR06':old,'rows':rows,'case_count':len(rows),'reflections':sum(r['reflections'] for r in rows),'wall_leg_guards':sum(r['wall_leg_guards'] for r in rows),'parity_shift_cases':sum(r['selection']['parity_shift'] for r in rows),'geometry_predicate_sha256':hashlib.sha256(pred.read_bytes()).hexdigest(),'discovery_search_used':False,'independent_positive_review':'pending','whole_r3_goal_complete':False}
 (HERE/'prescribed-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
 print(json.dumps({k:v for k,v in out.items() if k not in ('TR06','rows')}))
