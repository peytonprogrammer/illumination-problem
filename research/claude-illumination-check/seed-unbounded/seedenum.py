"""Exact physical seed enumeration on fixed rooms (approved): every primitive w with |w|<=R from S,
matched against D4 images from T at the same corner with a pi-fold check. Records corner type,
which fans each half visits, and whether the seed stays in the S-T fan path."""
import sys,json,math,random,os
from fractions import Fraction as F
from math import gcd
sys.argv,ARGS=['x'],sys.argv[1:]
src=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'seedcheck.py')).read().split("if __name__")[0]
src=src.replace("H=os.path.dirname(os.path.abspath(__file__))","H='"+os.path.dirname(os.path.abspath(__file__))+"'")
exec(src)
def walkpath(V,a,d):
    """Like walk, but returns the list of developed-segment points (physical) up to the corner."""
    n=len(V); Vs={(F(v[0]),F(v[1])) for v in V}; x,y=F(a[0]),F(a[1]); dx,dy=F(d[0]),F(d[1]); last=-1; pts=[(x,y)]
    for _ in range(2000):
        best=None
        for i in range(n):
            if i==last: continue
            ex,ey=V[(i+1)%n][0]-V[i][0],V[(i+1)%n][1]-V[i][1]; den=dx*ey-dy*ex
            if den==0: continue
            t=((V[i][0]-x)*ey-(V[i][1]-y)*ex)/den; s=((V[i][0]-x)*dy-(V[i][1]-y)*dx)/den
            if t>0 and 0<=s<=1 and (best is None or t<best[0]): best=(t,i)
        if best is None: return None
        t,bi=best; hx,hy=x+t*dx,y+t*dy; pts.append((hx,hy))
        if (hx,hy) in Vs: return pts
        ex,ey=V[(bi+1)%n][0]-V[bi][0],V[(bi+1)%n][1]-V[bi][1]
        dd=(dx*ex+dy*ey)/(ex*ex+ey*ey); dx,dy=2*dd*ex-dx,2*dd*ey-dy; x,y=hx,hy; last=bi
def fan_of(px,py):
    # A point owning the canonical triangle containing (px,py): nearest even-even point in L_inf/L1 sense
    ax=2*round(px/2); ay=2*round(py/2); return (ax,ay)
def fans_visited(pts):
    out=set()
    for (x0,y0),(x1,y1) in zip(pts,pts[1:]):
        for k in range(1,40):
            t=F(k,40); out.add(fan_of(float(x0+(x1-x0)*t),float(y0+(y1-y0)*t)))
    return out
def seeds_all(V,S,T,R):
    WALLD={(1,0),(0,1),(1,1),(1,-1)}; res=[]
    dirs=[(p,q) for p in range(-R,R+1) for q in range(-R,R+1) if gcd(p,q)==1 and p*p+q*q<=R*R]
    for w in dirs:
        if (abs(w[0]),abs(w[1])) in {(1,0),(0,1),(1,1)}: continue
        r=walk(V,S,w)
        if not r or r[1]!=1: continue
        c,_,v1=r
        for m in D4:
            w2=(m[0][0]*w[0]+m[0][1]*w[1],m[1][0]*w[0]+m[1][1]*w[1]); q=walk(V,T,w2)
            if q and q[1]==1 and q[0]==c and fold_ok(V,c,v1,(-q[2][0],-q[2][1])):
                res.append(dict(w=w,w2=w2,c=(int(c[0]),int(c[1])),fansS=sorted(fans_visited(walkpath(V,S,w))),fansT=sorted(fans_visited(walkpath(V,T,w2)))))
    return res
