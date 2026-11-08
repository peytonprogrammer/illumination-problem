"""Independent audit of named paths, angle coefficients and supplied residues.
No cap assignments, room/direction/word discovery, or source archives.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict, Counter
import hashlib, json, runpy

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
files={
 'proof':ROOT/'surplus-four-local/single-e2.txt',
 'cover':ROOT/'surplus-four-local/single-e2-check.json',
 'returns':ROOT/'surplus-four-local/left-return-check.json',
 'angles':ROOT/'surplus-four-local/single-e2-charge.json',
 'caps':ROOT/'zero-surplus-L/guard-incidence-check.json',
 'project':ROOT/'third-surplus-review/local-e2-project.json',
 'guard':ROOT/'lower-bound-proof-audit/full-replay/guard-checker.py',
}
d={k:json.loads(p.read_text()) for k,p in files.items() if p.suffix=='.json'}
guard=runpy.run_path(str(files['guard']))
tri=lambda t:tuple(sorted(map(tuple,t)))
T=lambda ts:{tri(t) for t in ts}
decode=lambda P:[tuple(F(*c) for c in p) for p in P]
sub=lambda a,b:(a[0]-b[0],a[1]-b[1])
cross=lambda a,b:a[0]*b[1]-a[1]*b[0]
dot=lambda a,b:a[0]*b[0]+a[1]*b[1]
D=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]

def fan(c,start,m):
 return {tri((c,(c[0]+D[i%8][0],c[1]+D[i%8][1]),
                 (c[0]+D[(i+1)%8][0],c[1]+D[(i+1)%8][1]))) for i in range(start,start+m)}

H=set().union(*(fan(c,0,8) for c in [(0,0),(2,0),(2,2)]))
caps={n:tri(t) for n,t in d['caps']['cap_options'].items()}
allcaps=set(caps.values())
sigma=lambda p:(2-p[1],2-p[0])
transform=lambda ts:{tri(sigma(p) for p in t) for t in ts}

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

# Compare independent parity-angle coefficients for the fourteen hand-listed roots.
angles={}
for site,c,starts in [('L',(-2,0),{3:[6,7,0],4:[5,6,7,0]}),('B',(0,-2),{3:[7,0,1],4:[6,7,0,1]})]:
 for m,ss in starts.items():
  for st in ss:
   key=f'{site}_m{m}_start{st}';row=d['angles']['families'][key]
   forced=['B+','E-','T-'] if site=='L' else ['L+','E-']
   fixed=H|fan(c,st,m)|{caps[n] for n in forced}
   occupied_slots={n[0] for n in forced}|{site}
   variables={n:t for n,t in caps.items() if n[0] not in occupied_slots}
   assert fixed==T(row['fixed_triangles'])
   assert variables=={n:tri(t) for n,t in row['variable_caps'].items()}
   points=set().union(*map(set,fixed|set(variables.values())))
   J=sum(sum(angle(t,p) for t in fixed)==8 for p in points if p[0]%2 or p[1]%2)
   assert J==row['J'] and row['ordinary_count_required_at_k6_Delta4']==J+3
   Bs=[];Cs=[]
   for p in sorted(points):
    base=sum(angle(t,p) for t in fixed)
    terms={n:angle(t,p) for n,t in variables.items() if p in t}
    if p[0]%2!=p[1]%2 and base==4 and {t for t in fixed if p in t}!={t for t in H if p in t}:Cs.append(list(p))
    if p[0]%2==p[1]%2==1 and base<=4 and base+sum(terms.values())>=4:
     Bs.append(dict(point=list(p),fixed_angle_45=base,variable_angles_45=terms,smooth_when_sum=4-base))
   assert Cs==row['outside_smooth_C'] and Bs==row['potential_smooth_B']
   angles[key]=dict(status='MATCH',J=J,n=J+3)

new={};pathspec={'short_square_flat':(7,3,False),'wide_rectangle_Ncap':(0,4,True),'trapezoid_Ncap':(0,3,True)}
for name,(st,m,N) in pathspec.items():
 row=d['returns']['paths'][name];P=[tuple(map(F,p)) for p in row['path']]
 assert P[0]==(0,0) and P[-1]==(2,2)
 U,Z=guard['path_requirements'](P)
 assert U==T(row['required']) and Z==T(row['forbidden'])
 fixed=H|fan((-2,0),st,m)|{caps['E-']}|({caps['Nr-']} if N else set())
 absent={'E+','Nb-','Nb+','Nr+'} if N else {'E+','Nr-'}
 possible=H|fan((-2,0),st,m)|{t for n,t in caps.items() if not n.startswith('L') and n not in absent}
 assert U<=fixed and not Z&possible
 room=T(row['fixture']['triangles']);V=[tuple(map(F,p)) for p in polygon(room)]
 assert U<=room and not Z&room
 physical(P,V);physical(P[::-1],V)
 Ps=[sigma(p) for p in reversed(P)]
 physical(Ps,[sigma(p) for p in V]);Us,Zs=guard['path_requirements'](Ps)
 assert Us==transform(U) and Zs==transform(Z)
 for es,em in ([(6,4)] if name=='short_square_flat' else [(7,4)] if name=='trapezoid_Ncap' else []):
  assert U<=H|fan((-2,0),es,em)|{caps['E-']}|({caps['Nr-']} if N else set()) and not Z&fan((-2,0),es,em)
 new[name]=dict(status='PASS',reflections=len(P)-2,physical_forward_reverse_sigma='PASS')

# Named old terms only: no source archive, no broad selection or new path.
def term(family,line,requires=None):
 rows=[r for r in d['project']['families'][family]['terms'] if r['source_line']==line and (requires is None or r['requires']==requires)]
 assert len(rows)==1;return decode(rows[0]['path'])
bindings={
 'B515':('B_outer3',515,None),'B2551':('B_outer3',2551,None),
 'Lupper14':('L_Hupper3_Nrminus',3580,None),
 'Lfull528':('L_Hupper4_Nbminus',528,None),'Lfull529':('L_Hupper4_Nbminus',529,None),'Lfull652':('L_Hupper4_Nbminus',652,None),
 'Louter2635':('L_outer4_Nbminus',2635,None),'Louter3866':('L_outer4_Nbminus',3866,None),
 'Louter361D':('L_outer4_Nbminus',361,['D-']),'Louter361R':('L_outer4_Nbminus',361,['R+']),
 'Louter3224':('L_outer4_Nbminus',3224,None),
}
roots={'Bouter3':((0,-2),7,3),'BHeast4':((0,-2),7,4),'Bfullwest':((0,-2),1,4),'Lrectangle':((-2,0),6,4),'Lfullnorth':((-2,0),7,4),'Louter3':((-2,0),0,3),'Louter4':((-2,0),0,4)}
old={}
for name,row in d['cover']['named_implications'].items():
 c,st,m=roots[name.split('_')[0]];P=term(*bindings[row['path']]);U,Z=guard['path_requirements'](P)
 fixed=H|fan(c,st,m)|{caps[n] for n in row['present']}
 possible=(H|fan(c,st,m)|allcaps)-{caps[n] for n in row['absent']}
 assert U<=fixed and not Z&possible,(name,U-fixed,Z&possible)
 old[name]='PASS'
assert len(old)==23

residues={}
for name,row in d['cover']['residues'].items():
 room=T(row['triangles']);ll=ledger(room)
 assert ll==row['ledger'] and (ll['W'],ll['k'],ll['Delta'])==(20,6,4)
 if 'selected_path' in row:
  P=[tuple(map(F,p)) for p in d['returns']['paths'][row['selected_path']]['path']]
  U,Z=guard['path_requirements'](P);assert U<=room and not Z&room
 residues[name]=dict(status=row['status'],ledger=ll)
remaining=sorted(n for n,r in residues.items() if r['status']=='VALID_GEOMETRY_NOT_DARKNESS')
assert remaining==sorted(d['cover']['remaining_exact_cases']) and len(remaining)==7

universal={}
for name,row in d['cover']['universal_lemmas'].items():
 P=[tuple(map(F,p)) for p in row['path']];U,Z=guard['path_requirements'](P)
 assert U==T(row['required']) and Z==T(row['forbidden'])
 if name=='uniform_seven':
  assert U<=H|{caps['L+'],caps['E-']}
  expected={caps['L-'],caps['E+'],caps['Nr-'],tri(((-2,0),(-2,1),(-1,1))),tri(((4,2),(4,1),(3,1)))}
  assert Z==expected
 else:assert U<=H|fan((0,-2),6,4) and not Z&(H|fan((0,-2),6,4)|allcaps-{caps['B-']})
 universal[name]=dict(status='PASS',reflections=len(P)-2)

result=dict(status='PASS',scope='Independent hand reduction audit supported by fourteen symbolic angle tables, three supplied return paths plus two extensions, two universal lemmas,23 named retained implications,16 prescribed residue ledgers. No assignments or discovery.',angles=angles,new_returns=new,universal=universal,named_old=old,residues=residues,remaining=remaining,
 inputs={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files.values()})
(HERE/'check.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS: angle coefficients, 3 new paths and sigma/reverse,23 named guards,16 fixed residues; seven remain in reviewed reduction')
