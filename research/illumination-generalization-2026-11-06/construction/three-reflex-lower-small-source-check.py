"""LJ04 sole prescribed actual-input arithmetic check; no discovery."""
from fractions import Fraction as F
from math import gcd,lcm
from pathlib import Path
import json

e,P,K,L,N=4,1,2,4,9;b,c,h,H=1,3,8,14;s,u,t,v=2,6,24,2
A=N*e;R=K*e;B=L*e
assert 0<e<A-B<A-R<A and 0<b<c<h<H and 0<s<e and b<u<h and A-B<t<A and 0<v<c
assert all(x%2==0 for x in [s,u,t,v])
a=(h-u)//2;be=H-h;f=(h-v)//2;d=a+be+f;z=A-t;g1=h-c;d2=c-v
assert (a,be,f,d)==(1,6,3,10) and f%2
vi=(F(-2*e*(be+f),d),F(-2*e*f,d));vj=(F(2*e*a,d),F(2*e*(a+be),d))
tau0=F(A+z-s,2*d);r0=(s+2*a*tau0,s+2*(a+be)*tau0-A);det=vi[0]*vj[1]-vi[1]*vj[0]
la=(r0[0]*vj[1]-r0[1]*vj[0])/det;mu=(vi[0]*r0[1]-vi[1]*r0[0])/det
assert (la,mu)==(F(-1),F(-3,4))
i=-int((la+F(1,2))//1);j=-int((mu+F(1,2))//1);m=0;q=i+N*m+j;tau=F(A+z-s+2*e*q,2*d)
z0=s+2*a*tau-2*e*i;z1=z0+2*be*tau-(2*m+1)*A
assert (i,j,q,tau,z0,z1)==(1,1,2,F(31,10),F(1,5),F(7,5))
assert abs(z0)<e and abs(z1)<e<=R
M=gcd(gcd(N*a,be),N*f);di,dm,dj=N*a//M,be//M,N*f//M;step=F(e*N,M)
Lam=lcm(N,K);Gamma=gcd(Lam*d2,L)
assert (M,di,dm,dj,step,Gamma)==(3,3,2,9,F(12),2) and dj%2 and j%Gamma!=0
ell=(-j*pow(dj,-1,Gamma))%Gamma;assert ell==1
i+=di*ell;m+=dm*ell;j+=dj*ell;q=i+N*m+j;tau+=step*ell
assert (i,m,j,q,tau)==(4,2,10,32,F(151,10)) and j%Gamma==0
assert s+2*a*tau-2*e*i==z0 and z0+2*be*tau-(2*m+1)*A==z1
Y=z1+g1*tau;k=int((Y+R)//(2*R));z2=Y-2*R*k;J=j-K*k
assert (k,z2,J)==(5,F(-31,10),0) and abs(z2)<R
assert F(g1*N,2*(K//Gamma)*M).denominator!=1
E=z2+d2*tau;phase=E%(2*B);assert E==z and A-min(phase,2*B-phase)==t
roof=z0+be*tau;assert roof==F(454,5) and roof%A!=0
out={'status':'PASS_LJ04_PRESCRIBED_MISSING_TARGET_RESIDUE_TRANSPORT','parameters':{'e':e,'P':P,'K':K,'L':L,'N':N,'b':b,'c':c,'h':h,'H':H},'S':[s,u],'T':[t,v],'Gamma':Gamma,'M':M,'rounding':list(map(str,[la,mu])),'bad_target_seed_j':1,'null_j_step':dj,'null_slope_step':str(step),'selected_null_steps':ell,'final_j':j,'final_q':q,'final_slope':str(tau),'residuals':list(map(str,[z0,z1,z2])),'indices':[i,m,k],'J':J,'roof_phase':str(roof),'actual_target':[t,v],'discovery_search':False,'physical_ray_replay':False,'independent_acceptance':False,'whole_goal_complete':False}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
