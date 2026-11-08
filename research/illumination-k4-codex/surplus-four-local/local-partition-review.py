"""Independent fixed guard and arithmetic checks for repaired local frontier."""
from pathlib import Path
from fractions import Fraction as F
import json,sys,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
sys.path.insert(0,str(ROOT/'triangle-composition/inputs'))
from guard_checker import path_requirements
tri=lambda t:tuple(sorted(map(tuple,t)))
dirs=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
def fan(c,ss):
 return {tri((c,(c[0]+dirs[i%8][0],c[1]+dirs[i%8][1]),(c[0]+dirs[(i+1)%8][0],c[1]+dirs[(i+1)%8][1]))) for i in ss}
H=set().union(*(fan(c,range(8)) for c in [(0,0),(2,0),(2,2)]))
read=lambda f:json.loads((ROOT/f).read_text())
caps={n:tri(t) for n,t in read('triangle-composition/inputs/caps.json')['cap_options'].items()}
assert caps=={n:tri(t) for n,t in read('zero-surplus-L/guard-incidence-check.json')['cap_options'].items()}
C=lambda ns:{caps[n] for n in ns}
decode=lambda p:[tuple(F(*v) for v in q) for q in p]
z=read('zero-surplus-L/cover-check.json')['paths']
sq=read('first-surplus-review/square-exchange-check.json')['paths']
paths={'one':decode(z['one']['path']),'one_sigma':decode(z['one_sigma']['path']),
 'sigma_four':decode(z['four_sigma']['path']),'B_two':decode(sq['B_four']['path']),
 'five':decode(read('second-surplus-review/five-path-check.json')['five_path']),
 'sigma13':decode(z['thirteen_sigma']['path'])}
B=fan((0,-2),[0,1]);D=fan((2,-2),[3,4,5]);Dall=fan((2,-2),range(8))
ordinary=C([n for n in caps if n not in ['B+','B-','D+','D-']])
minimum=H|B|D;maximum=H|B|Dall|ordinary
rules=[('Eminus_absent','one_sigma',minimum,maximum-C(['E-'])),
 ('Eminus_present_Lplus_absent','sigma_four',minimum|C(['E-']),maximum-C(['E+','L+'])),
 ('Lplus_Eminus_present_Tminus_absent','B_two',minimum|C(['L+','E-']),maximum-C(['T-'])),
 ('Lplus_Eminus_Tminus_Nbplus_absent','five',minimum|C(['L+','E-','T-']),
  H|B|Dall|C(['L+','E-','T-','R-','R+','Nb-','Nr-','Nr+'])),
 ('Lplus_Eminus_Tminus_Nbplus_present','sigma13',minimum|C(['L+','E-','T-','Nb+']),
  H|B|Dall|C(['L+','E-','T-','Nb+','R-','R+'])),
 ('Droot_Bleaf_Bplus_absent','one',H,(H|Dall|fan((0,-2),range(8))|ordinary)-C(['B+']))]
sigma=lambda p:(2-p[1],2-p[0])
transform=lambda tiles:{tri(sigma(p) for p in t) for t in tiles}
checks=[]
for name,key,needed,possible in rules:
 P=paths[key];U,Z=path_requirements(P)
 assert P[0]==(0,0) and P[-1]==(2,2)
 assert U<=needed and not Z&possible,(name,U-needed,Z&possible)
 Us,Zs=path_requirements([sigma(p) for p in P[::-1]])
 assert Us==transform(U) and Zs==transform(Z)
 checks.append({'name':name,'path':key,'reflections':len(P)-2,
  'required_subset_minimum':'PASS','forbidden_disjoint_maximum':'PASS','sigma':'PASS',
  'required':sorted(U),'forbidden':sorted(Z)})
 print(name,'full-envelope PASS')
partitions=[(4,[]),(3,[1]),(2,[2]),(2,[1,1]),(1,[3]),(1,[2,1]),
 (1,[1,1,1]),(0,[4]),(0,[3,1]),(0,[2,2]),(0,[2,1,1]),(0,[1,1,1,1])]
assert all(b+sum(es)==4 for b,es in partitions)
# Hand integer partition counts: p(0),...,p(4)=1,1,2,3,5.
assert [sum(b==k for b,es in partitions) for k in [4,3,2,1,0]]==[1,1,2,3,5]
assert len({(b,tuple(es)) for b,es in partitions})==12
fan_checks=[]
for m in [5,6]:
 for st in range(8):
  sectors={(st+i)%8 for i in range(m)}
  both=bool(sectors&{5,6}) and bool(sectors&{7,0})
  bridge={6,7}<=sectors
  if m==5:assert not both or bridge
  if m==6 and both and not bridge:assert sectors==set(range(6))
  pairs=[i for i in [0,2,4,6] if {i,(i-1)%8}<=sectors]
  if m==5:assert len(pairs)>=2
  fan_checks.append({'m':m,'start':st,'touches_both_H_sides':both,
   'bridge':bridge,'complete_C_rays':pairs})
assert [r['start'] for r in fan_checks if r['m']==6 and r['touches_both_H_sides'] and not r['bridge']]==[0]
# D leaf windows retained by the hand proof, not assembled rooms.
assert {3,4}<=set([3,4,5]) and not set([1,2])&set([3,4,5])
assert {5,6}<=set([3,4,5,6])
out={'status':'ACCEPT_REPAIRED_TEN_LOCAL_TYPES_AND_E3_E1_COVER',
 'twelve_arithmetic_partitions':[{'b':b,'positive_excesses':es} for b,es in partitions],
 'excluded_solitary':['e3+b1','e4'],'necessary_local_types':10,
 'restored_open_types':['e2+e1+b1','three_e1+b1'],
 'new_e3_e1_reflection_bound':max(r['reflections'] for r in checks),
 'six_guards':checks,'N_fan_identities':fan_checks,
 'hand_review':'local-partition-review.txt',
 'input_hashes':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in [
  'fourth-surplus-review/local-partition-audit.txt','zero-surplus-L/cover-check.json',
  'first-surplus-review/square-exchange-check.json','second-surplus-review/five-path-check.json']},
 'limits':'Finite fixed guard implications and named local fan identities; completeness/geometry follows hand argument. Mixed e2-leaf inheritance is a separate unreviewed request. No room/path discovery or fullDelta4 claim.'}
(HERE/'local-partition-review.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'],'bound',out['new_e3_e1_reflection_bound'])
