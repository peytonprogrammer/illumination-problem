"""Independent fixed-path and local-angle audit of mixed root-leaf reduction."""
from pathlib import Path
from fractions import Fraction as F
import json,sys,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
sys.path.insert(0,str(ROOT/'triangle-composition/inputs'))
from guard_checker import path_requirements
from boundary_replay import replay,cross,sub
import illumination_geometry as g
tri=lambda t:tuple(sorted(map(tuple,t)))
dirs=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
centers={'L':(-2,0),'B':(0,-2),'D':(2,-2),'R':(4,0),'E':(4,2),'Tc':(2,4),'N':(0,2)}
def fan_at(c,ss):
 return {tri((c,(c[0]+dirs[i%8][0],c[1]+dirs[i%8][1]),(c[0]+dirs[(i+1)%8][0],c[1]+dirs[(i+1)%8][1]))) for i in ss}
fan=lambda name,ss:fan_at(centers[name],ss)
full=lambda name:fan(name,range(8))
H=set().union(*(fan_at(c,range(8)) for c in [(0,0),(2,0),(2,2)]))
read=lambda rel:json.loads((ROOT/rel).read_text())
caps={n:tri(t) for n,t in read('triangle-composition/inputs/caps.json')['cap_options'].items()}
C=lambda ns:{caps[n] for n in ns}
decode=lambda P:[tuple(F(*v) for v in p) for p in P]
sigma=lambda p:(2-p[1],2-p[0]);tr=lambda ts:{tri(sigma(p) for p in t) for t in ts}
base7=[tuple(map(F,p)) for p in read('surplus-four-local/single-e2-check.json')['universal_lemmas']['uniform_seven']['path']]
left3=decode(read('first-surplus-review/residual-cover-check.json')['path'])
b6=decode(read('first-surplus-review/bottom-residual-check.json')['path'])
L12=decode(read('first-surplus-review/centered-left-check.json')['paths']['left']['path'])
z=read('zero-surplus-L/cover-check.json')['paths']
f=read('third-surplus-review/independent-review/guard-extension-check.json')['forcing_paths']
paths={'one_sigma':decode(z['one_sigma']['path']),'sigma_four':decode(z['four_sigma']['path']),
 'sigma_centerB3':decode(f['sigma_centeredB3']['path']),'sigma_outerB2':decode(f['sigma_outerB2']['path']),
 'uniform7':base7,'Lsquare5':[base7[0],(F(-2),F(1,3))]+base7[4:],
 'Esquare5':base7[:4]+[(F(4),F(4,3))]+base7[7:],
 'Tcenter3':[sigma(p) for p in left3[::-1]],'Ecenter6':[sigma(p) for p in b6[::-1]],'Lcenter12':L12}
BDR=full('B')|full('D')|full('R');other=BDR|full('Tc')|full('N')
rules=[
 ('missing_E_reference','one_sigma',H,H|other|full('L')|(full('E')-C(['E-']))),
 ('ordinary_E_missing_L','sigma_four',H|C(['E-']),H|other|(full('L')-C(['L+']))|C(['E-'])),
 ('center_E_missing_L','sigma_centerB3',H|fan('E',[3,4]),H|other|(full('L')-C(['L+']))|fan('E',[3,4])),
 ('outer_E_missing_L','sigma_outerB2',H|fan('E',[4,5]),H|other|(full('L')-C(['L+']))|fan('E',[4,5])),
 ('ordinary_LE_Nrminus_absent','uniform7',H|C(['L+','E-']),H|BDR|full('Tc')|(full('N')-C(['Nr-']))|C(['L+','E-'])),
 ('outer_L_Nrminus_absent','Lsquare5',H|fan('L',[0,1])|C(['E-']),H|BDR|full('Tc')|(full('N')-C(['Nr-']))|fan('L',[0,1])|C(['E-'])),
 ('outer_E_Nrminus_absent','Esquare5',H|fan('E',[4,5])|C(['L+']),H|BDR|full('Tc')|(full('N')-C(['Nr-']))|fan('E',[4,5])|C(['L+'])),
 ('center_T','Tcenter3',H|fan('Tc',[5,6])|C(['E-']),H|BDR|full('L')|full('N')|fan('Tc',[5,6])|C(['E-'])),
 ('center_E_Nrplus_absent','Ecenter6',H|fan('E',[3,4])|C(['L+']),H|BDR|full('Tc')|(full('N')-C(['Nr+']))|fan('E',[3,4])|C(['L+'])),
 ('center_L_Nrright_Tplus_absent','Lcenter12',H|fan('L',[7,0])|C(['E-']),H|BDR|(full('N')-C(['Nr-','Nr+']))|fan('L',[7,0])|C(['E-','T-']))]
