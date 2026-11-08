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
caps_doc=read(ROOT/'triangle-composition/inputs/caps.json')['cap_options'];caps={n:tuple(sorted(map(tuple,t))) for n,t in caps_doc.items()}
cap_site={n:next(k for k,c in C.items() if c in caps[n]) for n in caps}
Kcenters=set(C.values())|{(0,0),(2,0),(2,2)}
sides=[(2,0),(0,2),(0,2),(-2,0),(-2,0),(0,-2),(0,-2),(2,0)]
opposite=[3,6,5,0,7,2,1,4]
rows=[]
for site,ref,forced in [('L',0,['B+','E-','T-']),('B',1,['L+','E-'])]:
 center=C[site]
 for m in (3,4):
  for start in range(8):
   ss=tuple((start+j)%8 for j in range(m))
   if ref not in ss:continue
   root=fan(site,ss)
   for i in ss:
    other=tuple(center[j]+sides[i][j] for j in (0,1))
    if other in Kcenters:continue
    leaf=fan(other,(opposite[i],));base=H|root|leaf|{caps[n] for n in forced}
    names=[n for n in caps if cap_site[n]!=site and n not in forced and not any(cap_site[n]==cap_site[f] for f in forced)]
    maximum=base|{caps[n] for n in names}
    # Every potential completion is contained in this whole support upper.
    pts={p for t in maximum for p in t};fixed=[]
    for p in sorted(pts):
     if all(x%2==0 for x in p):continue
     baseline=angle(H,p)==180 and (p[0]%2!=p[1]%2)
     if not baseline and angle(base,p)==angle(maximum,p)==180:fixed.append(p)
    common={p for t in root for p in t}&{p for t in leaf for p in t}
    commonC=[p for p in common if p[0]%2!=p[1]%2];assert len(commonC)==1
    c=commonC[0];rootC=angle(root,c);assert rootC in (90,180) and angle(leaf,c)==90
    h_sides=[p for p in {p for t in H for p in t} if p[0]%2!=p[1]%2 and angle(H,p)==180 and angle(root,p)==180]
    assert len(h_sides)<=1;cH=len(h_sides)
    # Per-vertex slot maxima certify exact J without enumerating cap assignments.
    certain={p for p in pts if any(x%2 for x in p) and angle(base,p)==360};potential=[]
    for p in pts:
     if all(x%2==0 for x in p):continue
     value=angle(base,p)
     for k in C:
      opts=[angle({caps[n]},p) for n in names if cap_site[n]==k]
      if opts:value+=max(opts)
     if value>=360 and p not in certain:potential.append((p,value))
    assert len(certain)==2+cH and not potential,(site,ss,other,opposite[i],certain,potential)
    row={'name':site+''.join(map(str,ss))+'_remote'+str(other)+'s'+str(opposite[i]),'site':site,'sectors':ss,'remote_A':other,'remote_sector':opposite[i],'shared_C':c,'root_angle_at_shared_C':rootC,'c_H':cH,'J':2+cH,'ordinary_cap_count':4+cH,'forced_caps':forced,'variable_caps':names,'additional_occupied_slots':4+cH-len(forced),'fixed_extra_smooth':fixed,'excluded_b1':len(fixed)>=2,'minimum':sorted(base),'maximum':sorted(maximum)}
    rows.append(row)
# Symbolic exact extra-smooth ledger: outside-H C constants plus B angles.
for row in rows:
 base=decode(row['minimum']);allowed=row['variable_caps'];maximum=decode(row['maximum'])
 pts={p for t in maximum for p in t};outsideC=[];b_terms=[]
 for p in sorted(pts):
  if p[0]%2!=p[1]%2 and angle(H,p)==0 and angle(base,p)==180:
   assert angle(maximum,p)==180;outsideC.append(p)
  if not (p[0]%2 and p[1]%2):continue
  constant=angle(base,p);weights={n:angle({caps[n]},p) for n in allowed if angle({caps[n]},p)}
  byslot={}
  for n,v in weights.items():byslot[cap_site[n]]=max(byslot.get(cap_site[n],0),v)
  if constant<=180<=constant+sum(byslot.values()):b_terms.append({'point':p,'fixed_degrees':constant,'cap_degrees':weights,'smooth_when_total':180})
 row['extra_C_constant']=outsideC;row['extra_B_terms']=b_terms
old=read(ROOT/'fourth-surplus-review/three-unit-b1-independent/check.json');guards=dict(old['named_guards'])
for rel in ('fourth-surplus-review/west-D1-search/check.json','fourth-surplus-review/mixed-Llower-Nsw-search/check.json','fourth-surplus-review/peer-B12-R3-four-independent/check.json'):
 for n,g in read(ROOT/rel)['fixed_paths'].items():guards[rel+':'+n]=g
