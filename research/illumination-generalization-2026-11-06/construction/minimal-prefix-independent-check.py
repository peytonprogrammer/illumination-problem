from pathlib import Path
from fractions import Fraction as F
from datetime import datetime,timezone
import json,hashlib
R=Path(__file__).resolve().parent;P=R.parent/'review';pins={}
for filename in ('minimal-depth-shuttle-review-request.json','minimal-prefix-review-request.json'):
 q=json.loads((P/filename).read_text())
 for n,h in q['source_sha256'].items():assert hashlib.sha256((P/n).read_bytes()).hexdigest()==h,(filename,n);pins[n]=h
source=(P/'minimal-prefix-proof.md').read_text();literal=[]
for line in source.splitlines():
 if not line.startswith('|'):continue
 vs=line.strip('|').split('|')
 if len(vs)!=10 or not vs[0].isdigit():continue
 D,w,es,et,m,ns,nt,sigma,k=map(int,vs[:9]);tau=F(vs[9]);literal.append((D,w,es,et,m,ns,nt,sigma,k,tau))
expected={(D,w) for D,limit in ((0,12),(1,19),(2,66)) for w in range(1,limit+1)}
assert len(literal)==97 and {(q[0],q[1]) for q in literal}==expected
rows=[];mirrors=0
for D,w,es,et,m,ns,nt,sigma,k,tau in literal:
 assert es in (D,D+2) and et in (D,D+2) and sigma in(-1,1) and m>=0 and k>=0 and tau>0
 ys=-2+2*ns+es*tau;yt=2+2*nt-sigma*et*tau;P1=ys+(2*m+1)*tau;P2=yt-sigma*tau
 assert -3<ys<-1 and 1<yt<3 and 0<P1<2 and 0<P2<2
 for i in range(1,m+1):assert -2<ys+(2*i-1)*tau<0 and -1<ys+2*i*tau<1;mirrors+=2
 assert P1+2*w*tau==((P2 if sigma==1 else 4-P2)+4*k)
 phase=P1+w*tau;assert not(phase.denominator==1 and phase.numerator%2==0)
 if es==D+2 or et==D+2:assert not(tau.denominator==1 and tau.numerator%2)
 assert ys+3-tau*es==1+2*ns and yt-1+sigma*tau*et==1+2*nt
 rows.append({'D':D,'w':w,'ys':ys,'yt':yt,'entry':P1,'exit':P2,'far_phase':phase,'tau':tau})
# Independently recheck all strict tail intervals and threshold grid lengths.
for D,w,N,lo,hi,denextra in ((0,13,13,F(2,7),F(2,5),5),(1,20,20,F(1,4),F(1,3),5),(2,67,67,F(2,9),F(1,4),6)):
 assert (hi-lo)*(w+denextra)/2>1
 assert (D+2)*hi<=1 and (D+5)*hi<=2 and (D+4)*lo>=1 and (D+6)*hi<=3 and (D+7)*lo>=2
 beta=2 if D==0 else 3
 assert 0<beta*lo<beta*hi<=1
 # Strict open endpoints make all weak boundary equalities strict inside.
out={'status':'ALL_97_LITERAL_ROWS_AND_ALL_THREE_UNBOUNDED_TAIL_INTERVALS_PASS','literal_rows':97,'protected_core_mirrors':mirrors,'source_pins_checked':len(pins),'source_sha256':pins,'peer_optical_code_executed':False,'peer_controls_replayed':False,'discovery':False,'rows':rows,'finished_utc':datetime.now(timezone.utc).isoformat(),'whole_goal_complete':False}
(R/'minimal-prefix-independent-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in('rows','source_sha256')}))
