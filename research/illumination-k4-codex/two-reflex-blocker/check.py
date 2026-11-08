"""Exact prescribed U-room controls. No direction, word, or room search."""
from fractions import Fraction as F
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent

def cross(a,b): return a[0]*b[1]-a[1]*b[0]
def sub(a,b): return (a[0]-b[0],a[1]-b[1])
def fold(y,h):
    r=y%(2*h)
    return min(r,2*h-r)

# Fixed geometry: arms [0,2] and [3,5], height1, passage height1/10.
c=F(1,10)
polygon=[(F(x),F(y)) for x,y in [(0,0),(5,0),(5,1),(3,1),(3,c),(2,c),(2,1),(0,1)]]

def inside(p):
    x,y=p
    return 0<x<5 and 0<y<1 and (y<c or x<2 or x>3)

def verify_path(path, a=F(2), M=F(1), H=F(1), height=F(1,10), right_width=None, right_height=None):
    """All boundary intersections, open segment intervals and reflection law."""
    width_R=a if right_width is None else right_width
    height_R=H if right_height is None else right_height
    A=a+M+width_R; arm_left=a; arm_right=a+M; b=arm_right
    height_L=H
    polygon=[(F(0),F(0)),(A,F(0)),(A,height_R),(b,height_R),(b,height),(a,height),(a,height_L),(F(0),height_L)]
    def inside(p):
        x,y=p
        return 0<x<A and y>0 and (y<height or (x<arm_left and y<height_L) or (x>arm_right and y<height_R))
    checks=0
    for i,(p,q) in enumerate(zip(path,path[1:])):
        d=sub(q,p); ts={F(0),F(1)}
        for a,b in zip(polygon,polygon[1:]+polygon[:1]):
            e=sub(b,a); den=cross(d,e)
            if den==0:
                assert cross(sub(a,p),d)!=0, 'collinear with a wall line'
                continue
            t=cross(sub(a,p),e)/den; u=cross(sub(a,p),d)/den
            if 0<=t<=1 and 0<=u<=1:
                assert t in (0,1), ('unexpected wall intersection',i,t,u)
                assert 0<u<1, ('corner contact',i,t,u)
                ts.add(t); checks+=1
        cuts=sorted(ts)
        for lo,hi in zip(cuts,cuts[1:]):
            t=(lo+hi)/2
            assert inside((p[0]+t*d[0],p[1]+t*d[1]))
    for p,q,r in zip(path,path[1:],path[2:]):
        inc=sub(q,p); out=sub(r,q)
        on=[]
        for a,b in zip(polygon,polygon[1:]+polygon[:1]):
            if cross(sub(q,a),sub(b,a))==0 and min(a[0],b[0])<=q[0]<=max(a[0],b[0]) and min(a[1],b[1])<=q[1]<=max(a[1],b[1]): on.append((a,b))
        assert len(on)==1
        a,b=on[0]
        reflected=(-inc[0],inc[1]) if a[0]==b[0] else (inc[0],-inc[1])
        assert cross(reflected,out)==0 and sum(x*y for x,y in zip(reflected,out))>0
    return checks

# Fixed x-monotone path: Y_s=Y_t=2/5, sigma=-1,k=-1.
y=F(2,5); lam=F(-1,3); u=y+lam; v=-(y+2*lam+2*c)
assert u==v==F(1,15)
mono=[(F(1),y),(F(11,5),F(0)),(F(5,2),c),(F(14,5),F(0)),(F(4),y)]
mono_checks=verify_path(mono)

# Prescribed bypass with two outer-wall bounces and one bottom bounce.
bypass=[(F(1),y),(F(0),F(2,7)),(F(5,2),F(0)),(F(5),F(2,7)),(F(4),y)]
bypass_checks=verify_path(bypass)
z=(F(5,2),c)
for p,q in zip(bypass,bypass[1:]): assert cross(sub(z,p),sub(q,p))!=0

# The two signs on each image give these complete residue classes modulo2.
no_path_residues=sorted({(es*F(1,3)+et*F(2,3))%2 for es in (-1,1) for et in (-1,1)})
assert min(min(r,2-r) for r in no_path_residues)==F(1,3)>2*c
blocked_residues=sorted({(es*y+et*y)%2 for es in (-1,1) for et in (-1,1)})
assert blocked_residues==[0,F(4,5),F(6,5)]
# For sigma=-1, only zero invariant is possible; Y_s=Y_t.
# 0 < 10Y_s+2k <3, an even integer, forces2; k=1-(+/-2)-10n is odd.
assert all((1-sign*2)%2==1 for sign in (-1,1))

