"""Independent Beast hand-reduction guards and ONE fixed four-path replay.

No peer checker, new room construction, assignment enumeration or ray search.
"""
from pathlib import Path
from fractions import Fraction as F
import ast
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
helper = ROOT/'surplus-four-local/mixed-root-leaf-review/check.py'
source = helper.read_text()
# Retained definitions only: geometry imports, canonical stars/caps, decoder.
exec(compile(source[:source.index('base7=')],str(helper),'exec'),globals())
definitions = [n for n in ast.parse(source).body
               if isinstance(n,ast.FunctionDef) and n.name in ['polygon','ledger']]
exec(compile(ast.Module(body=definitions,type_ignores=[]),str(helper),'exec'),globals())
from boundary_replay import on

inputs = [
 'fourth-surplus-review/mixed-e2-e1/critical-B.txt',
 'fourth-surplus-review/mixed-e2-e1/critical-B-check.json',
 'fourth-surplus-review/mixed-e2-e1/four-Beast-hand.txt',
 'fourth-surplus-review/mixed-e2-e1/four-Beast-hand-check.json',
 'second-surplus-review/five-path-check.json',
 'zero-surplus-L/cover-check.json',
 'first-surplus-review/square-exchange-check.json',
 'first-surplus-review/bottom-residual-check.json',
 'first-surplus-review/residual-cover-check.json',
 'third-surplus-review/local-three-unit-check.json',
 'third-surplus-review/independent-review/guard-extension-check.json',
 'surplus-four-local/mixed-critical-B-review/review.txt',
 'surplus-four-local/mixed-root-leaf-review/check.py',
 'triangle-composition/inputs/guard_checker.py',
 'triangle-composition/inputs/boundary_replay.py',
 'triangle-composition/inputs/illumination_geometry.py',
 'triangle-composition/inputs/caps.json',
]
hashes = {f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in inputs}
sig = lambda P:[sigma(p) for p in P[::-1]]

def whole_guard(name,P,minimum,maximum):
    assert P[0] == (0,0) and P[-1] == (2,2),name
    assert minimum <= maximum,name
    U,Z = path_requirements(P)
    assert U <= minimum,(name,'required',U-minimum)
    assert not Z&maximum,(name,'forbidden',Z&maximum)
    for a,b in zip(P[:-2],P[1:-1]): assert not on((2,2),a,b),name
    Ur,Zr = path_requirements(P[::-1])
    Us,Zs = path_requirements(sig(P))
    assert (Ur,Zr) == (U,Z) and (Us,Zs) == (tr(U),tr(Z)),name
    return {'status':'PASS','reflections':len(P)-2,
            'minimum':sorted(minimum),'maximum':sorted(maximum),
            'required':sorted(U),'forbidden':sorted(Z),
            'first_actual_T_reverse_sigma':'PASS'}

five = decode(read('second-surplus-review/five-path-check.json')['five_path'])
assert five == [(0,0),(F(1,6),1),(F(2,3),-2),(F(8,5),F(18,5)),
                (2,F(11,3)),(F(12,7),F(26,7)),(2,2)]
axis = lambda p:(4-p[0],p[1])
P = [(F(0),F(0)),(F(1,6),F(1)),(F(2,3),F(-2)),
     (F(8,5),F(18,5)),(F(16,7),F(26,7)),(F(2),F(2))]
assert P == five[:4]+[axis(five[-2]),axis(five[-1])]
assert axis((2,2)) == (2,2)
assert on(five[-3],P[3],P[4]) and five[-3] not in [P[3],P[4]]

# Independent finite-wall directions, using the declared roof/square circuit.
mirrors = [((0,1),(1,1)),((0,-2),(1,-2)),
           ((1,3),(2,4)),((2,4),(3,3))]
dot = lambda a,b:sum(x*y for x,y in zip(a,b))
contact_rows = []
for i,((a,b),hit) in enumerate(zip(mirrors,P[1:-1]),1):
    edge = sub(b,a)
    u = dot(sub(hit,a),edge)/dot(edge,edge)
    assert cross(sub(hit,a),edge) == 0 and 0 < u < 1
    incoming,outgoing = sub(hit,P[i-1]),sub(P[i+1],hit)
    reflected = tuple(2*dot(incoming,edge)*edge[k]/dot(edge,edge)-incoming[k]
                      for k in [0,1])
    assert cross(reflected,outgoing) == 0 and dot(reflected,outgoing) > 0
    contact_rows.append({'point':list(map(str,hit)),'finite_mirror':[a,b],
                         'strict_parameter':str(u)})

