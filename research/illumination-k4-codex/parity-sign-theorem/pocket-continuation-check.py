"""Receipt/scope/snapshot audit only. Does not rerun optical discovery."""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import hashlib,json,re
b=Path(__file__).resolve().parent
def read(name):return json.loads((b/name).read_text())
def digest(path):return dict(sha256=hashlib.sha256(path.read_bytes()).hexdigest(),bytes=path.stat().st_size)
upper=read('pocket-end-upper.json');lower=read('pocket-end-lower.json');chain=read('pocket-corridor-chain.json')
assert upper['status']=='PRESCRIBED_UPPER_END_SOURCE_CAP_PASS' and int(upper['determinant'])==10
assert upper['geometry']['walls']==25 and upper['independent_review'].startswith('ACCEPTED')
assert lower['status']=='PRESCRIBED_LOWER_END_SQUARE_AND_RIGHT_CAP_PASS'
assert [(r['cap'],r['geometry']['walls'],int(r['determinant'])) for r in lower['cases']]==[('square',26,-8),('right_triangle',25,-8)]
assert lower['rejected_triangle_suffix']['geometry']['walls']==25
assert lower['rejected_triangle_suffix']['status']=='INVALID_EARLIER_VERTICAL_WALL_HIT'
assert chain['fixed_k']==2 and chain['geometry']['walls']==37
assert chain['independent_review'].startswith('ACCEPTED')
for name in ['pocket-end-upper-review.txt','pocket-end-lower-review.txt','pocket-corridor-chain-review.txt','pocket-end-lower-right-review.txt']:
 assert 'accept' in (b/name).read_text().lower()
for obj in [upper,lower,chain]:assert obj['universal_pocket_detection']=='OPEN' and obj['discovery_runs']==0
text=(b/'pocket-detection.md').read_text()
sections=[int(x) for x in re.findall(r'^## (\d+)\.',text,re.M)]
assert sections==list(range(1,35)),sections
subs=[int(x) for x in re.findall(r'^### 26\.(\d+) ',text,re.M)]
assert subs==list(range(1,16)),subs
blocks=[]
for name in ['findings.md','coverage.md','agenda.md']:
 doc=(b/name).read_text();a='<!-- current-pocket-checkpoint:start -->';z='<!-- current-pocket-checkpoint:end -->'
 assert doc.count(a)==doc.count(z)==1
 blocks.append(doc[doc.index(a):doc.index(z)+len(z)])
assert len(set(blocks))==1
# Live review outputs can mutate. They are excluded, never stamped as verified.
live=[]
excluded={n for item in live for n in item['mutable_outputs_excluded_from_snapshot']}
excluded.update(['manifest.json','checkpoint-verify.json','pocket-continuation-check.json','pocket-continuation-check.log','.DS_Store'])
m=read('manifest.json');old=m['files'];paths={k for k in old if k not in excluded}
paths.update(p.name for p in b.glob('pocket-*') if p.is_file() and p.name not in excluded)
files={}
for rel in sorted(paths):
 p=b/rel;assert p.is_file(),rel;files[rel]=digest(p)
changed=[k for k,v in old.items() if k in files and v!=files[k]]
allowed={'pocket-continuation-check.py','agenda.md','coverage.md','findings.md','pocket-detection.md','pocket-corridor-chain.py','pocket-corridor-chain.json','pocket-corridor-chain.log'}
allowed.update(k for k in files if k.startswith(('pocket-end-upper','pocket-end-lower')))
assert set(changed)<=allowed,sorted(set(changed)-allowed)
m.update(status='ACTIVE_GOAL_COORDINATE_WORK_SEALED_STRUCTURAL_GAP_OPEN',
 review='Scoped upper-end closure and all-k corridor hand proof accepted. Lower square accepted; lower right accepted57809; structural detector gap remains. No universal proof/counterexample.',
 files=files,updated_local=datetime.now(ZoneInfo('America/Los_Angeles')).isoformat(),live_jobs=live)
m['counts'].update(end_prescribed_valid_cases=3,lower_square_prescribed_cases=1,lower_right_prescribed_cases=1)
(b/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
# Read the saved snapshot back and check every recorded byte digest.
saved=read('manifest.json')
for rel,d in saved['files'].items():assert digest(b/rel)==d,rel
out=dict(status='PASS',recorded_files_checked=len(files),changed_prior_snapshot_files=changed,
 newly_recorded_files=sorted(set(files)-set(old)),sections=sections,subsections26=subs,
 actual_endpoint_receipts_checked=4,authoritative_checkpoint_copies=3,
 hand_reviews_checked=['upper8090','lower_square31817','lower_right57809','all_k97361'],live_jobs=[],
 mutable_outputs_excluded=sorted(excluded),goal_complete=False,discovery_runs=0,
 remaining_obligations=['Nright lower-end upperLEFTm1','Nleft lower-end','Disconnected H pockets',
 'Arbitrary-W actual one-corner seed','Nonzero actual pocket defect for arbitrary specified pocket'])
(b/'pocket-continuation-check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
