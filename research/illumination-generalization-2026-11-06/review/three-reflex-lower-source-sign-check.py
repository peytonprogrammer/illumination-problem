"""Prescribed LS01 lower and SS01 upper actual-source-sign replays."""
from fractions import Fraction as Q
from math import gcd,lcm,floor,ceil
from pathlib import Path
import ast,json,hashlib
HERE=Path(__file__).parent
REQ=HERE.parent/'construction/three-reflex-equal-arm-source-sign-review-request.json'
def pins():
    rows=json.loads(REQ.read_text())['source_pins']
    for row in rows:assert hashlib.sha256(Path(row['path']).read_bytes()).hexdigest()==row['sha256']
    return rows
before=pins();request_hash=hashlib.sha256(REQ.read_bytes()).hexdigest()
ns={'Q':Q,'F':Q}
tree=ast.parse((HERE/'resumed-exact-check.py').read_text())
names={'vec','det','dot','edges','on','location','intersect','simple','path_check','fold'}
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef)
    and n.name in names],type_ignores=[]),'<reviewer-geometry>','exec'),ns)
tree=ast.parse((HERE/'three-reflex-coprime-independent-check.py').read_text())
rns={'Q':Q,'ns':ns}
exec(compile(ast.Module(body=[next(n for n in tree.body if isinstance(n,ast.FunctionDef)
    and n.name=='replay_actual')],type_ignores=[]),'<reviewer-first-wall>','exec'),rns)
