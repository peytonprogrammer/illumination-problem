"""Exact interpolation diagnostics, not a room or ray search."""
from pathlib import Path
from fractions import Fraction as F
import json
B=Path(__file__).resolve().parent
records=[]
for n in (4,8,16,32,64):
 e=F(1,n);a=1-e;b=F(1);cs=-e+e**3;ct=e
 approximate=(cs+ct)/2;exact=(b*cs+a*ct)/(a+b)
 assert 0<approximate<e and exact<0
 records.append(dict(epsilon=str(e),source_normal_distance=str(a),target_normal_distance=str(b),source_offset=str(cs),target_offset=str(ct),limit_weight_prediction=str(approximate),exact_window_crossing=str(exact)))
scaled=[]
for n in (4,8,16,32,64):
 h=F(1,n);eps=h*h;a=1-h;b=F(1);cs=-1/h+F(1,2);ct=1/h
 predicted=(cs+ct)/2;exact=(b*cs+a*ct)/(a+b)
 assert predicted==F(1,4) and exact<0 and eps*abs(cs)<h
 scaled.append(dict(h=str(h),neck_width=str(eps),normalized_source_offset=str(cs),normalized_target_offset=str(ct),limit_weight_prediction=str(predicted),exact_normalized_crossing=str(exact)))
out=dict(status='PASS',corollary11=records,corollary14_missing_bounded_offsets=scaled,scope='Counterexamples to the interpolation inference for the specified pair of developed words, not examples of dark nearby rooms. Other paths may light them.',repair='Use exact current perpendicular distances a_n,b_n. For a first-order asymptotic statement require a uniform interior margin; for the local-model limit also bound individual offsets in neck units or explicitly control the interpolation remainder.')
(B/'pinch-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
