"""LC01 prescribed deterministic first-crossing constructor, not discovery."""
from pathlib import Path
from fractions import Fraction as Q
from math import ceil
import json,hashlib
HERE=Path(__file__).parent
src=(HERE/'three-reflex-coprime-source-width-check.py').read_text().split('\nfixtures=')[0]
old='delta=gcd(P*C,N);Lam=lcm(P,N,K);assert delta<K and gcd(Lam*d2,L)==1'
assert src.count(old)==1
src=src.replace(old,'delta=gcd(P*C,N);Lam=lcm(P,N,K);assert u<h and K>=4 and gcd(Lam*d2,L)==1')
a=src.index('    good=[]');b=src.index('    k=floor(',a)
src=src[:a]+'''    hstep=2*e*(d0+C)/D
    def phase(q):
        tau=(A+z-s+2*e*q)/D
        n=floor((s+d0*tau+a)/(2*a))
        z0=s+d0*tau-2*a*n
        return tau,n,z0,z0+C*tau
    Xinitial=phase(0)[3]
    m=max(0,floor((Xinitial+K*hstep-A-K*e)/(2*A))+1)
    U=(2*m+1)*A+K*e
    assert U>Xinitial+K*hstep and hstep<2*e
    # Derived guaranteed termination bound, not an optical search cutoff.
    bound=max(1,ceil((((U+a)*D/C)-(A+z-s))/(2*e))+1)
    qstar=next(q for q in range(bound+1) if phase(q)[3]>=U)
    assert qstar>K
    block=list(range(qstar-K,qstar))
    assert all(U-2*K*e<phase(q)[3]<U for q in block)
    good=[]
    for q in block:
        tau=phase(q)[0]
        events=[(s+d0*tau-a)/(2*e),(s+(D-d2)*tau-A-K*e)/(2*e)]
        if all(x.denominator!=1 for x in events):good.append(q)
    assert good;q=good[0] if q_fixed is None else q_fixed;assert q in good
    tau0,n,z0,X0=phase(q);tau=tau0;M=0
    z1=X0-(2*m+1)*A
''' +src[b:]
src=src.replace('cap_gcd=delta,slope=','cap_gcd=delta,first_crossing=qstar,termination_bound=bound,cap_block=block,good_indices=good,upper_cap_threshold=U,max_forward_step=hstep,slope=')
ns={'__file__':str(HERE/'three-reflex-coprime-source-width-check.py'),'__name__':'own_lower_first_crossing','ceil':ceil}
exec(compile(src,'<own-lower-first-crossing>','exec'),ns)
fixtures=[
 ('existing-CE03-noncoprime',4,1,4,5,9,1,4,8,11,(2,6),(18,2)),
 ('LC01-cap-gcd17-fails',4,1,4,7,17,1,3,4,21,(2,2),(48,2)),
 ('LC01-native-odd-composite',4,1,5,8,15,1,3,4,19,(2,2),(40,2))]
rows=[ns['ray'](*f) for f in fixtures]
assert rows[1]['cap_gcd']==17 and rows[2]['cap_gcd']==15
out=dict(status='PASS_LC01_THREE_PRESCRIBED_ORIGINAL_RAYS',rows=rows,cases=len(rows),reflections=sum(x['reflections'] for x in rows),wall_leg_guards=sum(x['wall_leg_guards'] for x in rows),author_code_executed=False,discovery_search_used=False,universal_proof_depends_on_hand_argument=True,whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='rows'}))
print(json.dumps([{k:r[k] for k in ['label','first_crossing','cap_block','good_indices','slope','finalJ']} for r in rows],default=str))
