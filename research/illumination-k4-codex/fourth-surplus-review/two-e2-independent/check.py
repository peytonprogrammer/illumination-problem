"""Independent review of named two-e2 implications and fixed controls. No discovery."""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
import json,runpy,hashlib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
source=ROOT/'surplus-four-local/two-e2-check.json'
d=json.loads(source.read_text())
g=runpy.run_path(str(ROOT/'lower-bound-proof-audit/full-replay/guard-checker.py'))
tri=lambda t:tuple(sorted(map(tuple,t)))
T=lambda ts:{tri(t) for t in ts}
sub=lambda a,b:(a[0]-b[0],a[1]-b[1])
cross=lambda a,b:a[0]*b[1]-a[1]*b[0]
dot=lambda a,b:a[0]*b[0]+a[1]*b[1]
sigma=lambda p:(2-p[1],2-p[0])
transform=lambda ts:{tri(sigma(p) for p in t) for t in ts}
D=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
centers={'L':(-2,0),'B':(0,-2),'D':(2,-2),'R':(4,0),'E':(4,2),'T':(2,4),'N':(0,2)}
def fan(c,st,m):
 return {tri((c,(c[0]+D[i%8][0],c[1]+D[i%8][1]),(c[0]+D[(i+1)%8][0],c[1]+D[(i+1)%8][1]))) for i in range(st,st+m)}
f=lambda n,st,m:fan(centers[n],st,m)
H=set().union(*(fan(c,0,8) for c in [(0,0),(2,0),(2,2)]))
caps={n:tri(t) for n,t in json.loads((ROOT/'zero-surplus-L/guard-incidence-check.json').read_text())['cap_options'].items()}
C=lambda ns:{caps[n] for n in ns}
DR=f('D',0,8)|f('R',0,8)
read=lambda p:json.loads((ROOT/p).read_text())
decode=lambda p:[tuple(F(*v) for v in q) for q in p]
sq=read('first-surplus-review/square-exchange-check.json')['paths']
z=read('zero-surplus-L/cover-check.json')['paths']
paths={'L11':decode(sq['L_thirteen']['path']),'five':decode(read('second-surplus-review/five-path-check.json')['five_path']),'thirteen':decode(z['thirteen']['path']),'sigma13':decode(z['thirteen_sigma']['path'])}
paths['sigmafive']=[sigma(p) for p in reversed(paths['five'])]
proj=read('third-surplus-review/local-mixed-project.json')['families']
for name,family,line in [('Bwest12','Bwest_Lcenter',664),('joined515','BDjoin_Bouter3',515),('joined2551','BDjoin_Bouter3',2551),('joined165','BDjoin_BHeast4',165)]:
 rows=[v for v in proj[family]['terms'] if v['source_line']==line];assert len(rows)==1
 paths[name]=decode(rows[0]['path'])
paths['uniform7']=[tuple(map(F,p)) for p in read('surplus-four-local/single-e2-check.json')['universal_lemmas']['uniform_seven']['path']]
paths['square_square3']=[(F(0),F(0)),(F(-2),F(1,3)),(F(4),F(4,3)),(F(1),F(11,6)),(F(2),F(2))]
def polygon(ts):
 edges=set()
 for a,b,c in ts:
  if cross(sub(b,a),sub(c,a))<0:b,c=c,b
  for u,v in [(a,b),(b,c),(c,a)]:
   if (v,u) in edges:edges.remove((v,u))
   else:edges.add((u,v))
 nxt=dict(edges);assert len(nxt)==len(edges)==len(set(nxt.values()))
 start=min(nxt);p=nxt[start];cyc=[start]
 while p!=start:
  assert p not in cyc;cyc.append(p);p=nxt[p]
 assert len(cyc)==len(edges)
 return [p for i,p in enumerate(cyc) if cross(sub(p,cyc[i-1]),sub(cyc[(i+1)%len(cyc)],p))]

def angle(t,p):
 return (1 if p[0]%2==p[1]%2 else 2) if p in t else 0

def ledger(ts):
 at=defaultdict(list);groups=defaultdict(list)
 for t in ts:
  a=next(p for p in t if p[0]%2==p[1]%2==0);groups[a].append(t)
  for p in t:at[p].append(t)
 fullA={a for a,parts in groups.items() if len(parts)==8}
 assert fullA=={(0,0),(2,0),(2,2)}
 Q=sum(3 if len(parts)==4 else len(parts) for a,parts in groups.items() if a not in fullA)
 J=sN=0
 for p,parts in at.items():
  if p[0]%2==p[1]%2==0:continue
  total=sum(angle(t,p) for t in parts);J+=total==8;sN+=total==4
 V=polygon(ts)
 return dict(W=len(V),Q=Q,J=J,sN=sN,k=J+sN,Delta=Q+sN-8)

