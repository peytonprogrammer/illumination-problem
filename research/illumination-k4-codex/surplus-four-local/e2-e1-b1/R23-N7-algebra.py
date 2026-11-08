"""Fixed hand-derived transport identities only; no optical or room search."""
from fractions import Fraction as F
from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent
# Polynomials in the one hand parameter d, constant coefficient first.
def add(a,b):
 n=max(len(a),len(b));r=[F(0)]*n
 for i in range(n):r[i]=(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0)
 while len(r)>1 and not r[-1]:r.pop()
 return r
def neg(a):return [-x for x in a]
def ev(a,d):return sum(v*d**i for i,v in enumerate(a))
# N normal3: a=(2-12d)/(1-d); top=a(1-d); c=top/(1+d).
# Exit y=2+d-(1+d)c=13d, then target height atx2=14d.
normal_n=[F(2),F(-12)];normal_den=[F(1),F(-1)]
assert add([F(2),F(1)],neg(normal_n))==[F(0),F(13)]
normal_endpoint=[F(0),F(14)]
# Ceiling-first4: first ceiling x=12-2/d, diagonal b=(12d-2)/(1+d),
# second ceiling x=b(1+d), final diagonal c=(12d-2)/(1-d).
# Exit y=2-d-(1-d)c=4-13d, endpoint atx2=4-14d.
four_n=[F(-2),F(12)]
assert add([F(2),F(-1)],neg(four_n))==[F(4),F(-13)]
four_endpoint=[F(4),F(-14)]
root=F(1,7)
assert ev(normal_endpoint,root)==ev(four_endpoint,root)==2
normal_gate=(F(1,7),F(2,13));four_gate=(F(1,6),F(2,11))
assert root==normal_gate[0] and root<four_gate[0]
# E first diagonal x=(2+4d)/(1-d), y=x-2; at the root this is (3,1).
ex=(2+4*root)/(1-root);assert (ex,ex-2)==(3,1) and 7*root==1
rays=((1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1))
def fan(a,ss):return {tuple(sorted((a,(a[0]+rays[i][0],a[1]+rays[i][1]),(a[0]+rays[(i+1)%8][0],a[1]+rays[(i+1)%8][1])))) for i in ss}
def angle(ts,p):
 result=0
 for t in ts:
  if p in t:
   a,b=[(q[0]-p[0],q[1]-p[1]) for q in t if q!=p]
   result+=90 if a[0]*b[0]+a[1]*b[1]==0 else 45
 return result
p=(3,1);H=set().union(*(fan(a,range(8)) for a in [(0,0),(2,0),(2,2)]))
parts={'H':angle(H,p),'R23':angle(fan((4,0),[2,3]),p),'E4':angle(fan((4,2),[4]),p)}
assert parts=={'H':180,'R23':90,'E4':45} and sum(parts.values())==315
for a,ss in [((0,-2),[6,7,0,1]),((-2,0),[0]),((0,2),[7])]:assert angle(fan(a,ss),p)==0
# D and Tc are empty by the accepted R23 b1 budget, not a new room choice.
source=HERE/'joined-top-absent.txt'
out={'status':'TWO_HAND_CONTINUATIONS_RETIRED','local_family':'O3/O4 + R23, ordinary L0/E4/N7, D/Tc empty; inherited necessary table only','normal3':{'N7_exit':'(1,13d), velocity(1,d)','target_height':'14d','strict_gate':list(map(str,normal_gate)),'root':str(root),'obstruction':'earlier E4 inlet (3,1), true315 corner'},'ceiling_first4':{'N7_exit':'(1,4-13d), velocity(1,-d)','target_height':'4-14d','strict_gate':list(map(str,four_gate)),'root':str(root),'obstruction':'root below ceiling-first gate; same earlier E inlet at root'},'corner_local_degrees':parts,'source_sha256':{str(source):hashlib.sha256(source.read_bytes()).hexdigest()},'limits':'Algebra for two analytically prescribed continuations and one local angle sum only. No new room, sample directions, word enumeration, physical replay or complete U/Z certificate. Other N7 transport branches and other paths are not exhausted. No darkness or closure claim.'}
(HERE/'R23-N7-algebra.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS algebra: both endpoint equations force d1/7 outside strict gates; earlier E inlet is a genuine315 corner. No new optical closure.')
