"""Exhaustive local cross-check and deliberately invalid certificate checks."""
import copy,itertools,json
from pathlib import Path
from illumination_geometry import *
base=Path(__file__).parent;allts=patch(-2,3,-2,3);cases=0
for p in [(0,0),(1,1),(1,0)]:
    its=[t for t in allts if p in t]
    for mask in range(1<<len(its)):
        ts=[t for j,t in enumerate(its) if mask>>j&1];owners=owners_of(ts);es=[e for e,o in owners.items() if len(o)==2 and p in e]
        for bits in itertools.product((0,1),repeat=len(es)):
            oe={e for e,b in zip(es,bits) if b}
            a,f=local_sectors(ts,p,oe);b,g=check_fan_angles(ts,p,owners,oe)
            assert (sorted(a),f)==(sorted(b),g),(p,mask,bits,a,b,f,g)
            cases+=1
mutations=[];x=json.loads((base/'illumination-20.json').read_text())
for name,mutate in [('removed slit',lambda x:x.update(slits=[])),('boundary target',lambda x:x.update(marked=[(0,0),(1,0)])),('duplicate tile',lambda x:x['triangles'].append(x['triangles'][0])),('false simple claim',lambda x:x.update(require_simple=True))]:
    d=copy.deepcopy(x);mutate(d)
    try:check(d);raise RuntimeError('accepted invalid mutation '+name)
    except AssertionError as e:mutations.append(dict(name=name,rejection=str(e)))
checked=[]
for path in base.glob('illumination-*.json'):
    data=json.loads(path.read_text())
    if 'triangles' in data:
        r=check(data);assert r['certificate'].startswith('PASS');checked.append(dict(file=path.name,walls=r['walls'],simple=r['simple_polygon']))
result=dict(patterns_checked=cases,status='PASS',method='All selected-tile and open-edge combinations at representative A B C vertices; angular slots vs independent tile-fan graph',invalid_mutations_rejected=mutations,certificates_checked=checked)
save(base/'illumination-local-audit.json',result);print(json.dumps(result,indent=2))
