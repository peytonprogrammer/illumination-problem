"""One hand-declared 19-contact path; no trajectory or room discovery."""
from pathlib import Path
from fractions import Fraction as F
import hashlib
import json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
helper=HERE/'critical-L-continuation-check.py'
source=helper.read_text()
# Load only our existing definitions; execute none of its prior path checks.
exec(compile(source[:source.index('# Derived by hand:')],str(helper),'exec'),globals())
inputs=[helper, ROOT/'triangle-composition/inputs/guard_checker.py',
        ROOT/'triangle-composition/inputs/boundary_replay.py',
        ROOT/'triangle-composition/inputs/illumination_geometry.py',
        ROOT/'triangle-composition/inputs/caps.json']
hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
d=F(3,20)
assert F(4,27)<d<F(2,13) and F(1,7)<d<F(1,6)
ld=lambda x:(x,x+2)
dd=lambda x:(x,x-4)
rd=lambda x:(x,4-x)
P=[(F(0),F(0)),
   (-2*d/(1+d),-2/(1+d)), (2*d/(1-d),-2+2*d/(1-d)),
   (5*d,F(1)),(7*d,F(-1)),
   ld(10*d/(1-d)),(F(2),2+12*d),ld(14*d/(1+d)),
   dd(20*d/(1+d)),(F(2),18*d-4),dd(16*d/(1-d)),
   rd(24*d/(1+d)),ld((2-24*d)/(1-d)),
   (F(-2),26-4/d),(27*d-6,F(-1)),ld((-6+30*d)/(1-d)),
   rd((8-30*d)/(1+d)),dd((8-38*d)/(1-d)),
   (F(2),4-36*d),dd((8-34*d)/(1+d)),(F(2),F(2))]
assert len(P)-2==19 and 8-40*d==2
Bleft=((-1,-1),(0,-2)); Bright=((0,-2),(1,-1))
Tcdiag=((1,3),(2,4)); Tcaxis=((2,3),(2,4))
Ddiag=((2,-2),(3,-1)); Daxis=((2,-2),(2,-1))
Rdiag=((3,1),(4,0)); Ldiag=((-2,0),(-1,1))
mirrors=[Bleft,Bright,((0,1),(1,1)),((1,-1),(2,-1)),
         Tcdiag,Tcaxis,Tcdiag,Ddiag,Daxis,Ddiag,Rdiag,Ldiag,
         ((-2,-1),(-2,0)),((-2,-1),(-1,-1)),Ldiag,Rdiag,
         Ddiag,Daxis,Ddiag]
dot=lambda a,b:sum(x*y for x,y in zip(a,b))
contacts=[]
for i,((a,b),hit) in enumerate(zip(mirrors,P[1:-1]),1):
    edge=sub(b,a); u=dot(sub(hit,a),edge)/dot(edge,edge)
    assert cross(sub(hit,a),edge)==0 and 0<u<1,(i,hit,u)
    incoming,outgoing=sub(hit,P[i-1]),sub(P[i+1],hit)
    reflected=tuple(2*dot(incoming,edge)*edge[k]/dot(edge,edge)-incoming[k] for k in [0,1])
    assert cross(reflected,outgoing)==0 and dot(reflected,outgoing)>0,(i,hit)
    contacts.append({'contact':i,'point':list(map(str,hit)),
                     'finite_mirror':[a,b],'strict_parameter':str(u)})
# Stated conditional envelopes; no completed room or boundary assembled.
minimum=H|fan('L',[6,7,0])|fan('B',[1,2])|{caps[n] for n in ['T-','D+','R+']}
maximum=minimum|{caps[n] for n in ['E-','Nb-']}
U,Z=path_requirements(P)
missing=U-minimum
blocked=Z&maximum
assert missing=={caps['R-']},missing
assert not blocked,blocked
corner=(F(3),F(0))
assert on(corner,P[10],P[11]) and corner not in [P[10],P[11]]
assert 3/d-20==0
# The first R+ inlet is strict only when 3/d-20>0, i.e. d<3/20.
assert not d<F(3,20)
receipt={'status':'REJECTED_TRUE_INTERMEDIATE_CORNER',
         'path':[[str(x) for x in p] for p in P],
         'required':sorted(U),'forbidden':sorted(Z),
         'minimum':sorted(minimum),'maximum':sorted(maximum),
         'missing_required':sorted(missing),'blocked_mirrors':sorted(blocked),
         'corner':['3','0'],'corner_on_open_segment_after_contact':10,
         'strict_Rplus_entry':'3/d-20>0 requires d<3/20; target forces equality',
         'physical_or_family_acceptance':False}
q=(F(2),F(2))
for a,b in reversed(mirrors):
    edge=sub(b,a);delta=sub(q,a)
    q=tuple(a[k]+2*dot(delta,edge)*edge[k]/dot(edge,edge)-delta[k] for k in [0,1])
assert cross(q,(-d,-1))==0 and dot(q,(-d,-1))>0,q
assert all(hashlib.sha256(p.read_bytes()).hexdigest()==hashes[str(p.relative_to(ROOT))] for p in inputs)
out={'status':'RETIRED_CENTERED_B_NO_DMINUS_HAND_CIRCUIT_CORNER_OBSTRUCTION',
     'hand_endpoint':'8-40d=2 => d=3/20; L-square branch allows it, but strict first R+ inlet requires d<3/20',
     'whole_support':receipt,'strict_contacts':contacts,
     'unfolded_actual_T':list(map(str,q)),
     'inward_necessary_descriptions_before':11,
     'inward_necessary_descriptions_after':11,
     'source_hashes':hashes,
     'limits':'One hand-derived candidate rejected; no illumination closure or darkness assertion. Finite reflection contacts alone pass, but intermediate corner violates open-segment interior. No completed room, cap census, discovery, archive, workers or peer checker execution. Outside-C partners remain unresolved; shared historical helpers.'}
(HERE/'centered-B-no-Dminus-check.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'])
print('REJECTED: open segment after contact10 passes (3,0); missing required Rminus. Endpoint unfolding',q,'does not establish a physical path. Unresolved count remains11.')
