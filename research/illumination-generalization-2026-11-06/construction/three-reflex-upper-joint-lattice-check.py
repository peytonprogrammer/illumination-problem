"""UJ01 four prescribed joint-lattice formula checks; no ray/discovery engine."""
from fractions import Fraction as F
from math import gcd,lcm
from pathlib import Path
import json

def center(x,w):
 k=(x+w)//(2*w)
 return x-2*w*k,int(k)

def fold(x,w):
 x=x%(2*w)
 return min(x,2*w-x)

def egcd(a,b):
 if b==0:return a,1,0
 g,x,y=egcd(b,a%b)
 return g,y,x-(a//b)*y

def ceildiv(a,b):return -((-a)//b)

def check(name,e,P,K,L,N,b,c,h,H,s,u,t,v,j,m,expected):
 A=N*e;R=K*e;z=A-t;n=(2*H-h-u)//2;d=(2*H-u-v)//2;f=d-n;g1=h-c;d2=c-v
 Lam=lcm(N,K);g=gcd(Lam*d2,L);H0=gcd(n*g,N*f);V=f*(s-A)+n*z
 assert g and K%g==0 and H0<=n*g and n<d and N%2==g1%2==1
 q=N*m+g*j;tau=F(A+z-s+2*e*q,2*d)
 z1=F(V+2*e*(n*g*j-N*f*m),d)
 assert abs(z1)<R and tau>0 and m>=0 and q>=0
 assert s+2*n*tau==(2*m+1)*A+z1
 z2,k=center(z1+g1*tau,R);assert abs(z2)<R
 J=q-N*m-K*k;assert J==g*j-K*k and J%g==0
 modulus=L//g;p=0 if modulus==1 else (-J//g*pow(Lam*d2//g,-1,modulus))%modulus
 final=tau+2*e*Lam*p;fm=m+2*n*Lam*p//N;fk=k+g1*Lam*p//K
 assert final==expected and s+2*n*final==(2*fm+1)*A+z1
 assert z1+g1*final==2*R*fk+z2
 E=z2+d2*final;fJ=J+Lam*d2*p
 assert fJ%L==0 and E==z+2*e*fJ and A-fold(E,L*e)==t
 # Prescribed proof algorithm, with no finite search over possible rays.
 ell=int((-F(V,2*e*H0)+F(1,2))//1)
 hh,x,y=egcd(n*g,N*f);assert hh==H0
 aj=x*ell;am=-y*ell;aq=N*am+g*aj
 dm=n*g//H0;dj=N*f//H0;dq=N*dm+g*dj
 shift=max(0,ceildiv(-am,dm),ceildiv(-aq,dq))
 am+=dm*shift;aj+=dj*shift;aq+=dq*shift
 at=F(A+z-s+2*e*aq,2*d);az1=s+2*n*at-(2*am+1)*A
 assert abs(az1)<=F(e*H0,d)<e*g<=R
 az2,ak=center(az1+g1*at,R);repair=abs(az2)==R
 if repair:
  am+=dm;aj+=dj;aq+=dq;at+=F(e*N*g,H0)
  az2,ak=center(az1+g1*at,R)
 assert abs(az2)<R and am>=0 and aq>=0 and at>0
 assert F(g1*N,2*(K//g)*H0).denominator!=1
 aJ=aq-N*am-K*ak;assert aJ%g==0
 ap=0 if modulus==1 else (-aJ//g*pow(Lam*d2//g,-1,modulus))%modulus
 afinal=at+2*e*Lam*ap
 assert A-fold(az2+d2*afinal,L*e)==t
 roof=s+(H-u)*final
 assert roof%A!=0 # These four prescribed controls all have ordinary roofs.
 return dict(name=name,widths=dict(P=P,K=K,L=L,N=N),n=n,d=d,g=g,H0=H0,j=j,m=m,q=q,seed_slope=str(tau),z1=str(z1),z2=str(z2),J=J,p=p,final_slope=str(final),final_indices=[fm,fk],actual_target=[t,v],algorithm=dict(ell=ell,positive_shift=shift,q=aq,m=am,j=aj,right_repair=repair,final_slope=str(afinal)))

cases=[check('power_two_K2',2,1,2,4,7,2,3,4,12,2,10,10,2,4,6,F(18)),check('power_two_K4',2,1,4,8,11,2,3,4,12,2,10,10,2,5,10,F(46)),check('actual_mouth_equality',2,1,2,4,7,2,3,4,12,2,4,10,2,1,3,F(6)),check('non_power_two_bottom_target_divisor3',2,1,3,6,9,1,3,4,9,2,6,10,2,2,3,F(258,5))]
out=dict(status='PASS_FOUR_UJ01_PRESCRIBED_FORMULA_AND_BEZOUT_SELECTION_CHECKS',cases=cases,discovery_search=False,physical_ray_replay=False,independent_acceptance=False,whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