d = F(1,6)
assert F(1,7) < d < F(1,5)
assert 0 < 3*d < 4*d < 5*d < 1 and 7*d > 1
a = 8*d/(1-d); b = (4-8*d)/(1+d)
assert 1 < a < 2 and 2 < b < 3
assert P[1] == (d,1) and P[2] == (4*d,-2)
assert P[3] == (a,a+2) and P[4] == (b,6-b)
assert (1+d)*b-4*d == 4-12*d == 2

BCore = H|fan('B',[0,1,2])
LO,LC = fan('L',[0,1]),fan('L',[7,0])
EO,EC = fan('E',[4,5]),fan('E',[3,4])
TO,TC = fan('Tc',[4,5]),fan('Tc',[5,6])
NB,DR = fan('N',[4,5,6]),full('D')|full('R')
minimum = BCore|EO|TC|C(['L+','Nr-'])
maximum = minimum|C(['D-','D+','R-','R+'])
four_guard = whole_guard('new_four_path',P,minimum,maximum)
peer = read('fourth-surplus-review/mixed-e2-e1/critical-B-check.json')
peer_path = read('fourth-surplus-review/mixed-e2-e1/four-Beast-hand-check.json')['new_four_reflection_certificate']
assert P == [tuple(map(F,p)) for p in peer_path['path']]
assert set(map(tri,peer_path['minimum'])) == minimum
assert set(map(tri,peer_path['maximum_all_four_caps'])) == maximum

def strictly_simple(V):
    edges = list(zip(V,V[1:]+V[:1]))
    for i,(a,b) in enumerate(edges):
        for j,(c,d) in enumerate(edges):
            if j <= i+1 or (i==0 and j==len(edges)-1): continue
            v,w,delta = sub(b,a),sub(d,c),sub(c,a)
            den = cross(v,w)
            if den:
                t,u = cross(delta,w)/den,cross(delta,v)/den
                assert not (0<=t<=1 and 0<=u<=1),(i,j)
            elif cross(delta,v)==0:
                t,u = F(dot(delta,v),dot(v,v)),F(dot(sub(d,a),v),dot(v,v))
                assert max(0,min(t,u)) > min(1,max(t,u)),(i,j)

physical = {}
for cap in ['D-','D+','R-','R+']:
    original = peer['Beast_four_declared_residuals'][cap]
    ts = set(map(tri,original['triangles']))
    # Read and match the four ORIGINAL controls; no new completions generated.
    assert ts == minimum|C([cap])
    V = polygon(ts)
    assert V == list(map(tuple,original['vertices']))
    strictly_simple(V)
    ld = ledger(ts)
    assert ld == original['ledger']
    assert ld == {'W':20,'k':6,'Q':10,'J':4,'sN':2,'Delta':4}
    assert replay(V,(0,0),(2,2),P) == 4
    assert replay(V,(2,2),(0,0),P[::-1]) == 4
    assert replay([sigma(p) for p in V],(0,0),(2,2),sig(P)) == 4
    # The omitted old vertical reflection is now strictly interior.
    assert not any(on(five[-3],x,y) for x,y in zip(V,V[1:]+V[:1]))
    qt = (F(2),F(2))
    for hit in reversed(P[1:-1]):
        walls = [(x,y) for x,y in zip(V,V[1:]+V[:1])
                 if on(hit,x,y) and hit not in (x,y)]
        assert len(walls) == 1
        x,y = walls[0]; edge = sub(y,x);delta = sub(qt,x)
        qt = tuple(x[k]+2*dot(delta,edge)*edge[k]/dot(edge,edge)-delta[k]
                   for k in [0,1])
    assert qt == (2,12) and cross(qt,(1,6)) == 0 and dot(qt,(1,6)) > 0
    physical[cap] = {'status':'PASS','ledger':ld,'reflections':4,
        'actual_first_T_finite_first_walls_interior_reverse_sigma':'PASS',
        'removed_axis_contact_is_interior':True,'unfolded_actual_T':['2','12']}

