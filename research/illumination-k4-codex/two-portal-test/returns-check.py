"""Exact affine-interval checks and replay of one analytically prescribed path.
No slope/room/word discovery. Parameter partitioning checks supplied formulas.
"""
from fractions import Fraction as Q
from pathlib import Path
import json

ROOT = Path(__file__).parent

def f(x): return Q(str(x))
def fold(z):
    r = z % 2
    return r if r <= 1 else 2-r

def enc(v):
    if isinstance(v, Q): return str(v)
    if isinstance(v, dict): return {k:enc(x) for k,x in v.items()}
    if isinstance(v, (list,tuple)): return [enc(x) for x in v]
    return v

# On the open e interval, partition an affine phase only at its exact fold
# breakpoints, then recover each affine branch and closed endpoint range.
def pieces(c,d,lo,hi):
    zlo,zhi=sorted((c+d*lo,c+d*hi))
    cuts={lo,hi}
    if d:
        for k in range(zlo.numerator//zlo.denominator,
                       zhi.numerator//zhi.denominator+2):
            e=(Q(k)-c)/d
            if lo<e<hi: cuts.add(e)
    cuts=sorted(cuts); out=[]
    for left,right in zip(cuts,cuts[1:]):
        mid=(left+right)/2
        z=c+d*mid; k=z.numerator//z.denominator
        s=1 if k%2==0 else -1
        b=-k if s==1 else k+1
        low,high=sorted((s*(c+d*left)+b,s*(c+d*right)+b))
        out.append((left,right,s*c+b,s*d,low,high,s))
    return out

rows=[
    ('A7-',Q(1,2),7,Q(1,20),Q(3,40),-1,Q(-13,20),Q(17,2)),
    ('A7+',Q(1,2),7,Q(3,40),Q(1,10),1,Q(21,20),Q(-17,2)),
    ('A11-',Q(1,2),11,Q(1,25),Q(1,20),-1,Q(-13,20),Q(25,2)),
    ('B5-',Q(-1,2),5,Q(1,15),Q(1,10),-1,Q(-3,20),Q(13,2)),
    ('B9-',Q(-1,2),9,Q(1,25),Q(3,50),-1,Q(-3,20),Q(21,2)),
    ('B9+',Q(-1,2),9,Q(3,50),Q(1,15),1,Q(11,20),Q(-21,2)),
]
expected_ranges=[(Q(-9,40),Q(-1,80)),(Q(1,5),Q(33,80)),
                 (Q(-3,20),Q(-1,40)),(Q(17,60),Q(1,2)),
                 (Q(27,100),Q(12,25)),(Q(-3,20),Q(-2,25))]
receipts=[]
for row,want in zip(rows,expected_ranges):
    name,pc,N,lo,hi,s,c,d=row
    phase_receipts=[]
    for n in range(1,N+1):
        # q+n*p = 1/10+n*pc-(n+1)*e, modulo 2mn.
        pp=pieces(Q(1,10)+n*pc,-Q(n+1),lo,hi)
        for left,right,xc,xd,xlo,xhi,derivative in pp:
            # No internal phase breakpoint: x=0/1 would be a side corner.
            assert left==lo and right==hi,(name,n,'internal corner')
            assert 0<=xlo<xhi<=1,(name,n,xlo,xhi)
            if n<N and n%2:
                assert xhi<=Q(4,5),(name,n,'early upper exit')
            elif n<N:
                assert xlo>=Q(1,10),(name,n,'early lower exit')
            else:
                assert n%2 and xlo>=Q(4,5) and derivative==s
                # u=xc+xd*e-4/5+(s/2)*(pc-e+2m).
                assert xc-Q(4,5)+s*pc/2==c and xd-Q(s,2)==d
            phase_receipts.append({'n':n,'x_range':(xlo,xhi)})
    urange=tuple(sorted((c+d*lo,c+d*hi)))
    assert urange==want
    # All six ranges lie strictly between consecutive half-integers;
    # endpoints are not attained because e interval is open.
    assert Q(-1,2)<=urange[0]<urange[1]<=Q(1,2)
    receipts.append({'row':name,'e_open':(lo,hi),'N':N,'sign':s,
                     'u_mod_integer_open':urange,'crossings':phase_receipts})

# Coverage of excluded small e: neither first top approach can exit;
# if it survives until n4, it is in the bottom opening or at a corner.
for pc in (Q(1,2),Q(-1,2)):
    for n in (1,3):
        for piece in pieces(Q(1,10)+n*pc,-Q(n+1),Q(0),Q(1,25)):
            assert piece[5]<Q(4,5)
    for piece in pieces(Q(1,10)+4*pc,-Q(5),Q(0),Q(1,25)):
        assert 0<=piece[4] and piece[5]<=Q(1,10)

# Every interior boundary omitted from the six rows is a first corner,
# never a missing valid itinerary.
boundaries=[(Q(1,2),Q(1,25),4),(Q(1,2),Q(1,20),7),
            (Q(1,2),Q(3,40),7),(Q(-1,2),Q(1,25),4),
            (Q(-1,2),Q(1,15),5),(Q(-1,2),Q(3,50),9)]
for pc,e,nstop in boundaries:
    q=Q(1,10)-e; p=pc-e
    for n in range(1,nstop):
        x=fold(q+n*p)
        assert 0<x<1
        assert x<Q(4,5) if n%2 else x>Q(1,10)
    x=fold(q+nstop*p)
    assert x in ((Q(0),Q(4,5),Q(1)) if nstop%2 else (Q(0),Q(1,10),Q(1)))

# Both source-unfolding signs, with arbitrary symbolic integer image m.
# A: initial rho=2m+1/2-e; .5+rho=2m+(q+.9).
# B: initial rho=-p; .5-p=2(1-m)-(q+.9).
for name,pc,*_ in rows:
    e=Q(13,190); q=Q(1,10)-e; p=pc-e
    if name.startswith('A'):
        assert Q(1,2)+p==q+Q(9,10)
    else:
        assert Q(1,2)-p==2-(q+Q(9,10))

# Independent direct boundary geometry, based on the previously frozen fixture.
old=json.loads((ROOT/'check.json').read_text())
V=[tuple(map(Q,v)) for v in old['vertices']]
E=list(zip(V,V[1:]+V[:1]))
S=(Q(-2,5),Q(1)); T=(Q(13,10),Q(7,2))
P=[S,(Q(44,95),Q(3)),(Q(17,19),Q(2)),(Q(1),Q(92,41)),
   (Q(64,95),Q(3)),(Q(23,95),Q(2)),(Q(0),Q(105,41)),
   (Q(18,95),Q(3)),(Q(59,95),Q(2)),(Q(1),Q(118,41)),
   (Q(4,5),Q(137,41)),(Q(103,95),Q(4)),T]

def sub(a,b): return a[0]-b[0],a[1]-b[1]
def cross(a,b): return a[0]*b[1]-a[1]*b[0]
def dot(a,b): return a[0]*b[0]+a[1]*b[1]
def on(p,a,b):
    return cross(sub(p,a),sub(b,a))==0 and all(min(a[k],b[k])<=p[k]<=max(a[k],b[k]) for k in (0,1))
def inside(p):
    if any(on(p,a,b) for a,b in E): return False
    parity=False
    for a,b in E:
        if (a[1]>p[1])!=(b[1]>p[1]):
            x=a[0]+(p[1]-a[1])*(b[0]-a[0])/(b[1]-a[1])
            if p[0]<x: parity=not parity
    return parity
assert inside(S) and inside(T)
contacts=[]; crossings=[]
for i,(a,b) in enumerate(zip(P,P[1:])):
    v=sub(b,a); hits=[]
    for j,(c,d) in enumerate(E):
        w=sub(d,c); den=cross(v,w)
        if not den: continue
        t=cross(sub(c,a),w)/den; u=cross(sub(c,a),v)/den
        if t>0 and 0<=u<=1: hits.append((t,j))
    assert inside(tuple((a[k]+b[k])/2 for k in (0,1)))
    assert abs(v[0]/v[1])==Q(41,95)
    if i==len(P)-2:
        assert all(t>1 for t,j in hits)
    else:
        first=min(t for t,j in hits); walls=[j for t,j in hits if t==first]
        assert first==1 and len(walls)==1 and b not in V,(i,first,walls)
        c,d=E[walls[0]]; w=sub(d,c)
        r=tuple(2*dot(v,w)*w[k]/dot(w,w)-v[k] for k in (0,1))
        outgoing=sub(P[i+2],b)
        assert cross(r,outgoing)==0 and dot(r,outgoing)>0
        contacts.append({'point':b,'wall':walls[0]})
    for y,lo,hi in [(Q(2),Q(0),Q(1,10)),(Q(3),Q(4,5),Q(1))]:
        if min(a[1],b[1])<y<max(a[1],b[1]):
            x=a[0]+(y-a[1])*v[0]/v[1]
            if lo<x<hi: crossings.append((x,y))
assert len(contacts)==11
assert crossings==[(Q(3,95),Q(2)),(Q(18,19),Q(3))]
assert sub(P[1],S)[1]>0 and cross(sub(P[1],S),(41,95))==0
# Solve the target equation, rather than select a tested direction.
e=(Q(23,20)-Q(1,2))/Q(19,2)
assert e==Q(13,190) and Q(1,20)<e<Q(3,40)
assert Q(1,2)-e==Q(41,95) and Q(1,10)-e==Q(3,95)
assert Q(-23,20)+Q(19,2)*e==Q(-1,2)
# Exact middle map agrees with all supplied horizontal arrivals.
assert [fold(Q(3,95)+n*Q(41,95)) for n in range(1,8)]==[
    Q(44,95),Q(17,19),Q(64,95),Q(23,95),Q(18,95),Q(59,95),Q(18,19)]
result={'status':'PASS','scope':'Six supplied whole open affine intervals and one analytically derived11-reflection path; no discovery search or independent review.',
        'interval_rows':receipts,'excluded_interior_boundaries':boundaries,
        'new_target':T,'path':P,'reflections':len(contacts),'contacts':contacts,
        'portal_crossings':crossings,'direction':(41,95),'e':e,
        'first_ascent_center_exclusion':True,'maximum_middle_crossing_N':11}
(ROOT/'returns-check.json').write_text(json.dumps(enc(result),indent=2)+'\n')
print(json.dumps({'status':'PASS','interval_rows':len(rows),'boundary_cases':len(boundaries),
                  'reflections':len(contacts),'target':enc(T),'receipt':str(ROOT/'returns-check.json')},indent=2))
