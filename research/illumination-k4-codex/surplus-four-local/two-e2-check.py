"""Hand-stated two-e2 implications and eleven named candidate fixtures.
No cap-assignment enumeration or optical discovery. Does not prove completeness.
"""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
sys.path.insert(0,str(ROOT/'triangle-composition/inputs'))
import illumination_geometry as g
from guard_checker import path_requirements,cross,sub
from boundary_replay import replay
tri=lambda t:tuple(sorted(map(tuple,t)))
D=g.DIRS
centers={'L':(-2,0),'B':(0,-2),'D':(2,-2),'R':(4,0),'E':(4,2),'T':(2,4),'N':(0,2)}
def fan(c,st,m):
 return {tri((c,(c[0]+D[i%8][0],c[1]+D[i%8][1]),(c[0]+D[(i+1)%8][0],c[1]+D[(i+1)%8][1]))) for i in range(st,st+m)}
f=lambda lab,st,m:fan(centers[lab],st,m)
H=set().union(*(fan(c,0,8) for c in [(0,0),(2,0),(2,2)]))
caps={n:tri(t) for n,t in json.loads((ROOT/'triangle-composition/inputs/caps.json').read_text())['cap_options'].items()}
C=lambda names:{caps[n] for n in names}
allcaps=set(caps.values());DR=f('D',0,8)|f('R',0,8)
dec=lambda p:[tuple(F(*v) for v in q) for q in p]
read=lambda rel:json.loads((ROOT/rel).read_text())
sq=read('first-surplus-review/square-exchange-check.json')['paths']
paths={'L11':dec(sq['L_thirteen']['path']),'five':dec(read('second-surplus-review/five-path-check.json')['five_path'])}
old=read('zero-surplus-L/cover-check.json')['paths']
paths['thirteen']=dec(old['thirteen']['path']);paths['sigma13']=dec(old['thirteen_sigma']['path'])
sigma=lambda p:(2-p[1],2-p[0])
paths['sigmafive']=[sigma(p) for p in paths['five']][::-1]
proj=read('third-surplus-review/local-mixed-project.json')['families']
for name,fam,line in [('Bwest12','Bwest_Lcenter',664),('joined515','BDjoin_Bouter3',515),('joined2551','BDjoin_Bouter3',2551),('joined165','BDjoin_BHeast4',165)]:
 rows=[t for t in proj[fam]['terms'] if t['source_line']==line];assert len(rows)==1
 paths[name]=dec(rows[0]['path'])
paths['uniform7']=[tuple(map(F,q)) for q in read('surplus-four-local/single-e2-check.json')['universal_lemmas']['uniform_seven']['path']]
paths['square_square3']=[(F(0),F(0)),(F(-2),F(1,3)),(F(4),F(4,3)),(F(1),F(11,6)),(F(2),F(2))]
# Every case is a prescribed symbolic implication: U<=fixed, Z disjoint possible.
cases=[]
def add(name,which,fixed,possible):cases.append((name,which,H|fixed,H|fixed|possible))
# Bwest/rectangle path is unchanged by ANY L/D/R/N/T triangle permitted here.
add('Bwest_or_rectangle_full_L_support','Bwest12',f('B',1,3)|C(['E-']),f('B',0,4)|f('L',0,8)|DR|f('N',0,8)|f('T',0,8)|C(['E-']))
# Both L-upper and L-rectangle: all other B/D/R triangles are harmless.
for name,st,m in [('Lupper',7,3),('Lrectangle',6,4)]:
 add(name+'_L11_full_B_DR_bottom_N','L11',f('L',st,m)|C(['E-']),f('B',0,8)|DR|f('N',1,6)|C(['E-','T-']))
