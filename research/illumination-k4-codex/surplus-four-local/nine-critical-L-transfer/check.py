"""Static support transfer of an already verified fixed nine-path.
No room, new ray, cap-assignment census or source-checker execution.
"""
from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent;BASE=HERE.parent.parent
rays=((1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1))
centers={'L':(-2,0),'B':(0,-2),'D':(2,-2),'R':(4,0),'E':(4,2),'Tc':(2,4),'N':(0,2)}
def fan(a,ss):
 a=centers[a] if isinstance(a,str) else a
 return {tuple(sorted((a,(a[0]+rays[i][0],a[1]+rays[i][1]),(a[0]+rays[(i+1)%8][0],a[1]+rays[(i+1)%8][1])))) for i in ss}
def decode(ts):return {tuple(sorted(map(tuple,t))) for t in ts}
src=BASE/'surplus-four-local/L70-N7-search/verification.json'
j=json.loads(src.read_text());assert j['status']=='PARENT_L70_N7_ELEVEN_NINE_PASS'
verify=src.parent/'verify.py';assert hashlib.sha256(verify.read_bytes()).hexdigest()==j['checker_sha256']
r=j['nine'];u,z=decode(r['required']),decode(r['forbidden']);max9=decode(r['maximum'])
H=set().union(*(fan(a,range(8)) for a in [(0,0),(2,0),(2,2)]))
# One lower support common to both original named D-/D+ descriptions.
mi=H|fan('L',[7,0,1])|fan('E',[3,4])|fan('B',[1])|fan('Tc',[5])|fan('N',[7])|fan('R',[3])
ma=mi|fan('D',range(8))
assert u<=mi<=ma<=max9 and not z&ma
assert (len(u),len(z))==(21,7)
assert z==fan('L',[6])|fan('B',[2])|fan('R',[2,4])|fan('N',[0,5,6])
# The key L1 is allowed; the older six/eleven upper-L mirrors forbid it.
assert fan('L',[1])<=max9 and not z&fan('L',[1])
# Do not overextend into the outside-C row requiring ordinaryN5 instead ofN7.
assert z&fan('N',[5])
table=BASE/'surplus-four-local/e2-e1-b1/critical-L.txt'
t=table.read_text();assert 'TWO:   L701 +EC+B+/T-/Nr- +R+ and D- or D+.' in t
sources=[src,verify,table,BASE/'fourth-surplus-review/peer-critical-L-classification-independent/review.txt',BASE/'fourth-surplus-review/peer-critical-L-optical-independent/review.txt']
out={'status':'PARENT_NINE_L701_ECENTER_N7_R3_TRANSFER_PASS','required':len(u),'forbidden':len(z),'common_minimum':sorted(mi),'maximum_with_full_D':sorted(ma),'removed_named_descriptions':['L701+E34+B1+Tc5+N7+R3+D2','L701+E34+B1+Tc5+N7+R3+D1'],'bound':9,'independent_status':'Newnine opticallemma and thistransfer pending peerHANDreview; inherited criticalL classification accepted separately.','relative_inward_count':'Ifaccepted, priorrecordedeight inward descriptions reduce bytwo tosix; not roomcounts or fullcriticalL closure.','source_sha256':{str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},'limits':'One static whole-envelope inclusion, no constructedroom/capassignments/newtrajectory/wordscan/search/archive/worker. OutsideC table not covered.'}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: original L701/E34/N7/R3 TWO inward descriptions fit whole nine envelope with fullD. Parent transfer; newnine still pending independent review.')
