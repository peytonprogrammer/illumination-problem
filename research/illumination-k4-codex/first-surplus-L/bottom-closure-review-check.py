"""Independent exact replay of the peer's ONE supplied six-reflection path.
No guard archive lookup, projection, room assignments or direction search.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import importlib.util
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
source = ROOT/'first-surplus-review/bottom-residual-check.json'
data = source.read_bytes()
peer = json.loads(data)
spec = importlib.util.spec_from_file_location('exact_replay',ROOT/'persisted-replay/audit.py')
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)
tri = lambda t:tuple(sorted(map(tuple,t)))
caps = {k:tri(t) for k,t in json.loads((ROOT/'zero-surplus-L/guard-incidence-check.json').read_text())['cap_options'].items()}
labels = {t:k for k,t in caps.items()}
core = set().union(*(a.incident(tuple(map(F,p))) for p in ((0,0),(2,0),(2,2))))
path = tuple(tuple(F(*v) for v in p) for p in peer['path'])
expected = ((0,0),(-F(1,6),1),(-F(4,7),-F(10,7)),
    (F(4,5),-F(6,5)),(F(8,5),F(18,5)),(2,F(11,3)),
    (F(12,7),F(26,7)),(2,2))
assert path == expected
u,z = a.path_requirements(path)
assert {labels[t] for t in u-core} == {'B-','B+','T-'}
assert {labels[t] for t in z if t in labels} == {'Nb-','T+'}
assert z-set(labels) == a.triangles(peer['forbidden_outside_alphabet'])
assert not z&core
assert len(z-set(labels)) == 3
assert len(path)-2 == 6

def family(d):
    return ((F(0),F(0)),(-d,F(1)),
        (-4*d/(1+d),4*d/(1+d)-2),
        (4*d/(1-d),4*d/(1-d)-2),
        (8*d/(1-d),8*d/(1-d)+2),
        (F(2),2+10*d),
        (12*d/(1+d),12*d/(1+d)+2),(12*d,F(2)))

d = F(1,6)
assert family(d) == path
lo,hi = F(1,7),F(2,11)
assert lo<d<hi<F(1,5)
# Every expression is affine or fractional-linear and monotone here.
# Exact endpoint bounds certify the hand-stated full open beam interval.
for t in (lo,hi):
    assert -1 < -t < 0
    assert -1 < -3*t < 0 and -1 < -5*t < 0
    assert -1 < -4*t/(1+t) < 0
    assert 0 < 4*t/(1-t) < 1
    assert 0 < 5*t < 1
    assert -1 < 1/t-6 <= 1
    assert 1 <= 7*t < 3
    assert 1 < 9*t < 2 and 1 < 11*t <= 2
    assert 1 < 8*t/(1-t) < 2
    assert 3 < 2+10*t < 4
    assert 1 < 12*t/(1+t) < 2
    assert 1 < 12*t < 3
assert 7*lo == 1 and 11*hi == 2

# Necessity of Nb- absence: H has two incident triangles at B=(-1,1);
# L+ and Nb- would make its fan four triangles, a smooth B prohibited
# in the centered defect branch (s_N=|M|, so no extra smooth B).
point = (-1,1)
assert sum(point in t for t in core) == 2
assert point in caps['L+'] and point in caps['Nb-']
assert sum(point in t for t in core|{caps['L+'],caps['Nb-']}) == 4

sigma = lambda p:(2-p[1],2-p[0])
reverse = tuple(sigma(p) for p in path[::-1])
ru,rz = a.path_requirements(reverse)
assert ru == {tri(sigma(p) for p in t) for t in u}
assert rz == {tri(sigma(p) for p in t) for t in z}
assert {labels[t] for t in ru-core} == {'E-','E+','L+'}
assert {labels[t] for t in rz if t in labels} == {'L-','Nr+'}

result = {'status':'PASS','reviewed_receipt_sha256':hashlib.sha256(data).hexdigest(),
    'supplied_path_reflections':6,'required_caps':['B-','B+','T-'],
    'forbidden_caps':['Nb-','T+'],
    'forbidden_outside_alphabet':sorted(z-set(labels)),
    'whole_parameter_interval':['1/7','2/11'],'actual_target_parameter':'1/6',
    'endpoint':'(12d,2)','no_smooth_B_Nbminus_exclusion':'PASS',
    'sigma_actual_endpoint_transfer':'PASS',
    'conclusion':'Independent hand review accepts entire centered bottom/east family closure. With accepted earlier branches, all fixed-I3-L rooms at Q+s_N<=9 illuminate within13reflections.',
    'limits':'Exact checker reused; no formal/expert verification or new independent boundary implementation; no archive lookup/search/solver.'}
for name in ('bottom-residual-cover.txt','first-layer-theorem.txt'):
    p = ROOT/'first-surplus-review'/name
    if p.exists():
        result[name+'_sha256'] = hashlib.sha256(p.read_bytes()).hexdigest()
(HERE/'bottom-closure-review-check.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS: supplied six-path, entire hand interval bounds, forced Nb- absence and sigma.')
