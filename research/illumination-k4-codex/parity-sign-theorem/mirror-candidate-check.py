"""Exact check of ONE supplied leaf-flip room and THREE fixed directions.
No peer code imports and no room/direction discovery.
"""
from fractions import Fraction as F
from collections import Counter, defaultdict
from pathlib import Path
import hashlib, json
ROOT=Path(__file__).resolve().parent
PEER=ROOT.parents[1]/'claude-illumination-check/b-not-in-k/verify_min_blind_R3_b0.json'
RING=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1),(1,0)]
def fan(c,ks): return [tuple([c]+[(c[0]+RING[j][0],c[1]+RING[j][1]) for j in (k,k+1)]) for k in ks]
TRI=fan((-4,0),range(8))+fan((0,0),range(8))+fan((-2,0),range(4))+[
 ((-2,2),(-2,1),(-1,1)),((2,0),(1,0),(1,1)),
 ((0,2),(0,1),(1,1)),((0,2),(1,1),(1,2)),
 ((0,-2),(0,-1),(1,-1)),((-6,0),(-5,0),(-5,1)),
 ((-4,2),(-4,1),(-3,1)),((-4,-2),(-4,-1),(-3,-1))]
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def scale(a,t): return tuple(x*t for x in a)
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def cross(a,b): return a[0]*b[1]-a[1]*b[0]
def mv(A,x): return tuple(dot(r,x) for r in A)
def mm(A,B): return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)) for i in range(2))
I=((F(1),F(0)),(F(0),F(1)))
D=tuple(sorted(((1,1),(2,0)))); H=tuple(sorted(((1,0),(2,0))))

def on(p,a,b): return cross(sub(p,a),sub(b,a))==0 and dot(sub(p,a),sub(p,b))<=0
def intersects(a,b,c,d):
 o=[cross(sub(b,a),sub(x,a)) for x in (c,d)]; u=[cross(sub(d,c),sub(x,c)) for x in (a,b)]
 return (o[0]*o[1]<0 and u[0]*u[1]<0) or any((k==0 and on(p,*e)) for k,p,e in [(o[0],c,(a,b)),(o[1],d,(a,b)),(u[0],a,(c,d)),(u[1],b,(c,d))])

def geometry(tri):
 assert len({tuple(sorted(t)) for t in tri})==len(tri)
 assert all(abs(cross(sub(t[1],t[0]),sub(t[2],t[0])))==1 for t in tri)
 count=Counter(tuple(sorted((t[j],t[(j+1)%3]))) for t in tri for j in range(3)); assert max(count.values())==2
 walls=sorted(e for e,n in count.items() if n==1)
 adj=defaultdict(list)
 for a,b in walls: adj[a].append(b); adj[b].append(a)
 assert all(len(v)==2 for v in adj.values()), 'boundary vertex degree'
 poly=[]; z=min(adj); previous=None
 while z not in poly:
  poly.append(z); nxt=next(v for v in adj[z] if v!=previous); previous,z=z,nxt
 assert z==poly[0] and len(poly)==len(adj), 'single boundary component'
 for i,(a,b) in enumerate(walls):
  for c,d in walls[i+1:]:
   if not {a,b}&{c,d}: assert not intersects(a,b,c,d), 'self intersection'
 corners={p for p,nb in adj.items() if cross(sub(nb[0],p),sub(nb[1],p))}
 def where(p):
  if any(on(p,a,b) for a,b in walls): return 'boundary'
  hits=0
  for a,b in walls:
   if (a[1]>p[1]) != (b[1]>p[1]):
    x=F(a[0])+F(p[1]-a[1],b[1]-a[1])*(b[0]-a[0]); hits+=x>p[0]
  return 'interior' if hits%2 else 'exterior'
 for x in range(min(p[0] for p in poly),max(p[0] for p in poly)+1):
  for y in range(min(p[1] for p in poly),max(p[1] for p in poly)+1):
   p=(x,y)
   if (x%2 or y%2) and where(p)!='exterior': assert p in corners, ('nonraw',p)
 assert where((-4,0))==where((0,0))=='interior'
 assert D in walls and H in walls and tuple(sorted(((1,-1),(1,0)))) in walls and tuple(sorted(((1,1),(1,2)))) in walls
 assert tuple(sorted(((1,0),(1,1)))) not in walls
 area=abs(sum(cross(poly[i],poly[(i+1)%len(poly)]) for i in range(len(poly))))/2
 assert area==len(tri)/2
 return walls,corners,poly,area