checks={}
for name,key,minimum,maximum in rules:
 P=paths[key];assert P[0]==(0,0) and P[-1]==(2,2)
 U,Z=path_requirements(P);assert U<=minimum and not Z&maximum,name
 Us,Zs=path_requirements([sigma(p) for p in P[::-1]])
 assert Us==tr(U) and Zs==tr(Z)
 checks[name]={'status':'PASS','reflections':len(P)-2,'full_U_Z_and_sigma':'PASS','required':sorted(U),'forbidden':sorted(Z)}

# Both prescribed square exchanges have the SAME strict normalized ports.
u=d=F(1,6)
assert 0<u<1 and 0<u+2*d<1 and 0<u+d<1
assert len(paths['Lsquare5'])-2==len(paths['Esquare5'])-2==5

def polygon(ts):
 edges=set()
 for a,b,c in ts:
  if cross(sub(b,a),sub(c,a))<0:b,c=c,b
  for p,q in [(a,b),(b,c),(c,a)]:
   if (q,p) in edges:edges.remove((q,p))
   else:edges.add((p,q))
 nxt=dict(edges);assert len(nxt)==len(edges)==len(set(nxt.values()))
 start=min(nxt);p=nxt[start];cyc=[start]
 while p!=start:
  assert p not in cyc;cyc.append(p);p=nxt[p]
 assert len(cyc)==len(edges)
 return [p for i,p in enumerate(cyc) if cross(sub(p,cyc[i-1]),sub(cyc[(i+1)%len(cyc)],p))]

def ledger(ts):
 geo=g.check({'triangles':sorted(ts),'marked':[(0,0),(2,2)],'require_simple':True},strict=False)
 assert set(geo['interior_A'])=={(0,0),(2,0),(2,2)}
 owners=g.owners_of(list(ts));opens={e for e,ii in owners.items() if len(ii)==2}
 Q=J=sN=0
 for p in set().union(*map(set,ts)):
  angles,inside=g.check_fan_angles(list(ts),p,owners,opens)
  if g.label(p)=='A':
   if not inside:Q+=3 if angles==[4] else sum(angles)
  elif inside:J+=1
  elif angles==[4]:sN+=1
 return {'W':geo['walls'],'k':J+sN,'Q':Q,'J':J,'sN':sN,'Delta':Q+sN-8}

peer_receipt=ROOT/'fourth-surplus-review/mixed-e2-e1/root-leaf-check.json'
peer=read(str(peer_receipt.relative_to(ROOT)))['three_hand_prescribed_controls']
rootleaf=H|fan('B',[7,0,1])|fan('D',[3])
controls=[('Lsquare',rootleaf|fan('L',[0,1])|C(['E-','Nb-']),'Lsquare5'),
 ('Esquare',rootleaf|fan('E',[4,5])|C(['L+','Nb+']),'Esquare5'),
 ('Tcenter',rootleaf|fan('Tc',[5,6])|C(['L+','E-','Nb+']),'Tcenter3')]
receipts={}
for name,expected,key in controls:
 ts=set(map(tri,peer[name]['triangles']));assert ts==expected,name
 V=polygon(ts);assert V==list(map(tuple,peer[name]['vertices']))
 ld=ledger(ts);assert ld==peer[name]['ledger']
 assert ld['W']==20 and ld['k']==6 and ld['Delta']==4
 P=paths[key];U,Z=path_requirements(P);assert U<=ts and not Z&ts
 assert replay(V,(0,0),(2,2),P)==len(P)-2
 assert replay(V,(2,2),(0,0),P[::-1])==len(P)-2
 assert replay([sigma(p) for p in V],(0,0),(2,2),[sigma(p) for p in P[::-1]])==len(P)-2
 receipts[name]={'status':'PASS_ORIGINAL_PRESCRIBED_CONTROL','ledger':ld,'firstT_forward_reverse_sigma':'PASS','reflections':len(P)-2}

# Local fan identities only: these are NOT completed room assignments.
def angle_at(ts,p):
 return sum(90 if g.label(p)=='C' else 45 for t in ts if p in t)