def v2(n):return (n&-n).bit_length()-1
def check(label,e,P,N,L,b,c,h,H,S,T,upper=False,expected=None):
    e=Q(e);s,u=map(Q,S);target,v=map(Q,T)
    a=e*P;A=e*N;B=e*L;z=A-target;beta=H-h
    assert P<L and L&(L-1)==0 and N>P+L and v2(N)==v2(P)+1
    assert 0<b<c<h<H and h%2==0 and c%2 and 0<s<a and b<u<H
    assert A-B<target<A and 0<v<c and u.denominator==v.denominator==1
    assert int(u)%2==int(v)%2==0
    f=int((h-v)/2);g1=h-c;d2=int(c-v)
    if upper:
        assert u>=h
        n=int((2*H-h-u)/2);d=n+f;hh=gcd(n*P,N*f)
        assert 2*hh>d*P and hh==n*P and n>f
        di=0;dm=1;dj=N*f//hh
    else:
        assert u<h
        alpha=int((h-u)/2);d=alpha+beta+f;hh=gcd(gcd(N*alpha,P*beta),N*f)
        di=N*alpha//hh;dm=P*beta//hh;dj=N*f//hh
    seeds=[]
    for sign in (1,-1):
        if upper:
            C=(f*(sign*s-A)+n*z)/d
            j=-floor(C/(2*n*a/d)+Q(1,2));i=0
        else:
            la=-sign*s/(2*a)-Q(alpha*N,2*P*beta)
            mu=z/(2*a)-Q(f*N,2*P*beta)
            i=-floor(la+Q(1,2));j=-floor(mu+Q(1,2))
        m=0;q=P*i+N*m+P*j
        tau=(A+z-sign*s+2*e*q)/(2*d)
        x0=sign*s if upper else sign*s+2*alpha*tau-2*a*i
        x=x0+2*beta*tau-(2*m+1)*A if not upper else sign*s+2*n*tau-(2*m+1)*A
        r=x+g1*tau;k=floor((r+a)/(2*a));w=r-2*a*k
        assert abs(x)<a and (upper or abs(x0)<a)
        seeds.append(dict(sign=sign,i=i,m=m,j=j,q=q,tau=tau,x0=x0,x=x,r=r,k=k,w=w))
    plus,minus=seeds
    if upper:
        delta_j=plus['j']-minus['j'];assert delta_j in (0,-1)
        assert (plus['r']-minus['r'])/a==Q(d2,d)*(s/a)+Q(2*n+g1,d)*delta_j
    else:
        delta_i=plus['i']-minus['i'];assert delta_i in (0,1)
        assert plus['j']==minus['j']
        diff=Q(d2,d)*(s-a*delta_i)
        assert plus['r']-minus['r']==diff and 0<abs(diff)<2*a
    assert any(abs(row['w'])<a for row in seeds)
    fiber_ratio=Q(g1*N,2*hh)
    chosen=minus if abs(minus['w'])<a else plus
    sign=chosen['sign'];i=chosen['i'];m=chosen['m'];j=chosen['j'];q=chosen['q']
    dq=P*di+N*dm+P*dj
    lift=max(0,ceil(Q(-m,dm)),ceil(Q(-q,dq)),ceil(Q(-i,di)) if di else 0)
    i+=di*lift;m+=dm*lift;j+=dj*lift;q+=dq*lift
    def state():
        tau=(A+z-sign*s+2*e*q)/(2*d)
        x0=sign*s if upper else sign*s+2*alpha*tau-2*a*i
        x=sign*s+2*n*tau-(2*m+1)*A if upper else x0+2*beta*tau-(2*m+1)*A
        k=floor((x+g1*tau+a)/(2*a));w=x+g1*tau-2*a*k
        assert tau>0 and min(i,m,q,k)>=0 and abs(x)<a and (upper or abs(x0)<a)
        return tau,x0,x,k,w
    tau,x0,x,k,w=state()
    if abs(w)==a:
        assert fiber_ratio.denominator>1
        i+=di;m+=dm;j+=dj;q+=dq;tau,x0,x,k,w=state()
    assert abs(w)<a
    literal=[x0,x,w]
    D0=gcd(g1*N,2*hh);B0=2*hh//D0;deltaM=Q(N*d2,D0)
    assert deltaM.denominator==1 and int(deltaM)%2
    Lam=lcm(P,N);Gamma=gcd(Lam*d2,L);rho=Gamma//2**v2(P)
    blocks=(-(j-k)*pow(int(deltaM),-1,rho))%rho
    i+=di*B0*blocks;m+=dm*B0*blocks;j+=dj*B0*blocks;q+=dq*B0*blocks
    tau,x0,x,k,w=state();assert [x0,x,w]==literal
    J=P*(j-k);assert J%Gamma==0;mod=L//Gamma
    p=(-J//Gamma*pow(Lam*d2//Gamma,-1,mod))%mod if mod>1 else 0
    if upper:m+=2*n*Lam//N*p
    else:i+=2*alpha*Lam//P*p;m+=2*beta*Lam//N*p
    j+=2*f*Lam//P*p;q+=2*d*Lam*p
    final,x0,x,k,w=state();assert [x0,x,w]==literal
    E=w+d2*final;assert (E-z)%(2*B)==0
    if expected is not None:assert final==expected
    polygon=[(a,b),(a,h),(A-a,h),(A-a,c),(A-B,c),(A-B,0),(A,0),(A,H),(0,H),(0,b)]
    result=rns['replay_actual'](polygon,(s,u),(target,v),sign*final,2*d)
    return dict(label=label,parameters=[e,P,N,L,b,c,h,H],S=S,T=T,upper=upper,
        H0=hh,fiber_ratio=fiber_ratio,seeds=seeds,selected_sign=sign,
        delta_index=delta_j if upper else delta_i,lift=lift,blocks=blocks,p=p,
        final_slope=final,final_signed_slope=sign*final,final_indices=[i,m,j,k],E=E,**result)
rows=[check('LS01-odd-beta1-delta_i0',4,1,6,4,1,3,6,7,(2,4),(12,2),expected=Q(47,4)),
      check('LS01-odd-beta5-delta_i1',4,1,6,4,1,3,6,11,(2,4),(12,2),expected=Q(595,8)),
      check('SS01-positive-corner-negative-actual-source-repair',40,1,10,4,1,5,8,14,(26,10),(246,2),True,Q(165,4))]
assert [r['delta_index'] for r in rows[:2]]==[0,1]
assert all(r['selected_sign']==-1 for r in rows)
assert abs(rows[2]['seeds'][0]['w'])==40 and rows[2]['seeds'][0]['tau']==38
assert rows[2]['seeds'][1]['x']==-Q(27,2) and rows[2]['E']==154
assert request_hash==hashlib.sha256(REQ.read_bytes()).hexdigest()
out=dict(status='PASS_PRESCRIBED_LS01_AND_SS01_ACTUAL_SOURCE_SIGNS',request_sha256=request_hash,
    source_pins_before=before,source_pins_after=pins(),rows=rows,cases=3,
    reflections=sum(r['reflections'] for r in rows),wall_leg_guards=sum(r['wall_leg_guards'] for r in rows),
    author_code_executed=False,discovery_search_used=False,LS01_independent_review_pending=True,
    whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['rows','source_pins_before','source_pins_after']}))
