"""Prescribed baseline RECEIPT reconciliation; never reruns old certificates."""
from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
OWN=ROOT/'illumination-k4-codex';PEER=ROOT/'claude-illumination-check'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    replay=OWN/'lower-bound-proof-audit/full-replay';m=read(replay/'manifest.json');final=read(replay/'final-binding.json');summary=read(replay/'summary.json')
    assert final['status']==summary['status']=='PASS' and final['all_receipts_bound_by_identity'] and final['all_inputs_rehashed_after_all_replays']
    assert len(m['guards'])==52 and len(m['proofs'])==61
    assert sum(r['records'] for r in m['guards'])==193480
    checker_pins=[]
    for key,path in [('guard_checker',Path(m['guard_checker'])),('drat_checker',Path(m['drat_checker'])),('runner',replay/'replay.py')]:
        assert sha(path)==m[key+'_sha256']==final[key+'_sha256'];checker_pins.append(str(path))
    counts={'checked':0,'reflections':0,'vertex_bounces':0,'room_checks':0,'vacuous':0}
    for g in m['guards']:
        r=read(replay/f"guard-{g['index']:02d}.json");assert r['status']=='PASS' and r['path']==g['path']
        assert r['binding']=={'input_sha256':g['sha256'],'checker_sha256':m['guard_checker_sha256'],'runner_sha256':m['runner_sha256'],'expected':g['records']}
        assert r['checked']==g['records']
        for k in counts:counts[k]+=r[k]
    assert counts=={'checked':193480,'reflections':3363038,'vertex_bounces':160831,'room_checks':17879,'vacuous':0}
    for p in m['proofs']:
        r=read(replay/f"drat-{p['tag']}.json");assert r['status']=='VERIFIED' and r['returncode']==0 and r['tag']==p['tag']
        assert r['binding']=={'cnf':p['cnf_sha256'],'proof':p['proof_sha256'],'checker':m['drat_checker_sha256']}
        assert r['bytes']==p['proof_bytes']==Path(p['proof']).stat().st_size
        assert 's VERIFIED' in (replay/f"drat-{p['tag']}.log").read_text()
    arithmetic=read(OWN/'lower-bound-proof-audit/arithmetic/receipts.json');assert arithmetic['status']=='PASS' and arithmetic['cases']==64 and arithmetic['full_run']
    assert len(arithmetic['calls'])==291
    provenance=read(OWN/'lower-bound-proof-audit/provenance/summary.json');assert provenance['status']=='PASS' and provenance['cases']==61 and provenance['matched_unique_clauses']==875332 and provenance['unexplained']==0 and not provenance['failed_cases']
    census=read(OWN/'k6-support-census/count.json');assert (census['total_supports'],census['total_marked_pairs_raw'],census['total_marked_pair_orbits'])==(36,61,56)
    i4=read(OWN/'k6-i4-review/check.json');assert i4['status']=='PASS' and len(i4['cases'])==3 and all(r['DRAT']=='VERIFIED' for r in i4['cases'])
    texts=[OWN/'restricted-theorem-note'/n for n in ['theorem.txt','certificate-appendix.txt','attainment-check.txt']]+[OWN/'lower-bound-proof-audit/hardening-status.txt',replay/'manifest.json',replay/'final-binding.json',replay/'summary.json',OWN/'lower-bound-proof-audit/arithmetic/receipts.json',OWN/'lower-bound-proof-audit/provenance/summary.json',OWN/'k6-support-census/count.json',OWN/'k6-i4-review/check.json']+[PEER/n/'findings.md' for n in ['encoder-necessity-audit','arithmetic-review','provenance-review','attainment-review','review-preprint-v02']]
    out={'status':'BASELINE_ACCEPTED_DEPENDENCY_RECEIPTS_RECONCILED','guard_receipts':52,'guard_records':193480,'I2_I3_verified_receipts_and_logs':61,'I4_verified_receipts':3,'arithmetic_call_receipts':291,'optical_clauses_accounted_for':875332,'counts':counts,'current_checker_hashes_verified':checker_pins,'source_sha256':{str(p.relative_to(ROOT)):sha(p) for p in texts},'personally_done_this_goal':'Read and reconcile hand arguments and later superseding findings; verify all receipt identities/bindings/log outcomes and current checker hashes.','accepted_prior_execution':'Full optical replay, all DRAT replays, complete arithmetic binding and provenance reconstruction as historically accepted.','not_done_this_goal':'No fresh rerun or rehash of8.75GB proof inputs, no new SAT/census/optical discovery, no formalization.','baseline_scope':'W<=21,k<=6,all distinct interior A pairs/supports; attainment22walls,k4 separately hand-accepted.','uncapped_theorem_accepted':False}
    (HERE/'baseline-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='source_sha256'}))
if __name__=='__main__':main()
