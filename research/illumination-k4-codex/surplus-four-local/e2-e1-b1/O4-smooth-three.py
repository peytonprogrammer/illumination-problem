"""Verify one hand-derived path and whole supports. No room or search."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
HERE=Path(__file__).resolve().parent;BASE=HERE.parent.parent
source=BASE/'surplus-four-local/R23-top6-search/verify.py'
# Load only our frozen, helper-free Fraction definitions. No frozen-room replay.
prefix=source.read_text().split('\ndef path(d,nine):')[0]
engine={'__file__':str(source.resolve())};exec(compile(prefix,str(source),'exec'),engine)
fan,H=engine['fan'],engine['H'];audit=engine['audit'];incident=engine['incident'];on=engine['on']
P=[(F(0),F(0)),(F(1),F(-2)),(F(1,2),F(-3)),(F(0),F(-2)),(F(2),F(2))]
walls=[((1,-3),(1,-1)),((0,-3),(1,-3)),((0,-3),(0,-1))]
minimum=H|fan('B',[6,7,0,1])
maximum=minimum|fan('D',[0,1,2,5,6,7])|set().union(*(fan(k,range(8)) for k in ['L','R','E','Tc','N']))
# Reflect actualT through last x0, floor-3, firstx1 gives actualimage(4,-8).
U,Z,proof=audit(P,walls,minimum,maximum,(4,-8))
assert Z==fan('B',[2,3,4,5])|fan('D',[3,4])|fan((0,-4),[1])
def angle(ts,p):
 n=0
 for t in ts:
  if p in t:
   a,b=[(q[0]-p[0],q[1]-p[1]) for q in t if q!=p]
   n+=90 if a[0]*b[0]+a[1]*b[1]==0 else 45
 return n
for p in [(1,-2),(0,-2)]:assert angle(minimum,p)==180
# At each smooth contact all incident interior half-plane tiles are required,
# all exterior half-plane tiles forbidden: no missing mirror at lattice events.
for p in [(1,-2),(0,-2)]:assert incident(p)==(U|Z)&incident(p)
assert incident((F(1),F(0)))<=H and on((1,0),P[3],P[4])
d=F(1,2);assert F(3,7)<d<F(3,5)
assert P==[(F(0),F(0)),(F(1),-1/d),(2-3*d,F(-3)),(F(0),2/d-6),(8*d-2,F(2))]
assert -3<-1/d<-1 and 0<2-3*d<1 and -3<2/d-6<-1 and 0<5*d-2<1 and 1<7*d-2<3
# Independent ROOT fan windows after accepted reference forcing.
forms={'L':[[6,7],[7,0],[0,1]],'D':[[0,1],[1,2],[2,3]],'E':[[2,3],[3,4],[4,5]],'R':[[2,3],[3,4],[4,5]],'Tc':[[4,5],[5,6],[6,7]],'N':[[4,5],[5,6],[6,7],[7,0],[0,1]]}
applications=[]
for site,units in forms.items():
 for ss in units:
  if site=='D' and ss==[2,3]:
   applications.append({'site':site,'sectors':ss,'cover':'accepted square two/four ordinary-Tc split','bound':4});continue
  assert minimum|fan(site,ss)<=maximum
  applications.append({'site':site,'sectors':ss,'cover':'NEW3 entire support','bound':3})
# D23 exceptions refer to already independently accepted square exchange.
oldsource=BASE/'fourth-surplus-review/mixed-e2-e1/joined-square-check.json'
old=json.loads(oldsource.read_text())
accepted_source=BASE/'surplus-four-local/joined-square-review/check.json'
accepted=json.loads(accepted_source.read_text())
assert hashlib.sha256(oldsource.read_bytes()).hexdigest()==accepted['source_sha256'][str(oldsource.relative_to(BASE))]
def decode(ts):return {tuple(sorted(map(tuple,t))) for t in ts}
D23=fan('D',[2,3]);other=set().union(*(fan(k,range(8)) for k in ['L','R','E','N','D']))
for name,mi,ma in [('two',minimum|D23,minimum|D23|other|fan('Tc',[0,1,2,3,4,6,7])),('four',minimum|D23|fan('Tc',[5]),minimum|D23|other|fan('Tc',[5]))]:
 r=old['paths'][name]
 assert decode(r['required'])<=mi and not decode(r['forbidden'])&ma
 assert r['reflections'] in [2,4]
# No L0/E4 forcing is needed: the new maximum allows FULL L/E.
for k in ['L','R','E','Tc','N']:assert fan(k,range(8))<=maximum
assert fan('D',[1,2])<=maximum
assert fan((0,-4),[1])&Z and not fan((0,-4),[1])&maximum

receipt={'status':'PARENT_O4_SMOOTH_THREE_SUPPORT_PASS','path':[[str(x) for x in p] for p in P],'reflections':3,'whole_support':{'minimum':sorted(minimum),'maximum':sorted(maximum),'required':sorted(U),'forbidden':sorted(Z)},'proof':proof,'smooth_contacts':{'(1,-2)':180,'(0,-2)':180},'endpoint':'8d-2=2','root':'1/2','sufficient_strict_gate':['3/7','3/5'],'applications':applications,'parent_O4_two_root_b1_bound':4,'source_sha256':{str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [source,oldsource,accepted_source,BASE/'surplus-four-local/joined-square-review/review.txt',HERE/'critical-B.txt',BASE/'fourth-surplus-review/peer-critical-B-b1-independent/review.txt']},'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'limits':'One hand-derived path, complete finite-wall/segment U-Z and reverse/sigma. No new room, direction/word search, census, archive or worker. Parent proof awaits independent hand review. BothD3/D4block, no singleleaf transfer. Whole branch inherits local two-root classification and accepted D23 square2/4. No L/E reference forcing needed; full L/E support allowed.'}
(HERE/'O4-smooth-three.json').write_text(json.dumps(receipt,indent=2,default=str)+'\n')
print('PASS: handO4three; U',len(U),'Z',len(Z),'finite mirrors/reverse/sigma/unfold(4,-8); parent whole O4 two-root b1<=4 pending independent review.')
