"""Standalone own Fraction verification of ONLY the stopped O3 candidate.
No search, no new room; conditional whole supports and frozen physical room.
"""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
HERE=Path(__file__).resolve().parent;BASE=HERE.parent.parent
engine_source=BASE/'surplus-four-local/R23-top6-search/verify.py'
e={'__file__':str(engine_source.resolve())};exec(compile(engine_source.read_text().split('\ndef path(d,nine):')[0],str(engine_source),'exec'),e)
fan,H,audit=e['fan'],e['H'],e['audit'];boundary,physical=e['boundary'],e['physical']
raw=json.loads((HERE/'room.json').read_text());found=json.loads((HERE/'result.json').read_text())
assert found['status']=='FOUND_EXACT_PATH_PENDING_INDEPENDENT_VERIFICATION'
assert hashlib.sha256((HERE/'room.json').read_bytes()).hexdigest()==found['room_sha256']
assert hashlib.sha256((HERE/'search.py').read_bytes()).hexdigest()==found['search_source_sha256']
P=[(F(0),F(0)),(F(-1),F(-2,5)),(F(1),F(-6,5)),(F(0),F(-8,5)),(F(1),F(-2)),(F(2,7),F(-16,7)),(F(2),F(2))]
assert P==[tuple(F(*x) for x in p) for p in found['candidate']['path']]
assert found['candidate']['initial_direction']==[-5,-2] and found['candidate']['reflections']==5
room={tuple(sorted(map(tuple,t))) for t in raw['triangles']}
V=boundary(room);assert len(V)==20 and set(V)==set(map(tuple,raw['vertices']))
physical(P,V);physical(P[::-1],V)
sigma=e['sigma'];physical([sigma(p) for p in P[::-1]],[sigma(p) for p in V])
mi=H|fan('B',[7,0,1])
ma=mi|fan('L',[0,1,2,3,4,5,6])|fan('D',[0,1,2,5,6,7])|set().union(*(fan(k,range(8)) for k in ['R','E','Tc','N']))
W=[((-1,-1),(-1,0)),((1,-3),(1,-1)),((0,-2),(0,-1)),((1,-3),(1,-1)),((0,-2),(1,-3))]
u,z,proof=audit(P,W,mi,ma,(-10,-4));assert mi<=room<=ma
assert z==fan('L',[7])|fan('D',[3,4])|fan('B',[2,6])
assert (1,-2) not in V
wall=[(a,b) for a,b in zip(V,V[1:]+V[:1]) if e['on']((1,-2),a,b)]
assert len(wall)==1 and set(wall[0])=={(1,-3),(1,-1)}
def angle(ts,p):
 n=0
 for t in ts:
  if p in t:
   a,b=[e['sub'](q,p) for q in t if q!=p];n+=90 if e['dot'](a,b)==0 else 45
 return n
assert angle(room,(1,-2))==180
pts={p for t in room for p in t};As={p for p in pts if p[0]%2==p[1]%2==0}
assert {p for p in As if angle(room,p)==360}=={(0,0),(2,0),(2,2)}
J=sum(angle(room,p)==360 for p in pts-As);sN=sum(angle(room,p)==180 for p in pts-As)
assert (J,sN)==(2,4)
d=F(2,5);assert F(1,3)<d<F(3,7)
assert P==[(F(0),F(0)),(F(-1),-d),(F(1),-3*d),(F(0),-4*d),(F(1),-5*d),((6*d-2)/(1+d),-8*d/(1+d)),(10*d-2,F(2))]
assert 0<7*d-2<1 and 1<9*d-2<3 and -1<3/d-8<1
# Whole unit-partner support implications, not rooms or cap assignments.
forms={'L':[[0,1]],'D':[[0,1],[1,2]],'R':[[2,3],[3,4],[4,5]],'E':[[2,3],[3,4],[4,5]],'Tc':[[4,5],[5,6],[6,7]],'N':[[4,5],[5,6],[6,7],[7,0],[0,1]]}
for k,units in forms.items():
 for ss in units:assert mi|fan(k,ss)<=ma
assert z&fan('L',[7]) and z&fan('D',[3]) and z&fan('D',[4])
# Accepted O3+D23 four/six exception, conditional ordinary Tc split.
prior=BASE/'fourth-surplus-review/mixed-e2-e1/joined-four-check.json'
old=json.loads(prior.read_text());accepted_source=BASE/'surplus-four-local/joined-six-review/check.json';accepted=json.loads(accepted_source.read_text())
assert hashlib.sha256(prior.read_bytes()).hexdigest()==accepted['source_sha256'][str(prior.relative_to(BASE))]
def decode(ts):return {tuple(sorted(map(tuple,t))) for t in ts}
D23=fan('D',[2,3]);other=set().union(*(fan(k,range(8)) for k in ['L','R','E','N']))
for r,minimum,maximum in [(old,mi|D23,mi|D23|other|fan('Tc',[0,1,2,3,4,6,7])),(old['six_path_complement'],mi|D23|fan('Tc',[5]),mi|D23|other|fan('Tc',[5]))]:
 assert decode(r['required'])<=minimum and not decode(r['forbidden'])&maximum
forcing_source=BASE/'surplus-four-local/e2-e1-b1/critical-B-check.json'
forcing=json.loads(forcing_source.read_text())
force_cases={r['name']:r['reflections'] for r in forcing['whole_envelopes'] if r['name'].startswith('force_')}
for name,bound in [('force_E4',1),('force_L0_Eordinary',4),('force_L0_Ecenter',3),('force_L0_Eouter',2)]:assert force_cases[name]==bound
sources=[HERE/'room.json',HERE/'result.json',HERE/'search.py',engine_source,prior,accepted_source,forcing_source,BASE/'surplus-four-local/e2-e1-b1/critical-B.txt']
out={'status':'FROZEN_O3_FIVE_AND_WHOLE_SUPPORT_PASS','path':[[str(x) for x in p] for p in P],'reflections':5,'initial_direction':[-5,-2],'physical_room':{'walls':20,'J':J,'s_N':sN,'full_A':'S,U,T','smooth_C':180,'finitewall_firstT_reverse_sigma':'PASS'},'whole_support':{'minimum':sorted(mi),'maximum':sorted(ma),'required':sorted(u),'forbidden':sorted(z)},'proof':proof,'hand_endpoint':'10d-2=2','root':'2/5','sufficient_gate':['1/3','3/7'],'conditional_branch_claim':'All O3 two-root b1 partners except L70 covered <=6 after accepted reference forcing; D23 uses accepted4/6. L70 remains open. Independent review pending.','source_sha256':{str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'limits':'ONE explicitly authorized O3/R23 discovery STOPPED first candidate57directions; only frozen room replayed. Own standalone Fraction definitions, no peer geometry. No extra room/search or unused budget reuse. Conditional maxima not rooms. Parent verification, not independent/expert/formal acceptance or full O3/Delta4 closure.'}
(HERE/'verification.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print('PASS: actual5/full',len(u),'U',len(z),'Z; frozen20wall/J2/sN4; smoothC180; finitewalls/firstT/reverse/sigma; unfold(-10,-4).')
