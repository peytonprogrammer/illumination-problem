"""AP03 two prescribed physical cases: real floor and exact-S suffix only."""
from pathlib import Path
from fractions import Fraction as Q
from math import gcd,lcm,floor,ceil
import ast,json,hashlib
HERE=Path(__file__).parent
paths=[HERE/'three-reflex-two-source-period-proof.md',
 HERE/'three-reflex-parity-free-effective-period-independent.md',
 HERE/'three-reflex-parity-free-floor-independent.md']
def pins():return [{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths]
before=pins()
ns={'Q':Q,'F':Q}
tree=ast.parse((HERE/'resumed-exact-check.py').read_text())
names={'vec','det','dot','edges','on','location','intersect','simple','path_check','fold'}
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef)
    and n.name in names],type_ignores=[]),'<own-geometry>','exec'),ns)
source=(HERE/'three-reflex-coprime-independent-check.py').read_text()
node=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name=='replay_actual')
code=ast.get_source_segment(source,node)
code=code.replace('def replay_actual(P,S,T,slope,D):',
    'def replay_actual(P,S,T,slope,D,initial_vy=Q(1),horizontal_count=1):')
code=code.replace('velocity=(slope,Q(1))','velocity=(slope,initial_vy)')
code=code.replace('assert len(roofs)==len(horizontal)==1',
    'assert len(roofs)==1 and len(horizontal)==horizontal_count')
env={'Q':Q,'ns':ns};exec(compile(code,'<own-earliest-original-walls>','exec'),env)
def polygon(a,R,A,B,b,c,h,H):
    return [(a,b),(a,h),(A-R,h),(A-R,c),(A-B,c),(A-B,0),(A,0),(A,H),(0,H),(0,b)]

def bezout(a,b):
    if b==0:return abs(a),1 if a>0 else -1,0
    g,x,y=bezout(b,a%b)
    return g,y,x-a//b*y
