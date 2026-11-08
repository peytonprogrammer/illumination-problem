"""Read-only property audit of seven frozen guard packets; no tracing or solving."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import json,hashlib
from functools import cmp_to_key, lru_cache
b=Path(__file__).resolve().parent
src=b.parents[1]/'claude-illumination-check'
names=['two-global-1-1','two-global-2-0','two-global-2-1','two-global-2-2','two-pair-search-1-1','two-pair-search-2-0','two-pair-search-2-1']
counts=Counter(); examples=[]; inputs={}; files={}
def label(p):
 if p[0].denominator!=1 or p[1].denominator!=1:return None
 x,y=map(int,p)
 return 'A' if x%2==y%2==0 else 'B' if x%2==y%2==1 else 'C'
def sub(p,q):return tuple(p[i]-q[i] for i in (0,1))
def unpack(p):return tuple(F(*c) for c in p)
def show(p):return [str(x) for x in p]

compat=Counter();compat_examples=[]
all_saved={};dirty_candidates=[]
def square(i,j):
 c=[(i,j),(i+1,j),(i+1,j+1),(i,j+1)]
 parts=[(0,1,2),(0,2,3)] if (i-j)%2==0 else [(1,2,3),(1,3,0)]
 return [tuple(sorted(c[k] for k in part)) for part in parts]
@lru_cache(None)
def incident(r):
 x,y=map(int,r)
 ts={t for i in (x-1,x) for j in (y-1,y) for t in square(i,j) if (x,y) in t}
 def v(t):return (sum(z[0] for z in t)-3*x,sum(z[1] for z in t)-3*y)
 def cmp(t,u):
  a,b=v(t),v(u)
  h=lambda z:0 if z[1]>0 or (z[1]==0 and z[0]>=0) else 1
  if h(a)!=h(b):return h(a)-h(b)
  c=a[0]*b[1]-a[1]*b[0]
  return -1 if c>0 else 1 if c<0 else 0
 out=tuple(sorted(ts,key=cmp_to_key(cmp)))
 assert len(out)==(4 if label(r)=='C' else 8)
 return out
@lru_cache(None)
def raw_masks(n):
 masks={0}
 for size in range(1,n):
  if size==n//2:continue
  for start in range(n):masks.add(sum(1<<((start+j)%n) for j in range(size)))
 return tuple(sorted(masks))
def indices(tgt):
 full={(0,0),tgt};nb=[(1,0),(-1,0),(0,1),(0,-1)]
 mandatory=full|{(x+dx,y+dy) for x,y in full for dx,dy in nb}
 r=9-len(mandatory-full);assert r>=0
 allowed={(x,y) for x in range(min(x for x,y in mandatory)-r,max(x for x,y in mandatory)+r+1)
                 for y in range(min(y for x,y in mandatory)-r,max(y for x,y in mandatory)+r+1)
          if min(abs(x-u)+abs(y-v) for u,v in mandatory)<=r}
 ts={t for x,y in allowed for i in (2*x-1,2*x) for j in (2*y-1,2*y) for t in square(i,j) if (2*x,2*y) in t}
 return tuple(sorted(ts))
def locally_compatible(g,table,pts,hit,other):
 j,p,ax=hit;normal=1-ax
 if {label(p),label(other)}!={'B','C'}:return False,'other endpoint has wrong parity'
 facts={table[i]:bool(value) for i,value in g['tile_facts']}
 bc={r for t in facts for r in t if label(tuple(map(F,r))) in ('B','C')}
 bc|={p,other}
 inside=1 if pts[j-1][normal]>p[normal] else -1
 c=p if label(p)=='C' else other
 tip=list(c);tip[normal]-=inside;tip=tuple(tip)
 assert label(tip)=='A'
 if any(facts.get(t) is True for t in incident(tip)):
  return False,'nonempty original pocket-tip fan in core'
 for r in bc:
  ts=incident(r);known=values=0
  for k,t in enumerate(ts):
   if t in facts:
    known|=1<<k
    if facts[t]:values|=1<<k
  if r in (p,other):
   mask=sum(1<<k for k,t in enumerate(ts) if inside*(sum(v[normal] for v in t)-3*r[normal])>0)
   options=(mask,)
  else:options=raw_masks(len(ts))
  if not any(mask&known==values for mask in options):
   return False,'incompatible prescribed local vertex status'
 return True,'necessary local compatibility only'

for name in names:
 p=src/(name+'.json'); raw=p.read_bytes();d=json.loads(raw)
 inputs[str(p)]=hashlib.sha256(raw).hexdigest();fc=Counter()
 tgt=tuple(map(int,name.split('-')[-2:]));table=indices(tgt)
 if 'complete_support_triangles' in d['summary']:assert len(table)==d['summary']['complete_support_triangles']
 for ri,r in enumerate(d['records']):
  for gi,g in enumerate(r['derived_guards']):
   fc['guards']+=1
   assert len(dict(g['tile_facts']))==len(g['tile_facts'])
   mask=sum(1<<i for i,value in g['tile_facts'])
   values=sum(1<<i for i,value in g['tile_facts'] if value)
   room={tuple(sorted(tuple(v) for v in t)) for t in g['room']['triangles']}
   assert all((table[i] in room)==bool(value) for i,value in g['tile_facts'])
   pts=list(map(unpack,g['witness']['path']))
   all_saved.setdefault(tgt,[]).append(({'packet':name,'record':ri,'guard':gi},mask,values,pts))
   hits=[]; unsupported=[]
   for j,q in enumerate(pts[1:-1],1):
    if label(q) not in ('B','C'):continue
    v=sub(q,pts[j-1]);w=sub(pts[j+1],q)
    ax=None
    if v[0]*w[1]+v[1]*w[0]==0:
     if v[0]*w[0]<0 and v[1]*w[1]>=0:ax=1
     elif v[1]*w[1]<0 and v[0]*w[0]>=0:ax=0
    if ax is None:unsupported.append(j);continue
    hits.append((j,q,ax))
   distinct={q for _,q,_ in hits}
   if unsupported:
    fc['has_nonaxis_integer_bounce']+=1;continue
   if not hits:
    fc['no_recorded_BC_bounce']+=1;continue
   if len(distinct)>2:
    fc['more_than_two_recorded_BC_points']+=1;continue
   if len(distinct)==2:
    q,z=sorted(distinct)
    # A sealed core has only two smooth BC points, an adjacent B/C pair on one axis wall.
    if {label(q),label(z)}!={'B','C'} or sum(abs(x-y) for x,y in zip(q,z))!=1:
     fc['two_points_incompatible_with_single_unit_seal']+=1;continue
    axis=0 if q[1]==z[1] else 1
    if any(ax!=axis for _,_,ax in hits):
     fc['two_points_incompatible_wall_tangents']+=1;continue
    intervals=[(q,z,axis)]
    fc['two_adjacent_BC_points']+=1
   else:
    q=next(iter(distinct));axes={ax for _,_,ax in hits}
    if len(axes)!=1:
     fc['same_point_incompatible_wall_tangents']+=1;continue
    axis=next(iter(axes));intervals=[]
    for sg in [-1,1]:
     z=list(q);z[axis]+=sg;intervals.append((q,tuple(z),axis))
    fc['one_distinct_BC_point']+=1
    for q,z,ax in intervals:
     hit=next(hit for hit in hits if hit[1]==q)
     ok,why=locally_compatible(g,table,pts,hit,z)
     if not ok:
      compat['locally_incompatible_interval_placements']+=1;continue
     compat['locally_compatible_interval_placements']+=1
     nx=1-ax;lo,hi=sorted((q[ax],z[ax]))
     offenders=[(jj,v) for jj,v in enumerate(pts[1:-1],1) if v[nx]==q[nx] and lo<v[ax]<hi]
     if offenders:
      compat['locally_compatible_dirty_intervals']+=1
      dirty_candidates.append((tgt,{'packet':name,'record':ri,'guard':gi},g,pts,hit,z))
      if len(compat_examples)<8:compat_examples.append({'packet':name,'record':ri,'guard':gi,'endpoints':[show(q),show(z)],'offenders':[{'index':jj,'point':show(v)} for jj,v in offenders]})
     else:compat['locally_compatible_clear_intervals']+=1
   dirty=[]
   for q,z,ax in intervals:
    normal=1-ax;lo,hi=sorted((q[ax],z[ax]))
    for j,v in enumerate(pts[1:-1],1):
     if v[normal]==q[normal] and lo<v[ax]<hi:
      dirty.append({'endpoint':show(q),'other_endpoint':show(z),'bounce_index':j,'bounce':show(v)})
   if dirty:
    fc['potential_open_seal_bounce']+=1
    if len(examples)<12:examples.append({'packet':name,'record':ri,'guard':gi,'violations':dirty})
   else:fc['all_compatible_unit_intervals_clear_at_recorded_bounces']+=1
 counts.update(fc);files[name]=dict(fc)

def extended_clause(g,table,pts,hit,other):
 j,p,ax=hit;normal=1-ax
 side=1 if pts[j-1][normal]>p[normal] else -1
 ix={t:i for i,t in enumerate(table)}
 facts=dict(g['tile_facts']);added={}
 c=p if label(p)=='C' else other
 tip=list(c);tip[normal]-=side;tip=tuple(tip)
 for r in (p,other,tip):
  for t in incident(r):
   value=0 if r==tip else int(side*(sum(v[normal] for v in t)-3*r[normal])>0)
   if t not in ix:
    if value:return None,'required triangle outside inherited complete support'
    continue
   i=ix[t]
   if i in facts and facts[i]!=value:return None,'conflicting endpoint/tip facts'
   facts[i]=value;added[i]=value
 mask=sum(1<<i for i in facts);values=sum(1<<i for i,v in facts.items() if v)
 return (mask,values,added,side),'ok'
substitutions=[];subcounts=Counter();clear_cache={}
for tgt,where,g,pts,hit,z in dirty_candidates:
 table=indices(tgt);extended,why=extended_clause(g,table,pts,hit,z)
 q=hit[1];ax=hit[2]
 item={'dirty_guard':where,'portal_endpoints':[show(q),show(z)]}
 if extended is None:
  subcounts['discharged_by_local_or_support_conflict']+=1
  item.update({'status':'INCOMPATIBLE_WITH_INHERITED_SUPPORT','reason':why})
 else:
  mask,values,added,side=extended
  key=(tgt,tuple(sorted((q,z))))
  if key not in clear_cache:
   nx=1-ax;lo,hi=sorted((q[ax],z[ax]))
   clear_cache[key]=[(wh,hm,hv) for wh,hm,hv,hpts in all_saved[tgt]
                    if not any(v[nx]==q[nx] and lo<v[ax]<hi for v in hpts[1:-1])]
  replacement=next((wh for wh,hm,hv in clear_cache[key]
                    if hm & ~mask==0 and (hv^values)&hm==0),None)
  item['core_interior_side']=side
  if replacement is not None:
   subcounts['discharged_by_clear_saved_guard_subset']+=1
   item.update({'status':'COVERED_BY_CLEAR_SAVED_GUARD','replacement':replacement,'added_facts':sorted(added.items())})
  else:
   subcounts['unresolved_dirty_guard_interval_implications']+=1
   item['status']='UNRESOLVED_NO_SUBSET_CERTIFICATE'
 substitutions.append(item)
assert len(substitutions)==compat['locally_compatible_dirty_intervals']


@lru_cache(None)
def a_masks(n):
 masks={0,(1<<n)-1}
 for size in range(1,n):
  for start in range(n):masks.add(sum(1<<((start+j)%n) for j in range(size)))
 return tuple(sorted(masks))
@lru_cache(None)
def support_vertices(table):return tuple(sorted({r for t in table for r in t}))
def propagate(tgt,table,initial,hit,other,side,charge_bound=None,forbidden_clear_guards=()):
 mask,values=initial;j,p,ax=hit;nx=1-ax
 c=p if label(p)=='C' else other
 tip=list(c);tip[nx]-=side;tip=tuple(tip)
 marks={(0,0),(2*tgt[0],2*tgt[1])}
 ix={t:i for i,t in enumerate(table)}
 vertices=set(support_vertices(table))|{p,other,tip}|marks
 domains=[]
 for r in sorted(vertices):
  ts=incident(r);n=len(ts)
  if r==tip:options=(0,)
  elif r in marks:options=((1<<n)-1,)
  elif r in (p,other):options=(sum(1<<k for k,t in enumerate(ts) if side*(sum(v[nx] for v in t)-3*r[nx])>0),)
  else:
   options=a_masks(n) if label(tuple(map(F,r)))=='A' else raw_masks(n)
   if charge_bound is not None and label(tuple(map(F,r)))=='A':options=tuple(d for d in options if d!=(1<<n)-1)
  domains.append([r,tuple(ix.get(t) for t in ts),list(options)])
 rounds=0;guard_forces=0
 maxrounds=len(table)+sum(len(row[2]) for row in domains)+2
 def charge(d,n):
  k=d.bit_count()
  return 0 if k in (0,n) else 3 if k==4 else k
 while True:
  rounds+=1;assert rounds<=maxrounds
  old=mask;oldsize=sum(len(row[2]) for row in domains)
  for row in domains:
   r,positions,options=row
   known=ones=0
   for k,i in enumerate(positions):
    if i is None:known|=1<<k
    elif mask>>i&1:
     known|=1<<k
     if values>>i&1:ones|=1<<k
   valid=[d for d in options if d&known==ones]
   if not valid:return None,{'rounds':rounds,'conflict_vertex':list(map(str,r))}
   row[2]=valid
   allone=(1<<len(positions))-1;anyone=0
   for d in valid:allone&=d;anyone|=d
   for k,i in enumerate(positions):
    if i is None or mask>>i&1:continue
    if allone>>k&1:mask|=1<<i;values|=1<<i
    elif not (anyone>>k&1):mask|=1<<i
  mincharge=None
  if charge_bound is not None:
   adomains=[row for row in domains if label(tuple(map(F,row[0])))=='A']
   mins=[min(charge(d,len(row[1])) for d in row[2]) for row in adomains]
   mincharge=sum(mins)
   if mincharge>charge_bound:return None,{'rounds':rounds,'minimum_A_charge':mincharge,'charge_cap':charge_bound}
   for row,low in zip(adomains,mins):
    row[2]=[d for d in row[2] if mincharge-low+charge(d,len(row[1]))<=charge_bound]
    assert row[2]
  for where,hm,hv in forbidden_clear_guards:
   if (hv^values)&hm&mask:continue
   unknown=hm&~mask
   if unknown==0:
    return None,{'rounds':rounds,'clear_guard_forced':where,'negated_clear_guard_unit_forces':guard_forces}
   if unknown&(unknown-1)==0:
    mask|=unknown
    if hv&unknown:values&=~unknown
    else:values|=unknown
    guard_forces+=1
  if mask==old and sum(len(row[2]) for row in domains)==oldsize:
   return (mask,values),{'rounds':rounds,'forced_facts':mask.bit_count()-initial[0].bit_count(),'minimum_A_charge':mincharge,'negated_clear_guard_unit_forces':guard_forces}
propcounts=Counter();propcases=[]
for candidate,earlier in zip(dirty_candidates,substitutions):
 if earlier['status']!='UNRESOLVED_NO_SUBSET_CERTIFICATE':continue
 tgt,where,g,pts,hit,z=candidate
 table=indices(tgt);ext,why=extended_clause(g,table,pts,hit,z)
 assert ext is not None
 mask,values,added,side=ext
 closure,detail=propagate(tgt,table,(mask,values),hit,z,side)
 item={'dirty_guard':where,'portal_endpoints':earlier['portal_endpoints'],'propagation':detail}
 if closure is None:
  propcounts['discharged_by_local_vertex_contradiction']+=1
  item['status']='LOCAL_VERTEX_CONTRADICTION'
 else:
  mask,values=closure;key=(tgt,tuple(sorted((hit[1],z))))
  replacement=next((wh for wh,hm,hv in clear_cache[key] if hm&~mask==0 and (hv^values)&hm==0),None)
  if replacement is not None:
   propcounts['discharged_by_clear_guard_after_propagation']+=1
   item.update({'status':'COVERED_BY_CLEAR_SAVED_GUARD_AFTER_PROPAGATION','replacement':replacement})
  else:
   propcounts['remaining_unresolved_guard_intervals']+=1
   item['status']='UNRESOLVED_AFTER_LOCAL_RULE_CLOSURE'
 propcases.append(item)
assert sum(propcounts.values())==subcounts['unresolved_dirty_guard_interval_implications']


chargedcounts=Counter();chargedcases=[]
remainingkeys={(d['dirty_guard']['packet'],d['dirty_guard']['record'],d['dirty_guard']['guard'],tuple(tuple(p) for p in d['portal_endpoints'])) for d in propcases if d['status']=='UNRESOLVED_AFTER_LOCAL_RULE_CLOSURE'}
for candidate in dirty_candidates:
 tgt,where,g,pts,hit,z=candidate
 q=hit[1];key0=(where['packet'],where['record'],where['guard'],tuple(tuple(show(p)) for p in (q,z)))
 if key0 not in remainingkeys:continue
 table=indices(tgt);ext,why=extended_clause(g,table,pts,hit,z);assert ext is not None
 mask,values,added,side=ext
 closure,detail=propagate(tgt,table,(mask,values),hit,z,side,charge_bound=11)
 item={'dirty_guard':where,'portal_endpoints':[show(q),show(z)],'propagation':detail}
 if closure is None:
  chargedcounts['discharged_by_I2_charge_or_vertex_contradiction']+=1
  item['status']='I2_CHARGE_OR_VERTEX_CONTRADICTION'
 else:
  mask,values=closure;key=(tgt,tuple(sorted((q,z))))
  replacement=next((wh for wh,hm,hv in clear_cache[key] if hm&~mask==0 and (hv^values)&hm==0),None)
  if replacement is not None:
   chargedcounts['discharged_by_clear_guard_after_I2_charge_propagation']+=1
   item.update({'status':'COVERED_AFTER_I2_CHARGE_PROPAGATION','replacement':replacement})
  else:
   chargedcounts['remaining_unresolved_I2_guard_intervals']+=1
   item['status']='UNRESOLVED_AFTER_I2_CHARGE_PROPAGATION'
 chargedcases.append(item)
assert sum(chargedcounts.values())==propcounts['remaining_unresolved_guard_intervals']


unitcounts=Counter();unitcases=[]
unitkeys={(d['dirty_guard']['packet'],d['dirty_guard']['record'],d['dirty_guard']['guard'],tuple(tuple(p) for p in d['portal_endpoints'])) for d in chargedcases if d['status']=='UNRESOLVED_AFTER_I2_CHARGE_PROPAGATION'}
for candidate in dirty_candidates:
 tgt,where,g,pts,hit,z=candidate;q=hit[1]
 key0=(where['packet'],where['record'],where['guard'],tuple(tuple(show(p)) for p in (q,z)))
 if key0 not in unitkeys:continue
 table=indices(tgt);ext,why=extended_clause(g,table,pts,hit,z);assert ext is not None
 mask,values,added,side=ext;key=(tgt,tuple(sorted((q,z))))
 closure,detail=propagate(tgt,table,(mask,values),hit,z,side,charge_bound=11,forbidden_clear_guards=clear_cache[key])
 item={'dirty_guard':where,'portal_endpoints':[show(q),show(z)],'propagation':detail}
 if closure is None:
  unitcounts['covered_by_clear_guard_disjunction_unit_resolution']+=1
  item['status']='COVERED_BY_CLEAR_GUARD_DISJUNCTION'
 else:
  unitcounts['remaining_unresolved_I2_guard_intervals']+=1
  item['status']='UNRESOLVED_AFTER_UNIT_RESOLUTION'
 unitcases.append(item)
assert sum(unitcounts.values())==chargedcounts['remaining_unresolved_I2_guard_intervals']

assert counts['guards']==3660,counts
out={'clear_guard_unit_resolution_counts':dict(unitcounts),'clear_guard_unit_resolution_cases':unitcases,'I2_charge_propagation_counts':dict(chargedcounts),'I2_charge_propagation_cases':chargedcases,'local_propagation_counts':dict(propcounts),'local_propagation_cases':propcases,'saved_guard_substitution_counts':dict(subcounts),'saved_guard_substitutions':substitutions,'local_compatibility_counts':dict(compat),'locally_compatible_dirty_examples':compat_examples,'status':'FROZEN_PACKET_PROPERTY_AUDIT_COMPLETE','counts':dict(counts),'files':files,'input_sha256':inputs,
'first_dirty_examples':examples,'universal_portal_avoidance_proved':False,
'scope':'Only rational arithmetic on previously saved path vertices. No new trajectories, room construction, direction/word search, solver, or coverage refutation. Finite local-mask tests are only necessary compatibility conditions, never a feasible-room or coverage certificate. No room eligibility or full guard applicability conclusion follows from these counts.'}
(b/'pocket-guard-portal-audit.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'counts':out['counts'],'local_compatibility_counts':dict(compat),'saved_guard_substitution_counts':dict(subcounts),'local_propagation_counts':dict(propcounts),'I2_charge_propagation_counts':dict(chargedcounts),'clear_guard_unit_resolution_counts':dict(unitcounts),'first_compatible_dirty_example':compat_examples[:1],'first_dirty_example':examples[:1]},indent=2))
