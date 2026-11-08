"""B02 prescribed exact chordgate and coefficient checks; not a triangulation census."""
from fractions import Fraction as Q
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parent;P=R.parent/'construction';rows=[]
for u,v,r,s,want in [(1,2,3,1,'inside'),(-3,2,-1,1,'left'),(5,2,9,1,'right'),(-2,2,1,1,'left-equality'),(2,2,5,1,'right-equality')]:
 u,v,r,s=map(Q,(u,v,r,s));L=Q(4);c=(s*u+v*r)/(v+s);t=v/(v+s)
 assert (u+t*(r-u),v+t*(-s-v))==(c,0)
 category='inside' if 0<c<L else 'left-equality' if c==0 else 'right-equality' if c==L else 'left' if c<0 else 'right'
 assert category==want;rows.append({'u':str(u),'v':str(v),'r':str(r),'s':str(s),'L':str(L),'c':str(c),'category':category})
# Universal algebra: E=3(2g-2+z)+6q, totalm<=q(W-2)/2.
# Check all stated finiteW/q budget coefficients, not a geometry inventory.
for q in [4,8]:
 for W in range(3,22):
  Ebound=Q(3*q*(W+2),2);Fbound=q*(W+2);assert Ebound<=276 and Fbound<=184
sources={f:hashlib.sha256((P/f).read_bytes()).hexdigest() for f in ['global-separator-assessment.md','global-separator-source-screen.json']}
assert sources['global-separator-assessment.md']=='0208710719ac9882c146e4fb5d1cfad4e7b8543da4fe0be473dc54f34da654f7'
out={'status':'EXACT_LOCAL_GATE_EQUALITY_AND_COMPLEXITY_COEFFICIENT_CHECKS_PASS','whole_goal_complete':False,'author_code_executed':False,'triangulation_enumerated':False,'source_sha256':sources,'rows':rows,'max_E':276,'max_F':184}
(R/'global-separator-independent-check.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
