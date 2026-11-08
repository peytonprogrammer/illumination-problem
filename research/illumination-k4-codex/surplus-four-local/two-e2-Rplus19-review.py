"""Independent review of the ONE supplied Rplus19 finite certificate."""
from pathlib import Path
from fractions import Fraction as F
import json,sys,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
sys.path.insert(0,str(ROOT/'triangle-composition/inputs'))
from boundary_replay import replay,sub,dot,cross,on
from guard_checker import path_requirements
import illumination_geometry as g
tri=lambda t:tuple(sorted(map(tuple,t)))
peer=ROOT/'fourth-surplus-review/rplus-exact-one'
r=json.loads((peer/'result.json').read_text())
geometry=json.loads((peer/'geometry.json').read_text())
name='Llower_Beast_Nbplus_Rplus'
original=json.loads((HERE/'two-e2-check.json').read_text())['hand_prescribed_fixtures'][name]
ts=set(map(tri,original['triangles']));V=[tuple(map(F,p)) for p in original['vertices']]
assert ts==set(map(tri,geometry['triangles']))
assert V==[tuple(map(F,p)) for p in geometry['vertices']]
P=[tuple(map(F,p)) for p in r['path']]
assert len(P)-2==19 and P[0]==(0,0) and P[-1]==(2,2)
assert cross(P[1],(-10,3))==0 and dot(P[1],(-10,3))>0
assert replay(V,(0,0),(2,2),P)==19
assert replay(V,(2,2),(0,0),P[::-1])==19
sigma=lambda p:(2-p[1],2-p[0])
Ps=[sigma(p) for p in P][::-1]
assert replay([sigma(p) for p in V],(0,0),(2,2),Ps)==19
U,Z=path_requirements(P);assert U<=ts and not Z&ts
Us,Zs=path_requirements(Ps);tr=lambda tiles:{tri(sigma(p) for p in t) for t in tiles}
assert Us==tr(U) and Zs==tr(Z)
geo=g.check({'triangles':sorted(ts),'marked':[(0,0),(2,2)],'require_simple':True},strict=False)
assert geo['simple_polygon'] and set(geo['interior_A'])=={(0,0),(2,0),(2,2)}
assert geo['walls']==20 and len(geo['transparent_vertices'])==6
owners=g.owners_of(list(ts));opens={e for e,ls in owners.items() if len(ls)==2}
Q=J=sN=0
for p in set().union(*map(set,ts)):
 angles,full=g.check_fan_angles(list(ts),p,owners,opens)
 if g.label(p)=='A':
  if not full:Q+=3 if angles==[4] else sum(angles)
 elif full:J+=1
 elif angles==[4]:sN+=1
ledger={'W':20,'k':J+sN,'Q':Q,'J':J,'sN':sN,'Delta':Q+sN-8}
assert ledger==original['ledger']==geometry['ledger']
# Reconstruct maximal boundary by oriented triangle-edge cancellation.
edges=set()
for a,b,c in ts:
 if cross(sub(b,a),sub(c,a))<0:b,c=c,b
 for x,y in [(a,b),(b,c),(c,a)]:
  if (y,x) in edges:edges.remove((y,x))
  else:edges.add((x,y))
nxt=dict(edges);assert len(nxt)==len(edges)==len(set(nxt.values()))
start=min(nxt);cyc=[start];p=nxt[start]
while p!=start:
 assert p not in cyc;cyc.append(p);p=nxt[p]
assert len(cyc)==len(edges)
maximal=[p for i,p in enumerate(cyc) if cross(sub(p,cyc[i-1]),sub(cyc[(i+1)%len(cyc)],p))]
assert maximal==V
walls=[];parameters=[]
for p in P[1:-1]:
 hits=[(a,b) for a,b in zip(V,V[1:]+V[:1]) if on(p,a,b)]
 assert len(hits)==1 and p not in V
 a,b=hits[0];e=sub(b,a);t=dot(sub(p,a),e)/dot(e,e)
 assert 0<t<1;parameters.append(str(t));walls.append((a,b))
q=P[-1]
for a,b in walls[::-1]:
 e=sub(b,a);w=sub(q,a)
 q=tuple(a[k]+2*dot(w,e)*e[k]/dot(e,e)-w[k] for k in (0,1))
assert q==(-40,12)
assert (F(1),F(2)) in P[1:-1] and (1,2) not in V
angles,full=g.check_fan_angles(list(ts),(1,2),owners,opens)
assert angles==[4] and not full
# Check the supplied hand-gate formulas at the actual witness, no new slope.
d=F(3,10)
expected=[(-2/(1+d),2*d/(1+d)),(3*d-2,-1),(5*d-2,1),(8*d-2,-2),
 (1,18-5/d),(19*d-4,-1),(23*d-4,3),(3,26-7/d),(10-27*d,-1),
 (1,9/d-28),(3,36-11/d),(14-37*d,-1)]
for i,p in zip([1,2,3,4,9,10,11,12,13,14,18,19],expected):assert P[i]==p
for p,a,b in [((13*d-2,F(3)),P[4],P[5]),((6-15*d,F(3)),P[8],P[9]),
 ((31*d-8,F(3)),P[14],P[15]),((33*d-8,F(3)),P[17],P[18])]:assert on(p,a,b)
assert 14-40*d==2
bad=P+[(F(2),F(5,2)),(F(2),F(2))]
try:replay(V,(0,0),(2,2),bad)
except AssertionError as ex:assert str(ex)=='earlier target'
else:raise AssertionError('earlier actual target accepted')
bad=P.copy();bad[1]=(P[1][0]+F(1,100),P[1][1])
try:replay(V,(0,0),(2,2),bad)
except AssertionError:pass
else:raise AssertionError('off-wall contact accepted')
out={'status':'INDEPENDENT_FINITE_CERTIFICATE_ACCEPT','fixture':name,
 'direction':[-10,3],'reflections':19,'path':[[str(v) for v in p] for p in P],
 'actual_first_target_forward_reverse_sigma':'PASS','full_guards':'PASS',
 'required':sorted(U),'forbidden':sorted(Z),'ledger':ledger,
 'maximal_boundary_matches_original':'PASS','smooth_1_2_angle_degrees':180,
 'unfolded_actual_target':[str(v) for v in q],'strict_wall_parameters':parameters,
 'hand_gate_formulas_at_witness':'PASS','negative_controls':['earlier_actual_T_rejected','off_wall_contact_rejected'],
 'input_hashes':{f:hashlib.sha256((peer/f).read_bytes()).hexdigest() for f in ['geometry.json','result.json']},
 'limits':'One supplied computationally discovered path, checked against original fixture using existing independent physical and guard routines. No discovery rerun, other-room checks, whole-parameter interval, or arbitrary-completion theorem. Not formal verification.'}
(HERE/'two-e2-Rplus19-review.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'],name,'19 reflections; actual first T; smooth(1,2)=180; unfolded T=(-40,12)')
