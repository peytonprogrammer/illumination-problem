"""Independent LC03 residue-grid constructor; five prescribed actual rays."""
from pathlib import Path
from fractions import Fraction as Q
from math import ceil
import hashlib,json
HERE=Path(__file__).parent;AUTHOR=HERE.parent/'construction';REQUEST=AUTHOR/'three-reflex-coprime-extension-reducedgrid-review-request.json'
def pins():
 items=json.loads(REQUEST.read_text())['source_pins']
 for p in items:assert hashlib.sha256(Path(p['path']).read_bytes()).hexdigest()==p['sha256'],p
 return items
before=pins();request_hash=hashlib.sha256(REQUEST.read_bytes()).hexdigest()
source=(HERE/'three-reflex-coprime-source-width-check.py').read_text().split('\nfixtures=')[0]
old='delta=gcd(P*C,N);Lam=lcm(P,N,K);assert delta<K and gcd(Lam*d2,L)==1'
assert source.count(old)==1
source=source.replace(old,'delta=gcd(P*C,N);Lam=lcm(P,N,K);g=gcd(Lam*d2,L);assert P%g==0 and K%g==0 and K>=2*g')
a=source.index('    good=[]');b=source.index('    k=floor(',a)
source=source[:a]+'''    ep=e*g;Pp=P//g;Kp=K//g
    rho=2*ep*(d0+C)/D
    taumax=(A+z-s+2*e*(g-1))/D
    B=a+C*taumax
    m=max(0,floor((B+4*rho-A-K*e)/(2*A))+1)
    U=(2*m+1)*A+K*e
    assert U>B+4*rho
    cap_m_seed=m
    residue=N*m%g
    taur=(A+z-s+2*e*residue)/D
    def phase(j):
        q=residue+g*j;tau=(A+z-s+2*e*q)/D
        n=floor((s+d0*tau+a)/(2*a)) if u<h else 0
        z0=s+d0*tau-2*a*n
        return q,tau,n,z0,z0+C*tau
    assert phase(0)[4]<B
    bound=max(1,ceil((((U+a)/C)-taur)*D/(2*ep))+1)
    jstar=next(j for j in range(bound+1) if phase(j)[4]>=U)
    assert jstar>4
    pS=Pp*D//gcd(d0,Pp*D) if u<h else None;pR=D//gcd(D-d2,D)
    def sbad(j):return u<h and ((s+d0*phase(j)[1]-a)/(2*a)).denominator==1
    def rbad(j):return ((s+(D-d2)*phase(j)[1]-(2*m+1)*A-K*e)/(2*ep)).denominator==1
    js=list(range(jstar-4,jstar));inside=[j for j in js if U-2*K*e<phase(j)[4]<U]
    good=[j for j in inside if not sbad(j) and not rbad(j)];assert good
    if u<h:
        assert not sbad(jstar)
        if pR==2:
            branch='right-period-two';assert rho<ep and pS!=2 and inside==js
        elif pS==2:
            branch='source-period-two';assert Pp==1 and d0*2==D and pR>2
            assert all(j in inside and not sbad(j) for j in [jstar-2,jstar-4])
        else:
            branch='both-periods-at-least-three';assert pS>=3 and pR>=3
            if all(sbad(j) or rbad(j) for j in [jstar-1,jstar-2]):
                assert jstar-3 in good
    else:
        branch='no-source-band';assert all(j in inside for j in [jstar-1,jstar-2])
        assert any(not rbad(j) for j in [jstar-1,jstar-2])
    if q_fixed is None:j=good[-1]
    else:
        assert (q_fixed-residue)%g==0;j=(q_fixed-residue)//g;assert j in good
    q,tau0,n,z0,X0=phase(j);tau=tau0;M=0;z1=X0-(2*m+1)*A
''' +source[b:]
source=source.replace('p=(-int(J)*pow(Lam*d2,-1,L))%L','assert int(J)%g==0;mod=L//g;p=0 if mod==1 else (-int(J)//g*pow(Lam*d2//g,-1,mod))%mod')
source=source.replace('cap_gcd=delta,slope=','cap_gcd=delta,target_gcd=g,reduced_widths=(Pp,Kp),eprime=ep,uniform_B=B,initial_cap_m=cap_m_seed,residue=residue,jstar=jstar,selected_j=j,inside_cap_j=inside,good_j=good,period_case=branch,source_bad_period=pS,right_strong_period=pR,slope=')
ns={'__file__':str(HERE/'three-reflex-coprime-source-width-check.py'),'__name__':'own_reduced_residue_grid','ceil':ceil}
exec(compile(source,'<own-LC03-residue-grid-original-walls>','exec'),ns)
fixtures=[
 ('author-A-P-not-multiple-K',2,10,6,8,23,1,3,6,23,(4,4),(34,2),27),
 ('author-B-reduced-source-period2',2,2,4,10,17,1,5,6,7,(2,2),(22,4),28),
 ('author-C-reduced-right-period2',2,2,4,14,19,1,7,8,9,(2,6),(18,2),42),
 ('same-A-mouth-level',2,10,6,8,23,1,3,6,23,(4,6),(34,2)),
 ('same-A-upper-source',2,10,6,8,23,1,3,6,23,(4,22),(34,2))]
rows=[ns['ray'](*f) for f in fixtures]
assert [(r['slope'],r['finalJ']) for r in rows[:3]]==[(Q(55281,20),688),(Q(39,2),0),(Q(4672,5),1162)]
assert [r['jstar'] for r in rows[:3]]==[14,16,22]
assert rows[0]['residue']==1 and 23%rows[0]['target_gcd']!=0
assert rows[1]['period_case']=='source-period-two' and rows[2]['period_case']=='right-period-two'
assert request_hash==hashlib.sha256(REQUEST.read_bytes()).hexdigest()
out=dict(status='PASS_INDEPENDENT_LC03_REDUCED_TARGET_GRID_ACTUAL_RAYS',source_pins_before=before,source_pins_after=pins(),request_sha256=request_hash,rows=rows,cases=len(rows),reflections=sum(r['reflections'] for r in rows),wall_leg_guards=sum(r['wall_leg_guards'] for r in rows),author_code_executed=False,discovery_search_used=False,whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('rows','source_pins_before','source_pins_after')}))
