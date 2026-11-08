"""Exact billiard witnesses with sector-aware boundary contacts/slit roots.

A pi-angle boundary sector remains smooth even when another sector at the same
coordinate is a corner. Rays stop at the corner of the sector they approach.
"""
from collections import defaultdict
from fractions import Fraction as F
from math import gcd
from illumination_geometry import owners_of,edge,label
from illumination_cover import reflection,mat
from verify_illumination_paths import cross,sub,on_segment,contained,intersect,at


def enters(t,p,d):
    for a,b,c in [(t[0],t[1],t[2]),(t[1],t[2],t[0]),(t[2],t[0],t[1])]:
        side=cross(sub(b,a),sub(c,a));v=cross(sub(b,a),sub(p,a));w=cross(sub(b,a),d)
        if v*side<0 or v==0 and w*side<0:return False
    return True


def prepare(data):
    ts=[tuple(map(tuple,t)) for t in data['triangles']];owners=owners_of(ts);cuts={edge(*e) for e in data.get('slits',[])};opens={e for e,o in owners.items() if len(o)==2 and e not in cuts};fans={};vertices={p for t in ts for p in t}
    for p in vertices:
        incident={i for i,t in enumerate(ts) if p in t};adj=defaultdict(set)
        for e in opens:
            if p in e:
                a,b=owners[e];adj[a].add(b);adj[b].add(a)
        while incident:
            i=incident.pop();comp={i};todo=[i]
            while todo:
                for j in adj[todo.pop()]:
                    if j in incident:incident.remove(j);comp.add(j);todo.append(j)
            boundaries=[e for e,os in owners.items() if p in e and e not in opens and any(i in comp for i in os)];angle=len(comp)*(2 if label(p)=='C' else 1);full=not boundaries;absorbing=not full and angle!=4
            f=dict(tiles=comp,boundaries=boundaries,full=full,absorbing=absorbing)
            for i in comp:fans[i,p]=f
    return ts,owners,opens,vertices,fans


def trace(data,direction,max_events=100000,prepared=None):
    ts,owners,opens,vertices,fans=prepared or prepare(data);pos=tuple(map(F,data['marked'][0]));target=tuple(map(F,data['marked'][1]));d=tuple(direction);i=next(i for i,t in enumerate(ts) if tuple(data['marked'][0]) in t and enters(t,pos,d));seen=set();path=[pos];events=0
    while events<max_events:
        state=(i,pos,d)
        if state in seen:return dict(status='periodic',events=events)
        seen.add(state);hits=[];minimum=None
        for e in owners_of([ts[i]]):
            a,b=e;s=sub(b,a);den=cross(d,s)
            if den==0:continue
            u=F(cross(sub(a,pos),d),den);t=F(cross(sub(a,pos),s),den)
            if t>0 and 0<=u<=1:
                if minimum is None or t<minimum:minimum=t;hits=[e]
                elif t==minimum:hits.append(e)
        delta=sub(target,pos)
        if cross(delta,d)==0:
            k=0 if d[0] else 1;t=F(delta[k],d[k])
            if t>0 and (minimum is None or t<=minimum):
                path.append(target)
                return dict(status='illuminated',direction=list(direction),bounces=len(path)-2,path=[[[v.numerator,v.denominator] for v in p] for p in path],events=events,corner_convention='occupied-sector')
        assert minimum is not None,('escaped triangle',i,pos,d)
        pos=tuple(pos[k]+minimum*d[k] for k in (0,1));events+=1
        if pos in vertices:
            p=tuple(map(int,pos));fan=fans[i,p]
            if fan['absorbing']:return dict(status='corner',events=events,point=list(p))
            if not fan['full']:
                d=mat(reflection(fan['boundaries'][0]),d);path.append(pos)
            i=next(j for j in fan['tiles'] if enters(ts[j],pos,d))
        else:
            assert len(hits)==1;e=hits[0]
            if e in opens:i=next(j for j in owners[e] if j!=i)
            else:d=mat(reflection(e),d);path.append(pos)
    return dict(status='limit',events=events)


def verify(data,witness):
    """Independent segment/wall validation, not a replay of tile tracing."""
    assert witness['status']=='illuminated';ts,owners,opens,vertices,fans=prepare(data);walls=[e for e in owners if e not in opens];points=[tuple(F(*v) for v in p) for p in witness['path']];assert points[0]==tuple(data['marked'][0]) and points[-1]==tuple(data['marked'][1]);assert len(points)-2==witness['bounces']
    for a,b in zip(points,points[1:]):
        assert a!=b
        for p,q in walls:
            t=intersect(a,b,p,q);assert t is None or t in (0,1),('boundary crossing',a,b,p,q)
        times={F(0),F(1)}
        for p,q in owners:
            t=intersect(a,b,p,q)
            if t is not None:times.add(t)
        times=sorted(times)
        for lo,hi in zip(times,times[1:]):
            mid=at(a,b,(lo+hi)/2);assert any(contained(mid,t) for t in ts);assert not any(on_segment(mid,*e) for e in walls),('travel along boundary',mid)
    for prev,p,nxt in zip(points,points[1:],points[2:]):
        incoming=sub(p,prev);outgoing=sub(nxt,p)
        if p in vertices:
            choices={}
            for i,t in enumerate(ts):
                if p in t and enters(t,p,tuple(-v for v in incoming)):
                    f=fans[i,p];choices[tuple(sorted(f['tiles']))]=f
            assert len(choices)==1,('ambiguous approach',p)
            fan=next(iter(choices.values()));assert not fan['absorbing'] and not fan['full'];assert any(enters(ts[j],p,outgoing) for j in fan['tiles']);line=fan['boundaries'][0]
        else:
            hits=[e for e in walls if on_segment(p,*e)];assert hits;line=hits[0]
        expected=mat(reflection(line),incoming);assert cross(expected,outgoing)==0 and sum(expected[k]*outgoing[k] for k in (0,1))>0,('reflection law',p)
    first=sub(points[1],points[0]);d=witness['direction'];assert cross(first,d)==0 and sum(first[k]*d[k] for k in (0,1))>0
    return True
