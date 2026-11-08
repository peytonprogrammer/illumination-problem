#!/usr/bin/env python3
"""Independent Fraction replay of prescribed section/matching controls; no search."""
from fractions import Fraction as F
from pathlib import Path
import json

Q=[(0,0),(8,0),(8,8),(0,8)]
def pt(x): return tuple(F(v) for v in x)
def cross(a,b): return a[0]*b[1]-a[1]*b[0]
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def scale(t,a): return tuple(t*x for x in a)
def first_boundary(p,v,poly=Q):
    hits=[]
    for i,(a,b) in enumerate(zip(poly,poly[1:]+poly[:1])):
        a,b=pt(a),pt(b); e=sub(b,a); den=cross(v,e)
        if not den: continue
        t=cross(sub(a,p),e)/den; u=cross(sub(a,p),v)/den
        if t>0 and 0<=u<=1: hits.append((t,i,u,add(p,scale(t,v))))
    if not hits: return None
    t=min(h[0] for h in hits)
    return [h for h in hits if h[0]==t]
def path(points,bounces):
    points=[pt(p) for p in points]; contacts=[]
    for j,(a,b) in enumerate(zip(points,points[1:])):
        v=sub(b,a); hits=first_boundary(a,v)
        if j<len(bounces):
            assert hits and hits[0][0]==1
            assert len(hits)==1 and 0<hits[0][2]<1
            wall=hits[0][1]; assert wall==bounces[j]
            outgoing=sub(points[j+2],b)
            reflected=(v[0],-v[1]) if wall in (0,2) else (-v[0],v[1])
            assert cross(reflected,outgoing)==0
            assert sum(x*y for x,y in zip(reflected,outgoing))>0
            contacts.append({'wall':wall,'point':[str(x) for x in b]})
        else:
            assert not hits or hits[0][0]>1
    return contacts

def scattering(c,z,cprime,m,e,v):
    L=e[0]*cprime+v[0]-c
    assert L>0
    return L,e[1]*(z+m*L-v[1]),(e[0],e[1]*m)

one=path([(3,2),(8,F(13,4)),(3,F(9,2))],[1])
two=path([(3,2),(8,F(13,4)),(0,F(21,4)),(3,6)],[1,3])
assert scattering(F(3),F(2),F(3),F(1,4),(-1,1),(16,0))==(10,F(9,2),(-1,F(1,4)))
assert scattering(F(3),F(2),F(3),F(1,4),(1,1),(16,0))==(16,F(6),(1,F(1,4)))
# Actual target equality via two prescribed compatible section graphs.
m=F(4); C=F(3)
z_source=F(2)+m*(C-2)
z_target=F(10)+m*(C-4)
assert z_source==z_target==6
bounce=path([(2,2),(F(7,2),8),(4,6)],[2])
# Algebraic target root with illegal simultaneous top/right contact.
S=pt((2,2)); image=pt((10,10)); v=sub(image,S)
assert v[1]/v[0]==1
hit=first_boundary(S,v)
assert len(hit)==2 and {h[1] for h in hit}=={1,2}
assert all(h[3]==(8,8) and h[2] in (0,1) for h in hit)
direct=path([(2,2),(6,6)],[])
result={
 'status':'PASS_PRESCRIBED_EXACT_CONTROLS',
 'method':'Independent rational segment/wall intersections and positive proportionality, no author imports or search',
 'single_vertical_reflection':{'contacts':one,'return':['3','9/2'],'velocity':['-1','1/4'],'identical_state':False},
 'two_vertical_reflections':{'contacts':two,'return':['3','6'],'velocity':['1','1/4'],'identical_state':False},
 'legal_matching_root':{'slope':'4','section':['3','6'],'target':['4','6'],'contacts':bounce},
 'illegal_matching_root':{'slope':'1','unfolded_target':['10','10'],'collision':['8','8'],'simultaneous_walls':[1,2],'selected_word_legal':False,'actual_pair_directly_lit':True},
 'whole_goal_complete':False,
}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
