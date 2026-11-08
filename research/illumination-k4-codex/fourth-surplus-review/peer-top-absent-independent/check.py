"""Fixed local proof checks only; no completed rooms or discovery.
Angles are independently computed by occupied angular wedges at each vertex.
"""
from pathlib import Path
import json, hashlib
P=Path(__file__).resolve().parent
ROOT=P.parent.parent
PEER=ROOT/'surplus-four-local/e2-e1-b1'
reads=[]
def load(p):
 reads.append(p)
 return json.loads(p.read_text())
def cross(a,b): return a[0]*b[1]-a[1]*b[0]
def sub(a,b): return (a[0]-b[0],a[1]-b[1])
rays=((1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1))
probes=((2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1))
C={'L':(-2,0),'B':(0,-2),'D':(2,-2),'R':(4,0),'E':(4,2),'Tc':(2,4),'N':(0,2)}
def fan(site,sectors):
 a=C.get(site,site) if isinstance(site,str) else site
 return {tuple(sorted((a,tuple(a[j]+rays[i][j] for j in (0,1)),tuple(a[j]+rays[(i+1)%8][j] for j in (0,1))))) for i in sectors}
def full(site): return fan(site,range(8))
H=set().union(*(full(a) for a in ((0,0),(2,0),(2,2))))
def wedges(t,p):
 if p not in t:return 0
 q,r=[sub(v,p) for v in t if v!=p]
 if cross(q,r)<0:q,r=r,q
 return sum(1<<i for i,d in enumerate(probes) if cross(q,d)>0 and cross(d,r)>0)
def angle(ts,p):
 mask=0
 for t in ts:
  w=wedges(t,p)
  assert not mask&w,('overlapping angular interiors',p)
  mask|=w
 return mask.bit_count()*45
partners={'LC':('L',(7,0),1),'EC':('E',(3,4),1),'EO':('E',(4,5),0),'D01':('D',(0,1),0),'D12':('D',(1,2),1),'R23':('R',(2,3),0),'R34':('R',(3,4),1),'R45':('R',(4,5),0),'N70':('N',(7,0),1)}
peer=load(PEER/'joined-top-absent-check.json')
old=load(ROOT/'fourth-surplus-review/peer-critical-B-b1-independent/check.json')
for receipt in (peer,old):
 for rel,digest in receipt['source_sha256'].items():
  path=ROOT/rel;reads.append(path)
  assert hashlib.sha256(path.read_bytes()).hexdigest()==digest,rel
clauses={c['name']:c for c in old['whole_envelopes']}
def triangles(values):return {tuple(tuple(p) for p in t) for t in values}
def inherit(name,minimum,maximum):
 c=clauses[name]
 # previously accepted whole-envelope implication contains this subfamily
 assert triangles(c['minimum'])<=minimum,name
 assert maximum<=triangles(c['maximum']),name
