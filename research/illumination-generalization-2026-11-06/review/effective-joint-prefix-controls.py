"""R27 prescribed rational root/error inequalities. Algebra only, no room/ray search."""
from pathlib import Path
from fractions import Fraction as Q
from datetime import datetime,timezone
import json,time,signal,math
H=Path(__file__).resolve().parent
eff=json.loads((H/'effective-joint-prefix-effort.json').read_text())
deadline=datetime.fromisoformat(eff['deadline_utc']).timestamp()
assert time.time()<deadline,'Original R27 aggregate deadline expired'
signal.alarm(max(1,int(deadline-time.time())))
rows=[]
fixtures=[(Q(1,3),Q(7),2,3,Q(2),Q(3),Q(1,100)),(Q(1),Q(3),1,1,Q(1),Q(1),Q(1,20)),(Q(5),Q(11),7,2,Q(4),Q(2),Q(1,40))]
for fixture in fixtures:
 tau0,D,a,b,u,v,r=fixture
 lo=tau0/2;hi=3*tau0/2;c=min(Q(a),Q(b)/(2*hi));C0=1+a+b*hi;C=C0/c
 eps=min(u/4,v/4,r/(8*(1+C+C/(lo*lo))),tau0/(8*(1+C)))
 j=min(r/4,tau0/8,eps/(2*D));ell=2*j;mu=eps*eps/(4*u*v)
 Astar=1+max(4*u/(ell*mu),(2*u+eps)/lo)
 Bstar=1+max(256*v*hi**3/(ell**2*mu**2),hi*(2*v+eps))
 for imbalance in ('balanced','horizontal_1000','vertical_1000'):
  assert time.time()<deadline
  tau1=tau0+j/2
  N=math.ceil(Astar*tau1/(2*u))+2;M=math.ceil(Bstar/(2*v*tau1))+2
  if imbalance=='horizontal_1000':N*=1000
  if imbalance=='vertical_1000':M*=1000
  alpha1=eps/3;beta1=-eps/4
  A=(2*u*N+alpha1)/tau1;B=tau1*(2*v*M+beta1)
  assert A>Astar and B>Bstar
  denom=D+a*A+2*v*b*M
  root=(tau0*D+b*B+2*u*a*N)/denom
  alpha=root*A-2*u*N;beta=B/root-2*v*M
  F1=(tau1-tau0)*D+a*alpha1-b*tau1*beta1
  assert denom>=c*(A+B)>0
  assert root-tau1==-F1/denom
  assert abs(F1)<=C0*eps
  assert abs(root-tau1)<=C*eps/(A+B)<min(r/16,tau0/16)
  assert lo<root<hi and abs(root-tau0)<r
  assert abs(alpha)<r and abs(beta)<r
  assert (root-tau0)*D+a*alpha-b*root*beta==0
  # Explicit density bounds imply each normalized character error <mu/2.
  assert 2*u/(ell*A)<mu/2
  assert 64*v*hi**3/(ell**2*B)<mu**2/4
  rows.append({'tau0':tau0,'counts':[a,b],'widths':[u,v],'margin':r,'imbalance':imbalance,'A_over_B':A/B,'A_threshold':Astar,'B_threshold':Bstar,'actual_fixed_integer_root':root,'phase_alpha':alpha,'phase_beta':beta,'all_inequalities_verified':True})
out={'status':'EXACT_QUANTITATIVE_PHASE_ROOT_INEQUALITIES_PASS','rows':rows,'fixtures':len(fixtures),'imbalances_each':3,'exact_roots_verified':len(rows),'discovery':False,'actual_room_certificates':False,'whole_goal_complete':False,'ended_utc':datetime.now(timezone.utc).isoformat(),'within_original_deadline':time.time()<deadline}
(H/'effective-joint-prefix-controls.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
signal.alarm(0)
print(json.dumps({k:v for k,v in out.items() if k!='rows'}))
