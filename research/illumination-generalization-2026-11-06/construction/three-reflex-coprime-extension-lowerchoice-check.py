"""LC02 prescribed algebra checks only; no discovery and no ray engine.
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
    Lam=lcm(P,N,K); g=gcd(Lam*d2,L)
    assert P%K==0 and K%g==0 and K>=3*g
    assert M==0
    tau0=(A+z-s+2*e*q)/D
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
    assert J0%g==0
    tau1=tau+2*e*Lam
    r1,J1,_,_=residuals(tau1)
    assert r0==r1 and J1-J0==Lam*d2
    final=tau+2*e*Lam*p
    r2,J,indices,E=residuals(final)
    assert r0==r2 and J%L==0 and A-fold(E,L*e)==t
    assert (final,J)==expected
    return dict(parameters=[str(e),P,K,L,N,b,c,h,H],source=[str(s),u],target=[str(t),v],q=q,M=M,p=p,target_gcd=g,initial_J=J0,slope=str(final),J=J,residuals=list(map(str,r2)),indices=indices,actual_target_x=str(A-fold(E,L*e)))

cases=[
 check(2,6,6,8,17,1,3,6,23,4,4,26,2,19,0,2,(F(16377,20),200)),
 check(2,3,3,4,9,1,3,6,9,2,4,14,2,6,0,0,(F(11,3),0)),
 check(2,3,3,4,9,1,3,6,9,2,6,14,2,3,0,0,(F(16,5),0)),
 check(2,3,3,4,9,1,3,6,9,2,8,14,2,3,0,0,(F(4),0))]

# Only the finite runs already specified in the hand proof; no search.
capruns=[]
for e,P,K,N,s,z,d0,C,D,m,qstar in [
 (2,6,6,17,4,8,2,34,40,1,22),
 (2,3,3,9,2,4,2,6,12,0,8)]:
    A=N*e; a=P*e; U=(2*m+1)*A+K*e
    def X(q):
        tau=F(A+z-s+2*e*q,D)
        n=(s+d0*tau+a)//(2*a)
        return s+d0*tau-2*a*n+C*tau
    assert all(X(q)<U for q in range(qstar)) and X(qstar)>=U
    assert all(U-2*K*e<X(q)<U for q in range(qstar-K,qstar))
    capruns.append(dict(qstar=qstar,m=m,q_run=list(range(qstar-K,qstar)),X=list(map(lambda q:str(X(q)),range(qstar-K,qstar)))))
# A's q18 is strictly physical at the interfaces but in the wrong target orbit.
e=2; q=18; tau=F(34+8-4+4*q,40); n=(4+2*tau+12)//24
z0=4+2*tau-24*n; z1=z0+34*tau-102
k=(z1+3*tau+12)//24; z2=z1+3*tau-24*k
J=(z2+tau-8)/4
assert abs(z0)<12 and abs(z1)<12 and abs(z2)<12 and J==1
assert gcd(102,8)==2 and J%2!=0
out=dict(status='PASS_FOUR_PRESCRIBED_LC02_ALGEBRA_CONTROLS',cases=cases,capruns=capruns,wrong_target_orbit=dict(q=18,J=str(J),target_gcd=2),discovery_search=False,physical_ray_replay=False,independent_acceptance=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
