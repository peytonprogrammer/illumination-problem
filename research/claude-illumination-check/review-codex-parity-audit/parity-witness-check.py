"""Replay exactly Opus's supplied 42 contacts; no trajectory discovery."""
from fractions import Fraction as F
from collections import Counter, defaultdict
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent
SRC = ROOT.parents[1] / 'claude-illumination-check/b-not-in-k/certificate-3-2.log'
RING = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1),(1,0)]
def fan(c, ks):
    return [tuple([c]+[(c[0]+RING[j][0], c[1]+RING[j][1]) for j in (k,k+1)]) for k in ks]
# Independently transcribed from pocket-detection.md Section 33.
TRI = fan((-4,0),range(8))+fan((0,0),range(8))+fan((-2,0),range(4))+[
    ((-2,2),(-2,1),(-1,1)), ((2,0),(1,0),(1,1)),
    ((0,2),(0,1),(1,1)), ((0,2),(1,1),(1,2)),
    ((0,-2),(0,-1),(1,-1)), ((-6,0),(-5,0),(-5,1)),
    ((-4,2),(-4,1),(-3,1)), ((-4,-2),(-4,-1),(-5,-1))]
def sub(a,b): return (a[0]-b[0],a[1]-b[1])
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def cross(a,b): return a[0]*b[1]-a[1]*b[0]
def mv(A,x): return tuple(dot(r,x) for r in A)
def mm(A,B): return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)) for i in range(2))
I=((F(1),F(0)),(F(0),F(1)))
C=Counter(tuple(sorted((t[j],t[(j+1)%3]))) for t in TRI for j in range(3))
W=[e for e,n in C.items() if n==1]
ADJ=defaultdict(list)
for a,b in W: ADJ[a].append(b); ADJ[b].append(a)
assert all(len(v)==2 for v in ADJ.values())
CORNERS={p for p,v in ADJ.items() if cross(sub(v[0],p),sub(v[1],p))!=0}
def inside(p):
    for t in TRI:
        d=[cross(sub(t[(j+1)%3],t[j]),sub(p,t[j])) for j in range(3)]
        if min(d)>=0 or max(d)<=0: return True
    return False
D=((1,1),(2,0)); H=((1,0),(2,0))
def verify(points, velocity=(-3,-2)):
    z=(F(11,10),F(9,10)); initial=z
    v=tuple(map(F,velocity)); L=I; Q=(F(0),F(0)); hol=(F(0),F(0))
    dcount=hcount=0; portals=[]
    for step,p in enumerate(points):
        delta=sub(p,z)
        assert cross(delta,v)==0 and dot(delta,v)>0, ('direction',step)
        assert p not in CORNERS, ('corner',step)
        hits=[]
        for a,b in W:
            edge=sub(b,a); den=cross(delta,edge)
            if den==0:
                assert cross(sub(a,z),delta)!=0, ('wall gliding',step)
                continue
            t=cross(sub(a,z),edge)/den; u=cross(sub(a,z),delta)/den
            if 0<t<=1 and 0<=u<=1:
                assert t==1, ('earlier boundary',step)
                hits.append((a,b))
        assert len(hits)==1, ('unique contact',step,hits)
        assert inside(tuple((x+y)/2 for x,y in zip(z,p))), ('outside',step)
        if delta[0]:
            t=(1-z[0])/delta[0]
            y=z[1]+t*delta[1]
            if 0<t<1 and 0<y<1: portals.append(dict(point=[str(F(1)),str(y)],kind='entry' if delta[0]>0 else 'exit'))
        seg=hits[0]
        if seg in (D,H):
            a=(1,1) if seg==D else (0,2)
            q=mv(L,a); Q=tuple(x+y for x,y in zip(Q,q))
            dcount+=seg==D; hcount+=seg==H
        h=mv(L,delta); hol=tuple(x+y for x,y in zip(hol,h))
        e=sub(seg[1],seg[0]); n=dot(e,e)
        R=tuple(tuple(2*F(e[i]*e[j],n)-(i==j) for j in range(2)) for i in range(2))
        v=mv(R,v); L=mm(L,R); z=p
        if step<len(points)-1: assert not(z==initial and v==velocity and L==I), 'early closure'
    assert len(points)==42 and z==initial and v==velocity and L==I, 'full closure'
    assert dcount==1 and hcount==0 and all(q.denominator==1 for q in Q), 'moving contacts'
    assert tuple(int(q)%2 for q in Q)==(1,1), 'odd response'
    assert [c['point'] for c in portals if c['kind']=='entry']==[['1','3/4']], 'portal entry'
    assert [c['point'] for c in portals if c['kind']=='exit']==[['1','5/6']], 'portal exit'
    return dict(contacts=len(points),D_hits=dcount,H_hits=hcount,Q=list(map(str,Q)),holonomy=list(map(str,hol)),portal_crossings=portals,frame_closed=True)
raw=SRC.read_bytes()
line=raw.decode().splitlines()[1]
points=[tuple(F(s) for s in match) for match in re.findall(r'\(([-\d/]+),([-\d/]+)\)',line)]
result=verify(points)
controls=[]
for name,pts,vel in [
    ('moved contact',[ (points[0][0]+F(1,100),points[0][1]) ]+points[1:],(-3,-2)),
    ('deleted contact',points[:5]+points[6:],(-3,-2)),
    ('wrong initial velocity',points,(-3,-1)),
    ('reversed initial velocity',points,(3,2)),
]:
    try: verify(pts,vel)
    except AssertionError as e: controls.append(dict(name=name,rejected=True,reason=str(e)))
    else: raise AssertionError(('corruption accepted',name))
out=dict(status='PASS',scope='One supplied path only; no all-direction or universal claim',source=str(SRC),source_sha256=hashlib.sha256(raw).hexdigest(),script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),triangles=len(TRI),boundary_atomic_edges=len(W),maximal_walls=len(CORNERS),witness=result,corruption_controls=controls)
ROOT.joinpath('parity-witness-check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
