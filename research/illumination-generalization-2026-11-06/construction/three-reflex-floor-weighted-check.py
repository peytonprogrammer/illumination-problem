"""FR02 prescribed arithmetic controls; no discovery or ray engine."""
from fractions import Fraction as F
from math import gcd
from pathlib import Path
import json

def fold(x,w):
 x=x%(2*w)
 return min(x,2*w-x)

def check(e,P,L,N,b,c,h,H,s,u,t,v,q,M,p,expected,failed_M=None):
 e,s,t=map(F,(e,s,t));a=P*e;A=N*e;z=A-t;d=h+u-2*b;C=2*(H-h);g1=h-c;d2=c-v;D=d+C+g1+d2
 a0=P//gcd(P,d//2)
 assert d%2==0 and D%2==0 and a0%2==1 and gcd((H-h)*a0,N)==1
 assert N%2==1 and h%2==0 and c%2==1 and L&(L-1)==0
 assert b<u<=h and 0<s<a and (N-L)*e<t<A and 0<v<c
 tau0=(A+z-s+2*e*q)/D
 assert (s+d*tau0-a)%(2*a)!=0
 assert (s+(d+C)*tau0-(N+1)*e)%(2*e)!=0
 def data(tau):
  n=(s+d*tau+a)//(2*a);z0=s+d*tau-2*a*n;X=z0+C*tau;m=X//(2*A);z1=X-(2*m+1)*A
  k=(z1+g1*tau+e)//(2*e);z2=z1+g1*tau-2*e*k;E=z2+d2*tau
  return n,m,k,z0,z1,z2,E
 if failed_M is not None:
  n,m,k,z0,z1,z2,E=data(tau0+e*a0*failed_M)
  assert abs(z0)<a and abs(z1)<e and abs(z2)==e
  assert M==failed_M+N
 tau=tau0+e*a0*M;n,m,k,z0,z1,z2,E=data(tau);J=(E-z)/(2*e)
 assert abs(z0)<a and abs(z1)<e and abs(z2)<e and J.denominator==1
 assert gcd(a0*N*d2,L)==1
 final=tau+2*e*a0*N*p;nn,mm,kk,zz0,zz1,zz2,EE=data(final)
 assert (zz0,zz1,zz2)==(z0,z1,z2) and (EE-z)/(2*e)==J+a0*N*d2*p
 assert (J+a0*N*d2*p)%L==0 and A-fold(EE,L*e)==t and final==expected
 floorphase=s+final*(u-b);floorx=fold(floorphase,a);suffix_used=floorx in(0,a)
 if suffix_used:assert fold(s+2*final*(u-b),a)==s
 roofphase=z0+final*(H-h)
 assert roofphase%A!=0
 return dict(parameters=[str(e),P,1,L,N,b,c,h,H],source=[str(s),u],target=[str(t),v],a0=a0,q=q,M=M,p=p,failed_M=failed_M,initial_slope=str(tau0),seed_J=str(J),final_slope=str(final),residuals=list(map(str,[z0,z1,z2])),floor_x=str(floorx),floor_corner_suffix_used=suffix_used,actual_target_x=str(A-fold(EE,L*e)))

cases=[
 check(4,3,4,11,1,3,6,8,8,4,36,2,0,6,0,F(299,4)),
 check(2,2,4,7,1,3,4,5,2,2,10,2,0,9,0,F(20),failed_M=2)]
out=dict(status='PASS_FR02_WEIGHTED_LOWER_SOURCE_AND_EXISTING_FLIP_CONTROL',cases=cases,discovery_search=False,physical_ray_replay=False,independent_acceptance=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
