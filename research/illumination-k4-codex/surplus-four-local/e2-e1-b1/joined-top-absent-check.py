"""Independent local angle bounds, no room or cap-assignment enumeration.
At each vertex, maximize each ordinary slot separately. This may overbound
an unrealizable combination; a strict upper bound still proves no hidden J.
"""
from pathlib import Path
from collections import defaultdict
import json,hashlib
HERE=Path(__file__).resolve().parent
R=((1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1))
A={'L':(-2,0),'B':(0,-2),'D':(2,-2),'R':(4,0),'E':(4,2),'Tc':(2,4),'N':(0,2)}
def fan(site,ss):
 a=A[site] if isinstance(site,str) else site
 return {tuple(sorted((a,(a[0]+R[i][0],a[1]+R[i][1]),(a[0]+R[(i+1)%8][0],a[1]+R[(i+1)%8][1])))) for i in ss}
H=set().union(*(fan(a,range(8)) for a in [(0,0),(2,0),(2,2)]))
def angle(ts,p):
 n=0
 for t in ts:
  if p in t:
   a,b=[(v[0]-p[0],v[1]-p[1]) for v in t if v!=p]
   n+=90 if a[0]*b[0]+a[1]*b[1]==0 else 45
 return n
# Slot options remain local alternatives, never a Cartesian product.
def options(site,sectors):return [set()]+[fan(site,[i]) for i in sectors]
def audit(name,fixed,slots,J):
 vertices={p for t in fixed for p in t}
 for opts in slots.values():
  vertices.update(p for ts in opts for t in ts for p in t)
 rows={};full=[]
 for p in sorted(vertices):
  if p[0]%2==p[1]%2==0:continue
  base=angle(fixed,p);terms={k:sorted({angle(ts,p) for ts in opts}) for k,opts in slots.items()}
  high=base+sum(max(v) for v in terms.values())
  assert high<=360,(name,p,base,terms)
  if base==360:
   assert high==360;full.append(p)
  else:assert high<360,(name,'possible hidden interior non-A',p,base,terms)
  rows[str(p)]={'fixed_degrees':base,'local_slot_options':terms,'upper_bound':high}
 assert len(full)==J,(name,full,J)
 return {'J':J,'fixed_interior_nonA':full,'per_vertex':rows}
# The THREE previously accepted root windows and NINE named remaining
# unit partners. Each template has symbolic ordinary slots, never joint
# completed cap assignments. No optical path search or room construction.
BASE=HERE.parent.parent
roots={'O3':([7,0,1],0),'O4':([6,7,0,1],0),'H4':([7,0,1,2],1)}
partners={
 'LC':('L',[7,0],1),'EC':('E',[3,4],1),'EO':('E',[4,5],0),
 'D01':('D',[0,1],0),'D12':('D',[1,2],1),
 'R23':('R',[2,3],0),'R34':('R',[3,4],1),'R45':('R',[4,5],0),
 'N70':('N',[7,0],1)}
