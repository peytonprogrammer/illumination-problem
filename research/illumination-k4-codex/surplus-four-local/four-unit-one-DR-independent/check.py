"""Review exactly-one D/R erasure from accepted stored guard clauses.
No new rooms, paths, cap products, or peer checker execution.
"""
from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent;BASE=HERE.parent.parent
src=BASE/'surplus-four-local/R23-top6-search/verify.py'
e={'__file__':str(src)}
exec(compile(src.read_text().split('\ndef path(d,nine):')[0],str(src),'exec'),e)
fan,H=e['fan'],e['H'];reads=[src,Path(__file__)]
def read(rel):
 p=BASE/rel;reads.append(p);return json.loads(p.read_text())
def decode(ts):return {tuple(sorted(map(tuple,t))) for t in ts}
def angle(ts,p):
 return sum(90 if e['dot'](*[e['sub'](v,p) for v in t if v!=p])==0 else 45 for t in ts if p in t)
def pins(receipt):
 for rel,h in receipt['source_sha256'].items():
  p=BASE/rel;reads.append(p);assert hashlib.sha256(p.read_bytes()).hexdigest()==h,rel
both=read('surplus-four-local/four-unit-DR-independent/check.json')
assert both['status']=='INDEPENDENT_BOTH_DR_FOUR_UNIT_ERASURE_ACCEPT';pins(both)
old=read('fourth-surplus-review/three-unit-b1-independent/check.json');pins(old)
assert old['bound']==13 and len(old['named_guards'])==148
D=fan('D',range(8));R=fan('R',range(8));sensitive=[]
for name,g in old['named_guards'].items():
 u,z=decode(g['required']),decode(g['forbidden'])
 lo,hi=decode(g['minimum']),decode(g['maximum'])
 assert u<=lo and not z&hi
 assert not u&(D|R),name
 hit=z&(D|R)
 if hit:
  sensitive.append({'name':name,'D_R_forbidden':sorted(hit)})
  if name=='three_CL_CE_BO_1':
   assert hit==fan('D',[3]) and fan('B',[0,1])<=lo
  elif name=='three_sigma_CL_CE_BO_1':
   assert hit==fan('R',[2]) and fan('E',[4,5])<=lo
  else:raise AssertionError(name)
assert len(sensitive)==2
# Test every restored unit's possible effect on each fixed accepted guard.
# These are clause/local-fan intersections, not assembled cap assignments.
conditional=[]
for site,windows in [('D',[(0,1),(1,2),(2,3)]),('R',[(2,3),(3,4),(4,5)])]:
 for ss in windows:
  added=fan(site,ss)
  for name,g in old['named_guards'].items():
   if not decode(g['forbidden'])&added:continue
   lo=decode(g['minimum'])
   if site=='D':
    assert ss==(2,3) and name=='three_CL_CE_BO_1'
    partner='B';mate=(0,1);p=(1,-2)
   else:
    assert ss==(2,3) and name=='three_sigma_CL_CE_BO_1'
    partner='E';mate=(4,5);p=(4,1)
   assert fan(partner,mate)<=lo
   assert angle(added,p)==angle(fan(partner,mate),p)==90
   others=H|set().union(*(fan(k,range(8)) for k in e['C'] if k not in (site,partner)))
   assert angle(others,p)==0
   conditional.append({'unit':site,'sectors':ss,'clause':name,'unhealed_C':p,'angle':180,'excluded_by_original_b0':True})
assert len(conditional)==2
# Single-site coefficients for all non-A vertices deletion can expose.
changed=set()
for ss in [(0,1),(1,2),(2,3)]:
 changed.update(p for t in fan('D',ss) for p in t if any(x%2 for x in p))
assert changed=={(1,-1),(1,-2),(2,-1),(3,-1),(3,-2)}
Bchoices=[(),(1,),(2,),(0,1),(1,2),(2,3)]
Rchoices=[(),(3,),(4,)]
rows=[]
for p in sorted(changed):
 bvals=sorted({angle(fan('B',ss),p) for ss in Bchoices})
 rvals=sorted({angle(fan('R',ss),p) for ss in Rchoices})
 for k in ('L','E','Tc','N'):assert angle(fan(k,range(8)),p)==0
 base=angle(H,p)
 if p==(1,-1):assert base==180 and bvals==[0,45,90] and rvals==[0]
 elif p==(3,-1):assert base==90 and bvals==[0] and rvals==[0,45]
 elif p==(1,-2):assert base==0 and bvals==[0,90] and rvals==[0]
 elif p==(3,-2):assert base==0 and bvals==rvals==[0]
 else:assert p==(2,-1) and base==180 and bvals==rvals==[0]
 rows.append({'p':p,'H':base,'B':bvals,'ordinary_R':rvals,'baseline_M':p==(2,-1),'only_possible_new_extra_smooth':p==(1,-1)})
# Cnorth was not smooth for ANY positive Dunit: it was270 or360.
# Deletion exposes one uncovered H midpoint: sN+1 and M+1 cancel in b.
assert [angle(H|fan('D',ss),(2,-1)) for ss in [(0,1),(1,2),(2,3)]]==[270,360,270]
parent=read('fourth-surplus-review/four-unit-one-DR-erasure/check.json');pins(parent)
for rel in ['fourth-surplus-review/four-unit-one-DR-erasure/argument.txt','fourth-surplus-review/four-unit-one-DR-erasure/check.py','fourth-surplus-review/three-unit-b1-independent/review.txt','surplus-four-local/three-unit-b1/argument.txt','surplus-four-local/four-unit-DR-independent/review.txt']:
 reads.append(BASE/rel)
out={'status':'INDEPENDENT_AT_LEAST_ONE_DR_FOUR_UNIT_ERASURE_ACCEPT','guard_count':148,'D_R_independent_guards':146,'sensitive_guards':sensitive,'all_possible_reinsertion_obstructions':conditional,'changed_vertex_coefficients':rows,'auxiliary_b_at_most':1,'reflections_at_most':13,'limits':'Topology inherited from separate own BOTH-DR review. Accepted THREE-root proof sections3-5 independently read for b<=1 use; stored full guards reused with current provenance, no fresh148-path optical replay. Underlying THREE-unit proof authored by this reviewer, a declared independence limitation. No full four-unit/Delta4/universal result.','source_sha256':{str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in dict.fromkeys(reads)}}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'],'148 guards,146 unconditional,2 conditional obstructions excluded by original b0; auxiliary b<=1')
