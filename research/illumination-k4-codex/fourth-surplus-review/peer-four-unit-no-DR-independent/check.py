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
from itertools import product
parent_dir=ROOT/'surplus-four-local/four-unit-no-DR'
parent=read(parent_dir/'join.json');probe=read(parent_dir/'check.json');new=read(parent_dir/'roof-center-four/verification.json')
for doc in (parent,probe,new):
 for rel,pin in doc['source_sha256'].items():
  p=ROOT/rel;reads.append(p);assert hashlib.sha256(p.read_bytes()).hexdigest()==pin,rel
old=read(ROOT/'fourth-surplus-review/three-unit-b1-independent/check.json')
assert old['bound']==13 and len(old['named_guards'])==148
for rel,pin in old['source_sha256'].items():
 p=ROOT/rel;reads.append(p);assert hashlib.sha256(p.read_bytes()).hexdigest()==pin,rel
P=fp([(0,0),('1/6',1),('2/3',-2),('8/5','18/5'),('16/7','26/7'),(2,2)])
W=[((0,1),(1,1)),((0,-2),(1,-2)),((1,3),(2,4)),((2,4),(3,3))]
mi=H|fan('B',(0,1))|fan('Tc',(5,6));z=fan('B',(7,))|fan('Tc',(4,7))|fan('N',(6,))
u,Z=optical('roof_center_four',P,W,mi,allK-z,(2,12),new)
assert len(u)==16 and Z==z
assert not (u|Z)&(full('D')|full('R'))
assert on((1,0),P[2],P[3]) and incident((F(1),F(0)))<=H
assert all(not on((0,0),a,b) for a,b in zip(P[1:],P[2:]))
PS=[sigma(p) for p in P[::-1]];WS=[(sigma(a),sigma(b)) for a,b in W[::-1]]
q=PS[-1]
for a,b in WS[::-1]:
 axis=sub(b,a);v=sub(q,a);q=tuple(a[k]+2*dot(v,axis)*axis[k]/dot(axis,axis)-v[k] for k in (0,1))
optical('sigma_roof_center_four',PS,WS,tr(mi),tr(allK-z),q,None)
assert tr(z)==fan('E',(6,))|fan('L',(1,6))|fan('N',(7,))
lo,hi=F(1,7),F(2,11)
for name,fn,a,b in [('ceil',lambda d:d,0,1),('Bfloor',lambda d:4*d,0,1),('up_source_portal',lambda d:7*d,1,3),('roof_inlet',lambda d:9*d,1,2),('Tc5',lambda d:8*d/(1-d),1,2),('Tc6',lambda d:(4-8*d)/(1+d),2,3),('roof_outlet',lambda d:4-11*d,2,3)]:
 x,y=fn(lo),fn(hi);assert a<=x<=b and a<=y<=b and x!=y,(name,x,y)
d=F(1,6);a=8*d/(1-d);c=(4-8*d)/(1+d)
assert lo<d<hi and 4-12*d==2
assert P==fp([(0,0),(d,1),(4*d,-2),(a,a+2),(c,6-c),(4-12*d,2)])
# Algebraic line identities of the new roof return, derived in the hand proof.
assert (1-d)*a==8*d and (1+d)*c==4-8*d
assert c-d*(6-c)==4-14*d
# Derive critical two-sector forms by consecutive-sector + forced-reference rules.
ref={'L':0,'B':1,'E':4,'Tc':5};critical=tuple(ref)
forms={}
for site,k in ref.items():
 possible={frozenset((j,(j+1)%8)) for j in range(8) if k in (j,(j+1)%8)}
 assert len(possible)==2
 forms[site]=sorted(possible,key=lambda s:tuple(sorted(s)))
expected={'L':{frozenset((7,0)),frozenset((0,1))},'B':{frozenset((0,1)),frozenset((1,2))},'E':{frozenset((3,4)),frozenset((4,5))},'Tc':{frozenset((4,5)),frozenset((5,6))}}
assert {k:set(v) for k,v in forms.items()}==expected
Nforms={frozenset((j,(j+1)%8)) for j in range(8) if set((j,(j+1)%8))&{5,6,7,0} and not {6,7}<=set((j,(j+1)%8))}
assert Nforms=={frozenset((4,5)),frozenset((5,6)),frozenset((7,0)),frozenset((0,1))}
# Explicit eight forcing conditions with other stars FULL.
forcing=[]
def force(label,mi,ma):
 g=old['named_guards'][label];U,Z=decode(g['required']),decode(g['forbidden']);assert U<=mi and not Z&ma
 forcing.append(label)
