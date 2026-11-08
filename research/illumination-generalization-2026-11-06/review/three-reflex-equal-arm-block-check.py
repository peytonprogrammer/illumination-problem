"""EA06 independent selector and three prescribed original-wall replays."""
from fractions import Fraction as Q
from math import floor, ceil, gcd, lcm
from pathlib import Path
import ast, hashlib, json

HERE = Path(__file__).parent
REQ = HERE.parent / 'construction/three-reflex-equal-arm-block-review-request.json'
request_hash = hashlib.sha256(REQ.read_bytes()).hexdigest()
def pins():
    rows = json.loads(REQ.read_text())['source_pins']
    for row in rows:
        assert hashlib.sha256(Path(row['path']).read_bytes()).hexdigest() == row['sha256']
    return rows
before = pins()
ns = {'Q': Q, 'F': Q}
tree = ast.parse((HERE / 'resumed-exact-check.py').read_text())
names = {'vec','det','dot','edges','on','location','intersect','simple','path_check','fold'}
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n, ast.FunctionDef)
    and n.name in names], type_ignores=[]), '<own-pure-geometry>', 'exec'), ns)
tree = ast.parse((HERE / 'three-reflex-coprime-independent-check.py').read_text())
fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'replay_actual')
rns = {'Q': Q, 'ns': ns}
exec(compile(ast.Module(body=[fn], type_ignores=[]), '<own-first-wall-replay>', 'exec'), rns)

def v2(n):
    assert n > 0
    return (n & -n).bit_length()-1

def check(label,e,P,N,L,b,c,h,H,S,T,expected=None):
    e=Q(e);s,u=map(Q,S);t,v=map(Q,T)
    a=e*P;A=e*N;B=e*L;z=A-t;beta=H-h
    assert P<L and L&(L-1)==0 and N>P+L and v2(N)>v2(P)
    assert h%2==0 and c%2 and beta%2**(v2(N)-v2(P))==0
    assert 0<b<c<h<H and 0<s<a and b<u<=h and A-B<t<A and 0<v<c
    assert u.denominator==v.denominator==1 and int(u)%2==int(v)%2==0
    alpha=(h-u)/2;f=(h-v)/2;g1=h-c;d2=c-v
    d=alpha+beta+f
    if alpha:
        la=-s/(2*a)-alpha*N/(2*P*beta)
        mu=z/(2*a)-f*N/(2*P*beta)
        i=-floor(la+Q(1,2));j=-floor(mu+Q(1,2));m=0
        hh=gcd(gcd(int(N*alpha),P*beta),int(N*f))
        di=int(N*alpha)//hh;dm=P*beta//hh;dj=int(N*f)//hh
    else:
        # Hand-selected Bezout solution for the declared mouth input.
        assert (e,P,N,L,S,T)==(4,1,6,4,(2,6),(12,2))
        i=0;m=0;j=1;hh=gcd(beta*P,int(N*f))
        di=0;dm=beta*P//hh;dj=int(N*f)//hh
        V=f*(s-A)+beta*z
        assert beta*P*j-N*f*m==hh and abs(V+2*e*hh)<e*P*d
    dq=P*di+N*dm+P*dj
    q=P*i+N*m+P*j
    lift=max(0,ceil(Q(-m,dm)),ceil(Q(-q,dq)),ceil(Q(-i,di)) if di else 0)
    i+=di*lift;m+=dm*lift;j+=dj*lift;q+=dq*lift
    def state():
        tau=(A+z-s+2*e*q)/(2*d)
        z0=s+2*alpha*tau-2*a*i
        z1=z0+2*beta*tau-(2*m+1)*A
        k=floor((z1+g1*tau+a)/(2*a))
        z2=z1+g1*tau-2*a*k
        assert tau>0 and min(i,m,q,k)>=0 and abs(z0)<a and abs(z1)<a
        return tau,z0,z1,k,z2
    tau,z0,z1,k,z2=state()
    repaired=abs(z2)==a
    if repaired:
        i+=di;m+=dm;j+=dj;q+=dq
        tau,z0,z1,k,z2=state()
    assert abs(z2)<a and v2(hh)>=v2(N)
    seed=dict(tau=tau,indices=[i,m,j,k],residuals=[z0,z1,z2])
    D0=gcd(g1*N,2*hh);B0=2*hh//D0
    delta_j=Q(2*N*f,D0);delta_k=Q(g1*N,D0);delta_M=Q(N*d2,D0)
    assert delta_j.denominator==delta_k.denominator==delta_M.denominator==1
    assert v2(D0)==v2(N) and int(delta_M)%2 and delta_M>0
    Lam=lcm(P,N);Gamma=gcd(int(Lam*d2),L);rho=Gamma//2**v2(P)
    M=j-k
    blocks=(-M*pow(int(delta_M),-1,rho))%rho if rho>1 else 0
    i+=di*B0*blocks;m+=dm*B0*blocks;j+=dj*B0*blocks;q+=dq*B0*blocks
    tau,x,y,k,w=state()
    assert [x,y,w]==[z0,z1,z2] and j-k==M+blocks*delta_M
    assert P*(j-k)%Gamma==0
    after_block=dict(tau=tau,indices=[i,m,j,k],M=j-k,residuals=[x,y,w])
    mod=L//Gamma
    p=(-int(P*(j-k))//Gamma*pow(int(Lam*d2)//Gamma,-1,mod))%mod if mod>1 else 0
    i+=int(2*alpha*Lam/P)*p;m+=2*beta*Lam//N*p
    j+=int(2*f*Lam/P)*p;q+=int(2*d*Lam)*p
    final,x,y,k,w=state();E=w+d2*final
    assert [x,y,w]==[z0,z1,z2] and (E-z)%(2*B)==0
    assert ns['fold'](E,B)==z and P*(j-k)%L==0
    if expected is not None:assert final==expected
    polygon=[(a,b),(a,h),(A-a,h),(A-a,c),(A-B,c),(A-B,0),(A,0),(A,H),(0,H),(0,b)]
    replay=rns['replay_actual'](polygon,(s,u),(t,v),final,2*d)
    return dict(label=label,parameters=[e,P,N,L,b,c,h,H],S=S,T=T,H0=hh,D0=D0,
        D0_divides_N=N%D0==0,B0=B0,delta_M=delta_M,Gamma=Gamma,rho=rho,
        seed=seed,blocks=blocks,after_block=after_block,p=p,final_slope=final,
        final_indices=[i,m,j,k],E=E,true_bottom_period=2*B,**replay)

rows=[check('EA06-author-lower',4,1,6,4,1,3,6,8,(2,4),(12,2),Q(389,5)),
      check('EA06-D0-not-dividing-N',2,3,30,8,1,5,8,26,(2,2),(50,2)),
      check('EA06-mouth',4,1,6,4,1,3,6,8,(2,6),(12,2),Q(309,4))]
assert rows[0]['final_indices']==[20,6,37,29] and rows[0]['E']==76
assert not rows[1]['D0_divides_N'] and rows[1]['D0']==18 and rows[1]['delta_M']==5
assert rows[2]['seed']['tau']==Q(21,4)
assert request_hash==hashlib.sha256(REQ.read_bytes()).hexdigest()
out=dict(status='PASS_EA06_THREE_PRESCRIBED_ACTUAL_RAYS',request_sha256=request_hash,
    source_pins_before=before,source_pins_after=pins(),rows=rows,cases=len(rows),
    reflections=sum(r['reflections'] for r in rows),wall_leg_guards=sum(r['wall_leg_guards'] for r in rows),
    author_code_executed=False,discovery_search_used=False,whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['rows','source_pins_before','source_pins_after']}))
