"""UB02 two prescribed P>K actual rays, reusing only own pure formula checker."""
from pathlib import Path
from fractions import Fraction as Q
from math import floor,ceil,gcd,lcm
import ast,json,hashlib
HERE=Path(__file__).parent
source=(HERE/'three-reflex-lower-unequal-box-check.py').read_text()
# The prefix initializes only reviewer-owned pure geometry and ray functions;
# no previous fixture loop, author code or request is executed.
env={'__file__':__file__}
exec(compile(source.split('\ndef val2')[0],'<reviewer-geometry-setup>','exec'),env)
tree=ast.parse(source)
for name in ['val2','check']:
 node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name)
 code=ast.get_source_segment(source,node)
 if name=='check':
  assert '1<=P<=K<L' in code and 'Bx<=a and By<=a<=R' in code
  code=code.replace('1<=P<=K<L','1<=P and 1<=K<L')
  code=code.replace('assert Bx<=a and By<=a<=R',
   'assert g<=P and (P-K)*f <= (K-g)*(al+be)\n    assert Bx<=a and By<=R')
 exec(compile(code,'<own-UB02-exact-quantified-formulas>','exec'),env)
rows=[env['check']('P5-K3-covering-boundary-equality',2,5,3,4,11,1,3,6,7,
                   (2,4),(18,2),Q(3981,2)),
      env['check']('P5-K3-covering-strict-margin',2,5,3,4,11,1,3,6,8,
                   (2,4),(18,2),Q(1986))]
assert rows[0]['bound_y']==6 and rows[1]['bound_y']<6
assert rows[0]['p']==rows[1]['p']==3
source_paths=[HERE/('three-reflex-lower-large-source-box-'+s) for s in ['candidate.md','proof.md']]
out=dict(status='PASS_UB02_TWO_LARGER_SOURCE_ACTUAL_RAYS_INCLUDING_METRIC_EQUALITY',
 source_pins=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in source_paths],
 rows=rows,cases=len(rows),reflections=sum(r['reflections'] for r in rows),
 wall_leg_guards=sum(r['wall_leg_guards'] for r in rows),author_code_executed=False,
 discovery_search_used=False,independent_acceptance=False,whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['rows','source_pins']}))
