"""Independent prescribed lemma controls. Does not execute peer writers."""
from pathlib import Path
from fractions import Fraction as F
from importlib.util import spec_from_file_location,module_from_spec
import hashlib,json
HERE=Path(__file__).resolve().parent
BASE=HERE.parent
spec=spec_from_file_location('own_frozen_geometry',BASE/'arbitrary-endpoints-independent/check.py')
geom=module_from_spec(spec);spec.loader.exec_module(geom)
fold=geom.fold

def Lroute(s,t,a,b,d,g,hm,hp):
    if s>=d:return [(s,-a),(t,g+b)]
    # Isometry (u,v)=(y+hm,2d-x), reversed target as L-source.
    xs,ys=hm+g+b,2*d-t;xt,yt=hm-a,2*d-s
    r=(yt-d)/(d-ys);h=-r*xs;period=2*hm
    candidates=[]
    for sign in (1,-1):
        m=((h-sign*xt)/period).__floor__()
        candidates.extend(sign*xt+period*j for j in range(m-1,m+3))
    target=min((x for x in candidates if x!=h),key=lambda x:abs(x-h))
    assert 0<abs(target-h)<=hm
    Xs,Xt=(xs,target) if target>h else (-xs,-target)
    v=(Xt-Xs)/(yt-ys);X=lambda y:Xs+v*(y-ys)
    assert 0<X(d)<hm
    points=[(xs,ys)]
    if Xs<0:
        y=ys-Xs/v;assert ys<y<d;points.append((F(0),y))
    x0,x1=X(d),X(yt)
    for j in range((min(x0,x1)/hm).__floor__()-1,(max(x0,x1)/hm).__floor__()+2):
        x=j*hm;y=ys+(x-Xs)/v
        if d<y<yt:points.append((fold(x,hm),y))
    points[1:]=sorted(points[1:],key=lambda p:p[1]);points.append((xt,yt))
    return [(2*d-y,x-hm) for x,y in points[::-1]]

def main():
    charts=[]
    for u,c,I,J in [(0,1,(1,2),(1,2)),(0,3,(2,3),(2,3)),(2,1,(1,2),(0,1)),(2,3,(2,3),(3,4))]:
        def affine(offset,extra,interval):
            lo,hi=map(F,interval);mid=(lo+hi)/2;k=(mid-offset)//2
            assert offset+2*k<=lo<hi<=offset+2*(k+1)
            slope=1 if k%2==0 else -1
            return slope,extra+fold(mid-offset,F(2))-slope*mid
        assert affine(0,0,I)==affine(c,1,I)
        assert affine(c,1,J)==affine(u,0,J)
        charts.append((u,c,I,J))
    rows=[];contacts=0
    for d,g in [(F(1),F(1)),(F(2,7),F(11,3)),(F(9),F(1,11))]:
        for a,b in [(F(1,10),F(3)),(F(5),F(1,10)),(F(1,3),F(7,9)),(F(5,7),F(12,7))]:
            for fs,ft in [(F(1,10),F(5,4)),(F(99,100),F(199,100)),(F(1,2),F(3,2)),(F(1),F(7,4))]:
                s,t=d*fs,d*ft;hm,hp=a+F(1,10000),b+F(1,10000)
                P=Lroute(s,t,a,b,d,g,hm,hp)
                n=geom.verify(P,d,g,a,b,s,t,hm,hp)
                assert all(P[i][0]<P[i+1][0] for i in range(len(P)-1))
                Q=[(x,g-y) for x,y in P[::-1]]
                assert geom.verify(Q,d,g,b,a,t,s,hp,hm)==n
                contacts+=2*n;rows.append({'d':str(d),'g':str(g),'a':str(a),'b':str(b),'s/d':str(fs),'t/d':str(ft),'contacts':n})
    # Algebraic identities supporting the whole-class midpoint obstruction.
    for a in map(F,['1/1000','1/2','1','37','10000']):
        b=a+1;H=a+1+b
        assert (a+1)/H==F(1,2)
        for j in range(-50,51):
            L=2*j+1;mid=F(1+L,2)
            assert mid.denominator==1
            for mirror in (-7,-1,0,1,2,3,17):
                assert (2*mirror-L)%2==1
                assert (2*mirror-mid).denominator==1
    # Snapshot is a review artifact, not a claim the live peer file is frozen.
    source=(BASE/'unequal-depth/proof.md').read_text()
    relevant=source.split('## 4.')[0]
    snapshot=HERE/'midpoint-source-snapshot.md'
    if snapshot.exists():assert snapshot.read_text()==relevant,'reviewed live sections changed; use a new revision receipt'
    else:snapshot.write_text(relevant)
    sources=['arbitrary-endpoints-independent/check.py','arbitrary-endpoints-independent/acceptance.json','../single-boundary-blocker/l-monotone-proof.md','../single-boundary-blocker/l-monotone-peer-review.txt','equal-depth-independent/review.md']
    pins={s:hashlib.sha256((BASE/s).read_bytes()).hexdigest() for s in sources}
    pins['unequal-depth-independent/midpoint-source-snapshot.md']=hashlib.sha256(snapshot.read_bytes()).hexdigest()
    pins['unequal-depth-independent/midpoint-check.py']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    out={'status':'PASS','scope':'peer sections1-3 snapshot; not full unequal-depth theorem','four_affine_charts':len(charts),'unequal_depth_L_paths':2*len(rows),'wall_contacts':contacts,'integer_midpoint_identity_controls':505,'source_sha256':pins,'records':rows,'limits':'Universal lemmas require the hand review; controls do not prove darkness. Imports only own frozen independent helper, no peer code.'}
    (HERE/'midpoint-check.json').write_text(json.dumps(out,indent=2)+'\n')
    print({k:v for k,v in out.items() if k not in ('records','source_sha256')})
if __name__=='__main__':main()
