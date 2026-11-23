"""Independent exact check of the DB55 corridor claims. Own tracer; reads D72 JSON only as data."""
from fractions import Fraction as F
from itertools import product
import json, sys, time
from pathlib import Path

def room(L):
    v=[(0,0),(5,0),(5,2),(5+L,2),(5+L,0),(10+L,0),(10+L,5),(5+L,5),(5+L,3),(5,3),(5,5),(0,5)]
    return [tuple(map(F,p)) for p in v]
def square(x0):  # sealed 5x5 chamber, door replaced by mirror
    return [(F(x0),F(0)),(F(x0+5),F(0)),(F(x0+5),F(5)),(F(x0),F(5))]

def trace(poly,P,d,target=None,stop=None,maxb=5000):
    """Billiard from P in direction d. Returns ('hit',travel_x) at target, ('stop',pt,d,travel_x)
    when the open segment `stop` (vertical x=c, y in (lo,hi)) is crossed, ('vertex',pt) or ('max',)."""
    V=set(poly); E=list(zip(poly,poly[1:]+poly[:1]))
    P=(F(P[0]),F(P[1])); dx,dy=map(F,d); ax=F(0)
    for _ in range(maxb):
        best=None
        for (a,b) in E:
            if a[0]==b[0] and dx!=0:
                t=(a[0]-P[0])/dx
                if t>0:
                    y=P[1]+t*dy
                    if min(a[1],b[1])<=y<=max(a[1],b[1]) and (best is None or t<best[0]): best=(t,'v')
            elif a[1]==b[1] and dy!=0:
                t=(a[1]-P[1])/dy
                if t>0:
                    x=P[0]+t*dx
                    if min(a[0],b[0])<=x<=max(a[0],b[0]) and (best is None or t<best[0]): best=(t,'h')
        t,kind=best; Q=(P[0]+t*dx,P[1]+t*dy)
        if target is not None:
            tx=(target[0]-P[0]); ty=(target[1]-P[1])
            # target on segment (P,Q]
            tt = tx/dx if dx else ty/dy
            if 0<tt<=t and P[0]+tt*dx==target[0] and P[1]+tt*dy==target[1]:
                return ('hit',ax+abs(tt*dx))
        if stop is not None and kind=='v' and Q[0]==stop[0] and stop[1]<Q[1]<stop[2]:
            return ('stop',Q,(dx,dy),ax+abs(t*dx))
        if Q in V: return ('vertex',Q)
        ax+=abs(t*dx); P=Q
        if kind=='v': dx=-dx
        else: dy=-dy
    return ('max',)

t0=time.process_time()
marks=list(product(range(1,5),repeat=2))
sc=F(1,10); h=F(1,450)
# leg data at central slope and both interval ends, for every mark (left chamber, right chamber by mirror)
def legL(m,s):  # from left mark rightward, upward, to door x=5,y in (2,3)
    return trace(square(0),m,(1,s),stop=(F(5),F(2),F(3)))
def legR(m,s,L):  # backward from right mark leftward, upward, to door x=5+L
    return trace([(x+5+L,y) for x,y in square(0)],(m[0]+5+L,m[1]),(-1,s),stop=(F(5+L),F(2),F(3)))
bad=0;maxa=0
for m in marks:
    r0=legL(m,sc)
    assert r0[0]=='stop'; maxa=max(maxa,r0[3])
    for s in (sc-h,sc+h):
        r=legL(m,s); assert r[0]=='stop' and r[3]==r0[3], (m,s,r)
print('left legs: 16/16 reach door at s in {1/10, 1/10±1/450} with same travel; max travel',maxa)
results={}
for L in (450,451,457,1000):
    ok=0;fails=[]
    for mS in marks:
        a_leg=legL(mS,sc); a=a_leg[3]; y1=a_leg[1][1]-2; e1=1 if a_leg[2][1]>0 else -1
        for mT in marks:
            T=(mT[0]+5+L,mT[1])
            b_leg=legR(mT,sc,L); b=b_leg[3]; y2=b_leg[1][1]-2; e2=-(1 if b_leg[2][1]>0 else -1)
            Fc=L*sc+e1*y1-e2*y2; slope=L+a+b
            lo,hi=Fc-slope*h,Fc+slope*h
            k=-(-lo//2)  # ceil(lo/2)
            assert 2*k<=hi,(L,mS,mT)
            s=sc+(2*k-Fc)/slope
            r=trace(room(L),mS,(1,s),target=T)
            if r[0]=='hit': ok+=1
            else: fails.append((mS,mT,r))
    results[L]=(ok,fails[:3]); print('L',L,'cross pairs lit by matched path:',ok,'/256',fails[:3])
# 3+6k replay of saved D72 directions (data only)
D=Path(sys.argv[1]); data=json.loads(D.read_text())['DB55']['pairs']
cross=[r for r in data if r['S'][0]<=4 and r['T'][0]>=9]
print('cross-chamber same-class records:',len(cross),'of',len(data))
for L in (3,9,15,21,4,5,6,7,8):
    ok=0
    for r in cross:
        (p,q),_=r['lit']; S=tuple(r['S']); T=(r['T'][0]+L-3,r['T'][1])
        if any(trace(room(L),S,(sg*p,sg*q),target=T,maxb=3000)[0]=='hit' for sg in (1,-1)): ok+=1
    print('L',L,'saved directions still light',ok,'/',len(cross))
print('CPU s',round(time.process_time()-t0,1))
