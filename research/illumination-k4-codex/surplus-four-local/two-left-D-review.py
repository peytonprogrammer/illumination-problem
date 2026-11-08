"""Independent physical replay of the peer's one supplied 32-hit witness."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
sys.path.insert(0,str(ROOT/'triangle-composition/inputs'))
from boundary_replay import replay,sub,cross,dot
from guard_checker import path_requirements
peer=ROOT/'fourth-surplus-review/two-left-D'
r=json.loads((peer/'check.json').read_text())
P=[tuple(map(F,q)) for q in r['path']]
assert len(P)-2==32 and P[0]==(0,0) and P[-1]==(2,2)
assert cross(sub(P[1],P[0]),(-20,-9))==0 and dot(sub(P[1],P[0]),(-20,-9))>0
tri=lambda t:tuple(sorted(map(tuple,t)))
U,Z=path_requirements(P)
assert U==set(map(tri,r['required'])) and Z==set(map(tri,r['forbidden']))
rooms=json.loads((HERE/'single-e2-check.json').read_text())['residues']
pgeo=json.loads((peer/'geometry.json').read_text())
sigma=lambda p:(2-p[1],2-p[0])
Ps=[sigma(p) for p in P][::-1]
Us,Zs=path_requirements(Ps)
transform=lambda ts:{tuple(sorted(sigma(p) for p in t)) for t in ts}
assert Us==transform(U) and Zs==transform(Z)
controls={}
for name in ['Louter3_Nbplus_Dminus','Louter4_Nbplus_Dminus']:
 row=rooms[name];V=[tuple(map(F,q)) for q in row['vertices']];tiles=set(map(tri,row['triangles']))
 assert tiles==set(map(tri,pgeo[name]['triangles'])) and row['vertices']==pgeo[name]['vertices']
 assert U<=tiles and not Z&tiles
 assert replay(V,(0,0),(2,2),P)==32
 assert replay(V,(2,2),(0,0),P[::-1])==32
 assert replay([sigma(p) for p in V],(0,0),(2,2),Ps)==32
 controls[name]={'status':'INDEPENDENT_PASS','actual_first_wall_strict_contact_interior_specular':'PASS','actual_ST_reverse_sigma':'PASS','full_U_Z':'PASS','original_fixture_identity':'PASS'}
 print(name,'32-hit actual S/T independent PASS')
# Fold the target backwards across actual mirror lines, then compare to launch.
V=[tuple(map(F,q)) for q in rooms['Louter3_Nbplus_Dminus']['vertices']]
walls=list(zip(V,V[1:]+V[:1]));target=P[-1];mirrors=[]
for q in P[1:-1]:
 hits=[(a,b) for a,b in walls if cross(sub(q,a),sub(b,a))==0 and 0<dot(sub(q,a),sub(b,a))<dot(sub(b,a),sub(b,a))]
 assert len(hits)==1;mirrors.append(hits[0])
for a,b in mirrors[::-1]:
 e=sub(b,a);v=sub(target,a)
 target=tuple(a[k]+2*dot(v,e)*e[k]/dot(e,e)-v[k] for k in (0,1))
assert cross(target,(-20,-9))==0 and dot(target,(-20,-9))>0
out={'status':'ACCEPT_TWO_D_MINUS_FIXED_WITNESSES','reflections':32,'direction':[-20,-9],'unfolded_target':list(map(str,target)),'required':sorted(U),'forbidden':sorted(Z),'controls':controls,'peer_receipt_sha256':hashlib.sha256((peer/'check.json').read_bytes()).hexdigest(),'own_fixture_sha256':hashlib.sha256((HERE/'single-e2-check.json').read_bytes()).hexdigest(),'scope':'One supplied witness only; own frozen exact physical replay and guard recomputation, original fixtures, reverse/sigma, backward target unfolding. No discovery, full parameter interval or broader completion-family claim.'}
(HERE/'two-left-D-review.json').write_text(json.dumps(out,indent=2)+'\n')
print('Unfolded target:',target)
