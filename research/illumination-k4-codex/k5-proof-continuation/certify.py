"""Generate a standalone refutation of one already-UNSAT final fixed formula."""
from pathlib import Path
import json,hashlib,sys,time,threading,subprocess,shutil
from pysat.formula import CNF
from pysat.solvers import Solver
ROOT=Path(__file__).resolve().parent;tag=sys.argv[1];source=ROOT/'cases'/tag;folder=ROOT/'certified'/tag;folder.mkdir(parents=True,exist_ok=False)
sha=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
old=json.loads((source/'result.json').read_text());assert old['status']=='UNSAT_UNVERIFIED'
shutil.copy2(source/'formula.cnf',folder/'formula.cnf');assert sha(folder/'formula.cnf')==old['cnf_sha256']
cnf=CNF(from_file=str(folder/'formula.cnf'));started=time.monotonic();proof=[]
with Solver(name='glucose4',bootstrap_with=cnf.clauses,with_proof=True) as solver:
 timer=threading.Timer(120,solver.interrupt);timer.start()
 try:
  sat=solver.solve_limited(expect_interrupt=True)
  if sat is False:proof=solver.get_proof()
  stats=solver.accum_stats()
 finally:timer.cancel()
status='OPEN_TIMEOUT' if sat is None else 'INCONSISTENT_SAT' if sat else 'UNSAT_UNVERIFIED';exitcode=None
if sat is False:
 with (folder/'proof.drat').open('w') as stream:
  for line in proof:stream.write(line+'\n')
 print('standalone UNSAT',len(proof),'proof lines',flush=True)
 with (folder/'proof-check.log').open('w') as log:
  try:check=subprocess.run([str(ROOT.parent/'bounded-proof/drat-trim'),str(folder/'formula.cnf'),str(folder/'proof.drat')],stdout=log,stderr=subprocess.STDOUT,timeout=120);exitcode=check.returncode
  except subprocess.TimeoutExpired:exitcode='TIMEOUT'
 if exitcode==0 and 's VERIFIED' in (folder/'proof-check.log').read_text():status='VERIFIED_UNSAT'
out=dict(tag=tag,status=status,seconds=round(time.monotonic()-started,3),checker_exit=exitcode,solver_stats=stats,cnf_sha256=sha(folder/'formula.cnf'),source_cnf_sha256=old['cnf_sha256'])
if sat is False:out['proof_sha256']=sha(folder/'proof.drat');out['proof_lines']=len(proof)
(folder/'result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)
