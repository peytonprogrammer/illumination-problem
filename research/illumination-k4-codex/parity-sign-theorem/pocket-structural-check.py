"""Prescribed local angle and covering identities; no surface/path search."""
from pathlib import Path
from fractions import Fraction as F
from math import gcd
import json
b=Path(__file__).resolve().parent
expected={1:(8,1),2:(4,1),3:(8,3),4:(2,1),5:(8,5),6:(4,3),7:(8,7)}
rows=[]
for m,(sectors,q) in expected.items():
 assert sectors==8//gcd(m,4)
 assert F(sectors*m,8)==q and q%2==1
 assert (q-1)%2==0
 rows.append(dict(angle_units=m,sectors=sectors,cone_multiplicity=q,zero_order=q-1))
# Algebraic identity in a local map z -> z^e: pulling back z^k dz
# gives e*z^(e*k+e-1) dz. These three fixed cases check bookkeeping.
cover_controls=[]
for e,k in [(1,2),(3,0),(5,2)]:
 order=e*k+e-1
 assert order+1==e*(k+1) and order%2==0
 cover_controls.append(dict(e=e,target_zero_order=k,source_zero_order=order))
# A simple target zero always gives an odd source zero, for ANY e>0:
# e*(1+1)-1 = 2e-1. This symbolic identity supplies the EW exclusion.
out=dict(status='LOCAL_ANGLE_AND_PULLBACK_IDENTITIES_PASS',local_rows=rows,
 cover_controls=cover_controls,ew_exclusion_identity='source_order=2e-1, odd for every positive integer e',
 forni_hiding_necessary_dimension=4,universal_detection_proved=False,
 loaded_cylinder_existence_proved=False,actual_event_existence_proved=False,discovery_runs=0)
(b/'pocket-structural-check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
