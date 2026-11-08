"""Check ONE fixed joined12 certificate against the six sibling fixtures."""
from pathlib import Path
from fractions import Fraction as F
import json,sys,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
sys.path.insert(0,str(ROOT/'triangle-composition/inputs'))
from boundary_replay import replay
from guard_checker import path_requirements
import illumination_geometry as g
tri=lambda t:tuple(sorted(map(tuple,t)))
P=[tuple(map(F,p)) for p in json.loads((HERE/'result.json').read_text())['path']]
assert len(P)-2==12 and P[0]==(0,0) and P[-1]==(2,2)
U,Z=path_requirements(P)
sigma=lambda p:(2-p[1],2-p[0]);Ps=[sigma(p) for p in P][::-1]
fixtures=json.loads((HERE.parent/'two-e2-check.json').read_text())['hand_prescribed_fixtures']
names=['Bouter3_Dhalf3_Rplus_Tempty','Bouter4_Dhalf3_Rplus_Tempty',
 'Bouter3_Dfullwest4_Rplus_Tminus','Bouter3_Dfullwest4_Rplus_Tplus',
 'Bouter4_Dfullwest4_Rplus_Tminus','Bouter4_Dfullwest4_Rplus_Tplus',
 'BHeast4_Dhalf3_Rplus_Tplus']
controls={}
for name in names:
 row=fixtures[name];ts=set(map(tri,row['triangles']));V=[tuple(map(F,p)) for p in row['vertices']]
 assert U<=ts and not Z&ts,(name,'guard conflict')
 assert replay(V,(0,0),(2,2),P)==12
 assert replay(V,(2,2),(0,0),P[::-1])==12
 assert replay([sigma(p) for p in V],(0,0),(2,2),Ps)==12
 geo=g.check({'triangles':sorted(ts),'marked':[(0,0),(2,2)],'require_simple':True},strict=False)
 assert geo['simple_polygon'] and set(geo['interior_A'])=={(0,0),(2,0),(2,2)}
 assert geo['walls']==20 and len(geo['transparent_vertices'])==6
 owners=g.owners_of(list(ts));opens={e for e,ls in owners.items() if len(ls)==2}
 angles,full=g.check_fan_angles(list(ts),(0,1),owners,opens)
 assert angles==[4] and not full and (0,1) not in V
 controls[name]={'status':'SAME_TWELVE_PATH_PASS','forward_reverse_sigma_first_T':'PASS',
  'full_U_Z':'PASS','smooth_0_1_degrees':180,'simple_fullSUT_W20_k6':'PASS'}
 print(name,'SAME12 PASS')
common=set.intersection(*(set(map(tri,fixtures[n]['triangles'])) for n in names))
union=set.union(*(set(map(tri,fixtures[n]['triangles'])) for n in names))
assert U<=common and not Z&union
out={'status':'ALL_SEVEN_JOINED_ORIGINAL_FIXTURES_CLOSED_BY_ONE_PATH',
 'reflections':12,'direction':[-3,4],'controls':controls,
 'common_required_and_union_forbidden':'PASS','required':sorted(U),'forbidden':sorted(Z),
 'path':[[str(v) for v in p] for p in P],
 'inputs_sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE/'result.json',HERE.parent/'two-e2-check.json']},
 'limits':'One discovered witness, unchanged fixed-path verification in seven original rooms and sigma. No additional discovery run or arbitrary-completion claim; broader local and remote partitions separate.'}
(HERE/'inheritance.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'])
