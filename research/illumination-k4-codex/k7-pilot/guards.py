"""Derive a sufficient whole-unit-square path guard, then audit as triangles."""
from fractions import Fraction as F
from math import floor
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'inputs'))
from guard_check import check as audit
from illumination_geometry import patch


def touching(p):
    xs={floor(p[0])};ys={floor(p[1])}
    if p[0].denominator==1:xs.add(int(p[0])-1)
    if p[1].denominator==1:ys.add(int(p[1])-1)
    return {(x,y) for x in xs for y in ys}

def derive(path,cells,S,T):
    P=[tuple(map(F,p)) for p in path];cells=set(map(tuple,cells));U=set();Z=set()
    for a,b in zip(P,P[1:]):
        cuts={F(0),F(1)}
        for k in (0,1):
            if a[k]==b[k]:continue
            for n in range(floor(min(a[k],b[k])),floor(max(a[k],b[k]))+2):
                t=(n-a[k])/(b[k]-a[k])
                if 0<t<1:cuts.add(t)
        cuts=sorted(cuts)
        points=[tuple(a[k]+t*(b[k]-a[k]) for k in (0,1)) for t in cuts]
        for p in points[1:-1]+[tuple((p[k]+q[k])/2 for k in (0,1)) for p,q in zip(points,points[1:])]:U|=touching(p)
    for p in P[1:-1]:
        for c in touching(p):(U if c in cells else Z).add(c)
    assert U<=cells and not(Z&cells) and not(U&Z)
    def shifted_tris(C):
        return [[[p[0]-S[0],p[1]-S[1]] for p in tri] for x,y in sorted(C) for tri in patch(x,x+1,y,y+1)]
    g={'U':shifted_tris(U),'Z':shifted_tris(Z),'q':[T[0]-S[0],T[1]-S[1]],
       'path':[[[(p[0]-S[0]).numerator,(p[0]-S[0]).denominator],
                [(p[1]-S[1]).numerator,(p[1]-S[1]).denominator]] for p in P]}
    verdict=audit(g);assert verdict=='ok',verdict
    return {'required_unit_cells':sorted(U),'absent_unit_cells':sorted(Z),'triangle_guard':g,'audit':verdict}
