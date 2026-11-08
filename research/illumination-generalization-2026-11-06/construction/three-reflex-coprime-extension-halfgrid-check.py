"""LC04 prescribed exact arithmetic only; no discovery or physical ray engine."""
from fractions import Fraction as F
from math import gcd,lcm
from pathlib import Path
import json

def fold(x,w):
 x=x%(2*w)
 return min(x,2*w-x)

def check(e,P,K,L,N,b,c,h,H,s,u,t,v,m,jstar,j,p,expected):
 e,s,t=map(F,(e,s,t));a=P*e;A=N*e;z=A-t
 assert 0<s<a and b<u<H and (N-L)*e<t<A and 0<v<c
 d0=max(h-u,0);C=2*(H-h) if u<=h else 2*H-h-u;g1=h-c;d2=c-v;D=2*H-u-v
 Lam=lcm(P,N,K);g=gcd(Lam*d2,L);ep=e*g/2
 assert P%g==0 and K==g and (2*z/(e*g)).denominator==1 and int(2*z/(e*g))%2==1
 r=(N*m)%g;rho=2*ep*(d0+C)/D;B=a+C*(A+z-s+2*e*(g-1))/D;U=(2*m+1)*A+K*e
 assert U>B+4*rho
 def at(index):
  q=r+F(g,2)*index;tau=(A+z-s+2*e*q)/D
  n=(s+d0*tau+a)//(2*a) if u<h else 0;z0=s+d0*tau-2*a*n if u<h else s
  X=z0+C*tau
  return q,tau,n,z0,X
 assert all(at(i)[4]<U for i in range(jstar)) and at(jstar)[4]>=U
 q,tau,n,z0,X=at(j);z1=X-(2*m+1)*A;k=(z1+g1*tau+K*e)//(2*K*e);z2=z1+g1*tau-2*K*e*k;E=z2+d2*tau;J=(E-z)/(2*e)
 assert abs(z0)<a and abs(z1)<K*e and abs(z2)<K*e
 assert (2*J/g).denominator==1
 sigma=1 if (J/g).denominator==1 else -1
 I=J if sigma==1 else J+z/e
 assert I.denominator==1 and I%g==0
 final=tau+2*e*Lam*p;Iend=I+Lam*d2*p;Eend=E+2*e*Lam*d2*p
 assert Iend%L==0 and A-fold(Eend,L*e)==t and final==expected
 # Literal signed residual preservation at the final original slope.
 nn=n+(Lam*d0*p//P if u<h else 0);mm=m+Lam*C*p//N;kk=k+Lam*g1*p//K
 assert s+d0*final-2*a*nn==z0
 assert z0+C*final-(2*mm+1)*A==z1
 assert z1+g1*final-2*K*e*kk==z2
 return dict(parameters=[str(e),P,K,L,N,b,c,h,H],source=[str(s),u],target=[str(t),v],g=g,m=m,r=r,jstar=jstar,j=j,q=str(q),initial_slope=str(tau),J=str(J),selected_target_sign=sigma,I=str(I),p=p,final_slope=str(final),final_target_index=str(Iend),final_E=str(Eend),residuals=list(map(str,[z0,z1,z2])),actual_target_x=str(A-fold(Eend,L*e)))

cases=[
 check(4,3,1,4,9,1,3,5,7,6,6,30,2,0,8,7,2,F(464,3)),
 check(4,3,1,4,9,1,3,5,7,6,4,30,2,1,43,42,2,F(339,2)),
 check(4,3,1,4,9,1,3,5,7,6,5,30,2,1,38,37,0,F(184,7)),
 check(2,2,2,4,7,1,3,6,9,2,4,8,2,1,17,15,0,F(41,6))]
out=dict(status='PASS_FOUR_PRESCRIBED_LC04_HALFGRID_CONTROLS',cases=cases,discovery_search=False,physical_ray_replay=False,independent_acceptance=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
