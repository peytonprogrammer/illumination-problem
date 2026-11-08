"""Read-only proof-receipt integrity audit; writes only own review-index.json.
Never runs peer programs. Integrity is distinct from mathematical coverage.
"""
from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent
BASE=HERE.parent

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    receipts=[BASE/'equal-depth-independent/acceptance.json',BASE/'arbitrary-endpoints-independent/acceptance.json',HERE/'midpoint-acceptance.json',HERE/'repair-acceptance.json',HERE/'centered-acceptance.json',HERE/'phase-lines-acceptance.json',HERE/'exterior-acceptance.json',HERE/'twist-acceptance.json',HERE/'rational-room-audit/acceptance.json',HERE/'auxiliary-acceptance.json',HERE/'corner-removal-acceptance.json',HERE/'horizontal-parity-acceptance.json',HERE/'one-fiber-acceptance.json',HERE/'vertical-escape-acceptance.json',HERE/'lattice-sampling-acceptance.json',HERE/'finite-short-counterexample-verdict.json',HERE/'outer-leg-transfer-acceptance.json',HERE/'short-line-margin-acceptance.json',HERE/'finite-support-audit/acceptance.json',HERE/'critical-rectangles-acceptance.json',HERE/'three-pass-acceptance.json',HERE/'family-joint-margin-acceptance.json',HERE/'residual-rooms-acceptance.json',HERE/'residual-optical-audit/acceptance.json',HERE/'whole-result-acceptance.json']
    records=[];checks=0
    for path in receipts:
        a=json.loads(path.read_text())
        pins=a.get('source_sha256',a.get('sha256',{}));assert pins
        observed=[]
        for rel,h in pins.items():
            target=path.parent/rel
            assert digest(target)==h,('acceptance artifact changed',str(target))
            checks+=1;observed.append(str(target.relative_to(BASE)))
            if target.suffix=='.json':
                data=json.loads(target.read_text())
                # Exact check receipts use BASE-relative hashes for sources.
                for source,expected in data.get('source_sha256',{}).items():
                    root=target.parent if target.name=='review-request.json' else BASE/a.get('source_roots',{}).get(rel,'')
                    assert digest(root/source)==expected,('checked source changed',source)
                    checks+=1
        for rel,expected in a.get('peer_review_sha256',{}).items():
            target=BASE/rel
            assert digest(target)==expected,('peer review changed',rel)
            checks+=1
            if target.suffix=='.json':
                data=json.loads(target.read_text())
                root=BASE/a['peer_check_source_root']
                for source,expected_source in data.get('source_sha256',{}).items():
                    assert digest(root/source)==expected_source,('peer reviewed source changed',source)
                    checks+=1
        for group in ('dependency_receipts_sha256','proof_source_sha256'):
            for rel,expected in a.get(group,{}).items():
                assert digest(BASE/rel)==expected,('final dependency changed',group,rel)
                checks+=1
        records.append({'receipt':str(path.relative_to(BASE)),'sha256':digest(path),'status':a['status'],'pinned_artifacts':observed})
    # The live proof may append new milestones, but the reviewed sections must
    # still agree exactly; changed mathematics needs a separate review receipt.
    live=(BASE/'unequal-depth/proof.md').read_text().split('## 4.')[0]
    assert live==(HERE/'midpoint-source-snapshot.md').read_text(),'peer sections1-3 revised; reconcile review'
    checks+=1
    out={'status':'ACCEPTED_PACKET_INTEGRITY_PASS','checked_hashes_and_snapshot':checks,'receipts':records,'mathematical_scope':'Equal depths, finite-resonance implication, unequal common-core endpoint reduction, four sufficient vertical charts, midpoint vertical-only obstruction, centered two-reflection repair and the full arbitrary-real centered-depth theorem, all noncommensurable depth pairs, irrational exterior-height reduction, irrational horizontal marks via corner-fixing twist, one fixed rational-height room with continuous horizontal coverage, portal-only cap-chart sufficiency via endpoint-loop trimming, horizontal parity and one-fiber transport criteria, vertical denominator escape, uniform q>100finite sampling, exact rejection of the strong norm4necessity premise, outer-simple equal-effective-depth cap transfer with pinned q4portal-coordinate erratum, 20short-relation closed-square uniform margin families, and the complete10critical-lines+11finite-points vertical-failure support theorem with mandatory irrational addendum. The final critical rectangle algebra, three-pass actual geometry,74family uniform margin/cutoff reduction, full22538residual room support,770912clause continuous optical proof and whole quantified theorem are independently accepted. See whole-result-review.md and individual hand reviews for quantified statements.','whole_unequal_depth_theorem_accepted':True,'final_acceptance':'unequal-depth-independent/whole-result-acceptance.json','missing_completion_evidence':[],'limits':'Integrity of final independently accepted whole theorem and all dependency receipts. Mathematical quantifiers and proof are in whole-result-review.md; exact controls do not substitute for the arbitrary-real hand argument.'}
    (HERE/'review-index.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='receipts'}))
if __name__=='__main__':main()