# Four fixed instances of the real-parameter symmetric construction.
# n follows a closed formula; no candidate directions or words are tried.
symmetric_controls=[]
for a,M,x,y,H,height in [
    (F(2),F(1),F(1),F(2,5),F(1),F(1,10)),
    (F(2),F(1),F(1),F(2,5),F(1),F(1,1000)),
    (F(1),F(1,10),F(1,4),F(1,2),F(1),F(1,5)),
    (F(3,2),F(7,3),F(2,7),F(9,10),F(2),F(1,20))]:
    L0=a-x; threshold=M*(y/height-1)/2
    n=max(0,(threshold-L0)//(2*a)+1)
    L=L0+2*n*a; beta=2*y/(2*L+M); portal=y-beta*L
    assert 0<portal<height
    if n: assert y-beta*(L-2*a)>height
    left=[(x,y)]+[(a if j%2 else F(0),y-beta*(j*a-x)) for j in range(1,2*n+1)]
    A=2*a+M
    path=left+[(A/2,F(0))]+[(A-px,py) for px,py in reversed(left)]
    contacts=verify_path(path,a,M,H,height)
    symmetric_controls.append(dict(n=n,portal=str(portal),reflections=len(path)-2,wall_incidence_checks=contacts))

def first_length(a,x,T,phase):
    ell=a-x if phase=='minus' else a+x
    n=max(0,(T-ell)//(2*a)+1)
    return ell+2*n*a,n

def prescribed_path(a,M,x,y,H,height,mode,phase,L,n):
    h=M/2; A=2*a+M
    beta=y/(L+h) if mode=='bottom' else (y+height)/(L+h)
    if phase=='minus':
        events=[(j*a-x,a if j%2 else F(0)) for j in range(1,2*n+1)]
        direction=1
    else:
        events=[(x+j*a,F(0) if j%2==0 else a) for j in range(2*n+1)]
        direction=-1
    vertices=[(d,px,abs(y-beta*d)) for d,px in events]
    if mode=='notch':
        bottom_d=y/beta
        assert bottom_d!=L and all(bottom_d!=d for d,px in events)
        px=fold(x+direction*bottom_d,a) if bottom_d<L else a+bottom_d-L
        vertices.append((bottom_d,px,F(0)))
    vertices.sort()
    left=[(x,y)]+[(px,py) for d,px,py in vertices]
    center=(A/2,F(0) if mode=='bottom' else height)
    path=left+[center]+[(A-px,py) for px,py in reversed(left)]
    incidence=verify_path(path,a,M,H,height)
    return path,incidence

def on_segment(z,p,q):
    return cross(sub(z,p),sub(q,p))==0 and all(min(p[d],q[d])<=z[d]<=max(p[d],q[d]) for d in (0,1))

three_path_controls=[]
fixtures=[
    ('ordinary',F(2),F(1),F(1),F(2,5),F(1),F(1,10)),
    ('thin-passage',F(2),F(1),F(1),F(2,5),F(1),F(1,1000)),
    ('notch-minus-resonance',F(2),F(1),F(1),F(1,5),F(1),F(1,10)),
    ('notch-plus-resonance',F(2),F(1),F(1),F(3,5),F(1),F(1,10)),
    ('near-passage-height',F(1),F(1,3),F(2,5),F(101,100),F(2),F(1)),
    ('short-notch',F(1),F(1,100),F(1,4),F(1,2),F(1),F(1,5)),
    ('long-notch',F(3,2),F(40),F(2,7),F(9,10),F(2),F(1,20)),
    ('rational-offset',F(3,2),F(7,3),F(2,7),F(9,10),F(2),F(1,20))]
for label,a,M,x,y,H,height in fixtures:
    h=M/2; Y=y/height; T=h*(Y-1)
    lengths=[first_length(a,x,T,phase) for phase in ('minus','plus')]
    assert 0<abs(lengths[0][0]-lengths[1][0])<2*a
    bottom=[]; contacts=0
    for phase,(L,n) in zip(('minus','plus'),lengths):
        path,count=prescribed_path(a,M,x,y,H,height,'bottom',phase,L,n)
        bottom.append(path); contacts+=count
    center=((2*a+M)/2,F(0))
    assert set(bottom[0][1:-1])&set(bottom[1][1:-1])=={center}
    TN=T/2; K=h*Y
    minus=first_length(a,x,TN,'minus'); plus=first_length(a,x,TN,'plus')
    phase,(L,n)=('minus',minus) if minus[0]!=K else ('plus',plus)
    assert L!=K and TN<L<=TN+2*a
    notch,count=prescribed_path(a,M,x,y,H,height,'notch',phase,L,n)
    assert all(not on_segment(center,p,q) for p,q in zip(notch,notch[1:]))
    contacts+=count
    assert not(set(bottom[0][1:-1])&set(bottom[1][1:-1])&set(notch[1:-1]))
    three_path_controls.append(dict(label=label,bottom_lengths=[str(v[0]) for v in lengths],
        notch_phase=phase,notch_length=str(L),discarded_resonance=minus[0]==K,
        reflections=[len(path)-2 for path in bottom]+[len(notch)-2],wall_incidence_checks=contacts))

result=dict(status='PASS' , method='fixed rational constructions and complete finite sign residues; no search',
    no_monotone_case=dict(source_y='1/3',target_y='2/3',minimum_invariant_distance='1/3',window_bound='1/5'),
    forced_blocker_case=dict(source_y='2/5',target_y='2/5',portal_height='1/15',central_k_parity='odd',blocker=['5/2','1/10']),
    monotone_path=[[str(x),str(y)] for x,y in mono],
    bypass_path=[[str(x),str(y)] for x,y in bypass],
    wall_incidence_checks=mono_checks+bypass_checks, symmetric_controls=symmetric_controls, three_path_controls=three_path_controls)
(HERE/'check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
