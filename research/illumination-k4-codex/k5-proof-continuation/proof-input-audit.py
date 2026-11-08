"""Bind each closed proof CNF to necessary geometry and exact saved path guards."""
from pathlib import Path
import importlib.util,json,hashlib
ROOT=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('r',ROOT/'run.py');r=importlib.util.module_from_spec(sp);sp.loader.exec_module(r)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
summary=json.loads((ROOT/'summary.json').read_text());raw=(ROOT/'learned.jsonl').read_text();lines=raw.splitlines()
if not raw.endswith('\n'):lines=lines[:-1]
records=[json.loads((r.PILOT/'orbit-guard.json').read_text())]+[json.loads(line) for line in lines if line.strip()]
cases=json.loads((r.PILOT/'inputs/branch-support.json').read_text())['cases'];lookup={f'{c["tag"]}-pair{i}':(c,pair) for c in cases for i,pair in enumerate(c['mark_pairs'])}
results=[]
for result in summary['results']:
 tag=result['tag'];folder=ROOT/'cases'/tag;certificate=result
 alternate=ROOT/'certified'/tag/'result.json'
 if alternate.exists() and json.loads(alternate.read_text())['status']=='VERIFIED_UNSAT':
  certificate=json.loads(alternate.read_text());folder=alternate.parent
 if certificate['status']!='VERIFIED_UNSAT':continue
 assert sha(folder/'formula.cnf')==result['cnf_sha256']==certificate['cnf_sha256'] and sha(folder/'proof.drat')==certificate['proof_sha256']
 assert 's VERIFIED' in (folder/'proof-check.log').read_text()
 library=records[:1]+(json.loads((ROOT/'peer-guards.json').read_text()) if result.get('peer_guards_used') else [])+records[1:]
 indices={(rec['source_case'],rec['generation']):i for i,rec in enumerate(library) if 'source_case' in rec}
 last=max(indices[(tag,x['generation'])] for x in result['generations'] if x['status']=='VERIFIED_LIT_GUARD')
 case,pair=lookup[tag];cnf,pool,x,ts=r.p.model.geometry(case,wmax=21,kmax=5);r.p.frozen_guards(pair,x,cnf)
 extra=r.guard_clauses(library[:last+1],pair,x);cnf.extend(list(map(list,extra)))
 actual=r.p.model.CNF(from_file=str(folder/'formula.cnf'))
 canonical=lambda clauses:{tuple(sorted(clause)) for clause in clauses}
 assert canonical(cnf.clauses)==canonical(actual.clauses),(tag,'premise mismatch')
 results.append(dict(tag=tag,status='PASS',certificate_folder=str(folder.relative_to(ROOT)),guard_prefix=last,necessary_geometry_and_guard_clauses=len(cnf.clauses),unique_clauses=len(canonical(cnf.clauses)),cnf_sha256=sha(folder/'formula.cnf'),proof_sha256=sha(folder/'proof.drat')))
 print(tag,'premise binding PASS',last,'guards',flush=True)
out=dict(status='PASS',checked=len(results),results=results,scope='Every CNF premise equals necessary geometry or a saved universal path implication; no classifier verdict enters a refutation.')
(ROOT/'proof-input-audit.json').write_text(json.dumps(out,indent=2)+'\n')
(ROOT/'certified-summary.json').write_text(json.dumps(dict(first_pass_exclusions=21,continuation_verified=len(results),total_verified=21+len(results),verified_cases=[r['tag'] for r in results],remaining_cases=[x['tag'] for x in summary['results'] if x['tag'] not in {r['tag'] for r in results}]),indent=2)+'\n')
