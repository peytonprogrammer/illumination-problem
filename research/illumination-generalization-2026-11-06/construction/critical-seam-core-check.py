"""Bounded exact zero-residual seam-core chart discovery, two vertical profiles."""
from pathlib import Path
from fractions import Fraction as Q
from datetime import datetime,timezone
import json,signal
P=Path(__file__).resolve().parent;E=json.loads((P/'critical-seam-core-effort.json').read_text());end=datetime.fromisoformat(E['deadline']);remaining=(end-datetime.now(timezone.utc)).total_seconds();assert remaining>0;signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('original deadline')));signal.setitimer(signal.ITIMER_REAL,remaining)
def fold(y,G):
 r=y%(2*G);return min(r,2*G-r)
def allowed(y,G,mouths):return 0<y<G and not any(a<=y<=b for a,b in mouths)
rows=[];tested=0;status='BOUNDED_EXACT_POINT_CHART_DISCOVERY_FINISHED'
try:
 for d in (7,10):
  G=d+10;left=[(3,5),(d+5,d+7)];right=[(1,3),(7,9)];found=None
  for m in range(1,65):
   if found:break
   for sigma in (1,-1):
    if found:break
    for l in range(2*m):
     if datetime.now(timezone.utc)>=end:raise TimeoutError
     K=sigma*8-2+2*l*G
     if K<=0:K+=4*m*G
     tested+=1;ys=[fold(2+Q(j*K,2*m),G) for j in range(1,2*m)]
     if all(allowed(y,G,left if j%2 else right) for j,y in enumerate(ys,1)):
      found={'m':m,'sigma':sigma,'K':K,'nominal_sides':list(map(str,ys))};break
  rows.append({'h':3,'d':d,'G':G,'candidate':found})
except TimeoutError:status='STOPPED_AT_ORIGINAL_AGGREGATE_DEADLINE'
finally:
 signal.setitimer(signal.ITIMER_REAL,0);out={'status':status,'discovery':True,'rows':rows,'tested':tested,'deadline':E['deadline'],'no_candidate_is_not_darkness':True,'whole_goal_complete':False};(P/'critical-seam-core-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
