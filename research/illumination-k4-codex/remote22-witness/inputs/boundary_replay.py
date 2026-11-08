"""Direct unit-square geometry and exact actual-boundary path replay."""
from fractions import Fraction as F
from collections import defaultdict

def cross(a,b): return a[0]*b[1]-a[1]*b[0]
def sub(a,b): return a[0]-b[0],a[1]-b[1]
def dot(a,b): return a[0]*b[0]+a[1]*b[1]
def on(p,a,b): return cross(sub(p,a),sub(b,a))==0 and all(min(a[k],b[k])<=p[k]<=max(a[k],b[k]) for k in (0,1))
def inspect(cells,marks):
    cells=set(map(tuple,cells));assert cells
    seen={next(iter(cells))};queue=list(seen)
    for x,y in queue:
        for q in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
            if q in cells and q not in seen:seen.add(q);queue.append(q)
    assert seen==cells,'disconnected unit cells'
    edges=set()
    for x,y in cells:
        P=[(x,y),(x+1,y),(x+1,y+1),(x,y+1)]
        for a,b in zip(P,P[1:]+P[:1]):
            if (b,a) in edges:edges.remove((b,a))
            else:edges.add((a,b))
    out=defaultdict(list);inc=defaultdict(list)
    for a,b in edges:out[a].append(b);inc[b].append(a)
    assert set(out)==set(inc) and all(len(out[p])==len(inc[p])==1 for p in out),'boundary pinch'
    start=min(out);p=start;cyc=[];walk=set()
    while True:
        cyc.append(p);q=out[p][0];assert (p,q) not in walk
        walk.add((p,q));p=q
        if p==start:break
    assert walk==edges,'multiple boundaries'
    V=[p for i,p in enumerate(cyc) if cross(sub(p,cyc[i-1]),sub(cyc[(i+1)%len(cyc)],p))]
    assert sum(cross(a,b) for a,b in zip(V,V[1:]+V[:1]))==2*len(cells)
    points={(x+dx,y+dy) for x,y in cells for dx in (0,1) for dy in (0,1)}
    fullA=[];exceptions=[];smoothA=[];Q=0;J=0;sN=0
    for x,y in points:
        occupied={(dx,dy) for dx,dy in ((-1,-1),(0,-1),(-1,0),(0,0)) if (x+dx,y+dy) in cells}
        n=len(occupied)
        if n==2:
            a,b=occupied;assert a[0]==b[0] or a[1]==b[1],'diagonal point pinch'
        A=x%2==0 and y%2==0
        if A:
            if n==4:fullA.append((x,y))
            else:Q+={1:2,2:3,3:6}[n]
            if n==2:smoothA.append((x,y))
        elif n in (2,4):
            exceptions.append((x,y));J+=n==4;sN+=n==2
    assert all(tuple(p) in fullA for p in marks),'marks not interior A'
    W=len(V);I=len(fullA);k=len(exceptions)
    assert W==2+6*I+Q-2*J-sN
    assert 2*len(cells)==8*I+Q+len(smoothA)
    return {'vertices':V,'unit_squares':len(cells),'triangles':2*len(cells),'walls':W,
            'interior_A':sorted(fullA),'k':k,'J':J,'s_N':sN,'Q':Q,'s_A':len(smoothA),
            'exceptions':sorted(exceptions),'simple':True,'orthogonal':True}

def inside(p,V):
    E=list(zip(V,V[1:]+V[:1]))
    if any(on(p,a,b) for a,b in E):return False
    answer=False
    for a,b in E:
        if (a[1]>p[1])!=(b[1]>p[1]):
            x=a[0]+F(p[1]-a[1])*(b[0]-a[0])/(b[1]-a[1])
            if p[0]<x:answer=not answer
    return answer

def replay(V,S,T,path):
    P=[tuple(map(F,p)) for p in path];S=tuple(S);T=tuple(T)
    assert P[0]==S and P[-1]==T and inside(S,V) and inside(T,V)
    E=list(zip(V,V[1:]+V[:1]))
    for i,(a,b) in enumerate(zip(P,P[1:])):
        v=sub(b,a);assert v!=(0,0)
        assert inside(tuple((a[k]+b[k])/2 for k in (0,1)),V)
        hits=[]
        for j,(c,d) in enumerate(E):
            w=sub(d,c);den=cross(v,w)
            if not den:continue
            t=cross(sub(c,a),w)/den;u=cross(sub(c,a),v)/den
            if t>0 and 0<=u<=1:hits.append((t,j))
        # Target must not occur earlier than the declared terminal point.
        if on(T,a,b):assert i==len(P)-2 and T==b,'earlier target'
        if i==len(P)-2:
            assert all(t>1 for t,j in hits);continue
        first=min(t for t,j in hits);js=[j for t,j in hits if t==first]
        assert first==1 and len(js)==1 and b not in V,'non-smooth/early contact'
        c,d=E[js[0]];w=sub(d,c)
        r=tuple(2*dot(v,w)*w[k]/dot(w,w)-v[k] for k in (0,1))
        nxt=sub(P[i+2],b)
        assert cross(r,nxt)==0 and dot(r,nxt)>0,'bad reflection'
    return len(P)-2
