"""Check the open-neighborhood corollary: perturb a symmetric U room and marks
asymmetrically, replay each of the three reflection words, and test the contact sets."""
import sys, random
sys.argv=[sys.argv[0],'0','0']+sys.argv[1:]
exec(open('sim.py').read().split("random.seed")[0])
from fractions import Fraction as F
def gen(aL,M,aR,c,HL,HR):
    A=aL+M+aR; b=aL+M
    return [(F(0),F(0)),(A,F(0)),(A,HR),(b,HR),(b,c),(aL,c),(aL,HL),(F(0),HL)]
def wall_of(V,q):
    n=len(V)
    for i in range(n):
        a,b=V[i],V[(i+1)%n]
        if (a[0]==b[0]==q[0] and min(a[1],b[1])<q[1]<max(a[1],b[1])) or (a[1]==b[1]==q[1] and min(a[0],b[0])<q[0]<max(a[0],b[0])): return i
def refl(V,i,p):
    a,b=V[i],V[(i+1)%len(V)]
    return (2*a[0]-p[0],p[1]) if a[0]==b[0] else (p[0],2*a[1]-p[1])
def replay(V,s,t,word):
    img=t
    for i in reversed(word): img=refl(V,i,img)
    d=(img[0]-s[0],img[1]-s[1])
    cs,st=shoot(V,s,t,d,cap=len(word)+5)
    if st!='ok': return None
    if [wall_of(V,q) for q in cs]!=word: return None
    return cs
random.seed(int(sys.argv[3]) if len(sys.argv)>3 else 0)
def rq(lo,hi,den=97): return F(random.randint(1,den-1),den)*(hi-lo)+lo
ok=bad=lost=0
for _ in range(int(sys.argv[4]) if len(sys.argv)>4 else 300):
    a=rq(0,2);M=rq(0,2);H=rq(0,2);c=rq(0,H);x=rq(0,a);y=rq(c,H)
    if not y>c: continue
    paths=three(a,M,c,H,x,y); res=[shoot(*p) for p in paths]
    if any(r[1]!='ok' for r in res) or max(len(r[0]) for r in res)>400: continue
    V0=paths[0][0]; words=[[wall_of(V0,q) for q in r[0]] for r in res]
    for k in (3,5,8):
        g=min(x,a-x,y-c,H-y,c,M)/4
        e=lambda: g*F(random.randint(-1000,1000),1000*10**k)
        V=gen(a+e(),M+e(),a+e(),c+e(),H+e(),H+e())
        s=(x+e(),y+e()); t=(V[1][0]-x+e(),y+e())
        S=[replay(V,s,t,w) for w in words]
        if any(v is None for v in S): lost+=1; continue
        S=[set(v) for v in S]
        if S[0]&S[1]&S[2]: bad+=1; print('TRIPLE',a,M,c,H,x,y,k)
        else: ok+=1
print('perturbed ok',ok,'triple-common',bad,'word-lost (perturbation too big)',lost)
