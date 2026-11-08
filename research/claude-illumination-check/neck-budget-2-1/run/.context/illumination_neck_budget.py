"""Sound local fan/domain propagation with the exact wall/exception budget.

This is a necessary relaxation, not a room enumerator or an illumination test.
It uses no ray cuts internally. A necessary triangle-connectivity backbone can
be propagated; this does not enforce a full room or Euler characteristic.
The input neck shortlist is conditional on earlier verified ray exclusions.
"""
from collections import defaultdict
import hashlib
import json
from pathlib import Path
from illumination_geometry import label,owners_of,local_sectors
from illumination_family_bound import triangles_in_cells
from illumination_three_two_star_bound import complete_support

OUT=Path(__file__).parent/'three-triples'

def metric_support(options,cap=23,base=14,exceptions=3):
    """Supported (walls, exceptions, charge-credit) tuples per local factor."""
    options=[set(rows) for rows in options]
    lo=-2*exceptions;hi=cap-base+2*exceptions
    def advance(states,opts):
        return {(w+a,b+c,q+d) for w,b,q in states for a,c,d in opts
                if w+a<=cap and b+c<=exceptions and lo<=q+d<=hi}
    prefix=[{(0,0,0)}]
    for rows in options:prefix.append(advance(prefix[-1],rows))
    suffix=[set() for _ in range(len(options)+1)];suffix[-1]={(0,0,0)}
    for i in reversed(range(len(options))):suffix[i]=advance(suffix[i+1],options[i])
    supported=[]
    for i,rows in enumerate(options):
        best={}
        for w,b,q in suffix[i+1]:
            key=(b,q-w);best[key]=min(w,best.get(key,cap+1))
        accepted=set()
        for a,c,d in rows:
            for w,b,q in prefix[i]:
                needed=(exceptions-b-c,-base-(q-w)-(d-a))
                if w+a+best.get(needed,cap+1)<=cap:
                    accepted.add((a,c,d));break
        supported.append(accepted)
    walls=sorted({w for w,b,q in prefix[-1] if b==exceptions and q==w-base})
    return supported,walls


