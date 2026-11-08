"""Independent exact prescribed checks. No peer imports or candidate search.
Universal real-parameter claims are audited in review.md.
"""
from fractions import Fraction as F
from math import comb, gcd, isqrt
from pathlib import Path
import hashlib, json

HERE=Path(__file__).resolve().parent
BASE=HERE.parent

class K:
    """Exact Q(sqrt(2),sqrt(3)); signs certified by rational enclosures."""
    def __init__(self,x=0):
        self.c=x.c if isinstance(x,K) else tuple(map(F,x)) if isinstance(x,tuple) else (F(x),F(0),F(0),F(0))
    def __add__(self,y):
        y=K(y);return K(tuple(a+b for a,b in zip(self.c,y.c)))
    __radd__=__add__
    def __neg__(self):return K(tuple(-a for a in self.c))
    def __sub__(self,y):return self+-K(y)
    def __rsub__(self,y):return K(y)+-self
    def __mul__(self,y):
        y=K(y);z=[F(0)]*4
        for i,a in enumerate(self.c):
            for j,b in enumerate(y.c):
                overlap=i&j;z[i^j]+=a*b*(2 if overlap&1 else 1)*(3 if overlap&2 else 1)
        return K(tuple(z))
    __rmul__=__mul__
    def conjugate(self,mask):return K(tuple(-a if (i&mask).bit_count()%2 else a for i,a in enumerate(self.c)))
    def inv(self):
        assert self!=0
        z=self.conjugate(1)*self.conjugate(2)*self.conjugate(3)
        norm=(self*z).c
        assert norm[0] and norm[1:]==(0,0,0)
        return K(tuple(a/norm[0] for a in z.c))
    def __truediv__(self,y):return self*K(y).inv()
    def __rtruediv__(self,y):return K(y)*self.inv()
    def bounds(self,digits):
        den=10**digits;lo=hi=self.c[0]
        for a,n in zip(self.c[1:],(2,3,6)):
            k=isqrt(n*den*den);l,u=F(k,den),F(k+1,den)
            assert l*l<n<u*u
            lo+=a*(l if a>=0 else u);hi+=a*(u if a>=0 else l)
        return lo,hi
    def sign(self):
        if all(a==0 for a in self.c):return 0
        digits=4
        while True:
            lo,hi=self.bounds(digits)
            if lo>0:return 1
            if hi<0:return -1
            digits*=2
    def __eq__(self,y):return self.c==K(y).c
    def __lt__(self,y):return (self-K(y)).sign()<0
    def __le__(self,y):return (self-K(y)).sign()<=0
    def __gt__(self,y):return (self-K(y)).sign()>0
    def __ge__(self,y):return (self-K(y)).sign()>=0
    def __bool__(self):return self!=0
    def __floor__(self):
        if self.c[1:]==(0,0,0):return self.c[0].__floor__()
        digits=4
        while True:
            lo,hi=self.bounds(digits)
            if lo.__floor__()==hi.__floor__():return lo.__floor__()
            digits*=2
    def __floordiv__(self,y):return (self/y).__floor__()
    def __mod__(self,y):return self-y*(self//y)
    def __repr__(self):return 'K'+repr(tuple(map(str,self.c)))


def sub(p,q):return tuple(a-b for a,b in zip(p,q))
def cross(v,w):return v[0]*w[1]-v[1]*w[0]
def dot(v,w):return sum(a*b for a,b in zip(v,w))
def fold(x,w):
    r=x%(2*w);return r if r<=w else 2*w-r

def inside(p,vertices):
    count=0
    for a,b in zip(vertices,vertices[1:]+vertices[:1]):
        if cross(sub(p,a),sub(b,a))==0 and dot(sub(p,a),sub(p,b))<=0:return False
        if (a[1]>p[1])!=(b[1]>p[1]):
            count+=a[0]+(p[1]-a[1])*(b[0]-a[0])/(b[1]-a[1])>p[0]
    return bool(count%2)

def verify(path,d,g,a,b,s,t,hm,hp,scalar=F):
    assert 0<a<hm and 0<b<hp and 0<s<2*d and 0<t<2*d
    vertices=[(0,-hm),(2*d,-hm),(2*d,0),(3*d,0),(3*d,g),(2*d,g),(2*d,g+hp),(0,g+hp),(0,g),(d,g),(d,0),(0,0)]
    vertices=[tuple(map(scalar,v)) for v in vertices]
    assert path[0]==(s,-a) and path[-1]==(t,g+b)
    assert inside(path[0],vertices) and inside(path[-1],vertices)
    for i,(A,B) in enumerate(zip(path,path[1:])):
        v=sub(B,A);assert v!=(0,0)
        assert inside(tuple((x+y)/2 for x,y in zip(A,B)),vertices)
        hits=[]
        for c,e in zip(vertices,vertices[1:]+vertices[:1]):
            w=sub(e,c);den=cross(v,w)
            if not den:
                if cross(sub(c,A),v)==0:
                    j=0 if v[0] else 1
                    lo,hi=sorted(((c[j]-A[j])/v[j],(e[j]-A[j])/v[j]))
                    assert hi<=0 or lo>=1,('boundary overlap',i)
                continue
            tau=cross(sub(c,A),w)/den;eta=cross(sub(c,A),v)/den
            if 0<tau<=1 and 0<=eta<=1:
                assert tau==1 and 0<eta<1,('prior wall or corner',i,tau,eta)
                hits.append((c,e))
        if i==len(path)-2:assert not hits
        else:
            assert len(hits)==1
            c,e=hits[0];normal=0 if c[0]==e[0] else 1
            reflected=tuple(-x if j==normal else x for j,x in enumerate(v))
            outgoing=sub(path[i+2],B)
            assert cross(reflected,outgoing)==0 and dot(reflected,outgoing)>0
            if cross(sub(path[-1],A),v)==0:
                j=0 if v[0] else 1
                assert not 0<(path[-1][j]-A[j])/v[j]<=1
    return len(path)-2

def chart_path(d,g,a,b,s,t,M,c,u,sign):
    H=a+g+b;L=u+sign*t+4*d*M;v=(L-s)/H
    X=lambda y:s+v*(y+a)
    E1,E2=X(0),X(g)
    def deriv(x,offset):
        r=(x-offset)%(4*d);assert r!=0 and r!=2*d
        return 1 if r<2*d else -1
    assert fold(E1,2*d)==d+fold(E1-c,2*d)
    assert d+fold(E2-c,2*d)==fold(E2-u,2*d)
    assert d<fold(E1,2*d)<2*d and d<fold(E2-u,2*d)<2*d
    assert deriv(E1,0)==deriv(E1,c)
    assert deriv(E2,c)==deriv(E2,u)
    assert fold(L-u,2*d)==t
    events=[];bandcounts=[]
    for ya,yb,offset,extra in [(-a,0,0,0),(0,g,c,d),(g,g+b,u,0)]:
        n=0
        if v:
            x0,x1=X(ya),X(yb);lo,hi=sorted((x0,x1))
            for k in range((lo-offset)//(2*d)-1,(hi-offset)//(2*d)+2):
                xx=offset+2*d*k
                if lo<xx<hi:
                    yy=(xx-s)/v-a;assert ya<yy<yb
                    events.append((extra+fold(xx-offset,2*d),yy));n+=1
        bandcounts.append(n)
    events.sort(key=lambda p:p[1])
    return [(s,-a)]+events+[(t,g+b)],bandcounts

def equal_choice(p,q,s,d):
    al=F(p,q)
    if q==4 and s==d:return None
    if q>=5:
        v=(s+2*al*(d-s))/(4*d)
        j=(q*(F(1,4)-v)).__floor__()+1
        M=(j*pow(p,-1,q))%q
    elif q==3:M=0 if s>d else 1
    else:M=0 if s>d else 1
    E=s+al*(2*d-2*s)+4*d*M*al
    return M,(d if E%(4*d)<2*d else 3*d)

def main():
    C=F(comb(64,32),2**64)
    coeff={j:F(comb(64,32+j),2**64) for j in range(-32,33)}
    assert sum(coeff.values())==1 and coeff[0]==C and all(x>0 for x in coeff.values())
    assert C*C>=F(1,128) and 128*6**32<7**32 and F(10,7)**2>2
    # Exact induction step for all steps used, and the general difference is 1.
    for k in range(1,32):assert (2*k+1)**2-4*k*(k+1)==1
    assert ((2+K((0,1,0,0)))/4)<F(6,7)
    # Whole-interval affine identities, d=1; positive scaling preserves them.
    identities=[]
    for c,u,I,J in [(1,0,(1,2),(1,2)),(1,2,(1,2),(0,1)),(3,2,(2,3),(3,4))]:
        def affine(offset,extra,interval):
            lo,hi=map(F,interval);mid=(lo+hi)/2;k=(mid-offset)//2
            assert offset+2*k<=lo<hi<=offset+2*(k+1)
            slope=1 if k%2==0 else -1
            return slope,extra+fold(mid-offset,F(2))-slope*mid
        assert affine(0,0,I)==affine(c,1,I)
        assert affine(c,1,J)==affine(u,0,J)
        identities.append((c,u,I,J))
    records=[];total=0
    for d,g in [(F(1),F(1)),(F(7,3),F(2,5))]:
        for k in (1,2,5,11):
            a=g;b=(6*k-2)*g
            for fs,ft in [(F(2,5),F(3,5)),(F(1,2),F(1,2)),(F(3,5),F(2,5))]:
                s,t=d*fs,d*ft
                P,counts=chart_path(d,g,a,b,s,t,k,d,F(0),1)
                n=verify(P,d,g,a,b,s,t,a+g/100,b+g/100)
                # Reverse plus reflect y exchanges depths and endpoints.
                Q=[(x,g-y) for x,y in P[::-1]]
                assert verify(Q,d,g,b,a,t,s,b+g/100,a+g/100)==n
                total+=2*n;records.append({'type':'unequal common chart','k':k,'contacts':n,'bands':counts})
    # Zero horizontal slope is allowed, with no reflected contact.
    P,counts=chart_path(F(1),F(1),F(2),F(3),F(3,2),F(3,2),0,F(1),F(0),1)
    assert verify(P,F(1),F(1),F(2),F(3),F(3,2),F(3,2),F(4),F(5))==0
    records.append({'type':'zero horizontal slope','contacts':0})
    equal_n=0
    for q in (3,4,5,7,8,11,16,23):
        for p in range(1,(q+1)//2):
            if gcd(p,q)!=1:continue
            for ratio in (F(1,100),F(1,2),F(1),F(3,2),F(199,100)):
                d,g=F(7,3),F(2,5);s=d*ratio;alpha=F(p,q);a=g*alpha/(1-2*alpha)
                choice=equal_choice(p,q,s,d)
                if choice is None:
                    P=[(s,-a),(5*d/2,g),(3*d,g/2),(5*d/2,F(0)),(s,g+a)]
                else:
                    M,c=choice;P,_=chart_path(d,g,a,a,s,s,M,c,2*d,-1)
                n=verify(P,d,g,a,a,s,s,a+g/100,a+g/50)
                total+=n;equal_n+=1;records.append({'type':'equal diagonal','p':p,'q':q,'s/d':str(ratio),'contacts':n})
    # Prescribed irrational connection, exact field arithmetic throughout.
    d,g=K(1),K(1);a=K((0,1,0,0));b=K((0,0,1,0));s,t=K(F(1,2)),K(F(3,2))
    P,counts=chart_path(d,g,a,b,s,t,12,d,K(0),1)
    assert counts==[8,6,10]
    n=verify(P,d,g,a,b,s,t,a+1,b+1,K);assert n==24;total+=n
    records.append({'type':'Q(sqrt2,sqrt3) exact irrational example','contacts':n,'bands':counts})
    sources=['arbitrary-endpoints/argument.md','arbitrary-endpoints/check.py','arbitrary-endpoints/check.json','proof.md','equal-depth-independent/review.md','equal-depth-independent/acceptance.json']
    pins={r:hashlib.sha256((BASE/r).read_bytes()).hexdigest() for r in sources}
    pins['arbitrary-endpoints-independent/check.py']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    out={'status':'PASS','finite_fourier_frequencies':len(coeff)**2,'nonzero_frequencies':len(coeff)**2-1,'fourier_l1_norm':'1','constant_coefficient':str(C),'threshold_chain_exact':True,'portal_affine_identity_charts':len(identities),'unequal_common_chart_paths':48,'zero_slope_paths':1,'equal_diagonal_paths':equal_n,'exact_irrational_paths':1,'actual_paths':48+1+equal_n+1,'wall_contacts':total,'source_sha256':pins,'records':records,'limits':'Prescribed formula controls, not proof by sampling or discovery. Universal real-parameter argument hand-reviewed separately. No peer code imports or execution.'}
    (HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('records','source_sha256')}))

if __name__=='__main__':main()
