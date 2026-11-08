"""Fresh proofs from the reviewed encode.py: encode, solve with proof logging, write CNF+DRAT here."""
import sys,json,time
from pathlib import Path
from collections import defaultdict
B=Path('<SOURCE_WORKSPACE>/.context/illumination-k4-codex/bounded-proof')
sys.path.insert(0,str(B))
import encode
from pysat.solvers import Solver
cases={c['tag']:c for c in json.loads((B.parent/'branch-support.json').read_text())['cases']}
tag=sys.argv[1];base,idx=tag.rsplit('-pair',1);case=cases[base];pair=case['mark_pairs'][int(idx)]
out=Path('regen')/tag;out.mkdir(parents=True,exist_ok=True);t0=time.monotonic()
cnf,pool,x,ts=encode.geometry(case);encode.guards(case,pair,x,cnf)
s=tuple(2*c for c in pair[0]);root=next(t for t in ts if s in t)
adj=defaultdict(set)
for ids in encode.owners_of(ts).values():
 if len(ids)==2:a,b=[ts[i] for i in ids];adj[a].add(b);adj[b].add(a)
cuts=0
with Solver(name='cadical195',bootstrap_with=cnf.clauses,with_proof=True) as S:
 while True:
  if not S.solve():status='UNSAT';break
  m=set(S.get_model());sel=[t for t in ts if x[t] in m];parts=encode.components(sel)
  if len(parts)==1:status='RESIDUAL';json.dump(sel,open(out/'residual.json','w'));break
  for part in parts:
   if root in part:continue
   bd=set().union(*(adj[t] for t in part))-part;seed=min(part)
   cl=[-x[seed]]+[x[t] for t in sorted(bd)];S.add_clause(cl);cnf.append(cl);cuts+=1
 proof=S.get_proof() if status=='UNSAT' else []
cnf.to_file(str(out/'formula.cnf'))
if proof:(out/'proof.drat').write_text('\n'.join(proof)+'\n')
print(tag,status,'cuts',cuts,'sec',round(time.monotonic()-t0,1),flush=True)
