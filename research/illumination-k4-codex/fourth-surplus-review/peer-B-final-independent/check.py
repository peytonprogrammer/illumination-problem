"""Independent fixed eights, one supplied polygon, whole-support transfers.
No peer execution/import, new room, direction/word discovery or archive scan.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
import json,hashlib,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
sys.path.insert(0,str(ROOT/'triangle-composition/inputs'))
from guard_checker import path_requirements,incident
from boundary_replay import replay,on,sub,cross,dot
import illumination_geometry as geo
reads=[]
def read(p):reads.append(p);return json.loads(p.read_text())
def decode(ts):return {tuple(sorted(map(tuple,t))) for t in ts}
R=((1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1))
C={'L':(-2,0),'B':(0,-2),'D':(2,-2),'R':(4,0),'E':(4,2),'Tc':(2,4),'N':(0,2)}
def fan(k,ss):
 a=C[k] if isinstance(k,str) else k
 return {tuple(sorted((a,tuple(a[j]+R[i%8][j] for j in (0,1)),tuple(a[j]+R[(i+1)%8][j] for j in (0,1))))) for i in ss}
def full(k):return fan(k,range(8))
H=set().union(*(full(p) for p in ((0,0),(2,0),(2,2))))
allK=H|set().union(*(full(k) for k in C))
sigma=lambda p:(2-p[1],2-p[0])
tr=lambda ts:{tuple(sorted(sigma(v) for v in t)) for t in ts}
def fp(xs):return [tuple(F(x) for x in p) for p in xs]
def angle(ts,p):
 n=0
 for t in ts:
  if p in t:
   a,b=[sub(v,p) for v in t if v!=p];n+=90 if dot(a,b)==0 else 45
 return n
def provenance(receipt,path):
 for rel,digest in receipt['source_sha256'].items():
  p=ROOT/rel;reads.append(p);assert hashlib.sha256(p.read_bytes()).hexdigest()==digest,rel
 p=path.parent/'verify.py';reads.append(p)
 assert hashlib.sha256(p.read_bytes()).hexdigest()==receipt['checker_sha256']
records={}
def optical(name,P,walls,mi,ma,image,parent):
 u,z=path_requirements(P)
 assert u<=mi and not z&ma,(name,u-mi,z&ma)
 assert P[0]==(0,0) and P[-1]==(2,2)
 assert all(not on((2,2),a,b) for a,b in zip(P[:-2],P[1:-1]))
 for a,p,b,(c,e) in zip(P,P[1:],P[2:],walls):
  assert on(p,c,e) and p not in (c,e),(name,p)
  v=sub(p,a);w=sub(e,c)
  ref=tuple(2*dot(v,w)*w[k]/dot(w,w)-v[k] for k in (0,1))
  assert cross(ref,sub(b,p))==0 and dot(ref,sub(b,p))>0
 assert len(walls)==len(P)-2
 a,b=path_requirements(P[::-1]);assert (a,b)==(u,z)
 a,b=path_requirements([sigma(p) for p in P[::-1]]);assert (a,b)==(tr(u),tr(z))
 q=P[-1]
 for a,b in walls[::-1]:
  w=sub(b,a);v=sub(q,a);q=tuple(a[k]+2*dot(v,w)*w[k]/dot(w,w)-v[k] for k in (0,1))
 assert q==image,(name,q,image)
 if parent is not None:
  assert u==decode(parent['required']) and z==decode(parent['forbidden'])
  assert mi==decode(parent['minimum']) and ma==decode(parent['maximum'])
 records[name]={'path':[[str(x) for x in p] for p in P],'reflections':len(P)-2,'U':len(u),'Z':len(z),'unfold':list(map(str,q)),'required':sorted(u),'forbidden':sorted(z),'minimum':sorted(mi),'maximum':sorted(ma)}
 return u,z
import itertools
base=read(ROOT/'surplus-four-remote2110/critical-logic/check.json');join=read(ROOT/'surplus-four-remote2110/B-frontier-join.json')
for doc in [base,join]:
 for rel,h in doc['source_sha256'].items():
  p=ROOT/rel;reads.append(p);assert hashlib.sha256(p.read_bytes()).hexdigest()==h,rel
reads += [ROOT/'surplus-four-remote2110'/f for f in ['B-frontier-join.py','B-frontier-join.txt','B-frontier-join-coverage.txt','critical-logic/argument.txt','critical-logic/check.py']]
G={}
def add(name,g):
 n=g.get('reflections',g.get('proof',g.get('audit',{})).get('reflections'));assert n is not None,name
 u,z=decode(g['required']),decode(g['forbidden']);G[name]=(u,z,n);G['sigma:'+name]=(tr(u),tr(z),n)
# Accepted prior proof dependencies. Current whole guards must match fresh
# independent receipts where newly reviewed, not merely a name/bound catalog.
for name,g in read(ROOT/'fourth-surplus-review/three-unit-b1-independent/check.json')['named_guards'].items():add('148:'+name,g)
for rel in ['surplus-four-remote2110/peer-optical-review/check.json','surplus-four-remote2110/N6-four-review/check.json','surplus-four-remote2110/B-eight-review/check.json','surplus-four-remote2110/peer-core-exchange-review/check.json']:
 for name,g in read(ROOT/rel)['paths'].items():add(name,g)
g=read(ROOT/'surplus-four-remote2110/roof-N5-search/verification.json');add('right_leaf_four',{**g,'reflections':4})
g=read(ROOT/'surplus-four-local/R23-top6-search/verification.json')['whole_support'];add('H4_smooth_three',{**g,'reflections':3})
for name,g in read(ROOT/'surplus-four-local/west-four-mixed-eleven-review/check.json')['new_path_records'].items():add('West_mixed:'+name,g)
for name,g in read(ROOT/'fourth-surplus-review/peer-Bfull-optical-independent/check.json')['fixed_paths'].items():add(name,g)
for name,g in read(ROOT/'fourth-surplus-review/peer-centered-square-independent/check.json')['fixed_paths'].items():
 rel='surplus-four-remote2110/'+name+'/'+('check.json' if name in ['R23-square-seven','N70-center-three']else'verification.json');add(rel,g)
g=read(ROOT/'surplus-four-local/mixed-O3-N70-search/verification.json')['four'];add('accepted_N70_four',{**g,'reflections':4})
# Core receipt names are peer-facing aliases. Verify all underlying new guards
# equal this agent's frozen independent paths before relying on them.
core=read(ROOT/'surplus-four-remote2110/peer-core-exchange-review/check.json')['paths']
for alias,subdir in [('L0_eight','remote2101-B-N0'),('N0_six','remote2101-D1-R3'),('Tc6_four','remote2101-D1-R3-Tc6'),('smooth_B_one','remote2101-smooth-B-one')]:
 g=next(iter(read(ROOT/'fourth-surplus-review'/subdir/'check.json')['fixed_paths'].values()))
 a=G[alias];assert a==(decode(g['required']),decode(g['forbidden']),g['reflections'])
forms={'L':[(7,0),(0,1)],'D':[(0,1),(1,2),(2,3)],'R':[(2,3),(3,4),(4,5)],'E':[(3,4),(4,5)],'Tc':[(4,5),(5,6),(6,7)],'N':[(4,5),(5,6),(7,0),(0,1)]}
assert sum(map(len,forms.values()))==17
ordinary={'L':[(),(0,),(7,)],'D':[(),(1,),(2,)],'R':[(),(3,),(4,)],'E':[(),(3,),(4,)],'Tc':[(),(5,),(6,)],'N':[(),(5,),(6,),(7,),(0,)]}
key=lambda r:(r['leaf'],r['unit'],tuple(sorted(r['unit_sectors'])))
original={key(r):r for r in base['templates']if r['parent']=='B'};joined={key(r):r for r in join['rows']}
assert len(original)==len(joined)==34
records=[];counts={0:0,7:0};oldcount=newcount=0;maxbound=0
for leaf in (0,7):
 for unit,windows in forms.items():
  for ss in windows:
   k=(leaf,unit,tuple(sorted(ss)));pr=original[k];jr=joined[k]
   assert pr['sectors']==[1,2,3,4] and pr['remote']==[-2,-2]
   fixed=H|fan('B',[1,2,3,4])|fan((-2,-2),[leaf])|fan(unit,ss)
   slots=[s for s in ordinary if s!=unit];opts={s:([cap for cap in ordinary[s]if {'L':0,'E':4}[s]in cap]if s in('L','E')else ordinary[s])for s in slots}
   assert unit not in ('L','E') or {'L':0,'E':4}[unit]in ss
   maxsupport=fixed|set().union(*(fan(s,c)for s in slots for c in opts[s]));pts={p for t in maxsupport for p in t};nonA={p for p in pts if p[0]%2 or p[1]%2}
   HC={p for p in nonA if p[0]%2!=p[1]%2 and angle(H,p)==180};baseline={p for p in HC if angle(fixed,p)==180}
   assert baseline==set(map(tuple,pr['baseline_M_vertices']))
   J=sum(angle(fixed,p)==360 for p in nonA);assert J==pr['J']==pr['ordinary_slots_required']
   for p in nonA:
    fixedangle=angle(fixed,p);upper=fixedangle+sum(max(angle(fan(s,c),p)for c in opts[s])for s in slots)
    assert fixedangle==360 or upper<360
   for term in pr['angle_terms']:
    p=tuple(term['vertex']);assert p in nonA-baseline and term['fixed_degrees']==angle(fixed,p)
    for s in slots:assert term['ordinary_coefficients'][s]=={str(c):angle(fan(s,c),p)for c in opts[s]}
   assert {tuple(t['vertex'])for t in pr['angle_terms']}==nonA-baseline
   got={}
   label=lambda caps:tuple((s,tuple(caps[s]))for s in slots if caps.get(s))
   for choices in itertools.product(*(opts[s]for s in slots)):
    if sum(bool(c)for c in choices)!=J:continue
    support=fixed|set().union(*(fan(s,c)for s,c in zip(slots,choices)))
    if any(angle(support,p)==180 for p in nonA-HC):continue
    cap=dict(zip(slots,choices));got[label(cap)]=support
   before={label(c['caps']):c for c in pr['covers']};missing={label(c)for c in pr['uncovered']}
   assert set(got)==set(before)|missing and not(set(before)&missing)and len(got)==pr['necessary_labels']
   after={label(c['caps']):c for c in jr['original_accepted_covers']+jr['new_covered']}
   assert not jr['remaining'] and set(got)==set(after)
   assert jr['original_accepted_covers']==pr['covers']
   assert {label(c['caps'])for c in jr['new_covered']}==missing
   for cap,support in got.items():
    rec=after[cap];u,z,n=G[rec['guard']];assert u<=support and not z&support and n==rec['bound']<=13
    if leaf==7:assert unit=='L'and set(ss)=={7,0}
    counts[leaf]+=1;maxbound=max(maxbound,n);oldcount+=cap in before;newcount+=cap in missing
    records.append({'leaf':leaf,'unit':unit,'unit_sectors':ss,'caps':dict(cap),'guard':rec['guard'],'bound':n})
assert counts=={0:151,7:35}and(oldcount,newcount)==(137,49)and maxbound==13
reads += [ROOT/'triangle-composition/inputs/guard_checker.py',Path(__file__)]
(HERE/'check.json').write_text(json.dumps({'status':'INDEPENDENT_COMPLETE_B_E_2110_WITHIN13_PASS','unit_forms':17,'rows':34,'necessary_counts':counts,'original_fullguards_checked':oldcount,'new_fullguards_checked':newcount,'bound':13,'whole_guard_dispatch':records,'limits':'Necessary symbolic descriptions, not valid rooms; prior accepted classification/optical dependencies. No peer execution/import, new room, archive, direction or word discovery.','source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in dict.fromkeys(reads)}},indent=2)+'\n')
print('PASS17unitforms/34rows/151upper35lower/137old49new/ALL186wholeguards<=13')
