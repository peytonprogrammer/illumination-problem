"""Count strict portal placements by integer lattice arithmetic, without producing rays."""
from fractions import Fraction as F
from functools import reduce
from math import gcd,lcm,ceil,floor
from pathlib import Path
import sys,os
here=Path(__file__).resolve().parent
d=next(here.parents[1].glob('illumination-generalization*/fable/directions*/d58-corridor-limit'))
os.chdir(d);sys.path.insert(0,str(d))
from tests_lib import resonant
from build import DOOR

def bez(a,b):
    if not b:return abs(a),1 if a>=0 else -1,0
    g,x,y=bez(b,a%b);return g,y,x-(a//b)*y

def floors(n,m,a,b):
    """Sum floor((a*i+b)/m), 0 <= i < n, by Euclidean division."""
    qa,a=divmod(a,m);qb,b=divmod(b,m)
    ans=qa*n*(n-1)//2+qb*n
    if not a:return ans
    h=(a*(n-1)+b)//m
    return ans+h*n-floors(h,a,m,m-b+a-1)

def count(room,geo):
    _,_,_,_,_,S,T=geo
    X=[S[0],*(x for x in room.xs if S[0]<x<T[0]),T[0]]
    bounds=[]
    for a,b in zip(X,X[1:]):
        i=sum(x< (a+b)/2 for x in room.xs)-1
        ys=sorted(y for x,y in room.cells if x==i)
        assert ys==list(range(min(ys),max(ys)+1))
        bounds.append((room.ys[min(ys)],room.ys[max(ys)+1]))
    ds=[b-a for a,b in zip(X,X[1:])];D=sum(ds)
    P=[2*(v-u) for u,v in bounds]
    data=[]
    for i in range(1,len(ds)):
        f=sum(ds[:i])/D
        data.append([max(bounds[i-1][0],bounds[i][0]),min(bounds[i-1][1],bounds[i][1]),S[1]+f*(T[1]-S[1]),*[p*(f-int(j<i)) for j,p in enumerate(P)]])
    scale=lcm(*(x.denominator for row in data for x in row))
    rows=[[int(x*scale) for x in row] for row in data]
    answer=boxcount(rows)
    if len(rows)==2:assert answer==boxcount(rows[::-1])
    return answer

def boxcount(rows):
    L,U,c,*v=rows[0];g=reduce(gcd,v);i0=(L-c)//g+1;i1=(U-c-1)//g
    if len(rows)==1:return i1-i0+1
    assert len(rows)==2
    l,u,e,*w=rows[1];h=t=0
    for a,b in zip(v,w):
        h,j,k=bez(h,a);t=j*t+k*b
    H=reduce(gcd,(a*b-A*B for a,B in zip(v,w) for A,b in zip(v,w)))//g
    n=i1-i0+1
    return floors(n,H,-t,u-1-e-t*i0)-floors(n,H,-t,l-e-t*i0)
if __name__=='__main__':
    for item in DOOR:
        vals=[]
        for k in range(2,16):
            try:r,g,info=resonant(*item,k,'double')
            except AssertionError:vals.append('-');continue
            if 2*(g[-1][1]-g[4])!=info['ell']:vals.append('outside');continue
            assert len(r.walls)==10
            placements=count(r,g);assert placements>0
            vals.append(str(placements))
        print(item,' '.join(vals))
