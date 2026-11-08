"""B06 independent prescribed verification. No author imports, orbit traversal or search.
Walks are obtained by cyclic-list slicing, independently of the author's iterative walker.
Run from any cwd: python3 -B <this file>.
"""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import gzip, hashlib, json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
BASE=HERE.parent/'construction'
REQUEST=BASE/'global-relational-exchange-review-request.json'
req=json.loads(REQUEST.read_text())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pins():
    out={}
    for group in ('files_sha256','dependencies_sha256'):
        for name,expected in req[group].items():
            path=BASE/name if group=='files_sha256' else ROOT.parent/name
            actual=digest(path)
            assert actual==expected,(name,actual,expected)
            out[str(path)]=actual
    return out
before=pins()
author=json.loads((BASE/'global-relational-exchange-check.json').read_text())
old=json.loads((BASE/'global-exchange-periodic-check.json').read_text())
audit=json.loads((ROOT/'codex-proof-verification/specialist-ideas/label-descent-audit.json').read_text())
raw=gzip.decompress((HERE/'marked-origami-known22-closure.gz').read_bytes())
assert hashlib.sha256(raw).hexdigest()==req['raw_known22_certificate_sha256']
assert len(raw)==10368*180
# Read the EXISTING lexicographically sorted records, without generating a neighbor set.
saved=sorted(tuple(tuple(raw[k+j*60:k+(j+1)*60]) for j in range(3)) for k in range(0,len(raw),180))
assert len(set(saved))==10368
A=saved[462]
assert saved[0]==tuple(map(tuple,audit['initial_state']))
def inverse(p):return tuple(p.index(i) for i in range(len(p)))
def product(*ps):
    out=tuple(range(len(ps[0])))
    for p in reversed(ps):out=tuple(p[i] for i in out)
    return out

def cycles(p):
    remaining=set(range(len(p)));out=[]
    while remaining:
        start=min(remaining);c=[start];x=p[start]
        while x!=start:
            assert x in remaining and x not in c
            c.append(x);x=p[x]
        remaining.difference_update(c);out.append(c)
    return out

def comm(h,v):return product(v,h,inverse(v),inverse(h))
def step(st,letter):
    h,v,L=st
    if letter=='T':v=product(v,inverse(h))
    elif letter=='Ti':v=product(v,h)
    elif letter=='U':h=product(h,inverse(v))
    elif letter=='Ui':h=product(h,v)
    else:raise AssertionError(letter)
    return h,v,L

def walk_records(p,L,Z):
    # Each p-cycle is a cyclic ordered list. Reverse its list to reverse orientation.
    records=[]
    for cyc in cycles(p):
        for sign,order in ((1,cyc),(-1,list(reversed(cyc)))):
            for j,start in enumerate(order):
                color=L[start]
                if color not in (1,2):continue
                forward=order[j+1:]+order[:j+1]
                stops=[k for k,x in enumerate(forward) if x in Z or L[x]==3-color or x==start]
                stop=stops[0];trace=forward[:stop+1];x=trace[-1]
                kind='zero' if x in Z else 'opposite' if L[x]==3-color else 'periodic'
                records.append(dict(color=color,sign=sign,start=start,terminal_type=kind,terminal_slot=x,trace=trace))
    return sorted(records,key=lambda r:(r['color'],-r['sign'],r['start']))

def measure(records,zeros):
    loads=[];F=0;same=0
    for sign in (1,-1):
        for z,cy in enumerate(zeros):
            counts=[]
            for color in (1,2):
                counts.append(Counter(r['terminal_slot'] for r in records if r['color']==color and r['sign']==sign and r['terminal_type']=='zero' and r['terminal_slot'] in cy))
            a,b=counts
            overlap=sum(a[x]*b[x] for x in cy);same+=overlap
            count=sum(a[x]*b[y] for x in cy for y in cy if x!=y);F+=count
            if a or b:loads.append(dict(sign=sign,zero_id=z,cycle=cy,source_slots={str(x):n for x,n in a.items()},target_slots={str(x):n for x,n in b.items()},shared_pairs=count))
    assert same==0
    return dict(F=F,H_pm=sum(r['color']==1 and r['terminal_type']=='opposite' for r in records),same_slot_pairs=same,incidences=loads,records=records)

def records_equal(x,y):
    key=lambda r:(r['color'],r['sign'],r['start'])
    return sorted(x,key=key)==sorted(y,key=key)
