"""Two prescribed second-gap controls, both needing target modulo four."""
from pathlib import Path
from fractions import Fraction as Q
import ast,json,hashlib
HERE=Path(__file__).parent
def selector(file):
    source=(HERE/file).read_text()
    prefix=source[:source.index('def v2')]
    # The upper checker defines Bezout before v2, included in its prefix.
    env={'__file__':__file__}
    exec(compile(prefix,'<own-prescribed-setup>','exec'),env)
    for n in ast.parse(source).body:
        if isinstance(n,ast.FunctionDef) and n.name in ['v2','check']:
            code=ast.get_source_segment(source,n)
            code=code.replace('v2(N)==v2(P)+1','v2(N)==v2(P)+2')
            exec(compile(code,'<own-prescribed-second-gap-selector>','exec'),env)
    return env
lower=selector('three-reflex-lower-source-sign-check.py')
upper=selector('three-reflex-equal-arm-upper-columns-check.py')
rows=[lower['check']('LS02-second-gap-lower',4,1,12,8,1,3,6,8,(2,4),(20,2),expected=Q(779,5)),
      upper['check']('LS02-second-gap-mouth',4,1,12,8,1,3,6,8,(2,6),(20,2),True,Q(621,4))]
assert rows[0]['blocks']==rows[1]['blocks']==2
assert rows[0]['final_indices']==[39,6,74,58] and rows[0]['E']==156
assert rows[1]['final_indices']==[6,74,58] and rows[1]['E']==156
out=dict(status='PASS_LS02_SECOND_GAP_ACTUAL_LOWER_AND_MOUTH_MOD4',rows=rows,cases=2,
    dependency_requests=[dict(path=str(env['REQ']),sha256=env['request_hash'],
        source_pins_before=env['before'],source_pins_after=env['pins']()) for env in [lower,upper]],
    reflections=sum(r['reflections'] for r in rows),wall_leg_guards=sum(r['wall_leg_guards'] for r in rows),
    author_code_executed=False,discovery_search_used=False,independent_review_pending=True,
    whole_r3_complete=False,whole_goal_complete=False)
for env in [lower,upper]:assert env['request_hash']==hashlib.sha256(env['REQ'].read_bytes()).hexdigest()
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['rows','dependency_requests']}))
