"""CE03 final-manifest independent replay; preserves the earlier receipt/checks."""
from pathlib import Path
from fractions import Fraction as Q
import json,hashlib
HERE=Path(__file__).parent
namespace={'__file__':str(HERE/'three-reflex-coprime-wide-check.py'),'__name__':'independent_ce03_definitions'}
source=(HERE/'three-reflex-coprime-wide-check.py').read_text().split('\nfixtures=')[0]
exec(compile(source,'<own-ce03-selector-and-original-walls>','exec'),namespace)
assert namespace['REQUEST'].exists()
before=namespace['capture']()
fixtures=[
 ('wider-lower-thin',4,5,2,3,1,4,5,6,(2,4),(10,2)),
 ('declared-singular-suffix',4,5,2,3,1,4,5,7,(2,6),(10,2),4),
 ('wider-upper-ordinary',4,5,2,3,1,4,5,7,(2,6),(14,2)),
 ('noncoprime-lower-cap',4,8,3,5,1,4,5,6,(2,4),(14,2)),
 ('noncoprime-upper-cap',4,9,4,5,1,4,5,7,(2,6),(18,2)),
 ('narrow-upper-odd-c',4,5,1,2,1,5,7,9,(2,8),(14,2)),
 ('narrow-source-on-h',4,5,1,3,1,4,6,8,(2,6),(10,2)),
 ('narrow-singular-roof-suffix',4,7,1,5,1,4,5,7,(1,6),(26,1),6),
 ('long-thick-cap',4,11,3,5,1,4,7,11,(2,10),(26,2)),
 ('power2L-oddK',4,7,3,4,1,5,7,9,(2,8),(14,2)),
 ('rational-horizontal',Q(3,2),7,2,3,1,4,5,7,(Q(1,7),6),(Q(67,11),2))]
rows=[namespace['ray'](*f) for f in fixtures]
narrow=next(x for x in rows if x['label']=='narrow-singular-roof-suffix')
assert narrow['slope']==27 and narrow['singular_prefix_discarded']
assert sum(x['cap_gcd']>1 for x in rows)==2
request=namespace['REQUEST'];after=namespace['capture']()
old=json.loads((HERE/'three-reflex-coprime-wide-check.json').read_text())
assert old['whole_pair_count']==171
# Earlier whole-room replay remains applicable to these unchanged proof revisions.
for item in old['source_pins_after']:
 assert hashlib.sha256(Path(item['path']).read_bytes()).hexdigest()==item['sha256']
for item in json.loads((HERE/'three-reflex-coprime-wide-independent.json').read_text())['evidence']:
 assert hashlib.sha256(Path(item['path']).read_bytes()).hexdigest()==item['sha256']
author=json.loads((HERE.parent/'construction/three-reflex-coprime-extension-wide-check.json').read_text())
out=dict(status='PASS_INDEPENDENT_FINAL_CE03_ALL42PINS_AND11CONTROLS',request_sha256=hashlib.sha256(request.read_bytes()).hexdigest(),source_pins_before=before,source_pins_after=after,rows=rows,terminal_cases=len(rows),terminal_reflections=sum(x['reflections'] for x in rows),terminal_wall_guards=sum(x['wall_leg_guards'] for x in rows),singular_suffix_controls=sum(x['singular_prefix_discarded'] for x in rows),noncoprime_controls=sum(x['cap_gcd']>1 for x in rows),earlier_whole_pairs=171,earlier_whole_reflections=2303,earlier_whole_wall_guards=25500,author_evidence_summary={k:v for k,v in author.items() if isinstance(v,(str,int,bool))},author_code_executed=False,discovery_search_used=False,whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('source_pins_before','source_pins_after','rows','author_evidence_summary')}))
