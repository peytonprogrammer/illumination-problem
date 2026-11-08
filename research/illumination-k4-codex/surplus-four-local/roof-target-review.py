"""Independent check of the peer's one prescribed roof-family path transfer."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
sys.path.insert(0,str(ROOT/'triangle-composition/inputs'))
import illumination_geometry as g
from boundary_replay import replay,cross,sub
from guard_checker import path_requirements
tri=lambda t:tuple(sorted(map(tuple,t)))
D=g.DIRS
def fan(c,inds):
 return {tri((c,(c[0]+D[i][0],c[1]+D[i][1]),(c[0]+D[(i+1)%8][0],c[1]+D[(i+1)%8][1]))) for i in inds}
H=set().union(*(fan(c,range(8)) for c in [(0,0),(2,0),(2,2)]))
caps={n:tri(t) for n,t in json.loads((ROOT/'triangle-composition/inputs/caps.json').read_text())['cap_options'].items()}
fixed=H|fan((-2,0),[7,0,1,2])|fan((-2,2),[6])|fan((2,4),[5,6])|{caps[n] for n in ['B+','E-','Nr-']}
possible=fixed|{caps[n] for n in ['D+','D-','R+','R-']}
source=HERE/'left-return-check.json';raw=json.loads(source.read_text())['paths']['trapezoid_Ncap'];P=[tuple(map(F,q)) for q in raw['path']]
assert len(P)-2==9 and P[0]==(0,0) and P[-1]==(2,2)
U,Z=path_requirements(P);assert U<=fixed and not Z&possible
peer=ROOT/'fourth-surplus-review/roof-target-first';fixture=json.loads((peer/'geometry.json').read_text())
ts=set(map(tri,fixture['triangles']));V=[tuple(map(F,q)) for q in fixture['vertices']]
assert ts==fixed|{caps['D-']}
data=g.check({'triangles':sorted(ts),'marked':[(0,0),(2,2)],'require_simple':True},strict=False)
assert set(data['interior_A'])=={(0,0),(2,0),(2,2)}
assert data['walls']==20 and len(data['transparent_vertices'])==6 and len(ts)==35
owners=g.owners_of(list(ts));opens={e for e,ls in owners.items() if len(ls)==2};Q=J=sN=0
for p in set().union(*map(set,ts)):
 angles,full=g.check_fan_angles(list(ts),p,owners,opens)
 if g.label(p)=='A':
  if not full:Q+=3 if angles==[4] else sum(angles)
 elif full:J+=1
 elif angles==[4]:sN+=1
assert (Q,J,sN)==(10,4,2)
# Independent oriented tile-edge cancellation reconstructs the boundary.
edges=set()
for a,b,c in ts:
 if cross(sub(b,a),sub(c,a))<0:b,c=c,b
 for u,v in [(a,b),(b,c),(c,a)]:
  if (v,u) in edges:edges.remove((v,u))
  else:edges.add((u,v))
nxt=dict(edges);assert len(nxt)==len(edges)==len(set(nxt.values()))
start=min(nxt);p=start;cycle=[]
while True:
 assert p not in cycle;cycle.append(p);p=nxt[p]
 if p==start:break
assert len(cycle)==len(edges)
VV=[p for i,p in enumerate(cycle) if cross(sub(p,cycle[i-1]),sub(cycle[(i+1)%len(cycle)],p))]
k=VV.index(V[0]);assert VV[k:]+VV[:k]==V
assert U<=ts and not Z&ts
assert replay(V,(0,0),(2,2),P)==9 and replay(V,(2,2),(0,0),P[::-1])==9
sigma=lambda p:(2-p[1],2-p[0]);Ps=[sigma(p) for p in P][::-1]
assert replay([sigma(p) for p in V],(0,0),(2,2),Ps)==9
Us,Zs=path_requirements(Ps);transform=lambda ts:{tri(sigma(p) for p in t) for t in ts}
assert Us==transform(U) and Zs==transform(Z)
pr=json.loads((peer/'check.json').read_text());assert U==set(map(tri,pr['required'])) and Z==set(map(tri,pr['forbidden']))
out={'status':'ACCEPT_NR_MINUS_PRESENT_REMOTE_ROOF_FAMILY','reflections':9,'whole_envelope_U_Z':'PASS','actual_first_walls_strict_contacts_interior_specular_reverse_sigma':'PASS','independent_geometry_boundary_ledger':'PASS','ledger':{'W':20,'k':6,'Q':Q,'J':J,'sN':sN,'Delta':Q+sN-8,'triangles':len(ts)},'scope':'Only fixed L7/0/1/2 + remote(-2,2)sector6 + centeredT5/6 + B+/E-/Nr-, ordinaryD/R arbitrary. Nr-absent remains open. No new path or room discovery.','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'peer_geometry_sha256':hashlib.sha256((peer/'geometry.json').read_bytes()).hexdigest()}
(HERE/'roof-target-review.json').write_text(json.dumps(out,indent=2)+'\n')
print('Independent HAND/exact transfer ACCEPT; prescribed nonvacuity control PASS')
