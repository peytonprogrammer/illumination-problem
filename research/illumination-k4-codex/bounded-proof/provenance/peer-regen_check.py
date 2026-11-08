"""Regenerate each case CNF from encode.py (geometry + guards + recorded cuts) and compare to formula.cnf."""
import sys,json,hashlib,io
from pathlib import Path
B=Path('<SOURCE_WORKSPACE>/.context/illumination-k4-codex/bounded-proof')
sys.path.insert(0,str(B))
import encode
cases={c['tag']:c for c in json.loads((B.parent/'branch-support.json').read_text())['cases']}
def clauses_of(path):
 out=[]
 for line in path.read_text().splitlines():
  if not line or line[0] in 'cp':continue
  out.append(tuple(map(int,line.split()[:-1])))
 return out
tag=sys.argv[1];base,idx=tag.rsplit('-pair',1);idx=int(idx);case=cases[base];pair=case['mark_pairs'][idx]
cnf,pool,x,ts=encode.geometry(case);encode.guards(case,pair,x,cnf)
cuts=json.loads((B/'cases'/tag/'connectivity-cuts.json').read_text())
for c in cuts:cnf.append(c['clause'])
mine=[tuple(c) for c in cnf.clauses];theirs=clauses_of(B/'cases'/tag/'formula.cnf')
same_seq=mine==theirs;same_set=set(map(lambda c:tuple(sorted(c)),mine))==set(map(lambda c:tuple(sorted(c)),theirs))
print(tag,'EXACT' if same_seq else ('SAMESET' if same_set else 'DIFF'),len(mine),len(theirs),len(cuts),flush=True)
