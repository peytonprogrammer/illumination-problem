"""One frozen archive, three hand-forced rooms, forced endpoint frames only."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,runpy
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
archive=ROOT.parent/'claude-illumination-check/k6-run/cases/I2_00_11-pair0/guards.jsonl'
raw=archive.read_bytes();sha=hashlib.sha256(raw).hexdigest()
check=runpy.run_path(str(ROOT/'lower-bound-proof-audit/full-replay/guard-checker.py'))
tri=lambda t:tuple(sorted(map(tuple,t)))
fixtures=json.loads((HERE/'center-residue-check.json').read_text())['records']
rooms={name:frozenset(tri(t) for t in r['triangles']) for name,r in fixtures.items() if r['in_active_class']}
transforms=[('identity',lambda p:(p[0],p[1])),('swap_xy',lambda p:(p[1],p[0]))]
hits={};count=0
for line,row in enumerate(raw.splitlines(),1):
 count+=1;r=json.loads(row)
 assert r['q']==[2,2]
 p0=[tuple(F(*v) for v in p) for p in r['path']]
 for frame,base in transforms:
  for reverse in (False,True):
   convert=(lambda p:(2-base(p)[0],2-base(p)[1])) if reverse else base
   u=frozenset(tri(convert(tuple(v)) for v in t) for t in r['U'])
   z=frozenset(tri(convert(tuple(v)) for v in t) for t in r['Z'])
   for name,room in rooms.items():
    if name in hits or not u<=room or z&room:continue
    path=[convert(p) for p in p0]
    if reverse:path.reverse()
    assert path[0]==(0,0) and path[-1]==(2,2)
    need,forbid=check['path_requirements'](path)
    assert need<=room and not forbid&room
    hits[name]={'source_line':line,'frame':frame,'endpoint_reversal':reverse,'reflections':len(path)-2,'path':[[[v.numerator,v.denominator] for v in p] for p in path],'required':sorted(need),'forbidden':sorted(forbid)}
 if len(hits)==len(rooms):break
out={'status':'ALL_COVERED' if len(hits)==len(rooms) else 'PARTIAL','archive':str(archive),'sha256':sha,'records_read':count,'fixture_source_sha256':hashlib.sha256((HERE/'center-residue-check.json').read_bytes()).hexdigest(),'hits':hits,'uncovered':sorted(set(rooms)-set(hits)),'scope':'One frozen archive, forced endpoint coordinate maps only, three hand-forced fixtures. First covering certificate retained for each; no path discovery or optimization.'}
(HERE/'center-residue-frozen.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','records_read','uncovered']}));print(json.dumps({n:{k:v[k] for k in ['source_line','frame','endpoint_reversal','reflections']} for n,v in hits.items()}))
