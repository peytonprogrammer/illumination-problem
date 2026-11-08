"""Retrieve the first existing guard matching one prescribed room; no path generation."""
from pathlib import Path
from fractions import Fraction as F
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CENTERS = ((0, 0), (2, 0), (2, 2))
CAPS = (((0,-2),(0,-1),(1,-1)), ((4,2),(3,2),(3,1)),
        ((2,4),(2,3),(1,3)), ((-2,0),(-1,0),(-1,1)))
room = set(tuple(sorted(t)) for t in CAPS)
for x,y in CENTERS:
    a = (x,y)
    sides = (((-1,-1),(0,-1),(1,-1)), ((1,-1),(1,0),(1,1)),
             ((1,1),(0,1),(-1,1)), ((-1,1),(-1,0),(-1,-1)))
    for p,c,q in sides:
        for b,d in ((p,c),(c,q)):
            room.add(tuple(sorted((a,(x+b[0],y+b[1]),(x+d[0],y+d[1])))))
assert len(room) == 28
def transform(p, swap, sx, sy):
    x,y = p[::-1] if swap else p
    return sx*x, sy*y
def triangles(raw):
    return frozenset(tuple(sorted(map(tuple,t))) for t in raw)
manifest = json.loads((ROOT/'lower-bound-proof-audit/full-replay/manifest.json').read_text())
files = [e for e in manifest['guards'] if e['index'] == 0 or 'I3_' in e['path']]
checked = 0
for entry in files:
    p = Path(entry['path'])
    data = p.read_bytes()
    assert hashlib.sha256(data).hexdigest() == entry['sha256']
    for index,line in enumerate(data.splitlines()):
        rec = json.loads(line)
        q = tuple(rec['q'])
        if sum(x*x for x in q) != 8:
            continue
        U,Z = triangles(rec['U']),triangles(rec['Z'])
        for origin, end in (((0,0),(2,2)), ((2,2),(0,0))):
            for swap in (False,True):
                for sx,sy in ((1,1),(1,-1),(-1,1),(-1,-1)):
                    if transform(q,swap,sx,sy) != (end[0]-origin[0],end[1]-origin[1]):
                        continue
                    checked += 1
                    def physical(v):
                        x,y = transform(v,swap,sx,sy)
                        return x+origin[0],y+origin[1]
                    u = frozenset(tuple(sorted(physical(v) for v in t)) for t in U)
                    if not u <= room:
                        continue
                    z = frozenset(tuple(sorted(physical(v) for v in t)) for t in Z)
                    if z & room:
                        continue
                    path = [physical(tuple(F(*v) for v in point)) for point in rec['path']]
                    if origin != (0,0):
                        path.reverse()
                    result = dict(status='MATCH', source=str(p), source_sha256=entry['sha256'],
                                  line=index+1, guard_transform=dict(swap=swap,sx=sx,sy=sy,origin=origin),
                                  checked_guard_images=checked, room=sorted(room), U=sorted(u),Z=sorted(z),
                                  path=[[[v.numerator,v.denominator] for v in point] for point in path],
                                  reflections=len(path)-2,
                                  scope='First matching previously saved certificate; no path or direction generation.')
                    (HERE/'lookup.json').write_text(json.dumps(result,indent=2)+'\n')
                    print(json.dumps({k:v for k,v in result.items() if k not in ('room','U','Z','path')},indent=2))
                    raise SystemExit(0)
result = dict(status='NO_MATCH',checked_guard_images=checked,scope='Only named saved learned/I3 guard files checked.')
(HERE/'lookup.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
