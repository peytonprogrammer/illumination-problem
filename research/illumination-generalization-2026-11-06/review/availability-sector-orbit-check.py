#!/usr/bin/env python3
"""Exact prescribed Q0 common-cone Gamma orbit replay; not an angular census."""
from pathlib import Path
import json
period=24
# Units pi/4; actual6pi cone, canonical physical wedge0..6units.
def orbit(j):return sorted({j%period,(-j)%period,(12-j)%period,(12+j)%period})
def dist(a,b):
 d=abs(a-b)%period
 return min(d,period-d)
source=orbit(5);target=orbit(1)
rows=[{'source_prong':a,'target_prong':b,'smaller_sector_units':dist(a,b)} for a in source for b in target]
assert len(rows)==16 and min(x['smaller_sector_units'] for x in rows)==4
assert all(x['smaller_sector_units']>=4 for x in rows)
# Existing exact physical segment verification, read only.
prior=json.loads(Path(__file__).with_name('availability-av01-independent-check.json').read_text())
assert prior['status']=='PASS'
for row in prior['prescribed_controls']:
 assert row['only_boundary_event_time']==1 and row['genuine_reflex'] and row['missing_quadrant']=='SE'
 assert row['source']==[0,0] and row['target']==[2*row['stretch'],2]
result={'status':'PASS','angle_units':'pi/4 mod24','source_canonical_angle':5,'target_canonical_angle':1,'source_Gamma_orbit':source,'target_Gamma_orbit':target,'all_sixteen_pairs':rows,'minimum_actual_sector_angle':'pi','strictly_narrow_Gamma_choice_exists':False,'prior_prescribed_Q0_Q100_physical_check':'PASS read-only','universal_criterion_proved_by_hand_not_sampling':True,'scope':'Selected common-cone arms and their Gamma images only; not all other arms/cones, not r<=8 counterexample.','search_used':False,'whole_goal_complete':False}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','prescribed_Gamma_pairs':16,'narrow_choice':False,'search_used':False}))
