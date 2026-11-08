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
checks={}
LC=fan('L',[7,0]);L0=fan('L',[0]);E4=fan('E',[4]);EC=fan('E',[3,4]);N0=fan('N',[0])
west=H|fan('B',[1,2,3,4])|LC|E4
ordinary={'Tc':options('Tc',[5,6]),'D':options('D',[1,2]),'R':options('R',[3,4]),'N':options('N',[0,5,6,7])}
checks['West1234_LC']=audit('West1234_LC',west,ordinary,4)
# Budget equation from accepted two-root class: n=J+1. E fixed ordinary,
# four remaining ordinary slots. J4 forces n5, hence all four nonempty.
assert checks['West1234_LC']['J']+1==1+len(ordinary)==5
assert angle(H|fan('B',[1,2,3,4])|L0,(-1,-1))==180
assert angle(west,(-1,-1))==225
assert angle(west,(-1,-2))==180
assert not any((-1,-2) in t for k in A if k!='B' for t in fan(k,range(8)))
# Only L7 among other K sites can heal (-1,-1); forced L0 restricts
# an e1 L root containing7 to70. This is a local support assertion.
healers={k:[i for i in range(8) if (-1,-1) in next(iter(fan(k,[i])))] for k in A if k!='B'}
assert healers['L']==[6,7]
assert all(not v for k,v in healers.items() if k!='L')
assert [i for i in [6,7] if i in [7,0]]==[7]
# Joined EC+N0: either Tc cap creates a second forbidden smooth point.
for label,ss,h in [('O3',[7,0,1],0),('O4',[6,7,0,1],0),('H4',[7,0,1,2],1)]:
 fixed=H|fan('B',ss)|L0|EC|N0
 assert angle(fixed,(1,-2))==180
 assert angle(fixed|fan('Tc',[5]),(1,3))==180
 assert angle(fixed|fan('Tc',[6]),(3,3))==180
 slots={'D':options('D',[1,2]),'R':options('R',[3,4])}
 j=3+h;checks[label+'_EC_N0_Tcempty']=audit(label+'_EC_N0',fixed,slots,j)
 need=j+1;capacity=2+len(slots)
 if h:assert need>capacity
 else:assert need==capacity
 checks[label+'_EC_N0_Tcempty']['ordinary_budget']={'required':need,'fixed_L_N':2,'maximum_with_empty_Tc':capacity,'outcome':'IMPOSSIBLE' if h else 'BOTH_D_R_FORCED'}
# D23 heals the east C and adds one interior B. No extra full vertex
# appears from any permitted ordinary-slot contribution.
for label,ss,h in [('O3',[7,0,1],0),('O4',[6,7,0,1],0),('H4',[7,0,1,2],1)]:
 fixed=H|fan('B',ss)|fan('D',[2,3])|L0|E4
 assert angle(fixed,(1,-2))==270 and angle(fixed,(1,-1))==360
 slots={'Tc':options('Tc',[5,6]),'R':options('R',[3,4]),'N':options('N',[0,5,6,7])}
 checks[label+'_D23']=audit(label+'_D23',fixed,slots,3+h)
source=HERE/'critical-B.txt';checker=HERE/'critical-B-check.py';receipt=HERE/'critical-B-check.json'
result={'status':'PASS','method':'At each non-A vertex sum fixed angle plus each slot maximum; no joint slot assignments, no new room, no optical search.','checks':checks,'limits':'Parent self-audit only; inherits two-root n=J+1 and b/M interpretation. Does not substitute for peer independent review.','source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [source,checker,receipt]},'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(HERE/'critical-B-budget-check.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS: seven named local J bounds; West1234 forces five ordinary slots, EC/N0 forces emptyTc and excludes H4, D23 adds exactly one J. No cap-assignment census.')
