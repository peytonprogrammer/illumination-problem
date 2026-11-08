"""Read-only small proof/receipt integrity; writes only review/integrity.json."""
from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    accepted=[item['receipt'] for item in json.loads((HERE/'acceptance.json').read_text())['accepted_milestones']]
    checks=0;receipts=[]
    for name in accepted:
        p=HERE/name;a=json.loads(p.read_text());assert a['whole_goal_complete'] is False
        assert not a.get('findings',a.get('mathematical_findings_remaining',[]))
        for key in ('source_sha256','peer_review_sha256'):
            for rel,h in a.get(key,{}).items():assert sha(HERE/rel)==h,(name,rel);checks+=1
        receipts.append({'receipt':name,'sha256':sha(p),'status':a['status']})
    baseline=json.loads((HERE/'baseline-check.json').read_text())
    for rel,h in baseline['source_sha256'].items():assert sha(HERE.parents[1]/rel)==h,rel;checks+=1
    pending=[]
    for name in sorted(p.name for p in HERE.glob('*-review-request.json')):
        a=json.loads((HERE/name).read_text())
        if 'input' in a:
            assert sha(HERE/a['input'])==a['sha256'];checks+=1
        else:
            assert a.get('source_sha256'),name
        for rel,h in a.get('source_sha256',{}).items():
            assert sha(HERE/rel)==h,(name,rel);checks+=1
        for rel,h in a.get('dependency_receipt_sha256',{}).items():assert sha(HERE/rel)==h,(name,rel);checks+=1
        candidate=name.replace('-review-request.json','-acceptance.json')
        reconciled=candidate if (HERE/candidate).exists() else None
        pending.append({'request':name,'input':a.get('input',list(a.get('source_sha256',{}))),'sha256':a.get('sha256',a.get('source_sha256')),'status':'RECONCILED_IN_ACCEPTANCE' if reconciled else 'FROZEN_REVIEW_REQUEST_NOT_ACCEPTANCE','receipt':reconciled})
    global_a=json.loads((HERE/'acceptance.json').read_text());status=json.loads((HERE/'status.json').read_text())
    assert not global_a['whole_goal_complete'] and not status['whole_goal_complete']
    waiver=json.loads((HERE/'native-budget-configuration.json').read_text())
    if status.get('native_enforcement_waived_by_user'):
        assert waiver.get('native_enforcement_waived_by_user') is True
        assert status['saved_native_token_budget'] is None
        assert status['native_limit_confirmed_by_readback'] is False
    else:
        assert status['saved_native_token_budget']==1000000 and status['native_limit_confirmed_by_readback']
    exact=HERE/'half-turn-check.json'
    if exact.exists():
        a=json.loads(exact.read_text())
        assert a['status']=='EXACT_GROUP_AND_RIEMANN_HURWITZ_GUARDS_PASS'
        assert a['angle_cases']==8 and a['necessary_inventory_summaries']==118
        for rel,h in a['source_sha256'].items():assert sha(HERE/rel)==h,rel;checks+=1
    for name in ('T-room-check.json','uneven-T-check.json','eight-wall-turn-check.json','wide-middle-constructor-check.json','wide-middle-boundary-controls.json','staircase-window-check.json','staircase-floor-check.json','staircase-roof-check.json','staircase-overlap-check.json','whole-staircase-check.json'):
        a=json.loads((HERE/name).read_text())
        assert a['whole_goal_complete'] is False
        for rel,h in a.get('source_sha256',{}).items():assert sha(HERE/rel)==h,(name,rel);checks+=1
    for item in global_a['accepted_milestones']:assert sha(HERE/item['receipt'])==item['sha256'];checks+=1
    out={'status':'SMALL_PROOF_RECEIPT_INTEGRITY_PASS','checks':checks,'accepted_partial_receipts':receipts,'pending_requests':pending,'whole_uncapped_theorem_accepted':False,'limits':'Integrity and scope reconciliation only. No newproof execution,8.75GBrehash,formalization or mainuncappedtheorem acceptance.'}
    (HERE/'integrity.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('accepted_partial_receipts','pending_requests')}))
if __name__=='__main__':main()
