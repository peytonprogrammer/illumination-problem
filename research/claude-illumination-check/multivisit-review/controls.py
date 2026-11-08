# Own exact check of the multivisit theorem on random orthogonal (staircase) rooms is overkill; instead
# test the key lemma: in an axis-parallel rectangle-free setting, a nonaxial billiard orbit's velocity
# takes 4 states and a reflection reverses velocity only if an axis component is 0.
from fractions import Fraction as F
import itertools
for p,q in itertools.product([F(1),F(2,3),F(-5,7)],[F(1),F(-3,4),F(9,2)]):
    for flip in ((-1,1),(1,-1)):
        v=(p,q); w=(flip[0]*p,flip[1]*q)
        assert w!=(-p,-q)          # a single orthogonal reflection never reverses a nonaxial velocity
print('reversal lemma ok')
# triangle control, own replay
s,z,c,t=(F(7,4),F(3,4)),(F(2),F(1)),(F(3,2),F(3,2)),(F(3,2),F(1,2))
inside=lambda p:0<p[1]<p[0]<2
P=[s,z,c,z,t]
for a,b in zip(P,P[1:]):
    for k in range(1,50):
        m=(a[0]+(b[0]-a[0])*F(k,50),a[1]+(b[1]-a[1])*F(k,50)); assert inside(m),m
    if (b[0]-a[0])*(t[1]-a[1])-(b[1]-a[1])*(t[0]-a[0])==0 and b!=t:
        lo=min(a[0],b[0]); hi=max(a[0],b[0]); assert not lo<=t[0]<=hi
def refl(d,n):
    k=2*(d[0]*n[0]+d[1]*n[1])/(n[0]**2+n[1]**2); return (d[0]-k*n[0],d[1]-k*n[1])
D=[(b[0]-a[0],b[1]-a[1]) for a,b in zip(P,P[1:])]
par=lambda u,v:u[0]*v[1]-u[1]*v[0]==0 and u[0]*v[0]+u[1]*v[1]>0
assert par(refl(D[0],(1,0)),D[1]) and par(refl(D[1],(1,-1)),D[2]) and par(refl(D[2],(1,0)),D[3])
print('triangle control ok')
