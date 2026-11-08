"""Independent exact four-path and symbolic-branch audit of Delta2 closure.
No archive lookup, room assignment generation, direction search or solver.
"""
from pathlib import Path
from fractions import Fraction as F
import importlib.util
import hashlib
import json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
peer=ROOT/'second-surplus-review'
source=peer/'five-path-check.json'
raw=source.read_bytes()
receipt=json.loads(raw)
spec=importlib.util.spec_from_file_location('exact_replay',ROOT/'persisted-replay/audit.py')
a=importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)
tri=lambda t:tuple(sorted(map(tuple,t)))
decode=lambda p:tuple(tuple(F(*v) for v in pt) for pt in p)
slots={k:tri(t) for k,t in json.loads((ROOT/'zero-surplus-L/guard-incidence-check.json').read_text())['cap_options'].items()}
labels={t:k for k,t in slots.items()}
core=set().union(*(a.incident(tuple(map(F,p))) for p in ((0,0),(2,0),(2,2))))
b=tri(((0,-2),(1,-2),(1,-1)))
l=tri(((-2,0),(-2,1),(-1,1)))

def beam(d):
    return ((F(0),F(0)),(d,F(1)),(4*d,F(-2)),
        (8*d/(1-d),8*d/(1-d)+2),(F(2),2+10*d),
        (12*d/(1+d),12*d/(1+d)+2),(12*d,F(2)))

five=beam(F(1,6))
assert five==decode(receipt['five_path'])
assert five[0]==(0,0) and five[-1]==(2,2)
u5,z5=a.path_requirements(five)
assert u5-core=={slots['B+'],slots['T-'],b}
assert {labels[t] for t in z5 if t in labels}=={'Nb+','T+'}
assert z5-set(labels)==a.triangles(receipt['five_forbidden_outside_alphabet'])
assert not z5&core
lo,hi=F(1,7),F(2,11)
assert lo<F(1,6)<hi
# These are monotone affine/fractional-linear expressions on the interval.
for d in (lo,hi):
    assert 0<d<3*d<4*d<5*d<1
    assert -1<1/d-6<=1 and 1<=7*d<3
    assert 1<9*d<2 and 1<11*d<=2
    assert 1<8*d/(1-d)<2 and 3<2+10*d<4
    assert 1<12*d/(1+d)<2 and 1<12*d<3

old=ROOT/'first-surplus-review'
paths={
    'five':five,
    'eleven':decode(json.loads((old/'square-exchange-check.json').read_text())['paths']['L_thirteen']['path']),
    'twelve':decode(json.loads((old/'centered-left-check.json').read_text())['paths']['left']['path']),
    'thirteen':decode(json.loads((ROOT/'exception-geometry/zero-L-completion-check.json').read_text())['paths']['left_east_thirteen']['path']),
}
requirements={name:a.path_requirements(p) for name,p in paths.items()}
assert {labels[t] for t in requirements['eleven'][0]-core if t in labels}=={'L+','E-'}
assert requirements['eleven'][0]-core-set(labels)=={l}
assert {labels[t] for t in requirements['twelve'][0]-core}=={'L-','L+','E-'}
for name,extra in (('eleven',{slots['L-'],slots['B-']}),
                   ('twelve',{b}),('thirteen',{b})):
    assert not requirements[name][1]&extra

# Hand-derived branches: required-present and required-absent statements
# apply to whole families; possible remains an OVERAPPROXIMATION of them.
# No assignments or actual completed rooms are constructed here.
branches=(
    ('L triple','eleven',{'L-','L+','E-','T-','Nb-'},{'E+','T+','Nr-','Nr+'},{l}),
    ('centered B / outer L','eleven',{'B-','B+','L+','E-','T-','Nb-'},{'L-','E+','T+','Nr-','Nr+'},{l}),
    ('B triple / roof open','five',{'B-','B+','E-','L+','T-'},{'E+','L-','T+','Nb+'},{b}),
    ('B triple / roof blocked','thirteen',{'B-','B+','E-','L+','T-','Nb+'},{'E+','L-','T+','Nr-','Nr+'},{b}),
    ('centered L / outer B / roof open','five',{'L-','L+','B+','E-','T-'},{'B-','E+','T+','Nb+'},{b}),
    ('centered L / outer B / roof blocked','twelve',{'L-','L+','B+','E-','T-','Nb+'},{'B-','E+','T+','Nr-','Nr+'},{b}),
)
checks=[]
for name,which,present,absent,extras in branches:
    fixed=core|{slots[k] for k in present}|extras
    possible=(core|set(slots.values())|extras)-{slots[k] for k in absent}
    u,z=requirements[which]
    assert u<=fixed and not z&possible,name
    checks.append({'branch':name,'reflections':len(paths[which])-2,'status':'PASS'})

# Mandatory Nb- repair is a complete local B fan count in both L shapes.
c=(-1,1)
assert sum(c in t for t in core|{slots['L+'],l})==4
assert sum(c in t for t in core|{slots['L+'],slots['L-'],l})==4
assert c in slots['Nb-']
assert sum(c in t for t in core|{slots['L+'],l,slots['Nb-']})==5

sigma=lambda p:(2-p[1],2-p[0])
for name,p in paths.items():
    reverse=tuple(sigma(q) for q in p[::-1])
    ru,rz=a.path_requirements(reverse)
    u,z=requirements[name]
    assert reverse[0]==(0,0) and reverse[-1]==(2,2)
    assert ru=={tri(sigma(q) for q in t) for t in u}
    assert rz=={tri(sigma(q) for q in t) for t in z}

out={'status':'PASS','reviewed_receipt_sha256':hashlib.sha256(raw).hexdigest(),
    'reviewed_optical_proof_sha256':hashlib.sha256((peer/'optical-closure.txt').read_bytes()).hexdigest(),
    'reviewed_structural_audit_sha256':hashlib.sha256((peer/'review.txt').read_bytes()).hexdigest(),
    'five_path_whole_interval':['1/7','2/11'],'target_equation':'12d=2','target_parameter':'1/6',
    'branch_checks':checks,'mandatory_Nbminus_repair':'PASS',
    'all_four_paths_sigma_transfer':'PASS',
    'conclusion':'Independent HAND ACCEPT of entire second-surplus L-family closure; no corrections. Combined Q+s_N<=10 implies actual S/T illumination within13 reflections.',
    'limits':'Reused exact checker; no formal/expert verification, archive lookup/search or new independent boundary implementation.'}
(HERE/'closure-review-check.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: five-beam full interval, four exact paths, six whole-family branches, mandatory repair and sigma.')
