"""Verify each saved proof tree using exact fractions and the Python cylinder implementation."""
from functools import lru_cache
from fractions import Fraction as F
from math import floor,ceil,lcm
from pathlib import Path
import sys
base=Path(__file__).resolve().parent
sys.path.insert(0,str(next(base.parents[1].glob('illumination-generalization*/fable/directions*/d13-cylinder-cover'))))
from cyl import labels
out=Path(sys.argv[1])
unit=65536
radius=3856
assert F(radius,unit)>=F(1,17)
totals=[0,0,0]
certificate_dir=Path(sys.argv[2]) if len(sys.argv)>2 else base
direct_tests=0
for room in (0,1):
 for swap in (0,1):
    tag=f'{room}{swap}'
    flat=list(map(int,(out/f'room{tag}').read_text().split()[2:]))
    cells=list(zip(flat[::2],flat[1::2]))
    C=frozenset(cells)
    def row(c):
        x,y=c;l=x;r=x+1
        while (l-1,y) in C:l-=1
        while (r,y) in C:r+=1
        return l,r
    period=lcm(*(2*(row(c)[1]-row(c)[0]) for c in C))
    target=iter((certificate_dir/f'cert{tag}.txt').read_text().splitlines())
    @lru_cache(None)
    def direction(p,q):return labels(C,p,q)
    @lru_cache(None)
    def stripe(p,q,c,sg,k,line):
        # Sample a point in the infinite straightened horizontal row. Fold x to the room.
        # h avoids vertical tile edges for integer and half-integer transverse samples.
        a,b=cells[c];l,r=row((a,b)); w=r-l
        h=F(1,4*(p+q+2))
        z=F(k) if line else F(2*k+1,2)
        xu=a+(z+p*h)/q
        v=(xu-l)%(2*w)
        assert v!=w and v!=0
        x=l+min(v,2*w-v)
        y=b+(h if sg==1 else 1-h)
        sign=sg*(1 if v<w else -1)
        L=direction(p,q)
        kphysical=q*x-sign*p*y
        assert (kphysical.denominator==1)==line
        d=(L.plusline if sign==1 else L.minusline) if line else (L.plus if sign==1 else L.minus)
        return d[floor(x),floor(y)][floor(kphysical)]
    def options(p,q,c,sg,lo,hi):
        # Intersect the open/closed label sets attained on every piece, separately.
        available=[]
        for k in range(floor(lo),ceil(hi)):
            lab=stripe(p,q,c,sg,k,False)
            available.append(({lab},{lab}))
        for k in range(ceil(lo),floor(hi)+1):
            op=stripe(p,q,c,sg,k,True)
            available.append(({op} if op is not None else set(),
                              {stripe(p,q,c,sg,k-1,False),stripe(p,q,c,sg,k,False)}))
        assert available
        return tuple(set.intersection(*(v[i] for v in available)) for i in (0,1))
    for marks in (list(map(int,l.split())) for l in (out/f'ends{tag}').read_text().splitlines()):
      for main in (0,1):
        c0=marks[0];c1=marks[5]
        assert next(target)==f'R {c0} {c1} {main}'
        top=max(unit//4,period*radius)
        bounds=[(0,radius)]*4+[(0,top)]*2
        bounds[4+main]=(unit//8,top)
        def verify(z):
            tok=next(target).split(); kind=tok[0]
            if kind=='S':
                i=int(tok[1]);l,r=z[i];mid=(l+r)//2;assert l<mid<r
                return sum(verify(z[:i]+[b]+z[i+1:]) for b in ((l,mid),(mid,r)))
            if kind=='E':
                assert z[5-main][0]>z[4+main][1]
                return 0
            assert kind=='W'
            j,p,q=map(int,tok[1:])
            sets=[]
            for e in (0,1):
                c,x,y,a,b=marks[5*e:5*e+5]
                sx=1 if x==a else -1;sy=1 if y==b else -1
                result=[set(),set()]
                for sg in (1,-1):
                    ychart=(y-b if sg==1 else 1-y+b)
                    off=unit*(q*(x-a)-p*ychart)
                    terms=[(q*sx,z[2*e]),(-sg*p*sy,z[2*e+1]),(-sg*q*j*sy,z[4+e])]
                    ranges=[sorted((coeff*l,coeff*h)) for coeff,(l,h) in terms]
                    lo,hi=(F(off+sum(w[k] for w in ranges),unit) for k in (0,1))
                    op,cl=options(p,q,c,sg,lo,hi)
                    result[0].update(op);result[1].update(cl)
                sets.append(result)
            assert (sets[0][0]&sets[1][1]) or (sets[1][0]&sets[0][1]),(tag,marks,main,tok,z)
            return 1
        n=verify(bounds)
        assert next(target)==f'{c0} {c1} {main} 1 {n}'
        totals[0]+=1;totals[1]+=n
    assert next(target,None) is None
    # Direct check of the pullback sign against the labels of the actual long slope.
    # Compare labeled strips up to relabeling, including integer leaves.
    for p,q in [(1,1),(3,2),(2,3)]:
     for h in (-1,1):
        P=p+h*period*q
        L=direction(abs(P),q)
        bij={};rev={}
        for c,(a,b) in enumerate(cells):
         for sg in (1,-1):
          finalsign=sg*(1 if P>0 else -1)
          bchart=b if sg==1 else -(b+1)
          for isline in (False,True):
           ds=(L.plusline if finalsign==1 else L.minusline) if isline else (L.plus if finalsign==1 else L.minus)
           for idx,actual in ds[a,b].items():
            # global transverse coordinate q*x-sg*P*y; difference from local index
            # is integral, including the shear of the chosen row boundary.
            local=idx-q*a+P*bchart
            predicted=stripe(p,q,c,sg,local,isline)
            assert (predicted is None)==(actual is None)
            if predicted is not None:
                assert bij.setdefault(predicted,actual)==actual
                assert rev.setdefault(actual,predicted)==predicted
            direct_tests+=1
    print(tag,'period',period,'verified',flush=True)
print(totals[0],'complete trees;',totals[1],'certified boxes;',direct_tests,'direct strip/line comparisons')
