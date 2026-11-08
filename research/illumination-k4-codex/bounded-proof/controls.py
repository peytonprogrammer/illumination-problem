from pathlib import Path
import json,subprocess,sys
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from encode import geometry,guards
from pysat.solvers import Solver
from pysat.formula import CNF
case=json.loads((HERE.parent/'branch-support.json').read_text())['cases'][0]
rooms=[('dark22',json.loads((HERE.parent/'peer-fast-inputs/cand-2_2-1.json').read_text()),22,True),
       ('dark22-cap21',json.loads((HERE.parent/'peer-fast-inputs/cand-2_2-1.json').read_text()),21,False)]
f=HERE.parent/'persisted-replay/inputs/claude-k4-w21-learned-L2,2.jsonl';lit=json.loads(f.read_text().splitlines()[0]);rooms.append(('lit-without-guards',dict(triangles=lit['room']),21,True))
results=[]
for name,room,cap,expected in rooms:
 cnf,pool,x,ts=geometry(case,wmax=cap)
 chosen={tuple(sorted(map(tuple,t))) for t in room['triangles']};assert chosen<=x.keys()
 cnf.extend([[v if tri in chosen else -v] for tri,v in x.items()])
 with Solver(name='glucose4',bootstrap_with=cnf) as s:got=s.solve()
 assert got==expected,(name,got,expected)
 result=dict(name=name,status='PASS',satisfiable=got)
 if name=='lit-without-guards':
  n=guards(case,case['mark_pairs'][0],x,cnf)
  with Solver(name='glucose4',bootstrap_with=cnf) as s:assert not s.solve()
  result['guarded_satisfiable']=False;result['guards']=n
 results.append(result);print(result,flush=True)
# Check independent proof checker on a valid nontrivial proof and a SAT negative control.
cnf=CNF(from_clauses=[[1,2],[-1,2],[1,-2],[-1,-2]])
with Solver(name='glucose4',bootstrap_with=cnf,with_proof=True) as s:assert not s.solve();proof=s.get_proof()
folder=HERE/'controls';folder.mkdir(exist_ok=True);cnf.to_file(str(folder/'unsat.cnf'));(folder/'valid.drat').write_text('\n'.join(proof)+'\n')
run=subprocess.run([str(HERE/'drat-trim'),str(folder/'unsat.cnf'),str(folder/'valid.drat')],text=True,capture_output=True);assert 's VERIFIED' in run.stdout,run.stdout
(folder/'valid.log').write_text(run.stdout+run.stderr)
CNF(from_clauses=[[1,2]]).to_file(str(folder/'sat.cnf'));(folder/'empty.drat').write_text('')
run=subprocess.run([str(HERE/'drat-trim'),str(folder/'sat.cnf'),str(folder/'empty.drat')],text=True,capture_output=True);assert 's VERIFIED' not in run.stdout; (folder/'negative.log').write_text(run.stdout+run.stderr)
(HERE/'controls.json').write_text(json.dumps(dict(status='PASS',room_controls=results,proof_checker_positive=True,proof_checker_negative_rejected=True),indent=2)+'\n')
