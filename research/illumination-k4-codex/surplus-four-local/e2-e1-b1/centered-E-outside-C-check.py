"""Hand-derived E34/Rplus six-path and symbolic family inclusions only."""
from pathlib import Path
from fractions import Fraction as F
import hashlib
import json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
helper=HERE/'critical-L-continuation-check.py'
source=helper.read_text()
exec(compile(source[:source.index('# Derived by hand:')],str(helper),'exec'),globals())
input_names=['surplus-four-local/e2-e1-b1/critical-L-continuation-check.py',
 'surplus-four-local/e2-e1-b1/critical-L-continuation-check.json',
 'surplus-four-local/e2-e1-b1/critical-L.txt',
 'surplus-four-local/e2-e1-b1/critical-L-continuation.txt',
 'fourth-surplus-review/peer-Bunit-six-independent/review.txt',
 'fourth-surplus-review/peer-Bunit-six-independent/check.json',
 'triangle-composition/inputs/guard_checker.py',
 'triangle-composition/inputs/boundary_replay.py',
 'triangle-composition/inputs/illumination_geometry.py',
 'triangle-composition/inputs/caps.json']
hashes={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in input_names}
prior=json.loads((HERE/'critical-L-continuation-check.json').read_text())
old=prior['centered_B_unit_Dminus_new6']
old_path=[tuple(map(F,p)) for p in old['path']]
d=F(1,6)
assert F(1,7)<d<F(1,5)
# Direct geometric derivation, also matched to the accepted sigma/reversal.
a=4/(1+d)
b=(4-8*d)/(1-d)
c=(2+6*d)/(1-d)
e=(2+14*d)/(1+d)
P=[(F(0),F(0)),(a,4-a),(4-4*d,F(0)),(b,4-b),
   (F(1),7*d),(c,c-2),(e,6-e),(F(2),F(2))]
assert P==sigma_path(old_path)
assert P==[(F(0),F(0)),(F(24,7),F(4,7)),(F(10,3),F(0)),
 (F(16,5),F(4,5)),(F(1),F(7,6)),(F(18,5),F(8,5)),
 (F(26,7),F(16,7)),(F(2),F(2))]
assert 0<3*d<5*d<1 and 1<7*d<2 and 1<9*d<2
assert 1<4-11*d<3 and 4-12*d==2
# Independent finite-wall and specular checks.
Rdiag=((3,1),(4,0)); Rfloor=((3,0),(4,0))
Tleft=((1,1),(1,2)); Elower=((3,1),(4,2)); Eupper=((4,2),(3,3))
mirrors=[Rdiag,Rfloor,Rdiag,Tleft,Elower,Eupper]
dot=lambda a,b:sum(x*y for x,y in zip(a,b))
contacts=[]
for i,((a,b),hit) in enumerate(zip(mirrors,P[1:-1]),1):
    edge=sub(b,a); u=dot(sub(hit,a),edge)/dot(edge,edge)
    assert cross(sub(hit,a),edge)==0 and 0<u<1,(i,hit,u)
    incoming,outgoing=sub(hit,P[i-1]),sub(P[i+1],hit)
    reflected=tuple(2*dot(incoming,edge)*edge[k]/dot(edge,edge)-incoming[k] for k in [0,1])
    assert cross(reflected,outgoing)==0 and dot(reflected,outgoing)>0,(i,hit)
    contacts.append({'point':list(map(str,hit)),'finite_mirror':[a,b],
                     'strict_parameter':str(u)})
for x,y,v in [(P[0],(F(3),3*d),(1,d)),
              ((F(3),3*d),P[1],(1,d)),
              (P[3],(F(3),5*d),(-1,d)),
              ((F(3),5*d),P[4],(-1,d)),
              (P[4],(F(3),9*d),(1,d)),
              ((F(3),9*d),P[5],(1,d)),
              (P[6],(F(3),4-11*d),(-1,-d)),
              ((F(3),4-11*d),P[-1],(-1,-d))]:
    delta=sub(y,x)
    assert cross(delta,v)==0 and dot(delta,v)>0
