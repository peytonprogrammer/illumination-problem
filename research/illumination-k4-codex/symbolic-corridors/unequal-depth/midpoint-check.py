"""Prescribed two-reflection formula, exact actual-wall controls only."""
from fractions import Fraction as F
from pathlib import Path
import json
BASE=Path(__file__).parent

def sub(A,B):return tuple(x-y for x,y in zip(A,B))
def cross(v,w):return v[0]*w[1]-v[1]*w[0]
def inside(P,poly):
    x,y=P;count=0
    for A,B in zip(poly,poly[1:]+poly[:1]):
        if cross(sub(P,A),sub(B,A))==0 and all(min(a,b)<=p<=max(a,b) for a,b,p in zip(A,B,P)):return False
        if (A[1]>y)!=(B[1]>y):count+=A[0]+(y-A[1])*(B[0]-A[0])/(B[1]-A[1])>x
    return count%2==1

def check(d,g,a,hm,hp):
    b=a+g;h=hp
    P=[(0,-hm),(2*d,-hm),(2*d,0),(3*d,0),(3*d,g),(2*d,g),
       (2*d,g+hp),(0,g+hp),(0,g),(d,g),(d,0),(0,0)]
    P=[tuple(map(F,p)) for p in P]
    path=[(d,-a),(2*d,h-a),(2*d-d*b/h,g+h),(d,g+b)]
    assert hm>a and hp>b and all(inside(p,P) for p in (path[0],path[-1]))
    for i,(A,B) in enumerate(zip(path,path[1:])):
        v=sub(B,A);assert v!=(0,0)
        assert inside(tuple((x+y)/2 for x,y in zip(A,B)),P)
        hits=[]
        for C,D in zip(P,P[1:]+P[:1]):
            w=sub(D,C);den=cross(v,w)
            if not den:
                if cross(sub(C,A),v)==0:
                    j=0 if v[0] else 1
                    lo,hi=sorted(((C[j]-A[j])/v[j],(D[j]-A[j])/v[j]))
                    assert hi<=0 or lo>=1
                continue
            t=cross(sub(C,A),w)/den;u=cross(sub(C,A),v)/den
            if 0<t<=1 and 0<=u<=1:
                assert t==1 and 0<u<1
                hits.append((C,D))
        if i==2:assert not hits
        else:
            assert len(hits)==1
            C,D=hits[0]
            r=(-v[0],v[1]) if C[0]==D[0] else (v[0],-v[1])
            out=sub(path[i+2],B)
            assert cross(r,out)==0 and sum(x*y for x,y in zip(r,out))>0
        if i<2 and cross(sub(path[-1],A),v)==0:
            j=0 if v[0] else 1;assert not 0<(path[-1][j]-A[j])/v[j]<=1
    return {'d':str(d),'g':str(g),'a':str(a),'h_minus':str(hm),'h_plus':str(hp),'contacts':2}

if __name__=='__main__':
    cases=[check(d,g,a,a+low,a+g+up)
           for d,g in ((F(1),F(1)),(F(2,3),F(5,2)))
           for a in map(F,('1/100','1/2','1','10','100'))
           for low in map(F,('1/1000','2'))
           for up in map(F,('1/1000','1','100'))]
    result={'status':'PASS','actual_paths':len(cases),'wall_contacts':2*len(cases),
            'scope':'Prescribed two-reflection centered b=a+g construction, exact polygon edges',
            'independent_review':False,'records':cases}
    (BASE/'midpoint-check.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='records'}))
