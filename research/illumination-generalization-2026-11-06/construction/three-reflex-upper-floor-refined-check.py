"""UP02 prescribed proof controls only: exact arithmetic, no ray discovery/engine."""
from fractions import Fraction as F
from math import gcd
from pathlib import Path
import json

def fold(x,w):
 x=x%(2*w)
 return min(x,2*w-x)

def check(e,P,L,N,b,c,h,H,s,u,t,v,npre,qstar,q,M,p,expected,expected_indices):
 e,s,t=map(F,(e,s,t));a=P*e;A=N*e;z=A-t;dp=u-h;dl=2*(h-b);C=2*(H-h);g1=h-c;d2=c-v;D=dp+dl+C+g1+d2;a0=P//gcd(P,h-b)
 assert P>=1 and P%2==1 and N%2==1 and N>P+L and gcd(P*(H-h),N)==1
 assert h%2==0 and c%2==1 and dp>0 and dp%(2*N)==0 and u<H and 0<s<a
 assert (N-L)*e<t<A and 0<v<c and D%2==0 and a0%2==1
 U=2*A*npre+a;delta=2*e*dp/D
 def pre(i):return s+dp*(A+z-s+2*e*i)/D
 assert U>pre(0)+4*delta
 assert all(pre(i)<U for i in range(qstar)) and pre(qstar)>=U
 ps=P*D//gcd(dp+dl,P*D);pc=D//gcd(dp+dl+C,D)
 count=4 if ps==2 or pc==2 else 3
 assert C>2*dp and delta<2*e/3
 if ps==2: assert P==1 and dp+dl==D//2 and delta<e/2
 if pc==2: assert dp+dl+C==D//2 and delta<e/3
 assert all(abs(pre(i)-2*A*npre)<a for i in range(qstar-count,qstar))
 assert q in range(qstar-count,qstar)
 tau0=(A+z-s+2*e*q)/D
 def data(tau):
  ip=(s+dp*tau+A)//(2*A);zp=s+dp*tau-2*A*ip
  il=(zp+dl*tau+a)//(2*a);z0=zp+dl*tau-2*a*il
  X=z0+C*tau;im=X//(2*A);z1=X-(2*im+1)*A
  ik=(z1+g1*tau+e)//(2*e);z2=z1+g1*tau-2*e*ik;E=z2+d2*tau
  return [int(ip),int(il),int(im),int(ik)],(zp,z0,z1,z2),E,X
 ix0,r0,E0,X0=data(tau0)
 assert ix0[0]==npre and abs(r0[0])<a and abs(r0[1])<a
 assert (s+(dp+dl+C)*tau0-(N+1)*e)%(2*e)!=0
 tau=tau0+e*a0*M;ix,r,E,X=data(tau)
 assert r[:2]==r0[:2] and abs(r[2])<e and abs(r[3])<e
 J=(E-z)/(2*e);assert J.denominator==1
 assert J==q+D*a0*M//2-N*ix[0]-P*ix[1]-N*ix[2]-ix[3]
 final=tau+2*e*a0*N*p;ifix,fr,FE,FX=data(final)
 assert fr==r and ifix==expected_indices
 assert (FE-z)/(2*e)==J+a0*N*d2*p and (J+a0*N*d2*p)%L==0
 assert A-fold(FE,L*e)==t and final==expected
 floor_phase=fr[0]+final*(h-b);floorx=fold(floor_phase,a)
 suffix=floorx in(0,a)
 if suffix:
  assert fr[1]==-fr[0] and fold(fr[1]+final*dp,A)==s and dp<H-h
 roofphase=fr[1]+final*(H-h)
 assert roofphase%A!=0
 return dict(parameters=[str(e),P,1,L,N,b,c,h,H],source=[str(s),u],target=[str(t),v],durations=[dp,dl,C,g1,d2],a0=a0,source_bad_period=ps,cap_bad_period=pc,predecessors_required=count,npre_seed=npre,qstar=qstar,q=q,M=M,p=p,initial_slope=str(tau0),seed_J=str(J),final_slope=str(final),final_target_index=str(J+a0*N*d2*p),residuals=list(map(str,fr)),indices=ifix,floor_x=str(floorx),floor_corner_suffix_used=suffix,actual_target_x=str(A-fold(FE,L*e)))

cases=[
 check(4,1,4,7,1,3,4,19,2,18,16,2,1,23,22,3,1,F(1875,26),[18,55,38,9]),
 check(4,1,4,7,1,3,16,31,2,30,18,2,1,42,41,2,0,F(267,22),[3,46,6,20]),
 check(4,1,4,7,48,49,50,65,2,64,18,2,1,46,44,2,3,F(4321,24),[45,90,96,23])]
# Fixed resonance classes from the hand proof, independently of the selected seed.
assert all(((2+44*F(9+2*q,22)-56-4)%8==0)==(q%2==0) for q in range(38,42))
assert all(((2+48*F(9+2*q,24)-32)%8==0)==(q%2==1) for q in range(42,46))
out=dict(status='PASS_THREE_UP02_P1_CONTROLS_AND_BOTH_NONEMPTY_PERIOD_TWO_CLASSES',cases=cases,discovery_search=False,physical_ray_replay=False,independent_acceptance=False,whole_r3_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
