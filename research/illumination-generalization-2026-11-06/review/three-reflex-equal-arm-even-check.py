"""EA01 prescribed even-N actual-wall replay, no author execution/search."""
from pathlib import Path
from fractions import Fraction as Q
import ast,json,hashlib
HERE=Path(__file__).parent
REQ=HERE.parent/'construction/three-reflex-equal-arm-even-review-request.json'
def pins():
 out=[]
 for pin in json.loads(REQ.read_text())['source_pins']:
  digest=hashlib.sha256(Path(pin['path']).read_bytes()).hexdigest()
  assert digest==pin['sha256'];out.append(dict(pin,actual=digest,passed=True))
 return out
before=pins();request_hash=hashlib.sha256(REQ.read_bytes()).hexdigest()
source=(HERE/'three-reflex-lower-equal-arm-check.py').read_text()
env={'__file__':__file__}
prefix=source.split('\ndef check')[0]
# Delete this old checker's pin setup; load its imports and ONLY own pure
# geometry setup. No old fixtures, outputs or author code are executed.
prefix=prefix[:prefix.index('REQUEST=')]+prefix[prefix.index("ns={'Q':Q,'F':Q}"):]
exec(compile(prefix,'<own-earliest-wall-geometry>','exec'),env)
def v2(n):
 out=0
 while n%2==0:out+=1;n//=2
 return out
env['v2']=v2
fn=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name=='check')
code=ast.get_source_segment(source,fn)
assert 'and N%2 and h%2==0' in code
code=code.replace('and N%2 and h%2==0','and v2(N)<=v2(P) and h%2==0')
code=code.replace('di,dm,dj=N*al//hh,P*be//hh,N*f//hh;dq=P*di+N*dm+P*dj',
 'di,dm,dj=N*al//hh,P*be//hh,N*f//hh;dq=P*di+N*dm+P*dj\n    assert v2(hh)>=v2(N)')
exec(compile(code,'<own-EA01-even-N-selector>','exec'),env)
row=env['check']('EA01-native-even-N10-P2',2,2,10,4,1,3,6,12,(2,4),(14,2),Q(376,9))
assert row['indices']==[11,12,16] and row['residuals']==[-Q(22,9),-Q(10,9),-Q(34,9)]
E=row['residuals'][-1]+row['final_slope']
assert E==38 and E%16==6 and env['ns']['fold'](E,Q(8))==6
assert row['roof']['point']==(Q(74,9),Q(12))
assert request_hash==hashlib.sha256(REQ.read_bytes()).hexdigest()
out=dict(status='PASS_EA01_EVEN_N_ACTUAL_WALLS_AND_FULL_TARGET_PERIOD',
 source_pins_before=before,source_pins_after=pins(),request_sha256=request_hash,
 row=row,cases=1,reflections=row['reflections'],wall_leg_guards=row['wall_leg_guards'],
 full_bottom_period=16,final_bottom_phase=E,author_code_executed=False,
 discovery_search_used=False,whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['row','source_pins_before','source_pins_after']},default=str))
