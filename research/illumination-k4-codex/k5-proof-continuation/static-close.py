"""One static necessary-CNF closure attempt with exact area propagation."""
from pathlib import Path
import importlib.util,json,threading,time,hashlib,subprocess
ROOT=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('r',ROOT/'run.py');r=importlib.util.module_from_spec(sp);sp.loader.exec_module(r)
sp=importlib.util.spec_from_file_location('area',ROOT/'area-identity.py');area=importlib.util.module_from_spec(sp);sp.loader.exec_module(area)
folder=ROOT/'static/I2_1_1-pair0';folder.mkdir(parents=True,exist_ok=True)
raw=(ROOT/'learned.jsonl').read_text();lines=raw.splitlines()
if not raw.endswith('\n'):lines=lines[:-1]
records=[json.loads((r.PILOT/'orbit-guard.json').read_text())]+[json.loads(l) for l in lines]
r.write(folder/'guard-prefix.json',dict(records=len(lines),sha256=hashlib.sha256(('\n'.join(lines)+'\n').encode()).hexdigest()))
case=next(c for c in json.loads((r.PILOT/'inputs/branch-support.json').read_text())['cases'] if c['tag']=='I2_1_1');pair=case['mark_pairs'][0]
cnf,pool,x,ts=r.p.model.geometry(case,wmax=21,kmax=5);r.p.frozen_guards(pair,x,cnf);extra=r.guard_clauses(records,pair,x);cnf.extend(list(map(list,extra)));ledger=area.add_area(cnf,pool,x)
cnf.to_file(str(folder/'formula.cnf'));started=time.monotonic();proof=[];model=None
with r.Solver(name='glucose4',bootstrap_with=cnf.clauses,with_proof=True) as solver:
 timer=threading.Timer(30,solver.interrupt);timer.start()
 try:
  sat=solver.solve_limited(expect_interrupt=True)
  if sat is False:proof=solver.get_proof()
  if sat is True:model=set(solver.get_model())
  stats=solver.accum_stats()
 finally:timer.cancel()
status='OPEN_SAT_TIMEOUT' if sat is None else 'RESIDUAL' if sat else 'UNSAT_UNVERIFIED'
if sat is True:
 chosen=[t for t,v in x.items() if v in model];room=dict(triangles=chosen,marked=[[2*a,2*b] for a,b in pair],require_simple=True);receipt=r.p.model.check(room,strict=False);r.write(folder/'residual-room.json',dict(room=room,geometry_receipt=receipt));r.write(folder/'vertices.json',dict(vertices=r.p.boundary(chosen),marked=room['marked']))
if sat is False:
 (folder/'proof.drat').write_text('\n'.join(proof)+'\n')
 with (folder/'proof-check.log').open('w') as log:
  check=subprocess.run([str(r.LEGACY/'drat-trim'),str(folder/'formula.cnf'),str(folder/'proof.drat')],stdout=log,stderr=subprocess.STDOUT,timeout=120)
 if check.returncode==0 and 's VERIFIED' in (folder/'proof-check.log').read_text():status='VERIFIED_UNSAT'
out=dict(status=status,seconds=round(time.monotonic()-started,3),ledger=ledger,guards=len(records),solver_stats=stats,cnf_sha256=r.sha(folder/'formula.cnf'));r.write(folder/'result.json',out);print(json.dumps(out),flush=True)