L0=fan('L',[0]);E4=fan('E',[4]);N7=fan('N',[7]);N0=fan('N',[0]);T6=fan('Tc',[6])
records={};budgets=[];angles={}
for root,(ss,h) in roots.items():
 for label,(site,sectors,c) in partners.items():
  fixed=H|fan('B',ss)|fan(site,sectors)
  refs={}
  if site!='L':refs['L']=L0
  if site!='E':refs['E']=E4
  if label=='EC':refs['N']=N0
  if label in ['D01','D12','R23','R34','R45']:refs['N']=N7
  fixed|=set().union(*refs.values())
  slots={k:options(k,sectors) for k,sectors in {'Tc':[6],'D':[1,2],'R':[3,4],'N':[0,5,6,7]}.items() if k!=site and k not in refs}
  name=root+'_'+label;J=2+h+c;n=J+1
  records[name]=audit(name,fixed,slots,J)
  assert angle(fixed,(1,-2))==180
  Bpoints={p for t in fixed|set().union(*(ts for opts in slots.values() for ts in opts)) for p in t if p[0]%2==p[1]%2==1}
  coeff={str(p):{'fixed':angle(fixed,p),'per_slot_options':{k:sorted({angle(ts,p) for ts in opts}) for k,opts in slots.items()}} for p in sorted(Bpoints)}
  angles[name]=coeff
  # Exhaustive dangerous B points are identified by angle bounds. A whole
  # slot maximum at each point is an upper bound, not an assignment scan.
  exceptional={'LC':{(-1,-1),(-1,1),(3,-1)},'EC':{(3,3),(3,-1)},'EO':{(-1,1),(3,-1)},'D01':{(3,-1)},'D12':{(3,-1)},'R23':set(),'R34':{(3,-1)},'R45':{(3,-1)},'N70':{(3,-1)}}[label]
  for p in Bpoints-exceptional:
   v=coeff[str(p)];upper=v['fixed']+sum(max(x) for x in v['per_slot_options'].values())
   assert v['fixed']>180 or upper<180,(name,p,v)
  if label in ['LC','EO']:
   assert angle(fixed,(-1,1))==135 and angle(fixed|fan('N',[5]),(-1,1))==180
  if label in ['LC','EC','EO','N70']:
   assert angle(fixed,(3,-1))==90
   assert angle(fixed|fan('D',[1])|fan('R',[4]),(3,-1))==180
  if label=='LC' and h:
   assert angle(fixed,(-1,-1))==180
   assert all(not any((-1,-1) in t for t in ts) for opts in slots.values() for ts in opts)
  if label=='EC':assert angle(fixed|T6,(3,3))==180
  if label=='D01':
   assert angle(fixed,(3,-1))==180
   assert angle(fixed|fan('R',[3]),(3,-1))==180
   assert angle(fixed|fan('R',[4]),(3,-1))==225
  if label=='D12':
   assert angle(fixed,(3,-1))==135
   assert angle(fixed|fan('R',[4]),(3,-1))==180
  if label=='R34':
   assert angle(fixed,(3,-1))==135
   assert angle(fixed|fan('D',[1]),(3,-1))==180
  if label=='R45':
   assert angle(fixed,(3,-1))==180
   assert angle(fixed|fan('D',[2]),(3,-1))==180
   assert angle(fixed|fan('D',[1]),(3,-1))==225
  # Only integer slot-capacity algebra for two named top branches.
  # No choice of ordinary directions, full support or room is generated.
  for top in [0,1]:
   row={'root':root,'partner':label,'Tc':'6' if top else 'empty','J':J,'n':n,'forced_reference_slots':len(refs)}
   if label=='LC':
    if h:row.update(outcome='IMPOSSIBLE',reason='second smooth lower B')
    elif not top:
     assert n-len(refs)==3
     row.update(outcome='NECESSARY',restriction='D,R,N all occupied; N0 or N7 after L12; forbidD1/R4')
    else:
     assert n-len(refs)-top==2
     row.update(outcome='NECESSARY',restriction='exactly TWO D/R/N occupied; N if present0/6/7; forbidD1/R4')
   elif label=='EC':
    if top:row.update(outcome='IMPOSSIBLE',reason='second smooth B(3,3)')
    elif n-len(refs)>2:row.update(outcome='IMPOSSIBLE',reason='emptyTc cap capacity')
    else:
     assert n-len(refs)==2
     row.update(outcome='NECESSARY',restriction='N0 fixed; D and R occupied; forbidD1/R4')
   elif label=='EO':
    if not top:
     assert n-len(refs)-1==1+h
     row.update(outcome='NECESSARY',restriction='N0 or N7 occupied after E11; exactly '+str(1+h)+' D/R occupied; forbidD1/R4')
    else:
     assert n-len(refs)-top==1+h
     row.update(outcome='NECESSARY',restriction='exactly '+str(1+h)+' D/R/N occupied; N if present0/6/7; forbidD1/R4')
   elif label in ['D01','R45']:
    available=n-len(refs)-top
    if available!=1:row.update(outcome='IMPOSSIBLE',reason='mandatory healing cap exceeds cap budget')
    else:
     assert h==1 and top==0
     row.update(outcome='NECESSARY',restriction='R4 compulsory' if label=='D01' else 'D1 compulsory')
   elif label in ['D12','R34']:
    required=n-len(refs)-top
    if required not in [0,1]:row.update(outcome='IMPOSSIBLE',reason='opposite slot capacity')
    else:row.update(outcome='NECESSARY',restriction=('R3' if label=='D12' else 'D2')+' occupied' if required else ('R empty' if label=='D12' else 'D empty'))
   elif label=='R23':
    required=n-len(refs)-top
    if required not in [0,1]:row.update(outcome='IMPOSSIBLE',reason='opposite slot capacity')
    else:row.update(outcome='NECESSARY',restriction='D1 or D2 occupied' if required else 'D empty')
   else:
    assert label=='N70'
    required=n-len(refs)-top
    if required>2:row.update(outcome='IMPOSSIBLE',reason='D/R slot capacity')
    else:
     assert required in [1,2]
     row.update(outcome='NECESSARY',restriction='exactly '+str(required)+' D/R occupied; forbidD1/R4')
   budgets.append(row)
