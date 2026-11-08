"""Fixed necessary B-label guard implications; no polygons or discovery."""
from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
src=ROOT/'surplus-four-local/R23-top6-search/verify.py';e={'__file__':str(src)};exec(src.read_text().split('\ndef path(d,nine):')[0],e)
fan,H=e['fan'],e['H'];pins={}
def read(rel):
 p=ROOT/rel;pins[rel]=hashlib.sha256(p.read_bytes()).hexdigest();return json.loads(p.read_text())
def dec(ts):return {tuple(sorted(map(tuple,t)))for t in ts}
guards=[]
def add(name,g,status):
 u,z=dec(g['required']),dec(g['forbidden']);n=g.get('reflections',g.get('proof',g.get('audit',{})).get('reflections'));assert n is not None
 guards.extend([(name,u,z,n,status),('sigma:'+name,e['transform'](u),e['transform'](z),n,status)])
new=read('surplus-four-remote2110/peer-core-exchange-review/check.json')
for name,g in new['paths'].items():add(name,g,'independently accepted')
for name in ['B-full-L70-lower-search','B-full-L70-lower-Tc6-search','B-full-L70-lower-N7Tc6-search','B-full-L70-lower-D1-search','B-full-L70-lower-R4-search','B-full-L70-upper-search']:
 g=read('surplus-four-remote2110/'+name+'/verification.json');add(name,g,'parent verified; independent review pending')
g=read('surplus-four-local/mixed-O3-N70-search/verification.json')['four'];g['reflections']=4;add('accepted_N70_four',g,'independently accepted')
for rel in ['surplus-four-remote2110/R34-centered-search/verification.json','surplus-four-remote2110/R23-square-seven/check.json','surplus-four-remote2110/E34-centered-search/verification.json','surplus-four-remote2110/N70-center-three/check.json','surplus-four-remote2110/N70-Tc6-search/verification.json']:
 g=read(rel);add(rel,g,'parent verified; independent review pending')
# Reconstruct exact old guard lookup independently from its accepted receipts.
oldguards={}
def oldadd(name,g):
 u,z=dec(g['required']),dec(g['forbidden']);n=g.get('reflections',g.get('proof',g.get('audit',{})).get('reflections'));assert n is not None,name
 oldguards[name]=(u,z,n);oldguards['sigma:'+name]=(e['transform'](u),e['transform'](z),n)
for name,g in read('fourth-surplus-review/three-unit-b1-independent/check.json')['named_guards'].items():oldadd('148:'+name,g)
for rel in ['surplus-four-remote2110/peer-optical-review/check.json','surplus-four-remote2110/N6-four-review/check.json','surplus-four-remote2110/B-eight-review/check.json']:
 for name,g in read(rel)['paths'].items():oldadd(name,g)
g=read('surplus-four-remote2110/roof-N5-search/verification.json');g['reflections']=4;oldadd('right_leaf_four',g)
g=read('surplus-four-local/R23-top6-search/verification.json')['whole_support'];g['reflections']=3;oldadd('H4_smooth_three',g)
for name,g in read('surplus-four-local/west-four-mixed-eleven-review/check.json')['new_path_records'].items():oldadd('West_mixed:'+name,g)
# The catalog already covers other labels. Revisit only its49 remaining ones.
base=read('surplus-four-remote2110/critical-logic/check.json');rows=[]
for r in base['templates']:
 if r['parent']!='B':continue
 fixed=H|fan('B',r['sectors'])|fan(tuple(r['remote']),[r['leaf']])|fan(r['unit'],r['unit_sectors'])
 covers=[];remaining=[]
 for cover in r['covers']:
  support=fixed|set().union(*(fan(k,v)for k,v in cover['caps'].items()))
  u,z,n=oldguards[cover['guard']];assert u<=support and not z&support and n==cover['bound'] and n<=13
 for caps in r['uncovered']:
  support=fixed|set().union(*(fan(k,s)for k,s in caps.items()))
  matches=[(name,n,status)for name,u,z,n,status in guards if u<=support and not z&support]
  if matches:
   name,n,status=min(matches,key=lambda v:(v[2]!='independently accepted',v[1]));covers.append({'caps':caps,'guard':name,'bound':n,'status':status})
  else:remaining.append(caps)
 rows.append({'leaf':r['leaf'],'unit':r['unit'],'unit_sectors':r['unit_sectors'],'original_covered':len(r['covers']),'old_complete_guard_rechecked':True,'original_accepted_covers':r['covers'],'new_covered':covers,'remaining':remaining})
assert sum(len(r['original_accepted_covers'])+len(r['new_covered'])+len(r['remaining'])for r in rows)==186
assert all(not r['remaining']for r in rows)
maxbound=max(c['bound']for r in rows for c in r['original_accepted_covers']+r['new_covered']);assert maxbound==13
summary={leaf:{'remaining':sum(len(r['remaining'])for r in rows if r['leaf']==leaf),'new_covers':sum(len(r['new_covered'])for r in rows if r['leaf']==leaf)}for leaf in (0,7)}
pins[str(src.relative_to(ROOT))]=hashlib.sha256(src.read_bytes()).hexdigest();pins[str(Path(__file__).resolve().relative_to(ROOT))]=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
(HERE/'B-frontier-join.json').write_text(json.dumps({'status':'NECESSARY_B_LABEL_GUARD_JOIN_PARENT_REVIEW_PENDING','bound':maxbound,'all_necessary_B_labels':186,'summary':summary,'rows':rows,'source_sha256':pins,'limits':'Necessarysymboliclabels NOTvalidrooms/darkness. Newown6pathparentspendingreview. Originalclassification/sourceguardsfrozen; no polygons/rays/search.'},indent=2)+'\n')
print(summary)
for r in rows:
 if r['remaining']:print('OPEN',r['leaf'],r['unit'],r['unit_sectors'],r['remaining'])
