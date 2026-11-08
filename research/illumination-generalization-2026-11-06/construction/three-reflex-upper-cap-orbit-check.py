"""UC01 three predeclared formula controls. No ray engine or discovery."""
from fractions import Fraction as F
from math import gcd
from pathlib import Path
import json

def fold(x,w):
 r=x%(2*w)
 return min(r,2*w-r)

def center(x,w):
 k=(x+w)//(2*w)
 return x-2*w*k,int(k)

def state(e,N,h,c,H,s,u,t,v,q):
 A=e*N;C=2*H-h-u;D=2*H-u-v;z=A-t
 tau=F(A+z-s+2*e*q,D)
 z1,m=center(s+C*tau-A,A)
 assert abs(z1)<e
 z2,k=center(z1+(h-c)*tau,e)
 J=q-N*m-k
 assert z2+(c-v)*tau==z+2*e*J
 return tau,z1,z2,m,k,J

def check(name,e,P,L,N,b,c,h,H,s,u,t,v,expected,needs_return):
 A=e*N;C=2*H-h-u;D=2*H-u-v;n=C//2;d=D//2;G=gcd(n,N*d);Q=N*d//G
 assert C==2*n and D==2*d and 1<=G<=n<d and gcd(n//G,Q)==1
 seed=state(e,N,h,c,H,s,u,t,v,0)
 # Exact cap return, including the deliberately bad seed in B.
 ret=state(e,N,h,c,H,s,u,t,v,Q)
 assert ret[0]-seed[0]==F(e*N,G) and ret[1]==seed[1]
 assert F((h-c)*N,2*G).denominator!=1
 if needs_return:
  assert abs(seed[2])==e and abs(ret[2])<e
  chosen=ret;q=Q
 else:
  assert abs(seed[2])<e
  chosen=seed;q=0
 tau,z1,z2,m,k,J=chosen
 p=(-J*pow(N*(c-v),-1,L))%L
 final=tau+2*e*N*p
 fm=m+C*p;fk=k+(h-c)*N*p;fJ=J+N*(c-v)*p
 assert final==expected and abs(z1)<e and abs(z2)<e and fJ%L==0
 assert s+C*final==(2*fm+1)*A+z1
 assert z1+(h-c)*final==2*e*fk+z2
 E=z2+(c-v)*final
 assert E==A-t+2*e*fJ and A-fold(E,L*e)==t
 roof=s+(H-u)*final
 # Reproduce the explicit nearest-coset algorithm on this same fixed input.
 X0=s+C*F(A+(A-t)-s,D);spacing=F(2*e*G,d)
 ell=((A-X0)/spacing+F(1,2))//1
 aq=int(ell*pow(n//G,-1,Q)%Q)
 ast=state(e,N,h,c,H,s,u,t,v,aq)
 assert abs(ast[1])<e and abs(X0+spacing*ell-A)<=F(e*G,d)<e
 if abs(ast[2])==e:
  aq+=Q;ast=state(e,N,h,c,H,s,u,t,v,aq)
 assert abs(ast[2])<e
 ap=(-ast[5]*pow(N*(c-v),-1,L))%L
 afinal=ast[0]+2*e*N*ap
 assert A-fold(ast[2]+(c-v)*afinal,L*e)==t
 return dict(name=name,n=n,d=d,G=G,Q=Q,seed=list(map(str,seed)),cap_return=list(map(str,ret)),selected_q=q,p=p,final_slope=str(final),final_indices=[fm,fk],final_J=fJ,residuals=[str(z1),str(z2)],ordinary_roof=roof%A!=0,actual_target=[t,v],nearest_algorithm_q=aq,nearest_algorithm_final_slope=str(afinal))

cases=[check('A_near_roof',4,1,4,7,2,3,4,12,2,10,20,2,F(1025,6),False),check('B_active_right_corner_repair',2,3,4,9,1,3,4,9,2,6,14,2,F(20),True),check('C_nontrivial_G',4,1,4,7,2,3,4,12,2,6,20,2,F(1361,8),False)]
out=dict(status='PASS_THREE_PRESCRIBED_UC01_FORMULA_AND_EXPLICIT_SELECTOR_CHECKS',cases=cases,discovery_search=False,physical_ray_replay=False,independent_acceptance=False,whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
