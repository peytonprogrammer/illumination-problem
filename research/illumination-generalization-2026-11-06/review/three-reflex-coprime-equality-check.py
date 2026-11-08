"""Independent CE05 fixed equality-window formula and actual-wall replays."""
from pathlib import Path
from fractions import Fraction as Q
import json,hashlib
HERE=Path(__file__).parent
source=(HERE/'three-reflex-coprime-source-width-check.py').read_text().split('\nfixtures=')[0]
changes={
 "REQUEST=AUTHOR/'three-reflex-coprime-extension-sourcewide-review-request.json'":"REQUEST=AUTHOR/'three-reflex-coprime-extension-equality-review-request.json'",
 'assert delta<K and gcd(Lam*d2,L)==1':'assert delta==K and P%K==0 and gcd(Lam*d2,L)==1',
 'for q in range(D):':'for q in range(D*P):',
 'phases=[(s+(D-d2)*tau-A,K*e)]+([(s+d0*tau,P*e)] if u<h else [])':'phases=[(s+(d0+C)*tau-A,K*e,2*K*e),(s+(D-d2)*tau-A,K*e,2*K*e)]+([(s+d0*tau,P*e,2*P*e)] if u<h else [])',
 'if all(((x-end)/(2*e)).denominator!=1 for x,end in phases)':'if all(((x-end)/period).denominator!=1 for x,end,period in phases)'
}
for old,new in changes.items():
 assert source.count(old)==1,old
 source=source.replace(old,new)
ns={'__file__':str(HERE/'three-reflex-coprime-source-width-check.py'),'__name__':'own_equality_constructor'}
exec(compile(source,'<own-source-width-selector-with-actual-equality-guards>','exec'),ns)
assert ns['REQUEST'].exists();before=ns['capture']()
fixtures=[
 ('CE05-A',2,2,2,3,10,1,4,5,6,(2,4),(18,2),0),
 ('CE05-B',1,3,3,4,15,1,3,5,7,(2,4),(13,2),0),
 ('CE05-C',1,2,2,3,10,1,4,5,7,(1,6),(9,2),0),
 ('CE05-source-h',2,2,2,3,10,1,4,5,6,(2,5),(18,2)),
 ('CE05-P-greater-K',1,4,2,3,10,1,4,5,6,(2,4),(8,2))]
rows=[ns['ray'](*x) for x in fixtures]
expected=[(Q(34,3),6,1,0),(Q(399,8),24,3,1),(Q(89,3),30,2,1)]
for row,value in zip(rows,expected):assert (row['slope'],row['finalJ'],row['M'],row['target_shift'])==value
out=dict(status='PASS_INDEPENDENT_CE05_ACTUAL_EQUALITY_WINDOWS',request_sha256=hashlib.sha256(ns['REQUEST'].read_bytes()).hexdigest(),source_pins_before=before,source_pins_after=ns['capture'](),rows=rows,cases=len(rows),reflections=sum(x['reflections'] for x in rows),wall_leg_guards=sum(x['wall_leg_guards'] for x in rows),author_code_executed=False,discovery_search_used=False,whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('source_pins_before','source_pins_after','rows')}))