assert len(records)==27 and len(budgets)==54
# These are algebraic named top-branches, NOT room counts.
excluded=sum(r['outcome']=='IMPOSSIBLE' for r in budgets)
expected_exclusions={'LC':2,'EC':4,'EO':0,'D01':5,'D12':1,'R23':2,'R34':1,'R45':5,'N70':1}
actual={k:sum(r['outcome']=='IMPOSSIBLE' and r['partner']==k for r in budgets) for k in partners}
assert actual==expected_exclusions,(actual,expected_exclusions)
assert excluded==sum(expected_exclusions.values())==21
# Verify the inherited optical clauses defining N0/N7 residuals are current.
consolidation=json.loads((HERE/'critical-B-check.json').read_text())
assert consolidation['status']=='PARENT_CRITICAL_B_CONSOLIDATION_PASS'
for n,h in consolidation['source_sha256'].items():assert hashlib.sha256((BASE/n).read_bytes()).hexdigest()==h,n
peer=BASE/'fourth-surplus-review/peer-critical-B-b1-independent/check.json'
review=json.loads(peer.read_text());assert review['status']=='INDEPENDENT_CRITICAL_B_B1_CONSOLIDATION_CHECK_PASS'
for n,h in review['source_sha256'].items():assert hashlib.sha256((BASE/n).read_bytes()).hexdigest()==h,n
sources=[HERE/'critical-B.txt',HERE/'critical-B-check.py',HERE/'critical-B-check.json',peer,BASE/'surplus-four-local/joined-six-review/review.txt',BASE/'surplus-four-local/joined-square-review/review.txt']
receipt={'status':'PARENT_JOINED_TC5_ABSENT_REDUCTION_PASS','local_J_bounds':records,'B_angle_coefficients':angles,'named_top_branch_budget_algebra':budgets,'excluded_named_branches':excluded,'branch_count_scope':'54 prescribed local template/top-status algebra branches; 21 capacity/angle exclusions. NOT completed rooms/cap-direction assignments or a validity census.','source_sha256':{str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'limits':'Necessary reductions within inherited two-root/M/n=J+1 class, accepted optical preclusions. Does not prove remaining descriptions valid or dark; no new optical witness or complete branch closure.'}
(HERE/'joined-top-absent-check.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('PASS:',len(records),'named symbolic J/angle templates;',len(budgets),'top-status budget identities;',excluded,'excluded algebraic branches (NOT rooms).')