W,CORNERS,POLY,AREA=geometry(TRI)
peer=json.loads(PEER.read_text())['rooms'][0]
assert len(peer['V'])==len(CORNERS) and set(map(tuple,peer['V']))==CORNERS
# Compare the actual polygon cycles after removing allowed smooth A boundary vertices.
merged=[p for p in POLY if p in CORNERS]; pv=list(map(tuple,peer['V']))
assert {tuple(sorted((merged[i],merged[(i+1)%len(merged)]))) for i in range(len(merged))}=={tuple(sorted((pv[i],pv[(i+1)%len(pv)]))) for i in range(len(pv))}
def interior_union(p):
 return any(all(cross(sub(t[(j+1)%3],t[j]),sub(p,t[j]))>=0 for j in range(3)) or all(cross(sub(t[(j+1)%3],t[j]),sub(p,t[j]))<=0 for j in range(3)) for t in TRI)
def trace(z,v):
 z=tuple(map(F,z)); v=tuple(map(F,v)); initial=(z,v); L=I; Q=(F(0),F(0)); affine=(F(0),F(0)); contacts=[]; states=set(); d=h=0
 while True:
  state=(z,v,L)
  assert state not in states, 'repeated state without initial closure'; states.add(state)
  hits=[]
  for a,b in W:
   e=sub(b,a); den=cross(v,e)
   if den:
    time=F(cross(sub(a,z),e),den); u=F(cross(sub(a,z),v),den)
    if time>0 and 0<=u<=1: hits.append((time,u,(a,b)))
  assert hits
  time=min(x[0] for x in hits); chosen=[x for x in hits if x[0]==time]
  assert len(chosen)==1 and 0<chosen[0][1]<1, 'corner hit'
  seg=chosen[0][2]; p=add(z,scale(v,time)); assert p not in CORNERS
  assert interior_union(add(z,scale(v,time/2))), 'outside segment'
  e=sub(seg[1],seg[0]); n=dot(e,e)
  R=tuple(tuple(2*F(e[i]*e[j],n)-(i==j) for j in range(2)) for i in range(2))
  a=(1,1) if seg==D else ((0,2) if seg==H else (0,0))
  Q=add(Q,mv(L,a)); affine=add(mv(R,affine),a)
  d+=seg==D;h+=seg==H
  L=mm(L,R); v=mv(R,v);z=p;contacts.append([list(map(str,p)),[list(x) for x in seg]])
  if (z,v)==initial and L==I: break
  assert len(contacts)<10000, 'safety cap, never an acceptance criterion'
 # Forward physical composition and unfolding holonomy have opposite signs
 # at a closed frame (each moving reflection reverses its normal shift).
 assert Q==scale(affine,-1), ('independent affine derivative mismatch',Q,affine)
 assert tuple(int(q)%2 for q in Q)==(d%2,d%2)
 return {'contacts':len(contacts),'D_hits':d,'H_hits':h,'Q':list(map(str,Q)),'closed_frame':True,'contact_list':contacts}

def check_direction(p,q):
 # Every unfolded physical vertex is integral. Phase det(z,v) is
 # constant modulo integers under integer-wall reflections. On D,
 # z=(1+t,1-t), so breakpoints can only be t=j/abs(vx+vy).
 # Between consecutive breakpoints no corner can occur, hence the
 # entire open strip has the same return word and period derivative.
 velocities=sorted({(a*sgn,b*sgn2) for a,b in [(p,q),(q,p)] for sgn in [-1,1] for sgn2 in [-1,1] if a*sgn+b*sgn2<0})
 rows=[]
 for v in velocities:
  n=abs(sum(v))
  for j in range(n):
   t=F(2*j+1,2*n); z=(1+t,1-t)
   r=trace(z,v);rows.append({'start':list(map(str,z)),'velocity':v,'phase_interval':[str(F(j,n)),str(F(j+1,n))],**r})
 return {'direction':[p,q],'all_D_outgoing_strips':len(rows),'loaded_strip_representatives':sum(any(F(x) for x in r['Q']) for r in rows),'rows':rows}
results=[check_direction(*w) for w in [(1,1),(2,1),(3,2)]]
assert results[0]['loaded_strip_representatives']==results[1]['loaded_strip_representatives']==0
assert results[2]['loaded_strip_representatives']>0
out={'status':'PASS','scope':'One supplied room; complete D-contact strips in three specified direction classes; no universal claim','triangles':len(TRI),'area':AREA,'maximal_walls':len(CORNERS),'strictly_simple':True,'raw':True,'marks_interior':True,'literal_fixed_flank_pocket':True,'peer_polygon_matches':True,'directions':results,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'peer_sha256':hashlib.sha256(PEER.read_bytes()).hexdigest()}
ROOT.joinpath('mirror-candidate-check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='directions'},indent=2))
for d in results: print(d['direction'], 'strips',d['all_D_outgoing_strips'],'loaded',d['loaded_strip_representatives'],'periods',[r['contacts'] for r in d['rows']],'loads',[r['Q'] for r in d['rows']])
