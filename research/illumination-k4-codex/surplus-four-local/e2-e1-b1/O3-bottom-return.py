"""Exact hand endpoint identities for one O3 pocket-return mechanism.
No room construction, trajectory search, parameter samples or word scan.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent
# Laurent expressions in d; derive the supplied continuous transport maps.
def add(*terms):
 out={}
 for term in terms:
  for k,v in term.items():out[k]=out.get(k,F(0))+v
 return {k:v for k,v in out.items() if v}
def scale(term,c):return {k:v*c for k,v in term.items() if v*c}
def shift(term,p):return {k+p:v for k,v in term.items()}
def const(n):return {0:F(n)} if n else {}
def at(term,d):return sum(v*d**k for k,v in term.items())
d={1:F(1)}
# Diagonal return Cx=(2-4d)/(1-d); subsequent vertical return
# has y=Cx/d-Cx-2=(2-4d)/d-2=2/d-6.
left_height=add(shift(add(const(2),scale(d,-4)),-1),const(-2))
assert left_height=={-1:F(2),0:F(-6)}
# Outgoing(d,1); x(y)=d*(y-left_height).
def xheight(y):return shift(add(const(y),scale(left_height,-1)),1)
direct=xheight(2);bare=add(xheight(3),d)
assert direct=={0:F(-2),1:F(8)} and bare=={0:F(-2),1:F(10)}
# Tc6 portal x=9d-2, local u=x-2=9d-4.
u=add(xheight(3),const(-2));assert u=={0:F(-4),1:F(9)}
# Normal triangle3 preserves tangent sign: u_out=u+2d.
top3=add(u,scale(d,2),const(2));end3=add(top3,d)
# Adjacent triangle4 reverses tangent sign: u_out=2-u-2d.
top4=add(const(4),scale(u,-1),scale(d,-2));end4=add(top4,scale(d,-1))
assert top3=={0:F(-2),1:F(11)} and end3=={0:F(-2),1:F(12)}
assert top4=={0:F(8),1:F(-11)} and end4=={0:F(8),1:F(-12)}
rows=[('direct',direct,F(1,2),(F(3,7),F(1,2))),
 ('bare_top',bare,F(2,5),(F(3,7),F(1,2))),
 ('Tc6_normal3',end3,F(1,3),(F(4,9),F(5,11))),
 ('Tc6_adjacent4',end4,F(1,2),(F(5,11),F(1,2)))]
for _,e,root,(lo,hi) in rows:assert at(e,root)==2 and not lo<root<hi
# Threshold Tc6 entry u>0: d>4/9. Triangle branch split u+2d=1:d5/11.
assert at(u,F(4,9))==0 and at(add(u,scale(d,2)),F(5,11))==1
# At normal3/four split the return contact is exactly the triangle base corner.
assert F(3,7)<F(4,9)<F(5,11)<F(1,2)
# Critical original lower-pocket events, not an assembled room/replay.
assert (2-4*F(1,2))/(1-F(1,2))==0
assert at(left_height,F(2,5))==-1
rays=((1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1))
def fan(a,ss):return {tuple(sorted((a,(a[0]+rays[i][0],a[1]+rays[i][1]),(a[0]+rays[(i+1)%8][0],a[1]+rays[(i+1)%8][1])))) for i in ss}
def angle(ts,p):
 result=0
 for t in ts:
  if p in t:
   a,b=[(q[0]-p[0],q[1]-p[1]) for q in t if q!=p]
   result+=90 if a[0]*b[0]+a[1]*b[1]==0 else 45
 return result
H=set().union(*(fan(a,range(8)) for a in [(0,0),(2,0),(2,2)]));B=fan((0,-2),[7,0,1])
assert angle(B,(0,-2))==135 and angle(H|B,(0,-1))==270
for a in [(-2,0),(2,-2),(4,0),(4,2),(2,4),(0,2)]:
 for p in [(0,-2),(0,-1)]:assert angle(fan(a,range(8)),p)==0
sources=[HERE/'O4-smooth-three.txt',HERE/'joined-top-absent.txt']
out={'status':'O3_RESTRICTED_BOTTOM_RETURN_MECHANISM_REJECTED','tested_premise':'Replace only O4 lower square by O3 triangular pocket, then direct target or one ordinary top-return can close O3.','branches':[{'suffix':name,'endpoint_x_at_y2':{str(k):str(v) for k,v in e.items()},'target_root':str(root),'strict_gate':list(map(str,gate))} for name,e,root,gate in rows],'decisive_corners':{'(0,-2)':135,'(0,-1)':270},'source_sha256':{str(p.relative_to(HERE.parent.parent)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},'limits':'One prescribed lower-pocket word, interval3/7<d<1/2, direct or first roof return only. Tcempty/6 dispatch within that motif, not exhaustive trajectories or O3 rooms. No discovery, room, samples, word enumeration, optical replay or full U/Z. Parent hand obstruction, not independent review or darkness proof.'}
(HERE/'O3-bottom-return.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: four analytic suffix equations; all target roots outside strict gates. O3 apex135 / upper-left portal270 unhealable by otherK stars. Restricted mechanism rejected; O3 still open.')
