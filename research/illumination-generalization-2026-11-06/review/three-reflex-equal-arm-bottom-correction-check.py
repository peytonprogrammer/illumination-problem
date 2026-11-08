"""EA02-F1 separate corrected-input replay, frozen old calibration preserved."""
from pathlib import Path
from fractions import Fraction as Q
import json,hashlib
HERE=Path(__file__).parent
REQ=HERE.parent/'construction/three-reflex-equal-arm-bottom-correction-review-request.json'
def pincheck():
 rows=[]
 for pin in json.loads(REQ.read_text())['source_pins']:
  actual=hashlib.sha256(Path(pin['path']).read_bytes()).hexdigest()
  assert actual==pin['sha256'];rows.append(dict(pin,actual=actual,passed=True))
 return rows
before=pincheck();rh=hashlib.sha256(REQ.read_bytes()).hexdigest()
src=(HERE/'three-reflex-equal-arm-bottom-check.py').read_text()
env={'__file__':__file__}
# Initialize only the earlier own pure lower selector and geometry setup;
# none of its valid fixture loop or JSON writing is executed.
exec(compile(src.split('rows=[lower[')[0],'<own-corrected-native-source-selector>','exec'),env)
row=env['lower']['check']('EA02-F1-replacement-e4-P1-native',4,1,11,3,1,3,6,12,
                         (2,4),(36,2),Q(539,3))
assert row['indices']==[45,24,68]
assert row['residuals']==[Q(4,3),Q(4,3),-Q(11,3)]
assert row['roof']['point']==(Q(70,3),Q(12))
E=row['residuals'][-1]+row['final_slope'];assert E==176 and E%24==8
assert rh==hashlib.sha256(REQ.read_bytes()).hexdigest()
out=dict(status='PASS_EA02_F1_CORRECTED_ACTUAL_SOURCE_AND_FULL_TARGET_RAY',
 source_pins_before=before,source_pins_after=pincheck(),request_sha256=rh,row=row,
 cases=1,reflections=row['reflections'],wall_leg_guards=row['wall_leg_guards'],
 old_boundary_source_rejected=True,old_frozen_files_preserved=True,
 author_code_executed=False,discovery_search_used=False,whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['row','source_pins_before','source_pins_after']}))
