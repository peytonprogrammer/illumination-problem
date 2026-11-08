"""Project one frozen guard library onto a proved cap alphabet, not room assignments."""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
inc = json.loads((HERE/'guard-incidence-check.json').read_text())
slots = {name:tuple(sorted(map(tuple,t))) for name,t in inc['cap_options'].items()}
slot_name = {t:name for name,t in slots.items()}
lookup = json.loads((ROOT/'cap-return-review/lookup.json').read_text())
core = frozenset(tuple(sorted(map(tuple,t))) for t in lookup['room']) - frozenset(slots[n] for n in ('L+','B+','E-','T-'))
assert len(core)==24
universe = core | frozenset(slots.values())
groups = [frozenset(x) for x in (('L-','L+'),('B-','B+'),('D-','D+'),
          ('R-','R+'),('E-','E+'),('T-','T+'),('Nb-','Nb+','Nr-','Nr+'))]
forbidden_pairs = [frozenset(x) for x in (('L-','B-'),('D+','R-'),('E+','T+'),('T-','Nr+'),('L+','Nb-'))]
forced = frozenset(('B+','E-'))
def transform(p, frame, reflected):
    swap,sx,sy = frame
    a,b = p[::-1] if swap else p
    x,y = sx*a,sy*b
    return (2-y,2-x) if reflected else (x,y)
def transform_triangles(raw, frame, reflected):
    return frozenset(tuple(sorted(transform(v,frame,reflected) for v in t)) for t in raw)
manifest = json.loads((ROOT/'lower-bound-proof-audit/full-replay/manifest.json').read_text())
entries = [entry for entry in manifest['guards'] if entry['path'] in (
    lookup['source'],str(ROOT/'k5-proof-continuation/learned.jsonl'),
    str(ROOT.parent/'claude-illumination-check/k6-run/cases/I2_00_11-pair0/guards.jsonl'))]
assert len(entries)==3
terms = {}
record_count=0
source_receipts=[]
for entry in entries:
 source = Path(entry['path'])
 data = source.read_bytes()
 assert hashlib.sha256(data).hexdigest() == entry['sha256']
 records = data.splitlines()
 record_count+=len(records)
 source_receipts.append(dict(path=str(source),sha256=entry['sha256'],records=len(records)))
 for line,raw in enumerate(records,1):
    rec=json.loads(raw)
    if sum(x*x for x in rec['q']) != 8:
        continue
    frames=[]
    for swap in (False,True):
      for sx,sy in ((1,1),(1,-1),(-1,1),(-1,-1)):
        frame=(swap,sx,sy)
        if transform(rec['q'],frame,False)==(2,2):frames.append(frame)
    assert len(frames)==2
    for frame,reflected in ((f,r) for f in frames for r in (False,True)):
        U,Z = transform_triangles(rec['U'],frame,reflected), transform_triangles(rec['Z'],frame,reflected)
        if not U <= universe or Z & core:
            continue
        required = frozenset(slot_name[t] for t in U-core)
        absent = frozenset(slot_name[t] for t in Z if t in slot_name)
        positive = required | forced
        if any(len(positive & g)>1 for g in groups) or any(p<=positive for p in forbidden_pairs):
            continue
        implied_absent = set()
        for g in groups:
            if g & positive:
                implied_absent.update(g-positive)
        for p in forbidden_pairs:
            if p & positive:
                implied_absent.update(p-positive)
        if absent & positive:
            continue
        required -= forced
        absent -= implied_absent
        key=(required,absent)
        value=dict(source=str(source),source_sha256=entry['sha256'],line=line,frame=frame,
                   reflected=reflected,reflections=len(rec['path'])-2,
                   required=sorted(required),absent=sorted(absent))
        if key not in terms or value['reflections']<terms[key]['reflections']:
            terms[key]=value
keys=sorted(terms,key=lambda k:(len(k[0])+len(k[1]),len(k[0]),sorted(k[0]),sorted(k[1])))
minimal=[]
for key in keys:
    if not any(a<=key[0] and b<=key[1] for a,b in minimal):
        minimal.append(key)
result=dict(sources=source_receipts,source_records=record_count,
            forced_caps=sorted(forced),distinct_projected_terms=len(terms),
            undominated_terms=[terms[k] for k in minimal],
            scope='Saved guard projection and syntactic dominance only. No room/cap-assignment enumeration, ray tracing, solving or uncovered-geometry generation.')
(HERE/'project-guards.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
