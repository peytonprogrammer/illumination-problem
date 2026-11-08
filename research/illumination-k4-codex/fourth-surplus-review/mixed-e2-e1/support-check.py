"""Named proof question: can the accepted two-unit cover survive a D/R leaf?"""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,runpy
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
catalog=json.loads((ROOT/'third-surplus-review/path-support-check.json').read_text())
paths={};hashes={}
for source,pinned in catalog['sources'].items():
 raw=(ROOT/source).read_bytes();hashes[source]=hashlib.sha256(raw).hexdigest()
 assert hashes[source]==pinned,('catalog drift',source)
 data=json.loads(raw)
 if 'forcing_paths' in data:
  for name,record in data['forcing_paths'].items():paths[source+':'+name]=record['path']
 elif 'paths' in data:
  for name,record in data['paths'].items():paths[source+':'+name]=record['path']
 else:paths[source]=data.get('path',data.get('five_path'))
assert set(paths)==set(catalog['paths'])
g=runpy.run_path(str(ROOT/'lower-bound-proof-audit/full-replay/guard-checker.py'))
def owner(t):
 a=[p for p in t if p[0]%2==p[1]%2==0];assert len(a)==1;return a[0]
sigma=lambda p:(2-p[1],2-p[0])
rows={}
for name,raw in paths.items():
 P=[tuple(F(*v) for v in p) for p in raw]
 U,Z=g['path_requirements'](P)
 cells={owner(t) for t in U|Z}
 assert not cells&{(2,-2),(4,0)},(name,'uses D/R',cells)
 us,zs=g['path_requirements']([sigma(p) for p in P[::-1]])
 assert not {owner(t) for t in us|zs}&{(2,-2),(4,0)}
 rows[name]={'status':'PASS','reflections':len(P)-2,'D_and_R_absent_from_required_and_forbidden':True,'sigma':'PASS'}
(HERE/'support-check.json').write_text(json.dumps({'status':'PASS','proof_question':'Every fixed inherited path in the pinned catalog is unaffected by adding/removing arbitrary D/R triangles. Hand proof separately checks cover completeness, deletion and square compositions.','paths':rows,'sources':hashes,'catalog_sha256':hashlib.sha256((ROOT/'third-surplus-review/path-support-check.json').read_bytes()).hexdigest(),'limits':'No discovery, room generation, archive or witness selection. This does not by itself prove geometric deletion or exhaustive optical dispatch.'},indent=2)+'\n')
print('PASS: pinned inherited path catalog and sigma avoid full D/R support')