force('forcing_missingB',H,allK-fan('B',(1,)))
force('forcing_sigma_missingB',H,allK-fan('E',(4,)))
for label,ss,ee in [('ordinaryB',(1,),(4,)),('centerB',(1,2),(3,4)),('outerB',(0,1),(4,5))]:
 force('forcing_missingT_'+label,H|fan('B',ss),(allK-full('B')-fan('Tc',(5,)))|fan('B',ss))
 force('forcing_sigma_missingT_'+label,H|fan('E',ee),(allK-full('E')-fan('L',(0,)))|fan('E',ee))
bridge_u,bridge_z=path_requirements(fp([(0,0),(2,2)]));assert bridge_u<=H|fan('N',(6,7)) and not bridge_z
# Build the two exhaustive shape categories independently, without peer row labels.
shapes=[]
for fs in product(*(forms[k] for k in critical)):
 for ns in ((),(5,),(6,),(7,),(0,)):
  shapes.append(dict(zip(critical,fs))|{'N':frozenset(ns)})
for missing in critical:
 sites=tuple(k for k in critical if k!=missing)
 for fs in product(*(forms[k] for k in sites)):
  for ns in Nforms:shapes.append(dict(zip(sites,fs))|{missing:frozenset((ref[missing],)),'N':ns})
key=lambda s:tuple((k,tuple(sorted(s[k]))) for k in (*critical,'N'))
assert len(shapes)==len({key(s) for s in shapes})==208
parent_rows={key(r['spec']):r for r in probe['rows']};assert {key(s) for s in shapes}==set(parent_rows)
guards={name:(decode(g['required']),decode(g['forbidden']),g['reflections']) for name,g in old['named_guards'].items()}
ordinary=fan('D',(1,2))|fan('R',(3,4));rows=[];counts=defaultdict(int)
for spec in sorted(shapes,key=key):
 minimum=H|set().union(*(fan(k,ss) for k,ss in spec.items()));maximum=minimum|ordinary
 points={p for t in maximum for p in t if p[0]%2 and p[1]%2}
 bad=[p for p in sorted(points) if angle(minimum,p)==angle(maximum,p)==180]
 prior=parent_rows[key(spec)]
 assert set(bad)==set(map(tuple,prior['excluded_b0']))
 if bad:
  counts['fixed_oddodd180_excluded']+=1;rows.append({'shape':key(spec),'excluded_at':bad[0]});continue
 fits=sorted((n,name) for name,(U,Z,n) in guards.items() if U<=minimum and not Z&maximum)
 if fits:
  n,name=fits[0];assert n<=13;counts['accepted_guard_cover']+=1
  rows.append({'shape':key(spec),'guard':name,'reflections':n});continue
 # No old guard works: independent direct/sigma test, with both D/R choices free.
 fits4=[name for name,U,Z in [('direct',u,z),('sigma',tr(u),tr(z))] if U<=minimum and not Z&maximum]
 assert fits4,(key(spec),'unclosed')
 counts['new_four_cover']+=1;rows.append({'shape':key(spec),'new_four':fits4,'reflections':4})
assert dict(counts)=={'accepted_guard_cover':44,'fixed_oddodd180_excluded':161,'new_four_cover':3} or sorted(counts.items())==sorted({'accepted_guard_cover':44,'fixed_oddodd180_excluded':161,'new_four_cover':3}.items())
# No peer code is executed; topology is inherited from independently accepted b0root lemma.
reads += [parent_dir/'argument.txt',parent_dir/'check.py',parent_dir/'join.py',parent_dir/'roof-center-four/verify.py',parent_dir/'roof-center-four/argument.txt',ROOT/'surplus-four-local/four-unit-DR-independent/review.txt',ROOT/'surplus-four-local/four-unit-one-DR-independent/review.txt']
reads += [ROOT/'triangle-composition/inputs'/f for f in ('guard_checker.py','boundary_replay.py','illumination_geometry.py')]+[Path(__file__)]
out={'status':'INDEPENDENT_NO_POSITIVE_DR_FOUR_UNIT_COVER_ACCEPT','bound':13,'new_fixed_paths':records,'counts':dict(counts),'forcing_guards':forcing,'direct_bridge':'PASS','rows':rows,'whole_four_unit_join':'Accepted positiveDR<=13 + independentlyacceptednoDR<=13 yields ENTIRE stated LOCAL four-e1/b0<=13.','limits':'Exact symbolic labels, no rooms generated or D/R assignments enumerated. Inherited accepted finiteoptics; root exclusion/topology handaudited. Historical helper origins shared, not formal/expertverification. Othermixed/remote/Delta4 not closed.','source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in dict.fromkeys(reads)}}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
print('ACCEPT independentnewroof4/sigma16U4Z/8forcing/bridge/208labels:161excluded,44oldguard,3newfour. ENTIRElocalfourunit<=13 withacceptedDRjoin.')
