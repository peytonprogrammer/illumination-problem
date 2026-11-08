"""Named hand substitutions/guard implications; three prescribed controls, no search."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,runpy
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
core=ROOT/'fourth-surplus-review/rplus-exact-one/verify.py'
ns={'__file__':str(core),'__name__':'retained_physical_helpers'}
exec(compile(core.read_text().split("r=json.loads((HERE/'result.json').read_text())")[0],str(core),'exec'),ns)
physical,polygon,ledger,tri=[ns[n] for n in ['physical','polygon','ledger','tri']]
sub,cross,dot=[ns[n] for n in ['sub','cross','dot']]
dirs=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
centers={'L':(-2,0),'B':(0,-2),'D':(2,-2),'R':(4,0),'E':(4,2),'Tc':(2,4),'N':(0,2)}
def fan_at(c,ss):
 return {tri((c,(c[0]+dirs[i%8][0],c[1]+dirs[i%8][1]),(c[0]+dirs[(i+1)%8][0],c[1]+dirs[(i+1)%8][1]))) for i in ss}
def fan(name,ss):return fan_at(centers[name],ss)
H=set().union(*(fan_at(c,range(8)) for c in [(0,0),(2,0),(2,2)]))
read=lambda rel:json.loads((ROOT/rel).read_text())
caps={n:tri(t) for n,t in read('zero-surplus-L/guard-incidence-check.json')['cap_options'].items()}
C=lambda ns:{caps[n] for n in ns};full=lambda n:fan(n,range(8))
decode=lambda p:[tuple(F(*v) for v in q) for q in p]
base7=[tuple(map(F,p)) for p in read('surplus-four-local/single-e2-check.json')['universal_lemmas']['uniform_seven']['path']]
sigma=lambda p:(2-p[1],2-p[0]);tr=lambda ts:{tri(sigma(p) for p in t) for t in ts}
left3=decode(read('first-surplus-review/residual-cover-check.json')['path'])
bottom6=decode(read('first-surplus-review/bottom-residual-check.json')['path'])
left12=decode(read('first-surplus-review/centered-left-check.json')['paths']['left']['path'])
forcing=read('third-surplus-review/independent-review/guard-extension-check.json')['forcing_paths']
zero=read('zero-surplus-L/cover-check.json')['paths']
paths={'one_sigma':decode(zero['one_sigma']['path']),'sigma_four':decode(zero['four_sigma']['path']),'sigma_centerB3':decode(forcing['sigma_centeredB3']['path']),'sigma_outerB2':decode(forcing['sigma_outerB2']['path']),'uniform7':base7,'Lsquare5':[base7[0],(F(-2),F(1,3))]+base7[4:],'Esquare5':base7[:4]+[(F(4),F(4,3))]+base7[7:],'Tcenter3':[sigma(p) for p in left3[::-1]],'Ecenter6':[sigma(p) for p in bottom6[::-1]],'Lcenter12':left12}
g=runpy.run_path(str(ROOT/'lower-bound-proof-audit/full-replay/guard-checker.py'))
BDR=full('B')|full('D')|full('R')
notNrminus=full('N')-C(['Nr-']);notNrplus=full('N')-C(['Nr+'])
# The first clause covers arbitrary noncritical unit R/N or top unit, conditional Nr- absent.
allother=full('B')|full('D')|full('R')|full('Tc')|full('N')
spec=[
 ('missing_E_reference','one_sigma',set(),allother|full('L')|(full('E')-C(['E-']))),
 ('ordinary_E_missing_L','sigma_four',C(['E-']),allother|(full('L')-C(['L+']))|C(['E-'])),
 ('center_E_missing_L','sigma_centerB3',fan('E',[3,4]),allother|(full('L')-C(['L+']))|fan('E',[3,4])),
 ('outer_E_missing_L','sigma_outerB2',fan('E',[4,5]),allother|(full('L')-C(['L+']))|fan('E',[4,5])),
 ('ordinary_LE_Nrminus_absent','uniform7',C(['L+','E-']),BDR|full('Tc')|notNrminus|C(['L+','E-'])),
 ('outer_L_Nrminus_absent','Lsquare5',fan('L',[0,1])|C(['E-']),BDR|full('Tc')|notNrminus|fan('L',[0,1])|C(['E-'])),
 ('outer_E_Nrminus_absent','Esquare5',fan('E',[4,5])|C(['L+']),BDR|full('Tc')|notNrminus|fan('E',[4,5])|C(['L+'])),
 ('center_T','Tcenter3',fan('Tc',[5,6])|C(['E-']),BDR|full('L')|full('N')|fan('Tc',[5,6])|C(['E-'])),
 ('center_E_Nrplus_absent','Ecenter6',fan('E',[3,4])|C(['L+']),BDR|full('Tc')|notNrplus|fan('E',[3,4])|C(['L+'])),
 ('center_L_Nrright_Tplus_absent','Lcenter12',fan('L',[7,0])|C(['E-']),BDR|(full('N')-C(['Nr-','Nr+']))|fan('L',[7,0])|C(['E-','T-'])),
]
checks={}
for name,which,fixed,possible in spec:
 P=paths[which];U,Z=g['path_requirements'](P);fixed|=H;possible|=H
 assert U<=fixed,(name,'required',U-fixed)
 assert not Z&possible,(name,'forbidden',Z&possible)
 us,zs=g['path_requirements']([sigma(p) for p in P[::-1]])
 assert us==tr(U) and zs==tr(Z)
 checks[name]={'status':'PASS','reflections':len(P)-2,'path':[[str(x) for x in p] for p in P],'required':sorted(U),'forbidden':sorted(Z),'fixed':sorted(fixed),'possible':sorted(possible),'sigma':'PASS'}
# Explicit controls declared on the board, not generated assignments.
rootleaf=H|fan('B',[7,0,1])|fan('D',[3])
controls=[
 ('Lsquare',rootleaf|fan('L',[0,1])|C(['E-','Nb-']),'Lsquare5'),
 ('Esquare',rootleaf|fan('E',[4,5])|C(['L+','Nb+']),'Esquare5'),
 ('Tcenter',rootleaf|fan('Tc',[5,6])|C(['L+','E-','Nb+']),'Tcenter3'),
]
receipts={}
for name,ts,which in controls:
 V=polygon(ts);ld=ledger(ts)
 assert ld['W']==20 and ld['k']==6 and ld['Delta']==4,(name,ld)
 P=paths[which];physical(P,V);physical(P[::-1],V);physical([sigma(p) for p in P[::-1]],[sigma(p) for p in V])
 U,Z=g['path_requirements'](P);assert U<=ts and not Z&ts
 receipts[name]={'status':'PASS','ledger':ld,'actual_first_target_forward_reverse_sigma':'PASS','triangles':sorted(ts),'vertices':V}
out={'status':'PASS','named_implications':checks,'three_hand_prescribed_controls':receipts,'input_core_sha256':hashlib.sha256(core.read_bytes()).hexdigest(),'limits':'Ten named whole-support implications only; fixed physical controls prove their own validity, not completeness of a classification. No cap-assignment, room, direction, word or orbit discovery.'}
(HERE/'root-leaf-check.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: ten whole-support implications/sigma; three prescribed W20/k6/Delta4 actual-first-target controls')
