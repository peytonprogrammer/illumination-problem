"""Replay the saved bottom-pair witness and check its old-path cover.

Fixed supplied paths and one analytic local substitution into the old
four-bounce beam; exact incidence and hand interval endpoints only.
No room/cap-assignment enumeration, direction/word search or archive lookup.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import importlib.util
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
spec = importlib.util.spec_from_file_location('exact_replay', ROOT/'persisted-replay/audit.py')
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)
source = ROOT/'exception-geometry/shared-extensions-check.json'
data = source.read_bytes()
saved = json.loads(data)
w = saved['rooms']['B_bottom_repair']['witness']
assert w['source_line'] == 167
assert saved['source_sha256'] == '8b68ec4bb37012e9c226c1bde8fa9e3c8e341e35cbcb7563f31b27c8a499c750'
tri = lambda t: tuple(sorted(map(tuple, t)))
caps = {name: tri(t) for name,t in json.loads((ROOT/'zero-surplus-L/guard-incidence-check.json').read_text())['cap_options'].items()}
labels = {t:name for name,t in caps.items()}
core = set().union(*(a.incident(tuple(map(F,p))) for p in ((0,0),(2,0),(2,2))))
path = tuple(tuple(F(*v) for v in p) for p in w['path'])
u,z = a.path_requirements(path)
assert u == a.triangles(w['required']) and z == a.triangles(w['forbidden'])
assert {labels[t] for t in u-core} == {'B-','B+','D-'}
assert {labels[t] for t in z if t in labels} == {'D+','R-','T+','Nb+'}
assert len(z-set(labels)) == 3
assert not z&core

def family(r):
    return ((F(0),F(0)), (-2*r/(1+r),-2/(1+r)),
        (2*r/(1-r),2*r/(1-r)-2), (5*r,F(1)),
        (6*r/(1-r),-6*r/(1-r)), (F(2),-8*r),
        (10*r/(1+r),-10*r/(1+r)), (13*r,F(3)),
        (F(3),16-3/r), (6-17*r,F(-1)),
        (6-21*r,F(3)), (6-22*r,F(2)))

r = F(2,11)
assert family(r) == path
assert path[0] == (0,0) and path[-1] == (2,2)
assert len(path)-2 == 10
lo,hi = F(3,17),F(3,16)
assert lo < r < hi
# Monotone affine or fractional-linear expressions: checking their interval
# endpoint values verifies these stated bounds throughout the open interval.
for t in (lo,hi):
    assert 0 < t < F(1,3)
    assert 0 < 3*t < 1 and 0 < 5*t < 1
    assert -1 < 6-1/t < 1
    assert 1 < 7*t < 2 and 1 < 9*t < 2
    assert 1 < 6*t/(1-t) < 2
    assert -2 < -8*t < -1
    assert 1 < 10*t/(1+t) < 2
    assert 1 < 11*t < 3 and 2 < 13*t < 3 and 2 < 15*t < 3
    assert -1 <= 16-3/t <= 0
    assert 2 <= 6-17*t <= 3
    assert 1 < 6-19*t < 3 and 2 < 6-21*t < 3
    assert 1 < 6-22*t < 3
assert 16-3/lo == -1 and 16-3/hi == 0
assert 6-17*lo == 3

# Recompute only the previously selected thirteen-bounce counterpart.
old_source = ROOT/'exception-geometry/zero-L-completion-check.json'
old = json.loads(old_source.read_text())['paths']['left_east_thirteen']
oldpath = tuple(tuple(F(*v) for v in p) for p in old['path'])
ou,oz = a.path_requirements(oldpath)
assert {labels[t] for t in ou-core} == {'L+','E-'}
assert {labels[t] for t in oz if t in labels} == {'L-','E+','T+','Nr-','Nr+'}
# Under B paired, E-/L+ forced: L-/E+ absent. If N is a right cap,
# it is neither Nb+ nor Nb-, so the new path has its source roof intact.
assert {caps['Nr-'],caps['Nr+']}.isdisjoint({caps['Nb+']})
assert caps['B-'] not in oz and caps['B+'] not in oz

sigma = lambda p: (2-p[1],2-p[0])
transform = lambda tiles: {tri(sigma(p) for p in t) for t in tiles}
reflected = tuple(sigma(p) for p in path[::-1])
ru,rz = a.path_requirements(reflected)
assert ru == transform(u) and rz == transform(z)
assert {labels[t] for t in ru-core} == {'E-','E+','R+'}
assert {labels[t] for t in rz if t in labels} == {'R-','D+','L-','Nr-'}

# The old single-cap launch(d,-1) and centered-cap launch(-d,-1)
# return to precisely (3d,-1), velocity(d,1). Replace the old first
# THREE cap reflections by TWO; preserve every point after cap exit.
def short_family(d):
    return ((F(0),F(0)), (-2*d/(1+d),-2/(1+d)),
        (2*d/(1-d),2*d/(1-d)-2), (7*d,F(3)), (8*d,F(2)))

d = F(1,4)
short = short_family(d)
su,sz = a.path_requirements(short)
assert {labels[t] for t in su-core} == {'B-','B+'}
assert {labels[t] for t in sz if t in labels} == {'T-'}
assert len(sz-set(labels)) == 2
assert short[0] == (0,0) and short[-1] == (2,2)
oldfour = json.loads(old_source.read_text())['paths']['bottom_cap_four']['path']
oldfour = tuple(tuple(F(*v) for v in p) for p in oldfour)
assert short[2:] == oldfour[3:]
assert F(1,5)<d<F(2,7)<F(1,3)
for t in (F(1,5),F(2,7)):
    assert 0<3*t<1 and -1<=1/t-4<=1
    assert 1<=5*t<3 and 1<7*t<=2 and 1<8*t<3
short_sigma = tuple(sigma(p) for p in short[::-1])
ssu,ssz = a.path_requirements(short_sigma)
assert ssu == transform(su) and ssz == transform(sz)
assert {labels[t] for t in ssu-core} == {'E-','E+'}
assert {labels[t] for t in ssz if t in labels} == {'L+'}
assert caps['Nr+'] not in su and caps['Nr-'] not in su

# One bounded analytic attempt at the now-forced Nr- cap, not a search.
# L+,E-,Nr- triple-return laws give exits y=3r,9r,13r.
# Their simultaneous strict branch interval is 1/7<r<2/13.
# The upper-left roof branch returns to height2 at x=22r-2,
# so its target equation r=2/11 lies OUTSIDE that branch interval.
# The upper-right roof branch, before the first descent to y2, has
# total horizontal travel 4/r in (26,80/3), containing no even integer.
nlo,nhi = F(1,7),F(2,13)
split = F(3,20)
assert nlo<split<nhi<F(2,11)
for t in (nlo,nhi):
    assert 0<t<F(1,3)
    assert 1<=7*t<2 and 9*t<2
    assert 1<11*t<2 and 13*t<=2
    assert 15*t>2 and 19*t<3 and 21*t>=3
    assert 1<=22-3/t<=F(5,2)
assert 4/nhi == 26 and 4/split == F(80,3)<28

result = {
    'status':'PASS', 'saved_witness_file':str(source),
    'saved_witness_sha256':hashlib.sha256(data).hexdigest(),
    'frozen_guard_source_sha256':saved['source_sha256'],
    'frozen_guard_line':167, 'reflections':10,
    'required_caps':sorted(labels[t] for t in u-core),
    'forbidden_caps':sorted(labels[t] for t in z if t in labels),
    'forbidden_outside_cap_alphabet':sorted(z-set(labels)),
    'parameter_interval':['3/17','3/16'], 'actual_target_parameter':'2/11',
    'target_expression':'(6-22r,2)',
    'bottom_two_hit_map':'(u,-1),(d,-1) -> (-u-2d,-1),(-d,1)',
    'bottom_two_hit_hypotheses':'-1<u<1, -1<u+2d<1, u+d!=0',
    'bottom_family_new_path':'D- and not Nb+ and not R- and not T+',
    'bottom_combined_sufficient':'not T+ and (N not in {Nr-,Nr+} or (D- and not R-))',
    'previous_necessary_residue_superseded':'T+ or (N in {Nr-,Nr+} and (not D- or R-))',
    'analytic_substitution_three_bounce':{
        'parameter':'1/4', 'interval':['1/5','2/7'], 'reflections':3,
        'required_caps':['B-','B+'], 'forbidden_caps':['T-'],
        'forbidden_outside_cap_alphabet':sorted(sz-set(labels)),
        'path':[[[v.numerator,v.denominator] for v in p] for p in short],
        'sigma_required_caps':['E-','E+'], 'sigma_forbidden_caps':['L+']},
    'bottom_forced_for_possible_darkness':['B-','B+','E-','L+','T-','Nr-'],
    'bottom_necessary_residue':'N=Nr- and (not D- or R-), after the forced caps',
    'east_necessary_residue':'N=Nb+ and (not R+ or D+), after sigma-transformed forced caps',
    'northwest_first_upper_pass':{
        'interval':['1/7','2/13'], 'roof_split':'3/20',
        'left_roof_height2_x':'22r-2; target needs r=2/11 outside interval',
        'right_roof_target_condition':'4/r even integer; 26<4/r<80/3<28, impossible',
        'conclusion':'This specified cap-return branch misses T on first upper passage; later passages unanalysed.'},
    'east_sigma_required_caps':sorted(labels[t] for t in ru-core),
    'east_sigma_forbidden_caps':sorted(labels[t] for t in rz if t in labels),
    'peer_left_hand_review':'ACCEPT paired-left.txt sections 1-5 as read before its second bounded attempt; shared tail independently derived here',
    'scope':'Fixed line167/reflected13 plus analytic two-for-three local substitution in old4beam. One bounded Nr- cap-return/first-upper-pass hand attempt; no assignments, parameter search, solver or archive lookup. Full paired-family closure remains open.'
}
(HERE/'paired-bottom-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ('status','reflections','required_caps','forbidden_caps','bottom_combined_sufficient','bottom_necessary_residue')},indent=2))
