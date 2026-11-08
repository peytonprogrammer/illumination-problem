"""Re-evaluate the fixed central-circle controls, without discovering rays/rooms."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent

def component(x,q):
    x=x%1
    assert x not in (q,1-q)
    return q<x<1-q

rows=[]
for a,d,q in product([F(1,7),F(2,5)],[F(1,6),F(3,8)],[F(1,8),F(1,4),F(3,8)]):
    Z={q,1-q}; X={a,(-a)%1}; Y={d,(-d)%1}
    if (X|Y)&Z:continue
    if not all(component(x,q)!=component(y,q) for x,y in product(X,Y)):continue
    residuals=sorted({(2*z-x-y)%1 for x,y,z in product(X,Y,Z)})
    midpoint=F(0) in residuals
    rows.append({'source':str(a),'target':str(d),'blocker':str(q),
                 'all_source_images':sorted(map(str,X)),
                 'all_target_images':sorted(map(str,Y)),
                 'both_blockers':sorted(map(str,Z)),
                 'every_source_target_arc_meets_a_blocker':True,
                 'has_midpoint_for_any_lift_sign':midpoint,
                 'midpoint_residuals_mod_one':list(map(str,residuals))})
assert len(rows)==3
assert all(not row['has_midpoint_for_any_lift_sign'] for row in rows)
# Positive control: the physical six-wall example's normalized core parameters.
X={F(1,8),F(7,8)};Y={F(3,8),F(5,8)};Z={F(1,4),F(3,4)}
assert all(component(x,F(1,4))!=component(y,F(1,4)) for x,y in product(X,Y))
assert any((2*z-x-y)%1==0 for x,y,z in product(X,Y,Z))
out={'status':'PASS','fixed_obstructions':rows,'six_wall_midpoint_control':'PASS',
     'scope':'Abstract invariant-cylinder core circles only; no polygon-realization or globally essential blocker claim; no ray search.'}
(ROOT/'check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
