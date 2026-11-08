"""Independent fixed horizontal-shear controls and exact nearest-wall tracer.
No peer executable imports or candidate/direction discovery.
"""
from fractions import Fraction as F
from pathlib import Path
from math import gcd,lcm
from importlib.util import spec_from_file_location,module_from_spec
import hashlib,json
HERE=Path(__file__).resolve().parent;BASE=HERE.parent
sp=spec_from_file_location('own_exact_geometry',BASE/'arbitrary-endpoints-independent/check.py')
G=module_from_spec(sp);sp.loader.exec_module(G)
def rgcd(xs):
    Q=lcm(*(x.denominator for x in xs));return F(gcd(*(int(Q*x) for x in xs)),Q)
def fold(x):return G.fold(x,F(2))
def v2(n):
    k=0
    while n%2==0:n//=2;k+=1
    return k

def prefix(path):
    T=path[-1]
    for i,(a,b) in enumerate(zip(path,path[1:])):
        w=G.sub(b,a)
        if G.cross(G.sub(T,a),w)==0:
            j=0 if w[0] else 1;q=(T[j]-a[j])/w[j]
            if 0<q<=1:return path[:i+1]+[T]
    raise AssertionError('no target')

def trace(params,velocity):
    s,t,a,b,hm,hp=map(F,params);vx,vy=map(F,velocity);v=(vx,vy)
    poly=[(0,-hm),(2,-hm),(2,0),(3,0),(3,1),(2,1),(2,1+hp),(0,1+hp),(0,1),(1,1),(1,0),(0,0)]
    poly=[tuple(map(F,p)) for p in poly];p=(s,-a);T=(t,1+b);path=[p];edges=[];elapsed=F(0)
    for _ in range(10000):
        events=[]
        for i,(A,B) in enumerate(zip(poly,poly[1:]+poly[:1])):
            w=G.sub(B,A);den=G.cross(v,w)
            if not den:continue
            tau=G.cross(G.sub(A,p),w)/den;eta=G.cross(G.sub(A,p),v)/den
            if tau>0 and 0<=eta<=1:events.append((tau,i,eta))
        assert events
        tau=min(e[0] for e in events)
        if G.cross(G.sub(T,p),v)==0:
            j=0 if v[0] else 1;tt=(T[j]-p[j])/v[j]
            if 0<tt<tau:
                path.append(T);elapsed+=tt;break
        hits=[e for e in events if e[0]==tau];assert len(hits)==1 and 0<hits[0][2]<1
        _,i,_=hits[0];p=tuple(x+tau*y for x,y in zip(p,v));path.append(p);edges.append(i);elapsed+=tau
        A,B=poly[i],poly[(i+1)%len(poly)]
        v=(-v[0],v[1]) if A[0]==B[0] else (v[0],-v[1])
    else:raise AssertionError('prescribed finite trace exceeds guard')
    n=G.verify(path,F(1),F(1),a,b,s,t,hm,hp);assert n==len(edges)
    reverse=prefix([(x,1-y) for x,y in reversed(path)])
    rn=G.verify(reverse,F(1),F(1),b,a,t,s,hp,hm)
    d,g=F(2,3),F(5,7);scaled=[(d*x,g*y) for x,y in path]
    assert G.verify(scaled,d,g,g*a,g*b,d*s,d*t,g*hm,g*hp)==n
    return {'contacts':n,'reverse_contacts':rn,'time':str(elapsed),'edges':edges,'path':[[str(x),str(y)] for x,y in path]}

def main():
    peer=json.loads((BASE/'unequal-depth/horizontal-parity-check.json').read_text());assert peer['status']=='PRESCRIBED_CONTROLS_PASS'
    rows=[];fiber_checks=annuli=vertices=0
    for row in peer['rows']:
        s,t,a,b,hm,hp=map(F,row['fixture']);delta=rgcd([hm,F(1),hp]);ra=2*a/delta;rb=2*b/delta
        n=lcm(ra.denominator,rb.denominator);L=4*n/delta
        ss=fold(s-L*a);tt=fold(t+L*(1+b));assert 1<ss<2 and 1<tt<2
        for x,y,wanted in [(s,-a,ss),(t,1+b,tt)]:
            for sigma in (-1,1):
                for tau in (-1,1):assert fold(x+sigma*tau*L*y)==wanted;fiber_checks+=1
        # Six annuli: each signed transverse band has circumference4.
        for height in (hm,F(1),hp):
            assert L*height%4==0
            for sign in (-1,1):
                for x in (F(1,7),F(3,2),F(25,7)):
                    for f in (F(1,7),F(1,2),F(6,7)):
                        Y=sign*f*height;Xp=(x+L*Y)%4;assert (Xp-L*Y)%4==x%4;annuli+=1
                for boundary in (F(0),sign*height):assert (L*boundary)%4==0
        for y in (-hm,F(0),F(1),1+hp):
            for x in (0,1,2,3):
                for sigma in (-1,1):
                    for tau in (-1,1):assert (sigma*x+L*tau*y)%4==(sigma*x)%4;vertices+=1
        ds=1 if int(n*ra)%2==0 else -1
        velocity=(ds*(tt-ss)-L*(1+a+b),1+a+b)
        assert list(map(str,velocity))==row['original_velocity']
        r=trace(row['fixture'],velocity)
        assert r['contacts']==row['wall_contacts'] and r['edges']==row['edges'] and r['time']==row['time']
        rows.append({'fixture':row['fixture'],'delta':str(delta),'n':n,'L':str(L),'source_image':str(ss),'target_image':str(tt),'velocity':list(map(str,velocity)),**r})
    arithmetic=[]
    qs=(1,2,3,4,6,8,9,12,16,18,24,25)
    for q in qs:
        for r in qs:
            for s,t in ((F(1,2),F(1,4)),(F(1),F(1,4)),(F(1,2),F(1)),(F(1),F(1))):
                A,B=F(1,q),F(1,r);D=lcm((2*A).denominator,(2*B).denominator)
                actual=(s<1 and int(D*2*A)%2==1) or (t<1 and int(D*2*B)%2==1)
                e,f=v2(q),v2(r);mx=max(e,f)
                expected=mx>0 and ((e==mx and s<1) or (f==mx and t<1))
                assert actual==expected
                arithmetic.append({'q':q,'r':r,'s':str(s),'t':str(t),'criterion':bool(actual)})
    names=['unequal-depth/horizontal-parity-twist.md','unequal-depth/horizontal-parity-check.py','unequal-depth/horizontal-parity-check.json','arbitrary-endpoints-independent/check.py','unequal-depth-independent/horizontal-parity-check.py']
    out={'status':'INDEPENDENT_HORIZONTAL_SHEAR_CONTROLS_PASS','prescribed_forward_paths':len(rows),'actual_paths_with_reverse_and_scaling':3*len(rows),'contacts_including_reverse_and_scaling':sum(2*r['contacts']+r['reverse_contacts'] for r in rows),'full_fiber_identities':fiber_checks,'annulus_roundtrips':annuli,'signed_vertex_representations':vertices,'two_adic_criterion_controls':len(arithmetic),'source_sha256':{n:hashlib.sha256((BASE/n).read_bytes()).hexdigest() for n in names},'records':rows,'arithmetic':arithmetic,'limits':'Prescribed physical rays and exact arithmetic controls only; universal annulus and parity arguments separately hand-reviewed. No peer executable imported/run, discovery or full rational theorem.'}
    (HERE/'horizontal-parity-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('source_sha256','records','arithmetic')}))
if __name__=='__main__':main()
