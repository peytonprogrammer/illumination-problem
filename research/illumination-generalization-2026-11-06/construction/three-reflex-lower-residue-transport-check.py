"""LJ05 one predeclared target-residue transport control; no search."""
from fractions import Fraction as F
from math import gcd,lcm
from pathlib import Path
import json

e,P,K,L,N=2,3,4,8,13;b,c,h,H=1,3,8,14;s,u,t,v=2,6,20,2;A=N*e;a=P*e;R=K*e;B=L*e
assert 0<a<A-B<A-R<A and 0<b<c<h<H and 0<s<a and b<u<h and A-B<t<A and 0<v<c
al=(h-u)//2;be=H-h;f=(h-v)//2;d=al+be+f;z=A-t;g1=h-c;d2=c-v
la=-F(s,2*e*P)-F(al*N,2*P*be);mu=F(z,2*e*P)-F(f*N,2*P*be)
assert (la,mu)==(F(-19,36),F(-7,12))
i=-int((la+F(1,2))//1);j=-int((mu+F(1,2))//1);m=0;q=P*i+N*m+P*j;tau=F(A+z-s+2*e*q,2*d)
z0=s+2*al*tau-2*a*i;z1=z0+2*be*tau-A
assert (i,j,q,tau,z0,z1)==(1,1,6,F(27,10),F(-23,5),F(9,5))
assert abs(z0)<a and abs(z1)<a<=R
hh=gcd(gcd(N*al,P*be),N*f);di,dm,dj=N*al//hh,P*be//hh,N*f//hh;step=F(e*P*N,hh)
Lam=lcm(P,N,K);Gamma=gcd(Lam*d2,L);rho=Gamma//gcd(P,Gamma)
assert (hh,di,dm,dj,step,Gamma,rho)==(1,13,18,39,F(78),4,4)
ell=(-j*pow(dj,-1,rho))%rho;assert ell==1
i+=di*ell;m+=dm*ell;j+=dj*ell;q=P*i+N*m+P*j;tau+=step*ell
assert (i,m,j,q,tau)==(14,18,40,396,F(807,10)) and j%rho==0
assert s+2*al*tau-2*a*i==z0 and z0+2*be*tau-(2*m+1)*A==z1
Y=z1+g1*tau;k=int((Y+R)//(2*R));z2=Y-2*R*k;J=P*j-K*k
assert (k,z2,J)==(25,F(53,10),20) and abs(z2)<R and J%Gamma==0
assert (g1*step*rho/(2*R)).denominator!=1
p=(-J//Gamma*pow(Lam*d2//Gamma,-1,L//Gamma))%(L//Gamma);assert p==1
final=tau+2*e*Lam*p;fi=i+2*al*Lam*p//P;fm=m+2*be*Lam*p//N;fk=k+g1*Lam*p//K
assert (final,fi,fm,fk)==(F(7047,10),118,162,220)
assert s+2*al*final-2*a*fi==z0 and z0+2*be*final-(2*fm+1)*A==z1 and z1+g1*final-2*R*fk==z2
E=z2+d2*final;phase=E%(2*B);assert A-min(phase,2*B-phase)==t and (J+Lam*d2*p)%L==0
roof=z0+be*final;assert roof==F(21118,5) and roof%A!=0
out={'status':'PASS_LJ05_PRESCRIBED_WIDER_SOURCE_TARGET_RESIDUE_TRANSPORT','parameters':{'e':e,'P':P,'K':K,'L':L,'N':N,'b':b,'c':c,'h':h,'H':H},'S':[s,u],'T':[t,v],'Gamma':Gamma,'rho':rho,'H0':hh,'initial_j':1,'null_j_step':dj,'null_slope_step':str(step),'null_steps':ell,'target_p':p,'final_slope':str(final),'residuals':list(map(str,[z0,z1,z2])),'indices':[fi,fm,fk],'actual_target':[t,v],'roof_phase':str(roof),'discovery_search':False,'physical_ray_replay':False,'independent_acceptance':False,'whole_goal_complete':False}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
