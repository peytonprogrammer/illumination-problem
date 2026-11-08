"""UDPA01 prescribed formula checks, no search/census/ray engine."""
from fractions import Fraction as F
from pathlib import Path
import json

def fold(x,w):
 x=x%(2*w)
 return min(x,2*w-x)

def check(N,r,expected,expected_indices):
 d=N+5;A=4*N;z=2*r;k=2+(r-1)%4;nu=int(k==5)
 assert 2<=k<=5 and (k-r-1)%4==0 and N>=7 and N%2==1
 q=N*N+4*N+(k-r-9)//4;tau0=4*N-2+F(k,d)
 assert tau0==F(A+z-2+8*q,2*d)
 zp=-2+F(2*k,d);z0=-2+F(6*k,d);z1=2*k-6-F(2*k,d)
 kr=(N-1)//2+nu;z2=z1+tau0-8*kr
 expected_z2=2*k-4-F(k,d) if k<=4 else -2-F(5,d)
 assert z2==expected_z2 and all(abs(x)<4 for x in (zp,z0,z1,z2))
 E0=z2+tau0;J=F(2*N+k-r-3,4)-nu
 assert J.denominator==1 and E0==4*N+2*k-6-8*nu and E0-z==8*J
 p=int((-N*J)%4);final=tau0+8*N*p
 np=1+2*p;nl=2*N-1+4*N*p;nm=N+2*(N+1)*p;nk=kr+N*p
 assert [np,nl,nm,nk]==expected_indices and final==expected
 assert 2+2*final-8*N*np==zp
 assert zp+4*final-8*nl==z0
 assert z0+2*(N+1)*final-(2*nm+1)*A==z1
 assert z1+final-8*nk==z2
 E=z2+final;I=(E-z)/8
 assert I==J+N*p and I%4==0 and A-fold(E,16)==A-z
 floor_phase=zp+2*final;floorx=fold(floor_phase,4)
 assert floorx==2+F(4*k,d) and 0<floorx<4
 roof_phase=z0+(N+1)*final
 assert roof_phase%1==F(2*k,d) and roof_phase%A!=0
 # The old seed belongs to a different, frozen wrong cap coset.
 old=4*N-F(3,d);assert final!=old and tau0!=old
 return dict(N=N,target_r=r,k=k,q=q,seed_slope=str(tau0),seed_J=str(J),p=p,final_slope=str(final),final_J=str(I),residuals=list(map(str,(zp,z0,z1,z2))),indices=[np,nl,nm,nk],floor_x=str(floorx),actual_target=[str(A-fold(E,16)),2])

cases=[check(7,4,F(1661,12),[5,69,39,18]),check(9,2,F(479,14),[1,17,9,4])]
out=dict(status='PASS_TWO_UDPA01_PRESCRIBED_FORMULA_CONTROLS',cases=cases,unfrozen_hand_calibration_correction='N7 final nleft is69, not41: general proof increment4Np was correct; corrected the hand-control typo before checker/freeze.',discovery_search=False,physical_ray_replay=False,independent_acceptance=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
