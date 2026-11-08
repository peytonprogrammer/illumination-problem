"""Independent prescribed-formula and real-wall checks; no peer execution.
The universal real-parameter argument is reviewed separately in review.md.
"""
from pathlib import Path
from fractions import Fraction as F
from math import gcd
import hashlib,json
HERE=Path(__file__).resolve().parent;BASE=HERE.parent

def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def cross(v,w):return v[0]*w[1]-v[1]*w[0]
def dot(v,w):return sum(x*y for x,y in zip(v,w))
def fold(x,w=F(2)):
 r=x%(2*w)
 return r if r<=w else 2*w-r

def inside(p,V):
 count=0
 for a,b in zip(V,V[1:]+V[:1]):
  if cross(sub(p,a),sub(b,a))==0 and dot(sub(p,a),sub(p,b))<=0:return False
  if (a[1]>p[1])!=(b[1]>p[1]):count+=a[0]+(p[1]-a[1])*(b[0]-a[0])/(b[1]-a[1])>p[0]
 return bool(count%2)

def verify(P,d,g,a,hm,hp):
 V=[(0,-hm),(2*d,-hm),(2*d,0),(3*d,0),(3*d,g),(2*d,g),(2*d,g+hp),(0,g+hp),(0,g),(d,g),(d,0),(0,0)]
 assert a<min(hm,hp) and all(inside(p,V) for p in (P[0],P[-1]))
 for i,(A,B) in enumerate(zip(P,P[1:])):
  v=sub(B,A);assert v!=(0,0)
  assert inside(tuple((x+y)/2 for x,y in zip(A,B)),V)
  hits=[]
  for c,dd in zip(V,V[1:]+V[:1]):
   w=sub(dd,c);den=cross(v,w)
   if not den:
    if cross(sub(c,A),v)==0:
     k=0 if v[0] else 1
     lo,hi=sorted(((c[k]-A[k])/v[k],(dd[k]-A[k])/v[k]))
     assert hi<=0 or lo>=1,('boundary overlap',i,A,B)
    continue
   tau=cross(sub(c,A),w)/den;eta=cross(sub(c,A),v)/den
   if 0<tau<=1 and 0<=eta<=1:
    assert tau==1 and 0<eta<1,('first-wall/corner failure',i,tau,eta,P)
    hits.append((c,dd))
  if i==len(P)-2:assert not hits
  else:
   assert len(hits)==1
   c,dd=hits[0];normal=0 if c[0]==dd[0] else 1
   reflected=tuple(-x if k==normal else x for k,x in enumerate(v));out=sub(P[i+2],B)
   assert cross(reflected,out)==0 and dot(reflected,out)>0
   target=P[-1]
   if cross(sub(target,A),v)==0:
    k=0 if v[0] else 1
    assert not 0<(target[k]-A[k])/v[k]<=1
 return len(P)-2

# Check each portal identity as an affine function over the WHOLE residue
# interval. It has no fold kink in its open interval; coefficients certify it.
charts=[(0,1,(1,2),(1,2)),(0,3,(2,3),(2,3)),(2,1,(1,2),(0,1)),(2,3,(2,3),(3,4))]
def affine(offset,add,interval):
 lo,hi=map(F,interval);mid=(lo+hi)/2;k=(mid-offset)//2
 assert offset+2*k<=lo<hi<=offset+2*(k+1)
 slope=1 if k%2==0 else -1
 return slope,add+fold(mid-offset)-slope*mid
for u,c,I,J in charts:
 assert affine(0,F(0),I)==affine(c,F(1),I)
 assert affine(c,F(1),J)==affine(u,F(0),J)
 for offset,add,interval in [(0,0,I),(c,1,J),(u,0,J)]:
  slope,b=affine(offset,F(add),interval)
  assert sorted((slope*interval[0]+b,slope*interval[1]+b))==[1,2]

low=[(1,5,2,-1,1,1,[(4,-1,1),(-4,1,4),(1,-4,4),(-1,4,1)]),
 (2,5,2,-1,1,3,[(3,-2,2),(-3,2,3),(2,-3,3),(-2,3,2)]),
 (2,7,2,-1,5,3,[(5,-2,2),(-5,2,5),(2,-5,5),(-2,5,2)]),
 (3,7,2,-1,5,1,[(4,-3,3),(-4,3,4),(3,-4,4),(-3,4,3)]),
 (1,7,2,-1,3,3,[(6,-1,0),(-6,1,7),(1,-6,7),(-1,6,0)]),
 (1,7,0,1,3,3,[(6,1,-2),(-6,-1,9),(1,6,2),(-1,-6,5)]),
 (1,7,2,1,2,1,[(6,1,3),(-6,-1,4),(1,6,4),(-1,-6,3)])]
