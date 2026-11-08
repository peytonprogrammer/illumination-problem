"""Exact local diagnostics; no ray or room search and no darkness claim."""
from fractions import Fraction as F
from pathlib import Path
import json
B=Path(__file__).resolve().parent
h=F(1,100)
c=(-h,F(0));s=(c[0]-h*h,c[1]-2*h*h);t=(F(2),F(1))
# Local sector [0, 3pi/2]: forbidden fourth quadrant relative to c.
d=(t[0]-s[0],t[1]-s[1])
# Intersect positive local x= h^2 / 10. The segment lies in the missing quadrant.
lam=(c[0]+h*h/10-s[0])/d[0]
p=tuple(s[j]+lam*d[j] for j in (0,1))
assert 0<lam<1 and p[0]>c[0] and p[1]<c[1]
# Fixed-origin s angle is near pi, actual corner-relative angle is pi+atan(2).
# psi=atan(1/2): fixed-origin difference <pi, local difference >pi.
assert s[0]<0 and s[1]<0 and abs(s[1]/s[0])<F(1,2)
assert F(2)>F(1,2)
vs=[(0,0),(2,0),(2,1),(2+h,1),(2+h,2),(0,2)]
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def sub(a,b):return (a[0]-b[0],a[1]-b[1])
def corners(v):return [v[i] for i in range(len(v)) if cross(sub(v[i],v[i-1]),sub(v[(i+1)%len(v)],v[i]))]
assert len(corners(vs))==6
limit=[(0,0),(2,0),(2,1),(2,2),(0,2)]
assert len(corners(limit))==4
out={'status':'PASS','moving_corner':{'epsilon':str(h),'corner':list(map(str,c)),'source':list(map(str,s)),'target':list(map(str,t)),'forbidden_point_on_prescribed_segment':list(map(str,p)),'conclusion':'Fixed-origin angle test accepts, but the prescribed segment exits the moving reflex sector. This refutes that proof step, not room illumination by another word.'},'smooth_step_collapse':{'before_walls':6,'after_maximal_walls':4,'merged_angle':'pi','conclusion':'One short horizontal step collapses; vertical neighbors merge. No notch is present and maximal wall count drops by two.'},'scope':'Deterministic exact local geometry only. No dark sequence, optical search, global exclusion or counterexample to global illumination is asserted.'}
(B/'other-degenerations-check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
