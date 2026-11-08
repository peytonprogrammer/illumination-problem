"""UJ02 sole predeclared even-N active-corner formula control."""
from fractions import Fraction as F
from math import gcd,lcm
from pathlib import Path
import json

def v2(n):
 v=0
 while n%2==0:v+=1;n//=2
 return v

e,P,N,K,L=2,1,10,2,4;b,c,h,H=2,3,4,12;s,u,t,v=2,10,14,2
A=N*e;R=K*e;B=L*e
assert 0<P*e<(N-L)*e<(N-K)*e<A and 0<s<A and h<u<H and (N-L)*e<t<A and 0<v<c
n=(2*H-h-u)//2;d=(2*H-u-v)//2;f=d-n;g1=h-c;d2=c-v;Lam=lcm(N,K);g=gcd(Lam*d2,L);Hg=gcd(n*g,N*f)
assert (n,d,f,g,Hg)==(5,6,1,2,10) and v2(N)<=v2(K) and v2(Hg)>=v2(N)
V=f*(s-A)+n*(A-t);assert V==12
ratio=F(g1*N,2*(K//g)*Hg);assert ratio==F(1,2) and ratio.denominator!=1
q=m=j=0;tau=F(A+(A-t)-s,2*d);z1=s+2*n*tau-A
assert tau==2 and z1==2 and z1+g1*tau==R # Illegal seed is discarded.
m+=n*g//Hg;j+=N*f//Hg;q=N*m+g*j;tau+=F(e*N*g,Hg)
y=z1+g1*tau;k=(y+R)//(2*R);z2=y-2*R*k;J=q-N*m-K*k
assert (j,m,q,tau,z1,z2,J)==(1,1,12,F(6),F(2),F(0),0)
assert s+2*n*tau==(2*m+1)*A+z1 and z1+g1*tau==2*R*k+z2
E=z2+d2*tau;r=E%(2*B);assert A-min(r,2*B-r)==t and s+(H-u)*tau==14 and 14%A!=0
out={'status':'PASS_UJ02_PRESCRIBED_EVEN_N_ACTIVE_CORNER_REPAIR','input':{'e':e,'P':P,'N':N,'K':K,'L':L,'S':[s,u],'T':[t,v]},'ratio':str(ratio),'bad_seed_slope':'2','safe_final_slope':str(tau),'residuals':[str(z1),str(z2)],'q':q,'indices':[m,int(k)],'J':J,'discovery_search':False,'physical_ray_replay':False,'independent_acceptance':False,'whole_goal_complete':False}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
