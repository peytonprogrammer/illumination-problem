"""Evaluate one prescribed analytic construction per input. No ray search."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from collections import Counter
import json
B=Path(__file__).resolve().parent

def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def on(a,b,p):return cross(sub(b,a),sub(p,a))==0 and all(min(a[j],b[j])<=p[j]<=max(a[j],b[j]) for j in (0,1))
def fold(x,w):
 u=x%(2*w)
 return u if u<=w else 2*w-u

def vertical(A,a,c,C,s,t):
 """Return vertices, including an interior portal marker, and exact metadata."""
 xs,ys=s;xt,yt=t
 assert 0<a<A and 0<c<C
 if (ys<=c and yt<=c) or (xs<=a and xt<=a):return [s,t],dict(kind='DIRECT')
 if ys>c:
  P,m=vertical(A,a,c,C,t,s);return P[::-1],m
 assert a<xs<A and 0<ys<c and 0<xt<a and c<yt<C
 ds,dt=c-ys,yt-c;r=dt/ds;h=-r*xs
 # Two neighboring members of each target-image progression. Rounding,
 # not enumeration of candidate directions/words, implements the theorem.
 image=[]
 for sign in (-1,1):
  n=(h-sign*xt)//(2*a)
  image.extend([sign*xt+2*n*a,sign*xt+2*(n+1)*a])
 chosen=min((x for x in image if x!=h),key=lambda x:(abs(x-h),x));delta=abs(chosen-h)
 assert 0<delta<=a
 Xs=xs if chosen>h else -xs;Xt=chosen if chosen>h else -chosen
 q=(r*Xs+Xt)/(1+r);assert q==delta/(1+r) and 0<q<a
 assert fold(Xt,a)==xt and fold(Xs,A)==xs
 P=[s]
 if Xs<0:P.append((F(0),ys+ds*xs/(xs+q)))
 P.append((q,c));portal=len(P)-1
 if Xt!=q:
  lo,hi=sorted((q,Xt));integers=range(lo//a+1,-((-hi)//a))
  crossings=[k for k in integers if lo<k*a<hi]
  crossings.sort(reverse=Xt<q)
  for k in crossings:
   mu=(k*a-q)/(Xt-q);assert 0<mu<1
   P.append((a if k%2 else F(0),c+dt*mu))
 P.append(t)
 return P,dict(kind='CONSTRUCTED',portal=portal,q=str(q),r=str(r),h_exact_target_image=h in image,source_sign=1 if Xs>0 else -1,reflections=len(P)-3,chosen_image=str(chosen),target_image=str(Xt))

def vertices(A,a,c,C):return[(F(0),F(0)),(A,F(0)),(A,c),(a,c),(a,C),(F(0),C)]
def inside(V,p):
 if any(on(a,b,p) for a,b in zip(V,V[1:]+V[:1])):return False
 w=0
 for a,b in zip(V,V[1:]+V[:1]):
  if a[1]<=p[1]<b[1] and cross(sub(b,a),sub(p,a))>0:w+=1
  if b[1]<=p[1]<a[1] and cross(sub(b,a),sub(p,a))<0:w-=1
 return bool(w)

def validate(V,P,orientation):
 assert inside(V,P[0]) and inside(V,P[-1]);contacts=0
 for a,b in zip(P,P[1:]):
  assert a!=b;assert all(not on(a,b,v) for v in V)
  assert inside(V,tuple((x+y)/2 for x,y in zip(a,b)))
  d=sub(b,a)
  for c,e in zip(V,V[1:]+V[:1]):
   w=sub(e,c);den=cross(d,w)
   if not den:
    assert cross(sub(c,a),d) or not any(on(a,b,v) for v in (c,e))
    continue
   u=cross(sub(c,a),w)/den;v=cross(sub(c,a),d)/den
   if 0<=u<=1 and 0<=v<=1:assert u in (0,1)
 for i,p in enumerate(P[1:-1],1):
  walls=[(a,b) for a,b in zip(V,V[1:]+V[:1]) if on(a,b,p)]
  incoming,outgoing=sub(p,P[i-1]),sub(P[i+1],p)
  if not walls:assert cross(incoming,outgoing)==0 and sum(x*y for x,y in zip(incoming,outgoing))>0;continue
  assert len(walls)==1 and p not in V;a,b=walls[0];contacts+=1
  n=0 if a[0]==b[0] else 1;assert n==orientation
  reflected=list(incoming);reflected[n]*=-1
  assert cross(reflected,outgoing)==0 and sum(x*y for x,y in zip(reflected,outgoing))>0
 # An opposite-orientation boundary point cannot lie on any segment.
 for a,b in zip(V,V[1:]+V[:1]):
  n=0 if a[0]==b[0] else 1
  if n==orientation:continue
  for lam in (F(1,3),F(1,2),F(2,3)):
   z=tuple((1-lam)*x+lam*y for x,y in zip(a,b))
   assert all(not on(p,q,z) for p,q in zip(P,P[1:]))
 return contacts

if __name__=='__main__':
 dims=[(2,1,1,2),(5,2,3,7),(7,1,1,5),(3,2,2,3),(F(7,2),F(5,4),F(3,2),F(17,4)),(F(9,4),F(1,4),2,F(9,4))]
 stats=Counter();maxref=0;total_contacts=0
 for shape in dims:
  A,a,c,C=map(F,shape);V=vertices(A,a,c,C)
  for u,v,w,z in product((F(1,5),F(1,2),F(4,5)),repeat=4):
   s=(a+(A-a)*u,c*v);t=(a*w,c+(C-c)*z)
   P,m=vertical(A,a,c,C,s,t);total_contacts+=validate(V,P,0)
   # Transpose t->s and reverse to recover the original source order.
   Q,n=vertical(C,c,a,A,(t[1],t[0]),(s[1],s[0]));Q=[(y,x) for x,y in Q][::-1];total_contacts+=validate(V,Q,1)
   assert P[0]==Q[0]==s and P[-1]==Q[-1]==t
   stats['interior_pairs']+=1;stats['connections']+=2
   for md in [m,n]:
    stats['source_sign_'+str(md['source_sign'])]+=1;stats['exact_image_center']+=int(md['h_exact_target_image']);maxref=max(maxref,md['reflections'])
 # An exact equality/tie fixture and the previously fixed central-core control.
 A,a,c,C=map(F,(2,1,1,2));s=(F(7,4),F(1,4));t=(F(1,4),F(7,4));P,m=vertical(A,a,c,C,s,t);Q,n=vertical(C,c,a,A,(t[1],t[0]),(s[1],s[0]));Q=[(y,x) for x,y in Q][::-1]
 assert m['h_exact_target_image'];validate(vertices(A,a,c,C),P,0);validate(vertices(A,a,c,C),Q,1)
 fixture=dict(dimensions=[A,a,c,C],s=s,t=t,vertical_only=P,horizontal_only=Q,metadata=[m,n]);(B/'l-monotone-fixture.json').write_text(json.dumps(fixture,indent=2,default=str)+'\n')
 A,a,c,C=map(F,(3,F(5,2),F(3,2),2));s=(F(3,4),F(1));t=(F(9,4),F(1));P,m=vertical(A,a,c,C,s,t);assert m['kind']=='DIRECT';validate(vertices(A,a,c,C),P,0)
 result=dict(status='PASS',formula_pairs=stats['interior_pairs'],formula_connections=stats['connections'],source_sign_counts={k:v for k,v in stats.items() if k.startswith('source_sign')},exact_image_center_cases=stats['exact_image_center'],wall_contacts_checked=total_contacts,max_reflections_in_fixture_grid=maxref,additional_equality_fixture_connections=2,central_core_bypass_control=True,scope='Exactly one prescribed analytic path per orientation for fixed rational input grid; no ray/direction/word search. General real-parameter theorem rests on l-monotone-proof.md, not finite controls.')
 (B/'arithmetic-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
