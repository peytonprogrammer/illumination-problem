#!/usr/bin/env python3
"""Exact finite cone-star symmetry replay, in units of pi/2; no room search."""
from pathlib import Path
import hashlib,json
base=Path(__file__).parents[1];author=base/'construction'
request=json.loads((author/'dark-interception-axis-midpoint-review-request.json').read_text())
pins={n:{'expected':p,'actual':hashlib.sha256((author/n).read_bytes()).hexdigest()} for n,p in request['source_pins'].items()}
assert all(a['actual']==a['expected'] for a in pins.values())
def h(j):return -j%12
def v(j):return (6-j)%12
fixed={j for j in range(12) if h(j)==j or v(j)==j}
assert fixed=={0,3,6,9}
rows=[]
for j in range(12):
    for turn in [-2,2]:
        k=(j+turn)%12
        if j in fixed or k in fixed:
            result='boundary-fixed prong excludes actual interior endpoint'
        else:
            witnesses=[name for name,op in [('h',h),('v',v)] if op(j)==k]
            assert len(witnesses)==1
            result=witnesses[0]
        rows.append({'first_prong':j,'second_prong':k,'signed_pi_turn':turn//2,'classification':result})
# Nonaxial pi/4 germ in units pi/4: opposite pi-separated germ is not in
# the four-element physical deck orbit. No nonaxial extension is justified.
nonaxial_orbit=sorted({1,(-1)%24,(12-1)%24,(1+12)%24})
assert 5 not in nonaxial_orbit
out={'status':'PASS','angle_units':'pi/2 mod12','source_pin_checks':pins,'fixed_axis_prongs':sorted(fixed),'rows':rows,'nonaxial_pi_over_four_orbit_units_pi_over_four':nonaxial_orbit,'nonaxial_pi_separated_prong':5,'nonaxial_orbit_rule_does_not_extend':True,'search_used':False,'whole_goal_complete':False}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'PASS','local_cases':len(rows),'author_pins_pass':True,'search_used':False}))
