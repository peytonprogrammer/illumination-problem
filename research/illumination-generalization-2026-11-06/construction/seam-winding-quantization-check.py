"""Prescribed finite arithmetic after the proved winding quantization; no rays."""
from fractions import Fraction as Q
from pathlib import Path
import json,datetime
P=Path(__file__).resolve().parent;deadline=datetime.datetime.fromisoformat('2026-11-07T08:01:00+00:00')
def m(q,H):return (q*H-(q*(H-Q(1,2))+Q(1,2))//1)/(1+q)
def phases(q,H):
 lower=q*H-(1+q)/2;upper=q*H+(1+q)/2
 return [(q*H-n)/(1+q) for n in range(max(0,int(lower//1)),int(upper//1)+2) if lower<n<upper]
rows=[]
for kind,h,d in [('A0',3,0),('A0',5,0),('A1',3,2),('A1',3,6),('A1',3,7),('A1',3,10)]:
 assert datetime.datetime.now(datetime.timezone.utc)<deadline
 G=2*h+4 if kind=='A0' else 2*h+d+4;mu=h+2
 # Source dark sign constraints at four ACTUAL end-fold chart corners.
 source_sign=[-1,1,1,-1] if kind=='A0' else [-1,-1,1,1]
 Hs=[h,h+G,mu,mu+G];qs=[];qt=[];qs_all=[];qt_all=[]
 for n in range(1,2*G+1):
  q=Q(n,2*G);vals=[m(q,H) for H in Hs]
  if all(sign*v>=0 for sign,v in zip(source_sign,vals)):qs.append(str(q))
  if all(sign*v<=0 for sign,v in zip(source_sign,vals)):qt.append(str(q))
  if all(all(sign*v>=0 for v in phases(q,H)) for sign,H in zip(source_sign,Hs)):qs_all.append(str(q))
  if all(all(sign*v<=0 for v in phases(q,H)) for sign,H in zip(source_sign,Hs)):qt_all.append(str(q))
 constraints=set()
 for eta_target in (-1,1):
  for winding in range(-3,4):
   image=eta_target*(2*h+2)+2*winding*G
   H=Q(abs(image-2),2);M=Q(image+2,2);res=M%(2*G);level=min(res,2*G-res)
   assert res not in (0,G)
   foldsign=1 if res<G else -1
   second=h+4 if kind=='A0' else h+d+2
   epsilon=1 if level in (h+2,second+2) else -1
   assert level in (h,h+2,second,second+2)
   source_role=1 if image>2 else -1
   constraints.add((H%(2*G) or Q(2*G),-epsilon*foldsign*source_role))
 qa_s=[];qa_t=[]
 for n in range(1,2*G+1):
  q=Q(n,2*G)
  if all(all(sign*v>=0 for v in phases(q,H)) for H,sign in constraints):qa_s.append(str(q))
  if all(all(sign*v<=0 for v in phases(q,H)) for H,sign in constraints):qa_t.append(str(q))
 rows.append({'all_image_source_ratios':qa_s,'all_image_target_ratios':qa_t,'all_image_candidate_pairs':len(qa_s)*len(qa_t),'all_image_constraints':[(str(H),v) for H,v in sorted(constraints)],'kind':kind,'h':h,'d':d,'G':G,'source_possible_ratios':qs,'target_possible_ratios':qt,'candidate_pairs':len(qs)*len(qt),'source_all_stationary_ratios':qs_all,'target_all_stationary_ratios':qt_all,'all_stationary_candidate_pairs':len(qs_all)*len(qt_all),'H':Hs,'source_dark_sign':source_sign})
out={'status':'EXACT_QUANTIZED_FOUR_CHART_SIGN_TABLE','discovery':False,'deadline':deadline.isoformat(),'rows':rows,'no_darkness_claim':True,'actual_endpoint_scope':'SEAMS ONLY','whole_goal_complete':False};(P/'seam-winding-quantization-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
