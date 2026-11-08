"""Two hand-derived roof paths and one retained path; no room/path search."""
from pathlib import Path
from fractions import Fraction as F
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / 'triangle-composition/inputs'))
from guard_checker import path_requirements
from boundary_replay import cross, sub, on

dirs = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
centers = {'L':(-2,0),'B':(0,-2),'D':(2,-2),'R':(4,0),
           'E':(4,2),'Tc':(2,4),'N':(0,2)}
tri = lambda t: tuple(sorted(map(tuple,t)))
def fan_at(c, ss):
    return {tri((c, (c[0]+dirs[i][0],c[1]+dirs[i][1]),
                    (c[0]+dirs[(i+1)%8][0],c[1]+dirs[(i+1)%8][1]))) for i in ss}
def fan(n, ss): return fan_at(centers[n],ss)
def full(n): return fan(n,range(8))
H = set().union(*(fan_at(c,range(8)) for c in [(0,0),(2,0),(2,2)]))
caps = {n:tri(t) for n,t in json.loads((ROOT/'triangle-composition/inputs/caps.json').read_text())['cap_options'].items()}
sigma = lambda p: (2-p[1],2-p[0])
def transform(ts): return {tri(sigma(p) for p in t) for t in ts}
def sigma_path(P): return [sigma(p) for p in reversed(P)]

def check_guard(P, minimum, maximum):
    assert P[0] == (0,0) and P[-1] == (2,2)
    assert minimum <= maximum
    U,Z = path_requirements(P)
    assert U <= minimum, ('missing support', U-minimum)
    assert not Z & maximum, ('mirror removed', Z&maximum)
    for a,b in zip(P[:-2],P[1:-1]): assert not on((2,2),a,b)
    Us,Zs = path_requirements(sigma_path(P))
    assert Us == transform(U) and Zs == transform(Z)
    # Reversal checks the very same actual endpoints and physical mirrors.
    Ur,Zr = path_requirements(list(reversed(P)))
    assert Ur == U and Zr == Z
    return {'status':'PASS', 'reflections':len(P)-2,
            'path':[[str(x) for x in p] for p in P],
            'required':sorted(U), 'forbidden':sorted(Z),
            'minimum':sorted(minimum), 'maximum':sorted(maximum),
            'first_actual_T':'PASS','reverse':'PASS','sigma':'PASS'}

# Derived by hand: N56 roof entry -d, exit 3d; bare U floor x=5d;
# final actual-target equation 8d=2. Only this forced rational root is checked.
d = F(1,4)
assert 0 < d < F(1,3)
entry = (-d,F(1))
exitpoint = (3*d,F(1))
left = (-2*d/(1+d), 2-2*d/(1+d))
right = (2*d/(1-d), 2-2*d/(1-d))
floor = (5*d,F(-1))
P = [(F(0),F(0)),left,right,floor,(F(2),F(2))]
assert left == (F(-2,5),F(8,5))
assert right == (F(2,3),F(4,3))
assert 0 < -left[0] < 1 and 0 < right[0] < 1
assert -1 < entry[0] < 1 and -1 < exitpoint[0] < 1
assert 1 < floor[0] < 2 and 8*d == 2
for a,b,v in [(P[0],entry,(-d,1)),(entry,left,(-d,1)),
              (left,right,(1,-d)),(right,exitpoint,(d,-1)),
              (exitpoint,floor,(d,-1)),(floor,P[-1],(d,1))]:
    delta = sub(b,a)
    assert cross(delta,v) == 0 and sum(x*y for x,y in zip(delta,v)) > 0

N = fan('N',[5,6])
minimum = H|N
maximum = minimum|set().union(*(full(n) for n in ['L','B','E','Tc','R']))|(full('D')-{caps['D-']})
new = check_guard(P,minimum,maximum)
assert caps['D-'] in {tri(t) for t in new['forbidden']}

# Reverse the three actual wall reflections to unfold T, not another A mark.
q = (F(2),F(2))
q = (q[0],-2-q[1])           # y=-1
q = (2-q[1],2-q[0])         # y=-x+2
q = (q[1]-2,q[0]+2)         # y=x+2
assert q == (-2,8) and cross(q,(-1,4)) == 0

# Complementary, already retained six-path. Read only its named coordinates;
# independently recompute the support rather than execute the prior checker.
prior_path = HERE/'critical-L-check.json'
prior = json.loads(prior_path.read_text())
assert prior['status'] == 'PARENT_CRITICAL_L_INWARD_FORMS_PARTIAL_COVER_CHECKS_PASS'
P6 = [tuple(map(F,p)) for p in prior['new_roof_Dcap_composition']['path']]
minimum6 = H|N|{caps['D-']}
maximum6 = minimum6|{caps['B+']}|set().union(*(full(n) for n in ['L','E','Tc','R']))
old = check_guard(P6,minimum6,maximum6)
assert len(P6)-2 == 6

