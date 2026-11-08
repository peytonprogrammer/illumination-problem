"""Independently validate explicit paths using segments and triangle coverage."""
from collections import Counter,defaultdict
from fractions import Fraction as F
from math import gcd
from illumination_geometry import edge

def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def sub(a,b):return a[0]-b[0],a[1]-b[1]
def at(a,b,t):return tuple(a[k]+t*(b[k]-a[k]) for k in (0,1))
def on_segment(p,a,b):
    return cross(sub(p,a),sub(b,a))==0 and all(min(a[k],b[k])<=p[k]<=max(a[k],b[k]) for k in (0,1))
def contained(p,t):
    vals=[cross(sub(t[(i+1)%3],t[i]),sub(p,t[i])) for i in range(3)]
    return all(v>=0 for v in vals) or all(v<=0 for v in vals)
def intersect(a,b,p,q):
    u=sub(b,a);v=sub(q,p);den=cross(u,v)
    if den==0:return None
    s=F(cross(sub(p,a),v),den);t=F(cross(sub(p,a),u),den)
    return s if 0<=s<=1 and 0<=t<=1 else None

def verify(data,witness):
    assert witness['status']=='illuminated'
    ts=[tuple(map(tuple,t)) for t in data['triangles']];counts=Counter(edge(t[i],t[(i+1)%3]) for t in ts for i in range(3));cuts={edge(*e) for e in data.get('slits',[])};walls={e for e,n in counts.items() if n==1}|cuts
    rays=defaultdict(set)
    for a,b in walls:
        for p,q in [(a,b),(b,a)]:
            d=sub(q,p);g=gcd(abs(d[0]),abs(d[1]));rays[p].add((d[0]//g,d[1]//g))
    corners={p for p,ds in rays.items() if len(ds)!=2 or tuple(-v for v in next(iter(ds))) not in ds}
    points=[tuple(F(*v) for v in p) for p in witness['path']]
    assert points[0]==tuple(data['marked'][0]) and points[-1]==tuple(data['marked'][1])
    assert len(points)-2==witness['bounces']
    for a,b in zip(points,points[1:]):
        assert a!=b
        for p in corners:assert not (p!=a and p!=b and on_segment(p,a,b)),('corner crossing',p)
        for p,q in walls:
            t=intersect(a,b,p,q)
            assert t is None or t in (0,1),('wall crossing',a,b,p,q,t)
        times={F(0),F(1)}
        for p,q in counts:
            t=intersect(a,b,p,q)
            if t is not None:times.add(t)
        times=sorted(times)
        for lo,hi in zip(times,times[1:]):
            mid=at(a,b,(lo+hi)/2)
            assert any(contained(mid,t) for t in ts),('outside room',mid)
            assert not any(on_segment(mid,p,q) for p,q in walls),('travel along wall',mid)
    for prev,p,nxt in zip(points,points[1:],points[2:]):
        assert p not in corners,('corner bounce',p)
        hit=[e for e in walls if on_segment(p,*e)];assert hit,('bounce without wall',p)
        tangent=sub(hit[0][1],hit[0][0]);incoming=sub(p,prev);outgoing=sub(nxt,p);dot=sum(incoming[k]*tangent[k] for k in (0,1));norm=sum(v*v for v in tangent)
        reflected=tuple(2*F(dot,norm)*tangent[k]-incoming[k] for k in (0,1))
        assert cross(reflected,outgoing)==0 and sum(reflected[k]*outgoing[k] for k in (0,1))>0,('reflection law',p)
    d=tuple(witness['direction']);first=sub(points[1],points[0]);assert cross(d,first)==0 and sum(d[k]*first[k] for k in (0,1))>0
    return True

if __name__=='__main__':
    import json,sys
    records=json.load(open(sys.argv[1]))['records'];count=0
    for r in records:
        if r['witness']['status']=='illuminated':verify(r['room'],r['witness']);count+=1
    print(json.dumps(dict(independent_paths_verified=count,status='PASS')))
