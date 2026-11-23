"""Solve one-seam placement on the original D72 witness charts, using integer arithmetic."""
from contextlib import redirect_stdout
from functools import lru_cache
from itertools import product
from math import gcd
from pathlib import Path
import io
import runpy

with redirect_stdout(io.StringIO()):
    prev=runpy.run_path(str(Path(__file__).with_name('convex-cylinder.py')))
cyl=prev['cyl']


def chart_graph(O,v):
    charts=prev['charts'](O,v)
    r,u=cyl.act(O.r,O.u,cyl.word(*v))
    edges=[]
    # charts() iterates its set of cut row indices; preserve that exact order.
    rows=cyl.cycles(r)
    cut={i for i,row in enumerate(rows) if any(cyl.incid(O.cells,O.ll[s])==3 for s in row)}
    bottoms=[rows[i] for i in cut]
    positions={s:(j,f) for j,row in enumerate(bottoms) for f,s in enumerate(row)}
    for i,(row,chart) in enumerate(zip(bottoms,charts)):
        H=max(y for ps in chart[1].values() for _,y in ps)
        top=row[:]
        for _ in range(H): top=[u[s] for s in top]
        for e,s in enumerate(top):
            j,f=positions[s]
            edges.append((i,j,H,e,f,not O.marked[s]))
    return charts,edges


def blocked(chart,x,y,d,h,end_y):
    return any(min(y,end_y)<b<max(y,end_y) and
               ((x-a)*h+(b-y)*d)%(chart[0]*h)==0 for a,b in chart[2])


def crossing(left,right,H,e,f,allow_start,S,T):
    C,D=left[0],right[0]
    for (x,y),(z,b) in product(left[1].get(S,()),right[1].get(T,())):
        a=H-y
        if a<=0 or b<=0: continue
        h=a+b
        for I,J in product(range(2),repeat=2):
            d0=e-x+z-f+C*I+D*J
            if d0%2 or h%2 or d0%4==h%4==0: continue
            u0=a*(z-f+D*J)-b*(e-x+C*I)
            P,Q=2*b*C,2*a*D
            g=gcd(P,Q)
            start=u0%g
            if start==0 and not allow_start: start+=g
            for U in range(start,h,g):
                # Q*j-P*i=U-u0 after fixing parities of both windings.
                mod=P//g
                j=((U-u0)//g*pow(Q//g,-1,mod))%mod if mod!=1 else 0
                i=(Q*j-(U-u0))//P
                d=d0+2*C*i+2*D*j
                step=2*C*(Q//g)+2*D*(P//g)
                for k in range(4):
                    dx=d+k*step
                    if not blocked(left,x,y,dx,h,H) and not blocked(right,z,b,dx,h,0):
                        return dx,h
    return None


def solve(graph,S,T):
    charts,edges=graph
    for i,j,H,e,f,allow in edges:
        for start,target in ((S,T),(T,S)):
            vec=crossing(charts[i],charts[j],H,e,f,allow,start,target)
            if vec:return vec
    return None


for name,report in prev['data'].items():
    if report['group']!='BBBB':continue
    O=cyl.Origami(prev['rooms'][name])
    graph=lru_cache(None)(lambda v:chart_graph(O,v))
    extra=[]; residual=[]
    for pair in report['pairs']:
        S,T=tuple(pair['S']),tuple(pair['T'])
        vs=[tuple(pair[label][0]) for label in ('cc','lit')]
        if prev['old_test'](O,S,T,pair) or any(prev['on_saved_leaf'](O,S,T,v) or
                any(prev['midpoint_witness'](c,S,T) for c in graph(v)[0]) for v in vs):continue
        for v in vs:
            vec=solve(graph(v),S,T)
            if vec:
                physical=prev['verify_displacement'](O.cells,S,T,prev['orig'](vec,v))
                extra.append((S,T,v,physical))
                break
        else:residual.append((S,T))
    print(name,'additional',len(extra),'residual',len(residual))
    if extra: print('example',extra[0])
    if residual:print('residual pairs',residual)

# The three residual pairs lie across one rectangular doorway or are direct.
O=cyl.Origami(prev['rooms']['DBw2'])
for S,T,vec in [((2,2),(6,2),(4,14)),((12,2),(8,2),(-4,10)),((8,2),(12,4),(4,2))]:
    end,ok,hits=prev['trace'](O.cells,S,vec)
    assert ok and end==T
    mid=hits[len(hits)//2-1]
    assert any((a-b)%2 for a,b in zip(S,mid))
    print('DBw2 explicit',S,T,vec,'midpoint',mid)
