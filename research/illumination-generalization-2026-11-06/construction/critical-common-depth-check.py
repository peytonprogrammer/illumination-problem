"""Bounded exact one-residual chart discovery; COMMON depth only."""
from pathlib import Path
from fractions import Fraction as Q
from datetime import datetime,timezone
import json,signal
P=Path(__file__).resolve().parent;E=json.loads((P/'critical-common-depth-effort.json').read_text());end=datetime.fromisoformat(E['deadline']);left=(end-datetime.now(timezone.utc)).total_seconds();assert left>0;signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('original deadline')));signal.setitimer(signal.ITIMER_REAL,left)
def fold(y,G):
 r=y%(2*G);return min(r,2*G-r)
def allowed(y,r,G,mouths):
 if r==0:return 0<y<G and not any(a<=y<=b for a,b in mouths)
 return r<=y<=G-r and all(y+r<=a or y-r>=b for a,b in mouths)
rows=[];tested=0;status='BOUNDED_EXACT_COMMON_RESIDUAL_FINISHED'
try:
 for kind,h,d in [('A0',3,0),('A0',5,0),('A1',3,2),('A1',3,6),('A1',3,7),('A1',3,10)]:
  G=2*h+4 if kind=='A0' else 2*h+d+4;second=h+4 if kind=='A0' else h+d+2;ls=[(h,h+2),(second,second+2)];rs=[(1,3),(2*h+1,2*h+3)];ans=None
  for m in range(1,33):
   if ans:break
   for sigma in (1,-1):
    if ans:break
    for l in range(2*m):
     if datetime.now(timezone.utc)>=end:raise TimeoutError
     K=sigma*(2*h+2)-2+2*l*G
     if K<=0:K+=4*m*G
     tested+=1;ys=[fold(2+Q(j*K,2*m),G) for j in range(1,2*m)];radii=[abs(1-Q(j,m)) for j in range(1,2*m)]
     if all(allowed(y,r,G,ls if j%2 else rs) for j,(y,r) in enumerate(zip(ys,radii),1)):
      ans={'m':m,'sigma':sigma,'K':K,'nominal_sides':list(map(str,ys)),'radii':list(map(str,radii))};break
  rows.append({'kind':kind,'h':h,'d':d,'G':G,'candidate':ans})
except TimeoutError:status='STOPPED_AT_ORIGINAL_AGGREGATE_DEADLINE'
finally:
 signal.setitimer(signal.ITIMER_REAL,0);out={'status':status,'rows':rows,'tested':tested,'deadline':E['deadline'],'discovery':True,'no_candidate_is_not_darkness':True,'whole_goal_complete':False};(P/'critical-common-depth-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
