"""Independent check of Codex's symmetric-U two-phase theorem.
Builds each path by exact billiard simulation from the initial direction only."""
from fractions import Fraction as F
import random, math, sys, os
CAP=int(os.environ.get("CAP","5000"))
def room(a,M,c,H,AL=None,HR=None):
    A=2*a+M; b=a+M
    return [(F(0),F(0)),(A,F(0)),(A,H),(b,H),(b,c),(a,c),(a,H),(F(0),H)]
def shoot(V,s,t,d,cap=CAP):
    p=s; contacts=[]; n=len(V)
    for _ in range(cap):
        best=None
        # target hit?
        w=(t[0]-p[0],t[1]-p[1])
        if w[0]*d[1]-w[1]*d[0]==0 and w[0]*d[0]+w[1]*d[1]>0:
            tt=w[0]/d[0] if d[0] else w[1]/d[1]; best=(tt,'T',None)
        for i in range(n):
            a,b=V[i],V[(i+1)%n]; e=(b[0]-a[0],b[1]-a[1])
            den=d[0]*e[1]-d[1]*e[0]
            if den==0: continue
            ap=(a[0]-p[0],a[1]-p[1])
            tt=(ap[0]*e[1]-ap[1]*e[0])/den; u=(ap[0]*d[1]-ap[1]*d[0])/den
            if tt>0 and 0<=u<=1 and (best is None or tt<best[0]):
                best=(tt,'W',(i,u))
        tt,kind,info=best
        q=(p[0]+tt*d[0],p[1]+tt*d[1])
        if kind=='T': return contacts,'ok'
        i,u=info
        if u in (0,1): return None,'corner'
        a,b=V[i],V[(i+1)%n]
        d=(-d[0],d[1]) if a[0]==b[0] else (d[0],-d[1])
        contacts.append(q); p=q
    return None,'cap'
def first(a,x,T,phase):
    ell=a-x if phase=='minus' else a+x
    n=max(0,math.floor((T-ell)/(2*a))+1); return ell+2*n*a
def three(a,M,c,H,x,y):
    h=M/2; Y=y/c; A=2*a+M; V=room(a,M,c,H); s=(x,y); t=(A-x,y)
    out=[]
    for ph in ('minus','plus'):
        L=first(a,x,h*(Y-1),ph); out.append((V,s,t,(1 if ph=='minus' else -1, -y/(L+h))))
    K=h*Y; TN=h*(Y-1)/2
    L=first(a,x,TN,'minus'); ph='minus'
    if L==K: L=first(a,x,TN,'plus'); ph='plus'
    out.append((V,s,t,(1 if ph=='minus' else -1, -(y+c)/(L+h))))
    return out
def rq(lo,hi,den=97): return F(random.randint(1,den-1),den)*(hi-lo)+lo
random.seed(int(sys.argv[1]) if len(sys.argv)>1 else 0)
fails=0; N=int(sys.argv[2]) if len(sys.argv)>2 else 2000; maxb=0
for _ in range(N):
    a=rq(0,3); M=rq(0,3); H=rq(0,3); c=rq(0,H); x=rq(0,a); y=rq(c,H)
    if random.random()<0.2: y=c+F(1,10**random.randint(2,4))*(H-c)   # near passage height
    if random.random()<0.2: c=c/10**random.randint(1,3)               # thin passage
    if not (0<c<y<H): continue
    res=[shoot(*args) for args in three(a,M,c,H,x,y)]
    if any(r[1]!='ok' for r in res): fails+=1; print('FAIL',[r[1] for r in res],a,M,c,H,x,y); continue
    S=[set(r[0]) for r in res]; maxb=max(maxb,max(len(r[0]) for r in res))
    zB=((2*a+M)/2,F(0))
    if S[0]&S[1]!={zB} or S[0]&S[1]&S[2] or zB in S[2]: fails+=1; print('CONTACT',a,M,c,H,x,y,S[0]&S[1])
print('instances',N,'fails',fails,'max reflections',maxb)
