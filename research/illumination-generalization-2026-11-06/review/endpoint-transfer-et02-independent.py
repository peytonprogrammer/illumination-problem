#!/usr/bin/env python3
"""ET02 prescribed 14-wall verification. No search or author-code execution."""
from fractions import Fraction as F
from pathlib import Path
import json

P=[(0,0),(49,0),(49,19),(51,19),(51,0),(80,0),(80,40),
   (40,40),(40,80),(0,80),(0,51),(19,51),(19,49),(0,49)]
P=[tuple(map(F,p)) for p in P]
S=(F(60),F(20)); T=(F(20),F(60)); C=(F(40),F(40))

def sub(a,b): return (a[0]-b[0],a[1]-b[1])
def cross(a,b): return a[0]*b[1]-a[1]*b[0]
def dot(a,b): return a[0]*b[0]+a[1]*b[1]
def at(p,t,v): return (p[0]+t*v[0],p[1]+t*v[1])
def serial(p): return [str(x) for x in p]
E=list(zip(P,P[1:]+P[:1]))
def first(p,v):
    hit=[]
    for i,(a,b) in enumerate(E):
        e=sub(b,a); den=cross(v,e)
        if not den: continue
        t=cross(sub(a,p),e)/den; u=cross(sub(a,p),v)/den
        if t>0 and 0<=u<=1: hit.append((t,i,u,at(p,t,v)))
    m=min(h[0] for h in hit)
    return [h for h in hit if h[0]==m]

# Strict simplicity: nonadjacent closed segments are disjoint, also in
# parallel/collinear cases. This is a finite exact polygon audit.
for i,(a,b) in enumerate(E):
    assert (a[0]==b[0]) != (a[1]==b[1])
    for j,(c,d) in enumerate(E):
        if j<=i or j==i+1 or (i==0 and j==len(E)-1): continue
        e=sub(b,a); f=sub(d,c); den=cross(e,f)
        if den:
            t=cross(sub(c,a),f)/den; u=cross(sub(c,a),e)/den
            assert not (0<=t<=1 and 0<=u<=1), (i,j)
        elif not cross(sub(c,a),e):
            k=0 if e[0] else 1
            assert max(min(a[k],b[k]),min(c[k],d[k]))>min(max(a[k],b[k]),max(c[k],d[k])),(i,j)
area2=sum(cross(a,b) for a,b in E); assert area2>0
turns=[cross(sub(P[i],P[i-1]),sub(P[(i+1)%len(P)],P[i])) for i in range(len(P))]
assert all(turns) and sum(t<0 for t in turns)==5
# Strict interior using exact even/odd horizontal crossing; no vertex shares
# the marks' y coordinates. Both marks are in the respective original arms.
def inside(q):
    n=0
    for a,b in E:
        assert cross(sub(q,a),sub(b,a)) or not (min(a[0],b[0])<=q[0]<=max(a[0],b[0]) and min(a[1],b[1])<=q[1]<=max(a[1],b[1]))
        if (a[1]>q[1])!=(b[1]>q[1]):
            x=a[0]+(q[1]-a[1])*(b[0]-a[0])/(b[1]-a[1])
            n+=x>q[0]
    return n%2==1
assert inside(S) and inside(T)
assert all(v.denominator==1 for p in P for v in p)
assert all(int(v)%2==0 for p in [S,T] for v in p)
h=first(S,sub(T,S)); assert len(h)==2 and all(x[0]==F(1,2) and x[3]==C for x in h)
h=first(T,sub(S,T)); assert len(h)==2 and all(x[0]==F(1,2) and x[3]==C for x in h)

# Exhaust every one-reflection word by its ACTUAL finite wall.
rows=[]
for i,(a,b) in enumerate(E):
    vertical=a[0]==b[0]; k=0 if vertical else 1; c=a[k]
    image=list(T); image[k]=2*c-T[k]; image=tuple(image)
    v=sub(image,S)
    row={'wall':i,'edge':[serial(a),serial(b)],'target_image':serial(image)}
    if not v[k]:
        assert S[k]!=c
        row['rejection']='parallel_to_support'
    else:
        tau=(c-S[k])/v[k]; f=at(S,tau,v)
        row.update({'unfolded_contact_time':str(tau),'contact':serial(f)})
        if not 0<tau<1:
            row['rejection']='nonpositive_first_or_second_flight'
        else:
            other=1-k
            lo,hi=sorted((a[other],b[other]))
            if not lo<f[other]<hi:
                row['rejection']='outside_smooth_finite_wall'
            else:
                incoming=first(S,sub(f,S))
                if not (len(incoming)==1 and incoming[0][0]==1 and incoming[0][1]==i and 0<incoming[0][2]<1):
                    row['rejection']='earlier_incoming_actual_wall'
                    row['first_hit']=[{'wall':x[1],'time':str(x[0]),'point':serial(x[3])} for x in incoming]
                else:
                    outgoing=first(f,sub(T,f))
                    assert outgoing[0][0]<=1
                    row['rejection']='earlier_outgoing_actual_wall'
                    row['first_hit']=[{'wall':x[1],'time':str(x[0]),'point':serial(x[3])} for x in outgoing]
    rows.append(row)
assert len(rows)==14
assert rows[5]['rejection']=='earlier_outgoing_actual_wall'
assert rows[8]['rejection']=='earlier_incoming_actual_wall'

# Prescribed two-reflection path, with all actual walls checked on each leg.
Q1=(F(160,3),F(40)); Q2=(F(40),F(0)); route=[S,Q1,Q2,T]
contacts=[]
for i in range(2):
    h=first(route[i],sub(route[i+1],route[i]))
    assert len(h)==1 and h[0][0]==1 and 0<h[0][2]<1
    wall=h[0][1]; assert wall==[6,0][i]
    incoming=sub(route[i+1],route[i]); outgoing=sub(route[i+2],route[i+1])
    a,b=E[wall]; refl=list(incoming); refl[0 if a[0]==b[0] else 1]*=-1
    assert cross(refl,outgoing)==0 and dot(refl,outgoing)>0
    # Actual target is not reached along an earlier leg.
    assert cross(sub(T,route[i]),incoming)!=0
    contacts.append({'wall':wall,'point':serial(route[i+1]),'positive_speed_scale':str(outgoing[0]/refl[0])})
assert first(Q2,sub(T,Q2))[0][0]>1
out={'status':'PASS_PRESCRIBED_ET02_INDEPENDENT_AUDIT','method':'Own rational polygon intersection audit, exhaustive 14 finite actual mirrors, and two prescribed physical reflections','polygon':[serial(p) for p in P],'area':str(area2/2),'r':5,'walls':14,'actual_even_even_marks':[serial(S),serial(T)],'singular_direct_chord':serial(C),'one_reflection_rows':rows,'one_reflection_path_exists':False,'two_reflection_path':[serial(p) for p in route],'contacts':contacts,'actual_pair_lit':True,'universal_one_reflection_availability':'REJECTED_BY_THIS_R5_ROOM','all_multi_reflection_transfer_rejected':False,'nine_distinct_corner_bound_proved':False,'whole_goal_complete':False}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'r':5,'walls':14,'one_reflection_words_checked':len(rows),'actual_pair_lit':True}))