# A single explicit conditional cover, with arbitrary subsets in the named
# maxima. No completed rooms or D/R cap assignments are generated.
assert N <= minimum and N <= minimum6
assert all(full(n) <= maximum and full(n) <= maximum6 for n in ['L','E','Tc','R'])
assert caps['B+'] in maximum and caps['B+'] in maximum6
assert caps['D+'] in maximum and caps['D-'] in maximum6

# A separate declared hand composition for the CENTERED B UNIT (not a
# larger e2 B root). Its two-diagonal bottom roof and flat S ceiling
# reach exactly the retained D- portal state when d=1/6.
db = F(1,6)
assert F(1,7) < db < F(1,5)
PB = [(F(0),F(0)),(F(-2,7),F(-12,7)),(F(2,5),F(-8,5)),
      (F(5,6),F(1)),(F(6,5),F(-6,5)),(F(2),F(-4,3)),
      (F(10,7),F(-10,7)),(F(2),F(2))]
assert PB[1] == (-2*db/(1+db),-2+2*db/(1+db))
assert PB[2] == (2*db/(1-db),-2+2*db/(1-db))
assert 12*db == 2 and 0 < 5*db < 1
for a,b,v in [(PB[0],(-db,F(-1)),(-db,-1)),
              ((-db,F(-1)),PB[1],(-db,-1)),
              (PB[1],PB[2],(1,db)),
              (PB[2],(3*db,F(-1)),(db,1)),
              ((3*db,F(-1)),PB[3],(db,1)),
              (PB[3],(7*db,F(-1)),(db,-1)),
              ((7*db,F(-1)),PB[4],(db,-1)),
              (PB[6],(9*db,F(-1)),(db,1)),
              ((9*db,F(-1)),PB[-1],(db,1))]:
    delta = sub(b,a)
    assert cross(delta,v) == 0 and sum(x*y for x,y in zip(delta,v)) > 0
minimumB = H|fan('B',[1,2])|{caps['D-']}
maximumB = minimumB|set().union(*(full(n) for n in ['L','E','Tc','R']))|fan('N',[0,1,2,3,4,5,7])
bottom = check_guard(PB,minimumB,maximumB)
assert len(PB)-2 == 6
qb = (F(2),F(2))
for reflect in [lambda p:(-p[1],-p[0]),lambda p:(4-p[0],p[1]),
                lambda p:(-p[1],-p[0]),lambda p:(p[0],2-p[1]),
                lambda p:(p[1]+2,p[0]-2),lambda p:(-p[1]-2,-p[0]-2)]:
    qb = reflect(qb)
assert qb == (-2,-12) and cross(qb,(-1,-6)) == 0

out = {'status':'PARENT_ENTIRE_CENTERED_N_CRITICAL_L_COVER_PASS',
       'absent_Dminus_new3':new, 'present_Dminus_retained6':old,
       'centered_B_unit_Dminus_new6':bottom,
       'inward_necessary_descriptions_remaining_up_to_sigma':11,
       'inward_necessary_split':{'lower_Bcenter':1,'lower_Bouter':4,
                               'rectangle_Ecenter':2,'upper_Ecenter':4},
       'centered_B_unit_derivation':{'d':str(db),'strict_interval':['1/7','1/5'],
          'B_roof_exit':['3d','-1'],'S_ceiling':['5d','1'],
          'Dminus_entry':['7d','-1'],'Dminus_exit':['9d','-1'],
          'actual_T_equation':'12d=2','unfolded_actual_T':list(map(str,qb))},
       'new3_derivation':{'d':str(d),'strict_interval':['0','1/3'],
          'roof_entry':list(map(str,entry)),'roof_exit':list(map(str,exitpoint)),
          'floor':list(map(str,floor)),'actual_T_equation':'8d=2',
          'unfolded_actual_T':list(map(str,q))},
       'scope':'Entire N56 unit partner for all seven critical L roots in e2+e1+b1, ordinary B+ and ordinary/empty D. If D- absent use3; if present use6. No W/k bound used for this optical implication. All L/E/Tc/R additions within local K are permitted. Sigma gives N70 and critical Tc.',
       'limits':'Parent hand proof and exact support checks; independent review pending. No whole critical-L or e2+e1+b1 theorem. No completed-room construction, room census, ray/direction/word discovery or workers.',
       'input_hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in [prior_path,ROOT/'triangle-composition/inputs/guard_checker.py',ROOT/'triangle-composition/inputs/boundary_replay.py',ROOT/'triangle-composition/inputs/caps.json']}}
(HERE/'critical-L-continuation-check.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'])
print('NEW3 + retained6 full U/Z, first actual T, reversal, sigma PASS; entire centered-N critical-L partner covered <=6.')
print('NEW centered-B-unit/Dminus6 full guard PASS; inward necessary descriptions reduced 13 to 11.')
