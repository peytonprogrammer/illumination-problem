"""Exact prescribed corner-reversal removals, not discovery or corner traversal."""
from pathlib import Path
from fractions import Fraction as F
import json
B=Path(__file__).parent

def fold(x):
    r=x%4;return r if r<=2 else 4-r

def sub(A,B):return tuple(x-y for x,y in zip(A,B))
def cross(v,w):return v[0]*w[1]-v[1]*w[0]
def inside(P,poly):
    x,y=P;count=0
    for C,D in zip(poly,poly[1:]+poly[:1]):
        if cross(sub(P,C),sub(D,C))==0 and all(min(c,d)<=p<=max(c,d) for c,d,p in zip(C,D,P)):return False
        if (C[1]>y)!=(D[1]>y):count+=C[0]+(y-C[1])*(D[0]-C[0])/(D[1]-C[1])>x
    return count%2==1

def validate(path,a,b,hm,hp,d=F(1),g=F(1)):
    poly=[(0,-hm),(2*d,-hm),(2*d,0),(3*d,0),(3*d,g),(2*d,g),
          (2*d,g+hp),(0,g+hp),(0,g),(d,g),(d,0),(0,0)]
    poly=[tuple(map(F,P)) for P in poly]
    assert path[0][1]==-a and path[-1][1]==g+b
    assert inside(path[0],poly) and inside(path[-1],poly)
    for i,(C,D) in enumerate(zip(path,path[1:])):
        v=sub(D,C);assert v!=(0,0)
        assert inside(tuple((x+y)/2 for x,y in zip(C,D)),poly)
        hits=[]
        for E,G in zip(poly,poly[1:]+poly[:1]):
            w=sub(G,E);det=cross(v,w)
            if not det:
                if cross(sub(E,C),v)==0:
                    j=0 if v[0] else 1;lo,hi=sorted(((E[j]-C[j])/v[j],(G[j]-C[j])/v[j]));assert hi<=0 or lo>=1
                continue
            t=cross(sub(E,C),w)/det;u=cross(sub(E,C),v)/det
            if 0<t<=1 and 0<=u<=1:
                assert t==1 and 0<u<1,('illegal retained contact',i,t,u)
                hits.append((E,G))
        if i==len(path)-2:assert not hits
        else:
            assert len(hits)==1
            E,G=hits[0];r=(-v[0],v[1]) if E[0]==G[0] else (v[0],-v[1]);out=sub(path[i+2],D)
            assert cross(r,out)==0 and sum(x*y for x,y in zip(r,out))>0
    return len(path)-2

def construct(fixture):
    s,t,a,b,hm,hp=map(F,fixture[:6]);lc,uc,u,eps,M,c=fixture[6:]
    A=2*hm-a if lc else a;C=2*hp-b if uc else b;H=A+1+C
    L=u+eps*t+4*M;v=(L-s)/H;X=lambda z:s+v*(z+A)
    boxes={(0,1):((1,2),(1,2)),(0,3):((2,3),(2,3)),(2,1):((1,2),(0,1)),(2,3):((2,3),(3,4))}
    for e,I in zip((X(F(0))%4,X(F(1))%4),boxes[u,c]):assert I[0]<e<I[1]
    cl=bool(lc and X(-hm)%2==0);cu=bool(uc and (X(1+hp)-u)%2==0)
    assert cl or cu
    start=-a if cl else -A;end=1+b if cu else 1+C
    Y=lambda z:-2*hm-z if lc and z<-hm else 2*(1+hp)-z if uc and z>1+hp else z
    assert fold(X(start))==s and Y(start)==-a
    assert fold(X(end)-u)==t and Y(end)==1+b
    events=[]
    for za,zb,offset,add in [(-A,F(0),0,0),(F(0),F(1),c,1),(F(1),1+C,u,0)]:
        za,zb=max(za,start),min(zb,end)
        if za>=zb:continue
        lo,hi=sorted((X(za),X(zb)))
        for j in range(((lo-offset)/2).__floor__()-1,((hi-offset)/2).__floor__()+2):
            x=F(offset+2*j)
            if lo<x<hi:
                z=-A+(x-s)/v;assert za<z<zb
                events.append((z,add+fold(x-offset)))
    if lc and start<-hm<end:
        assert not cl;events.append((-hm,fold(X(-hm))))
    if uc and start<1+hp<end:
        assert not cu;events.append((1+hp,fold(X(1+hp)-u)))
    events.sort();path=[(s,-a)]+[(x,Y(z)) for z,x in events]+[(t,1+b)]
    target=path[-1]
    for i,(C0,D0) in enumerate(zip(path,path[1:])):
        w=sub(D0,C0)
        if cross(sub(target,C0),w)==0:
            j=0 if w[0] else 1;tau=(target[j]-C0[j])/w[j]
            if 0<tau<=1:
                path=path[:i+1]+[target];break
    assert len(path)>=2
    return path,(a,b,hm,hp),{'lower_corner_removed':cl,'upper_corner_removed':cu,'retained_virtual_interval':[str(start),str(end)]}

def main():
    fixtures=[('1','1','1','3','2','11/2',0,1,0,1,1,1),
              ('1','1','3','1','11/2','2',1,0,0,1,-1,1),
              ('1','1','1','1','7/4','7/4',1,1,2,-1,-2,1),
              ('3/2','5/4','1','1','7','16',1,1,0,1,1,3)]
    records=[]
    for fixture in fixtures:
        path,params,detail=construct(fixture);a,b,hm,hp=params
        n=validate(path,*params)
        d,g=F(2,3),F(5,2);scaled=[(x*d,y*g) for x,y in path]
        assert validate(scaled,a*g,b*g,hm*g,hp*g,d,g)==n
        rev=[(x,1-y) for x,y in reversed(path)]
        assert validate(rev,b,a,hp,hm)==n
        records.append({'fixture':list(fixture),'contacts_after_removal':n,'path':[[str(x),str(y)] for x,y in path],**detail})
    out={'status':'PASS','prescribed_formal_corner_fixtures':len(fixtures),'actual_retained_paths':3*len(fixtures),
         'total_retained_wall_contacts':3*sum(r['contacts_after_removal'] for r in records),
         'method':'Exact formal symmetry, retained interval only, all actual edges and smooth specular contacts; includes both corners and zero-contact remainder',
         'independent_review':False,'records':records}
    (B/'corner-removal-check.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out))
if __name__=='__main__':main()
