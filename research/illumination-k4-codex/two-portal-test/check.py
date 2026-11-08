"""Exact checks of one analytically specified room/path; no discovery loops."""
from fractions import Fraction as F
from pathlib import Path
import json

def pt(x,y): return F(x),F(y)
def sub(a,b): return a[0]-b[0],a[1]-b[1]
def cross(a,b): return a[0]*b[1]-a[1]*b[0]
def dot(a,b): return a[0]*b[0]+a[1]*b[1]
def sign(a): return (a>0)-(a<0)
def encode(value):
    if isinstance(value,F): return str(value)
    if isinstance(value,(tuple,list)): return [encode(x) for x in value]
    if isinstance(value,dict): return {k:encode(v) for k,v in value.items()}
    return value
V=[pt('-9/10',0),pt('1/10',0),pt('1/10',2),pt(1,2),pt(1,3),pt('9/5',3),pt('9/5',4),pt('4/5',4),pt('4/5',3),pt(0,3),pt(0,2),pt('-9/10',2)]
S=pt('-2/5',1); T=pt('47/50','7/2')
P=[S,pt('12/25',3),pt('23/25',2),pt(1,'24/11'),pt('16/25',3),pt('1/5',2),pt(0,'27/11'),pt('6/25',3),pt('17/25',2),pt(1,'30/11'),pt('4/5','35/11'),T]
E=list(zip(V,V[1:]+V[:1]))

def on(p,a,b): return cross(sub(p,a),sub(b,a))==0 and all(min(a[k],b[k])<=p[k]<=max(a[k],b[k]) for k in (0,1))
def meet(a,b,c,d):
    # Closed intersections, including collinear contacts.
    v=sub(b,a); w=sub(d,c); den=cross(v,w)
    if not den: return cross(sub(c,a),v)==0 and (on(a,c,d) or on(b,c,d) or on(c,a,b) or on(d,a,b))
    t=cross(sub(c,a),w)/den; u=cross(sub(c,a),v)/den
    return 0<=t<=1 and 0<=u<=1
for i,(a,b) in enumerate(E):
    assert a!=b and ((a[0]==b[0]) != (a[1]==b[1]))
    for j,(c,d) in enumerate(E):
        if j<=i or j==i+1 or (i==0 and j==len(E)-1): continue
        assert not meet(a,b,c,d),(i,j)
turns=[sign(cross(sub(V[i],V[i-1]),sub(V[(i+1)%len(V)],V[i]))) for i in range(len(V))]
assert all(turns)
area=sum(cross(a,b) for a,b in E)/2
assert area==4 and turns.count(-1)==4 and turns.count(1)==8

def inside(p):
    if any(on(p,a,b) for a,b in E): return False
    result=False
    for a,b in E:
        if (a[1]>p[1])!=(b[1]>p[1]):
            x=a[0]+(p[1]-a[1])*(b[0]-a[0])/(b[1]-a[1])
            if p[0]<x: result=not result
    return result
assert inside(S) and inside(T)
contacts=[]
for i,(a,b) in enumerate(zip(P,P[1:])):
    v=sub(b,a); hits=[]
    for j,(c,d) in enumerate(E):
        w=sub(d,c); den=cross(v,w)
        if not den: continue
        t=cross(sub(c,a),w)/den; u=cross(sub(c,a),v)/den
        if t>0 and 0<=u<=1: hits.append((t,j))
    assert inside(((a[0]+b[0])/2,(a[1]+b[1])/2)),(i,'outside')
    if i==len(P)-2:
        assert all(t>1 for t,j in hits),(i,'premature')
        continue
    assert hits
    first=min(t for t,j in hits); js=[j for t,j in hits if t==first]
    assert first==1 and len(js)==1,(i,first,js)
    assert b not in V
    c,d=E[js[0]]; wall=sub(d,c)
    reflected=tuple(2*dot(v,wall)*wall[k]/dot(wall,wall)-v[k] for k in (0,1))
    following=sub(P[i+2],b)
    assert cross(reflected,following)==0 and dot(reflected,following)>0,(i,'reflection')
    contacts.append({'point':b,'edge':js[0]})
assert len(contacts)==10 and cross(sub(P[1],S),(11,25))==0
# Every fixed segment has constant absolute slope 11/25.
assert all(abs((b[0]-a[0])/(b[1]-a[1]))==F(11,25) for a,b in zip(P,P[1:]))
# Exact interval algebra after eliminating the arbitrary integer bounce count.
qlo,qhi=F(0),F(1,10)
# At first portal q is strictly between these endpoints.
# Incoming-sheet sign + gives F_1(2q+2/5)=2q+2/5.
# Sign - gives F_1(2q+7/5)=3/5-2q.
branches=[{'sign':1,'slope':F(2),'offset':F(2,5),'unfolded_range':(F(2,5),F(3,5))},
          {'sign':-1,'slope':F(-2),'offset':F(3,5),'unfolded_range':(F(7,5),F(8,5))}]
for branch in branches:
    values=sorted(branch['slope']*q+branch['offset'] for q in (qlo,qhi))
    assert values==[F(2,5),F(3,5)]
assert F(3,5)<F(4,5)
# Extract all crossings of the two specified horizontal passage levels.
passages=[]
for y,lo,hi in [(F(2),F(0),F(1,10)),(F(3),F(4,5),F(1))]:
    for i,(a,b) in enumerate(zip(P,P[1:])):
        if (a[1]<y<b[1]) or (b[1]<y<a[1]):
            t=(y-a[1])/(b[1]-a[1]); x=a[0]+t*(b[0]-a[0])
            if lo<x<hi: passages.append({'level':y,'point':(x,y),'segment':i})
assert [p['point'] for p in passages]==[pt('1/25',2),pt('22/25',3)]
result={'status':'PASS','scope':'One prescribed fixed room and one hand-derived path, plus exact branch interval identities. No room/ray/direction/word search; no independent review.',
        'walls':len(V),'reflex_corners':turns.count(-1),'area':area,'vertices':V,'source':S,'target':T,
        'monotone_obstruction':{'first_portal_x':(qlo,qhi),'reachable_second_level_x':(F(2,5),F(3,5)),
                                'second_portal_x':(F(4,5),F(1)),'branches':branches,'all_intervals_open':True},
        'connecting_path':{'direction':(11,25),'reflections':len(contacts),'path':P,'contacts':contacts,'passage_crossings':passages}}
out=Path(__file__).with_name('check.json');out.write_text(json.dumps(encode(result),indent=2)+'\n')
print(json.dumps({'status':result['status'],'walls':len(V),'reflections':len(contacts),'area':str(area),'monotone_second_level_range':'(2/5,3/5)','second_portal':'(4/5,1)','receipt':str(out)},indent=2))