# Rebuild named inherited optical witnesses from accepted sources.
z = read('zero-surplus-L/cover-check.json')['paths']
f = read('third-surplus-review/independent-review/guard-extension-check.json')['forcing_paths']
sq = read('first-surplus-review/square-exchange-check.json')['paths']
B6 = decode(read('first-surplus-review/bottom-residual-check.json')['path'])
B4 = B6[:4]+[(F(5,3),F(4))]+B6[7:]
L3 = decode(read('first-surplus-review/residual-cover-check.json')['path'])
L11,E11 = decode(sq['L_thirteen']['path']),decode(sq['E_thirteen']['path'])
E6,T3,sigmaB4 = sig(B6),sig(L3),sig(B4)
F3 = decode(read('third-surplus-review/local-three-unit-check.json')['new_paths']['fiveTop3'])
double3 = [(F(0),F(0)),(F(-2),F(1,3)),(F(4),F(4,3)),(F(1),F(11,6)),(F(2),F(2))]
base = BCore|C(['L+','E-','T-'])
specs = [
 ('no_critical_notNbplus',five,base,base|DR|(full('N')-C(['Nb+']))),
 ('no_critical_Nbplus',decode(z['thirteen_sigma']['path']),base|C(['Nb+']),base|DR|NB),
 ('Louter_Eordinary',L11,BCore|LO|C(['E-','T-']),BCore|LO|C(['E-'])|TO|DR|NB),
 ('Louter_Eouter',double3,BCore|LO|EO|C(['T-']),BCore|LO|EO|DR|NB|full('Tc')),
 ('Louter_Ecenter',sigmaB4,BCore|LO|EC|C(['T-']),BCore|LO|EC|C(['T-'])|DR|NB),
 ('Tcenter_Eordinary',T3,BCore|TC|C(['E-']),H|TC|C(['E-'])|full('B')|full('L')|DR|full('N')),
 ('Ecenter_noncritical_notNbplus',five,BCore|EC|C(['L+','T-']),BCore|EC|C(['L+','T-'])|DR|(full('N')-C(['Nb+']))),
 ('Ecenter_noncritical_Nbplus',E6,BCore|EC|C(['L+','T-','Nb+']),BCore|EC|C(['L+','T-'])|DR|NB),
 ('Eouter_noncritical_notNbplus',five,BCore|EO|C(['L+','T-']),BCore|EO|C(['L+','T-'])|DR|(full('N')-C(['Nb+']))),
 ('Eouter_noncritical_Nbplus',E11,BCore|EO|C(['L+','T-','Nb+']),BCore|EO|C(['L+','T-'])|DR|NB),
 ('Touter_Eordinary',F3,BCore|TO|C(['L+','E-']),BCore|TO|C(['L+','E-'])|DR|(full('N')-C(['Nb+']))),
 ('Ecenter_Touter',F3,BCore|EC|TO|C(['L+']),BCore|EC|TO|C(['L+'])|DR|(full('N')-C(['Nb+']))),
 ('Eouter_Touter',F3,BCore|EO|TO|C(['L+']),BCore|EO|TO|C(['L+'])|DR|(full('N')-C(['Nb+']))),
 ('Eouter_Tcenter_notNrminus',sig(five),BCore|EO|TC|C(['L+']),BCore|EO|TC|C(['L+'])|DR|(full('N')-C(['Nr-']))),
]
guards = {name:whole_guard(name,path,mi,ma) for name,path,mi,ma in specs}
assert len(guards) == 14 and max(row['reflections'] for row in guards.values()) == 13
for name,row in peer['Beast_critical_guards'].items():
    own = guards[name]
    assert set(map(tri,row['minimum'])) == set(map(tri,own['minimum']))
    assert set(map(tri,row['maximum'])) == set(map(tri,own['maximum']))

allK = H|set().union(*(full(n) for n in centers))
forcing_specs = [
 ('force_Eminus',decode(z['one_sigma']['path']),H,allK-C(['E-'])),
 ('ordinary_E_force_Lplus',decode(z['four_sigma']['path']),H|C(['E-']),
  (allK-full('E')-C(['L+']))|C(['E-'])),
 ('center_E_force_Lplus',decode(f['sigma_centeredB3']['path']),H|EC,
  (allK-full('E')-C(['L+']))|EC),
 ('outer_E_force_Lplus',decode(f['sigma_outerB2']['path']),H|EO,
  (allK-full('E')-C(['L+']))|EO),
 ('Beast_force_Tminus',decode(f['outerB2']['path']),BCore,
  BCore|(allK-full('B')-C(['T-']))),
 ('Nbridge_lights_directly',[(F(0),F(0)),(F(2),F(2))],H|fan('N',[6,7]),allK),
]
forcing = {name:whole_guard(name,path,mi,ma) for name,path,mi,ma in forcing_specs}

