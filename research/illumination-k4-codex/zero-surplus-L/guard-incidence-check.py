"""Static incidence of 16 explicitly listed cap options with two saved guards."""
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
def tri(*points):
    return tuple(sorted(points))
def triangles(raw):
    return frozenset(tuple(sorted(map(tuple,t))) for t in raw)
slots = {}
for label,a,c,b in (
    ('L-',(-2,0),(-1,0),(-1,-1)), ('L+',(-2,0),(-1,0),(-1,1)),
    ('B-',(0,-2),(0,-1),(-1,-1)), ('B+',(0,-2),(0,-1),(1,-1)),
    ('D-',(2,-2),(2,-1),(1,-1)), ('D+',(2,-2),(2,-1),(3,-1)),
    ('R-',(4,0),(3,0),(3,-1)), ('R+',(4,0),(3,0),(3,1)),
    ('E-',(4,2),(3,2),(3,1)), ('E+',(4,2),(3,2),(3,3)),
    ('T-',(2,4),(2,3),(1,3)), ('T+',(2,4),(2,3),(3,3)),
    ('Nb-',(0,2),(0,1),(-1,1)), ('Nb+',(0,2),(0,1),(1,1)),
    ('Nr-',(0,2),(1,2),(1,1)), ('Nr+',(0,2),(1,2),(1,3))):
    slots[label] = tri(a,c,b)
ten = json.loads((ROOT/'exception-geometry/cap-continuation-check.json').read_text())
thirteen = json.loads((ROOT/'cap-return-review/verify.json').read_text())
rows = {}
expected = {
    'ten': {'requires':['L+','E-'], 'forbids':['B-','D-','D+','R-','Nb-','E+','L-']},
    'thirteen': {'requires':['B+','T-'], 'forbids':['L-','B-','Nb-','Nb+','T+']},
}
for name,need,absent in (
    ('ten',triangles(ten['required']),triangles(ten['forbidden'])),
    ('thirteen',triangles(thirteen['required_tiles']),triangles(thirteen['forbidden_tiles']))):
    requires = sorted(label for label,t in slots.items() if t in need)
    forbids = sorted(label for label,t in slots.items() if t in absent)
    assert requires == sorted(expected[name]['requires']), (name,requires)
    assert forbids == sorted(expected[name]['forbids']), (name,forbids)
    fixed = json.loads((ROOT/'cap-return-review/lookup.json').read_text())
    core = triangles(fixed['room']) - frozenset(slots[label] for label in ('L+','B+','E-','T-'))
    assert len(core)==24
    assert need - core == frozenset(slots[label] for label in requires)
    rows[name] = dict(requires=requires,forbids=forbids,
                     required_tiles_outside_core=len(need-core),
                     forbidden_tile_count=len(absent))
def sigma(p):
    return 2-p[1],2-p[0]
sig_need = frozenset(tuple(sorted(sigma(v) for v in t)) for t in triangles(thirteen['required_tiles']))
sig_absent = frozenset(tuple(sorted(sigma(v) for v in t)) for t in triangles(thirteen['forbidden_tiles']))
assert frozenset(tuple(sorted(sigma(v) for v in t)) for t in core) == core
requires = sorted(label for label,t in slots.items() if t in sig_need)
forbids = sorted(label for label,t in slots.items() if t in sig_absent)
assert requires == ['E-','L+']
assert forbids == ['E+','L-','Nr+','Nr-','T+']
assert sig_need-core == frozenset(slots[label] for label in requires)
rows['sigma_thirteen'] = dict(requires=requires,forbids=forbids)
base = {'L+','B+','E-','T-'}
# The opposite caps in those four cells are excluded by the one-cap rule;
# Nb- and Nr+ are excluded by the no-smooth-B rule with L+ and T-.
available = {'D-','D+','R-','R+','Nb+','Nr-'}
original_blockers = available & set(rows['thirteen']['forbids'])
sigma_blockers = available & set(rows['sigma_thirteen']['forbids'])
assert original_blockers == {'Nb+'} and sigma_blockers == {'Nr-'}
assert not base & set(rows['thirteen']['forbids'])
assert not base & set(rows['sigma_thirteen']['forbids'])
assert set(rows['thirteen']['requires']) <= base
assert set(rows['sigma_thirteen']['requires']) <= base
assert all(next(v for v in slots[label] if v[0]%2 == v[1]%2 == 0) == (0,2)
           for label in ('Nb+','Nr-'))
result = dict(status='PASS',cap_options=slots,guards=rows,
              subfamily_cover=dict(base_caps=sorted(base),available_extra_caps=sorted(available),
                                   original_blockers=sorted(original_blockers),sigma_blockers=sorted(sigma_blockers),
                                   reason='Both blockers occupy the same NW A cell; equality permits at most one unless the direct bridge lights the marks.'),
              scope='Static16cap-option comparison with two saved exact guards, no room or path enumeration.')
(HERE/'guard-incidence-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(rows,indent=2))
