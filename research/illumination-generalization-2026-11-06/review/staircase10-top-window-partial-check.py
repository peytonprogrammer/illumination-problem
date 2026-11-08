"""One extra hand-prescribed control for the previously untested partial-overlap branch."""
import json,hashlib
from pathlib import Path
from fractions import Fraction as Q
HERE=Path('.context/illumination-generalization-2026-11-06/review')
extra=json.loads((HERE/'staircase10-top-window-partial-input.json').read_text())
base=Path(extra['base_checker'])
assert hashlib.sha256(base.read_bytes()).hexdigest()==extra['base_checker_sha256']
# Load pure setup/definitions, NOT the original eight-case execution block.
env={}
exec(compile(base.read_text().split('rows=[check_case',1)[0],str(base)+' [definitions only]','exec'),env)
row=env['check_case'](extra['case'])
assert row['bounds']['ell2']==14
assert row['bounds']['ell3']==Q(20,3)
assert row['tau']==Q(327,236)
assert row['criterion_span']==8
for p in env['inputs']['author_pins']:assert hashlib.sha256(Path(p['path']).read_bytes()).hexdigest()==p['sha256']
out={'status':'PASS_NATIVE_INTEGER_EXACT_B_EQUALITY_WITH_TWO_PARTIAL_OVERLAPS','row':row,'base_checker_sha256':extra['base_checker_sha256'],'input_sha256':hashlib.sha256((HERE/'staircase10-top-window-partial-input.json').read_bytes()).hexdigest(),'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'new_search':False,'new_engine':False,'old_eight_cases_rerun':False,'full_goal_complete':False}
(HERE/'staircase10-top-window-partial-check.json').write_text(json.dumps(out,default=str,indent=2)+'\n')
print(json.dumps({**out,'row':{k:v for k,v in row.items() if k!='path'}},default=str,indent=2))
