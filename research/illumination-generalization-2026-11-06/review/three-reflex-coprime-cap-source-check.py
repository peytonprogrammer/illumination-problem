"""Prescribed CS01 hand-constructor checks; no direction or room discovery."""
from fractions import Fraction as Q
from pathlib import Path
from math import gcd,floor
import ast,json,hashlib
HERE=Path(__file__).parent
ns={'Q':Q,'F':Q}
tree=ast.parse((HERE/'resumed-exact-check.py').read_text());names={'vec','det','dot','edges','on','location','intersect','simple','path_check','fold'}
exec(compile(ast.Module(body=[f for f in tree.body if isinstance(f,ast.FunctionDef) and f.name in names],type_ignores=[]),'<reviewer-geometry>','exec'),ns)
rns={'Q':Q,'ns':ns};tree=ast.parse((HERE/'three-reflex-coprime-independent-check.py').read_text())
exec(compile(ast.Module(body=[f for f in tree.body if isinstance(f,ast.FunctionDef) and f.name=='replay_actual'],type_ignores=[]),'<reviewer-prescribed-ray>','exec'),rns)
def prescribed(label,a,N,L,b,c,h,H,S,T):
    a=Q(a);s,u=map(Q,S);t,v=map(Q,T);A=N*a;w=(N-1)*a;l=(N-L)*a
    assert a>0 and N>=L+2 and L>=2 and 0<b<c<h<H
    assert 0<s<a and h<u<H and l<t<A and 0<v<c
    assert u.denominator==v.denominator==1
    C=int(2*H-u-h);R=int(H-u);g1=h-c;d2=int(c-v);D=C+g1+d2;z=A-t
    assert gcd(C,N)==gcd(N*d2,L)==1 and C<N and C//gcd(C,R)%2==0
    good=[]
    for q in range(D):
        tau=(A+z-s+2*a*q)/D
        if all(((x-a)/(2*a)).denominator!=1 for x in (s+C*tau-A,s+(C+g1)*tau-A)):good.append(q)
    assert good;q=good[-1];tau=(A+z-s+2*a*q)/D
    # gcd(C,N)=1 and C even force N odd in this guarded lemma.
    assert N%2
    M=(pow(C,-1,N)*((N-1)//2-floor((s+C*tau)/(2*a))))%N
    tau+=2*a*M
    X=s+C*tau;m=floor(X/(2*A));z1=X-(2*m+1)*A
    k=floor((z1+g1*tau+a)/(2*a));z2=z1+g1*tau-2*a*k
    assert abs(z1)<a and abs(z2)<a
    J=(z2+d2*tau-z)/(2*a);assert J.denominator==1
    p=(-int(J)*pow(N*d2,-1,L))%L
    tau+=2*a*N*p;m+=C*p;k+=N*g1*p
    assert s+C*tau-(2*m+1)*A==z1
    assert z1+g1*tau-2*a*k==z2
    assert ns['fold'](z2+d2*tau,L*a)==z
    roof_phase=s+R*tau
    assert (roof_phase/A).denominator!=1
    P=[(a,b),(a,h),(w,h),(w,c),(l,c),(l,0),(A,0),(A,H),(0,H),(0,b)]
    return dict(label=label,source=S,target=T,C=C,R=R,q=q,cap_M=M,target_shift=p,slope=tau,**rns['replay_actual'](P,(s,u),(t,v),tau,D))
# Three fixed algebraic fixtures explicitly selected in the hand proof; no sweep.
fixtures=[
 ('depth3-capmark',4,11,4,1,5,8,11,(2,10),(30,2)),
 ('depth5-lowercapmark',4,13,4,1,5,8,13,(2,10),(38,2)),
 ('depth5-nearroof',4,13,4,1,5,8,13,(2,12),(38,2))]
rows=[prescribed(*x) for x in fixtures]
out=dict(status='PASS_PRESCRIBED_CS01_ACTUAL_WALLS',rows=rows,cases=len(rows),reflections=sum(x['reflections'] for x in rows),wall_guards=sum(x['wall_leg_guards'] for x in rows),discovery_search_used=False,author_code_executed=False,independently_accepted=False,whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='rows'}))
