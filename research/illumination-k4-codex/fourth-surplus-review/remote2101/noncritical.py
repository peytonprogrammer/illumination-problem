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
old=read(ROOT/'fourth-surplus-review/three-unit-b1-independent/check.json')['named_guards']
capdoc=read(ROOT/'triangle-composition/inputs/caps.json')['cap_options'];caps={n:tuple(sorted(map(tuple,t)))for n,t in capdoc.items()}
# NoncriticalparentcannotchangeB/E/L/Tc ordinaryslots. Missingreference
# guards contain noD/R/NoroutsideK, so forceonecap at eachcriticalsite.
force=['forcing_missingB','forcing_sigma_missingB','forcing_missingT_ordinaryB','forcing_sigma_missingT_ordinaryB']
forcing=[]
for n in force:
 g=old[n];u,z=decode(g['required']),decode(g['forbidden'])
 assert (u|z)<=allK and not (u|z)&(full('D')|full('R')|full('N'))
 forcing.append({'name':n,'reflections':g['reflections'],'required_caps':[c for c,t in caps.items()if t in u],'forbidden_caps':[c for c,t in caps.items()if t in z]})
base=H|fan('L',[0])|fan('B',[1])|fan('E',[4])|fan('Tc',[5])
g1,g2=old['N_OO_L-E_NE'],old['N_CO_BTc_SW'];u1,z1=decode(g1['required']),decode(g1['forbidden']);u2,z2=decode(g2['required']),decode(g2['forbidden'])
assert u1<=base and u2<=base
assert not (z1|z2)&(base|full('D')|full('R')) and(z1|z2)<=allK
assert z1&full('N')==fan('N',[5,6]) and z2&full('N')==fan('N',[0,7])
windows=[]
for m in (3,4):
 for start in range(8):
  ss={(start+j)%8 for j in range(m)}
  d=int(bool(ss&{5,6}))+int(bool(ss&{0,7}))
  if d!=1:continue
  root=fan('N',ss);covers=[]
  for n,u,z in [('old13',u1,z1),('sigma13',u2,z2)]:
   if u<=base and not z&(base|root|full('D')|full('R')):covers.append(n)
  assert covers;windows.append({'sectors':sorted(ss),'covers':covers})
assert len(windows)==8
reads += [Path(__file__)]
out={'status':'PARENT_NONCRITICAL2101_D_R_N_WHOLE13','forcing':forcing,'N_windows':windows,'limits':'Onlysixalreadyacceptedguards; noopticalsearch/newroom/ordinaryassignment. Fullguard supportallwithinK, soallsoleoutsideKremoteleavesareharmless. Independenthandreviewneeded.','source_sha256':{str(q.relative_to(ROOT)):hashlib.sha256(q.read_bytes()).hexdigest()for q in dict.fromkeys(reads)}}
(HERE/'noncritical.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS noncritical2101whole13; fourforcing, twoopposite13, eightNwindows')
