"""Exact check of one hand-derived healed-C path and old fallback."""
from fractions import Fraction as F
from pathlib import Path
import json,runpy
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
checker=runpy.run_path(str(ROOT/'lower-bound-proof-audit/full-replay/guard-checker.py'))
tri=lambda t:tuple(sorted(map(tuple,t)))
slots={n:tri(t) for n,t in json.loads((ROOT/'zero-surplus-L/guard-incidence-check.json').read_text())['cap_options'].items()}
labels={t:n for n,t in slots.items()}
core=frozenset().union(*(checker['incident']((F(x),F(y))) for x,y in ((0,0),(2,0),(2,2))))
l=tri(((-2,0),(-2,1),(-1,1)));c=tri(((-2,0),(-2,1),(-3,1)))
remote=[tri(((-2,2),(-2,1),(x,1))) for x in (-3,-1)]
d=F(2,13)
path=[(F(0),F(0)),(-2/(1-d),2*d/(1-d)),(-2-3*d,F(1)),(-2*(1+3*d)/(1+d),4*d/(1+d)),((2+6*d)/(1-d),8*d/(1-d)),(2+10*d,F(2)),((2+14*d)/(1+d),12*d/(1+d))]
# E-third-contact y = x-2 =12d/(1+d).
# Upper square: unfolded horizontal distances measured from E exit (3,11d).
for length in [F(2),F(4),F(6),F(8),F(17,2),F(10),F(12),F(14),F(15)]:
 phase=length%4;x=3-phase if phase<=2 else phase-1
 unfolded=11*d+d*length;y=unfolded if unfolded<=3 else 6-unfolded
 path.append((x,y))
assert len(path)-2==14 and path[-1]==(2,2)
# The hand candidate is expected to fail: record the exact contradictory guard.
u=set();z=set()
for a,b in zip(path,path[1:]):u.update(checker['segment'](a,b))
for prev,p,nxt in zip(path,path[1:],path[2:]):
 used,absent=checker['bounce'](prev,p,nxt);u.update(used);z.update(absent)
conflict=u&z
assert conflict=={slots['Nr-']},conflict
segments=[i for i,(a,b) in enumerate(zip(path,path[1:])) if checker['segment'](a,b)&conflict]
assert segments==[3]
# Entire simple upper-chamber return is impossible, by the two strict bounds.
# Legal H transit demands d<1/7; next E-side reflection demands d>2/15.
# Target before first downward exit needs d=1/n or2/n, n positive integer.
# The open interval (2/15,1/7) lies strictly between adjacent possibilities.
assert F(1,8)<F(2,15)<F(1,7)
assert F(2,15)<F(2,14)==F(1,7)
raw=json.loads((ROOT/'zero-surplus-L/cover-check.json').read_text())['paths']['thirteen']['path']
old=[tuple(F(*v) for v in p) for p in raw];uo,zo=checker['path_requirements'](old)
forced=core|{slots[n] for n in ['L+','B+','E-','T-']}|{l,c}
oldpossible=core|set(slots.values())|{l,c}|set(remote)
oldpossible-={slots[n] for n in ['L-','B-','E+','T+','Nb-','Nb+']}
assert uo<=forced and not zo&oldpossible
result={'check_status':'PASS_EXPECTED_REJECTION','candidate_valid':False,'Nb_absent_old13_guard':'PASS',
 'candidate_reflections':14,'candidate_d':'2/13',
 'conflicting_triangle':slots['Nr-'],'conflicting_open_segment_indices':segments,
 'failure':'Candidate needs Nr- on L-to-E transit but forbids it on a later upper-chamber reflection.',
 'strict_same_branch_interval':'2/15<d<1/7',
 'target_before_lower_portal_exit':'d=1/n or d=2/n for a positive integer n; neither occurs in the strict interval',
 'scope':'One rejected analytic candidate and arithmetic obstruction to its simple upper-chamber continuation. Not a darkness result or a discovery search.'}
(HERE/'healed-c-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
