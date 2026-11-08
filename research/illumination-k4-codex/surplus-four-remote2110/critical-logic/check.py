"""Named symbolic guard implications under b0/n equations, no polygons/rays."""
from pathlib import Path
import json,hashlib,itertools,time,signal
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
effort=json.loads((HERE/'effort.json').read_text());remaining=effort['deadline_unix']-time.time();assert remaining>0
signal.signal(signal.SIGALRM,lambda *_:(_ for _ in()).throw(TimeoutError('840s aggregate logic effort')));signal.alarm(max(1,int(remaining)))
engine=ROOT/'surplus-four-local/R23-top6-search/verify.py';e={'__file__':str(engine)};exec(engine.read_text().split('\ndef path(d,nine):')[0],e)
fan,H,C=e['fan'],e['H'],e['C'];pins={}
def read(rel):
 p=ROOT/rel;pins[rel]=hashlib.sha256(p.read_bytes()).hexdigest();return json.loads(p.read_text())
def dec(ts):return {tuple(sorted(map(tuple,t)))for t in ts}
def edges(ts):return {tuple(sorted((a,b)))for t in ts for a,b in zip(t,t[1:]+t[:1])}
HE=edges(H)
def angle(ts,p):return sum(90 if e['dot'](*[e['sub'](v,p)for v in t if v!=p])==0 else 45 for t in ts if p in t)
# Exact per-vertex additive angle algebra; combinations are necessary labels only.
ordinary={k:[()]+[(i,)for i in range(8)if edges(fan(k,[i]))&HE]for k in C}
units={k:[(i,(i+1)%8)for i in range(8)if edges(fan(k,[i,(i+1)%8]))&HE and not(k=='N'and i==6)]for k in C}
refs={'L':0,'B':1,'E':4,'Tc':5}
# All named guards are accepted dependencies, never interpreted as a complete library.
guards=[]
def add(name,g):
 U,Z=dec(g['required']),dec(g['forbidden']);n=g.get('reflections',g.get('audit',{}).get('reflections'))
 if n is None:n=g.get('proof',{}).get('reflections')
 assert n is not None,name
 guards.append((name,U,Z,n));guards.append(('sigma:'+name,e['transform'](U),e['transform'](Z),n))
x=read('fourth-surplus-review/three-unit-b1-independent/check.json')
for name,g in x['named_guards'].items():add('148:'+name,g)
for rel in ['surplus-four-remote2110/peer-optical-review/check.json','surplus-four-remote2110/N6-four-review/check.json','surplus-four-remote2110/B-eight-review/check.json']:
 for name,g in read(rel)['paths'].items():add(name,g)
g=read('surplus-four-remote2110/roof-N5-search/verification.json');g['reflections']=4;add('right_leaf_four',g)
g=read('surplus-four-local/R23-top6-search/verification.json');g['whole_support']['reflections']=3;add('H4_smooth_three',g['whole_support'])
x=read('surplus-four-local/west-four-mixed-eleven-review/check.json')
for name,g in x['new_path_records'].items():
 # Own records store their proof's reflection number under proof.
 if 'required'in g:add('West_mixed:'+name,g)
