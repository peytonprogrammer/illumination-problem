"""Rebuild a case from frozen reviewed sources; adopt peer proof once, then check."""
from pathlib import Path
import sys,json,hashlib,shutil,subprocess
P=Path(__file__).resolve().parent;B=P.parent;FB=P/'frozen/illumination-k4-codex/bounded-proof'
sys.path.insert(0,str(FB))
import encode
sys.path.insert(0,str(B))
from verify import verify
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
tag=sys.argv[1];base,idx=tag.rsplit('-pair',1)
case=next(c for c in json.loads((FB.parent/'branch-support.json').read_text())['cases'] if c['tag']==base);pair=case['mark_pairs'][int(idx)]
cnf,pool,x,ts=encode.geometry(case);ng=encode.guards(case,pair,x,cnf)
out=P/'regenerated'/tag;out.mkdir(parents=True,exist_ok=True);cnf.to_file(str(out/'formula.cnf'))
peer=B.parent.parent/'claude-illumination-check/drat-review/regen'/tag
folder=B/'cases'/tag
adopting=not (P/'adopted.json').exists()
reference=peer if adopting else folder
assert sha(out/'formula.cnf')==sha(reference/'formula.cnf'),(tag,'regeneration differs')
if adopting:
 for name in ('formula.cnf','proof.drat'):shutil.copy2(peer/name,folder/name)
 (folder/'connectivity-cuts.json').write_text('[]\n')
 (folder/'tile-variables.json').write_text(json.dumps([[t,v] for t,v in x.items()])+'\n')
 meta=dict(tag=tag,status='UNSAT',solver='cadical195',variables=cnf.nv,clauses=len(cnf.clauses),tiles=len(ts),guards=ng,connectivity_cuts=0,full=case['full'],marks=pair,provenance='provenance/frozen; byte-exact regenerated CNF, peer DRAT freshly checked by Codex')
 (folder/'result.json').write_text(json.dumps(meta,indent=2)+'\n')
 receipt=verify(folder)
 assert receipt['status']=='VERIFIED'
else:
 receipt=json.loads((folder/'verification.json').read_text())
 assert receipt['status']=='VERIFIED' and sha(folder/'formula.cnf')==receipt['formula_sha256'] and sha(folder/'proof.drat')==receipt['proof_sha256']
print(json.dumps(dict(tag=tag,status=receipt['status'],formula_sha256=sha(out/'formula.cnf'),clauses=len(cnf.clauses),variables=cnf.nv,regeneration='BYTE_EXACT',fresh_drat_check=adopting)),flush=True)
