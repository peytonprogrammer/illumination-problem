"""One frozen-guard symbolic projection; no room assignments or ray discovery."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
slotdata=json.loads((ROOT/'zero-surplus-L/guard-incidence-check.json').read_text())['cap_options']
tri=lambda t:tuple(sorted(map(tuple,t)))
slots={n:tri(t) for n,t in slotdata.items()};labels={t:n for n,t in slots.items()}
lookup=json.loads((ROOT/'cap-return-review/lookup.json').read_text())
core=frozenset(map(tri,lookup['room']))-frozenset(slots[n] for n in ('L+','B+','E-','T-'))
universe=core|frozenset(slots.values())
forced=frozenset(('L+','B-','B+','E-','T-','Nr-'))
groups=[frozenset(x) for x in (('L-','L+'),('D-','D+'),('R-','R+'),('E-','E+'),('T-','T+'),('Nb-','Nb+','Nr-','Nr+'))]
pairs=[frozenset(x) for x in (('L-','B-'),('D+','R-'),('E+','T+'),('T-','Nr+'),('L+','Nb-'))]
transform=lambda p,f,r:(lambda xy:(2-xy[1],2-xy[0]) if r else xy)((f[1]*(p[1] if f[0] else p[0]),f[2]*(p[0] if f[0] else p[1])))
tset=lambda ts,f,r:frozenset(tri(transform(v,f,r) for v in t) for t in ts)
sources=json.loads((ROOT/'zero-surplus-L/project-guards.json').read_text())['sources']
terms={};count=0
for source in sources:
 data=Path(source['path']).read_bytes();assert hashlib.sha256(data).hexdigest()==source['sha256']
 for line,raw in enumerate(data.splitlines(),1):
  count+=1;rec=json.loads(raw)
  if sum(v*v for v in rec['q'])!=8:continue
  frames=[(sw,sx,sy) for sw in (False,True) for sx,sy in ((1,1),(1,-1),(-1,1),(-1,-1)) if transform(rec['q'],(sw,sx,sy),False)==(2,2)]
  for frame,reflected in ((f,r) for f in frames for r in (False,True)):
   u,z=tset(rec['U'],frame,reflected),tset(rec['Z'],frame,reflected)
   if not u<=universe or z&core:continue
   required=frozenset(labels[t] for t in u-core);absent=frozenset(labels[t] for t in z if t in labels)
   positive=set(required|forced)
   if 'D-' in positive:positive.add('R-') # proved remaining darkness condition
   if any(len(positive&g)>1 for g in groups) or any(p<=positive for p in pairs):continue
   neg=set()
   for g in groups:
    if positive&g:neg.update(g-positive)
   for pair in pairs:
    if pair&positive:neg.update(pair-positive)
   if 'R-' in absent or 'R-' in neg:neg.add('D-')
   if absent&positive or neg&positive:continue
   required=set(required-forced);absent=set(absent-neg)
   if 'D-' in required:required.discard('R-')
   key=(frozenset(required),frozenset(absent))
   if key in terms and terms[key]['reflections']<=len(rec['path'])-2:continue
   path=[transform(tuple(F(*c) for c in point),frame,reflected) for point in rec['path']]
   if reflected:path=path[::-1]
   assert path[0]==(0,0) and path[-1]==(2,2)
   terms[key]={'required':sorted(key[0]),'absent':sorted(key[1]),'reflections':len(path)-2,
    'source':source['path'],'source_sha256':source['sha256'],'line':line,'frame':frame,'sigma_reversed':reflected,
    'path':[[[v.numerator,v.denominator] for v in point] for point in path]}
keys=sorted(terms,key=lambda k:(len(k[0])+len(k[1]),sorted(k[0]),sorted(k[1])))
minimal=[]
for key in keys:
 if not any(a<=key[0] and b<=key[1] for a,b in minimal):minimal.append(key)
result={'status':'projection_complete','forced_caps':sorted(forced),'remaining_assumption':'not D- or R-',
 'source_records':count,'sources':sources,'distinct_terms':len(terms),'undominated_terms':[terms[k] for k in minimal],
 'scope':'Symbolic conditions on optional D/R from fixed previously hashed archives; no occupancy assignments or rooms generated; no new directions or words.'}
(HERE/'bottom-residual-projection.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'projection_complete','distinct_terms':len(terms),'undominated':[{k:v for k,v in terms[t].items() if k not in ('path','source_sha256','frame','source','sigma_reversed')} for t in minimal]},indent=2))
