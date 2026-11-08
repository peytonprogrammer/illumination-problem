"""CE08 prescribed upper-window arithmetic checks only; no discovery and no ray engine.
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
    assert 2<=K<L and P<N-L and h<=u<H
    assert 0<b<c<h<H and 0<s<a and b<u<H and (N-L)*e<t<A and 0<v<c
    Lam=lcm(N,K);g=gcd(Lam*d2,L)
    assert K%g==0 and K*D>2*g*C
    tau0=(A+z-s+2*e*q)/D
    assert d0==0 or (s+d0*tau0-P*e)%(2*e)!=0
    assert M==0
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
    tau=tau0
    r0,J0,indices0,E0=residuals(tau)
    assert J0%g==0 and (q-N*indices0[1])%g==0
    tau1=tau+2*e*Lam
    r1,J1,_,_=residuals(tau1)
    assert r0==r1 and J1-J0==Lam*d2
    final=tau+2*e*Lam*p
    r2,J,indices,E=residuals(final)
    assert r0==r2 and J%L==0 and A-fold(E,L*e)==t
    assert (final,J)==expected
    return dict(target_gcd=g,initial_J=J0,cap_window_length=str(F(K*D,C)),parameters=[str(e),P,K,L,N,b,c,h,H],source=[str(s),u],target=[str(t),v],q=q,M=M,p=p,slope=str(final),J=J,residuals=list(map(str,r2)),indices=indices,actual_target_x=str(A-fold(E,L*e)))

cases=[
 check(4,1,3,4,9,1,3,6,10,2,8,28,2,1,0,3,(F(221),28)),
 check(4,1,3,4,9,2,3,4,10,2,4,28,2,0,0,0,(F(3),0)),
 check(4,1,6,8,11,2,3,4,10,2,4,28,2,2,0,2,(F(7429,7),128)),
 check(1,1,2,3,8,1,3,5,7,F(1,2),6,F(39,5),1,41,0,2,(F(3137,70),45))]
# Prescribed alternative42 stays strictly inside SAME cap branch m2
# but reaches the actual inner right endpoint, unlike retained41.
bad_tau=F(131,10);bad_X=F(1,2)+3*bad_tau;bad_z1=bad_X-40
assert 38<bad_X<42 and bad_z1+2*bad_tau==26
assert (bad_z1+2*bad_tau-2)%4==0
# Another fixed alternative has strict physical portals but the wrong J class.
miss_tau=F(33,7);miss_z1=F(2)+12*miss_tau-44
miss_z2=miss_z1+miss_tau;miss_J=(miss_z2+miss_tau-16)/8
assert abs(miss_z1)<24 and abs(miss_z2)<24 and miss_J==1
assert all((1+66*p)%8!=0 for p in range(4))
out=dict(status='PASS_FOUR_PRESCRIBED_CE08_CHOICE_CONTROLS',cases=cases,true_corner_alternative_q42=True,strict_portal_wrong_target_class_q1=True,discovery_search=False,physical_ray_replay=False,independent_acceptance=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
