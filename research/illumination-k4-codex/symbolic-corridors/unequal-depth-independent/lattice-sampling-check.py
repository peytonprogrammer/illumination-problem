"""Exact prescribed controls for uniform finite-orbit sampling hand lemma.
No parameter/direction discovery; all phase tuples and offsets fixed below.
"""
from fractions import Fraction as F
from pathlib import Path
from math import gcd,isqrt
import hashlib,json
HERE=Path(__file__).resolve().parent;BASE=HERE.parent
PHASES=((1,4,101),(1,13,101),(1,17,103),(1,11,121),(3,11,127),(1,12,144),(1,13,169),(5,31,257),(1,32,1024))
BOXES=(((F(0),F(0)),(F(1),F(1))),((F(1,7),F(1,11)),(F(15,4),F(-7,5))),((F(-13,7),F(20,11)),(F(4,3),F(11,7))),((F(17,23),F(9,13)),(F(-3,2),F(17,9))))
def bezout(a,b):
    x,y=abs(a),abs(b);u,v,r,s=1,0,0,1
    while y:
        k=x//y;x,y=y,x-k*y;u,r=r,u-k*r;v,s=s,v-k*s
    return x,u*(1 if a>=0 else -1),v*(1 if b>=0 else -1)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def main():
    rows=[];box_controls=[];totalpoints=0;components=0
    for A,C,q in PHASES:
        assert 0<A<C<q and gcd(gcd(A,C),q)==1 and q>100
        R=isqrt(2*q);vectors=[]
        for m in range(-R,R+1):
            for n in range(-R,R+1):
                if 0<abs(m)+abs(n)<=R and (m*A+n*C)%q==0:vectors.append((abs(m)+abs(n),m,n))
        assert vectors
        w,m,n=min(vectors);assert 5<=w and w*w<=2*q
        r=(m*A+n*C)//q;g=gcd(abs(m),abs(n))
        assert gcd(g,r)==1 and q%g==0 and gcd(gcd(abs(m),abs(n)),abs(r))==1
        assert q*(w-4)>4*w*w
        # The integer minimum and component counts are independently rebuilt.
        orbit={(F(j*A,q)%1,F(j*C,q)%1) for j in range(q)};assert len(orbit)==q
        groups={k:[] for k in range(g)}
        for j in range(q):groups[(j*r)%g].append(j)
        N=q//g;assert all(len(v)==N for v in groups.values())
        T=(-n//g,m//g);gg,u,v=bezout(*T);assert gg==1 and u*T[0]+v*T[1]==1
        coeff=u*A+v*C
        for js in groups.values():
            j0=js[0];coords={F((j-j0)*coeff,q)%1 for j in js}
            assert coords=={F(k,N) for k in range(N)}
        rho=F(w-4,2*w);norm2=m*m+n*n
        assert F(4*norm2,q*q)<rho*rho
        gg,um,un=bezout(m,n);assert gg==g and um*m+un*n==g
        for offset,origin in BOXES:
            z=tuple(x+F(1,2) for x in origin);h=(dot((m,n),z)-dot((m,n),offset))/4
            k=(h+F(1,2)).__floor__();delta=dot((m,n),offset)+4*k-dot((m,n),z)
            assert abs(delta)<=2
            signs=(0 if m==0 else 1 if m>0 else -1,0 if n==0 else 1 if n>0 else -1)
            zp=tuple(x+delta*sg/w for x,sg in zip(z,signs))
            assert dot((m,n),zp)==dot((m,n),offset)+4*k
            assert all(abs(x-y)<=F(2,w) for x,y in zip(zp,z))
            nearest=[]
            for j in groups[k%g]:
                hshift=(k-j*r)//g;point=(offset[0]+F(4*j*A,q)+4*hshift*um,offset[1]+F(4*j*C,q)+4*hshift*un)
                assert dot((m,n),point)==dot((m,n),offset)+4*k
                lam=dot(tuple(a-b for a,b in zip(zp,point)),T)/(4*dot(T,T));wind=(lam+F(1,2)).__floor__()
                point=tuple(x+4*wind*t for x,t in zip(point,T));dist2=sum((x-y)**2 for x,y in zip(point,zp));nearest.append((dist2,j,point))
            dist2,j,point=min(nearest)
            assert dist2<=F(4*norm2,q*q)<rho*rho
            assert all(a<x<a+1 for a,x in zip(origin,point))
            box_controls.append({'phase':[A,C,q],'offset':list(map(str,offset)),'origin':list(map(str,origin)),'component':k%g,'M':j,'distance_squared':str(dist2),'rho_squared':str(rho*rho),'strict_lifted_hit':list(map(str,point))})
        rows.append({'phase':[A,C,q],'minimum_l1':w,'minimizer':[m,n,r],'components':g,'points_per_component':N,'primitive_tangent':list(T),'sampling_inequality_slack':str(F(q)-F(4*w*w,w-4))})
        totalpoints+=q;components+=g
    # Exact sufficient-bound controls, independent of the phase exemplars.
    inequalities=0
    for q in (101,102,127,144,256,1024,10000,1000000):
        for w in range(5,isqrt(2*q)+1):assert q*(w-4)>4*w*w;inequalities+=1
    names=['unequal-depth/lattice-sampling.md','unequal-depth-independent/vertical-completeness-review.md','unequal-depth-independent/lattice-sampling-check.py']
    out={'status':'INDEPENDENT_FINITE_ORBIT_SAMPLING_CONTROLS_PASS','prescribed_phase_triples':len(rows),'exact_orbit_points':totalpoints,'components_verified':components,'strict_translated_box_controls':len(box_controls),'sufficient_bound_controls':inequalities,'source_sha256':{n:hashlib.sha256((BASE/n).read_bytes()).hexdigest() for n in names},'phase_records':rows,'box_records':box_controls,'limits':'Allq theorem proved separately by area/component/spacing/strict-segment hand argument. Prescribed finite controls do not replace that proof, claim q<=100coverage, or prove universal rational room illumination.'}
    (HERE/'lattice-sampling-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('source_sha256','phase_records','box_records')}))
if __name__=='__main__':main()
