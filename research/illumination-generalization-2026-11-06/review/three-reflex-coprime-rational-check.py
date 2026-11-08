"""Independent rational preserving coefficient via Bezout; four prescribed rays."""
from pathlib import Path
from fractions import Fraction as Q
import json,hashlib
HERE=Path(__file__).parent
source=(HERE/'three-reflex-coprime-source-width-check.py').read_text().split('\nfixtures=')[0]
changes={
 "REQUEST=AUTHOR/'three-reflex-coprime-extension-sourcewide-review-request.json'":"REQUEST=AUTHOR/'three-reflex-coprime-extension-rational-review-request.json'",
 'Lam=lcm(P,N,K);assert delta<K and gcd(Lam*d2,L)==1':
 'F=P*N*K;G=gcd(d0*N*K,C*P*K,g1*P*N);Qmin=Q(F,G);primitive_step=Qmin*d2;Lam=Qmin*primitive_step.denominator;alpha=int(Lam*d2);assert Lam*d2==alpha;Z=lcm(P//gcd(P,d0),N//gcd(N,C),K//gcd(K,g1));gamma=gcd(d0//gcd(P,d0),C//gcd(N,C),g1//gcd(K,g1));assert Qmin==Q(Z,gamma) and Lam==Q(Z,gcd(gamma,d2));g=gcd(alpha,L);r=z/e;assert delta<K and (g==1 or (g==2 and r.denominator==1 and int(r)%2));assert all(x.denominator==1 for x in (Lam*d0/P,Lam*C/N,Lam*g1/K))',
 'p=(-int(J)*pow(Lam*d2,-1,L))%L':
 'sign=1 if g==1 or int(J)%2==0 else -1;desired=Q(0) if sign==1 else -r;modulus=L//g;rhs=(desired-int(J))/g;assert rhs.denominator==1;p=0 if modulus==1 else (int(rhs)*pow(alpha//g,-1,modulus))%modulus',
 'n+=(Lam//P)*d0*p;m+=(Lam//N)*C*p;k+=(Lam//K)*g1*p':
 'n+=int(Lam*d0/P)*p;m+=int(Lam*C/N)*p;k+=int(Lam*g1/K)*p',
 "assert J.denominator==1 and int(J)%L==0 and ns['fold'](E,L*e)==z":
 "assert J.denominator==1 and ((E-sign*z)/(2*L*e)).denominator==1 and ns['fold'](E,L*e)==z",
 'finalJ=int(J),residuals=':'finalJ=int(J),primitive_period=Qmin,gamma=gamma,weighted_integer_period=Z,primitive_target_step=primitive_step,target_step=alpha,target_sign=sign,target_gcd=g,residuals='
}
for old,new in changes.items():
 assert source.count(old)==1,old
 source=source.replace(old,new)
ns={'__file__':str(HERE/'three-reflex-coprime-source-width-check.py'),'__name__':'own_rational_preserving_constructor'}
exec(compile(source,'<own-original-wall-constructor-with-Bezout-period>','exec'),ns)
assert ns['REQUEST'].exists();before=ns['capture']()
fixtures=[
 ('CE06-lower',2,3,3,4,11,1,4,6,9,(2,4),(18,2),1),
 ('CE06-upper',2,3,3,4,11,1,4,6,9,(2,8),(18,2),2),
 ('CE06-denominator-two',2,3,3,4,11,1,4,8,10,(2,4),(18,2)),
 ('CE06-optional-negative',1,6,2,4,11,1,4,6,9,(2,4),(10,2),11)]
rows=[ns['ray'](*f) for f in fixtures]
assert (rows[0]['slope'],rows[0]['finalJ'],rows[0]['Lambda'])==(Q(673,3),112,Q(33,2))
assert (rows[1]['slope'],rows[1]['finalJ'],rows[1]['Lambda'])==(148,72,Q(33,2))
assert rows[2]['gamma']==4 and rows[2]['primitive_period']==Q(33,4) and rows[2]['primitive_target_step']==Q(33,2) and rows[2]['Lambda']==Q(33,2)
assert rows[3]['target_sign']==-1 and rows[3]['slope']==Q(8,3) and rows[3]['finalJ']==3
out=dict(status='PASS_INDEPENDENT_CE06_BEZOUT_PERIOD_AND_ACTUAL_TARGETS',request_sha256=hashlib.sha256(ns['REQUEST'].read_bytes()).hexdigest(),source_pins_before=before,source_pins_after=ns['capture'](),rows=rows,cases=len(rows),reflections=sum(x['reflections'] for x in rows),wall_leg_guards=sum(x['wall_leg_guards'] for x in rows),author_code_executed=False,discovery_search_used=False,whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('source_pins_before','source_pins_after','rows')}))
