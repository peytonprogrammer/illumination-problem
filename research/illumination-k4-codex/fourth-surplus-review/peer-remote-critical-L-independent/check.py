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
q=ROOT/'surplus-four-remote2110/critical-logic';parent=read(q/'check.json');refresh=read(q/'guard-refresh.json')
for doc in[parent,refresh]:
 for rel,h in doc['source_sha256'].items():
  f=ROOT/rel;reads.append(f);assert hashlib.sha256(f.read_bytes()).hexdigest()==h,rel
reads += [q/'argument.txt',q/'coverage.txt',q/'check.py',q/'guard-refresh.py']
# Buildonlytheselectedacceptedguardmap, withfreshOLDcoordinates.
G={}
for name,g in refresh['paths'].items():
 P=fp(g['path']);u,z=path_requirements(P);assert(u,z)==(decode(g['required']),decode(g['forbidden']))
 assert path_requirements(P[::-1])==(u,z)and path_requirements([sigma(p)for p in P[::-1]])==(tr(u),tr(z))
 G['148:'+name]={'required':sorted(u),'forbidden':sorted(z),'reflections':len(P)-2}
for rel in ['surplus-four-remote2110/peer-optical-review/check.json','surplus-four-remote2110/N6-four-review/check.json','surplus-four-remote2110/B-eight-review/check.json']:
 for name,g in read(ROOT/rel)['paths'].items():G[name]=g
G['right_leaf_four']=read(ROOT/'surplus-four-remote2110/roof-N5-search/verification.json');G['right_leaf_four']={**G['right_leaf_four'],'reflections':4}
for name,g in read(ROOT/'surplus-four-local/west-four-mixed-eleven-review/check.json')['new_path_records'].items():
 if'required'in g:G['West_mixed:'+name]={**g,'reflections':g['proof']['reflections']}
for name,g in list(G.items()):G['sigma:'+name]={'required':sorted(tr(decode(g['required']))),'forbidden':sorted(tr(decode(g['forbidden']))),'reflections':g.get('reflections',g.get('proof',{}).get('reflections'))}
forms={'B':[(0,1),(1,2)],'D':[(0,1),(1,2),(2,3)],'R':[(2,3),(3,4),(4,5)],'E':[(3,4),(4,5)],'Tc':[(4,5),(5,6)],'N':[(4,5),(5,6),(7,0),(0,1)]}
assert sum(map(len,forms.values()))==16
ordinary={'B':[(),(1,),(2,)],'D':[(),(1,),(2,)],'R':[(),(3,),(4,)],'E':[(),(3,),(4,)],'Tc':[(),(5,),(6,)],'N':[(),(5,),(6,),(7,),(0,)]}
parents=read(ROOT/'fourth-surplus-review/peer-remote-noncritical-independent/check.json')['templates'];parents=[t for t in parents if t[0]=='L'];assert len(parents)==8
pt={ (tuple(sorted(t['sectors'])),tuple(t['remote']),t['leaf'],t['unit'],tuple(sorted(t['unit_sectors']))):t for t in parent['templates']if t['parent']=='L'}
assert len(pt)==128
records=[];unitrows=[]
for _,ps,rc,leafs in parents:
 base=H|fan('L',ps)|fan(tuple(rc),[leafs])
 for unit,windows in forms.items():
  for unitss in windows:
   key=(tuple(sorted(ps)),tuple(rc),leafs,unit,tuple(sorted(unitss)));pr=pt[key]
   fixed=base|fan(unit,unitss);slots=[k for k in ordinary if k!=unit]
   refs={'B':1,'E':4,'Tc':5};opts={k:([ss for ss in ordinary[k]if refs[k]in ss]if k in refs else ordinary[k])for k in slots}
   assert all(k not in refs or refs[k]in unitss for k in[unit])
   maximum=fixed|set().union(*(fan(k,ss)for k in slots for ss in opts[k]));pts={p for t in maximum for p in t}
   nonA={p for p in pts if p[0]%2 or p[1]%2};HC={p for p in nonA if p[0]%2!=p[1]%2 and angle(H,p)==180}
   baseline={p for p in HC if angle(fixed,p)==180};assert baseline==set(map(tuple,pr['baseline_M_vertices']))
   J=sum(angle(fixed,p)==360 for p in nonA);assert J==pr['J']==pr['ordinary_slots_required']
   for p0 in nonA:
    a=angle(fixed,p0);mx=a+sum(max(angle(fan(k,ss),p0)for ss in opts[k])for k in slots)
    assert a==360 or mx<360
   for term in pr['angle_terms']:
    p0=tuple(term['vertex']);assert p0 in nonA-baseline and term['fixed_degrees']==angle(fixed,p0)
    for k in slots:
     assert term['ordinary_coefficients'][k]=={str(ss):angle(fan(k,ss),p0)for ss in opts[k]}
   assert {tuple(t['vertex'])for t in pr['angle_terms']}==nonA-baseline
   got={}
   for selection in itertools.product(*(opts[k]for k in slots)):
    if sum(bool(ss)for ss in selection)!=J:continue
    symbolic=fixed|set().union(*(fan(k,ss)for k,ss in zip(slots,selection)))
    # AtH-sideC uncovered180 isbaseline; neverextraB. Directactualangle
    # evaluationratherthanparentcoefficientstringsfortheb0filter.
    if any(angle(symbolic,p0)==180 for p0 in nonA-HC):continue
    label=tuple((k,tuple(ss))for k,ss in zip(slots,selection)if ss);got[label]=symbolic
   supplied={tuple((k,tuple(c['caps'][k]))for k in slots if k in c['caps']):c for c in pr['covers']}
   assert not pr['uncovered']and set(got)==set(supplied)and len(got)==pr['necessary_labels']
   for label,symbolic in got.items():
    rec=supplied[label];g=G[rec['guard']];u,z=decode(g['required']),decode(g['forbidden']);n=g.get('reflections',g.get('proof',{}).get('reflections'))
    assert u<=symbolic and not z&symbolic and n==rec['bound']<=13
    records.append({'parent':ps,'remote':rc,'leaf':leafs,'unit':unit,'unit_sectors':unitss,'caps':dict(label),'guard':rec['guard'],'bound':n})
   unitrows.append({'key':key,'J':J,'labels':len(got)})
assert len(records)==205
counts={}
for g in records:
 k=''.join(map(str,g['parent']))+'/leaf'+str(g['leaf']);counts[k]=counts.get(k,0)+1
reads += [ROOT/'triangle-composition/inputs/guard_checker.py',Path(__file__)]
out={'status':'INDEPENDENT_CRITICAL_L2110_16_INTERFACE_WHOLE13_CHECK_PASS','unit_forms':16,'parent_unit_rows':128,'necessary_labels':205,'bound':13,'per_interface':counts,'whole_guard_dispatch':records,'limits':'128localfan/equationrows and205necessarysymboliclabels, NOT validrooms; no completedpolygon/search/archive/peerexecution. Handcompleteness/forcing/scope review inreview.txt.','source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in dict.fromkeys(reads)}}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS independent16unitforms/8Linterfaces/128rows/205labels/allfullguards<=13')
