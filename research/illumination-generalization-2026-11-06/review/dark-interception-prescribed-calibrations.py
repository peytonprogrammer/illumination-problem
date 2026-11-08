#!/usr/bin/env python3
"""Exact prescribed DI01/DI02 checks only. No search or orbit engine."""
from fractions import Fraction as F
from pathlib import Path
import json
Q0=[(-1,-1),(0,-1),(0,-2),(1,-2),(1,-3),(2,-3),(2,-1),(1,-1),(1,1),(3,1),(3,0),(5,0),(5,1),(4,1),(4,2),(3,2),(3,3),(1,3),(1,2),(0,2),(0,1),(-1,1)]
def sub(a,b):return(a[0]-b[0],a[1]-b[1])
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def first(P,x,w):
    hits=[]
    for i,(a,b) in enumerate(zip(P,P[1:]+P[:1])):
        e=sub(b,a);d=cross(w,e)
        if not d:continue
        t=F(cross(sub(a,x),e),d);u=F(cross(sub(a,x),w),d)
        if t>0 and 0<=u<=1:hits.append((t,i,u,(x[0]+t*w[0],x[1]+t*w[1])))
    m=min(z[0] for z in hits);return [z for z in hits if z[0]==m]
def reflex(P):
    assert sum(cross(a,b) for a,b in zip(P,P[1:]+P[:1]))>0
    return [P[i] for i in range(len(P)) if cross(sub(P[i],P[i-1]),sub(P[(i+1)%len(P)],P[i]))<0]
def interior(P,p):
    count=0
    for a,b in zip(P,P[1:]+P[:1]):
        assert cross(sub(p,a),sub(b,a)) or not(min(a[0],b[0])<=p[0]<=max(a[0],b[0]) and min(a[1],b[1])<=p[1]<=max(a[1],b[1]))
        if (a[1]>p[1])!=(b[1]>p[1]):
            x=F(a[0])+F((p[1]-a[1])*(b[0]-a[0]),b[1]-a[1]);count+=x>p[0]
    return count%2==1
R0=reflex(Q0);assert len(R0)==9 and all((x%2,y%2)!=(0,0) for x,y in R0)
Q100=[(100*x,y) for x,y in Q0];C=(100,-2);S=(0,0);T=(200,2)
assert C in reflex(Q100) and interior(Q100,S) and interior(Q100,T) and interior(Q100,(50,-1))
h=first(Q100,S,(50,-1));assert all(z[0]==2 and z[3]==C for z in h)
L=[(-2,-2),(4,-2),(4,2),(2,2),(2,4),(-2,4)]
A=(0,0);B=(0,2);D=(2,2);u=(1,1);v=(-1,0);w=(0,1)
assert reflex(L)==[D] and interior(L,A) and interior(L,B) and interior(L,(0,1))
assert cross(u,v)==1
for p,direction in [(A,u),(B,(1,0))]:
    h=first(L,p,direction);assert all(z[0]==2 and z[3]==D for z in h)
assert first(L,A,w)[0][0]==4  # Actual target at2 precedes every wall.
out={'status':'PASS_PRESCRIBED_DI01_DI02_CALIBRATIONS','method':'Own exact finitewall arithmetic/turns/interiority, no author checker or discovery','Q0':{'r':9,'reflex_corners':R0,'all_reflex_non_A':True,'time2_shared_A_cone_antecedent_impossible':True},'Q100':{'actual_dark_pair_inherited':{'S':S,'T':T},'primitive_direction':[50,-1],'first_genuine_cone':C,'first_time':2,'time1_transparent_interior':[50,-1],'joint_DI02_chain_not_asserted':True},'lit_six_wall':{'polygon':L,'r':1,'S':A,'T':B,'shared_cone':D,'u':u,'v':v,'first_times':[2,2],'mediant':w,'midpoint':[0,1],'midpoint_regular':True,'actual_target_time':2,'first_wall_after_target_time':4,'necessity_refuted':False},'new_darkness_proof':False,'whole_goal_complete':False}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'prescribed_geometry_checks':3,'new_search':False}))
