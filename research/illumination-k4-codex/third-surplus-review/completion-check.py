"""Completion gate: current explicit proof artifacts, never a discovery search."""
from pathlib import Path
from fractions import Fraction as F
import subprocess,sys,json,hashlib,runpy
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
checker=runpy.run_path(str(ROOT/'lower-bound-proof-audit/full-replay/guard-checker.py'))
tri=lambda t:tuple(sorted(map(tuple,t)))
paths=lambda raw:[tuple(F(*v) for v in p) for p in raw]
scripts=['independent-review/guard-extension-check.py','path-support-check.py','healed-c-check.py','healed-budget-check.py','half-fan-check.py','center-residue-check.py','local-e2-residue-check.py','local-two-unit-check.py','local-three-unit-check.py','local-mixed-check.py','local-mixed-residue-check.py']
checks={}
for s in scripts:
 r=subprocess.run([sys.executable,'-B',str(HERE/s)],capture_output=True,text=True)
 assert r.returncode==0,(s,r.stdout,r.stderr)
 checks[s]='PASS'
archive1=ROOT.parent/'claude-illumination-check/k6-run/cases/I3_00_01_10-pair0/guards.jsonl'
archive2=ROOT.parent/'claude-illumination-check/k6-run/cases/I2_00_11-pair0/guards.jsonl'
archives={p.name+':'+p.parent.name:{'path':p,'bytes':p.read_bytes()} for p in [archive1,archive2]}
for a in archives.values():
 a['hash']=hashlib.sha256(a['bytes']).hexdigest();a['lines']=a['bytes'].splitlines()
a1=archives[archive1.name+':'+archive1.parent.name];a2=archives[archive2.name+':'+archive2.parent.name]
files=['healed-frozen.json','half-fan-frozen.json','center-half-project.json','center-residue-frozen.json','remote-B-project.json','local-e2-project.json','local-e2-residue-frozen.json','local-three-residue-project.json','local-mixed-project.json','local-mixed-residue-frozen.json']
validated={}
for name in files:
 d=json.loads((HERE/name).read_text());a=a1 if d['sha256']==a1['hash'] else a2
 assert d['sha256']==a['hash'],name
 if 'fixture_source_sha256' in d:
  fixtures={'healed-frozen.json':'healed-budget-check.json','half-fan-frozen.json':'half-fan-check.json','center-residue-frozen.json':'center-residue-check.json','local-e2-residue-frozen.json':'local-e2-residue-check.json','local-mixed-residue-frozen.json':'local-mixed-residue-check.json'}
  assert d['fixture_source_sha256']==hashlib.sha256((HERE/fixtures[name]).read_bytes()).hexdigest(),(name,'fixture changed')
 if 'hits' in d:
  assert d['status']=='ALL_COVERED' and not d['uncovered'],(name,'missing residue')
  fixture_name=fixtures.get(name) if 'fixture_source_sha256' in d else None
  if fixture_name:
   fixture_data=json.loads((HERE/fixture_name).read_text())
   fixture_records=fixture_data.get('records',fixture_data.get('rooms',{}))
   if name=='local-e2-residue-frozen.json':
    assert set(d['hits'])==set(fixture_records),(name,'fixture coverage')
    for fixture_id,hit in d['hits'].items():
     room={tri(t) for t in fixture_records[fixture_id]['triangles']}
     need,forbid=checker['path_requirements'](paths(hit['path']))
     assert need<=room and not forbid&room,(name,fixture_id,'fixture guard')
  records=list(d['hits'].values())
 elif 'families' in d:records=[r for v in d['families'].values() for r in v['terms']]
 else:records=d['terms']
 for r in records:
  p=paths(r['path']);assert p[0]==(0,0) and p[-1]==(2,2)
  u,z=checker['path_requirements'](p)
  savedU={tri(t) for t in r.get('required_triangles',r.get('required',[]))}
  savedZ={tri(t) for t in r.get('forbidden_triangles',r.get('forbidden',[]))}
  assert u==savedU and z==savedZ,(name,r['source_line'],'guard changed')
  source=json.loads(a['lines'][r['source_line']-1]);sp=paths(source['path'])
  frame=r['frame'];reverse=r['endpoint_reversal']
  def convert(v):
   if frame=='identity':q=v
   elif frame=='swap_xy':q=(v[1],v[0])
   elif frame=='flip_y':q=(v[0],-v[1])
   elif frame=='rotate90':q=(-v[1],v[0])
   else:raise AssertionError(frame)
   return (2-q[0],2-q[1]) if reverse else q
  pp=[convert(v) for v in sp]
  if reverse:pp.reverse()
  assert pp==p,(name,r['source_line'],'source path mismatch')
 validated[name]={'status':'PASS','retained_paths_replayed':len(records),'sha256':hashlib.sha256((HERE/name).read_bytes()).hexdigest()}
proofs=['theorem.txt','remote-roots.txt','remote-erasure.txt','healed-budget.txt','half-fan.txt','center-half.txt','remote-B.txt','local-e2.txt','local-two-unit.txt','local-three-unit.txt','local-mixed.txt']
out={'status':'PASS','fixed_script_checks':checks,'frozen_receipts':validated,'proof_hashes':{n:hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in proofs},'archive_hashes':{a['path'].parent.name:a['hash'] for a in archives.values()},'scope':'All current explicit proof paths, guard equality, source hashes/lines/frames, and named fixed geometry checks. No room/direction/word/ray discovery or logical proof-coverage inference. Independent hand review and coverage audit remain separate.'}
(HERE/'completion-check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'PASS','scripts':len(checks),'receipts':len(validated),'retained_paths':sum(r['retained_paths_replayed'] for r in validated.values())}))
