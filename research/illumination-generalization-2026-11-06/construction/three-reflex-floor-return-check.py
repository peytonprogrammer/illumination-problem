"""FR01 fixed arithmetic controls; no discovery or ray engine."""
from fractions import Fraction as F
from math import gcd
from pathlib import Path
import json

def fold(x,w):
 x=x%(2*w)
 return min(x,2*w-x)

def check(e,P,L,N,b,c,h,H,s,u,t,v,q,M,p,expected,failed_M=None):
 e,s,t=map(F,(e,s,t));a=P*e;A=N*e;z=A-t;d=h+u-2*b;C=2*(H-h);g1=h-c;d2=c-v;D=d+C+g1+d2
 assert d==2*P and C==2 and D%2==0 and N%2==1 and h%2==0 and c%2==1 and L&(L-1)==0
 assert b<u<=h and 0<s<a and (N-L)*e<t<A and 0<v<c
 tau0=(A+z-s+2*e*q)/D
 assert (s+d*tau0-a)%(2*a)!=0
 assert (s+(d+C)*tau0-(N+1)*e)%(2*e)!=0
 def data(tau):
  n=(s+d*tau+a)//(2*a);z0=s+d*tau-2*a*n;X=z0+C*tau;m=X//(2*A);z1=X-(2*m+1)*A
  k=(z1+g1*tau+e)//(2*e);z2=z1+g1*tau-2*e*k;E=z2+d2*tau
  return n,m,k,z0,z1,z2,E
 if failed_M is not None:
  n,m,k,z0,z1,z2,E=data(tau0+e*failed_M)
  assert abs(z0)<a and abs(z1)<e and abs(z2)==e
  assert M==failed_M+N
 tau=tau0+e*M;n,m,k,z0,z1,z2,E=data(tau);J=(E-z)/(2*e)
 assert abs(z0)<a and abs(z1)<e and abs(z2)<e and J.denominator==1
 assert gcd(N*d2,L)==1
 final=tau+2*e*N*p;nn,mm,kk,zz0,zz1,zz2,EE=data(final)
 assert (zz0,zz1,zz2)==(z0,z1,z2) and (EE-z)/(2*e)==J+N*d2*p
 assert (J+N*d2*p)%L==0 and A-fold(EE,L*e)==t and final==expected
 floorphase=s+final*(u-b);floorx=fold(floorphase,a);suffix_used=floorx in(0,a)
 if suffix_used:assert fold(s+2*final*(u-b),a)==s
 roofphase=z0+final*(H-h)
 assert roofphase%A!=0
 return dict(parameters=[str(e),P,1,L,N,b,c,h,H],source=[str(s),u],target=[str(t),v],q=q,M=M,p=p,failed_M=failed_M,initial_slope=str(tau0),seed_J=str(J),final_slope=str(final),residuals=list(map(str,[z0,z1,z2])),floor_x=str(floorx),floor_corner_suffix_used=suffix_used,actual_target_x=str(A-fold(EE,L*e)))

cases=[
 check(4,3,4,9,1,3,4,5,8,4,28,2,0,3,3,F(1158,5)),
 check(4,3,4,9,1,3,6,7,8,2,28,2,1,3,3,F(695,3)),
 check(2,2,4,7,1,3,4,5,2,2,10,2,0,9,0,F(20),failed_M=2)]
# Exactly the formal floor-corner suffix prescribed in proof section6.D.
e=F(4);a=12;A=36;R=4;B=16;s=8;u=4;b=1;h=4;H=5;c=3;v=2;t=F(88,3);tau=F(172,3);d=6;C=2;g1=d2=1;f=3
assert s+tau*f==180 and fold(s+tau*f,a)==a
assert fold(s+2*tau*f,a)==s and 2*f==d
n=(s+d*tau+a)//(2*a);z0=s+d*tau-2*a*n;X=z0+C*tau;m=X//(2*A);z1=X-(2*m+1)*A
k=(z1+g1*tau+R)//(2*R);z2=z1+g1*tau-2*R*k;E=z2+d2*tau
assert (z0,z1,z2)==(F(-8),F(-4,3),F(0)) and abs(z0)<a and abs(z1)<R and abs(z2)<R
assert A-fold(E,B)==t and (z0+tau*(H-h))%A!=0
suffix=dict(status='FORMAL_PREFIX_INVALID_RETAIN_EXACT_S_SUFFIX',slope=str(tau),formal_corner_time=3,formal_corner_x=12,return_S_time=6,remaining_duration=4,residuals=list(map(str,[z0,z1,z2])),actual_target_x=str(t))
out=dict(status='PASS_THREE_FR01_NATIVE_CONTROLS_AND_GENERAL_FLOOR_CORNER_SUFFIX',cases=cases,suffix_control=suffix,discovery_search=False,physical_ray_replay=False,independent_acceptance=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
