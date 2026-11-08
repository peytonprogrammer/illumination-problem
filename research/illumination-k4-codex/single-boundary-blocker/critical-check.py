#!/usr/bin/env python3
"""Prescribed exact cylinder algebra and one analytic six-wall control.

No billiard words, directions, or rooms are discovered or enumerated.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent
counts={}

# The four-winding proof's finite combinatorial ingredient.
independent=[mask for mask in range(16) if not (mask & (mask << 1))]
cover=[]
for m,n in product(independent, repeat=2):
    if m | n == 15:
        cover.append((m,n))
assert cover==[(5,10),(10,5)]
counts['independent_ownership_pairs']=len(independent)**2

n=0
for den in range(2,32):
    for num in range(1,den):
        lam=F(num,den)
        assert ((2*lam).denominator==1) == (lam==F(1,2))
        assert lam.denominator!=1
        n+=1
counts['midpoint_congruence_controls']=n

def between(v,a,b):
    return min(a,b)<v<max(a,b)

def point_hit(a,u,d,v,n,b,L=F(1)):
    if u==v:
        raise ValueError('use core arcs for equal heights')
    q,w=b
    if not between(w,u,v):
        return False
    lam=(w-u)/(v-u)
    return (a+lam*(d-a+n*L)-q) % L==0

def arc_avoids(a,d,u,Z,L=F(1)):
    if (d-a) % L==0:
        return False
    target=(d-a) % L
    blockers=[(q-a) % L for q,w in Z if w==u]
    # Endpoint/blocker coincidence is excluded by the callers.
    return (not any(0<b<target for b in blockers)
            or not any(target<b<L for b in blockers))

def some_prescribed_connection(a,u,d,v,Z):
    if u==v:
        return arc_avoids(a,d,u,Z)
    return any(not any(point_hit(a,u,d,v,n,b) for b in Z) for n in range(4))

# Abstract involution-cylinder charts, not polygon configurations.
# Compare the proposed constructive alternatives with the exact central-core case.
n=0; exceptional=0
for a,d,u,v,q,w in product(
    [F(1,7),F(2,5)], [F(1,6),F(3,8)],
    [F(1,4),F(1,2),F(3,4)], [F(1,4),F(1,2),F(3,4)],
    [F(1,8),F(1,4),F(3,8)], [F(1,4),F(1,2),F(3,4)]):
    Z=[(q,w),((-q) % 1,1-w)]
    target_images=[(d,v),((-d) % 1,1-v)]
    if (a,u) in Z or any(y in Z for y in target_images):
        continue
    found=any(some_prescribed_connection(a,u,yd,yv,Z) for yd,yv in target_images)
    assert found or u==v==w==F(1,2)
    if u==v==w==F(1,2):
        assert found==arc_avoids(a,d,u,Z)
        exceptional+=not found
    n+=1
counts['invariant_cylinder_charts']=n
counts['central_obstructions_within_charts']=int(exceptional)

# Off-center negative control: first target is blocked by two midpoint points,
# but its involution mate is on the source core and avoids both.
a,u,d,v,c=F(0),F(1,4),F(1,3),F(3,4),F(5,6)
Z=[(F(1,6),F(1,2)),(F(2,3),F(1,2))]
assert all(any(point_hit(a,u,d,v,n,b) for b in Z) for n in range(4))
assert ((-Z[0][0]+c) % 1,1-Z[0][1])==Z[1]
y2=((-d+c) % 1,1-v)
assert y2==(F(1,2),F(1,4))
assert arc_avoids(a,y2[0],u,Z)
counts['conjugate_target_negative_control']=1

# Minimal endpoint-transition retracing contradiction: the two one-sided
# choices always create a strictly interior visit to one endpoint.
n=0
for den in range(2,32):
    for num in range(1,den):
        ctime=F(num,den)
        if ctime<F(1,2):
            assert 0<2*ctime<1
        elif ctime>F(1,2):
            assert 0<2*ctime-1<1
        else:
            assert 2*ctime==1  # Forces the same physical endpoint, excluded.
        n+=1
counts['retracing_time_controls']=n

# Fixed analytic six-wall room and prescribed corner-to-corner reflection.
P=[(F(0),F(0)),(F(3),F(0)),(F(3),F(3,2)),
   (F(5,2),F(3,2)),(F(5,2),F(2)),(F(0),F(2))]
c0,c1,z,s,t=P[0],P[1],(F(3,2),F(2)),(F(3,4),F(1)),(F(9,4),F(1))
reflex=(F(5,2),F(3,2))
sub=lambda a,b:(a[0]-b[0],a[1]-b[1])
dot=lambda a,b:a[0]*b[0]+a[1]*b[1]
cross=lambda a,b:a[0]*b[1]-a[1]*b[0]
vin=sub(z,c0);vout=sub(c1,z)
assert (vin[0],-vin[1])==vout
assert s==((c0[0]+z[0])/2,(c0[1]+z[1])/2)
assert t==((z[0]+c1[0])/2,(z[1]+c1[1])/2)
# First leg has x<=3/2. On second leg, x>=5/2 implies y<=2/3.
assert F(3,2)<F(5,2)
assert F(4)-F(4,3)*F(5,2)==F(2,3)<F(3,2)
# Direct bypass has constant y=1 and stays below the notch.
assert s[1]==t[1]==1<F(3,2)
# Exact distance from the only reflex corner to the two legs.
def distance2(p,a,b):
    d=sub(b,a)
    f=max(F(0),min(F(1),dot(sub(p,a),d)/dot(d,d)))
    foot=(a[0]+f*d[0],a[1]+f*d[1])
    return dot(sub(p,foot),sub(p,foot))
dists=[distance2(reflex,c0,z),distance2(reflex,z,c1)]
assert dists==[F(5,4),F(1,4)]
turns=[cross(sub(P[(i+1)%6],P[i]),sub(P[(i+2)%6],P[(i+1)%6])) for i in range(6)]
assert sum(k<0 for k in turns)==1 and all(k!=0 for k in turns)
# The proposed primitive core closes after the two halves. Within each open
# half it uses disjoint copy interiors I/H and V/HV; z has two distinct lifts.
source={F(1,4),F(7,4)}; target={F(3,4),F(5,4)}; block={F(1,2),F(3,2)}
component=lambda q:0 if q<F(1,2) or q>F(3,2) else 1
assert {component(q) for q in source}=={0}
assert {component(q) for q in target}=={1}
assert {(-q) % 2 for q in source}==source
assert {(-q) % 2 for q in target}==target
assert {(-q) % 2 for q in block}==block
# Folding q reproduces all prescribed points without tracing other words.
def fold(v,side):
    q=v % (2*side)
    return q if q<=side else 2*side-q
for qs,expected in [(source,s),(target,t),(block,z)]:
    assert all((fold(3*q,F(3)),fold(4*q,F(2)))==expected for q in qs)
counts['prescribed_six_wall_geometry_control']=1

result={'status':'PASS','checks':counts,
        'scope':'Exact cylinder proof controls and one prescribed non-dark L room; no discovery.',
        'six_wall_control':{'walls':6,'reflex_vertices':1,'genus':2,
                            'minimum_squared_reflex_clearance':str(min(dists)),
                            'direct_bypass':True,'dark':False},
        'global_removal':'OPEN','independent_peer_review':'requested'}
(ROOT/'critical-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
