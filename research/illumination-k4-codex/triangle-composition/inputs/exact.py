"""Exact rational lit-path check for one room/pair; prints first lit direction."""
from fractions import Fraction as F
from math import gcd
import sys
def run1(V,a,b,d,B=400):
    return run(V,a,b,B=B,dirs=[d])[0] is not None
def run(V,a,b,R=10,B=400,dirs=None):
    n=len(V)
    if sum(V[i][0]*V[(i+1)%n][1]-V[(i+1)%n][0]*V[i][1] for i in range(n))<0:V=V[::-1]
    def inside(x,y):
        c=False
        for i in range(n):
            (ax,ay),(bx,by)=V[i],V[(i+1)%n]
            if (ay>y)!=(by>y) and x<ax+F(y-ay)*(bx-ax)/(by-ay):c=not c
        return c
    D=dirs or [(p,q) for p in range(-R,R+1) for q in range(-R,R+1) if gcd(p,q)==1]
    for p,q in D:
        if True:
            x,y,dx,dy=F(a[0]),F(a[1]),F(p),F(q)
            e=F(1,10**6)
            if not inside(x+dx*e,y+dy*e+e*e):continue
            last=-1;path=[(x,y)]
            for k in range(B):
                best=None
                for i in range(n):
                    if i==last:continue
                    ex,ey=V[(i+1)%n][0]-V[i][0],V[(i+1)%n][1]-V[i][1]
                    den=dx*ey-dy*ex
                    if den==0:continue
                    t=((V[i][0]-x)*ey-(V[i][1]-y)*ex)/den;s=((V[i][0]-x)*dy-(V[i][1]-y)*dx)/den
                    if t>0 and 0<=s<=1 and (best is None or t<best[0]):best=(t,i)
                if best is None:break
                t,bi=best
                tx,ty=b[0]-x,b[1]-y
                if tx*dy-ty*dx==0 and 0<tx*dx+ty*dy<=t*(dx*dx+dy*dy):return (p,q),path+[b]
                hx,hy=x+t*dx,y+t*dy
                if (hx,hy) in set(map(lambda v:(F(v[0]),F(v[1])),V)):break
                ex,ey=V[(bi+1)%n][0]-V[bi][0],V[(bi+1)%n][1]-V[bi][1]
                dd=(dx*ex+dy*ey)/(ex*ex+ey*ey);dx,dy=2*dd*ex-dx,2*dd*ey-dy;x,y=hx,hy;last=bi;path.append((x,y))
    return None,None
if __name__=='__main__':
    V=[tuple(map(int,s.split(','))) for s in sys.argv[1].split()]
    a=tuple(map(int,sys.argv[2].split(',')));b=tuple(map(int,sys.argv[3].split(',')))
    d,P=run(V,a,b,int(sys.argv[4]) if len(sys.argv)>4 else 10)
    print(d,[(str(x),str(y)) for x,y in P] if P else '')
