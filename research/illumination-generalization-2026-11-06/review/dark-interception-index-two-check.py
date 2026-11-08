#!/usr/bin/env python3
"""Prescribed Q0 and transported Q100 boundary checks; no room/direction search."""
from fractions import Fraction as F
from pathlib import Path
import json
P=[(-1,-1),(0,-1),(0,-2),(1,-2),(1,-3),(2,-3),(2,-1),(1,-1),(1,1),(3,1),(3,0),(5,0),(5,1),(4,1),(4,2),(3,2),(3,3),(1,3),(1,2),(0,2),(0,1),(-1,1)]
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def sub(a,b):return(a[0]-b[0],a[1]-b[1])
def boundary_events(poly,start,direction):
    events=[]
    for a,b in zip(poly,poly[1:]+poly[:1]):
        edge=sub(b,a);q=sub(a,start);den=cross(direction,edge)
        if den:
            time=F(cross(q,edge),den);side=F(cross(q,direction),den)
            if time>0 and 0<=side<=1:events.append(time)
        elif cross(q,direction)==0:
            axis=0 if direction[0] else 1
            ta=F(a[axis]-start[axis],direction[axis]);tb=F(b[axis]-start[axis],direction[axis])
            lo,hi=sorted([ta,tb])
            if hi>0:
                assert lo>0, 'Initial positive interval lies on boundary'
                events.append(lo)
    return sorted(set(events))
def inside(poly,p):
    result=False
    for a,b in zip(poly,poly[1:]+poly[:1]):
        if cross(sub(p,a),sub(b,a))==0 and min(a[0],b[0])<=p[0]<=max(a[0],b[0]) and min(a[1],b[1])<=p[1]<=max(a[1],b[1]):return False
        if (a[1]>p[1])!=(b[1]>p[1]):
            xx=F(a[0])+F((p[1]-a[1])*(b[0]-a[0]),b[1]-a[1])
            if xx>p[0]:result=not result
    return result
records=[]
for stretch in [1,100]:
    poly=[(stretch*x,y) for x,y in P]
    S=(0,0);T=(2*stretch,2);C=(0,1);D=(stretch,1)
    u=(0,1);v=(2*stretch,1);w=(stretch,1)
    # Each first hit is a genuine reflex corner; exact first intersection plus
    # one interior point certifies the whole open straight leg by Jordan separation.
    for start,direction,corner in [(S,u,C),(T,(-v[0],-v[1]),C),(S,w,D)]:
        events=boundary_events(poly,start,direction)
        assert events[0]==1 and tuple(start[j]+direction[j] for j in range(2))==corner
        assert inside(poly,tuple(F(start[j])+F(direction[j],2) for j in range(2)))
        i=poly.index(corner)
        assert cross(sub(corner,poly[i-1]),sub(poly[(i+1)%len(poly)],corner))<0
    assert inside(poly,S) and inside(poly,T)
    assert cross(u,w)==-stretch and cross(u,v)==-2*stretch
    # At C the missing physical quadrant is northwest. The narrow CCW angle
    # from the downward source germ to outgoing v lies through southeast.
    i=poly.index(C)
    assert sub(poly[i-1],C)==(0,1) and sub(poly[(i+1)%len(poly)],C)==(-stretch,0)
    assert cross((0,-1),v)>0 and inside(poly,(F(stretch,10),F(9,10)))
    records.append({'stretch':stretch,'S':S,'T':T,'shared_corner':C,'forced_corner':D,'u':u,'v':v,'w':w,'first_times':[1,1,1],'narrow_sector_verified':True,'normalized_neighbor_determinant':-1,'fixed_unit_neighbor_determinant':-stretch,'corner_parities_in_transported_lattice':[[0,1],[1,1]],'darkness_inherited_not_reproved':True})
# Canonical unimodular-basis triangle: (0,0),(1,0),(0,2).
points=[(x,y) for x in range(2) for y in range(3) if 2*x+y<=2]
assert points==[(0,0),(0,1),(0,2),(1,0)]
result={'status':'PASS','method':'Exact rational segment/edge intersections including collinearity; direct physical sectors; finite prescribed lattice triangle','controls':records,'triangle_lattice_points':points,'search_used':False,'whole_goal_complete':False}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','prescribed_controls':2,'triangle_points':len(points),'search_used':False}))
