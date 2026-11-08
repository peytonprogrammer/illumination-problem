"""EA07 prescribed upper selectors and a separately scoped equality check."""
from pathlib import Path
from fractions import Fraction as Q
from math import gcd,lcm,floor,ceil
import ast,json,hashlib
HERE=Path(__file__).parent
REQ=HERE.parent/'construction/three-reflex-equal-arm-upper-columns-review-request.json'
def pins():
    rows=json.loads(REQ.read_text())['source_pins']
    for row in rows:assert hashlib.sha256(Path(row['path']).read_bytes()).hexdigest()==row['sha256']
    return rows
before=pins();request_hash=hashlib.sha256(REQ.read_bytes()).hexdigest()
ns={'Q':Q,'F':Q}
tree=ast.parse((HERE/'resumed-exact-check.py').read_text())
names={'vec','det','dot','edges','on','location','intersect','simple','path_check','fold'}
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef)
    and n.name in names],type_ignores=[]),'<own-geometry>','exec'),ns)
tree=ast.parse((HERE/'three-reflex-coprime-independent-check.py').read_text())
rns={'Q':Q,'ns':ns}
exec(compile(ast.Module(body=[next(n for n in tree.body if isinstance(n,ast.FunctionDef)
    and n.name=='replay_actual')],type_ignores=[]),'<own-first-wall>','exec'),rns)
def bezout(a,b):
    if b==0:return abs(a),1 if a>0 else -1,0
    g,x,y=bezout(b,a%b)
    return g,y,x-(a//b)*y
def v2(n):return (n&-n).bit_length()-1
def check(label,e,P,N,L,b,c,h,H,S,T,equality=False,expected=None):
    e=Q(e);s,u=map(Q,S);target,v=map(Q,T)
    a=e*P;A=e*N;B=e*L;z=A-target
    assert P<L and L&(L-1)==0 and N>P+L and v2(N)==v2(P)+1
    assert 0<b<c<h<H and h%2==0 and c%2 and 0<s<a and h<=u<H
    assert A-B<target<A and 0<v<c and int(u)%2==int(v)%2==0
    n=int((2*H-h-u)/2);f=int((h-v)/2);d=n+f;g1=h-c;d2=int(c-v)
    hh,bm,bj=bezout(-N*f,n*P)
    assert -N*f*bm+n*P*bj==hh
    assert d*P>=2*hh and (d*P==2*hh)==equality
    vm=(-2*N*f,-N*d2);vj=(2*n*P,P*(2*n+g1))
    assert vm[0]*vj[1]-vm[1]*vj[0]==-2*P*N*g1*d
    Y=bm*vm[1]+bj*vj[1];Fy=P*N*g1*d//hh
    assert gcd(Y,Fy)==gcd(vm[1],vj[1])<2*P*d
    fiber_ratio=Q(g1*N,2*hh)
    V=f*(s-A)+n*z
    ell0=-floor(V/(2*e*hh)+Q(1,2))
    columns=[]
    # At most two PREDETERMINED neighboring columns; no ray/direction search.
    x0=(V+2*e*hh*ell0)/d
    neighbor=ell0-1 if x0>0 else ell0+1
    for ell in (ell0,neighbor):
        m=bm*ell;j=bj*ell;q=N*m+P*j
        tau=(A+z-s+2*e*q)/(2*d)
        x=s+2*n*tau-(2*m+1)*A
        right=x+g1*tau
        safe=((right-a)/(2*a)).denominator!=1
        columns.append(dict(ell=ell,m=m,j=j,q=q,tau=tau,x=x,right=right,
            cap_safe=abs(x)<a,right_safe=safe))
    available=[row for row in columns if row['cap_safe']]
    assert available
    if fiber_ratio.denominator==1:
        available=[row for row in available if row['right_safe']]
        assert available
    chosen=available[0];m=chosen['m'];j=chosen['j'];q=chosen['q']
    dm=n*P//hh;dj=N*f//hh;dq=N*dm+P*dj
    lift=max(0,ceil(Q(-m,dm)),ceil(Q(-q,dq)))
    m+=dm*lift;j+=dj*lift;q+=dq*lift
    def state():
        tau=(A+z-s+2*e*q)/(2*d)
        x=s+2*n*tau-(2*m+1)*A
        k=floor((x+g1*tau+a)/(2*a));w=x+g1*tau-2*a*k
        assert tau>0 and min(m,q,k)>=0 and abs(x)<a
        return tau,x,k,w
    tau,x,k,w=state();repair=abs(w)==a
    if repair:
        assert fiber_ratio.denominator>1
        m+=dm;j+=dj;q+=dq;tau,x,k,w=state()
    assert abs(w)<a
    seed=dict(tau=tau,indices=[m,j,k],residuals=[x,w])
    D0=gcd(g1*N,2*hh);B0=2*hh//D0;deltaM=Q(N*d2,D0)
    assert deltaM.denominator==1 and int(deltaM)%2
    Lam=lcm(P,N);Gamma=gcd(Lam*d2,L);rho=Gamma//2**v2(P)
    blocks=(-(j-k)*pow(int(deltaM),-1,rho))%rho
    m+=dm*B0*blocks;j+=dj*B0*blocks;q+=dq*B0*blocks
    tau,x1,k,w1=state();assert [x1,w1]==[x,w]
    J=P*(j-k);assert J%Gamma==0
    mod=L//Gamma;p=(-J//Gamma*pow(Lam*d2//Gamma,-1,mod))%mod if mod>1 else 0
    m+=2*n*Lam//N*p;j+=2*f*Lam//P*p;q+=2*d*Lam*p
    final,x1,k,w1=state();assert [x1,w1]==[x,w]
    E=w+d2*final;assert (E-z)%(2*B)==0
    if expected is not None:assert final==expected
    polygon=[(a,b),(a,h),(A-a,h),(A-a,c),(A-B,c),(A-B,0),(A,0),(A,H),(0,H),(0,b)]
    replay=rns['replay_actual'](polygon,(s,u),(target,v),final,2*d)
    return dict(label=label,parameters=[e,P,N,L,b,c,h,H],S=S,T=T,
        n=n,f=f,H0=hh,Fy=Fy,Y=Y,fiber_ratio=fiber_ratio,equality=equality,
        columns=columns,lift=lift,right_repair=repair,seed=seed,blocks=blocks,p=p,
        final_slope=final,final_indices=[m,j,k],E=E,**replay)
rows=[check('EA07-full-period-fiber',4,1,6,4,1,5,12,16,(2,14),(12,2)),
      check('EA07-nonfull-period-fiber',4,1,10,4,1,9,14,18,(2,16),(28,2)),
      check('REVIEWER-equality-single-column',4,1,6,4,1,3,8,12,(2,10),(10,2),True,Q(35,3))]
assert rows[0]['fiber_ratio']==7 and rows[1]['fiber_ratio']==Q(25,3)
assert sum(row['cap_safe'] for row in rows[2]['columns'])==1
assert rows[2]['columns'][0]['x']==0 and rows[2]['seed']['tau']==Q(11,3)
assert request_hash==hashlib.sha256(REQ.read_bytes()).hexdigest()
out=dict(status='PASS_EA07_AND_SEPARATE_EQUALITY_PRESCRIBED_RAYS',
    request_sha256=request_hash,source_pins_before=before,source_pins_after=pins(),
    rows=rows,cases=3,reflections=sum(r['reflections'] for r in rows),
    wall_leg_guards=sum(r['wall_leg_guards'] for r in rows),author_code_executed=False,
    discovery_search_used=False,equality_extension_separate_from_author_packet=True,
    whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['rows','source_pins_before','source_pins_after']}))
