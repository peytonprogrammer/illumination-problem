"""Two predeclared symbolic support implications; no room or path discovery."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
sys.path.insert(0,str(ROOT/'triangle-composition/inputs'))
from guard_checker import path_requirements
source=ROOT/'fourth-surplus-review/single-room-search/verification.json'
r=json.loads(source.read_text())
P=[tuple(F(x) for x in p) for p in r['path']]
assert P[0]==(0,0) and P[-1]==(2,2) and len(P)-2==9
U,Z=path_requirements(P)
dirs=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
centers={'L':(-2,0),'B':(0,-2),'D':(2,-2),'R':(4,0),'E':(4,2),'Tc':(2,4),'N':(0,2)}
def fan(site,ss):
 a=centers[site] if isinstance(site,str) else site
 return {tuple(sorted((a,(a[0]+dirs[i%8][0],a[1]+dirs[i%8][1]),(a[0]+dirs[(i+1)%8][0],a[1]+dirs[(i+1)%8][1])))) for i in ss}
def decode(ts):return {tuple(sorted(map(tuple,t))) for t in ts}
H=set().union(*(fan(a,range(8)) for a in [(0,0),(2,0),(2,2)]))
base=H|fan('L',[7,0])|fan('E',[3,4])|fan('Tc',[5])|fan('N',[6])|fan('D',[2])
assert U==decode(r['whole_family']['required']) and Z==decode(r['whole_family']['forbidden'])
family={}
# EXACTLY two declared envelopes, R entirely free. No completed room tested.
for label,sectors in [('west',[1,2,3]),('rectangle',[0,1,2,3])]:
 minimum=base|fan('B',sectors)
 maximum=minimum|fan('R',range(8))
 assert U<=minimum and not Z&maximum
 family[label]={'minimum':sorted(minimum),'maximum':sorted(maximum),'status':'WHOLE_SUPPORT_PASS','R':'arbitrary within full star','reflections':9}
# The claimed unrestricted extension fails at these specific added mirrors.
blockers={f'{site}{sector}':sorted(Z&fan(site,[sector])) for site,sector in [('N',5),('N',7),('D',1),('D',3),('Tc',6)]}
assert all(blockers.values())
# Local b=0 exclusion only: not an assembled support or a validity census.
def angle(ts,v):
 from math import gcd
 index={p:i for i,p in enumerate(dirs)};total=0
 for t in ts:
  if v not in t:continue
  a,b=[p for p in t if p!=v]
  def ray(p):
   dx,dy=p[0]-v[0],p[1]-v[1];g=gcd(abs(dx),abs(dy));return index[(dx//g,dy//g)]
  delta=(ray(a)-ray(b))%8;total+=45*min(delta,8-delta)
 return total
local=H|fan('L',[7,0])
assert angle(local,(-1,1))==135
assert angle(local|fan('N',[5]),(-1,1))==180
assert not any((-1,1) in t for site in ['B','D','R','E','Tc'] for t in fan(site,range(8)))
receipt={'status':'TWO_NAMED_MIXED_SUPPORT_IMPLICATIONS_PASS','families':family,'required':sorted(U),'forbidden':sorted(Z),'specific_blockers':blockers,'Nbminus_angle':[135,180],'limits':'Conditional optical transfer only; no census, new room, search, or independent review of underlying nine-path. Other critical-L fixtures do not fit envelope.','source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [source,HERE/'critical-B.txt',HERE/'critical-L.txt',Path(__file__),ROOT/'triangle-composition/inputs/guard_checker.py']}}
(HERE/'nine-path-transfer-check.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('PASS: Bwest and Brectangle centered-E/N6/D2 whole-family transfer; arbitrary R; five specific mirror blockers retained.')
