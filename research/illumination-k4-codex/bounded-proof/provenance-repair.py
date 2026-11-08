"""Link every adopted contradiction to frozen reviewed source and inputs.
No solver or optical discovery: regenerate formulas, compare, replay DRAT.
"""
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import hashlib, json, shutil, subprocess, sys
B=Path(__file__).resolve().parent
P=B/'provenance'
PEER=B.parent.parent/'claude-illumination-check/drat-review'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for block in iter(lambda:f.read(1048576),b''): h.update(block)
 return h.hexdigest()
def save(p,obj):p.write_text(json.dumps(obj,indent=2)+'\n')
def one(tag):
 run=subprocess.run([sys.executable,'-B',str(P/'regenerate.py'),tag],capture_output=True,text=True)
 (P/'logs'/f'{tag}.log').write_text(run.stdout+run.stderr)
 if run.returncode:raise RuntimeError((tag,run.stderr))
 return json.loads(run.stdout)
if __name__=='__main__':
 P.mkdir(exist_ok=True);(P/'logs').mkdir(exist_ok=True)
 frozen=P/'frozen';fb=frozen/'illumination-k4-codex/bounded-proof';fb.mkdir(parents=True,exist_ok=True)
 assert not (P/'adopted.json').exists(),'Already adopted: use provenance/regenerate.py and verify.py for read-only reconstruction'
 # Preserve original final artifacts before replacing anything.
 archive=P/'original-final';archive.mkdir(exist_ok=True)
 for name in ('proof-manifest.json','source-lock.json','summary.json','findings.md','encoding-proof.md'):
  
  if not (archive/name).exists():shutil.copy2(B/name,archive/name)
 for f in (B/'cases').iterdir():
  if not f.is_dir():continue
  out=archive/'cases'/f.name;out.mkdir(parents=True,exist_ok=True)
  for name in ('formula.cnf','proof.drat','verification.json','verify.log','result.json','tile-variables.json','connectivity-cuts.json'):
   if (f/name).exists() and not (out/name).exists():shutil.copy2(f/name,out/name)
 shutil.copy2(B/'encode.py',fb/'encode.py')
 shutil.copy2(B/'inputs/illumination_geometry.py',frozen/'illumination_geometry.py')
 assert sha(B.parent.parent/'illumination_geometry.py')==sha(frozen/'illumination_geometry.py')
 shutil.copy2(B/'inputs/branch-support.json',fb.parent/'branch-support.json')
 assert sha(B.parent/'branch-support.json')==sha(fb.parent/'branch-support.json')
 shutil.copytree(B.parent/'persisted-replay/inputs',fb.parent/'persisted-replay/inputs',dirs_exist_ok=True)
 shutil.copy2(B/'dependencies.lock',P/'dependencies.lock')
 for name in ('regen_solve.py','regen_check.py','regen-drat.txt','regen-solve.txt','regen-results.txt'):
  shutil.copy2(PEER/name,P/('peer-'+name))
 save(P/'source-input-lock.json',[dict(path=str(p.relative_to(P)),sha256=sha(p)) for p in sorted(frozen.rglob('*')) if p.is_file()])
 cases=json.loads((fb.parent/'branch-support.json').read_text())['cases']
 tags=[f'{c["tag"]}-pair{i}' for c in cases for i in range(len(c['mark_pairs']))]
 with ProcessPoolExecutor(max_workers=4) as ex: results=list(ex.map(one,tags))
 assert len(results)==31 and all(r['status']=='VERIFIED' for r in results)
 save(B/'proof-manifest.json',[json.loads((B/'cases'/t/'verification.json').read_text()) for t in tags])
 save(P/'adopted.json',dict(status='VERIFIED',cases=results,encoder_sha256=sha(fb/'encode.py'),source_input_lock_sha256=sha(P/'source-input-lock.json')))
 save(B/'provenance-repair.json',dict(status='VERIFIED',cases=len(results),byte_exact_regenerations=len(results),fresh_drat_checks=len(results),proof_bytes=sum((B/'cases'/t/'proof.drat').stat().st_size for t in tags),clauses=sum(r['clauses'] for r in results)))
 print((B/'provenance-repair.json').read_text(),flush=True)
