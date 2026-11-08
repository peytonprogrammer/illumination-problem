"""Bounded exact robust side-chart discovery, same A58 aggregate deadline."""
import datetime,json
from fractions import Fraction as Q
from pathlib import Path
P=Path(__file__).resolve().parent;deadline=datetime.datetime.fromisoformat('2026-11-07T07:53:00+00:00')
def guard():
 if datetime.datetime.now(datetime.timezone.utc)>=deadline:raise TimeoutError('original A58 aggregate deadline')
def fold(y,G):
 r=y%(2*G);return min(r,2*G-r)
def allowed(y,G,mouths):
 # Whole open unit-neighborhood must avoid ends and every closed mouth.
 if not 1<=y<=G-1:return False
 return all(y<=a-1 or y>=b+1 for a,b in mouths)
rows=[];tested=0
try:
 for kind,h,d in [('A0',h,0) for h in (3,4,5)]+[('A1',h,d) for h,lo,hi in [(3,2,14),(4,3,17),(5,4,20)] for d in range(lo,hi+1)]:
  guard();G=2*h+4 if kind=='A0' else 2*h+d+4;second=h+4 if kind=='A0' else h+d+2
  left=[(h,h+2),(second,second+2)];right=[(1,3),(2*h+1,2*h+3)];found=None
  for m in range(1,33):
   if found:break
   for sigma in (1,-1):
    if found:break
    for l in range(2*m):
     guard();K=sigma*(2*h+2)-2+2*l*G
     # Add one full vertical period to make K positive without changing side phases.
     if K<=0:K+=4*m*G
     tested+=1
     ys=[fold(2+Q(j*K,2*m),G) for j in range(1,2*m)]
     if all(allowed(y,G,left if j%2 else right) for j,y in enumerate(ys,1)):
      found={'m':m,'sigma':sigma,'K':K,'l_residue':l,'nominal_physical_sides':list(map(str,ys))};break
  rows.append({'kind':kind,'h':h,'d':d,'G':G,'robust_chart':found})
 status='BOUNDED_EXACT_CHART_INVENTORY_FINISHED'
except TimeoutError:
 status='STOPPED_AT_ORIGINAL_DEADLINE'
report={'status':status,'deadline':deadline.isoformat(),'hypothesis':'remaining48verticalpatterns may have a whole-open-unit-portal-box tooth-free rectangularcore chart','cap_m':32,'rows':rows,'chart_candidates':sum(r['robust_chart'] is not None for r in rows),'tested_charts':tested,'no_chart_is_not_darkness':True,'whole_goal_complete':False}
(P/'low-band-robust-core-check.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='rows'}))
