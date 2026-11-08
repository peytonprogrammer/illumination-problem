"""One stopped N70 four plus analytic N0 triangle companion six."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
HERE=Path(__file__).resolve().parent;BASE=HERE.parent.parent
src=BASE/'surplus-four-local/R23-top6-search/verify.py'
e={'__file__':str(src.resolve())};exec(compile(src.read_text().split('\ndef path(d,nine):')[0],str(src),'exec'),e)
fan,H=e['fan'],e['H']
raw=json.loads((HERE/'room.json').read_text());j=json.loads((HERE/'result.json').read_text())
assert j['status']=='FOUND_EXACT_PATH_PENDING_INDEPENDENT_VERIFICATION'
for name,key in [('room.json','room_sha256'),('search.py','search_source_sha256')]:assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==j[key]
P4=[tuple(F(*x) for x in p) for p in j['candidate']['path']]
assert P4==[(F(0),F(0)),(F(3),F(9,4)),(F(2),F(3)),(F(2,7),F(12,7)),(F(5,4),F(3)),(F(2),F(2))]
P6=P4[:3]+[(F(2,3),F(2)),(F(2,7),F(16,7)),(F(1,2),F(2))]+P4[4:]
W4=[((3,2),(3,3)),((1,3),(3,3)),((0,2),(1,1)),((1,3),(2,3))]
W6=W4[:2]+[((0,2),(1,2)),((0,2),(1,3)),((0,2),(1,2))]+W4[-1:]
mi4=H|fan('N',[7,0]);ma4=mi4|fan('N',[1,2,3,4,5])|fan('E',[0,1,2,4,5,6,7])|fan('Tc',[0,1,2,3,4,7])|set().union(*(fan(k,range(8)) for k in ['L','B','D','R']))
mi6=H|fan('N',[0]);ma6=mi6|fan('N',[2,3,4,5,6])|fan('E',[0,1,2,4,5,6,7])|fan('Tc',[0,1,2,3,4,7])|set().union(*(fan(k,range(8)) for k in ['L','B','D','R']))
def verify(P,W,mi,ma):
 q=P[-1]
 for a,b in W[::-1]:
  v=e['reflect'](e['sub'](q,a),a,b);q=tuple(a[k]+v[k] for k in (0,1))
 u,z,proof=e['audit'](P,W,mi,ma,q)
 assert all(not e['on']((0,0),a,b) for a,b in zip(P[1:],P[2:]))
 return {'path':[[str(x) for x in p] for p in P],'proof':proof,'required':sorted(u),'forbidden':sorted(z),'minimum':sorted(mi),'maximum':sorted(ma),'image':list(map(str,q))},u,z
r4,u4,z4=verify(P4,W4,mi4,ma4);r6,u6,z6=verify(P6,W6,mi6,ma6)
for label,u,z in [('4',u4,z4),('6',u6,z6)]:
 print('COUNTS',label,len(u),len(z))
 for k in ['L','B','D','R','E','Tc','N']:print(label,'U',k,[i for i in range(8) if fan(k,[i])&u]);print(label,'Z',k,[i for i in range(8) if fan(k,[i])&z])
room={tuple(sorted(map(tuple,t))) for t in raw['triangles']};assert room==H|set().union(*(fan(k,ss) for k,ss in raw['spec'].items()))
V=e['boundary'](room);assert len(V)==20 and set(V)==set(map(tuple,raw['vertices']))
e['physical'](P4,V);e['physical'](P4[::-1],V);sigma=e['sigma'];e['physical']([sigma(p) for p in P4[::-1]],[sigma(p) for p in V])
assert mi4<=room<=ma4 and (2,3) not in V
cw=[(a,b) for a,b in zip(V,V[1:]+V[:1]) if e['on']((2,3),a,b)];assert len(cw)==1 and set(cw[0])=={(1,3),(3,3)}
# Remaining N70 row upper BOTH O3/O4 andDleaves fits four, no R restriction.
base=H|fan('B',[6,7,0,1])|fan('D',[3,4])|fan('L',[0])|fan('E',[4])|fan('R',[3])
assert u4<=H|fan('N',[7,0]) and base|fan('N',[7,0])<=ma4
assert u6<=H|fan('N',[0]) and base|fan('L',[7])|fan('N',[0])<=ma6
assert z4==fan('E',[3])|fan('Tc',[5,6])|fan('N',[6])
assert z6==fan('E',[3])|fan('Tc',[5,6])|fan('N',[1,7])
d=F(3,4);assert F(5,7)<d<F(4,5) and 8*d-4==2
f=6-3/d;a=(6*d-4)/(1+d)
assert P4==[(F(0),F(0)),(F(3),3*d),(f,F(3)),(a,2-a),(7*d-4,F(3)),(8*d-4,F(2))]
assert P6==P4[:3]+[(6-4/d,F(2)),(a,a+2),(6*d-4,F(2))]+P4[4:]
assert 2<3*d<3 and 1<f<3 and 0<a<1 and 1<7*d-4<2
assert 2<6-5*d<3 and 2<5/d-4<3 and 0<6-4/d<1 and 0<6*d-4<1
# Exact same forward exitline after N70 single vs N0 triple.
assert P4[3][0]-d*P4[3][1]==P6[5][0]-d*P6[5][1]==4*d-4
assert r4['image']==r6['image']
# Reconstruct angle ledger/simplicity for ONLY supplied four-path room.
def angle(ts,p):
 n=0
 for t in ts:
  if p in t:
   aa,bb=[e['sub'](x,p) for x in t if x!=p];n+=90 if e['dot'](aa,bb)==0 else 45
 return n
pts={p for t in room for p in t};A={p for p in pts if p[0]%2==p[1]%2==0}
assert {p for p in A if angle(room,p)==360}=={(0,0),(2,0),(2,2)}
assert sum(angle(room,p)==360 for p in pts-A)==3 and sum(angle(room,p)==180 for p in pts-A)==3
assert angle(room,(2,3))==180
for i,(aa,bb) in enumerate(zip(V,V[1:]+V[:1])):
 for k,(cc,ff) in enumerate(zip(V,V[1:]+V[:1])):
  if i<k and (k-i) not in (1,len(V)-1):assert not e['edge_times'](aa,bb,cc,ff)
for P,W,mi,ma,z in [(P4,W4,mi4,ma4,z4),(P6,W6,mi6,ma6,z6)]:
 for t in z:
  try:e['audit'](P,W,mi,ma|{t},tuple(map(F,r4['image'])))
  except AssertionError:pass
  else:raise AssertionError('missed blocker')
sources=[src,HERE/'room.json',HERE/'result.json',HERE/'search.py',BASE/'fourth-surplus-review/mixed-e2-e1/argument.txt',BASE/'surplus-four-local/mixed-H4-R23-search/findings.txt']
out={'status':'PARENT_N70_FOUR_N0_SIX_AND_FINAL_TWO_SINGLELEAF_FORMS_PASS','four':r4,'six':r6,'frozen_physical':'ONLYfour frozen20wallpolygon firstwalls/firstT/reverse/sigma PASS; firstroof2,3 smooth180 inside maximal1,3--3,3','remaining_row_implications':['N70 O3/O4 R3 bothDleaves <=4','L70 O3/O4 N0/R3 bothDleaves <=6'],'root':'3/4','strict_gate':['5/7','4/5'],'endpoint_equation':'8d-4=2','source_sha256':{str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'limits':'ONE stoppedauthorizedpatternfour; analyticN0six hasnoextra room/search. Parentnewpaths/rowjoinsawaitreview. No entireDelta4claim.'}
(HERE/'verification.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print('PASS BOTH REMAINING FORMS')
