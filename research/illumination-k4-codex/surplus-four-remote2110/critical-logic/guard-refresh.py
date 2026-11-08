"""Fresh own exact guards for the four OLD selected L-family witnesses."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
engine=ROOT/'surplus-four-local/R23-top6-search/verify.py';e={'__file__':str(engine)};exec(engine.read_text().split('\ndef path(d,nine):')[0],e)
pins={};records={}
def read(rel):
 p=ROOT/rel;pins[rel]=hashlib.sha256(p.read_bytes()).hexdigest();return json.loads(p.read_text())
def dec(ts):return {tuple(sorted(map(tuple,t)))for t in ts}
def fp(P):return [tuple(F(*v)for v in p)for p in P]
paths={
 'N_CC_L-B_right_center':fp(read('first-surplus-review/bottom-residual-check.json')['path']),
 'N_CC_L-E_bottom_center':fp(read('first-surplus-review/residual-cover-check.json')['path']),
 'N_CO_LB_right_center':fp(read('second-surplus-review/five-path-check.json')['five_path']),
 'N_OO_L-E_right_center':fp(read('zero-surplus-L/cover-check.json')['paths']['thirteen']['path'])}
old=read('fourth-surplus-review/three-unit-b1-independent/check.json')['named_guards']
for name,P in paths.items():
 walls=[]
 for a,p,b in zip(P,P[1:],P[2:]):
  v=e['sub'](p,a);w=e['sub'](b,p);v=tuple(x/max(map(abs,v))for x in v);w=tuple(x/max(map(abs,w))for x in w)
  t=tuple(v[k]+w[k]for k in (0,1))
  if t==(0,0):t=(-v[1],v[0])
  walls.append((tuple(p[k]-t[k]for k in (0,1)),tuple(p[k]+t[k]for k in (0,1))))
 U,Z,_=e['constraints'](P,walls);assert (U,Z)==(dec(old[name]['required']),dec(old[name]['forbidden']))
 ur,zr,_=e['constraints'](P[::-1],walls[::-1]);assert(U,Z)==(ur,zr)
 us,zs,_=e['constraints']([e['sigma'](p)for p in P[::-1]],[(e['sigma'](a),e['sigma'](b))for a,b in walls[::-1]])
 assert(us,zs)==(e['transform'](U),e['transform'](Z))
 records[name]={'path':[[str(x)for x in p]for p in P],'required':sorted(U),'forbidden':sorted(Z),'reflections':len(P)-2}
 print('PASS',name,len(P)-2,len(U),len(Z),flush=True)
pins[str(engine.relative_to(ROOT))]=hashlib.sha256(engine.read_bytes()).hexdigest();pins[str(Path(__file__).resolve().relative_to(ROOT))]=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
(HERE/'guard-refresh.json').write_text(json.dumps({'status':'FOUR_SELECTED_OLD_L_GUARDS_FRESH_FRACTION_PASS','paths':records,'source_sha256':pins,'limits':'Fixed witnesses only; specularity/openleg support/reverse/sigma refreshed. Prior accepted finite path bounds and firstT are explicit dependencies; no discovery.'},indent=2)+'\n')
