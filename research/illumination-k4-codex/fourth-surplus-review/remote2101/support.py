from pathlib import Path
import json,itertools,hashlib,time,signal
HERE=Path(__file__).resolve().parent
signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('840s logic effort')));signal.alarm(840)
x=json.loads((HERE/'classification.json').read_text());out=[]
# Ordinary slot labels from established cap alphabet, not geometry enumeration.
site=lambda n:'N' if n.startswith(('Nb','Nr')) else n[0]
for r in x['templates']:
 if r['excluded_b1']:out.append({'name':r['name'],'excluded_fixed_b1':True});continue
 groups={}
 for n in r['variable_caps']:groups.setdefault(site(n),[]).append(n)
 rows=[];matched=[]
 for tup in itertools.product(*[[None]+v for v in groups.values()]):
  caps={n for n in tup if n}
  if len(caps)!=r['additional_occupied_slots']:continue
  b=len(r['extra_C_constant'])+sum(t['fixed_degrees']+sum(v for n,v in t['cap_degrees'].items() if n in caps)==180 for t in r['extra_B_terms'])
  if b!=1:continue
  covers=[c for c in r['sufficient_old_guard_conditions'] if set(c['required'])<=caps and not set(c['forbidden'])&caps]
  if covers:matched.append({'caps':sorted(caps),'guard':min(covers,key=lambda c:c['reflections'])})
  else:rows.append(sorted(caps))
 out.append({'name':r['name'],'necessary_labels':len(rows)+len(matched),'covered_labels':len(matched),'uncovered_labels':rows,'covers':matched})
source=[HERE/'classification.json',Path(__file__)]
y={'status':'EXACT_NAMED_SLOT_EQUATIONS_GUARD_IMPLICATION','templates':out,'limits':'Finite symbolic necessary cap descriptions, NOT valid room counts. No polygons constructed; no trajectory/discovery search. Row completeness still requires hand derivation.','source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in source}}
(HERE/'support.json').write_text(json.dumps(y,indent=2)+'\n');signal.alarm(0)
for r in out:
 print(r['name'], 'excluded' if r.get('excluded_fixed_b1') else ('necessary '+str(r['necessary_labels'])+' covered '+str(r['covered_labels'])+' OPEN '+str(r['uncovered_labels'])))