def physical(P,V):
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
 assert inside(P[0]) and inside(P[-1])
 for prev,p,nxt in zip(P,P[1:],P[2:]):
  hit=[(a,b) for a,b in walls if cross(sub(b,a),sub(p,a))==0 and 0<dot(sub(p,a),sub(b,a))<dot(sub(b,a),sub(b,a))]
  assert len(hit)==1,('contact',p)
  a,b=hit[0];e=sub(b,a);v=sub(p,prev);w=sub(nxt,p)
  reflected=tuple(2*dot(v,e)*e[k]/dot(e,e)-v[k] for k in [0,1])
  assert cross(reflected,w)==0 and dot(reflected,w)>0
 for p,q in zip(P,P[1:]):
  assert inside(tuple((p[k]+q[k])/2 for k in [0,1]))
  v=sub(q,p)
  for a,b in walls:
   w,ap=sub(b,a),sub(a,p);den=cross(v,w)
   if den:
    t,s=cross(ap,w)/den,cross(ap,v)/den
    assert not(0<t<1 and 0<=s<=1),('early boundary',p,q,a,b)
   elif cross(ap,v)==0:
    aa,bb=dot(ap,v)/dot(v,v),dot(sub(b,p),v)/dot(v,v)
    assert max(min(aa,bb),F(0))>=min(max(aa,bb),F(1))


# Rebuild the thirteen fixed/possible implications from the proof's clauses.
spec=[]
def case(n,path,fixed,extra):spec.append((n,path,H|fixed,H|fixed|extra))
case('Bwest_or_rectangle_full_L_support','Bwest12',f('B',1,3)|C(['E-']), f('B',0,4)|f('L',0,8)|DR|f('N',0,8)|f('T',0,8)|C(['E-']))
for n,st,m in [('Lupper',7,3),('Lrectangle',6,4)]:
 case(n+'_L11_full_B_DR_bottom_N','L11',f('L',st,m)|C(['E-']),f('B',0,8)|DR|f('N',1,6)|C(['E-','T-']))
case('B_east_five_full_DR','five',f('B',0,3)|C(['T-']),DR|f('E',0,8)|f('L',0,8)|C(['T-','Nb-','Nr-','Nr+']))
case('B_east_bottom_N_sigma13','sigma13',f('B',0,3)|C(['L+','E-']),DR|f('N',1,6)|C(['L+','E-','T-']))
case('noncritical_bottom_N_sigma13','sigma13',C(['L+','E-']),DR|f('N',1,6)|C(['L+','E-','B+','T-']))
case('noncritical_right_N_thirteen','thirteen',C(['B+','T-']),DR|f('N',7,6)|C(['L+','E-','B+','T-']))
case('B_E_east_bottom_N_sigmafive','sigmafive',f('B',0,3)|f('E',3,3)|C(['L+']),DR|f('N',1,6)|C(['L+','T-']))
case('Lupper_Eeast_square_square3','square_square3',f('L',7,3)|f('E',3,3),DR|C(['B+','T-','Nb-']))
case('joined_N_not_Nrminus_uniform7','uniform7',C(['L+','E-']),f('B',0,8)|DR|f('T',0,8)|C(['L+','E-','Nb-','Nb+','Nr+']))
Bunion=f('B',6,5)
case('joined_Rplus_absent_515','joined515',f('B',7,3)|C(['L+','E-','Nr-']),Bunion|f('D',0,8)|C(['L+','E-','Nr-','R-','T-','T+']))
case('joined_Heast_Rplus_Tplus_absent_165','joined165',f('B',7,4)|C(['R+','Nr-']),f('D',0,8)|C(['L+','E-','Nr-','R+','T-']))
case('joined_Dplus_Tminus_absent_2551','joined2551',f('B',7,3)|C(['R+','E-','Nr-']),Bunion|(f('D',0,8)-C(['D+']))|C(['L+','E-','Nr-','R+','T+']))
assert {v[0] for v in spec}==set(d['named_implications'])
checks={}
for n,path,fixed,possible in spec:
 row=d['named_implications'][n]
 assert fixed==T(row['fixed']) and possible==T(row['possible'])
 U,Z=g['path_requirements'](paths[path]);assert U<=fixed and not Z&possible,n
 assert U==T(row['required']) and Z==T(row['forbidden'])
 Us,Zs=g['path_requirements']([sigma(p) for p in reversed(paths[path])]);assert Us==transform(U) and Zs==transform(Z)
 checks[n]={'status':'PASS','reflections':len(paths[path])-2}