# The named five-path has no forbidden D/R/E/L triangles in these supports.
add('B_east_five_full_DR','five',f('B',0,3)|C(['T-']),DR|f('E',0,8)|f('L',0,8)|C(['T-','Nb-','Nr-','Nr+']))
add('B_east_bottom_N_sigma13','sigma13',f('B',0,3)|C(['L+','E-']),DR|f('N',1,6)|C(['L+','E-','T-']))
# No-critical pairs: ordinary reference caps and only one inward N side.
add('noncritical_bottom_N_sigma13','sigma13',C(['L+','E-']),DR|f('N',1,6)|C(['L+','E-','B+','T-']))
add('noncritical_right_N_thirteen','thirteen',C(['B+','T-']),DR|f('N',7,6)|C(['L+','E-','B+','T-']))
add('B_E_east_bottom_N_sigmafive','sigmafive',f('B',0,3)|f('E',3,3)|C(['L+']),DR|f('N',1,6)|C(['L+','T-']))
add('Lupper_Eeast_square_square3','square_square3',f('L',7,3)|f('E',3,3),DR|C(['B+','T-','Nb-']))
# Joined roots or root/leaf: broad full-D guards, no ordinary assignment scan.
Bunion=f('B',6,5)
add('joined_N_not_Nrminus_uniform7','uniform7',C(['L+','E-']),f('B',0,8)|DR|f('T',0,8)|C(['L+','E-','Nb-','Nb+','Nr+']))
add('joined_Rplus_absent_515','joined515',f('B',7,3)|C(['L+','E-','Nr-']),Bunion|f('D',0,8)|C(['L+','E-','Nr-','R-','T-','T+']))
add('joined_Heast_Rplus_Tplus_absent_165','joined165',f('B',7,4)|C(['R+','Nr-']),f('D',0,8)|C(['L+','E-','Nr-','R+','T-']))
add('joined_Dplus_Tminus_absent_2551','joined2551',f('B',7,3)|C(['R+','E-','Nr-']),Bunion|(f('D',0,8)-C(['D+']))|C(['L+','E-','Nr-','R+','T+']))
checks={}
for name,which,fixed,possible in cases:
 U,Z=path_requirements(paths[which]);assert U<=fixed and not Z&possible,(name,'missing',U-fixed,'conflict',Z&possible)
 Ps=[sigma(p) for p in paths[which]][::-1];Us,Zs=path_requirements(Ps)
 transform=lambda ts:{tri(sigma(p) for p in t) for t in ts}
 assert Us==transform(U) and Zs==transform(Z)
 checks[name]={'status':'PASS','path':which,'reflections':len(paths[which])-2,'fixed':sorted(fixed),'possible':sorted(possible),'required':sorted(U),'forbidden':sorted(Z)}
 print(name,'full symbolic guard PASS')

def polygon(ts):
 edges=set()
 for a,b,c in ts:
  if cross(sub(b,a),sub(c,a))<0:b,c=c,b
  for u,v in [(a,b),(b,c),(c,a)]:
   if (v,u) in edges:edges.remove((v,u))
   else:edges.add((u,v))
 out={a:b for a,b in edges};assert len(out)==len(edges)
 start=min(out);p=start;cyc=[]
 while True:
  assert p not in cyc;cyc.append(p);p=out[p]
  if p==start:break
 assert len(cyc)==len(edges)
 return [p for i,p in enumerate(cyc) if cross(sub(p,cyc[i-1]),sub(cyc[(i+1)%len(cyc)],p))]
def ledger(ts):
 data=g.check({'triangles':sorted(ts),'marked':[(0,0),(2,2)],'require_simple':True},strict=False)
 assert set(data['interior_A'])=={(0,0),(2,0),(2,2)}
 os=g.owners_of(list(ts));opens={e for e,ls in os.items() if len(ls)==2};Q=J=sN=0
 for p in set().union(*map(set,ts)):
  a,full=g.check_fan_angles(list(ts),p,os,opens)
  if g.label(p)=='A':
   if not full:Q+=3 if a==[4] else sum(a)
  elif full:J+=1
  elif a==[4]:sN+=1
 return {'W':data['walls'],'k':len(data['transparent_vertices']),'Q':Q,'J':J,'sN':sN,'Delta':Q+sN-8}
