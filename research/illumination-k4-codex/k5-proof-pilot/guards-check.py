"""Exact isometry and non-vacuity checks of the supplied universal guard."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import importlib.util,json,hashlib
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('audit',ROOT.parent/'persisted-replay/audit.py')
audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)
r=json.loads((ROOT/'cases/I2_1_1-pair0/guard.json').read_text())
original=audit.check_record(r,(2,2),True)
path=[tuple(F(*c) for c in p) for p in r['path']]
matrices=[(a,0,0,b) for a,b in product((1,-1),repeat=2)]+[(0,a,b,0) for a,b in product((1,-1),repeat=2)]
receipts=[]
for g in matrices:
 for origin in ((0,0),(4,-2),(-6,8)):
  def point(p):return (g[0]*p[0]+g[1]*p[1]+origin[0],g[2]*p[0]+g[3]*p[1]+origin[1])
  def tris(raw):return frozenset(tuple(sorted(point(p) for p in t)) for t in raw)
  mapped=tuple(point(p) for p in path);need,forbid=audit.path_requirements(mapped)
  assert need==tris(r['U']) and forbid==tris(r['Z'])
  room=tris(r['room']);assert need<=room and not forbid&room
  # Reversing the connection must give identical tile conditions.
  back_need,back_forbid=audit.path_requirements(tuple(reversed(mapped)))
  assert (need,forbid)==(back_need,back_forbid)
  receipts.append(dict(matrix=g,origin=origin,used=len(need),absent=len(forbid)))
# Bind current proof inputs to the previously completed universal-path audit.
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
old_manifest={v['file']:v['sha256'] for v in json.loads((ROOT.parent/'persisted-replay/manifest.json').read_text())}
assert not json.loads((ROOT.parent/'persisted-replay/result.json').read_text())['failures']
summary=json.loads((ROOT/'pass-summary.json').read_text());sources=summary['input_hashes']
for name,h in sources.items():
 p=ROOT/name;assert digest(p)==h==old_manifest[p.name],name
assert digest(ROOT.parent.parent/'illumination_geometry.py')==digest(ROOT/'inputs/illumination_geometry.py')
assert digest(ROOT.parent/'bounded-proof/encode.py')==digest(ROOT/'inputs/encode.py')
cases=json.loads((ROOT/'inputs/branch-support.json').read_text())['cases'];expected={f"{c['tag']}-pair{i}" for c in cases for i,pair in enumerate(c['mark_pairs'])}
assert expected=={r['tag'] for r in summary['results']} and len(expected)==31
proofs=[];residuals=[]
for r in summary['results']:
 folder=ROOT/'cases'/r['tag'];assert digest(folder/'formula.cnf')==r['cnf_sha256']
 if r['status']=='VERIFIED_UNSAT':
  assert digest(folder/'proof.drat')==r['proof_sha256']
  assert 's VERIFIED' in (folder/'proof-check.log').read_text()
  proofs.append(r['tag'])
 else:
  assert r['status']=='RESIDUAL'
  data=json.loads((folder/'residual-room.json').read_text());g=data['geometry_receipt']
  assert g['simple_polygon'] and g['walls']<=21 and g['tiles']<=38 and len(g['transparent_vertices'])<=5
  residuals.append(dict(tag=r['tag'],sha256=digest(folder/'vertices.json')))
assert len(proofs)==21 and len(residuals)==10 and summary['positive_control']
result=dict(status='PASS',original=original,isometries_checked=len(receipts),reverse_checks=len(receipts),receipts=receipts,old_audited_input_hashes_checked=len(sources),proof_receipts_bound=proofs,residual_packets=residuals,complete_31case_coverage=True,scope='Exact universal guard and all D4/even-translation isometries; no path discovery.')
(ROOT/'guards-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='receipts'},indent=2))
