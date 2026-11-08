"""One fixed accepted six-path against the named whole West/D2 envelope."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
HERE=Path(__file__).resolve().parent;BASE=HERE.parent.parent
src=BASE/'surplus-four-local/R23-top6-search/verify.py'
e={'__file__':str(src)}
exec(compile(src.read_text().split('\ndef path(d,nine):')[0],str(src),'exec'),e)
fan,H=e['fan'],e['H'];reads=[src,Path(__file__)]
parentfile=BASE/'surplus-four-local/mixed-H4-R23-search/verification.json'
parent=json.loads(parentfile.read_text());reads.append(parentfile)
reviewfile=BASE/'fourth-surplus-review/peer-E4-six-independent/check.json'
peer=json.loads(reviewfile.read_text());reads.append(reviewfile)
for receipt in (parent,peer):
 for rel,h in receipt['source_sha256'].items():
  p=BASE/rel;reads.append(p);assert hashlib.sha256(p.read_bytes()).hexdigest()==h,rel
P=[tuple(F(x) for x in p) for p in parent['path']]
walls=[tuple(tuple(F(x) for x in p) for p in wall) for wall in parent['walls']]
assert len(P)==8 and P[0]==(0,0) and P[-1]==(2,2)
assert P==[(F(0),F(0)),(F(4,5),F(1)),(F(12,5),F(-1)),(F(3),F(-1,4)),(F(1),F(9,4)),(F(8,5),F(3)),(F(28,9),F(10,9)),(F(2),F(2))]
for a,b in zip(P[1:-1],P[2:]):assert not e['on']((0,0),a,b)
mi=H|fan('E',[4])
west=H|fan('B',[1,2,3,4])|fan('L',[7,0])|fan('E',[4])|fan('Tc',[6])|fan('R',[3])|fan('N',[7])|fan('D',[2])
u,z,proof=e['audit'](P,walls,mi,west,(8,10))
assert len(u)==19 and z==set().union(*(fan(k,ss) for k,ss in [('D',[1]),('R',[4]),('N',[0,6]),('Tc',[5]),('E',[5])]))
assert not z&west and u<=mi<=west
assert z&fan('D',[1])==fan('D',[1])
# Rejecting this one path with D1 does not imply darkness of D1 rooms.
for rel in ['fourth-surplus-review/peer-E4-six-independent/review.txt','fourth-surplus-review/peer-E4-six-independent/coverage.txt','fourth-surplus-review/west1234-coupled/argument.txt']:
 reads.append(BASE/rel)
out={'status':'INDEPENDENT_WEST_D2_SIX_TRANSFER_ACCEPT','reflections':6,'required':sorted(u),'forbidden':sorted(z),'whole_West_D2_upper':sorted(west),'proof':proof,'D1_control':'This fixed path requires D1 absence; no D1 darkness or impossibility conclusion.','limits':'Whole-family fixed-path transfer conditional on accepted West forced-cap classification/localK; no West polygon reconstructed, no discovery/cap assignments/peer checker execution.','source_sha256':{str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in dict.fromkeys(reads)}}
(HERE/'check.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(out['status'],'19U6Z/finite6/firstT/noSrevisit/reverse/sigma/unfold8,10; WestD2 upper fits; D1 blocks this path')
