"""Explicit reviewer correction calibration; frozen P1 original is still rejected."""
from pathlib import Path
import json,hashlib
HERE=Path(__file__).parent
parent=HERE/'three-reflex-upper-joint-lattice-check.py'
ns={'__file__':str(parent),'__name__':'own_UJ01_pure_review_prefix'}
exec(compile(parent.read_text().split('\nvalid=[')[0],'<own-UJ01-functions-and-pin-checks>','exec'),ns)
Q=ns['Q'];params=(2,2,2,4,7,2,3,4,12);S=(2,4);T=(10,2)
rows=[]
for preset in [(1,3),None]:
 selection=ns['select'](params,S,T,preset)
 if preset is not None:assert selection['final_slope']==6 and selection['q']==23 and selection['p']==0
 rows.append(dict(selection=selection,**ns['physical']('explicit-P2-mouth-repair'+('-fixed' if preset else '-own-Bezout'),params,S,T,selection['final_slope'])))
assert ns['pins']()==ns['before']
out=dict(status='PASS_EXPLICIT_NEW_P2_NATIVE_INTERIOR_MOUTH_REPAIR',original_frozen_P1_case_still_rejected=True,repair='Change P1 toP2 explicitly, a2 toa4; same actualS2,4 nowstrictmouthinterior; no original source edited.',original_request_sha256=ns['request_hash'],original_pins_before=ns['before'],original_pins_after=ns['pins'](),rows=rows,cases=len(rows),reflections=sum(x['reflections'] for x in rows),wall_leg_guards=sum(x['wall_leg_guards'] for x in rows),author_code_executed=False,discovery_search_used=False,whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['rows','original_pins_before','original_pins_after']}))