local={};budgets=[];guards=[]
for root,ss in [('O3',(7,0,1)),('O4',(6,7,0,1))]:
 b=fan('B',ss)
 for label,(site,sectors,centered) in partners.items():
  fixed=H|b|fan(site,sectors)
  refs={k:s for k,s in [('L',0),('E',4)] if k!=site}
  if label=='EC':refs['N']=0
  if label in ('D01','D12','R23','R34','R45'):refs['N']=7
  fixed|=set().union(*(fan(k,(s,)) for k,s in refs.items()))
  slots={k:[set()]+[fan(k,(s,)) for s in opts] for k,opts in {'Tc':(6,),'D':(1,2),'R':(3,4),'N':(0,5,6,7)}.items() if k!=site and k not in refs}
  points={p for t in fixed for p in t}|{p for opts in slots.values() for ts in opts for t in ts for p in t}
  counts={};fullpoints=[]
  for p in points:
   if all(v%2==0 for v in p):continue
   base=angle(fixed,p)
   terms={k:sorted({angle(ts,p) for ts in opts}) for k,opts in slots.items()}
   upper=base+sum(max(v) for v in terms.values())
   if base==360:assert upper==360;fullpoints.append(p)
   else:assert upper<360,(root,label,p,base,terms)
   counts[str(p)]={'fixed':base,'terms':terms,'upper':upper}
  J=2+centered;n=J+1
  assert len(fullpoints)==J
  assert angle(fixed,(1,-2))==180
  assert all(angle(ts,(1,-2))==0 for opts in slots.values() for ts in opts)
  def at(p,extra=()):return angle(fixed|set().union(*(fan(k,(s,)) for k,s in extra)),p)
  if label in ('LC','EO'):assert at((-1,1))==135 and at((-1,1),(('N',5),))==180
  if label in ('LC','EC','EO','N70'):
   assert at((3,-1))==90 and at((3,-1),(('D',1),('R',4)))==180
  if label=='EC':assert at((3,3),(('Tc',6),))==180
  if label in ('D01','R45'):
   k,heal,other=('R',4,3) if label=='D01' else ('D',1,2)
   assert at((3,-1))==180 and at((3,-1),((k,other),))==180 and at((3,-1),((k,heal),))==225
   assert all(angle(ts,(3,-1))==0 for name,opts in slots.items() if name!=k for ts in opts)
  if label in ('D12','R34'):
   k,bad=('R',4) if label=='D12' else ('D',1)
   assert at((3,-1))==135 and at((3,-1),((k,bad),))==180
  # Independently reconstruct optical conditions for the empty-top N restrictions.
  if label in ('LC','EO'):
   key='LC' if label=='LC' else 'EO'
   ma=fixed|full('D')|full('R')|fan('N',(5,6))
   inherit(root+('_701' if root=='O3' else '_6701')+'_'+key+'_T6N0N7abs',fixed,ma)
   guards.append(root+'_'+label+'_emptyTc_needsN0or7')
  if label=='EC':
   mi=H|b|fan('L',(0,))|fan('E',(3,4))
   ma=mi|full('D')|full('R')|full('Tc')|fan('N',(1,2,3,4,5,6,7))
   inherit(root+('_701' if root=='O3' else '_6701')+'_EC_N0abs',mi,ma)
   guards.append(root+'_EC_needsN0')
  local[root+'_'+label]={'J':J,'n':n,'full_nonA':sorted(fullpoints),'vertices':counts}
  for top in (0,1):
   free=n-len(refs)-top
   if label=='LC': feasible=True; occupancy=free; assert free==(3 if not top else 2)
   elif label=='EC':feasible=not top;occupancy=free;assert top or free==2
   elif label=='EO':feasible=True;occupancy=free-(not top);assert occupancy==1
   elif label in ('D01','R45'):feasible=free==1;occupancy=free;assert not feasible
   elif label in ('D12','R34'):feasible=free in (0,1);occupancy=free;assert free==1-top
   elif label=='R23':feasible=free in (0,1);occupancy=free;assert free==-top
   else:feasible=free<=2;occupancy=free;assert free==2-top
   actual=next(r for r in peer['named_top_branch_budget_algebra'] if r['root']==root and r['partner']==label and r['Tc']==('6' if top else 'empty'))
   assert (actual['outcome']=='NECESSARY')==feasible
   assert actual['J']==J and actual['n']==n and actual['forced_reference_slots']==len(refs)
   budgets.append({'root':root,'partner':label,'top':top,'feasible_necessary_description':feasible,'remaining_occupancy':occupancy})
reads += [PEER/'joined-top-absent.txt',PEER/'joined-top-absent-check.py',PEER/'argument.txt',PEER/'critical-B.txt']
result={'status':'INDEPENDENT_O3_O4_TOP_ABSENT_PASS','templates':len(local),'budget_branches':len(budgets),'excluded_algebraic_branches':sum(not r['feasible_necessary_description'] for r in budgets),'local_angles':local,'budgets':budgets,'inherited_optical_conditions':guards,'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in dict.fromkeys(reads)},'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'limits':'Necessary O3/O4 table only, inherited root classification and n=J+1. Angular wedges and budget identities; no completed rooms, global cap assignments or discovery. H4 superseded, no new optical closure.'}
(P/'check.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS',result['templates'],'local templates;',len(budgets),'top-status branches;',result['excluded_algebraic_branches'],'excluded algebraic branches, not rooms.')
