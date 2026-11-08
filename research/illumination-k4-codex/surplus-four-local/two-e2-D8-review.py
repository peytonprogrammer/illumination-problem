"""Review supplied eight-word: truncate at earlier actual T, verify four-prefix."""
from pathlib import Path
from fractions import Fraction as F
import json,sys,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
sys.path.insert(0,str(ROOT/'triangle-composition/inputs'))
from boundary_replay import replay,cross,dot,sub,on
from guard_checker import path_requirements
tri=lambda t:tuple(sorted(map(tuple,t)))
peer=ROOT/'fourth-surplus-review/two-e2-residuals'
r=json.loads((peer/'check.json').read_text());original=[tuple(map(F,q)) for q in r['path']]
assert original[0]==(0,0) and original[-1]==(2,2) and len(original)-2==8
assert on((2,2),original[4],original[5])
P=original[:5]+[(F(2),F(2))];assert len(P)-2==4
assert cross(P[1],(-5,-2))==0 and dot(P[1],(-5,-2))>0
rooms=json.loads((HERE/'two-e2-check.json').read_text())['hand_prescribed_fixtures']
U,Z=path_requirements(P)
sigma=lambda q:(2-q[1],2-q[0]);Ps=[sigma(q) for q in P][::-1]
Us,Zs=path_requirements(Ps);trans=lambda ss:{tri(sigma(q) for q in t) for t in ss}
assert Us==trans(U) and Zs==trans(Z)
controls={}
for variant in ['Dminus','Dplus','Rminus']:
 name='Llower_Beast_Nbplus_'+variant;row=rooms[name]
 V=[tuple(map(F,q)) for q in row['vertices']];ts=set(map(tri,row['triangles']))
 assert U<=ts and not Z&ts
 assert replay(V,(0,0),(2,2),P)==4 and replay(V,(2,2),(0,0),P[::-1])==4
 assert replay([sigma(q) for q in V],(0,0),(2,2),Ps)==4
 controls[name]={'status':'FOUR_REFLECTION_ACTUAL_ST_PASS','forward_reverse_sigma':'PASS','full_U_Z':'PASS'}
 print(name,'FOUR-HIT actual S/T PASS')
other=set(map(tri,rooms['Llower_Beast_Nbplus_Rplus']['triangles']));assert Z&other
caps={n:tri(t) for n,t in json.loads((ROOT/'triangle-composition/inputs/caps.json').read_text())['cap_options'].items()}
Uo,Zo=path_requirements(original);assert U<=Uo and Z<=Zo
# Verify the original failure is specifically an earlier T, not bad billiard geometry.
V=[tuple(map(F,q)) for q in rooms['Llower_Beast_Nbplus_Dminus']['vertices']]
try:replay(V,(0,0),(2,2),original)
except AssertionError as e:assert str(e)=='earlier target'
else:raise AssertionError('earlier actual target was not detected')
# Hand endpoint: after lower square exit(-1,3d-2), right/inner contacts,
# rising final leg has y=10d-2 atx2, hence d2/5.
assert 10*F(2,5)-2==2
out={'status':'ACCEPT_TRUNCATED_FOUR_PATH_THREE_ROOMS','review_finding':'Supplied8word crosses actual T on segment4->5; truncation gives valid4word.','reflections':4,'direction':[-5,-2],'path':[[str(a) for a in q] for q in P],'required':sorted(U),'forbidden':sorted(Z),'ordinary_forbidden_caps':sorted(n for n,t in caps.items() if t in Z),'controls':controls,'Rplus_conflicts':sorted(Z&other),'peer_receipt_sha256':hashlib.sha256((peer/'check.json').read_bytes()).hexdigest(),'scope':'Earlier-target truncation of supplied path, checked against three ORIGINAL fixtures and sigma; other Rplus variant excluded. No direction/word/room discovery or whole-interval assertion.'}
(HERE/'two-e2-D8-review.json').write_text(json.dumps(out,indent=2)+'\n')
print('Review corrected: three rooms closed by four-prefix; Rplus remains')
