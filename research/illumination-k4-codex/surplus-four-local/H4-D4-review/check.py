"""Independent local support/angle review; no peer code, room or ray search."""
from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent
BASE=HERE.parent.parent
C={'L':(-2,0),'B':(0,-2),'D':(2,-2),'R':(4,0),'E':(4,2),'Tc':(2,4),'N':(0,2)}
R=((1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1))
def fan(a,ss):
 a=C[a] if isinstance(a,str) else a
 return {tuple(sorted((a,(a[0]+R[i][0],a[1]+R[i][1]),(a[0]+R[(i+1)%8][0],a[1]+R[(i+1)%8][1])))) for i in ss}
def decode(ts):return {tuple(sorted(map(tuple,t))) for t in ts}
def angle(ts,p):
 result=0
 for t in ts:
  if p in t:
   a,b=[(q[0]-p[0],q[1]-p[1]) for q in t if q!=p]
   result+=90 if a[0]*b[0]+a[1]*b[1]==0 else 45
 return result
peer=BASE/'fourth-surplus-review/peer-smooth-A-three-independent'
receipt=json.loads((peer/'check.json').read_text())
checks={k:hashlib.sha256((BASE/k).read_bytes()).hexdigest()==v for k,v in receipt['source_sha256'].items()}
assert all(checks.values())
own=BASE/'surplus-four-local/R23-top6-search/verification.json'
j=json.loads(own.read_text());U=decode(j['whole_support']['required']);Z=decode(j['whole_support']['forbidden'])
H=set().union(*(fan(a,range(8)) for a in [(0,0),(2,0),(2,2)]))
minimum=H|fan('B',[7,0,1,2]);D4=fan('D',[4])
maximum=minimum|fan('L',[0,1,2,3,4,5,6])|fan('D',[0,1,2,4,5,6,7])|set().union(*(fan(k,range(8)) for k in ['R','E','Tc','N']))
assert U<=minimum and not Z&maximum
assert Z==fan('L',[7])|fan('D',[3])|fan('B',[3,4,5,6])
assert D4<=maximum and not Z&D4 and Z&fan('D',[3])
faces={'L':[{7,0}],'E':[{3,4}],'R':[{3,4}],'Tc':[{5,6}],'N':[{5,6},{7,0}]}
rows=[]
for site,sides in faces.items():
 for start in range(8):
  ss={start,(start+1)%8}
  if sum(bool(ss&side) for side in sides)!=1:continue
  unit=fan(site,ss)
  if site=='E' and 4 not in ss:reason='forcing_E4';bound=1
  elif site=='L' and 0 not in ss:reason='forcing_L0';bound=4
  elif site=='L' and 7 in ss:
   fixed=minimum|D4|unit;p=(-1,-1)
   assert angle(H,p)==90 and angle(fan('B',[7,0,1,2]),p)==45 and angle(unit,p)==45
   assert angle(fixed,p)==180
   assert all(not any(p in t for t in fan(k,range(8))) for k in ['D','E','R','Tc','N'])
   reason='impossible_b0_unhealable_180';bound=None
  else:
   # All other ordinary caps lie inside this deliberately broader maximum.
   assert minimum|D4|unit<=maximum and U<=minimum|D4|unit and not Z&maximum
   reason='accepted_NEW3_whole_support';bound=3
  rows.append({'site':site,'sectors':sorted(ss),'dispatch':reason,'bound':bound})
assert len(rows)==16
assert sum(r['dispatch']=='accepted_NEW3_whole_support' for r in rows)==13
# Check forcing receipt support instead of executing its author code.
fsource=BASE/'fourth-surplus-review/mixed-e2-e1/root-leaf-check.json'
f=json.loads(fsource.read_text())
forcing={}
for name,r in f['named_implications'].items():
 if name=='missing_E_reference' or name.endswith('_missing_L'):
  assert r['status']=='PASS' and r['reflections']<=4
  assert decode(r['required'])<=decode(r['fixed']) and not decode(r['forbidden'])&decode(r['possible'])
  forcing[name]=r['reflections']
assert len(forcing)==4
sources=[peer/'review.txt',peer/'coverage.txt',peer/'check.py',peer/'check.json',own,fsource,BASE/'fourth-surplus-review/mixed-e2-e1/argument.txt']
out={'status':'INDEPENDENT_H4_D4_TRANSFER_ACCEPT','peer_pinned_hashes':checks,'local_fan_dispatch':rows,'local_forms':16,'new3_support_forms':13,'whole_bound_including_forcing':4,'source_sha256':{str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},'limits':'Local fan/support/angle implications only. No room or cap-assignment census, peer code execution, new optical search or workers. Inherits accepted root/leaf class, reference forcing and independently reviewed NEW3 optical certificate.'}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: 12 pinned hashes; 16 local forms = 13 NEW3 + 2 forcing + 1 b0 exclusion; whole H4/D4 <=4.')
