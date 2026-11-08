"""Local geometric facts sufficient to preserve an exact connecting ray."""
from fractions import Fraction as F
from verify_illumination_paths import intersect,on_segment,at,contained,cross,sub

def path_facts(ts,owners,shared,witness,selected,opened):
    facts={};points=[tuple(F(*v) for v in p) for p in witness['path']];vertices={p for t in ts for p in t}
    def tile(i):assert selected[i]==1;facts[('tile',i)]=1
    def opening(e,value):
        if e in shared:
            assert opened[e]==value;facts[('open',e)]=value
        else:assert value==0
    for a,b in zip(points,points[1:]):
        times={F(0),F(1)}
        for e in owners:
            t=intersect(a,b,*e)
            if t is not None:
                times.add(t)
                if 0<t<1:
                    p=at(a,b,t)
                    if p not in vertices:opening(e,1)
        times=sorted(times)
        for lo,hi in zip(times,times[1:]):
            p=at(a,b,(lo+hi)/2);support=[i for i,t in enumerate(ts) if contained(p,t)]
            assert support
            for i in support:tile(i)
            for e in owners:
                if on_segment(p,*e):opening(e,1)
        # Every visited lattice vertex keeps its complete incident geometry.
        for p in vertices:
            if not on_segment(p,a,b):continue
            for i,t in enumerate(ts):
                if p in t:facts[('tile',i)]=selected[i]
            for e in shared:
                if p in e:facts[('open',e)]=opened[e]
    for p in points[1:-1]:
        for e in owners:
            if on_segment(p,*e) and (e not in shared or opened[e]==0):opening(e,0)
    return facts