templates=read('surplus-four-remote2110/parent-templates.json')['templates'];rows=[]
for t in templates:
 if t['parent']not in ('L','B'):continue # sigma handled by accepted guard transform
 parent=t['parent'];leaf=fan(tuple(t['remote_center']),[t['remote_sector']]);ps=t['parent_sectors'];base=H|fan(parent,ps)|leaf
 for site,us in units.items():
  if site==parent:continue
  for sectors in us:
   req=dict(refs)
   if parent=='B':req.pop('Tc') # no Tc5 forcing for larger B
   if site in req and req[site]not in sectors:continue
   fixed=base|fan(site,sectors);slots=[k for k in C if k not in(parent,site)]
   options={k:([s for s in ordinary[k]if req[k]in s]if k in req else ordinary[k])for k in slots}
   fixedpts={p for tr in fixed for p in tr};pts=fixedpts|{p for k in slots for opt in options[k]for tr in fan(k,opt)for p in tr}
   # Exclude baseline uncovered H-side C midpoints from b only. Full H stars unchanged.
   HC={p for p in fixedpts if (p[0]%2)!=(p[1]%2) and angle(H,p)==180}
   baseline={p for p in HC if angle(fixed,p)==180}
   # H-facing ordinary caps never complete a C pair, so baseline is fixed.
   J=sum(angle(fixed,p)==360 for p in pts if p[0]%2 or p[1]%2)
   for p in pts:
    if p[0]%2==p[1]%2==0:continue
    maximum=angle(fixed,p)+sum(max(angle(fan(k,s),p)for s in options[k])for k in slots)
    assert angle(fixed,p)==360 or maximum<360,(parent,ps,site,sectors,p,maximum)
   n=J # Q6+n, sN6-n, k6 =>n=J
   fixed_occ={k for k in slots if k in req};free=[k for k in slots if k not in req]
   # Store per-vertex independent angle coefficients, used in exact b0 equations.
   terms=[]
   for p in sorted(pts):
    if p in baseline or p[0]%2==p[1]%2==0:continue
    terms.append((p,angle(fixed,p),{k:{str(s):angle(fan(k,s),p)for s in options[k]}for k in slots}))
   covers=[];uncovered=[];necessary=0;excluded_smooth=0
   for opts in itertools.product(*(options[k]for k in slots)):
    if sum(bool(s)for s in opts)!=n:continue
    choice=dict(zip(slots,opts))
    if any(a+sum(co[k][str(choice[k])]for k in slots)==180 for p,a,co in terms):excluded_smooth+=1;continue
    necessary+=1
    # Symbolic tile membership envelope only; NOT geometry validation or a room.
    support=fixed|set().union(*(fan(k,s)for k,s in choice.items()))
    matching=[(g,nr)for g,u,z,nr in guards if u<=support and not z&support]
    label={k:list(s)for k,s in choice.items()if s}
    if matching:
     name,nr=min(matching,key=lambda g:g[1]);covers.append({'caps':label,'guard':name,'bound':nr})
    else:uncovered.append(label)
   rows.append({'parent':parent,'sectors':ps,'remote':t['remote_center'],'leaf':t['remote_sector'],'unit':site,'unit_sectors':list(sectors),'J':J,'ordinary_slots_required':n,'baseline_M_vertices':sorted(baseline),'angle_terms':[{'vertex':p,'fixed_degrees':a,'ordinary_coefficients':co}for p,a,co in terms],'necessary_labels':necessary,'smooth_excluded_labels':excluded_smooth,'covers':covers,'uncovered':uncovered})
summary={}
for r in rows:
 key=r['parent']+''.join(map(str,r['sectors']))+'/leaf'+str(r['leaf'])
 a=summary.setdefault(key,{'unit_forms':0,'necessary_labels':0,'uncovered':0});a['unit_forms']+=1;a['necessary_labels']+=r['necessary_labels'];a['uncovered']+=len(r['uncovered'])
pins[str(engine.relative_to(ROOT))]=hashlib.sha256(engine.read_bytes()).hexdigest();pins[str(Path(__file__).resolve().relative_to(ROOT))]=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
(HERE/'check.json').write_text(json.dumps({'status':'NECESSARY_CRITICAL2110_SLOT_GUARD_PROJECTION','templates':rows,'summary':summary,'source_sha256':pins,'limits':'Necessary angle/slot labels only. No strict simplicity or room existence assertion. Hand completeness and reference-forcing dependencies separate; unmatched does not mean dark. No new ray/word/path discovery.'},indent=2)+'\n');signal.alarm(0)
print(json.dumps(summary,indent=2))
for r in rows:
 if r['uncovered']:print('OPEN',r['parent'],r['sectors'],'leaf',r['leaf'],'unit',r['unit'],r['unit_sectors'],r['uncovered'])