def add(v,w):return tuple(a+b for a,b in zip(v,w))
def scale(k,v):return tuple(k*x for x in v)
for p,q,u,sign,M,c,listed in low:
 al=F(p,q);E1=(1-al,al*sign,al*(u+4*M));E2=(al,(1-al)*sign,(1-al)*(u+4*M))
 _,_,I,J=next(row for row in charts if row[:2]==(u,c))
 # Determine unique period at an interior point, then compare every affine
 # coefficient with the supplied strict interval inequality.
 s,t=F(1,2),F(1,4)
 def at(E):return E[0]*s+E[1]*t+E[2]
 guards=[]
 for E,(lo,hi) in [(E1,I),(E2,J)]:
  k=(at(E)-F(lo+hi,2))//4
  # Floor can select the prior translate if sample is outside this chart.
  # Pick translate dictated by listed constant, then demand integral period.
  lower=listed[len(guards)]
  kval=(q*E[2]-q*lo-lower[2])/(4*q)
  assert kval.denominator==1;k=int(kval)
  guards.extend([scale(q,add(E,(0,0,-lo-4*k))),scale(q,add(scale(-1,E),(0,0,hi+4*k)))])
 assert guards==list(map(tuple,listed)),(p,q,guards,listed)
 if (p,q)!=(1,7):
  # Any admissible(s,t) has barycentric weight t>0 at vertex(1,1).
  for A,B,C in listed:assert min(C,A+C,A+B+C)>=0 and A+B+C>0

