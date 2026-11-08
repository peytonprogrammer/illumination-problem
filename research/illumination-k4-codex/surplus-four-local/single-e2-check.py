"""Named symbolic guard implications and sixteen hand-forced geometry checks."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
sys.path.insert(0,str(ROOT/'triangle-composition/inputs'))
from guard_checker import path_requirements,cross,sub
from boundary_replay import replay
import illumination_geometry as g
tri=lambda t:tuple(sorted(map(tuple,t)))
D=g.DIRS
def fan(c,st,m):return {tri((c,(c[0]+D[i%8][0],c[1]+D[i%8][1]),(c[0]+D[(i+1)%8][0],c[1]+D[(i+1)%8][1]))) for i in range(st,st+m)}
H=set().union(*(fan(c,0,8) for c in [(0,0),(2,0),(2,2)]))
caps={n:tri(t) for n,t in json.loads((ROOT/'triangle-composition/inputs/caps.json').read_text())['cap_options'].items()}
allcaps=set(caps.values());decode=lambda p:[tuple(F(*v) for v in q) for q in p]
proj=json.loads((ROOT/'third-surplus-review/local-e2-project.json').read_text())['families']
res=json.loads((ROOT/'third-surplus-review/local-e2-residue-frozen.json').read_text())['hits']
def term(fam,line):
 rows=[v for v in proj[fam]['terms'] if v['source_line']==line]
 assert len(rows)==1,(fam,line)
 return decode(rows[0]['path'])
P7=decode(res['B_outer3_Dplus_Rplus_Tplus']['path'])
P3=decode(res['B_outer4_Nrminus_Rplus_Tminus']['path'])
U7,Z7=path_requirements(P7);U3,Z3=path_requirements(P3)
assert U7==H.intersection(U7)|{caps['L+'],caps['E-']}
assert not Z7&H
assert sorted(n for n,t in caps.items() if t in Z7)==['E+','L-','Nr-']
outerL=tri(((-2,0),(-2,1),(-1,1)))
outerE=tri(((4,2),(4,1),(3,1)))
assert Z7=={caps['L-'],caps['E+'],caps['Nr-'],outerL,outerE}
assert U3<=H|fan((0,-2),6,4) and not Z3&(H|fan((0,-2),6,4)|allcaps-{caps['B-']})
# Full B/D/R/T stars may be changed arbitrarily under the seven-path guard.
assert not Z7&set().union(*(fan(c,0,8) for c in [(0,-2),(2,-2),(4,0),(2,4)]))
paths={'uniform_seven':P7,'rectangle_three':P3}
for label,path in [('Lsquare11',decode(json.loads((ROOT/'first-surplus-review/square-exchange-check.json').read_text())['paths']['L_thirteen']['path']))]:paths[label]=path
paths['Lupper14']=term('L_Hupper3_Nrminus',3580)
paths['Bwest12']=term('B_Hwest3',664)
paths['Brectangle12']=term('B_rectangle4',664)
paths['B515']=term('B_outer3',515)
paths['B2551']=term('B_outer3',2551)
for line in [528,529,652]:paths[f'Lfull{line}']=term('L_Hupper4_Nbminus',line)
for line in [2635,3866]:paths[f'Louter{line}']=term('L_outer4_Nbminus',line)
# D-/R+ and isolated D- use the D-required line361, not the distinct R+ term.
for t in proj['L_outer4_Nbminus']['terms']:
 if t['source_line']==361:
  paths['Louter361D' if t['requires']==['D-'] else 'Louter361R']=decode(t['path'])
paths['Louter3224']=term('L_outer4_Nbminus',3224)
# Each tuple is a hand-written symbolic implication, with remaining caps free.
branches={
 'Bouter3_Nrminus':('B515',(0,-2),7,3,['L+','E-','Nr-','D+','R-'],['L-','E+','Nb-','Nb+','Nr+','R+','D-','T-','T+']),
 'BHeast4_Nrminus':('B515',(0,-2),7,4,['L+','E-','Nr-','D+','R-'],['L-','E+','Nb-','Nb+','Nr+','R+','D-']),
 'Bfullwest_Nrminus_Rminus':('B515',(0,-2),1,4,['L+','E-','Nr-','D-','R-'],['L-','E+','Nb-','Nb+','Nr+','R+','D+']),
 'Bfullwest_Nrminus_Rplus_Dminus_Tplus':('B2551',(0,-2),1,4,['L+','E-','Nr-','D-','R+','T+'],['L-','E+','Nb-','Nb+','Nr+','R-','D+','T-']),
 'Lrectangle_Nrminus':('Lupper14',(-2,0),6,4,['B+','E-','T-','Nr-'],['B-','E+','T+','Nb-','Nb+','Nr+']),
 'Lfullnorth_Nbminus':('Lfull528',(-2,0),7,4,['B+','E-','T-','Nb-','D+','R-'],['B-','E+','T+','Nb+','Nr-','Nr+','D-','R+']),
 'Lfullnorth_Nbplus_Rminus':('Lfull528',(-2,0),7,4,['B+','E-','T-','Nb+','D-','R-'],['B-','E+','T+','Nb-','Nr-','Nr+','D+','R+']),
 'Lfullnorth_Nbplus_Rplus':('Lfull652',(-2,0),7,4,['B+','E-','T-','Nb+','R+'],['B-','E+','T+','Nb-','Nr-','Nr+','R-']),
 'Lfullnorth_Nrminus_Rminus':('Lfull529',(-2,0),7,4,['B+','E-','T-','Nr-','D-','R-'],['B-','E+','T+','Nb-','Nb+','Nr+','D+','R+']),
}
# The same four stated implications for each of the two outward L fans.
for name,st,m in [('Louter3',0,3),('Louter4',0,4)]:
 for suffix,which,present,absent in [
  ('Nempty_Dminus_Rminus','Louter2635',['D-','R-'],['D+','R+','Nb-','Nb+','Nr-','Nr+']),
  ('Nempty_Dminus_Rplus','Louter361D',['D-','R+'],['D+','R-','Nb-','Nb+','Nr-','Nr+']),
  ('Nempty_Dplus_Rplus','Louter3866',['D+','R+'],['D-','R-','Nb-','Nb+','Nr-','Nr+']),
  ('Nbplus_Dplus','Louter3224',['Nb+','D+'],['D-','R-','R+','Nb-','Nr-','Nr+']),
  ('Nbplus_Rplus','Louter361R',['Nb+','R+'],['D-','D+','R-','Nb-','Nr-','Nr+']),
  ('Nrminus_Dminus','Louter361D',['Nr-','D-'],['D+','R-','R+','Nb-','Nb+','Nr+']),
  ('Nrminus_Dplus','Louter3224',['Nr-','D+'],['D-','R-','R+','Nb-','Nb+','Nr+'])]:
  branches[name+'_'+suffix]=(which,(-2,0),st,m,['B+','E-','T-']+present,['L-','B-','E+','T+']+absent)
receipts={}
for name,(which,c,st,m,present,absent) in branches.items():
 fixed=H|fan(c,st,m)|{caps[n] for n in present}
 possible=(H|fan(c,st,m)|allcaps)-{caps[n] for n in absent}
 u,z=path_requirements(paths[which])
 assert u<=fixed and not z&possible,(name,'missing',u-fixed,'conflict',z&possible)
 receipts[name]={'status':'PASS','path':which,'reflections':len(paths[which])-2,'present':present,'absent':absent}

def polygon(ts):
 edges=set()
 for t in ts:
  a,b,c=t
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
 os=g.owners_of(list(ts));opens={e for e,ls in os.items() if len(ls)==2}
 Q=J=sN=0
 for p in set().union(*map(set,ts)):
  a,full=g.check_fan_angles(list(ts),p,os,opens)
  if g.label(p)=='A':
   if not full:Q+=3 if a==[4] else sum(a)
  elif full:J+=1
  elif a==[4]:sN+=1
 return {'W':data['walls'],'k':len(data['transparent_vertices']),'Q':Q,'J':J,'sN':sN,'Delta':Q+sN-8}

# The following sixteen rooms are the exact residues forced by the hand proof.
# They are explicitly named, with no generation of cap choices.
residue_specs=[
 ('Lupper_Nrplus_Dminus_Rminus',(-2,0),7,3,['B+','E-','T-','Nr+','D-','R-']),
 ('Lupper_Nrplus_Dminus_Rplus',(-2,0),7,3,['B+','E-','T-','Nr+','D-','R+']),
 ('Lupper_Nrplus_Dplus_Rplus',(-2,0),7,3,['B+','E-','T-','Nr+','D+','R+']),
 ('Lfullnorth_Nrminus_Dminus_Rplus',(-2,0),7,4,['B+','E-','T-','Nr-','D-','R+']),
 ('Lfullnorth_Nrminus_Dplus_Rplus',(-2,0),7,4,['B+','E-','T-','Nr-','D+','R+']),
 ('Louter3_Nbplus_Dminus',(-2,0),0,3,['B+','E-','T-','Nb+','D-']),
 ('Louter3_Nbplus_Rminus',(-2,0),0,3,['B+','E-','T-','Nb+','R-']),
 ('Louter3_Nrminus_Rminus',(-2,0),0,3,['B+','E-','T-','Nr-','R-']),
 ('Louter3_Nrminus_Rplus',(-2,0),0,3,['B+','E-','T-','Nr-','R+']),
 ('Louter4_Nbplus_Dminus',(-2,0),0,4,['B+','E-','T-','Nb+','D-']),
 ('Louter4_Nbplus_Rminus',(-2,0),0,4,['B+','E-','T-','Nb+','R-']),
 ('Louter4_Nrminus_Rminus',(-2,0),0,4,['B+','E-','T-','Nr-','R-']),
 ('Louter4_Nrminus_Rplus',(-2,0),0,4,['B+','E-','T-','Nr-','R+']),
 ('Bfullwest_Nrminus_Rplus_Dminus_Tminus',(0,-2),1,4,['L+','E-','Nr-','R+','D-','T-']),
 ('Bfullwest_Nrminus_Rplus_Dplus_Tminus',(0,-2),1,4,['L+','E-','Nr-','R+','D+','T-']),
 ('Bfullwest_Nrminus_Rplus_Dplus_Tplus',(0,-2),1,4,['L+','E-','Nr-','R+','D+','T+']),
]
residues={}
for name,c,st,m,labels in residue_specs:
 ts=H|fan(c,st,m)|{caps[n] for n in labels}
 ll=ledger(ts)
 assert ll['W']==20 and ll['k']==6 and ll['Delta']==4,(name,ll)
 residues[name]={'status':'VALID_GEOMETRY_NOT_DARKNESS','fan_center':c,'start':st,'sectors':m,'caps':labels,'ledger':ll,'triangles':sorted(ts),'vertices':polygon(ts)}
# Apply only the newly derived named compositions to the nine specified L
# residues they prove. This is full guard verification, not path selection.
new_paths=json.loads((HERE/'left-return-check.json').read_text())['paths']
for name,rr in residues.items():
 which=None
 if name.startswith('Lupper_Nrplus_'):which='short_square_flat'
 elif name.startswith('Lfullnorth_Nrminus_') or name.startswith('Louter3_Nrminus_'):which='trapezoid_Ncap'
 elif name.startswith('Louter4_Nrminus_'):which='wide_rectangle_Ncap'
 if which:
  row=new_paths[which]
  P=[tuple(map(F,p)) for p in row['path']]
  u,z=path_requirements(P);ts={tri(t) for t in rr['triangles']}
  assert u<=ts and not z&ts,(name,which)
  rr['status']='CLOSED_BY_DERIVED_COMPOSITION'
  rr['selected_path']=which
  rr['reflections']=row['reflections']
remaining=[n for n,r in residues.items() if r['status']=='VALID_GEOMETRY_NOT_DARKNESS']
assert len(remaining)==7
# Controls only for the two new universal lemmas. They are prescribed above.
for which,name in [('uniform_seven','Bfullwest_Nrminus_Rplus_Dplus_Tplus'),('rectangle_three',None)]:
 if which=='uniform_seven':
  # Replace Nr- by Nb+ in the named control, exactly as prescribed here.
  rr=residues[name];ts={tri(t) for t in rr['triangles']}-{caps['Nr-']}|{caps['Nb+']}
 else:ts=H|fan((0,-2),6,4)|{caps[n] for n in ['L+','E-','Nr-','R+','T-']}
 V=polygon(ts);P=paths[which];u,z=path_requirements(P)
 assert u<=ts and not z&ts
 replay(V,(0,0),(2,2),P);replay(V,(2,2),(0,0),P[::-1])
result={'status':'PARTIAL_COVER_WITH_EXACT_RESIDUES','remaining_exact_cases':remaining,'universal_lemmas':{k:{'reflections':len(paths[k])-2,'path':[[str(v) for v in p] for p in paths[k]],'required':sorted(path_requirements(paths[k])[0]),'forbidden':sorted(path_requirements(paths[k])[1])} for k in ['uniform_seven','rectangle_three']},'named_implications':receipts,'residues':residues,'scope':'23 hand-stated symbolic implications, two prescribed path controls, 16 hand-forced geometry validations and nine named applications of newly derived compositions. No cap-assignment, path, direction, word or archive discovery. Residue completeness is the hand argument in single-e2.txt, not an enumeration.','source_hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'third-surplus-review/local-e2-project.json',ROOT/'third-surplus-review/local-e2-residue-frozen.json']}}
(HERE/'single-e2-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'symbolic_implications':len(receipts),'hand_forced_valid_candidates':len(residues),'remaining_exact_cases':len(remaining),'universal_paths':[7,3]}))
