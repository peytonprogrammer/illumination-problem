"""UP03 fixed exact proof control only; no discovery or ray engine."""
from fractions import Fraction as F
from math import gcd
from pathlib import Path
import json

def fold(x,w):
 x=x%(2*w)
 return min(x,2*w-x)

e=F(2);P=7;N=15;L=4;b=1;c=3;h=4;H=15;s=F(4);u=14;t=F(26);v=2
a=P*e;A=N*e;z=A-t;dp=u-h;dl=2*(h-b);C=2*(H-h);g1=h-c;d2=c-v;D=dp+dl+C+g1+d2
deltaN=N//gcd(N,dp//2);aP=P//gcd(P,h-b);a0=aP*deltaN
assert (deltaN,aP,a0)==(3,7,21) and P>=deltaN+4 and dp%(2*N)!=0
assert gcd((H-h)*a0,N)==deltaN

def data(tau):
 ip=(s+dp*tau+A)//(2*A);zp=s+dp*tau-2*A*ip
 il=(zp+dl*tau+a)//(2*a);z0=zp+dl*tau-2*a*il
 X=z0+C*tau;im=X//(2*A);z1=X-(2*im+1)*A
 ik=(z1+g1*tau+e)//(2*e);z2=z1+g1*tau-2*e*ik;E=z2+d2*tau
 return [int(ip),int(il),int(im),int(ik)],(zp,z0,z1,z2),E,X

def tau(q):return (A+z-s+2*e*q)/D
qstart=35;qend=62;npre=1;U=F(116);qcross=46;q=45;M=4;p=2
assert s+dp*tau(qstart-1)<=2*A*npre-a and s+dp*tau(qend+1)>=2*A*npre+a
assert all(abs(s+dp*tau(j)-2*A*npre)<a for j in range(qstart,qend+1))
Xs=data(tau(qstart))[3];Xe=data(tau(qend))[3];rho=2*e*(dp+dl+C)/D
assert (Xs,Xe,rho)==(F(211,2),F(1521,10),F(19,5))
assert Xe-Xs>2*a-4*e>=2*e*deltaN+4*e>2*e*deltaN+2*rho
assert U>Xs+2*rho and U<=Xe and (U-A-e)%(2*e*deltaN)==0
assert all(data(tau(j))[3]<U for j in range(qstart,qcross)) and data(tau(qcross))[3]>=U
assert data(tau(37))[3]<data(tau(36))[3] # Prescribed backwards source reset inside the block.
ix0,r0,E0,X0=data(tau(q));assert (r0[0],r0[1],X0)==(F(-7,2),F(0),F(231,2))
assert U-2*e<X0<U and abs(r0[0])<a and abs(r0[1])<a
seed=tau(q)+e*a0*M;ix,r,E,X=data(seed)
assert r[:2]==r0[:2] and r[2:]==(F(3,2),F(-5,4)) and seed==F(693,4)
J=(E-z)/(2*e);assert J==42 and J==q+D*a0*M//2-N*ix[0]-P*ix[1]-N*ix[2]-ix[3]
assert M<N//deltaN and gcd((H-h)*aP,N//deltaN)==1
final=seed+2*e*aP*N*p;ifix,fr,FE,FX=data(final)
assert final==F(4053,4) and ifix==[169,217,371,254] and fr==r
assert (FE-z)/(2*e)==252==J+aP*N*d2*p and 252%L==0
assert A-fold(FE,L*e)==t
floorx=fold(fr[0]+final*(h-b),a);assert floorx not in(0,a)
assert (fr[1]+final*(H-h))%A!=0
out=dict(status='PASS_UP03_FIXED_NONTRIVIAL_CAP_COSET_AND_BACKWARD_RESET',parameters=[str(e),P,1,L,N,b,c,h,H],source=[str(s),u],target=[str(t),v],deltaN=deltaN,aP=aP,a0=a0,initial_q_block=[qstart,qend],Xstart=str(Xs),Xend=str(Xe),rho=str(rho),cap_threshold=str(U),qcross=qcross,selected_q=q,M=M,p=p,seed_slope=str(seed),seed_J=str(J),final_slope=str(final),final_J=252,residuals=list(map(str,fr)),indices=ifix,floor_x=str(floorx),actual_target_x=str(A-fold(FE,L*e)),discovery_search=False,physical_ray_replay=False,independent_acceptance=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