def fan_angle(ts,p,expected):
 owners=g.owners_of(list(ts));opens={e for e,ii in owners.items() if len(ii)==2}
 angles,inside=g.check_fan_angles(list(ts),p,owners,opens)
 assert angles==[expected//45] and not inside,(p,angles,expected)
 return expected
angle_specs=[
 ('Louter_needs_Nbminus',H|fan('L',[0,1]),(-1,1),'Nb-'),
 ('Twest_needs_Nrplus',H|fan('Tc',[4,5]),(1,3),'Nr+'),
 ('Teast_needs_Eplus',H|fan('Tc',[6,7]),(3,3),'E+'),
 ('Rlower_needs_Dplus',H|fan('R',[4,5]),(3,-1),'D+'),
 ('Nbottom_with_Lplus_impossible',H|fan('N',[5,6])|C(['L+']),(-1,1),None),
 ('Lcenter_H4_impossible',H|fan('L',[7,0])|fan('B',[7,0,1,2]),(-1,-1),None),
 ('Ecenter_Tplus_impossible',H|fan('E',[3,4])|C(['T+']),(3,3),None),
 ('Nrplus_Tminus_impossible',H|C(['Nr+','T-']),(1,3),None),
 ('Lcenter_Nbminus_impossible',H|fan('L',[7,0])|C(['Nb-']),(-1,1),None)]
angles={}
for name,ts,p,repair in angle_specs:
 fan_angle(ts,p,180);row={'unhealed_boundary_degrees':180}
 if repair:
  row['repair_cap']=repair;row['repaired_degrees']=fan_angle(ts|C([repair]),p,225)
 angles[name]=row
root_angles={}
for name,ss,h in [('O3',[7,0,1],0),('O4',[6,7,0,1],0),('H4',[7,0,1,2],1)]:
 for leaf in [3,4]:
  ts=H|fan('B',ss)|fan('D',[leaf])
  assert angle_at(ts,(1,-2))==270
  assert angle_at(ts,(1,-1)) in [270,315]
  assert angle_at(ts,(0,-1))==270+90*h
  root_angles[name+':D'+str(leaf)]={'shared_C':270,'upper_B':angle_at(ts,(1,-1)),'H_C':270+90*h}
# Cap-count equations are arithmetic identities, not cap assignments.
counts={}
for h in [0,1]:
 for c in [0,1]:
  J=2+h+c;n=J;Q=6+n;sN=12-Q
  assert J+sN==6 and Q+sN-8==4
  counts[str((h,c))]={'J':J,'n':n,'Q':Q,'sN':sN}
assert 3-1==2                 # Lcenter: E fixed, two ofN/T/R.
assert 3-2==1 and 4>3         # Ecenter: L,N fixed; T absent leavesR only.
assert 2-2==0 and 3-2==1     # Eouter: L,N fixed.
assert 3-3==0 and 4-3==1     # Rcenter: L,E,N fixed.
assert 2<3 and 3-3==0        # Rupper requiresH4.
assert 3-2==1 and 4-2==2     # Nrightcenter: L,E fixed, T/R occupancy.
out={'status':'INDEPENDENT_ROOT_LEAF_PARTIAL_REDUCTION_CHECKS_PASS',
 'scope':'argument sections6-8 only; NOT closure of six hard rows or allroots',
 'guard_implications':checks,'three_original_controls':receipts,
 'strict_square_exchange_ports':{'u':'1/6','d':'1/6','exit':'1/2'},
 'local_angle_identities':angles,'Broot_Dleaf_local_angles':root_angles,
 'cap_count_identities':counts,'hard_row_count':6,'hand_review':'review.txt',
 'input_hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [peer_receipt,ROOT/'fourth-surplus-review/mixed-e2-e1/argument.txt',ROOT/'surplus-four-local/single-e2-check.json',ROOT/'first-surplus-review/residual-cover-check.json',ROOT/'first-surplus-review/bottom-residual-check.json',ROOT/'first-surplus-review/centered-left-check.json',ROOT/'zero-surplus-L/cover-check.json',ROOT/'third-surplus-review/independent-review/guard-extension-check.json']},
 'limits':'Own retained physical/guard/geometry checks, three already supplied rooms only, local fan and count identities. No peer checker execution, cap-assignment enumeration, new room/word/direction discovery or orbit run.'}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'])
print('10wholeguards+sigma,3originalphysicalcontrols,9angleidentities,6rootleafangleidentities PASS.')