def factors_for(ts,bounded):
    incident=defaultdict(list)
    for i,t in enumerate(ts):
        for p in t:incident[p].append(i)
    full={(2*a,2*b) for a,b in bounded['full']};factors=[]
    for p,ids in sorted(incident.items()):
        kind=label(p);rows=[]
        for mask in range(1<<len(ids)):
            chosen=[ts[i] for j,i in enumerate(ids) if mask>>j&1]
            owners=owners_of(chosen);opened={e for e,os in owners.items() if len(os)==2}
            sizes,is_full=local_sectors(chosen,p,opened)
            if len(sizes)>1 or kind=='A' and is_full!=(p in full):continue
            wall=int(bool(sizes) and sizes[0]!=4)
            bad=int(kind!='A' and (is_full or 4 in sizes))
            credit=(2 if is_full else 1) if bad else 0
            charge=0 if kind!='A' or is_full or not sizes else 3 if sizes[0]==4 else sizes[0]
            missing=int(kind=='A' and (p[0]//2,p[1]//2) in bounded['mandatory']-bounded['full'] and not chosen)
            rows.append((mask,wall,bad,charge-credit,len(chosen) if kind=='A' else 0,credit+missing))
        factors.append(dict(point=p,kind=kind,ids=ids,rows=rows))
    return factors


def connectivity_backbone(adjacency,domains):
    """Force bridges between already occupied tiles; discard unreachable tiles."""
    possible={i for i,d in enumerate(domains) if d&2};forced={i for i,d in enumerate(domains) if d==2}
    assert forced
    root=min(forced)
    def reachable(removed=None):
        if root==removed:return set()
        seen={root};todo=[root]
        for i in todo:
            for j in adjacency[i]&possible-seen:
                if j!=removed:seen.add(j);todo.append(j)
        return seen
    connected=reachable()
    if not forced<=connected:return None
    result=list(domains)
    for i in possible-connected:result[i]=1
    for i in connected-forced:
        if not forced<=reachable(i):result[i]=2
    return result


def propagate(ts,bounded,templates,pattern,connectivity=False):
    outside,first,second=pattern;outside=set(map(tuple,outside));domains=[3]*len(ts)
    for i,t in enumerate(ts):
        a=next(p for p in t if label(p)=='A');cell=(a[0]//2,a[1]//2)
        if cell not in bounded['mandatory']|outside:domains[i]=1
    for cell,mask in [((1,0),first),((1,1),second)]:
        ids=[i for i,t in enumerate(ts) if (2*cell[0],2*cell[1]) in t]
        for j,i in enumerate(ids):domains[i]=1<<int(bool(mask>>j&1))
    factors=[]
    for f in templates:
        rows=f['rows']
        if f['kind']=='A' and (f['point'][0]//2,f['point'][1]//2) in outside:
            rows=[row for row in rows if row[0]]
        factors.append(dict(f,rows=list(rows)))
    adjacency={i:set() for i in range(len(ts))}
    for _,owners in owners_of(ts).items():
        if len(owners)==2:
            a,b=owners;adjacency[a].add(b);adjacency[b].add(a)
    trace=[]
    for iteration in range(100):
        before=sum(len(f['rows']) for f in factors);old_domains=list(domains)
        if connectivity:
            domains=connectivity_backbone(adjacency,domains)
            if domains is None:return dict(status='RELAXATION_INFEASIBLE',iteration=iteration,reason='potential triangle connectivity')
        for f in factors:
            f['rows']=[r for r in f['rows'] if all(domains[i]&(1<<((r[0]>>j)&1)) for j,i in enumerate(f['ids']))]
        if any(not f['rows'] for f in factors):return dict(status='RELAXATION_INFEASIBLE',iteration=iteration,reason='local fan')
        allowed,walls=metric_support([{r[1:4] for r in f['rows']} for f in factors])
        for f,metrics in zip(factors,allowed):f['rows']=[r for r in f['rows'] if r[1:4] in metrics]
        if any(not f['rows'] for f in factors):return dict(status='RELAXATION_INFEASIBLE',iteration=iteration,reason='wall/charge/exception budget')
        for column,limit in [(4,36),(5,6)]:
            minima=[min(r[column] for r in f['rows']) for f in factors];total=sum(minima)
            for f,own in zip(factors,minima):f['rows']=[r for r in f['rows'] if r[column]+total-own<=limit]
            if any(not f['rows'] for f in factors):return dict(status='RELAXATION_INFEASIBLE',iteration=iteration,reason=f'nonnegative budget {column}')
        for f in factors:
            for j,i in enumerate(f['ids']):
                support=0
                for r in f['rows']:support|=1<<((r[0]>>j)&1)
                domains[i]&=support
        assert all(domains)
        after=sum(len(f['rows']) for f in factors)
        trace.append(dict(iteration=iteration+1,rows_before=before,rows_after=after,unknown_triangles=sum(d==3 for d in domains)))
        if before==after and domains==old_domains:break
    else:raise AssertionError('propagation did not converge')
    cells=[]
    for f in factors:
        if f['kind']!='A':continue
        cell=(f['point'][0]//2,f['point'][1]//2)
        if cell not in bounded['mandatory']|outside:continue
        cells.append(dict(cell=cell,masks=sorted({r[0] for r in f['rows']}),charge_values=sorted({r[3] for r in f['rows']}),tile_counts=sorted({r[4] for r in f['rows']})))
    forced_bad=[f['point'] for f in factors if all(r[2] for r in f['rows'])]
    possible_bad=[f['point'] for f in factors if any(r[2] for r in f['rows'])]
    return dict(status='RELAXATION_FEASIBLE',connectivity_backbone=connectivity,outside_cells=sorted(outside),first_mask=first,second_mask=second,
                iterations=trace,triangle_domains=domains,cells=cells,relaxed_wall_values=walls,
                forced_exceptions=forced_bad,possible_exceptions=possible_bad,
                factor_masks=[dict(point=f['point'],masks=[r[0] for r in f['rows']]) for f in factors],
                scope='Necessary local fan/budget consequences; consistency is not a valid connected room or darkness certificate.')


def run():
    bounded=complete_support((2,1));ts=triangles_in_cells(bounded['allowed']);factors=factors_for(ts,bounded)
    source=OUT/'neck-patterns-2-1.json';patterns=json.loads(source.read_text())['canonical_patterns'];cases=[];baselines=[]
    for number,pattern in enumerate(patterns,1):
        baseline=propagate(ts,bounded,factors,pattern);baseline['neck_type']=number;baselines.append(baseline)
        result=propagate(ts,bounded,factors,pattern,connectivity=True);result['neck_type']=number;cases.append(result)
        print(json.dumps(dict(event='neck_budget',neck_type=number,status=result['status'],
                             rounds=len(result.get('iterations',[])),forced_exceptions=result.get('forced_exceptions'),
                             neighbor_domains=[dict(cell=c['cell'],choices=len(c['masks'])) for c in result.get('cells',[]) if tuple(c['cell']) not in ((0,0),(2,1),(1,0),(1,1))])),flush=True)
    data=dict(status='NECESSARY_RELAXATION',source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
              triangle_index_sha256=hashlib.sha256(json.dumps(ts).encode()).hexdigest(),cases=cases,budget_only_baselines=baselines,
              assumptions=dict(max_walls=23,full_A=2,BC_exceptions=3,max_triangles=36,max_credit_plus_missing=6),
              scope='No ray cuts, Euler enforcement or room search within the propagation. Potential triangle connectivity is propagated as a necessary condition. The12 input neck types themselves rely on earlier ray exclusions.')
    (OUT/'neck-budget-2-1.json').write_text(json.dumps(data,indent=2)+'\n')

if __name__=='__main__':run()
