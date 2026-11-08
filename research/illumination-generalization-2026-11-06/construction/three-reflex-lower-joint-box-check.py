"""LJ01 sole predeclared lower-source joint-box formula check; no search."""
from fractions import Fraction as F
from math import gcd
from pathlib import Path
import json

e,N,L=4,9,4;b,c,h,H=1,3,6,9;s,u,t,v=2,4,24,2
A=N*e;B=L*e;l=A-B;w=A-e
assert 0<e<l<w<A and 0<b<c<h<H
assert 0<s<e and b<u<h and l<t<A and 0<v<c
assert all(x%2==0 for x in [s,u,t,v])
alpha=(h-u)//2;beta=H-h;f=(h-v)//2;d=alpha+beta+f;z=A-t;g1=h-c;d2=c-v
assert (alpha,beta,f,d)==(1,3,2,6) and beta%2 and gcd(beta,N)==3 and F(z,e).denominator==1
vi=(F(-2*e*(beta+f),d),F(-2*e*f,d));vj=(F(2*e*alpha,d),F(2*e*(alpha+beta),d))
tau0=F(A+z-s,2*d);r0=(s+2*alpha*tau0,s+2*(alpha+beta)*tau0-A)
det=vi[0]*vj[1]-vi[1]*vj[0];assert det==F(-4*e*e*beta,d)
lam=(r0[0]*vj[1]-r0[1]*vj[0])/det;mu=(vi[0]*r0[1]-vi[1]*r0[0])/det
assert (lam,mu)==(F(-7,4),F(-3,2))
i=-int((lam+F(1,2))//1);j=-int((mu+F(1,2))//1);m=0;q=i+N*m+j
assert (i,j,q)==(2,1,3)
tau=F(A+z-s+2*e*q,2*d);z0=s+2*alpha*tau-2*e*i;z1=z0+2*beta*tau-(2*m+1)*A
assert (tau,z0,z1)==(F(35,6),F(-7,3),F(-10,3))
assert abs(z0)<e and abs(z1)<e
assert (abs(vi[0])+abs(vj[0]))/2==e and (abs(vi[1])+abs(vj[1]))/2==e
assert F(s,e).denominator>1 and beta%2==1 and F(beta*s,e).denominator>1
M=gcd(gcd(alpha*N,beta),N*f);di,dm,dj=alpha*N//M,beta//M,N*f//M
assert M==3 and di+N*dm+dj==N*d//M
step=F(e*N,M);assert 2*alpha*step==2*e*di and 2*beta*step==2*A*dm
assert F(g1*N,2*M).denominator!=1
Y=z1+g1*tau;k=int((Y+e)//(2*e));z2=Y-2*e*k;J=j-k
assert (k,z2,J)==(2,F(-11,6),-1) and abs(z2)<e
p=(-J*pow(N*d2,-1,L))%L;assert p==1
final=tau+2*e*N*p;fi=i+2*alpha*N*p;fm=m+2*beta*p;fk=k+g1*N*p;fq=q+2*d*N*p;fJ=J+N*d2*p
assert (final,fi,fm,fk)==(F(467,6),20,6,29)
assert s+2*alpha*final-2*e*fi==z0
assert z0+2*beta*final-(2*fm+1)*A==z1
assert z1+g1*final-2*e*fk==z2
E=z2+d2*final;assert E==z+2*e*fJ and fJ%L==0
foldphase=E%(2*B);assert A-min(foldphase,2*B-foldphase)==t
roof=z0+beta*final;assert roof==F(1387,6) and roof%A!=0
out={'status':'PASS_LJ01_PRESCRIBED_LOWER_JOINT_BOX_FORMULAS','input':{'e':e,'N':N,'L':L,'b':b,'c':c,'h':h,'H':H,'S':[s,u],'T':[t,v]},'cap_gcd':gcd(beta,N),'coefficient_rounding':[str(lam),str(mu)],'seed':{'i':i,'m':m,'j':j,'q':q,'slope':str(tau),'J':J},'M':M,'null_increment':[di,dm,dj],'final':{'slope':str(final),'indices':[fi,fm,fk],'q':fq,'J':fJ,'residuals':list(map(str,[z0,z1,z2])),'roof_phase':str(roof),'actual_target':[t,v]},'discovery_search':False,'physical_ray_replay':False,'independent_acceptance':False,'whole_goal_complete':False}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
