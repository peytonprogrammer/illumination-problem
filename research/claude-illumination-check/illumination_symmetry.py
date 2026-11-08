"""Exact square-lattice symmetries preserving a patch and unordered marks."""
from fractions import Fraction as F
from math import gcd,lcm

def orbit(data,witness):
    source,target=map(tuple,data['marked'])
    assert source==(0,0) and all(v%2==0 for v in target)
    points=[tuple(F(*v) for v in p) for p in witness['path']]
    bounds=data['search']['bounds'];x0,x1,y0,y1=bounds
    corners={(x0,y0),(x0,y1),(x1,y0),(x1,y1)}
    for permute in (False,True):
        for sx in (1,-1):
            for sy in (1,-1):
                for swap in (False,True):
                    shift=target if swap else source
                    def transform(p):
                        a,b=p[::-1] if permute else p
                        return (sx*a+shift[0],sy*b+shift[1])
                    if transform(target)!=(source if swap else target):continue
                    if {transform(p) for p in corners}!=corners:continue
                    triangles=[tuple(sorted(transform(tuple(p)) for p in t)) for t in data['triangles']]
                    slits=[tuple(sorted(transform(tuple(p)) for p in e)) for e in data['slits']]
                    path=[transform(p) for p in (points[::-1] if swap else points)]
                    d=tuple(path[1][k]-path[0][k] for k in (0,1));den=lcm(*(v.denominator for v in d));direction=[int(v*den) for v in d];g=gcd(*map(abs,direction));direction=[v//g for v in direction]
                    changed=dict(data,triangles=triangles,slits=slits)
                    ray=dict(witness,direction=direction,path=[[[v.numerator,v.denominator] for v in p] for p in path],derived_symmetry=dict(swap=swap,permute=permute,sx=sx,sy=sy))
                    yield changed,ray
