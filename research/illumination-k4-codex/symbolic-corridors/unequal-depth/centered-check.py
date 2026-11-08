"""Finite prescribed rational proof table for the centered Fourier reduction."""
from fractions import Fraction as F
from math import gcd
from pathlib import Path
import json
B=Path(__file__).parent

def cos_sign(x):
    r=x%2
    return 0 if r in (F(1,2),F(3,2)) else 1 if r<F(1,2) or r>F(3,2) else -1

def positive(n,alpha,beta):
    return (n*alpha)%1!=0 and (n*beta)%1!=0 and cos_sign(n*alpha)*cos_sign(n*beta)>0

def fold(x):
    r=x%4
    return r if r<=2 else 4-r

def sub(A,B):return tuple(x-y for x,y in zip(A,B))
def cross(v,w):return v[0]*w[1]-v[1]*w[0]
def inside(P,poly):
    x,y=P;count=0
    for A,B in zip(poly,poly[1:]+poly[:1]):
        if cross(sub(P,A),sub(B,A))==0 and all(min(a,b)<=p<=max(a,b) for a,b,p in zip(A,B,P)):return False
        if (A[1]>y)!=(B[1]>y):count+=A[0]+(y-A[1])*(B[0]-A[0])/(B[1]-A[1])>x
    return count%2==1

def validate(path,a,b,d=F(1),g=F(1)):
    hm,hp=a+g,b+2*g
    P=[(0,-hm),(2*d,-hm),(2*d,0),(3*d,0),(3*d,g),(2*d,g),
       (2*d,g+hp),(0,g+hp),(0,g),(d,g),(d,0),(0,0)]
    P=[tuple(map(F,p)) for p in P]
    assert path[0]==(d,-a) and path[-1]==(d,g+b)
    assert inside(path[0],P) and inside(path[-1],P)
    for i,(A,Bb) in enumerate(zip(path,path[1:])):
        v=sub(Bb,A);assert v!=(0,0)
        assert inside(tuple((x+y)/2 for x,y in zip(A,Bb)),P)
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
        if i==len(path)-2:assert not hits
        else:
            assert len(hits)==1
            C,D=hits[0]
            r=(-v[0],v[1]) if C[0]==D[0] else (v[0],-v[1])
            out=sub(path[i+2],Bb)
            assert cross(r,out)==0 and sum(x*y for x,y in zip(r,out))>0
        if i<len(path)-2 and cross(sub(path[-1],A),v)==0:
            j=0 if v[0] else 1;assert not 0<(path[-1][j]-A[j])/v[j]<=1
    return len(path)-2

def chart_path(alpha,beta,n,c,u):
    H=1/(beta-alpha);a=alpha*H;b=(1-beta)*H
    v=2*n/H
    assert v
    X=lambda y:1+v*(y+a)
    events=[]
    for ya,yb,offset,add in [(-a,F(0),0,0),(F(0),F(1),c,1),(F(1),1+b,u,0)]:
        lo,hi=sorted((X(ya),X(yb)))
        for j in range(((lo-offset)/2).__floor__()-1,((hi-offset)/2).__floor__()+2):
            x=F(offset+2*j)
            if lo<x<hi:
                y=-a+(x-1)/v
                assert ya<y<yb
                events.append((add+fold(x-offset),y))
    events.sort(key=lambda P:P[1])
    return [(F(1),-a)]+events+[(F(1),1+b)],a,b

def main():
    rows=[];failures=set()
    for q in range(2,13):
      for p in range(1,q):
        if gcd(p,q)!=1:continue
        theta=F(p,q)
        for line in ('beta=3alpha','3alpha+beta=2','alpha+3beta=2','3beta-alpha=2'):
            alpha,beta={'beta=3alpha':(theta,3*theta),
                        '3alpha+beta=2':(theta,2-3*theta),
                        'alpha+3beta=2':(2-3*theta,theta),
                        '3beta-alpha=2':(3*theta-2,theta)}[line]
            if not 0<alpha<beta<1 or F(1,2) in (alpha,beta):continue
            # On each line the two trig factors reduce exactly to theta,3theta.
            assert all(positive(n,alpha,beta)==positive(n,theta,3*theta) for n in range(2*q))
            n=next((n for n in range(2*q) if positive(n,alpha,beta)),None)
            if n is None:failures.add((alpha,beta))
            rows.append({'line':line,'p':p,'q':q,'alpha':str(alpha),'beta':str(beta),'witness_n':n})
    expected={(F(1,4),F(3,4)),(F(1,5),F(3,5)),(F(2,5),F(4,5))}
    assert failures==expected
    # Explicit vertical chart selection for every finite successful row.
    for r in rows:
        n=r['witness_n']
        if n is None:continue
        alpha,beta=F(r['alpha']),F(r['beta'])
        if not 1<(1+2*n*alpha)%4<3:n=-n
        e1,e2=(1+2*n*alpha)%4,(1+2*n*beta)%4
        c=1 if 1<e1<2 else 3
        assert 1<e1<3 and e1!=2
        if c==1:
            assert 0<e2<2 and e2!=1
            u=2 if e2<1 else 0
        else:
            assert 2<e2<4 and e2!=3
            u=0 if e2<3 else 2
        assert abs(((1+2*n-u)%4)-2)==1 # F2(L-u)=1
        r['signed_n']=n;r['middle_shift']=c;r['upper_shift']=u
    special=[]
    for a,b in [(F(1,2),F(1,2)),(F(1,2),F(1)),(F(1),F(1,2))]:
        v=4/(a+b+3);e=1+a*v;f=1+b*v;ps=e+v;pt=f+v
        eta=1-(3-ps)/v
        assert 1<e<2 and 1<f<2 and 2<ps<3 and 2<pt<3 and 0<eta<1
        assert ps+pt+v==6
        special.append({'a':str(a),'b':str(b),'v':str(v),'e':str(e),'f':str(f),
                        'p_s':str(ps),'p_t':str(pt),'eta':str(eta)})
    physical=[]
    for r in rows:
        if r['witness_n'] is None:continue
        path,a,b=chart_path(F(r['alpha']),F(r['beta']),r['signed_n'],r['middle_shift'],r['upper_shift'])
        num=validate(path,a,b)
        d,g=F(2,3),F(5,2)
        assert validate([(x*d,y*g) for x,y in path],a*g,b*g,d,g)==num
        physical.append({'kind':'prescribed table chart','alpha':r['alpha'],'beta':r['beta'],'contacts':num})
    for r in special:
        a,b=F(r['a']),F(r['b'])
        path=[(F(1),-a),(F(r['p_s']),F(1)),(F(3),F(r['eta'])),(F(r['p_t']),F(0)),(F(1),1+b)]
        num=validate(path,a,b)
        d,g=F(2,3),F(5,2)
        assert validate([(x*d,y*g) for x,y in path],a*g,b*g,d,g)==num
        physical.append({'kind':'isolated three-contact repair','a':str(a),'b':str(b),'contacts':num})
    out={'physical_paths':2*len(physical),'wall_contacts':2*sum(r['contacts'] for r in physical),'physical_records':physical,'status':'PASS','finite_rows':len(rows),'exceptional_phase_pairs':[list(map(str,p)) for p in sorted(failures)],
         'three_reflection_repairs':special,'rows':rows,
         'scope':'Exact sign residues and chart/guard identities after HAND finite reduction; not discovery extrapolation',
         'independent_review':False}
    (B/'centered-check.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('rows','physical_records')}))
if __name__=='__main__':main()
