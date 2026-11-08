"""One hand-prescribed eight-path on two frozen old residues, no discovery."""
from pathlib import Path
from fractions import Fraction as F
import json,runpy,hashlib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
sub=lambda a,b:(a[0]-b[0],a[1]-b[1])
cross=lambda a,b:a[0]*b[1]-a[1]*b[0]
dot=lambda a,b:a[0]*b[0]+a[1]*b[1]
tri=lambda t:tuple(sorted(map(tuple,t)))
raw=[('0','0'),('-2','-4/5'),('-3/2','-1'),('3','4/5'),('1','8/5'),('3','12/5'),('8/7','22/7'),('14/5','-1'),('3','-1/2'),('2','2')]
original_raw=raw
# Stop the prescribed trajectory at its FIRST actual target encounter.
P=[tuple(map(F,p)) for p in raw[:5]]+[(F(2),F(2))]
raw=[tuple(str(c) for c in p) for p in P]
def physical(path,V):
 # A valid connection stops at the requested mark's first encounter.
 target=path[-1]
 for i,(p,q) in enumerate(zip(path,path[1:])):
  if i==len(path)-2:break
  v=sub(q,p); w=sub(target,p)
  assert cross(v,w)!=0 or not(0<dot(w,v)<=dot(v,v)),('earlier target',i,target)
 walls=list(zip(V,V[1:]+V[:1]))
 def inside(p):
  value=False
  for a,b in walls:
   e,v=sub(b,a),sub(p,a)
   assert cross(e,v) or not(min(a[0],b[0])<=p[0]<=max(a[0],b[0]) and min(a[1],b[1])<=p[1]<=max(a[1],b[1]))
   if (a[1]>p[1])!=(b[1]>p[1]):
    x=a[0]+(p[1]-a[1])*(b[0]-a[0])/(b[1]-a[1])
    if p[0]<x:value=not value
  return value
 assert inside(path[0]) and inside(path[-1])
 for prev,p,nxt in zip(path,path[1:],path[2:]):
  hits=[(a,b) for a,b in walls if cross(sub(b,a),sub(p,a))==0 and 0<dot(sub(p,a),sub(b,a))<dot(sub(b,a),sub(b,a))]
  assert len(hits)==1,('nonstrict',p)
  a,b=hits[0];e,v,out=sub(b,a),sub(p,prev),sub(nxt,p)
  reflected=tuple(2*dot(v,e)*e[k]/dot(e,e)-v[k] for k in [0,1])
  assert cross(reflected,out)==0 and dot(reflected,out)>0
 for p,q in zip(path,path[1:]):
  assert inside(tuple((p[k]+q[k])/2 for k in [0,1]))
  v=sub(q,p)
  for a,b in walls:
   w,ap=sub(b,a),sub(a,p);den=cross(v,w)
   if den:
    t,s=cross(ap,w)/den,cross(ap,v)/den
    assert not(0<t<1 and 0<=s<=1),('earlier boundary',p,q,a,b)
   elif cross(ap,v)==0:
    aa,bb=dot(ap,v)/dot(v,v),dot(sub(b,p),v)/dot(v,v)
    assert max(min(aa,bb),F(0))>=min(max(aa,bb),F(1))



g=runpy.run_path(str(ROOT/'lower-bound-proof-audit/full-replay/guard-checker.py'))
U,Z=g['path_requirements'](P);rows={}
sigma=lambda p:(2-p[1],2-p[0])
for name,row in json.loads((HERE/'geometry.json').read_text()).items():
 V=[tuple(map(F,p)) for p in row['vertices']];room={tri(t) for t in row['triangles']}
 physical(P,V);physical(P[::-1],V);physical([sigma(p) for p in reversed(P)],[sigma(p) for p in V])
 assert U<=room and not Z&room
 rows[name]={'status':'PASS','reflections':4,'physical_forward_reverse_sigma':'PASS','ledger':row['ledger']}
V0=[tuple(map(F,p)) for p in next(iter(json.loads((HERE/'geometry.json').read_text()).values()))['vertices']]
try:
 physical([tuple(map(F,p)) for p in original_raw],V0)
except AssertionError as err:
 assert err.args[0][0]=='earlier target',err
else:
 raise AssertionError('original eight-contact path must be rejected for earlier target')
(HERE/'check.json').write_text(json.dumps({'status':'PASS','path':raw,'superseded_eight_contact_path':original_raw,'first_target_arrival':'fourth-reflection prefix, original fifth flight','initial_direction':[-5,-2],'required':sorted(U),'forbidden':sorted(Z),'controls':rows,'scope':'Suppliedeightpath truncated at FIRSTactualT:4reflections, threeoriginalDminus/Dplus/Rminusfixtures. SoleRplusoutsideclaim.'},indent=2)+'\n')
print('PASS: three original rooms, FIRST actualST after4reflections; forward/reverse/sigma/fullguards')
