"""Independent replay of exactly named critical-L dependency certificates."""
from pathlib import Path
from fractions import Fraction as F
import json,sys,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
sys.path.insert(0,str(ROOT/'triangle-composition/inputs'))
from guard_checker import path_requirements
DIRECTIONS=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
CENTERS={'L':(-2,0),'B':(0,-2),'D':(2,-2),'R':(4,0),'E':(4,2),'Tc':(2,4),'N':(0,2)}
def tri(t):return tuple(sorted(map(tuple,t)))
def at(a,ss):return {tri((a,(a[0]+DIRECTIONS[i%8][0],a[1]+DIRECTIONS[i%8][1]),(a[0]+DIRECTIONS[(i+1)%8][0],a[1]+DIRECTIONS[(i+1)%8][1]))) for i in ss}
def fan(k,ss):return at(CENTERS[k],ss)
def full(k):return fan(k,range(8))
H=set().union(*(at(a,range(8)) for a in [(0,0),(2,0),(2,2)]))
CAP={'B+':('B',1),'B-':('B',2),'E-':('E',4),'T-':('Tc',5),'T+':('Tc',6),'Nb-':('N',5),'Nb+':('N',6),'Nr-':('N',7),'Nr+':('N',0),'D-':('D',2),'D+':('D',1),'R-':('R',4),'R+':('R',3)}
def C(ns):return set().union(*(fan(CAP[n][0],[CAP[n][1]]) for n in ns))
def number(x):return F(*x) if isinstance(x,list) else F(x)
def decode(raw):return [tuple(number(x) for x in p) for p in raw]
sources={}
def read(rel):
 p=ROOT/rel;data=p.read_bytes();sources[rel]=hashlib.sha256(data).hexdigest();return json.loads(data)
sub=lambda a,b:(a[0]-b[0],a[1]-b[1])
cross=lambda a,b:a[0]*b[1]-a[1]*b[0]
dot=lambda a,b:a[0]*b[0]+a[1]*b[1]
sigma=lambda p:(2-p[1],2-p[0])
def transformed(ts):return {tri(sigma(p) for p in t) for t in ts}
def sigpath(P):return [sigma(p) for p in P[::-1]]
def on(p,a,b):return cross(sub(p,a),sub(b,a))==0 and dot(sub(p,a),sub(p,b))<=0

def local(P):
 assert P[0]==(0,0) and P[-1]==(2,2)
 for a,b in zip(P[:-2],P[1:-1]):assert not on(P[-1],a,b)
 for before,p,after in zip(P,P[1:],P[2:]):
  vin=sub(p,before);vout=sub(after,p);matches=[]
  for t in [(1,0),(0,1),(1,1),(1,-1)]:
   rv=tuple(2*dot(vin,t)*t[k]-dot(t,t)*vin[k] for k in (0,1))
   if cross(rv,vout)==0 and dot(rv,vout)>0 and cross(t,vin)!=0:matches.append(t)
  assert len(matches)==1,(p,matches)
  tangent=matches[0]
  assert cross(tangent,sub(before,p))*cross(tangent,sub(after,p))>0
 return True
P={
 'L3':decode(read('first-surplus-review/residual-cover-check.json')['path']),
 'B6':decode(read('first-surplus-review/bottom-residual-check.json')['path']),
 'five':decode(read('second-surplus-review/five-path-check.json')['five_path'])}
P['T3']=sigpath(P['L3'])
U7=decode(read('surplus-four-local/single-e2-check.json')['universal_lemmas']['uniform_seven']['path'])
P['square5']=[U7[0],(F(-2),F(1,3))]+U7[4:]
P['double3']=[U7[0],(F(-2),F(1,3)),(F(4),F(4,3))]+U7[7:]
# Only five exact identifiers in the two named projection families.
def retained(rel,family,line):
 records=read(rel)['families'][family]['terms']
 selected=[r for r in records if r['source_line']==line]
 assert len(selected)==1
 r=selected[0];path=decode(r['path']);U,Z=path_requirements(path)
 assert U=={tri(t) for t in r['required_triangles']}
 assert Z=={tri(t) for t in r['forbidden_triangles']}
 return path