def check(label,e,P,K,N,L,b,c,h,H,S,T,upper=False,expected=None,source_floor=False):
    e=Q(e);s,u=map(Q,S);target,v=map(Q,T)
    a=e*P;R=e*K;A=e*N;B=e*L;z=A-target;g1=h-c;d2=int(c-v)
    Craw=int(2*H-h-u) if upper else 2*(H-h)
    Araw=int(h+u-2*b) if source_floor else int(h-u)
    Lam=lcm(N//gcd(N,Craw),K//gcd(K,g1)) if upper else lcm(P//gcd(P,Araw),N//gcd(N,Craw),K//gcd(K,g1))
    g=gcd(Lam*d2,L)
    assert 0<K<L and N>P+L and 0<b<c<h<H and K%g==0
    assert 0<s<a and b<u<H and A-B<target<A and 0<v<c
    assert u.denominator==v.denominator==1
    F=int(h-v);C=int(2*H-h-u) if upper else 2*(H-h)
    d0=0 if upper else Araw;D=C+F if upper else d0+C+F
    assert C>0 and F==g1+d2>0 and D>0
    def raw(sign,i,m,j):
        q=P*i+N*m+g*j;tau=(A+z-sign*s+2*e*q)/D
        x0=sign*s+d0*tau-2*a*i
        x=sign*s+C*tau-(2*m+1)*A if upper else x0+C*tau-(2*m+1)*A
        r=x+g1*tau;k=floor((r+R)/(2*R));w=r-2*R*k
        return dict(sign=sign,i=i,m=m,j=j,q=q,tau=tau,x0=x0,x=x,r=r,k=k,w=w)
    choices=[]
    if not upper:
        assert d0>0 and g<=P and P*F+g*(d0+C)<=K*D
        for sign in (1,-1):
            la=-sign*s/(2*a)-Q(d0*N,2*P*C)
            mu=z/(2*e*g)-Q(F*N,2*g*C)
            i=-floor(la+Q(1,2));j=-floor(mu+Q(1,2))
            row=raw(sign,i,0,j)
            assert abs(row['x0'])<a and abs(row['x'])<R
            choices.append(row)
        di=choices[0]['i']-choices[1]['i']
        assert di in (0,1) and choices[0]['j']==choices[1]['j']
        diff=Q(2*d2,D)*(s-a*di)
        assert choices[0]['r']-choices[1]['r']==diff and 0<abs(diff)<2*R
        safe=[row for row in choices if abs(row['w'])<R]
        assert safe;chosen=safe[-1]
        branch='lower-paired-sources'
    else:
        assert u>=h and (g<K or P==K)
        hh,bm,bj=bezout(-N*F,C*g)
        assert -N*F*bm+C*g*bj==hh
        if 2*hh<K*D:
            V=F*(s-A)+C*z;ell=-floor(V/(2*e*hh)+Q(1,2))
            x=(V+2*e*hh*ell)/D
            adjacent=ell-1 if x>0 else ell+1
            for col in (ell,adjacent):
                row=raw(1,0,bm*col,bj*col);assert abs(row['x'])<R;choices.append(row)
            ratio=Q(g1*N*g,K*hh)
            safe=[row for row in choices if abs(row['w'])<R]
            if not safe:
                assert ratio.denominator>1
                row=choices[0];chosen=raw(1,0,row['m']+C*g//hh,row['j']+N*F//hh)
                assert abs(chosen['w'])<R
            else:chosen=safe[-1]
            branch='upper-two-columns'
        else:
            assert g==K==P and hh==C*P and C>=F
            for sign in (1,-1):
                offset=(F*(sign*s-A)+C*z)/D
                j=-floor(offset/(2*C*a/D)+Q(1,2))
                row=raw(sign,0,0,j);assert abs(row['x'])<R;choices.append(row)
            delta=choices[0]['j']-choices[1]['j'];assert delta in (0,-1)
            diff=(choices[0]['r']-choices[1]['r'])/a
            assert diff==Q(2*d2,D)*(s/a)+Q(2*(C+g1),D)*delta
            assert diff%2!=0
            safe=[row for row in choices if abs(row['w'])<R]
            if not safe:
                assert Q(g1*N*g,K*hh).denominator>1
                row=choices[0];chosen=raw(1,0,row['m']+C*g//hh,row['j']+N*F//hh)
            else:chosen=safe[-1]
            branch='upper-critical-paired-sources'
    # Independent alternative to the author's minimal kernel: g|K|Lambda
    # makes one complete period an integral ALL-guard positivity kernel.
    assert (F*Lam)%g==0 and (g1*Lam)%K==0 and (C*Lam)%N==0
    if not upper:assert (d0*Lam)%P==0
    sign=chosen['sign'];i=chosen['i'];m=chosen['m'];j=chosen['j'];q=chosen['q']
    inc_i=d0*Lam//P;inc_m=C*Lam//N;inc_j=F*Lam//g;inc_q=D*Lam
    assert P*inc_i+N*inc_m+g*inc_j==inc_q
    lift=max(0,ceil(Q(-m,inc_m)),ceil(Q(-q,inc_q)),ceil(Q(-i,inc_i)) if inc_i else 0)
    positive=raw(sign,i+lift*inc_i,m+lift*inc_m,j+lift*inc_j)
    assert [positive[k] for k in ['x0','x','w']]==[chosen[k] for k in ['x0','x','w']]
    assert min(positive['i'],positive['m'],positive['q'],positive['k'])>=0 and positive['tau']>0
    J=g*positive['j']-K*positive['k'];assert J%g==0
    mod=L//g;p=(-J//g*pow(Lam*d2//g,-1,mod))%mod if mod>1 else 0
    final=raw(sign,positive['i']+p*inc_i,positive['m']+p*inc_m,positive['j']+p*inc_j)
    assert [final[k] for k in ['x0','x','w']]==[chosen[k] for k in ['x0','x','w']]
    E=final['w']+d2*final['tau'];assert (E-z)%(2*B)==0
    if expected is not None:assert final['tau']==expected
    polygon=[(a,b),(a,h),(A-R,h),(A-R,c),(A-B,c),(A-B,0),(A,0),(A,H),(0,H),(0,b)]
    floor_phase=sign*s+(u-b)*final['tau']
    corner=source_floor and floor_phase%a==0
    horizon=D-2*(u-b) if corner else D
    signed_tau=-sign*final['tau'] if corner else sign*final['tau']
    vy=Q(-1) if source_floor and not corner else Q(1)
    replay=env['replay_actual'](polygon,(s,u),(target,v),signed_tau,horizon,initial_vy=vy,horizontal_count=2 if source_floor and not corner else 1)
    return dict(label=label,parameters=[e,P,K,N,L,b,c,h,H],S=S,T=T,upper=upper,
        g=g,M=Lam,source_floor=source_floor,floor_phase=floor_phase,discarded_corner_prefix=corner,times=[d0,C,F,D],branch=branch,choices=choices,selected_sign=sign,lift=lift,
        p=p,final=final,E=E,**replay)
rows=[check('AP06-u2-upward',2,4,5,13,8,1,3,6,7,(2,2),(18,2)),
 check('AP06-u4-real-floor',2,4,5,13,8,1,3,6,7,(2,4),(18,2),source_floor=True)]
assert all(r['g']==1 and r['M']%2 for r in rows)
assert all(r['times'][0]%4==0 for r in rows)
assert rows[1]['source_floor'] and not rows[1]['discarded_corner_prefix']
assert before==pins()
out=dict(status='PASS_AP06_TWO_PRESCRIBED_ACTUAL_SOURCE_CHARTS',source_pins_before=before,source_pins_after=pins(),
 rows=rows,cases=2,reflections=sum(x['reflections'] for x in rows),wall_leg_guards=sum(x['wall_leg_guards'] for x in rows),
 author_code_executed=False,discovery_search_used=False,independent_reciprocal_review_pending=True,
 whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['rows','source_pins_before','source_pins_after']}))
