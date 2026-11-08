"""Independent static count-to-cap and whole-support review; no discovery."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
HERE=Path(__file__).resolve().parent;BASE=HERE.parent.parent
src=BASE/'surplus-four-local/R23-top6-search/verify.py'
e={'__file__':str(src.resolve())};exec(compile(src.read_text().split('\ndef path(d,nine):')[0],str(src),'exec'),e)
fan,H=e['fan'],e['H']
peer=BASE/'fourth-surplus-review/mixed-Eouter-four-transfer'
j=json.loads((peer/'check.json').read_text())
assert j['status']=='MIXED_EOUTER_O3_O4_CLOSED_PARENT_AND_H4_D3_REDUCED'
for rel,h in j['source_sha256'].items():assert hashlib.sha256((BASE/rel).read_bytes()).hexdigest()==h,rel
root=BASE/'fourth-surplus-review/mixed-e2-e1/root-leaf-check.json'
r=json.loads(root.read_text());decode=lambda ts:{tuple(sorted(map(tuple,t))) for t in ts}
# The two named established optical implications are read, never re-executed.
missing=r['named_implications']['outer_E_missing_L'];five=r['named_implications']['outer_E_Nrminus_absent']
allK=H|set().union(*(fan(k,range(8)) for k in ['L','B','D','R','E','Tc','N']))
for rec in [missing,five]:
 assert decode(rec['required'])<=decode(rec['fixed']) and not decode(rec['forbidden'])&decode(rec['possible'])
# Four independently accepted in our prior review. Its complete support is pinned.
fpath=BASE/'surplus-four-local/source-suffix-four-review/check.json';four=json.loads(fpath.read_text())
assert four['status']=='INDEPENDENT_SOURCE_SUFFIX_FOUR_AND_O3_BOUND_NINE_ACCEPT'
u,z=decode(four['required']),decode(four['forbidden']);ma=decode(four['maximum'])
assert z==fan('R',[3])|fan('N',[0,6])
# Exact symbolic local angles and ledger, not room assignments.
def angle(ts,p):
 n=0
 for t in ts:
  if p in t:
   a,b=[e['sub'](x,p) for x in t if x!=p];n+=90 if e['dot'](a,b)==0 else 45
 return n
assert decode(missing['fixed'])<=H|fan('E',[4,5])
assert H|fan('E',[4,5])|fan('L',[1,2,3,4,5,6,7])|set().union(*(fan(k,range(8)) for k in ['B','D','R','Tc','N']))<=decode(missing['possible'])
assert decode(five['fixed'])<=H|fan('L',[0])|fan('E',[4,5])
assert H|fan('E',[4,5])|fan('L',[0])|fan('N',[0,1,2,3,4,5,6])|set().union(*(fan(k,range(8)) for k in ['B','D','R','Tc']))<=decode(five['possible'])
assert angle(H|fan('B',[7,0,1]),(0,-1))==270
assert angle(H|fan('B',[7,0,1,2]),(0,-1))==360
assert angle(H|fan('E',[4,5]),(3,2))<360
assert angle(H|fan('L',[0]),(-1,1))==135
assert angle(H|fan('L',[0])|fan('N',[5]),(-1,1))==180
applications=[]
for name,ss,h in [('O3',[7,0,1],0),('O4',[6,7,0,1],0),('H4',[7,0,1,2],1)]:
 J=2+h;ordinary_n=J
 assert 6-ordinary_n+J==6 # Delta4 implies sN=6-n; k6 implies n=J.
 for leaf in [3,4]:
  local=H|fan('B',ss)|fan('D',[leaf])
  assert angle(local,(1,-2))==270 and angle(local,(1,-1))<=315
 low=H|fan('B',ss)|fan('E',[4,5])|fan('L',[0])|fan('N',[7])
 if h==0:
  assert ordinary_n-2==0
  upper=low|fan('D',[3,4])
  assert u<=low<=upper<=ma
  applications.append({'B':name,'residual_cap_budget':0,'bound':5,'meaning':'missingL2, absentN7five, otherwisefour; both leaves'})
 else:
  assert ordinary_n-2==1
  upper=low|fan('D',[3])|fan('Tc',[5,6])|fan('R',[4])
  assert u<=low<=upper<=ma and z&fan('R',[3])
  applications.append({'B':name,'leaf':3,'residual_cap_budget':1,'remaining':'R3 only; Tc5/Tc6/R4 fit four'})
sources=[src,root,fpath,peer/'argument.txt',peer/'check.py',peer/'check.json',peer/'coverage.txt',BASE/'fourth-surplus-review/mixed-e2-e1/argument.txt']
out={'status':'INDEPENDENT_MIXED_EOUTER_O3_O4_DISPATCH_AND_H4_REDUCTION_ACCEPT','applications':applications,'peer_hashes_current':len(j['source_sha256']),'source_sha256':{str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},'limits':'Independent count/whole-support review; accepted opticallemmas inherited. Entireupstreamrootleafclassification/H4D4notre-audited. No peer execution/newroom/discovery/worker.'}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
print('ACCEPT O3/O4 Eouter<=5, bothDleaves; H4D3 onlyR3 remains;',len(j['source_sha256']),'peerhashes current.')
