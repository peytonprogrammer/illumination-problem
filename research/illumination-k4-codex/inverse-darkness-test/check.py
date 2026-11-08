"""Exact replay of prescribed analytic fixtures; no trajectory discovery."""
from fractions import Fraction as Q
from pathlib import Path
import json

ROOT=Path(__file__).parent
V=[(Q(x),Q(y)) for x,y in [(0,0),(2,0),(2,1),(1,1),(1,2),(0,2)]]
E=list(zip(V,V[1:]+V[:1]))
S=(Q(3,2),Q(1,2)); T=(Q(1,2),Q(3,2)); C=(Q(1),Q(1))

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

def hits(a,v):
    out=[]
    for j,(c,d) in enumerate(E):
        w=sub(d,c); den=cross(v,w)
        if not den: continue
        t=cross(sub(c,a),w)/den; u=cross(sub(c,a),v)/den
        if t>0 and 0<=u<=1: out.append((t,j))
    return out

def replay(P,allow_corner=False):
    assert P[0]==S and P[-1]==T and inside(S) and inside(T)
    contacts=[]; corners=[]
    for i,(a,b) in enumerate(zip(P,P[1:])):
        v=sub(b,a)
        assert v!=(0,0)
        assert inside(tuple((a[k]+b[k])/2 for k in (0,1)))
        hh=hits(a,v)
        if i==len(P)-2:
            assert all(t>1 for t,j in hh)
            continue
        first=min(t for t,j in hh); walls=[j for t,j in hh if t==first]
        assert first==1,(i,b,first)
        outgoing=sub(P[i+2],b)
        if b in V:
            assert allow_corner and b==C and len(walls)==2
            # Prescribed straight singular continuation, never legal dynamics.
            assert cross(v,outgoing)==0 and dot(v,outgoing)>0
            corners.append(b)
        else:
            assert len(walls)==1
            c,d=E[walls[0]]; w=sub(d,c)
            r=tuple(2*dot(v,w)*w[k]/dot(w,w)-v[k] for k in (0,1))
            assert cross(r,outgoing)==0 and dot(r,outgoing)>0
            contacts.append({'point':b,'wall':walls[0]})
    return contacts,corners

def fold(z,b):
    r=z%(2*b)
    return r if r<=b else 2*b-r

def encode(v):
    if isinstance(v,Q): return str(v)
    if isinstance(v,dict): return {k:encode(x) for k,x in v.items()}
    if isinstance(v,(tuple,list)): return [encode(x) for x in v]
    return v

area=sum(cross(a,b) for a,b in E)/2
turns=[cross(sub(V[i],V[i-1]),sub(V[(i+1)%6],V[i])) for i in range(6)]
assert area==3 and sum(t<0 for t in turns)==1 and turns[3]<0
# The two constituent open rectangles establish the simple L geometry;
# independently exclude nonadjacent edge intersections.
for i,(a,b) in enumerate(E):
    for j,(c,d) in enumerate(E):
        if j<=i+1 or (i==0 and j==5): continue
        u=sub(b,a); w=sub(d,c); den=cross(u,w)
        if den:
            t=cross(sub(c,a),w)/den; q=cross(sub(c,a),u)/den
            assert not(0<=t<=1 and 0<=q<=1)
        elif cross(sub(c,a),u)==0:
            assert not(on(a,c,d) or on(b,c,d) or on(c,a,b) or on(d,a,b))

examples=[]
for k in (0,1,7):
    # These k are fixed controls of the already proved all-k formula.
    a=8*k+1
    lower=[(Q(0 if j%2==0 else 2),Q(1,2)+Q(3,2*a)+Q(2*j,a))
           for j in range(2*k)]
    upper=[(Q(0 if j%2==0 else 1),Q(1)+Q(1+j,a)) for j in range(4*k)]
    P=[S]+lower+[C]+upper+[T]
    contacts,corners=replay(P,allow_corner=True)
    assert len(contacts)==6*k and corners==[C]
    assert all(b[1]>v[1] for v,b in zip(P,P[1:]))
    assert all(abs((b[0]-v[0])/(b[1]-v[1]))==a for v,b in zip(P,P[1:]))
    for x,y in P:
        expected=(fold(Q(3,2)-a*(y-Q(1,2)),Q(2)) if y<=1
                  else fold(1-a*(y-1),Q(1)))
        assert x==expected
    target_image=(Q(1,2)-8*k,Q(3,2)); corner_image=(Q(1)-4*k,Q(1))
    assert corner_image==tuple((S[i]+target_image[i])/2 for i in (0,1))
    displacement=sub(target_image,S)
    assert displacement==(-a,1) and dot(displacement,displacement)==a*a+1
    assert fold(corner_image[0],Q(2))==1 and fold(target_image[0],Q(1))==T[0]
    examples.append({'k':k,'direction':(-a,1),'path':P,'smooth_reflections':len(contacts),
                     'singular_contacts':corners,'target_image':target_image,
                     'corner_image':corner_image,'length_squared':a*a+1})

legal=[S,(Q(0),Q(5,4)),T]
contacts,corners=replay(legal)
assert len(contacts)==1 and not corners
assert [dot(sub(b,a),sub(b,a)) for a,b in zip(legal,legal[1:])]==[Q(45,16),Q(5,16)]
assert sub(legal[1],S)==(Q(-3,2),Q(3,4))
assert sub(T,legal[1])==(Q(1,2),Q(1,4))
assert sum(b[1]-a[1] for a,b in zip(legal,legal[1:]))==1
assert S[0]+(1-S[1])*Q(-2)==Q(1,2)

# Exactly the four directions forced by squared length2; no other rays tested.
short_controls=[]
for direction,corner in [((1,1),(2,1)),((-1,1),(1,1)),((1,-1),(2,0))]:
    hh=hits(S,direction); first=min(t for t,j in hh)
    p=tuple(S[i]+first*direction[i] for i in (0,1))
    assert first==Q(1,2) and p==corner and p in V
    short_controls.append({'direction':direction,'corner':p,'time':first})
hh=hits(S,(-1,-1)); first=min(t for t,j in hh)
assert first==Q(1,2)
z=(Q(1),Q(0)); remaining=Q(1)-first
end=(z[0]-remaining,z[1]+remaining)
assert end==(Q(1,2),Q(1,2)) and end!=T
assert all(t>remaining for t,j in hits(z,(-1,1)))
short_controls.append({'direction':(-1,-1),'bounce':z,'time1_position':end})

result={'status':'PASS','scope':'Prescribed analytic family controls k0/1/7, explicit legal path, and four forced shorter-length directions. All-k theorem and minimal length use hand proof; no independent review.',
        'walls':6,'reflex_corners':1,'area':area,'source':S,'target':T,
        'singular_family_controls':examples,'legal_path':legal,
        'legal_reflections':len(contacts),'minimum_legal_length_squared':5,
        'shorter_length_controls':short_controls}
(ROOT/'check.json').write_text(json.dumps(encode(result),indent=2)+'\n')
print(json.dumps({'status':'PASS','family_controls':[r['k'] for r in examples],
                  'smooth_reflections':[r['smooth_reflections'] for r in examples],
                  'one_reflex_corner':True,'minimum_legal_length_squared':5,
                  'receipt':str(ROOT/'check.json')},indent=2))