# Direct per-vertex angle sum for the fifteen explicitly listed root joins.
rootJ={}
for bn,bs,bm,bh in [('Bouter3',7,3,0),('Bouter4',6,4,0),('BHeast4',7,4,1)]:
 for dn,ds,dm,base in [('Dhalf3',1,3,4),('Dhalf4',0,4,4),('Dwest3',2,3,4),('Dwest4a',1,4,5),('Dwest4b',2,4,4)]:
  ts=H|f('B',bs,bm)|f('D',ds,dm)
  pts=set().union(*map(set,ts));J=sum(sum(angle(t,p) for t in ts)==8 for p in pts if p[0]%2 or p[1]%2)
  assert J==base+bh,(bn,dn,J)
  rootJ[bn+'_'+dn]=J
leafJ={}
for n,bs,bm,ds,expect in [('Bouter3_Dcenter',7,3,3,3),('Bouter4_Dcenter',6,4,3,3),('BHeast4_Dcenter',7,4,3,4),('Bouter3_Dquarter',7,3,4,2),('BHeast4_Dquarter',7,4,4,3)]:
 ts=H|f('B',bs,bm)|f('D',ds,2);pts=set().union(*map(set,ts))
 J=sum(sum(angle(t,p) for t in ts)==8 for p in pts if p[0]%2 or p[1]%2)
 assert J==expect and d['root_leaf_angle_tables'][n]['ordinary_caps_at_k6_Delta4']==J+1
 leafJ[n]={'J':J,'n':J+1}
# Eleven named fixtures: independently reconstruct all vertices and ledgers.
controls={}
for n,row in d['hand_prescribed_fixtures'].items():
 ts=H|C(row['caps'])|set().union(*(f(*v) for v in row['fans']))
 assert ts==T(row['triangles']);ll=ledger(ts);assert ll==row['ledger']
 assert ll['W']==20 and ll['k']==6 and ll['Delta']==4
 V=polygon(ts);assert set(V)==set(map(tuple,row['vertices']))
 controls[n]={'status':'MATCH','ledger':ll}
# Own actual-boundary checks on both specified optical controls.
room=H|f('L',7,3)|f('E',3,3)|C(['B+','T-','Nb-','D-']);V=polygon(room);P=paths['square_square3']
physical(P,V);physical(P[::-1],V);physical([sigma(p) for p in reversed(P)],[sigma(p) for p in V]);assert ledger(room)==d['new_three_path']['control_ledger']
leaf=H|f('B',7,4)|f('D',3,2)|C(['L+','E-','Nr-','R+','T-']);V=polygon(leaf);P=paths['joined165']
physical(P,V);physical(P[::-1],V);assert ledger(leaf)==d['corrected_leaf_budget_control']['ledger']
# Reference cap forcing: fixed named paths and complete possible supersets.
allpartial=set().union(*(f(n,0,8) for n in centers));forces={}
force_specs=[('Bplus',decode(z['one']['path']),H,(H|allpartial)-C(['B+'])),('Eminus',decode(z['one_sigma']['path']),H,(H|allpartial)-C(['E-'])),('Tminus_Bordinary',decode(z['four']['path']),H|C(['B+']),H|(allpartial-f('B',0,8)-C(['T-']))|C(['B+'])),('Tminus_Beast',decode(sq['B_four']['path']),H|f('B',0,3),H|(allpartial-f('B',0,8)-C(['T-']))|f('B',0,3))]
for n,P,fixed,possible in force_specs:
 U,Z=g['path_requirements'](P);assert U<=fixed and not Z&possible,n
 forces[n]='PASS'
out={'status':'EXACT_CHECKS_PASS_HAND_VERDICT_SEPARATE','named_implications':checks,'fifteen_root_J_entries':rootJ,'five_leaf_J_entries':leafJ,'prescribed_residual_ledgers':controls,'reference_cap_forcing':forces,'new_three_path_actual_boundary_forward_reverse_sigma':'PASS','leaf_eighteen_path_actual_boundary_forward_reverse':'PASS','peer_receipt_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'limits':'No cap-assignment/room/path discovery. Finite checks verify named ingredients, not completeness.'}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS:13implications,15rootJ,5leafJ,11residualledgers,4forcingguards,3/18pathactualcontrols')
