"""Check two hand-prescribed portal families at declared rational controls."""
from pathlib import Path
from fractions import Fraction as F
import json,sys,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
sys.path.insert(0,str(ROOT/'triangle-composition/inputs'))
from boundary_replay import replay,inside
from guard_checker import path_requirements
tri=lambda t:tuple(sorted(map(tuple,t)))
fixture=HERE/'two-e2-check.json'
name='Bouter3_Dhalf3_Rplus_Tempty'
row=json.loads(fixture.read_text())['hand_prescribed_fixtures'][name]
V=[tuple(map(F,q)) for q in row['vertices']]
room=set(map(tri,row['triangles']))

def source(d):
 return [(F(0),F(0)),(F(-1),-1/d),(d-2,F(-1)),
  (4*d-2,F(2)),((8*d-2)/(d+1),(6*d-4)/(d+1)),
  (8-6/d,F(2)),(F(2),8-6*d)]

def target(d):
 a=4*(d-1)/(d+1);b=(4*d-6)/(d-1)
 return [(F(2),F(2)),(F(0),2-2*d),(F(1),2-3*d),
  (a,-2-a),(F(1),5/d-6),(b,-2-b),
  (F(0),4*d-8),(F(2),6*d-8)]

def check(P,count):
 assert replay(V,P[0],P[-1],P)==count
 assert replay(V,P[-1],P[0],P[::-1])==count
 U,Z=path_requirements(P);assert U<=room and not Z&room
 assert P[-1][0]==2 and -1<P[-1][1]<2
 return {'status':'PASS_ACTUAL_WALLS_REVERSE_FULL_GUARDS',
  'reflections':count,'path':[[str(v) for v in q] for q in P],
  'required':sorted(U),'forbidden':sorted(Z)}

s=F(13,10);t=F(8,5);root=F(4,3)
assert F(5,4)<s<F(7,5) and F(3,2)<t<F(5,3)
controls={'source_13_over_10':check(source(s),5),
 'target_backward_8_over_5':check(target(t),6),
 'source_at_matching_root':check(source(root),5)}
assert source(root)[-1]==target(root)[-1]==(2,0)
assert inside(target(root)[1],V)
try:replay(V,(2,2),(2,0),target(root))
except AssertionError:pass
else:raise AssertionError('interior target-side mirror accepted')
# Matching outgoing source (-1,-d) to reversed target direction (-1,-d)
# reduces to 8-6d=6d-8. This is its unique root.
assert 12*root==16
out={'status':'TWO_ENDED_TEST_NO_LEGAL_MATCH',
 'fixture':name,'fixture_receipt_sha256':hashlib.sha256(fixture.read_bytes()).hexdigest(),
 'section':'x=2,-1<y<2',
 'source_family':{'word':['x=-1','y=-1','y=2','x-y=2','y=2'],
  'launch':['-d','-1'],'section_height':'8-6*d','outgoing':['-1','-d'],
  'hand_derived_strict_interval':['5/4','7/5']},
 'target_backward_family':{'word':['x=0','x=1','x+y=-2','x=1','x+y=-2','x=0'],
  'launch':['-1','-d'],'section_height':'6*d-8','outgoing':['1','d'],
  'hand_derived_strict_interval':['3/2','5/3']},
 'matching':{'equation':'8-6*d=6*d-8','unique_root':'4/3',
  'formal_join':['2','0'],'status':'REJECTED_TARGET_BRANCH',
  'first_false_target_contact':['0','-2/3'],
  'false_contact_is_strictly_interior':True},
 'controls':controls,'new_case_closures':0,
 'limits':'Whole interval arguments are hand-derived in two-e2-joined-match.txt. This script checks only three prescribed rational paths and rejection at the derived root; no interval sampling, itinerary discovery, solver or room scan.'}
(HERE/'two-e2-joined-match.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'])
for k,v in controls.items():print(k,v['status'],v['reflections'])
print('Matching root4/3 rejected: target first proposed mirror is interior.')
