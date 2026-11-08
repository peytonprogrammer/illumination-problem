"""Critical-L named inheritance guards and seven hand-forced geometry fixtures."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,runpy
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
helper=HERE/'root-leaf-check.py';ns={'__file__':str(helper),'__name__':'retained_helpers'}
exec(compile(helper.read_text().split('BDR=')[0],str(helper),'exec'),ns)
H,fan,full,C,tri,g=[ns[n] for n in ['H','fan','full','C','tri','g']]
physical,polygon,ledger=[ns[n] for n in ['physical','polygon','ledger']]
read,decode,sigma,tr=[ns[n] for n in ['read','decode','sigma','tr']]
B6=decode(read('first-surplus-review/bottom-residual-check.json')['path'])
B4=B6[:4]+[(F(5,3),F(4))]+B6[7:]
L11=decode(read('first-surplus-review/square-exchange-check.json')['paths']['L_thirteen']['path'])
double3=[(F(0),F(0)),(F(-2),F(1,3)),(F(4),F(4,3)),(F(1),F(11,6)),(F(2),F(2))]
low=fan('L',[6,7,0]);upper=fan('L',[7,0,1]);rect=fan('L',[6,7,0,1]);BC=fan('B',[1,2]);EC=fan('E',[3,4]);EO=fan('E',[4,5]);TO=fan('Tc',[4,5]);NB=fan('N',[4,5,6]);DR=full('D')|full('R')
spec=[
 ('Llower_Bcenter_B6','B6',H|low|BC|C(['T-']),H|low|BC|DR|full('E')|(full('N')-C(['Nb-']))|C(['T-'])),
 ('Llower_Bcenter_Touter_B4','B4',H|low|BC|TO,H|low|BC|TO|DR|full('E')|(full('N')-C(['Nb-']))),
 ('Lrectangle_ordinaryE_L11','L11',H|rect|C(['E-']),H|rect|full('B')|DR|NB|TO|C(['E-'])),
 ('Lupper_ordinaryE_L11','L11',H|upper|C(['E-']),H|upper|full('B')|DR|NB|TO|C(['E-'])),
 ('Lrectangle_Eouter_double3','double3',H|rect|EO,H|rect|EO|full('B')|DR|full('Tc')|NB),
 ('Lupper_Eouter_double3','double3',H|upper|EO,H|upper|EO|full('B')|DR|full('Tc')|NB),
]
paths={'B6':B6,'B4':B4,'L11':L11,'double3':double3};checks={}

# Only four retained, explicitly scoped line records; no archive or term search.
terms=read('third-surplus-review/local-mixed-project.json')['families']['Lupper_Ecenter']['terms']
retained={}
for line in [2997,2823,2240,2224]:
 rows=[v for v in terms if v['source_line']==line];assert len(rows)==1
 retained[line]=rows[0];paths[str(line)]=decode(rows[0]['path'])
upperbase=H|upper|EC|C(['B+','T-','Nb-'])
BO=fan('B',[0,1]);NSW=fan('N',[4,5]);NC=fan('N',[5,6])
upperB=H|upper|EC|BO|C(['T-','Nb-'])
upperN=H|upper|EC|NSW|C(['B+','T-'])
spec += [
 ('rectangle_BC_EC_Dplus_Rplus_2997','2997',H|rect|BC|EC|C(['Nb-','T-','D+','R+']),H|rect|BC|EC|C(['Nb-','T-','D+','R+'])),
 ('upper_EC_Bouter_Dplus_2997','2997',upperB|C(['D+']),upperB|C(['D+','R+'])),
 ('upper_EC_Bouter_noDplus_noRminus_2823','2823',upperB,upperB|C(['D-','R+'])),
 ('upper_EC_Dupperquarter_2240','2240',upperbase|fan('D',[0,1]),upperbase|fan('D',[0,1])),
 ('upper_EC_Dwestquarter_2823','2823',upperbase|fan('D',[2,3]),upperbase|fan('D',[2,3])),
 ('upper_EC_Rupperquarter_2823','2823',upperbase|fan('R',[2,3]),upperbase|fan('R',[2,3])),
 ('upper_EC_Nsw_noDplus_noRminus_2823','2823',upperN,upperN|C(['D-','R+'])),
 ('upper_EC_Nsw_Dplus_2997','2997',upperN|C(['D+']),upperN|C(['D+'])),
 ('upper_EC_Nsw_Rminus_2240','2240',upperN|C(['R-']),upperN|C(['R-'])),
 ('upper_EC_Ncenter_Dplus_Rplus_2997','2997',H|upper|EC|NC|C(['B+','T-','D+','R+']),H|upper|EC|NC|C(['B+','T-','D+','R+'])),
]
for name,which,fixed,possible in spec:
 P=paths[which];U,Z=g['path_requirements'](P)
 assert U<=fixed,(name,'required',U-fixed)
 assert not Z&possible,(name,'forbidden',Z&possible)
 us,zs=g['path_requirements']([sigma(p) for p in P[::-1]])
 assert us==tr(U) and zs==tr(Z)
 checks[name]={'status':'PASS','reflections':len(P)-2,'path':[[str(x) for x in p] for p in P],'required':sorted(U),'forbidden':sorted(Z),'fixed':sorted(fixed),'possible':sorted(possible),'sigma':'PASS'}
# Hand-forced fixtures: geometry only except the ONE previously named 2997 closure.
fixtures={}
base=H|low|BC|fan('N',[4,5])|C(['E-','T-'])
for cap in ['D-','D+','R-','R+']:fixtures['Llower_Bcenter_Nsw_'+cap]=base|C([cap])
base=H|rect|BC|EC|C(['Nb-','T-'])
for dc,rc in [('D-','R-'),('D-','R+'),('D+','R+')]:fixtures['Lrectangle_Bcenter_Ecenter_'+dc+rc]=base|C([dc,rc])
base=H|upper|EC
fixtures['Lupper_Ecenter_Bouter_Rminus']=base|BO|C(['T-','Nb-','R-'])
for rc in ['R-','R+']:fixtures['Lupper_Ecenter_Ncenter_Dminus_'+rc]=base|NC|C(['B+','T-','D-',rc])
for cap in ['D+','R-']:fixtures['Lupper_Ecenter_Nsw_'+cap]=base|NSW|C(['B+','T-',cap])
fixtures['Lupper_Ecenter_Dcenter_Rplus']=base|fan('D',[1,2])|C(['B+','T-','Nb-','R+'])
fixtures['Lupper_Ecenter_Rcenter_Dminus']=base|fan('R',[3,4])|C(['B+','T-','Nb-','D-'])
assert len(fixtures)==14
geompath=ROOT/'triangle-composition/inputs/illumination_geometry.py'
geom=runpy.run_path(str(geompath))
# Compute d from actual H-side BC incidences, not array position or assumed root count.
from collections import Counter
edges=Counter(tuple(sorted(e)) for t in H for e in [(t[0],t[1]),(t[1],t[2]),(t[2],t[0])])
hbound={e for e,c in edges.items() if c==1}
receipts={}
for name,ts in fixtures.items():
 gd=geom['check']({'triangles':sorted(ts),'marked':[(0,0),(2,2)],'require_simple':True},strict=False)
 ld=ledger(ts)
 assert gd['walls']==20 and set(map(tuple,gd['interior_A']))=={(0,0),(2,0),(2,2)}
 assert ld['W']==20 and ld['k']==6 and ld['Delta']==4,(name,ld)
 groups={}
 for t in ts:
  a=next(p for p in t if p[0]%2==p[1]%2==0);groups.setdefault(a,[]).append(t)
 charges=[]
 for a,tt in groups.items():
  if len(tt)==8:continue
  touched=set()
  for t in tt:
   edge=tuple(sorted(p for p in t if p!=a))
   if edge in hbound:
    touched.add(next(p for p in edge if (p[0]%2)!=(p[1]%2)))
  q=3 if len(tt)==4 else len(tt);d=len(touched);e=q-d
  if e:charges.append({'A':a,'q':q,'d':d,'e':e})
 assert sorted(v['e'] for v in charges)==[1,1,2] and all(v['d']==1 for v in charges),(name,charges)
 assert ld['Delta']-sum(v['e'] for v in charges)==0
 receipts[name]={'status':'VALID_GEOMETRY_ONLY_OPTICS_OPEN','ledger':ld,'charges':charges,'b':0,'triangles':sorted(ts),'vertices':polygon(ts)}
covered={
 'Lrectangle_Bcenter_Ecenter_D+R+':'2997',
 'Lupper_Ecenter_Nsw_D+':'2997',
 'Lupper_Ecenter_Nsw_R-':'2240',
}
for name,which in covered.items():
 assert name in fixtures
 P=paths[which];V=polygon(fixtures[name])
 physical(P,V);physical(P[::-1],V);physical([sigma(p) for p in P[::-1]],[sigma(p) for p in V])
 receipts[name]['status']='CLOSED_BY_PREDECLARED_RETAINED_PATH_ACTUAL_FIRST_T_REPLAY'
 receipts[name]['retained_line']=which
 receipts[name]['reflections']=len(P)-2
out={'status':'PASS','named_implications':checks,'hand_forced_fixtures':receipts,'optically_open_fixture_names':[n for n in receipts if n not in covered],'limits':'No room/cap-assignment discovery or new ray/path/direction/word selection. Fourteen explicitly hand-forced fixtures receive geometry; THREE are closed by predeclared retained2997/2240 physical replays. Eleven remain optically open. Guards are sixteen specified inherited/composed implications, not a classification proof.','source_hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [helper,geompath]}}
(HERE/'critical-L-check.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS:16 named guards/sigma;14 hand-forced geometries; THREE fixed-path closures,11 OPTICS OPEN')
