"""Exact validation of prescribed equal-depth paths, not ray discovery."""
from fractions import Fraction as F
from pathlib import Path
import importlib.util
import json
import math
import hashlib

BASE = Path(__file__).parent
spec = importlib.util.spec_from_file_location('own_helpers', BASE.parent/'check.py')
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)


def validate(path, a, d=F(1), g=F(1)):
    # All controls use different positive exterior clearances.
    hm,hp = a+g,a+2*g
    polygon = [(0,-hm),(2*d,-hm),(2*d,0),(3*d,0),(3*d,g),
               (2*d,g),(2*d,g+hp),(0,g+hp),(0,g),(d,g),(d,0),(0,0)]
    polygon = [tuple(map(F,P)) for P in polygon]
    edges = list(zip(polygon,polygon[1:]+polygon[:1]))
    assert h.inside(path[0],polygon) and h.inside(path[-1],polygon)
    target=path[-1]
    for i,(A,B) in enumerate(zip(path,path[1:])):
        v=h.sub(B,A)
        assert v!=(0,0)
        assert h.inside(tuple((x+y)/2 for x,y in zip(A,B)),polygon)
        contacts=[]
        for C,D in edges:
            w=h.sub(D,C)
            den=h.cross(v,w)
            if den==0:
                # Check actual collinear overlap, rather than rejecting a
                # parallel supporting line whose wall segment is disjoint.
                if h.cross(h.sub(C,A),v)==0:
                    j=0 if v[0] else 1
                    lo,hi=sorted(((C[j]-A[j])/v[j],(D[j]-A[j])/v[j]))
                    assert hi<=0 or lo>=1
                continue
            tau=h.cross(h.sub(C,A),w)/den
            u=h.cross(h.sub(C,A),v)/den
            if 0<tau<=1 and 0<=u<=1:
                assert tau==1 and 0<u<1, ('earlier wall/corner',i,tau,u)
                contacts.append((C,D))
        if i==len(path)-2:
            assert not contacts
        else:
            assert len(contacts)==1
            C,D=contacts[0]
            reflected=(-v[0],v[1]) if C[0]==D[0] else (v[0],-v[1])
            outgoing=h.sub(path[i+2],B)
            assert h.cross(reflected,outgoing)==0
            assert sum(x*y for x,y in zip(reflected,outgoing))>0
        if i<len(path)-2 and h.cross(h.sub(target,A),v)==0:
            j=0 if v[0] else 1
            tau=(target[j]-A[j])/v[j]
            assert not 0<tau<=1
    return len(path)-2


def choose(p,q,s,t):
    alpha=F(p,q); D=s-t
    def grid(u,sign,lo,hi,c):
        base=(1-alpha)*s+alpha*sign*t+alpha*u
        z=q*(lo-base)/4
        j=z.__floor__()+1
        assert lo<base+F(4*j,q)<hi
        M=(j*pow(p,-1,q))%q
        return u,sign,M,c
    if q==3:
        return 'three'
    if q%2==0:
        if s==t==1:
            if q==4:
                return 'center'
            return grid(2,-1,1,2,1)
        return 0,1,q//2,3
    if q>=9:
        return grid(2,-1,1+D,2,1) if D<F(1,2) else grid(0,-1,2,2+D,3)
    if q==5:
        return 2,-1,1,1 if p==1 else 3
    assert q==7
    if p==2:return 2,-1,5,3
    if p==3:return 2,-1,5,1
    if s<6*t:return 2,-1,3,3
    if 6*s+t>2:return 0,1,3,3
    return 2,1,2,1


def prescribed(p,q,s,t):
    alpha=F(p,q); a=alpha/(1-2*alpha)
    selected=choose(p,q,s,t)
    if selected=='three':
        v=(6-s-t)/5
        ps,pt=s+2*v,t+2*v
        eta=1-(3-ps)/v
        assert 1<s+v<2 and 1<t+v<2
        assert 2<ps<3 and 2<pt<3 and 0<eta<1
        return [(s,-a),(ps,F(1)),(F(3),eta),(pt,F(0)),(t,1+a)],a,selected
    if selected=='center':
        return [(s,-a),(F(5,2),F(1)),(F(3),F(1,2)),(F(5,2),F(0)),(t,1+a)],a,selected
    u,sign,M,c=selected
    L=u+sign*t+4*M
    slope=(L-s)/(2*a+1)
    X=lambda y:s+slope*(y+a)
    e1,e2=X(F(0)),X(F(1))
    fold=lambda x,offset,add=0:add+h.fold(x-offset,F(2))
    deriv=lambda x,offset:1 if (x-offset)%4<2 else -1
    assert fold(e1,0)==fold(e1,c,1) and 1<fold(e1,0)<2
    assert fold(e2,c,1)==fold(e2,u) and 1<fold(e2,u)<2
    assert deriv(e1,0)==deriv(e1,c) and deriv(e2,c)==deriv(e2,u)
    assert fold(L,u)==t
    events=[]
    if slope:
        for ya,yb,offset,add in [(-a,F(0),0,0),(F(0),F(1),c,1),(F(1),1+a,u,0)]:
            lo,hi=sorted((X(ya),X(yb)))
            for j in range(((lo-offset)/2).__floor__()-1,((hi-offset)/2).__floor__()+2):
                x=F(offset+2*j)
                if lo<x<hi:
                    y=-a+(x-s)/slope
                    assert ya<y<yb
                    events.append((fold(x,offset,add),y))
    events.sort(key=lambda P:P[1])
    return [(s,-a)]+events+[(t,1+a)],a,selected


def main():
    pairs=[('1','1'),('1','1/6'),('1/3','1/18'),('1','1/100'),
           ('1/100','1/200'),('1/3','1/100'),('2/5','1/50'),
           ('1','1/2'),('3/4','1/4'),('2/7','2/7')]
    records=[]
    for q in (3,4,5,6,7,8,9,10,11):
        for p in range(1,(q+1)//2):
            if math.gcd(p,q)!=1:continue
            for ss,tt in pairs:
                s,t=F(ss),F(tt)
                path,a,chart=prescribed(p,q,s,t)
                n=validate(path,a)
                # One anisotropic control per prescribed case checks scaling
                # and the exact physical reflection law in actual coordinates.
                d,g=F(2,3),F(5,2)
                scaled=[(x*d,y*g) for x,y in path]
                assert validate(scaled,a*g,d,g)==n
                records.append({'p':p,'q':q,'s':ss,'t':tt,'chart':chart,'contacts':n})
    result={'status':'PASS','prescribed_normalized_cases':len(records),
            'scaled_cases':len(records),'actual_paths_checked':2*len(records),
            'total_wall_contacts':2*sum(r['contacts'] for r in records),
            'max_contacts':max(r['contacts'] for r in records),
            'method':'Prescribed theorem formulas only; exact actual-polygon edge and specular checks',
            'independent_review':False,'records':records}
    (BASE/'physical-check.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='records'}))

if __name__=='__main__':main()
