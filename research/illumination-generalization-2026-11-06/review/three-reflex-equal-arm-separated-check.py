"""EA04 fixed overlap/equality geometry and global transpose verification."""
from pathlib import Path
from fractions import Fraction as Q
import ast,json,hashlib
HERE=Path(__file__).parent
REQ=HERE.parent/'construction/three-reflex-equal-arm-separated-review-request.json'
def pins():
 rows=[]
 for pin in json.loads(REQ.read_text())['source_pins']:
  digest=hashlib.sha256(Path(pin['path']).read_bytes()).hexdigest()
  assert digest==pin['sha256'];rows.append(dict(pin,actual=digest,passed=True))
 return rows
before=pins();request_hash=hashlib.sha256(REQ.read_bytes()).hexdigest()
def v2(n):
 out=0
 while n%2==0:out+=1;n//=2
 return out
source=(HERE/'three-reflex-lower-equal-arm-check.py').read_text()
env={'__file__':__file__,'v2':v2}
prefix=source.split('\ndef check')[0]
prefix=prefix[:prefix.index('REQUEST=')]+prefix[prefix.index("ns={'Q':Q,'F':Q}"):]
exec(compile(prefix,'<own-pure-wall-setup>','exec'),env)
fn=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name=='check')
code=ast.get_source_segment(source,fn)
code=code.replace('N>P+L and N%2','P<L<N and N>2*P and (N>P+L or c<b) and v2(N)<=v2(P)')
code=code.replace('0<b<c<h<H','0<b<h<H and 0<c<h')
exec(compile(code,'<own-enlarged-equal-arm-selector>','exec'),env)
rows=[env['check']('EA04-horizontal-overlap-height-separated',1,5,11,8,5,3,8,12,(2,6),(4,2),Q(331)),
      env['check']('EA04-a-equals-l-even-N',2,2,6,4,5,3,8,12,(2,6),(6,2),Q(51,2))]
assert rows[0]['indices']==[66,120,166] and rows[0]['residuals']==[4,1,-4]
assert rows[0]['roof']['point']==(Q(8),Q(12))
ns=env['ns']
original=list(map(lambda p:tuple(map(Q,p)),[(3,3),(3,6),(8,6),(8,5),(5,5),(5,0),(12,0),(12,11),(0,11),(0,3)]))
S=(Q(6),Q(2));T=(Q(2),Q(4));path=[(y,x) for x,y in rows[0]['path']]
ns['simple'](original);assert ns['location'](original,S)==ns['location'](original,T)==1
assert path[0]==S and path[-1]==T
assert all(not ns['on'](a,b,T) for a,b in zip(path[:-2],path[1:-1]))
original_check=ns['path_check'](original,path)
assert original_check['reflections']==rows[0]['reflections']
assert original_check['wall_leg_guards']==rows[0]['wall_leg_guards']
assert request_hash==hashlib.sha256(REQ.read_bytes()).hexdigest()
out=dict(status='PASS_EA04_OVERLAPPING_PROJECTIONS_EQUALITY_AND_GLOBAL_TRANSPOSE',
 source_pins_before=before,source_pins_after=pins(),request_sha256=request_hash,
 rows=rows,cases=2,reflections=sum(row['reflections'] for row in rows),
 wall_leg_guards=sum(row['wall_leg_guards'] for row in rows),
 original_transposed_path=path,original_transposed_check=original_check,
 original_first_target_preserved=True,author_code_executed=False,
 discovery_search_used=False,whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['rows','source_pins_before','source_pins_after','original_transposed_path']}))
