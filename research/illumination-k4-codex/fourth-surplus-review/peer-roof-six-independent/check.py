"""Independent roof/D-minus six-path audit. No room construction or discovery."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
sys.path.insert(0,str(ROOT/'triangle-composition/inputs'))
from guard_checker import path_requirements
D=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
centers={'L':(-2,0),'B':(0,-2),'D':(2,-2),'R':(4,0),'E':(4,2),'Tc':(2,4),'N':(0,2)}
def tri(t):return tuple(sorted(map(tuple,t)))
def at(a,ss):return {tri((a,(a[0]+D[i%8][0],a[1]+D[i%8][1]),(a[0]+D[(i+1)%8][0],a[1]+D[(i+1)%8][1]))) for i in ss}
def fan(k,ss):return at(centers[k],ss)
H=set().union(*(at(a,range(8)) for a in [(0,0),(2,0),(2,2)]))
sub=lambda a,b:(a[0]-b[0],a[1]-b[1]);dot=lambda a,b:a[0]*b[0]+a[1]*b[1];cross=lambda a,b:a[0]*b[1]-a[1]*b[0]
sigma=lambda p:(2-p[1],2-p[0]);transform=lambda ts:{tri(sigma(p) for p in t) for t in ts}
P=[(F(0),F(0)),(F(-1,6),F(-1)),(F(-4,7),F(10,7)),(F(4,5),F(6,5)),(F(6,5),F(-6,5)),(F(2),F(-4,3)),(F(10,7),F(-10,7)),(F(2),F(2))]
# Only six declared finite mirror segments; no boundary of a new room is generated.
W=[((-1,-1),(0,-1)),((-1,1),(0,2)),((0,2),(1,1)),((1,-1),(2,-2)),((2,-2),(2,-1)),((1,-1),(2,-2))]
def reflect_vector(v,a,b):
 e=sub(b,a);return tuple(2*dot(v,e)*e[k]/dot(e,e)-v[k] for k in (0,1))
def on(p,a,b):return cross(sub(p,a),sub(b,a))==0 and dot(sub(p,a),sub(p,b))<=0
def strict(p,a,b):return on(p,a,b) and p!=a and p!=b
def check_reflections(path,walls):
 assert len(path)==len(walls)+2
 for i,(a,b) in enumerate(walls,1):
  assert strict(path[i],a,b)
  vin=sub(path[i],path[i-1]);out=sub(path[i+1],path[i]);want=reflect_vector(vin,a,b)
  assert cross(out,want)==0 and dot(out,want)>0
 for i,(a,b) in enumerate(zip(path[:-1],path[1:])):
  assert a!=b
  if i<len(path)-2:assert not on(path[-1],a,b)
check_reflections(P,W)
check_reflections(P[::-1],W[::-1])
check_reflections([sigma(p) for p in P[::-1]],[(sigma(a),sigma(b)) for a,b in W[::-1]])
# Entire min/max optical implication, with the two endpoint marks fixed.
minimum=H|fan('N',[5,6])|fan('D',[2])
maximum=minimum|fan('B',[1])|set().union(*(fan(k,range(8)) for k in ['L','E','Tc','R']))
U,Z=path_requirements(P)
assert U<=minimum and not Z&maximum
Us,Zs=path_requirements([sigma(p) for p in P[::-1]])
assert Us==transform(U) and Zs==transform(Z)
# Actual wall unfolding, with the finite segments above fixing mirror identity.
q=P[-1]
for a,b in W[::-1]:
 vv=sub(q,a);rv=reflect_vector(vv,a,b);q=tuple(a[k]+rv[k] for k in (0,1))
assert q==(-2,-12) and cross(q,(-1,-6))==0 and dot(q,(-1,-6))>0
# Roof and Dcap gates, reconstructed from formulas rather than peer receipt.
d=F(1,6);assert F(1,7)<d<F(1,5) and 12*d==2
entry=(-3*d,F(1));exit=(5*d,F(1))
left=(-4*d/(1+d),2-4*d/(1+d));right=(4*d/(1-d),2-4*d/(1-d))
assert [left,right]==P[2:4]
assert 0<2-7*d<1 and 0<2-9*d<1
for a,b,v in [(P[1],entry,(-d,1)),(entry,left,(-d,1)),(right,exit,(d,-1)),(exit,(7*d,F(-1)),(d,-1)),((7*d,F(-1)),P[4],(d,-1)),(P[6],(9*d,F(-1)),(d,1)),((9*d,F(-1)),P[-1],(d,1))]:
 delta=sub(b,a);assert cross(delta,v)==0 and dot(delta,v)>0
peer=ROOT/'surplus-four-local/e2-e1-b1/critical-L-check.json';pj=json.loads(peer.read_text())
assert P==[tuple(F(x) for x in p) for p in pj['new_roof_Dcap_composition']['path']]
row=pj['named_guards']['Ncenter_Dminus6_full_L_E_T_R']
assert U=={tri(t) for t in row['required']} and Z=={tri(t) for t in row['forbidden']}
assert q==tuple(map(F,pj['new_roof_Dcap_composition']['unfolded_actual_target']))
# Application obstruction is logical: the original R-Beast rooms have B012,
# N7 and no D cell. The SOURCE-floor reflection needs B2 absent, while the
# roof and lower cap require N5/N6 and D2. No new room is assembled here.
assert U&fan('N',[5,6])==fan('N',[5,6])
assert U&fan('D',[2])==fan('D',[2])
assert Z&fan('B',[2])==fan('B',[2])
out={'status':'INDEPENDENT_SIX_PATH_AND_WHOLE_SUPPORT_CHECKS_PASS','reflections':6,'path':[[str(x) for x in p] for p in P],'declared_finite_mirrors':W,'specular_strict_contacts_first_T_reverse_sigma':'PASS','minimum':sorted(minimum),'maximum':sorted(maximum),'required':sorted(U),'forbidden':sorted(Z),'actual_unfolded_target':list(map(str,q)),'roof':{'parameter':'1/6','strict_interval':['1/7','1/5'],'entry':list(map(str,entry)),'exit':list(map(str,exit))},'R_Beast_transfer':'INAPPLICABLE: required N5,N6,D2 missing; forbidden B2 present','source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [peer,ROOT/'surplus-four-local/e2-e1-b1/critical-L.txt',ROOT/'triangle-composition/inputs/guard_checker.py']},'limits':'Independent local reflection arithmetic and hand derivation; retained guard checker shared historically. No peer checker executed, new assembled room, geometry control, ray/direction/word discovery, archive or worker. Does not review critical-L classification, thirteen descriptions or two531 exchanges.'}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: independent finite six mirrors, strict ports, first actual T/reverse/sigma, full guard, unfold(-2,-12). R-Beast transfer INAPPLICABLE.')
