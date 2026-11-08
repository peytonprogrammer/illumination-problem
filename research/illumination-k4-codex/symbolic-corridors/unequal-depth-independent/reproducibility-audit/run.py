"""Replay fixed independent verifiers in an isolated copy; never run peer code.
All original proof/certificate bytes are compared before and after replay.
"""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys,tempfile,time,os,signal
HERE=Path(__file__).resolve().parent;BASE=HERE.parents[1]
CHECKS=[
 ('equal-depth-independent/check.py','equal-depth-independent/check.json'),
 ('arbitrary-endpoints-independent/check.py','arbitrary-endpoints-independent/check.json'),
 *[(f'unequal-depth-independent/{n}.py',f'unequal-depth-independent/{n}.json') for n in ('midpoint-check','repair-check','cap-sheet-check','vertical-failure-check','centered-check','centered-source-update','phase-lines-check','exterior-check','twist-check','rational-controls-review')],
 ('unequal-depth-independent/rational-room-audit/verify.py','unequal-depth-independent/rational-room-audit/verification.json'),
 ('unequal-depth-independent/verify-receipts.py','unequal-depth-independent/review-index.json'),
]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    started=time.monotonic()
    sources={str(p.relative_to(BASE)):digest(p) for p in BASE.rglob('*') if p.is_file() and '__pycache__' not in p.parts and HERE not in p.parents}
    records=[]
    with tempfile.TemporaryDirectory(prefix='corridor-independent-replay-') as tmp:
        root=Path(tmp);snapshot=root/'symbolic-corridors'
        shutil.copytree(BASE,snapshot,ignore=shutil.ignore_patterns('__pycache__','reproducibility-audit'))
        dep=root/'single-boundary-blocker';dep.mkdir()
        for name in ('l-monotone-proof.md','l-monotone-peer-review.txt'):
            shutil.copy2(BASE.parent/'single-boundary-blocker'/name,dep/name)
        for script,out in CHECKS:
            t=time.monotonic()
            proc=subprocess.Popen([sys.executable,str(snapshot/script)],cwd=snapshot,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,start_new_session=True)
            timed_out=False
            try:log,_=proc.communicate(timeout=300)
            except subprocess.TimeoutExpired:
                timed_out=True;os.killpg(proc.pid,signal.SIGTERM)
                try:log,_=proc.communicate(timeout=3)
                except subprocess.TimeoutExpired:os.killpg(proc.pid,signal.SIGKILL);log,_=proc.communicate()
            record={'script':script,'output':out,'returncode':proc.returncode,'timed_out':timed_out,'elapsed_seconds':round(time.monotonic()-t,3),'original_sha256':digest(BASE/out),'replay_sha256':digest(snapshot/out),'byte_identical':(BASE/out).read_bytes()==(snapshot/out).read_bytes(),'stdout':log}
            records.append(record)
            print(json.dumps({k:v for k,v in record.items() if k not in ('stdout','original_sha256','replay_sha256')}),flush=True)
            if proc.returncode or timed_out or not record['byte_identical']:break
    changed=[rel for rel,h in sources.items() if not (BASE/rel).is_file() or digest(BASE/rel)!=h]
    # Source originals may be live peer files. Report any change rather than silently recopying.
    result={'status':'ALL_FIXED_INDEPENDENT_CHECKS_REPRODUCED' if len(records)==len(CHECKS) and all(r['byte_identical'] and not r['returncode'] and not r['timed_out'] for r in records) and not changed else 'REPRODUCIBILITY_RECONCILIATION_REQUIRED','checkers_planned':len(CHECKS),'checkers_replayed':len(records),'original_files_verified_unchanged':len(sources)-len(changed),'changed_originals':changed,'elapsed_seconds':round(time.monotonic()-started,3),'records':records,'runner_sha256':digest(Path(__file__)),'limits':'Replays accepted prescribed exact checks only, not peer discovery programs. Confirms reproducibility and original artifact preservation, not full theorem coverage. Fully rational universal case remains open.'}
    (HERE/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='records'}),flush=True)
    if result['status']!='ALL_FIXED_INDEPENDENT_CHECKS_REPRODUCED':raise SystemExit(1)
if __name__=='__main__':main()