# Local angle coefficients and root-fan exhaustion only, no room census.
def angle_info(ts,p):
    owners = g.owners_of(list(ts)); opens = {e for e,ii in owners.items() if len(ii)==2}
    aa,interior = g.check_fan_angles(list(ts),p,owners,opens)
    return ([45*a for a in aa],interior)

angles = {}
for name,ts,p,expected in [
 ('Lcenter_excluded',BCore|LC,(-1,-1),180),
 ('both_E_T_centered_excluded',BCore|EC|TC,(3,3),180),
 ('Louter_needs_N5',BCore|LO,(-1,1),180),
 ('Louter_repaired_N5',BCore|LO|C(['Nb-']),(-1,1),225),
 ('Touter_needs_N0',BCore|TO,(1,3),180),
 ('Touter_repaired_N0',BCore|TO|C(['Nr+']),(1,3),225),
 ('Tcenter_forbids_N0',BCore|TC|C(['Nr+']),(1,3),180),
]:
    assert angle_info(ts,p) == ([expected],False),(name,angle_info(ts,p))
    angles[name] = expected
for p,allowed in [((-1,-1),{'L','B'}),((3,3),{'E','Tc'}),
                  ((-1,1),{'L','N'}),((1,3),{'N','Tc'})]:
    assert all(p not in t for n in centers if n not in allowed for t in full(n))
assert {i for i in range(8) if any((-1,1) in t for t in fan('N',[i]))} == {4,5}
assert {i for i in range(8) if any((1,3) in t for t in fan('N',[i]))} == {0,1}
# Within the forced active N unit windows, only the stated repairs occur.
Nwindows = {'bottom_center':[5,6],'bottom_outer':[4,5],
            'right_center':[7,0],'right_outer':[0,1]}
assert all(5 in ss for ss in Nwindows.values() if any((-1,1) in t for t in fan('N',ss)))
assert all(0 in ss for ss in Nwindows.values() if any((1,3) in t for t in fan('N',ss)))
for h in range(8):
    ss={h,(h+1)%8}
    Hsides = int(bool(ss&{5,6}))+int(bool(ss&{7,0}))
    if Hsides == 1: assert sorted(ss) in [sorted(x) for x in Nwindows.values()]

# Count identities behind the forced four-control frontier.
J = 4; n = J-1; Q = 7+n; sN = 12-Q
assert (n,Q,sN,J+sN) == (3,10,2,6)
assert n-2 == 1      # L+ and Nr- leave exactly ONE D/R ordinary cap.

assert all(hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h for f,h in hashes.items()),'Input changed during review'
out = {'status':'INDEPENDENT_WHOLE_BEAST_BRANCH_HAND_ACCEPT_CHECKS_PASS',
 'new_four_reflections':four_guard,'strict_contacts':contact_rows,
 'endpoint_fixed_suffix':'x=2 fixes actual T; omitted contact lies on new interior segment',
 'analytic_root':'4-12d=2; d=1/6 in (1/7,1/5)',
 'four_original_physical_receipts':physical,'inherited_whole_guards':guards,
 'forcing_whole_guards':forcing,'local_angle_clauses':angles,
 'active_N_root_windows':Nwindows,'residual_budget':{'J':J,'n':n,'Q':Q,'sN':sN,'k':6},
 'whole_Beast_reflection_bound':13,'source_hashes':hashes,
 'limits':'Independent hand case-exhaustion in review.txt plus named support checks and ONE fixed4 path on four ORIGINAL rooms. Shared historical geometry helpers, not formal verification/expert refereeing. No peer checker executed, old20 replay, new rooms/cap assignments/rays/directions/words/archive/solver/workers. Other mixed and b1 branches remain separate.'}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'])
print('ONE new4path/four original rooms;14 inherited and6 forcing guards/sigma;7 local angles;J4/n3 PASS. Entire bounded Beast branch <=13.')
