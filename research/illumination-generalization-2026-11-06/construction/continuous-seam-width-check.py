from pathlib import Path
from fractions import Fraction as F
from datetime import datetime,timezone
from math import floor,ceil
import json
R=Path(__file__).resolve().parent;E=json.loads((R/'seam-width-rigidity-effort.json').read_text())
def alive():assert datetime.now(timezone.utc)<datetime.fromisoformat(E['deadline'])
def continuous(target):
 alive();N=F(target['best']['w_min']);forms=[];cuts={F(0),N}
 for v in target['intervals']:
  lo,hi=F(v['lo']),F(v['hi']);B=v['virtual_depth']+v['l']+v['r']-1;H=v['H'];n=v['n'];alpha=v['l']-v['r'];K=H+2-v['Y']
  for k in range(max(0,ceil((hi*(N+B)-H-2*n)/2)+1)):
   M=H+2*n+2*k;left=max(F(0),M/hi-B);right=min(N,M/lo-B)
   if not left<right:continue
   bad=set();flo,fhi=sorted((K+2*k+alpha*lo,K+2*k+alpha*hi))
   if alpha:
    for j in range(floor(flo/2)-1,ceil(fhi/2)+2):
     denom=2*j-K-2*k
     if not denom:continue
     z=F(alpha*M,denom)-B
     if left<z<right:bad.add(z)
   elif K%2==0:continue
   # The original strict I is already split at every selected-far odd slope.
   assert v['virtual_depth']==0 or not any(lo<j<hi for j in range(1,100,2))
   forms.append((left,right,bad,v,k));cuts.update((left,right));cuts.update(bad)
 def covered(w):return any(a<w<b and w not in bad for a,b,bad,_,_ in forms)
 cuts=sorted(cuts);gaps=[]
 for a,b in zip(cuts,cuts[1:]):
  if not covered((a+b)/2):gaps.append((a,b))
 points=[q for q in cuts if 0<q<N and not covered(q)]
 # N and every larger width have the all-width tail proof; not a cutoff inference.
 return {'tail_from':N,'retained_chart_intervals':len(target['intervals']),'finite_winding_forms':len(forms),'uncovered_open_cells':gaps,'uncovered_points':points,'all_above_N_covered_by_proof':True}
r=json.loads((R/'seam-four-band-chart-check.json').read_text());z=next(q for q in r['rows'] if q['kind']=='A1' and q['h']==3 and q['d']==1);out={'status':'EXACT_CONTINUOUS_WIDTH_COVER_FOR_FROZEN_BALANCED_RETURN_CHARTS','room':'A1h3d1 selectedwidth1 actualseams','targets':[continuous(t) for t in z['targets']],'original_deadline':E['deadline'],'finished_utc':datetime.now(timezone.utc).isoformat(),'discovery':True,'darkness_claimed':False,'whole_goal_complete':False};(R/'continuous-seam-width-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps(out,indent=2,default=str))
