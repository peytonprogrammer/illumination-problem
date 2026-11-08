"""Accepted opposite-side path plus a withdrawn formal end-leaf control.

The end-leaf algebra does not represent a raw room: its assumed fixed
central flank contradicts raw B incidence. No discovery or scans.
"""
from fractions import Fraction as F
from pathlib import Path
from math import gcd
import json
base=Path(__file__).resolve().parent
def p(x,y):return (F(x),F(y))
def sub(a,b):return (a[0]-b[0],a[1]-b[1])
def add(a,b):return (a[0]+b[0],a[1]+b[1])
def mul(k,a):return (k*a[0],k*a[1])
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def det(a,b):return a[0]*b[1]-a[1]*b[0]
def ref(a,n,c):return sub(a,mul(2*(dot(n,a)-c)/dot(n,n),n))
def refv(v,n):return ref(v,n,F(0))
def horizontal(y):return (p(0,1),F(y))
def vertical(x):return (p(1,0),F(x))
S=p(0,0);T=p(4,0);H1=horizontal(1)
cases=[dict(name='opposite_right_portal',corner=p(5,-1),w=p(5,3),
 first=[S,p(F(5,3),1),p(5,-1)],first_times=[F(1,3),F(2,3)],
 corner_mirror=horizontal(-1),
 second=[p(5,-1),p(6,F(-2,5)),p(F(16,3),0),p(F(11,3),-1),p(3,F(-3,5)),T],
 second_times=[F(1,5),F(2,15),F(1,3),F(2,15),F(1,5)],
 mirrors=[vertical(6),horizontal(0),horizontal(-1),vertical(3)],
 u=p(1,0),corner_image=p(5,3),target_image=p(10,6),Q=p(-2,0)),
 dict(name='upper_end_left_portal',corner=p(5,0),w=p(5,2),
 first=[S,p(F(5,2),1),p(5,0)],first_times=[F(1,2),F(1,2)],
 corner_mirror=vertical(5),
 second=[p(5,0),p(3,F(-4,5)),p(F(7,2),-1),p(5,F(-2,5)),T],
 second_times=[F(2,5),F(1,10),F(3,10),F(1,5)],
 mirrors=[vertical(3),horizontal(-1),vertical(5)],
 u=p(0,1),corner_image=p(5,2),target_image=p(10,4),Q=p(0,2))]
receipts=[]
for c in cases:
 w=c['w'];assert gcd(int(w[0]),int(w[1]))==1
 v=w
 assert c['first'][0]==S and c['first'][-1]==c['corner']
 assert sum(c['first_times'])==1
 for i,t in enumerate(c['first_times']):
  assert sub(c['first'][i+1],c['first'][i])==mul(t,v)
  if i==0:
   hit=c['first'][i+1];assert hit[1]==1 and hit[0].denominator>1
   assert 1<hit[0]<2 if c['name'].startswith('opposite') else 2<hit[0]<3
   v=refv(v,H1[0])
 v=refv(v,c['corner_mirror'][0])
 assert sum(c['second_times'])==1
 for i,t in enumerate(c['second_times']):
  assert t>0 and sub(c['second'][i+1],c['second'][i])==mul(t,v)
  if i<len(c['mirrors']):
   n,offset=c['mirrors'][i];hit=c['second'][i+1]
   assert dot(n,hit)==offset
   assert hit[0].denominator>1 or hit[1].denominator>1
   if n==p(0,1):
    if offset==-1:assert 3<hit[0]<4
    else:assert 5<hit[0]<6
   else:assert -1<hit[1]<0
   v=refv(v,n)
 assert c['second'][-1]==T
 assert all(3<=x<=6 and -1<=y<=0 for x,y in c['second'])
 if c['name'].startswith('upper_end'):
  assert all(x<=5 for x,y in c['second'])
 else:
  # First-half crossing into the full target square occurs before y=0.
  assert add(c['first'][1],mul(F(4,15),p(5,-3)))==p(3,F(1,5))
  # Second-half return through the supplied lower right portal.
  assert add(c['second'][2],mul(F(1,15),p(-5,-3)))==p(5,F(-1,5))
 image=T
 all_mirrors=[H1,c['corner_mirror']]+c['mirrors']
 for n,offset in reversed(all_mirrors):image=ref(image,n,offset)
 corner_image=ref(c['corner'],*H1)
 assert image==c['target_image'] and corner_image==c['corner_image']
 assert sub(corner_image,S)==sub(image,corner_image)==w
 # Fixed supporting lines; corner velocity must be developed by prefix.
 developed_velocity=refv(c['u'],H1[0]);Q=mul(-2,developed_velocity)
 assert Q==c['Q'] and det(w,Q)!=0
 receipts.append(dict(name=c['name'],geometry_status=('ACCEPTED_CONDITIONAL' if c['name'].startswith('opposite') else 'WITHDRAWN_INCOMPATIBLE_RAW_PREMISES_FORMAL_ONLY'),first=c['first'],second=c['second'],
  half_vector=w,actual_target=T,developed_corner=corner_image,
  developed_actual_target=image,defect=Q,determinant=det(w,Q)))
out=dict(status='OPPOSITE_PRESCRIBED_PATH_PASS_END_CONTROL_FORMAL_ONLY',cases=receipts,
 proof_scope='Opposite-side case with fixed left central flank accepted; end-leaf computation FORMAL ONLY, incompatible raw premise.',
 independent_review='OPPOSITE_ACCEPTED_END_WITHDRAWN',universal_detection='OPEN',optical_discovery_runs=0)
(base/'pocket-opposite.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps(out,indent=2,default=str))
