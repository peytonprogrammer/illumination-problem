"""Fixed accepted guard implications over explicit FOUR-root C/O labels.
Symbolic supports are not asserted to be valid rooms. No cap products.
"""
from pathlib import Path
from itertools import product
import json,hashlib
HERE=Path(__file__).resolve().parent;BASE=HERE.parent.parent
src=BASE/'surplus-four-local/R23-top6-search/verify.py'
e={'__file__':str(src)}
exec(compile(src.read_text().split('\ndef path(d,nine):')[0],str(src),'exec'),e)
fan,H=e['fan'],e['H'];C=e['C']
def angle(ts,p):
 return sum(90 if e['dot'](*[e['sub'](v,p) for v in t if v!=p])==0 else 45 for t in ts if p in t)
def decode(ts):return {tuple(sorted(map(tuple,t))) for t in ts}
oldfile=BASE/'fourth-surplus-review/three-unit-b1-independent/check.json'
old=json.loads(oldfile.read_text());assert old['bound']==13 and len(old['named_guards'])==148
for rel,pin in old['source_sha256'].items():assert hashlib.sha256((BASE/rel).read_bytes()).hexdigest()==pin,rel
guards={name:(decode(g['required']),decode(g['forbidden']),g['reflections']) for name,g in old['named_guards'].items()}
shapes={'L':{'C':(7,0),'O':(0,1)},'B':{'C':(1,2),'O':(0,1)},'E':{'C':(3,4),'O':(4,5)},'Tc':{'C':(5,6),'O':(4,5)}}
reference={'L':0,'B':1,'E':4,'Tc':5}
DR=fan('D',[1,2])|fan('R',[3,4])
rows=[]
def check(label,spec):
 mi=H|set().union(*(fan(k,ss) for k,ss in spec.items()));ma=mi|DR
 # Only an angle fixed180 in BOTH extremes rules out every actual room.
 points={p for t in ma for p in t if any(x%2 for x in p)}
 fixed=[p for p in sorted(points) if p[0]%2 and p[1]%2 and angle(mi,p)==angle(ma,p)==180]
 # Odd/odd points are B vertices, never baseline uncovered-H C points.
 fits=[(n,r) for n,(u,z,r) in guards.items() if u<=mi and not z&ma]
 fits.sort(key=lambda x:(x[1],x[0]))
 rows.append({'label':label,'spec':spec,'excluded_b0':fixed,'path':fits[0][0] if fits else None,'reflections':fits[0][1] if fits else None,'fitting_guard_count':len(fits)})
for bits in product('CO',repeat=4):
 ss={k:shapes[k][v] for k,v in zip(shapes,bits)}
 for n in [(),(5,),(6,),(7,),(0,)]:check('ALLcrit-'+''.join(bits)+'-N'+''.join(map(str,n)),dict(ss,N=n))
for missing in shapes:
 sites=[k for k in shapes if k!=missing]
 for bits in product('CO',repeat=3):
  ss={k:shapes[k][v] for k,v in zip(sites,bits)};ss[missing]=(reference[missing],)
  for n in [(5,6),(4,5),(7,0),(0,1)]:check('missing-'+missing+'-'+''.join(bits)+'-N'+''.join(map(str,n)),dict(ss,N=n))
assert len(rows)==208
remaining=[r for r in rows if not r['excluded_b0'] and r['path'] is None]
counts={'symbolic_labels':len(rows),'excluded_fixed_B180':sum(bool(r['excluded_b0']) for r in rows),'covered_nonexcluded':sum(not r['excluded_b0'] and r['path'] is not None for r in rows),'unmatched':len(remaining)}
out={'status':'FIXED_208_LABEL_GUARD_PROBE_NOT_COMPLETENESS_PROOF','counts':counts,'remaining':remaining,'rows':rows,'source_sha256':{str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [src,oldfile,Path(__file__)]},'limits':'Only explicit active critical C/O labels with ordinary D/R left free; completeness/reference forcing/topology hand proof still required. Excluded labels have fixed odd/odd180, incompatibleb0. No completed rooms, validity census, cap assignment product, rays, words, archive or new optics.'}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(counts));print('UNMATCHED:',json.dumps(remaining))
