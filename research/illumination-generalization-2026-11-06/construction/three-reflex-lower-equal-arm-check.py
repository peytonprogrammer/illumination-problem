"""LJ03 two prescribed equal-arm half-open rounding controls, no search."""
from fractions import Fraction as F
from math import gcd,lcm
from pathlib import Path
import json

def check(label,e,P,N,L,b,c,h,H,s,u,t,v,expected,coefficients):
 A=N*e;a=P*e;R=a;B=L*e
 assert 1<=P<L and N>P+L and N%2 and h%2==0 and c%2 and 0<b<c<h<H
 assert 0<s<a and b<u<h and A-B<t<A and 0<v<c and u%2==v%2==0
 al=(h-u)//2;be=H-h;f=(h-v)//2;d=al+be+f;z=A-t;g1=h-c;d2=c-v
 vi=(F(-2*e*P*(be+f),d),F(-2*e*P*f,d));vj=(F(2*e*P*al,d),F(2*e*P*(al+be),d))
 tau0=F(A+z-s,2*d);r0=(s+2*al*tau0,s+2*(al+be)*tau0-A);det=vi[0]*vj[1]-vi[1]*vj[0]
 assert det==F(-4*e*e*P*P*be,d)
 la=(r0[0]*vj[1]-r0[1]*vj[0])/det;mu=(vi[0]*r0[1]-vi[1]*r0[0])/det
 assert (la,mu)==coefficients
 i=-int((la+F(1,2))//1);j=-int((mu+F(1,2))//1);m=0;q=P*i+N*m+P*j
 assert F(-1,2)<=la+i<F(1,2) and F(-1,2)<=mu+j<F(1,2)
 tau=F(A+z-s+2*e*q,2*d);z0=s+2*al*tau-2*a*i;z1=z0+2*be*tau-(2*m+1)*A
 assert abs(z0)<a and abs(z1)<R
 assert (abs(vi[0])+vj[0])/2==a and (abs(vi[1])+vj[1])/2==a
 hh=gcd(gcd(N*al,P*be),N*f);di,dm,dj=N*al//hh,P*be//hh,N*f//hh
 assert di>0 and dm>0 and dj>0 and P*di+N*dm+P*dj==P*N*d//hh
 step=F(e*P*N,hh)
 assert 2*al*step==2*a*di and 2*be*step==2*A*dm and F(g1*N,2*hh).denominator!=1
 # Both fixed rounded seeds are already positive and right-safe.
 assert min(i,m,q)>=0 and tau>0
 Y=z1+g1*tau;k=int((Y+R)//(2*R));z2=Y-2*R*k;assert abs(z2)<R
 J=P*(j-k);Lam=lcm(P,N);Gamma=gcd(Lam*d2,L);assert P%Gamma==0 and J%Gamma==0
 mod=L//Gamma;p=0 if mod==1 else (-J//Gamma*pow(Lam*d2//Gamma,-1,mod))%mod
 final=tau+2*e*Lam*p;fi=i+2*al*Lam*p//P;fm=m+2*be*Lam*p//N;fk=k+g1*Lam*p//P
 assert final==expected and s+2*al*final-2*a*fi==z0 and z0+2*be*final-(2*fm+1)*A==z1 and z1+g1*final-2*R*fk==z2
 E=z2+d2*final;phase=E%(2*B);assert A-min(phase,2*B-phase)==t and (J+Lam*d2*p)%L==0
 roof=z0+be*final;assert roof%A!=0
 return dict(label=label,e=e,P=P,N=N,L=L,S=[s,u],T=[t,v],beta=be,rounding=[str(la),str(mu)],coefficient_residuals=[str(la+i),str(mu+j)],slope=str(final),residuals=list(map(str,[z0,z1,z2])),Gamma=Gamma,J=J,p=p,indices=[fi,fm,fk],roof_phase=str(roof),actual_target=[t,v])

cases=[check('A_simultaneous_half_ties',4,1,9,4,1,3,8,26,2,6,34,2,F(9,11),(F(-1,2),F(-1,2))),check('B_even_equal_armfactor',2,2,9,4,1,3,6,12,2,4,14,2,F(14,9),(F(-5,8),F(-1,4)))]
out=dict(status='PASS_TWO_LJ03_PRESCRIBED_HALF_OPEN_EQUAL_ARM_CONTROLS',cases=cases,discovery_search=False,physical_ray_replay=False,independent_acceptance=False,whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
