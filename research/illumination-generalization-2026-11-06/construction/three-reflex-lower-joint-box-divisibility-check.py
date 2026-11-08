"""LJ02 sole predeclared even-beta/non-dyadic formula check; no discovery."""
from fractions import Fraction as F
from math import gcd
from pathlib import Path
import json

e,N,L=5,9,4;b,c,h,H=1,3,6,12;s,u,t,v=2,4,32,2;A=N*e;B=L*e
assert 0<e<A-B<A-e<A and 0<b<c<h<H and 0<s<e and b<u<h and A-B<t<A and 0<v<c
assert all(x%2==0 for x in [s,u,t,v])
a=(h-u)//2;beta=H-h;f=(h-v)//2;d=a+beta+f;z=A-t;g1=h-c;d2=c-v
assert beta==6 and gcd(e,beta)==1 and gcd(beta,N)==3 and F(beta*s,e)==F(12,5)
vi=(F(-2*e*(beta+f),d),F(-2*e*f,d));vj=(F(2*e*a,d),F(2*e*(a+beta),d));det=vi[0]*vj[1]-vi[1]*vj[0]
tau0=F(A+z-s,2*d);r0=(s+2*a*tau0,s+2*(a+beta)*tau0-A)
la=(r0[0]*vj[1]-r0[1]*vj[0])/det;mu=(vi[0]*r0[1]-vi[1]*r0[0])/det
assert (la,mu)==(F(-19,20),F(-1,5))
i=-int((la+F(1,2))//1);j=-int((mu+F(1,2))//1);m=0;q=i+N*m+j;tau=F(A+z-s+2*e*q,2*d)
z0=s+2*a*tau-2*e*i;z1=z0+2*beta*tau-(2*m+1)*A
assert (i,m,j,q,tau,z0,z1)==(1,0,0,1,F(11,3),F(-2,3),F(-5,3))
assert abs(z0)<e and abs(z1)<e
Y=z1+g1*tau;k=int((Y+e)//(2*e));z2=Y-2*e*k;J=j-k
assert (k,z2,J)==(1,F(-2,3),-1) and abs(z2)<e
M=gcd(gcd(a*N,beta),N*f);step=F(e*N,M)
assert M==3 and F(g1*N,2*M).denominator!=1 and 2*a*step==2*e*(a*N//M) and 2*beta*step==2*A*(beta//M)
p=(-J*pow(N*d2,-1,L))%L;final=tau+2*e*N*p;fi=i+2*a*N*p;fm=m+2*beta*p;fk=k+g1*N*p
assert (p,final,fi,fm,fk)==(1,F(281,3),19,12,28)
assert s+2*a*final-2*e*fi==z0 and z0+2*beta*final-(2*fm+1)*A==z1 and z1+g1*final-2*e*fk==z2
E=z2+d2*final;r=E%(2*B);assert E==93 and A-min(r,2*B-r)==t
roof=z0+beta*final;assert roof==F(1684,3) and roof%A!=0
out={'status':'PASS_LJ02_PRESCRIBED_EVEN_BETA_NON_DYADIC_FORMULA_CONTROL','input':{'e':e,'N':N,'L':L,'b':b,'c':c,'h':h,'H':H,'S':[s,u],'T':[t,v]},'source_divisibility':str(F(beta*s,e)),'width_cap_gcd':gcd(e,beta),'cap_outer_gcd':gcd(beta,N),'rounding':[str(la),str(mu)],'seed_slope':str(tau),'final_slope':str(final),'residuals':list(map(str,[z0,z1,z2])),'indices':[fi,fm,fk],'actual_target':[t,v],'roof_phase':str(roof),'discovery_search':False,'physical_ray_replay':False,'independent_acceptance':False,'whole_goal_complete':False}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
