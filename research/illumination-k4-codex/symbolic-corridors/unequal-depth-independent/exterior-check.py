"""Exact prescribed cap examples and affine identities; no candidate search."""
from pathlib import Path
from fractions import Fraction as F
from importlib.util import spec_from_file_location,module_from_spec
import hashlib,json
HERE=Path(__file__).resolve().parent;BASE=HERE.parent
spec=spec_from_file_location('own_geometry',BASE/'arbitrary-endpoints-independent/check.py')
G=module_from_spec(spec);spec.loader.exec_module(G);K=G.K

def control(lower):
    a,b,s,t=map(K,([1,F(1,2),F(1,2),F(3,4)] if lower else [F(1,2),1,F(3,4),F(1,2)]))
    root=K((0,1,0,0));hm=a+root if lower else a+1;hp=b+1 if lower else b+root
    A=2*hm-a if lower else a;B=b if lower else 2*hp-b
    H=A+1+B;H0=a+1+b;u=0;eps=-1;M=1;c=3 if lower else 1
    z=(u+eps*t-s+4*M)/H;X=lambda y:s+z*(y+A)
    E1,E2=X(0),X(1)
    assert G.fold(E1,2)==1+G.fold(E1-c,2)
    assert 1+G.fold(E2-c,2)==G.fold(E2-u,2)
    assert 1<G.fold(E1,2)<2 and 1<G.fold(E2-u,2)<2
    cap=-hm if lower else 1+hp
    capx=X(cap)
    affine=(s+u+eps*t)/2+2*M+(-1 if lower else 1)*H0*z/2
    assert capx==affine and capx%2!=0
    q=2;p=2 if lower else 1;r=1 if lower else 2
    assert H0*2*q==2*(p+q+r)
    if lower:
        assert A-hm==(H-H0)/2
        assert E1-(u+eps*t-(1+b)*z)==4*M
        assert E2-(u+eps*t-b*z)==4*M
        assert (1+b)*4*q%4==0 and b*4*q%4==0
    else:
        assert a+1+hp==(H+H0)/2
        assert a*4*q%4==0 and (a+1)*4*q%4==0
    def Y(y):
        if lower and y<-hm:return -2*hm-y
        if not lower and y>1+hp:return 2*(1+hp)-y
        return y
    events=[]
    for ya,yb,offset,extra in [(-A,K(0),0,0),(K(0),K(1),c,1),(K(1),1+B,u,0)]:
        lo,hi=sorted((X(ya),X(yb)))
        for j in range((lo-offset)//2-1,(hi-offset)//2+2):
            xx=K(offset+2*j)
            if lo<xx<hi:
                yy=(xx-s)/z-A;assert ya<yy<yb
                events.append((yy,(extra+G.fold(xx-offset,2),Y(yy))))
    events.append((cap,(G.fold(capx,2) if lower else G.fold(capx-u,2),Y(cap))))
    events.sort(key=lambda e:e[0])
    P=[(s,-a)]+[point for y,point in events]+[(t,1+b)]
    target=P[-1];prefix=[P[0]];trimmed=False
    for i,(x,y) in enumerate(zip(P,P[1:])):
        v=G.sub(y,x)
        if G.cross(G.sub(target,x),v)==0:
            j=0 if v[0] else 1;tau=(target[j]-x[j])/v[j]
            if 0<tau<=1:prefix.append(target);trimmed=i<len(P)-2;break
        prefix.append(y)
    count=G.verify(prefix,K(1),K(1),a,b,s,t,hm,hp,K)
    rev=[(x,1-y) for x,y in prefix[::-1]]
    assert G.verify(rev,K(1),K(1),b,a,t,s,hp,hm,K)==count
    return {'cap':'lower' if lower else 'upper','actual_paths':2,'contacts_per_path':count,'early_target_trimmed':trimmed,'cap_phase_not_even_integer':True,'period_identity':True}

def main():
    sources=['unequal-depth/exterior-irrational.md','unequal-depth-independent/phase-lines-acceptance.json','unequal-depth-independent/cap-sheet-review.md','arbitrary-endpoints-independent/check.py']
    pins={r:hashlib.sha256((BASE/r).read_bytes()).hexdigest() for r in sources}
    rows=[control(False),control(True)]
    for r,h in pins.items():assert hashlib.sha256((BASE/r).read_bytes()).hexdigest()==h,r
    pins['unequal-depth-independent/exterior-check.py']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    out={'status':'EXACT_EXTERIOR_IRRATIONAL_CONTROLS_PASS','actual_paths':sum(r['actual_paths'] for r in rows),'wall_contacts':sum(r['actual_paths']*r['contacts_per_path'] for r in rows),'source_sha256':pins,'records':rows,'limits':'Prescribed exact quadratic-radical cap paths and affine identities. Universal circle-density and finite bad-set avoidance are hand-reviewed; no discovery or rational-depth conclusion.'}
    (HERE/'exterior-check.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='source_sha256'}))
if __name__=='__main__':main()
