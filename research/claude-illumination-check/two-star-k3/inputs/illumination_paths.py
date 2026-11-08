"""Exact rational witnesses of illumination; finite misses are not certificates."""
from fractions import Fraction as F
from math import gcd
from illumination_geometry import owners_of,edge,check_fan_angles

def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def sub(a,b):return a[0]-b[0],a[1]-b[1]
def add(a,b):return a[0]+b[0],a[1]+b[1]
def mul(t,a):return t*a[0],t*a[1]
def room(data):
    ts=[tuple(map(tuple,t)) for t in data['triangles']];owners=owners_of(ts);cuts={edge(*e) for e in data.get('slits',[])};opens={e for e,o in owners.items() if len(o)==2 and e not in cuts}
    walls=[e for e in owners if e not in opens];vertices={p for t in ts for p in t};corners=set()
    for p in vertices:
        sizes,full=check_fan_angles(ts,p,owners,opens)
        if not full and any(s!=4 for s in sizes):corners.add(p)
    return walls,corners

def trace(data,direction,max_bounces=1000,prepared=None):
    walls,corners=prepared or room(data);pos=tuple(map(F,data['marked'][0]));target=tuple(map(F,data['marked'][1]));d=tuple(direction);seen=set();path=[pos]
    for bounce in range(max_bounces+1):
        state=(pos,d)
        if state in seen:return dict(status='periodic',bounces=bounce)
        seen.add(state);hits=[];minimum=None
        for e in walls:
            a,b=e;s=sub(b,a);den=cross(d,s)
            if den==0:continue
            t=F(cross(sub(a,pos),s),den);u=F(cross(sub(a,pos),d),den)
            if t>0 and 0<=u<=1:
                if minimum is None or t<minimum:minimum=t;hits=[e]
                elif t==minimum:hits.append(e)
        to=sub(target,pos)
        if cross(to,d)==0:
            k=0 if d[0] else 1;t=F(to[k],d[k])
            if t>0 and (minimum is None or t<minimum):
                path.append(target)
                return dict(status='illuminated',direction=direction,bounces=bounce,path=[[[v.numerator,v.denominator] for v in p] for p in path])
        if minimum is None:return dict(status='escaped',bounces=bounce)
        pos=add(pos,mul(minimum,d));path.append(pos)
        if pos in corners:return dict(status='corner',bounces=bounce,point=[str(v) for v in pos])
        a,b=hits[0];s=sub(b,a);dot=d[0]*s[0]+d[1]*s[1];norm=s[0]**2+s[1]**2
        nd=tuple(F(2*dot*s[k],norm)-d[k] for k in (0,1));assert all(v.denominator==1 for v in nd);d=tuple(map(int,nd))
    return dict(status='limit',bounces=max_bounces)

def directions(bound):
    return sorted([(x,y) for x in range(-bound,bound+1) for y in range(-bound,bound+1) if gcd(abs(x),abs(y))==1],key=lambda p:(max(map(abs,p)),p))
def find_path(data,bound=8,max_bounces=1000):
    prepared=room(data);counts={}
    for i,d in enumerate(directions(bound)):
        r=trace(data,d,max_bounces,prepared);counts[r['status']]=counts.get(r['status'],0)+1
        if r['status']=='illuminated':r.update(directions_tested=i+1,counts=counts);return r
    return dict(status='no_witness_in_direction_bound',direction_bound=bound,counts=counts,directions_tested=sum(counts.values()))

if __name__=='__main__':
    import json,sys
    print(json.dumps(find_path(json.load(open(sys.argv[1])),int(sys.argv[2]) if len(sys.argv)>2 else 8),indent=2))
