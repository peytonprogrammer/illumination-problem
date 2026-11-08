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
classification=read(HERE/'classification.json');old=read(ROOT/'fourth-surplus-review/three-unit-b1-independent/check.json');guards=dict(old['named_guards'])
rels=['remote2101-left-N6','peer-remote-roof-nine-independent','peer-remote-leaf-four-independent','remote2101-left-full','remote2101-B-upper','remote2101-B-roof','remote2101-B-roof-R3','remote2101-B-roof-D2','remote2101-B-N0','remote2101-smooth-B-one','remote2101-D1-R3','remote2101-D1-R3-Tc6','remote2101-Bfull-N5','remote2101-Bfull-lower','west-D1-search','mixed-Llower-Nsw-search','peer-B12-R3-four-independent']
short={}
for name in rels:
 rel='fourth-surplus-review/'+name+'/check.json'
 for n,g in read(ROOT/rel)['fixed_paths'].items():guards[rel+':'+n]=g;short[n]=g
for rel in ['triangle-composition/seven-path.json','triangle-composition/six-path.json']:
 g=read(ROOT/rel);guards[rel]={'required':g['required_triangles'],'forbidden':g['forbidden_triangles'],'reflections':len(g['path'])-2}
for label,g in list(guards.items()):
 if label.startswith(('fourth-surplus-review/remote2101-left-N6/','fourth-surplus-review/remote2101-B-roof-R3/')):
  guards[label+':sigma']={'required':sorted(tr(decode(g['required']))),'forbidden':sorted(tr(decode(g['forbidden']))),'reflections':g['reflections']}
def sg(name):
 g=short[name];return{'required':sorted(tr(decode(g['required']))),'forbidden':sorted(tr(decode(g['forbidden']))),'reflections':g['reflections']}
G={**short,'sigma_core_three':sg('core_three'),'sigma_N6_four':sg('N6_four'),'sigma13':old['named_guards']['N_CO_BTc_SW'],'Btwo':old['named_guards']['forcing_missingT_outerB'],'Bfive':old['named_guards']['N_CO_LB_NE']}
capdoc=read(ROOT/'triangle-composition/inputs/caps.json')['cap_options'];caps={n:tuple(sorted(map(tuple,t)))for n,t in capdoc.items()}
site=lambda n:'N'if n.startswith(('Nb','Nr'))else n[0]
def hand_B(row,cc):
 if 'D+'in cc and 'R-'in cc:return'smooth_B_one'
 if row['sectors']==[0,1,2,3]:
  if 'T-'not in cc:return'Btwo'
  return'Bfive'if'Nb+'not in cc else'sigma13'
 if 'Nr-'in cc:return'Bcenter_R3_N7_nine'if'R+'in cc else'sigma_N6_four'
 if 'Nb+'in cc:
  if'D-'not in cc:return'N6_four'
  return'L0_eight'if'T+'in cc else'sigma13'
 if 'Nr+'in cc:
  if not cc&{'T-','T+'}:return'N0_six'
  if'D+'in cc:return'core_three'
  if'R-'in cc:return'sigma_core_three'
  return'L0_eight'
 if 'Nb-'in cc:
  assert row['sectors']==[1,2,3,4]and row['remote_sector']==0
  if'T+'not in cc:return'sigma13'
  if'D+'in cc:return'core_three'
  if'D-'in cc:return'core_five'
  if'R+'in cc:return'Bcenter_R3_eight'
  assert'R-'in cc;return'sigma_core_three'
 # Nempty -> D,R,Tc mustallbeoccupied byexactthreeextras.
 assert cc&{'D-','D+'}and cc&{'R-','R+'}and cc&{'T-','T+'}
 if'T-'in cc:return'sigma13'
 if'D+'in cc:return'Tc6_four' # D1R4 wasalreadyhandledone.
 if'R+'in cc:return'Bcenter_R3_eight'
 assert'D-'in cc and'R-'in cc
 if row['sectors']==[1,2,3]:return'B_upper_Tc6_six'
 assert row['sectors']==[1,2,3,4]and row['remote_sector']==7
 return'L0_B12_R4_E4_eight'
rows=[]
for row in classification['templates']:
 if row['excluded_b1']:continue
 base=decode(row['minimum']);groups={}
 for n in row['variable_caps']:groups.setdefault(site(n),[]).append(n)
 for tup in itertools.product(*[[None]+v for v in groups.values()]):
  cc={n for n in tup if n}
  if len(cc)!=row['additional_occupied_slots']:continue
  b=len(row['extra_C_constant'])+sum(term['fixed_degrees']+sum(v for n,v in term['cap_degrees'].items()if n in cc)==180 for term in row['extra_B_terms'])
  if b!=1:continue
  symbolic=base|{caps[n]for n in cc}
  if row['site']=='B':label=hand_B(row,cc);g=G[label]
  else:
   matches=[c for c in row['sufficient_old_guard_conditions']if set(c['required'])<=cc and not set(c['forbidden'])&cc]
   assert matches,row['name'];label=min(matches,key=lambda c:c['reflections'])['guard'];g=guards[label]
  u,z=decode(g['required']),decode(g['forbidden'])
  assert u<=symbolic and not z&symbolic,(row['name'],cc,label,u-symbolic,z&symbolic)
  assert g['reflections']<=13
  rows.append({'template':row['name'],'variable_caps':sorted(cc),'hand_dispatch_guard':label,'reflections':g['reflections']})
assert len(rows)==205
reads += [HERE/'classification.txt',HERE/'support.json',HERE/'noncritical.txt',HERE/'noncritical.json',Path(__file__)]
out={'status':'PARENT_WHOLE_CRITICAL_REMOTE2101_HAND_DISPATCH_PASS','necessary_symbolic_labels':len(rows),'bound':max(r['reflections']for r in rows),'rows':rows,'limits':'Necessaryb/nslotassignments, notvalidrooms; no polygonconstruction ordiscovery. Classificationcompleteness arguedinhandtext. Everylabelselectsoneexplicitwholeopticalguard; independentreviewandnoncriticaljoinneeded.','source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in dict.fromkeys(reads)}}
(HERE/'final-dispatch.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS HAND Bdispatch plusL',len(rows),'necessarylabels, wholebound',out['bound'])
