"""Exact planar trajectory replay for isolated rational endpoint pairs."""
from fractions import Fraction
from itertools import product
from math import lcm
def tracer(cells,s,t):
    den=lcm(*(v.denominator for v in (*s,*t)))
    sx,sy,tx,ty=(int(v*den) for v in (*s,*t))
    def trace(X,Y):
        p,q=X-sx,Y-sy
        if not p or not q:return False
        dx,dy=(1 if p>0 else -1),(1 if q>0 else -1)
        a=(sx-(dx<0))//den;b=(sy-(dy<0))//den
        assert (a,b) in cells
        ix=abs((a+(dx>0))*den-sx);iy=abs((b+(dy>0))*den-sy)
        hx,hy=dx,dy;ex=ey=1;bx=by=0
        P,Q=abs(p),abs(q)
        while ix<P or iy<Q:
            u,v=ix*Q,iy*P
            if u==v:
                cx=a+(hx>0);cy=b+(hy>0)
                star=sum((cx-i,cy-j) in cells for i,j in product((0,1),repeat=2))
                if star not in (2,4):return False
            if u<=v:
                if (a+hx,b) in cells:a+=hx
                else:
                    bx=2*(a+(hx>0))*den-bx;ex=-ex;hx=-hx
                ix+=den
            if v<=u:
                if (a,b+hy) in cells:b+=hy
                else:
                    by=2*(b+(hy>0))*den-by;ey=-ey;hy=-hy
                iy+=den
        return ex*X+bx==tx and ey*Y+by==ty
    return den,tx,ty,trace
def find(cells,s,t):
    den,x,y,trace=tracer(cells,s,t)
    for r in range(41):
        for a,b in product(range(-r,r+1),repeat=2):
            if max(abs(a),abs(b))!=r:continue
            for h,k in product((1,-1),repeat=2):
                X,Y=2*a*den+h*x,2*b*den+k*y
                if trace(X,Y):return den,X,Y
def point(pair):return tuple(map(Fraction,pair.split(',')))
