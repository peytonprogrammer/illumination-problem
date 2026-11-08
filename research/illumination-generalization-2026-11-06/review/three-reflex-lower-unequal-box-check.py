"""UB01 three prescribed exact formula and actual-wall checks; no search."""
from pathlib import Path
from fractions import Fraction as Q
from math import floor,ceil,gcd,lcm
import ast,json,hashlib
HERE=Path(__file__).parent
ns={'Q':Q,'F':Q};txt=(HERE/'resumed-exact-check.py').read_text()
names={'vec','det','dot','edges','on','location','intersect','simple','path_check','fold'}
exec(compile(ast.Module(body=[n for n in ast.parse(txt).body if isinstance(n,ast.FunctionDef)
    and n.name in names],type_ignores=[]),'<own-pure-geometry>','exec'),ns)
txt=(HERE/'three-reflex-coprime-independent-check.py').read_text()
fn=next(n for n in ast.parse(txt).body if isinstance(n,ast.FunctionDef) and n.name=='replay_actual')
rns={'Q':Q,'ns':ns};exec(compile(ast.get_source_segment(txt,fn),'<own-earliest-wall>','exec'),rns)

def val2(n):
    out=0
    while n%2==0:out+=1;n//=2
    return out

def check(label,e,P,K,L,N,b,c,h,H,S,T,expected=None):
    e=Q(e);s,u=map(Q,S);t,v=map(Q,T);a=P*e;R=K*e;A=N*e;B=L*e;z=A-t
    assert 1<=P<=K<L and N>P+L and N%2 and not L&(L-1)
    assert h%2==0 and c%2 and 0<b<c<h<H
    assert 0<s<a and b<u<h and A-B<t<A and 0<v<c
    assert u.denominator==v.denominator==1 and int(u)%2==int(v)%2==0
    al=Q(h-u,2);be=H-h;f=Q(h-v,2);d=al+be+f
    assert al.denominator==f.denominator==1 and al>0 and f>0
    al,f,d=int(al),int(f),int(d)
    Lam=lcm(P,N,K);g=gcd(Lam*int(c-v),L)
    assert g<=P and K%g==0 and g==2**val2(K) and val2(P)<=val2(K)
    la=-s/(2*e*P)-Q(al*N,2*P*be)
    mu=z/(2*e*g)-Q(f*N,2*g*be)
    i=-floor(la+Q(1,2));j=-floor(mu+Q(1,2));m=0
    errs=(la+i,mu+j)
    assert all(-Q(1,2)<=x<Q(1,2) for x in errs)
    q=P*i+N*m+g*j
    raw=(i,m,j,q)
    Bx=e*Q(P*(be+f)+g*al,d);By=e*Q(P*f+g*(al+be),d)
    assert Bx<=a and By<=a<=R
    hh=gcd(gcd(N*g*al,P*g*be),P*N*f)
    di,dm,dj=N*g*al//hh,P*g*be//hh,P*N*f//hh
    dq=P*di+N*dm+g*dj
    assert dq==P*N*g*d//hh and min(di,dm,dj,dq)>0
    assert val2(hh)>=val2(P)
    shift=max(0,ceil(Q(-i,di)),ceil(Q(-m,dm)),ceil(Q(-q,dq)))
    i+=di*shift;m+=dm*shift;j+=dj*shift;q+=dq*shift
    def state():
        tau=(A+z-s+2*e*q)/(2*d)
        x=s+2*al*tau-2*a*i;y=x+2*be*tau-(2*m+1)*A
        assert abs(x)<Bx<=a and abs(y)<By<=R and tau>0 and min(i,m,q)>=0
        assert floor((s+2*al*tau+a)/(2*a))==i
        assert floor((x+2*be*tau)/(2*A))==m
        k=floor((y+(h-c)*tau+R)/(2*R));w=y+(h-c)*tau-2*R*k
        return tau,x,y,k,w
    tau,x,y,k,w=state();repair=abs(w)==R
    step=e*P*N*g/hh;ratio=(h-c)*step/(2*R)
    assert ratio.denominator>1
    if repair:i+=di;m+=dm;j+=dj;q+=dq;tau,x,y,k,w=state()
    assert abs(w)<R
    J=g*j-K*k;assert J%g==0 and w+(c-v)*tau==z+2*e*J
    mod=L//g;p=0 if mod==1 else (-J//g*pow(Lam*int(c-v)//g,-1,mod))%mod
    final=tau+2*e*Lam*p
    fi=i+2*al*Lam*p//P;fm=m+2*be*Lam*p//N;fk=k+(h-c)*Lam*p//K
    assert s+2*al*final-2*a*fi==x
    assert x+2*be*final-(2*fm+1)*A==y
    assert y+(h-c)*final-2*R*fk==w
    assert ns['fold'](w+(c-v)*final,B)==z and (J+Lam*int(c-v)*p)%L==0
    roof=x+be*final;assert (roof/A).denominator>1
    if expected is not None:assert final==expected
    polygon=[(a,b),(a,h),(A-R,h),(A-R,c),(A-B,c),(A-B,0),(A,0),(A,H),(0,H),(0,b)]
    result=rns['replay_actual'](polygon,(s,u),(t,v),final,2*d)
    return dict(label=label,parameters=[e,P,K,L,N,b,c,h,H],S=S,T=T,
       coefficients=[la,mu],errors=errs,raw_indices=raw,positive_steps=shift,
       right_repair=repair,g=g,H0=hh,return_ratio=ratio,
       J=J,p=p,final_slope=final,indices=[fi,fm,fk],residuals=[x,y,w],
       bound_x=Bx,bound_y=By,roof_phase=roof,**result)

fixtures=[
 ('strict-unequal-P3-K6',2,3,6,8,13,1,3,6,12,(2,4),(14,2),Q(8,3)),
 ('positive-null-index-restoration',2,3,6,8,13,1,3,6,24,(2,4),(12,2),None),
 ('even-P2-K6-nonzero-target-correction',2,2,6,8,11,1,3,6,12,(2,4),(10,2),Q(2392,9))]
rows=[check(*x) for x in fixtures]
assert rows[1]['raw_indices']==(0,0,-1,-2) and rows[1]['positive_steps']>0
assert rows[2]['p']==1
source_paths=[HERE/('three-reflex-lower-unequal-box-'+s) for s in ['candidate.md','proof.md']]
out=dict(status='PASS_UB01_THREE_PRESCRIBED_UNEQUAL_ARM_ACTUAL_RAYS',
 source_pins=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in source_paths],
 rows=rows,cases=len(rows),reflections=sum(r['reflections'] for r in rows),
 wall_leg_guards=sum(r['wall_leg_guards'] for r in rows),author_code_executed=False,
 discovery_search_used=False,independent_acceptance=False,whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['rows','source_pins']}))
