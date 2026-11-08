"""Check DRAT with a separate C program and independently validate connectivity cuts."""
from pathlib import Path
import json,hashlib,subprocess,sys
HERE=Path(__file__).resolve().parent

def verify(folder):
 result=json.loads((folder/'result.json').read_text())
 if result['status']!='UNSAT':return dict(tag=result['tag'],status=result['status'])
 tiles={tuple(sorted(map(tuple,t))):v for t,v in json.loads((folder/'tile-variables.json').read_text())}
 from itertools import combinations
 owners={}
 for t in tiles:
  for e in combinations(t,2):owners.setdefault(e,[]).append(t)
 adj={t:set() for t in tiles}
 for ts in owners.values():
  if len(ts)==2:a,b=ts;adj[a].add(b);adj[b].add(a)
 source=tuple(2*c for c in result['marks'][0]);roots={t for t in tiles if source in t};assert len(roots)==8
 for cut in json.loads((folder/'connectivity-cuts.json').read_text()):
  C={tuple(sorted(map(tuple,t))) for t in cut['component']};seed=tuple(sorted(map(tuple,cut['seed'])))
  assert seed in C and not roots&C
  boundary=set().union(*(adj[t] for t in C))-C
  assert boundary=={tuple(sorted(map(tuple,t))) for t in cut['boundary']}
  assert cut['clause']==[-tiles[seed]]+[tiles[t] for t in sorted(boundary)]
 # A proof can be large; stream checker stdout to its per-case file.
 with (folder/'verify.log').open('w') as log:
  run=subprocess.run([str(HERE/'drat-trim'),str(folder/'formula.cnf'),str(folder/'proof.drat')],stdout=log,stderr=subprocess.STDOUT,timeout=600)
 log=(folder/'verify.log').read_text();ok='s VERIFIED' in log
 out=dict(tag=result['tag'],status='VERIFIED' if ok else 'CHECK_FAILED',checker_exit=run.returncode,
          formula_sha256=hashlib.sha256((folder/'formula.cnf').read_bytes()).hexdigest(),proof_sha256=hashlib.sha256((folder/'proof.drat').read_bytes()).hexdigest(),connectivity_cuts_checked=result['connectivity_cuts'])
 (folder/'verification.json').write_text(json.dumps(out,indent=2)+'\n');return out

if __name__=='__main__':print(json.dumps(verify(HERE/'cases'/sys.argv[1])),flush=True)
