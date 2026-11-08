"""Three predeclared WP01 formula rays using own prior original-wall replay."""
from pathlib import Path
from fractions import Fraction as Q
import json,hashlib
HERE=Path(__file__).parent
text=(HERE/'three-reflex-coprime-source-width-check.py').read_text().split('\nfixtures=')[0]
changes={
 'Lam=lcm(P,N,K);assert delta<K and gcd(Lam*d2,L)==1':
 'Lam=lcm(P//gcd(P,d0),N//gcd(N,C),K//gcd(K,g1));g=gcd(Lam*d2,L);r=z/e;assert delta<K and (g==1 or (g==2 and r.denominator==1 and int(r)%2));assert Lam*d0%P==0 and Lam*C%N==0 and Lam*g1%K==0',
 'p=(-int(J)*pow(Lam*d2,-1,L))%L':
 'sign=1 if g==1 or int(J)%2==0 else -1;desired=Q(0) if sign==1 else -r;modulus=L//g;rhs=(desired-int(J))/g;assert rhs.denominator==1;p=0 if modulus==1 else (int(rhs)*pow(Lam*d2//g,-1,modulus))%modulus',
 'n+=(Lam//P)*d0*p;m+=(Lam//N)*C*p;k+=(Lam//K)*g1*p':
 'n+=(Lam*d0//P)*p;m+=(Lam*C//N)*p;k+=(Lam*g1//K)*p',
 'assert J.denominator==1 and int(J)%L==0 and ns[\'fold\'](E,L*e)==z':
 'assert J.denominator==1 and ((E-sign*z)/(2*L*e)).denominator==1 and ns[\'fold\'](E,L*e)==z',
 'finalJ=int(J),residuals=':'finalJ=int(J),target_sign=sign,target_gcd=g,residuals='
}
for old,new in changes.items():
 assert text.count(old)==1,old
 text=text.replace(old,new)
namespace={'__file__':str(HERE/'three-reflex-coprime-source-width-check.py'),'__name__':'own_ce04_weighted_period_wrapper'}
exec(compile(text,'<same-own-ray-constructor-with-height-weighted-step>','exec'),namespace)
rows=[
 namespace['ray']('both-even-negative',1,6,2,4,11,1,4,6,9,(2,4),(10,2),11),
 namespace['ray']('both-even-positive',1,6,2,4,11,1,4,6,9,(2,4),(8,2),11),
 namespace['ray']('even-K-positive',2,3,2,4,11,1,5,7,9,(2,4),(16,2),11)]
expected=[(33,Q(8,3),3,-1,0,0),(33,Q(917,6),152,1,7,1),(11,Q(371,6),44,1,1,1)]
for row,want in zip(rows,expected):
 assert (row['Lambda'],row['slope'],row['finalJ'],row['target_sign'],row['M'],row['target_shift'])==want,(row,want)
 e,P,K,L,N,*_=row['parameters'];old=namespace['lcm'](P,N,K)
 assert namespace['gcd'](old*(4-2 if row['label'].startswith('both-even') else 5-2),L)>1
out=dict(status='PASS_THREE_PREDECLARED_WP01_ORIGINAL_WALL_RAYS',rows=rows,cases=len(rows),reflections=sum(x['reflections'] for x in rows),wall_leg_guards=sum(x['wall_leg_guards'] for x in rows),parent_source_pins_before=namespace['before'],parent_source_pins_after=namespace['capture'](),author_code_executed=False,discovery_search_used=False,independent_acceptance=False,whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('rows','parent_source_pins_before','parent_source_pins_after')}))
