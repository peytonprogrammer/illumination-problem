"""Independent LC02 fixed-constructor and original-wall checks; no discovery."""
from pathlib import Path
from math import ceil
from fractions import Fraction as Q
import hashlib,json
HERE=Path(__file__).parent;AUTHOR=HERE.parent/'construction'
REQUEST=AUTHOR/'three-reflex-coprime-extension-lowerchoice-review-request.json'
def pins():
 if REQUEST.exists():items=json.loads(REQUEST.read_text())['source_pins']
 else:items=[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(AUTHOR.glob('three-reflex-coprime-extension-lowerchoice-*'))]
 for p in items:assert hashlib.sha256(Path(p['path']).read_bytes()).hexdigest()==p['sha256'],p
 return items
before=pins();manifest_start=REQUEST.exists()
source=(HERE/'three-reflex-coprime-source-width-check.py').read_text().split('\nfixtures=')[0]
old='delta=gcd(P*C,N);Lam=lcm(P,N,K);assert delta<K and gcd(Lam*d2,L)==1'
assert source.count(old)==1
source=source.replace(old,'delta=gcd(P*C,N);Lam=lcm(P,N,K);g=gcd(Lam*d2,L);assert P%K==0 and K%g==0 and K>=3*g')
a=source.index('    good=[]');b=source.index('    k=floor(',a)
source=source[:a]+'''    hstep=2*e*(d0+C)/D
    def phase(q):
        tau=(A+z-s+2*e*q)/D
        n=floor((s+d0*tau+a)/(2*a)) if u<h else 0
        z0=s+d0*tau-2*a*n
        return tau,n,z0,z0+C*tau
    Xinitial=phase(0)[3]
    m=max(0,floor((Xinitial+K*hstep-A-K*e)/(2*A))+1)
    U=(2*m+1)*A+K*e
    assert U>Xinitial+K*hstep and hstep<2*e
    bound=max(1,ceil((((U+a)*D/C)-(A+z-s))/(2*e))+1)
    qstar=next(q for q in range(bound+1) if phase(q)[3]>=U)
    assert qstar>K
    block=list(range(qstar-K,qstar));assert all(U-2*K*e<phase(q)[3]<U for q in block)
    compatible=[q for q in block if (q-N*m)%g==0]
    assert len(compatible)==K//g>=3
    psource=P*D//gcd(d0,P*D) if u<h else None
    pright=K*D//gcd(D-d2,K*D)
    assert (psource is None or psource>P>=K) and pright>K>2*g
    good=[]
    for q in compatible:
        tau,n,z0,X=phase(q);z1=X-(2*m+1)*A;Y=z1+g1*tau
        # Check actual source and actual right periods independently.
        sourcebad=u<h and ((s+d0*tau-a)/(2*a)).denominator==1
        rightbad=((Y-K*e)/(2*K*e)).denominator==1
        linearbad=((s+(D-d2)*tau-(2*m+1)*A-K*e)/(2*K*e)).denominator==1
        assert rightbad==linearbad
        if not sourcebad and not rightbad:good.append(q)
    assert good;q=good[0] if q_fixed is None else q_fixed;assert q in good
    tau0,n,z0,X0=phase(q);tau=tau0;M=0;z1=X0-(2*m+1)*A
''' +source[b:]
old='p=(-int(J)*pow(Lam*d2,-1,L))%L'
assert source.count(old)==1
source=source.replace(old,'assert int(J)%g==0;mod=L//g;p=0 if mod==1 else (-int(J)//g*pow(Lam*d2//g,-1,mod))%mod')
source=source.replace('cap_gcd=delta,slope=','cap_gcd=delta,first_crossing=qstar,termination_bound=bound,cap_block=block,target_gcd=g,compatible_indices=compatible,good_indices=good,source_bad_period=psource,right_bad_period=pright,slope=')
ns={'__file__':str(HERE/'three-reflex-coprime-source-width-check.py'),'__name__':'own_target_compatible_lower','ceil':ceil}
exec(compile(source,'<own-LC02-selector-original-walls>','exec'),ns)
fixtures=[
 ('author-A-g2',2,6,6,8,17,1,3,6,23,(4,4),(26,2),19),
 ('author-B-K3',2,3,3,4,9,1,3,6,9,(2,4),(14,2),6),
 ('author-C-mouth',2,3,3,4,9,1,3,6,9,(2,6),(14,2),3),
 ('author-D-upper-zero',2,3,3,4,9,1,3,6,9,(2,8),(14,2),3),
 ('same-A-source-fold-varies',2,6,6,8,17,1,3,6,23,(4,2),(26,2)),
 ('P-greater-than-K-no-K-div-N',2,6,3,5,13,1,3,6,9,(2,4),(22,2))]
rows=[ns['ray'](*f) for f in fixtures]
assert [(r['slope'],r['finalJ']) for r in rows[:4]]==[(Q(16377,20),200),(Q(11,3),0),(Q(16,5),0),(Q(4),0)]
assert rows[0]['cap_block']==list(range(16,22)) and rows[0]['compatible_indices']==[17,19,21]
assert rows[3]['residuals'][1:]==(0,0)
# A: q18 passes physical portal inequalities but has unsolvable target J.
tau=Q(38+4*18,40);z0=4+2*tau;X=z0+34*tau;z1=X-102;Y=z1+3*tau;k=(Y+12)//24;z2=Y-24*k;J=(z2+tau-8)/4
assert abs(z0)<12 and abs(z1)<12 and abs(z2)<12 and J==1
assert all((int(J)+102*p)%8!=0 for p in range(4))
after=pins()
# Existing snapshot entries must remain unchanged even if final manifest arrives.
for p in before:assert hashlib.sha256(Path(p['path']).read_bytes()).hexdigest()==p['sha256']
out=dict(status='PASS_INDEPENDENT_LC02_TARGET_CLASS_AND_ACTUAL_WALLS',source_pins_before=before,source_pins_after=after,manifest_present_at_start=manifest_start,manifest_present_at_end=REQUEST.exists(),rows=rows,cases=len(rows),reflections=sum(r['reflections'] for r in rows),wall_leg_guards=sum(r['wall_leg_guards'] for r in rows),strict_portal_wrong_target_q18_verified=True,author_code_executed=False,discovery_search_used=False,whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('rows','source_pins_before','source_pins_after')}))
