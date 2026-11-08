"""Independent fixed CNF binding and DRAT replay; no SAT solving."""
from pathlib import Path
from itertools import product
import importlib.util,sys,subprocess,hashlib,json,shutil
ROOT=Path(__file__).resolve().parent;OWNER=ROOT.parent
PEER=ROOT.parents[1]/'claude-illumination-check/k6-i4'
FROZEN=OWNER/'k5-proof-pilot/inputs'
for n in ['encode.py','illumination_geometry.py']:
    shutil.copyfile(FROZEN/n,ROOT/'inputs'/n)
shutil.copyfile(OWNER/'global-route-review/check.json',ROOT/'inputs/accepted-four-cell-check.json')
sys.path.insert(0,str(ROOT/'inputs'))
spec=importlib.util.spec_from_file_location('bound_encoder',ROOT/'inputs/encode.py')
e=importlib.util.module_from_spec(spec);spec.loader.exec_module(e)
SHAPES={'O':[(0,0),(1,0),(0,1),(1,1)],'T':[(0,1),(1,0),(1,1),(2,1)],'S':[(0,0),(1,0),(1,1),(2,1)]}

def canon(S):
    S=set(S)
    return min(tuple(sorted((x-a,y-b) for x,y in T)) for swap in [False,True]
               for sx,sy in product((-1,1),repeat=2)
               for T in [{(sx*(y if swap else x),sy*(x if swap else y)) for x,y in S}]
               for a,b in T)
old=json.loads((ROOT/'inputs/accepted-four-cell-check.json').read_text())['support']
assert {canon(S) for S in SHAPES.values()}=={canon(map(tuple,S)) for S in old['minimal_boundary_shapes']}
rows=[]
for name,F in SHAPES.items():
    F=set(F);R=F|{(x+dx,y+dy) for x,y in F for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))}
    assert len(R-F)==8
    case={'full':sorted(F),'allowed':sorted(R)}
    cnf,pool,x,ts=e.geometry(case,wmax=21,kmax=6)
    assert len(ts)==96
    generated=ROOT/'inputs'/f'{name}.regenerated.cnf';cnf.to_file(str(generated))
    for suffix in ('cnf','drat'):shutil.copyfile(PEER/f'{name}.{suffix}',ROOT/'inputs'/f'{name}.{suffix}')
    assert generated.read_bytes()==(ROOT/'inputs'/f'{name}.cnf').read_bytes(),'Premise mismatch'
    with (ROOT/f'proof-check-{name}.log').open('w') as log:
        r=subprocess.run([str(OWNER/'bounded-proof/drat-trim'),str(generated),str(ROOT/'inputs'/f'{name}.drat')],stdout=log,stderr=subprocess.STDOUT,timeout=60)
    assert r.returncode==0 and 's VERIFIED' in (ROOT/f'proof-check-{name}.log').read_text()
    rows.append({'shape':name,'full':sorted(F),'mandatory_cells':len(R),'triangle_universe':len(ts),
                 'CNF_binding':'byte-identical regenerated necessary W21/k6 geometry',
                 'DRAT':'VERIFIED','cnf_sha256':hashlib.sha256(generated.read_bytes()).hexdigest(),
                 'proof_sha256':hashlib.sha256((ROOT/'inputs'/f'{name}.drat').read_bytes()).hexdigest()})
out={'status':'PASS','W_cap':21,'k_cap':6,'I':4,'cases':rows,
     'classification':'Three D4 classes from prior independently accepted four-cell equality classification; no fresh classification search.',
     'scope':'Confirms peer I4 impossibility from necessary geometry and checked proof; no threshold/minimum-W controls replayed, no SAT or optical search.'}
(ROOT/'check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
