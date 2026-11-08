"""Check support of the previously proved paths only; no path discovery."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,runpy
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
check=runpy.run_path(str(ROOT/'lower-bound-proof-audit/full-replay/guard-checker.py'))
centers={(0,0),(2,0),(2,2),(-2,0),(0,-2),(2,-2),(4,0),(4,2),(2,4),(0,2)}
sources=['zero-surplus-L/cover-check.json','first-surplus-review/square-exchange-check.json','first-surplus-review/centered-left-check.json','first-surplus-review/bottom-residual-check.json','first-surplus-review/residual-cover-check.json','second-surplus-review/five-path-check.json','third-surplus-review/independent-review/guard-extension-check.json']
paths={}; hashes={}
for source in sources:
 raw=(ROOT/source).read_bytes(); hashes[source]=hashlib.sha256(raw).hexdigest();data=json.loads(raw)
 if 'forcing_paths' in data:
  for name,record in data['forcing_paths'].items(): paths[source+':'+name]=record['path']
 elif 'paths' in data:
  for name,record in data['paths'].items(): paths[source+':'+name]=record['path']
 else: paths[source]=data.get('path',data.get('five_path'))
results={}
for name,raw in paths.items():
 path=[tuple(F(*c) for c in p) for p in raw]
 assert path[0]==(0,0) and path[-1]==(2,2)
 required,forbidden=check['path_requirements'](path)
 def cell(t):
  a=[v for v in t if v[0]%2==0 and v[1]%2==0]
  assert len(a)==1
  return a[0]
 rc={cell(t) for t in required};fc={cell(t) for t in forbidden}
 assert rc<=centers,(name,'required',rc-centers)
 assert fc<=centers,(name,'forbidden',fc-centers)
 results[name]={'reflections':len(path)-2,'required_cells':sorted(rc),'forbidden_cells':sorted(fc),'status':'PASS'}
 # Also retain endpoint-exchanging sigma paths used throughout the proofs.
 sigma=lambda p:(2-p[1],2-p[0])
 ur,zr=check['path_requirements']([sigma(p) for p in path][::-1])
 assert {cell(t) for t in ur|zr}<=centers
out={'status':'PASS','paths_checked':len(paths),'sources':hashes,'paths':results,'all_sigma_supports':'PASS','support':sorted(centers),'scope':'Previously specified fixed paths only. Any added triangles in A cells outside this support leave all required/forbidden guards unchanged. Does not classify rooms or prove that deletion lowers surplus.'}
(HERE/'path-support-check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'PASS','paths_checked':len(paths),'sigma_supports':'PASS'}))
