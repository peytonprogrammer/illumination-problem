"""Exact prescribed physical realization of existing central-circle controls.

No reflection words, directions or rooms are discovered or searched.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
ROOM=[(F(0),F(0)),(F(6),F(0)),(F(6),F(3)),(F(5),F(3)),(F(5),F(4)),(F(0),F(4))]
C0=(F(0),F(0));C1=(F(6),F(0));Z=(F(3),F(4));REFLEX=(F(5),F(3))
PERIOD=(F(12),F(16))
sub=lambda a,b:(a[0]-b[0],a[1]-b[1])
dot=lambda a,b:a[0]*b[0]+a[1]*b[1]
cross=lambda a,b:a[0]*b[1]-a[1]*b[0]

def fold(t,L):
    t=t%(2*L)
    return t if t<=L else 2*L-t

def physical(theta):return (fold(12*theta,F(6)),fold(16*theta,F(4)))
def torus(p):return tuple(x%2 for x in p)
def fibers(p):return {torus((ex*p[0],ey*p[1])) for ex,ey in product((-1,1),repeat=2)}
def lower_window(p):return 0<p[0]<6 and 0<p[1]<3

def same_core_component(theta):
    theta%=1
    assert theta not in (F(1,4),F(3,4))
    return F(1,4)<theta<F(3,4)

def distance2(p,a,b):
    v=sub(b,a);lam=max(F(0),min(F(1),dot(sub(p,a),v)/dot(v,v)))
    foot=(a[0]+lam*v[0],a[1]+lam*v[1])
    return dot(sub(p,foot),sub(p,foot))

# The prescribed c0 -> z -> c1 arc and its reversed continuation.
vin=sub(Z,C0);vout=sub(C1,Z)
assert vout==(vin[0],-vin[1])
assert Z[0]<5  # Entire first leg lies left of the removed notch.
assert F(8)-F(4,3)*5==F(4,3)<3  # Second leg is below notch for x>=5.
clearances=[distance2(REFLEX,C0,Z),distance2(REFLEX,Z,C1)]
assert clearances==[F(5),F(1)]
assert physical(F(0))==physical(F(1))==C0
assert physical(F(1,2))==C1
assert physical(F(1,4))==physical(F(3,4))==Z
assert torus(PERIOD)==(0,0) and torus(tuple(c/2 for c in PERIOD))==(0,0)
assert torus(tuple(c/4 for c in PERIOD))!=(0,0)
turns=[cross(sub(ROOM[(i+1)%6],ROOM[i]),sub(ROOM[(i+2)%6],ROOM[(i+1)%6])) for i in range(6)]
assert sum(v<0 for v in turns)==1 and sum(v>0 for v in turns)==5

rows=[]
for a,d in [(F(1,7),F(3,8)),(F(2,5),F(1,6))]:
    s=physical(a);t=physical(d)
    assert lower_window(s) and lower_window(t) and s!=t
    source_core={a,(-a)%1};target_core={d,(-d)%1}
    assert all(physical(u)==s for u in source_core)
    assert all(physical(v)==t for v in target_core)
    assert all(same_core_component(u)!=same_core_component(v) for u,v in product(source_core,target_core))
    xs=fibers(s);ys=fibers(t);bs=fibers(Z)
    assert bs=={(F(1),F(0))}
    # Midpoint modulo half-periods on R^2 / 2Z^2 is 2b-x-y in 2Z^2.
    residues={torus((2*b[0]-x[0]-y[0],2*b[1]-x[1]-y[1])) for x,y,b in product(xs,ys,bs)}
    assert (F(0),F(0)) not in residues
    # The vertical coordinate alone excludes all midpoint choices.
    yres={r[1] for r in residues};assert F(0) not in yres
    rows.append({'source_core_parameter':a,'target_core_parameter':d,'source':s,'target':t,
                 'source_torus_images':sorted(xs),'target_torus_images':sorted(ys),
                 'blocker_torus_images':sorted(bs),'all_selected_core_arcs_blocked':True,
                 'torus_midpoint_for_any_lift':False,'vertical_midpoint_residues_mod_two':sorted(yres),
                 'ordinary_direct_bypass':True,'bypass_reason':'Both marks are in convex open lower rectangle (0,6)x(0,3), disjoint from z.'})

# The earlier physical control has a midpoint; the test must accept it.
s=physical(F(1,8));t=physical(F(3,8))
assert any(torus((2*b[0]-x[0]-y[0],2*b[1]-x[1]-y[1]))==(0,0)
           for x,y,b in product(fibers(s),fibers(t),fibers(Z)))
# The third abstract control's proposed blocker is interior, not a wall point.
assert physical(F(3,8))==(F(9,2),F(2)) and lower_window(physical(F(3,8)))
# Rational endpoint checks for a prescribed open family of mark placements.
family=[]
for a,d in product((F(2,15),F(1,7),F(1,6)),(F(1,3),F(3,8),F(5,12))):
    assert F(1,8)<a<F(3,16) and F(5,16)<d<F(7,16)
    assert lower_window(physical(a)) and lower_window(physical(d))
    assert same_core_component(a)!=same_core_component(d)
    midpoint=any(torus((2*b[0]-x[0]-y[0],2*b[1]-x[1]-y[1]))==(0,0) for x,y,b in product(fibers(physical(a)),fibers(physical(d)),fibers(Z)))
    assert midpoint==(a+d==F(1,2))
    family.append({'source_parameter':a,'target_parameter':d,'midpoint':midpoint})
out={'status':'PASS','room':ROOM,'blocker':Z,'developed_core_period':PERIOD,
     'minimum_squared_reflex_clearances':clearances,'fixed_physical_controls':rows,
     'old_midpoint_positive_control':'PASS','third_abstract_blocker_is_interior':True,
     'prescribed_open_family_controls':family,
     'scope':'Physical local core separation without torus midpoint; both rooms are the SAME fixed L and both pairs have direct bypasses. No global essential blocker or darkness claim.'}
(ROOT/'check.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps(out,indent=2,default=str))
