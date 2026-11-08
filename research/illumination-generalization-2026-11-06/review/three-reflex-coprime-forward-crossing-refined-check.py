"""LC01R seven predeclared deterministic constructor checks; no discovery."""
from pathlib import Path
from fractions import Fraction as Q
import json
HERE=Path(__file__).parent
source=(HERE/'three-reflex-coprime-forward-crossing-check.py').read_text().split('\nfixtures=')[0]
source=source.replace("K>=4 and gcd(Lam*d2,L)==1","K>=2 and gcd(Lam*d2,L)==1")
source=source.replace('Xinitial+K*hstep','Xinitial+4*hstep').replace('qstar>K','qstar>4')
a=source.index('    block=list(range(qstar-K,qstar))');b=source.index('    tau0,n,z0,X0=phase(q);',a)
source=source[:a]+'''    pS=P*D//gcd(d0,P*D);pR=D//gcd(D-d2,D)
    assert pS>P and pR>=2
    block=list(range(qstar-4,qstar))
    inside=[q for q in block if U-2*K*e<phase(q)[3]<U]
    def source_bad(q):return ((s+d0*phase(q)[0]-a)/(2*a)).denominator==1
    def right_bad(q):return ((s+(D-d2)*phase(q)[0]-A-K*e)/(2*e)).denominator==1
    assert not source_bad(qstar)
    if pR==2:
        branch='right-period-two';assert pS!=2 and hstep<e and inside==block
    elif pS==2:
        branch='source-period-two';assert P==1 and d0*2==D and pR>2
        assert all(q in inside and not source_bad(q) for q in (qstar-2,qstar-4))
        assert phase(qstar)[3]-phase(qstar-2)[3]==4*e*C/D
        assert phase(qstar)[3]-phase(qstar-4)[3]==8*e*C/D
    else:
        branch='both-periods-at-least-three';assert pS>=3 and pR>=3
        if all(source_bad(q) or right_bad(q) for q in (qstar-1,qstar-2)):
            assert qstar-3 in inside and not source_bad(qstar-3) and not right_bad(qstar-3)
    good=[q for q in inside if not source_bad(q) and not right_bad(q)]
    assert good;q=good[-1] if q_fixed is None else q_fixed;assert q in good
''' +source[b:]
source=source.replace('cap_block=block,good_indices=good,','cap_block=block,inside_cap_indices=inside,good_indices=good,period_case=branch,source_bad_period=pS,right_bad_period=pR,')
ns={'__file__':str(HERE/'three-reflex-coprime-forward-crossing-check.py'),'__name__':'own_refined_crossing'}
exec(compile(source,'<own-refined-first-crossing>','exec'),ns)
fixtures=[
 ('LC01-existing-CE03',4,1,4,5,9,1,4,8,11,(2,6),(18,2)),
 ('LC01-cap-gcd17',4,1,4,7,17,1,3,4,21,(2,2),(48,2)),
 ('LC01-odd-composite',4,1,5,8,15,1,3,4,19,(2,2),(40,2)),
 ('existing-CE07-K2',4,1,2,3,8,1,4,6,7,(2,4),(26,2)),
 ('existing-CE04-P2K2',1,2,2,3,7,1,4,5,6,(1,4),(5,2)),
 ('prescribed-source-period2',4,1,2,3,8,1,5,6,7,(2,2),(26,4)),
 ('prescribed-right-period2',4,1,2,3,8,1,7,8,9,(2,6),(26,2))]
rows=[ns['ns']['ray'](*f) for f in fixtures]
assert rows[-2]['period_case']=='source-period-two' and rows[-1]['period_case']=='right-period-two'
out=dict(status='PASS_LC01R_SEVEN_PRESCRIBED_ORIGINAL_RAYS',rows=rows,cases=len(rows),reflections=sum(x['reflections'] for x in rows),wall_leg_guards=sum(x['wall_leg_guards'] for x in rows),author_code_executed=False,discovery_search_used=False,whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='rows'}))
print(json.dumps([{k:r[k] for k in ['label','first_crossing','inside_cap_indices','good_indices','period_case','slope','finalJ']} for r in rows],default=str))