for rel in ('triangle-composition/seven-path.json','triangle-composition/six-path.json'):
 g=read(ROOT/rel);u,z=path_requirements(fp(g['path']))
 assert u==decode(g['required_triangles']) and z==decode(g['forbidden_triangles'])
 guards[rel]={'required':sorted(u),'forbidden':sorted(z),'reflections':len(g['path'])-2}
for rel in ('fourth-surplus-review/remote2101-left-N6/check.json','fourth-surplus-review/peer-remote-roof-nine-independent/check.json','fourth-surplus-review/peer-remote-leaf-four-independent/check.json','fourth-surplus-review/remote2101-left-full/check.json','fourth-surplus-review/remote2101-B-upper/check.json','fourth-surplus-review/remote2101-B-roof/check.json','fourth-surplus-review/remote2101-B-roof-R3/check.json','fourth-surplus-review/remote2101-B-roof-D2/check.json','fourth-surplus-review/remote2101-B-N0/check.json','fourth-surplus-review/remote2101-smooth-B-one/check.json','fourth-surplus-review/remote2101-D1-R3/check.json','fourth-surplus-review/remote2101-D1-R3-Tc6/check.json'):
 for n,g in read(ROOT/rel)['fixed_paths'].items():guards[rel+':'+n]=g
# Sigma plus path reversal fixes actual ordered S/T; no new path search.
for label,g in list(guards.items()):
 if label.startswith(('fourth-surplus-review/remote2101-left-N6/','fourth-surplus-review/remote2101-B-roof-R3/')):
  guards[label+':sigma']={'required':sorted(tr(decode(g['required']))),'forbidden':sorted(tr(decode(g['forbidden']))),'reflections':g['reflections']}
assert len(old['named_guards'])==148
for row in rows:
 base,maximum=decode(row['minimum']),decode(row['maximum']);allowed=set(row['variable_caps']);conds=[]
 for label,g in guards.items():
  u,z=decode(g['required']),decode(g['forbidden'])
  if z&base or not u<=maximum:continue
  req={n for n in allowed if caps[n] in u-base};forbid={n for n in allowed if caps[n] in z}
  if req&forbid or len({cap_site[n] for n in req})!=len(req):continue
  forbid={n for n in forbid if cap_site[n] not in {cap_site[x] for x in req}}
  conds.append({'required':sorted(req),'forbidden':sorted(forbid),'guard':label,'reflections':g['reflections']})
 # Keep only logically minimal sufficient conjunctions; ordinary slot
 # exclusivity was already used, no assignment or trajectory enumeration.
 keep=[]
 for c in sorted(conds,key=lambda c:(len(c['required'])+len(c['forbidden']),c['reflections'],c['guard'])):
  if any(set(d['required'])<=set(c['required']) and set(d['forbidden'])<=set(c['forbidden']) for d in keep):continue
  keep.append(c)
 row['sufficient_old_guard_conditions']=keep
 row['unconditional_guard']=next((c for c in keep if not c['required'] and not c['forbidden']),None)
reads += [ROOT/'fourth-surplus-review/structural-reduction.txt',ROOT/'fourth-surplus-review/remote22.txt']
reads += [ROOT/'triangle-composition/inputs'/f for f in ('guard_checker.py','boundary_replay.py','illumination_geometry.py')]+[Path(__file__)]
out={'status':'REMOTE2101_CRITICAL_PARENT_SINGLELEAF_NECESSARY_TEMPLATES_AND_FIXED_GUARD_PROJECTION','candidate_templates':len(rows),'fixed_b1_excluded':sum(r['excluded_b1'] for r in rows),'templates':rows,'guard_inventory_size':len(guards),'limits':'Root/leaf fan templates and per-vertex angle/slot upper bounds only; no completed rooms/cap assignments/rays/directions/words/archive. Necessary table completeness needs hand proof; oldguard implications exact, unmatched is not dark.','source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in dict.fromkeys(reads)}}
(HERE/'classification.json').write_text(json.dumps(out,indent=2)+'\n')
print('Critical parent-leaf templates',len(rows),'fixedb1 exclusions',out['fixed_b1_excluded'])
for row in rows:
 print(row['name'],'Cangle',row['root_angle_at_shared_C'],'n',row['ordinary_cap_count'],'extra',row['additional_occupied_slots'],'fixed',row['fixed_extra_smooth'],'terms',len(row['sufficient_old_guard_conditions']),'unconditional',row['unconditional_guard'])
