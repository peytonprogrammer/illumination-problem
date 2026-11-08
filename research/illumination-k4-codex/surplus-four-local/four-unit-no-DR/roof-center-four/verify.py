"""Hand-derived FOUR, symmetric FOUR and whole remaining support envelopes.
No room construction or discovery. Own Fraction engine only.
"""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
HERE=Path(__file__).resolve().parent;BASE=HERE.parents[2]
src=BASE/'surplus-four-local/R23-top6-search/verify.py'
e={'__file__':str(src)}
exec(compile(src.read_text().split('\ndef path(d,nine):')[0],str(src),'exec'),e)
fan,H=e['fan'],e['H']
d=F(1,6)
def path(t):
 a=8*t/(1-t);b=(4-8*t)/(1+t)
 return [(F(0),F(0)),(t,F(1)),(4*t,F(-2)),(a,a+2),(b,6-b),(4-12*t,F(2))]
P=path(d)
assert P[-1]==(2,2)
walls=[((0,1),(1,1)),((0,-2),(1,-2)),((1,3),(2,4)),((2,4),(3,3))]
mi=H|fan('B',[0,1])|fan('Tc',[5,6])
maxi=H|fan('B',[0,1,2,3,4,5,6])|fan('Tc',[0,1,2,3,5,6])|fan('N',[0,1,2,3,4,5,7])|set().union(*(fan(k,range(8)) for k in ['L','E','D','R']))
# Actual mirror unfolding computed independently rather than asserted.
image=P[-1]
for a,b in walls[::-1]:
 v=e['reflect'](e['sub'](image,a),a,b);image=tuple(a[k]+v[k] for k in (0,1))
u,z,proof=e['audit'](P,walls,mi,maxi,image)
assert len(walls)==4 and image==(2,12)
assert z==fan('B',[7])|fan('Tc',[4,7])|fan('N',[6])
assert not (u|z)&(fan('D',range(8))|fan('R',range(8)))
for a,b in zip(P[1:-1],P[2:]):assert not e['on']((0,0),a,b)
# The earlier ascending crossing of(1,0) is fullH interior.
assert e['on']((1,0),P[2],P[3]) and e['incident']((F(1),F(0)))<=H
# All contacts and portal coordinates are monotone with no pole on this
# interval. Closed endpoint inequalities imply strict inequalities inside.
lo,hi=F(1,7),F(2,11)
assert lo<d<hi
for t in (lo,hi):
 a=8*t/(1-t);b=(4-8*t)/(1+t)
 assert 0<t<1 and 0<4*t<1
 assert 1<=7*t<=2 and 1<9*t<2
 assert 1<a<2 and 2<b<3
 assert 2<=4-11*t<=3
# Algebraic coefficients give outgoing line x=d*y+4-14d after roof pair.
# At y2 target x4-12d; exact identities at both endpoints and root are
# redundant arithmetic checks of the displayed linear identities.
for t in (lo,d,hi):
 a=8*t/(1-t);b=(4-8*t)/(1+t)
 assert a+2-t*a==8*t+2
 assert (1+t)*b==4-8*t
 assert b-t*(6-b)==4-14*t
# Whole missing-label upper envelopes from the proof, not valid rooms.
fixed=H|fan('L',[7,0])|fan('B',[0,1])|fan('E',[4,5])|fan('Tc',[5,6])
ordinary=fan('D',[1,2])|fan('R',[3,4])
applications=[]
for n in [(),(6,),(7,)]:
 upper=fixed|ordinary|fan('N',n)
 use_sigma=n==(6,)
 uu,zz=(e['transform'](u),e['transform'](z)) if use_sigma else (u,z)
 assert uu<=fixed|fan('N',n) and not zz&upper
 applications.append({'ordinary_N':n,'sigma':use_sigma,'reflections':4,'maximum':sorted(upper)})
reads=[src,Path(__file__),BASE/'second-surplus-review/five-path-check.json']
out={'status':'PARENT_HAND_ROOF_CENTER_FOUR_AND_THREE_REMAINING_ENVELOPES_PASS','path':[[str(x) for x in p] for p in P],'walls':walls,'minimum':sorted(mi),'maximum':sorted(maxi),'required':sorted(u),'forbidden':sorted(z),'proof':proof,'image':image,'parameter':'1/6','strict_gate':['1/7','2/11'],'endpoint_equation':'4-12d=2','applications':applications,'source_sha256':{str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in reads},'limits':'Hand derivation/fixed exact path only, no completed room/search. Full four-unit shape/forcing/b0 classification and independent review separate. No fullDelta4 claim.'}
(HERE/'verification.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(out['status'],len(u),'U',len(z),'Z',proof)