P['L14']=retained('third-surplus-review/local-e2-project.json','L_Hupper3_Nrminus',3580)
P['531']=retained('third-surplus-review/local-e2-project.json','L_outer3_Nbminus',531)
for line in [2997,2240,2224]:
 P[str(line)]=retained('third-surplus-review/local-mixed-project.json','Lupper_Ecenter',line)
P['531N13']=P['531'][:2]+[(F(-8,11),F(2))]+P['531'][5:]
P['531E13']=P['531'][:12]+[(F(4),F(14,11))]+P['531'][15:]
P['roof6']=[(F(0),F(0)),(F(-1,6),F(-1)),(F(-4,7),F(10,7)),(F(4,5),F(6,5)),(F(6,5),F(-6,5)),(F(2),F(-4,3)),(F(10,7),F(-10,7)),(F(2),F(2))]
lo=fan('L',[6,7,0]);up=fan('L',[7,0,1]);rect=fan('L',[6,7,0,1]);lo4=fan('L',[5,6,7,0]);out=fan('L',[0,1,2])
BC=fan('B',[1,2]);BO=fan('B',[0,1]);EC=fan('E',[3,4]);EO=fan('E',[4,5]);TO=fan('Tc',[4,5]);DR=full('D')|full('R')
notNb=full('N')-C(['Nb-']);notNr=full('N')-C(['Nr-']);notNbplus=full('N')-C(['Nb+'])
# Rebuilt proof envelopes; labels correspond to the sixteen explicit usages.
specs=[
 ('lower_nonB','L3',H|lo|C(['B+']),H|lo|C(['B+'])|full('E')|full('Tc')|full('N')|DR),
 ('lower_BC_withoutN5','B6',H|lo|BC|C(['T-']),H|lo|BC|C(['T-'])|full('E')|notNb|DR),
 ('lower_BO_withoutN6','five',H|lo|BO|C(['T-']),H|full('L')|BO|C(['T-'])|full('E')|notNbplus|DR),
 ('lower4_BC_withoutN5','B6',H|lo4|BC|C(['T-']),H|lo4|BC|C(['T-'])|full('E')|notNb|DR),
 ('upper_rectangle_BC_withoutN5','B6',H|BC|C(['T-']),H|full('L')|BC|C(['T-'])|full('E')|notNb|DR),
 ('upper_rectangle_ordinaryE_withoutN7','square5',H|up|C(['E-']),H|rect|full('B')|C(['E-'])|full('Tc')|notNr|DR),
 ('upper_rectangle_Eouter_withoutN7','double3',H|up|EO,H|rect|full('B')|EO|full('Tc')|notNr|DR),
 ('upper_rectangle_N7_outer_or_ordinary','L14',H|up|C(['B+','E-','T-','Nr-']),H|rect|BO|EO|TO|fan('N',[7,0])|DR),
 ('Tcenter_fullL','T3',H|fan('Tc',[5,6])|C(['E-']),H|full('L')|full('B')|C(['E-'])|fan('Tc',[5,6])|full('N')|DR),
 ('upper_EC_N5_D1R4','2240',H|up|EC|C(['B+','T-','D+','R-']),H|up|EC|C(['B+','T-','D+','R-','Nb-'])),
 ('upper_rectangle_EC_bottomN_D1R3','2997',H|up|EC|C(['B+','T-','D+','R+']),H|rect|EC|C(['B+','T-','D+','R+','Nb-','Nb+'])),
 ('upper_EC_N7_D2R4','2224',H|up|EC|C(['B+','T-','D-','R-']),H|up|EC|C(['B+','T-','D-','R-','Nr-'])),
 ('outer3_N5_Bordinary_outer','531',H|out|C(['B+','E-','T-','Nb-']),H|out|BO|C(['E-','Nb-'])|full('Tc')|DR),
 ('outer3_N45_composed','531N13',H|out|fan('N',[4,5])|C(['B+','E-','T-']),H|out|fan('N',[4,5])|C(['B+','E-','T-'])|DR),
 ('outer3_E45_composed','531E13',H|out|EO|C(['B+','T-','Nb-']),H|out|EO|C(['B+','T-','Nb-'])|DR),
 ('N56_D2_roof','roof6',H|fan('N',[5,6])|C(['D-']),H|fan('N',[5,6])|C(['D-','B+'])|full('L')|full('E')|full('Tc')|full('R'))]
