"""Independent L012 guard dispatch and conditional seven-shape proof join."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
HERE=Path(__file__).resolve().parent;BASE=HERE.parent.parent
src=BASE/'surplus-four-local/R23-top6-search/verify.py'
e={'__file__':str(src.resolve())};exec(compile(src.read_text().split('\ndef path(d,nine):')[0],str(src),'exec'),e)
fan,H=e['fan'],e['H'];sources=[src]
def read(rel):
 p=BASE/rel;sources.append(p);return json.loads(p.read_text())
peer=read('fourth-surplus-review/peer-outside-two-three-independent/check.json')
assert peer['status']=='INDEPENDENT_OUTSIDE_TWO_THREE_AND_L0123_JOIN_PASS_WITH_NEW_L012_EIGHT_EXTENSION'
for rel,h in peer['source_sha256'].items():assert hashlib.sha256((BASE/rel).read_bytes()).hexdigest()==h,rel
B8=read('surplus-four-local/L670-B12-D1-search/verification.json')
B5=read('surplus-four-local/L670-BO-D2-search/verification.json')
D2=read('surplus-four-local/outside-L0123-D12-search/verification.json')
C3=read('surplus-four-local/outside-L0123-N45-search/verification.json')
B6=read('fourth-surplus-review/peer-Bunit-six-independent/check.json')
T=read('fourth-surplus-review/peer-critical-L-optical-independent/check.json')
N=read('fourth-surplus-review/peer-roof-three-independent/check.json')
fp=lambda P:[tuple(F(x) for x in p) for p in P]
P6=fp(B6['fixed_six']['path']);sigma=e['sigma']
rawpaths={'BC8':B8['path'],'BO5':B5['path'],'EC8':B8['sigma_eight']['path'],'EO5':B5['sigma_five']['path'],'T3':T['named_paths']['T3'],'N3':N['three']['path'],'N6':N['accepted_six_rechecked']['path'],'D2':D2['path'],'R2':D2['sigma_two']['path'],'C3':C3['path']}
paths={k:fp(v) for k,v in rawpaths.items()};paths['BC6']=P6;paths['EC6']=[sigma(p) for p in P6[::-1]]
# Recompute full incidence guard from each fixed accepted path. The mirror
# tangent is recovered from equal-length normalized incoming/outgoing vectors.
# Finite mirror bounds are inherited from their independent optical reviews.
def guard(P):
 walls=[]
 for a,p,b in zip(P,P[1:],P[2:]):
  v=e['sub'](p,a);w=e['sub'](b,p);nv=max(map(abs,v));nw=max(map(abs,w))
  v=tuple(x/nv for x in v);w=tuple(x/nw for x in w);t=tuple(v[k]+w[k] for k in (0,1))
  if t==(0,0):t=(-v[1],v[0])
  walls.append((tuple(p[k]-t[k] for k in (0,1)),tuple(p[k]+t[k] for k in (0,1))))
 return e['constraints'](P,walls)[:2]
guards={k:guard(P) for k,P in paths.items()}
L=fan('L',[0,1,2]);refs=fan('B',[1])|fan('E',[4])|fan('Tc',[5])|fan('N',[5]);clauses=[]
def cover(row,low,extra,path):
 u,z=guards[path];assert u<=low and not z&(low|extra),row
 clauses.append({'row':row,'path':path,'reflections':len(paths[path])-2,'minimum':sorted(low),'maximum':sorted(low|extra)})
cover('BO',H|L|fan('B',[0,1])|fan('E',[4])|fan('Tc',[5])|fan('N',[5]),set(),'BO5')
low=H|L|fan('B',[1,2])|fan('E',[4])|fan('Tc',[5])|fan('N',[5])
cover('BC D2abs',low,fan('D',[1])|fan('R',[3,4]),'BC8');cover('BC D2present',low|fan('D',[2]),set(),'BC6')
low=H|L|fan('E',[4,5])|fan('B',[1])|fan('Tc',[5])|fan('N',[5]);cover('EO',low,set(),'EO5')
low=H|L|fan('E',[3,4])|fan('B',[1])|fan('Tc',[5])|fan('N',[5])
cover('EC R3abs',low,fan('D',[1,2])|fan('R',[4]),'EC8');cover('EC R3present',low|fan('R',[3]),set(),'EC6')
other=fan('D',[1,2])|fan('R',[3,4])
cover('Tc56',H|L|fan('Tc',[5,6])|fan('B',[1])|fan('E',[4])|fan('N',[5]),other,'T3')
cover('D12',H|L|refs|fan('D',[1,2]),set(),'D2');cover('R34',H|L|refs|fan('R',[3,4]),set(),'R2')
low=H|L|fan('N',[5,6])|fan('B',[1])|fan('E',[4])|fan('Tc',[5])
cover('N56 D2abs',low,fan('D',[1])|fan('R',[3,4]),'N3');cover('N56 D2present',low|fan('D',[2]),set(),'N6')
cover('N45',H|L|fan('N',[4,5])|fan('B',[1])|fan('E',[4])|fan('Tc',[5]),set(),'C3')
assert len(clauses)==12 and max(c['reflections'] for c in clauses)==8
four=read('surplus-four-local/L7012-D23-search/verification.json')
assert four['status']=='PARENT_L7012_FOUR_AND_WHOLE_EIGHT_REMAINING_DESCRIPTIONS_PASS'
# The seven windows are explicitly the accepted classification, not inferred
# from optical success. Earlier inward bounds remain 14 rather than 9.
bounds={'670':14,'701':14,'012':8,'5670':6,'6701':14,'7012':4,'0123':8}
assert max(bounds.values())==14
sources += [BASE/'fourth-surplus-review/peer-outside-two-three-independent/review.txt',BASE/'fourth-surplus-review/peer-outside-two-three-independent/coverage.txt',BASE/'fourth-surplus-review/peer-critical-L-classification-independent/review.txt',BASE/'fourth-surplus-review/peer-critical-L-optical-independent/review.txt',BASE/'fourth-surplus-review/peer-BO-five-independent/review.txt',BASE/'surplus-four-local/e2-e1-b1/critical-L.txt']
out={'status':'INDEPENDENT_L012_EIGHT_ACCEPT_AND_PARENT_CRITICAL_L_T_FOURTEEN_JOIN','L012_independent_verdict':'ACCEPT SAME9ROWS/12CLAUSES bound8; inherited accepted opticalfinitebounds','L012_clauses':clauses,'seven_shapes_conditional_bounds':bounds,'parent_critical_L_T_bound':14,'independent_status':'Earlieroutside2/3+L0123<=8 acceptance fullyincorporated. NewL012<=8 independentlyacceptedhere. L7012four/final7shapejoin pendingpeerchallenge.','peer_pinned_hashes_current':len(peer['source_sha256']),'source_sha256':{str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in dict.fromkeys(sources)},'limits':'Staticfixedacceptedpathguards/conditionaljoin only, no room/search/worker. Entireupstreamrootleaf/forcing/bridge prerequisites retained; fullDelta4notproved.'}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
print('ACCEPT L012<=8, all9rows/12clauses; parentcompletecriticalL/T<=14 pendingL7012four/finaljoinreview;',len(peer['source_sha256']),'peerhashes current.')
