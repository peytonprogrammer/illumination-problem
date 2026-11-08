"""One hand-derived four-reflection path on three supplied exact residues.
No ray/direction/word discovery, room generation, or source archives.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,runpy

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
source=ROOT/'surplus-four-local/single-e2-check.json'
review=ROOT/'fourth-surplus-review/single-e2-independent/check.json'
cap_source=ROOT/'zero-surplus-L/guard-incidence-check.json'
guard_source=ROOT/'lower-bound-proof-audit/full-replay/guard-checker.py'
frozen_source=HERE/'geometry.json'
d={'residues':json.loads(frozen_source.read_text())}
reviewed=json.loads(review.read_text())
guard=runpy.run_path(str(guard_source))
P=[(F(0),F(0)),(F(-1),F(-2)),(F(-2,3),F(-8,3)),
   (F(-1),F(-5,2)),(F(0),F(-2)),(F(2),F(2))]
sub=lambda a,b:(a[0]-b[0],a[1]-b[1])
cross=lambda a,b:a[0]*b[1]-a[1]*b[0]
dot=lambda a,b:a[0]*b[0]+a[1]*b[1]
tri=lambda t:tuple(sorted(map(tuple,t)))
H=set().union(*(guard['incident'](tuple(map(F,p))) for p in [(0,0),(2,0),(2,2)]))
D=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
c=(0,-2)
root={tri((c,(c[0]+D[i][0],c[1]+D[i][1]),
             (c[0]+D[(i+1)%8][0],c[1]+D[(i+1)%8][1]))) for i in [1,2,3,4]}
caps={n:tri(t) for n,t in json.loads(cap_source.read_text())['cap_options'].items()}
U,Z=guard['path_requirements'](P)
assert U<=H|root and not Z&(H|root|set(caps.values()))

def physical(path,V):
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

sigma=lambda p:(2-p[1],2-p[0])
Ps=[sigma(p) for p in reversed(P)]
Us,Zs=guard['path_requirements'](Ps)
assert Us=={tri(sigma(p) for p in t) for t in U}
assert Zs=={tri(sigma(p) for p in t) for t in Z}
rows={};geometry={}
names=['Bfullwest_Nrminus_Rplus_Dminus_Tminus',
       'Bfullwest_Nrminus_Rplus_Dplus_Tminus',
       'Bfullwest_Nrminus_Rplus_Dplus_Tplus']
for name in names:
 row=d['residues'][name];room={tri(t) for t in row['triangles']}
 V=[tuple(map(F,p)) for p in row['vertices']]
 assert U<=room and not Z&room
 physical(P,V);physical(P[::-1],V);physical(Ps,[sigma(p) for p in V])
 smooth={}
 for p in [(-1,-2),(0,-2)]:
  angle=sum((45 if p[0]%2==p[1]%2 else 90) for t in room if p in t)
  assert angle==180 and p not in V
  smooth[str(p)]=angle
 assert row['ledger']==reviewed['residues'][name]['ledger']
 rows[name]=dict(status='PASS',reflections=4,physical_forward_reverse_sigma='PASS',
                 smooth_contact_angles=smooth,previously_reviewed_ledger=row['ledger'])
 geometry[name]=dict(vertices=row['vertices'],triangles=row['triangles'],ledger=row['ledger'])

# Hand contact formulas, evaluated only at the analytically solved parameter.
d0=F(1,2)
formulas=[(F(0),F(0)),(F(-1),-1/d0),
          ((2*d0-2)/(1+d0),-4/(1+d0)),(F(-1),3*d0-4),
          ((4*d0-2)/(1-d0),(6*d0-4)/(1-d0)),(8*d0-2,F(2))]
assert formulas==P and F(3,7)<d0<F(3,5)
out=dict(status='PASS',scope='One analytically prescribed four-path, universal ordinary-cap guard, three supplied old residues. No discovery.',
         path=[[str(q) for q in p] for p in P],initial_direction=[-1,-2],reflections=4,
         parameter='1/2',sufficient_open_interval=['3/7','3/5'],target_equation='x=8d-2 at y=2',
         required=sorted(U),forbidden=sorted(Z),ordinary_cap_blockers=[n for n,t in caps.items() if t in Z],
         universal_implication='H+Bfullwest suffice; every ordinary cap is harmless',controls=rows,
         inputs={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in [frozen_source,review,cap_source,guard_source]})
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: universal four-reflection path; all three residues/reverse/sigma; both integer hits smooth180')
