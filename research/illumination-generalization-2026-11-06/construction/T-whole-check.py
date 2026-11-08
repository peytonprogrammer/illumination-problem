#!/usr/bin/env python3
from fractions import Fraction as F
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent

def cross(u,v):return u[0]*v[1]-u[1]*v[0]
def sub(u,v):return(u[0]-v[0],u[1]-v[1])
def contains_mid(poly,p):
    x,y=p; inside=False
    for a,b in zip(poly,poly[1:]+poly[:1]):
        if cross(sub(p,a),sub(b,a))==0 and min(a[0],b[0])<=x<=max(a[0],b[0]) and min(a[1],b[1])<=y<=max(a[1],b[1]):return False
        if (a[1]>y)!=(b[1]>y):
            xx=a[0]+(y-a[1])*(b[0]-a[0])/(b[1]-a[1])
            if x<xx:inside=not inside
    return inside

def verify(poly,pts):
    poly=[tuple(map(F,p)) for p in poly];pts=[tuple(map(F,p)) for p in pts]
    edges=list(zip(poly,poly[1:]+poly[:1]));contacts=[]
    assert contains_mid(poly,pts[0]) and contains_mid(poly,pts[-1])
    for i,(p,q) in enumerate(zip(pts,pts[1:])):
        d=sub(q,p)
        assert d!=(0,0)
        for a,b in edges:
            e=sub(b,a);den=cross(d,e)
            if den:
                t=cross(sub(a,p),e)/den;u=cross(sub(a,p),d)/den
                assert not(0<t<1 and 0<=u<=1),('interior wall crossing',i,p,q,a,b,t,u)
            elif cross(sub(a,p),d)==0:
                j=0 if d[0] else 1
                t1=(a[j]-p[j])/d[j];t2=(b[j]-p[j])/d[j]
                assert max(min(t1,t2),F(0))>=min(max(t1,t2),F(1)),('wall gliding',i)
        assert contains_mid(poly,((p[0]+q[0])/2,(p[1]+q[1])/2))
    for i,p in enumerate(pts[1:-1],1):
        assert p not in poly,('corner',p)
        touching=[(a,b) for a,b in edges if cross(sub(p,a),sub(b,a))==0 and min(a[0],b[0])<=p[0]<=max(a[0],b[0]) and min(a[1],b[1])<=p[1]<=max(a[1],b[1])]
        assert len(touching)==1
        a,b=touching[0];incoming=sub(p,pts[i-1]);outgoing=sub(pts[i+1],p)
        expected=(-incoming[0],incoming[1]) if a[0]==b[0] else (incoming[0],-incoming[1])
        assert cross(expected,outgoing)==0 and expected[0]*outgoing[0]+expected[1]*outgoing[1]>0,('specular',p)
        contacts.append({'point':list(map(str,p)),'wall':'vertical' if a[0]==b[0] else 'horizontal'})
    return {'segments':len(pts)-1,'contacts':len(contacts),'exact_specular_and_true_finite_wall_guards':'PASS','contact_records':contacts}

poly1=[(4,0),(5,0),(5,1),(10,1),(10,3),(0,3),(0,1),(4,1)]
pts1=[(F(9,2),F(1,2))]+[(F(311-32*j,78),F(3 if j%2==0 else 1)) for j in range(9)]+[(F(1,2),F(2))]
poly2=[(4,0),(5,0),(5,2),(10,2),(10,4),(0,4),(0,1),(4,1)]
pts2=[(F(9),F(21,10))]+[(F(0 if j%2==0 else 5),F(3579-100*j,1790)) for j in range(17)]+[(F(1,2),F(11,10))]
results={'equal_floor_nine':verify(poly1,pts1),'unequal_floor_seventeen_reversed':verify(poly2,pts2)}
r=ROOT.parent/'review'
out={'status':'PASS','kind':'prescribed fixed-witness verification; not discovery or arbitrary-parameter proof','results':results,'source_sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),r/'T-room-theorem.md',r/'uneven-T-theorem.md']},'whole_goal_complete':False}
(ROOT/'T-whole-check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:{'segments':v['segments'],'contacts':v['contacts']} for k,v in results.items()}))
