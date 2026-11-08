"""Replay one hand-forced d=4/21 circuit in two original rooms; no discovery."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
helper=HERE/'root-leaf-check.py';ns={'__file__':str(helper),'__name__':'retained_helpers'}
exec(compile(helper.read_text().split('BDR=')[0],str(helper),'exec'),ns)
physical,polygon,tri,g,fan,H,C,sigma,tr=[ns[n] for n in ['physical','polygon','tri','g','fan','H','C','sigma','tr']]
sub,cross,dot=[ns[n] for n in ['sub','cross','dot']]
source=HERE/'critical-B-check.json';original=json.loads(source.read_text())['Beast_four_declared_residuals']
d=F(4,21)
assert F(3,16)<d<F(1,5) and d>F(2,11)
P=[(F(0),F(0)),
 (F(-8,25),F(-42,25)),(F(1),F(-10,7)),(F(-16,17),F(-18,17)),
 (F(-1),F(-3,4)),(F(-2,3),F(1)),
 (F(-2,17),F(-32,17)),(F(1,2),F(-2)),(F(1),F(-40,21)),(F(-6,17),F(-28,17)),
 (F(-6,7),F(1)),(F(-22,21),F(0)),(F(-6,5),F(4,5)),
 (F(3),F(0)),(F(-1),F(-16,21)),(F(1),F(-8,7)),(F(-14,25),F(-36,25)),
 (F(-2,21),F(1)),(F(10,21),F(-2)),
 (F(26,17),F(60,17)),(F(58,25),F(92,25)),(F(2),F(2))]
assert len(P)-2==20
assert F(7,37)<d<F(1,5) and 10-42*d==2
leftTc=(38*d-6)/(1-d);rightTc=(10-38*d)/(1+d)
formula=[(F(0),F(0)),(-2*d/(1+d),-2/(1+d)),(F(1),3*d-2),
 (-4*d/(1-d),(6*d-2)/(1-d)),(F(-1),1/d-6),(7*d-2,F(1)),
 ((10*d-2)/(1-d),-8*d/(1-d)),(2/d-10,F(-2)),(F(1),11*d-4),
 ((2-12*d)/(1-d),(14*d-4)/(1-d)),(2-15*d,F(1)),(2-16*d,F(0)),
 ((2-18*d)/(1+d),(4-16*d)/(1+d)),(F(3),4-21*d),(F(-1),4-25*d),
 (F(1),4-27*d),((28*d-6)/(1+d),(4-30*d)/(1+d)),(31*d-6,F(1)),
 (34*d-6,F(-2)),(leftTc,leftTc+2),(rightTc,6-rightTc),(10-42*d,F(2))]
assert P==formula

minimum=H|fan('B',[0,1,2])|fan('E',[4,5])|fan('Tc',[5,6])|C(['L+','Nr-'])
maximum=minimum|C(['D-','D+'])
U,Z=g['path_requirements'](P)
assert U<=minimum,("required",U-minimum)
assert not Z&maximum,("forbidden",Z&maximum)
Us,Zs=g['path_requirements']([sigma(p) for p in P[::-1]])
assert Us==tr(U) and Zs==tr(Z)
receipts={}
for cap in ['D-','D+']:
 ts={tri(t) for t in original[cap]['triangles']}
 assert ts==minimum|C([cap])
 V=polygon(ts);assert V==[tuple(p) for p in original[cap]['vertices']]
 physical(P,V);physical(P[::-1],V);physical([sigma(p) for p in P[::-1]],[sigma(p) for p in V])
 assert (3,0) not in V
 # Unfold actual finite walls to the actual target, rather than a discovery frame.
 def on(q,a,b):return cross(sub(q,a),sub(b,a))==0 and dot(sub(q,a),sub(q,b))<=0
 q=P[-1]
 for p in reversed(P[1:-1]):
  walls=[(a,b) for a,b in zip(V,V[1:]+V[:1]) if on(p,a,b) and p not in [a,b]]
  assert len(walls)==1,(cap,p,walls)
  a,b=walls[0];e=sub(b,a);v=sub(q,a)
  q=tuple(a[k]+2*dot(v,e)*e[k]/dot(e,e)-v[k] for k in [0,1])
 assert cross(sub(P[1],P[0]),q)==0 and dot(sub(P[1],P[0]),q)>0
 receipts[cap]={'status':'PASS_ACTUAL_FIRST_T_FINITE_WALLS_SPECULAR_INTERIOR_REVERSE_SIGMA','reflections':20,'unfolded_actual_target':list(map(str,q)),'smooth_R_hit':[3,0],'original_vertices':V}
corner_limits={}
for cap in ['R-','R+']:
 V=[tuple(p) for p in original[cap]['vertices']]
 assert (3,0) in V
 corner_limits[cap]={'status':'NOT_COVERED_TRUE_CORNER_AT_PRESCRIBED_HIT','corner':[3,0]}
out={'status':'TWO_ORIGINAL_BEAST_D_ROOMS_CLOSED_BY_ONE_HAND_DERIVED_PATH','parameter':'4/21','reflections':20,'path':[[str(x) for x in p] for p in P],'minimum':sorted(minimum),'maximum':sorted(maximum),'required':sorted(U),'forbidden':sorted(Z),'sigma':'PASS','physical_receipts':receipts,'uncovered_R_variants':corner_limits,'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [source,helper]},'limits':'One predeclared hand-derived fixed circuit, two ORIGINAL room replays, two original-room corner observations. No discovery or parameter scan. Reuses retained physical and guard helpers; hand derivation/completeness separately documented, independent review pending.'}
# NEW endpoint-fixed suffix unfolding of the accepted FIVE path.
oldsource=ROOT/'second-surplus-review/five-path-check.json'
oldraw=json.loads(oldsource.read_text())['five_path']
oldfive=[tuple(F(*v) for v in q) for q in oldraw]
assert oldfive[-3]==(2,F(11,3))
assert oldfive[-2]==(F(12,7),F(26,7)) and oldfive[-1]==(2,2)
# The removed vertical mirror x2 contains actual T; reflect ONLY its suffix.
axis=lambda p:(4-p[0],p[1])
Q=oldfive[:4]+[axis(oldfive[-2]),axis(oldfive[-1])]
assert Q==[(0,0),(F(1,6),1),(F(2,3),-2),(F(8,5),F(18,5)),(F(16,7),F(26,7)),(2,2)]
assert len(Q)-2==4 and axis(Q[-1])==Q[-1]
# Independent endpoint derivation through the paired Tc roof.
d4=F(1,6);a4=8*d4/(1-d4);b4=(4-8*d4)/(1+d4)
assert F(1,7)<d4<F(1,5) and 4-12*d4==2
assert Q[1]==(d4,1) and Q[2]==(4*d4,-2)
assert Q[3]==(a4,a4+2) and Q[4]==(b4,6-b4)
# B square gates: entry3d, far4d, exit5d, all strict.
assert 0<3*d4<4*d4<5*d4<1
# At y1 on the final ascent x7d>1, so source-roof corner/notch is avoided.
assert 7*d4>1
max4=minimum|C(['D-','D+','R-','R+'])
u4,z4=g['path_requirements'](Q)
assert u4<=minimum and not z4&max4,(u4-minimum,z4&max4)
us4,zs4=g['path_requirements']([sigma(p) for p in Q[::-1]])
assert us4==tr(u4) and zs4==tr(z4)
newreceipts={}
for cap in ['D-','D+','R-','R+']:
 ts={tri(t) for t in original[cap]['triangles']};assert ts==minimum|C([cap])
 V=polygon(ts);assert V==[tuple(p) for p in original[cap]['vertices']]
 physical(Q,V);physical(Q[::-1],V);physical([sigma(p) for p in Q[::-1]],[sigma(p) for p in V])
 qt=Q[-1]
 for p in Q[-2:0:-1]:
  walls=[(a,b) for a,b in zip(V,V[1:]+V[:1]) if cross(sub(p,a),sub(b,a))==0 and dot(sub(p,a),sub(p,b))<0]
  assert len(walls)==1
  a,b=walls[0];e=sub(b,a);v=sub(qt,a)
  qt=tuple(a[k]+2*dot(v,e)*e[k]/dot(e,e)-v[k] for k in (0,1))
 assert qt==(2,12) and cross(qt,(1,6))==0 and dot(qt,(1,6))>0
 newreceipts[cap]={'status':'PASS_ACTUAL_FIRST_T_FINITE_WALLS_SPECULAR_INTERIOR_REVERSE_SIGMA','reflections':4,'unfolded_actual_target':['2','12'],'original_boundary_unchanged':True}
out['current_result']='ALL_FOUR_ORIGINAL_BEAST_RESIDUES_CLOSED_BY_SAME_FOUR_REFLECTION_PATH'
out['new_four_reflection_certificate']={'status':'PASS_INDEPENDENT_REVIEW_PENDING','mechanism':'Remove x2 mirror and reflect only suffix; x2 fixes actual T','path':[[str(x) for x in p] for p in Q],'reflections':4,'source_five_sha256':hashlib.sha256(oldsource.read_bytes()).hexdigest(),'strict_parameter_interval':['1/7','1/5'],'parameter':'1/6','target_equation':'4-12d=2','required':sorted(u4),'forbidden':sorted(z4),'minimum':sorted(minimum),'maximum_all_four_caps':sorted(max4),'sigma':'PASS','physical_receipts':newreceipts}
out['limits']='Current FOUR-path is a fixed endpoint-preserving suffix unfolding of the accepted five-path, with its one hand-forced parameter; all FOUR ORIGINAL rooms replayed. Prior twenty-path fields are historical valid proofs of two rooms only. No newroom/discovery/archive/worker; shared retained helpers and independent peer review pending.'
(HERE/'four-Beast-hand-check.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: NEW SAME FOUR-reflection path closes ALL FOUR ORIGINAL rooms; fullguards/physicalfirstT/reverse/sigma; actualTunfold(2,12). Old20 remains valid, nonessential.')