# Exactly ELEVEN hand-forced candidate fixtures, not generated cap assignments.
specs=[
 ('Llower_Beast_Nbplus_Dminus',[('L',6,3),('B',0,3)],['E-','T-','Nb+','D-']),
 ('Llower_Beast_Nbplus_Dplus',[('L',6,3),('B',0,3)],['E-','T-','Nb+','D+']),
 ('Llower_Beast_Nbplus_Rminus',[('L',6,3),('B',0,3)],['E-','T-','Nb+','R-']),
 ('Llower_Beast_Nbplus_Rplus',[('L',6,3),('B',0,3)],['E-','T-','Nb+','R+']),
 ('Bouter3_Dhalf3_Rplus_Tempty',[('B',7,3),('D',1,3)],['L+','E-','Nr-','R+']),
 ('Bouter4_Dhalf3_Rplus_Tempty',[('B',6,4),('D',1,3)],['L+','E-','Nr-','R+']),
 ('Bouter3_Dfullwest4_Rplus_Tminus',[('B',7,3),('D',1,4)],['L+','E-','Nr-','R+','T-']),
 ('Bouter3_Dfullwest4_Rplus_Tplus',[('B',7,3),('D',1,4)],['L+','E-','Nr-','R+','T+']),
 ('Bouter4_Dfullwest4_Rplus_Tminus',[('B',6,4),('D',1,4)],['L+','E-','Nr-','R+','T-']),
 ('Bouter4_Dfullwest4_Rplus_Tplus',[('B',6,4),('D',1,4)],['L+','E-','Nr-','R+','T+']),
 ('BHeast4_Dhalf3_Rplus_Tplus',[('B',7,4),('D',1,3)],['L+','E-','Nr-','R+','T+']),
]
fixtures={}
for name,fs,cs in specs:
 ts=H|C(cs)|set().union(*(f(*v) for v in fs));ll=ledger(ts)
 assert ll['W']==20 and ll['k']==6 and ll['Delta']==4,(name,ll)
 fixtures[name]={'status':'VALID_GEOMETRY_NOT_DARKNESS','fans':fs,'caps':cs,'ledger':ll,'triangles':sorted(ts),'vertices':polygon(ts)}
 print(name,'prescribed geometry PASS')
# One prescribed physical control for the new three-contact square composition.
ts=H|f('L',7,3)|f('E',3,3)|C(['B+','T-','Nb-','D-'])
ll=ledger(ts);V=polygon(ts);P=paths['square_square3']
assert replay(V,(0,0),(2,2),P)==3 and replay(V,(2,2),(0,0),P[::-1])==3
assert replay([sigma(p) for p in V],(0,0),(2,2),[sigma(p) for p in P][::-1])==3
# Hand-listed root/leaf angle identities. No cap choices or polygons generated.
leaf_tables={}
for name,bst,bm,dst,expect in [
 ('Bouter3_Dcenter',7,3,3,3),('Bouter4_Dcenter',6,4,3,3),
 ('BHeast4_Dcenter',7,4,3,4),('Bouter3_Dquarter',7,3,4,2),
 ('BHeast4_Dquarter',7,4,4,3)]:
 fixed=H|f('B',bst,bm)|f('D',dst,2)
 pts=set().union(*map(set,fixed))
 J=sum(sum(len(g.wedge_slots(t,p)) for t in fixed if p in t)==8 for p in pts if g.label(p)!='A')
 assert J==expect,(name,J,expect)
 leaf_tables[name]={'J':J,'Q':'5+n','ordinary_caps_at_k6_Delta4':J+1}
# One prescribed full leaf control exercising the corrected n=J+1 equation.
leaf=H|f('B',7,4)|f('D',3,2)|C(['L+','E-','Nr-','R+','T-'])
leaf_ledger=ledger(leaf);assert leaf_ledger=={'W':20,'k':6,'Q':10,'J':4,'sN':2,'Delta':4}
LP=paths['joined165'];U,Z=path_requirements(LP);assert U<=leaf and not Z&leaf
LV=polygon(leaf);assert replay(LV,(0,0),(2,2),LP)==18
assert replay(LV,(2,2),(0,0),LP[::-1])==18
sources=['first-surplus-review/square-exchange-check.json','second-surplus-review/five-path-check.json','zero-surplus-L/cover-check.json','third-surplus-review/local-mixed-project.json','surplus-four-local/single-e2-check.json']
out={'status':'PARTIAL_TWO_E2_COVER','symbolic_guard_count':len(checks),'named_implications':checks,'hand_prescribed_fixtures':fixtures,'new_three_path':{'path':[[str(v) for v in q] for q in P],'actual_boundary_forward_reverse_sigma':'PASS','control_ledger':ll},'root_leaf_angle_tables':leaf_tables,'corrected_leaf_budget_control':{'ledger':leaf_ledger,'actual_boundary_forward_reverse':'PASS','path':'joined165','reflections':18},'scope':'Thirteen hand-stated whole-guard implications, eleven explicitly prescribed candidate geometries, one prescribed new three-path control. Completeness is not established by receipt counts; four additional symbolic B/E families retained. No cap-assignment/room/direction/word discovery scan.','source_hashes':{s:hashlib.sha256((ROOT/s).read_bytes()).hexdigest() for s in sources}}
(HERE/'two-e2-check.json').write_text(json.dumps(out,indent=2)+'\n')
