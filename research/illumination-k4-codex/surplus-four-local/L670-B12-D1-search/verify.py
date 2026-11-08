"""Exact replay of the single stopped candidate; no search or second room."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
HERE=Path(__file__).resolve().parent;BASE=HERE.parent.parent
src=BASE/'surplus-four-local/R23-top6-search/verify.py'
e={'__file__':str(src.resolve())};exec(compile(src.read_text().split('\ndef path(d,nine):')[0],str(src),'exec'),e)
fan,H=e['fan'],e['H']
raw=json.loads((HERE/'room.json').read_text());found=json.loads((HERE/'result.json').read_text())
assert found['status']=='FOUND_EXACT_PATH_PENDING_INDEPENDENT_VERIFICATION'
for name,key in [('room.json','room_sha256'),('search.py','search_source_sha256')]:assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==found[key]
P=[tuple(F(*x) for x in p) for p in found['candidate']['path']]
assert P==[(F(0),F(0)),(F(2,5),F(1)),(F(6,5),F(-1)),(F(14,5),F(3)),(F(3),F(5,2)),(F(8,5),F(-1)),(F(4,5),F(1)),(F(-2,7),F(-12,7)),(F(2,3),F(-4,3)),(F(2),F(2))]
assert found['candidate']['initial_direction']==[2,5] and found['candidate']['reflections']==8
W=[((0,1),(1,1)),((1,-1),(2,-1)),((2,3),(3,3)),((3,2),(3,3)),((1,-1),(2,-1)),((0,1),(1,1)),((-1,-1),(0,-2)),((0,-2),(1,-1))]
U,Z,events=e['constraints'](P,W)
print('COUNTS',len(U),len(Z))
for k in ['L','B','D','R','E','Tc','N']:
 print('U',k,[i for i in range(8) if fan(k,[i])&U]); print('Z',k,[i for i in range(8) if fan(k,[i])&Z])
minimum=H|fan('B',[1,2]);maximum=minimum|fan('B',[4,5,6,7])|fan('D',[0,1,3,4,5,6,7])|fan('E',[0,1,2,4,5,6,7])|fan('Tc',[0,1,2,3,4,5,7])|fan('N',[0,1,2,3,4,5,7])|fan('L',range(8))|fan('R',range(8))
assert Z==fan('B',[0,3])|fan('D',[2])|fan('E',[3])|fan('Tc',[6])|fan('N',[6])
q=P[-1]
for a,b in W[::-1]:
 v=e['reflect'](e['sub'](q,a),a,b);q=tuple(a[k]+v[k] for k in (0,1))
u,z,proof=e['audit'](P,W,minimum,maximum,q)
room={tuple(sorted(map(tuple,t))) for t in raw['triangles']}
assert room==H|set().union(*(fan(k,ss) for k,ss in raw['spec'].items()))
V=e['boundary'](room);assert len(V)==20 and set(V)==set(map(tuple,raw['vertices']))
e['physical'](P,V);e['physical'](P[::-1],V);sigma=e['sigma'];e['physical']([sigma(p) for p in P[::-1]],[sigma(p) for p in V])
assert minimum<=room<=maximum
assert all(not e['on']((0,0),a,b) for a,b in zip(P[1:],P[2:]))
# Recompute the frozen geometry independently from its triangles and polygon.
def angle(ts,p):
 n=0
 for t in ts:
  if p in t:
   a,b=[e['sub'](q,p) for q in t if q!=p];n+=90 if e['dot'](a,b)==0 else 45
 return n
pts={p for t in room for p in t};A={p for p in pts if p[0]%2==p[1]%2==0}
assert {p for p in A if angle(room,p)==360}=={(0,0),(2,0),(2,2)}
J=sum(angle(room,p)==360 for p in pts-A);sN=sum(angle(room,p)==180 for p in pts-A)
assert (J,sN)==(4,2)
for i,(a,b) in enumerate(zip(V,V[1:]+V[:1])):
 for j,(c,d) in enumerate(zip(V,V[1:]+V[:1])):
  if i<j and (j-i) not in (1,len(V)-1):assert not e['edge_times'](a,b,c,d)
# Prescribed symbolic itinerary evaluated only at the forced rational root.
d=F(2,5);assert F(5,13)<d<F(7,17) and 20*d-6==2
c=(6-16*d)/(1+d);r=(16*d-6)/(1-d)
formula=[(F(0),F(0)),(d,F(1)),(3*d,F(-1)),(7*d,F(3)),(F(3),10-3/d),(6-11*d,F(-1)),(6-13*d,F(1)),(c,-c-2),(r,r-2),(20*d-6,F(2))]
assert formula==P and q==(8,20)
assert 0<d<1 and 1<3*d<2 and 2<7*d<3 and 2<10-3/d<3
assert 1<6-11*d<2 and 0<6-13*d<1 and -1<c<0 and 0<r<1
# Both singular-looking intermediate lattice crossings are full interior support.
for p in [(F(2),F(1)),(F(0),F(-1))]:
 assert e['incident'](p)<=minimum and any(e['on'](p,a,b) for a,b in zip(P,P[1:]))
# One inward description plus symbolic outside-C envelopes; no extra room.
applications=[]
def inclusion(name,low,high,meaning):
 assert low<=high and U<=low and not Z&high and high<=maximum
 applications.append({'name':name,'meaning':meaning,'minimum':sorted(low),'maximum':sorted(high),'reflections':8})
ordinary=fan('E',[4])|fan('Tc',[5])|fan('N',[5])
low=minimum|fan('L',[6,7,0])|ordinary|fan('D',[1])|fan('R',[3])
inclusion('L670_BC_D1R3',low,low,'one remaining original inward description')
for shape in [(0,1,2),(0,1,2,3)]:
 low=minimum|fan('L',shape)|ordinary
 high=low|fan('D',[1])|fan('R',[3,4])
 inclusion('outside_L'+''.join(map(str,shape))+'_BC_noD2',low,high,'all One-DR choices D1/R3/R4 fit one upper support; D2 covered separately by accepted six')
# Accepted six handles the exact D2 complement for either outside-C L form.
prior=BASE/'fourth-surplus-review/peer-Bunit-six-independent/check.json'
six=json.loads(prior.read_text());assert six['status']=='INDEPENDENT_B_UNIT_SIX_AND_TWO_CONDITIONAL_INWARD_COVERS_PASS'
# Recompute only its supplied fixed path with our exact engine; no peer execution.
P6=[tuple(F(x) for x in p) for p in six['fixed_six']['path']]
W6=[tuple(map(tuple,w)) for w in six['fixed_six']['finite_mirrors']]
mi6=minimum|fan('D',[2]);ma6=mi6|fan('L',range(8))|fan('E',range(8))|fan('Tc',range(8))|fan('R',range(8))|fan('N',[0,1,2,3,4,5,7])
_,_,proof6=e['audit'](P6,W6,mi6,ma6,(-2,-12))
for shape in [(0,1,2),(0,1,2,3)]:
 low=mi6|fan('L',shape)|ordinary
 assert mi6<=low<=ma6
# Sigma plus time reversal gives a distinct useful E34 complement, no room.
PS=[sigma(p) for p in P[::-1]];WS=[(sigma(a),sigma(b)) for a,b in W[::-1]]
mis=e['transform'](minimum);mas=e['transform'](maximum)
assert mis==H|fan('E',[3,4])
ZS=e['transform'](Z)
for k in ['L','B','D','R','E','Tc','N']:print('SIGMA Z',k,[i for i in range(8) if fan(k,[i])&ZS])
qs=PS[-1]
for a,b in WS[::-1]:
 v=e['reflect'](e['sub'](qs,a),a,b);qs=tuple(a[k]+v[k] for k in (0,1))
us,zs,proofs=e['audit'](PS,WS,mis,mas,qs)
assert ZS==fan('E',[2,5])|fan('R',[3])|fan('B',[2])|fan('L',[7])|fan('N',[7])
sigma_applications=[]
for shape in [(0,1,2),(0,1,2,3)]:
 low=mis|fan('L',shape)|fan('B',[1])|fan('Tc',[5])|fan('N',[5])
 high=low|fan('D',[1,2])|fan('R',[4])
 assert us<=low<=high<=mas and not zs&high
 sigma_applications.append({'L':shape,'condition':'centered E34, One-DR D1/D2/R4 (R3 absent)','reflections':8,'minimum':sorted(low),'maximum':sorted(high)})
# Accepted six's sigma is exactly the R3-present E34 complement.
P6s=[sigma(p) for p in P6[::-1]];W6s=[(sigma(a),sigma(b)) for a,b in W6[::-1]]
mi6s=e['transform'](mi6);ma6s=e['transform'](ma6)
_,_,proof6s=e['audit'](P6s,W6s,mi6s,ma6s,(12,2))
for shape in [(0,1,2),(0,1,2,3)]:
 low=mi6s|fan('L',shape)|fan('B',[1])|fan('Tc',[5])|fan('N',[5])
 assert mi6s<=low<=ma6s
# Every forbidden tile really removes a declared mirror in the same exact path.
negative=[]
for t in sorted(Z):
 try:e['audit'](P,W,minimum,maximum|{t},q)
 except AssertionError:negative.append(t)
 else:raise AssertionError('missed mirror blocker')
assert len(negative)==6
out={'status':'PARENT_EIGHT_HAND_AND_WHOLE_BCENTER_TRANSFERS_PASS','path':[[str(x) for x in p] for p in P],'proof':proof,'required':sorted(U),'forbidden':sorted(Z),'minimum':sorted(minimum),'maximum':sorted(maximum),'applications':applications,'sigma_eight':{'path':[[str(x) for x in p] for p in PS],'proof':proofs,'required':sorted(us),'forbidden':sorted(zs),'minimum':sorted(mis),'maximum':sorted(mas),'applications':sigma_applications},'accepted_D2_complement_recheck':proof6,'accepted_R3_Ecenter_complement_recheck':proof6s,'outside_BC_EC_conclusion':'Both L012 and L0123 centered-B and centered-E One-DR rows covered <=8: BC D2 accepted6 versus noD2 new8; EC R3 accepted6 versus noR3 sigma8. Parent new8 and transfers pending independent review.','root':'2/5','endpoint_equation':'20d-6=2','strict_gate':['5/13','7/17'],'geometry':{'walls':20,'J':J,'s_N':sN,'full_A':'S,U,T','simple_polygon':'PASS'},'negative_controls':len(negative),'frozen_room_physical':'20 walls, first-wall/first actual T/reverse/sigma PASS','unfolded_target':list(map(str,q)),'source_sha256':{str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [src,HERE/'room.json',HERE/'result.json',HERE/'search.py',prior,BASE/'fourth-surplus-review/peer-Bunit-six-independent/review.txt',BASE/'surplus-four-local/e2-e1-b1/critical-L.txt']},'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'limits':'ONE stopped authorized pattern replay; no second room/search. Parent exact checks; independent review pending.'}
(HERE/'verification.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print('PASS',q)
