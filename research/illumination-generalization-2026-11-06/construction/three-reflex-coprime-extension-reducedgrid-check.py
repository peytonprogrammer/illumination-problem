"""LC03 prescribed algebra checks only; no discovery and no ray engine.
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
    assert P%g==0 and K%g==0 and K>=2*g
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
 check(2,10,6,8,23,1,3,6,23,4,4,34,2,27,0,1,(F(55281,20),688)),
 check(2,2,4,10,17,1,5,6,7,2,2,22,4,28,0,0,(F(39,2),0)),
 check(2,2,4,14,19,1,7,8,9,2,6,18,2,42,0,3,(F(4672,5),1162))]

# Prescribed finite first crossings, not parameter or ray discovery.
checks=[]
for P,K,L,N,b,c,h,H,s,u,t,v,m,jstar,selected in [
 (10,6,8,23,1,3,6,23,4,4,34,2,1,14,13),
 (2,4,10,17,1,5,6,7,2,2,22,4,0,16,14),
 (2,4,14,19,1,7,8,9,2,6,18,2,0,22,21)]:
 e=2;a=P*e;A=N*e;z=A-t;d0=h-u;C=2*(H-h);g1=h-c;d2=c-v;D=2*H-u-v
 Lam=lcm(P,N,K);g=gcd(Lam*d2,L); ep=e*g;r=(N*m)%g
 rho=F(2*ep*(d0+C),D);B=a+C*F(A+z-s+2*e*(g-1),D);U=(2*m+1)*A+K*e
 assert U>B+4*rho and P%g==K%g==0
 def data(j):
  q=r+g*j;tau=F(A+z-s+2*e*q,D);n=(s+d0*tau+a)//(2*a);z0=s+d0*tau-2*a*n
  X=z0+C*tau;R=s+(D-d2)*tau-(2*m+1)*A-K*e
  return X,z0,R%(2*ep)
 assert all(data(j)[0]<U for j in range(jstar)) and data(jstar)[0]>=U
 X,z0,R=data(selected)
 assert U-2*K*e<X<U and abs(z0)<a and R!=0
 pS=(P//g)*D//gcd(d0,(P//g)*D);pR=D//gcd(D-d2,D)
 if pS==2:
  assert abs(data(jstar)[1])<a
  assert all(abs(data(j)[1])<a and U-2*K*e<data(j)[0]<U for j in (jstar-2,jstar-4))
 if pR==2: assert rho<ep
 checks.append(dict(m=m,r=r,g=g,jstar=jstar,selected_j=selected,source_period=pS,right_strong_period=pR,B=str(B),U=U,selected_X=str(X)))
out=dict(status='PASS_THREE_PRESCRIBED_LC03_CONTROLS',cases=cases,first_crossings=checks,discovery_search=False,physical_ray_replay=False,independent_acceptance=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
