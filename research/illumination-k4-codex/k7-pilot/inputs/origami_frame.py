"""Exact darkness decision for a room in the canonical 45-degree tiling.

The unfolding X of the room (8 copies under D4) is a square-tiled surface: it covers R^2/Z^2,
branched only over lattice points. Darkness of (S,T) means: in every primitive direction w, the
straight ray in X from a fixed lift of S meets a lift of a room corner before a lift of T.
Take A in SL2(Z) with A w = e1. The ray is then the horizontal ray on A.X, which runs along square
bottom edges through lower-left corners s, r(s), r^2(s), ... The labeled origami orbit under the
shears T:(r,u)->(r,u r^-1) and L:(r,u)->(r u^-1,u) is finite. Both shears keep each square's
lower-left corner, so the corner labels stay fixed. Hence there are finitely many checks, exactly.
Usage: origami_dark.py "x,y x,y ..." Sx,Sy Tx,Ty
"""
import sys
from fractions import Fraction as F
D4 = [((1,0),(0,1)),((0,-1),(1,0)),((-1,0),(0,-1)),((0,1),(-1,0)),
      ((1,0),(0,-1)),((-1,0),(0,1)),((0,1),(1,0)),((0,-1),(-1,0))]
def mul(g,h): return tuple(tuple(sum(g[i][k]*h[k][j] for k in range(2)) for j in range(2)) for i in range(2))
def ap(g,p): return (g[0][0]*p[0]+g[0][1]*p[1], g[1][0]*p[0]+g[1][1]*p[1])
def cls(p): return (p[0]&1)+(p[1]&1)  # 0 A, 2 B, 1 C

def build(V, S, T):
    n=len(V)
    if sum(V[i][0]*V[(i+1)%n][1]-V[(i+1)%n][0]*V[i][1] for i in range(n))<0: V=V[::-1]
    def inside(x,y):
        c=False
        for i in range(n):
            (ax,ay),(bx,by)=V[i],V[(i+1)%n]
            if (ay>y)!=(by>y) and x<ax+F(y-ay)*(bx-ax)/(by-ay): c=not c
        return c
    corners=set(V)
    xs=[p[0] for p in V]; ys=[p[1] for p in V]
    tris=[]
    for x in range(min(xs),max(xs)):
        for y in range(min(ys),max(ys)):
            c=[(x,y),(x+1,y),(x+1,y+1),(x,y+1)]
            k=[i for i in range(4) if cls(c[i])==0][0]  # A corner; B is opposite
            a,b=c[k],c[(k+2)%4]
            for o in (c[(k+1)%4],c[(k+3)%4]):
                cx,cy=F(a[0]+b[0]+o[0],3),F(a[1]+b[1]+o[1],3)
                if inside(cx,cy): tris.append((a,b,o))
    edge={}
    for i,t in enumerate(tris):
        for j in range(3):
            e=frozenset((t[j],t[(j+1)%3])); edge.setdefault(e,[]).append(i)
    def refl_lin(p,q):
        dx,dy=q[0]-p[0],q[1]-p[1]
        if dx==0: return ((-1,0),(0,1))
        if dy==0: return ((1,0),(0,-1))
        return ((0,1),(1,0)) if dx*dy>0 else ((0,-1),(-1,0))
    gi={g:i for i,g in enumerate(D4)}
    # X triangles: (i,g); neighbor across edge e
    def nb(i,g,e):
        o=[j for j in edge[e] if j!=i]
        if o: return (o[0],g)
        p,q=tuple(e); return (i,mul(g,refl_lin(p,q)))
    # squares: pair across A-B edge
    sq={}; sqs=[]
    for i,t in enumerate(tris):
        for g in D4:
            if (i,g) in sq: continue
            m=nb(i,g,frozenset((t[0],t[1])))
            sq[(i,g)]=sq[m]=len(sqs); sqs.append(((i,g),m))
    def dev(i,g): return [ap(g,v) for v in tris[i]]
    nS=len(sqs); r=[None]*nS; u=[None]*nS; lab=[None]*nS; sstart=None
    for s,(m1,m2) in enumerate(sqs):
        for (i,g) in (m1,m2):
            D=dev(i,g)  # each triangle in its own copy frame; frames differ by translations
            X0=min(p[0] for p in D); Y0=min(p[1] for p in D)
            for k in range(3):
                if D[k]==(X0,Y0):
                    v=tris[i][k]
                    lab[s]='block' if v in corners else ('T' if v==T else ('S' if v==S else '.'))
                    if v==S and sstart is None: sstart=s; source_frame=g
            for k in range(3):
                a,b=D[k],D[(k+1)%3]
                e=frozenset((tris[i][k],tris[i][(k+1)%3]))
                if a[0]==b[0]==X0+1: r[s]=sq[nb(i,g,e)]
                if a[1]==b[1]==Y0+1: u[s]=sq[nb(i,g,e)]
    assert None not in r and None not in u and None not in lab and sstart is not None
    return r,u,lab,sstart,source_frame

def inv(p):
    q=[0]*len(p)
    for i,x in enumerate(p): q[x]=i
    return q
def comp(p,q): return [p[q[i]] for i in range(len(q))]  # p after q

def canon(R,U,lab,s0):
    # relabel by BFS from the start square; labels and s0 ride along
    order=[s0]; idx={s0:0}; k=0
    while k<len(order):
        x=order[k]; k+=1
        for y in (R[x],U[x]):
            if y not in idx: idx[y]=len(order); order.append(y)
    return (tuple(idx[R[x]] for x in order), tuple(idx[U[x]] for x in order), tuple(lab[x] for x in order))

def decide(V,S,T,limit=5_000_000):
    r,u,lab,s0=build(V,S,T)
    start=canon(r,u,lab,s0); seen={start}; todo=[start]
    while todo:
        R,U,lab=todo.pop(); s0=0
        s=R[s0]
        while s!=s0:
            if lab[s]=='block': break
            if lab[s]=='T': return 'LIT', len(seen)
            s=R[s]
        Ri,Ui=inv(R),inv(U)
        for a,b in ((R,tuple(comp(U,Ri))),(tuple(comp(R,Ui)),U)):
            nxt=canon(a,b,lab,0)
            if nxt not in seen:
                seen.add(nxt); todo.append(nxt)
                if len(seen)>limit: return 'UNDECIDED', len(seen)
    return 'DARK', len(seen)

if __name__=='__main__':
    V=[tuple(map(int,s.split(','))) for s in sys.argv[1].split()]
    S=tuple(map(int,sys.argv[2].split(','))); T=tuple(map(int,sys.argv[3].split(',')))
    print(*decide(V,S,T))