# Formula-only chart selection, not a direction or reflection-word search.
def select(p,q,s,t):
 if q==3:return 'three'
 if q%2==0 and (s,t)!=(1,1):return (0,1,q//2,3)
 if q==4:return 'center'
 if q%2==0 or q>=9:
  al=F(p,q);D=s-t
  u,sign,lo,hi,c=(2,-1,1+D,2,1) if D<F(1,2) else (0,-1,2,2+D,3)
  E=(1-al)*s+al*sign*t+al*u
  j=(q*(lo-E)/4).__floor__()+1
  assert lo<E+F(4*j,q)<hi
  return u,sign,(j*pow(p,-1,q))%q,c
 if q==5:return (2,-1,1,1 if p==1 else 3)
 if p in (2,3):return (2,-1,5,3 if p==2 else 1)
 if s<6*t:return (2,-1,3,3)
 if 6*s+t>2:return (0,1,3,3)
 return (2,1,2,1)

def construct(p,q,s,t):
 al=F(p,q);a=al/(1-2*al);choice=select(p,q,s,t)
 if choice=='three':
  v=(6-s-t)/5;ps=s+2*v;pt=t+2*v;eta=1-(3-ps)/v
  assert 1<s+v<2 and 1<t+v<2 and 2<ps<3 and 2<pt<3 and 0<eta<1
  return [(s,-a),(ps,F(1)),(F(3),eta),(pt,F(0)),(t,1+a)],a,choice
 if choice=='center':return [(s,-a),(F(5,2),F(1)),(F(3),F(1,2)),(F(5,2),0),(t,1+a)],a,choice
 u,sign,M,c=choice;L=u+sign*t+4*M;v=(L-s)/(2*a+1);X=lambda y:s+v*(y+a)
 P=[(s,-a)]
 for ya,yb,offset,extra in [(-a,F(0),0,0),(F(0),F(1),c,1),(F(1),1+a,u,0)]:
  x0,x1=X(ya),X(yb)
  if v:
   k0=((min(x0,x1)-offset)/2).__floor__();k1=((max(x0,x1)-offset)/2).__floor__()+1
   for k in range(k0,k1+1):
    x=F(offset+2*k);y=(x-s)/v-a
    if ya<y<yb:P.append((extra+fold(x-offset),y))
 P[1:]=sorted(P[1:],key=lambda z:z[1]);P.append((t,1+a))
 assert fold(X(0))==1+fold(X(0)-c) and 1<fold(X(0))<2
 assert 1+fold(X(1)-c)==fold(X(1)-u) and 1<fold(X(1)-u)<2
 return P,a,choice

# Independent exact implementation of the cited L proof, after the explicit
# isometry (u,v)=(y+hm,2d-x). Generate its prescribed nearest image only.
def Lroute(s,t,a,d,g,hm,hp):
 if s>=d:return [(s,-a),(t,g+a)]
 xs,ys=hm+g+a,2*d-t;xt,yt=hm-a,2*d-s
 r=(yt-d)/(d-ys);h=-r*xs;period=2*hm
 candidates=[]
 for sign in (1,-1):
  m=((h-sign*xt)/period).__floor__()
  candidates += [sign*xt+period*j for j in range(m-1,m+3)]
 target=min((x for x in candidates if x!=h),key=lambda x:abs(x-h))
 assert 0<abs(target-h)<=hm
 Xs,Xt=(xs,target) if target>h else (-xs,-target)
 v=(Xt-Xs)/(yt-ys);X=lambda y:Xs+v*(y-ys)
 portal=X(d);assert 0<portal<hm
 points=[(xs,ys)]
 if Xs<0:
  y=ys-Xs/v;assert ys<y<d;points.append((F(0),y))
 x0,x1=X(d),X(yt)
 for j in range((min(x0,x1)/hm).__floor__()-1,(max(x0,x1)/hm).__floor__()+2):
  x=j*hm;y=ys+(x-Xs)/v
  if d<y<yt:points.append((fold(x,hm),y))
 points[1:]=sorted(points[1:],key=lambda P:P[1]);points.append((xt,yt))
 return [(2*d-y,x-hm) for x,y in points[::-1]]

def main():
 records=[];branches=Counter();contacts=0;maxcontacts=0
 for q in (3,4,5,6,7,8,9,10,11,13,16,19,23):
  for p in range(1,(q+1)//2):
   if gcd(p,q)!=1:continue
   for s,t in [(F(1),F(1)),(F(1),F(1,6)),(F(1,3),F(1,18)),(F(12,37),F(2,37)),(F(1,2),F(1,12)),(F(2,7),F(2,7)),(F(1),F(1,100)),(F(3,4),F(1,4)),(F(1,50),F(1,100))]:
    P,a,selected=construct(p,q,s,t);n=verify(P,F(1),F(1),a,a+F(1,1000),a+F(2,1000))
    branches[str((p,q,selected))]+=1
    # Endpoint order reversal, asymmetric clearances, and anisotropic scale.
    d,g=F(7,3),F(2,5);PP=[(d*x,g*y) for x,y in P]
    assert verify(PP,d,g,a*g,a*g+1,a*g+2)==n
    reflected=[(x,1-y) for x,y in P[::-1]]
    assert verify(reflected,F(1),F(1),a,a+1,a+2)==n
    contacts+=3*n;maxcontacts=max(maxcontacts,n);records.append((p,q,str(s),str(t),selected,n))
 lcontrols=0
 for d,g,a in [(F(1),F(1),F(1,2)),(F(2,3),F(7,2),F(4,3)),(F(5),F(1,3),F(1,100))]:
  for fs,ft in [(F(1,4),F(5,4)),(F(1),F(3,2)),(F(9,10),F(11,10)),(F(1,10),F(19,10))]:
   s,t=d*fs,d*ft;hm,hp=a+F(1,7),a+F(2,9)
   P=Lroute(s,t,a,d,g,hm,hp);contacts+=verify(P,d,g,a,hm,hp);lcontrols+=1
 sources=['equal-depth/proof.md','equal-depth/physical-check.py','equal-depth/physical-check.json','equal-depth/check.py','equal-depth/check.json','../single-boundary-blocker/l-monotone-proof.md','../single-boundary-blocker/l-monotone-peer-review.txt']
 pins={rel:hashlib.sha256((BASE/rel).read_bytes()).hexdigest() for rel in sources}
 pins['equal-depth-independent/check.py']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
 out={'status':'INDEPENDENT_EXACT_CHECKS_PASS_HAND_VERDICT_IN_REVIEW','normalized_prescribed_cases':len(records),'actual_corridor_paths':3*len(records),'actual_L_subroom_paths':lcontrols,'total_wall_contacts':contacts,'maximum_in_controls':maxcontacts,'four_portal_affine_identity_rows':4,'low_denominator_affine_guard_rows':7,'source_sha256':pins,'records':records,'limits':'Prescribed formulas only. Counts are controls, not proof by sampling or universal bounce bounds. Universal real-parameter coverage independently hand-reviewed in review.md. No peer program imported/executed, discovery, CAD, room/ray census, worker, or source edits.'}
 (HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
 print({k:v for k,v in out.items() if k not in ('records','source_sha256')})
from collections import Counter
if __name__=='__main__':main()
