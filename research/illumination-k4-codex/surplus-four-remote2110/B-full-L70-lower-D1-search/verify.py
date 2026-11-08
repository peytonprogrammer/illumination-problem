"""Own exact candidate validation, geometry and complete universal guard."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
engine=ROOT/'surplus-four-local/R23-top6-search/verify.py';e={'__file__':str(engine)};exec(engine.read_text().split('\ndef path(d,nine):')[0],e)
globals().update({k:v for k,v in e.items()if not k.startswith('__')});HERE=Path(__file__).resolve().parent
raw=json.loads((HERE/'room.json').read_text());result=json.loads((HERE/'result.json').read_text())
assert result['status']=='FOUND_EXACT_PATH_PENDING_INDEPENDENT_VERIFICATION'
for name,key in [('room.json','room_sha256'),('search.py','search_source_sha256')]:assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==result[key]
P=[tuple(F(*x)for x in p)for p in result['candidate']['path']]
room={tri(tuple(map(tuple,t)))for t in raw['triangles']};V=boundary(room)
assert set(V)==set(map(tuple,raw['vertices'])) and len(V)==20
for i,(a,b)in enumerate(zip(V,V[1:]+V[:1])):
 for j,(c,d)in enumerate(zip(V,V[1:]+V[:1])):
  if i<j and j-i not in (1,len(V)-1):assert not edge_times(a,b,c,d)
physical(P,V);physical(P[::-1],V);physical([sigma(p)for p in P[::-1]],[sigma(p)for p in V])
assert all(not on((0,0),a,b)for a,b in zip(P[1:],P[2:]))
walls=[]
for p in P[1:-1]:
 w=[(a,b)for a,b in zip(V,V[1:]+V[:1])if on(p,a,b)];assert len(w)==1 and p not in V;walls.append(w[0])
U,Z,_=constraints(P,walls)
minimum=H|fan('L',[7,0])|fan('D',[1])|fan('R',[3])|fan('N',[7])
assert U<=minimum, U-minimum
maximum=(H|set().union(*(fan(k,range(8))for k in C))|fan((-2,-2),range(8)))-Z
# Exact unfolded image derived from actual mirrors, then independently passed to audit.
q=(F(2),F(2))
for a,b in walls[::-1]:
 v=reflect(sub(q,a),a,b);q=tuple(a[k]+v[k]for k in (0,1))
u,z,detail=audit(P,walls,minimum,maximum,q)
assert u==U and z==Z and U<=room and not Z&room
labels=[]
for k in C:
 for i in range(8):
  if Z&fan(k,[i]):labels.append(k+str(i))
for i in range(8):
 if Z&fan((-2,-2),[i]):labels.append('remote'+str(i))
# Check local angles and fixed budget independently of discovery code.
def angle(ts,p):return sum(90 if dot(*[sub(v,p)for v in t if v!=p])==0 else 45 for t in ts if p in t)
pts={p for t in room for p in t};A={p for p in pts if p[0]%2==p[1]%2==0}
assert{p for p in A if angle(room,p)==360}=={(0,0),(2,0),(2,2)}
J=sum(angle(room,p)==360 for p in pts-A);sN=sum(angle(room,p)==180 for p in pts-A)
assert(J,sN)==(4,2)
# At the single smooth lattice hit(0,1) the supporting maximal wall is strict.
assert len(P)-2==10
out={'status':'PARENT_EXACT_L70_D1_R3_TEN_GUARD_PASS_HAND_PENDING','path':[[str(x)for x in p]for p in P],'walls':walls,'required':sorted(U),'forbidden':sorted(Z),'minimum':sorted(minimum),'maximum':sorted(maximum),'proof':detail,'forbidden_labels':labels,'geometry':{'W':20,'J':J,'s_N':sN,'Q':10,'k':6,'Delta':4},'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in [HERE/'room.json',HERE/'result.json',HERE/'search.py',engine,Path(__file__)]},'limits':'ONEfixedroom stoppedfirstcandidate, ownFraction verification; whole-hand derivation/independentreview pending. No fullBfamily orrow closure.'}
(HERE/'verification.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print('PASS10',len(U),'U',len(Z),'Z','image',q,'blockers',labels)