rows=[];compared_records=0;compared_loads=0
for row in author['rows']:
    name=row['name']
    st=tuple(tuple(row[k]) for k in ('h','v','labels'))
    if name=='pinned_lex_root':assert st==saved[0]
    else:
        expected=A
        word=name.split(':')[1].split(',') if name.split(':')[1] else []
        for letter in word:expected=step(expected,letter)
        assert st==expected,('raw provenance',name)
        prior=next(r for r in old['rows'] if r['word']==word)
        assert st==(tuple(prior['h']),tuple(prior['v']),tuple(old['base_labels']))
    h,v,L=st;N=len(h)
    assert sorted(h)==sorted(v)==list(range(N)) and L.count(1)==L.count(2)==4
    C=comm(h,v);zeros=[c for c in cycles(C) if len(c)>1];Z=set(sum(zeros,[]))
    assert len(zeros)==9 and all(len(c)==3 for c in zeros)
    assert all(C[i]==i for i,x in enumerate(L) if x in (1,2))
    assert all(L[i]==3 for i in Z) and sum(x==3 and C[i]==i for i,x in enumerate(L))==13
    connected={0}; frontier=[0]
    while frontier:
        i=frontier.pop()
        for j in (h[i],v[i]):
            if j not in connected:connected.add(j);frontier.append(j)
    assert len(connected)==N
    assert zeros==row['zero_cycles']
    ht,vt,_=step(st,'T');hu,vu,_=step(st,'U');d=product(h,inverse(v))
    assert C==comm(ht,vt)==comm(hu,vu)
    assert ht==h and vu==v and vt==inverse(d) and hu==d
    permutations={'h':h,'v':v,'d':d,'T_v':vt,'U_h':hu}
    data={k:measure(walk_records(p,L,Z),zeros) for k,p in permutations.items()}
    for k,ak in [('h','horizontal'),('v','vertical'),('T_v','T_vertical'),('U_h','U_horizontal')]:
        a=row[ak];ours=data[k]
        assert records_equal(ours['records'],a['records']),(name,k,'full record')
        for field in ['F','H_pm','same_slot_pairs','incidences']:assert ours[field]==a[field],(name,k,field)
        compared_records+=len(ours['records']);compared_loads+=len(ours['incidences'])
    swapped=[dict(r,sign=-r['sign']) for r in data['d']['records']]
    assert records_equal(data['T_v']['records'],swapped)
    assert records_equal(data['U_h']['records'],data['d']['records'])
    assert records_equal(walk_records(ht,L,Z),data['h']['records'])
    assert records_equal(walk_records(vu,L,Z),data['v']['records'])
    # Common relabelling retains the full ordered records and zero-cycle relation.
    sigma=tuple(reversed(range(N)));si=inverse(sigma)
    relabel=lambda p:product(sigma,p,si)
    L2=tuple(L[si[i]] for i in range(N));Z2={sigma[x] for x in Z}
    zeros2=[c for c in cycles(relabel(C)) if len(c)>1]
    for k,p in permutations.items():
        transformed=[dict(r,start=sigma[r['start']],terminal_slot=sigma[r['terminal_slot']],trace=[sigma[x] for x in r['trace']]) for r in data[k]['records']]
        got=walk_records(relabel(p),L2,Z2)
        assert records_equal(transformed,got)
        assert measure(got,zeros2)['F']==data[k]['F']
    fh,fv,fd=[data[k]['F'] for k in ('h','v','d')];D=2*fd-fh-fv;H=data['h']['H_pm']
    gap=16*N*(H-D)-(9-len(zeros))*fh
    for k,val in dict(F_h=fh,F_v=fv,F_diag=fd,D=D,H_pm=H,candidate_gap_times_16N=gap,candidate_pass=gap>=0,candidate_domain=True).items():assert row[k]==val,(name,k)
    rows.append(dict(name=name,n=N,r=len(zeros),F_h=fh,F_v=fv,F_d=fd,D=D,H_pm=H,candidate_gap_times_16N=gap,full_records=data))
assert author['failed_named_controls']==[r['name'] for r in rows if r['candidate_gap_times_16N']<0]
# Square: coordinate invariants prove all three specified directions avoid opposite marks.
S={(x,y) for x in (12,36) for y in (12,36)};T={(x,y) for x in (16,32) for y in (18,30)}
assert len(S)==len(T)==4 and S.isdisjoint(T)
invariants=[lambda p:p[1],lambda p:p[0],lambda p:(p[0]+p[1])%48]
for invariant in invariants:assert {invariant(p) for p in S}.isdisjoint({invariant(p) for p in T})
sq=author['square_control'];assert sq['r']==0 and sq['F_every_direction']==0 and not sq['candidate_domain']
for r in sq['direction_rows']:
    assert r['F']==r['H_pm']==0 and len(r['records'])==16
    for rec in r['records']:assert rec['terminal_type']=='periodic' and rec['length']==48
assert sq['direct_original_endpoint_segment']==[[12,12],[16,18]]
assert all(0<x<24 and 0<y<24 for x,y in sq['direct_original_endpoint_segment'])
after=pins();assert before==after
out=dict(status='PASS_INDEPENDENT_B06_PRESCRIBED_REPLAY',updated_utc=datetime.now(timezone.utc).isoformat(),method='Cyclic-order slicing, independently implemented; raw saved certificate provenance, full records and loads, sign swap and common relabelling.',pinned_sources_before=before,pinned_sources_after=after,raw_certificate_sha256=hashlib.sha256(raw).hexdigest(),prescribed_states_checked=len(rows),author_records_compared=compared_records,author_incidence_rows_compared=compared_loads,rows=rows,square=dict(r=0,F_every_direction=0,three_direction_separation='coordinate invariants y, x, x+y modulo48',period=48,direct_segment=[[12,12],[16,18]]),author_checker_executed=False,new_discovery_or_census=False,whole_goal_complete=False,native_goal_or_budget_changed=False)
(HERE/'global-relational-exchange-independent-replay.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','prescribed_states_checked','author_records_compared','author_incidence_rows_compared']},indent=2))
print(json.dumps([{k:r[k] for k in ['name','F_h','F_v','F_d','D','H_pm']} for r in rows],indent=2))
