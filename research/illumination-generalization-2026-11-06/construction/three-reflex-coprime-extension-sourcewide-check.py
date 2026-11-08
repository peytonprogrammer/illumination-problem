"""CE04 prescribed algebra checks only; no discovery and no ray engine.
Physical path guards are established by the hand proof and peer replay.
"""
from fractions import Fraction as F
from math import gcd, lcm
from pathlib import Path
import json

def fold(x,w):
    x=x%(2*w)
    return min(x,2*w-x)

def check(e,P,K,L,N,b,c,h,H,s,u,t,v,q,M,p,expected):
    e,s,t=map(F,(e,s,t)); a=P*e; A=N*e
    d0=max(h-u,0); C=2*(H-h) if u<=h else 2*H-h-u
    g1=h-c;d2=c-v;D=2*H-u-v;z=A-t
    assert 2<=K<L and P<N-L
    assert 0<b<c<h<H and 0<s<a and b<u<H and (N-L)*e<t<A and 0<v<c
    delta=gcd(P*C,N); Lam=lcm(P,N,K)
    assert delta<K and gcd(Lam*d2,L)==1
    tau0=(A+z-s+2*e*q)/D
    assert d0==0 or (s+d0*tau0-P*e)%(2*e)!=0
    assert (s+(D-d2)*tau0-A-K*e)%(2*e)!=0
    def residuals(tau):
        n=(s+d0*tau+a)//(2*a) if u<=h else 0
        z0=s+d0*tau-2*a*n if u<=h else s
        X=z0+C*tau
        m=X//(2*A)
        z1=X-(2*m+1)*A
        assert abs(z0)<a and abs(z1)<K*e
        k=(z1+g1*tau+K*e)//(2*K*e)
        z2=z1+g1*tau-2*K*e*k
        assert abs(z2)<K*e
        E=z2+d2*tau
        J=(E-z)/(2*e)
        assert J.denominator==1
        return (z0,z1,z2),int(J),[int(n),int(m),int(k)],E
    tau=tau0+2*P*e*M
    r0,J0,indices0,E0=residuals(tau)
    tau1=tau+2*e*Lam
    r1,J1,_,_=residuals(tau1)
    assert r0==r1 and J1-J0==Lam*d2
    final=tau+2*e*Lam*p
    r2,J,indices,E=residuals(final)
    assert r0==r2 and J%L==0 and A-fold(E,L*e)==t
    assert (final,J)==expected
    return dict(parameters=[str(e),P,K,L,N,b,c,h,H],source=[str(s),u],target=[str(t),v],q=q,M=M,p=p,slope=str(final),J=J,residuals=list(map(str,r2)),indices=indices,actual_target_x=str(A-fold(E,L*e)))

cases=[
 check(2,3,3,4,11,1,3,5,7,2,4,18,2,0,1,0,(F(15),4)),
 check(1,2,2,3,7,1,4,5,6,1,4,5,2,0,6,2,(F(244,3),81))]
out=dict(status='PASS_TWO_PRESCRIBED_CE04_ALGEBRA_CONTROLS',cases=cases,discovery_search=False,physical_ray_replay=False,independent_acceptance=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
