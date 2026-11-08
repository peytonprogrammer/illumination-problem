"""Validate ONE stopped nine-candidate; truncate its exact S loop to FOUR.
No discovery rerun or extra room. Own Fraction primitive prefix only.
"""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
HERE=Path(__file__).resolve().parent;BASE=HERE.parent.parent
src=BASE/'surplus-four-local/R23-top6-search/verify.py';e={'__file__':str(src)}
exec(compile(src.read_text().split('\ndef path(d,nine):')[0],str(src),'exec'),e)
fan,H=e['fan'],e['H'];fp=lambda ps:[tuple(F(x)for x in p)for p in ps]
raw=json.loads((HERE/'room.json').read_text());found=json.loads((HERE/'result.json').read_text())
assert found['status']=='FOUND_EXACT_PATH_PENDING_INDEPENDENT_VERIFICATION'
for n,k in [('room.json','room_sha256'),('search.py','search_source_sha256')]:assert hashlib.sha256((HERE/n).read_bytes()).hexdigest()==found[k]
long=[tuple(F(*x)for x in p)for p in found['candidate']['path']]
assert len(long)==11 and e['on']((0,0),long[5],long[6]) and (0,0)not in(long[5],long[6])
P=[(F(0),F(0))]+long[6:]
assert P==fp([(0,0),(-2,'3/2'),('-12/7','12/7'),(-2,'4/3'),('-1/4',-1),(2,2)])
walls=[((-2,1),(-2,2)),((-2,2),(-1,1)),((-2,1),(-2,2)),((-1,-1),(0,-1))]
mi=H|fan('L',[7,0,1])|fan((-2,2),[6])
allK=H|set().union(*(fan(k,range(8))for k in e['C']))
ma=(allK-fan('B',[2]))|fan((-2,2),[6])
u,z,proof=e['audit'](P,walls,mi,ma,(-8,6))
assert z==fan('B',[2])|fan((-2,2),[5,7])
for a,b in zip(P[1:-1],P[2:]):assert not e['on']((0,0),a,b)
room={tuple(sorted(map(tuple,t)))for t in raw['triangles']}
assert room==H|set().union(*(fan(k,ss)for k,ss in raw['spec'].items()))|fan((-2,2),[6])
assert len(room)==35 and mi<=room<=ma
V=e['boundary'](room);assert len(V)==20 and set(V)==set(map(tuple,raw['vertices']))
e['physical'](P,V);e['physical'](P[::-1],V);e['physical']([e['sigma'](p)for p in P[::-1]],[e['sigma'](p)for p in V])
assert e['incident']((F(-1),F(0)))<=mi and e['on']((-1,0),P[3],P[4])
# Direct hand parameterization of the SHORTENED actual trajectory.
def path(d):
 a=4*d/(1+d)
 return fp([(0,0),(-2,2*d),(-a,a),(-2,4-2/d),(5*d-4,-1),(8*d-4,2)])
d=F(3,4);lo,hi=F(5,7),F(4,5)
assert path(d)==P and lo<d<hi and 8*d-4==2
checks=[(lambda t:2*t,1,2),(lambda t:-4*t/(1+t),-2,-1),(lambda t:4-2/t,1,2),(lambda t:5*t-4,-1,0),(lambda t:-1/t,-2,-1),(lambda t:3*t-4,-2,-1),(lambda t:4-3/t,-1,1),(lambda t:7*t-4,1,3)]
for fn,a,b in checks:
 x,y=fn(lo),fn(hi);assert a<=x<=b and a<=y<=b and x!=y,(x,y,a,b)
# All other six local stars may be arbitrary except B2. Whole-family,
# not a claim that the maximum itself is a valid room.
assert not z&set().union(*(fan(k,range(8))for k in ['D','R','E','Tc','N']))
assert not z&fan('L',range(8))
# Full class relevance: Bcenter12 with fixedL7 makes unhealed B180;
# the sole remoteleaf is ABOVE, so it cannot heal(-1,-1).
def angle(ts,p):
 return sum(90 if e['dot'](*[e['sub'](v,p)for v in t if v!=p])==0 else 45 for t in ts if p in t)
bc=mi|fan('B',[1,2]);other=fan('D',range(8))|fan('R',range(8))|fan('E',range(8))|fan('Tc',range(8))|fan('N',range(8))
assert angle(bc,(-1,-1))==angle(bc|other,(-1,-1))==180
pts={p for t in room for p in t};A={p for p in pts if p[0]%2==p[1]%2==0}
assert {p for p in A if angle(room,p)==360}=={(0,0),(2,0),(2,2)}
J=sum(angle(room,p)==360 for p in pts-A);sN=sum(angle(room,p)==180 for p in pts-A)
Q=sum(3 if angle(room,p)==180 else angle(room,p)//45 for p in A if angle(room,p)!=360)
assert (J,sN,Q,J+sN,Q+sN-8)==(4,2,10,6,4)
reads=[src,Path(__file__),HERE/'room.json',HERE/'result.json',HERE/'search.py']
out={'status':'PARENT_SHORTENED_REMOTE_LEAF_FOUR_WHOLE_L7012_LEAF6_ORIENTATION_PASS','path':[[str(x)for x in p]for p in P],'walls':walls,'minimum':sorted(mi),'maximum':sorted(ma),'required':sorted(u),'forbidden':sorted(z),'proof':proof,'root':'3/4','strict_gate':['5/7','4/5'],'actual_endpoint_equation':'8d-4=2','candidate_loop_reconciliation':'Search returned9reflectingcandidate with exactS revisit betweencontacts5and6. Discardclosedprefix5; suffix startsactualS withdirection(-4,3) andhas4reflections, noSrevisit.','original_search_direction':[-4,-3],'actual_shortened_direction':[-4,3],'geometry':{'tiles':35,'W':20,'J':4,'sN':2,'Q':10,'k':6,'Delta':4,'fullA':'SUT'},'structural_Bcenter_exclusion':'FixedL7+H+B12 givesunhealableoddodd(-1,-1)180, impossibleb0 whensole remoteis(-2,2)6.','parent_whole_2110_fixed_orientation_claim':'ForL7012+remote(-2,2)6, B1missing usesone. Otherwise B ordinaryB1 oractiveunitBO01 avoidsB2; unitBC12 excludedb0. Thus ALLadditionalunitlocations/ordinarychoices in2110 fixedorientation illuminate<=4. In2101 BordinaryB1 makessamecorollary. Exact localunitforcing/root assumptions inherited, fullparent/leafclassificationstillseparate.','source_sha256':{str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest()for p in reads},'limits':'ONE fixedN5D2 search, stop41directions; no further room/search/archive. ExactSsuffixalgebra, fullguards/actualfrozenboundary verified. Parentwholeorientationneedsindependentreview, notwhole2110/Delta4.'}
(HERE/'verification.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(out['status'],len(u),'U',len(z),'Z; looptruncated9to4; wholeotherKsafe exceptB2')
