"""One stopped L7012 candidate, exact Fraction full support; no search."""
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
P=[tuple(F(*x) for x in p) for p in j['candidate']['path']]
assert P==[(F(0),F(0)),(F(-4,3),F(1)),(F(-16,7),F(2,7)),(F(-7,4),F(1)),(F(-1,4),F(-1)),(F(2),F(2))]
W=[((-3,1),(-1,1)),((-3,1),(-2,0)),((-3,1),(-1,1)),((-1,-1),(0,-1))]
U,Z,_=e['constraints'](P,W)
print('COUNTS',len(U),len(Z))
for k in ['L','B','D','R','E','Tc','N']:print('U',k,[i for i in range(8) if fan(k,[i])&U]);print('Z',k,[i for i in range(8) if fan(k,[i])&Z])
mi=H|fan('L',[7,0,1,2]);ma=mi|fan('L',[4,5,6])|fan('B',[0,1,3,4,5,6,7])|set().union(*(fan(k,range(8)) for k in ['D','R','E','Tc','N']))
q=P[-1]
for a,b in W[::-1]:
 v=e['reflect'](e['sub'](q,a),a,b);q=tuple(a[k]+v[k] for k in (0,1))
u,z,proof=e['audit'](P,W,mi,ma,q)
room={tuple(sorted(map(tuple,t))) for t in raw['triangles']};assert room==H|set().union(*(fan(k,ss) for k,ss in raw['spec'].items()))
V=e['boundary'](room);assert len(V)==20 and set(V)==set(map(tuple,raw['vertices']))
e['physical'](P,V);e['physical'](P[::-1],V);sigma=e['sigma'];e['physical']([sigma(p) for p in P[::-1]],[sigma(p) for p in V])
assert mi<=room<=ma
assert Z==fan('L',[3])|fan('B',[2])|fan((-2,2),[6])
assert all(not e['on']((0,0),a,b) for a,b in zip(P[1:],P[2:]))
d=F(3,4);assert F(5,7)<d<F(4,5) and -4+8*d==2
c=-4/(1+d)
assert P==[(F(0),F(0)),(-1/d,F(1)),(c,-c-2),(-4+3*d,F(1)),(-4+5*d,F(-1)),(-4+8*d,F(2))]
assert -2<-1/d<-1 and -3<c<-2 and -2<-4+3*d<-1 and -1<-4+5*d<0
assert -1<4-3/d<1 and 1<-4+7*d<3 and q==(-8,6)
assert e['on']((-1,0),P[3],P[4]) and e['incident']((F(-1),F(0)))<=mi
# One upper contains every originally remaining L7012 description and all
# other allowed table rows. It is not assembled as a room.
upper=mi|fan('B',[0,1])|set().union(*(fan(k,range(8)) for k in ['D','R','E','Tc','N']))
assert U<=mi<=upper<=ma and not Z&upper
refs=fan('B',[1])|fan('Tc',[5])
cases=[('EO_D2',fan('E',[4,5])|fan('N',[5])|fan('D',[2])),('EO_R3',fan('E',[4,5])|fan('N',[5])|fan('R',[3])),('EC_D2_R4',fan('E',[3,4])|fan('N',[5])|fan('D',[2])|fan('R',[4])),('DC_R3',fan('D',[1,2])|fan('E',[4])|fan('N',[5])|fan('R',[3])),('DQ23',fan('D',[2,3])|fan('E',[4])|fan('N',[5])),('RQ23',fan('R',[2,3])|fan('E',[4])|fan('N',[5])),('NSW_D2',fan('N',[4,5])|fan('E',[4])|fan('D',[2])),('NSW_R3',fan('N',[4,5])|fan('E',[4])|fan('R',[3]))]
for name,extra in cases:assert U<=mi|refs|extra<=upper
# Reconstruct only supplied frozen polygon geometry and full A ledger.
def angle(ts,p):
 n=0
 for t in ts:
  if p in t:
   a,b=[e['sub'](x,p) for x in t if x!=p];n+=90 if e['dot'](a,b)==0 else 45
 return n
pts={p for t in room for p in t};A={p for p in pts if p[0]%2==p[1]%2==0}
assert {p for p in A if angle(room,p)==360}=={(0,0),(2,0),(2,2)}
assert sum(angle(room,p)==360 for p in pts-A)==3 and sum(angle(room,p)==180 for p in pts-A)==3
for i,(a,b) in enumerate(zip(V,V[1:]+V[:1])):
 for k,(c,f) in enumerate(zip(V,V[1:]+V[:1])):
  if i<k and (k-i) not in (1,len(V)-1):assert not e['edge_times'](a,b,c,f)
# Both top contacts are inside a single straight maximal horizontal wall.
for hit in [P[1],P[3]]:
 cw=[(a,b) for a,b in zip(V,V[1:]+V[:1]) if e['on'](hit,a,b)]
 assert len(cw)==1 and set(cw[0])=={(-3,1),(-1,1)} and hit not in cw[0]
# Original Bcenter exclusion is preserved: fixed second smooth point.
BC=mi|fan('B',[1,2])|set().union(*(fan(k,range(8)) for k in ['D','R','E','Tc','N']))
assert angle(BC,(-2,1))==angle(BC,(-1,-1))==180
for t in Z:
 try:e['audit'](P,W,mi,ma|{t},q)
 except AssertionError:pass
 else:raise AssertionError('missed blocker')
sources=[src,HERE/'room.json',HERE/'result.json',HERE/'search.py',BASE/'surplus-four-local/outside-C-frontier.txt',BASE/'surplus-four-local/e2-e1-b1/critical-L.txt',BASE/'fourth-surplus-review/peer-critical-L-classification-independent/review.txt']
out={'status':'PARENT_L7012_FOUR_AND_WHOLE_EIGHT_REMAINING_DESCRIPTIONS_PASS','path':[[str(x) for x in p] for p in P],'walls':W,'proof':proof,'required':sorted(U),'forbidden':sorted(Z),'minimum':sorted(mi),'maximum':sorted(ma),'image':list(map(str,q)),'frozen_physical':'20wall firstwall/firstactualT/reverse/sigma PASS','root':'3/4','strict_gate':['5/7','4/5'],'endpoint_equation':'-4+8d=2','whole_table_upper':sorted(upper),'eight_case_inclusions':[name for name,_ in cases],'geometry':{'W':20,'J':3,'s_N':3,'Q':9,'k':6,'Delta':4,'full_A':'S,U,T'},'source_sha256':{str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'limits':'ONE stoppedauthorizedpattern, noadditionalroom/search/capproduct/worker. ParentwholeL7012<=4 pendingindependentreview; remote(-2,2)6 expresslyabsentbylocalK, fullDelta4open.'}
(HERE/'verification.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print('PASS',q,'REMOTE Z',Z-set().union(*(fan(k,range(8)) for k in ['L','B','D','R','E','Tc','N'])))
