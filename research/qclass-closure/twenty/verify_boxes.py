"""Replay the complete bisections with independent physical-row folding and cylinder labels."""
from pathlib import Path
from functools import lru_cache
from fractions import Fraction as F
from math import lcm
import sys
base=Path(__file__).resolve().parent
sys.path.insert(0,str(next(base.parents[1].glob('illumination-generalization*/fable/directions*/d13-cylinder-cover'))))
from cyl import labels
unit=65536
def geometry(d):
    raw=list(map(int,(d/'room').read_text().split()))
    cells=list(zip(raw[2::2],raw[3::2]));C=frozenset(cells)
    def row(c):
        x,y=c;l=x;r=x+1
        while (l-1,y) in C:l-=1
        while (r,y) in C:r+=1
        return l,r
    period=lcm(*(2*(row(c)[1]-row(c)[0]) for c in C))
    @lru_cache(None)
    def direction(p,q):return labels(C,p,q)
    @lru_cache(None)
    def stripe(p,q,c,sg,k,line):
        a,b=cells[c];l,r=row((a,b));w=r-l
        h=F(1,4*(p+q+2));z=F(k) if line else F(2*k+1,2)
        v=(a+(z+p*h)/q-l)%(2*w)
        assert 0<v<2*w and v!=w
        x=l+min(v,2*w-v);y=b+(h if sg==1 else 1-h)
        sign=sg*(1 if v<w else -1);L=direction(p,q)
        t=q*x-sign*p*y
        assert (t.denominator==1)==line
        dictionary=(L.plusline if sign==1 else L.minusline) if line else (L.plus if sign==1 else L.minus)
        return dictionary[x//1,y//1][t//1]
    @lru_cache(None)
    def options(p,q,c,sg,a,b,u,v):
        options=[]
        for k in range(a,b):
            lab=stripe(p,q,c,sg,k,False);options.append(({lab},{lab}))
        for k in range(u,v+1):
            op=stripe(p,q,c,sg,k,True)
            cl={stripe(p,q,c,sg,k-1,False),stripe(p,q,c,sg,k,False)}
            options.append(({op} if op is not None else set(),cl))
        assert options
        return tuple(set.intersection(*(z[i] for z in options)) for i in (0,1))
    return cells,period,options

def verify_axis(d,skip=None,standalone=False):
    if skip is None:skip=set()
    cells,period,options=geometry(d)
    trees=leaves=0
    for f in sorted(d.glob('ends-*')):
      radius=int(f.name.split('-')[1]);tokens=iter((d/f'cert-{radius}').read_text().splitlines())
      for line in f.read_text().splitlines():
       marks=list(map(int,line.split()))
       for main in [0,1]:
        for fixed in [0,1]:
          cap=(unit//8+period-1)//period
          if fixed and radius<cap:continue
          typ=f'{marks[0]} {marks[5]} {main} {fixed}'
          assert next(tokens)==f'R {typ} {radius}'
          if (tuple(marks),radius) in skip:
              while True:
                  token=next(tokens)
                  if token.startswith('END '):
                      assert token.startswith(f'END {typ} ')
                      break
              continue
          rr=radius if fixed else min(radius,cap)
          bounds=[(0,rr)]*4+[(0,0)]*2
          if standalone:bounds[0]=bounds[2]=(0,radius)
          if fixed:bounds[2*main+1]=(unit//8//period,rr)
          else:
              top=max(unit//4,period*rr)
              bounds[4+main]=(unit//8,top);bounds[5-main]=(0,top)
          def visit(z):
              tok=next(tokens).split()
              if tok[0]=='S':
                  i=int(tok[1]);l,r=z[i];m=(l+r)//2;assert l<m<r
                  return sum(visit(z[:i]+[k]+z[i+1:]) for k in ((l,m),(m,r)))
              if tok[0]=='E':
                  assert not fixed and z[5-main][0]>z[4+main][1]
                  return 0
              assert tok[0]=='W'
              j,p,q=map(int,tok[1:]);both=[]
              for e in (0,1):
                  c,x,y,a,b=marks[5*e:5*e+5];sx=1 if a==x else -1;sy=1 if b==y else -1
                  assert (a,b)==cells[c] and x in (a,a+1) and y in (b,b+1)
                  op=set();cl=set()
                  for sg in (1,-1):
                      off=unit*(q*(x-a)-p*(y-b if sg==1 else 1-y+b))
                      terms=[(q*sx,z[2*e])]
                      if fixed:terms.append((-sg*sy*(p+j*q*period),z[2*e+1]))
                      else:terms.extend([(-sg*sy*p,z[2*e+1]),(-sg*sy*q*j,z[4+e])])
                      ranges=[sorted([k*l,k*h]) for k,(l,h) in terms]
                      lo,hi=[off+sum(v[i] for v in ranges) for i in [0,1]]
                      w,w2=options(p,q,c,sg,lo//unit,-(-hi//unit),-(-lo//unit),hi//unit)
                      op.update(w);cl.update(w2)
                  both.append((op,cl))
              assert both[0][0]&both[1][1] or both[1][0]&both[0][1]
              return 1
          n=visit(bounds)
          assert next(tokens)==f'END {typ} 1 {n}'
          trees+=1;leaves+=n
      assert next(tokens,None) is None
    return trees,leaves
if __name__=='__main__':
    for p in map(Path,sys.argv[1:]):print(p,verify_axis(p),flush=True)
