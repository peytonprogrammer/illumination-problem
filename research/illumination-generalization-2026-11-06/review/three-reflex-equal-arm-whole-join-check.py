"""WJ01 prescribed separated geometry and entire actual isometry replay."""
from pathlib import Path
from fractions import Fraction as Q
import ast,json,hashlib
HERE=Path(__file__).parent
source=(HERE/'three-reflex-lower-source-sign-check.py').read_text()
prefix=source[:source.index('def v2')]
prefix=prefix.replace("three-reflex-equal-arm-source-sign-review-request.json",
    "three-reflex-equal-arm-whole-join-review-request.json")
env={'__file__':__file__}
exec(compile(prefix,'<own-fixed-geometry-setup>','exec'),env)
tree=ast.parse(source)
functions=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['v2','check']]
for node in functions:
    code=ast.get_source_segment(source,node)
    if node.name=='check':
        code=code.replace('N>P+L and v2(N)',
            'L<N and N>2*P and (N>P+L or c<b) and v2(N)')
        code=code.replace('0<b<c<h<H and h%2==0',
            '0<b<h<H and 0<c<h and (a<A-B or c<b) and h%2==0')
    exec(compile(code,'<own-signed-selector-separated-domain>','exec'),env)
row=env['check']('WJ01-vertical-separation-odd-cap-actual-negative-vx',
    2,3,10,8,5,3,8,13,(2,6),(6,2),expected=Q(14))
assert row['selected_sign']==-1 and row['final_indices']==[2,3,6,6]
assert row['E']==14
original=[(3,4),(3,14),(8,14),(8,6),(5,6),(5,0),(13,0),(13,20),(0,20),(0,4)]
path=[(y,x) for x,y in row['path']]
ns=env['ns'];ns['simple'](original)
assert path[0]==(6,2) and path[-1]==(2,6)
assert ns['location'](original,path[0])==ns['location'](original,path[-1])==1
transposed=ns['path_check'](original,path)
assert transposed['reflections']==row['reflections']
assert env['request_hash']==hashlib.sha256(env['REQ'].read_bytes()).hexdigest()
out=dict(status='PASS_WJ01_ORIGINAL_SEPARATED_PATH_AND_FULL_TRANSPOSE',
    request_sha256=env['request_hash'],source_pins_before=env['before'],source_pins_after=env['pins'](),
    row=row,original_polygon=original,original_S=[6,2],original_T=[2,6],
    original_transposed_path=path,original_wall_verification=transposed,
    cases=1,reflections=row['reflections'],wall_leg_guards=row['wall_leg_guards'],
    transposed_validation_is_same_witness=True,author_code_executed=False,
    discovery_search_used=False,whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['row','source_pins_before','source_pins_after','original_transposed_path']}))