minimum=H|fan('E',[3,4])|{caps['R+']}
maximum=minimum|set().union(*(full(n) for n in ['L','B','Tc','D']))|fan('N',[0,1,2,3,4,5,6])
receipt=check_guard(P,minimum,maximum)
# The max/min themselves transform exactly, including all unit blockers.
assert minimum==transform(set(map(tri,old['minimum'])))
assert maximum==transform(set(map(tri,old['maximum'])))
assert set(map(tri,receipt['required']))==transform(set(map(tri,old['required'])))
assert set(map(tri,receipt['forbidden']))==transform(set(map(tri,old['forbidden'])))
q=(F(2),F(2))
for a,b in reversed(mirrors):
    edge=sub(b,a);delta=sub(q,a)
    q=tuple(a[k]+2*dot(delta,edge)*edge[k]/dot(edge,edge)-delta[k] for k in [0,1])
assert cross(q,(1,d))==0 and dot(q,(1,d))>0
# Named conditional-envelope inclusions only: no completed room assembled.
inclusions={}
for name,L,ordinary in [
 ('outside_L012_EC_Rplus',[0,1,2],['B+','T-','Nb-','R+']),
 ('outside_L0123_EC_Rplus',[0,1,2,3],['B+','T-','Nb-','R+']),
 ('outside_L7012_EC_Dminus_Rplus',[7,0,1,2],['B+','T-','Nb-','D-','R+']),
 ('outside_L7012_EC_Dplus_Rplus',[7,0,1,2],['B+','T-','Nb-','D+','R+']),
 ('inward_rectangle_EC_Nbminus_Dminus_Rplus',[6,7,0,1],['B+','T-','Nb-','D-','R+']),
 ('inward_upper_EC_Nbplus_Dminus_Rplus',[7,0,1],['B+','T-','Nb+','D-','R+']),
]:
    assert 'R+' in ordinary and 'Nr-' not in ordinary
    assert fan('L',L)<=maximum and all(caps[n] in maximum for n in ordinary)
    inclusions[name]={'status':'CONDITIONAL_WHOLE_ENVELOPE_INCLUSION_PASS',
                      'L_window':L,'E_window':[3,4],'ordinary_caps':ordinary,
                      'geometric_validity_or_case_completeness_claim':False}
Z=set(map(tri,receipt['forbidden']))
negative={}
for name,t in [('Nrminus',caps['Nr-']),('Rminus',caps['R-']),
               ('R2',next(iter(fan('R',[2])))),
               ('E2',next(iter(fan('E',[2])))),('E5',next(iter(fan('E',[5]))))]:
    assert t in Z,name
    negative[name]='REMOVES_REQUIRED_MIRROR'
assert len(Z)==5 and len(receipt['required'])==13
assert all(hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==h for n,h in hashes.items())
out={'status':'PARENT_CENTERED_E_RPLUS_CONDITIONAL_SIX_PATH_PASS',
 'hand_endpoint':'4-12d=2; d=1/6 in (1/7,1/5)',
 'whole_support':receipt,'strict_contacts':contacts,
 'actual_T_unfolded':list(map(str,q)),
 'accepted_Bunit6_sigma_reverse_exact_match':True,
 'conditional_inclusions':inclusions,'negative_controls':negative,
 'inward_necessary_descriptions_before':11,'inward_necessary_descriptions_after':9,
 'source_hashes':hashes,
 'limits':'Conditional optical implication and six symbolic inclusions, no case census or geometry construction; two inward descriptions removed relative to previous list, whose completeness remains independently unreviewed. Shared historical geometry helpers. Independent review pending. No room/cap/ray/direction/word discovery, archives, solver, orbit or workers.'}
(HERE/'centered-E-outside-C-check.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'])
print('6 strict contacts; full13U/5Z; firstactualT/reverse/sigma; actualT unfolds',q)
print('Six conditional inclusions PASS; inward necessary frontier11 ->9 relative to prior list.')
