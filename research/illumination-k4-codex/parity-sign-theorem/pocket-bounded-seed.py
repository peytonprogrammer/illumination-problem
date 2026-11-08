"""Prescribed local fan algebra and two hand-derived segment controls.

No room, trajectory, word, direction, cylinder, or surface discovery.
The finite fan table is a necessary per-vertex table, not a room census.
"""
from fractions import Fraction as F
from math import gcd
from pathlib import Path
import json

base=Path(__file__).resolve().parent
local=[]
equality=[]
for m in range(1,8):
    for q in range(3):
        numerator=m-2+q
        if numerator<0 or numerator%2:
            continue
        outgoing=numerator//2
        charge=3 if m==4 else m
        for incoming in range(3-q):
            degree=incoming+outgoing
            assert charge>=degree
            row=dict(m=m,q=q,incoming=incoming,outgoing=outgoing,
                     degree=degree,charge=charge)
            local.append(row)
            if charge==degree:
                equality.append(row)
assert [(r['m'],r['q'],r['incoming'],r['outgoing']) for r in equality]==[
    (1,1,1,0),(2,0,2,0),(4,0,2,1)]
bridge_upstream=[r for r in local if r['incoming']==r['outgoing']==1]
bridge_downstream=[r for r in local if r['incoming']==2 and r['outgoing']==0]
assert [(r['m'],r['q']) for r in bridge_upstream]==[(3,1),(4,0)]
assert [(r['m'],r['q']) for r in bridge_downstream]==[(2,0)]

# Prescribed contiguous local fans: ring index even=C, odd=B.
# This tests the exact local perpendicular-radius inference only.
perpendicular_controls=[]
for row in bridge_upstream:
    m=row['m']
    for start in range(8):
        endpoints=(start,(start+m)%8)
        if sum(j%2 for j in endpoints)!=row['q']:
            continue
        endpoint_C=[j for j in endpoints if j%2==0]
        internal_C=[(start+j)%8 for j in range(1,m) if (start+j)%2==0]
        assert len(internal_C)==1
        for incoming in endpoint_C:
            outgoing=internal_C[0]
            assert (outgoing-incoming)%8 in (2,6)
            perpendicular_controls.append(dict(m=m,start=start,
                incoming_C=incoming,outgoing_C=outgoing))

# Six FORCED triangles of the turning-bridge proof, not a complete room.
S=(0,0); c=(2,1); T=(4,2)
forced=[(S,(1,0),(1,1)),((2,0),(1,0),(1,1)),
        ((2,0),(2,1),(1,1)),((2,2),(2,1),(3,1)),
        ((2,2),(3,1),(3,2)),(T,(3,2),(3,1))]
def det(a,b):return a[0]*b[1]-a[1]*b[0]
def sub(a,b):return (a[0]-b[0],a[1]-b[1])
def inside(point,tri):
    signs=[det(sub(tri[(i+1)%3],tri[i]),sub(point,tri[i])) for i in range(3)]
    return all(x>=0 for x in signs) or all(x<=0 for x in signs)
# Exact cut parameters from the six prescribed triangle boundaries.
# Every subsegment has both endpoints in its assigned convex triangle.
cuts=[F(0),F(1,4),F(1,3),F(1,2),F(2,3),F(3,4),F(1)]
for i,tri in enumerate(forced):
    for t in (cuts[i],cuts[i+1]):
        assert inside((4*t,2*t),tri)
assert gcd(2,1)==1
assert sub(c,S)==sub(T,c)==(2,1)
assert all((4*t).denominator>1 or (2*t).denominator>1
           for t in cuts[1:-1] if t!=F(1,2))

# Shared-neighbor case: upper-left and upper-right portions of M.
M=(2,0); T_axis=(4,0); T_image=(4,2)
left=[(S,(1,0),(1,1)),(M,(1,0),(1,1)),(M,c,(1,1))]
leftcuts=[F(0),F(1,2),F(2,3),F(1)]
for i,tri in enumerate(left):
    for t in (leftcuts[i],leftcuts[i+1]):
        assert inside((2*t,t),tri)
# Reflect the left triangles across x=2 to check the actual second leg.
right=[tuple((4-x,y) for x,y in tri) for tri in reversed(left)]
rightcuts=[F(0),F(1,3),F(1,2),F(1)]
for i,tri in enumerate(right):
    for t in (rightcuts[i],rightcuts[i+1]):
        assert inside((2+2*t,1-t),tri)
assert sub(c,S)==sub(T_image,c)==(2,1)
assert (T_axis[0],2-T_axis[1])==T_image

out=dict(status='PRESCRIBED_BOUNDED_SEED_CONTROLS_PASS',
    local_degree_rows=len(local),equality_types=equality,
    turning_bridge_upstream_types=bridge_upstream,
    turning_bridge_downstream_types=bridge_downstream,
    perpendicular_controls=len(perpendicular_controls),
    exact_triangle_subsegments=12,
    bounded_claim='Raw strictly simple canonical W<=26 has actual S/T one-C-corner seed',
    proof_scope='Fan-tree and charge deductions require the hand proof; controls do not prove a universal theorem alone.',
    pocket_defect='NOT_ESTABLISHED',unrestricted_seed='OPEN',
    optical_discovery_runs=0,room_enumeration_runs=0)
(base/'pocket-bounded-seed.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