checks={}
for label,key,mi,ma in specs:
 path=P[key];local(path);local(sigpath(path))
 U,Z=path_requirements(path)
 assert mi<=ma and U<=mi and not Z&ma,(label,'guard')
 Ur,Zr=path_requirements(path[::-1]);assert U==Ur and Z==Zr
 Us,Zs=path_requirements(sigpath(path));assert Us==transformed(U) and Zs==transformed(Z)
 checks[label]={'path':key,'reflections':len(path)-2,'status':'PASS','minimum':sorted(mi),'maximum':sorted(ma),'required':sorted(U),'forbidden':sorted(Z)}
# Two one-hit replacements: fixed predecessor/successor and exact portal states.
ports={}
for key,first,last,entry,vel,exitpoint,outvel,hit,u,d in [
 ('531N13',2,4,(F(-6,11),F(1)),(-2,11),(F(-10,11),F(1)),(-2,-11),(F(-8,11),F(2)),F(6,11),F(2,11)),
 ('531E13',12,14,(F(3),F(12,11)),(11,2),(F(3),F(16,11)),(-11,2),(F(4),F(14,11)),F(1,11),F(2,11))]:
 assert 0<u<1 and 0<u+2*d<1
 for a,b,v in [(P['531'][first-1],entry,vel),(entry,P['531'][first],vel),(P['531'][last],exitpoint,outvel),(exitpoint,P['531'][last+1],outvel),(entry,hit,vel),(hit,exitpoint,outvel)]:
  delta=sub(b,a);assert cross(delta,v)==0 and dot(delta,v)>0
 assert len(P[key])-2==13
 ports[key]={'entry':list(map(str,entry)),'exit':list(map(str,exitpoint)),'same_velocities':True,'strict_phase':[str(u),str(u+2*d)]}
# Negative controls on central branches: preserve scope, no extra path retrieval.
assert path_requirements(P['L14'])[1]&BC
assert path_requirements(P['square5'])[1]&fan('N',[7])
assert path_requirements(P['double3'])[1]&fan('N',[7])
assert path_requirements(P['531'])[1]&fan('L',[7])
assert path_requirements(P['531'])[1]&fan('L',[3])
# Disclose and pin inherited-prerequisite sources without asserting their audit.
proof=ROOT/'surplus-four-local/e2-e1-b1/critical-L.txt';sources[str(proof.relative_to(ROOT))]=hashlib.sha256(proof.read_bytes()).hexdigest()
sources[str(Path(__file__).relative_to(ROOT))]=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
out={'status':'INDEPENDENT_SIXTEEN_NAMED_OPTICAL_DEPENDENCIES_PASS','checks':checks,'normal_composition_ports':ports,'named_paths':{k:[[str(x) for x in p] for p in v] for k,v in P.items()},'source_sha256':sources,
 'limits':'Exactly16 named guard applications and two normal531 compositions; actual ordered endpoints, local specularity, complete open-segment/bounce requirements, firstT, reverse and sigma. Historical guard helper shared. Does not reprove earlier root/leaf partition or short-path forcing prerequisites; no peer checker execution, extra source-line selection, completed-room/cap enumeration, ray/direction/word search, solver, worker or raw archive.'}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: all16 named optical implications; exact two531 portal exchanges; actual endpoints/firstT/specular/fullU-Z/reverse/sigma; no extra certificate retrieval.')
