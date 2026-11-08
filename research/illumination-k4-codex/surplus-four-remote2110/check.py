"""Saved-source reconciliation for the independently accepted entire2110 row."""
from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
m=json.loads((HERE/'manifest.json').read_text())
for rel,h in m['source_sha256'].items():assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==h,rel
for name in ['peer-remote-noncritical-independent','peer-remote-critical-L-independent','peer-Bfull-optical-independent','peer-centered-square-independent','peer-B-final-independent']:
 r=json.loads((ROOT/'fourth-surplus-review'/name/'check.json').read_text())
 for rel,h in r['source_sha256'].items():assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==h,(name,rel)
x=m['interfaces'];assert x['total']==44==x['noncritical_D_R_N']+x['critical_L_Tc']+x['critical_B_E']
b=json.loads((HERE/'B-frontier-join.json').read_text());assert b['bound']==13 and b['all_necessary_B_labels']==186 and all(r['remaining']==0 for r in b['summary'].values())
assert not m['independent_review_obligations_open'] and m['bound']==13
for name in ['B-L70-effort-ended.json','centered-unit-effort-ended.json']:
 d=json.loads((HERE/name).read_text());assert d['aggregate_seconds_including_setup_and_proofs']<840
out={'status':'ENTIRE_REMOTE2110_SOURCE_RECONCILIATION_PASS','bound':13,'interfaces':x,'all_review_pins_current':True,'independent_review_obligations_open':[],'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in [HERE/'manifest.json',HERE/'theorem.txt',Path(__file__)]}}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS entire2110<=13;44=24+16+4; ALLfive independentreview receipts and sourcepinscurrent; no remainingrowreview')
